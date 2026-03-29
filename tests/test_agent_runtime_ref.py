from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from agent_runtime_ref.__main__ import main
from agent_runtime_ref.config import (
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
        policy = load_policy_engine(config_dir / "policy.yaml")
        runtime = AgentRuntime(catalog=catalog, policy=policy, memory=memory)
        result = runtime.run(
            RunRequest(
                user_input="Please open a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-7",
                trace_id="trace-config-001",
            ),
        )
        self.assertEqual(result.status, "success")
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
            ),
        )
        self.assertEqual(decision.action, "deny")

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
        self.assertEqual(payload["status"], "success")
        self.assertGreaterEqual(payload["events"], 1)
        self.assertGreaterEqual(payload["memory_records"], 3)

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
