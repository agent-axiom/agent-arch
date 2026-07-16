from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pytest
import yaml

from agent_runtime_ref.evidence import (
    EvidenceVerificationResult,
    verify_evidence_manifest,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_manifest(root: Path, payload: object) -> Path:
    path = root / "evidence-manifest.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def _valid_manifest(root: Path) -> dict[str, Any]:
    artifact = root / "reports" / "evaluation.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text('{"passed": true}\n', encoding="utf-8")
    return {
        "version": 1,
        "issuer": "release-pipeline",
        "subject": "support-agent@1.4.0",
        "measured_at": "2026-07-16T09:30:00Z",
        "artifacts": [
            {
                "id": "evaluation-report",
                "path": "reports/evaluation.json",
                "sha256": _sha256(artifact),
            }
        ],
        "signals": {
            "duplicate_ticket_eval_passed": {
                "value": True,
                "artifact_refs": ["evaluation-report"],
            }
        },
    }


def _codes(result: EvidenceVerificationResult) -> set[str]:
    return {diagnostic.code for diagnostic in result.diagnostics}


def test_verifies_manifest_and_exposes_normalized_evidence(tmp_path: Path) -> None:
    manifest_path = _write_manifest(tmp_path, _valid_manifest(tmp_path))

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is True
    assert result.diagnostics == ()
    assert result.version == "1"
    assert result.issuer == "release-pipeline"
    assert result.subject == "support-agent@1.4.0"
    assert result.measured_at == "2026-07-16T09:30:00Z"
    assert result.artifact_ids == ("evaluation-report",)
    assert result.signals == {"duplicate_ticket_eval_passed": True}


def test_resolves_relative_manifest_path_from_explicit_root(tmp_path: Path) -> None:
    _write_manifest(tmp_path, _valid_manifest(tmp_path))

    result = verify_evidence_manifest("evidence-manifest.yaml", root=tmp_path)

    assert result.verified is True


def test_accepts_unquoted_yaml_timestamp(tmp_path: Path) -> None:
    payload = _valid_manifest(tmp_path)
    manifest_path = _write_manifest(tmp_path, payload)
    text = manifest_path.read_text(encoding="utf-8")
    manifest_path.write_text(
        text.replace("'2026-07-16T09:30:00Z'", "2026-07-16T09:30:00Z"),
        encoding="utf-8",
    )

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is True
    assert result.measured_at == "2026-07-16T09:30:00Z"


@pytest.mark.parametrize("field", ["version", "issuer", "subject", "measured_at"])
def test_rejects_missing_manifest_metadata(tmp_path: Path, field: str) -> None:
    payload = _valid_manifest(tmp_path)
    del payload[field]
    manifest_path = _write_manifest(tmp_path, payload)

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert "missing_field" in _codes(result)
    assert any(diagnostic.location == field for diagnostic in result.diagnostics)


def test_reports_invalid_yaml_as_a_structured_diagnostic(tmp_path: Path) -> None:
    manifest_path = tmp_path / "evidence-manifest.yaml"
    manifest_path.write_text("artifacts: [\n", encoding="utf-8")

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert _codes(result) == {"invalid_yaml"}


def test_rejects_missing_artifact_and_signal_collections(tmp_path: Path) -> None:
    manifest_path = _write_manifest(
        tmp_path,
        {
            "version": 1,
            "issuer": "release-pipeline",
            "subject": "support-agent@1.4.0",
            "measured_at": "2026-07-16T09:30:00Z",
        },
    )

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert {
        diagnostic.location
        for diagnostic in result.diagnostics
        if diagnostic.code == "missing_field"
    } == {"artifacts", "signals"}


def test_rejects_duplicate_artifact_ids(tmp_path: Path) -> None:
    payload = _valid_manifest(tmp_path)
    artifact = dict(payload["artifacts"][0])
    payload["artifacts"] = [artifact, dict(artifact)]
    manifest_path = _write_manifest(tmp_path, payload)

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert "duplicate_artifact_id" in _codes(result)


def test_rejects_duplicate_signal_ids_in_list_form(tmp_path: Path) -> None:
    payload = _valid_manifest(tmp_path)
    payload["signals"] = [
        {"id": "quality", "value": 0.99, "artifact_refs": ["evaluation-report"]},
        {"id": "quality", "value": 1.0, "artifact_refs": ["evaluation-report"]},
    ]
    manifest_path = _write_manifest(tmp_path, payload)

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert "duplicate_signal_id" in _codes(result)


def test_rejects_unknown_artifact_reference(tmp_path: Path) -> None:
    payload = _valid_manifest(tmp_path)
    payload["signals"] = {"quality": {"value": 0.99, "artifact_refs": ["missing-report"]}}
    manifest_path = _write_manifest(tmp_path, payload)

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert "unknown_artifact_ref" in _codes(result)


@pytest.mark.parametrize("artifact_path", ["../outside.json", "/tmp/outside.json"])
def test_rejects_artifact_paths_outside_root(tmp_path: Path, artifact_path: str) -> None:
    payload = _valid_manifest(tmp_path)
    payload["artifacts"][0]["path"] = artifact_path
    manifest_path = _write_manifest(tmp_path, payload)

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert "artifact_outside_root" in _codes(result)


def test_rejects_symlink_that_resolves_outside_root(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside.json"
    outside.write_text("external\n", encoding="utf-8")
    link = tmp_path / "linked.json"
    link.symlink_to(outside)

    payload = _valid_manifest(tmp_path)
    payload["artifacts"][0].update({"path": "linked.json", "sha256": _sha256(outside)})
    manifest_path = _write_manifest(tmp_path, payload)

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert "artifact_outside_root" in _codes(result)


def test_rejects_missing_artifact_file(tmp_path: Path) -> None:
    payload = _valid_manifest(tmp_path)
    payload["artifacts"][0]["path"] = "reports/missing.json"
    manifest_path = _write_manifest(tmp_path, payload)

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert "artifact_not_found" in _codes(result)


def test_rejects_invalid_or_mismatched_sha256(tmp_path: Path) -> None:
    invalid_payload = _valid_manifest(tmp_path)
    invalid_payload["artifacts"][0]["sha256"] = "not-a-digest"
    invalid_result = verify_evidence_manifest(
        _write_manifest(tmp_path, invalid_payload), root=tmp_path
    )

    mismatch_payload = _valid_manifest(tmp_path)
    mismatch_payload["artifacts"][0]["sha256"] = "0" * 64
    mismatch_result = verify_evidence_manifest(
        _write_manifest(tmp_path, mismatch_payload), root=tmp_path
    )

    assert "invalid_sha256" in _codes(invalid_result)
    assert "sha256_mismatch" in _codes(mismatch_result)


def test_rejects_signal_without_value_or_evidence_references(tmp_path: Path) -> None:
    payload = _valid_manifest(tmp_path)
    payload["signals"] = {"quality": {}}
    manifest_path = _write_manifest(tmp_path, payload)

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    locations = {
        diagnostic.location
        for diagnostic in result.diagnostics
        if diagnostic.code == "missing_field"
    }
    assert locations == {"signals.quality.value", "signals.quality.artifact_refs"}


def test_collects_independent_diagnostics_in_one_pass(tmp_path: Path) -> None:
    payload = _valid_manifest(tmp_path)
    payload["issuer"] = ""
    payload["artifacts"][0]["sha256"] = "f" * 64
    payload["signals"] = {"quality": {"value": True, "artifact_refs": ["unknown-artifact"]}}
    manifest_path = _write_manifest(tmp_path, payload)

    result = verify_evidence_manifest(manifest_path, root=tmp_path)

    assert result.verified is False
    assert {"invalid_field", "sha256_mismatch", "unknown_artifact_ref"} <= _codes(result)


def test_check_rollout_without_manifest_is_declarative_only(cli_json) -> None:
    exit_code, payload = cli_json(["check-rollout"])

    assert exit_code == 0
    assert payload["ready"] is True
    assert payload["production_ready"] is False
    assert payload["evidence_mode"] == "declarative_only"
    assert payload["evidence_verified"] is False
    assert payload["recommended_action"] == "attach_verified_evidence"


def test_check_rollout_accepts_only_verified_manifest_for_production(
    cli_json,
    config_dir: Path,
    tmp_path: Path,
) -> None:
    payload = _valid_manifest(tmp_path)
    rollout = yaml.safe_load((config_dir / "rollout.yaml").read_text(encoding="utf-8"))["rollout"]
    artifact_ref = payload["artifacts"][0]["id"]
    payload["signals"] = {
        signal: {"value": True, "artifact_refs": [artifact_ref]} for signal in rollout["require"]
    }
    payload["signals"].update(
        {
            signal: {"value": False, "artifact_refs": [artifact_ref]}
            for signal in rollout["block_if"]
        }
    )
    manifest_path = _write_manifest(tmp_path, payload)

    exit_code, result = cli_json(["check-rollout", "--evidence-manifest", str(manifest_path)])

    assert exit_code == 0
    assert result["ready"] is True
    assert result["production_ready"] is True
    assert result["evidence_mode"] == "verified"
    assert result["evidence_verified"] is True
    assert result["evidence_artifact_ids"] == ["evaluation-report"]
    assert result["evidence_diagnostics"] == []
    assert result["recommended_action"] == "proceed_to_canary"


def test_check_rollout_invalid_manifest_fails_closed(cli_json, tmp_path: Path) -> None:
    payload = _valid_manifest(tmp_path)
    payload["artifacts"][0]["sha256"] = "0" * 64
    manifest_path = _write_manifest(tmp_path, payload)

    exit_code, result = cli_json(["check-rollout", "--evidence-manifest", str(manifest_path)])

    assert exit_code == 0
    assert result["ready"] is False
    assert result["production_ready"] is False
    assert result["evidence_mode"] == "invalid"
    assert result["evidence_verified"] is False
    assert {item["code"] for item in result["evidence_diagnostics"]} == {"sha256_mismatch"}
    assert result["recommended_action"] == "repair_evidence_manifest"


def test_check_rollout_manual_override_is_never_production_evidence(
    cli_json,
    config_dir: Path,
    tmp_path: Path,
) -> None:
    payload = _valid_manifest(tmp_path)
    rollout = yaml.safe_load((config_dir / "rollout.yaml").read_text(encoding="utf-8"))["rollout"]
    artifact_ref = payload["artifacts"][0]["id"]
    payload["signals"] = {
        signal: {"value": True, "artifact_refs": [artifact_ref]} for signal in rollout["require"]
    }
    payload["signals"].update(
        {
            signal: {"value": False, "artifact_refs": [artifact_ref]}
            for signal in rollout["block_if"]
        }
    )
    manifest_path = _write_manifest(tmp_path, payload)

    exit_code, result = cli_json(
        [
            "check-rollout",
            "--evidence-manifest",
            str(manifest_path),
            "--signal",
            "offline_eval_pass=true",
        ]
    )

    assert exit_code == 0
    assert result["ready"] is True
    assert result["production_ready"] is False
    assert result["evidence_mode"] == "verified_with_overrides"
    assert result["recommended_action"] == "remove_manual_overrides"


def test_checked_in_teaching_manifest_is_verified_but_holds_rollout(cli_json) -> None:
    exit_code, result = cli_json(
        [
            "check-rollout",
            "--evidence-manifest",
            "artifacts/evidence-manifest.yaml",
        ]
    )

    assert exit_code == 0
    assert result["evidence_verified"] is True
    assert result["ready"] is False
    assert result["production_ready"] is False
    assert result["missing_required"] == ["duplicate_ticket_eval_passed"]
    assert result["recommended_action"] == "collect_missing_evidence"
