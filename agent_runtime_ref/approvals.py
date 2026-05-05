from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ApprovalPolicy:
    default_reviewer: str
    escalation_sla_minutes: int

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ApprovalPolicy":
        raw_approvals = data.get("approvals", {})
        if not isinstance(raw_approvals, Mapping):
            raise TypeError("'approvals' must be a mapping")
        default_reviewer = str(raw_approvals.get("default_reviewer", "manager")).strip()
        if not default_reviewer:
            raise ValueError("approvals.default_reviewer is required")
        escalation_sla_minutes = raw_approvals.get("escalation_sla_minutes", 30)
        if not isinstance(escalation_sla_minutes, int) or isinstance(
            escalation_sla_minutes, bool
        ):
            raise TypeError("approvals.escalation_sla_minutes must be an integer")
        if escalation_sla_minutes <= 0:
            raise ValueError("approvals.escalation_sla_minutes must be positive")
        return cls(
            default_reviewer=default_reviewer,
            escalation_sla_minutes=escalation_sla_minutes,
        )


def _read_required_approval_string(value: str, *, field: str) -> str:
    normalized = str(value).strip()
    if not normalized:
        raise ValueError(f"Approval field is required: {field}")
    return normalized


def _read_authorization_mode(value: str) -> str:
    authorization_mode = _read_required_approval_string(
        value,
        field="authorization_mode",
    )
    if authorization_mode not in {"platform_owned", "user_delegated", "human_approved"}:
        raise ValueError(f"Authorization mode is not supported: {authorization_mode}")
    return authorization_mode


@dataclass(slots=True)
class ApprovalRequest:
    approval_id: str
    trace_id: str
    capability_name: str
    requested_by: str
    reviewer: str
    reason: str
    session_id: str = ""
    capability_session_id: str = ""
    capability_session_status: str = "pending"
    authorization_mode: str = "platform_owned"
    delegated_principal_id: str = ""
    delegated_scope: str = ""
    status: str = "pending"
    resolution_note: str = ""


class ApprovalQueue:
    def __init__(self, policy: ApprovalPolicy | None = None) -> None:
        self.policy = policy or ApprovalPolicy(
            default_reviewer="manager",
            escalation_sla_minutes=30,
        )
        self._items: list[ApprovalRequest] = []
        self._counter = 0

    def submit(
        self,
        *,
        trace_id: str,
        capability_name: str,
        requested_by: str,
        reviewer: str | None,
        reason: str,
        session_id: str = "",
        authorization_mode: str = "platform_owned",
        delegated_principal_id: str = "",
        delegated_scope: str = "",
    ) -> ApprovalRequest:
        trace_id = _read_required_approval_string(trace_id, field="trace_id")
        capability_name = _read_required_approval_string(
            capability_name,
            field="capability_name",
        )
        requested_by = _read_required_approval_string(requested_by, field="requested_by")
        reason = _read_required_approval_string(reason, field="reason")
        session_id = _read_required_approval_string(session_id, field="session_id")
        reviewer = (
            self.policy.default_reviewer
            if reviewer is None
            else _read_required_approval_string(reviewer, field="reviewer")
        )
        authorization_mode = _read_authorization_mode(authorization_mode)
        delegated_principal_id = str(delegated_principal_id).strip()
        delegated_scope = str(delegated_scope).strip()
        if authorization_mode == "user_delegated":
            delegated_principal_id = _read_required_approval_string(
                delegated_principal_id,
                field="delegated_principal_id",
            )
            delegated_scope = _read_required_approval_string(
                delegated_scope,
                field="delegated_scope",
            )
        self._counter += 1
        request = ApprovalRequest(
            approval_id=f"apr-{self._counter:03d}",
            trace_id=trace_id,
            capability_name=capability_name,
            requested_by=requested_by,
            reviewer=reviewer,
            reason=reason,
            session_id=session_id,
            capability_session_id=f"cap-session-{self._counter:03d}",
            authorization_mode=authorization_mode,
            delegated_principal_id=delegated_principal_id,
            delegated_scope=delegated_scope,
        )
        self._items.append(request)
        return request

    def all(self) -> tuple[ApprovalRequest, ...]:
        return tuple(self._items)

    def pending(self) -> tuple[ApprovalRequest, ...]:
        return tuple(item for item in self._items if item.status == "pending")

    def resolve(self, approval_id: str, *, decision: str, note: str = "") -> ApprovalRequest:
        approval_id = _read_required_approval_string(approval_id, field="approval_id")
        decision = str(decision).strip()
        if decision not in {"approved", "rejected"}:
            raise ValueError(f"Approval decision is not supported: {decision}")
        resolution_note = str(note).strip()
        for item in self._items:
            if item.approval_id == approval_id:
                if item.status != "pending":
                    raise ValueError(f"Approval request is not pending: {approval_id}")
                item.status = decision
                item.capability_session_status = decision
                item.resolution_note = resolution_note
                return item
        raise ValueError(f"Approval request not found: {approval_id}")
