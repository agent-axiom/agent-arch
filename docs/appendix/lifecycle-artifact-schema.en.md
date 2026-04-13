# Lifecycle Artifact Schema

This page defines a minimal contract layer for lifecycle artifacts: change records, approved artifact bundles, and retirement plans. If the trace schema answers "what happened" and the eval schema answers "how do we grade it," the lifecycle artifact schema answers "what exactly was approved, changed, replaced, or retired."

## 1. Why this matters

Production-grade agent systems have several artifact classes that should not live only in team memory or a wiki:

- change records;
- approved artifact bundles;
- retirement plans;
- replacement mappings;
- runtime-control schemas and contract-version linkages;
- operational approvals and lifecycle decisions.

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

## 4. Approved artifact bundle

`artifact_bundle` captures the set of artifacts that are considered trusted and mutually compatible for a specific release configuration.

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
  capability_catalog: catalog-v5
  eval_dataset: eval-set-2026-04-07
  contract_version: capability-contract-v5
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
- it makes incident review and rollback much shorter.

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
- archived bundles.

## 6. How this connects to Part VIII

This schema directly supports several chapters:

- Chapter 20: change management;
- Chapter 21: assurance findings as lifecycle input;
- Chapter 22: approved artifacts and provenance;
- Chapter 23: replacement and retirement.

That is why lifecycle artifacts work best not as prose-only documentation, but as reviewable YAML or JSON contracts.

## 7. Minimal invariants

At minimum, a healthy lifecycle artifact layer should enforce:

- every high-risk change has a `change_record`;
- every production rollout points to an `artifact_bundle`;
- every artifact bundle links runtime-control schema and contract version when those controls exist;
- every deprecated artifact has a `retirement_plan` or an explicit exception;
- lifecycle artifacts have an owner and version;
- incident review can reconstruct `change -> bundle -> run -> retirement`.

## 8. What usually breaks

The failure modes are usually familiar:

- the bundle exists only "by agreement" and not as an artifact;
- change records are disconnected from eval requirements;
- retirement lives in the roadmap but not in operational config;
- replacement happens without dual-run semantics;
- historical state has no retention owner;
- provenance stops at the git commit and never reaches the runtime bundle.

## 9. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Do high-risk changes have explicit change records?
- Do you have an approved artifact bundle instead of a list of latest YAML files?
- Can you reconstruct the active bundle from an incident trace?
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
