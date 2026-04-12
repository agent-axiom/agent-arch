# Postmortem Template for Agent Systems

This template is not meant to produce a polished document. It is meant to ensure that incident review ends with concrete corrective actions, lifecycle updates, and changes to eval discipline.

Use it after the containment phase, once traces, approvals, rollout data, and the active bundle have been reconstructed.

## 1. Short summary

- `incident_id`:
- Date and time:
- Severity:
- Status:
- Owner:
- Short incident summary:

## 2. What happened

- Which agent or workflow was involved:
- Which user input, retrieved context, or external trigger started the path:
- Which risky action or failure occurred:
- Whether a real side effect happened:

The purpose of this section is to capture the event chain briefly and without interpretation.

## 3. Which artifacts were active

- `trace_id`:
- `session_id`:
- `bundle_id`:
- `change_id`:
- `rollout_wave`:
- `policy_bundle`:
- `approval_mode`:
- `tool_principal`:

If this section cannot be filled quickly, the team has a problem not only with the incident, but also with observability or the lifecycle layer.

## 4. Containment actions

- Which actions were taken in the first minutes:
- What was disabled, restricted, or moved into restricted mode:
- Whether rollback was required:
- Whether any principals, connectors, or capabilities were revoked:

It is useful to distinguish between:

- temporary containment;
- permanent correction.

## 5. Root cause

- What the immediate cause of the incident was:
- Which contributing factors amplified the problem:
- Which gate, review, or assumption failed:
- Whether the problem lived in policy, approvals, rollout, memory, observability, or inventory:

This section should lead to a systemic explanation, not just “the model made a mistake.”

## 6. What failed in the control layer

- Which policy decision allowed the risky path:
- Whether there was approval bypass, missing approval, or the wrong approval scope:
- Which checks or evals failed to catch the issue:
- Which detection rules failed or triggered too late:

The goal here is to describe not only the error, but the missing guardrail.

## 7. Blast radius

- Which users, systems, or data were affected:
- Whether external systems were touched:
- Whether memory records were affected:
- Whether this was a single run or a broader pattern across a rollout wave or session family:

## 8. Corrective actions

For each action, it is useful to record:

- the action;
- the owner;
- the due date;
- which artifact is updated.

Typical corrective actions include:

- update policy bundle;
- tighten approval mode;
- update eval dataset;
- add targeted regression;
- update rollout gate;
- retire a capability or principal;
- update the registry record;
- add a detection rule.

## 9. What changes in lifecycle artifacts

- New `change_id`, if a correction release is needed:
- New `bundle_id`, if the release configuration changes:
- Whether a new `retirement_plan` is needed:
- Whether registry or inventory must be updated:
- Whether incident taxonomy or postmortem rubric must change:

This section is useful because it ties the postmortem to managed artifacts, not only tracker tasks.

## 10. What changes in evals and rollout

- Which cases should enter the eval dataset:
- Which behavioral or control evals should be added:
- Whether rollout gate criteria must change:
- Whether canary scope or approval thresholds must change:

If incidents do not flow back into evals and rollout rules, teams usually repeat the same failure class.

## 11. Short YAML template

```yaml
postmortem:
  incident_id: inc-2026-04-09-001
  severity: sev2
  owner: platform-operations
  active_artifacts:
    trace_id: trace-2026-04-09-001
    session_id: session-2026-04-09-001
    bundle_id: bundle-2026-04-07-a
    change_id: chg-2026-04-07-001
    rollout_wave: canary
  root_cause:
    primary: approval_scope_too_broad
    contributing:
      - missing_targeted_eval
      - stale_rollout_gate
  corrective_actions:
    - owner: platform-safety
      action: tighten_approval_policy
      due: 2026-04-12
    - owner: runtime-team
      action: add_regression_eval
      due: 2026-04-13
  lifecycle_updates:
    change_id: chg-2026-04-09-003
    bundle_id: bundle-2026-04-09-b
```

## 12. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Does the postmortem include a precise `incident_id`?
- Are `trace_id`, `session_id`, `bundle_id`, and `change_id` reconstructed?
- Does it include contributing factors, not only a root cause?
- Are control gaps recorded?
- Are there concrete corrective actions with owners and due dates?
- Is it clear which lifecycle artifacts must change?
- Does the incident flow back into evals and rollout criteria?

## What to Do Next

- [Incident Response Playbook for Agent Systems](incident-response-playbook.en.md)
- [Incident Record and Postmortem Linkage Schema](incident-record-schema.en.md)
- [Change Review and Rollout Gate Schema](change-rollout-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Handbook for Agent Registry and Inventory Operations](registry-operations-handbook.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](../book/part-viii/chapter-21.en.md)
