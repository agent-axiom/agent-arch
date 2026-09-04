from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_runtime_ref.evidence import verify_evidence_manifest  # noqa: E402
from docs.companion.examples.build_lab_evidence_manifest import (  # noqa: E402
    LAB_ARTIFACTS,
)

REQUIRED_LAB8_FILES = frozenset(
    {
        "01-manifest-check.json",
        "02-unknown-effect.json",
        "03-retirement-check.json",
        "release-decision.json",
    }
)
REQUIRED_BLOCKERS = {
    "unknown_side_effect_path_missing": "02-unknown-effect.json",
    "revoke_egress": "03-retirement-check.json",
}


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return payload


def _contained_file(root: Path, reference: str) -> bool:
    if not reference or Path(reference).is_absolute():
        return False
    candidate = (root / reference).resolve()
    return candidate.is_relative_to(root) and candidate.is_file()


def _cumulative_manifest(artifacts_dir: Path) -> tuple[bool, str]:
    manifest_path = artifacts_dir / "evidence-manifest.yaml"
    required_paths = {artifact_id: path for _, artifact_id, path in LAB_ARTIFACTS}
    verification = verify_evidence_manifest(
        manifest_path,
        root=artifacts_dir,
        required_artifact_ids=tuple(required_paths),
    )
    if not verification.verified:
        return False, "; ".join(
            f"{item.code} at {item.location}: {item.message}" for item in verification.diagnostics
        )
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    artifacts = manifest["artifacts"]
    actual_paths = {item["id"]: item["path"] for item in artifacts}
    valid = len(artifacts) == len(required_paths) and actual_paths == required_paths
    return valid, "verified" if valid else "artifact ids must link the exact laboratory paths"


def validate_lab8_package(artifacts_dir: Path) -> dict[str, object]:
    """Validate Lab 8 evidence, decision semantics, and cumulative manifest."""

    artifacts_dir = artifacts_dir.resolve()
    lab_dir = artifacts_dir / "lab-08"
    passed_checks: list[str] = []
    failed_checks: list[dict[str, str]] = []

    def record(check: str, passed: bool, reason: str) -> None:
        if passed:
            passed_checks.append(check)
        else:
            failed_checks.append({"check": check, "reason": reason})

    present = (
        {path.relative_to(lab_dir).as_posix() for path in lab_dir.rglob("*") if path.is_file()}
        if lab_dir.is_dir()
        else set()
    )
    missing = sorted(REQUIRED_LAB8_FILES - present)
    unexpected = sorted(present - REQUIRED_LAB8_FILES)
    record(
        "lab8_inventory",
        not missing and not unexpected,
        f"missing={missing}; unexpected={unexpected}",
    )

    manifest_check: dict[str, Any] = {}
    try:
        manifest_check = _load_json(lab_dir / "01-manifest-check.json")
        record(
            "prior_manifest_gate",
            manifest_check.get("manifest_integrity_verified") is True
            and manifest_check.get("production_ready") is False,
            "prior laboratories must be intact without claiming production readiness",
        )
    except (OSError, TypeError, ValueError) as error:
        record("prior_manifest_gate", False, str(error))

    try:
        unknown_effect = _load_json(lab_dir / "02-unknown-effect.json")
        blocking_signals = unknown_effect.get("blocking_signals", [])
        record(
            "unknown_effect_gate",
            unknown_effect.get("ready") is False
            and unknown_effect.get("production_ready") is False
            and isinstance(blocking_signals, list)
            and "unknown_side_effect_path_missing" in blocking_signals,
            "unknown external effect must keep rollout closed",
        )
    except (OSError, TypeError, ValueError) as error:
        record("unknown_effect_gate", False, str(error))

    try:
        retirement = _load_json(lab_dir / "03-retirement-check.json")
        missing_steps = retirement.get("missing_steps", [])
        record(
            "retirement_gate",
            retirement.get("ready") is False
            and retirement.get("evidence_mode") == "declared"
            and isinstance(missing_steps, list)
            and missing_steps == ["revoke_egress"],
            "revoke_egress must remain the explicit retirement blocker",
        )
    except (OSError, TypeError, ValueError) as error:
        record("retirement_gate", False, str(error))

    try:
        decision = _load_json(lab_dir / "release-decision.json")
        blockers = decision.get("blocking_findings", [])
        blockers_by_id = (
            {
                item.get("id"): item
                for item in blockers
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            }
            if isinstance(blockers, list)
            else {}
        )
        blocker_schema_ok = (
            isinstance(blockers, list)
            and len(blockers) == len(REQUIRED_BLOCKERS)
            and set(blockers_by_id) == set(REQUIRED_BLOCKERS)
        ) and all(
            all(
                isinstance(item.get(field), str) and bool(item[field].strip())
                for field in (
                    "id",
                    "evidence_ref",
                    "owner",
                    "required_evidence",
                    "reconsider_when",
                )
            )
            and item["evidence_ref"] == REQUIRED_BLOCKERS[blocker_id]
            and _contained_file(lab_dir, item["evidence_ref"])
            for blocker_id, item in blockers_by_id.items()
        )
        evidence_refs = decision.get("evidence_refs", [])
        refs_ok = (
            isinstance(evidence_refs, list)
            and len(evidence_refs) == 3
            and set(evidence_refs)
            == {
                "01-manifest-check.json",
                "02-unknown-effect.json",
                "03-retirement-check.json",
            }
            and all(
                isinstance(reference, str) and _contained_file(lab_dir, reference)
                for reference in evidence_refs
            )
        )
        decision_ok = (
            decision.get("decision") == "hold"
            and decision.get("scope") == "first_wave"
            and decision.get("control_action") == "not_started"
            and isinstance(decision.get("owner"), str)
            and bool(decision["owner"].strip())
            and blocker_schema_ok
            and refs_ok
        )
        record(
            "release_decision",
            decision_ok,
            "hold decision must own and link both observed blockers",
        )
    except (OSError, TypeError, ValueError) as error:
        record("release_decision", False, str(error))

    try:
        manifest_ok, manifest_reason = _cumulative_manifest(artifacts_dir)
        record("cumulative_manifest", manifest_ok, manifest_reason)
    except (OSError, TypeError, ValueError, yaml.YAMLError) as error:
        record("cumulative_manifest", False, str(error))

    return {
        "valid": not failed_checks,
        "decision": "hold" if "release_decision" in passed_checks else None,
        "lab8_files": len(present),
        "manifest_artifacts": len(LAB_ARTIFACTS),
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the Lab 8 evidence package.")
    parser.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_lab8_package(args.artifacts_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
