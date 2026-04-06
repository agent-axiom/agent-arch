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


@dataclass(frozen=True, slots=True)
class SessionEvalSummary:
    session_id: str
    total_runs: int
    success_runs: int
    approval_wait_runs: int
    denied_runs: int
    latest_trace_id: str | None
    latest_status: str | None


def summarize_session(
    session_id: str,
    runs: tuple[RunRecord, ...],
) -> SessionEvalSummary:
    latest = runs[-1] if runs else None
    return SessionEvalSummary(
        session_id=session_id,
        total_runs=len(runs),
        success_runs=sum(1 for run in runs if run.status == "success"),
        approval_wait_runs=sum(
            1 for run in runs if "waiting for human approval" in run.output_text.lower()
        ),
        denied_runs=sum(1 for run in runs if run.status == "denied"),
        latest_trace_id=latest.trace_id if latest is not None else None,
        latest_status=latest.status if latest is not None else None,
    )
