from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class AgentIdentity:
    agent_id: str
    display_name: str
    owner_team: str
    runtime_principal: str


@dataclass(frozen=True, slots=True)
class ApprovedInventory:
    capabilities: frozenset[str]

    def allows(self, capability_name: str) -> bool:
        return capability_name in self.capabilities

    @classmethod
    def from_agent_config(cls, data: Mapping[str, Any]) -> "ApprovedInventory":
        raw_agent = data.get("agent", {})
        if not isinstance(raw_agent, Mapping):
            raise TypeError("'agent' must be a mapping")
        raw_inventory = raw_agent.get("approved_capabilities", [])
        if not isinstance(raw_inventory, list):
            raise TypeError("'approved_capabilities' must be a list")
        return cls(capabilities=frozenset(str(item) for item in raw_inventory))


def load_agent_identity(data: Mapping[str, Any]) -> AgentIdentity:
    raw_agent = data.get("agent", {})
    if not isinstance(raw_agent, Mapping):
        raise TypeError("'agent' must be a mapping")
    return AgentIdentity(
        agent_id=str(raw_agent.get("id", "agent-runtime-ref")),
        display_name=str(raw_agent.get("display_name", "Reference Runtime")),
        owner_team=str(raw_agent.get("owner_team", "agent_platform")),
        runtime_principal=str(raw_agent.get("runtime_principal", "svc-agent-runtime-ref")),
    )
