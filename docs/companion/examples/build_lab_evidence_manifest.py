from __future__ import annotations

import argparse
import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

import yaml

LAB_ARTIFACTS: Final[tuple[tuple[int, str, str], ...]] = (
    (1, "lab-01", "lab-01/decision.md"),
    (2, "lab-02", "lab-02/approval-state.json"),
    (3, "lab-03", "lab-03/memory-boundary.md"),
    (4, "lab-04-pre-dispatch", "lab-04/pre-dispatch-timeout.json"),
    (4, "lab-04", "lab-04/unknown-effect.json"),
    (5, "lab-05", "lab-05/evidence.yaml"),
    (6, "lab-06", "lab-06/ownership-registry-change.yaml"),
    (7, "lab-07", "lab-07/assurance-drill.yaml"),
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(
    artifacts_dir: Path,
    *,
    through: int,
    subject: str,
    measured_at: str,
) -> dict[str, object]:
    if not 1 <= through <= 7:
        raise ValueError("through must be between 1 and 7")

    artifacts: list[dict[str, str]] = []
    signals: dict[str, dict[str, object]] = {}
    for laboratory, artifact_id, relative_path in LAB_ARTIFACTS:
        if laboratory > through:
            continue
        path = artifacts_dir / relative_path
        if not path.is_file():
            raise FileNotFoundError(f"Missing laboratory artifact: {path}")
        artifacts.append(
            {
                "id": artifact_id,
                "path": relative_path,
                "sha256": _sha256(path),
            }
        )
        signal_id = artifact_id.replace("-", "_") + "_observed"
        signals[signal_id] = {"value": True, "artifact_refs": [artifact_id]}

    return {
        "version": 1,
        "issuer": "reader-laboratory",
        "subject": subject,
        "measured_at": measured_at,
        "artifacts": artifacts,
        "signals": signals,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the cumulative evidence manifest for laboratories 1-7."
    )
    parser.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--through", type=int, default=7)
    parser.add_argument("--subject", default="support-triage-ref@reader-lab")
    parser.add_argument(
        "--measured-at",
        default=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    artifacts_dir = args.artifacts_dir.resolve()
    output = args.output or artifacts_dir / "evidence-manifest.yaml"
    manifest = build_manifest(
        artifacts_dir,
        through=args.through,
        subject=args.subject,
        measured_at=args.measured_at,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()
