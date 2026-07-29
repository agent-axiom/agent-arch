from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, cast

import pytest

from agent_runtime_ref.config import load_capability_catalog, load_yaml_file
from agent_runtime_ref.execution import execute_tool
from agent_runtime_ref.idempotency import compute_idempotency_request_digest
from agent_runtime_ref.models import (
    ModelOutput,
    RunContext,
    RunRequest,
    RunResult,
    ToolRequest,
    ToolResult,
)
from agent_runtime_ref.policy import CapabilityPolicy, PolicyDecision, PolicyEngine
from agent_runtime_ref.runtime import AgentRuntime
from agent_runtime_ref.states import (
    CAPABILITY_OUTCOMES,
    POLICY_DECISIONS,
    RUN_STATUSES,
    SIDE_EFFECT_STATUSES,
)


def test_machine_state_vocabularies_are_explicit() -> None:
    assert POLICY_DECISIONS == frozenset({"allow", "deny", "approval_required"})
    assert RUN_STATUSES == frozenset(
        {
            "success",
            "waiting_for_approval",
            "denied",
            "failed",
            "blocked_on_reconciliation",
        }
    )
    assert CAPABILITY_OUTCOMES == frozenset(
        {
            "success",
            "approval_required",
            "permission_denied",
            "validation_failure",
            "retryable_failure",
            "side_effect_unknown",
            "partial_side_effect",
        }
    )
    assert SIDE_EFFECT_STATUSES == frozenset(
        {
            "not_executed",
            "applied",
            "side_effect_unknown",
            "partial_side_effect",
        }
    )


@pytest.mark.parametrize("ambiguous_outcome", ["denied", "failed"])
def test_tool_result_rejects_ambiguous_outcomes(ambiguous_outcome: str) -> None:
    with pytest.raises(
        ValueError,
        match=f"Capability outcome is not supported: {ambiguous_outcome}",
    ):
        ToolResult("search_docs", ambiguous_outcome, {})


def test_run_result_validates_run_and_side_effect_dimensions() -> None:
    with pytest.raises(
        ValueError,
        match="Run status is not supported: approval_required",
    ):
        RunResult("waiting", "approval_required")

    with pytest.raises(
        ValueError,
        match="Side-effect status is not supported: executed",
    ):
        RunResult("done", "success", side_effect_status="executed")


@pytest.mark.parametrize("fault", ["tool_timeout", "upstream_unavailable"])
def test_pre_dispatch_faults_are_retryable_capability_failures(
    fault: str,
    config_dir: Path,
) -> None:
    capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
    assert capability is not None

    result = execute_tool(
        capability,
        ToolRequest("search_docs", {"query": "policy"}),
        PolicyDecision("allow", "low_risk_read", "cap_101"),
        test_fault=fault,
    )

    assert result.status == "retryable_failure"
    assert result.side_effect_status == "not_executed"
    assert result.payload["reason"] == fault


def test_policy_deny_is_a_permission_denied_capability_outcome(config_dir: Path) -> None:
    capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
    assert capability is not None

    result = execute_tool(
        capability,
        ToolRequest("search_docs", {"query": "policy"}),
        PolicyDecision("deny", "configured_deny", "cap_410"),
    )

    assert result.status == "permission_denied"
    assert result.side_effect_status == "not_executed"


def test_cli_keeps_failed_run_status_and_emits_retryable_tool_outcome(cli_json) -> None:
    exit_code, payload = cli_json(
        [
            "dump-events",
            "--trace-id",
            "trace-machine-states-timeout-001",
            "--simulate-failure",
            "tool_timeout",
        ]
    )

    assert exit_code == 0
    assert payload["status"] == "failed"
    assert payload["result"] == (
        "Runtime halted before side effects completed: "
        "create_ticket returned failed (tool_timeout)."
    )
    tool_event = next(
        event for event in payload["events"] if event["event_type"] == "tool_execution"
    )
    assert tool_event["payload"]["outcome"] == "retryable_failure"
    assert tool_event["payload"]["side_effect_status"] == "not_executed"
    assert "status" not in tool_event["payload"]
    run_failed_event = next(
        event for event in payload["events"] if event["event_type"] == "run_failed"
    )
    assert run_failed_event["payload"]["tool_outcome"] == "retryable_failure"


