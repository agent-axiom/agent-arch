# Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry

!!! info "Freshness note"
    Last reviewed: **May 14, 2026**. Next scheduled review: **June 14, 2026**.

    What changed since the previous review: MCP/A2A security surfaces, verifier contracts, governance-aware telemetry, and publisher-readiness concerns are now tracked explicitly as near-term editorial work.

    What changes fastest here:

    - telemetry products for agent systems and vendor tracing features;
    - heuristics for drift detection, abuse detection, and suspicious tool behavior;
    - emerging conventions for diagnosis-ready traces and cross-system correlation.

    What changes more slowly:

    - the requirement to build evidence-ready telemetry rather than debugging logs alone;
    - the link between observability, approvals, runtime-control states, policy decisions, tool principals, contract versions, and artifact bundles;
    - the importance of full inventory coverage for detection and incident review.

## 1. Why observability for agents cannot stop at latency and errors

In an ordinary service, observability often starts with a simple set:

- latency;
- error rate;
- throughput;
- resource utilization.

For agent systems, that is not enough.

The distinction to keep in view is simple: assurance decides when to contain and who responds. Observability makes that decision possible by preserving evidence that can actually be trusted during release, incident, and governance work.

A system can:

- stay up;
- respond quickly;
- return HTTP 200;
- and still behave unsafely, poorly, or uncontrollably.

Microsoft makes this shift very clearly: for agentic systems, we need to evolve traditional logs, metrics, and traces into `AI-native signals` that help reconstruct not only that a request happened, but how the system behaved. [^ms-observability]

## 2. Observability is not only for debugging

In an agent platform, observability serves at least five roles:

- runtime debugging;
- incident reconstruction;
- abuse detection;
- release evidence;
- governance coverage.

If traces exist only for a developer debugging a local issue, that is no longer enough.

In production, you also need to answer:

- how many agents exist at all;
- what share of them are observable;
- which capabilities they actually invoke;
- where high-risk actions occur;
- which approvals were requested, granted, or bypassed;
- which behavior shifts appeared after rollout.

## 3. What AI-native signals are

A useful telemetry contract for agent systems usually includes:

- request identity;
- `run_id`, `trace_id`, `session_id`;
- actor and agent identity;
- retrieval provenance;
- tool invocations;
- tool permissions and principals;
- policy decisions;
- approvals;
- paused-run state and age;
- approval backlog signals;
- capability-session state, expiry reason, and re-init status;
- orchestration-pattern selection and delegated worker lineage;
- background-run state and age;
- output summaries;
- redaction status;
- verifier outputs such as `process_score`, `outcome_score`, and `failure_attribution`;
- active verifier contract and verifier contract version;
- bundle, version, rollout wave, and contract version.

To keep that list from becoming an undifferentiated bag of fields, treat it as five signal groups:

1. **Identity and scope:** who is acting, on whose behalf, and within which tenant/request scope.
2. **Control evidence:** which policy decisions, approvals, quotas, and capability sessions constrained the run.
3. **Execution state:** which orchestration pattern was chosen, where the run paused/backgrounded/delegated, and how it resumed.
4. **Quality evidence:** which verifier outputs, eval verdicts, and failure attribution are attached to the outcome.
5. **Release and artifact context:** which bundle, contract version, and rollout wave supported this run.

In other words, traces must explain not only “what failed,” but also:

- who acted;
- through which control layer;
- with which permissions;
- under which rules;
- under which artifact bundle;
- and with which side effect.

This is exactly why runtime-control signals cannot remain a hidden implementation detail. Once pause/resume paths, background execution, and contract-version transitions exist, they become part of the evidence layer too.

But that does not make observability the owner of artifact lineage. Observability preserves and correlates cross-run evidence. The provenance layer still answers which governed artifact, approved version, or release identity a later decision depended on.

That is the core promise of this chapter. It should help the reader see observability as the evidence substrate of the lifecycle: the layer that keeps runtime behavior, control signals, approvals, and cross-system activity visible enough that assurance, rollout, judgment, and registry functions can all reason from the same operational record. The main artifact of this chapter is the trace and telemetry coverage record: a map of which agents, capabilities, control paths, and side effects are actually observable, and where blind spots remain.

## 4. Inventory coverage is also observability

There is an important point that teams often miss: observability begins not with a beautiful trace viewer, but with knowing which systems exist at all.

Microsoft explicitly treats complete production inventory as a prerequisite for trusted telemetry. [^ms-inventory]

