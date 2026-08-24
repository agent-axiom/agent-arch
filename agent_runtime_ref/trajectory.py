from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from decimal import (
    Clamped,
    Context,
    Decimal,
    DecimalException,
    DivisionByZero,
    Inexact,
    InvalidOperation,
    Overflow,
    Rounded,
    Subnormal,
    Underflow,
    localcontext,
)
from typing import TypeAlias

_FINGERPRINT_PATTERN = re.compile(r"sha256:[0-9a-f]{64}\Z")
_SAFE_IDENTIFIER_PATTERN = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}\Z")
_SAFE_REFERENCE_PATTERN = re.compile(
    r"[a-z][a-z0-9+.-]{0,15}://[a-z0-9][a-z0-9._~:/#-]*\Z"
)
_SAFE_TELEMETRY_PATTERN = re.compile(
    r"[a-z0-9][a-z0-9+._~:/#=;,\[\]-]*\Z"
)
_MAX_REFERENCE_LENGTH = 256
_MAX_TELEMETRY_VALUE_LENGTH = 8192
_HISTORY_INTEGRITY = {"verified", "missing", "corrupt", "unverified"}
_HISTORY_STATUSES = {"current", "missing", "stale"}
_WINDOW_STATES = {"open", "closed", "stale"}
_APPROVAL_STATES = {"none", "pending", "approved", "rejected", "revoked", "expired"}
_INACTIVE_APPROVAL_STATES = {"rejected", "revoked", "expired"}
_DECISIONS = {"allow", "deny", "approval_required"}
_MAX_COUNTER_SCALE = 6
_MAX_COUNTER_VALUE = Decimal("999999999999.999999")
_MAX_FINGERPRINTS = 16
_MAX_COUNTERS = 32
_COUNTER_CONTEXT = Context(prec=32, Emax=18, Emin=-18)
for _signal in (
    Clamped,
    DivisionByZero,
    Inexact,
    InvalidOperation,
    Overflow,
    Rounded,
    Subnormal,
    Underflow,
):
    _COUNTER_CONTEXT.traps[_signal] = True


def _required_string(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Trajectory field must be a string: {field}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"Trajectory field is required: {field}")
    return normalized


def _safe_identifier(value: object, *, field: str) -> str:
    normalized = _required_string(value, field=field)
    if not _SAFE_IDENTIFIER_PATTERN.fullmatch(normalized):
        raise ValueError(f"Trajectory identifier is invalid: {field}")
    return normalized


def _safe_reference(value: object, *, field: str) -> str:
    normalized = _required_string(value, field=field)
    if (
        len(normalized) > _MAX_REFERENCE_LENGTH
        or not _SAFE_REFERENCE_PATTERN.fullmatch(normalized)
    ):
        raise ValueError(f"Trajectory reference is invalid: {field}")
    return normalized


def _safe_telemetry_value(value: object, *, field: str) -> str:
    normalized = _required_string(value, field=field)
    if (
        len(normalized) > _MAX_TELEMETRY_VALUE_LENGTH
        or not _SAFE_TELEMETRY_PATTERN.fullmatch(normalized)
    ):
        raise ValueError(f"Trajectory telemetry value is invalid: {field}")
    return normalized


def _nonnegative_integer(value: object, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"Trajectory field must be an integer: {field}")
    if value < 0:
        raise ValueError(f"Trajectory integer must not be negative: {field}")
    return value


def _positive_integer(value: object, *, field: str) -> int:
    normalized = _nonnegative_integer(value, field=field)
    if normalized == 0:
        raise ValueError(f"Trajectory integer must be positive: {field}")
    return normalized


def _choice(value: object, *, field: str, supported: set[str]) -> str:
    normalized = _required_string(value, field=field)
    if normalized not in supported:
        raise ValueError(f"Trajectory field is not supported: {field}={normalized}")
    return normalized


def _fingerprint(value: object, *, field: str) -> str:
    normalized = _required_string(value, field=field).lower()
    if not _FINGERPRINT_PATTERN.fullmatch(normalized):
        raise ValueError(f"Trajectory fingerprint must be sha256: {field}")
    return normalized


