from __future__ import annotations

import json
import shutil
from dataclasses import replace
from pathlib import Path
from typing import Any, cast

import pytest

from agent_runtime_ref.config import (
    load_change_record,
    load_controls_policy,
    load_yaml_file,
)
from agent_runtime_ref.controls import ControlsPolicy
from agent_runtime_ref.lifecycle import assess_change_gate


def test_controls_policy_defaults_required_approval_roles_for_legacy_callers() -> None:
    direct = ControlsPolicy(required_controls=(), blocked_findings=())
    parsed = ControlsPolicy.from_dict({"controls": {"require": [], "block_if": []}})

    assert direct.required_approval_roles == ()
    assert parsed.required_approval_roles == ()


def test_controls_policy_loads_required_change_approval_roles(
    config_dir: Path,
) -> None:
    policy = load_controls_policy(config_dir / "controls.yaml")

    assert policy.required_approval_roles == (
        "platform-owner",
        "security-reviewer",
    )


@pytest.mark.parametrize(
    ("value", "error_type", "message"),
    [
        (
            "platform-owner",
            TypeError,
            "'controls.required_approval_roles' must be a list",
        ),
        (
            [7],
            TypeError,
            "controls.required_approval_roles entries must be strings",
        ),
        (
            [" "],
            ValueError,
            "controls.required_approval_roles entries must not be empty",
        ),
        (
            ["platform-owner", " platform-owner "],
            ValueError,
            "controls.required_approval_roles entries must be unique",
        ),
    ],
)
def test_controls_policy_rejects_malformed_required_approval_roles(
    value: object,
    error_type: type[Exception],
    message: str,
    config_dir: Path,
    tmp_path: Path,
) -> None:
    changed_config_dir = tmp_path / error_type.__name__ / "configs"
    shutil.copytree(config_dir, changed_config_dir)
    controls = load_yaml_file(changed_config_dir / "controls.yaml")
    cast(dict[str, Any], controls["controls"])["required_approval_roles"] = value
    controls_path = changed_config_dir / "controls.yaml"
    controls_path.write_text(json.dumps(controls), encoding="utf-8")

    with pytest.raises(error_type, match=message):
        load_controls_policy(controls_path)


def test_change_gate_role_requirements_are_optional_and_fail_closed(
    config_dir: Path,
) -> None:
    change = load_change_record(config_dir / "change.yaml")
    observed = {signal: True for signal in change.required_signals}

    legacy = assess_change_gate(change, observed)
    complete = assess_change_gate(
        change,
        observed,
        required_approval_roles=("platform-owner", "security-reviewer"),
    )
    incomplete = assess_change_gate(
        replace(change, approval_roles=("security-reviewer",)),
        observed,
        required_approval_roles=("platform-owner", "security-reviewer"),
    )

    assert legacy.ready is True
    assert legacy.missing_approval_roles == ()
    assert complete.ready is True
    assert complete.missing_approval_roles == ()
    assert incomplete.ready is False
    assert incomplete.missing_signals == ()
    assert incomplete.missing_approval_roles == ("platform-owner",)


def test_cli_check_change_surfaces_required_approval_roles(cli_json) -> None:
    exit_code, payload = cli_json(["check-change"])

    assert exit_code == 0
    assert payload["ready"] is True
    assert payload["required_approval_roles"] == [
        "platform-owner",
        "security-reviewer",
    ]
    assert payload["missing_approval_roles"] == []


def test_cli_check_change_fails_when_platform_owner_is_removed(
    cli_json,
    config_dir: Path,
    tmp_path: Path,
) -> None:
    changed_config_dir = tmp_path / "missing-platform-owner" / "configs"
    shutil.copytree(config_dir, changed_config_dir)
    change = load_yaml_file(changed_config_dir / "change.yaml")
    approval_roles = cast(
        list[str],
        cast(dict[str, Any], change["change"])["approval_roles"],
    )
    approval_roles.remove("platform-owner")
    (changed_config_dir / "change.yaml").write_text(
        json.dumps(change),
        encoding="utf-8",
    )

    exit_code, payload = cli_json(["check-change", "--config-dir", str(changed_config_dir)])

    assert exit_code == 0
    assert payload["ready"] is False
    assert payload["missing_signals"] == []
    assert payload["required_approval_roles"] == [
        "platform-owner",
        "security-reviewer",
    ]
    assert payload["missing_approval_roles"] == ["platform-owner"]
