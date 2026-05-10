from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class DelegatedAuthorizationPolicy:
    reviewer_required_for_user_delegation: str = "manager"
    require_principal_binding: bool = True
    require_scope_visibility: bool = True
    on_scope_revoked: str = "cancel_or_reapprove"
    subagent_inheritance: str = "explicit_only"

    def __post_init__(self) -> None:
        reviewer = _read_required_approval_string(
            self.reviewer_required_for_user_delegation,
            field="delegated_authorization.reviewer_required_for_user_delegation",
        )
        on_scope_revoked = _read_required_approval_string(
            self.on_scope_revoked,
            field="delegated_authorization.on_scope_revoked",
        )
        subagent_inheritance = _read_required_approval_string(
            self.subagent_inheritance,
            field="delegated_authorization.subagent_inheritance",
        )
        if not isinstance(self.require_principal_binding, bool):
            raise TypeError(
                "delegated_authorization.require_principal_binding must be a boolean"
            )
        if not isinstance(self.require_scope_visibility, bool):
            raise TypeError(
                "delegated_authorization.require_scope_visibility must be a boolean"
            )
        object.__setattr__(self, "reviewer_required_for_user_delegation", reviewer)
        object.__setattr__(self, "on_scope_revoked", on_scope_revoked)
        object.__setattr__(self, "subagent_inheritance", subagent_inheritance)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "DelegatedAuthorizationPolicy":
        if not isinstance(data, Mapping):
            raise TypeError("approvals.delegated_authorization must be a mapping")
        return cls(
            reviewer_required_for_user_delegation=data.get(
                "reviewer_required_for_user_delegation",
                "manager",
            ),
            require_principal_binding=data.get("require_principal_binding", True),
            require_scope_visibility=data.get("require_scope_visibility", True),
            on_scope_revoked=data.get("on_scope_revoked", "cancel_or_reapprove"),
            subagent_inheritance=data.get("subagent_inheritance", "explicit_only"),
        )


@dataclass(frozen=True, slots=True)
class ApprovalPolicy:
    default_reviewer: str
    escalation_sla_minutes: int
    delegated_authorization: DelegatedAuthorizationPolicy = field(
        default_factory=DelegatedAuthorizationPolicy
    )

    def __post_init__(self) -> None:
        if not isinstance(self.default_reviewer, str):
            raise TypeError("approvals.default_reviewer must be a string")
        default_reviewer = self.default_reviewer.strip()
        if not default_reviewer:
            raise ValueError("approvals.default_reviewer is required")
        if not isinstance(self.escalation_sla_minutes, int) or isinstance(
            self.escalation_sla_minutes, bool
        ):
            raise TypeError("approvals.escalation_sla_minutes must be an integer")
        if self.escalation_sla_minutes <= 0:
            raise ValueError("approvals.escalation_sla_minutes must be positive")
        if not isinstance(self.delegated_authorization, DelegatedAuthorizationPolicy):
            raise TypeError(
                "approvals.delegated_authorization must be DelegatedAuthorizationPolicy"
            )
        object.__setattr__(self, "default_reviewer", default_reviewer)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ApprovalPolicy":
        if not isinstance(data, Mapping):
            raise TypeError("Approval policy config must be a mapping")
        raw_approvals = data.get("approvals", {})
        if not isinstance(raw_approvals, Mapping):
            raise TypeError("'approvals' must be a mapping")
        raw_delegated_authorization = raw_approvals.get("delegated_authorization", {})
        return cls(
            default_reviewer=raw_approvals.get("default_reviewer", "manager"),
            escalation_sla_minutes=raw_approvals.get("escalation_sla_minutes", 30),
            delegated_authorization=DelegatedAuthorizationPolicy.from_dict(
                raw_delegated_authorization
            ),
        )


