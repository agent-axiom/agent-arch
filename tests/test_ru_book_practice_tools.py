from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from agent_runtime_ref.evidence import verify_evidence_manifest
from docs.companion.examples.build_capstone_reference import build_capstone
from docs.companion.examples.run_lab_negative_scenario import run_scenario

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "agent_runtime_ref/configs"
MEASURED_AT = "2026-09-04T10:00:00Z"
CAPSTONE_CHECKS = {
    "package_inventory",
    "manifest_integrity",
    "release_decision",
    "release_evidence_refs",
    "unknown_effect_path",
    "trace_continuity",
    "eval_unknown_effect",
    "reconciliation_contract",
    "rollout_fails_closed",
}


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


@pytest.fixture(scope="module")
def capstone_template(tmp_path_factory: pytest.TempPathFactory) -> Path:
    package = tmp_path_factory.mktemp("capstone")
    build_capstone(
        package,
        repo_root=ROOT,
        measured_at=MEASURED_AT,
    )
    return package


@pytest.fixture
def capstone_dir(capstone_template: Path, tmp_path: Path) -> Path:
    return shutil.copytree(capstone_template, tmp_path / "package")


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")


def _rebuild_capstone_manifest(package: Path) -> None:
    from docs.companion.examples.build_capstone_evidence_manifest import (
        build_capstone_manifest,
    )

    build_capstone_manifest(package, measured_at=MEASURED_AT)


def _validate_capstone(package: Path):
    from docs.companion.examples.validate_capstone_package import validate_capstone_package

    return validate_capstone_package(package)


def _failed_checks(validation) -> set[str]:
    assert validation["valid"] is False
    return {item["check"] for item in validation["failed_checks"]}


def test_capstone_builder_creates_a_verifiable_hold_package(capstone_dir: Path) -> None:
    tmp_path = capstone_dir

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
    assert expected_files == {path.name for path in tmp_path.iterdir()}
    assert len(expected_files) == 17

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
    unknown = _read_json(tmp_path / "02-unknown-effect-trace-summary.json")
    assert unknown["status"] == "blocked_on_reconciliation"
    assert unknown["failure_reason"] == "post_dispatch_timeout"
    assert "effect_reconciliation_required" in unknown["event_types"]
    evaluation = _read_json(tmp_path / "04-eval.json")
    assert evaluation["sessions"][0]["eval"]["scenario"] == "unknown_effect_reconciliation"
    run = evaluation["sessions"][0]["runs"][0]
    assert run["failure_reason"] == "post_dispatch_timeout"
    assert run["side_effect_status"] == "side_effect_unknown"
    assert run["status"] == "blocked_on_reconciliation"
    rollout = _read_json(tmp_path / "04-rollout-hold.json")
    assert rollout["ready"] is False
    assert rollout["production_ready"] is False
    validation = _validate_capstone(tmp_path)
    assert validation["valid"] is True
    assert validation["decision"] == "hold"
    assert validation["checked_files"] == 17
    assert set(validation["passed_checks"]) == CAPSTONE_CHECKS
    assert len(validation["passed_checks"]) == 9
    assert validation["failed_checks"] == []


def test_capstone_builder_rejects_nonempty_output_without_changing_it(tmp_path: Path) -> None:
    stale = tmp_path / "stale.txt"
    stale.write_text("do not mix packages\n", encoding="utf-8")
    with pytest.raises(FileExistsError, match="must be empty or absent"):
        build_capstone(tmp_path, repo_root=ROOT, measured_at=MEASURED_AT)
    assert list(tmp_path.iterdir()) == [stale]
    assert stale.read_text(encoding="utf-8") == "do not mix packages\n"


@pytest.mark.parametrize(
    "filename",
    [
        "01-agent.json",
        "02-unknown-effect-trace.jsonl",
        "release-decision.json",
        "evidence-manifest.yaml",
    ],
)
def test_capstone_rejects_missing_artifacts(capstone_dir: Path, filename: str) -> None:
    (capstone_dir / filename).unlink()
    failed = _failed_checks(_validate_capstone(capstone_dir))
    assert {"package_inventory", "manifest_integrity"} <= failed


