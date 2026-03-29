from __future__ import annotations

import json

from agent_runtime_ref.models import RunRequest
from agent_runtime_ref.rollout import RolloutReadiness, ready_for_rollout
from agent_runtime_ref.runtime import AgentRuntime


def main() -> None:
    runtime = AgentRuntime()
    result = runtime.run(
        RunRequest(
            user_input="Please create a ticket for this onboarding issue.",
            tenant_id="tenant-acme",
            principal_id="user-42",
            trace_id="trace-demo-001",
        ),
    )
    readiness = ready_for_rollout(
        RolloutReadiness(
            trace_coverage=True,
            offline_eval_pass=True,
            slo_defined=True,
            rollback_plan=True,
        ),
    )
    print(json.dumps({"result": result.output_text, "rollout_ready": readiness}, ensure_ascii=True))


if __name__ == "__main__":
    main()