def _read_optional_approval_string(value: str, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Approval field must be a string: {field}")
    return value.strip()


def _read_required_approval_string(value: str, *, field: str) -> str:
    normalized = _read_optional_approval_string(value, field=field)
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


def _read_approval_status(value: str, *, field: str) -> str:
    status = _read_required_approval_string(value, field=field)
    if status not in {"pending", "approved", "rejected"}:
        raise ValueError(f"Approval status is not supported: {status}")
    return status


@dataclass(slots=True)
class ApprovalRequest:
    approval_id: str
    trace_id: str
    capability_name: str
    requested_by: str
    reviewer: str
    reason: str
    tenant_id: str = ""
    agent_id: str = ""
    session_id: str = ""
    capability_session_id: str = ""
    capability_session_status: str = "pending"
    authorization_mode: str = "platform_owned"
    delegated_principal_id: str = ""
    delegated_scope: str = ""
    idempotency_key: str = ""
    status: str = "pending"
    resolution_note: str = ""

    def __post_init__(self) -> None:
        self.approval_id = _read_required_approval_string(
            self.approval_id,
            field="approval_id",
        )
        self.trace_id = _read_required_approval_string(self.trace_id, field="trace_id")
        self.tenant_id = _read_optional_approval_string(
            self.tenant_id,
            field="tenant_id",
        )
        self.agent_id = _read_optional_approval_string(
            self.agent_id,
            field="agent_id",
        )
        self.capability_name = _read_required_approval_string(
            self.capability_name,
            field="capability_name",
        )
        self.requested_by = _read_required_approval_string(
            self.requested_by,
            field="requested_by",
        )
        self.reviewer = _read_required_approval_string(self.reviewer, field="reviewer")
        self.reason = _read_required_approval_string(self.reason, field="reason")
        self.session_id = _read_optional_approval_string(
            self.session_id,
            field="session_id",
        )
        self.capability_session_id = _read_optional_approval_string(
            self.capability_session_id,
            field="capability_session_id",
        )
        self.capability_session_status = _read_approval_status(
            self.capability_session_status,
            field="capability_session_status",
        )
        self.authorization_mode = _read_authorization_mode(self.authorization_mode)
        self.delegated_principal_id = _read_optional_approval_string(
            self.delegated_principal_id,
            field="delegated_principal_id",
        )
        self.delegated_scope = _read_optional_approval_string(
            self.delegated_scope,
            field="delegated_scope",
        )
        self.idempotency_key = _read_optional_approval_string(
            self.idempotency_key,
            field="idempotency_key",
        )
        if self.authorization_mode == "user_delegated":
            self.delegated_principal_id = _read_required_approval_string(
                self.delegated_principal_id,
                field="delegated_principal_id",
            )
            self.delegated_scope = _read_required_approval_string(
                self.delegated_scope,
                field="delegated_scope",
            )
        self.status = _read_approval_status(self.status, field="status")
        self.resolution_note = _read_optional_approval_string(
            self.resolution_note,
            field="resolution_note",
        )


class ApprovalQueue:
    def __init__(self, policy: ApprovalPolicy | None = None) -> None:
        if policy is None:
            policy = ApprovalPolicy(
                default_reviewer="manager",
                escalation_sla_minutes=30,
            )
        if not isinstance(policy, ApprovalPolicy):
            raise TypeError("Approval queue policy must be ApprovalPolicy")
        self.policy = policy
        self._items: list[ApprovalRequest] = []
        self._counter = 0

    def submit(
        self,
        *,
        trace_id: str,
        capability_name: str,
        requested_by: str,
        tenant_id: str = "",
        agent_id: str = "",
        reviewer: str | None,
        reason: str,
        session_id: str = "",
        authorization_mode: str = "platform_owned",
        delegated_principal_id: str = "",
        delegated_scope: str = "",
        idempotency_key: str = "",
    ) -> ApprovalRequest:
        trace_id = _read_required_approval_string(trace_id, field="trace_id")
        capability_name = _read_required_approval_string(
            capability_name,
            field="capability_name",
        )
        requested_by = _read_required_approval_string(requested_by, field="requested_by")
        tenant_id = _read_optional_approval_string(tenant_id, field="tenant_id")
        agent_id = _read_optional_approval_string(agent_id, field="agent_id")
        reason = _read_required_approval_string(reason, field="reason")
        session_id = _read_required_approval_string(session_id, field="session_id")
        reviewer = (
            self.policy.default_reviewer
            if reviewer is None
            else _read_required_approval_string(reviewer, field="reviewer")
        )
        authorization_mode = _read_authorization_mode(authorization_mode)
        delegated_principal_id = _read_optional_approval_string(
            delegated_principal_id,
            field="delegated_principal_id",
        )
        delegated_scope = _read_optional_approval_string(
            delegated_scope,
            field="delegated_scope",
        )
        idempotency_key = _read_optional_approval_string(
            idempotency_key,
            field="idempotency_key",
        )
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
            tenant_id=tenant_id,
            agent_id=agent_id,
            capability_name=capability_name,
            requested_by=requested_by,
            reviewer=reviewer,
            reason=reason,
            session_id=session_id,
            capability_session_id=f"cap-session-{self._counter:03d}",
            authorization_mode=authorization_mode,
            delegated_principal_id=delegated_principal_id,
            delegated_scope=delegated_scope,
            idempotency_key=idempotency_key,
        )
        self._items.append(request)
        return request

    def all(self) -> tuple[ApprovalRequest, ...]:
        return tuple(self._items)

    def pending(self) -> tuple[ApprovalRequest, ...]:
        return tuple(item for item in self._items if item.status == "pending")

    def resolve(self, approval_id: str, *, decision: str, note: str = "") -> ApprovalRequest:
        approval_id = _read_required_approval_string(approval_id, field="approval_id")
        decision = _read_required_approval_string(decision, field="decision")
        if decision not in {"approved", "rejected"}:
            raise ValueError(f"Approval decision is not supported: {decision}")
        resolution_note = _read_optional_approval_string(note, field="note")
        for item in self._items:
            if item.approval_id == approval_id:
                if item.status != "pending":
                    raise ValueError(f"Approval request is not pending: {approval_id}")
                item.status = decision
                item.capability_session_status = decision
                item.resolution_note = resolution_note
                return item
        raise ValueError(f"Approval request not found: {approval_id}")
