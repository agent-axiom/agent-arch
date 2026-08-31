from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

from agent_runtime_ref.evidence import verify_evidence_manifest
from docs.companion.examples.build_capstone_evidence_manifest import (
    build_capstone_manifest,
)
from docs.companion.examples.build_capstone_reference import build_capstone
from docs.companion.examples.build_lab_evidence_manifest import (
    LAB_ARTIFACTS,
    build_manifest,
)
from docs.companion.examples.run_lab_negative_scenario import run_scenario
from docs.companion.examples.validate_capstone_package import validate_capstone_package
from docs.companion.examples.validate_lab8_package import validate_lab8_package

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


def test_high_risk_capability_requires_approval_before_safe_transport() -> None:
    payload = run_scenario("high-risk-safe-transport", config_dir=CONFIG_DIR)

    assert payload == {
        "scenario": "high-risk-safe-transport",
        "decision": "approval_required",
        "reason": "critical_risk_tier",
        "status": "approval_required",
        "transport": "sandboxed_exec",
        "execution_started": False,
        "effect_state": "not_executed",
    }


def test_stale_worker_cannot_complete_a_reclaimed_run() -> None:
    payload = run_scenario("stale-run-completion", config_dir=CONFIG_DIR)

    assert payload == {
        "scenario": "stale-run-completion",
        "accepted": False,
        "reason": "expected_version_mismatch",
        "run_id": "run-lease-demo",
        "stale_worker": "worker-a",
        "lease_owner": "worker-b",
        "expected_version": 2,
        "current_version": 3,
        "idempotency_scope": "run-lease-demo",
        "effect_state": "not_executed",
    }


def test_assurance_decision_without_owner_fails_closed() -> None:
    payload = run_scenario("assurance-owner-missing", config_dir=CONFIG_DIR)

    assert payload == {
        "scenario": "assurance-owner-missing",
        "ready": False,
        "action": "freeze_reinitialization",
        "owner": "",
        "evidence_event": "assurance_response_decision",
        "missing_fields": ["owner"],
        "blocking_findings": ["assurance_decision_owner_missing"],
    }


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


