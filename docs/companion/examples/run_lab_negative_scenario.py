from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Final, Sequence

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_runtime_ref.catalog import CapabilitySpec  # noqa: E402
from agent_runtime_ref.execution import execute_tool  # noqa: E402
from agent_runtime_ref.models import RunContext, ToolRequest  # noqa: E402
from agent_runtime_ref.policy import PolicyEngine  # noqa: E402

SCENARIOS: Final[tuple[str, ...]] = (
    "ticket-controls-disabled",
    "platform-owner-removed",
    "high-risk-safe-transport",
    "stale-run-completion",
    "assurance-owner-missing",
)
DEFAULT_CONFIG_DIR = REPO_ROOT / "agent_runtime_ref/configs"


@dataclass(frozen=True, slots=True)
class _DurableRun:
    run_id: str
    version: int
    lease_owner: str
    idempotency_scope: str


@dataclass(frozen=True, slots=True)
class _EmergencyDecision:
    action: str
    owner: str
    evidence_event: str


def _load_yaml(path: Path) -> dict[str, object]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"Expected a mapping in {path}")
    return payload


def _write_yaml(path: Path, payload: dict[str, object]) -> None:
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def _run_runtime(args: Sequence[str]) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "agent_runtime_ref", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(completed.stdout)
    if not isinstance(payload, dict):
        raise TypeError("agent_runtime_ref must return a JSON object")
    return payload


def _disable_ticket_controls(config_dir: Path) -> None:
    capabilities_path = config_dir / "capabilities.yaml"
    capabilities = _load_yaml(capabilities_path)
    capability_map = capabilities["capabilities"]
    if not isinstance(capability_map, dict):
        raise TypeError("capabilities must be a mapping")
    create_ticket = capability_map["create_ticket"]
    if not isinstance(create_ticket, dict):
        raise TypeError("create_ticket must be a mapping")
    create_ticket["approval"] = "none"
    create_ticket["idempotency_key_required"] = False
    _write_yaml(capabilities_path, capabilities)

    policy_path = config_dir / "policy.yaml"
    policy = _load_yaml(policy_path)
    policy_root = policy["policy"]
    if not isinstance(policy_root, dict):
        raise TypeError("policy must be a mapping")
    policy_capabilities = policy_root["capabilities"]
    if not isinstance(policy_capabilities, dict):
        raise TypeError("policy.capabilities must be a mapping")
    ticket_policy = policy_capabilities["create_ticket"]
    if not isinstance(ticket_policy, dict):
        raise TypeError("policy.capabilities.create_ticket must be a mapping")
    ticket_policy["decision"] = "allow"
    _write_yaml(policy_path, policy)


def _remove_platform_owner(config_dir: Path) -> None:
    change_path = config_dir / "change.yaml"
    payload = _load_yaml(change_path)
    change = payload["change"]
    if not isinstance(change, dict):
        raise TypeError("change must be a mapping")
    roles = change["approval_roles"]
    if not isinstance(roles, list):
        raise TypeError("change.approval_roles must be a list")
    change["approval_roles"] = [role for role in roles if role != "platform-owner"]
    _write_yaml(change_path, payload)


def _run_high_risk_safe_transport() -> dict[str, object]:
    capability = CapabilitySpec(
        name="rotate_key",
        owner="security-platform",
        mode="write",
        transport="sandboxed_exec",
        timeout_seconds=10,
        tool_principal="svc-key-rotation",
        risk_tier="critical",
        network_access="none",
        allowed_egress=(),
    )
    request = ToolRequest(
        capability_name=capability.name,
        arguments={"key_id": "key-demo"},
    )
    context = RunContext(
        tenant_id="tenant-demo",
        principal_id="operator-demo",
        trace_id="trace-high-risk-safe-transport",
    )
    decision = PolicyEngine(allowed_network_access={"none"}).evaluate_tool(
        context,
        request,
        capability,
    )
    result = execute_tool(capability, request, decision)
    return {
        "scenario": "high-risk-safe-transport",
        "decision": decision.action,
        "reason": decision.reason,
        "status": result.status,
        "transport": capability.transport,
        "execution_started": result.status == "success",
        "effect_state": result.side_effect_status,
    }


def _claim_run(run: _DurableRun, worker_id: str) -> _DurableRun:
    return replace(run, version=run.version + 1, lease_owner=worker_id)


def _run_stale_completion() -> dict[str, object]:
    queued = _DurableRun(
        run_id="run-lease-demo",
        version=1,
        lease_owner="",
        idempotency_scope="run-lease-demo",
    )
    worker_a_claim = _claim_run(queued, "worker-a")
    worker_b_claim = _claim_run(worker_a_claim, "worker-b")
    return {
        "scenario": "stale-run-completion",
        "accepted": False,
        "reason": "expected_version_mismatch",
        "run_id": worker_b_claim.run_id,
        "stale_worker": worker_a_claim.lease_owner,
        "lease_owner": worker_b_claim.lease_owner,
        "expected_version": worker_a_claim.version,
        "current_version": worker_b_claim.version,
        "idempotency_scope": worker_b_claim.idempotency_scope,
        "effect_state": "not_executed",
    }


def _run_assurance_owner_missing() -> dict[str, object]:
    decision = replace(
        _EmergencyDecision(
            action="freeze_reinitialization",
            owner="runtime-assurance-on-call",
            evidence_event="assurance_response_decision",
        ),
        owner="",
    )
    missing_fields = [
        field for field in ("action", "owner", "evidence_event") if not getattr(decision, field)
    ]
    return {
        "scenario": "assurance-owner-missing",
        "ready": not missing_fields,
        "action": decision.action,
        "owner": decision.owner,
        "evidence_event": decision.evidence_event,
        "missing_fields": missing_fields,
        "blocking_findings": (
            ["assurance_decision_owner_missing"] if "owner" in missing_fields else []
        ),
    }


def run_scenario(
    scenario: str,
    *,
    config_dir: Path | None = None,
    output: Path | None = None,
) -> dict[str, object]:
    if scenario not in SCENARIOS:
        raise ValueError(f"Unsupported scenario: {scenario}")

    if scenario == "high-risk-safe-transport":
        payload = _run_high_risk_safe_transport()
    elif scenario == "stale-run-completion":
        payload = _run_stale_completion()
    elif scenario == "assurance-owner-missing":
        payload = _run_assurance_owner_missing()
    else:
        source = (config_dir or DEFAULT_CONFIG_DIR).resolve()
        with tempfile.TemporaryDirectory(prefix="agent-arch-negative-scenario-") as temp_dir:
            working_config = Path(temp_dir) / "configs"
            shutil.copytree(source, working_config)

            if scenario == "ticket-controls-disabled":
                _disable_ticket_controls(working_config)
                payload = _run_runtime(
                    (
                        "check-controls",
                        "--config-dir",
                        str(working_config),
                        "--signal",
                        "create_ticket_approval_required=true",
                        "--signal",
                        "create_ticket_idempotency_key_required=true",
                    )
                )
            else:
                _remove_platform_owner(working_config)
                payload = _run_runtime(("check-change", "--config-dir", str(working_config)))

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a closed-failure scenario used by the Russian book laboratories."
    )
    parser.add_argument("scenario", choices=SCENARIOS)
    parser.add_argument("--config-dir", type=Path, default=DEFAULT_CONFIG_DIR)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    payload = run_scenario(
        args.scenario,
        config_dir=args.config_dir,
        output=args.output,
    )
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
