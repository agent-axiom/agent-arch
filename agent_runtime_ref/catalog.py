from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, cast


def _normalize_string_list_items(
    items: list[object] | tuple[str, ...],
    *,
    label: str,
) -> tuple[str, ...]:
    values = tuple(str(item).strip() for item in items)
    if any(not value for value in values):
        raise ValueError(f"{label} entries must not be empty")
    return values


def _read_string_list_items(items: object, *, label: str) -> tuple[str, ...]:
    if not isinstance(items, list):
        raise TypeError(f"'{label}' must be a list")
    return _normalize_string_list_items(cast(list[object], items), label=label)


def _normalize_required_string(value: object, *, label: str) -> str:
    normalized = str(value).strip()
    if not normalized:
        raise ValueError(f"{label} is required")
    return normalized


def _read_required_string(spec: Mapping[str, Any], key: str, *, label: str) -> str:
    return _normalize_required_string(spec.get(key, ""), label=f"{label}.{key}")


def _read_positive_int(spec: Mapping[str, Any], key: str, *, label: str) -> int:
    value = spec.get(key, 10)
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"'{label}.{key}' must be an integer")
    if value < 1:
        raise ValueError(f"{label}.{key} must be positive")
    return value


def _read_bool(spec: Mapping[str, Any], key: str, *, label: str) -> bool:
    value = spec.get(key, False)
    if not isinstance(value, bool):
        raise TypeError(f"'{label}.{key}' must be a boolean")
    return value


def _read_approval(spec: Mapping[str, Any], *, label: str) -> str:
    approval = str(spec.get("approval", "none")).strip()
    if not approval:
        raise ValueError(f"{label}.approval must not be empty")
    if approval not in {"none", "manager"}:
        raise ValueError(f"{label}.approval is not supported: {approval}")
    return approval


@dataclass(frozen=True, slots=True)
class CapabilitySpec:
    name: str
    owner: str
    mode: str
    transport: str
    timeout_seconds: int
    tool_principal: str
    risk_tier: str
    network_access: str
    allowed_egress: tuple[str, ...]
    approval_required: bool = False
    idempotency_key_required: bool = False

    def __post_init__(self) -> None:
        for field in (
            "name",
            "owner",
            "mode",
            "transport",
            "tool_principal",
            "risk_tier",
            "network_access",
        ):
            object.__setattr__(
                self,
                field,
                _normalize_required_string(
                    getattr(self, field),
                    label=f"capability.{field}",
                ),
            )
        object.__setattr__(
            self,
            "allowed_egress",
            _normalize_string_list_items(self.allowed_egress, label="allowed_egress"),
        )


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
                tool_principal="svc-knowledge-reader",
                risk_tier="low",
                network_access="restricted",
                allowed_egress=("docs.internal",),
            ),
            "create_ticket": CapabilitySpec(
                name="create_ticket",
                owner="support_platform",
                mode="write",
                transport="gateway",
                timeout_seconds=15,
                tool_principal="svc-ticket-writer",
                risk_tier="high",
                network_access="brokered",
                allowed_egress=("tickets.internal",),
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
            capability_name = str(name).strip()
            if not capability_name:
                raise ValueError("Capability name must not be empty")
            if not isinstance(raw_spec, Mapping):
                raise TypeError(f"Capability spec for {name!r} must be a mapping")
            label = f"capabilities.{capability_name}"
            approval = _read_approval(raw_spec, label=label)
            registry[capability_name] = CapabilitySpec(
                name=capability_name,
                owner=_read_required_string(raw_spec, "owner", label=label),
                mode=_read_required_string(raw_spec, "mode", label=label),
                transport=_read_required_string(raw_spec, "transport", label=label),
                timeout_seconds=_read_positive_int(
                    raw_spec, "timeout_seconds", label=label
                ),
                tool_principal=_read_required_string(
                    raw_spec, "tool_principal", label=label
                ),
                risk_tier=_read_required_string(raw_spec, "risk_tier", label=label),
                network_access=_read_required_string(
                    raw_spec, "network_access", label=label
                ),
                allowed_egress=_read_string_list_items(
                    raw_spec.get("allowed_egress", []), label="allowed_egress"
                ),
                approval_required=approval != "none",
                idempotency_key_required=_read_bool(
                    raw_spec, "idempotency_key_required", label=label
                ),
            )
        return cls(registry=registry)

    def get(self, name: str) -> CapabilitySpec | None:
        capability_name = str(name).strip()
        if not capability_name:
            raise ValueError("Tool request capability name must not be empty")
        return self._registry.get(capability_name)

    def all(self) -> tuple[CapabilitySpec, ...]:
        return tuple(self._registry.values())
