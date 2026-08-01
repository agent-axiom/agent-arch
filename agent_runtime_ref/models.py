from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from agent_runtime_ref.states import (
    validate_capability_outcome,
    validate_run_status,
    validate_side_effect_status,
)

REDACTED_INPUT_DESCRIPTION = "[REDACTED]"


def compute_input_sha256(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("User input must be a string")
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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
            raise TypeError(f"Tool request argument value must be a string: {argument_key}")
        normalized[argument_key] = argument
    return normalized


def _normalize_action_digest_field(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Tool action digest field must be a string: {field}")
    return value.strip()


def compute_action_digest(
    *,
    capability_name: object,
    arguments: object,
    tenant_id: object,
    agent_id: object,
    session_id: object,
    idempotency_key: object,
    principal_id: object = "",
    authorization_mode: object = "",
    delegated_principal_id: object = "",
    delegated_scope: object = "",
    policy_version: object = "",
    capability_version: object = "",
    expires_at: object = "",
    nonce: object = "",
) -> str:
    capability = normalize_tool_capability_name(capability_name)
    normalized_arguments = normalize_tool_arguments(arguments)
    canonical_payload = {
        "agent_id": _normalize_action_digest_field(agent_id, field="agent_id"),
        "arguments": dict(sorted(normalized_arguments.items())),
        "capability": capability,
        "idempotency_key": _normalize_action_digest_field(
            idempotency_key,
            field="idempotency_key",
        ),
        "principal_id": _normalize_action_digest_field(
            principal_id,
            field="principal_id",
        ),
        "authorization_mode": _normalize_action_digest_field(
            authorization_mode,
            field="authorization_mode",
        ),
        "delegated_principal_id": _normalize_action_digest_field(
            delegated_principal_id,
            field="delegated_principal_id",
        ),
        "delegated_scope": _normalize_action_digest_field(
            delegated_scope,
            field="delegated_scope",
        ),
        "policy_version": _normalize_action_digest_field(
            policy_version,
            field="policy_version",
        ),
        "capability_version": _normalize_action_digest_field(
            capability_version,
            field="capability_version",
        ),
        "expires_at": _normalize_action_digest_field(
            expires_at,
            field="expires_at",
        ),
        "nonce": _normalize_action_digest_field(nonce, field="nonce"),
        "session_id": _normalize_action_digest_field(session_id, field="session_id"),
        "tenant_id": _normalize_action_digest_field(tenant_id, field="tenant_id"),
    }
    canonical_json = json.dumps(
        canonical_payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def normalize_tool_result_status(value: object) -> str:
    return validate_capability_outcome(value)


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
    intent_id: str = ""
    test_fault: str = ""


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
    side_effect_status: str = "not_executed"

    def __post_init__(self) -> None:
        self.capability_name = normalize_tool_capability_name(self.capability_name)
        self.status = normalize_tool_result_status(self.status)
        self.payload = normalize_tool_result_payload(self.payload)
        self.side_effect_status = validate_side_effect_status(self.side_effect_status)

    @property
    def outcome(self) -> str:
        return self.status


@dataclass(slots=True)
class ModelOutput:
    text: str
    tool_request: ToolRequest | None = None
    reasoning_summary: str = ""
    reasoning_reference: str = ""
    encrypted_reasoning_item: str = ""


@dataclass(slots=True)
class RunResult:
    output_text: str
    status: str
    task_success: bool | None = None
    side_effect_status: str = "not_executed"

    def __post_init__(self) -> None:
        self.status = validate_run_status(self.status)
        self.side_effect_status = validate_side_effect_status(self.side_effect_status)
