from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


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

    def __init__(self, registry: Mapping[str, CapabilitySpec] | None = None) -> None:
        self._registry = dict(registry or self._default_registry())

    @staticmethod
    def _default_registry() -> dict[str, CapabilitySpec]:
        return {
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

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CapabilityCatalog":
        raw_capabilities = data.get("capabilities", {})
        if not isinstance(raw_capabilities, Mapping):
            raise TypeError("'capabilities' must be a mapping")

        registry: dict[str, CapabilitySpec] = {}
        for name, raw_spec in raw_capabilities.items():
            if not isinstance(raw_spec, Mapping):
                raise TypeError(f"Capability spec for {name!r} must be a mapping")
            approval = str(raw_spec.get("approval", "none"))
            registry[str(name)] = CapabilitySpec(
                name=str(name),
                owner=str(raw_spec.get("owner", "unknown_owner")),
                mode=str(raw_spec.get("mode", "read")),
                transport=str(raw_spec.get("transport", "gateway")),
                timeout_seconds=int(raw_spec.get("timeout_seconds", 10)),
                approval_required=approval != "none",
                idempotency_key_required=bool(raw_spec.get("idempotency_key_required", False)),
            )
        return cls(registry=registry)

    def get(self, name: str) -> CapabilitySpec | None:
        return self._registry.get(name)

    def all(self) -> tuple[CapabilitySpec, ...]:
        return tuple(self._registry.values())
