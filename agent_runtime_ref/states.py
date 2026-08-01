from __future__ import annotations

POLICY_DECISIONS = frozenset({"allow", "deny", "approval_required"})
RUN_STATUSES = frozenset(
    {
        "success",
        "waiting_for_approval",
        "denied",
        "failed",
        "blocked_on_reconciliation",
    }
)
CAPABILITY_OUTCOMES = frozenset(
    {
        "success",
        "approval_required",
        "permission_denied",
        "validation_failure",
        "retryable_failure",
        "side_effect_unknown",
        "partial_side_effect",
    }
)
SIDE_EFFECT_STATUSES = frozenset(
    {
        "not_executed",
        "applied",
        "side_effect_unknown",
        "partial_side_effect",
    }
)


def validate_policy_decision(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Policy decision must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError("Policy decision must not be empty")
    if normalized not in POLICY_DECISIONS:
        raise ValueError(f"Policy decision is not supported: {normalized}")
    return normalized


def validate_run_status(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Run status must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError("Run status must not be empty")
    if normalized not in RUN_STATUSES:
        raise ValueError(f"Run status is not supported: {normalized}")
    return normalized


def validate_capability_outcome(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Capability outcome must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError("Capability outcome must not be empty")
    if normalized not in CAPABILITY_OUTCOMES:
        raise ValueError(f"Capability outcome is not supported: {normalized}")
    return normalized


def validate_side_effect_status(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Side-effect status must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError("Side-effect status must not be empty")
    if normalized not in SIDE_EFFECT_STATUSES:
        raise ValueError(f"Side-effect status is not supported: {normalized}")
    return normalized
