from __future__ import annotations

from dataclasses import dataclass

from agent_runtime_ref.catalog import CapabilitySpec
from agent_runtime_ref.models import RunContext, RunRequest, ToolRequest


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    action: str
    reason: str
    policy_id: str


class PolicyEngine:
    """Reference policy engine with explicit structured decisions."""

    def precheck(self, request: RunRequest) -> PolicyDecision:
        if not request.tenant_id:
            return PolicyDecision("deny", "tenant_missing", "run_001")
        if not request.principal_id:
            return PolicyDecision("deny", "principal_missing", "run_002")
        return PolicyDecision("allow", "run_context_valid", "run_010")

    def evaluate_tool(
        self,
        context: RunContext,
        tool_request: ToolRequest,
        capability: CapabilitySpec | None,
    ) -> PolicyDecision:
        if capability is None:
            return PolicyDecision("deny", "capability_unknown", "cap_404")
        if capability.mode == "read":
            return PolicyDecision("allow", "low_risk_read", "cap_101")
        if capability.approval_required:
            return PolicyDecision("approval_required", "write_action", "cap_201")
        if capability.mode == "write":
            return PolicyDecision("allow", "approved_write", "cap_202")
        return PolicyDecision("deny", "unsupported_mode", "cap_999")

    def allow_memory_write(self, kind: str) -> PolicyDecision:
        if kind in {"validated_fact", "session_summary"}:
            return PolicyDecision("allow", "memory_kind_allowed", "mem_001")
        return PolicyDecision("deny", "memory_kind_denied", "mem_002")
