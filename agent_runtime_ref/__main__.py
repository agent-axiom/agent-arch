from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from agent_runtime_ref.approvals import ApprovalQueue
from agent_runtime_ref.config import (
    default_config_dir,
    load_agent_profile,
    load_approval_policy,
    load_artifact_bundle,
    load_capability_catalog,
    load_change_record,
    load_controls_policy,
    load_memory_store,
    load_policy_engine,
    load_retirement_plan,
    load_rollout_policy,
)
from agent_runtime_ref.controls import assess_controls, assess_inventory_drift
from agent_runtime_ref.lifecycle import assess_change_gate, assess_retirement
from agent_runtime_ref.models import RunRequest, RunResult
from agent_runtime_ref.rollout import assess_rollout
from agent_runtime_ref.runtime import AgentRuntime
from agent_runtime_ref.session import summarize_session
from agent_runtime_ref.telemetry import StructuredEvent, TelemetryEmitter

DEFAULT_SESSION_INPUTS = ("Please create a ticket for this onboarding issue.",)
DEFAULT_MULTI_RUN_INPUTS = (
    "Please create a ticket for this onboarding issue.",
    "What language preference do you remember?",
)
EVAL_DATASET_SCENARIOS: dict[str, tuple[str, tuple[str, ...], str, str | None]] = {
    "support_ticket": (
        "session-eval-support",
        ("Please create a ticket for this onboarding issue.",),
        "trace-eval-support",
        None,
    ),
    "profile_memory": (
        "session-eval-memory",
        ("What language preference do you remember?",),
        "trace-eval-memory",
        None,
    ),
    "mixed_session": (
        "session-eval-mixed",
        DEFAULT_MULTI_RUN_INPUTS,
        "trace-eval-mixed",
        None,
    ),
    "failed_run_timeout": (
        "session-eval-failed-run",
        ("Please create a ticket for this onboarding issue.",),
        "trace-eval-failed-run",
        "tool_timeout",
    ),
}
EVAL_DATASET_LABELS: dict[str, dict[str, object]] = {
    "support_ticket": {
        "scenario": "support_ticket",
        "labels": ["write_path", "approval_required", "ticketing"],
        "expected_outcomes": {
            "latest_status": "success",
            "approval_wait_runs": 1,
            "required_output_substrings": ["waiting for human approval"],
        },
    },
    "profile_memory": {
        "scenario": "profile_memory",
        "labels": ["memory_read", "profile_lookup", "grounded_answer"],
        "expected_outcomes": {
            "latest_status": "success",
            "approval_wait_runs": 0,
            "required_output_substrings": ["Retrieved profile hint"],
        },
    },
    "mixed_session": {
        "scenario": "mixed_session",
        "labels": ["multi_run", "approval_then_memory", "session_evals"],
        "expected_outcomes": {
            "latest_status": "success",
            "approval_wait_runs": 1,
            "required_run_count": 2,
            "required_output_substrings": [
                "waiting for human approval",
                "Retrieved profile hint",
            ],
        },
    },
    "failed_run_timeout": {
        "scenario": "failed_run_timeout",
        "labels": ["failed_run", "tool_timeout", "failure_drill"],
        "expected_outcomes": {
            "latest_status": "failed",
            "failed_runs": 1,
            "required_output_substrings": ["tool_timeout"],
            "failed_run_traceable": True,
        },
    },
}


def _parse_signal(raw_signal: str) -> tuple[str, bool]:
    if "=" not in raw_signal:
        raise ValueError(f"Signal must use key=value format: {raw_signal!r}")
    key, raw_value = raw_signal.split("=", 1)
    normalized = raw_value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return key.strip(), True
    if normalized in {"0", "false", "no", "off"}:
        return key.strip(), False
    raise ValueError(f"Unsupported boolean value in signal: {raw_signal!r}")


def _build_runtime(config_dir: Path) -> AgentRuntime:
    agent, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
    return AgentRuntime(
        agent=agent,
        approvals=ApprovalQueue(load_approval_policy(config_dir / "approvals.yaml")),
        catalog=load_capability_catalog(config_dir / "capabilities.yaml"),
        memory=load_memory_store(config_dir / "memory.yaml"),
        policy=load_policy_engine(
            config_dir / "policy.yaml",
            approved_inventory=approved_inventory,
        ),
    )


def _run_runtime(
    config_dir: Path,
    *,
    user_input: str,
    tenant_id: str,
    principal_id: str,
    trace_id: str,
    session_id: str,
    agent_id: str | None = None,
    simulate_failure: str | None = None,
) -> tuple[AgentRuntime, RunResult]:
    runtime = _build_runtime(config_dir)
    return _run_on_runtime(
        runtime,
        user_input=user_input,
        tenant_id=tenant_id,
        principal_id=principal_id,
        trace_id=trace_id,
        session_id=session_id,
        agent_id=agent_id,
        simulate_failure=simulate_failure,
    )


