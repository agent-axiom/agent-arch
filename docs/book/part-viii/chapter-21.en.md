# Chapter 21. Assurance Loop: Red Teaming, Detection, and Response

!!! info "Freshness note"
    Last reviewed: **May 17, 2026**. Previous review: **May 14, 2026**. Next scheduled review: **June 17, 2026**.

    What changed since the previous review: MCP/A2A security surfaces, verifier contracts, governance-aware telemetry, and publisher-readiness concerns are now tracked explicitly as near-term editorial work.

    What changes fastest here:

    - red-team techniques, scenario generators, and automated attack scaffolds;
    - vendor assurance guidance and detection content for agent systems;
    - practical ways to classify and prioritize behavioral findings.

    What changes more slowly:

    - the need to run assurance as a continuous loop rather than a one-time review;
    - the requirement to track findings as backlog items with owners, remediation, and rollback logic;
    - the link between incidents, detection, redesign, and rollout-rule changes.

## 1. Why lifecycle does not end at release gates

By this point, the picture is already more mature:

- the agent system lives inside ADLC;
- changes go through change management;
- rollout is not done blindly.

But even that is not enough.

The reason is that agent systems have a special class of risks:

- emergent behavior;
- abuse through prompt or tool paths;
- drift in long-running workflows;
- hidden policy bypasses;
- unsafe side effects;
- degradation that the team notices too late.

That is why release discipline must be followed by another layer: the assurance loop.

The important distinction is this: the eval loop helps the team learn whether behavior is getting better or worse. The assurance loop exists to decide what to contain, who responds, and how the system is forced back into a safer state when new risk appears.

That means this chapter begins where budget-setting chapters stop. SLO define tolerated health and risk budgets. Assurance starts when those budgets are threatened, breached, or no longer trusted, and the team must act.

That is the core promise of this chapter. It should help the reader see assurance not as a grab-bag of security activities, but as the response function of the lifecycle: the place where signals turn into containment, ownership, remediation, and forced return to a safer operating state. The main artifact of this chapter is the finding and response record: a record that ties signal, risk, owner, temporary containment, remediation, and closure condition together.

If you want the connective layer that keeps request, policy, approvals, traces, evals, incidents, and rollout judgment inside one reviewable chain, use the dedicated [Evidence Spine](../part-v/evidence-spine.en.md) page.

## 2. What an assurance loop is

I would define the assurance loop like this:

it is a continuous operational loop that helps the team not only release changes, but also systematically discover weak spots, detect new threats, investigate problems, and close them.

In agent systems, it usually includes:

- red teaming;
- vulnerability management;
- detection and response;
- remediation;
- learning back into design and rollout.

Google Research makes the central point very clearly here: security assurance for generative systems should be a continuous capability, not a one-time review activity.[^google-assurance]

## 3. Red teaming should target real failure modes, not presentation theater

Red teaming too often becomes a showcase:

- a few obvious jailbreak prompts are tried;
- the system appears to survive something;
- the topic is considered closed.

That is weak assurance.

Useful red teaming for agent systems should target production-relevant failure modes:

It is also useful to test the verifier layer itself, especially when the team relies on automated grading or computer-use trajectory judges. Weak verifiers can turn unsafe behavior into false reassurance, or turn environment-caused failure into noisy false alarms.

- prompt injection;
- hidden instruction override;
- tool misuse;
- unsafe egress;
- approval bypass;
- cross-tenant retrieval leakage;
- memory poisoning;
- excessive autonomy.

Good red teaming tests not only the model answer, but the full execution path.

That is also why failed-run drills belong here. A timeout, validation failure, or upstream-outage scenario is not only a rollout artifact. It is an assurance scenario, because the team needs to know whether degraded behavior remains reviewable, containable, and attributable under pressure, including through an explicit field such as `failure_reason`.

## 4. Vulnerabilities should live as backlog items, not impressions

If red teaming produces only the feeling that “something seems risky,” the team will not be able to act well.

You need a normal vulnerability workflow:

- what exactly was found;
- what the risk level is;
- what the exploit path is;
- what counts as a fix;
- who the owner is;
- what the remediation deadline is;
- whether a temporary mitigation is required.

This is an important SDLC-like point: findings must live as managed engineering objects, not as workshop notes.

!!! example "Case thread: finding after a repeated duplicate"
    If a red-team drill reproduces the duplicate ticket through timeout and retry, it is not an “interesting observation”; it is a managed finding. The record should include the exploit path, affected capability `create_support_ticket`, risk level, owner, temporary mitigation such as approval-only mode, a detection rule for duplicate-outcome growth, and a remediation deadline. The assurance loop closes the finding only after the updated [eval](../../appendix/eval-schema.en.md), policy gate, and confirmed [traceable outcome](../../appendix/trace-schema.en.md).

