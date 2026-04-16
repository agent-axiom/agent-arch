from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

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


@dataclass(slots=True)
class ModelOutput:
    text: str
    tool_request: ToolRequest | None = None


@dataclass(slots=True)
class RunResult:
    output_text: str
    status: str
