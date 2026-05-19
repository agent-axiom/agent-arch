# Chapter 22. Supply Chain, Provenance, and Approved Artifacts

!!! info "Freshness note"
    Last reviewed: **May 14, 2026**. Next scheduled review: **June 14, 2026**.

    What changed since the previous review: MCP/A2A security surfaces, verifier contracts, governance-aware telemetry, and publisher-readiness concerns are now tracked explicitly as near-term editorial work.

    What changes fastest here:

    - attestation, signing, and provenance tooling for models and configurations;
    - vendor features for artifact governance and managed supply-chain controls;
    - working practices for treating prompt, policy, and eval artifacts as reviewable units.

    What changes more slowly:

    - the need for every approved artifact to have an owner, provenance, and review status;
    - the idea of multiple chains of trust rather than one global chain;
    - the link between supply chain discipline, incident review, change management, and rollout.

## 1. Why the agent supply chain is wider than a normal service supply chain

When engineers hear the words “software supply chain,” they usually think about familiar things:

- package dependencies;
- containers;
- CI/CD artifacts;
- signing and provenance for build outputs.

That is not enough for agent systems.

The problem is that production behavior here depends on more than code. It also depends on:

- model artifacts;
- prompt and routine bundles;
- [policy configs](../../appendix/policy-bundle-schema.en.md);
- [retrieval corpora](../../appendix/memory-retrieval-schema.en.md);
- [capability contracts](../../appendix/lifecycle-artifact-schema.en.md);
- [eval datasets](../../appendix/eval-schema.en.md);
- [approval rules and schemas](../../appendix/approval-schema.en.md);
- [runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md);
- verifier contracts, [grading rules and evidence-linkage rules](../../appendix/eval-schema.en.md);
- [orchestration-pattern governance rules and worker-safe catalog definitions](../../appendix/change-rollout-schema.en.md);
- [capability-session interruption and re-initialization rules](../../appendix/lifecycle-artifact-schema.en.md);
- [rollout bundles](../../appendix/change-rollout-schema.en.md).

In other words, the agent supply chain is wider because the system itself is wider.

## 2. What an approved artifact is in an agent system

It helps to define this very directly:

an [approved artifact](../../appendix/lifecycle-artifact-schema.en.md) is any artifact that is allowed in production because it has an owner, provenance, review status, a clear operational role, and an identifiable place in release identity.

That means approved artifacts are not only images or wheel files. They are the governed objects a later rollout decision, assurance judgment, or incident review must be able to point back to precisely.

In an agent platform, they often include:

- an approved model route;
- an approved prompt bundle;
- an approved [policy bundle](../../appendix/policy-bundle-schema.en.md);
- an approved [capability contract](../../appendix/lifecycle-artifact-schema.en.md);
- an approved [approval schema](../../appendix/approval-schema.en.md);
- an approved [runtime-control schema](../../appendix/lifecycle-artifact-schema.en.md);
- an approved [retrieval corpus](../../appendix/memory-retrieval-schema.en.md);
- an approved [eval dataset](../../appendix/eval-schema.en.md);
- an approved [rollout gate](../../appendix/change-rollout-schema.en.md).

If a team does not have this category, it quickly starts living in an implicit trust system: “this artifact is probably fine because somebody already used it.”

## 3. Provenance is needed to answer very practical questions

Google Research makes the point clearly: provenance for AI systems is not only a formal security idea, but an operational necessity.[^google-supply-chain]

You need to be able to answer:

- where this model came from;
- which prompt bundle is active now;
- which [policy bundle](../../appendix/policy-bundle-schema.en.md) was active during the incident;
- which [retrieval corpus](../../appendix/memory-retrieval-schema.en.md) was used;
- which [eval dataset](../../appendix/eval-schema.en.md) validated the release;
- which [verifier contract](../../appendix/eval-schema.en.md), [grading rubric and evidence-linkage rules](../../appendix/eval-schema.en.md) were active;
- which contract version and [approval schema](../../appendix/approval-schema.en.md) were active;
- which [interruption or expiry policy](../../appendix/lifecycle-artifact-schema.en.md) governed the run;
- which [orchestration pattern and worker-boundary policy](../../appendix/change-rollout-schema.en.md) governed the run;
- which [delegated authorization mode, principal binding, and revoke policy](../../appendix/lifecycle-artifact-schema.en.md) governed the run;
- who approved the change.

!!! example "Case thread: provenance for the duplicate-ticket fix"
    After the duplicate-ticket incident, a later review should be able to reconstruct more than the retry-patch commit. It needs the versions of the [eval dataset](../../appendix/eval-schema.en.md), `side_effect_unknown` [policy bundle](../../appendix/policy-bundle-schema.en.md), `create_support_ticket` [capability contract](../../appendix/lifecycle-artifact-schema.en.md), [rollout gate](../../appendix/change-rollout-schema.en.md), [approval schema](../../appendix/approval-schema.en.md), and [trace schema](../../appendix/trace-schema.en.md) that were active during the canary. If even one of those artifacts lives “somewhere in chat” instead of the [approved release bundle](../../appendix/lifecycle-artifact-schema.en.md), the team cannot prove whether a repeated duplicate happened under the fixed controls or the old rule set.

