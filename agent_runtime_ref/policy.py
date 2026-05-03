from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from agent_runtime_ref.catalog import CapabilitySpec
from agent_runtime_ref.identity import ApprovedInventory
from agent_runtime_ref.models import RunContext, RunRequest, ToolRequest


def _read_string_list_items(items: list[object], *, label: str) -> set[str]:
    values = {str(item).strip() for item in items}
    if "" in values:
        raise ValueError(f"{label} entries must not be empty")
    return values


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    action: str
    reason: str
    policy_id: str


@dataclass(frozen=True, slots=True)
class CapabilityPolicy:
    decision: str
    approver: str | None = None


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
        self.require_tenant = require_tenant
        self.deny_if_principal_missing = deny_if_principal_missing
        self.capability_policies = dict(capability_policies or {})
        self.allowed_memory_kinds = allowed_memory_kinds or {"validated_fact", "session_summary"}
        self.approved_inventory = approved_inventory
        self.allowed_network_access = allowed_network_access or {"restricted", "brokered"}

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
            capability_name = str(name).strip()
            if not capability_name:
                raise ValueError("Policy capability name must not be empty")
            if not isinstance(raw_entry, Mapping):
                raise TypeError(f"Policy for capability {name!r} must be a mapping")
            decision = str(raw_entry.get("decision", "deny")).strip()
            if decision not in {"allow", "approval_required", "deny"}:
                raise ValueError(f"Policy decision is not supported: {decision}")
            approver = (
                str(raw_entry["approver"]).strip()
                if raw_entry.get("approver") is not None
                else None
            )
            if decision == "approval_required" and approver == "":
                raise ValueError(f"Policy approver must not be empty: {capability_name}")
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
            require_tenant=bool(raw_precheck.get("require_tenant", True)),
            deny_if_principal_missing=bool(
                raw_precheck.get("deny_if_principal_missing", True),
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
        del context
        if self.approved_inventory is not None and not self.approved_inventory.allows(
            tool_request.capability_name,
        ):
            return PolicyDecision("deny", "capability_not_in_inventory", "cap_403")
        if capability is not None:
            if capability.network_access not in self.allowed_network_access:
                return PolicyDecision("deny", "network_access_not_allowed", "cap_405")
            if capability.network_access != "none" and not capability.allowed_egress:
                return PolicyDecision("deny", "egress_policy_missing", "cap_406")
        simulate_failure = tool_request.arguments.get("simulate_failure")
        if tool_request.capability_name == "create_ticket":
            if simulate_failure in {"tool_timeout", "upstream_unavailable"}:
                return PolicyDecision("allow", "failure_drill_execution", "cap_120")
            if tool_request.arguments.get("idempotency_key") in {None, ""}:
                return PolicyDecision("allow", "validation_drill_execution", "cap_121")

        configured = self.capability_policies.get(tool_request.capability_name)
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
        if kind in self.allowed_memory_kinds:
            return PolicyDecision("allow", "memory_kind_allowed", "mem_001")
        return PolicyDecision("deny", "memory_kind_denied", "mem_002")