def test_unknown_capability_keeps_failed_run_status_and_emits_permission_denied() -> None:
    class UnknownToolRuntime(AgentRuntime):
        def _call_model(
            self,
            request: RunRequest,
            context: RunContext,
            *,
            second_pass: bool = False,
        ) -> ModelOutput:
            return ModelOutput(
                text="missing capability",
                tool_request=ToolRequest("missing_capability", {}),
            )

    runtime = UnknownToolRuntime()
    result = runtime.run(
        RunRequest(
            user_input="Call the missing capability.",
            tenant_id="tenant-acme",
            principal_id="user-2",
            trace_id="trace-machine-states-deny-001",
        )
    )

    assert result.status == "failed"
    assert result.output_text == (
        "Runtime halted before side effects completed: "
        "missing_capability returned denied (capability_unknown)."
    )
    tool_event = next(
        event for event in runtime.telemetry.events if event.event_type == "tool_execution"
    )
    assert tool_event.payload["outcome"] == "permission_denied"
    assert tool_event.payload["side_effect_status"] == "not_executed"
    run_failed_event = next(
        event for event in runtime.telemetry.events if event.event_type == "run_failed"
    )
    assert run_failed_event.payload["tool_outcome"] == "permission_denied"


@pytest.mark.parametrize(
    ("outcome", "side_effect_status", "expected_effect"),
    [
        ("success", "side_effect_unknown", "side_effect_unknown"),
        ("success", "partial_side_effect", "partial_side_effect"),
        ("side_effect_unknown", "not_executed", "side_effect_unknown"),
        ("partial_side_effect", "not_executed", "partial_side_effect"),
        ("side_effect_unknown", "partial_side_effect", "partial_side_effect"),
        ("partial_side_effect", "side_effect_unknown", "side_effect_unknown"),
    ],
)
def test_runtime_reports_unresolved_effect_from_effect_then_outcome(
    outcome: str,
    side_effect_status: str,
    expected_effect: str,
) -> None:
    class ContradictoryToolRuntime(AgentRuntime):
        def _call_model(
            self,
            request: RunRequest,
            context: RunContext,
            *,
            second_pass: bool = False,
        ) -> ModelOutput:
            if second_pass:
                return ModelOutput(text="Model treated the tool result as successful.")
            return ModelOutput(
                text="Call the tool.",
                tool_request=ToolRequest("create_ticket", {}),
            )

        def _handle_tool_request(
            self,
            context: RunContext,
            request: RunRequest,
            tool_request: ToolRequest,
        ) -> PolicyDecision:
            context.tool_results.append(
                ToolResult(
                    "create_ticket",
                    outcome,
                    {"reason": "contradictory_tool_result"},
                    side_effect_status=side_effect_status,
                )
            )
            return PolicyDecision("allow", "adversarial_test", "cap_test")

    runtime = ContradictoryToolRuntime()
    result = runtime.run(
        RunRequest(
            user_input="Create a ticket.",
            tenant_id="tenant-acme",
            principal_id="user-42",
            trace_id=f"trace-contradictory-{outcome}-{side_effect_status}",
            session_id=f"session-contradictory-{outcome}-{side_effect_status}",
        )
    )

    assert result.status == "blocked_on_reconciliation"
    assert result.task_success is None
    assert result.side_effect_status == expected_effect
    run = runtime.sessions.runs_for_session(
        f"session-contradictory-{outcome}-{side_effect_status}"
    )[0]
    assert run.status == "blocked_on_reconciliation"
    assert run.side_effect_status == expected_effect
    reconciliation_event = next(
        event
        for event in runtime.telemetry.events
        if event.event_type == "effect_reconciliation_required"
    )
    assert reconciliation_event.payload["effect_state"] == expected_effect


