# Change Review and Rollout Gate Schema

This page defines the minimal contract layer for change review and rollout gates in agent systems. It becomes useful when a team already knows that policy, prompt, model routing, retrieval, and tool exposure changes should not be released “by feel,” but has not yet shaped those checks into explicit artifacts.

If the [lifecycle artifact schema](lifecycle-artifact-schema.en.md) answers “which lifecycle entities should exist,” the change-rollout schema answers “which fields are needed to make a real release decision.”

## 1. Why a separate schema layer matters

In many agent systems, change review splits into disconnected fragments:

- engineering review in a pull request;
- safety review in a separate document;
- eval results in CI;
- rollout decision in chat or in spoken agreement.

That can feel acceptable while the system is small. But once there are multiple owners, high-risk actions, and staged rollout waves, the process stops being manageable.

A machine-readable layer is useful because it:

- ties the change record to eval requirements;
- makes the release gate explicit instead of tribal memory;
- preserves rollout strategy and blast radius;
- shortens incident review and rollback.

## 2. Core entities

A minimal layer here usually works around two entities:

- `change_review_record`
- `rollout_gate_record`

That is already enough to connect Part V, Part VII, and Part VIII into one operational discipline.

## 3. Change review record

`change_review_record` describes what changed, who reviewed it, and which conditions must be satisfied before release.

```yaml
kind: change_review_record
review_id: cr-2026-04-07-001
change_id: chg-2026-04-07-001
owner: platform-runtime
change_type: policy_update
risk_level: high
affected_surfaces:
  - policy_bundle
  - approval_contract
  - delegated_authorization_contract
  - runtime_control_schema
  - capability_session_contract
  - sandbox_profile_contract
  - failed_run_handling
  - rollout_rules
required_reviews:
  - engineering
  - safety
  - runtime_owner
required_evals:
  - offline_regression
  - targeted_safety_eval
  - trace_regression_check
  - failed_run_drill
  - sandbox_profile_review
  - verifier_quality_check
status: approved
```

The key fields are:

- `affected_surfaces` prevents risky changes from being disguised as “small tuning”;
- `required_reviews` makes ownership explicit;
- `required_evals` reduces repeated debates about what must be run;
- `status` is an operational fact, not decorative prose.

## 4. Rollout gate record

`rollout_gate_record` captures not the quality of the change in isolation, but whether the system is ready to release it into a specific rollout wave.

```yaml
kind: rollout_gate_record
gate_id: gate-2026-04-07-001
change_id: chg-2026-04-07-001
bundle_id: bundle-2026-04-07-a
rollout_wave: canary
traffic_scope: 5_percent
required_checks:
  - telemetry_ready
  - oncall_ready
  - rollback_plan_ready
  - approval_path_verified
  - high_risk_flow_checked
  - sandbox_profile_reviewed
  - failed_run_traceability_verified
blocking_findings: []
decision: go
# sandbox_profile_reviewed implies workspace materialization, permissions,
# and snapshot/resume policy were explicitly checked for sandbox-backed paths.
# failed_run_traceability_verified implies traces, release identity,
# and exported fields such as failure_reason were checked for degraded paths.
decided_by:
  - runtime_owner
  - safety_owner
```

This layer matters because even a good change review does not automatically imply rollout readiness.

That becomes even more important when rollout depends on richer verifier outputs rather than only binary pass/fail status. In that case, gate records should make explicit whether verifier quality and evidence linkage were reviewed for the affected high-risk paths.

Once approval and stateful capability sessions are part of the runtime, the gate should also say whether interruption behavior was reviewed explicitly, not assumed.

## 5. How change review differs from the rollout gate

These two layers are often confused, but they solve different questions:

- `change_review_record` answers: “should this change be releasable at all?”
- `rollout_gate_record` answers: “should it be released now, and at this scale?”

That is why the fields differ:

- the review cares more about change type, risk, and required evals;
- the rollout gate cares more about telemetry, on-call readiness, rollback, traffic scope, live readiness, and interruption handling for approval-bound or stateful capability paths.

In practice, that usually means the gate should also make explicit:

- whether capability-session expiry behavior was exercised before rollout;
- whether re-init is denied, allowed, or approval-bound for the affected path;
- whether delegated authorization continuity was checked across run traces, approval records, and session export;
- whether orchestration-pattern changes were reviewed as runtime-control changes before rollout;
- whether the sandbox profile contract, including workspace materialization, permissions, and snapshot/resume policy, was included in review when the change touches sandbox-backed execution;
- who owns emergency freeze if interruption semantics start drifting after release.

## 6. How this connects to the eval schema

Change review and rollout gates are tightly connected to the [eval schema](eval-schema.en.md):

- the review specifies which evals are mandatory;
- the gate checks whether the results are sufficient for the specific rollout wave;
- incidents and findings later flow back into the required checks;
- verifier regressions and evidence-linkage failures also become rollout-relevant findings.

That means the eval layer is not separate from release discipline. It becomes one of the pillars of the gate.

## 7. How this connects to the trace schema