**Supply-chain case-spine note:** the [approved artifact bundle](../../appendix/lifecycle-artifact-schema.en.md) should preserve provenance for all three canonical cases. Support triage needs the [eval dataset](../../appendix/eval-schema.en.md), [policy bundle](../../appendix/policy-bundle-schema.en.md), [capability contract](../../appendix/lifecycle-artifact-schema.en.md), [approval schema](../../appendix/approval-schema.en.md), [trace schema](../../appendix/trace-schema.en.md), and [rollout gate](../../appendix/change-rollout-schema.en.md) versions for the write path. Internal knowledge assistant needs an [approved retrieval corpus](../../appendix/memory-retrieval-schema.en.md), [source-grounding rubric, tenant-filter config, memory-write policy, and freshness attestation](../../appendix/memory-retrieval-schema.en.md). Incident coordination needs an [escalation-policy bundle, notification contract, and responder-role map](../../appendix/lifecycle-artifact-schema.en.md), [incident-state schema](../../appendix/incident-record-schema.en.md), and [post-incident artifact update](../../appendix/lifecycle-artifact-schema.en.md).

If those questions cannot be answered quickly, change management and incident review start breaking almost immediately.

That is why provenance in this chapter should be read narrowly and concretely. It is not the whole evidence layer. It is the governed lineage layer for approved artifacts, release identity, and decision-bearing versions.

That is the core promise of this chapter. It should help the reader see where evidence stops being generic telemetry and becomes a governed backbone: the layer that preserves which reviewed artifact set, trusted contract version, and approved release identity a later decision or incident review is actually standing on. The main artifact of this chapter is the [approved artifact bundle](../../appendix/lifecycle-artifact-schema.en.md): a reviewed set of versions, contracts, and schemas, not a generic evidence folder.

If you want the bridge that shows how this governed backbone stays connected to request, policy, approvals, traces, evals, incidents, and rollout judgment, use the dedicated [Evidence Spine](../part-v/evidence-spine.en.md) page.

!!! info "Need supply-chain artifacts?"
    For the contract-level view, open the [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md), the [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md), and the [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md).

## 4. An agent needs several chains of trust, not one

In a normal system, a team often thinks in one trust chain: “the code was built in CI, the container is signed, so things are fine.”

For agent systems, it is better to think in several linked chains:

- code and build chain;
- model chain;
- prompt and routine chain;
- policy chain;
- capability chain;
- approval and runtime-control chain;
- capability-session governance chain;
- delegated authorization chain;
- data and retrieval chain;
- eval chain.

<div class="diagram-card">
<p>It is more useful to think in several linked chains of trust, not one</p>

``` mermaid
flowchart LR
    A["Code and build"] --> G["Approved release bundle"]
    B["Model artifacts"] --> G
    C["Prompt and routine bundles"] --> G
    D["Policy bundles"] --> G
    E["Capability contracts"] --> G
    F["Approval and runtime-control schemas"] --> G
    H["Eval datasets and reports"] --> G
```

</div>

## 5. Approved inventory and approved artifacts are not the same

These concepts are related, but not identical.

[approved inventory](../../appendix/registry-operations-handbook.en.md) answers:

- which runtimes, gateways, capabilities, and patterns are allowed on the platform at all.

[approved artifacts](../../appendix/lifecycle-artifact-schema.en.md) answers:

- which exact versions and bundles are approved to run right now.

For example:

- capability `create_ticket` may belong to the approved inventory;
- but `policy_bundle_v12` or `prompt_bundle_support_v7` is an approved artifact.

This distinction is useful because inventory provides the platform-level frame, while approved artifacts provide release-level discipline.

That release-level discipline is the heart of provenance here. The question is not only whether telemetry exists, but which governed version, approved bundle, reviewed schema, or verifier-bearing contract family the system was actually running under.

The same rule matters for failed runs. If a capability timed out, an approval path failed validation, or an upstream dependency collapsed, later reviewers still need to know which approved artifact set and release identity governed that failure, which exported failure field such as `failure_reason` preserved the concrete condition, whether operator-facing summaries still exposed it through fields such as `latest_failure_reason`, and whether the run still counted as `traceable_failed_runs` in session review. Otherwise the organization preserves the happy path as provenance, but treats degraded behavior as unowned residue.

## 6. A prompt bundle without provenance is a supply-chain gap

Teams often treat prompt changes like living text, not like release artifacts.

But if you do not know:

- who changed the prompt;
- which version is in production;
- which evals covered it;
- which rollout wave it is active on;

then that prompt bundle is operationally no better than a build artifact of unknown origin.

The same is true for:

- routines;
- [policy YAML](../../appendix/policy-bundle-schema.en.md);
- [retrieval configs](../../appendix/memory-retrieval-schema.en.md);
- [approval thresholds](../../appendix/approval-schema.en.md);
- [runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md) that define paused/background behavior.

## 7. Eval datasets should also be trusted artifacts

It is easy to treat an [eval dataset](../../appendix/eval-schema.en.md) as secondary: “it is just a set of examples.”

In reality, it is a critical governance artifact.

If it is:

- assembled from unclear sources;
- not versioned;
- without an owner;
- quietly changed between releases;

then the team starts making release decisions on a shaky foundation.

That is why a good ADLC should treat [eval datasets](../../appendix/eval-schema.en.md) as part of the approved artifact model.

The same should increasingly be true for [verifier contracts](../../appendix/eval-schema.en.md). If release or assurance depends on process scores, outcome scores, failure attribution, or linked evidence, then the verifier layer is no longer informal scaffolding. It becomes a governed production artifact.

This matters because a [verifier contract](../../appendix/eval-schema.en.md) does not merely score quality. It also defines what the system will count as acceptable evidence, which failures it can name precisely, and which release claims can be defended later. Once a verifier contract influences release judgment, incident attribution, or assurance status, its lineage becomes part of the evidence backbone rather than an optional eval detail.

## 8. Capability contracts and egress rules are part of the supply chain too

In an agent system, a tool contract is not just documentation. It is part of the trusted operational surface.

For a capability, the team should know:

- who the owner is;
- what the risk tier is;
- which tool principal is used;
- what the network access profile is;
- which egress destinations are allowed;
- which approval semantics apply.

If the contract changes quietly, without provenance or review trail, that change can be as dangerous as an unreviewed code deploy.

The same is true for [approval schemas](../../appendix/approval-schema.en.md) and [runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md). If a team changes timeout, pause/resume behavior, expiry semantics, re-initialization rules, or expected payload structure without governed artifact discipline, it is changing production behavior even if no model or source file moved.

That means provenance should increasingly preserve not only that a runtime-control schema existed, but also which interruption-governance version was active:

- whether paused runs expired or waited indefinitely;
- whether capability-session re-init was allowed, denied, or approval-bound;
- whether telemetry was expected to link the original and reinitialized capability sessions;
- which [orchestration pattern](../../appendix/change-rollout-schema.en.md) was approved for the path, and whether worker-safe catalog boundaries were in force;
- whether approval and session-control logic were governed under one contract version or had already drifted apart;
- whether delegated access was platform-owned or user-delegated;
- which principal-binding rule and revoke behavior governed in-flight or paused actions.

Anthropic's later harness work makes another supply-chain consequence explicit.[^anthropic-harness] If long-running work depends on context resets, planner/generator/evaluator separation, sprint contracts, and structured handoff artifacts, then those handoff artifacts are not disposable coordination notes. They become provenance-bearing artifacts too. A later incident review or rollout challenge may need to know which handoff artifact carried scope, which evaluator critique shaped the next sprint, and which reset boundary changed the active context without changing the user-visible run.

Those are provenance questions because they determine the governed identity of the behavior, not merely whether the behavior was visible in telemetry.

That is exactly where this chapter's boundary matters. Telemetry may show that a pause, re-init, or delegated action happened. Provenance has to preserve which reviewed contract family made that behavior legitimate in the first place. Without that layer, incident review can see events but still fail to explain why the platform considered them valid.

## 9. Example approved artifact policy

Here is a practical skeleton:

```yaml
artifacts:
  require_owner: true
  require_version: true
  require_provenance: true
  require_review_status: true
  types:
    - model_route
    - prompt_bundle
    - policy_bundle
    - capability_contract
    - approval_schema
    - runtime_control_schema
    - capability_session_contract
    - verifier_contract
    - eval_dataset
    - retrieval_source
```

This helps move the conversation from “it seems like a valid config” to “this is a real production artifact.”

## 10. Example approved inventory policy

Here is a more platform-level example:

```yaml
inventory:
  approved_runtimes:
    - agent_runtime_v3
  approved_gateways:
    - shared_tool_gateway
    - approval_gateway
  approved_patterns:
    - staged_rollout
    - approval_required_for_high_risk
    - governed_background_mode
    - reviewed_routing
    - bounded_parallelization
    - worker_safe_orchestrator_workers
  deprecated_patterns:
    - direct_prod_tool_access
    - unversioned_prompt_override
```

This inventory matters not because it “looks organized,” but because it gives the platform an explicit map of trusted and untrusted operational patterns.

## 11. Example artifact readiness check

