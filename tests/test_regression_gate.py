from __future__ import annotations

import pytest

from agent_runtime_ref.regression import RateObservation, assess_regression_gate


def test_small_regression_sample_is_inconclusive() -> None:
    result = assess_regression_gate(
        baseline=RateObservation(failures=0, total=20),
        current=RateObservation(failures=0, total=20),
        max_rate_increase=0.01,
        min_samples=100,
    )

    assert result.decision == "INCONCLUSIVE"
    assert result.reason == "insufficient_samples"


def test_any_confirmed_critical_violation_fails_regression_gate() -> None:
    result = assess_regression_gate(
        baseline=RateObservation(failures=0, total=1000),
        current=RateObservation(failures=1, total=1000, critical_failures=1),
        max_rate_increase=0.01,
        min_samples=100,
    )

    assert result.decision == "FAIL"
    assert result.reason == "critical_violation"


def test_statistically_supported_rate_regression_fails() -> None:
    result = assess_regression_gate(
        baseline=RateObservation(failures=5, total=1000),
        current=RateObservation(failures=80, total=1000),
        max_rate_increase=0.02,
        min_samples=100,
    )

    assert result.decision == "FAIL"
    assert result.reason == "rate_regression"
    assert result.upper_rate_delta > 0.02


def test_supported_non_regression_passes() -> None:
    result = assess_regression_gate(
        baseline=RateObservation(failures=2, total=1000),
        current=RateObservation(failures=3, total=1000),
        max_rate_increase=0.01,
        min_samples=100,
    )

    assert result.decision == "PASS"
    assert result.reason == "within_regression_budget"


def test_zero_observed_failures_does_not_collapse_uncertainty() -> None:
    result = assess_regression_gate(
        baseline=RateObservation(failures=0, total=100),
        current=RateObservation(failures=0, total=100),
        max_rate_increase=0.01,
        min_samples=100,
    )

    assert result.decision == "INCONCLUSIVE"
    assert result.reason == "insufficient_statistical_support"
    assert result.upper_rate_delta > 0.01


@pytest.mark.parametrize(
    ("failures", "total"),
    [(-1, 100), (101, 100), (0, 0), (True, 100)],
)
def test_rate_observation_rejects_invalid_counts(failures: int, total: int) -> None:
    with pytest.raises((TypeError, ValueError)):
        RateObservation(failures=failures, total=total)
