from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


def _read_required_string(data: Mapping[str, Any], key: str, *, label: str) -> str:
    value = str(data.get(key, "")).strip()
    if not value:
        raise ValueError(f"{label}.{key} is required")
    return value


@dataclass(frozen=True, slots=True)
class AgentIdentity:
    agent_id: str
    display_name: str
    owner_team: str
    runtime_principal: str


@dataclass(frozen=True, slots=True)
class ApprovedInventory:
    capabilities: frozenset[str]

    def __post_init__(self) -> None:
        capabilities = frozenset(str(capability).strip() for capability in self.capabilities)
        if "" in capabilities:
            raise ValueError("approved_capabilities entries must not be empty")
        object.__setattr__(self, "capabilities", capabilities)

    def allows(self, capability_name: str) -> bool:
        return str(capability_name).strip() in self.capabilities

    @classmethod
    def from_agent_config(cls, data: Mapping[str, Any]) -> "ApprovedInventory":
        raw_agent = data.get("agent", {})
        if not isinstance(raw_agent, Mapping):
            raise TypeError("'agent' must be a mapping")
        raw_inventory = raw_agent.get("approved_capabilities", [])
        if not isinstance(raw_inventory, list):
            raise TypeError("'approved_capabilities' must be a list")
        capabilities = frozenset(str(item).strip() for item in raw_inventory)
        if "" in capabilities:
            raise ValueError("approved_capabilities entries must not be empty")
        return cls(capabilities=capabilities)


def load_agent_identity(data: Mapping[str, Any]) -> AgentIdentity:
    raw_agent = data.get("agent", {})
    if not isinstance(raw_agent, Mapping):
        raise TypeError("'agent' must be a mapping")
    return AgentIdentity(
        agent_id=_read_required_string(raw_agent, "id", label="agent"),
        display_name=_read_required_string(raw_agent, "display_name", label="agent"),
        owner_team=_read_required_string(raw_agent, "owner_team", label="agent"),
        runtime_principal=_read_required_string(
            raw_agent, "runtime_principal", label="agent"
        ),
    )