def test_capstone_rejects_unexpected_files_after_rehash(capstone_dir: Path) -> None:
    (capstone_dir / "stale.txt").write_text("stale\n", encoding="utf-8")
    _rebuild_capstone_manifest(capstone_dir)
    failed = _failed_checks(_validate_capstone(capstone_dir))
    assert {"package_inventory", "manifest_integrity"} <= failed


def test_capstone_tampered_artifact_has_structured_digest_diagnostic(capstone_dir: Path) -> None:
    (capstone_dir / "01-baseline.md").write_text("changed\n", encoding="utf-8")
    validation = _validate_capstone(capstone_dir)
    assert _failed_checks(validation) == {"manifest_integrity"}
    assert "sha256_mismatch" in validation["failed_checks"][0]["reason"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("owner", ""),
        ("decision", "limited_wave"),
        ("blocking_findings", []),
        ("evidence_refs", ["../outside.json"]),
        ("evidence_refs", [{}]),
    ],
)
def test_capstone_rejects_bad_decisions_after_rehash(
    capstone_dir: Path,
    field: str,
    value: object,
) -> None:
    path = capstone_dir / "release-decision.json"
    decision = _read_json(path)
    decision[field] = value
    _write_json(path, decision)
    _rebuild_capstone_manifest(capstone_dir)
    failed = _failed_checks(_validate_capstone(capstone_dir))
    assert "manifest_integrity" not in failed
    assert ("release_evidence_refs" if field == "evidence_refs" else "release_decision") in failed


def test_capstone_malformed_refs_report_each_check_once(capstone_dir: Path) -> None:
    path = capstone_dir / "release-decision.json"
    decision = _read_json(path)
    decision["evidence_refs"][-1] = {}
    _write_json(path, decision)
    _rebuild_capstone_manifest(capstone_dir)
    validation = _validate_capstone(capstone_dir)
    assert _failed_checks(validation) == {"release_evidence_refs"}
    reported = validation["passed_checks"] + [item["check"] for item in validation["failed_checks"]]
    assert len(reported) == len(set(reported)) == 9


@pytest.mark.parametrize("mutation", ["duplicate", "non_object", "owner", "evidence_ref"])
def test_capstone_rejects_malformed_blockers_after_rehash(
    capstone_dir: Path,
    mutation: str,
) -> None:
    path = capstone_dir / "release-decision.json"
    decision = _read_json(path)
    blockers = decision["blocking_findings"]
    if mutation == "duplicate":
        blockers.append(dict(blockers[0]))
    elif mutation == "non_object":
        blockers.append("ignored blocker")
    else:
        blockers[0][mutation] = ""
    _write_json(path, decision)
    _rebuild_capstone_manifest(capstone_dir)
    assert "release_decision" in _failed_checks(_validate_capstone(capstone_dir))


@pytest.mark.parametrize(
    "mutation",
    [
        "empty",
        "malformed",
        "trace_id",
        "session_id",
        "tool_effect",
        "tool_outcome",
        "reconciliation_effect",
        "completion_effect",
        "completion_reason",
        "event_order",
    ],
)
def test_capstone_rejects_tampered_raw_trace_after_rehash(
    capstone_dir: Path,
    mutation: str,
) -> None:
    path = capstone_dir / "02-unknown-effect-trace.jsonl"
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    by_type = {event["event_type"]: event for event in events}
    if mutation == "trace_id":
        events[-1]["trace_id"] = "another-trace"
    elif mutation == "session_id":
        events[-1]["payload"]["session_id"] = "another-session"
    elif mutation == "event_order":
        events[-1], events[-2] = events[-2], events[-1]
        summary_path = capstone_dir / "02-unknown-effect-trace-summary.json"
        summary = _read_json(summary_path)
        summary["event_types"] = [event["event_type"] for event in events]
        _write_json(summary_path, summary)
    elif mutation not in {"empty", "malformed"}:
        event_type, field = {
            "tool_effect": ("tool_execution", "side_effect_status"),
            "tool_outcome": ("tool_execution", "outcome"),
            "reconciliation_effect": ("effect_reconciliation_required", "effect_state"),
            "completion_effect": ("run_complete", "side_effect_status"),
            "completion_reason": ("run_complete", "failure_reason"),
        }[mutation]
        by_type[event_type]["payload"][field] = "not_executed"
    content = "\n".join(json.dumps(event) for event in events) + "\n"
    if mutation == "empty":
        content = ""
    elif mutation == "malformed":
        content = "not json\n"
    path.write_text(content, encoding="utf-8")
    if mutation not in {"empty", "malformed"}:
        summary_path = capstone_dir / "02-unknown-effect-trace-summary.json"
        summary = _read_json(summary_path)
        summary["events"] = events
        _write_json(summary_path, summary)
    _rebuild_capstone_manifest(capstone_dir)
    failed = _failed_checks(_validate_capstone(capstone_dir))
    assert "manifest_integrity" not in failed
    assert "trace_continuity" in failed


