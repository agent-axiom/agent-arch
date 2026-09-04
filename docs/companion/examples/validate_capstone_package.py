from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_runtime_ref.evidence import verify_evidence_manifest  # noqa: E402
from agent_runtime_ref.telemetry import TelemetryEmitter  # noqa: E402

REQUIRED_FILES = frozenset(
    {
        "README.md",
        "01-agent.json",
        "01-approval-state.json",
        "01-approval.json",
        "01-baseline.md",
        "01-lifecycle.json",
        "02-normal-trace-summary.json",
        "02-normal-trace.jsonl",
        "02-unknown-effect-trace-summary.json",
        "02-unknown-effect-trace.jsonl",
        "02-trace-comparison.md",
        "03-reconciliation.yaml",
        "04-eval.json",
        "04-rollout-hold.json",
        "05-limited-wave-plan.md",
        "evidence-manifest.yaml",
        "release-decision.json",
    }
)
REQUIRED_BLOCKERS = {
    "unknown_external_effect_not_reconciled": "02-unknown-effect-trace.jsonl",
    "trusted_duplicate_ticket_attestation_missing": "04-rollout-hold.json",
}
REQUIRED_DECISION_REFS = {
    "02-unknown-effect-trace.jsonl",
    "03-reconciliation.yaml",
    "04-rollout-hold.json",
}


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return payload


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    events = [event.as_dict() for event in TelemetryEmitter.load_jsonl(path)]
    if not events:
        raise ValueError(f"{path.name} must contain at least one event")
    return events


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path.name} must contain a YAML object")
    return payload


def _contained_file(root: Path, reference: str) -> bool:
    if not reference or Path(reference).is_absolute():
        return False
    candidate = (root / reference).resolve()
    return candidate.is_relative_to(root) and candidate.is_file()


