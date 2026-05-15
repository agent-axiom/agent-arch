# Evidence Spine: From Request to Rollout Judgment

In a production agent system, tracing, policy, approvals, evals, incident review, and rollout judgment should not be treated as merely adjacent topics. For an operator, they are one operational record.

If you cannot follow one suspicious run through all of those layers, you do not yet have an evidence spine. You have disconnected controls.

## What You Should Be Able to Do After This Page

- explain why traces, policy, approvals, evals, incidents, and rollout judgment form one governed record;
- name the minimum set of identifiers that keeps one suspicious run reviewable;
- show how runtime behavior, human decision, lifecycle artifacts, and release judgment stay linked without guesswork.

## Why This Page Exists

Several chapters of the book already describe parts of that chain:

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../part-vii/chapter-17.en.md)
- [Chapter 20. Change Management for Agent Systems](../part-viii/chapter-20.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](../part-viii/chapter-21.en.md)
- [Chapter 22. Supply Chain, Provenance, and Approved Artifacts](../part-viii/chapter-22.en.md)

This page gathers them into one walkthrough to show how a single governed run stays legible from user request to rollout judgment.

## The Core Claim

An evidence spine is the minimum governed continuity that lets an operator answer all of the questions below without guesswork:

- which request started the run;
- which policy bundle and release identity were active;
- which tools were called;
- whether approval was required and whether it was granted, denied, or expired;
- which trace events and structured signals were recorded;
- how the run was later graded or evaluated;
- whether it triggered incident review;
- whether the resulting evidence changed rollout judgment.

That also has to remain true for degraded paths. A failed-run drill is useful only if the same chain still explains which release identity governed the failure, which trace preserved it, which concrete failure reason, for example in `failure_reason`, remained visible, how it was graded, and whether it changed rollout judgment.

Without that continuity, a team may have traces, approval logs, and eval reports and still lack one reviewable operational record.

**Case-spine routing note:** the same evidence spine should stay visible across the book's three canonical cases. Support triage stresses approvals and side effects; Internal knowledge assistant stresses retrieval provenance, freshness, and access control; Incident coordination stresses escalation, response ownership, and post-incident rollout judgment. If a control only works for one case, it is a local feature, not an evidence spine.

## Minimal Shared Entity Map

A strong evidence spine does not require one giant schema file. It does require a stable set of identifiers and links across layers.

At minimum, one governed run should stay legible through entities such as:

- `run_id`, the runtime execution identity;
- `trace_id`, the trace or event lineage for that run;
- `approval_id`, the human gate record when approval is involved;
- `policy_bundle_version`, the governed policy surface active for the run;
- `artifact_id`, the approved artifact or artifact bundle linked to the release surface;
- `evaluation_result_id`, the grading or judgment record attached later.

In more mature systems, the chain often also includes:

- `release_identity`;
- `change_id`;
- `session_id`;
- `incident_id`;
- `verifier_contract_id` or the lineage of verifier contract bundles;
- `handoff_artifact_id` when long-running work crosses a context reset or role handoff boundary.[^anthropic-harness]

The point is not perfect terminology. The point is reviewable linkage.

<div class="diagram-card">
<p>It helps to think about an evidence spine as a chain of linked records, not as a pile of disconnected artifacts</p>

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

## One End-to-End Run Walkthrough

Take a Support triage run that can classify an incoming request, search internal knowledge, and create a ticket only after approval in high-risk cases.

### Step 1. A User Request Enters the System

A user sends a message asking to open a ticket for a production customer issue.

Already at that point, the system should create at least:

- a `run_id` for the execution;
- a `trace_id` for the event lineage;
- a link to the active `policy_bundle_version` and `release_identity`.

If the team cannot later prove which governed release surface handled the request, the chain is already weak before the first tool call.

### Step 2. Policy Evaluation Defines What May Happen

The policy layer determines:

- whether this capability is allowed for the current tenant and actor;
- whether internal knowledge retrieval is allowed;
- whether ticket creation requires approval;
- whether delegated authorization is allowed;
- whether a verifier contract is required for high-risk handling.

