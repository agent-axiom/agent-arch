from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from agent_runtime_ref.evidence import verify_evidence_manifest
from docs.companion.examples.build_lab_evidence_manifest import (
    LAB_ARTIFACTS,
    build_manifest,
)


def test_builds_a_verifiable_relative_manifest_for_all_laboratories(
    tmp_path: Path,
) -> None:
    for _laboratory, _artifact_id, relative_path in LAB_ARTIFACTS:
        artifact = tmp_path / relative_path
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(f"evidence:{relative_path}\n", encoding="utf-8")

    payload = build_manifest(
        tmp_path,
        through=7,
        subject="support-triage-ref@test",
        measured_at="2026-08-01T12:00:00Z",
    )
    manifest_path = tmp_path / "evidence-manifest.yaml"

    manifest_path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    result = verify_evidence_manifest(
        manifest_path,
        root=tmp_path,
        required_artifact_ids=tuple(f"lab-{number:02d}" for number in range(1, 8)),
    )

    assert result.verified is True
    assert result.diagnostics == ()
    assert "lab-04-pre-dispatch" in result.artifact_ids
    assert result.signals["lab_07_observed"] is True


def test_partial_manifest_requires_only_completed_laboratory_files(tmp_path: Path) -> None:
    first = tmp_path / "lab-01/decision.md"
    first.parent.mkdir(parents=True)
    first.write_text("decision: workflow\n", encoding="utf-8")

    payload = build_manifest(
        tmp_path,
        through=1,
        subject="support-triage-ref@test",
        measured_at="2026-08-01T12:00:00Z",
    )

    assert [item["id"] for item in payload["artifacts"]] == ["lab-01"]


def test_manifest_includes_the_release_decision_from_laboratory_eight(
    tmp_path: Path,
) -> None:
    for _laboratory, _artifact_id, relative_path in LAB_ARTIFACTS:
        artifact = tmp_path / relative_path
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(f"evidence:{relative_path}\n", encoding="utf-8")

    payload = build_manifest(
        tmp_path,
        through=8,
        subject="support-triage-ref@test",
        measured_at="2026-08-01T12:00:00Z",
    )

    artifact_ids = [item["id"] for item in payload["artifacts"]]
    assert artifact_ids[-1] == "lab-08"
    assert payload["artifacts"][-1]["path"] == "lab-08/release-decision.json"
    assert artifact_ids[-4:] == [
        "lab-08-manifest-check",
        "lab-08-unknown-effect",
        "lab-08-retirement-check",
        "lab-08",
    ]
    assert len(artifact_ids) == 12
    assert payload["signals"]["lab_08_observed"]["value"] is True


@pytest.mark.parametrize(
    "missing",
    [
        "lab-08/01-manifest-check.json",
        "lab-08/02-unknown-effect.json",
        "lab-08/03-retirement-check.json",
        "lab-08/release-decision.json",
    ],
)
def test_lab8_manifest_requires_all_checkpoints(tmp_path: Path, missing: str) -> None:
    for _laboratory, _artifact_id, relative_path in LAB_ARTIFACTS:
        artifact = tmp_path / relative_path
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("evidence\n", encoding="utf-8")
    (tmp_path / missing).unlink(missing_ok=True)
    with pytest.raises(FileNotFoundError, match="Missing laboratory artifact"):
        build_manifest(
            tmp_path,
            through=8,
            subject="test",
            measured_at="2026-09-04T10:00:00Z",
        )


def test_capstone_manifest_is_relative_recursive_and_does_not_hash_itself(tmp_path: Path) -> None:
    from docs.companion.examples.build_capstone_evidence_manifest import build_capstone_manifest

    nested = tmp_path / "evidence" / "trace.jsonl"
    nested.parent.mkdir()
    nested.write_text("{}\n", encoding="utf-8")
    for _ in range(2):
        manifest = build_capstone_manifest(tmp_path, measured_at="2026-09-04T10:00:00Z")
        assert [item["path"] for item in manifest["artifacts"]] == ["evidence/trace.jsonl"]
        verification = verify_evidence_manifest(tmp_path / "evidence-manifest.yaml", root=tmp_path)
        assert verification.verified is True
    nested.write_text("tampered\n", encoding="utf-8")
    verification = verify_evidence_manifest(tmp_path / "evidence-manifest.yaml", root=tmp_path)
    assert {item.code for item in verification.diagnostics} == {"sha256_mismatch"}
