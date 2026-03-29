from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from agent_runtime_ref.catalog import CapabilityCatalog
from agent_runtime_ref.memory import MemoryStore
from agent_runtime_ref.policy import PolicyEngine
from agent_runtime_ref.rollout import RolloutPolicy


def default_config_dir() -> Path:
    return Path(__file__).resolve().parent / "configs"


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise TypeError(f"Config at {path!s} must be a mapping at the top level")
    return payload


def load_capability_catalog(path: str | Path) -> CapabilityCatalog:
    return CapabilityCatalog.from_dict(load_yaml_file(path))


def load_policy_engine(path: str | Path) -> PolicyEngine:
    return PolicyEngine.from_dict(load_yaml_file(path))


def load_rollout_policy(path: str | Path) -> RolloutPolicy:
    return RolloutPolicy.from_dict(load_yaml_file(path))


def load_memory_store(path: str | Path) -> MemoryStore:
    return MemoryStore.from_dict(load_yaml_file(path))
