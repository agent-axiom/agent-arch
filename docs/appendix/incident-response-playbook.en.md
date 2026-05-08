# Incident Response Playbook for Agent Systems

This playbook is useful once a team already has traces, policy gates, approval paths, and rollout rules, but still lacks a short operational path for handling a failure, a risky action, or a policy bypass.

It does not replace the chapters on assurance, observability, or change management. It turns them into one working response path.

## 1. What counts as an incident

For an agent system, an incident usually includes more than an outage or quality degradation:

- an irreversible side effect without the required approval path;
- a policy bypass or an incorrect gateway decision;
- risky egress to an unapproved external system;
- memory contamination or an incorrect persistent write;
- a rollout escape that bypassed evals or rollout gates;
- suspicious autonomy, sabotage-like behavior, or attempts to hide actions.

## 2. The first 15 minutes

In the first minutes, the goal is not full root-cause analysis. The goal is to contain damage and preserve evidence.

A minimal order of actions usually looks like this:

1. Stop or narrow the risky path.
2. Capture trace and session context.
3. Determine whether an external side effect already happened.
4. Check whether a capability, principal, or connector must be disabled.
5. Record which bundle and rollout wave were active during the incident.

## 3. What to preserve immediately

If these artifacts are not preserved in the first minutes, incident review quickly degrades into reconstruction from memory:

- `trace_id`
- `session_id`
- `agent_id`
- `tool_principal`
- `approval_id`, if an approval path was involved;
- `bundle_id`
- `change_id`
- `rollout_wave`
- policy decision events;
- approval decision events;
- memory records that were read or modified;
- `allowed_egress` data and the actual network path.

## 4. Fast containment actions

Good incident response depends on predesigned containment actions:

- disable a specific capability instead of the whole runtime;
- switch a high-risk action into mandatory approval mode;
- temporarily pause memory writes;
- revoke a connector credential or tool principal;
- stop the current rollout wave;
- activate a stricter policy bundle.

Without these actions, incident response becomes an argument about who is allowed to shut something down.

## 5. Minimal triage taxonomy

It is useful to classify the incident immediately:

- `policy_bypass`
- `unauthorized_side_effect`
- `dangerous_egress`
- `memory_contamination`
- `approval_failure`
- `eval_escape`
- `agentic_misalignment`

These categories are useful not only for a ticket, but also for linking incidents back into eval datasets, rollout gates, and postmortem discipline.

!!! example "Duplicate-ticket response path"
    For the running support-triage incident, first freeze `create_ticket` or switch it to mandatory approval, preserve `trace_id`, `session_id`, `approval_id`, `tool_principal`, `idempotency_key`, `bundle_id`, and `rollout_wave`, then check whether the side effect already happened. If status is unknown, mark the run as `side_effect_unknown`, do not blindly repeat the write, and turn the review into an eval/rollout gate before the next release.

## 6. What to check in traces and events

During first-pass investigation, the team should answer a few questions quickly:

- which input or retrieved context triggered the risky path;
- which policy decision allowed it;
- which principal actually executed the action;
- whether there was an approval request, denial, or bypass;
- which memory records were read or written;
- which artifact bundle was active in the run;
- whether this was a single run or a broader pattern across the session or rollout wave.

If traces cannot answer these questions, the problem is no longer only the incident. It is also the observability layer.

## 7. When to roll back and when to fix locally

Not every incident requires a full rollback. Local containment is acceptable only when:

- the blast radius is understood;
- the risky path can be isolated cleanly;
- the active bundle is known precisely;
- the rollout wave can be stopped without hidden dependencies.

Full rollback is more common when the team cannot confidently separate the affected surface from the rest of the system.

## 8. What should enter the postmortem

A useful postmortem for an agent system usually includes:

- which artifact bundle was active;
- which change review and rollout gate allowed this path;
- which checks or evals were missing;
- which detection rules failed;
- which containment action was used;
- what changes next in policy, evals, rollout rules, or inventory.

A good postmortem ends not only with a document, but with updated lifecycle artifacts.

## 9. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Can you disable one capability quickly?
- Can you reconstruct `trace -> session -> bundle -> rollout wave`?
- Is it clear which principal executed the external call?
- Is the approval path and its decision visible?
- Can you pause memory writes temporarily?
- Is ownership for containment actions clear?
- Do incidents flow back into evals and rollout gates?

## What to Do Next

- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Policy Bundle Schema and Approval Contract](policy-bundle-schema.en.md)
- [Approval Request and Decision Schema](approval-schema.en.md)
- [Change Review and Rollout Gate Schema](change-rollout-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](../book/part-viii/chapter-21.en.md)
- [Chapter 23. Retirement, Replacement, and End-of-Life Discipline](../book/part-viii/chapter-23.en.md)
- [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](../book/part-viii/chapter-26.en.md)
