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
        for required_field in ("event_type", "trace_id"):
            if required_field not in data:
                raise ValueError(
                    f"Telemetry event is missing required field: {required_field}"
                )
        payload = data.get("payload", {})
        if not isinstance(payload, dict):
            raise TypeError("payload must be a mapping")
        redacted_fields = data.get("redacted_fields", [])
        if not isinstance(redacted_fields, list):
            raise TypeError("redacted_fields must be a list")
        return cls(
            schema_version=str(data.get("schema_version", SCHEMA_VERSION)),
            event_type=str(data["event_type"]),
            trace_id=str(data["trace_id"]),
            payload={str(key): str(value) for key, value in payload.items()},
            redacted_fields=tuple(str(item) for item in redacted_fields),
        )


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
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            for event in self.events:
                serialized = event
                if redact_fields:
                    serialized = self._redact_event(event, redact_fields)
                handle.write(json.dumps(serialized.as_dict(), ensure_ascii=True))
                handle.write("\n")
        return output_path

    @staticmethod
    def load_jsonl(path: str | Path) -> list[StructuredEvent]:
        input_path = Path(path)
        events: list[StructuredEvent] = []
        with input_path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line:
                    continue
                raw_event = json.loads(line)
                if not isinstance(raw_event, dict):
                    raise TypeError("Telemetry event must be a mapping")
                events.append(StructuredEvent.from_dict(raw_event))
        return events

    def emit(self, event_type: str, trace_id: str, **payload: str) -> None:
        self.events.append(
            StructuredEvent(event_type=event_type, trace_id=trace_id, payload=payload),
        )

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