def test_new_negative_scenarios_are_executable_by_documented_commands() -> None:
    expected = {
        "high-risk-safe-transport": ("status", "approval_required"),
        "stale-run-completion": ("reason", "expected_version_mismatch"),
        "assurance-owner-missing": ("ready", False),
    }
    for scenario, (field, value) in expected.items():
        completed = subprocess.run(
            [
                sys.executable,
                "docs/companion/examples/run_lab_negative_scenario.py",
                scenario,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        payload = json.loads(completed.stdout)
        assert payload[field] == value


def test_capstone_builder_creates_a_verifiable_hold_package(tmp_path: Path) -> None:
    result = build_capstone(
        tmp_path,
        repo_root=ROOT,
        measured_at="2026-08-03T10:00:00Z",
    )

    expected_files = {
        "README.md",
        "01-baseline.md",
        "01-agent.json",
        "01-approval-state.json",
        "01-approval.json",
        "01-lifecycle.json",
        "02-normal-trace.jsonl",
        "02-normal-trace-summary.json",
        "02-unknown-effect-trace.jsonl",
        "02-unknown-effect-trace-summary.json",
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

    unknown_effect = json.loads(
        (tmp_path / "02-unknown-effect-trace-summary.json").read_text(
            encoding="utf-8"
        )
    )
    assert unknown_effect["status"] == "blocked_on_reconciliation"
    assert unknown_effect["failure_reason"] == "post_dispatch_timeout"
    assert "effect_reconciliation_required" in unknown_effect["event_types"]

    evaluation = json.loads((tmp_path / "04-eval.json").read_text(encoding="utf-8"))
    assert evaluation["sessions"][0]["eval"]["scenario"] == (
        "unknown_effect_reconciliation"
    )
    assert evaluation["sessions"][0]["runs"][0]["failure_reason"] == (
        "post_dispatch_timeout"
    )

    validation = validate_capstone_package(tmp_path)
    assert validation["valid"] is True
    assert validation["decision"] == "hold"
    assert validation["checked_files"] == 17
    assert validation["failed_checks"] == []


def test_capstone_manifest_builder_and_validator_detect_tampering(tmp_path: Path) -> None:
    build_capstone(
        tmp_path,
        repo_root=ROOT,
        measured_at="2026-08-03T10:00:00Z",
    )

    decision_path = tmp_path / "release-decision.json"
    decision = json.loads(decision_path.read_text(encoding="utf-8"))
    decision["owner"] = ""
    decision_path.write_text(
        json.dumps(decision, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    stale_validation = validate_capstone_package(tmp_path)
    assert stale_validation["valid"] is False
    failed = {item["check"] for item in stale_validation["failed_checks"]}
    assert "manifest_integrity" in failed
    assert "release_decision" in failed

    build_capstone_manifest(
        tmp_path,
        measured_at="2026-08-03T10:30:00Z",
    )
    refreshed_validation = validate_capstone_package(tmp_path)
    assert refreshed_validation["valid"] is False
    refreshed_failed = {
        item["check"] for item in refreshed_validation["failed_checks"]
    }
    assert "manifest_integrity" not in refreshed_failed
    assert "release_decision" in refreshed_failed


def test_capstone_rejects_unexpected_files_even_after_manifest_rebuild(
    tmp_path: Path,
) -> None:
    build_capstone(
        tmp_path,
        repo_root=ROOT,
        measured_at="2026-08-03T10:00:00Z",
    )
    (tmp_path / "stale.txt").write_text("stale\n", encoding="utf-8")
    build_capstone_manifest(
        tmp_path,
        measured_at="2026-08-03T10:30:00Z",
    )

    validation = validate_capstone_package(tmp_path)

    assert validation["valid"] is False
    failed = {item["check"] for item in validation["failed_checks"]}
    assert "package_inventory" in failed
    assert "manifest_integrity" in failed


def test_capstone_builder_rejects_a_nonempty_output_directory(tmp_path: Path) -> None:
    (tmp_path / "stale.txt").write_text("do not mix packages\n", encoding="utf-8")

    try:
        build_capstone(
            tmp_path,
            repo_root=ROOT,
            measured_at="2026-08-03T10:00:00Z",
        )
    except FileExistsError as error:
        assert "must be empty or absent" in str(error)
    else:
        raise AssertionError("nonempty capstone output must fail closed")


def test_lab8_package_links_checkpoints_and_validates_the_hold(tmp_path: Path) -> None:
    for laboratory, _artifact_id, relative_path in LAB_ARTIFACTS:
        if laboratory >= 8:
            continue
        artifact = tmp_path / relative_path
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(f"evidence:{relative_path}\n", encoding="utf-8")

    prior_manifest = build_manifest(
        tmp_path,
        through=7,
        subject="support-triage-ref@test",
        measured_at="2026-08-01T12:00:00Z",
    )
    manifest_path = tmp_path / "evidence-manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(prior_manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    lab_dir = tmp_path / "lab-08"
    lab_dir.mkdir()

    prior_ids = tuple(item[1] for item in LAB_ARTIFACTS if item[0] <= 7)
    manifest_command = [
        sys.executable,
        "-m",
        "agent_runtime_ref",
        "check-rollout",
        "--evidence-manifest",
        str(manifest_path),
    ]
    for artifact_id in prior_ids:
        manifest_command.extend(("--required-artifact-id", artifact_id))
    manifest_command.extend(("--output", str(lab_dir / "01-manifest-check.json")))
    subprocess.run(manifest_command, cwd=ROOT, check=True, capture_output=True, text=True)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_runtime_ref",
            "check-rollout",
            "--signal",
            "unknown_side_effect_path_missing=true",
            "--output",
            str(lab_dir / "02-unknown-effect.json"),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    retirement_steps = [
        "freeze_rollout=true",
        "disable_risky_capabilities=true",
        "stop_memory_write=true",
        "expire_paused_runs=true",
        "stop_background_routes=true",
        "freeze_reinitialization=true",
        "revoke_egress=false",
        "archive_audit_state=true",
        "set_retired_status=true",
    ]
    retirement_command = [
        sys.executable,
        "-m",
        "agent_runtime_ref",
        "check-retirement",
    ]
    for step in retirement_steps:
        retirement_command.extend(("--step", step))
    retirement_command.extend(
        ("--output", str(lab_dir / "03-retirement-check.json"))
    )
    subprocess.run(
        retirement_command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    decision = {
        "version": 1,
        "decision": "hold",
        "scope": "first_wave",
        "control_action": "not_started",
        "blocking_findings": [
            {
                "id": "unknown_side_effect_path_missing",
                "evidence_ref": "02-unknown-effect.json",
                "owner": "support-platform-on-call",
                "required_evidence": "external_effect_reconciliation",
                "reconsider_when": "verification_result=not_found",
            },
            {
                "id": "revoke_egress",
                "evidence_ref": "03-retirement-check.json",
                "owner": "identity-platform-owner",
                "required_evidence": "egress_revocation_receipt",
                "reconsider_when": "revoke_egress=true",
            },
        ],
        "owner": "support-platform-release-owner",
        "evidence_refs": [
            "01-manifest-check.json",
            "02-unknown-effect.json",
            "03-retirement-check.json",
        ],
    }
    (lab_dir / "release-decision.json").write_text(
        json.dumps(decision, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    final_manifest = build_manifest(
        tmp_path,
        through=8,
        subject="support-triage-ref@test",
        measured_at="2026-08-01T13:00:00Z",
    )
    manifest_path.write_text(
        yaml.safe_dump(final_manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    validation = validate_lab8_package(tmp_path)

    assert validation["valid"] is True
    assert validation["decision"] == "hold"
    assert validation["lab8_files"] == 4
    assert validation["manifest_artifacts"] == 12


def test_capstone_documented_commands_run_as_scripts(tmp_path: Path) -> None:
    package_dir = tmp_path / "capstone-reference"
    subprocess.run(
        [
            sys.executable,
            "docs/companion/examples/build_capstone_reference.py",
            "--output-dir",
            str(package_dir),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    completed = subprocess.run(
        [
            sys.executable,
            "docs/companion/examples/validate_capstone_package.py",
            "--package-dir",
            str(package_dir),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    validation = json.loads(completed.stdout)
    assert validation["valid"] is True
    assert validation["decision"] == "hold"
