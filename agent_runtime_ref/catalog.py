from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CapabilitySpec:
    name: str
    owner: str
    mode: str
    transport: str
    timeout_seconds: int
    approval_required: bool = False
    idempotency_key_required: bool = False


class CapabilityCatalog:
    """Small in-memory capability registry for the reference runtime."""

    def __init__(self) -> None:
        self._registry: dict[str, CapabilitySpec] = {
            "search_docs": CapabilitySpec(
                name="search_docs",
                owner="knowledge_platform",
                mode="read",
                transport="mcp",
                timeout_seconds=5,
            ),
            "create_ticket": CapabilitySpec(
                name="create_ticket",
                owner="support_platform",
                mode="write",
                transport="gateway",
                timeout_seconds=15,
                approval_required=True,
                idempotency_key_required=True,
            ),
        }

    def get(self, name: str) -> CapabilitySpec | None:
        return self._registry.get(name)

    def all(self) -> tuple[CapabilitySpec, ...]:
        return tuple(self._registry.values())
