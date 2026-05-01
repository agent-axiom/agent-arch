# Lifecycle Artifact Schema

This page defines a minimal contract layer for lifecycle artifacts: change records, approved artifact bundles, and retirement plans. If the trace schema answers "what happened" and the eval schema answers "how do we grade it," the lifecycle artifact schema answers "what exactly was approved, changed, replaced, or retired."

It also connects directly to the book's [Evidence Spine: From Request to Rollout Judgment](../book/part-v/evidence-spine.en.md), because lifecycle artifacts are part of the governed record that later judgment and incident review stand on.

## 1. Why this matters

Production-grade agent systems have several artifact classes that should not live only in team memory or a wiki:

- change records;
- approved artifact bundles;
- retirement plans;
- replacement mappings;
- runtime-control schemas and contract-version linkages;
- operational approvals and lifecycle decisions;
- capability-session interruption, expiry, and re-initialization rules when those are part of the runtime contract;
- delegated authorization rules, principal-binding assumptions, and revoke behavior when those are part of the runtime contract;
- verifier contracts, grading rubrics, and evidence-linkage rules when release or assurance depends on verifier output;
- structured handoff artifacts when long-running work crosses context-reset or role-handoff boundaries.

Without them, change management turns into oral tradition. Incident review then becomes an exercise in reconstructing who "probably changed the policy or routing."

## 2. Core entities

A minimal lifecycle layer works well around three entities:

- `change_record`
- `artifact_bundle`
- `retirement_plan`

That is already enough to connect design review, release gates, assurance loops, and end-of-life discipline.

## 3. Change record

`change_record` describes one concrete change and its operational semantics.

Minimal fields:

```yaml
kind: change_record
change_id: chg-2026-04-07-001
title: "Tighten outbound policy for ticket_write"
change_type: policy_update
risk_level: high
owner: platform-safety
affected_surfaces:
  - policy_bundle
  - capability_contract
  - runtime_control_schema
  - capability_session_contract
  - sandbox_profile_contract
  - rollout_rules
eval_requirements:
  - offline_regression
  - targeted_safety_eval
approval_requirements:
  - safety_review
  - platform_review
rollback_unit:
  - policy_bundle:v4
  - approvals_bundle:v3
status: approved
```

The important parts are:

- `affected_surfaces` prevents teams from pretending the change is tiny;
- `eval_requirements` ties change management to the eval loop;
- `rollback_unit` forces teams to know what can be reverted;
- `status` acts as an operational fact, not just paperwork.

And once approval-bound runs, stateful capability sessions, or sandbox-backed execution exist, the change record should usually make it visible whether interruption behavior, expiry handling, re-init semantics, delegated authorization rules, and the sandbox profile contract were part of the reviewed surface.

## 4. Approved artifact bundle

`artifact_bundle` captures the set of artifacts that are considered trusted and mutually compatible for a specific release configuration. In practice, it is also the contract surface that gives a release its governed identity.

The reference runtime stores that contract in `artifacts.yaml`: `bundle_name`, `version`, `provenance_required`, `signed`, and `session_control_owner` describe the bundle identity and accountability, while `artifacts` explicitly lists release-bearing files such as `agent.yaml`, `capabilities.yaml`, `policy.yaml`, `memory.yaml`, `controls.yaml`, `approvals.yaml`, `runtime-controls.yaml`, `change.yaml`, `retirement.yaml`, `eval-dataset.json`, and `runtime-control-bundle-metadata`.

```yaml
kind: artifact_bundle
bundle_id: bundle-2026-04-07-a
owner: platform-runtime
artifacts:
  model_route: gpt-5.4-tools
  policy_bundle: policy-v4
  approvals_bundle: approvals-v3
  controls_bundle: controls-v2
  runtime_control_schema: runtime-controls-v2
  sandbox_profile: sandbox-profile-v1
  capability_catalog: catalog-v5
  eval_dataset: eval-set-2026-04-07
  verifier_contract: verifier-v2
  contract_version: capability-contract-v5
review_evidence:
  sandbox_profile_reviewed:
    trace_event: sandbox_profile_reviewed
    workspace_manifest_ref: runtime-controls.yaml#runtime_controls.sandbox_profile.workspace
    permissions_profile: restricted-shell-network-denied
    network_secrets_posture: network:denied,secrets:none
    snapshot_policy: required_on_completion
    review_evidence_refs:
      - trace:trace-sandbox-review-001
      - eval:sandbox_profile_review
status: approved
release_scope: canary
provenance:
  change_record: chg-2026-04-07-001
  reviewed_by:
    - safety-review
    - runtime-review
```

This layer is useful because:

- it separates "artifact exists" from "artifact is approved for release";
- it makes release identity inspectable instead of implicit;
- it makes incident review and rollback much shorter.

And once capability-session governance is explicit, the bundle should usually make visible not only the contract version, but also the session-control assumptions and verifier-bearing contract family that were approved together:

