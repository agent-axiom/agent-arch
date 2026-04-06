from __future__ import annotations

from agent_runtime_ref.catalog import CapabilitySpec
from agent_runtime_ref.models import ToolRequest, ToolResult
from agent_runtime_ref.policy import PolicyDecision


def execute_tool(
    capability: CapabilitySpec,
    tool_request: ToolRequest,
    decision: PolicyDecision,
) -> ToolResult:
    if decision.action == "deny":
        return ToolResult(
            capability_name=tool_request.capability_name,
            status="denied",
            payload={"reason": decision.reason},
        )
    if decision.action == "approval_required":
        return ToolResult(
            capability_name=tool_request.capability_name,
            status="approval_required",
            payload={"reason": decision.reason},
        )
    if capability.idempotency_key_required and "idempotency_key" not in tool_request.arguments:
        return ToolResult(
            capability_name=tool_request.capability_name,
            status="validation_failure",
            payload={"reason": "missing_idempotency_key"},
        )

    payload = {
        "transport": capability.transport,
        "mode": capability.mode,
        "owner": capability.owner,
        "tool_principal": capability.tool_principal,
        "risk_tier": capability.risk_tier,
        "network_access": capability.network_access,
        "allowed_egress": ",".join(capability.allowed_egress),
    }
    return ToolResult(
        capability_name=tool_request.capability_name,
        status="success",
        payload=payload,
    )