def _run_on_runtime(
    runtime: AgentRuntime,
    *,
    user_input: str,
    tenant_id: str,
    principal_id: str,
    trace_id: str,
    session_id: str,
    agent_id: str | None = None,
    simulate_failure: str | None = None,
) -> tuple[AgentRuntime, RunResult]:
    if simulate_failure and "ticket" in user_input.lower():
        user_input = f"{user_input} [simulate_failure={simulate_failure}]"
    result = runtime.run(
        RunRequest(
            user_input=user_input,
            tenant_id=tenant_id,
            principal_id=principal_id,
            trace_id=trace_id,
            session_id=session_id,
            agent_id=agent_id or runtime.agent.agent_id,
        ),
    )
    return runtime, result


def _run_session_sequence(
    config_dir: Path,
    *,
    user_inputs: Sequence[str],
    tenant_id: str,
    principal_id: str,
    session_id: str,
    agent_id: str | None = None,
    trace_prefix: str = "trace-session",
) -> tuple[AgentRuntime, list[RunResult]]:
    runtime = _build_runtime(config_dir)
    results: list[RunResult] = []
    for index, user_input in enumerate(user_inputs, start=1):
        _, result = _run_on_runtime(
            runtime,
            user_input=user_input,
            tenant_id=tenant_id,
            principal_id=principal_id,
            trace_id=f"{trace_prefix}-{index:03d}",
            session_id=session_id,
            agent_id=agent_id,
        )
        results.append(result)
    return runtime, results


def _resolve_trace_id(events: list[StructuredEvent], requested_trace_id: str | None) -> str:
    trace_ids = sorted({event.trace_id for event in events})
    if requested_trace_id is not None:
        if requested_trace_id not in trace_ids:
            raise ValueError(f"Trace ID not found in event file: {requested_trace_id}")
        return requested_trace_id
    if len(trace_ids) != 1:
        raise ValueError("Trace file contains multiple trace IDs; pass --trace-id explicitly")
    return trace_ids[0]


