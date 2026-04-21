# Evidence Spine: From Request to Rollout Judgment

This page makes one structural claim explicit: a production agent system should not treat tracing, policy, approvals, evals, incident review, and rollout judgment as adjacent topics.

They are one operating record.

If you cannot follow one run across those layers, you do not yet have an evidence spine. You have disconnected controls.

## After this page, you should be able to

- explain why traces, policy, approvals, evals, incidents, and rollout judgment belong to one governed record;
- name the minimum identifiers that keep one suspicious run reviewable;
- show how runtime behavior, human decision, lifecycle artifacts, and release judgment connect without guesswork.

## Why this page exists

Several chapters in the book already describe parts of this chain:

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../part-vii/chapter-17.en.md)
- [Chapter 20. Change Management for Agent Systems](../part-viii/chapter-20.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](../part-viii/chapter-21.en.md)
- [Chapter 22. Supply Chain, Provenance, and Approved Artifacts](../part-viii/chapter-22.en.md)

What those chapters still need, as a shared bridge, is one explicit walkthrough that shows how a single governed run remains legible from user request to rollout judgment.

That is the job of this page.

## The core claim

An evidence spine is the minimum governed continuity that lets an operator answer all of these questions without guesswork:

- what request started the run;
- which policy bundle and release identity were active;
- which tools were called;
- whether approval was required, granted, denied, or expired;
- which trace events and structured signals were emitted;
- how the run was graded or evaluated afterward;
- whether the run triggered incident review;
- whether the resulting evidence changed rollout judgment.

That should hold for degraded paths too. A failed-run drill is only useful if the same chain still explains which release identity governed the failure, which trace preserved it, which concrete failure reason remained visible, how it was graded, and whether it changed rollout judgment.

Without that continuity, teams may still have traces, approval logs, and eval reports, but they do not yet have one reviewable operating record.

## Minimal shared entity map

A strong evidence spine does not require one giant schema. It does require a stable set of identifiers and links across layers.

At minimum, one governed run should stay legible through entities such as:

- `run_id`, the runtime identity of the execution;
- `trace_id`, the trace or event lineage for that run;
- `approval_id`, the human gate record when approval is involved;
- `policy_bundle_version`, the governed policy surface active for the run;
- `artifact_id`, the approved artifact or artifact bundle linked to the release surface;
- `evaluation_result_id`, the grading or judgment record attached afterward.

In more mature systems, the chain often also includes:

- `release_identity`;
- `change_id`;
- `session_id`;
- `incident_id`;
- `verifier_contract_id` or verifier bundle lineage.

The point is not naming purity. The point is reviewable linkage.

<div class="diagram-card">
<p>A useful evidence spine is a chain of linked records, not a pile of disconnected artifacts</p>

``` mermaid
flowchart LR
    A["run_id"] --> B["trace_id"]
    A --> C["policy_bundle_version"]
    A --> D["approval_id"]
    A --> E["evaluation_result_id"]
    C --> F["release_identity"]
    C --> G["artifact_id"]
    E --> H["verifier_contract_id"]
    E --> I["incident_id"]
    I --> J["rollout judgment"]
```

</div>

## One end-to-end run walkthrough

Take a support-triage agent that can classify an incoming request, search internal knowledge, and create a ticket only after approval for high-risk cases.

### Step 1. User request enters the system

A user sends a message asking for a ticket to be opened against a production customer issue.

At this moment, the system should already create at least:

- a `run_id` for the execution;
- a `trace_id` for the event lineage;
- a link to the currently active `policy_bundle_version` and `release_identity`.

If the team cannot later prove which governed release surface handled the request, the chain is already weak before the first tool call.

### Step 2. Policy evaluation shapes what may happen

The policy layer determines:

- whether this capability is allowed for this tenant and actor;
- whether internal knowledge retrieval is permitted;
- whether ticket creation requires approval;
- whether delegated authorization is allowed;
- whether a verifier contract is required for high-risk handling.

This is why [Chapter 17](../part-vii/chapter-17.en.md) matters inside the spine. Policy is not just a static configuration layer. It is part of the evidence that explains why the run was or was not allowed to proceed.

### Step 3. Tool calls and runtime events create raw history