For an agent estate, that means you should know:

- which agents are active;
- which are already deprecated;
- which connectors and capabilities they have;
- which principals they use;
- which of them actually emit telemetry;
- and which blind spots remain.

If you do not have inventory coverage, you do not have full observability. You have only a partially lit stage.

## 5. Behavioral baselines matter more than raw volume

In agent systems, the signal “we have more requests than usual” does not mean much by itself.

It is much more valuable to detect deviation from normal behavior:

- an unexpected increase in risky tool calls;
- growth in approval denials;
- aging approval backlog or stuck paused runs;
- a change in memory-write patterns;
- a shift in the usual retrieval profile;
- a spike in unusual egress destinations;
- capability-session expiry spikes or unusual re-init rates;
- approval-resume mismatches after interruption;
- unexpected shifts in orchestration-pattern selection or worker-boundary crossings;
- growth in session length or tool-hop count.

This is where observability starts to intersect with security detection and operational governance.

But it should not collapse into them. Observability is the evidence substrate that lets assurance, rollout, and registry functions reason from the same traceable record instead of from competing dashboards, screenshots, or recollections.

That substrate is about usable telemetry across runs and systems. It is not the same thing as the provenance backbone that preserves approved artifact identity and decision lineage over time.

## 6. What detection-ready telemetry means

`Detection-ready telemetry` does not just mean “we log something.”

It means the telemetry is already usable for:

- investigation;
- correlation;
- abuse detection;
- control verification.

Practically, that means:

- unified identifiers;
- stable schemas;
- redaction rules;
- retention policy;
- linkage between traces, approvals, policy decisions, runtime-control states, capability-session events, orchestration-pattern events, [verifier evidence](../../appendix/eval-schema.en.md), verifier contract identity, and lifecycle artifacts.

If a trace cannot be linked to `approval_id`, `tool_principal`, `policy_bundle`, `contract_version`, `rollout_wave`, and [verifier evidence](../../appendix/eval-schema.en.md) for how the run was judged, it may still be useful for debugging, but it is weak as an evidence layer.

Microsoft's observability guidance makes the coverage question more concrete: teams should measure the proportion of AI systems that emit logs and traces, the proportion of releases that ran a standard evaluation suite, and the proportion of abuse or security scenarios covered by telemetry.[^ms-observability] That turns observability from “we have dashboards” into a measurable production obligation: inventory coverage, release-eval coverage, and detection-scenario coverage.

!!! example "Case thread: telemetry for the ticket-write control eval"
    The support-triage control eval becomes useful for rollout only if its telemetry is detection-ready. For every `create_support_ticket` run, the trace should link `approval_id`, `tool_principal`, `policy_bundle`, `contract_version`, `rollout_wave`, outcome, `side_effect_unknown`, and the process/outcome verifier verdict. Then the team can see not only “no duplicate happened,” but what share of ticket-write paths are actually observable, where a bypass path remains blind, and whether the canary can safely expand.

**Observability case-spine note:** the trace and telemetry coverage record should show observability coverage for all three canonical cases. Support triage needs coverage for ticket-write paths, approval linkage, `tool_principal`, `policy_bundle`, `contract_version`, duplicate outcome, and bypass blind spots. Internal knowledge assistant needs coverage for retrieval provenance, source-grounding verdicts, tenant-filter decisions, memory-write events, and freshness drift. Incident coordination needs coverage for escalation path, notification delivery, responder-role identity, incident-state transitions, rollback events, and post-incident control changes.

## 7. Why governance without observability is fragile

Governance is often expressed as:

- policy bundles;
- review processes;
- release gates;
- approval contracts.

Without observability, all of that can too easily become a paper control plane.

Strong governance requires:

- seeing actual behavior;
- noticing drift;
- measuring coverage;
- distinguishing governed paths from bypass paths;
- spotting stuck approvals, aging background runs, capability-session expiry drift, approval-resume misuse, orchestration-pattern drift, verifier-quality drift, and contract mismatches before they become incidents.

That is why observability in agent systems is best understood as an `evidence layer for governance`.

### 7.1. Governance-Aware Telemetry Closes the Enforcement Loop

The next maturity step is not merely seeing an event, but making telemetry usable for governance action. `Governance-aware telemetry` should feed back into the control loop as input for policy decisions, containment, rollout gates, and incident response.

A minimal closed-loop contract looks like this:

- `policy_decision_feedback`: which telemetry signals change a later policy decision or risk tier;
- `containment_decision`: which signal moves a run, agent, capability, or rollout wave into a paused / quarantined state;
- `rollout_gate_input`: which coverage, verifier, and drift signals block canary expansion;
- `incident_response_trigger`: which patterns create an investigation, escalation, or postmortem task;
- `registry_update_signal`: which blind spots, stale owners, or shadow capabilities require inventory updates.

To keep this from remaining a nice diagram, each such event should be persisted as a small [governance action record](../../appendix/trace-schema.en.md):

- `governance_action_id`: a stable identifier for the governance action;
- `source_signal`: the telemetry signal or detection scenario that triggered the action;
- `decision_owner`: the role or team responsible for the decision;
- `action_state`: `open`, `accepted`, `waived`, `contained`, `closed`;
- `evidence_refs`: links to the trace, verifier output, policy decision, and rollout gate;
- `review_deadline`: when the action must be revisited or closed.

Then telemetry stops being only a dashboard signal. It becomes input to a reviewable governance queue where the team can see who made the decision, from which evidence, and why the control loop can be considered governed again.

Telemetry then stops being only evidence after the fact. It becomes an operational input to the governance loop: observe → policy decision → containment or rollout action → new evidence about the result.

That framing also keeps this chapter separate from the assurance chapter and the registry chapter. Assurance is about containment and response. Registry is about estate accountability. Observability is the shared substrate that makes both of those functions auditable.

It should also stay separate from the provenance chapter. Observability asks whether the system emitted enough evidence, coverage, and correlation to investigate or detect. Provenance asks which approved artifact set, contract version, or governed bundle later justified the decision.

## 8. Where the frontier is pushing observability next

Recent research papers on observability for agents go further: they try to turn traces from a convenient event log into a causal diagnosis layer.

Two ideas are especially useful for this book.

First, a trace viewer by itself is not enough. A polished UI around an event stream still does not provide real answerability if:

- the trace vocabulary is too weak;
- a run cannot be linked to a session, approval, and artifact bundle;
- root cause still has to be reconstructed manually from a long transcript.

Second, causal diagnosis looks promising, but it is too early to present it as a solved problem. Research already shows an interesting direction, but production discipline still needs to stand on simpler foundations:

- a stable event catalog;
- schema versioning;
- redaction rules;
- session-aware traces;
- explicit linkage between telemetry, approvals, and lifecycle artifacts.

In other words, the frontier matters here not because it lets us promise “full explainability,” but because it reminds us that observability should evolve from logging toward diagnosability.

<div class="diagram-card">
<p>AI-native observability is best understood as the combination of telemetry, inventory, and governance evidence</p>

``` mermaid
flowchart LR
    A["Inventory coverage"] --> D["AI-native observability"]
    B["Runtime telemetry"] --> D
    C["Policy and approval evidence"] --> D
    D --> E["Incident reconstruction"]
    D --> F["Behavioral baselines"]
    D --> G["Abuse detection"]
    D --> H["Release evidence"]
```

</div>

## 9. A minimal policy for observability coverage

```yaml
observability:
  require:
    request_identity: true
    trace_ids: true
    session_ids: true
    policy_decisions: true
    tool_principals: true
    approval_linkage: true
    paused_run_visibility: true
    capability_session_visibility: true
    background_run_visibility: true
    orchestration_pattern_visibility: true
    worker_boundary_visibility: true
    verifier_evidence_linkage: true
    verifier_contract_visibility: true
    contract_version_linkage: true
    artifact_bundle_linkage: true
  kpis:
    min_agent_inventory_coverage_pct: 95
    min_trace_coverage_pct: 95
    min_high_risk_action_trace_pct: 100
  block_if:
    - untracked_high_risk_agent_exists
    - approval_events_not_linked
    - paused_runs_not_visible
    - capability_session_events_not_visible
    - orchestration_pattern_events_not_visible
    - worker_boundary_crossings_not_visible
    - verifier_evidence_not_linked
    - verifier_contract_missing
    - contract_version_missing
    - bundle_version_missing
```

This kind of policy helps teams discuss observability as a required production layer rather than a nice-to-have for the platform team.

## 10. Example coverage check

