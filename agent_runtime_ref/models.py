from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RunRequest:
    user_input: str
    tenant_id: str
    principal_id: str
    trace_id: str


@dataclass(slots=True)
class RunContext:
    tenant_id: str
    principal_id: str
    trace_id: str
    retrieved_context: list[str] = field(default_factory=list)
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