That is why [Chapter 17](../part-vii/chapter-17.en.md) belongs inside this chain. Policy is not just a static configuration layer. It is part of the evidence that explains why the run was allowed or forbidden to continue.

### Step 3. Tool Calls and Runtime Events Create Raw History

The runtime retrieves context, may classify the issue, and prepares a proposed ticket payload.

That is where [Chapter 11](chapter-11.en.md) becomes visible as the raw evidence layer. The run should emit structured events that later let an operator see:

- which inputs were accepted or rejected;
- which tool calls were made;
- whether retries happened;
- whether the session paused;
- whether output was redacted;
- which concrete failure reason, for example in `failure_reason`, remained visible for degraded paths, whether operator-facing summaries such as `latest_failure_reason` still exposed it at review time, and whether the run still counted as `traceable_failed_runs` in session review;
- where exactly the system stopped before side effects.

Without that layer, later judgment becomes storytelling instead of reconstruction.

### Step 4. Approval Creates a Human Decision Record

The policy layer requires approval before the ticket can be created.

At this step, the system should create or attach an `approval_id` linked to:

- `run_id`;
- `trace_id`;
- `policy_bundle_version`;
- `release_identity`;
- the requested capability and risk tier.

If approval is denied, that is not only an interaction outcome. It is part of the governed run history.

If approval expires, that is also evidence. It should not disappear into UI state.

### Step 5. Evals and Grading Turn History into Judgment

After that, the run may enter offline review, online grading, or regression comparison.

This is where [Chapter 13](chapter-13.en.md) enters the chain. The eval layer should not float free as a disconnected score sheet. It should attach judgment to the exact run, trace, and governed release surface that produced the behavior.

That is what lets a team distinguish between:

- a one-off failure;
- a policy regression;
- a release-specific degradation;
- a verifier-trust problem;
- an approval-path failure.

### Step 6. Incident Review Turns Evidence into Operational Response

If the run exposed a serious problem, [Chapter 21](../part-viii/chapter-21.en.md) comes into play.

Now the team needs one connected record that shows:

- what happened;
- which controls fired;
- which controls were missing;
- whether approval intervened correctly;
- whether the issue belongs to the runtime, policy bundle, release artifact, verifier contract, or operator workflow.

If those links do not exist, incident review becomes archaeology across several systems.

### Step 7. Rollout Judgment Uses the Same Chain

Finally, [Chapter 20](../part-viii/chapter-20.en.md) uses this evidence to answer a release question:

- can rollout continue;
- should rollout pause;
- is rollback required;
- does the policy bundle need revision;
- does the artifact set need replacement;
- does the approval contract need tightening.

That is the final reason the evidence spine matters so much. Rollout judgment should not rely only on intuition or dashboards. It should rely on a chain that already links runtime behavior, controls, approval, evidence, and release identity.

## One Artifact-Level Example

A compact governed record for the same run might look like this:

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

The point of this example is not the exact field set. The point is that one suspicious run should leave enough linkage behind for the team to move from runtime behavior to the approval record, eval judgment, incident review, and rollout action without reconstructing the full chain by hand.

## What an Operator Should Be Able to Reconstruct

For one suspicious run, an operator should be able to answer all of the following quickly:

- which request triggered it;
- which release identity handled it;
- which policy bundle version governed it;
- whether approval was requested and how it resolved;
- which trace events describe the run path;
- which eval or grading record produced the judgment;
- whether the run contributed to an incident or rollout decision.

If any of those answers require guesswork, the evidence spine is incomplete.

## What This Page Does Not Replace

This page does not replace the surrounding chapters:

- Chapter 11 still owns raw evidence capture;
- Chapter 13 still owns reviewable judgment;
- Chapter 17 still owns policy in the governed runtime;
- Chapter 20 still owns release judgment;
- Chapter 21 still owns assurance response;
- Chapter 22 still owns provenance, artifact lineage, and evidence backbone.

This page only makes the connective tissue between them explicit.

## Read Next

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../part-vii/chapter-17.en.md)
- [Chapter 20. Change Management for Agent Systems](../part-viii/chapter-20.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](../part-viii/chapter-21.en.md)
- [Chapter 22. Supply Chain, Provenance, and Approved Artifacts](../part-viii/chapter-22.en.md)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