@pytest.mark.parametrize("mutation", ["empty", "summary", "status", "effect"])
def test_capstone_rejects_tampered_normal_trace_after_rehash(
    capstone_dir: Path,
    mutation: str,
) -> None:
    path = capstone_dir / "02-normal-trace.jsonl"
    summary_path = capstone_dir / "02-normal-trace-summary.json"
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    summary = _read_json(summary_path)
    if mutation == "empty":
        path.write_text("", encoding="utf-8")
    elif mutation == "summary":
        summary["event_count"] = 0
    else:
        completion = events[-1]["payload"]
        if mutation == "status":
            completion["status"] = "success"
            summary["status"] = "success"
        else:
            completion["side_effect_status"] = "executed"
        summary["events"] = events
        path.write_text("\n".join(json.dumps(event) for event in events), encoding="utf-8")
    _write_json(summary_path, summary)
    _rebuild_capstone_manifest(capstone_dir)
    assert "trace_continuity" in _failed_checks(_validate_capstone(capstone_dir))


@pytest.mark.parametrize(
    "filename,field,value,check",
    [
        ("02-unknown-effect-trace-summary.json", "status", "failed", "unknown_effect_path"),
        (
            "02-unknown-effect-trace-summary.json",
            "failure_reason",
            "tool_timeout",
            "unknown_effect_path",
        ),
        ("03-reconciliation.yaml", "automatic_retry_allowed", True, "reconciliation_contract"),
        ("03-reconciliation.yaml", "owner", "", "reconciliation_contract"),
        ("04-rollout-hold.json", "ready", True, "rollout_fails_closed"),
        ("04-rollout-hold.json", "production_ready", True, "rollout_fails_closed"),
        ("04-rollout-hold.json", "missing_required", [], "rollout_fails_closed"),
    ],
)
def test_capstone_rejects_inconsistent_contracts_after_rehash(
    capstone_dir: Path,
    filename: str,
    field: str,
    value: object,
    check: str,
) -> None:
    path = capstone_dir / filename
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    payload[field] = value
    _write_json(path, payload)
    _rebuild_capstone_manifest(capstone_dir)
    failed = _failed_checks(_validate_capstone(capstone_dir))
    assert "manifest_integrity" not in failed
    assert check in failed


@pytest.mark.parametrize(
    "field,value",
    [
        ("failure_reason", "tool_timeout"),
        ("side_effect_status", "not_executed"),
        ("status", "failed"),
        ("trace_id", "another-trace"),
    ],
)
def test_capstone_rejects_wrong_eval_after_rehash(
    capstone_dir: Path,
    field: str,
    value: str,
) -> None:
    path = capstone_dir / "04-eval.json"
    payload = _read_json(path)
    payload["sessions"][0]["runs"][0][field] = value
    _write_json(path, payload)
    _rebuild_capstone_manifest(capstone_dir)
    assert "eval_unknown_effect" in _failed_checks(_validate_capstone(capstone_dir))


@pytest.mark.parametrize("field", ["trace_ids", "session_ids", "duplicate_ticket_scenarios"])
def test_capstone_rejects_eval_string_instead_of_list(capstone_dir: Path, field: str) -> None:
    path = capstone_dir / "04-eval.json"
    payload = _read_json(path)
    payload[field] = payload[field][0]
    _write_json(path, payload)
    _rebuild_capstone_manifest(capstone_dir)
    assert "eval_unknown_effect" in _failed_checks(_validate_capstone(capstone_dir))


