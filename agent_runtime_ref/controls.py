from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from agent_runtime_ref.catalog import CapabilityCatalog
from agent_runtime_ref.identity import ApprovedInventory


@dataclass(frozen=True, slots=True)
class ControlsPolicy:
    required_controls: tuple[str, ...]
    blocked_findings: tuple[str, ...]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ControlsPolicy":
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
            required_controls=tuple(str(item) for item in require),
            blocked_findings=tuple(str(item) for item in block_if),
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
    missing_controls = tuple(
        control for control in policy.required_controls if not observed_controls.get(control, False)
    )
    blocking_findings = list(
        finding for finding in policy.blocked_findings if observed_controls.get(finding, False)
    )
    if inventory_drift.has_drift:
        blocking_findings.append("inventory_drift_present")
    return ControlsAssessment(
        healthy=not missing_controls and not blocking_findings,
        missing_controls=missing_controls,
        blocking_findings=tuple(blocking_findings),
        inventory_drift=inventory_drift,
    )