Here is a small sketch:

```python
from dataclasses import dataclass


@dataclass
class ArtifactRecord:
    has_owner: bool
    has_version: bool
    has_provenance: bool
    review_passed: bool
    schema_linked: bool


def artifact_ready(record: ArtifactRecord) -> bool:
    return (
        record.has_owner
        and record.has_version
        and record.has_provenance
        and record.review_passed
        and record.schema_linked
    )
```

The point is simple: trusted artifacts should be defined by explicit properties, not intuition. If the platform cannot test artifact readiness explicitly, it will eventually fall back to social trust, stale defaults, and weak release identity.

## 12. What usually breaks in artifact discipline

The usual problems look like this:

- prompt bundles are not versioned;
- [eval datasets](../../appendix/eval-schema.en.md) change quietly;
- [capability contracts](../../appendix/lifecycle-artifact-schema.en.md) are edited without review trail;
- [approval schemas](../../appendix/approval-schema.en.md) or [runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md) change without version discipline;
- [orchestration-pattern governance changes](../../appendix/change-rollout-schema.en.md) have no artifact lineage;
- nobody knows which exact artifact was active during an incident;
- [contract-version linkage](../../appendix/trace-schema.en.md) is missing from [incident evidence](../../appendix/incident-record-schema.en.md);
- [verifier-contract lineage](../../appendix/eval-schema.en.md) is missing from release or assurance evidence;
- [deprecated patterns](../../appendix/lifecycle-artifact-schema.en.md) remain in production too long;
- [approved inventory](../../appendix/registry-operations-handbook.en.md) exists in a wiki, but not in operational tooling.

When this happens, the platform loses controllability not because of one giant error, but because of hundreds of small untracked artifacts.

## 13. A Fast Maturity Test for Artifact Governance

A team should not think it has supply-chain discipline only because builds are signed and a few configs are stored in version control.

A stronger bar is this:

- prompt, [policy](../../appendix/policy-bundle-schema.en.md), [eval](../../appendix/eval-schema.en.md), [capability](../../appendix/lifecycle-artifact-schema.en.md), [approval](../../appendix/approval-schema.en.md), [runtime-control](../../appendix/lifecycle-artifact-schema.en.md), and [verifier](../../appendix/eval-schema.en.md) artifacts are treated as production artifacts;
- provenance can be restored quickly during incident review and rollout decisions;
- release and assurance evidence can be traced back to the active [verifier contract](../../appendix/eval-schema.en.md) and contract family;
- [approved inventory](../../appendix/registry-operations-handbook.en.md) and [approved artifacts](../../appendix/lifecycle-artifact-schema.en.md) are kept as distinct control layers;
- [deprecated patterns](../../appendix/lifecycle-artifact-schema.en.md) can be blocked before they quietly persist in production;
- trust is attached to explicit artifact properties, not inherited socially.

If most of those conditions are missing, the team may have some artifact hygiene, but it still does not have real artifact governance.

## 14. Practical checklist

If you want to test your artifact discipline quickly, ask:

- Do all [production artifacts](../../appendix/lifecycle-artifact-schema.en.md) have owners?
- Do model, prompt, [policy](../../appendix/policy-bundle-schema.en.md), [approval-schema](../../appendix/approval-schema.en.md), [runtime-control](../../appendix/lifecycle-artifact-schema.en.md), [eval, and verifier](../../appendix/eval-schema.en.md) artifacts have versions?
- Can provenance, [verifier lineage](../../appendix/eval-schema.en.md), and [active contract/schema versions](../../appendix/trace-schema.en.md) be restored quickly during incident review?
- Does the platform have an [approved inventory](../../appendix/registry-operations-handbook.en.md)?
- Do you distinguish a [platform-approved pattern](../../appendix/change-rollout-schema.en.md) from a [release-approved artifact](../../appendix/lifecycle-artifact-schema.en.md)?
- Can a [deprecated artifact](../../appendix/lifecycle-artifact-schema.en.md) be blocked quickly?

If the answer is “no” several times in a row, you do not yet have a real artifact governance layer.

## 15. What to read next

After supply chain and artifact discipline, the natural final operational topic in this part is retirement, replacement, and end-of-life discipline. A mature system must not only launch and recover, but also leave the stage cleanly.

## 16. Useful Reference Pages

- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Approval Schema](../../appendix/approval-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md)
- [Eval Dataset Schema and Grading Contract](../../appendix/eval-schema.en.md)
- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Memory and Retrieval Schema](../../appendix/memory-retrieval-schema.en.md)
- [Reference Package](../../appendix/reference-package.en.md)

- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](chapter-21.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../part-vii/chapter-17.en.md)
- [Chapter 18. Production Rollout Checklist](../part-vii/chapter-18.en.md)
- [Sources](../../appendix/sources.en.md)

[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
