from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


def _read_string_list_items(items: list[object], *, label: str) -> tuple[str, ...]:
    values = tuple(str(item).strip() for item in items)
    if any(not value for value in values):
        raise ValueError(f"{label} entries must not be empty")
    if len(set(values)) != len(values):
        raise ValueError(f"{label} entries must be unique")
    return values


def _read_string_mapping_items(items: Mapping[str, object], *, label: str) -> dict[str, str]:
    values = {str(key).strip(): str(value).strip() for key, value in items.items()}
    if any(not key or not value for key, value in values.items()):
        raise ValueError(f"{label} entries must not be empty")
    return values


def _read_observed_flags(items: Mapping[str, bool]) -> dict[str, bool]:
    observed: dict[str, bool] = {}
    for key, value in items.items():
        field = str(key).strip()
        if not isinstance(value, bool):
            raise TypeError(f"Assessment signal value must be a boolean: {field}")
        observed[field] = value
    return observed


@dataclass(slots=True)
class RolloutReadiness:
    trace_coverage: bool
    offline_eval_pass: bool
    slo_defined: bool
    rollback_plan: bool


def _read_readiness_flag(value: bool, *, field: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"Rollout readiness flag must be a boolean: {field}")
    return value


def ready_for_rollout(state: RolloutReadiness) -> bool:
    return (
        _read_readiness_flag(state.trace_coverage, field="trace_coverage")
        and _read_readiness_flag(state.offline_eval_pass, field="offline_eval_pass")
        and _read_readiness_flag(state.slo_defined, field="slo_defined")
        and _read_readiness_flag(state.rollback_plan, field="rollback_plan")
    )


@dataclass(frozen=True, slots=True)
class RolloutPolicy:
    required_checks: tuple[str, ...]
    blocked_checks: tuple[str, ...]
    rollout_mode: dict[str, str]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "required_checks",
            _read_string_list_items(
                list(self.required_checks),
                label="rollout.require",
            ),
        )
        object.__setattr__(
            self,
            "blocked_checks",
            _read_string_list_items(
                list(self.blocked_checks),
                label="rollout.block_if",
            ),
        )
        object.__setattr__(
            self,
            "rollout_mode",
            _read_string_mapping_items(
                self.rollout_mode,
                label="rollout.rollout_mode",
            ),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RolloutPolicy":
        raw_rollout = data.get("rollout", {})
        if not isinstance(raw_rollout, Mapping):
            raise TypeError("'rollout' must be a mapping")
        require = raw_rollout.get("require", [])
        block_if = raw_rollout.get("block_if", [])
        rollout_mode = raw_rollout.get("rollout_mode", {})
        if not isinstance(require, list):
            raise TypeError("'require' must be a list")
        if not isinstance(block_if, list):
            raise TypeError("'block_if' must be a list")
        if not isinstance(rollout_mode, Mapping):
            raise TypeError("'rollout_mode' must be a mapping")
        return cls(
            required_checks=_read_string_list_items(require, label="rollout.require"),
            blocked_checks=_read_string_list_items(block_if, label="rollout.block_if"),
            rollout_mode=_read_string_mapping_items(rollout_mode, label="rollout.rollout_mode"),
        )


@dataclass(frozen=True, slots=True)
class RolloutAssessment:
    ready: bool
    missing_required: tuple[str, ...]
    blocking_signals: tuple[str, ...]


def assess_rollout(policy: RolloutPolicy, observed_checks: Mapping[str, bool]) -> RolloutAssessment:
    observed = _read_observed_flags(observed_checks)
    missing_required = tuple(
        check for check in policy.required_checks if not observed.get(check, False)
    )
    blocking_signals = tuple(
        check for check in policy.blocked_checks if observed.get(check, False)
    )
    return RolloutAssessment(
        ready=not missing_required and not blocking_signals,
        missing_required=missing_required,
        blocking_signals=blocking_signals,
    )
