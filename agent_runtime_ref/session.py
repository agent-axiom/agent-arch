from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict


class RunPayload(TypedDict):
    trace_id: str
    status: str
    user_input: str
    output_text: str
    failure_reason: str
    capability_session_id: str
    capability_session_status: str
    authorization_mode: str
    delegated_principal_id: str
    delegated_scope: str


class SessionMetadataPayload(TypedDict):
    session_id: str
    tenant_id: str
    principal_id: str
    traces: list[str]


class SessionSummaryPayload(TypedDict):
    total_runs: int
    success_runs: int
    approval_wait_runs: int
    denied_runs: int
    failed_runs: int
    traceable_failed_runs: int
    latest_trace_id: str | None
    latest_status: str | None


class SessionPayload(TypedDict, total=False):
    session: SessionMetadataPayload
    summary: SessionSummaryPayload
    runs: list[RunPayload]
    eval: dict[str, object]


@dataclass(slots=True)
class RunRecord:
    trace_id: str
    session_id: str
    status: str
    user_input: str
    output_text: str
    failure_reason: str = ""
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


def _read_required_string(value: str, *, field: str) -> str:
    normalized = str(value).strip()
    if not normalized:
        raise ValueError(f"Session field is required: {field}")
    return normalized


def _read_optional_string(value: str) -> str:
    return str(value).strip()


def _read_authorization_mode(value: str) -> str:
    authorization_mode = _read_required_string(value, field="authorization_mode")
    if authorization_mode not in {"platform_owned", "user_delegated", "human_approved"}:
        raise ValueError(f"Authorization mode is not supported: {authorization_mode}")
    return authorization_mode


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
        failure_reason: str = "",
        capability_session_id: str = "",
        capability_session_status: str = "",
        authorization_mode: str = "platform_owned",
        delegated_principal_id: str = "",
        delegated_scope: str = "",
    ) -> RunRecord:
        session_id = _read_required_string(session_id, field="session_id")
        status = _read_required_string(status, field="status")
        tenant_id = (
            _read_optional_string(tenant_id)
            if status == "denied"
            else _read_required_string(tenant_id, field="tenant_id")
        )
        principal_id = (
            _read_optional_string(principal_id)
            if status == "denied"
            else _read_required_string(principal_id, field="principal_id")
        )
        trace_id = _read_required_string(trace_id, field="trace_id")
        user_input = _read_required_string(user_input, field="user_input")
        output_text = _read_required_string(output_text, field="output_text")
        failure_reason = _read_optional_string(failure_reason)
        capability_session_id = _read_optional_string(capability_session_id)
        capability_session_status = _read_optional_string(capability_session_status)
        authorization_mode = _read_authorization_mode(authorization_mode)
        delegated_principal_id = _read_optional_string(delegated_principal_id)
        delegated_scope = _read_optional_string(delegated_scope)
        if status not in {"success", "denied", "failed", "approval_required"}:
            raise ValueError(f"Session status is not supported: {status}")
        if status == "failed":
            failure_reason = _read_required_string(failure_reason, field="failure_reason")
        if authorization_mode == "user_delegated":
            delegated_principal_id = _read_required_string(
                delegated_principal_id,
                field="delegated_principal_id",
            )
            delegated_scope = _read_required_string(delegated_scope, field="delegated_scope")
        if any(run.trace_id == trace_id for run in self._runs):
            raise ValueError(f"Session trace_id already exists: {trace_id}")
        session = self._sessions.get(session_id)
        if session is None:
            session = SessionRecord(
                session_id=session_id,
                tenant_id=tenant_id,
                principal_id=principal_id,
            )
            self._sessions[session_id] = session
        elif session.tenant_id != tenant_id:
            raise ValueError(f"Session tenant_id does not match existing session: {session_id}")
        elif session.principal_id != principal_id:
            raise ValueError(f"Session principal_id does not match existing session: {session_id}")
        session.traces.append(trace_id)
        record = RunRecord(
            trace_id=trace_id,
            session_id=session_id,
            status=status,
            user_input=user_input,
            output_text=output_text,
            failure_reason=failure_reason,
            capability_session_id=capability_session_id,
            capability_session_status=capability_session_status,
            authorization_mode=authorization_mode,
            delegated_principal_id=delegated_principal_id,
            delegated_scope=delegated_scope,
        )
        self._runs.append(record)
        return record

    def get_session(self, session_id: str) -> SessionRecord | None:
        session_id = _read_required_string(session_id, field="session_id")
        return self._sessions.get(session_id)

    def runs_for_session(self, session_id: str) -> tuple[RunRecord, ...]:
        session_id = _read_required_string(session_id, field="session_id")
        return tuple(run for run in self._runs if run.session_id == session_id)

    def export_session_json(
        self,
        session_id: str,
        *,
        output_path: str | Path,
    ) -> Path:
        session_id = _read_required_string(session_id, field="session_id")
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
        dataset_name = _read_required_string(dataset_name, field="dataset_name")
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        normalized_session_ids = tuple(
            _read_required_string(session_id, field="session_id")
            for session_id in session_ids
        )
        if len(set(normalized_session_ids)) != len(normalized_session_ids):
            raise ValueError("Session field entries must be unique: session_id")
        normalized_eval_specs: dict[str, dict[str, object]] = {}
        if eval_specs is not None:
            for session_id, eval_spec in eval_specs.items():
                normalized_session_id = _read_required_string(
                    session_id,
                    field="session_id",
                )
                if normalized_session_id in normalized_eval_specs:
                    raise ValueError("Session field entries must be unique: session_id")
                normalized_eval_specs[normalized_session_id] = eval_spec
        sessions = []
        for session_id in normalized_session_ids:
            payload = self._session_payload(session_id)
            if session_id in normalized_eval_specs:
                payload["eval"] = normalized_eval_specs[session_id]
            sessions.append(payload)
        run_count = sum(
            summarize_session(session_id, self.runs_for_session(session_id)).total_runs
            for session_id in normalized_session_ids
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

    def _session_payload(self, session_id: str) -> SessionPayload:
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
                "failed_runs": summary.failed_runs,
                "traceable_failed_runs": summary.traceable_failed_runs,
                "latest_trace_id": summary.latest_trace_id,
                "latest_status": summary.latest_status,
            },
            "runs": [
                {
                    "trace_id": run.trace_id,
                    "status": run.status,
                    "user_input": run.user_input,
                    "output_text": run.output_text,
                    "failure_reason": run.failure_reason,
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
    failed_runs: int
    traceable_failed_runs: int
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
        failed_runs=sum(1 for run in runs if run.status == "failed"),
        traceable_failed_runs=sum(
            1
            for run in runs
            if run.status == "failed"
            and bool(run.trace_id)
            and bool(run.output_text)
            and bool(run.failure_reason)
        ),
        latest_trace_id=latest.trace_id if latest is not None else None,
        latest_status=latest.status if latest is not None else None,
    )
