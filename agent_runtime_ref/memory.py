from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, Mapping


def _read_required_string(record: Mapping[str, Any], key: str, *, idx: int) -> str:
    value = record.get(key, "")
    if not isinstance(value, str):
        raise TypeError(f"Memory record #{idx} field must be a string: {key}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"Memory record #{idx} field is required: {key}")
    return normalized


def _read_memory_id(record: Mapping[str, Any], *, idx: int) -> str:
    value = record.get("memory_id", f"mem-{idx:03d}")
    if not isinstance(value, str):
        raise TypeError(f"Memory record #{idx} field must be a string: memory_id")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"Memory record #{idx} field is required: memory_id")
    return normalized


def _read_confidence(record: Mapping[str, Any], *, idx: int) -> float:
    value = record.get("confidence", 0.5)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"Memory record #{idx} confidence must be a number")
    confidence = float(value)
    if not isfinite(confidence) or confidence < 0 or confidence > 1:
        raise ValueError(f"Memory record #{idx} confidence must be between 0 and 1")
    return confidence


def _read_revision(record: Mapping[str, Any], *, idx: int) -> int:
    value = record.get("revision", 1)
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"Memory record #{idx} revision must be an integer")
    if value < 1:
        raise ValueError(f"Memory record #{idx} revision must be positive")
    return value


def _read_record_string(value: str, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Memory record field must be a string: {field}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"Memory record field is required: {field}")
    return normalized


def _read_record_confidence(value: float) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError("Memory record confidence must be a number")
    confidence = float(value)
    if not isfinite(confidence) or confidence < 0 or confidence > 1:
        raise ValueError("Memory record confidence must be between 0 and 1")
    return confidence


