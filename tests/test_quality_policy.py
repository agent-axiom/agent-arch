from __future__ import annotations

import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_project_keeps_recommended_ruff_policy_defaults() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dev_dependencies = project["dependency-groups"]["dev"]

    assert "pre-commit>=4.3,<5" in dev_dependencies
    assert {"C901", "PLR0912"} <= set(project["tool"]["ruff"]["lint"]["select"])
    assert "src" not in project["tool"].get("ty", {})

    ruff_lint = project["tool"]["ruff"]["lint"]
    assert ruff_lint.get("mccabe", {}).get("max-complexity", 10) == 10
    assert ruff_lint.get("pylint", {}).get("max-branches", 12) == 12


def test_complexity_suppressions_are_protected() -> None:
    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))

    repository = next(
        item
        for item in config["repos"]
        if item["repo"] == "https://github.com/ternaus/ruff-policy-hooks"
    )
    assert repository["rev"] == "v0.4.0"
    hook = next(item for item in repository["hooks"] if item["id"] == "check-ruff-suppressions")
    assert hook["args"] == ["--protect=C901,PLR0912"]


def test_quality_workflow_runs_the_local_policy_checks() -> None:
    workflow = yaml.load(
        (ROOT / ".github" / "workflows" / "quality.yml").read_text(encoding="utf-8"),
        Loader=yaml.BaseLoader,
    )

    assert workflow["on"] == {
        "pull_request": "",
        "push": {"branches": ["main"]},
        "workflow_dispatch": "",
    }
    assert workflow["env"] == {"FORCE_JAVASCRIPT_ACTIONS_TO_NODE24": "true"}
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["concurrency"] == {
        "group": "quality-${{ github.ref }}",
        "cancel-in-progress": "true",
    }

    quality = workflow["jobs"]["quality"]
    assert quality["if"] == (
        "github.event_name == 'pull_request' || "
        "github.event_name == 'workflow_dispatch' || "
        "github.ref == 'refs/heads/main'"
    )
    assert quality["runs-on"] == "ubuntu-latest"
    assert quality["timeout-minutes"] == "15"
    assert [step["uses"] for step in quality["steps"] if "uses" in step] == [
        "actions/checkout@v6.0.2",
        "astral-sh/setup-uv@v8.1.0",
    ]
    assert [step["run"] for step in quality["steps"] if "run" in step] == [
        "uv python install 3.12",
        "uv sync --locked --group dev",
        "uv run pytest tests/test_agent_runtime_ref.py -q -k workflow",
        "uv run pytest tests/test_quality_policy.py -q",
        "uv run ruff check .",
        "uv run ty check agent_runtime_ref",
        "uv run pre-commit run --all-files",
    ]
