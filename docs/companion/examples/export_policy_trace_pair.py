"""Export two local search_docs traces through the reference runtime.

The teaching subclass overrides only model request selection and the final text
after a tool result. Catalog, inventory, memory, policy, execution, telemetry and
run-state transitions use the normal reference implementation. The same request
is evaluated against the source configs and a copy with one policy leaf changed.

There is no LLM call, MCP connection, network access or real document lookup.
execute_tool is a policy-aware synthetic adapter: its entry point is reached on
both paths, but deny returns before its post-policy execution stage. A recorded
tool_execution event is an outcome, not proof of an external adapter call. A
successful read still has side_effect_status=not_executed (no external write).
Case labels describe the intended policy variants; summary fields report actual
outcomes, including denial by any other source-config guard. This example does
not establish production authorization, authenticated identity or persistence.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_runtime_ref.approvals import ApprovalQueue  # noqa: E402
from agent_runtime_ref.config import (  # noqa: E402
    default_config_dir,
    load_agent_profile,
    load_approval_policy,
    load_capability_catalog,
    load_memory_store,
    load_policy_engine,
    load_yaml_file,
)
from agent_runtime_ref.models import ModelOutput, RunContext, RunRequest, ToolRequest  # noqa: E402
from agent_runtime_ref.runtime import AgentRuntime  # noqa: E402

QUERY = "Find the onboarding policy."


class _SearchDocsRuntime(AgentRuntime):
    def _call_model(
        self,
        request: RunRequest,
        context: RunContext,
        *,
        second_pass: bool = False,
    ) -> ModelOutput:
        if second_pass:
            result = context.tool_results[-1]
            return ModelOutput(text=f"{result.capability_name} returned {result.outcome}.")
        return ModelOutput(
            text="Request search_docs through the runtime.",
            tool_request=ToolRequest("search_docs", {"query": request.user_input}),
        )


def _build_runtime(config_dir: Path) -> _SearchDocsRuntime:
    agent, inventory = load_agent_profile(config_dir / "agent.yaml")
    controls = load_yaml_file(config_dir / "runtime-controls.yaml")["runtime_controls"]
    return _SearchDocsRuntime(
        agent=agent,
        approvals=ApprovalQueue(load_approval_policy(config_dir / "approvals.yaml")),
        catalog=load_capability_catalog(config_dir / "capabilities.yaml"),
        memory=load_memory_store(config_dir / "memory.yaml"),
        policy=load_policy_engine(config_dir / "policy.yaml", approved_inventory=inventory),
        sandbox_profile=controls.get("sandbox_profile", {}),
    )


def _run_case(config_dir: Path, output_dir: Path, case: str) -> dict[str, object]:
    runtime = _build_runtime(config_dir)
    request = RunRequest(
        user_input=QUERY,
        tenant_id="tenant-acme",
        principal_id="user-42",
        trace_id=f"trace-ch27-{case}",
        session_id=f"session-ch27-{case}",
        agent_id=runtime.agent.agent_id,
    )
    result = runtime.run(request)
    events_file = f"{case}.jsonl"
    runtime.telemetry.export_jsonl(output_dir / events_file)
    policy = next(
        event.payload
        for event in runtime.telemetry.events
        if event.event_type == "tool_policy_decision"
    )
    tool = next(
        event.payload for event in runtime.telemetry.events if event.event_type == "tool_execution"
    )
    return {
        "trace_id": request.trace_id,
        "session_id": request.session_id,
        "events_file": events_file,
        "policy": {key: policy[key] for key in ("action", "reason", "policy_id")},
        "tool": {key: tool[key] for key in ("outcome", "side_effect_status")},
        "run": asdict(result),
    }


def export_policy_trace_pair(
    output_dir: Path, *, config_dir: Path | None = None
) -> dict[str, object]:
    source = (config_dir or default_config_dir()).resolve()
    output_dir = output_dir.resolve()
    if output_dir.is_relative_to(source):
        raise ValueError("Output directory must be outside the source config directory")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Output directory must be empty or absent: {output_dir}")
    policy = load_yaml_file(source / "policy.yaml")
    if policy["policy"]["capabilities"]["search_docs"]["decision"] != "allow":
        raise ValueError("Source search_docs decision must be allow")

    output_dir.mkdir(parents=True, exist_ok=True)
    deny_config = output_dir / "deny-config"
    shutil.copytree(source, deny_config)
    policy["policy"]["capabilities"]["search_docs"]["decision"] = "deny"
    (deny_config / "policy.yaml").write_text(
        yaml.safe_dump(policy, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    summary = {
        "request": {"capability": "search_docs", "arguments": {"query": QUERY}},
        "evidence_scope": "local_reference_runtime",
        "allow": _run_case(source, output_dir, "allow"),
        "deny": _run_case(deny_config, output_dir, "deny"),
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--config-dir", type=Path, default=default_config_dir())
    args = parser.parse_args(argv)
    summary = export_policy_trace_pair(args.output_dir, config_dir=args.config_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
