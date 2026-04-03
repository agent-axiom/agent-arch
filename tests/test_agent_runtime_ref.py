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
    load_memory_store,
    load_policy_engine,
    load_rollout_policy,
)
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
        self.assertIn("Ticket request accepted", result.output_text)

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

    def test_memory_store_filters_by_tenant(self) -> None:
        store = MemoryStore()
        records = store.retrieve("language preference", "tenant-acme", limit=5)
        self.assertTrue(records)
        self.assertTrue(all(record.tenant_id == "tenant-acme" for record in records))

    def test_cli_simulate_run_returns_json(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main([])
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["agent_id"], "support-triage-ref")
        self.assertEqual(payload["status"], "success")
        self.assertGreaterEqual(payload["events"], 1)
        self.assertGreaterEqual(payload["memory_records"], 3)

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

    def test_cli_inspect_agent_returns_identity_and_inventory(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(["inspect-agent"])
        payload = json.loads(buffer.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["agent_id"], "support-triage-ref")
        self.assertIn("create_ticket", payload["approved_capabilities"])
        self.assertIn("search_docs", payload["catalog_capabilities"])

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


if __name__ == "__main__":
    unittest.main()
