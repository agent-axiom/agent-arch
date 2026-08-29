from __future__ import annotations

import json
import sys
from dataclasses import dataclass, replace
from decimal import Decimal
from pathlib import Path
from typing import Final

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_runtime_ref.telemetry import TelemetryEmitter  # noqa: E402
from agent_runtime_ref.trajectory import (  # noqa: E402
    ApprovalRecord,
    CumulativeLimitRule,
    Fingerprint,
    RequiredApprovalRule,
    RequiredPredecessorRule,
    TrajectoryCounter,
    TrajectoryPolicy,
    TrajectoryRequest,
    TrajectorySnapshot,
    ValueBindingRule,
    compute_trajectory_request_fingerprint,
    evaluate_trajectory_policy,
)

DESTINATION_A: Final = f"sha256:{'a' * 64}"
DESTINATION_B: Final = f"sha256:{'b' * 64}"


@dataclass(frozen=True, slots=True)
class Scenario:
    name: str
    request: TrajectoryRequest
    snapshot: TrajectorySnapshot


def _policy() -> TrajectoryPolicy:
    return TrajectoryPolicy(
        policy_id="transfer-trajectory",
        policy_version="2026.08.23",
        rules=(
            ValueBindingRule("destination-binding", "destination"),
            CumulativeLimitRule("daily-amount-limit", "amount", Decimal("100")),
            RequiredPredecessorRule(
                "destination-confirmed-first",
                "confirm_destination",
            ),
            RequiredApprovalRule("transfer-approval", "transfer"),
        ),
    )


def _base_request() -> TrajectoryRequest:
    return TrajectoryRequest(
        action="submit_transfer",
        tenant_id="tenant-example",
        subject_id="subject-example",
        expected_history_ref="trajectory://transfer/example-001",
        expected_history_version=7,
        sequence_number=3,
        fingerprints=(Fingerprint("destination", DESTINATION_A),),
        counters=(TrajectoryCounter("amount", Decimal("20")),),
        window_id="daily-2026-08-23",
    )


def _base_snapshot(
    request: TrajectoryRequest,
    policy: TrajectoryPolicy,
) -> TrajectorySnapshot:
    return TrajectorySnapshot(
        history_ref=request.expected_history_ref,
        history_version=request.expected_history_version,
        tenant_id=request.tenant_id,
        subject_id=request.subject_id,
        policy_id=policy.policy_id,
        policy_version=policy.policy_version,
        integrity="verified",
        status="current",
        observed_sequence=("read_destination", "confirm_destination"),
        fingerprints=(Fingerprint("destination", DESTINATION_A),),
        counters=(TrajectoryCounter("amount", Decimal("40")),),
        window_id="daily-2026-08-23",
        window_state="open",
        approval_records=(
            ApprovalRecord(
                approval_id="approval-example-001",
                scope="transfer",
                request_fingerprint=compute_trajectory_request_fingerprint(
                    request,
                    policy,
                ),
                state="approved",
            ),
        ),
        approval_state="approved",
    )


def build_scenarios(policy: TrajectoryPolicy) -> tuple[Scenario, ...]:
    request = _base_request()
    snapshot = _base_snapshot(request, policy)
    return (
        Scenario(
            name="destination_fingerprint_mismatch",
            request=replace(
                request,
                fingerprints=(Fingerprint("destination", DESTINATION_B),),
            ),
            snapshot=snapshot,
        ),
        Scenario(
            name="cumulative_limit_exceeded",
            request=replace(
                request,
                counters=(TrajectoryCounter("amount", Decimal("40")),),
            ),
            snapshot=replace(
                snapshot,
                counters=(TrajectoryCounter("amount", Decimal("70")),),
            ),
        ),
        Scenario(
            name="required_predecessor_missing",
            request=replace(request, sequence_number=2),
            snapshot=replace(snapshot, observed_sequence=("read_destination",)),
        ),
        Scenario(
            name="required_approval_missing",
            request=request,
            snapshot=replace(snapshot, approval_records=(), approval_state="none"),
        ),
        Scenario(
            name="trusted_trajectory_allowed",
            request=request,
            snapshot=snapshot,
        ),
    )


def run_scenarios() -> dict[str, object]:
    emitter = TelemetryEmitter()
    scenario_results: list[dict[str, str]] = []
    policy = _policy()
    for scenario in build_scenarios(policy):
        decision = evaluate_trajectory_policy(scenario.request, scenario.snapshot, policy)
        emitter.emit(
            "trajectory_policy_decision",
            f"trace-{scenario.name}",
            **decision.to_event_payload(),
        )
        scenario_results.append(
            {
                "scenario": scenario.name,
                "decision": decision.decision,
                "rule_id": decision.rule_id,
                "reason": decision.reason,
            }
        )
    return {
        "contract": "trajectory-policy-scenarios/v1",
        "scenarios": scenario_results,
        "events": emitter.as_dicts(),
    }


def main() -> int:
    print(json.dumps(run_scenarios(), ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
