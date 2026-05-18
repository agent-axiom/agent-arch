# Chapter 23. Retirement, Replacement, and End-of-Life Discipline

## 1. Why a mature agent system must know how to leave the stage

Many teams think about lifecycle like this:

- invent the system;
- build it;
- secure it;
- observe it;
- roll changes out safely.

But every production system has one more mandatory stage: at some point it must be replaced, shut down, or retired.

This matters especially for agent systems because they usually leave behind a long operational tail:

- memory state;
- tool access;
- approvals and audit trails;
- paused-run state and background-run state;
- capability-session state and interruption lineage;
- orchestration-pattern lineage and worker-boundary decisions;
- delegated authorization lineage and revoke state;
- verifier-contract lineage and [evidence-retention obligations](../../appendix/eval-schema.en.md);
- handoff-artifact lineage across context resets and role handoffs;[^anthropic-harness]
- external integrations;
- user expectations;
- dependent workflows.

In other words, retirement is not “delete the service and forget it.” It is a managed operational process.

That is the core promise of this chapter. It should help the reader see retirement not as an appendix to delivery, but as the closure function of the lifecycle: the point where the system loses the right to act, while its memory, evidence, approvals, and operational lineage are brought to a controlled end. The main artifact of this chapter is the retirement plan: a plan for closing rights, state, evidence, and owners, not simply deleting an old agent.

## 2. When to start thinking about retirement

It helps to stop treating retirement as a distant and unpleasant topic.

In practice, common triggers include:

- the runtime or model is obsolete;
- a capability contract is no longer considered safe;
- maintenance cost is too high;
- quality has hit a ceiling and replacement is needed;
- a new platform path is replacing the old one;
- regulatory or governance requirements changed;
- the product problem no longer exists.

If the team has no explicit retirement triggers, old agent systems almost always live longer than is safe or useful.

## 3. Retirement and replacement are not the same thing

It is useful to separate two scenarios:

- `retirement`: the system or capability is simply taken out of service;
- `replacement`: the old system is removed, but only after or alongside a new one taking its place.

That distinction matters.

In retirement, the main question is how to remove the system safely.

In replacement, the main question is how to perform a controlled transition without losing quality, control, or history.

## 4. The biggest risk is leaving the system able to act

One of the ugliest operational mistakes looks like this:

- the team believes the system is “basically off”;
- but it still has:
  - an active tool principal;
  - a live connector;
  - memory access;
  - an old rollout path;
  - a background job;
  - a resumable paused approval path;
  - an expired capability session that can still be re-initialized through an old path;
  - an old runtime-control schema still accepted by gateways.

Formally the system is “dead,” but operationally it can still act.

That is especially dangerous for agents because autonomous and semi-autonomous execution paths are easy to forget.

!!! example "Case thread: the old ticket writer after replacement"
    If support-triage v2 replaces the old path that once created duplicate tickets, retirement must prove that the old `create_support_ticket` path can no longer act. Removing the prompt route is not enough: the team must close the tool principal, revoke gateway exposure, expire paused approvals, stop background retries, and preserve the audit trail so a future duplicate cannot be blamed on an “unknown” old agent.

**Retirement case-spine note:** each canonical case retires a different kind of right to act. Support triage retires deprecated write paths and paused approvals; Internal knowledge assistant retires stale corpora, obsolete embeddings, and memory-write rules; Incident coordination retires emergency-only capabilities, escalation routes, and notification channels once the response path is no longer valid. A retirement plan that only deletes a runtime leaves old authority behind.

## 5. Retirement should happen layer by layer

A good end-of-life process rarely looks like one action. It is usually better to break it down by layer:

- stop new rollout waves;
- disable risky capabilities;
- move write actions to approval-only or disable them;
- stop memory writes;
- expire or cancel paused runs;
- stop background jobs and background routes;
- close or archive capability-session state and block uncontrolled re-init;
- disable deprecated orchestration patterns and revoke worker-safe catalog exposure;
- revoke delegated authorization paths and archive their final lineage;
- retire deprecated verifier contracts and preserve the evidence needed to explain prior rollout or assurance decisions, including exported failed-run fields such as `failure_reason` when they justified earlier judgment;
- archive handoff artifacts that carried sprint scope, evaluator critique, or reset-boundary decisions for long-running work, when those artifacts affected what the retired system was allowed to do;
- revoke egress access;
- close principals, secrets, and connectors;
- record the final audit state.

<div class="diagram-card">
<p>Retirement works best as a stepwise narrowing of the operational surface</p>

``` mermaid
flowchart LR
    A["Freeze rollout"] --> B["Disable risky capabilities"]
    B --> C["Disable writes and background jobs"]
    C --> D["Revoke egress and principals"]
    D --> E["Archive audit and memory state"]
    E --> F["Mark system retired"]
```

</div>

## 6. Memory and audit data need their own discipline

As soon as a system is retired, an uncomfortable question appears: what should happen to accumulated state?

The team usually needs to decide separately:

- what to archive;
- what to delete;
- what to anonymize;
- how long traces and approvals should be kept;
- who remains the owner of archived state;
- whether old datasets and memory artifacts may be reused by the replacement;
- whether delegated authorization records must be retained to explain under whose identity old actions ran;
- whether [verifier evidence](../../appendix/eval-schema.en.md) and verifier-contract history must be retained to explain why earlier releases were judged acceptable.

So retirement affects not only the running system, but also the historical operational footprint.

## 7. Replacement should be staged, not binary

When an old system is replaced by a new one, the temptation is obvious: “cut over and move on.”

For agent systems, that is risky.