def _decimal(value: object, *, field: str) -> Decimal:
    if not isinstance(value, Decimal):
        raise TypeError(f"Trajectory counter value must be a Decimal: {field}")
    if not value.is_finite():
        raise ValueError(f"Trajectory counter value must be finite: {field}")
    if value < 0:
        raise ValueError(f"Trajectory counter value must not be negative: {field}")
    exponent = value.as_tuple().exponent
    if not isinstance(exponent, int):
        raise ValueError(f"Trajectory counter value must be finite: {field}")
    if max(-exponent, 0) > _MAX_COUNTER_SCALE:
        raise ValueError(f"Trajectory counter scale exceeds maximum: {field}")
    if value > _MAX_COUNTER_VALUE:
        raise ValueError(f"Trajectory counter value exceeds maximum: {field}")
    return value


def _add_counter_values(left: Decimal, right: Decimal) -> Decimal | None:
    try:
        with localcontext(_COUNTER_CONTEXT):
            total = left + right
    except DecimalException:
        return None
    if not total.is_finite() or total > _MAX_COUNTER_VALUE:
        return None
    return total


def _tuple(value: object, *, label: str) -> tuple[object, ...]:
    if not isinstance(value, tuple):
        raise TypeError(f"Trajectory {label} must be a tuple")
    return value


def _normalize_sequence(value: object) -> tuple[str, ...]:
    items = _tuple(value, label="observed_sequence")
    return tuple(
        _safe_identifier(item, field=f"observed_sequence[{index}]")
        for index, item in enumerate(items)
    )


def _typed_tuple(
    value: object,
    *,
    label: str,
    item_type: type,
) -> tuple[object, ...]:
    items = _tuple(value, label=label)
    for item in items:
        if not isinstance(item, item_type):
            raise TypeError(f"Trajectory {label} entries must be {item_type.__name__}")
    return items


def _require_unique_names(items: tuple[object, ...], *, label: str) -> None:
    names = [getattr(item, "name") for item in items]
    if len(names) != len(set(names)):
        raise ValueError(f"Trajectory {label} names must be unique")


def _require_bounded_collection(
    items: tuple[object, ...],
    *,
    label: str,
    maximum: int,
) -> None:
    if len(items) > maximum:
        raise ValueError(
            f"Trajectory {label} must contain at most {maximum} entries"
        )


@dataclass(frozen=True, slots=True)
class Fingerprint:
    name: str
    value: str

    def __post_init__(self) -> None:
        name = _safe_identifier(self.name, field="fingerprint.name")
        value = _fingerprint(self.value, field=f"fingerprints.{name}")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "value", value)


@dataclass(frozen=True, slots=True)
class TrajectoryCounter:
    name: str
    value: Decimal

    def __post_init__(self) -> None:
        name = _safe_identifier(self.name, field="counter.name")
        value = _decimal(self.value, field=name)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "value", value)


@dataclass(frozen=True, slots=True)
class ApprovalRecord:
    approval_id: str
    scope: str
    request_fingerprint: str
    state: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "approval_id",
            _safe_identifier(self.approval_id, field="approval_id"),
        )
        object.__setattr__(self, "scope", _safe_identifier(self.scope, field="scope"))
        object.__setattr__(
            self,
            "request_fingerprint",
            _fingerprint(self.request_fingerprint, field="approval.request_fingerprint"),
        )
        object.__setattr__(
            self,
            "state",
            _choice(self.state, field="approval.state", supported=_APPROVAL_STATES - {"none"}),
        )


@dataclass(frozen=True, slots=True)
class TrajectoryRequest:
    action: str
    tenant_id: str
    subject_id: str
    expected_history_ref: str
    expected_history_version: int
    sequence_number: int
    fingerprints: tuple[Fingerprint, ...]
    counters: tuple[TrajectoryCounter, ...]
    window_id: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "action", _safe_identifier(self.action, field="action"))
        for field in ("tenant_id", "subject_id"):
            object.__setattr__(
                self,
                field,
                _safe_identifier(getattr(self, field), field=field),
            )
        object.__setattr__(
            self,
            "expected_history_ref",
            _safe_reference(
                self.expected_history_ref,
                field="expected_history_ref",
            ),
        )
        object.__setattr__(
            self,
            "expected_history_version",
            _nonnegative_integer(
                self.expected_history_version,
                field="expected_history_version",
            ),
        )
        object.__setattr__(
            self,
            "sequence_number",
            _positive_integer(self.sequence_number, field="sequence_number"),
        )
        fingerprints = _typed_tuple(
            self.fingerprints,
            label="fingerprints",
            item_type=Fingerprint,
        )
        counters = _typed_tuple(
            self.counters,
            label="counters",
            item_type=TrajectoryCounter,
        )
        _require_bounded_collection(
            fingerprints,
            label="fingerprints",
            maximum=_MAX_FINGERPRINTS,
        )
        _require_bounded_collection(
            counters,
            label="counters",
            maximum=_MAX_COUNTERS,
        )
        _require_unique_names(fingerprints, label="fingerprint")
        _require_unique_names(counters, label="counter")
        object.__setattr__(self, "fingerprints", fingerprints)
        object.__setattr__(self, "counters", counters)
        object.__setattr__(
            self,
            "window_id",
            _safe_identifier(self.window_id, field="window_id"),
        )