The rollout gate becomes much stronger once the trace schema is in place:

- traces show whether high-risk paths were exercised;
- session summaries show whether regressions are appearing;
- structured events show what was actually checked before release;
- interruption and expiry signals show whether approval-bound runs are degrading before operators notice;
- verifier evidence shows whether process/outcome judgments used in rollout review are actually traceable.

That is why mature teams usually keep trace and rollout gate layers close together.

They should also make failed-run evidence visible before release judgment. If timeout-heavy tool paths, validation failures, or upstream outages only appear as generic unsuccessful demos, the rollout gate cannot distinguish product risk from runtime degradation. A mature gate should be able to see whether those failed runs were exercised, whether their traces and concrete failure reasons, for example `failure_reason`, stayed reviewable, and whether the same release identity governed both the happy path and the degraded path.

## 8. How this connects to the reference package

The [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) package already includes parts of this model:

- [rollout.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/rollout.py)
- [lifecycle.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/lifecycle.py)
- [configs/rollout.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/rollout.yaml)
- [configs/change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
- [configs/runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)
- CLI:
  - `check-rollout`
  - `check-change`

`check-rollout` returns `ready`, `missing_required`, `blocking_signals`, and `rollout_mode`; internally the rollout policy normalizes `block_if` into `blocked_checks`, which keeps the executable gate aligned with the schema's distinction between absent required evidence and explicit blockers.

The bundled `rollout.yaml` makes the gate inputs concrete and validates them with `'rollout' must be a mapping`, `'require' must be a list`, `'block_if' must be a list`, `'rollout_mode' must be a mapping`, and `rollout.rollout_mode entries must not be empty`: required evidence includes `trace_coverage`, `policy_prechecks`, `capability_owners`, `offline_eval_pass`, `slo_defined`, `rollback_plan`, and `oncall_owner`; `rollout_mode` sets `initial`, `max_tenant_exposure_pct`, and `require_shadow_period`; and `block_if` names hard blockers such as `unknown_side_effect_path_missing`, `direct_tool_access_present`, and `policy_decisions_not_traced`.

The adjacent `change.yaml` defines the reviewed change surface too: `change_id` is `chg-2026-04-07-support-runtime`, `change_type` is `capability_contract_update`, `risk_level` is `high`, and `rollout_strategy` is `staged_canary`. Its `required_signals` name release evidence such as `design_review_passed`, `offline_eval_passed`, `policy_diff_reviewed`, `rollback_plan_ready`, `session_expiry_behavior_checked`, `reinit_policy_reviewed`, `sandbox_profile_reviewed`, and `failed_run_drill_checked`, while `approval_roles` identifies `platform-owner` and `security-reviewer` as required reviewers.

That makes it possible to show not only the idea of a gate, but also a runnable skeleton of it.

## 9. Minimal invariants

At minimum, a healthy change-rollout layer should enforce:

- a high-risk change does not enter rollout without a review record;
- the rollout gate points to a concrete `bundle_id` and `rollout_wave`;
- required checks and blocking findings are explicit;
- every decision has an owner;
- review and gate can be reconstructed from an incident trace;
- interruption behavior for approval-bound or stateful capability sessions is checked before rollout;
- expiry and re-init behavior for capability sessions is checked before rollout;
- delegated authorization continuity between run traces, approval records, and session export is checked before rollout;
- verifier quality and evidence linkage are checked before rollout when release control depends on graded outcomes;
- orchestration-pattern changes are reviewed before rollout, especially when they add routing, parallelization, or delegated worker surfaces;
- sandbox profile changes are reviewed before rollout, especially when they change workspace entries, shell/filesystem permissions, or snapshot/resume behavior;
- the rollback plan does not live only in people’s heads.

## 10. What usually breaks

The common failure modes are familiar:

- review and rollout decisions live in different places and are disconnected;
- gating criteria are not versioned;
- telemetry readiness is judged informally;
- safety findings are not treated as blockers;
- verifier quality or evidence linkage is assumed rather than checked;
- capability-session expiry or re-init behavior is left unmodeled;
- orchestration-pattern changes slip through as “implementation detail” without explicit review;
- the rollout wave is described too vaguely;
- nobody can explain why the change was allowed into canary at all.

## 11. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Is there an explicit review record for high-risk changes?
- Is there a separate rollout gate, not just “review approved”?
- Is it clear which checks must pass before rollout?
- Is there a visible `change_id -> bundle_id -> rollout_wave` link?
- Are verifier quality and evidence-linkage checks visible when graded outcomes affect release?
- Are blocking findings and decision owners retained?
- Can incident review reconstruct which gate allowed the change through?

If the answer is “no” several times in a row, you may already have a change process, but not yet a complete rollout gate layer.

## What to Do Next

- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Policy Bundle Schema and Approval Contract](policy-bundle-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Chapter 18. Production Rollout Checklist](../book/part-vii/chapter-18.en.md)
- [Chapter 20. Change Management for Agent Systems](../book/part-viii/chapter-20.en.md)