- expiry policy;
- re-init policy;
- ownership for stuck or expired capability-session state;
- linkage expectations between approval events and session events;
- delegated authorization mode;
- principal-binding requirements;
- revoke behavior for paused or in-flight actions;
- verifier contract version, grading rubric, and evidence-linkage expectations when rollout or assurance depends on verifier judgments;
- sandbox profile review evidence, including the `sandbox_profile_reviewed` trace event, `workspace_manifest_ref`, and links to eval/rollout evidence when release identity includes sandbox-backed execution.

## 5. Retirement plan

`retirement_plan` is useful not only for shutting down a whole agent, but also for controlled replacement of a capability, policy bundle, or artifact family.

```yaml
kind: retirement_plan
retirement_id: retire-2026-04-ticket-write-v1
target: capability:ticket_write_v1
trigger: deprecated_capability
replacement: capability:ticket_write_v2
phases:
  - freeze_new_rollouts
  - dual_run
  - traffic_shift
  - expire_paused_runs
  - stop_background_routes
  - revoke_principal
  - archive_artifacts
historical_state:
  traces: retain_90_days
  approvals: retain_180_days
  memory: review_before_delete
status: planned
owner: platform-operations
```

Its strength is that it forces the team to think not only about replacement, but also about the remains of the old system:

- traces;
- approvals;
- paused-run state;
- background-route ownership;
- principals;
- memory;
- archived bundles;
- structured handoff artifacts that carried sprint scope, evaluator critique, or reset-boundary decisions;
- expired capability-session state that may still matter for audit or delayed operator response.

## 6. How this connects to Part VIII

This schema directly supports several chapters:

- Chapter 20: change management;
- Chapter 21: assurance findings as lifecycle input;
- Chapter 22: approved artifacts and provenance;
- Chapter 23: replacement and retirement.

That is why lifecycle artifacts work best not as prose-only documentation, but as reviewable YAML or JSON contracts.

The reference runtime mirrors that shape in `retirement.yaml`: `system_id` and `replacement_mode` identify the retiring surface, `triggers` list why retirement starts, `required_steps` includes controls such as `freeze_rollout`, `disable_risky_capabilities`, `stop_memory_write`, `expire_paused_runs`, `stop_background_routes`, `freeze_reinitialization`, `revoke_egress`, `archive_audit_state`, and `set_retired_status`, while `session_control_owner`, `emergency_freeze_owner`, and `archive_targets` keep the ownership and retained evidence explicit. Its archive list names `telemetry_jsonl`, `session_exports`, `approval_history`, `paused_run_state`, `capability_session_state`, and `runtime_control_bundle`, matching the records that must remain reviewable after retirement.

## 7. Minimal invariants

At minimum, a healthy lifecycle artifact layer should enforce:

- every high-risk change has a `change_record`;
- every production rollout points to an `artifact_bundle`;
- every artifact bundle can serve as a concrete release-identity record, not just a loose list of versions;
- every artifact bundle links runtime-control schema and contract version when those controls exist;
- verifier contract lineage and contract-family identity can be reconstructed when release or assurance depends on graded outcomes;
- sandbox profile review evidence can be reconstructed from the bundle, trace, or eval artifact when rollout required `sandbox_profile_reviewed`;
- every deprecated artifact has a `retirement_plan` or an explicit exception;
- retirement or replacement paths explain what happens to paused runs, handoff artifacts, and expired capability-session state when those paths exist;
- delegated authorization ownership and revoke behavior can be reconstructed for affected runs when those controls exist;
- lifecycle artifacts have an owner and version;
- incident review can reconstruct `change -> bundle -> run -> retirement`;
- session-control ownership can be reconstructed for expired, paused, or re-initialized capability paths.

## 8. What usually breaks

The failure modes are usually familiar:

- the bundle exists only "by agreement" and not as an artifact;
- change records are disconnected from eval requirements;
- retirement lives in the roadmap but not in operational config;
- replacement happens without dual-run semantics;
- historical state has no retention owner;
- provenance stops at the git commit and never reaches the runtime bundle;
- paused-run and expired-session state are forgotten during replacement even though operators may still need them;
- verifier contract lineage is lost even though rollout or assurance decisions depended on it;
- the bundle names `sandbox_profile`, but does not retain a review-evidence link for workspace, permissions, and snapshot/resume policy.

## 9. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Do high-risk changes have explicit change records?
- Do you have an approved artifact bundle instead of a list of latest YAML files?
- Can you reconstruct the active bundle and its release identity from an incident trace?
- Can you tell which verifier-bearing contract family a release was approved under?
- If the bundle includes `sandbox_profile`, can you find review evidence for workspace, permissions, and snapshot/resume policy?
- Is there a retirement plan for deprecated capabilities and policy bundles?
- Does archived state have an owner after replacement?
- Is the rollback unit clear at the lifecycle-artifact level?

If the answer is "no" several times in a row, your SDLC and rollout may already be decent, but the lifecycle layer is still incomplete.

## What to Do Next

- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)
- [Policy Bundle Schema and Approval Contract](policy-bundle-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Chapter 20. Change Management for Agent Systems](../book/part-viii/chapter-20.en.md)
- [Chapter 22. Supply Chain, Provenance, and Approved Artifacts](../book/part-viii/chapter-22.en.md)
- [Chapter 23. Retirement, Replacement, and End-of-Life Discipline](../book/part-viii/chapter-23.en.md)