@dataclass(frozen=True, slots=True)
class TrajectorySnapshot:
    history_ref: str
    history_version: int
    tenant_id: str
    subject_id: str
    policy_id: str
    policy_version: str
    integrity: str
    status: str
    observed_sequence: tuple[str, ...]
    fingerprints: tuple[Fingerprint, ...]
    counters: tuple[TrajectoryCounter, ...]
    window_id: str
    window_state: str
    approval_records: tuple[ApprovalRecord, ...]
    approval_state: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "history_ref",
            _safe_reference(self.history_ref, field="history_ref"),
        )
        object.__setattr__(
            self,
            "history_version",
            _nonnegative_integer(self.history_version, field="history_version"),
        )
        for field in ("tenant_id", "subject_id", "policy_id", "policy_version"):
            object.__setattr__(
                self,
                field,
                _safe_identifier(getattr(self, field), field=field),
            )
        object.__setattr__(
            self,
            "integrity",
            _choice(self.integrity, field="integrity", supported=_HISTORY_INTEGRITY),
        )
        object.__setattr__(
            self,
            "status",
            _choice(self.status, field="status", supported=_HISTORY_STATUSES),
        )
        object.__setattr__(
            self,
            "observed_sequence",
            _normalize_sequence(self.observed_sequence),
        )
        fingerprints = _typed_tuple(
            self.fingerprints,
            label="fingerprints",
            item_type=Fingerprint,
        )
        counters = _typed_tuple(
            self.counters,
            label="counters",
            item_type=TrajectoryCounter,
        )
        approval_records = _typed_tuple(
            self.approval_records,
            label="approval_records",
            item_type=ApprovalRecord,
        )
        _require_bounded_collection(
            fingerprints,
            label="fingerprints",
            maximum=_MAX_FINGERPRINTS,
        )
        _require_bounded_collection(
            counters,
            label="counters",
            maximum=_MAX_COUNTERS,
        )
        _require_unique_names(fingerprints, label="fingerprint")
        _require_unique_names(counters, label="counter")
        approval_ids = [record.approval_id for record in approval_records]
        if len(approval_ids) != len(set(approval_ids)):
            raise ValueError("Trajectory approval record IDs must be unique")
        object.__setattr__(self, "fingerprints", fingerprints)
        object.__setattr__(self, "counters", counters)
        object.__setattr__(self, "approval_records", approval_records)
        object.__setattr__(
            self,
            "window_id",
            _safe_identifier(self.window_id, field="window_id"),
        )
        object.__setattr__(
            self,
            "window_state",
            _choice(self.window_state, field="window_state", supported=_WINDOW_STATES),
        )
        object.__setattr__(
            self,
            "approval_state",
            _choice(self.approval_state, field="approval_state", supported=_APPROVAL_STATES),
        )


@dataclass(frozen=True, slots=True)
class ValueBindingRule:
    rule_id: str
    fingerprint_name: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "rule_id",
            _safe_identifier(self.rule_id, field="rule_id"),
        )
        object.__setattr__(
            self,
            "fingerprint_name",
            _safe_identifier(self.fingerprint_name, field="fingerprint_name"),
        )


@dataclass(frozen=True, slots=True)
class CumulativeLimitRule:
    rule_id: str
    counter_name: str
    limit: Decimal

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "rule_id",
            _safe_identifier(self.rule_id, field="rule_id"),
        )
        counter_name = _safe_identifier(self.counter_name, field="counter_name")
        limit = _decimal(self.limit, field=f"rules.{counter_name}.limit")
        if limit == 0:
            raise ValueError(f"Trajectory counter limit must be positive: {counter_name}")
        object.__setattr__(self, "counter_name", counter_name)
        object.__setattr__(self, "limit", limit)