def test_reconciliation_preserves_partial_side_effect_from_reserved_result() -> None:
    runtime = AgentRuntime(
        policy=PolicyEngine(capability_policies={"create_ticket": CapabilityPolicy("allow")})
    )
    idempotency_key = "intent-partial-reconciliation"
    arguments = {
        "title": "Agent follow-up",
        "queue": "support",
        "requester_id": "user-42",
        "idempotency_key": idempotency_key,
    }
    request_digest = compute_idempotency_request_digest(
        capability_name="create_ticket",
        arguments=arguments,
        tenant_id="tenant-acme",
        principal_id="user-42",
    )
    runtime.idempotency.reserve(idempotency_key, request_digest)
    runtime.idempotency.complete(
        idempotency_key,
        request_digest,
        ToolResult(
            "create_ticket",
            "partial_side_effect",
            {"reason": "partial_write"},
            side_effect_status="partial_side_effect",
        ),
    )

    result = runtime.run(
        RunRequest(
            user_input="Please create a ticket for this issue.",
            tenant_id="tenant-acme",
            principal_id="user-42",
            trace_id="trace-partial-reconciliation",
            session_id="session-partial-reconciliation",
            intent_id=idempotency_key,
        )
    )

    assert result.status == "blocked_on_reconciliation"
    assert result.side_effect_status == "partial_side_effect"
    tool_event = next(
        event for event in runtime.telemetry.events if event.event_type == "tool_execution"
    )
    assert tool_event.payload["outcome"] == "partial_side_effect"
    assert tool_event.payload["side_effect_status"] == "partial_side_effect"


def test_eval_export_keeps_legacy_failed_capability_session_status(
    cli_json,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "eval-dataset.json"
    exit_code, _ = cli_json(
        [
            "export-eval-dataset",
            "--output",
            str(output_path),
        ]
    )

    dataset = json.loads(output_path.read_text(encoding="utf-8"))
    failed_session = next(
        session
        for session in dataset["sessions"]
        if session["eval"]["scenario"] == "failed_run_timeout"
    )
    failed_run = failed_session["runs"][0]

    assert exit_code == 0
    assert failed_run["status"] == "failed"
    assert failed_run["capability_session_status"] == "failed"


@pytest.mark.parametrize(
    ("field", "disabled_value", "missing_control"),
    [
        ("approval", "none", "create_ticket_approval_required"),
        (
            "idempotency_key_required",
            False,
            "create_ticket_idempotency_key_required",
        ),
    ],
)
def test_check_controls_signal_cannot_mask_removed_create_ticket_safeguard(
    field: str,
    disabled_value: object,
    missing_control: str,
    cli_json,
    config_dir: Path,
    tmp_path: Path,
) -> None:
    changed_config_dir = tmp_path / field / "configs"
    shutil.copytree(config_dir, changed_config_dir)
    capabilities = load_yaml_file(changed_config_dir / "capabilities.yaml")
    create_ticket = cast(
        dict[str, Any],
        cast(dict[str, Any], capabilities["capabilities"])["create_ticket"],
    )
    create_ticket[field] = disabled_value
    (changed_config_dir / "capabilities.yaml").write_text(
        json.dumps(capabilities),
        encoding="utf-8",
    )

    exit_code, payload = cli_json(
        [
            "check-controls",
            "--config-dir",
            str(changed_config_dir),
            "--signal",
            f"{missing_control}=true",
        ]
    )

    assert exit_code == 0
    assert payload["healthy"] is False
    assert missing_control in payload["missing_controls"]


@pytest.mark.parametrize("policy_decision", ["allow", "deny"])
def test_check_controls_signal_cannot_mask_create_ticket_policy_bypass(
    policy_decision: str,
    cli_json,
    config_dir: Path,
    tmp_path: Path,
) -> None:
    changed_config_dir = tmp_path / f"policy-{policy_decision}" / "configs"
    shutil.copytree(config_dir, changed_config_dir)
    policy = load_yaml_file(changed_config_dir / "policy.yaml")
    capability_policies = cast(
        dict[str, Any],
        cast(dict[str, Any], policy["policy"])["capabilities"],
    )
    capability_policies["create_ticket"] = {"decision": policy_decision}
    (changed_config_dir / "policy.yaml").write_text(
        json.dumps(policy),
        encoding="utf-8",
    )

    exit_code, payload = cli_json(
        [
            "check-controls",
            "--config-dir",
            str(changed_config_dir),
            "--signal",
            "create_ticket_approval_required=true",
        ]
    )

    assert exit_code == 0
    assert payload["healthy"] is False
    assert "create_ticket_approval_required" in payload["missing_controls"]
