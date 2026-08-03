from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

from agent_runtime_ref.evidence import verify_evidence_manifest
from docs.companion.examples.build_capstone_reference import build_capstone
from docs.companion.examples.run_lab_negative_scenario import run_scenario

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "agent_runtime_ref/configs"


def test_negative_scenarios_materialize_the_claimed_closed_failures(
    tmp_path: Path,
) -> None:
    ticket_output = tmp_path / "ticket-controls-disabled.json"
    ticket = run_scenario(
        "ticket-controls-disabled",
        config_dir=CONFIG_DIR,
        output=ticket_output,
    )
    assert ticket["healthy"] is False
    assert ticket["missing_controls"] == [
        "create_ticket_approval_required",
        "create_ticket_idempotency_key_required",
    ]
    assert json.loads(ticket_output.read_text(encoding="utf-8")) == ticket

    owner_output = tmp_path / "platform-owner-removed.json"
    owner = run_scenario(
        "platform-owner-removed",
        config_dir=CONFIG_DIR,
        output=owner_output,
    )
    assert owner["ready"] is False
    assert owner["missing_approval_roles"] == ["platform-owner"]
    assert json.loads(owner_output.read_text(encoding="utf-8")) == owner


def test_negative_scenario_is_executable_by_the_documented_command() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "docs/companion/examples/run_lab_negative_scenario.py",
            "ticket-controls-disabled",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["healthy"] is False
    assert payload["missing_controls"] == [
        "create_ticket_approval_required",
        "create_ticket_idempotency_key_required",
    ]


def test_capstone_builder_creates_a_verifiable_hold_package(tmp_path: Path) -> None:
    result = build_capstone(
        tmp_path,
        repo_root=ROOT,
        measured_at="2026-08-03T10:00:00Z",
    )

    expected_files = {
        "README.md",
        "01-baseline.md",
        "02-normal-trace.jsonl",
        "02-timeout-trace.jsonl",
        "02-trace-comparison.md",
        "03-reconciliation.yaml",
        "04-eval.json",
        "04-rollout-hold.json",
        "05-limited-wave-plan.md",
        "release-decision.json",
        "evidence-manifest.yaml",
    }
    assert expected_files <= {path.name for path in tmp_path.iterdir()}

    release = json.loads((tmp_path / "release-decision.json").read_text(encoding="utf-8"))
    assert release["decision"] == "hold"
    assert release["next_eligible_decision"] == "limited_wave"
    assert release["blocking_findings"]

    manifest = yaml.safe_load((tmp_path / "evidence-manifest.yaml").read_text(encoding="utf-8"))
    artifact_ids = tuple(item["id"] for item in manifest["artifacts"])
    verification = verify_evidence_manifest(
        tmp_path / "evidence-manifest.yaml",
        root=tmp_path,
        required_artifact_ids=artifact_ids,
    )
    assert verification.verified is True
    assert verification.diagnostics == ()
    assert result["decision"] == "hold"
