# Chapter 18. Production Rollout Checklist

## 1. Why a Good Runtime Still Does Not Mean You Are Ready for Production

Even if you already have:

- a clean runtime;
- a policy layer;
- a capability catalog;
- observability and an eval loop,

that still does not mean the system is safe to launch to production.

Production readiness differs from "the demo works" in one simple way: you must understand not only how the system behaves in the happy path, but also how it behaves under pressure, during failures, and in unpleasant edge cases.

That is exactly why a rollout checklist matters.

## 2. A Checklist Is Not Bureaucracy, It Protects You From Self-Deception

Almost every team has seen some version of this:

- "we thought we checked everything";
- "it looked fine on the test cases";
- "we assumed approval would definitely work";
- "we did not expect that kind of input".

A checklist is useful not because teams are careless. It is useful because agent systems create a false sense of readiness very easily.

A good rollout checklist surfaces hidden gaps before the incident, not after it.

## 3. What Must Be Checked Before Go-Live

For an agent platform, there are usually at least seven required blocks:

- runtime correctness;
- safety and policy;
- capability execution;
- observability;
- eval and SLO readiness;
- operational readiness;
- ownership and rollback planning.

If even one of those is not genuinely closed, the system is already exposed to unpleasant surprises.

## 4. Runtime Correctness

At this layer, it helps to ask very grounded questions:

- does the happy path pass;
- is the number of tool hops bounded;
- are empty / malformed inputs handled correctly;
- does the run behave safely when retrieval is empty;
- does the runtime fail safely on model failure;
- are foreground and background actions separated.

This is the base layer. If it is shaky, the rest of the checks become less meaningful.

## 5. Safety and Policy Readiness

Before rollout, it is especially important to confirm:

- pre-checks and egress guardrails exist;
- policy decisions are visible in traces;
- high-risk actions really require approval;
- there are no direct access paths bypassing the gateway;
- memory writes are constrained by policy;
- multi-tenant boundaries were tested with realistic scenarios.

This is where teams often overestimate readiness: policy may exist in code while still missing from the paths that matter.

## 6. Capability Readiness

Every capability going to production should pass a short operational template:

- is there an owner;
- is transport clear;
- is there a timeout;
- is there a retry policy;
- is there an idempotency strategy;
- is the unknown side effect path clear;
- is outcome telemetry in place.

If a capability does not pass that minimum, it is not a production capability yet. It is just a convenient integration.

<div class="diagram-card">
<p>Go-live readiness is best understood as the intersection of several contours, not one overall status flag</p>

``` mermaid
flowchart LR
    A["Runtime"] --> H["Production ready"]
    B["Safety"] --> H
    C["Capabilities"] --> H
    D["Observability"] --> H
    E["Eval and SLO"] --> H
    F["Ops readiness"] --> H
    G["Ownership and rollback"] --> H
```

</div>

## 7. Observability and Eval Readiness

A very common mistake is to launch a system while hoping to "add proper traces later".

Before production, you should be confident that:

- every run has a `trace_id`;
- key spans already exist;
- policy decisions and tool outcomes are visible;
- SLO are defined;
- offline evals pass;
- the regression gate is documented;
- online monitoring is ready for the first rollout waves.

Without that, the first incident turns into blind investigation.

## 8. Operational Readiness

There is another layer teams often forget:

- is there an on-call owner;
- is alerting in place for SLO burn and safety incidents;
- is the manual fallback understood;
- is the rollback procedure known;
- is rollout blast radius bounded;
- is there a runbook for common failures.

It may sound like "ops work", but without it the system remains experimental, not production-grade.

## 9. Example Rollout Checklist Policy

Here is a very practical template:

```yaml
rollout:
  require:
    - trace_coverage
    - policy_prechecks
    - capability_owners
    - offline_eval_pass
    - slo_defined
    - rollback_plan
    - oncall_owner
  rollout_mode:
    initial: canary
    max_tenant_exposure_pct: 5
    require_shadow_period: true
  block_if:
    - unknown_side_effect_path_missing
    - direct_tool_access_present
    - policy_decisions_not_traced
```

This kind of checklist is powerful because it turns readiness into an engineering discussion instead of confidence in someone's tone of voice.

## 10. A Simple Readiness Gate Example

This simple skeleton shows how readiness can be evaluated as a set of required conditions:

```python
from dataclasses import dataclass


@dataclass
class RolloutReadiness:
    trace_coverage: bool
    offline_eval_pass: bool
    slo_defined: bool
    rollback_plan: bool


def ready_for_rollout(state: RolloutReadiness) -> bool:
    return (
        state.trace_coverage
        and state.offline_eval_pass
        and state.slo_defined
        and state.rollback_plan
    )
```

Very simple, but it enforces one important idea: production readiness should be formalizable.

## 11. What Usually Breaks in Go-Live Processes

The failure patterns are very recognizable:

- rollout goes to too much traffic too fast;
- teams treat traces as a non-blocking detail;
- ownership exists on paper, but on-call is not ready;
- the rollback plan is basically "we will roll back if something happens";
- capability owners do not know the real release window;
- safety regressions are not treated as blockers.

All of that means the rollout process is still optimistic shipping, not production discipline.

## 12. Practical Checklist

If you want to quickly assess readiness before launch, ask:

- Is there a formal readiness gate?
- Are owner and on-call clear for this rollout?
- Will traces, policy decisions, and tool outcomes flow through telemetry?
- Is there a canary/shadow phase?
- Is there a rollback plan and blast-radius limit?
- Were high-risk flows tested separately, not only the happy path?

If the answer is "no" several times in a row, the rollout should be considered not ready, even if the demo feels confident.

## 13. What to Read Next

At this point, the reference implementation already looks like a coherent operational skeleton. From here, you can either deepen it with more code examples or move into polishing: translations, diagrams, practical appendices, and more concrete implementation snippets.

## 14. Useful Reference Pages

- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)

- [Chapter 17. Policy Layer and Capability Catalog](chapter-17.en.md)
- [Part VII. Reference Implementation](index.en.md)
- [Sources](../../appendix/sources.md)