@dataclass(frozen=True, slots=True)
class RequiredPredecessorRule:
    rule_id: str
    predecessor: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "rule_id",
            _safe_identifier(self.rule_id, field="rule_id"),
        )
        object.__setattr__(
            self,
            "predecessor",
            _safe_identifier(self.predecessor, field="predecessor"),
        )


@dataclass(frozen=True, slots=True)
class RequiredApprovalRule:
    rule_id: str
    approval_scope: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "rule_id",
            _safe_identifier(self.rule_id, field="rule_id"),
        )
        object.__setattr__(
            self,
            "approval_scope",
            _safe_identifier(self.approval_scope, field="approval_scope"),
        )


TrajectoryRule: TypeAlias = (
    ValueBindingRule
    | CumulativeLimitRule
    | RequiredPredecessorRule
    | RequiredApprovalRule
)
_RULE_TYPES = (
    ValueBindingRule,
    CumulativeLimitRule,
    RequiredPredecessorRule,
    RequiredApprovalRule,
)


@dataclass(frozen=True, slots=True)
class TrajectoryPolicy:
    policy_id: str
    policy_version: str
    rules: tuple[TrajectoryRule, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "policy_id",
            _safe_identifier(self.policy_id, field="policy_id"),
        )
        object.__setattr__(
            self,
            "policy_version",
            _safe_identifier(self.policy_version, field="policy_version"),
        )
        rules = _tuple(self.rules, label="rules")
        if not rules:
            raise ValueError("Trajectory policy must contain at least one rule")
        for rule in rules:
            if not isinstance(rule, _RULE_TYPES):
                raise TypeError("Trajectory rules entries must be trajectory rule objects")
        rule_ids = [rule.rule_id for rule in rules]
        if len(rule_ids) != len(set(rule_ids)):
            raise ValueError("Trajectory rule IDs must be unique")
        object.__setattr__(self, "rules", rules)


def _canonical_decimal(value: Decimal) -> str:
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered or "0"


def compute_trajectory_request_fingerprint(
    request: TrajectoryRequest,
    policy: TrajectoryPolicy,
) -> str:
    if not isinstance(request, TrajectoryRequest):
        raise TypeError("Trajectory fingerprint request must be TrajectoryRequest")
    if not isinstance(policy, TrajectoryPolicy):
        raise TypeError("Trajectory fingerprint policy must be TrajectoryPolicy")
    payload = {
        "action": request.action,
        "counter_deltas": [
            (item.name, _canonical_decimal(item.value))
            for item in sorted(request.counters, key=lambda item: item.name)
        ],
        "expected_history_ref": request.expected_history_ref,
        "expected_history_version": request.expected_history_version,
        "fingerprints": [
            (item.name, item.value)
            for item in sorted(request.fingerprints, key=lambda item: item.name)
        ],
        "policy_id": policy.policy_id,
        "policy_version": policy.policy_version,
        "sequence_number": request.sequence_number,
        "subject_id": request.subject_id,
        "tenant_id": request.tenant_id,
        "window_id": request.window_id,
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True, slots=True)
class TrajectoryPolicyDecision:
    policy_id: str
    policy_version: str
    rule_id: str
    reason: str
    history_ref: str
    history_version: int
    sequence_summary: str
    sequence_ref: str
    fingerprints: str
    counters: str
    window_id: str
    window_state: str
    approval_state: str
    decision: str

    def __post_init__(self) -> None:
        for field in (
            "policy_id",
            "policy_version",
            "rule_id",
            "reason",
            "history_ref",
            "sequence_summary",
            "sequence_ref",
            "fingerprints",
            "counters",
            "window_id",
            "window_state",
            "approval_state",
        ):
            object.__setattr__(
                self,
                field,
                _required_string(getattr(self, field), field=field),
            )
        object.__setattr__(
            self,
            "history_version",
            _nonnegative_integer(self.history_version, field="history_version"),
        )
        object.__setattr__(
            self,
            "decision",
            _choice(self.decision, field="decision", supported=_DECISIONS),
        )

    def to_event_payload(self) -> dict[str, str]:
        payload = {
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "rule_id": self.rule_id,
            "reason": self.reason,
            "history_ref": self.history_ref,
            "history_version": str(self.history_version),
            "sequence_summary": self.sequence_summary,
            "sequence_ref": self.sequence_ref,
            "fingerprints": self.fingerprints,
            "counters": self.counters,
            "window_id": self.window_id,
            "window_state": self.window_state,
            "approval_state": self.approval_state,
            "decision": self.decision,
        }
        return {
            field: _safe_telemetry_value(value, field=field)
            for field, value in payload.items()
        }


