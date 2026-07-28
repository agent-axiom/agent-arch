from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
import yaml

from agent_runtime_ref.approvals import ApprovalQueue
from agent_runtime_ref.lifecycle import classify_change_surfaces
from agent_runtime_ref.memory import MemoryRecord, MemoryStore
from agent_runtime_ref.models import (
    RunContext,
    RunRequest,
    ToolRequest,
    compute_action_digest,
)
from agent_runtime_ref.policy import CapabilityPolicy


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _complete_rollout_manifest(config_dir: Path, root: Path) -> Path:
    artifact = root / "reports" / "evaluation.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text('{"passed": true}\n', encoding="utf-8")
    rollout = yaml.safe_load((config_dir / "rollout.yaml").read_text(encoding="utf-8"))[
        "rollout"
    ]
    artifact_id = "evaluation-report"
    signals: dict[str, dict[str, Any]] = {
        signal: {"value": True, "artifact_refs": [artifact_id]}
        for signal in rollout["require"]
    }
    signals.update(
        {
            signal: {"value": False, "artifact_refs": [artifact_id]}
            for signal in rollout["block_if"]
        }
    )
    manifest = root / "evidence-manifest.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "issuer": "release-pipeline",
                "subject": "support-agent@1.4.0",
                "measured_at": "2026-07-18T09:30:00Z",
                "artifacts": [
                    {
                        "id": artifact_id,
                        "path": "reports/evaluation.json",
                        "sha256": _sha256(artifact),
                    }
                ],
                "signals": signals,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return manifest


def test_post_dispatch_timeout_blocks_on_reconciliation(runtime_from_config) -> None:
    runtime_from_config.policy.capability_policies["create_ticket"] = CapabilityPolicy(
        "allow"
    )

    result = runtime_from_config.run(
        RunRequest(
            user_input="Please create a ticket for this issue.",
            tenant_id="tenant-acme",
            principal_id="user-42",
            trace_id="trace-unknown-effect-001",
            session_id="session-unknown-effect-001",
            intent_id="intent-ticket-001",
            test_fault="post_dispatch_timeout",
        )
    )

    assert result.status == "blocked_on_reconciliation"
    assert result.task_success is None
    assert result.side_effect_status == "side_effect_unknown"
    run = runtime_from_config.sessions.runs_for_session(
        "session-unknown-effect-001"
    )[0]
    assert run.status == "blocked_on_reconciliation"
    assert run.side_effect_status == "side_effect_unknown"
    assert run.idempotency_key == "intent-ticket-001"
    assert "effect_reconciliation_required" in {
        event.event_type for event in runtime_from_config.telemetry.events
    }


def test_unknown_effect_is_not_dispatched_twice(runtime_from_config) -> None:
    runtime_from_config.policy.capability_policies["create_ticket"] = CapabilityPolicy(
        "allow"
    )
    common = {
        "user_input": "Please create a ticket for this issue.",
        "tenant_id": "tenant-acme",
        "principal_id": "user-42",
        "session_id": "session-reconcile-once",
        "intent_id": "intent-ticket-once",
    }

    first = runtime_from_config.run(
        RunRequest(
            **common,
            trace_id="trace-reconcile-once-001",
            test_fault="post_dispatch_timeout",
        )
    )
    second = runtime_from_config.run(
        RunRequest(
            **common,
            trace_id="trace-reconcile-once-002",
        )
    )

    tool_spans = [
        event
        for event in runtime_from_config.telemetry.events
        if event.event_type == "span"
        and event.payload.get("span_name") == "tool:create_ticket"
    ]
    idempotency_actions = [
        event.payload["action"]
        for event in runtime_from_config.telemetry.events
        if event.event_type == "idempotency_decision"
    ]
    assert first.status == "blocked_on_reconciliation"
    assert second.status == "blocked_on_reconciliation"
    assert len(tool_spans) == 1
    assert idempotency_actions == ["execute", "reconcile"]


