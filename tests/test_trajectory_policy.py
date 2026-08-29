from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import FrozenInstanceError, replace
from decimal import Decimal, getcontext, setcontext

import pytest

from agent_runtime_ref.telemetry import TelemetryEmitter
from agent_runtime_ref.trajectory import (
    ApprovalRecord,
    CumulativeLimitRule,
    Fingerprint,
    RequiredApprovalRule,
    RequiredPredecessorRule,
    TrajectoryCounter,
    TrajectoryPolicy,
    TrajectoryRequest,
    TrajectorySnapshot,
    ValueBindingRule,
    compute_trajectory_request_fingerprint,
    evaluate_trajectory_policy,
)


def _fingerprint(raw_value: str) -> str:
    return f"sha256:{hashlib.sha256(raw_value.encode('utf-8')).hexdigest()}"


DESTINATION_A = _fingerprint("account-a")
DESTINATION_B = _fingerprint("account-b")


def _policy(
    *rules: object,
    policy_id: str = "transfer-trajectory",
    policy_version: str = "2026.08.23",
) -> TrajectoryPolicy:
    return TrajectoryPolicy(
        policy_id=policy_id,
        policy_version=policy_version,
        rules=rules,  # type: ignore[arg-type]
    )


def _request(**overrides: object) -> TrajectoryRequest:
    values: dict[str, object] = {
        "action": "submit_transfer",
        "tenant_id": "tenant-acme",
        "subject_id": "subject-42",
        "expected_history_ref": "trajectory://transfer/001",
        "expected_history_version": 7,
        "sequence_number": 3,
        "fingerprints": (Fingerprint("destination", DESTINATION_A),),
        "counters": (TrajectoryCounter("amount", Decimal("20")),),
        "window_id": "daily-2026-08-23",
    }
    values.update(overrides)
    return TrajectoryRequest(**values)  # type: ignore[arg-type]


def _approval_record(
    approval_id: str,
    *,
    request: TrajectoryRequest | None = None,
    policy: TrajectoryPolicy | None = None,
    scope: str = "transfer",
    state: str = "approved",
) -> ApprovalRecord:
    bound_request = request or _request()
    bound_policy = policy or _policy(RequiredApprovalRule("transfer-approval", "transfer"))
    return ApprovalRecord(
        approval_id=approval_id,
        scope=scope,
        request_fingerprint=compute_trajectory_request_fingerprint(
            bound_request,
            bound_policy,
        ),
        state=state,
    )


def _snapshot(
    *,
    request: TrajectoryRequest | None = None,
    policy: TrajectoryPolicy | None = None,
    **overrides: object,
) -> TrajectorySnapshot:
    bound_request = request or _request()
    bound_policy = policy or _policy(RequiredApprovalRule("transfer-approval", "transfer"))
    values: dict[str, object] = {
        "history_ref": bound_request.expected_history_ref,
        "history_version": bound_request.expected_history_version,
        "tenant_id": bound_request.tenant_id,
        "subject_id": bound_request.subject_id,
        "policy_id": bound_policy.policy_id,
        "policy_version": bound_policy.policy_version,
        "integrity": "verified",
        "status": "current",
        "observed_sequence": ("read_destination", "confirm_destination"),
        "fingerprints": (Fingerprint("destination", DESTINATION_A),),
        "counters": (TrajectoryCounter("amount", Decimal("40")),),
        "window_id": "daily-2026-08-23",
        "window_state": "open",
        "approval_records": (
            _approval_record(
                "approval-001",
                request=bound_request,
                policy=bound_policy,
            ),
        ),
        "approval_state": "approved",
    }
    values.update(overrides)
    return TrajectorySnapshot(**values)  # type: ignore[arg-type]


def test_evaluator_rejects_wrong_public_input_types() -> None:
    policy = _policy(ValueBindingRule("destination-binding", "destination"))

    with pytest.raises(TypeError, match="Trajectory request must be TrajectoryRequest"):
        evaluate_trajectory_policy(object(), None, policy)
    with pytest.raises(TypeError, match="Trajectory policy must be TrajectoryPolicy"):
        evaluate_trajectory_policy(_request(), None, object())