def test_capstone_cli_build_rehash_validate_and_failure(tmp_path: Path) -> None:
    package = tmp_path / "capstone-reference"
    for script, args in [
        ("build_capstone_reference.py", ["--output-dir", str(package)]),
        ("build_capstone_evidence_manifest.py", ["--package-dir", str(package)]),
        ("validate_capstone_package.py", ["--package-dir", str(package)]),
    ]:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "docs/companion/examples" / script), *args],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=True,
        )
    assert json.loads(completed.stdout)["valid"] is True
    (package / "02-unknown-effect-trace.jsonl").unlink()
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "docs/companion/examples/validate_capstone_package.py"),
            "--package-dir",
            str(package),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 1
    assert json.loads(completed.stdout)["valid"] is False


def _runtime_json(*args: str):
    completed = subprocess.run(
        [sys.executable, "-m", "agent_runtime_ref", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


def _write_lab_manifest(artifacts: Path, through: int = 8) -> None:
    from docs.companion.examples.build_lab_evidence_manifest import build_manifest

    manifest = build_manifest(
        artifacts,
        through=through,
        subject="support-triage-ref@test",
        measured_at=MEASURED_AT,
    )
    (artifacts / "evidence-manifest.yaml").write_text(
        yaml.safe_dump(manifest),
        encoding="utf-8",
    )


def _validate_lab8(artifacts: Path):
    from docs.companion.examples.validate_lab8_package import validate_lab8_package

    return validate_lab8_package(artifacts)


@pytest.fixture(scope="module")
def lab8_template(tmp_path_factory: pytest.TempPathFactory) -> Path:
    from docs.companion.examples.build_lab_evidence_manifest import LAB_ARTIFACTS

    artifacts = tmp_path_factory.mktemp("laboratories")
    prior_ids = []
    for laboratory, artifact_id, relative_path in LAB_ARTIFACTS:
        if laboratory >= 8:
            continue
        artifact = artifacts / relative_path
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(f"evidence:{relative_path}\n", encoding="utf-8")
        prior_ids.extend(("--required-artifact-id", artifact_id))
    _write_lab_manifest(artifacts, through=7)
    lab_dir = artifacts / "lab-08"
    lab_dir.mkdir()
    _write_json(
        lab_dir / "01-manifest-check.json",
        _runtime_json(
            "check-rollout",
            "--evidence-manifest",
            str(artifacts / "evidence-manifest.yaml"),
            *prior_ids,
        ),
    )
    _write_json(
        lab_dir / "02-unknown-effect.json",
        _runtime_json(
            "check-rollout",
            "--signal",
            "unknown_side_effect_path_missing=true",
        ),
    )
    steps = (
        "freeze_rollout",
        "disable_risky_capabilities",
        "stop_memory_write",
        "expire_paused_runs",
        "stop_background_routes",
        "freeze_reinitialization",
        "revoke_egress",
        "archive_audit_state",
        "set_retired_status",
    )
    step_args = [
        arg
        for step in steps
        for arg in ("--step", f"{step}={'false' if step == 'revoke_egress' else 'true'}")
    ]
    _write_json(
        lab_dir / "03-retirement-check.json",
        _runtime_json(
            "check-retirement",
            *step_args,
        ),
    )
    _write_json(
        lab_dir / "release-decision.json",
        {
            "version": 1,
            "decision": "hold",
            "scope": "first_wave",
            "control_action": "not_started",
            "owner": "support-platform-release-owner",
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
            "evidence_refs": [
                "01-manifest-check.json",
                "02-unknown-effect.json",
                "03-retirement-check.json",
            ],
        },
    )
    _write_lab_manifest(artifacts)
    return artifacts


@pytest.fixture
def lab8_dir(lab8_template: Path, tmp_path: Path) -> Path:
    return shutil.copytree(lab8_template, tmp_path / "artifacts")


def test_lab8_validates_real_runtime_hold_without_production_readiness(lab8_dir: Path) -> None:
    validation = _validate_lab8(lab8_dir)
    assert validation["valid"] is True
    assert validation["decision"] == "hold"
    assert validation["lab8_files"] == 4
    assert validation["manifest_artifacts"] == 12
    assert len(validation["passed_checks"]) == 6
    assert validation["failed_checks"] == []


@pytest.mark.parametrize(
    "filename",
    [
        "01-manifest-check.json",
        "02-unknown-effect.json",
        "03-retirement-check.json",
        "release-decision.json",
    ],
)
def test_lab8_missing_checkpoints_fail_closed(lab8_dir: Path, filename: str) -> None:
    (lab8_dir / "lab-08" / filename).unlink()
    validation = _validate_lab8(lab8_dir)
    assert {"lab8_inventory", "cumulative_manifest"} <= _failed_checks(validation)
    assert any("artifact_not_found" in item["reason"] for item in validation["failed_checks"])


@pytest.mark.parametrize(
    "filename,field,value,check",
    [
        ("01-manifest-check.json", "manifest_integrity_verified", False, "prior_manifest_gate"),
        ("01-manifest-check.json", "production_ready", True, "prior_manifest_gate"),
        ("02-unknown-effect.json", "ready", True, "unknown_effect_gate"),
        ("02-unknown-effect.json", "blocking_signals", [], "unknown_effect_gate"),
        ("03-retirement-check.json", "missing_steps", [], "retirement_gate"),
        ("03-retirement-check.json", "evidence_mode", "verified", "retirement_gate"),
        ("release-decision.json", "owner", "", "release_decision"),
        ("release-decision.json", "evidence_refs", ["../outside.json"], "release_decision"),
        ("release-decision.json", "blocking_findings", [], "release_decision"),
    ],
)
def test_lab8_tampering_fails_before_and_after_rehash(
    lab8_dir: Path,
    filename: str,
    field: str,
    value: object,
    check: str,
) -> None:
    path = lab8_dir / "lab-08" / filename
    payload = _read_json(path)
    payload[field] = value
    _write_json(path, payload)
    validation = _validate_lab8(lab8_dir)
    assert {"cumulative_manifest", check} <= _failed_checks(validation)
    assert any("sha256_mismatch" in item["reason"] for item in validation["failed_checks"])
    _write_lab_manifest(lab8_dir)
    assert _failed_checks(_validate_lab8(lab8_dir)) == {check}


@pytest.mark.parametrize("mutation", ["duplicate", "non_object"])
def test_lab8_rejects_malformed_blockers(lab8_dir: Path, mutation: str) -> None:
    path = lab8_dir / "lab-08/release-decision.json"
    decision = _read_json(path)
    blockers = decision["blocking_findings"]
    blockers.append(dict(blockers[0]) if mutation == "duplicate" else "ignored blocker")
    _write_json(path, decision)
    _write_lab_manifest(lab8_dir)
    assert "release_decision" in _failed_checks(_validate_lab8(lab8_dir))


@pytest.mark.parametrize("mutation", ["missing", "malformed", "wrong_path", "duplicate_id"])
def test_lab8_rejects_invalid_cumulative_manifest(lab8_dir: Path, mutation: str) -> None:
    path = lab8_dir / "evidence-manifest.yaml"
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    if mutation == "missing":
        path.unlink()
    elif mutation == "malformed":
        path.write_text("artifacts: [\n", encoding="utf-8")
    else:
        entries = manifest["artifacts"]
        if mutation == "wrong_path":
            entries[-1]["path"] = entries[0]["path"]
            entries[-1]["sha256"] = entries[0]["sha256"]
        else:
            entries.append(dict(entries[-1]))
        path.write_text(yaml.safe_dump(manifest), encoding="utf-8")
    assert "cumulative_manifest" in _failed_checks(_validate_lab8(lab8_dir))


def test_lab8_cli_reports_success_and_failed_validation(lab8_dir: Path, tmp_path: Path) -> None:
    command = [
        sys.executable,
        str(ROOT / "docs/companion/examples/validate_lab8_package.py"),
        "--artifacts-dir",
        str(lab8_dir),
    ]
    completed = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, check=True)
    assert json.loads(completed.stdout)["valid"] is True
    (lab8_dir / "lab-08/02-unknown-effect.json").unlink()
    completed = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, check=False)
    assert completed.returncode == 1
    assert json.loads(completed.stdout)["valid"] is False