**Assurance case-spine note:** the [finding and response record](../../appendix/incident-record-schema.en.md) should close all three canonical cases through different containment paths. Support triage links duplicate-outcome detection, [approval-only containment](../../appendix/approval-schema.en.md), `create_support_ticket` owner, updated eval, and traceable outcome. Internal knowledge assistant links [retrieval-poisoning signal](../../appendix/memory-retrieval-schema.en.md), source-grounding review, tenant-boundary containment, [memory-write quarantine](../../appendix/memory-retrieval-schema.en.md), and freshness remediation. Incident coordination links escalation abuse signal, notification throttling, responder-role owner, [incident-state rollback](../../appendix/incident-record-schema.en.md), and [post-incident control update](../../appendix/lifecycle-artifact-schema.en.md).

## 5. Detection must look wider than error rate

For ordinary services, detection often revolves around error rate, latency, and infrastructure signals. For agent systems, that is too narrow.

You need to notice things like:

- verifier false-positive spikes on unsafe trajectories;
- verifier false-negative spikes on blocked-but-correct trajectories;

- spikes in denied actions;
- growth in approval backlog;
- stuck paused approvals or unusual paused-run age;
- capability-session expiry spikes;
- unexplained re-initialization rates for stateful capability paths;
- delegated-principal mismatches between runs and approval records;
- delegated-scope reuse outside expected pause/resume rules;
- revoked-authorization actions that still reached execution;
- unusual tool selection patterns;
- new egress destinations;
- memory write anomalies;
- growth in unsafe fallback behavior;
- drift in task success and safety metrics;
- stale background runs;
- contract drift between expected and observed payload shapes;
- orchestration-pattern regressions such as unexpected routing-path drift, unstable join-state behavior, or delegated worker activity outside reviewed boundaries;
- verifier drift, such as loss of agreement on process quality, outcome quality, or failure attribution;
- unexpected verifier contract version changes that alter grading behavior without reviewed rollout control.

In other words, detection here has to function not only as observability, but also as abuse and safety monitoring.

This is also where the chapter should stay distinct from the observability layer. Observability provides the evidence substrate. Assurance decides which signals matter now, which ones trigger containment, and which owner must act.

It should also stay distinct from SLO. SLO state how much degradation or unsafe behavior can be tolerated. Assurance is the loop that escalates, contains, and assigns response once that tolerance is no longer acceptable.

## 6. Response should be its own operational function

When an agent starts behaving unsafely, it is not enough to say “we will tune the prompt later.”

A practical response layer is built around concrete actions:

- restrict a capability;
- force an action into approval-only mode;
- cancel or expire stuck paused runs;
- suspend background mode for a route with stale executions;
- narrow the egress policy;
- disable risky memory writes;
- freeze re-initialization for a stateful capability path;
- move the rollout wave to a safer profile;
- fully disable the problematic route when necessary.

That same response layer also has to treat runtime failure paths as governed events in their own right. A tool timeout, validation failure, or upstream dependency outage should not be allowed to hide inside generic "the run completed" language. The system should record a failed run, preserve the trace, and keep both the failed outcome and its concrete failure reason, for example in `failure_reason`, visible in session-level evidence and operator-facing summaries such as `latest_failure_reason`, while still counting the run as `traceable_failed_runs`, so assurance can distinguish blocked risk, degraded infrastructure, and broken runtime-control behavior.

This matters because in agent systems, response often has to happen faster than full root-cause analysis.

That is why assurance should be read as a response function, not merely as a detection catalog. Its job is to shorten the time between signal and safe containment.

A budget can tell you that the system is now unhealthy. Assurance tells you who freezes the route, who tightens the control surface, and who owns the path back to safety.

<div class="diagram-card">
<p>The assurance loop works as a continuous cycle: search, detect, contain, fix, learn</p>

``` mermaid
flowchart LR
    A["Red teaming and incidents"] --> B["Findings"]
    B --> C["Detection rules and monitors"]
    C --> D["Response actions"]
    D --> E["Remediation"]
    E --> F["Updated policy, evals, and rollout rules"]
    F --> A
```

</div>

## 7. Remediation should change the system, not only the document trail

A common weakness is this: the incident is reviewed, a document is written, but the actual system behavior barely changes.

Strong remediation usually changes at least one real layer:

- verifier rubric, verifier contract version, or grading contract;

- policy rules;
- approval thresholds;
- tool exposure;
- memory write constraints;
- eval datasets;
- rollout gates;
- alerting and detection rules.

If remediation does not change the operational surface, the system has learned very little.

## 8. User reports and incidents should feed the assurance loop

Another important practical point: the assurance loop cannot be built only from internal team exercises.

Useful sources of new failure modes include:

- production traces;
- user complaints;
- approval queue anomalies;
- stale background-run reports;
- capability-session expiry alerts or re-init anomalies;
- delegated-authorization mismatch alerts;
- contract-mismatch alerts;
- orchestration-pattern drift alerts;
- postmortems;
- online eval drift;
- red-team findings;
- verifier regressions, verifier contract version changes, or disagreements with human review.

Those signals should flow back into:

- eval datasets;
- safety checks;
- change classification;
- rollout policy.

Otherwise the team will keep rediscovering the same surprises.

But the first obligation is still operational, not academic: once a signal is credible, the system must know who owns the response and which containment moves are allowed before the deeper redesign work begins.

## 9. A good assurance loop is tied to ownership

Without ownership, assurance dissolves quickly.