def test_destination_fingerprint_mismatch_is_denied_without_raw_values() -> None:
    raw_destination = "account-b"
    request = _request(
        fingerprints=(Fingerprint("destination", _fingerprint(raw_destination)),),
    )

    decision = evaluate_trajectory_policy(
        request,
        _snapshot(),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "destination-binding"
    assert decision.reason == "value_binding_mismatch"
    assert decision.history_ref == "trajectory://transfer/001"
    assert decision.history_version == 7
    assert decision.sequence_summary == "observed=2;current=3"
    assert decision.sequence_ref == "trajectory://transfer/001#observed_sequence"
    assert DESTINATION_A in decision.fingerprints
    assert DESTINATION_B in decision.fingerprints

    payload = decision.to_event_payload()
    assert set(payload) == {
        "policy_id",
        "policy_version",
        "rule_id",
        "reason",
        "history_ref",
        "history_version",
        "sequence_summary",
        "sequence_ref",
        "fingerprints",
        "counters",
        "window_id",
        "window_state",
        "approval_state",
        "decision",
    }
    assert all(isinstance(value, str) for value in payload.values())
    assert raw_destination not in repr(payload)

    emitter = TelemetryEmitter()
    emitter.emit("trajectory_policy_decision", "trace-trajectory-001", **payload)
    assert emitter.events[0].payload == payload


def test_accumulated_amount_over_limit_is_denied_when_current_amount_is_below_limit() -> None:
    decision = evaluate_trajectory_policy(
        _request(counters=(TrajectoryCounter("amount", Decimal("40")),)),
        _snapshot(counters=(TrajectoryCounter("amount", Decimal("70")),)),
        _policy(
            CumulativeLimitRule(
                rule_id="daily-amount-limit",
                counter_name="amount",
                limit=Decimal("100"),
            )
        ),
    )

    assert Decimal("40") < Decimal("100")
    assert decision.decision == "deny"
    assert decision.rule_id == "daily-amount-limit"
    assert decision.reason == "cumulative_limit_exceeded"
    assert decision.counters == "amount=limit_exceeded"
    assert decision.window_id == "daily-2026-08-23"
    assert decision.window_state == "open"


def test_cumulative_limit_uses_exact_arithmetic_under_low_global_precision() -> None:
    previous_context = getcontext().copy()
    try:
        getcontext().prec = 3
        decision = evaluate_trajectory_policy(
            _request(counters=(TrajectoryCounter("amount", Decimal("0.6")),)),
            _snapshot(counters=(TrajectoryCounter("amount", Decimal("99.6")),)),
            _policy(CumulativeLimitRule("exact-limit", "amount", Decimal("100.1"))),
        )
    finally:
        setcontext(previous_context)

    assert decision.decision == "deny"
    assert decision.rule_id == "exact-limit"
    assert decision.reason == "cumulative_limit_exceeded"


def test_cumulative_total_outside_numeric_range_is_denied_as_arithmetic_error() -> None:
    decision = evaluate_trajectory_policy(
        _request(counters=(TrajectoryCounter("amount", Decimal("0.000001")),)),
        _snapshot(counters=(TrajectoryCounter("amount", Decimal("999999999999.999999")),)),
        _policy(
            CumulativeLimitRule(
                "maximum-limit",
                "amount",
                Decimal("999999999999.999999"),
            )
        ),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "maximum-limit"
    assert decision.reason == "counter_arithmetic_error"


@pytest.mark.parametrize(
    ("value", "message"),
    [
        (Decimal("0.0000001"), "Trajectory counter scale exceeds maximum: amount"),
        (
            Decimal("1000000000000"),
            "Trajectory counter value exceeds maximum: amount",
        ),
    ],
)
def test_counter_rejects_values_outside_numeric_contract(
    value: Decimal,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        TrajectoryCounter("amount", value)


@pytest.mark.parametrize(
    ("field", "values", "message"),
    (
        (
            "fingerprints",
            tuple(Fingerprint(f"field-{index:02d}", DESTINATION_A) for index in range(17)),
            "Trajectory fingerprints must contain at most 16 entries",
        ),
        (
            "counters",
            tuple(TrajectoryCounter(f"counter-{index:02d}", Decimal("1")) for index in range(33)),
            "Trajectory counters must contain at most 32 entries",
        ),
    ),
)
def test_request_rejects_collections_that_can_overflow_telemetry(
    field: str,
    values: tuple[object, ...],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        _request(**{field: values})


@pytest.mark.parametrize(
    ("field", "values", "message"),
    (
        (
            "fingerprints",
            tuple(Fingerprint(f"field-{index:02d}", DESTINATION_A) for index in range(17)),
            "Trajectory fingerprints must contain at most 16 entries",
        ),
        (
            "counters",
            tuple(TrajectoryCounter(f"counter-{index:02d}", Decimal("1")) for index in range(33)),
            "Trajectory counters must contain at most 32 entries",
        ),
    ),
)
def test_snapshot_rejects_collections_that_can_overflow_telemetry(
    field: str,
    values: tuple[object, ...],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        _snapshot(**{field: values})


def test_maximum_collection_sizes_still_produce_bounded_telemetry() -> None:
    def long_name(prefix: str, index: int) -> str:
        stem = f"{prefix}-{index:02d}-"
        return stem + "x" * (64 - len(stem))

    request = _request(
        fingerprints=tuple(
            Fingerprint(long_name("request", index), DESTINATION_A) for index in range(16)
        ),
        counters=tuple(
            TrajectoryCounter(long_name("request-counter", index), Decimal("1"))
            for index in range(32)
        ),
    )
    policy = _policy(ValueBindingRule("binding", "shared"))
    snapshot = _snapshot(
        request=request,
        policy=policy,
        fingerprints=tuple(
            Fingerprint(long_name("history", index), DESTINATION_B) for index in range(16)
        ),
        counters=tuple(
            TrajectoryCounter(long_name("history-counter", index), Decimal("1"))
            for index in range(32)
        ),
        approval_records=(),
        approval_state="none",
    )

    payload = evaluate_trajectory_policy(request, snapshot, policy).to_event_payload()

    assert len(payload["fingerprints"]) <= 8192
    assert len(payload["counters"]) <= 8192


def test_cumulative_limit_rejects_scale_outside_numeric_contract() -> None:
    with pytest.raises(
        ValueError,
        match=r"Trajectory counter scale exceeds maximum: rules\.amount\.limit",
    ):
        CumulativeLimitRule("daily-amount-limit", "amount", Decimal("0.0000001"))


def test_missing_required_predecessor_is_denied() -> None:
    decision = evaluate_trajectory_policy(
        _request(sequence_number=2),
        _snapshot(observed_sequence=("read_destination",)),
        _policy(
            RequiredPredecessorRule(
                rule_id="destination-confirmed-first",
                predecessor="confirm_destination",
            )
        ),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "destination-confirmed-first"
    assert decision.reason == "required_predecessor_missing"


def test_missing_required_approval_requests_approval() -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(approval_records=(), approval_state="none"),
        _policy(RequiredApprovalRule("transfer-approval", "transfer")),
    )

    assert decision.decision == "approval_required"
    assert decision.rule_id == "transfer-approval"
    assert decision.reason == "required_approval_missing"
    assert decision.approval_state == "none"


def test_approval_for_another_request_fingerprint_does_not_satisfy_binding() -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(
            approval_records=(
                _approval_record(
                    "approval-other-request",
                    request=_request(action="submit_refund"),
                ),
            ),
            approval_state="approved",
        ),
        _policy(RequiredApprovalRule("transfer-approval", "transfer")),
    )

    assert decision.decision == "approval_required"
    assert decision.rule_id == "transfer-approval"
    assert decision.reason == "approval_binding_mismatch"


def test_approval_for_another_scope_does_not_satisfy_required_scope() -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(
            approval_records=(
                _approval_record(
                    "approval-other-scope",
                    scope="refund",
                ),
            ),
            approval_state="approved",
        ),
        _policy(RequiredApprovalRule("transfer-approval", "transfer")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "transfer-approval"
    assert decision.reason == "approval_state_mismatch"


def test_inactive_record_for_another_request_does_not_revoke_current_binding() -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(
            approval_records=(
                _approval_record(
                    "approval-revoked-other-request",
                    request=_request(action="submit_refund"),
                    state="revoked",
                ),
            ),
            approval_state="revoked",
        ),
        _policy(RequiredApprovalRule("transfer-approval", "transfer")),
    )

    assert decision.decision == "approval_required"
    assert decision.rule_id == "transfer-approval"
    assert decision.reason == "approval_binding_mismatch"


@pytest.mark.parametrize("inactive_state", ["rejected", "revoked", "expired"])
def test_inactive_bound_approval_takes_precedence_over_approved_record(
    inactive_state: str,
) -> None:
    approved = _snapshot().approval_records[0]
    inactive = _approval_record(
        f"approval-{inactive_state}",
        state=inactive_state,
    )

    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(
            approval_records=(approved, inactive),
            approval_state="approved",
        ),
        _policy(RequiredApprovalRule("transfer-approval", "transfer")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "transfer-approval"
    assert decision.reason == "required_approval_inactive"


def test_aggregate_state_mismatch_with_bound_approval_is_denied() -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(approval_state="pending"),
        _policy(RequiredApprovalRule("transfer-approval", "transfer")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "transfer-approval"
    assert decision.reason == "approval_state_mismatch"


def test_mixed_approved_and_pending_bound_records_are_denied() -> None:
    approved = _snapshot().approval_records[0]
    pending = _approval_record(
        "approval-pending",
        state="pending",
    )

    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(
            approval_records=(approved, pending),
            approval_state="approved",
        ),
        _policy(RequiredApprovalRule("transfer-approval", "transfer")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "transfer-approval"
    assert decision.reason == "approval_state_mismatch"


def test_aggregate_approved_without_records_is_denied() -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(approval_records=(), approval_state="approved"),
        _policy(RequiredApprovalRule("transfer-approval", "transfer")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "transfer-approval"
    assert decision.reason == "approval_state_mismatch"


def test_canonical_request_fingerprint_sorts_significant_values() -> None:
    policy = _policy(RequiredApprovalRule("transfer-approval", "transfer"))
    request = _request(
        fingerprints=(
            Fingerprint("destination", DESTINATION_A),
            Fingerprint("beneficiary", DESTINATION_B),
        ),
        counters=(
            TrajectoryCounter("amount", Decimal("20.00")),
            TrajectoryCounter("fee", Decimal("0.50")),
        ),
    )
    reordered = replace(
        request,
        fingerprints=tuple(reversed(request.fingerprints)),
        counters=tuple(reversed(request.counters)),
    )

    assert compute_trajectory_request_fingerprint(
        request,
        policy,
    ) == compute_trajectory_request_fingerprint(reordered, policy)


@pytest.mark.parametrize(
    (
        "request_overrides",
        "snapshot_overrides",
        "policy_version",
        "policy_id",
    ),
    [
        (
            {"action": "delete_tenant"},
            {},
            "2026.08.23",
            "transfer-trajectory",
        ),
        (
            {"tenant_id": "tenant-beta"},
            {"tenant_id": "tenant-beta"},
            "2026.08.23",
            "transfer-trajectory",
        ),
        (
            {"subject_id": "subject-99"},
            {"subject_id": "subject-99"},
            "2026.08.23",
            "transfer-trajectory",
        ),
        (
            {"expected_history_ref": "trajectory://transfer/002"},
            {"history_ref": "trajectory://transfer/002"},
            "2026.08.23",
            "transfer-trajectory",
        ),
        (
            {"expected_history_version": 8},
            {"history_version": 8},
            "2026.08.23",
            "transfer-trajectory",
        ),
        (
            {"sequence_number": 4},
            {
                "observed_sequence": (
                    "read_destination",
                    "confirm_destination",
                    "review_transfer",
                )
            },
            "2026.08.23",
            "transfer-trajectory",
        ),
        (
            {"window_id": "daily-2026-08-24"},
            {"window_id": "daily-2026-08-24"},
            "2026.08.23",
            "transfer-trajectory",
        ),
        (
            {"fingerprints": (Fingerprint("destination", DESTINATION_B),)},
            {},
            "2026.08.23",
            "transfer-trajectory",
        ),
        (
            {"counters": (TrajectoryCounter("amount", Decimal("21")),)},
            {},
            "2026.08.23",
            "transfer-trajectory",
        ),
        (
            {},
            {"policy_id": "transfer-trajectory-v2"},
            "2026.08.23",
            "transfer-trajectory-v2",
        ),
        (
            {},
            {"policy_version": "2026.08.24"},
            "2026.08.24",
            "transfer-trajectory",
        ),
    ],
    ids=(
        "action",
        "tenant",
        "subject",
        "history_ref",
        "history_version",
        "sequence_number",
        "window_id",
        "fingerprints",
        "counters",
        "policy_id",
        "policy_version",
    ),
)
def test_old_approval_does_not_authorize_changed_request_identity(
    request_overrides: dict[str, object],
    snapshot_overrides: dict[str, object],
    policy_version: str,
    policy_id: str,
) -> None:
    approval_policy = _policy(
        RequiredApprovalRule("transfer-approval", "transfer"),
    )
    original_request = _request()
    snapshot = _snapshot(request=original_request, policy=approval_policy)
    current_policy = _policy(
        RequiredApprovalRule("transfer-approval", "transfer"),
        policy_id=policy_id,
        policy_version=policy_version,
    )
    current_request = _request(**request_overrides)

    decision = evaluate_trajectory_policy(
        current_request,
        replace(snapshot, **snapshot_overrides),
        current_policy,
    )

    assert decision.decision == "approval_required"
    assert decision.rule_id == "transfer-approval"
    assert decision.reason == "approval_binding_mismatch"


@pytest.mark.parametrize(
    "snapshot_overrides",
    [
        {"tenant_id": "tenant-beta"},
        {"subject_id": "subject-99"},
    ],
    ids=("tenant", "subject"),
)
def test_snapshot_request_identity_mismatch_is_denied(
    snapshot_overrides: dict[str, object],
) -> None:
    policy = _policy(ValueBindingRule("destination-binding", "destination"))
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(**snapshot_overrides),
        policy,
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "trajectory.identity"
    assert decision.reason == "trajectory_identity_mismatch"


def test_snapshot_policy_identity_mismatch_is_denied() -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(policy_version="2026.08.24"),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "trajectory.policy_identity"
    assert decision.reason == "policy_identity_mismatch"


def test_matching_trusted_trajectory_is_allowed() -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(),
        _policy(
            ValueBindingRule("destination-binding", "destination"),
            CumulativeLimitRule("daily-amount-limit", "amount", Decimal("100")),
            RequiredPredecessorRule(
                "destination-confirmed-first",
                "confirm_destination",
            ),
            RequiredApprovalRule("transfer-approval", "transfer"),
        ),
    )

    assert decision.decision == "allow"
    assert decision.rule_id == "trajectory.all_rules"
    assert decision.reason == "all_rules_satisfied"
    assert decision.counters == "amount=within_limit"
    assert decision.approval_state == "approved"


def test_rules_stop_at_first_failure_and_keep_prior_counter_evidence() -> None:
    decision = evaluate_trajectory_policy(
        _request(fingerprints=(Fingerprint("destination", DESTINATION_B),)),
        _snapshot(),
        _policy(
            CumulativeLimitRule("daily-amount-limit", "amount", Decimal("100")),
            ValueBindingRule("destination-binding", "destination"),
            RequiredPredecessorRule("unreached-predecessor", "review_transfer"),
        ),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "destination-binding"
    assert decision.reason == "value_binding_mismatch"
    assert decision.counters == "amount=within_limit"


@pytest.mark.parametrize(
    (
        "request_overrides",
        "snapshot_overrides",
        "expected_rule_id",
        "expected_reason",
    ),
    [
        (
            {},
            {"status": "missing", "integrity": "corrupt"},
            "trajectory.history_trust",
            "history_missing",
        ),
        (
            {"expected_history_ref": "trajectory://transfer/002"},
            {"history_version": 8, "tenant_id": "tenant-beta"},
            "trajectory.history_trust",
            "history_ref_mismatch",
        ),
        (
            {"sequence_number": 4},
            {
                "tenant_id": "tenant-beta",
                "policy_version": "2026.08.24",
                "window_id": "daily-2026-08-24",
            },
            "trajectory.identity",
            "trajectory_identity_mismatch",
        ),
        (
            {"sequence_number": 4, "window_id": "daily-2026-08-24"},
            {},
            "trajectory.sequence",
            "observed_sequence_mismatch",
        ),
    ],
    ids=(
        "missing-before-corrupt",
        "reference-before-version",
        "identity-before-policy",
        "sequence-before-window",
    ),
)
def test_snapshot_validation_preserves_fail_closed_precedence(
    request_overrides: dict[str, object],
    snapshot_overrides: dict[str, object],
    expected_rule_id: str,
    expected_reason: str,
) -> None:
    decision = evaluate_trajectory_policy(
        _request(**request_overrides),
        _snapshot(**snapshot_overrides),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.rule_id == expected_rule_id
    assert decision.reason == expected_reason


@pytest.mark.parametrize(
    ("integrity", "status", "reason"),
    [
        ("missing", "missing", "history_missing"),
        ("corrupt", "current", "history_corrupt"),
        ("verified", "stale", "history_stale"),
        ("unverified", "current", "history_unverified"),
    ],
)
def test_untrusted_history_fails_closed(
    integrity: str,
    status: str,
    reason: str,
) -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(integrity=integrity, status=status),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "trajectory.history_trust"
    assert decision.reason == reason


@pytest.mark.parametrize(
    ("snapshot", "reason"),
    [
        (None, "history_missing"),
        ({"history_ref": "RAW_SECRET\ncontrol"}, "history_malformed"),
        (object(), "history_malformed"),
    ],
    ids=("none", "mapping", "object"),
)
def test_absent_or_malformed_history_returns_redacted_denial(
    snapshot: object,
    reason: str,
) -> None:
    request = _request()
    decision = evaluate_trajectory_policy(
        request,
        snapshot,
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "trajectory.history_trust"
    assert decision.reason == reason
    assert decision.history_ref == request.expected_history_ref
    payload = decision.to_event_payload()
    assert all(isinstance(value, str) for value in payload.values())
    assert "RAW_SECRET" not in repr(payload)


def test_history_version_mismatch_is_denied() -> None:
    decision = evaluate_trajectory_policy(
        _request(expected_history_version=8),
        _snapshot(),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "trajectory.history_trust"
    assert decision.reason == "history_version_mismatch"


def test_history_reference_mismatch_is_denied() -> None:
    decision = evaluate_trajectory_policy(
        _request(expected_history_ref="trajectory://transfer/002"),
        _snapshot(),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "trajectory.history_trust"
    assert decision.reason == "history_ref_mismatch"


def test_observed_sequence_mismatch_is_denied() -> None:
    decision = evaluate_trajectory_policy(
        _request(sequence_number=4),
        _snapshot(),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "trajectory.sequence"
    assert decision.reason == "observed_sequence_mismatch"


def test_window_mismatch_is_denied() -> None:
    decision = evaluate_trajectory_policy(
        _request(window_id="daily-2026-08-24"),
        _snapshot(),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "trajectory.window"
    assert decision.reason == "window_mismatch"


@pytest.mark.parametrize("window_state", ["closed", "stale"])
def test_window_not_open_is_denied(window_state: str) -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(window_state=window_state),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "trajectory.window"
    assert decision.reason == "window_not_open"


def test_snapshot_is_deeply_immutable_and_requires_tuple_collections() -> None:
    snapshot = _snapshot()

    with pytest.raises(FrozenInstanceError):
        snapshot.history_version = 8  # type: ignore[misc]
    with pytest.raises(TypeError, match="Trajectory fingerprints must be a tuple"):
        _snapshot(fingerprints=[Fingerprint("destination", DESTINATION_A)])


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (
            lambda: _request(fingerprints=(object(),)),
            "Trajectory fingerprints entries must be Fingerprint",
        ),
        (
            lambda: _snapshot(approval_records=(object(),)),
            "Trajectory approval_records entries must be ApprovalRecord",
        ),
        (
            lambda: _policy(object()),
            "Trajectory rules entries must be trajectory rule objects",
        ),
    ],
    ids=("request-fingerprint", "snapshot-approval", "policy-rule"),
)
def test_typed_collections_reject_wrong_entry_types(
    factory: Callable[[], object],
    message: str,
) -> None:
    with pytest.raises(TypeError, match=message):
        factory()


def test_fingerprints_are_normalized_and_invalid_counter_types_are_rejected() -> None:
    fingerprint = Fingerprint(" destination ", f"SHA256:{'A' * 64}")

    assert fingerprint.name == "destination"
    assert fingerprint.value == f"sha256:{'a' * 64}"
    with pytest.raises(
        TypeError,
        match="Trajectory counter value must be a Decimal: amount",
    ):
        TrajectoryCounter("amount", 20)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field", "factory"),
    [
        (
            "policy_id",
            lambda value: _policy(
                ValueBindingRule("destination-binding", "destination"),
                policy_id=value,
            ),
        ),
        ("action", lambda value: _request(action=value)),
        ("fingerprint.name", lambda value: Fingerprint(value, DESTINATION_A)),
        ("counter.name", lambda value: TrajectoryCounter(value, Decimal("1"))),
        (
            "rule_id",
            lambda value: ValueBindingRule(value, "destination"),
        ),
        (
            "approval_id",
            lambda value: _approval_record(value),
        ),
        ("window_id", lambda value: _request(window_id=value)),
    ],
)
def test_security_identifiers_reject_uppercase_free_form_or_control_values(
    field: str,
    factory: Callable[[str], object],
) -> None:
    unsafe_value = {
        "action": "delete tenant",
        "fingerprint.name": "destination\nraw_secret",
        "counter.name": "RAW_SECRET",
        "rule_id": "rule\tsecret",
        "window_id": "a" * 65,
    }.get(field, "RAW_SECRET")

    with pytest.raises(
        ValueError,
        match=f"Trajectory identifier is invalid: {field}",
    ):
        factory(unsafe_value)


def test_history_reference_rejects_uppercase_or_control_content() -> None:
    with pytest.raises(
        ValueError,
        match="Trajectory reference is invalid: expected_history_ref",
    ):
        _request(expected_history_ref="trajectory://transfer/RAW_SECRET\ncontrol")


def test_event_payload_rejects_unsafe_replacement_value() -> None:
    decision = evaluate_trajectory_policy(
        _request(),
        _snapshot(),
        _policy(ValueBindingRule("destination-binding", "destination")),
    )
    unsafe_decision = replace(decision, counters="RAW_SECRET\ncontrol")

    with pytest.raises(
        ValueError,
        match="Trajectory telemetry value is invalid: counters",
    ):
        unsafe_decision.to_event_payload()