def test_eval_dataset_has_a_real_unknown_effect_reconciliation_scenario(
    cli_json,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "unknown-effect-eval.json"

    exit_code, payload = cli_json(
        [
            "export-eval-dataset",
            "--scenario",
            "unknown_effect_reconciliation",
            "--output",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert payload["duplicate_ticket_scenarios"] == [
        "unknown_effect_reconciliation"
    ]
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    session = exported["sessions"][0]
    run = session["runs"][0]
    assert run["status"] == "blocked_on_reconciliation"
    assert run["side_effect_status"] == "side_effect_unknown"
    assert run["failure_reason"] == "post_dispatch_timeout"
    assert session["eval"]["expected_outcomes"] == {
        "latest_status": "blocked_on_reconciliation",
        "reconciliation_runs": 1,
        "duplicate_ticket_eval_passed": True,
        "idempotency_key_required": True,
        "max_ticket_side_effects": 1,
    }


def test_pre_dispatch_timeout_is_not_claimed_as_duplicate_side_effect_proof(
    cli_json,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "pre-dispatch-eval.json"

    _, payload = cli_json(
        [
            "export-eval-dataset",
            "--scenario",
            "failed_run_timeout",
            "--output",
            str(output_path),
        ]
    )

    assert payload["duplicate_ticket_scenarios"] == []
    session = json.loads(output_path.read_text(encoding="utf-8"))["sessions"][0]
    assert "duplicate_ticket_eval_passed" not in session["eval"]["labels"]
    assert "max_ticket_side_effects" not in session["eval"]["expected_outcomes"]


@pytest.mark.parametrize(
    "artifact_name",
    [
        "trace-demo.jsonl",
        "trace-failed-tool-timeout.jsonl",
        "trace-post-dispatch-timeout.jsonl",
    ],
)
def test_companion_trace_artifacts_redact_raw_input(artifact_name: str) -> None:
    path = Path("docs/companion/artifacts") / artifact_name
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    run_start = next(event for event in events if event["event_type"] == "run_start")

    assert "user_input" not in run_start["payload"]
    assert run_start["payload"]["input_description"] == "[REDACTED]"
    assert len(run_start["payload"]["input_sha256"]) == 64
    assert all(
        event["payload"].get("status") != "success"
        for event in events
        if event["event_type"] == "span"
        and event["payload"].get("span_name", "").startswith("tool:")
        and artifact_name != "trace-demo.jsonl"
    )


def test_export_events_supports_post_dispatch_reconciliation(
    cli_json,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "post-dispatch.jsonl"

    _, payload = cli_json(
        [
            "export-events",
            "--simulate-failure",
            "post_dispatch_timeout",
            "--output",
            str(output_path),
        ]
    )

    assert payload["status"] == "blocked_on_reconciliation"
    assert payload["failure_reason"] == "post_dispatch_timeout"
    events = [json.loads(line) for line in output_path.read_text().splitlines()]
    assert "effect_reconciliation_required" in {
        event["event_type"] for event in events
    }


@pytest.mark.parametrize(
    ("surfaces", "risk_level", "review_required"),
    [
        (("documentation_only",), "low_risk", False),
        (("prompt_bundle",), "medium_risk", False),
        (("capability_contract",), "high_risk", False),
        (("prompt_bundle", "new_surface"), "review_required", True),
        ((), "review_required", True),
    ],
)
def test_change_surface_classifier_fails_closed(
    surfaces: tuple[str, ...],
    risk_level: str,
    review_required: bool,
) -> None:
    result = classify_change_surfaces(surfaces)

    assert result.risk_level == risk_level
    assert result.review_required is review_required
    assert result.unknown_surfaces == (
        ("new_surface",) if "new_surface" in surfaces else ()
    )


def test_intent_id_keeps_idempotency_key_stable_across_traces(
    runtime_from_config,
) -> None:
    runtime_from_config.policy.capability_policies["create_ticket"] = CapabilityPolicy(
        "allow"
    )
    for suffix in ("001", "002"):
        runtime_from_config.run(
            RunRequest(
                user_input="Please create a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-42",
                trace_id=f"trace-stable-intent-{suffix}",
                session_id="session-stable-intent",
                intent_id="intent-ticket-stable",
                test_fault="tool_timeout",
            )
        )

    assert [
        run.idempotency_key
        for run in runtime_from_config.sessions.runs_for_session(
            "session-stable-intent"
        )
    ] == ["intent-ticket-stable", "intent-ticket-stable"]


def test_structurally_valid_manifest_is_not_production_attestation(
    cli_json,
    config_dir: Path,
    tmp_path: Path,
) -> None:
    manifest = _complete_rollout_manifest(config_dir, tmp_path)

    exit_code, result = cli_json(
        ["check-rollout", "--evidence-manifest", str(manifest)]
    )

    assert exit_code == 0
    assert result["ready"] is True
    assert result["manifest_integrity_verified"] is True
    assert result["trusted_attestation_verified"] is False
    assert result["production_ready"] is False
    assert result["recommended_action"] == "attach_trusted_attestation"


def test_retirement_is_unknown_until_every_step_has_evidence(
    cli_json,
    config_dir: Path,
) -> None:
    required_steps = yaml.safe_load(
        (config_dir / "retirement.yaml").read_text(encoding="utf-8")
    )["retirement"]["required_steps"]

    exit_code, result = cli_json(["check-retirement"])

    assert exit_code == 0
    assert result["ready"] is False
    assert result["evidence_mode"] == "unknown"
    assert result["missing_steps"] == required_steps


@pytest.mark.parametrize(
    ("field", "changed_value"),
    [
        ("capability_name", "close_ticket"),
        ("arguments", {"queue": "security"}),
        ("tenant_id", "tenant-other"),
        ("agent_id", "support-triage-v2"),
        ("session_id", "session-002"),
        ("idempotency_key", "intent-002"),
        ("principal_id", "user-99"),
        ("authorization_mode", "platform_owned"),
        ("delegated_principal_id", "user-99"),
        ("delegated_scope", "tickets:admin"),
        ("policy_version", "policy-v4"),
        ("capability_version", "create-ticket-v3"),
        ("expires_at", "2026-07-18T10:05:00Z"),
        ("nonce", "nonce-002"),
    ],
)
def test_action_digest_binds_every_approved_field(
    field: str,
    changed_value: object,
) -> None:
    common = {
        "capability_name": "create_ticket",
        "arguments": {"queue": "support"},
        "tenant_id": "tenant-acme",
        "agent_id": "support-triage-ref",
        "session_id": "session-001",
        "idempotency_key": "intent-001",
        "principal_id": "user-42",
        "authorization_mode": "user_delegated",
        "delegated_principal_id": "user-42",
        "delegated_scope": "tickets:create",
        "policy_version": "policy-v3",
        "capability_version": "create-ticket-v2",
        "expires_at": "2026-07-18T10:00:00Z",
        "nonce": "nonce-001",
    }

    digest = compute_action_digest(**common)
    changed = compute_action_digest(**{**common, field: changed_value})

    assert digest != changed


def test_approval_cli_rejects_a_stale_expected_action_digest(
    cli_json,
    tmp_path: Path,
) -> None:
    from agent_runtime_ref.__main__ import main

    store_path = tmp_path / "approval-state.json"
    _, created = cli_json(
        ["inspect-approvals", "--approval-store", str(store_path)]
    )
    approval_id = created["approvals"][0]["approval_id"]

    with pytest.raises(ValueError, match="Approval action digest does not match"):
        main(
            [
                "resolve-approval",
                "--approval-store",
                str(store_path),
                "--approval-id",
                approval_id,
                "--expected-action-digest",
                "0" * 64,
            ]
        )


def test_approval_rejects_self_approval_and_expired_decision() -> None:
    queue = ApprovalQueue()
    request = queue.submit(
        trace_id="trace-approval-001",
        capability_name="create_ticket",
        arguments={"idempotency_key": "intent-001"},
        requested_by="user-42",
        tenant_id="tenant-acme",
        agent_id="support-triage-ref",
        reviewer="manager-1",
        reason="write_action",
        session_id="session-approval-001",
        idempotency_key="intent-001",
    )

    with pytest.raises(ValueError, match="cannot approve their own request"):
        queue.resolve(
            request.approval_id,
            decision="approved",
            resolved_by="user-42",
        )

    request.expires_at = "2020-01-01T00:00:00Z"
    with pytest.raises(ValueError, match="Approval request expired"):
        queue.resolve(
            request.approval_id,
            decision="approved",
            resolved_by="manager-1",
        )


def test_tool_policy_binds_ticket_requester_to_run_principal(
    runtime_from_config,
) -> None:
    context = RunContext(
        tenant_id="tenant-acme",
        principal_id="user-42",
        trace_id="trace-policy-001",
        session_id="session-policy-001",
    )
    request = ToolRequest(
        capability_name="create_ticket",
        arguments={
            "title": "Unexpected requester",
            "queue": "support",
            "requester_id": "user-99",
            "idempotency_key": "intent-policy-001",
        },
    )

    decision = runtime_from_config.policy.evaluate_tool(
        context,
        request,
        runtime_from_config.catalog.get("create_ticket"),
    )

    assert decision.action == "deny"
    assert decision.reason == "requester_principal_mismatch"


def test_memory_retrieval_excludes_untrusted_and_expired_records() -> None:
    store = MemoryStore(
        records=[
            MemoryRecord(
                memory_id="mem-trusted",
                tenant_id="tenant-acme",
                memory_class="long_term",
                kind="validated_fact",
                content="Support queue is trusted.",
                source="trusted_service",
                confidence=0.7,
                provenance="service_rule",
                trust_state="trusted",
                expires_at="2030-01-01T00:00:00Z",
            ),
            MemoryRecord(
                memory_id="mem-untrusted",
                tenant_id="tenant-acme",
                memory_class="long_term",
                kind="validated_fact",
                content="Support queue is untrusted.",
                source="external_document",
                confidence=1.0,
                provenance="unverified_import",
                trust_state="untrusted",
                expires_at="2030-01-01T00:00:00Z",
            ),
            MemoryRecord(
                memory_id="mem-expired",
                tenant_id="tenant-acme",
                memory_class="long_term",
                kind="validated_fact",
                content="Support queue is expired.",
                source="trusted_service",
                confidence=1.0,
                provenance="old_rule",
                trust_state="trusted",
                expires_at="2020-01-01T00:00:00Z",
            ),
        ]
    )

    records = store.retrieve("support queue", "tenant-acme", limit=10)

    assert [record.memory_id for record in records] == ["mem-trusted"]


def test_rollout_manifest_requires_every_accumulated_lab_artifact(
    cli_json,
    config_dir: Path,
    tmp_path: Path,
) -> None:
    manifest = _complete_rollout_manifest(config_dir, tmp_path)
    command = ["check-rollout", "--evidence-manifest", str(manifest)]
    for lab_number in range(1, 8):
        command.extend(["--required-artifact-id", f"lab-{lab_number:02d}"])

    exit_code, result = cli_json(command)

    assert exit_code == 0
    assert result["manifest_integrity_verified"] is False
    assert result["production_ready"] is False
    assert {
        diagnostic["location"] for diagnostic in result["evidence_diagnostics"]
    } == {f"artifacts.lab-{lab_number:02d}" for lab_number in range(1, 8)}


def test_cli_exposes_post_dispatch_unknown_effect_and_stable_intent(cli_json) -> None:
    exit_code, result = cli_json(
        [
            "simulate-run",
            "--trace-id",
            "trace-lab-04-unknown",
            "--session-id",
            "session-lab-04",
            "--intent-id",
            "intent-lab-04-ticket",
            "--simulate-failure",
            "post_dispatch_timeout",
        ]
    )

    assert exit_code == 0
    assert result["status"] == "blocked_on_reconciliation"
    assert result["task_success"] is None
    assert result["side_effect_status"] == "side_effect_unknown"
    assert result["intent_id"] == "intent-lab-04-ticket"
    assert result["idempotency_keys"] == ["intent-lab-04-ticket"]
    assert "effect_reconciliation_required" in result["event_types"]


def test_cli_simulate_run_can_write_a_structured_lab_artifact(
    cli_json,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "lab-04" / "unknown-effect.json"

    exit_code, result = cli_json(
        [
            "simulate-run",
            "--intent-id",
            "intent-lab-04-ticket",
            "--simulate-failure",
            "post_dispatch_timeout",
            "--output",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert result["output_path"] == str(output_path)
    stored = json.loads(output_path.read_text(encoding="utf-8"))
    assert stored["status"] == "blocked_on_reconciliation"
    assert stored["side_effect_status"] == "side_effect_unknown"
    assert stored["intent_id"] == "intent-lab-04-ticket"


def test_approval_queue_persists_pending_and_resolved_state(tmp_path: Path) -> None:
    store_path = tmp_path / "approvals.json"
    first_process = ApprovalQueue(storage_path=store_path)
    submitted = first_process.submit(
        trace_id="trace-durable-approval-001",
        capability_name="create_ticket",
        arguments={"idempotency_key": "intent-durable-001"},
        requested_by="user-42",
        tenant_id="tenant-acme",
        agent_id="support-triage-ref",
        reviewer="manager-1",
        reason="write_action",
        session_id="session-durable-approval-001",
        idempotency_key="intent-durable-001",
    )

    second_process = ApprovalQueue(storage_path=store_path)
    assert [item.approval_id for item in second_process.pending()] == [
        submitted.approval_id
    ]
    second_process.resolve(
        submitted.approval_id,
        decision="approved",
        resolved_by="manager-1",
        expected_action_digest=submitted.action_digest,
    )

    third_process = ApprovalQueue(storage_path=store_path)
    restored = third_process.all()[0]
    assert restored.status == "approved"
    assert restored.resolved_by == "manager-1"
    assert third_process.pending() == ()


def test_approval_cli_resumes_one_persisted_request_across_processes(
    cli_json,
    tmp_path: Path,
) -> None:
    store_path = tmp_path / "approval-state.json"

    _, created = cli_json(
        ["inspect-approvals", "--approval-store", str(store_path)]
    )
    approval = created["approvals"][0]
    assert approval["status"] == "pending"
    assert approval["action_digest"]
    assert approval["expires_at"]
    assert approval["nonce"]

    _, resolved = cli_json(
        [
            "resolve-approval",
            "--approval-store",
            str(store_path),
            "--approval-id",
            approval["approval_id"],
            "--resolved-by",
            "manager-1",
        ]
    )

    assert resolved["approval_id"] == approval["approval_id"]
    assert resolved["status"] == "approved"
    assert resolved["resolved_by"] == "manager-1"
    assert resolved["action_digest"] == approval["action_digest"]

    _, inspected = cli_json(
        ["inspect-approvals", "--approval-store", str(store_path)]
    )
    assert inspected["count"] == 1
    assert inspected["pending_approval_ids"] == []
    assert inspected["approvals"][0]["status"] == "approved"
