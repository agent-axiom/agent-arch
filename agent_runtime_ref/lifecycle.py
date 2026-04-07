from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _require_mapping(payload: object, *, label: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TypeError(f"{label} config must be a mapping")
    return {str(key): value for key, value in payload.items()}


def _read_string_list(data: dict[str, Any], key: str) -> tuple[str, ...]:
    value = data.get(key, [])
    if not isinstance(value, list):
        raise TypeError(f"{key} must be a list")
    return tuple(str(item) for item in value)


@dataclass(frozen=True, slots=True)
class ChangeRecord:
    change_id: str
    change_type: str
    risk_level: str
    rollout_strategy: str
    artifacts: tuple[str, ...]
    required_signals: tuple[str, ...]
    approval_roles: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> ChangeRecord:
        data = _require_mapping(payload.get("change", payload), label="change")
        return cls(
            change_id=str(data["change_id"]),
            change_type=str(data["change_type"]),
            risk_level=str(data["risk_level"]),
            rollout_strategy=str(data["rollout_strategy"]),
            artifacts=_read_string_list(data, "artifacts"),
            required_signals=_read_string_list(data, "required_signals"),
            approval_roles=_read_string_list(data, "approval_roles"),
        )


@dataclass(frozen=True, slots=True)
class ArtifactBundle:
    bundle_name: str
    version: str
    provenance_required: bool
    signed: bool
    artifacts: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> ArtifactBundle:
        data = _require_mapping(payload.get("bundle", payload), label="artifact bundle")
        return cls(
            bundle_name=str(data["bundle_name"]),
            version=str(data["version"]),
            provenance_required=bool(data.get("provenance_required", True)),
            signed=bool(data.get("signed", False)),
            artifacts=_read_string_list(data, "artifacts"),
        )


@dataclass(frozen=True, slots=True)
class RetirementPlan:
    system_id: str
    replacement_mode: str
    triggers: tuple[str, ...]
    required_steps: tuple[str, ...]
    archive_targets: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> RetirementPlan:
        data = _require_mapping(payload.get("retirement", payload), label="retirement")
        return cls(
            system_id=str(data["system_id"]),
            replacement_mode=str(data["replacement_mode"]),
            triggers=_read_string_list(data, "triggers"),
            required_steps=_read_string_list(data, "required_steps"),
            archive_targets=_read_string_list(data, "archive_targets"),
        )


@dataclass(frozen=True, slots=True)
class ChangeGateAssessment:
    ready: bool
    missing_signals: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RetirementAssessment:
    ready: bool
    missing_steps: tuple[str, ...]


def assess_change_gate(
    change: ChangeRecord,
    observed_signals: dict[str, bool],
) -> ChangeGateAssessment:
    missing = tuple(
        signal for signal in change.required_signals if not observed_signals.get(signal, False)
    )
    return ChangeGateAssessment(ready=not missing, missing_signals=missing)


def assess_retirement(
    plan: RetirementPlan,
    observed_steps: dict[str, bool],
) -> RetirementAssessment:
    missing = tuple(
        step for step in plan.required_steps if not observed_steps.get(step, False)
    )
    return RetirementAssessment(ready=not missing, missing_steps=missing)