def _fingerprint_summary(
    request: TrajectoryRequest,
    snapshot: TrajectorySnapshot | None,
    request_fingerprint: str,
) -> str:
    current = {item.name: item.value for item in request.fingerprints}
    history = (
        {item.name: item.value for item in snapshot.fingerprints}
        if snapshot is not None
        else {}
    )
    fields = sorted(current.keys() | history.keys())
    summaries: list[str] = []
    for field in fields:
        values: list[str] = []
        if field in history:
            values.append(f"history={history[field]}")
        if field in current:
            values.append(f"current={current[field]}")
        summaries.append(f"{field}[{','.join(values)}]")
    summaries.append(f"request[{request_fingerprint}]")
    return ";".join(summaries)


def _counter_summary(states: dict[str, str]) -> str:
    if not states:
        return "none"
    return ";".join(f"{name}={states[name]}" for name in sorted(states))


def _history_boundary_decision(
    request: TrajectoryRequest,
    policy: TrajectoryPolicy,
    request_fingerprint: str,
    *,
    reason: str,
) -> TrajectoryPolicyDecision:
    counter_states = {item.name: "not_evaluated" for item in request.counters}
    return TrajectoryPolicyDecision(
        policy_id=policy.policy_id,
        policy_version=policy.policy_version,
        rule_id="trajectory.history_trust",
        reason=reason,
        history_ref=request.expected_history_ref,
        history_version=request.expected_history_version,
        sequence_summary=f"observed=unknown;current={request.sequence_number}",
        sequence_ref=f"{request.expected_history_ref}#observed_sequence",
        fingerprints=_fingerprint_summary(request, None, request_fingerprint),
        counters=_counter_summary(counter_states),
        window_id=request.window_id,
        window_state="unknown",
        approval_state="unknown",
        decision="deny",
    )


