from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def config_dir() -> Path:
    return Path("agent_runtime_ref/configs")


@pytest.fixture
def runtime_from_config(config_dir: Path):
    from agent_runtime_ref.config import (
        load_agent_profile,
        load_capability_catalog,
        load_memory_store,
        load_policy_engine,
    )
    from agent_runtime_ref.runtime import AgentRuntime

    catalog = load_capability_catalog(config_dir / "capabilities.yaml")
    memory = load_memory_store(config_dir / "memory.yaml")
    agent, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
    policy = load_policy_engine(
        config_dir / "policy.yaml",
        approved_inventory=approved_inventory,
    )
    return AgentRuntime(catalog=catalog, policy=policy, memory=memory, agent=agent)


@pytest.fixture
def cli_json(capsys: pytest.CaptureFixture[str]):
    from agent_runtime_ref.__main__ import main

    def run(args: list[str]) -> tuple[int, dict[str, Any]]:
        exit_code = main(args)
        payload = json.loads(capsys.readouterr().out)
        return exit_code, payload

    return run