def _simulate_run(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime, result = _run_runtime(
        config_dir,
        user_input=args.user_input,
        tenant_id=args.tenant_id,
        principal_id=args.principal_id,
        trace_id=args.trace_id,
        session_id=args.session_id,
        agent_id=args.agent_id,
        simulate_failure=args.simulate_failure,
    )
    session_payload = runtime.sessions._session_payload(args.session_id)
    latest_run = session_payload["runs"][-1] if session_payload["runs"] else {}
    return {
        "agent_id": runtime.agent.agent_id,
        "session_id": args.session_id,
        "result": result.output_text,
        "status": result.status,
        "failure_reason": latest_run.get("failure_reason", ""),
        "trace_id": args.trace_id,
        "events": len(runtime.telemetry.events),
        "memory_records": len(runtime.memory.all()),
        "pending_approvals": len(runtime.approvals.pending()),
        "config_dir": str(config_dir),
    }


def _inspect_memory(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    store = load_memory_store(config_dir / "memory.yaml")
    records = list(store.all())
    if args.tenant_id:
        records = [record for record in records if record.tenant_id == args.tenant_id]
    if args.memory_class:
        records = [record for record in records if record.memory_class == args.memory_class]
    if args.limit is not None:
        records = records[: args.limit]
    return {
        "count": len(records),
        "config_dir": str(config_dir),
        "records": [
            {
                "memory_id": record.memory_id,
                "tenant_id": record.tenant_id,
                "memory_class": record.memory_class,
                "kind": record.kind,
                "source": record.source,
                "confidence": record.confidence,
                "provenance": record.provenance,
                "revision": record.revision,
                "content": record.content,
            }
            for record in records
        ],
    }


def _inspect_agent(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    agent, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
    catalog = load_capability_catalog(config_dir / "capabilities.yaml")
    return {
        "agent_id": agent.agent_id,
        "display_name": agent.display_name,
        "owner_team": agent.owner_team,
        "runtime_principal": agent.runtime_principal,
        "approved_capabilities": sorted(approved_inventory.capabilities),
        "catalog_capabilities": [
            {
                "name": spec.name,
                "risk_tier": spec.risk_tier,
                "network_access": spec.network_access,
                "allowed_egress": list(spec.allowed_egress),
            }
            for spec in sorted(catalog.all(), key=lambda item: item.name)
        ],
    }


def _dump_events(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime, result = _run_runtime(
        config_dir,
        user_input=args.user_input,
        tenant_id=args.tenant_id,
        principal_id=args.principal_id,
        trace_id=args.trace_id,
        session_id=args.session_id,
        agent_id=args.agent_id,
        simulate_failure=args.simulate_failure,
    )
    session_payload = runtime.sessions._session_payload(args.session_id)
    latest_run = session_payload["runs"][-1] if session_payload["runs"] else {}
    return {
        "status": result.status,
        "result": result.output_text,
        "failure_reason": latest_run.get("failure_reason", ""),
        "trace_id": args.trace_id,
        "event_count": len(runtime.telemetry.events),
        "events": runtime.telemetry.as_dicts(),
    }


def _export_events(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime, result = _run_runtime(
        config_dir,
        user_input=args.user_input,
        tenant_id=args.tenant_id,
        principal_id=args.principal_id,
        trace_id=args.trace_id,
        session_id=args.session_id,
        agent_id=args.agent_id,
        simulate_failure=args.simulate_failure,
    )
    session_payload = runtime.sessions._session_payload(args.session_id)
    latest_run = session_payload["runs"][-1] if session_payload["runs"] else {}
    output_path = runtime.telemetry.export_jsonl(
        args.output,
        redact_fields=tuple(args.redact_field),
    )
    return {
        "status": result.status,
        "result": result.output_text,
        "failure_reason": latest_run.get("failure_reason", ""),
        "trace_id": args.trace_id,
        "event_count": len(runtime.telemetry.events),
        "output_path": str(output_path),
        "redact_fields": list(args.redact_field),
    }


def _inspect_trace(args: argparse.Namespace) -> dict[str, object]:
    events = TelemetryEmitter.load_jsonl(args.input)
    trace_id = _resolve_trace_id(events, args.trace_id)
    filtered = [event for event in events if event.trace_id == trace_id]
    return {
        "trace_id": trace_id,
        "event_count": len(filtered),
        "events": [event.as_dict() for event in filtered],
    }


def _replay_run(args: argparse.Namespace) -> dict[str, object]:
    events = TelemetryEmitter.load_jsonl(args.input)
    source_trace_id = _resolve_trace_id(events, args.trace_id)
    source_events = [event for event in events if event.trace_id == source_trace_id]
    run_start = next((event for event in source_events if event.event_type == "run_start"), None)
    if run_start is None:
        raise ValueError("Trace file does not contain a run_start event")

    config_dir = Path(args.config_dir)
    replay_trace_id = args.replay_trace_id or f"{source_trace_id}-replay"
    runtime, result = _run_runtime(
        config_dir,
        user_input=run_start.payload["user_input"],
        tenant_id=run_start.payload["tenant_id"],
        principal_id=run_start.payload["principal_id"],
        trace_id=replay_trace_id,
        session_id=run_start.payload.get("session_id", "session-replay-001"),
        agent_id=run_start.payload.get("agent_id"),
    )
    return {
        "source_trace_id": source_trace_id,
        "replay_trace_id": replay_trace_id,
        "status": result.status,
        "result": result.output_text,
        "event_count": len(runtime.telemetry.events),
    }


def _check_rollout(args: argparse.Namespace) -> dict[str, object]:
    policy = load_rollout_policy(args.config)
    observed = {name: True for name in policy.required_checks}
    observed.update({name: False for name in policy.blocked_checks})
    for raw_signal in args.signal:
        key, value = _parse_signal(raw_signal)
        observed[key] = value
    assessment = assess_rollout(policy, observed)
    return {
        "ready": assessment.ready,
        "missing_required": list(assessment.missing_required),
        "blocking_signals": list(assessment.blocking_signals),
        "rollout_mode": policy.rollout_mode,
    }


def _check_controls(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    policy = load_controls_policy(config_dir / "controls.yaml")
    _, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
    catalog = load_capability_catalog(config_dir / "capabilities.yaml")
    observed = {
        "registry_reviewed": True,
        "capability_owners_confirmed": True,
        "memory_provenance_enforced": True,
        "policy_traces_present": True,
        "direct_tool_access_present": False,
        "unmanaged_runtime_present": False,
    }
    for raw_signal in args.signal:
        key, value = _parse_signal(raw_signal)
        observed[key] = value
    inventory_drift = assess_inventory_drift(approved_inventory, catalog)
    assessment = assess_controls(
        policy,
        observed,
        inventory_drift=inventory_drift,
    )
    return {
        "healthy": assessment.healthy,
        "missing_controls": list(assessment.missing_controls),
        "blocking_findings": list(assessment.blocking_findings),
        "inventory_drift": {
            "has_drift": assessment.inventory_drift.has_drift,
            "missing_from_catalog": list(assessment.inventory_drift.missing_from_catalog),
            "missing_from_inventory": list(assessment.inventory_drift.missing_from_inventory),
        },
    }


def _inspect_lifecycle(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    change = load_change_record(config_dir / "change.yaml")
    bundle = load_artifact_bundle(config_dir / "artifacts.yaml")
    retirement = load_retirement_plan(config_dir / "retirement.yaml")
    return {
        "change": {
            "change_id": change.change_id,
            "change_type": change.change_type,
            "risk_level": change.risk_level,
            "rollout_strategy": change.rollout_strategy,
            "artifacts": list(change.artifacts),
            "required_signals": list(change.required_signals),
            "approval_roles": list(change.approval_roles),
            "failed_run_signals": [
                signal for signal in change.required_signals if "failed_run" in signal
            ],
        },
        "artifact_bundle": {
            "bundle_name": bundle.bundle_name,
            "version": bundle.version,
            "provenance_required": bundle.provenance_required,
            "signed": bundle.signed,
            "artifacts": list(bundle.artifacts),
        },
        "retirement": {
            "system_id": retirement.system_id,
            "replacement_mode": retirement.replacement_mode,
            "triggers": list(retirement.triggers),
            "required_steps": list(retirement.required_steps),
            "archive_targets": list(retirement.archive_targets),
        },
    }


def _check_change(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    change = load_change_record(config_dir / "change.yaml")
    observed = {signal: True for signal in change.required_signals}
    for raw_signal in args.signal:
        key, value = _parse_signal(raw_signal)
        observed[key] = value
    assessment = assess_change_gate(change, observed)
    return {
        "change_id": change.change_id,
        "ready": assessment.ready,
        "missing_signals": list(assessment.missing_signals),
        "missing_failed_run_signals": [
            signal for signal in assessment.missing_signals if "failed_run" in signal
        ],
        "rollout_strategy": change.rollout_strategy,
        "risk_level": change.risk_level,
    }


def _check_retirement(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    plan = load_retirement_plan(config_dir / "retirement.yaml")
    observed = {step: True for step in plan.required_steps}
    for raw_step in args.step:
        key, value = _parse_signal(raw_step)
        observed[key] = value
    assessment = assess_retirement(plan, observed)
    return {
        "system_id": plan.system_id,
        "ready": assessment.ready,
        "missing_steps": list(assessment.missing_steps),
        "replacement_mode": plan.replacement_mode,
    }


def _inspect_approvals(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime, _ = _run_runtime(
        config_dir,
        user_input=args.user_input,
        tenant_id=args.tenant_id,
        principal_id=args.principal_id,
        trace_id=args.trace_id,
        session_id=args.session_id,
        agent_id=args.agent_id,
    )
    approvals = runtime.approvals.all()
    return {
        "trace_id": args.trace_id,
        "session_id": args.session_id,
        "count": len(approvals),
        "approvals": [
            {
                "approval_id": item.approval_id,
                "capability_name": item.capability_name,
                "requested_by": item.requested_by,
                "reviewer": item.reviewer,
                "reason": item.reason,
                "authorization_mode": item.authorization_mode,
                "delegated_principal_id": item.delegated_principal_id,
                "delegated_scope": item.delegated_scope,
                "status": item.status,
            }
            for item in approvals
        ],
    }


def _resolve_demo_approval(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime, _ = _run_runtime(
        config_dir,
        user_input=args.user_input,
        tenant_id=args.tenant_id,
        principal_id=args.principal_id,
        trace_id=args.trace_id,
        session_id=args.session_id,
        agent_id=args.agent_id,
    )
    pending = runtime.approvals.pending()
    if not pending:
        raise ValueError("No pending approval requests were generated for this run")
    target = pending[0] if args.approval_id is None else next(
        item for item in pending if item.approval_id == args.approval_id
    )
    resolved = runtime.approvals.resolve(
        target.approval_id,
        decision=args.decision,
        note=args.note,
    )
    return {
        "approval_id": resolved.approval_id,
        "status": resolved.status,
        "reviewer": resolved.reviewer,
        "resolution_note": resolved.resolution_note,
        "authorization_mode": resolved.authorization_mode,
        "delegated_principal_id": resolved.delegated_principal_id,
        "delegated_scope": resolved.delegated_scope,
    }


def _inspect_session(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime = _build_runtime(config_dir)
    results = []
    for index, user_input in enumerate(args.user_input, start=1):
        _, result = _run_on_runtime(
            runtime,
            user_input=user_input,
            tenant_id=args.tenant_id,
            principal_id=args.principal_id,
            trace_id=f"{args.trace_prefix}-{index:03d}",
            session_id=args.session_id,
            agent_id=args.agent_id,
            simulate_failure=args.simulate_failure,
        )
        results.append(result)
    session = runtime.sessions.get_session(args.session_id)
    runs = runtime.sessions.runs_for_session(args.session_id)
    if session is None:
        raise ValueError(f"Session not found: {args.session_id}")
    summary = summarize_session(args.session_id, runs)
    latest_failed_run = next((run for run in reversed(runs) if run.status == "failed"), None)
    return {
        "session_id": session.session_id,
        "tenant_id": session.tenant_id,
        "principal_id": session.principal_id,
        "trace_count": len(session.traces),
        "latest_status": results[-1].status if results else None,
        "summary": {
            "total_runs": summary.total_runs,
            "success_runs": summary.success_runs,
            "approval_wait_runs": summary.approval_wait_runs,
            "denied_runs": summary.denied_runs,
            "failed_runs": summary.failed_runs,
            "traceable_failed_runs": summary.traceable_failed_runs,
            "latest_failure_reason": latest_failed_run.failure_reason if latest_failed_run else "",
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
            }
            for run in runs
        ],
    }


def _session_eval_summary(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime = _build_runtime(config_dir)
    for index, user_input in enumerate(args.user_input, start=1):
        _run_on_runtime(
            runtime,
            user_input=user_input,
            tenant_id=args.tenant_id,
            principal_id=args.principal_id,
            trace_id=f"{args.trace_prefix}-{index:03d}",
            session_id=args.session_id,
            agent_id=args.agent_id,
            simulate_failure=args.simulate_failure,
        )
    runs = runtime.sessions.runs_for_session(args.session_id)
    summary = summarize_session(args.session_id, runs)
    latest_failed_run = next((run for run in reversed(runs) if run.status == "failed"), None)
    return {
        "session_id": summary.session_id,
        "total_runs": summary.total_runs,
        "success_runs": summary.success_runs,
        "approval_wait_runs": summary.approval_wait_runs,
        "denied_runs": summary.denied_runs,
        "failed_runs": summary.failed_runs,
        "traceable_failed_runs": summary.traceable_failed_runs,
        "latest_failure_reason": latest_failed_run.failure_reason if latest_failed_run else "",
        "latest_trace_id": summary.latest_trace_id,
        "latest_status": summary.latest_status,
    }


def _session_replay(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime = _build_runtime(config_dir)
    results = []
    for index, user_input in enumerate(args.user_input, start=1):
        results.append(
            _run_on_runtime(
                runtime,
                user_input=user_input,
                tenant_id=args.tenant_id,
                principal_id=args.principal_id,
                trace_id=f"{args.trace_prefix}-{index:03d}",
                session_id=args.session_id,
                agent_id=args.agent_id,
                simulate_failure=args.simulate_failure,
            )
        )
    runs = runtime.sessions.runs_for_session(args.session_id)
    summary = summarize_session(args.session_id, runs)
    latest_failed_run = next((run for run in reversed(runs) if run.status == "failed"), None)
    return {
        "session_id": args.session_id,
        "run_count": len(results),
        "summary": {
            "total_runs": summary.total_runs,
            "success_runs": summary.success_runs,
            "approval_wait_runs": summary.approval_wait_runs,
            "denied_runs": summary.denied_runs,
            "failed_runs": summary.failed_runs,
            "traceable_failed_runs": summary.traceable_failed_runs,
            "latest_failure_reason": latest_failed_run.failure_reason if latest_failed_run else "",
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
            }
            for run in runs
        ],
    }


def _export_session(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime = _build_runtime(config_dir)
    for index, user_input in enumerate(args.user_input, start=1):
        _run_on_runtime(
            runtime,
            user_input=user_input,
            tenant_id=args.tenant_id,
            principal_id=args.principal_id,
            trace_id=f"{args.trace_prefix}-{index:03d}",
            session_id=args.session_id,
            agent_id=args.agent_id,
            simulate_failure=args.simulate_failure,
        )
    output_path = runtime.sessions.export_session_json(
        args.session_id,
        output_path=args.output,
    )
    runs = runtime.sessions.runs_for_session(args.session_id)
    summary = summarize_session(args.session_id, runs)
    latest_failed_run = next((run for run in reversed(runs) if run.status == "failed"), None)
    return {
        "session_id": args.session_id,
        "output_path": str(output_path),
        "total_runs": summary.total_runs,
        "failed_runs": summary.failed_runs,
        "traceable_failed_runs": summary.traceable_failed_runs,
        "latest_failure_reason": latest_failed_run.failure_reason if latest_failed_run else "",
        "latest_trace_id": summary.latest_trace_id,
    }


def _export_eval_dataset(args: argparse.Namespace) -> dict[str, object]:
    config_dir = Path(args.config_dir)
    runtime = _build_runtime(config_dir)
    selected_scenarios = args.scenario or list(EVAL_DATASET_SCENARIOS)
    session_ids: list[str] = []
    eval_specs: dict[str, dict[str, object]] = {}
    session_summaries = []
    for scenario_name in selected_scenarios:
        session_suffix, user_inputs, trace_prefix, simulate_failure = EVAL_DATASET_SCENARIOS[
            scenario_name
        ]
        session_id = f"{args.session_prefix}-{session_suffix.removeprefix('session-eval-')}"
        for index, user_input in enumerate(user_inputs, start=1):
            _run_on_runtime(
                runtime,
                user_input=user_input,
                tenant_id=args.tenant_id,
                principal_id=args.principal_id,
                trace_id=f"{trace_prefix}-{index:03d}",
                session_id=session_id,
                agent_id=args.agent_id,
                simulate_failure=simulate_failure,
            )
        session_ids.append(session_id)
        eval_specs[session_id] = EVAL_DATASET_LABELS[scenario_name]
        session_summaries.append(
            summarize_session(session_id, runtime.sessions.runs_for_session(session_id))
        )
    output_path = runtime.sessions.export_eval_dataset_json(
        tuple(session_ids),
        output_path=args.output,
        dataset_name=args.dataset_name,
        eval_specs=eval_specs,
    )
    latest_failed_run = None
    for session_id in reversed(session_ids):
        runs = runtime.sessions.runs_for_session(session_id)
        latest_failed_run = next((run for run in reversed(runs) if run.status == "failed"), None)
        if latest_failed_run is not None:
            break
    return {
        "dataset_name": args.dataset_name,
        "output_path": str(output_path),
        "session_count": len(session_ids),
        "run_count": sum(summary.total_runs for summary in session_summaries),
        "failed_runs": sum(summary.failed_runs for summary in session_summaries),
        "traceable_failed_runs": sum(
            summary.traceable_failed_runs for summary in session_summaries
        ),
        "latest_failure_reason": latest_failed_run.failure_reason if latest_failed_run else "",
        "sessions": session_ids,
    }


def build_parser() -> argparse.ArgumentParser:
    config_dir = default_config_dir()
    parser = argparse.ArgumentParser(description="Reference runtime demo CLI")
    subparsers = parser.add_subparsers(dest="command")

    simulate = subparsers.add_parser("simulate-run", help="Run the reference runtime demo")
    simulate.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with capabilities.yaml, memory.yaml, and policy.yaml",
    )
    simulate.add_argument(
        "--user-input",
        default="Please create a ticket for this onboarding issue.",
    )
    simulate.add_argument("--tenant-id", default="tenant-acme")
    simulate.add_argument("--principal-id", default="user-42")
    simulate.add_argument("--trace-id", default="trace-demo-001")
    simulate.add_argument("--session-id", default="session-demo-001")
    simulate.add_argument("--agent-id", default=None)
    simulate.add_argument(
        "--simulate-failure",
        choices=["tool_timeout", "upstream_unavailable"],
        default=None,
    )

    inspect_memory = subparsers.add_parser(
        "inspect-memory",
        help="Inspect seeded memory records",
    )
    inspect_memory.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with memory.yaml",
    )
    inspect_memory.add_argument("--tenant-id", default="tenant-acme")
    inspect_memory.add_argument("--memory-class", default=None)
    inspect_memory.add_argument("--limit", type=int, default=None)

    inspect_agent = subparsers.add_parser(
        "inspect-agent",
        help="Inspect agent identity and approved capability inventory",
    )
    inspect_agent.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with agent.yaml and capabilities.yaml",
    )

    dump_events = subparsers.add_parser(
        "dump-events",
        help="Run the demo and print structured events",
    )
    dump_events.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with capabilities.yaml, memory.yaml, and policy.yaml",
    )
    dump_events.add_argument(
        "--user-input",
        default="Please create a ticket for this onboarding issue.",
    )
    dump_events.add_argument("--tenant-id", default="tenant-acme")
    dump_events.add_argument("--principal-id", default="user-42")
    dump_events.add_argument("--trace-id", default="trace-demo-001")
    dump_events.add_argument("--session-id", default="session-demo-001")
    dump_events.add_argument("--agent-id", default=None)
    dump_events.add_argument(
        "--simulate-failure",
        choices=["tool_timeout", "upstream_unavailable"],
        default=None,
    )

    export_events = subparsers.add_parser(
        "export-events",
        help="Run the demo and export trace events as JSONL",
    )
    export_events.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with capabilities.yaml, memory.yaml, and policy.yaml",
    )
    export_events.add_argument(
        "--user-input",
        default="Please create a ticket for this onboarding issue.",
    )
    export_events.add_argument("--tenant-id", default="tenant-acme")
    export_events.add_argument("--principal-id", default="user-42")
    export_events.add_argument("--trace-id", default="trace-demo-001")
    export_events.add_argument("--session-id", default="session-demo-001")
    export_events.add_argument("--agent-id", default=None)
    export_events.add_argument(
        "--simulate-failure",
        choices=["tool_timeout", "upstream_unavailable"],
        default=None,
    )
    export_events.add_argument(
        "--output",
        default="artifacts/trace-demo-001.jsonl",
        help="Path for JSONL trace export",
    )
    export_events.add_argument(
        "--redact-field",
        action="append",
        default=[],
        help="Repeatable payload field to redact at export time, e.g. user_input",
    )

    inspect_trace = subparsers.add_parser(
        "inspect-trace",
        help="Read a JSONL event file and inspect a trace",
    )
    inspect_trace.add_argument(
        "--input",
        required=True,
        help="Path to a JSONL event export",
    )
    inspect_trace.add_argument(
        "--trace-id",
        default=None,
        help="Trace ID to inspect when the file contains multiple traces",
    )

    replay_run = subparsers.add_parser(
        "replay-run",
        help="Replay a run from an exported JSONL trace",
    )
    replay_run.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with capabilities.yaml, memory.yaml, and policy.yaml",
    )
    replay_run.add_argument(
        "--input",
        required=True,
        help="Path to a JSONL event export",
    )
    replay_run.add_argument(
        "--trace-id",
        default=None,
        help="Source trace ID when the file contains multiple traces",
    )
    replay_run.add_argument(
        "--replay-trace-id",
        default=None,
        help="Optional override for the replay trace ID",
    )

    rollout = subparsers.add_parser("check-rollout", help="Evaluate rollout readiness")
    rollout.add_argument(
        "--config",
        default=str(config_dir / "rollout.yaml"),
        help="Path to rollout policy YAML",
    )
    rollout.add_argument(
        "--signal",
        action="append",
        default=[],
        help="Override an observed signal, e.g. trace_coverage=true",
    )

    controls = subparsers.add_parser(
        "check-controls",
        help="Evaluate continuous controls and inventory drift",
    )
    controls.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with controls.yaml, agent.yaml, and capabilities.yaml",
    )
    controls.add_argument(
        "--signal",
        action="append",
        default=[],
        help="Override a control signal, e.g. registry_reviewed=false",
    )

    inspect_lifecycle = subparsers.add_parser(
        "inspect-lifecycle",
        help="Inspect lifecycle-oriented artifacts for change, bundles, and retirement",
    )
    inspect_lifecycle.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with change.yaml, artifacts.yaml, and retirement.yaml",
    )

    check_change = subparsers.add_parser(
        "check-change",
        help="Evaluate whether a lifecycle change record is ready for rollout",
    )
    check_change.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with change.yaml",
    )
    check_change.add_argument(
        "--signal",
        action="append",
        default=[],
        help="Override a change signal, e.g. offline_eval_passed=false",
    )

    check_retirement = subparsers.add_parser(
        "check-retirement",
        help="Evaluate whether a retirement plan has completed required steps",
    )
    check_retirement.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with retirement.yaml",
    )
    check_retirement.add_argument(
        "--step",
        action="append",
        default=[],
        help="Override a retirement step, e.g. revoke_egress=false",
    )

    inspect_approvals = subparsers.add_parser(
        "inspect-approvals",
        help="Run the demo and inspect generated approval requests",
    )
    inspect_approvals.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with agent, policy, approvals, and capability configs",
    )
    inspect_approvals.add_argument(
        "--user-input",
        default="Please create a ticket for this onboarding issue.",
    )
    inspect_approvals.add_argument("--tenant-id", default="tenant-acme")
    inspect_approvals.add_argument("--principal-id", default="user-42")
    inspect_approvals.add_argument("--trace-id", default="trace-approval-001")
    inspect_approvals.add_argument("--session-id", default="session-approval-001")
    inspect_approvals.add_argument("--agent-id", default=None)

    resolve_approval = subparsers.add_parser(
        "resolve-approval",
        help="Run the demo, create an approval request, and resolve it",
    )
    resolve_approval.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with agent, policy, approvals, and capability configs",
    )
    resolve_approval.add_argument(
        "--user-input",
        default="Please create a ticket for this onboarding issue.",
    )
    resolve_approval.add_argument("--tenant-id", default="tenant-acme")
    resolve_approval.add_argument("--principal-id", default="user-42")
    resolve_approval.add_argument("--trace-id", default="trace-approval-001")
    resolve_approval.add_argument("--session-id", default="session-approval-001")
    resolve_approval.add_argument("--agent-id", default=None)
    resolve_approval.add_argument("--approval-id", default=None)
    resolve_approval.add_argument(
        "--decision",
        choices=("approved", "rejected"),
        default="approved",
    )
    resolve_approval.add_argument("--note", default="")

    inspect_session = subparsers.add_parser(
        "inspect-session",
        help="Run the demo and inspect the trace-linked session record",
    )
    inspect_session.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with runtime configs",
    )
    inspect_session.add_argument(
        "--user-input",
        action="append",
        default=[],
        help="Repeatable input for multi-run session replay; defaults are used when omitted",
    )
    inspect_session.add_argument("--tenant-id", default="tenant-acme")
    inspect_session.add_argument("--principal-id", default="user-42")
    inspect_session.add_argument("--session-id", default="session-demo-001")
    inspect_session.add_argument("--trace-prefix", default="trace-session")
    inspect_session.add_argument("--agent-id", default=None)
    inspect_session.add_argument(
        "--simulate-failure",
        choices=("tool_timeout", "upstream_unavailable"),
        default=None,
        help="Inject a failure scenario into each inspected run",
    )

    session_eval = subparsers.add_parser(
        "session-eval-summary",
        help="Run the demo and compute a compact session evaluation summary",
    )
    session_eval.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with runtime configs",
    )
    session_eval.add_argument(
        "--user-input",
        action="append",
        default=[],
        help="Repeatable input for multi-run session replay; defaults are used when omitted",
    )
    session_eval.add_argument("--tenant-id", default="tenant-acme")
    session_eval.add_argument("--principal-id", default="user-42")
    session_eval.add_argument("--session-id", default="session-demo-001")
    session_eval.add_argument("--trace-prefix", default="trace-session")
    session_eval.add_argument("--agent-id", default=None)
    session_eval.add_argument(
        "--simulate-failure",
        choices=("tool_timeout", "upstream_unavailable"),
        default=None,
        help="Inject a failure scenario into each summarized run",
    )

    session_replay = subparsers.add_parser(
        "session-replay",
        help="Replay multiple inputs into a single session and inspect the full run series",
    )
    session_replay.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with runtime configs",
    )
    session_replay.add_argument(
        "--user-input",
        action="append",
        default=[],
        help="Repeatable input for the session replay; defaults are used when omitted",
    )
    session_replay.add_argument("--tenant-id", default="tenant-acme")
    session_replay.add_argument("--principal-id", default="user-42")
    session_replay.add_argument("--session-id", default="session-demo-001")
    session_replay.add_argument("--trace-prefix", default="trace-session")
    session_replay.add_argument("--agent-id", default=None)
    session_replay.add_argument(
        "--simulate-failure",
        choices=("tool_timeout", "upstream_unavailable"),
        default=None,
        help="Inject a failure scenario into each replayed run",
    )

    export_session = subparsers.add_parser(
        "export-session",
        help="Replay a session and export it as structured JSON for eval workflows",
    )
    export_session.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with runtime configs",
    )
    export_session.add_argument(
        "--user-input",
        action="append",
        default=[],
        help="Repeatable input for the session export; defaults are used when omitted",
    )
    export_session.add_argument("--tenant-id", default="tenant-acme")
    export_session.add_argument("--principal-id", default="user-42")
    export_session.add_argument("--session-id", default="session-demo-001")
    export_session.add_argument("--trace-prefix", default="trace-session")
    export_session.add_argument("--agent-id", default=None)
    export_session.add_argument(
        "--simulate-failure",
        choices=("tool_timeout", "upstream_unavailable"),
        default=None,
        help="Inject a failure scenario into each exported run",
    )
    export_session.add_argument(
        "--output",
        default="artifacts/session-demo-001.json",
        help="Path for structured session export",
    )

    export_eval_dataset = subparsers.add_parser(
        "export-eval-dataset",
        help="Export a small multi-session dataset for offline eval workflows",
    )
    export_eval_dataset.add_argument(
        "--config-dir",
        default=str(config_dir),
        help="Directory with runtime configs",
    )
    export_eval_dataset.add_argument(
        "--scenario",
        action="append",
        choices=tuple(EVAL_DATASET_SCENARIOS),
        default=[],
        help="Repeatable built-in scenario to include; all scenarios are used when omitted",
    )
    export_eval_dataset.add_argument("--tenant-id", default="tenant-acme")
    export_eval_dataset.add_argument("--principal-id", default="user-42")
    export_eval_dataset.add_argument("--session-prefix", default="session-eval")
    export_eval_dataset.add_argument("--agent-id", default=None)
    export_eval_dataset.add_argument(
        "--dataset-name",
        default="agent-runtime-ref-eval-seed",
        help="Human-readable dataset name stored in the export payload",
    )
    export_eval_dataset.add_argument(
        "--output",
        default="artifacts/eval-dataset.json",
        help="Path for structured eval dataset export",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    if argv is None:
        raw_args = None if len(sys.argv) > 1 else ["simulate-run"]
    else:
        raw_args = list(argv)
    if raw_args == []:
        raw_args = ["simulate-run"]
    args = parser.parse_args(raw_args)
    command = args.command or "simulate-run"
    if command == "simulate-run":
        payload = _simulate_run(args)
    elif command == "inspect-memory":
        payload = _inspect_memory(args)
    elif command == "inspect-agent":
        payload = _inspect_agent(args)
    elif command == "dump-events":
        payload = _dump_events(args)
    elif command == "export-events":
        payload = _export_events(args)
    elif command == "inspect-trace":
        payload = _inspect_trace(args)
    elif command == "replay-run":
        payload = _replay_run(args)
    elif command == "check-rollout":
        payload = _check_rollout(args)
    elif command == "check-controls":
        payload = _check_controls(args)
    elif command == "inspect-lifecycle":
        payload = _inspect_lifecycle(args)
    elif command == "check-change":
        payload = _check_change(args)
    elif command == "check-retirement":
        payload = _check_retirement(args)
    elif command == "inspect-approvals":
        payload = _inspect_approvals(args)
    elif command == "resolve-approval":
        payload = _resolve_demo_approval(args)
    elif command == "inspect-session":
        if not args.user_input:
            args.user_input = ["Please create a ticket for this onboarding issue."]
        payload = _inspect_session(args)
    elif command == "session-eval-summary":
        if not args.user_input:
            args.user_input = ["Please create a ticket for this onboarding issue."]
        payload = _session_eval_summary(args)
    elif command == "session-replay":
        if not args.user_input:
            args.user_input = [
                "Please create a ticket for this onboarding issue.",
                "What language preference do you remember?",
            ]
        payload = _session_replay(args)
    elif command == "export-session":
        if not args.user_input:
            args.user_input = list(DEFAULT_MULTI_RUN_INPUTS)
        payload = _export_session(args)
    elif command == "export-eval-dataset":
        payload = _export_eval_dataset(args)
    else:
        parser.error(f"Unsupported command: {command}")
        return 2
    print(json.dumps(payload, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
