from __future__ import annotations

import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_complexity_suppressions_are_protected() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert {"C901", "PLR0912"} <= set(project["tool"]["ruff"]["lint"]["select"])
    assert project["tool"]["ty"]["src"]["include"] == ["agent_runtime_ref"]

    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    repository = next(
        item
        for item in config["repos"]
        if item["repo"] == "https://github.com/ternaus/ruff-policy-hooks"
    )
    assert repository["rev"] == "v0.4.0"
    hook = next(item for item in repository["hooks"] if item["id"] == "check-ruff-suppressions")
    assert hook["args"] == ["--protect=C901,PLR0912"]
