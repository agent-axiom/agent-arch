# Incident Record and Postmortem Linkage Schema

This page describes the minimal contract layer for incident review in agent systems: which fields an incident record should contain, how it should connect to traces, approvals, rollout, and lifecycle artifacts, and which data should survive the containment phase.

It also connects directly to the book's [Evidence Spine: From Request to Rollout Judgment](../book/part-v/evidence-spine.en.md), because incident review is one of the places where that governed chain must stay intact.

If the [Incident Response Playbook](incident-response-playbook.en.md) answers the question “what should the team do in the first minutes and during review,” this schema answers “how should that be recorded.”

## 1. Why a separate incident record is useful

Without a dedicated incident artifact, review usually falls apart into disconnected pieces:

- traces live in the observability system;
- approval history lives in the audit trail;
- rollback decisions live in chat;
- postmortems live in a document;
- change linkage is reconstructed from memory.

That might work once or twice, but it scales poorly for repeated incidents, audit, regression updates, and lifecycle corrections.

## 2. Core entities

The minimal schema usually revolves around two entities:

- `incident_record`
- `incident_postmortem_link`

That is already enough to connect operational response and lifecycle correction.

## 3. Incident record

`incident_record` captures what happened, the blast radius, and which artifacts were active during the event.

```yaml
kind: incident_record
incident_id: inc-2026-04-09-001
title: "Unauthorized ticket_write path during onboarding run"
severity: sev2
status: contained
category: unauthorized_side_effect
detected_at: 2026-04-09T09:14:00Z
detected_by: automated_detection
agent_id: support-triage-ref
trace_id: trace-2026-04-09-001
session_id: session-2026-04-09-001
bundle_id: bundle-2026-04-07-a
change_id: chg-2026-04-07-001
rollout_wave: canary
tool_principal: svc-ticket-writer
approval_id: apr-2026-04-09-001
idempotency_key: ticket-req-2026-04-09-001
affected_surfaces:
  - approval_path
  - tool_gateway
  - rollout_gate
containment_actions:
  - force_mandatory_approval
  - disable_ticket_write_v1
owner: platform-operations
```

The most important fields here are:

- `category`, which links the incident to triage taxonomy and eval updates;
- `bundle_id`, `change_id`, and `rollout_wave`, which link the incident to release discipline;
- `tool_principal`, `approval_id`, and `idempotency_key`, which shorten the path to the real side effect and show whether a retry could safely match an already-created object;
- `affected_surfaces`, which helps avoid reducing review to model output alone.

!!! example "Incident record for the duplicate-ticket thread"
    In the support-triage incident, the record must keep `idempotency_key` next to `trace_id`, `session_id`, `approval_id`, `tool_principal`, `bundle_id`, and `rollout_wave`. Without that, review cannot reliably distinguish one unknown write from a second real `create_ticket` side effect or turn the incident into an eval/update gate.

## 4. Incident postmortem link

`incident_postmortem_link` connects a specific incident to corrective actions and lifecycle artifacts.

```yaml
kind: incident_postmortem_link
incident_id: inc-2026-04-09-001
postmortem_id: pm-2026-04-09-001
corrective_actions:
  - change_id: chg-2026-04-09-003
  - bundle_id: bundle-2026-04-09-b
  - eval_dataset_update: eval-set-2026-04-09
  - retirement_plan: retire-ticket-write-v1
owners:
  - platform-safety
  - platform-runtime
status: open
```

This layer is useful because it forces incident review to end with concrete lifecycle updates, not just text.

## 5. How this relates to the trace schema

Incident records almost always depend on the [trace schema](trace-schema.en.md):

- `trace_id` and `session_id` connect the incident to run history;
- policy events show what was allowed;
- approval events show whether a human gate existed;
- tool events show the real side effect;
- session summaries help determine whether this was a single run or a broader pattern, including whether exported failed-run evidence such as `failure_reason` stayed intact.

## 6. How this relates to approvals and the policy bundle

Incident records are especially useful when the team needs to recover quickly:

- which approval path was active;
- which decision was made;
- which policy bundle was active;
- which principal actually executed the action.

That is why incident schema belongs next to:

- [Policy Bundle Schema and Approval Contract](policy-bundle-schema.en.md)
- [Approval Request and Decision Schema](approval-schema.en.md)

## 7. How this relates to change management and rollout

Incident review rarely ends at containment.

The team usually must determine:

- which `change_id` introduced the risky path;
- which `rollout_gate_record` allowed it;
- which checks failed to catch it;
- whether rollback, restricted mode, or retirement is required.

That is why incident records should connect to the [change-rollout schema](change-rollout-schema.en.md) and the [lifecycle artifact schema](lifecycle-artifact-schema.en.md).

## 8. Relation to the reference package

The [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) package already contains several primitives that make this model practical:

- traces and session summaries;
- approval queue;
- lifecycle artifacts;
- rollout checks;
- policy and controls linkage.

Even if the package does not yet store a full `incident_record`, the book can already define which fields such a record should contain.

## 9. Minimal invariants

A mature incident layer usually has these invariants:

- each incident has a stable `incident_id`;
- `trace_id` and `session_id` are preserved immediately;
- `bundle_id`, `change_id`, and `rollout_wave` can be reconstructed without guesswork;
- containment actions are recorded explicitly;
- the incident is linked to corrective actions;
- the postmortem leads to lifecycle artifact, eval, or policy bundle updates.

## 10. What usually breaks

Common failure modes are usually:

- the incident ticket does not know about trace and session;
- the side effect is visible, but the principal is unclear;
- change linkage is reconstructed from memory;
- the postmortem is not linked to a corrective artifact;
- incidents never enter eval datasets or rollout criteria;
- a retired path remains alive after a supposedly closed incident.

## 11. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Does the incident have a stable `incident_id`?
- Can the team quickly recover `trace_id`, `session_id`, `bundle_id`, and `change_id`?
- Is it visible which principal and approval path were involved?
- Are containment actions recorded?
- Is there a clear incident -> postmortem -> corrective action link?
- Do incidents flow back into evals, rollout gates, and lifecycle updates?

## What to Do Next

- [Incident Response Playbook for Agent Systems](incident-response-playbook.en.md)
- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Approval Request and Decision Schema](approval-schema.en.md)
- [Change Review and Rollout Gate Schema](change-rollout-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Handbook for Agent Registry and Inventory Operations](registry-operations-handbook.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](../book/part-viii/chapter-21.en.md)
- [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](../book/part-viii/chapter-26.en.md)
