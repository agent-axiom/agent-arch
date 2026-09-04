from __future__ import annotations

import argparse
import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

import yaml


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_id(path: Path) -> str:
    return path.as_posix().replace("/", "-").replace("_", "-").replace(".", "-")


def build_capstone_manifest(
    package_dir: Path,
    *,
    measured_at: str,
    issuer: str = "agent-arch-capstone-reader",
    subject: str = "support-triage-ref",
    output: Path | None = None,
) -> dict[str, object]:
    """Build and write a hash-linked manifest for a capstone package."""

    package_dir = package_dir.resolve()
    package_dir.mkdir(parents=True, exist_ok=True)
    output_path = (output or package_dir / "evidence-manifest.yaml").resolve()
    artifact_files = sorted(
        path for path in package_dir.rglob("*") if path.is_file() and path.resolve() != output_path
    )
    artifacts = [
        {
            "id": _artifact_id(path.relative_to(package_dir)),
            "path": path.relative_to(package_dir).as_posix(),
            "sha256": _sha256(path),
        }
        for path in artifact_files
    ]
    manifest: dict[str, object] = {
        "version": 1,
        "issuer": issuer,
        "subject": subject,
        "measured_at": measured_at,
        "artifacts": artifacts,
        "signals": {
            "capstone_package_built": {
                "value": True,
                "artifact_refs": [item["id"] for item in artifacts],
            }
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the evidence manifest for a capstone package."
    )
    parser.add_argument("--package-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--issuer", default="agent-arch-capstone-reader")
    parser.add_argument("--subject", default="support-triage-ref")
    parser.add_argument(
        "--measured-at",
        default=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    package_dir = args.package_dir.resolve()
    output = args.output or package_dir / "evidence-manifest.yaml"
    build_capstone_manifest(
        package_dir,
        measured_at=args.measured_at,
        issuer=args.issuer,
        subject=args.subject,
        output=output,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
