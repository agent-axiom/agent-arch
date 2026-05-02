from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


def _read_string_list_items(items: list[object], *, label: str) -> tuple[str, ...]:
    values = tuple(str(item).strip() for item in items)
    if any(not value for value in values):
        raise ValueError(f"{label} entries must not be empty")
    return values


@dataclass(slots=True)
class RolloutReadiness:
    trace_coverage: bool
    offline_eval_pass: bool
    slo_defined: bool
    rollback_plan: bool


def ready_for_rollout(state: RolloutReadiness) -> bool:
    return (
        state.trace_coverage
        and state.offline_eval_pass
        and state.slo_defined
        and state.rollback_plan
    )


@dataclass(frozen=True, slots=True)
class RolloutPolicy:
    required_checks: tuple[str, ...]
    blocked_checks: tuple[str, ...]
    rollout_mode: dict[str, str]

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
            rollout_mode={str(key): str(value) for key, value in rollout_mode.items()},
        )


@dataclass(frozen=True, slots=True)
class RolloutAssessment:
    ready: bool
    missing_required: tuple[str, ...]
    blocking_signals: tuple[str, ...]


def assess_rollout(policy: RolloutPolicy, observed_checks: Mapping[str, bool]) -> RolloutAssessment:
    missing_required = tuple(
        check for check in policy.required_checks if not observed_checks.get(check, False)
    )
    blocking_signals = tuple(
        check for check in policy.blocked_checks if observed_checks.get(check, False)
    )
    return RolloutAssessment(
        ready=not missing_required and not blocking_signals,
        missing_required=missing_required,
        blocking_signals=blocking_signals,
    )
