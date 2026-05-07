from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Any, cast

import yaml

from agent_runtime_ref.approvals import ApprovalPolicy
from agent_runtime_ref.catalog import CapabilityCatalog
from agent_runtime_ref.controls import ControlsPolicy
from agent_runtime_ref.identity import AgentIdentity, ApprovedInventory, load_agent_identity
from agent_runtime_ref.lifecycle import ArtifactBundle, ChangeRecord, RetirementPlan
from agent_runtime_ref.memory import MemoryStore
from agent_runtime_ref.policy import PolicyEngine
from agent_runtime_ref.rollout import RolloutPolicy


def default_config_dir() -> Path:
    return Path(__file__).resolve().parent / "configs"


def _read_config_path(path: object) -> Path:
    if not isinstance(path, (str, PathLike)):
        raise TypeError("Config path must be a string or path-like object")
    return Path(cast(str | PathLike[str], path))


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    config_path = _read_config_path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise TypeError(f"Config at {config_path!s} must be a mapping at the top level")
    return payload


def load_capability_catalog(path: str | Path) -> CapabilityCatalog:
    return CapabilityCatalog.from_dict(load_yaml_file(path))


def load_agent_profile(path: str | Path) -> tuple[AgentIdentity, ApprovedInventory]:
    payload = load_yaml_file(path)
    return load_agent_identity(payload), ApprovedInventory.from_agent_config(payload)


def load_policy_engine(
    path: str | Path,
    *,
    approved_inventory: ApprovedInventory | None = None,
) -> PolicyEngine:
    engine = PolicyEngine.from_dict(load_yaml_file(path))
    if approved_inventory is not None:
        engine.approved_inventory = approved_inventory
    return engine


def load_rollout_policy(path: str | Path) -> RolloutPolicy:
    return RolloutPolicy.from_dict(load_yaml_file(path))


def load_memory_store(path: str | Path) -> MemoryStore:
    return MemoryStore.from_dict(load_yaml_file(path))


def load_controls_policy(path: str | Path) -> ControlsPolicy:
    return ControlsPolicy.from_dict(load_yaml_file(path))


def load_approval_policy(path: str | Path) -> ApprovalPolicy:
    return ApprovalPolicy.from_dict(load_yaml_file(path))


def load_change_record(path: str | Path) -> ChangeRecord:
    return ChangeRecord.from_dict(load_yaml_file(path))


def load_artifact_bundle(path: str | Path) -> ArtifactBundle:
    return ArtifactBundle.from_dict(load_yaml_file(path))


def load_retirement_plan(path: str | Path) -> RetirementPlan:
    return RetirementPlan.from_dict(load_yaml_file(path))