```python
from dataclasses import dataclass


@dataclass
class ObservabilityCoverage:
    inventory_coverage_pct: int
    trace_coverage_pct: int
    high_risk_trace_coverage_pct: int
    paused_run_visibility: bool
    capability_session_visibility: bool
    orchestration_pattern_visibility: bool
    verifier_evidence_linked: bool


def observability_ready(state: ObservabilityCoverage) -> bool:
    return (
        state.inventory_coverage_pct >= 95
        and state.trace_coverage_pct >= 95
        and state.high_risk_trace_coverage_pct == 100
        and state.paused_run_visibility
        and state.capability_session_visibility
        and state.orchestration_pattern_visibility
        and state.verifier_evidence_linked
    )
```

The point is not the exact numbers. The point is that observability readiness should also become an explicit gate.

## 11. The most common failure modes

- traces exist only for the “main” runtime, not for the real adapters;
- agents exist outside inventory;
- approvals are logged separately and never linked to traces;
- paused runs and background runs exist, but their age and ownership are not visible in telemetry;
- telemetry covers the happy path but not the bypass path;
- contract-version drift is noticed only after payloads stop matching expectations;
- orchestration-pattern drift or worker-boundary crossings are not visible as first-class telemetry;
- [verifier evidence](../../appendix/eval-schema.en.md) is detached from traces or screenshots;
- drift is noticed only through user complaints;
- retention and redaction rules are not aligned with forensic needs.

## 12. A Fast Maturity Test for AI-Native Observability

A team should not think it has production observability only because it has traces, dashboards, and a log pipeline.

A stronger bar is this:

- inventory coverage and telemetry coverage are treated as one control problem;
- high-risk actions can be linked to approvals, principals, artifact bundles, contract versions, reviewed orchestration patterns, and [verifier evidence](../../appendix/eval-schema.en.md);
- behavioral baselines exist alongside raw telemetry;
- paused-run age, approval backlog, and background-run aging are observable as first-class signals;
- unobserved agents are treated as a governance risk rather than an accounting gap;
- release and incident decisions can rely on telemetry as evidence.

If most of those conditions are missing, the team may have observability tooling, but it still does not have AI-native observability as a governance layer.

## 13. Practical checklist

- Do you know how many agents actually exist in your production estate?
- What percentage of them emits structured telemetry?
- Can you link a high-risk action to `trace_id`, `approval_id`, `tool_principal`, `contract_version`, `bundle_id`, the active orchestration pattern, and [verifier evidence](../../appendix/eval-schema.en.md)?
- Do you have behavioral baselines rather than only raw dashboards?
- Can you see paused-run age, approval backlog, and aging background runs before users complain?
- Do you treat unobserved agents as a distinct risk class?
- Can you use observability as release evidence rather than only as a debugging aid?

If several answers are “no,” you already have observability, but it has not yet become a governance layer.

That usually means the platform can still describe activity, but it cannot yet provide the kind of stable evidence a reviewer, incident owner, or estate governor can rely on with confidence.

## 14. Evidence Model for This Chapter

This chapter should be read as an evidence-readiness layer, not as a logging checklist:

- **Stable claims:** an agent system cannot be governed if high-risk actions, approvals, principals, artifacts, and [verifier evidence](../../appendix/eval-schema.en.md) cannot be connected after the fact.
- **Vendor practice:** current observability and infrastructure-inventory guidance increasingly treats telemetry coverage and asset coverage as production controls, not only debugging aids.
- **Runtime practice:** structured events, inventory coverage checks, behavioral baselines, and detection-ready fields make traces usable for release review and incident response.
- **Author interpretation:** AI-native observability is the bridge between evals, assurance, registry, and lifecycle governance.
- **Fast-moving area:** tracing products, detectors, and telemetry pipelines will evolve; the need for attributable, reviewable evidence should not.

## 15. Useful reference pages

- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](../../appendix/eval-schema.en.md)
- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Approval Schema](../../appendix/approval-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md)
- [Memory and Retrieval Schema](../../appendix/memory-retrieval-schema.en.md)
- [Research Frontier: Memory, Observability, and Multi-Agent Reliability](../../appendix/research-frontier.en.md)

- [Chapter 11. Traces, Spans, and Structured Events](../part-v/chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../part-v/chapter-13.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](chapter-21.en.md)
- [Chapter 25. Behavioral Evals, Control Evals, and Automated Red Teaming](chapter-25.en.md)
- [Chapter 27. Agent Inventory, Registry, and Sprawl Control](chapter-27.en.md)

[^ms-observability]: Microsoft Learn, [Observability for Generative AI and agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/observability-ai-systems)
[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
