from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, cast

import yaml

_SHA256_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")
_SUPPORTED_VERSION = "1"


@dataclass(frozen=True, slots=True)
class EvidenceDiagnostic:
    code: str
    location: str
    message: str


@dataclass(frozen=True, slots=True)
class EvidenceVerificationResult:
    verified: bool
    diagnostics: tuple[EvidenceDiagnostic, ...]
    version: str | None = None
    issuer: str | None = None
    subject: str | None = None
    measured_at: str | None = None
    artifact_ids: tuple[str, ...] = ()
    signals: Mapping[str, Any] = field(default_factory=dict)


def verify_evidence_manifest(
    manifest_path: str | Path,
    *,
    root: str | Path | None = None,
    required_artifact_ids: Sequence[str] = (),
) -> EvidenceVerificationResult:
    """Validate an evidence manifest and every artifact it references."""

    path = Path(manifest_path)
    root_path = Path(root) if root is not None else path.parent
    if root is not None and not path.is_absolute():
        path = root_path / path
    diagnostics: list[EvidenceDiagnostic] = []

    try:
        resolved_root = root_path.resolve(strict=True)
    except (OSError, RuntimeError):
        return _result(
            diagnostics=[
                EvidenceDiagnostic(
                    code="root_not_found",
                    location="root",
                    message=f"Evidence root does not exist: {root_path}",
                )
            ]
        )

    if not resolved_root.is_dir():
        return _result(
            diagnostics=[
                EvidenceDiagnostic(
                    code="invalid_root",
                    location="root",
                    message=f"Evidence root is not a directory: {root_path}",
                )
            ]
        )

    try:
        resolved_manifest = path.resolve(strict=True)
    except (OSError, RuntimeError):
        return _result(
            diagnostics=[
                EvidenceDiagnostic(
                    code="manifest_not_found",
                    location="manifest",
                    message=f"Evidence manifest does not exist: {path}",
                )
            ]
        )

    if not resolved_manifest.is_relative_to(resolved_root):
        return _result(
            diagnostics=[
                EvidenceDiagnostic(
                    code="manifest_outside_root",
                    location="manifest",
                    message="Evidence manifest resolves outside the evidence root",
                )
            ]
        )

    try:
        payload = yaml.safe_load(resolved_manifest.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        return _result(
            diagnostics=[
                EvidenceDiagnostic(
                    code="invalid_yaml",
                    location="manifest",
                    message=f"Evidence manifest is not valid YAML: {error}",
                )
            ]
        )
    except (OSError, UnicodeError) as error:
        return _result(
            diagnostics=[
                EvidenceDiagnostic(
                    code="manifest_unreadable",
                    location="manifest",
                    message=f"Evidence manifest cannot be read: {error}",
                )
            ]
        )

    if not isinstance(payload, Mapping):
        return _result(
            diagnostics=[
                EvidenceDiagnostic(
                    code="invalid_manifest",
                    location="manifest",
                    message="Evidence manifest must be a mapping",
                )
            ]
        )

    version = _validate_version(payload, diagnostics)
    issuer = _validate_required_text(payload, "issuer", diagnostics)
    subject = _validate_required_text(payload, "subject", diagnostics)
    measured_at = _validate_measured_at(payload, diagnostics)
    artifact_ids = _validate_artifacts(payload, resolved_root, diagnostics)
    _validate_required_artifact_ids(
        artifact_ids,
        required_artifact_ids,
        diagnostics,
    )
    signals = _validate_signals(payload, set(artifact_ids), diagnostics)

    return _result(
        diagnostics=diagnostics,
        version=version,
        issuer=issuer,
        subject=subject,
        measured_at=measured_at,
        artifact_ids=artifact_ids,
        signals=signals,
    )


def _validate_required_artifact_ids(
    artifact_ids: tuple[str, ...],
    required_artifact_ids: Sequence[str],
    diagnostics: list[EvidenceDiagnostic],
) -> None:
    if isinstance(required_artifact_ids, str) or not isinstance(
        required_artifact_ids, Sequence
    ):
        raise TypeError("Required artifact ids must be a sequence")
    normalized: list[str] = []
    for raw_id in required_artifact_ids:
        if not isinstance(raw_id, str):
            raise TypeError("Required artifact ids must be strings")
        artifact_id = raw_id.strip()
        if not artifact_id:
            raise ValueError("Required artifact id must not be empty")
        if artifact_id in normalized:
            raise ValueError(f"Required artifact ids must be unique: {artifact_id}")
        normalized.append(artifact_id)
    present = set(artifact_ids)
    for artifact_id in normalized:
        if artifact_id not in present:
            diagnostics.append(
                EvidenceDiagnostic(
                    code="missing_required_artifact",
                    location=f"artifacts.{artifact_id}",
                    message=f"Required artifact is missing: {artifact_id}",
                )
            )


def _validate_version(
    payload: Mapping[Any, Any], diagnostics: list[EvidenceDiagnostic]
) -> str | None:
    if "version" not in payload:
        _missing(diagnostics, "version")
        return None

    raw_version = payload["version"]
    if isinstance(raw_version, bool) or not isinstance(raw_version, (str, int)):
        _invalid(diagnostics, "version", "Version must be a string or integer")
        return None

    version = str(raw_version).strip()
    if not version:
        _invalid(diagnostics, "version", "Version cannot be empty")
        return None
    if version != _SUPPORTED_VERSION:
        diagnostics.append(
            EvidenceDiagnostic(
                code="unsupported_version",
                location="version",
                message=f"Unsupported evidence manifest version: {version}",
            )
        )
    return version


def _validate_required_text(
    payload: Mapping[Any, Any],
    field_name: str,
    diagnostics: list[EvidenceDiagnostic],
) -> str | None:
    if field_name not in payload:
        _missing(diagnostics, field_name)
        return None

    value = payload[field_name]
    if not isinstance(value, str) or not value.strip():
        _invalid(diagnostics, field_name, f"{field_name} must be a non-empty string")
        return None
    return value.strip()


def _validate_measured_at(
    payload: Mapping[Any, Any], diagnostics: list[EvidenceDiagnostic]
) -> str | None:
    if "measured_at" not in payload:
        _missing(diagnostics, "measured_at")
        return None

    raw_value = payload["measured_at"]
    if isinstance(raw_value, datetime):
        parsed = raw_value
        measured_at = raw_value.isoformat()
        if measured_at.endswith("+00:00"):
            measured_at = measured_at.removesuffix("+00:00") + "Z"
    elif isinstance(raw_value, str) and raw_value.strip():
        measured_at = raw_value.strip()
        try:
            parsed = datetime.fromisoformat(measured_at.replace("Z", "+00:00"))
        except ValueError:
            parsed = None
    else:
        _invalid(
            diagnostics,
            "measured_at",
            "measured_at must be a non-empty ISO-8601 timestamp",
        )
        return None

    if parsed is None or parsed.tzinfo is None:
        diagnostics.append(
            EvidenceDiagnostic(
                code="invalid_measured_at",
                location="measured_at",
                message="measured_at must be an ISO-8601 timestamp with a timezone",
            )
        )
    return measured_at


def _validate_artifacts(
    payload: Mapping[Any, Any],
    root: Path,
    diagnostics: list[EvidenceDiagnostic],
) -> tuple[str, ...]:
    if "artifacts" not in payload:
        _missing(diagnostics, "artifacts")
        return ()

    artifacts = payload["artifacts"]
    if not isinstance(artifacts, list) or not artifacts:
        _invalid(diagnostics, "artifacts", "artifacts must be a non-empty list")
        return ()

    artifact_ids: list[str] = []
    seen_ids: set[str] = set()
    for index, artifact in enumerate(artifacts):
        location = f"artifacts[{index}]"
        if not isinstance(artifact, Mapping):
            _invalid(diagnostics, location, "Artifact entry must be a mapping")
            continue

        artifact_id = _required_entry_text(artifact, "id", location, diagnostics)
        artifact_path = _required_entry_text(artifact, "path", location, diagnostics)
        expected_sha256 = _required_entry_text(artifact, "sha256", location, diagnostics)

        if artifact_id is not None:
            if artifact_id in seen_ids:
                diagnostics.append(
                    EvidenceDiagnostic(
                        code="duplicate_artifact_id",
                        location=f"{location}.id",
                        message=f"Duplicate artifact id: {artifact_id}",
                    )
                )
            else:
                seen_ids.add(artifact_id)
                artifact_ids.append(artifact_id)

        resolved_artifact = _resolve_artifact_path(
            artifact_path, root, f"{location}.path", diagnostics
        )
        digest_valid = _validate_sha256(expected_sha256, f"{location}.sha256", diagnostics)
        if resolved_artifact is not None and digest_valid and expected_sha256 is not None:
            _verify_artifact_digest(
                resolved_artifact,
                expected_sha256,
                f"{location}.sha256",
                diagnostics,
            )

    return tuple(artifact_ids)


def _required_entry_text(
    entry: Mapping[Any, Any],
    field_name: str,
    base_location: str,
    diagnostics: list[EvidenceDiagnostic],
) -> str | None:
    location = f"{base_location}.{field_name}"
    if field_name not in entry:
        _missing(diagnostics, location)
        return None
    value = entry[field_name]
    if not isinstance(value, str) or not value.strip():
        _invalid(diagnostics, location, f"{field_name} must be a non-empty string")
        return None
    return value.strip()


def _resolve_artifact_path(
    raw_path: str | None,
    root: Path,
    location: str,
    diagnostics: list[EvidenceDiagnostic],
) -> Path | None:
    if raw_path is None:
        return None

    candidate = Path(raw_path)
    if candidate.is_absolute():
        diagnostics.append(
            EvidenceDiagnostic(
                code="artifact_outside_root",
                location=location,
                message="Artifact path must be relative to the evidence root",
            )
        )
        return None

    try:
        resolved = (root / candidate).resolve(strict=False)
    except (OSError, RuntimeError, ValueError) as error:
        _invalid(diagnostics, location, f"Artifact path cannot be resolved: {error}")
        return None

    if not resolved.is_relative_to(root):
        diagnostics.append(
            EvidenceDiagnostic(
                code="artifact_outside_root",
                location=location,
                message="Artifact path resolves outside the evidence root",
            )
        )
        return None
    if not resolved.exists():
        diagnostics.append(
            EvidenceDiagnostic(
                code="artifact_not_found",
                location=location,
                message=f"Artifact does not exist: {raw_path}",
            )
        )
        return None
    if not resolved.is_file():
        diagnostics.append(
            EvidenceDiagnostic(
                code="artifact_not_file",
                location=location,
                message=f"Artifact is not a regular file: {raw_path}",
            )
        )
        return None
    return resolved


def _validate_sha256(
    value: str | None, location: str, diagnostics: list[EvidenceDiagnostic]
) -> bool:
    if value is None:
        return False
    if _SHA256_PATTERN.fullmatch(value) is None:
        diagnostics.append(
            EvidenceDiagnostic(
                code="invalid_sha256",
                location=location,
                message="sha256 must contain exactly 64 hexadecimal characters",
            )
        )
        return False
    return True


def _verify_artifact_digest(
    path: Path,
    expected: str,
    location: str,
    diagnostics: list[EvidenceDiagnostic],
) -> None:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as artifact_file:
            for chunk in iter(lambda: artifact_file.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        diagnostics.append(
            EvidenceDiagnostic(
                code="artifact_unreadable",
                location=location.removesuffix(".sha256") + ".path",
                message=f"Artifact cannot be read: {error}",
            )
        )
        return

    if digest.hexdigest() != expected.lower():
        diagnostics.append(
            EvidenceDiagnostic(
                code="sha256_mismatch",
                location=location,
                message=f"Artifact SHA-256 does not match: {path.name}",
            )
        )


def _validate_signals(
    payload: Mapping[Any, Any],
    artifact_ids: set[str],
    diagnostics: list[EvidenceDiagnostic],
) -> dict[str, Any]:
    if "signals" not in payload:
        _missing(diagnostics, "signals")
        return {}

    entries = _normalize_signal_entries(payload["signals"], diagnostics)
    normalized: dict[str, Any] = {}
    seen_ids: set[str] = set()
    for raw_id, raw_signal, location in entries:
        normalized_entry = _validate_signal_entry(
            raw_id,
            raw_signal,
            location,
            artifact_ids,
            seen_ids,
            diagnostics,
        )
        if normalized_entry is not None:
            signal_id, value = normalized_entry
            normalized.setdefault(signal_id, value)

    return normalized


def _normalize_signal_entries(
    raw: Any,
    diagnostics: list[EvidenceDiagnostic],
) -> list[tuple[Any, Any, str]]:
    entries: list[tuple[Any, Any, str]] = []
    if isinstance(raw, Mapping):
        entries = [(signal_id, signal, f"signals.{signal_id}") for signal_id, signal in raw.items()]
    elif isinstance(raw, list):
        for index, signal in enumerate(raw):
            location = f"signals[{index}]"
            if not isinstance(signal, Mapping):
                entries.append((None, signal, location))
                continue
            signal_mapping = cast(Mapping[Any, Any], signal)
            entries.append((signal_mapping.get("id"), signal_mapping, location))
    else:
        _invalid(diagnostics, "signals", "signals must be a mapping or list")
        return []

    if not entries:
        _invalid(diagnostics, "signals", "signals cannot be empty")
    return entries


def _validate_signal_entry(
    raw_id: Any,
    raw_signal: Any,
    location: str,
    artifact_ids: set[str],
    seen_ids: set[str],
    diagnostics: list[EvidenceDiagnostic],
) -> tuple[str, Any] | None:
    signal_id = _validate_signal_id(raw_id, location, diagnostics)
    if signal_id is not None:
        if signal_id in seen_ids:
            diagnostics.append(
                EvidenceDiagnostic(
                    code="duplicate_signal_id",
                    location=f"{location}.id",
                    message=f"Duplicate signal id: {signal_id}",
                )
            )
        else:
            seen_ids.add(signal_id)

    if not isinstance(raw_signal, Mapping):
        _invalid(diagnostics, location, "Signal entry must be a mapping")
        return None

    normalized_entry: tuple[str, Any] | None = None
    value_location = f"{location}.value"
    if "value" not in raw_signal:
        _missing(diagnostics, value_location)
    elif raw_signal["value"] is None:
        _invalid(diagnostics, value_location, "Signal value cannot be null")
    elif signal_id is not None:
        normalized_entry = (signal_id, raw_signal["value"])

    _validate_signal_artifact_refs(raw_signal, location, artifact_ids, diagnostics)
    return normalized_entry


def _validate_signal_artifact_refs(
    raw_signal: Mapping[Any, Any],
    location: str,
    artifact_ids: set[str],
    diagnostics: list[EvidenceDiagnostic],
) -> None:
    refs_location = f"{location}.artifact_refs"
    if "artifact_refs" not in raw_signal:
        _missing(diagnostics, refs_location)
        return

    refs = raw_signal["artifact_refs"]
    if not isinstance(refs, list) or not refs:
        _invalid(
            diagnostics,
            refs_location,
            "artifact_refs must be a non-empty list of artifact ids",
        )
        return

    for ref_index, artifact_ref in enumerate(refs):
        ref_location = f"{refs_location}[{ref_index}]"
        if not isinstance(artifact_ref, str) or not artifact_ref.strip():
            _invalid(diagnostics, ref_location, "Artifact reference must be a string")
        elif artifact_ref not in artifact_ids:
            diagnostics.append(
                EvidenceDiagnostic(
                    code="unknown_artifact_ref",
                    location=ref_location,
                    message=f"Unknown artifact reference: {artifact_ref}",
                )
            )


def _validate_signal_id(
    value: object, location: str, diagnostics: list[EvidenceDiagnostic]
) -> str | None:
    id_location = f"{location}.id"
    if value is None:
        _missing(diagnostics, id_location)
        return None
    if not isinstance(value, str) or not value.strip():
        _invalid(diagnostics, id_location, "Signal id must be a non-empty string")
        return None
    return value.strip()


def _missing(diagnostics: list[EvidenceDiagnostic], location: str) -> None:
    diagnostics.append(
        EvidenceDiagnostic(
            code="missing_field",
            location=location,
            message=f"Required field is missing: {location}",
        )
    )


def _invalid(diagnostics: list[EvidenceDiagnostic], location: str, message: str) -> None:
    diagnostics.append(EvidenceDiagnostic(code="invalid_field", location=location, message=message))


def _result(
    *,
    diagnostics: list[EvidenceDiagnostic],
    version: str | None = None,
    issuer: str | None = None,
    subject: str | None = None,
    measured_at: str | None = None,
    artifact_ids: tuple[str, ...] = (),
    signals: Mapping[str, Any] | None = None,
) -> EvidenceVerificationResult:
    return EvidenceVerificationResult(
        verified=not diagnostics,
        diagnostics=tuple(diagnostics),
        version=version,
        issuer=issuer,
        subject=subject,
        measured_at=measured_at,
        artifact_ids=artifact_ids,
        signals={} if signals is None else dict(signals),
    )
