from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from agent_runtime_ref.__main__ import main
from agent_runtime_ref.config import (
    load_agent_profile,
    load_capability_catalog,
    load_controls_policy,
    load_memory_store,
    load_policy_engine,
    load_rollout_policy,
)
from agent_runtime_ref.controls import assess_controls, assess_inventory_drift
from agent_runtime_ref.memory import MemoryStore
from agent_runtime_ref.models import RunRequest
from agent_runtime_ref.policy import PolicyEngine
from agent_runtime_ref.rollout import RolloutReadiness, assess_rollout, ready_for_rollout
from agent_runtime_ref.runtime import AgentRuntime


class AgentRuntimeRefTests(unittest.TestCase):
    def test_config_loader_builds_runtime_components(self) -> None:
        config_dir = Path("agent_runtime_ref/configs")
        catalog = load_capability_catalog(config_dir / "capabilities.yaml")
        memory = load_memory_store(config_dir / "memory.yaml")
        agent, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
        policy = load_policy_engine(
            config_dir / "policy.yaml",
            approved_inventory=approved_inventory,
        )
        runtime = AgentRuntime(catalog=catalog, policy=policy, memory=memory, agent=agent)
        result = runtime.run(
            RunRequest(
                user_input="Please open a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-7",
                trace_id="trace-config-001",
                agent_id=agent.agent_id,
            ),
        )
        self.assertEqual(result.status, "success")
        self.assertEqual(agent.agent_id, "support-triage-ref")
        self.assertEqual(catalog.get("create_ticket") is not None, True)
        self.assertEqual(policy.allow_memory_write("session_summary").action, "allow")
        self.assertGreaterEqual(len(memory.all()), 4)

    def test_runtime_returns_success_for_plain_request(self) -> None:
        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input="Summarize the current architecture.",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-plain-001",
                agent_id="agent-runtime-ref",
            ),
        )
        self.assertEqual(result.status, "success")
        self.assertIn("Reference runtime completed", result.output_text)

    def test_runtime_uses_memory_for_preference_query(self) -> None:
        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input="What language preference do you remember?",
                tenant_id="tenant-acme",
                principal_id="user-9",
                trace_id="trace-pref-001",
                agent_id="agent-runtime-ref",
            ),
        )
        self.assertEqual(result.status, "success")
        self.assertIn("Retrieved profile hint", result.output_text)

    def test_runtime_uses_tool_path_for_ticket_request(self) -> None:
        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input="Please open a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-2",
                trace_id="trace-ticket-001",
                agent_id="agent-runtime-ref",
            ),
        )
        self.assertEqual(result.status, "success")
        self.assertIn("waiting for human approval", result.output_text)
        self.assertEqual(len(runtime.approvals.pending()), 1)

    def test_policy_denies_missing_principal(self) -> None:
        engine = PolicyEngine()
        decision = engine.precheck(
            RunRequest(
                user_input="hi",
                tenant_id="tenant-acme",
                principal_id="",
                trace_id="trace-deny-001",
                agent_id="agent-runtime-ref",
            ),
        )
        self.assertEqual(decision.action, "deny")

    def test_policy_denies_capability_outside_approved_inventory(self) -> None:
        config_dir = Path("agent_runtime_ref/configs")
        catalog = load_capability_catalog(config_dir / "capabilities.yaml")
        memory = load_memory_store(config_dir / "memory.yaml")
        agent, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
        restricted_inventory = type(approved_inventory)(frozenset({"search_docs"}))
        policy = load_policy_engine(
            config_dir / "policy.yaml",
            approved_inventory=restricted_inventory,
        )
        runtime = AgentRuntime(catalog=catalog, policy=policy, memory=memory, agent=agent)
        result = runtime.run(
            RunRequest(
                user_input="Please open a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-2",
                trace_id="trace-inventory-001",
                agent_id=agent.agent_id,
            ),
        )
        self.assertEqual(result.status, "success")
        tool_event = next(
            event
            for event in runtime.telemetry.events
            if event.event_type == "tool_policy_decision"
        )
        self.assertEqual(tool_event.payload["reason"], "capability_not_in_inventory")

    def test_policy_denies_capability_without_egress_policy(self) -> None:
        config_dir = Path("agent_runtime_ref/configs")
        catalog = load_capability_catalog(config_dir / "capabilities.yaml")
        _, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
        policy = load_policy_engine(
            config_dir / "policy.yaml",
            approved_inventory=approved_inventory,
        )
        broken_spec = catalog.get("search_docs")
        assert broken_spec is not None
        from agent_runtime_ref.catalog import CapabilitySpec
        from agent_runtime_ref.models import RunContext, ToolRequest

        decision = policy.evaluate_tool(
            RunContext(
                tenant_id="tenant-acme",
                principal_id="user-2",
                trace_id="trace-egress-001",
            ),
            ToolRequest(
                capability_name="search_docs",
                arguments={"query": "onboarding policy"},
            ),
            CapabilitySpec(
                name=broken_spec.name,
                owner=broken_spec.owner,
                mode=broken_spec.mode,
                transport=broken_spec.transport,
                timeout_seconds=broken_spec.timeout_seconds,
                tool_principal=broken_spec.tool_principal,
                risk_tier=broken_spec.risk_tier,
                network_access="restricted",
                allowed_egress=(),
                approval_required=broken_spec.approval_required,
                idempotency_key_required=broken_spec.idempotency_key_required,
            ),
        )
        self.assertEqual(decision.action, "deny")
        self.assertEqual(decision.reason, "egress_policy_missing")

    def test_rollout_gate_requires_all_flags(self) -> None:
        self.assertTrue(
            ready_for_rollout(
                RolloutReadiness(
                    trace_coverage=True,
                    offline_eval_pass=True,
                    slo_defined=True,
                    rollback_plan=True,
                ),
            ),
        )
        self.assertFalse(
            ready_for_rollout(
                RolloutReadiness(
                    trace_coverage=True,
                    offline_eval_pass=False,
                    slo_defined=True,
                    rollback_plan=True,
                ),
            ),
        )

    def test_rollout_policy_detects_blockers(self) -> None:
        policy = load_rollout_policy("agent_runtime_ref/configs/rollout.yaml")
        assessment = assess_rollout(
            policy,
            {
                "trace_coverage": True,
                "policy_prechecks": True,
                "capability_owners": True,
                "offline_eval_pass": True,
                "slo_defined": True,
                "rollback_plan": True,
                "oncall_owner": True,
                "direct_tool_access_present": True,
            },
        )
        self.assertFalse(assessment.ready)
        self.assertIn("direct_tool_access_present", assessment.blocking_signals)

    def test_controls_policy_detects_inventory_drift(self) -> None:
        policy = load_controls_policy("agent_runtime_ref/configs/controls.yaml")
        catalog = load_capability_catalog("agent_runtime_ref/configs/capabilities.yaml")
        _, approved_inventory = load_agent_profile("agent_runtime_ref/configs/agent.yaml")
        drift = assess_inventory_drift(approved_inventory, catalog)
        assessment = assess_controls(
            policy,
            {
                "registry_reviewed": True,
                "capability_owners_confirmed": True,
                "memory_provenance_enforced": True,
                "policy_traces_present": True,
                "direct_tool_access_present": False,
                "unmanaged_runtime_present": False,
            },
            inventory_drift=drift,
        )
        self.assertTrue(assessment.healthy)
        self.assertFalse(assessment.inventory_drift.has_drift)

    def test_memory_store_filters_by_tenant(self) -> None:
        store = MemoryStore()
        records = store.retrieve("language preference", "tenant-acme", limit=5)
        self.assertTrue(records)
        self.assertTrue(all(record.tenant_id == "tenant-acme" for record in records))
        self.assertTrue(all(record.provenance for record in records))

    def test_background_persisted_records_include_revision_and_provenance(self) -> None:
        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input="Please open a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-3",
                trace_id="trace-memory-001",
                agent_id="agent-runtime-ref",
            ),
        )
        self.assertEqual(result.status, "success")
        persisted_event = next(
            event
            for event in runtime.telemetry.events
            if event.event_type == "memory_persisted"
        )
        self.assertIn("provenance", persisted_event.payload)
        self.assertIn("revision", persisted_event.payload)
        self.assertEqual(persisted_event.payload["revision"], "1")

    def test_runtime_emits_context_layers(self) -> None:
        runtime = AgentRuntime()
        runtime.run(
            RunRequest(
                user_input="What language preference do you remember?",
                tenant_id="tenant-acme",
                principal_id="user-4",
                trace_id="trace-context-001",
                agent_id="agent-runtime-ref",
            ),
        )
        context_event = next(
            event
            for event in runtime.telemetry.events
            if event.event_type == "context_layers_built"
        )
        self.assertGreaterEqual(int(context_event.payload["static_items"]), 1)
        self.assertGreaterEqual(int(context_event.payload["retrieved_items"]), 1)

    def test_cli_simulate_run_returns_json(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main([])
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["agent_id"], "support-triage-ref")
        self.assertEqual(payload["session_id"], "session-demo-001")
        self.assertEqual(payload["status"], "success")
        self.assertGreaterEqual(payload["events"], 1)
        self.assertGreaterEqual(payload["memory_records"], 3)
        self.assertGreaterEqual(payload["pending_approvals"], 1)

    def test_cli_inspect_memory_filters_records(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(
                [
                    "inspect-memory",
                    "--memory-class",
                    "profile",
                ],
            )
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertGreaterEqual(payload["count"], 1)
        self.assertTrue(all(item["memory_class"] == "profile" for item in payload["records"]))
        self.assertTrue(all("provenance" in item for item in payload["records"]))
        self.assertTrue(all("revision" in item for item in payload["records"]))

    def test_cli_inspect_agent_returns_identity_and_inventory(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(["inspect-agent"])
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["agent_id"], "support-triage-ref")
        self.assertIn("create_ticket", payload["approved_capabilities"])
        self.assertTrue(
            any(item["name"] == "search_docs" for item in payload["catalog_capabilities"]),
        )
        self.assertTrue(
            any(item["risk_tier"] == "high" for item in payload["catalog_capabilities"]),
        )

    def test_cli_dump_events_returns_trace_events(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(
                [
                    "dump-events",
                    "--user-input",
                    "Please open a ticket for this issue.",
                ],
            )
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertGreaterEqual(payload["event_count"], 1)
        self.assertTrue(any(item["event_type"] == "tool_execution" for item in payload["events"]))
        self.assertTrue(any(item["event_type"] == "run_start" for item in payload["events"]))

    def test_cli_export_and_inspect_trace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "trace.jsonl"
            export_buffer = io.StringIO()
            with redirect_stdout(export_buffer):
                export_code = main(
                    [
                        "export-events",
                        "--user-input",
                        "Please open a ticket for this issue.",
                        "--trace-id",
                        "trace-export-001",
                        "--output",
                        str(output_path),
                    ],
                )
            export_payload = json.loads(export_buffer.getvalue())
            self.assertEqual(export_code, 0)
            self.assertTrue(output_path.exists())
            self.assertEqual(export_payload["trace_id"], "trace-export-001")

            inspect_buffer = io.StringIO()
            with redirect_stdout(inspect_buffer):
                inspect_code = main(
                    [
                        "inspect-trace",
                        "--input",
                        str(output_path),
                    ],
                )
            inspect_payload = json.loads(inspect_buffer.getvalue())
            self.assertEqual(inspect_code, 0)
            self.assertEqual(inspect_payload["trace_id"], "trace-export-001")
            self.assertTrue(
                any(
                    item["event_type"] == "run_complete"
                    for item in inspect_payload["events"]
                ),
            )
            self.assertTrue(
                any(
                    item["payload"].get("session_id") == "session-demo-001"
                    for item in inspect_payload["events"]
                ),
            )

    def test_cli_replay_run_uses_exported_trace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "trace.jsonl"
            with redirect_stdout(io.StringIO()):
                export_code = main(
                    [
                        "export-events",
                        "--user-input",
                        "What language preference do you remember?",
                        "--trace-id",
                        "trace-replay-source",
                        "--output",
                        str(output_path),
                    ],
                )
            self.assertEqual(export_code, 0)

            replay_buffer = io.StringIO()
            with redirect_stdout(replay_buffer):
                replay_code = main(
                    [
                        "replay-run",
                        "--input",
                        str(output_path),
                        "--replay-trace-id",
                        "trace-replay-target",
                    ],
                )
            replay_payload = json.loads(replay_buffer.getvalue())
            self.assertEqual(replay_code, 0)
            self.assertEqual(replay_payload["source_trace_id"], "trace-replay-source")
            self.assertEqual(replay_payload["replay_trace_id"], "trace-replay-target")
            self.assertEqual(replay_payload["status"], "success")

    def test_cli_check_rollout_reports_missing_signal(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(
                [
                    "check-rollout",
                    "--signal",
                    "trace_coverage=true",
                    "--signal",
                    "offline_eval_pass=false",
                ],
            )
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertFalse(payload["ready"])
        self.assertIn("offline_eval_pass", payload["missing_required"])

    def test_cli_check_controls_reports_control_failure(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(
                [
                    "check-controls",
                    "--signal",
                    "registry_reviewed=false",
                ],
            )
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertFalse(payload["healthy"])
        self.assertIn("registry_reviewed", payload["missing_controls"])
        self.assertFalse(payload["inventory_drift"]["has_drift"])

    def test_cli_inspect_approvals_returns_pending_item(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(["inspect-approvals"])
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertGreaterEqual(payload["count"], 1)
        self.assertEqual(payload["approvals"][0]["status"], "pending")

    def test_cli_resolve_approval_marks_item_resolved(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(
                [
                    "resolve-approval",
                    "--decision",
                    "approved",
                    "--note",
                    "manager approved demo request",
                ],
            )
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["status"], "approved")
        self.assertEqual(payload["resolution_note"], "manager approved demo request")

    def test_cli_inspect_session_returns_trace_linked_history(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(["inspect-session"])
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["session_id"], "session-demo-001")
        self.assertGreaterEqual(payload["trace_count"], 1)
        self.assertEqual(payload["runs"][0]["trace_id"], "trace-session-001")
        self.assertEqual(payload["summary"]["total_runs"], 1)
        self.assertEqual(payload["summary"]["approval_wait_runs"], 1)

    def test_cli_session_eval_summary_returns_compact_metrics(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(["session-eval-summary"])
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["session_id"], "session-demo-001")
        self.assertEqual(payload["total_runs"], 1)
        self.assertEqual(payload["approval_wait_runs"], 1)
        self.assertEqual(payload["latest_trace_id"], "trace-session-001")

    def test_cli_session_replay_runs_multiple_inputs(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(
                [
                    "session-replay",
                    "--user-input",
                    "Please create a ticket for this onboarding issue.",
                    "--user-input",
                    "What language preference do you remember?",
                ],
            )
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["run_count"], 2)
        self.assertEqual(payload["summary"]["total_runs"], 2)
        self.assertEqual(payload["summary"]["approval_wait_runs"], 1)
        self.assertEqual(payload["summary"]["latest_trace_id"], "trace-session-002")
        self.assertEqual(payload["runs"][1]["trace_id"], "trace-session-002")

    def test_cli_inspect_session_with_multiple_inputs_returns_both_runs(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(
                [
                    "inspect-session",
                    "--user-input",
                    "Please create a ticket for this onboarding issue.",
                    "--user-input",
                    "What language preference do you remember?",
                ],
            )
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["trace_count"], 2)
        self.assertEqual(payload["summary"]["total_runs"], 2)
        self.assertIn("waiting for human approval", payload["runs"][0]["output_text"])
        self.assertIn("Retrieved profile hint", payload["runs"][1]["output_text"])

    def test_cli_export_session_writes_structured_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "session.json"
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = main(
                    [
                        "export-session",
                        "--output",
                        str(output_path),
                    ],
                )
            payload = json.loads(buffer.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())
            self.assertEqual(payload["session_id"], "session-demo-001")
            self.assertEqual(payload["total_runs"], 2)
            exported = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(exported["summary"]["total_runs"], 2)
            self.assertEqual(len(exported["runs"]), 2)

    def test_cli_export_eval_dataset_writes_multi_session_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "eval-dataset.json"
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = main(
                    [
                        "export-eval-dataset",
                        "--output",
                        str(output_path),
                    ],
                )
            payload = json.loads(buffer.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())
            self.assertEqual(payload["dataset_name"], "agent-runtime-ref-eval-seed")
            self.assertEqual(payload["session_count"], 3)
            self.assertEqual(payload["run_count"], 4)
            exported = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(exported["dataset_name"], "agent-runtime-ref-eval-seed")
            self.assertEqual(exported["session_count"], 3)
            self.assertEqual(exported["run_count"], 4)
            self.assertEqual(len(exported["sessions"]), 3)


if __name__ == "__main__":
    unittest.main()