Staged replacement is safer:

- shadow comparison;
- limited tenant migration;
- dual-run for critical scenarios;
- side-by-side evals;
- staged traffic shift;
- final cutover only after confidence is high.

This is where replacement resembles rollout discipline, but adds one more question: how to preserve continuity between the old and new systems.

## 8. Old capabilities and patterns should be formally deprecated

It is useful to maintain not only an `approved inventory`, but also a `deprecated inventory`.

For example:

- a deprecated runtime;
- a deprecated prompt-bundle family;
- a deprecated gateway pattern;
- a deprecated memory strategy;
- a deprecated capability contract;
- a deprecated approval schema;
- a deprecated runtime-control schema;
- a deprecated orchestration pattern or worker-boundary policy;
- a deprecated capability-session contract;
- a deprecated verifier contract.

This matters because retirement almost always starts not with a shutdown, but with a clear signal:

“this is no longer considered a normal path.”

## 9. User-facing transition is part of lifecycle too

If the agent system affects a user or internal workflow, end-of-life cannot happen only inside the platform layer.

It helps to decide separately:

- who must be notified;
- which flows will change;
- which expectations must be reset;
- which fallback paths will exist;
- how long old integrations must be supported.

This is especially important for internal agent systems, which quickly become embedded in real team habits.

## 10. Example retirement policy

Here is a practical skeleton:

```yaml
retirement:
  triggers:
    - deprecated_runtime
    - unsafe_capability_pattern
    - maintenance_cost_exceeded
    - replacement_ready
  required_steps:
    - freeze_rollout
    - disable_risky_capabilities
    - stop_memory_write
    - expire_paused_runs
    - stop_background_routes
    - freeze_reinitialization
    - disable_deprecated_patterns
    - revoke_worker_capability_exposure
    - retire_verifier_contracts
    - revoke_egress
    - archive_audit_state
    - set_retired_status
```

This is useful not because YAML solves the problem, but because retirement becomes an explicit operational contract.

## 11. Example replacement readiness check

This sketch shows the right kind of gate:

```python
from dataclasses import dataclass


@dataclass
class ReplacementState:
    shadow_eval_passed: bool
    migration_plan_ready: bool
    risky_capabilities_disabled: bool
    archive_plan_ready: bool
    paused_runs_drained: bool
    capability_sessions_resolved: bool


def ready_for_replacement(state: ReplacementState) -> bool:
    return (
        state.shadow_eval_passed
        and state.migration_plan_ready
        and state.risky_capabilities_disabled
        and state.archive_plan_ready
        and state.paused_runs_drained
        and state.capability_sessions_resolved
    )
```

The point is simple: replacement should have a gate too, not just a mood-driven switch.

## 12. What usually breaks in end-of-life discipline

The problems are fairly repetitive:

- the system is considered retired, but principals are still active;
- background jobs were forgotten;
- the memory write path remained live;
- paused approvals were left resumable after retirement;
- expired capability sessions could still be re-initialized through stale control paths;
- deprecated orchestration patterns or worker-boundary policies remained usable after retirement;
- deprecated verifier contracts or verifier evidence obligations remained unclear after retirement;
- background routes were forgotten;
- archived state belongs to nobody;
- deprecated schemas still remain accepted by gateways or runtimes;
- deprecated patterns remain usable too long;
- replacement happens without dual-run or staged migration.

These small details are exactly what turns an “almost complete” lifecycle into a source of fresh incidents.

## 13. A Fast Maturity Test for End-of-Life Discipline

A team should not think it handles retirement well only because it can switch traffic away and mark a system as deprecated.

A stronger bar is this:

- the system loses the ability to act before it is called retired;
- principals, connectors, memory writes, paused runs, capability sessions, orchestration patterns, and background jobs are narrowed down deliberately;
- replacement is staged rather than treated as a binary cutover;
- deprecated approval and runtime-control schemas are turned off instead of lingering as hidden compatibility paths;
- archived state has an owner and a retention decision;
- deprecated patterns are turned into blocked paths, not only warnings.

If most of those conditions are missing, the team may have shutdown mechanics, but it still does not have real end-of-life discipline.

## 14. Practical checklist

If you want to test your end-of-life discipline quickly, ask:

- Does the system have explicit retirement triggers?
- Can capabilities be disabled step by step, not only all at once?
- Is it clear what happens to memory, traces, approvals, paused-run state, and capability-session state after shutdown?
- Is there a staged replacement plan?
- Can principals, connectors, egress access, paused approvals, capability-session re-init, and background routes be revoked or drained quickly?
- Is it clear who owns archived artifacts and historical state?

If the answer is “no” several times in a row, your lifecycle still ends at release, not at real operations.

## 15. What to read next

This chapter closes Part VIII into a complete operational cycle:

- SDLC to ADLC;
- change management;
- assurance loop;
- artifact governance;
- retirement and replacement.

That means this part can now serve not only as architecture explanation, but also as a lifecycle handbook for production-grade agent systems.

## 16. Useful Reference Pages

- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Reference Package](../../appendix/reference-package.en.md)

- [Chapter 19. From SDLC to ADLC](chapter-19.en.md)
- [Chapter 22. Supply Chain, Provenance, and Approved Artifacts](chapter-22.en.md)
- [Chapter 24. Agentic Misalignment and Insider Risk](chapter-24.en.md)
- [Chapter 27. Agent Inventory, Registry, and Sprawl Control](chapter-27.en.md)
- [Part VIII. Agent System Lifecycle](index.en.md)
- [Sources](../../appendix/sources.en.md)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