def _manifest_integrity(package_dir: Path) -> tuple[bool, str]:
    manifest_path = package_dir / "evidence-manifest.yaml"
    manifest = _load_yaml(manifest_path)
    artifacts = manifest.get("artifacts", [])
    if not isinstance(artifacts, list):
        return False, "artifacts must be a list"

    artifact_ids = [
        item.get("id")
        for item in artifacts
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    artifact_paths = [
        item.get("path")
        for item in artifacts
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    ]
    expected_paths = REQUIRED_FILES - {"evidence-manifest.yaml"}
    diagnostics: list[str] = []
    if len(artifact_ids) != len(artifacts) or len(set(artifact_ids)) != len(artifact_ids):
        diagnostics.append("artifact ids must be present and unique")
    if len(artifact_paths) != len(artifacts) or len(set(artifact_paths)) != len(artifact_paths):
        diagnostics.append("artifact paths must be present and unique")
    missing_paths = sorted(expected_paths - set(artifact_paths))
    unexpected_paths = sorted(set(artifact_paths) - expected_paths)
    if missing_paths:
        diagnostics.append("manifest missing: " + ", ".join(missing_paths))
    if unexpected_paths:
        diagnostics.append("manifest unexpected: " + ", ".join(unexpected_paths))

    verification = verify_evidence_manifest(
        manifest_path,
        root=package_dir,
        required_artifact_ids=tuple(artifact_ids),
    )
    diagnostics.extend(
        f"{item.code} at {item.location}: {item.message}" for item in verification.diagnostics
    )
    return verification.verified and not diagnostics, "; ".join(diagnostics) or "verified"


def _trace_matches_summary(
    events: list[dict[str, Any]],
    summary: dict[str, Any],
) -> bool:
    event_types = [event.get("event_type") for event in events]
    trace_ids = {event.get("trace_id") for event in events}
    return (
        bool(events)
        and events == summary.get("events")
        and event_types == summary.get("event_types")
        and len(events) == summary.get("event_count")
        and bool(summary.get("trace_id"))
        and trace_ids == {summary.get("trace_id")}
        and bool(summary.get("session_id"))
        and all(
            event["payload"].get("session_id") == summary["session_id"]
            for event in events
            if event["event_type"] != "span"
        )
        and event_types[0] == "run_start"
        and event_types[-1] == "run_complete"
        and event_types.count("run_start") == event_types.count("run_complete") == 1
        and events[-1]["payload"].get("status") == summary.get("status")
        and events[-1]["payload"].get("failure_reason", "") == summary.get("failure_reason")
    )


def _validate_raw_unknown_trace(
    events: list[dict[str, Any]],
    summary: dict[str, Any],
) -> tuple[bool, str]:
    event_types = [event.get("event_type") for event in events]
    tool_events = [
        event
        for event in events
        if event.get("event_type") == "tool_execution" and isinstance(event.get("payload"), dict)
    ]
    reconciliation_events = [
        event
        for event in events
        if event.get("event_type") == "effect_reconciliation_required"
        and isinstance(event.get("payload"), dict)
    ]
    completion_events = [
        event
        for event in events
        if event.get("event_type") == "run_complete" and isinstance(event.get("payload"), dict)
    ]
    ok = (
        _trace_matches_summary(events, summary)
        and len(tool_events) == 1
        and tool_events[0]["payload"].get("capability") == "create_ticket"
        and tool_events[0]["payload"].get("outcome") == "side_effect_unknown"
        and tool_events[0]["payload"].get("side_effect_status") == "side_effect_unknown"
        and len(reconciliation_events) == 1
        and reconciliation_events[0]["payload"].get("failure_reason") == "post_dispatch_timeout"
        and reconciliation_events[0]["payload"].get("effect_state") == "side_effect_unknown"
        and reconciliation_events[0]["payload"].get("capability") == "create_ticket"
        and bool(tool_events[0]["payload"].get("idempotency_key"))
        and reconciliation_events[0]["payload"].get("idempotency_key")
        == tool_events[0]["payload"].get("idempotency_key")
        and len(completion_events) == 1
        and completion_events[0]["payload"].get("status") == "blocked_on_reconciliation"
        and completion_events[0]["payload"].get("side_effect_status") == "side_effect_unknown"
        and completion_events[0]["payload"].get("failure_reason") == "post_dispatch_timeout"
        and event_types.index("tool_execution")
        < event_types.index("effect_reconciliation_required")
        < event_types.index("run_complete")
    )
    return ok, "raw JSONL must agree with its summary and unknown-effect contract"


def _validate_normal_trace(package_dir: Path) -> bool:
    events = _load_jsonl(package_dir / "02-normal-trace.jsonl")
    summary = _load_json(package_dir / "02-normal-trace-summary.json")
    event_types = [event["event_type"] for event in events]
    tools = [event["payload"] for event in events if event["event_type"] == "tool_execution"]
    return (
        _trace_matches_summary(events, summary)
        and summary.get("status") == "waiting_for_approval"
        and summary.get("failure_reason") == ""
        and event_types.count("approval_requested") == 1
        and "effect_reconciliation_required" not in event_types
        and len(tools) == 1
        and tools[0].get("capability") == "create_ticket"
        and tools[0].get("outcome") == "approval_required"
        and tools[0].get("side_effect_status") == "not_executed"
        and events[-1]["payload"].get("side_effect_status") == "not_executed"
    )


def _validate_eval(payload: dict[str, Any]) -> tuple[bool, str]:
    sessions = payload.get("sessions", [])
    if not isinstance(sessions, list) or len(sessions) != 1:
        return False, "evaluation must contain exactly one session"
    session = sessions[0]
    if not isinstance(session, dict):
        return False, "evaluation session must be an object"
    runs = session.get("runs", [])
    evaluation = session.get("eval", {})
    if not isinstance(runs, list) or len(runs) != 1 or not isinstance(runs[0], dict):
        return False, "evaluation must contain exactly one run"
    run = runs[0]
    session_record = session.get("session", {})
    session_summary = session.get("summary", {})
    if not isinstance(session_record, dict) or not isinstance(evaluation, dict):
        return False, "evaluation session and rubric must be objects"
    if not isinstance(session_summary, dict):
        return False, "evaluation summary must be an object"
    ok = (
        evaluation.get("scenario") == "unknown_effect_reconciliation"
        and payload.get("duplicate_ticket_scenarios") == ["unknown_effect_reconciliation"]
        and session_summary.get("latest_status") == "blocked_on_reconciliation"
        and run.get("status") == "blocked_on_reconciliation"
        and run.get("failure_reason") == "post_dispatch_timeout"
        and run.get("side_effect_status") == "side_effect_unknown"
        and isinstance(run.get("trace_id"), str)
        and bool(run["trace_id"].strip())
        and payload.get("trace_ids") == [run["trace_id"]]
        and isinstance(session_record.get("session_id"), str)
        and bool(session_record["session_id"].strip())
        and payload.get("session_ids") == [session_record["session_id"]]
    )
    return ok, "evaluation must exercise the post-dispatch unknown-effect path"


def validate_capstone_package(package_dir: Path) -> dict[str, object]:
    """Validate the observable contracts of the book's capstone package."""

    package_dir = package_dir.resolve()
    passed_checks: list[str] = []
    failed_checks: list[dict[str, str]] = []

    def record(check: str, passed: bool, reason: str) -> None:
        if passed:
            passed_checks.append(check)
        else:
            failed_checks.append({"check": check, "reason": reason})

    present_files = {
        path.relative_to(package_dir).as_posix()
        for path in package_dir.rglob("*")
        if path.is_file()
    }
    missing_files = sorted(REQUIRED_FILES - present_files)
    unexpected_files = sorted(present_files - REQUIRED_FILES)
    record(
        "package_inventory",
        not missing_files and not unexpected_files,
        f"missing={missing_files}; unexpected={unexpected_files}",
    )

    try:
        integrity_ok, integrity_reason = _manifest_integrity(package_dir)
        record("manifest_integrity", integrity_ok, integrity_reason)
    except (OSError, TypeError, ValueError, yaml.YAMLError) as error:
        record("manifest_integrity", False, str(error))

    decision: dict[str, Any] = {}
    try:
        decision = _load_json(package_dir / "release-decision.json")
        blockers = decision.get("blocking_findings", [])
        blockers_by_id = (
            {
                item.get("id"): item
                for item in blockers
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            }
            if isinstance(blockers, list)
            else {}
        )
        blockers_complete = (
            isinstance(blockers, list)
            and len(blockers) == len(REQUIRED_BLOCKERS)
            and set(blockers_by_id) == set(REQUIRED_BLOCKERS)
        ) and all(
            all(
                isinstance(item.get(field), str) and bool(item[field].strip())
                for field in (
                    "id",
                    "evidence_ref",
                    "owner",
                    "required_evidence",
                    "reconsider_when",
                )
            )
            and item["evidence_ref"] == REQUIRED_BLOCKERS[blocker_id]
            and _contained_file(package_dir, item["evidence_ref"])
            for blocker_id, item in blockers_by_id.items()
        )
        decision_ok = (
            decision.get("decision") == "hold"
            and decision.get("next_eligible_decision") == "limited_wave"
            and isinstance(decision.get("owner"), str)
            and bool(decision["owner"].strip())
            and blockers_complete
        )
        record(
            "release_decision",
            decision_ok,
            "expected an owned hold decision with both evidence-linked blockers",
        )
        evidence_refs = decision.get("evidence_refs", [])
        refs_ok = (
            isinstance(evidence_refs, list)
            and len(evidence_refs) == len(REQUIRED_DECISION_REFS)
            and all(
                isinstance(reference, str) and _contained_file(package_dir, reference)
                for reference in evidence_refs
            )
            and set(evidence_refs) == REQUIRED_DECISION_REFS
        )
        record(
            "release_evidence_refs",
            refs_ok,
            "every evidence reference must resolve inside the exact package",
        )
    except (OSError, TypeError, ValueError) as error:
        record("release_decision", False, str(error))
        record("release_evidence_refs", False, "release decision could not be read")

    unknown_summary: dict[str, Any] = {}
    try:
        unknown_summary = _load_json(package_dir / "02-unknown-effect-trace-summary.json")
        event_types = unknown_summary.get("event_types", [])
        unknown_ok = (
            unknown_summary.get("status") == "blocked_on_reconciliation"
            and unknown_summary.get("failure_reason") == "post_dispatch_timeout"
            and isinstance(event_types, list)
            and "effect_reconciliation_required" in event_types
        )
        record(
            "unknown_effect_path",
            unknown_ok,
            "unknown effect must stop in blocked_on_reconciliation",
        )
    except (OSError, TypeError, ValueError) as error:
        record("unknown_effect_path", False, str(error))

    try:
        raw_events = _load_jsonl(package_dir / "02-unknown-effect-trace.jsonl")
        trace_ok, trace_reason = _validate_raw_unknown_trace(
            raw_events,
            unknown_summary,
        )
        normal_ok = _validate_normal_trace(package_dir)
        record(
            "trace_continuity",
            trace_ok and normal_ok,
            f"unknown-effect={trace_ok}; normal={normal_ok}; {trace_reason}",
        )
    except (OSError, TypeError, ValueError) as error:
        record("trace_continuity", False, str(error))

    try:
        evaluation = _load_json(package_dir / "04-eval.json")
        eval_ok, eval_reason = _validate_eval(evaluation)
        record("eval_unknown_effect", eval_ok, eval_reason)
    except (OSError, TypeError, ValueError) as error:
        record("eval_unknown_effect", False, str(error))

    try:
        reconciliation = _load_yaml(package_dir / "03-reconciliation.yaml")
        reconciliation_ok = (
            reconciliation.get("automatic_retry_allowed") is False
            and reconciliation.get("required_before_retry") == "verification_result=not_found"
            and isinstance(reconciliation.get("owner"), str)
            and bool(reconciliation["owner"].strip())
            and reconciliation.get("business_key") == "support-request:onboarding-issue:user-42"
        )
        record(
            "reconciliation_contract",
            reconciliation_ok,
            "retry must remain blocked until verification_result=not_found",
        )
    except (OSError, TypeError, ValueError, yaml.YAMLError) as error:
        record("reconciliation_contract", False, str(error))

    try:
        rollout = _load_json(package_dir / "04-rollout-hold.json")
        missing_required = rollout.get("missing_required", [])
        rollout_ok = (
            rollout.get("ready") is False
            and rollout.get("production_ready") is False
            and isinstance(missing_required, list)
            and "duplicate_ticket_eval_passed" in missing_required
        )
        record(
            "rollout_fails_closed",
            rollout_ok,
            "missing duplicate-ticket evidence must keep rollout closed",
        )
    except (OSError, TypeError, ValueError) as error:
        record("rollout_fails_closed", False, str(error))

    return {
        "valid": not failed_checks,
        "decision": decision.get("decision"),
        "checked_files": len(present_files),
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a book capstone package.")
    parser.add_argument("--package-dir", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_capstone_package(args.package_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
