from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


def _read_count(value: int, *, field: str, positive: bool = False) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"Regression count must be an integer: {field}")
    minimum = 1 if positive else 0
    if value < minimum:
        requirement = "positive" if positive else "non-negative"
        raise ValueError(f"Regression count must be {requirement}: {field}")
    return value


def _read_probability(value: float, *, field: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"Regression threshold must be a number: {field}")
    normalized = float(value)
    if not isfinite(normalized) or normalized < 0 or normalized > 1:
        raise ValueError(f"Regression threshold must be between 0 and 1: {field}")
    return normalized


def _read_positive_float(value: float, *, field: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"Regression parameter must be a number: {field}")
    normalized = float(value)
    if not isfinite(normalized) or normalized <= 0:
        raise ValueError(f"Regression parameter must be positive: {field}")
    return normalized


@dataclass(frozen=True, slots=True)
class RateObservation:
    failures: int
    total: int
    critical_failures: int = 0

    def __post_init__(self) -> None:
        failures = _read_count(self.failures, field="failures")
        total = _read_count(self.total, field="total", positive=True)
        critical_failures = _read_count(
            self.critical_failures,
            field="critical_failures",
        )
        if failures > total:
            raise ValueError("Regression failures cannot exceed total")
        if critical_failures > failures:
            raise ValueError("Regression critical_failures cannot exceed failures")

    @property
    def rate(self) -> float:
        return self.failures / self.total


@dataclass(frozen=True, slots=True)
class RegressionGateResult:
    decision: str
    reason: str
    baseline_rate: float
    current_rate: float
    upper_rate_delta: float
    min_samples: int


def _wilson_interval(
    observation: RateObservation,
    *,
    z_value: float,
) -> tuple[float, float]:
    rate = observation.rate
    total = observation.total
    z_squared = z_value**2
    denominator = 1 + z_squared / total
    center = (rate + z_squared / (2 * total)) / denominator
    half_width = (
        z_value
        * sqrt(rate * (1 - rate) / total + z_squared / (4 * total**2))
        / denominator
    )
    return max(0.0, center - half_width), min(1.0, center + half_width)


def assess_regression_gate(
    *,
    baseline: RateObservation,
    current: RateObservation,
    max_rate_increase: float,
    min_samples: int,
    confidence_z: float = 1.96,
) -> RegressionGateResult:
    if not isinstance(baseline, RateObservation):
        raise TypeError("Regression baseline must be RateObservation")
    if not isinstance(current, RateObservation):
        raise TypeError("Regression current must be RateObservation")
    max_increase = _read_probability(max_rate_increase, field="max_rate_increase")
    minimum = _read_count(min_samples, field="min_samples", positive=True)
    z_value = _read_positive_float(confidence_z, field="confidence_z")

    baseline_rate = baseline.rate
    current_rate = current.rate
    baseline_lower, baseline_upper = _wilson_interval(
        baseline,
        z_value=z_value,
    )
    current_lower, current_upper = _wilson_interval(
        current,
        z_value=z_value,
    )
    lower_delta = current_lower - baseline_upper
    upper_delta = current_upper - baseline_lower

    if baseline.total < minimum or current.total < minimum:
        return RegressionGateResult(
            decision="INCONCLUSIVE",
            reason="insufficient_samples",
            baseline_rate=baseline_rate,
            current_rate=current_rate,
            upper_rate_delta=upper_delta,
            min_samples=minimum,
        )
    if current.critical_failures:
        return RegressionGateResult(
            decision="FAIL",
            reason="critical_violation",
            baseline_rate=baseline_rate,
            current_rate=current_rate,
            upper_rate_delta=upper_delta,
            min_samples=minimum,
        )
    if lower_delta > max_increase:
        return RegressionGateResult(
            decision="FAIL",
            reason="rate_regression",
            baseline_rate=baseline_rate,
            current_rate=current_rate,
            upper_rate_delta=upper_delta,
            min_samples=minimum,
        )
    if upper_delta > max_increase:
        return RegressionGateResult(
            decision="INCONCLUSIVE",
            reason="insufficient_statistical_support",
            baseline_rate=baseline_rate,
            current_rate=current_rate,
            upper_rate_delta=upper_delta,
            min_samples=minimum,
        )
    return RegressionGateResult(
        decision="PASS",
        reason="within_regression_budget",
        baseline_rate=baseline_rate,
        current_rate=current_rate,
        upper_rate_delta=upper_delta,
        min_samples=minimum,
    )
