from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from agent_runtime_ref.catalog import CapabilitySpec
from agent_runtime_ref.identity import ApprovedInventory
from agent_runtime_ref.models import (
    RunContext,
    RunRequest,
    ToolRequest,
    normalize_tool_arguments,
    normalize_tool_capability_name,
)


def _read_string_list_items(items: list[object], *, label: str) -> set[str]:
    values: set[str] = set()
    for item in items:
        if not isinstance(item, str):
            raise TypeError(f"{label} entries must be strings")
        value = item.strip()
        if not value:
            raise ValueError(f"{label} entries must not be empty")
        if value in values:
            raise ValueError(f"{label} entries must be unique")
        values.add(value)
    return values


def _read_bool(value: object, *, label: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"'{label}' must be a boolean")
    return value


def _read_memory_kind(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("Policy memory kind must be a string")
    kind = value.strip()
    if not kind:
        raise ValueError("Policy memory kind must not be empty")
    return kind


def _read_policy_decision(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Policy decision must be a string")
    decision = value.strip()
    if decision not in {"allow", "approval_required", "deny"}:
        raise ValueError(f"Policy decision is not supported: {decision}")
    return decision


def _read_policy_approver(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("Policy approver must be a string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    action: str
    reason: str
    policy_id: str


@dataclass(frozen=True, slots=True)
class CapabilityPolicy:
    decision: str
    approver: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision", _read_policy_decision(self.decision))
        object.__setattr__(self, "approver", _read_policy_approver(self.approver))


class PolicyEngine:
    """Reference policy engine with explicit structured decisions."""

    def __init__(
        self,
        *,
        require_tenant: bool = True,
        deny_if_principal_missing: bool = True,
        capability_policies: Mapping[str, CapabilityPolicy] | None = None,
        allowed_memory_kinds: set[str] | None = None,
        approved_inventory: ApprovedInventory | None = None,
        allowed_network_access: set[str] | None = None,
    ) -> None:
        self.require_tenant = _read_bool(
            require_tenant,
            label="run_precheck.require_tenant",
        )
        self.deny_if_principal_missing = _read_bool(
            deny_if_principal_missing,
            label="run_precheck.deny_if_principal_missing",
        )
        self.capability_policies: dict[str, CapabilityPolicy] = {}
        for name, policy in (capability_policies or {}).items():
            if not isinstance(name, str):
                raise TypeError("Policy capability names must be strings")
            capability_name = name.strip()
            if not capability_name:
                raise ValueError("Policy capability name must not be empty")
            if capability_name in self.capability_policies:
                raise ValueError("Policy capability names must be unique")
            if not isinstance(policy, CapabilityPolicy):
                raise TypeError("Policy capability entries must be CapabilityPolicy")
            if policy.decision == "approval_required" and policy.approver == "":
                raise ValueError(f"Policy approver must not be empty: {capability_name}")
            self.capability_policies[capability_name] = policy
        self.allowed_memory_kinds = _read_string_list_items(
            list(allowed_memory_kinds or {"validated_fact", "session_summary"}),
            label="memory_write.allow_kinds",
        )
        self.approved_inventory = approved_inventory
        self.allowed_network_access = _read_string_list_items(
            list(allowed_network_access or {"restricted", "brokered"}),
            label="execution.allow_network_access",
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PolicyEngine":
        raw_policy = data.get("policy", {})
        if not isinstance(raw_policy, Mapping):
            raise TypeError("'policy' must be a mapping")

        raw_precheck = raw_policy.get("run_precheck", {})
        if not isinstance(raw_precheck, Mapping):
            raise TypeError("'run_precheck' must be a mapping")

        raw_capabilities = raw_policy.get("capabilities", {})
        if not isinstance(raw_capabilities, Mapping):
            raise TypeError("'capabilities' must be a mapping")

        capability_policies: dict[str, CapabilityPolicy] = {}
        for name, raw_entry in raw_capabilities.items():
            if not isinstance(name, str):
                raise TypeError("Policy capability names must be strings")
            capability_name = name.strip()
            if not capability_name:
                raise ValueError("Policy capability name must not be empty")
            if not isinstance(raw_entry, Mapping):
                raise TypeError(f"Policy for capability {name!r} must be a mapping")
            decision = _read_policy_decision(raw_entry.get("decision", "deny"))
            approver = _read_policy_approver(raw_entry.get("approver"))
            if decision == "approval_required" and approver == "":
                raise ValueError(f"Policy approver must not be empty: {capability_name}")
            if capability_name in capability_policies:
                raise ValueError("Policy capability names must be unique")
            capability_policies[capability_name] = CapabilityPolicy(
                decision=decision,
                approver=approver,
            )

        raw_memory = raw_policy.get("memory_write", {})
        if not isinstance(raw_memory, Mapping):
            raise TypeError("'memory_write' must be a mapping")
        allow_kinds = raw_memory.get("allow_kinds", [])
        if not isinstance(allow_kinds, list):
            raise TypeError("'allow_kinds' must be a list")

        raw_execution = raw_policy.get("execution", {})
        if not isinstance(raw_execution, Mapping):
            raise TypeError("'execution' must be a mapping")
        allowed_network_access = raw_execution.get("allow_network_access", [])
        if not isinstance(allowed_network_access, list):
            raise TypeError("'allow_network_access' must be a list")

        return cls(
            require_tenant=_read_bool(
                raw_precheck.get("require_tenant", True),
                label="run_precheck.require_tenant",
            ),
            deny_if_principal_missing=_read_bool(
                raw_precheck.get("deny_if_principal_missing", True),
                label="run_precheck.deny_if_principal_missing",
            ),
            capability_policies=capability_policies,
            allowed_memory_kinds=_read_string_list_items(
                allow_kinds, label="memory_write.allow_kinds"
            ),
            allowed_network_access=_read_string_list_items(
                allowed_network_access, label="execution.allow_network_access"
            ),
        )

    def precheck(self, request: RunRequest) -> PolicyDecision:
        if not isinstance(request, RunRequest):
            raise TypeError("Policy precheck request must be RunRequest")
        if self.require_tenant and not request.tenant_id:
            return PolicyDecision("deny", "tenant_missing", "run_001")
        if self.deny_if_principal_missing and not request.principal_id:
            return PolicyDecision("deny", "principal_missing", "run_002")
        if not request.agent_id:
            return PolicyDecision("deny", "agent_identity_missing", "run_003")
        return PolicyDecision("allow", "run_context_valid", "run_010")

    def evaluate_tool(
        self,
        context: RunContext,
        tool_request: ToolRequest,
        capability: CapabilitySpec | None,
    ) -> PolicyDecision:
        if not isinstance(context, RunContext):
            raise TypeError("Policy context must be RunContext")
        if not isinstance(tool_request, ToolRequest):
            raise TypeError("Policy tool request must be ToolRequest")
        if capability is not None and not isinstance(capability, CapabilitySpec):
            raise TypeError("Policy capability must be CapabilitySpec")
        del context
        capability_name = normalize_tool_capability_name(tool_request.capability_name)
        tool_arguments = normalize_tool_arguments(tool_request.arguments)
        if self.approved_inventory is not None and not self.approved_inventory.allows(
            capability_name,
        ):
            return PolicyDecision("deny", "capability_not_in_inventory", "cap_403")
        if capability is not None:
            if capability.network_access not in self.allowed_network_access:
                return PolicyDecision("deny", "network_access_not_allowed", "cap_405")
            if capability.network_access != "none" and not capability.allowed_egress:
                return PolicyDecision("deny", "egress_policy_missing", "cap_406")
        simulate_failure = tool_arguments.get("simulate_failure")
        if capability_name == "create_ticket":
            if simulate_failure in {"tool_timeout", "upstream_unavailable"}:
                return PolicyDecision("allow", "failure_drill_execution", "cap_120")
            if tool_arguments.get("idempotency_key") in {None, ""}:
                return PolicyDecision("allow", "validation_drill_execution", "cap_121")

        configured = self.capability_policies.get(capability_name)
        if configured is not None:
            if configured.decision == "allow":
                return PolicyDecision("allow", "configured_allow", "cap_110")
            if configured.decision == "approval_required":
                approver = configured.approver or "policy"
                return PolicyDecision("approval_required", f"approver:{approver}", "cap_210")
            return PolicyDecision("deny", "configured_deny", "cap_410")
        if capability is None:
            return PolicyDecision("deny", "capability_unknown", "cap_404")
        if capability.risk_tier == "critical":
            return PolicyDecision("approval_required", "critical_risk_tier", "cap_211")
        if capability.mode == "read":
            return PolicyDecision("allow", "low_risk_read", "cap_101")
        if capability.approval_required:
            return PolicyDecision("approval_required", "write_action", "cap_201")
        if capability.mode == "write":
            return PolicyDecision("allow", "approved_write", "cap_202")
        return PolicyDecision("deny", "unsupported_mode", "cap_999")

    def allow_memory_write(self, kind: str) -> PolicyDecision:
        kind = _read_memory_kind(kind)
        if kind in self.allowed_memory_kinds:
            return PolicyDecision("allow", "memory_kind_allowed", "mem_001")
        return PolicyDecision("deny", "memory_kind_denied", "mem_002")
