from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _require_mapping(payload: object, *, label: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TypeError(f"{label} config must be a mapping")
    return {str(key): value for key, value in payload.items()}


def _read_required_string(data: dict[str, Any], key: str, *, label: str) -> str:
    value = str(data.get(key, "")).strip()
    if not value:
        raise ValueError(f"{label}.{key} is required")
    return value


def _read_string_list(data: dict[str, Any], key: str) -> tuple[str, ...]:
    value = data.get(key, [])
    if not isinstance(value, list):
        raise TypeError(f"{key} must be a list")
    values = tuple(str(item).strip() for item in value)
    if any(not item for item in values):
        raise ValueError(f"{key} entries must not be empty")
    if len(set(values)) != len(values):
        raise ValueError(f"{key} entries must be unique")
    return values


def _read_bool(data: dict[str, Any], key: str, *, label: str, default: bool) -> bool:
    value = data.get(key, default)
    if not isinstance(value, bool):
        raise TypeError(f"'{label}.{key}' must be a boolean")
    return value


def _read_observed_flags(items: dict[str, bool]) -> dict[str, bool]:
    observed: dict[str, bool] = {}
    for key, value in items.items():
        field = str(key).strip()
        if not isinstance(value, bool):
            raise TypeError(f"Assessment signal value must be a boolean: {field}")
        observed[field] = value
    return observed


@dataclass(frozen=True, slots=True)
class ChangeRecord:
    change_id: str
    change_type: str
    risk_level: str
    rollout_strategy: str
    artifacts: tuple[str, ...]
    affected_surfaces: tuple[str, ...]
    required_signals: tuple[str, ...]
    approval_roles: tuple[str, ...]
    session_control_owner: str
    emergency_freeze_owner: str

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> ChangeRecord:
        data = _require_mapping(payload.get("change", payload), label="change")
        return cls(
            change_id=_read_required_string(data, "change_id", label="change"),
            change_type=_read_required_string(data, "change_type", label="change"),
            risk_level=_read_required_string(data, "risk_level", label="change"),
            rollout_strategy=_read_required_string(
                data, "rollout_strategy", label="change"
            ),
            artifacts=_read_string_list(data, "artifacts"),
            affected_surfaces=_read_string_list(data, "affected_surfaces"),
            required_signals=_read_string_list(data, "required_signals"),
            approval_roles=_read_string_list(data, "approval_roles"),
            session_control_owner=_read_required_string(
                data, "session_control_owner", label="change"
            ),
            emergency_freeze_owner=_read_required_string(
                data, "emergency_freeze_owner", label="change"
            ),
        )


@dataclass(frozen=True, slots=True)
class ArtifactBundle:
    bundle_name: str
    version: str
    provenance_required: bool
    signed: bool
    session_control_owner: str
    artifacts: tuple[str, ...]
    review_evidence: dict[str, object]

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> ArtifactBundle:
        data = _require_mapping(payload.get("bundle", payload), label="artifact bundle")
        return cls(
            bundle_name=_read_required_string(data, "bundle_name", label="bundle"),
            version=_read_required_string(data, "version", label="bundle"),
            provenance_required=_read_bool(
                data, "provenance_required", label="bundle", default=True
            ),
            signed=_read_bool(data, "signed", label="bundle", default=False),
            session_control_owner=_read_required_string(
                data, "session_control_owner", label="bundle"
            ),
            artifacts=_read_string_list(data, "artifacts"),
            review_evidence=_require_mapping(
                data.get("review_evidence", {}),
                label="artifact bundle review_evidence",
            ),
        )


@dataclass(frozen=True, slots=True)
class RetirementPlan:
    system_id: str
    replacement_mode: str
    triggers: tuple[str, ...]
    required_steps: tuple[str, ...]
    session_control_owner: str
    emergency_freeze_owner: str
    archive_targets: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> RetirementPlan:
        data = _require_mapping(payload.get("retirement", payload), label="retirement")
        return cls(
            system_id=_read_required_string(data, "system_id", label="retirement"),
            replacement_mode=_read_required_string(
                data, "replacement_mode", label="retirement"
            ),
            triggers=_read_string_list(data, "triggers"),
            required_steps=_read_string_list(data, "required_steps"),
            session_control_owner=_read_required_string(
                data, "session_control_owner", label="retirement"
            ),
            emergency_freeze_owner=_read_required_string(
                data, "emergency_freeze_owner", label="retirement"
            ),
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
    observed = _read_observed_flags(observed_signals)
    missing = tuple(
        signal for signal in change.required_signals if not observed.get(signal, False)
    )
    return ChangeGateAssessment(ready=not missing, missing_signals=missing)


def assess_retirement(
    plan: RetirementPlan,
    observed_steps: dict[str, bool],
) -> RetirementAssessment:
    observed = _read_observed_flags(observed_steps)
    missing = tuple(
        step for step in plan.required_steps if not observed.get(step, False)
    )
    return RetirementAssessment(ready=not missing, missing_steps=missing)
