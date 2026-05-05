from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from time import monotonic

SCHEMA_VERSION = "1.0"
REDACTED_VALUE = "[REDACTED]"


@dataclass(slots=True)
class StructuredEvent:
    event_type: str
    trace_id: str
    payload: dict[str, str]
    schema_version: str = SCHEMA_VERSION
    redacted_fields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.payload, dict):
            raise TypeError("Telemetry event payload must be a mapping")
        if not isinstance(self.redacted_fields, tuple):
            raise TypeError("Telemetry event redacted_fields must be a tuple")
        self.payload = {str(key): str(value) for key, value in self.payload.items()}
        self.redacted_fields = self._normalize_redacted_fields(self.redacted_fields)
        self.event_type = self.event_type.strip()
        if not self.event_type:
            raise ValueError("Telemetry event field must not be empty: event_type")
        self.trace_id = self.trace_id.strip()
        if not self.trace_id:
            raise ValueError("Telemetry event field must not be empty: trace_id")
        schema_version = self.schema_version.strip()
        if not schema_version:
            raise ValueError("Telemetry event field must not be empty: schema_version")
        if schema_version != SCHEMA_VERSION:
            raise ValueError(
                f"Telemetry schema version is not supported: {schema_version}"
            )
        self.schema_version = schema_version

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "event_type": self.event_type,
            "trace_id": self.trace_id,
            "payload": dict(self.payload),
            "redacted_fields": list(self.redacted_fields),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> StructuredEvent:
        required_values: dict[str, str] = {}
        for required_field in ("event_type", "trace_id"):
            if required_field not in data:
                raise ValueError(
                    f"Telemetry event is missing required field: {required_field}"
                )
            value = str(data[required_field]).strip()
            if not value:
                raise ValueError(
                    f"Telemetry event field must not be empty: {required_field}"
                )
            required_values[required_field] = value
        schema_version = str(data.get("schema_version", SCHEMA_VERSION)).strip()
        if not schema_version:
            raise ValueError("Telemetry event field must not be empty: schema_version")
        if schema_version != SCHEMA_VERSION:
            raise ValueError(f"Telemetry schema version is not supported: {schema_version}")
        payload = data.get("payload", {})
        if not isinstance(payload, dict):
            raise TypeError("payload must be a mapping")
        normalized_payload: dict[str, str] = {}
        for key, value in payload.items():
            payload_key = str(key)
            if not isinstance(value, str):
                raise TypeError(
                    f"Telemetry event payload value must be a string: {payload_key}"
                )
            normalized_payload[payload_key] = value
        redacted_fields = data.get("redacted_fields", [])
        if not isinstance(redacted_fields, list):
            raise TypeError("redacted_fields must be a list")
        return cls(
            schema_version=schema_version,
            event_type=required_values["event_type"],
            trace_id=required_values["trace_id"],
            payload=normalized_payload,
            redacted_fields=tuple(str(item) for item in redacted_fields),
        )

    @staticmethod
    def _normalize_redacted_fields(redacted_fields: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(str(field).strip() for field in redacted_fields)
        if "" in normalized:
            raise ValueError("Telemetry redact field must not be empty")
        return tuple(dict.fromkeys(normalized))


class TelemetryEmitter:
    """In-memory telemetry store for examples and tests."""

    def __init__(self) -> None:
        self.events: list[StructuredEvent] = []

    def as_dicts(self) -> list[dict[str, object]]:
        return [event.as_dict() for event in self.events]

    def events_for_trace(self, trace_id: str) -> list[StructuredEvent]:
        return [event for event in self.events if event.trace_id == trace_id]

    def export_jsonl(
        self,
        path: str | Path,
        *,
        redact_fields: tuple[str, ...] = (),
    ) -> Path:
        normalized_redact_fields = self._normalize_redact_fields(redact_fields)
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            for event in self.events:
                serialized = event
                if normalized_redact_fields:
                    serialized = self._redact_event(event, normalized_redact_fields)
                handle.write(json.dumps(serialized.as_dict(), ensure_ascii=True))
                handle.write("\n")
        return output_path

    @staticmethod
    def load_jsonl(path: str | Path) -> list[StructuredEvent]:
        input_path = Path(path)
        events: list[StructuredEvent] = []
        with input_path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    raw_event = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Telemetry event line is not valid JSON: {line_number}"
                    ) from exc
                if not isinstance(raw_event, dict):
                    raise TypeError("Telemetry event must be a mapping")
                events.append(StructuredEvent.from_dict(raw_event))
        return events

    def emit(self, event_type: str, trace_id: str, **payload: str) -> None:
        self.events.append(
            StructuredEvent(event_type=event_type, trace_id=trace_id, payload=payload),
        )

    @staticmethod
    def _normalize_redact_fields(redact_fields: tuple[str, ...]) -> tuple[str, ...]:
        return StructuredEvent._normalize_redacted_fields(redact_fields)

    @staticmethod
    def _redact_event(
        event: StructuredEvent,
        redact_fields: tuple[str, ...],
    ) -> StructuredEvent:
        redacted_keys = tuple(
            key for key in event.payload if key in set(redact_fields)
        )
        if not redacted_keys:
            return event
        payload = dict(event.payload)
        for key in redacted_keys:
            payload[key] = REDACTED_VALUE
        return StructuredEvent(
            event_type=event.event_type,
            trace_id=event.trace_id,
            payload=payload,
            schema_version=event.schema_version,
            redacted_fields=redacted_keys,
        )

    def traced_call(self, trace_id: str, span_name: str, fn) -> object:
        started = monotonic()
        status = "success"
        try:
            return fn()
        except Exception:
            status = "failure"
            raise
        finally:
            duration_ms = int((monotonic() - started) * 1000)
            self.emit(
                "span",
                trace_id,
                span_name=span_name,
                status=status,
                duration_ms=str(duration_ms),
            )
