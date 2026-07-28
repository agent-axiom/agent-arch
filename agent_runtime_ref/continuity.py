from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime

_SCHEMA_VERSION = "continuity-envelope/v1"
_AUTHORIZATION_MODES = {"platform_owned", "user_delegated", "human_approved"}
_SIDE_EFFECT_STATUSES = {
    "not_started",
    "side_effect_committed",
    "side_effect_unknown",
}
_APPROVAL_STATUSES = {"approved", "pending", "rejected", "revoked", "expired"}


def _required_string(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Continuity field must be a string: {field}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"Continuity field is required: {field}")
    return normalized


def _optional_string(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Continuity field must be a string: {field}")
    return value.strip()


def _parse_timestamp(value: str, *, field: str) -> datetime:
    normalized = _required_string(value, field=field)
    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"Continuity timestamp is invalid: {field}") from error
    if parsed.tzinfo is None:
        raise ValueError(f"Continuity timestamp must include a timezone: {field}")
    return parsed.astimezone(UTC)


def summary_sha256(summary: str) -> str:
    """Return the stable digest used to bind a derived summary to an envelope."""
    normalized = _required_string(summary, field="summary")
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


@dataclass(frozen=True, slots=True)
class ContinuityEnvelope:
    schema_version: str
    envelope_id: str
    session_id: str
    source_trace_id: str
    tenant_id: str
    principal_id: str
    authorization_mode: str
    delegated_principal_id: str
    delegated_scope: str
    policy_version: str
    capability_name: str
    capability_version: str
    approval_id: str
    action_digest: str
    approval_expires_at: str
    idempotency_key: str
    side_effect_status: str
    checkpoint_ref: str
    summary_sha256: str
    requires_reauthorization: bool = True

    def __post_init__(self) -> None:
        required_fields = (
            "schema_version",
            "envelope_id",
            "session_id",
            "source_trace_id",
            "tenant_id",
            "principal_id",
            "authorization_mode",
            "policy_version",
            "capability_name",
            "capability_version",
            "approval_id",
            "action_digest",
            "approval_expires_at",
            "idempotency_key",
            "side_effect_status",
            "checkpoint_ref",
            "summary_sha256",
        )
        for field in required_fields:
            object.__setattr__(
                self,
                field,
                _required_string(getattr(self, field), field=field),
            )
        for field in ("delegated_principal_id", "delegated_scope"):
            object.__setattr__(
                self,
                field,
                _optional_string(getattr(self, field), field=field),
            )

        if self.schema_version != _SCHEMA_VERSION:
            raise ValueError(f"Continuity schema version is not supported: {self.schema_version}")
        if self.authorization_mode not in _AUTHORIZATION_MODES:
            raise ValueError(
                f"Continuity authorization mode is not supported: {self.authorization_mode}"
            )
        if self.authorization_mode == "user_delegated":
            if not self.delegated_principal_id:
                raise ValueError("Continuity field is required: delegated_principal_id")
            if not self.delegated_scope:
                raise ValueError("Continuity field is required: delegated_scope")
        if self.side_effect_status not in _SIDE_EFFECT_STATUSES:
            raise ValueError(
                f"Continuity side-effect status is not supported: {self.side_effect_status}"
            )
        _parse_timestamp(self.approval_expires_at, field="approval_expires_at")
        if not self.summary_sha256.startswith("sha256:"):
            raise ValueError("Continuity summary digest must use sha256")
        if not isinstance(self.requires_reauthorization, bool):
            raise TypeError("Continuity reauthorization flag must be a boolean")
        if not self.requires_reauthorization:
            raise ValueError("Continuity envelope must require reauthorization")


