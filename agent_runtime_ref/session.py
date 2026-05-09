from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from os import PathLike
from pathlib import Path
from typing import TypedDict, cast


class RunPayload(TypedDict):
    trace_id: str
    status: str
    user_input: str
    output_text: str
    failure_reason: str
    request_agent_id: str
    capability_session_id: str
    capability_session_status: str
    authorization_mode: str
    delegated_principal_id: str
    delegated_scope: str
    idempotency_key: str
    approval_id: str
    capability_name: str


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
    trace_ids: list[str]
    failed_trace_ids: list[str]
    idempotency_keys: list[str]
    approval_ids: list[str]
    approval_capability_names: list[str]
    pending_approval_ids: list[str]
    pending_approval_capability_names: list[str]
    approval_status_counts: dict[str, int]
    latest_trace_id: str | None
    latest_status: str | None


class SessionPayload(TypedDict, total=False):
    session: SessionMetadataPayload
    summary: SessionSummaryPayload
    total_runs: int
    failed_runs: int
    traceable_failed_runs: int
    trace_ids: list[str]
    failed_trace_ids: list[str]
    idempotency_keys: list[str]
    approval_ids: list[str]
    approval_capability_names: list[str]
    pending_approval_ids: list[str]
    pending_approval_capability_names: list[str]
    approval_status_counts: dict[str, int]
    latest_failure_reason: str
    latest_trace_id: str | None
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
    request_agent_id: str = ""
    capability_session_id: str = ""
    capability_session_status: str = ""
    authorization_mode: str = "platform_owned"
    delegated_principal_id: str = ""
    delegated_scope: str = ""
    idempotency_key: str = ""
    approval_id: str = ""
    capability_name: str = ""

    def __post_init__(self) -> None:
        self.trace_id = _read_required_string(self.trace_id, field="trace_id")
        self.session_id = _read_required_string(self.session_id, field="session_id")
        self.status = _read_required_string(self.status, field="status")
        self.user_input = _read_required_string(self.user_input, field="user_input")
        self.output_text = _read_required_string(self.output_text, field="output_text")
        self.failure_reason = _read_optional_string(
            self.failure_reason,
            field="failure_reason",
        )
        self.request_agent_id = _read_optional_string(
            self.request_agent_id,
            field="request_agent_id",
        )
        self.capability_session_id = _read_optional_string(
            self.capability_session_id,
            field="capability_session_id",
        )
        self.capability_session_status = _read_optional_string(
            self.capability_session_status,
            field="capability_session_status",
        )
        self.authorization_mode = _read_authorization_mode(self.authorization_mode)
        self.delegated_principal_id = _read_optional_string(
            self.delegated_principal_id,
            field="delegated_principal_id",
        )
        self.delegated_scope = _read_optional_string(
            self.delegated_scope,
            field="delegated_scope",
        )
        self.idempotency_key = _read_optional_string(
            self.idempotency_key,
            field="idempotency_key",
        )
        self.approval_id = _read_optional_string(
            self.approval_id,
            field="approval_id",
        )
        self.capability_name = _read_optional_string(
            self.capability_name,
            field="capability_name",
        )
        status = self.status
        if status not in {"success", "denied", "failed", "approval_required"}:
            raise ValueError(f"Session status is not supported: {status}")
        if self.status == "failed":
            self.failure_reason = _read_required_string(
                self.failure_reason,
                field="failure_reason",
            )
        if self.authorization_mode == "user_delegated":
            self.delegated_principal_id = _read_required_string(
                self.delegated_principal_id,
                field="delegated_principal_id",
            )
            self.delegated_scope = _read_required_string(
                self.delegated_scope,
                field="delegated_scope",
            )


@dataclass(slots=True)
class SessionRecord:
    session_id: str
    tenant_id: str
    principal_id: str
    traces: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.session_id = _read_required_string(self.session_id, field="session_id")
        self.tenant_id = _read_optional_string(self.tenant_id, field="tenant_id")
        self.principal_id = _read_optional_string(self.principal_id, field="principal_id")
        self.traces = _read_string_entries(self.traces, field="trace_id")