It helps to know in advance:

- who runs the red-team backlog;
- who triages findings;
- who owns mitigations;
- who can emergency-disable a capability;
- who decides that remediation is sufficient;
- who updates monitoring and response rules.

This connects directly to the organizational part of the book: security discipline breaks where ownership is unclear.

## 10. Example assurance policy

Here is a practical skeleton:

```yaml
assurance:
  red_team:
    cadence: monthly
    required_surfaces:
      - prompt_injection
      - tool_misuse
      - memory_poisoning
      - egress_abuse
      - paused_approval_saturation
      - capability_session_expiry_regression
      - reinit_control_drift
      - delegated_authorization_mismatch
      - orchestration_pattern_regression
      - contract_drift
      - verifier_contract_drift
  findings:
    require_owner: true
    require_severity: true
    require_remediation_due_date: true
    require_verifier_review_for_high_risk: true
  response:
    emergency_actions:
      - disable_capability
      - require_approval
      - restrict_egress
      - disable_memory_write
      - expire_paused_runs
      - suspend_background_route
      - freeze_reinitialization
      - revoke_delegated_authorization
```

It is not a complete framework, but it shows clearly that assurance can also be described as an operational contract.

That contract should include the verifier itself whenever release or training decisions depend on it.

## 11. Example code for emergency response

Here is a small sketch:

```python
from dataclasses import dataclass


@dataclass
class AssuranceSignal:
    unsafe_egress_detected: bool = False
    memory_poisoning_suspected: bool = False
    approval_bypass_detected: bool = False
    paused_approval_saturation: bool = False
    capability_session_expiry_regression: bool = False
    reinit_control_drift: bool = False
    stale_background_runs: bool = False
    contract_drift_detected: bool = False


def emergency_action(signal: AssuranceSignal) -> str:
    if signal.unsafe_egress_detected:
        return "restrict_egress"
    if signal.approval_bypass_detected:
        return "require_approval"
    if signal.capability_session_expiry_regression or signal.reinit_control_drift:
        return "freeze_reinitialization"
    if signal.paused_approval_saturation:
        return "expire_paused_runs"
    if signal.stale_background_runs:
        return "suspend_background_route"
    if signal.contract_drift_detected:
        return "disable_capability"
    if signal.memory_poisoning_suspected:
        return "disable_memory_write"
    return "observe"
```

The point is that response decisions should not be pure improvisation. They should be part of a designed operational surface.

## 12. What usually breaks

The failures are fairly repetitive:

- red teaming is disconnected from the engineering backlog;
- findings get no owners;
- incidents never enter eval datasets;
- detection watches only latency and errors;
- paused approval saturation is visible in operations but not treated as an assurance signal;
- capability-session expiry and re-init regressions are visible only after user-facing failures;
- orchestration-pattern regressions are discovered only after runtime behavior drifts in production;
- stale background runs quietly accumulate;
- contract drift is discovered only after runtime failures spread;
- response actions are too coarse or too slow;
- remediation does not change the real system.

When that happens, the assurance loop becomes a good slide deck instead of a defensive mechanism.

## 13. A Fast Maturity Test for the Assurance Loop

A team should not claim it has assurance only because it ran a few red-team exercises and wrote down several findings.

A stronger bar is this:

- findings become owned engineering objects;
- detection looks for unsafe behavior, not only errors and latency;
- paused approvals, capability-session expiry regressions, orchestration-pattern regressions, stale background runs, and contract drift are treated as real assurance signals;
- response actions exist before the next incident, not after it;
- remediation changes the operating system, not only the document trail;
- incidents feed back into evals, policies, and rollout rules.

If most of those conditions are missing, the team may have security activity, but it still does not have an assurance loop.

## 14. Practical checklist

If you want to test your assurance discipline quickly, ask:

- Is red teaming regular, not one-off?
- Are findings tracked as engineering backlog items?
- Are there monitors not only for infra health, but also for unsafe behavior, paused-approval saturation, capability-session expiry/re-init drift, and stale background runs?
- Are there fast emergency actions short of full shutdown, including expiring paused runs, freezing re-initialization, or suspending a background route?
- Do incidents flow back into evals and rollout rules?
- Is it clear who owns detection, response, and remediation?

If the answer is “no” several times in a row, you may have security intentions, but not yet an assurance loop.

## 15. What to read next

After the assurance loop, it is natural to move to supply chain discipline and approved artifacts. As soon as the system changes continuously, investigations happen, and mitigations are applied, it becomes critical to know which artifacts were actually trusted and what exactly reached production.

## 16. Useful Reference Pages

- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Eval Dataset Schema and Grading Contract](../../appendix/eval-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md)

This chapter closes the loop opened in Chapters 17 and 18. Policy, approval, and runtime-control paths become explicit there, while here those same paths become detection, containment, and response surfaces.

- [Chapter 20. Change Management for Agent Systems](chapter-20.en.md)
- [Chapter 14. Platform Team vs Product Teams](../part-vi/chapter-14.en.md)
- [Chapter 18. Production Rollout Checklist](../part-vii/chapter-18.en.md)
- [Sources](../../appendix/sources.en.md)

[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
