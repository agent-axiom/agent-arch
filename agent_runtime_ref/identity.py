from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


def _read_required_string(data: Mapping[str, Any], key: str, *, label: str) -> str:
    value = data.get(key, "")
    if not isinstance(value, str):
        raise TypeError(f"{label}.{key} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{label}.{key} is required")
    return normalized


def _normalize_approved_capabilities(items: Iterable[object]) -> frozenset[str]:
    capabilities: set[str] = set()
    for item in items:
        if not isinstance(item, str):
            raise TypeError("approved_capabilities entries must be strings")
        capability = item.strip()
        if not capability:
            raise ValueError("approved_capabilities entries must not be empty")
        if capability in capabilities:
            raise ValueError("approved_capabilities entries must be unique")
        capabilities.add(capability)
    return frozenset(capabilities)


@dataclass(frozen=True, slots=True)
class AgentIdentity:
    agent_id: str
    display_name: str
    owner_team: str
    runtime_principal: str

    def __post_init__(self) -> None:
        fields = {
            "agent_id": "id",
            "display_name": "display_name",
            "owner_team": "owner_team",
            "runtime_principal": "runtime_principal",
        }
        for attr, key in fields.items():
            object.__setattr__(
                self,
                attr,
                _read_required_string({key: getattr(self, attr)}, key, label="agent"),
            )


@dataclass(frozen=True, slots=True)
class ApprovedInventory:
    capabilities: frozenset[str]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "capabilities",
            _normalize_approved_capabilities(self.capabilities),
        )

    def allows(self, capability_name: str) -> bool:
        if not isinstance(capability_name, str):
            raise TypeError("approved_capabilities lookup must be a string")
        return capability_name.strip() in self.capabilities

    @classmethod
    def from_agent_config(cls, data: Mapping[str, Any]) -> "ApprovedInventory":
        if not isinstance(data, Mapping):
            raise TypeError("Agent inventory config must be a mapping")
        raw_agent = data.get("agent", {})
        if not isinstance(raw_agent, Mapping):
            raise TypeError("'agent' must be a mapping")
        raw_inventory = raw_agent.get("approved_capabilities", [])
        if not isinstance(raw_inventory, list):
            raise TypeError("'approved_capabilities' must be a list")
        return cls(capabilities=_normalize_approved_capabilities(raw_inventory))


def load_agent_identity(data: Mapping[str, Any]) -> AgentIdentity:
    if not isinstance(data, Mapping):
        raise TypeError("Agent identity config must be a mapping")
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