@dataclass(frozen=True, slots=True)
class ContinuityState:
    tenant_id: str
    principal_id: str
    authorization_mode: str
    delegated_principal_id: str
    delegated_scope: str
    policy_version: str
    capability_name: str
    capability_version: str
    approval_id: str
    action_digest: str
    approval_status: str
    idempotency_key: str
    side_effect_status: str
    checkpoint_ref: str

    def __post_init__(self) -> None:
        required_fields = (
            "tenant_id",
            "principal_id",
            "authorization_mode",
            "policy_version",
            "capability_name",
            "capability_version",
            "approval_id",
            "action_digest",
            "approval_status",
            "idempotency_key",
            "side_effect_status",
            "checkpoint_ref",
        )
        for field in required_fields:
            object.__setattr__(
                self,
                field,
                _required_string(getattr(self, field), field=field),
            )
        for field in ("delegated_principal_id", "delegated_scope"):
            object.__setattr__(
                self,
                field,
                _optional_string(getattr(self, field), field=field),
            )
        if self.authorization_mode not in _AUTHORIZATION_MODES:
            raise ValueError(
                f"Continuity authorization mode is not supported: {self.authorization_mode}"
            )
        if self.approval_status not in _APPROVAL_STATUSES:
            raise ValueError(f"Continuity approval status is not supported: {self.approval_status}")
        if self.side_effect_status not in _SIDE_EFFECT_STATUSES:
            raise ValueError(
                f"Continuity side-effect status is not supported: {self.side_effect_status}"
            )


@dataclass(frozen=True, slots=True)
class ContinuityDecision:
    status: str
    authorized: bool
    requires_reauthorization: bool
    reason: str


def _decision(status: str, reason: str) -> ContinuityDecision:
    return ContinuityDecision(
        status=status,
        authorized=False,
        requires_reauthorization=True,
        reason=reason,
    )


def validate_rehydration(
    envelope: ContinuityEnvelope,
    current: ContinuityState,
    summary: str,
    *,
    now: datetime | None = None,
) -> ContinuityDecision:
    """Validate continuity without granting authority to the reconstructed view."""
    if not isinstance(envelope, ContinuityEnvelope):
        raise TypeError("Continuity envelope must be ContinuityEnvelope")
    if not isinstance(current, ContinuityState):
        raise TypeError("Continuity state must be ContinuityState")
    if now is None:
        now = datetime.now(UTC)
    if not isinstance(now, datetime):
        raise TypeError("Continuity validation time must be a datetime")
    if now.tzinfo is None:
        raise ValueError("Continuity validation time must include a timezone")
    now = now.astimezone(UTC)

    if summary_sha256(summary) != envelope.summary_sha256:
        return _decision("continuity_validation_failed", "summary_digest_mismatch")

    comparisons = (
        ("tenant_id", "tenant_mismatch"),
        ("principal_id", "principal_mismatch"),
        ("authorization_mode", "authorization_mode_changed"),
        ("delegated_principal_id", "delegated_principal_changed"),
        ("delegated_scope", "delegated_scope_changed"),
        ("policy_version", "policy_version_changed"),
        ("capability_name", "capability_changed"),
        ("capability_version", "capability_version_changed"),
        ("approval_id", "approval_binding_changed"),
        ("action_digest", "action_digest_changed"),
        ("idempotency_key", "idempotency_key_changed"),
        ("side_effect_status", "side_effect_status_changed"),
        ("checkpoint_ref", "checkpoint_changed"),
    )
    for field, reason in comparisons:
        if getattr(envelope, field) != getattr(current, field):
            return _decision("continuity_validation_failed", reason)

    if current.approval_status != "approved":
        reason = (
            "approval_revoked" if current.approval_status == "revoked" else "approval_not_active"
        )
        return _decision("continuity_validation_failed", reason)
    expires_at = _parse_timestamp(
        envelope.approval_expires_at,
        field="approval_expires_at",
    )
    if expires_at <= now:
        return _decision("continuity_validation_failed", "approval_expired")
    if current.side_effect_status == "side_effect_unknown":
        return _decision("blocked_on_reconciliation", "unknown_side_effect")

    return _decision("reauthorization_required", "continuity_validated")