def evaluate_trajectory_policy(
    request: TrajectoryRequest,
    snapshot: object,
    policy: TrajectoryPolicy,
) -> TrajectoryPolicyDecision:
    """Evaluate one request against one trusted, caller-supplied history snapshot."""
    if not isinstance(request, TrajectoryRequest):
        raise TypeError("Trajectory request must be TrajectoryRequest")
    if not isinstance(policy, TrajectoryPolicy):
        raise TypeError("Trajectory policy must be TrajectoryPolicy")

    request_fingerprint = compute_trajectory_request_fingerprint(request, policy)
    if snapshot is None:
        return _history_boundary_decision(
            request,
            policy,
            request_fingerprint,
            reason="history_missing",
        )
    if not isinstance(snapshot, TrajectorySnapshot):
        return _history_boundary_decision(
            request,
            policy,
            request_fingerprint,
            reason="history_malformed",
        )

    counter_states = {
        item.name: "not_evaluated" for item in (*snapshot.counters, *request.counters)
    }

    def decide(
        decision: str,
        rule_id: str,
        reason: str,
    ) -> TrajectoryPolicyDecision:
        return TrajectoryPolicyDecision(
            policy_id=policy.policy_id,
            policy_version=policy.policy_version,
            rule_id=rule_id,
            reason=reason,
            history_ref=snapshot.history_ref,
            history_version=snapshot.history_version,
            sequence_summary=(
                f"observed={len(snapshot.observed_sequence)};current={request.sequence_number}"
            ),
            sequence_ref=f"{snapshot.history_ref}#observed_sequence",
            fingerprints=_fingerprint_summary(request, snapshot, request_fingerprint),
            counters=_counter_summary(counter_states),
            window_id=snapshot.window_id,
            window_state=snapshot.window_state,
            approval_state=snapshot.approval_state,
            decision=decision,
        )

    if snapshot.status == "missing" or snapshot.integrity == "missing":
        return decide("deny", "trajectory.history_trust", "history_missing")
    if snapshot.integrity == "corrupt":
        return decide("deny", "trajectory.history_trust", "history_corrupt")
    if snapshot.status == "stale":
        return decide("deny", "trajectory.history_trust", "history_stale")
    if snapshot.integrity != "verified":
        return decide("deny", "trajectory.history_trust", "history_unverified")
    if request.expected_history_ref != snapshot.history_ref:
        return decide("deny", "trajectory.history_trust", "history_ref_mismatch")
    if request.expected_history_version != snapshot.history_version:
        return decide("deny", "trajectory.history_trust", "history_version_mismatch")
    if (
        request.tenant_id != snapshot.tenant_id
        or request.subject_id != snapshot.subject_id
    ):
        return decide("deny", "trajectory.identity", "trajectory_identity_mismatch")
    if (
        policy.policy_id != snapshot.policy_id
        or policy.policy_version != snapshot.policy_version
    ):
        return decide("deny", "trajectory.policy_identity", "policy_identity_mismatch")
    if request.sequence_number != len(snapshot.observed_sequence) + 1:
        return decide("deny", "trajectory.sequence", "observed_sequence_mismatch")
    if request.window_id != snapshot.window_id:
        return decide("deny", "trajectory.window", "window_mismatch")
    if snapshot.window_state != "open":
        return decide("deny", "trajectory.window", "window_not_open")

    current_fingerprints = {item.name: item.value for item in request.fingerprints}
    history_fingerprints = {item.name: item.value for item in snapshot.fingerprints}
    current_counters = {item.name: item.value for item in request.counters}
    history_counters = {item.name: item.value for item in snapshot.counters}

    for rule in policy.rules:
        if isinstance(rule, ValueBindingRule):
            current_value = current_fingerprints.get(rule.fingerprint_name)
            history_value = history_fingerprints.get(rule.fingerprint_name)
            if current_value is None:
                return decide("deny", rule.rule_id, "current_fingerprint_missing")
            if history_value is None:
                return decide("deny", rule.rule_id, "history_fingerprint_missing")
            if current_value != history_value:
                return decide("deny", rule.rule_id, "value_binding_mismatch")
            continue

        if isinstance(rule, CumulativeLimitRule):
            current_value = current_counters.get(rule.counter_name)
            history_value = history_counters.get(rule.counter_name)
            if current_value is None:
                return decide("deny", rule.rule_id, "current_counter_missing")
            if history_value is None:
                return decide("deny", rule.rule_id, "history_counter_missing")
            total = _add_counter_values(history_value, current_value)
            if total is None:
                counter_states[rule.counter_name] = "arithmetic_error"
                return decide("deny", rule.rule_id, "counter_arithmetic_error")
            if total > rule.limit:
                counter_states[rule.counter_name] = "limit_exceeded"
                return decide("deny", rule.rule_id, "cumulative_limit_exceeded")
            counter_states[rule.counter_name] = "within_limit"
            continue

        if isinstance(rule, RequiredPredecessorRule):
            if rule.predecessor not in snapshot.observed_sequence:
                return decide("deny", rule.rule_id, "required_predecessor_missing")
            continue

        scope_approvals = tuple(
            record
            for record in snapshot.approval_records
            if record.scope == rule.approval_scope
        )
        bound_approvals = tuple(
            record
            for record in scope_approvals
            if record.request_fingerprint == request_fingerprint
        )

        if not bound_approvals:
            if scope_approvals:
                return decide("approval_required", rule.rule_id, "approval_binding_mismatch")
            if snapshot.approval_state != "none":
                return decide("deny", rule.rule_id, "approval_state_mismatch")
            return decide("approval_required", rule.rule_id, "required_approval_missing")

        bound_states = {record.state for record in bound_approvals}
        if bound_states & _INACTIVE_APPROVAL_STATES:
            return decide("deny", rule.rule_id, "required_approval_inactive")
        if bound_states == {"approved"}:
            if snapshot.approval_state != "approved":
                return decide("deny", rule.rule_id, "approval_state_mismatch")
            continue
        if bound_states == {"pending"}:
            if snapshot.approval_state != "pending":
                return decide("deny", rule.rule_id, "approval_state_mismatch")
            return decide("approval_required", rule.rule_id, "approval_binding_mismatch")
        return decide("deny", rule.rule_id, "approval_state_mismatch")

    return decide("allow", "trajectory.all_rules", "all_rules_satisfied")
