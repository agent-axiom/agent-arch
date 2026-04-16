from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class RunRecord:
    trace_id: str
    session_id: str
    status: str
    user_input: str
    output_text: str
    capability_session_id: str = ""
    capability_session_status: str = ""
    authorization_mode: str = "platform_owned"
    delegated_principal_id: str = ""
    delegated_scope: str = ""


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
        capability_session_id: str = "",
        capability_session_status: str = "",
        authorization_mode: str = "platform_owned",
        delegated_principal_id: str = "",
        delegated_scope: str = "",
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
            capability_session_id=capability_session_id,
            capability_session_status=capability_session_status,
            authorization_mode=authorization_mode,
            delegated_principal_id=delegated_principal_id,
            delegated_scope=delegated_scope,
        )
        self._runs.append(record)
        return record

    def get_session(self, session_id: str) -> SessionRecord | None:
        return self._sessions.get(session_id)

    def runs_for_session(self, session_id: str) -> tuple[RunRecord, ...]:
        return tuple(run for run in self._runs if run.session_id == session_id)

    def export_session_json(
        self,
        session_id: str,
        *,
        output_path: str | Path,
    ) -> Path:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = self._session_payload(session_id)
        with destination.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=True, indent=2)
            handle.write("\n")
        return destination

    def export_eval_dataset_json(
        self,
        session_ids: tuple[str, ...],
        *,
        output_path: str | Path,
        dataset_name: str,
        eval_specs: dict[str, dict[str, object]] | None = None,
    ) -> Path:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        sessions = []
        for session_id in session_ids:
            payload = self._session_payload(session_id)
            if eval_specs is not None and session_id in eval_specs:
                payload["eval"] = eval_specs[session_id]
            sessions.append(payload)
        run_count = sum(
            summarize_session(session_id, self.runs_for_session(session_id)).total_runs
            for session_id in session_ids
        )
        payload = {
            "dataset_name": dataset_name,
            "session_count": len(sessions),
            "run_count": run_count,
            "sessions": sessions,
        }
        with destination.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=True, indent=2)
            handle.write("\n")
        return destination

    def _session_payload(self, session_id: str) -> dict[str, object]:
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session not found: {session_id}")
        runs = self.runs_for_session(session_id)
        summary = summarize_session(session_id, runs)
        return {
            "session": {
                "session_id": session.session_id,
                "tenant_id": session.tenant_id,
                "principal_id": session.principal_id,
                "traces": list(session.traces),
            },
            "summary": {
                "total_runs": summary.total_runs,
                "success_runs": summary.success_runs,
                "approval_wait_runs": summary.approval_wait_runs,
                "denied_runs": summary.denied_runs,
                "latest_trace_id": summary.latest_trace_id,
                "latest_status": summary.latest_status,
            },
            "runs": [
                {
                    "trace_id": run.trace_id,
                    "status": run.status,
                    "user_input": run.user_input,
                    "output_text": run.output_text,
                    "capability_session_id": run.capability_session_id,
                    "capability_session_status": run.capability_session_status,
                    "authorization_mode": run.authorization_mode,
                    "delegated_principal_id": run.delegated_principal_id,
                    "delegated_scope": run.delegated_scope,
                }
                for run in runs
            ],
        }


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
