from __future__ import annotations

import unittest

from agent_runtime_ref.models import RunRequest
from agent_runtime_ref.policy import PolicyEngine
from agent_runtime_ref.rollout import RolloutReadiness, ready_for_rollout
from agent_runtime_ref.runtime import AgentRuntime


class AgentRuntimeRefTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
