from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from agent_runtime_ref.config import (
    default_config_dir,
    load_capability_catalog,
    load_memory_store,
    load_policy_engine,
    load_rollout_policy,
)
from agent_runtime_ref.models import RunRequest, RunResult
from agent_runtime_ref.rollout import assess_rollout
from agent_runtime_ref.runtime import AgentRuntime
from agent_runtime_ref.telemetry import StructuredEvent, TelemetryEmitter


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
    return AgentRuntime(
        catalog=load_capability_catalog(config_dir / "capabilities.yaml"),
        memory=load_memory_store(config_dir / "memory.yaml"),
        policy=load_policy_engine(config_dir / "policy.yaml"),
    )


def _run_runtime(
    config_dir: Path,
    *,
    user_input: str,
    tenant_id: str,
    principal_id: str,
    trace_id: str,
) -> tuple[AgentRuntime, RunResult]:
    runtime = _build_runtime(config_dir)
    result = runtime.run(
        RunRequest(
            user_input=user_input,
            tenant_id=tenant_id,
            principal_id=principal_id,
            trace_id=trace_id,
        ),
    )
    return runtime, result


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
    )
    return {
        "result": result.output_text,
        "status": result.status,
        "trace_id": args.trace_id,
        "events": len(runtime.telemetry.events),
        "memory_records": len(runtime.memory.all()),
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
                "content": record.content,
            }
            for record in records
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
    )
    return {
        "status": result.status,
        "result": result.output_text,
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
    )
    output_path = runtime.telemetry.export_jsonl(args.output)
    return {
        "status": result.status,
        "result": result.output_text,
        "trace_id": args.trace_id,
        "event_count": len(runtime.telemetry.events),
        "output_path": str(output_path),
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
    export_events.add_argument(
        "--output",
        default="artifacts/trace-demo-001.jsonl",
        help="Path for JSONL trace export",
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
    else:
        parser.error(f"Unsupported command: {command}")
        return 2
    print(json.dumps(payload, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
