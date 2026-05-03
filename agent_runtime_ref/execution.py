from __future__ import annotations

from agent_runtime_ref.catalog import CapabilitySpec
from agent_runtime_ref.models import ToolRequest, ToolResult
from agent_runtime_ref.policy import PolicyDecision


def _read_tool_capability_name(value: str) -> str:
    capability_name = str(value).strip()
    if not capability_name:
        raise ValueError("Tool request capability name must not be empty")
    return capability_name


def _read_tool_arguments(value: dict[str, str]) -> dict[str, str]:
    if not isinstance(value, dict):
        raise TypeError("Tool request arguments must be a mapping")
    return {str(key): str(argument) for key, argument in value.items()}


def execute_tool(
    capability: CapabilitySpec,
    tool_request: ToolRequest,
    decision: PolicyDecision,
) -> ToolResult:
    capability_name = _read_tool_capability_name(tool_request.capability_name)
    arguments = _read_tool_arguments(tool_request.arguments)
    if capability_name != capability.name:
        raise ValueError(
            "Tool request capability does not match catalog entry: "
            f"{capability_name} != {capability.name}"
        )
    action = decision.action.strip()
    if action not in {"allow", "approval_required", "deny"}:
        raise ValueError(f"Policy action is not supported: {action}")
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