The runtime retrieves context, maybe classifies the issue, and prepares a proposed ticket payload.

Now [Chapter 11](chapter-11.en.md) becomes visible as the raw evidence layer. The run should emit structured events that let an operator later see:

- what inputs were accepted or rejected;
- which tool calls were attempted;
- whether retries happened;
- whether a session paused;
- whether output was redacted;
- which concrete failure reason was preserved for degraded paths;
- where the system stopped before side effects.

Without this layer, later judgment becomes storytelling instead of reconstruction.

### Step 4. Approval creates a human decision record

The policy layer requires approval before the ticket can be created.

The approval step should create or attach an `approval_id` that is linked back to:

- `run_id`;
- `trace_id`;
- `policy_bundle_version`;
- `release_identity`;
- the requested capability and risk tier.

If approval is denied, that denial is not only an interaction outcome. It is part of the governed run history.

If approval expires, that expiry is also evidence. It should not disappear into UI state.

### Step 5. Eval and grading turn history into judgment

Afterward, the run may enter offline review, online grading, or regression comparison.

This is where [Chapter 13](chapter-13.en.md) enters the spine. The eval layer should not float free as a disconnected score sheet. It should attach judgment to the exact run, trace, and governed release surface that produced the behavior.

That is what lets a team distinguish between:

- a one-off failure;
- a policy regression;
- a release-specific degradation;
- a verifier-trust problem;
- an approval-path breakdown.

### Step 6. Incident review turns evidence into operational response

If the run exposed a serious problem, [Chapter 21](../part-viii/chapter-21.en.md) becomes active.

Now the team needs one connected record that shows:

- what happened;
- what controls fired;
- which controls were missing;
- whether approval intervened correctly;
- whether the issue belongs to the runtime, policy bundle, release artifact, verifier contract, or operator workflow.

If those links do not exist, incident review turns into cross-system archaeology.

### Step 7. Rollout judgment uses the same chain

Finally, [Chapter 20](../part-viii/chapter-20.en.md) uses this evidence to answer a release question:

- can rollout continue;
- should it pause;
- should it roll back;
- does the policy bundle need revision;
- does the artifact set need replacement;
- does the approval contract need tightening.

This is the last reason the evidence spine matters. Rollout judgment should not rely on intuition or dashboards alone. It should rely on a chain that already links runtime behavior, controls, approval, evidence, and release identity.

## One artifact-level example

A compact governed record for the same run may look like this:

```yaml
run_id: run-support-042
trace_id: trace-support-042
session_id: session-support-007
policy_bundle_version: 2026.04.19
release_identity: release-support-triage-2026-04-19-canary
approval_id: approval-118
artifact_id: artifact-bundle-2026-04-19-a
change_id: change-2026-04-19-17
verifier_contract_id: verifier-contract-v3
evaluation_result_id: eval-result-042
incident_id: incident-2026-04-19-3
latest_rollout_decision: pause-canary
```

The point of this example is not the exact field set. The point is that one suspicious run should leave behind enough linkage that the team can move from runtime behavior to approval record, eval judgment, incident review, and rollout action without reconstructing the chain by hand.

## What operators should be able to reconstruct

For one suspicious run, an operator should be able to answer all of the following quickly:

- which request triggered it;
- which release identity handled it;
- which policy bundle version governed it;
- whether approval was requested and how it resolved;
- what trace events describe the path;
- what eval or grading record judged the outcome;
- whether the run contributed to an incident or rollout decision.

If any of those answers require guesswork, the evidence spine is incomplete.

## What this page does not replace

This page does not replace the surrounding chapters:

- Chapter 11 still owns raw evidence capture;
- Chapter 13 still owns reviewable judgment;
- Chapter 17 still owns governed runtime policy;
- Chapter 20 still owns release judgment;
- Chapter 21 still owns assurance response;
- Chapter 22 still owns provenance, artifact lineage, and evidence backbone.

This page only makes the connective tissue explicit.

## Read next

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../part-vii/chapter-17.en.md)
- [Chapter 20. Change Management for Agent Systems](../part-viii/chapter-20.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](../part-viii/chapter-21.en.md)
- [Chapter 22. Supply Chain, Provenance, and Approved Artifacts](../part-viii/chapter-22.en.md)
