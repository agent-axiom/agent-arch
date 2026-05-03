from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


def _read_required_string(record: Mapping[str, Any], key: str, *, idx: int) -> str:
    value = str(record.get(key, "")).strip()
    if not value:
        raise ValueError(f"Memory record #{idx} field is required: {key}")
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
                    memory_id=str(record.get("memory_id", f"mem-{idx:03d}")),
                    tenant_id=_read_required_string(record, "tenant_id", idx=idx),
                    memory_class=_read_required_string(record, "memory_class", idx=idx),
                    kind=_read_required_string(record, "kind", idx=idx),
                    content=_read_required_string(record, "content", idx=idx),
                    source=_read_required_string(record, "source", idx=idx),
                    confidence=float(record.get("confidence", 0.5)),
                    provenance=str(record.get("provenance", "unknown")),
                    revision=int(record.get("revision", 1)),
                ),
            )
        return cls(records=records)

    def all(self) -> tuple[MemoryRecord, ...]:
        return tuple(self._records)

    def retrieve(self, query: str, tenant_id: str, *, limit: int = 3) -> list[MemoryRecord]:
        query_tokens = {token for token in query.lower().split() if token}
        scoped = [record for record in self._records if record.tenant_id == tenant_id]
        ranked = sorted(
            scoped,
            key=lambda record: self._score(record, query_tokens),
            reverse=True,
        )
        return ranked[:limit]

    def persist(self, candidate: MemoryCandidate) -> MemoryRecord:
        revision = 1
        if candidate.revision_mode == "replace":
            prior_revisions = [
                record.revision
                for record in self._records
                if record.tenant_id == candidate.tenant_id
                and record.memory_class == candidate.memory_class
                and record.kind == candidate.kind
            ]
            revision = (max(prior_revisions) if prior_revisions else 0) + 1
        self._counter += 1
        record = MemoryRecord(
            memory_id=f"mem-{self._counter:03d}",
            tenant_id=candidate.tenant_id,
            memory_class=candidate.memory_class,
            kind=candidate.kind,
            content=candidate.content,
            source=candidate.source,
            confidence=candidate.confidence,
            provenance=candidate.provenance,
            revision=revision,
        )
        self._records.append(record)
        return record

    def compact(self, tenant_id: str) -> int:
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
