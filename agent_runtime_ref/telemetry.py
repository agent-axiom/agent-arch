from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from time import monotonic


@dataclass(slots=True)
class StructuredEvent:
    event_type: str
    trace_id: str
    payload: dict[str, str]

    def as_dict(self) -> dict[str, object]:
        return {
            "event_type": self.event_type,
            "trace_id": self.trace_id,
            "payload": dict(self.payload),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> StructuredEvent:
        payload = data.get("payload", {})
        if not isinstance(payload, dict):
            raise TypeError("payload must be a mapping")
        return cls(
            event_type=str(data["event_type"]),
            trace_id=str(data["trace_id"]),
            payload={str(key): str(value) for key, value in payload.items()},
        )


class TelemetryEmitter:
    """In-memory telemetry store for examples and tests."""

    def __init__(self) -> None:
        self.events: list[StructuredEvent] = []

    def as_dicts(self) -> list[dict[str, object]]:
        return [event.as_dict() for event in self.events]

    def events_for_trace(self, trace_id: str) -> list[StructuredEvent]:
        return [event for event in self.events if event.trace_id == trace_id]

    def export_jsonl(self, path: str | Path) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            for event in self.events:
                handle.write(json.dumps(event.as_dict(), ensure_ascii=True))
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
                events.append(StructuredEvent.from_dict(json.loads(line)))
        return events

    def emit(self, event_type: str, trace_id: str, **payload: str) -> None:
        self.events.append(
            StructuredEvent(event_type=event_type, trace_id=trace_id, payload=payload),
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
