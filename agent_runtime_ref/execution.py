from __future__ import annotations

from agent_runtime_ref.catalog import CapabilitySpec
from agent_runtime_ref.models import (
    ToolRequest,
    ToolResult,
    normalize_tool_arguments,
    normalize_tool_capability_name,
)
from agent_runtime_ref.policy import PolicyDecision


def _read_policy_action(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Policy action must be a string")
    action = value.strip()
    if action not in {"allow", "approval_required", "deny"}:
        raise ValueError(f"Policy action is not supported: {action}")
    return action


def execute_tool(
    capability: CapabilitySpec,
    tool_request: ToolRequest,
    decision: PolicyDecision,
) -> ToolResult:
    if not isinstance(capability, CapabilitySpec):
        raise TypeError("Tool capability must be CapabilitySpec")
    if not isinstance(tool_request, ToolRequest):
        raise TypeError("Tool request must be ToolRequest")
    if not isinstance(decision, PolicyDecision):
        raise TypeError("Tool policy decision must be PolicyDecision")
    capability_name = normalize_tool_capability_name(tool_request.capability_name)
    arguments = normalize_tool_arguments(tool_request.arguments)
    if capability_name != capability.name:
        raise ValueError(
            "Tool request capability does not match catalog entry: "
            f"{capability_name} != {capability.name}"
        )
    action = _read_policy_action(decision.action)
    if action == "deny":
        return ToolResult(
            capability_name=capability_name,
            status="denied",
            payload={"reason": decision.reason},
        )
    if action == "approval_required":
        return ToolResult(
            capability_name=capability_name,
            status="approval_required",
            payload={"reason": decision.reason},
        )
    if capability.idempotency_key_required and "idempotency_key" not in arguments:
        return ToolResult(
            capability_name=capability_name,
            status="validation_failure",
            payload={"reason": "missing_idempotency_key"},
        )
    if arguments.get("simulate_failure") == "tool_timeout":
        return ToolResult(
            capability_name=capability_name,
            status="failed",
            payload={"reason": "tool_timeout"},
        )
    if arguments.get("simulate_failure") == "upstream_unavailable":
        return ToolResult(
            capability_name=capability_name,
            status="failed",
            payload={"reason": "upstream_unavailable"},
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
        capability_name=capability_name,
        status="success",
        payload=payload,
    )
