from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from math import isfinite
from threading import Lock

from agent_runtime_ref.models import (
    ToolResult,
    normalize_tool_arguments,
    normalize_tool_capability_name,
)


def _read_required_string(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Idempotency field must be a string: {field}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"Idempotency field is required: {field}")
    return normalized


def _read_now(value: datetime | None) -> datetime:
    now = datetime.now(UTC) if value is None else value
    if not isinstance(now, datetime):
        raise TypeError("Idempotency clock value must be a datetime")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Idempotency clock value must be timezone-aware")
    return now


def _clone_result(result: ToolResult) -> ToolResult:
    return ToolResult(
        capability_name=result.capability_name,
        status=result.status,
        payload=dict(result.payload),
        side_effect_status=result.side_effect_status,
    )


def compute_idempotency_request_digest(
    *,
    capability_name: object,
    arguments: object,
    tenant_id: object,
    principal_id: object,
) -> str:
    payload = {
        "arguments": dict(sorted(normalize_tool_arguments(arguments).items())),
        "capability": normalize_tool_capability_name(capability_name),
        "principal_id": _read_required_string(principal_id, field="principal_id"),
        "tenant_id": _read_required_string(tenant_id, field="tenant_id"),
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class IdempotencyDecision:
    action: str
    result: ToolResult | None = None


@dataclass(slots=True)
class _IdempotencyRecord:
    request_digest: str
    state: str
    expires_at: datetime
    result: ToolResult | None = None


class IdempotencyStore:
    """Thread-safe teaching adapter; production deployments need durable storage."""

    def __init__(self, *, ttl: timedelta = timedelta(hours=24)) -> None:
        if not isinstance(ttl, timedelta):
            raise TypeError("Idempotency TTL must be a timedelta")
        if not isfinite(ttl.total_seconds()) or ttl <= timedelta(0):
            raise ValueError("Idempotency TTL must be positive")
        self._ttl = ttl
        self._records: dict[str, _IdempotencyRecord] = {}
        self._lock = Lock()

    def reserve(
        self,
        idempotency_key: object,
        request_digest: object,
        *,
        now: datetime | None = None,
    ) -> IdempotencyDecision:
        key = _read_required_string(idempotency_key, field="idempotency_key")
        digest = _read_required_string(request_digest, field="request_digest")
        observed_at = _read_now(now)
        with self._lock:
            record = self._records.get(key)
            if record is None:
                self._records[key] = _IdempotencyRecord(
                    request_digest=digest,
                    state="in_progress",
                    expires_at=observed_at + self._ttl,
                )
                return IdempotencyDecision("execute")
            if record.request_digest != digest:
                return IdempotencyDecision("conflict")
            if record.state == "side_effect_unknown":
                return IdempotencyDecision("reconcile", _clone_optional(record.result))
            if observed_at >= record.expires_at:
                self._records[key] = _IdempotencyRecord(
                    request_digest=digest,
                    state="in_progress",
                    expires_at=observed_at + self._ttl,
                )
                return IdempotencyDecision("execute")
            if record.state == "succeeded":
                return IdempotencyDecision("replay", _clone_optional(record.result))
            if record.state == "in_progress":
                return IdempotencyDecision("wait")
            if record.state == "retryable_failure":
                record.state = "in_progress"
                record.expires_at = observed_at + self._ttl
                record.result = None
                return IdempotencyDecision("execute")
            raise RuntimeError(f"Unsupported idempotency state: {record.state}")

    def complete(
        self,
        idempotency_key: object,
        request_digest: object,
        result: ToolResult,
        *,
        now: datetime | None = None,
    ) -> None:
        key = _read_required_string(idempotency_key, field="idempotency_key")
        digest = _read_required_string(request_digest, field="request_digest")
        if not isinstance(result, ToolResult):
            raise TypeError("Idempotency result must be a ToolResult")
        observed_at = _read_now(now)
        with self._lock:
            record = self._records.get(key)
            if record is None or record.request_digest != digest:
                raise ValueError("Idempotency reservation does not match completion")
            if record.state != "in_progress":
                raise ValueError("Idempotency reservation is not in progress")
            record.state = _state_for_result(result)
            record.expires_at = observed_at + self._ttl
            record.result = _clone_result(result)


def _clone_optional(result: ToolResult | None) -> ToolResult | None:
    return None if result is None else _clone_result(result)


def _state_for_result(result: ToolResult) -> str:
    unresolved_effects = {"side_effect_unknown", "partial_side_effect"}
    if result.outcome in unresolved_effects or result.side_effect_status in unresolved_effects:
        return "side_effect_unknown"
    if result.status == "success":
        return "succeeded"
    if result.side_effect_status == "not_executed":
        return "retryable_failure"
    return "side_effect_unknown"
