from __future__ import annotations

from pathlib import Path

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
