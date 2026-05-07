from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Mapping

from agent_runtime_ref.catalog import CapabilityCatalog
from agent_runtime_ref.identity import ApprovedInventory


def _read_string_list_items(items: object, *, label: str) -> tuple[str, ...]:
    if not isinstance(items, Sequence) or isinstance(items, str):
        raise TypeError(f"{label} entries must be strings")
    values: list[str] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, str):
            raise TypeError(f"{label} entries must be strings")
        value = item.strip()
        if not value:
            raise ValueError(f"{label} entries must not be empty")
        if value in seen:
            raise ValueError(f"{label} entries must be unique")
        seen.add(value)
        values.append(value)
    return tuple(values)


def _read_observed_flags(items: Mapping[str, bool]) -> dict[str, bool]:
    if not isinstance(items, Mapping):
        raise TypeError("Assessment signals must be a mapping")
    observed: dict[str, bool] = {}
    for key, value in items.items():
        if not isinstance(key, str):
            raise TypeError("Assessment signal key must be a string")
        field = key.strip()
        if not field:
            raise ValueError("Assessment signal key must not be empty")
        if field in observed:
            raise ValueError("Assessment signal keys must be unique")
        if not isinstance(value, bool):
            raise TypeError(f"Assessment signal value must be a boolean: {field}")
        observed[field] = value
    return observed


@dataclass(frozen=True, slots=True)
class ControlsPolicy:
    required_controls: tuple[str, ...]
    blocked_findings: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "required_controls",
            _read_string_list_items(
                self.required_controls,
                label="controls.require",
            ),
        )
        object.__setattr__(
            self,
            "blocked_findings",
            _read_string_list_items(
                self.blocked_findings,
                label="controls.block_if",
            ),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ControlsPolicy":
        if not isinstance(data, Mapping):
            raise TypeError("Controls policy config must be a mapping")
        raw_controls = data.get("controls", {})
        if not isinstance(raw_controls, Mapping):
            raise TypeError("'controls' must be a mapping")
        require = raw_controls.get("require", [])
        block_if = raw_controls.get("block_if", [])
        if not isinstance(require, list):
            raise TypeError("'controls.require' must be a list")
        if not isinstance(block_if, list):
            raise TypeError("'controls.block_if' must be a list")
        return cls(
            required_controls=_read_string_list_items(require, label="controls.require"),
            blocked_findings=_read_string_list_items(block_if, label="controls.block_if"),
        )


@dataclass(frozen=True, slots=True)
class InventoryDrift:
    missing_from_catalog: tuple[str, ...]
    missing_from_inventory: tuple[str, ...]

    @property
    def has_drift(self) -> bool:
        return bool(self.missing_from_catalog or self.missing_from_inventory)


@dataclass(frozen=True, slots=True)
class ControlsAssessment:
    healthy: bool
    missing_controls: tuple[str, ...]
    blocking_findings: tuple[str, ...]
    inventory_drift: InventoryDrift


def assess_inventory_drift(
    approved_inventory: ApprovedInventory,
    catalog: CapabilityCatalog,
) -> InventoryDrift:
    if not isinstance(approved_inventory, ApprovedInventory):
        raise TypeError("Controls inventory must be ApprovedInventory")
    if not isinstance(catalog, CapabilityCatalog):
        raise TypeError("Controls catalog must be CapabilityCatalog")
    approved = set(approved_inventory.capabilities)
    catalog_names = {spec.name for spec in catalog.all()}
    return InventoryDrift(
        missing_from_catalog=tuple(sorted(approved - catalog_names)),
        missing_from_inventory=tuple(sorted(catalog_names - approved)),
    )


def assess_controls(
    policy: ControlsPolicy,
    observed_controls: Mapping[str, bool],
    *,
    inventory_drift: InventoryDrift,
) -> ControlsAssessment:
    if not isinstance(policy, ControlsPolicy):
        raise TypeError("Controls policy must be ControlsPolicy")
    if not isinstance(inventory_drift, InventoryDrift):
        raise TypeError("Controls inventory_drift must be InventoryDrift")
    observed = _read_observed_flags(observed_controls)
    missing_controls = tuple(
        control for control in policy.required_controls if not observed.get(control, False)
    )
    blocking_findings = list(
        finding for finding in policy.blocked_findings if observed.get(finding, False)
    )
    if inventory_drift.has_drift:
        blocking_findings.append("inventory_drift_present")
    return ControlsAssessment(
        healthy=not missing_controls and not blocking_findings,
        missing_controls=missing_controls,
        blocking_findings=tuple(blocking_findings),
        inventory_drift=inventory_drift,
    )
