from __future__ import annotations

from dataclasses import dataclass
from time import monotonic


@dataclass(slots=True)
class StructuredEvent:
    event_type: str
    trace_id: str
    payload: dict[str, str]


class TelemetryEmitter:
    """In-memory telemetry store for examples and tests."""

    def __init__(self) -> None:
        self.events: list[StructuredEvent] = []

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
