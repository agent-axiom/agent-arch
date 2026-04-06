from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RunRecord:
    trace_id: str
    session_id: str
    status: str
    user_input: str
    output_text: str


@dataclass(slots=True)
class SessionRecord:
    session_id: str
    tenant_id: str
    principal_id: str
    traces: list[str] = field(default_factory=list)


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionRecord] = {}
        self._runs: list[RunRecord] = []

    def register_run(
        self,
        *,
        session_id: str,
        tenant_id: str,
        principal_id: str,
        trace_id: str,
        status: str,
        user_input: str,
        output_text: str,
    ) -> RunRecord:
        session = self._sessions.setdefault(
            session_id,
            SessionRecord(
                session_id=session_id,
                tenant_id=tenant_id,
                principal_id=principal_id,
            ),
        )
        session.traces.append(trace_id)
        record = RunRecord(
            trace_id=trace_id,
            session_id=session_id,
            status=status,
            user_input=user_input,
            output_text=output_text,
        )
        self._runs.append(record)
        return record

    def get_session(self, session_id: str) -> SessionRecord | None:
        return self._sessions.get(session_id)

    def runs_for_session(self, session_id: str) -> tuple[RunRecord, ...]:
        return tuple(run for run in self._runs if run.session_id == session_id)