def _read_record_revision(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("Memory record revision must be an integer")
    if value < 1:
        raise ValueError("Memory record revision must be positive")
    return value


def _read_candidate_confidence(value: float) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError("Memory candidate confidence must be a number")
    confidence = float(value)
    if not isfinite(confidence) or confidence < 0 or confidence > 1:
        raise ValueError("Memory candidate confidence must be between 0 and 1")
    return confidence


def _read_optional_seed_string(value: object, *, field: str, idx: int) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Memory record #{idx} field must be a string: {field}")
    return value.strip()


def _read_candidate_string(value: str, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Memory candidate field must be a string: {field}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"Memory candidate field is required: {field}")
    return normalized


def _read_lookup_string(value: str, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Memory lookup field must be a string: {field}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"Memory lookup field is required: {field}")
    return normalized


def _read_lookup_limit(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("Memory lookup limit must be an integer")
    if value < 0:
        raise ValueError("Memory lookup limit must be non-negative")
    return value


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    tenant_id: str
    memory_class: str
    kind: str
    content: str
    source: str
    confidence: float
    provenance: str = "unknown"
    revision: int = 1

    def __post_init__(self) -> None:
        for field in (
            "memory_id",
            "tenant_id",
            "memory_class",
            "kind",
            "content",
            "source",
            "provenance",
        ):
            object.__setattr__(
                self,
                field,
                _read_record_string(getattr(self, field), field=field),
            )
        object.__setattr__(self, "confidence", _read_record_confidence(self.confidence))
        object.__setattr__(self, "revision", _read_record_revision(self.revision))


@dataclass(frozen=True, slots=True)
class MemoryCandidate:
    tenant_id: str
    memory_class: str
    kind: str
    content: str
    source: str
    confidence: float
    provenance: str
    revision_mode: str = "append"


class MemoryStore:
    """Small in-memory store with explicit record classes and tenant filtering."""

    def __init__(self, records: list[MemoryRecord] | None = None) -> None:
        self._records = list(records or self._default_records())
        for record in self._records:
            if not isinstance(record, MemoryRecord):
                raise TypeError("Memory store records must be MemoryRecord")
        self._counter = len(self._records)

    @staticmethod
    def _default_records() -> list[MemoryRecord]:
        return [
            MemoryRecord(
                memory_id="mem-001",
                tenant_id="tenant-acme",
                memory_class="profile",
                kind="language_preference",
                content="User usually prefers concise English answers.",
                source="trusted_profile",
                confidence=0.95,
                provenance="user_confirmed_preference",
            ),
            MemoryRecord(
                memory_id="mem-002",
                tenant_id="tenant-acme",
                memory_class="long_term",
                kind="validated_fact",
                content="Support tickets must use the support queue and include requester_id.",
                source="trusted_service",
                confidence=0.92,
                provenance="validated_service_rule",
            ),
            MemoryRecord(
                memory_id="mem-003",
                tenant_id="tenant-acme",
                memory_class="short_term",
                kind="working_note",
                content="Recent runtime demo used create_ticket as the main write capability.",
                source="session_state",
                confidence=0.7,
                provenance="ephemeral_session_note",
            ),
        ]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MemoryStore":
        raw_memory = data.get("memory", {})
        if not isinstance(raw_memory, Mapping):
            raise TypeError("'memory' must be a mapping")
        raw_records = raw_memory.get("seed_records", [])
        if not isinstance(raw_records, list):
            raise TypeError("'seed_records' must be a list")
        records: list[MemoryRecord] = []
        for idx, raw_record in enumerate(raw_records, start=1):
            if not isinstance(raw_record, Mapping):
                raise TypeError(f"Memory record #{idx} must be a mapping")
            record = dict(raw_record)
            records.append(
                MemoryRecord(
                    memory_id=_read_memory_id(record, idx=idx),
                    tenant_id=_read_required_string(record, "tenant_id", idx=idx),
                    memory_class=_read_required_string(record, "memory_class", idx=idx),
                    kind=_read_required_string(record, "kind", idx=idx),
                    content=_read_required_string(record, "content", idx=idx),
                    source=_read_required_string(record, "source", idx=idx),
                    confidence=_read_confidence(record, idx=idx),
                    provenance=_read_optional_seed_string(
                        record.get("provenance", "unknown"),
                        field="provenance",
                        idx=idx,
                    ),
                    revision=_read_revision(record, idx=idx),
                ),
            )
        return cls(records=records)

    def all(self) -> tuple[MemoryRecord, ...]:
        return tuple(self._records)

    def retrieve(self, query: str, tenant_id: str, *, limit: int = 3) -> list[MemoryRecord]:
        query = _read_lookup_string(query, field="query")
        tenant_id = _read_lookup_string(tenant_id, field="tenant_id")
        limit = _read_lookup_limit(limit)
        query_tokens = {token for token in query.lower().split() if token}
        scoped = [record for record in self._records if record.tenant_id == tenant_id]
        ranked = sorted(
            scoped,
            key=lambda record: self._score(record, query_tokens),
            reverse=True,
        )
        return ranked[:limit]

    def persist(self, candidate: MemoryCandidate) -> MemoryRecord:
        tenant_id = _read_candidate_string(candidate.tenant_id, field="tenant_id")
        memory_class = _read_candidate_string(candidate.memory_class, field="memory_class")
        kind = _read_candidate_string(candidate.kind, field="kind")
        content = _read_candidate_string(candidate.content, field="content")
        source = _read_candidate_string(candidate.source, field="source")
        provenance = _read_candidate_string(candidate.provenance, field="provenance")
        if not isinstance(candidate.revision_mode, str):
            raise TypeError("Memory candidate revision mode must be a string")
        revision_mode = candidate.revision_mode.strip()
        if revision_mode not in {"append", "replace"}:
            raise ValueError(
                f"Memory candidate revision mode is not supported: {revision_mode}"
            )
        confidence = _read_candidate_confidence(candidate.confidence)
        revision = 1
        if revision_mode == "replace":
            prior_revisions = [
                record.revision
                for record in self._records
                if record.tenant_id == tenant_id
                and record.memory_class == memory_class
                and record.kind == kind
            ]
            revision = (max(prior_revisions) if prior_revisions else 0) + 1
        self._counter += 1
        record = MemoryRecord(
            memory_id=f"mem-{self._counter:03d}",
            tenant_id=tenant_id,
            memory_class=memory_class,
            kind=kind,
            content=content,
            source=source,
            confidence=confidence,
            provenance=provenance,
            revision=revision,
        )
        self._records.append(record)
        return record

    def compact(self, tenant_id: str) -> int:
        tenant_id = _read_lookup_string(tenant_id, field="tenant_id")
        seen: set[tuple[str, str, str]] = set()
        compacted: list[MemoryRecord] = []
        removed = 0
        for record in self._records:
            if record.tenant_id != tenant_id:
                compacted.append(record)
                continue
            key = (record.memory_class, record.kind, record.content)
            if key in seen:
                removed += 1
                continue
            seen.add(key)
            compacted.append(record)
        self._records = compacted
        return removed

    @staticmethod
    def _score(record: MemoryRecord, query_tokens: set[str]) -> float:
        content_tokens = set(record.content.lower().split())
        overlap = len(query_tokens & content_tokens)
        class_bonus = {
            "profile": 0.15,
            "long_term": 0.1,
            "short_term": 0.05,
        }.get(record.memory_class, 0.0)
        trusted_bonus = 0.1 if record.source.startswith("trusted") else 0.0
        return overlap + record.confidence + class_bonus + trusted_bonus
