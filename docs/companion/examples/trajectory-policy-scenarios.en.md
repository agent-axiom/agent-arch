# Trajectory Policy Scenarios

Status: executable companion example with an intentionally limited contract.

Sources:

- `agent_runtime_ref/trajectory.py`
- `tests/test_trajectory_policy.py`
- `docs/companion/examples/run_trajectory_policy_scenarios.py`

## Run

From the selected worktree root, run:

```bash
/path/to/agent-arch/.venv/bin/python \
  docs/companion/examples/run_trajectory_policy_scenarios.py
```

Here `/path/to/agent-arch` denotes the main clone directory that owns `.venv`;
the runner imports code from the current worktree. Its output is JSON with
sorted keys and a fixed scenario order.

## Expected decisions

| Scenario | Decision | Rule | Reason |
| --- | --- | --- | --- |
| `destination_fingerprint_mismatch` | `deny` | `destination-binding` | `value_binding_mismatch` |
| `cumulative_limit_exceeded` | `deny` | `daily-amount-limit` | `cumulative_limit_exceeded` |
| `required_predecessor_missing` | `deny` | `destination-confirmed-first` | `required_predecessor_missing` |
| `required_approval_missing` | `approval_required` | `transfer-approval` | `required_approval_missing` |
| `trusted_trajectory_allowed` | `allow` | `trajectory.all_rules` | `all_rules_satisfied` |

In the second scenario, the current value `40` is below the limit `100`, but
the trusted snapshot already contains `70`, so the total is denied closed. The
first scenario compares normalized fingerprints, never raw account details.
Addition uses a local exact Decimal contract: scale up to 6, maximum value
`999999999999.999999`, precision 32, and traps. It does not depend on mutable
global Decimal context.

The runner does not supply a request fingerprint. It derives one from the
action, tenant and subject, expected history reference and version, sequence,
window, policy ID and version, sorted significant fingerprints, and counter
deltas. The positive scenario binds its `ApprovalRecord` to that value. A
change to any bound field prevents reuse of the earlier approval.

For each scenario, the runner calls `TelemetryEmitter.emit` with the event type
`trajectory_policy_decision`. Every value in `event.payload` is a string. The
event contains fingerprints and counter states but no raw destination, account
details, tool arguments, or secrets.

Identifiers and references pass a bounded lowercase ASCII allowlist, and the
completed payload is validated again before emission. This is a structural
safeguard, not a semantic secret scanner: the snapshot provider remains
responsible for keeping secrets out of formally valid identifiers, references,
and hash inputs.

To keep a formally valid request from breaking the mandatory audit event, the
contract accepts at most 16 fingerprints and 32 counters in each request and
snapshot. Construction enforces these bounds, and maximum valid collections
still fit within the telemetry string limits.

## Implementation boundary

`evaluate_trajectory_policy` is a pure deterministic function. It receives the
current `TrajectoryRequest`, a frozen `TrajectorySnapshot`, and a
`TrajectoryPolicy`; model context and compaction summaries are never sources of
history. `integrity=verified` is an assertion made by the trusted snapshot
provider. The teaching evaluator does not verify that assertion's signature or
provenance. A `None` history is denied with `history_missing`; a malformed
mapping or object is denied with `history_malformed`, without reflecting the raw
object into the decision or telemetry.

This example does **not** provide distributed transactional consistency,
locking, compare-and-swap for history versions, atomic action-and-counter
updates, protection from the race between policy evaluation and the external
effect, a durable append-only log, or crash recovery. It is not connected to
`AgentRuntime`. In production, an external component must obtain an integral
snapshot from a trusted log, enforce version synchronization and locking or a
transaction, atomically record the decision and action result, and perform
recovery or reconciliation after a failure.
