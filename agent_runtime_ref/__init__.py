"""Minimal reference runtime package for the book."""

from agent_runtime_ref.catalog import CapabilityCatalog, CapabilitySpec
from agent_runtime_ref.controls import ControlsAssessment, ControlsPolicy
from agent_runtime_ref.identity import AgentIdentity, ApprovedInventory
from agent_runtime_ref.models import (
    ModelOutput,
    RunContext,
    RunRequest,
    RunResult,
    ToolRequest,
    ToolResult,
)
from agent_runtime_ref.policy import PolicyDecision, PolicyEngine
from agent_runtime_ref.rollout import RolloutReadiness, ready_for_rollout
from agent_runtime_ref.runtime import AgentRuntime

__all__ = [
    "AgentRuntime",
    "AgentIdentity",
    "ApprovedInventory",
    "CapabilityCatalog",
    "CapabilitySpec",
    "ControlsAssessment",
    "ControlsPolicy",
    "ModelOutput",
    "PolicyDecision",
    "PolicyEngine",
    "RolloutReadiness",
    "RunContext",
    "RunRequest",
    "RunResult",
    "ToolRequest",
    "ToolResult",
    "ready_for_rollout",
]
