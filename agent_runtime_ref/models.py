from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


def normalize_tool_capability_name(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Tool request capability name must be a string")
    capability_name = value.strip()
    if not capability_name:
        raise ValueError("Tool request capability name must not be empty")
    return capability_name


def normalize_tool_arguments(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        raise TypeError("Tool request arguments must be a mapping")
    normalized: dict[str, str] = {}
    for key, argument in value.items():
        if not isinstance(key, str):
            raise TypeError("Tool request argument key must be a string")
        argument_key = key.strip()
        if not argument_key:
            raise ValueError("Tool request argument key must not be empty")
        if argument_key in normalized:
            raise ValueError("Tool request argument keys must be unique")
        if not isinstance(argument, str):
            raise TypeError(
                f"Tool request argument value must be a string: {argument_key}"
            )
        normalized[argument_key] = argument
    return normalized


def normalize_tool_result_status(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Tool result status must be a string")
    status = value.strip()
    if not status:
        raise ValueError("Tool result status must not be empty")
    return status


def normalize_tool_result_payload(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        raise TypeError("Tool result payload must be a mapping")
    normalized: dict[str, str] = {}
    for key, payload_value in value.items():
        if not isinstance(key, str):
            raise TypeError("Tool result payload key must be a string")
        payload_key = key.strip()
        if not payload_key:
            raise ValueError("Tool result payload key must not be empty")
        if payload_key in normalized:
            raise ValueError("Tool result payload keys must be unique")
        if not isinstance(payload_value, str):
            raise TypeError(f"Tool result payload value must be a string: {payload_key}")
        normalized[payload_key] = payload_value
    return normalized


if TYPE_CHECKING:
    from agent_runtime_ref.identity import AgentIdentity
    from agent_runtime_ref.memory import MemoryRecord


@dataclass(slots=True)
class RunRequest:
    user_input: str
    tenant_id: str
    principal_id: str
    trace_id: str
    session_id: str = "session-demo-001"
    agent_id: str = "agent-runtime-ref"
    authorization_mode: str = "platform_owned"
    delegated_principal_id: str = ""
    delegated_scope: str = ""


@dataclass(slots=True)
class RunContext:
    tenant_id: str
    principal_id: str
    trace_id: str
    session_id: str = "session-demo-001"
    agent: "AgentIdentity | None" = None
    context_layers: dict[str, list[str]] = field(default_factory=dict)
    retrieved_context: list[str] = field(default_factory=list)
    retrieved_records: list[MemoryRecord] = field(default_factory=list)
    tool_results: list["ToolResult"] = field(default_factory=list)


@dataclass(slots=True)
class ToolRequest:
    capability_name: str
    arguments: dict[str, str]


@dataclass(slots=True)
class ToolResult:
    capability_name: str
    status: str
    payload: dict[str, str]

    def __post_init__(self) -> None:
        self.capability_name = normalize_tool_capability_name(self.capability_name)
        self.status = normalize_tool_result_status(self.status)
        self.payload = normalize_tool_result_payload(self.payload)


@dataclass(slots=True)
class ModelOutput:
    text: str
    tool_request: ToolRequest | None = None


@dataclass(slots=True)
class RunResult:
    output_text: str
    status: str