def _read_optional_string(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Session field must be a string: {field}")
    return value.strip()


def _read_required_string(value: object, *, field: str) -> str:
    normalized = _read_optional_string(value, field=field)
    if not normalized:
        raise ValueError(f"Session field is required: {field}")
    return normalized


def _read_string_entries(value: object, *, field: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise TypeError(f"Session field entries must be a sequence: {field}")
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        entry = _read_required_string(item, field=field)
        if entry in seen:
            raise ValueError(f"Session field entries must be unique: {field}")
        seen.add(entry)
        normalized.append(entry)
    return normalized


def _read_authorization_mode(value: object) -> str:
    authorization_mode = _read_required_string(value, field="authorization_mode")
    if authorization_mode not in {"platform_owned", "user_delegated", "human_approved"}:
        raise ValueError(f"Authorization mode is not supported: {authorization_mode}")
    return authorization_mode


def _read_session_output_path(path: object) -> Path:
    if not isinstance(path, (str, PathLike)):
        raise TypeError("Session output path must be a string or path-like object")
    return Path(cast(str | PathLike[str], path))


def _read_eval_spec(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError("Session eval spec must be a mapping")
    normalized: dict[str, object] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise TypeError("Session eval spec key must be a string")
        field = key.strip()
        if not field:
            raise ValueError("Session eval spec key must not be empty")
        if field in normalized:
            raise ValueError("Session eval spec keys must be unique")
        normalized[field] = item
    return normalized


def _eval_spec_has_duplicate_ticket_evidence(eval_spec: Mapping[str, object]) -> bool:
    labels = eval_spec.get("labels")
    if isinstance(labels, Sequence) and not isinstance(labels, str):
        if any(label == "duplicate_ticket_eval_passed" for label in labels):
            return True
    grading_rules = eval_spec.get("grading_rules")
    if isinstance(grading_rules, Sequence) and not isinstance(grading_rules, str):
        for rule in grading_rules:
            if (
                isinstance(rule, Mapping)
                and cast(Mapping[str, object], rule).get("type")
                == "duplicate_ticket_guard"
            ):
                return True
    return False


def _duplicate_ticket_scenarios_from_sessions(
    sessions: Sequence[SessionPayload],
) -> list[str]:
    scenarios: list[str] = []
    seen: set[str] = set()
    for session in sessions:
        eval_spec = session.get("eval")
        if not isinstance(eval_spec, Mapping):
            continue
        if not _eval_spec_has_duplicate_ticket_evidence(eval_spec):
            continue
        scenario = eval_spec.get("scenario")
        if not isinstance(scenario, str):
            continue
        normalized = scenario.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            scenarios.append(normalized)
    return scenarios


def _merge_approval_status_counts(
    status_counts: Iterable[Mapping[str, int]],
) -> dict[str, int]:
    merged: dict[str, int] = {}
    for counts in status_counts:
        for status, count in counts.items():
            merged[status] = merged.get(status, 0) + count
    return merged


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
        request_agent_id: str = "",
        capability_session_id: str = "",
        capability_session_status: str = "",
        authorization_mode: str = "platform_owned",
        delegated_principal_id: str = "",
        delegated_scope: str = "",
        idempotency_key: str = "",
        approval_id: str = "",
        capability_name: str = "",
    ) -> RunRecord:
        session_id = _read_required_string(session_id, field="session_id")
        status = _read_required_string(status, field="status")
        tenant_id = (
            _read_optional_string(tenant_id, field="tenant_id")
            if status == "denied"
            else _read_required_string(tenant_id, field="tenant_id")
        )
        principal_id = (
            _read_optional_string(principal_id, field="principal_id")
            if status == "denied"
            else _read_required_string(principal_id, field="principal_id")
        )
        trace_id = _read_required_string(trace_id, field="trace_id")
        user_input = _read_required_string(user_input, field="user_input")
        output_text = _read_required_string(output_text, field="output_text")
        failure_reason = _read_optional_string(failure_reason, field="failure_reason")
        request_agent_id = _read_optional_string(
            request_agent_id,
            field="request_agent_id",
        )
        capability_session_id = _read_optional_string(
            capability_session_id,
            field="capability_session_id",
        )
        capability_session_status = _read_optional_string(
            capability_session_status,
            field="capability_session_status",
        )
        authorization_mode = _read_authorization_mode(authorization_mode)
        delegated_principal_id = _read_optional_string(
            delegated_principal_id,
            field="delegated_principal_id",
        )
        delegated_scope = _read_optional_string(delegated_scope, field="delegated_scope")
        idempotency_key = _read_optional_string(idempotency_key, field="idempotency_key")
        approval_id = _read_optional_string(approval_id, field="approval_id")
        capability_name = _read_optional_string(capability_name, field="capability_name")
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
            request_agent_id=request_agent_id,
            capability_session_id=capability_session_id,
            capability_session_status=capability_session_status,
            authorization_mode=authorization_mode,
            delegated_principal_id=delegated_principal_id,
            delegated_scope=delegated_scope,
            idempotency_key=idempotency_key,
            approval_id=approval_id,
            capability_name=capability_name,
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
        output_path: str | PathLike[str],
    ) -> Path:
        session_id = _read_required_string(session_id, field="session_id")
        destination = _read_session_output_path(output_path)
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
        output_path: str | PathLike[str],
        dataset_name: str,
        eval_specs: dict[str, dict[str, object]] | None = None,
    ) -> Path:
        dataset_name = _read_required_string(dataset_name, field="dataset_name")
        destination = _read_session_output_path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not isinstance(session_ids, Sequence) or isinstance(session_ids, str):
            raise TypeError("Session field entries must be a sequence: session_id")
        normalized_session_ids = tuple(
            _read_required_string(session_id, field="session_id")
            for session_id in session_ids
        )
        if len(set(normalized_session_ids)) != len(normalized_session_ids):
            raise ValueError("Session field entries must be unique: session_id")
        normalized_eval_specs: dict[str, dict[str, object]] = {}
        if eval_specs is not None:
            if not isinstance(eval_specs, Mapping):
                raise TypeError("Session eval specs must be a mapping")
            for session_id, eval_spec in eval_specs.items():
                normalized_session_id = _read_required_string(
                    session_id,
                    field="session_id",
                )
                if normalized_session_id in normalized_eval_specs:
                    raise ValueError("Session field entries must be unique: session_id")
                normalized_eval_specs[normalized_session_id] = _read_eval_spec(eval_spec)
        sessions = []
        for session_id in normalized_session_ids:
            payload = self._session_payload(session_id)
            if session_id in normalized_eval_specs:
                payload["eval"] = normalized_eval_specs[session_id]
            sessions.append(payload)
        session_summaries = [
            summarize_session(session_id, self.runs_for_session(session_id))
            for session_id in normalized_session_ids
        ]
        latest_failed_run = None
        for session_id in reversed(normalized_session_ids):
            runs = self.runs_for_session(session_id)
            latest_failed_run = next(
                (run for run in reversed(runs) if run.status == "failed"),
                None,
            )
            if latest_failed_run is not None:
                break
        payload = {
            "dataset_name": dataset_name,
            "session_count": len(sessions),
            "session_ids": list(normalized_session_ids),
            "run_count": sum(summary.total_runs for summary in session_summaries),
            "failed_runs": sum(summary.failed_runs for summary in session_summaries),
            "traceable_failed_runs": sum(
                summary.traceable_failed_runs for summary in session_summaries
            ),
            "trace_ids": list(
                dict.fromkeys(
                    trace_id
                    for session in sessions
                    for trace_id in session["summary"]["trace_ids"]
                )
            ),
            "failed_trace_ids": list(
                dict.fromkeys(
                    trace_id
                    for session in sessions
                    for trace_id in session["summary"]["failed_trace_ids"]
                )
            ),
            "idempotency_keys": list(
                dict.fromkeys(
                    key
                    for session in sessions
                    for key in session["summary"]["idempotency_keys"]
                )
            ),
            "approval_ids": list(
                dict.fromkeys(
                    approval_id
                    for session in sessions
                    for approval_id in session["summary"]["approval_ids"]
                )
            ),
            "approval_capability_names": list(
                dict.fromkeys(
                    capability_name
                    for session in sessions
                    for capability_name in session["summary"]["approval_capability_names"]
                )
            ),
            "pending_approval_ids": list(
                dict.fromkeys(
                    approval_id
                    for session in sessions
                    for approval_id in session["summary"]["pending_approval_ids"]
                )
            ),
            "pending_approval_capability_names": list(
                dict.fromkeys(
                    capability_name
                    for session in sessions
                    for capability_name in session["summary"]["pending_approval_capability_names"]
                )
            ),
            "approval_status_counts": _merge_approval_status_counts(
                session["summary"]["approval_status_counts"] for session in sessions
            ),
            "latest_failure_reason": (
                latest_failed_run.failure_reason if latest_failed_run else ""
            ),
            "duplicate_ticket_scenarios": _duplicate_ticket_scenarios_from_sessions(
                sessions
            ),
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
        latest_failed_run = next((run for run in reversed(runs) if run.status == "failed"), None)
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
                "trace_ids": list(summary.trace_ids),
                "failed_trace_ids": list(summary.failed_trace_ids),
                "idempotency_keys": list(summary.idempotency_keys),
                "approval_ids": list(summary.approval_ids),
                "approval_capability_names": list(summary.approval_capability_names),
                "pending_approval_ids": list(summary.pending_approval_ids),
                "pending_approval_capability_names": list(
                    summary.pending_approval_capability_names
                ),
                "approval_status_counts": dict(summary.approval_status_counts),
                "latest_trace_id": summary.latest_trace_id,
                "latest_status": summary.latest_status,
            },
            "total_runs": summary.total_runs,
            "failed_runs": summary.failed_runs,
            "traceable_failed_runs": summary.traceable_failed_runs,
            "trace_ids": list(summary.trace_ids),
            "failed_trace_ids": list(summary.failed_trace_ids),
            "idempotency_keys": list(summary.idempotency_keys),
            "approval_ids": list(summary.approval_ids),
            "approval_capability_names": list(summary.approval_capability_names),
            "pending_approval_ids": list(summary.pending_approval_ids),
            "pending_approval_capability_names": list(summary.pending_approval_capability_names),
            "approval_status_counts": dict(summary.approval_status_counts),
            "latest_failure_reason": latest_failed_run.failure_reason if latest_failed_run else "",
            "latest_trace_id": summary.latest_trace_id,
            "runs": [
                {
                    "trace_id": run.trace_id,
                    "status": run.status,
                    "user_input": run.user_input,
                    "output_text": run.output_text,
                    "failure_reason": run.failure_reason,
                    "request_agent_id": run.request_agent_id,
                    "capability_session_id": run.capability_session_id,
                    "capability_session_status": run.capability_session_status,
                    "authorization_mode": run.authorization_mode,
                    "delegated_principal_id": run.delegated_principal_id,
                    "delegated_scope": run.delegated_scope,
                    "idempotency_key": run.idempotency_key,
                    "approval_id": run.approval_id,
                    "capability_name": run.capability_name,
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
    trace_ids: tuple[str, ...]
    failed_trace_ids: tuple[str, ...]
    idempotency_keys: tuple[str, ...]
    approval_ids: tuple[str, ...]
    approval_capability_names: tuple[str, ...]
    pending_approval_ids: tuple[str, ...]
    pending_approval_capability_names: tuple[str, ...]
    approval_status_counts: dict[str, int]
    latest_trace_id: str | None
    latest_status: str | None


def summarize_session(
    session_id: str,
    runs: tuple[RunRecord, ...],
) -> SessionEvalSummary:
    session_id = _read_required_string(session_id, field="session_id")
    if not isinstance(runs, Sequence) or isinstance(runs, str):
        raise TypeError("Session runs must be a sequence")
    normalized_runs: tuple[RunRecord, ...] = tuple(runs)
    for run in normalized_runs:
        if not isinstance(run, RunRecord):
            raise TypeError("Session runs entries must be RunRecord")
    latest = normalized_runs[-1] if normalized_runs else None
    idempotency_keys = tuple(
        dict.fromkeys(run.idempotency_key for run in normalized_runs if run.idempotency_key)
    )
    approval_ids = tuple(
        dict.fromkeys(run.approval_id for run in normalized_runs if run.approval_id)
    )
    approval_capability_names = tuple(
        dict.fromkeys(
            run.capability_name
            for run in normalized_runs
            if run.approval_id and run.capability_name
        )
    )
    pending_approval_ids = tuple(
        dict.fromkeys(
            run.approval_id
            for run in normalized_runs
            if run.approval_id and run.capability_session_status == "pending"
        )
    )
    pending_approval_capability_names = tuple(
        dict.fromkeys(
            run.capability_name
            for run in normalized_runs
            if run.approval_id
            and run.capability_name
            and run.capability_session_status == "pending"
        )
    )
    approval_status_counts: dict[str, int] = {}
    for run in normalized_runs:
        if not run.approval_id:
            continue
        approval_status = run.capability_session_status or run.status
        approval_status_counts[approval_status] = (
            approval_status_counts.get(approval_status, 0) + 1
        )
    trace_ids = tuple(dict.fromkeys(run.trace_id for run in normalized_runs if run.trace_id))
    failed_trace_ids = tuple(
        run.trace_id
        for run in normalized_runs
        if run.status == "failed"
        and bool(run.trace_id)
        and bool(run.output_text)
        and bool(run.failure_reason)
    )
    return SessionEvalSummary(
        session_id=session_id,
        total_runs=len(normalized_runs),
        success_runs=sum(1 for run in normalized_runs if run.status == "success"),
        approval_wait_runs=sum(
            1 for run in normalized_runs if "waiting for human approval" in run.output_text.lower()
        ),
        denied_runs=sum(1 for run in normalized_runs if run.status == "denied"),
        failed_runs=sum(1 for run in normalized_runs if run.status == "failed"),
        traceable_failed_runs=len(failed_trace_ids),
        trace_ids=trace_ids,
        failed_trace_ids=failed_trace_ids,
        idempotency_keys=idempotency_keys,
        approval_ids=approval_ids,
        approval_capability_names=approval_capability_names,
        pending_approval_ids=pending_approval_ids,
        pending_approval_capability_names=pending_approval_capability_names,
        approval_status_counts=approval_status_counts,
        latest_trace_id=latest.trace_id if latest is not None else None,
        latest_status=latest.status if latest is not None else None,
    )
