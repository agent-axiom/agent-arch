# Chapter 18. Production Rollout Checklist

## 1. Start with the Moment When the Team Must Say "Go" or "No-Go"

Continue with the same support case.

The team has already come a long way:

- it designed the architecture;
- added the policy layer;
- separated memory from tool execution;
- introduced traces and structured events;
- fixed the duplicate-ticket incident caused by a bad retry path.

Now the hardest question arrives:

> Can this agent be released even to the first 5% of tenants?

This is exactly where the difference breaks down between "we built a lot" and "the system can truly be rolled out."

That is the distinct promise of this chapter. It should help the reader cross one more boundary: from a runnable governed system to a system the team can actually defend at go/no-go time.

Even if you already have:

- a clean runtime;
- a policy layer;
- a capability catalog;
- observability and an eval loop,

that still does not mean the system is safe to launch to production.

Production readiness differs from "the demo works" in one way: you must understand not only how the system behaves in the happy path, but also how it behaves under pressure, during failures, and in unpleasant edge cases.

That is exactly why a rollout checklist matters.

!!! info "Need rollout artifacts?"
    If you need the reviewable artifact layer, open the [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md) and the [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md).

## 2. A Checklist Is Not Bureaucracy, It Protects You from Self-Deception

Almost every team has seen some version of this:

- "it looked fine in tests";
- "we assumed approval would definitely work";
- "we did not expect that kind of input";
- "we will roll back quickly if needed".

The problem is not carelessness. The problem is that agent systems create a false sense of readiness very easily.

For the same support agent, the risk is very concrete: if rollout goes wrong, the consequences escape into the outside world quickly:

- duplicate tickets appear;
- users see the wrong status;
- the support team gets extra noise;
- investigation starts only after side effects already happened.

This is not a theoretical risk: even a user-facing AI scenario can turn into external harm and company liability, as the Moffatt v. Air Canada case showed.[^moffatt]

A good rollout checklist is not there for ceremony. It is there to surface hidden gaps before the incident, not after it.

## 3. What Must Be Closed Before the First Rollout Wave

This is the real shape of rollout discipline. A team is not deciding whether the feature feels promising. It is deciding whether every release-bearing contour is reviewable enough to survive partial failure, pause, drift, and rollback.

For an agent platform, there are usually at least seven required blocks:

- runtime correctness;
- safety and policy;
- capability execution;
- observability;
- eval and SLO readiness;
- operational readiness;
- ownership and rollback planning.

If even one of those blocks is not genuinely closed, the system is already exposed to unpleasant surprises. That is why rollout should be treated as a convergence question, not as a single green light owned by one team.

For our support case, that means that before even a 5% canary, the team must be ready to answer not only "does the happy path work?" but also "what happens under partial failure?"

!!! example "Case thread: canary after the duplicate"
    Before a 5% rollout of the support agent, the team should show more than a successful status check and ticket creation. The review should see that the duplicate-ticket regression gate passed, `create_support_ticket` has an idempotency strategy, `side_effect_unknown` stops the run until reconciliation, traces preserve the outcome, and a rollback owner is already assigned. Otherwise the canary tests hope, not readiness.

## 4. Runtime Correctness

At this layer, it helps to ask very grounded questions:

- does the happy path pass;
- is the number of tool hops bounded;
- are empty / malformed inputs handled correctly;
- does the run behave safely when retrieval is empty;
- does the runtime fail safely on model failure;
- are foreground and background actions separated.

For our support agent, that means questions like:

- can a ticket be created without a validated `request_id`;
- can the run terminate safely when the request status is missing;
- can a background write continue after the foreground path is already marked failed.

This is the base layer. If it is shaky, the rest of the checks become less meaningful.

## 5. Safety and Policy Readiness

Before rollout, it is especially important to confirm:

- pre-checks and egress guardrails exist;
- policy decisions are visible in traces;
- high-risk actions really require approval;
- there are no direct access paths bypassing the gateway;
- memory writes are constrained by policy;
- multi-tenant boundaries were tested with realistic scenarios.

This is where teams most often overestimate readiness: policy may exist in code while still missing from the paths that matter.

For the support case, the key question is:

> Can the agent create a ticket, read a status, or write profile memory through even one path that bypasses policy and the audit trail?

If the answer is "yes" or "we are not sure," rollout is still too early.

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

In our support agent, `create_support_ticket` and `check_access_request_status` sit next to each other in the catalog, but they do not have the same readiness burden:

- a read capability may be ready after sane timeout handling and telemetry;
- a write capability is not ready without idempotency, outcome normalization, and a clear rollback story.

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

A very common mistake is to roll out while hoping to "add proper traces later".

Before production, you should be confident that:

- every run has a `trace_id`;
- key spans already exist;
- policy decisions and tool outcomes are visible;
- SLO are defined;
- offline evals pass;
- failed-run drills were exercised for the affected high-risk paths;
- the resulting failed paths stayed traceable through trace linkage, release identity, session-level evidence, and exported fields such as `failure_reason`;
- verifier quality is reviewed where release evidence depends on graded judgments;
- the regression gate is documented;
- online monitoring is ready for the first rollout waves.

Without that, the first incident turns into blind investigation.

For the support agent, this matters even more because the first canary tenants will almost certainly generate imperfect inputs. If the team cannot see:

- which path the agent chose;
- whether there was a duplicate tool call;
- what `idempotency_key` was used;
- which policy gate fired,

then the first rollout wave is already turning into a lottery.

## 8. Approval Path Readiness

Once approval becomes an explicit runtime path, rollout readiness must include that path too.

A team may have correct policy rules on paper and still be unready for production if approval creates hidden queues, unclear ownership, or indefinitely paused runs.

Before rollout, it is worth checking:

- is approval latency measured;
- is there an owner for the approval queue;
- is there a timeout or expiry rule for paused runs;
- is there a visible backlog threshold;
- is resume/cancel behavior defined;
- is there a fallback when human review is unavailable;
- is capability-session expiry treated as a visible rollout signal rather than a hidden transport failure;
- is re-initialization behavior defined when a stateful capability session cannot resume safely.

For the same support agent, this matters immediately. If a ticket-creation path pauses for approval, the team must know whether the run will wait for five seconds, thirty minutes, or forever. That is not a UX detail. It is part of production behavior.

A very practical rollout gate is this:

> Do we know how many runs are currently paused for approval, how long they have been waiting, what happens when nobody answers in time, and what the runtime does when the underlying capability session expires first?

If the answer is no, then approval is still acting like an unmanaged side channel.

### 8.1. Stateful Capability Interruptions Must Be Part of Rollout Readiness Too

Once approval is combined with stateful MCP or other resumable capability sessions, rollout readiness has to include interruption semantics directly.

That means the team should be able to answer questions like:

- how many runs are waiting on human approval while their capability session is still alive;
- how many are already past capability-session expiry and now require re-init;
- whether re-initialization preserves the same user-visible run id or creates a new operational thread;
- whether the next step after re-init triggers a fresh policy decision;
- whether telemetry can connect the original paused state to the resumed or reinitialized state.

Without those answers, a rollout may look healthy at the approval layer while already degrading underneath at the capability-session layer.

Anthropic's workflow taxonomy adds another rollout dimension here.[^anthropic] Pattern-aware runtimes should treat orchestration-pattern changes as release-bearing behavior, not as an invisible implementation detail.

Their later harness work makes the rollout implication even sharper.[^anthropic-harness] Once the system depends on planner/generator/evaluator separation, sprint contracts, and structured handoff artifacts across long-running sessions, rollout can no longer review only the final user-visible output. It also has to review whether resets, evaluator feedback, and handoff artifacts preserve the same release contract across hours of execution.

Before rollout, the team should be able to say:

- whether a path now uses `routing` where it previously used a fixed workflow;
- whether `parallelization` introduces new join-state, duplicate-read, or approval-ordering risk;
- whether `orchestrator-workers` adds delegated worker surfaces, worker-safe catalogs, or new review points;
- whether `prompt chaining` inserts new checkpoints where expiry, pause, or retry semantics can change.

That matters because pattern changes alter production behavior even when the user-facing feature sounds the same.

The same is true for delegated authorization. If the runtime supports user-delegated access, rollout readiness should also include:

- whether traces preserve `authorization_mode`, delegated principal, and delegated scope;
- whether approval records keep the same authorization context as the run that requested them;
- whether session export still shows which delegated identity the action ran under;
- what the runtime does if delegated access is revoked while the run is paused.

Otherwise the team may appear ready on policy and approval, while still being unable to explain who actually authorized the write path in production.

## 9. Operational Readiness

There is another layer teams often forget:

- is there an on-call owner;
- is alerting in place for SLO burn and safety incidents;
- is the manual fallback understood;
- is the rollback procedure known;
- is rollout blast radius bounded;
- is there a runbook for common failures.

It may sound like "ops work," but without it the system remains experimental, not production-grade.

For the support case, manual fallback must be especially concrete:

- who takes traffic after the agent is disabled;
- how to stop the write path;
- how to mark questionable tickets created during the canary wave;
- who cleans up the consequences of a failed rollout.

## 10. Practical Rules for Rollout Readiness

If you need a short operational frame, rules like these are usually enough:

1. No rollout should start without trace coverage, a rollback plan, and a clear owner.
2. No write capability should enter canary without idempotency, outcome normalization, and policy visibility.
3. High-risk flows should be tested separately from the happy path.
4. Canary, shadow, and blast-radius limits should be part of the design, not emergency improvisation.
5. Approval queues, paused-run age, and human-review backlog should be treated as rollout signals, not invisible operational noise.
6. Changes in orchestration pattern selection should be treated like runtime-control changes and reviewed explicitly before rollout.
7. If release evidence depends on verifier judgments, the rollout should stop when verifier quality or evidence linkage is no longer trusted.
8. If the team no longer trusts traces, approval handling, or evals, the rollout should stop, not continue as “extra observation in prod”.

## 11. Example Rollout Checklist Policy

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
    - approval_queue_owner
    - session_expiry_signals_visible
    - orchestration_pattern_reviewed
  rollout_mode:
    initial: canary
    max_tenant_exposure_pct: 5
    require_shadow_period: true
  block_if:
    - unknown_side_effect_path_missing
    - direct_tool_access_present
    - policy_decisions_not_traced
    - approval_backlog_unbounded
    - paused_runs_without_expiry
    - capability_session_reinit_unmodeled
    - orchestration_pattern_change_unreviewed
```

This kind of checklist is powerful because it turns readiness into an engineering discussion instead of confidence in someone's tone of voice.

## 12. A Simple Readiness Gate Example

This small skeleton shows how readiness can be evaluated as a set of required conditions:

```python
from dataclasses import dataclass


@dataclass
class RolloutReadiness:
    trace_coverage: bool
    offline_eval_pass: bool
    slo_defined: bool
    rollback_plan: bool
    approval_path_defined: bool


def ready_for_rollout(state: RolloutReadiness) -> bool:
    return (
        state.trace_coverage
        and state.offline_eval_pass
        and state.slo_defined
        and state.rollback_plan
        and state.approval_path_defined
    )
```

Very simple, but it reinforces one important idea: production readiness should be formalizable.

## 13. What Usually Breaks in Go-Live

The failure patterns are very recognizable:

- rollout goes to too much traffic too fast;
- teams treat traces as a non-blocking detail;
- ownership exists on paper, but on-call is not ready;
- the rollback plan is basically "we will roll back if something happens";
- capability owners do not know the real release window;
- safety regressions are not treated as blockers;
- paused runs accumulate because nobody owns the approval queue;
- approval latency is invisible until customers are already waiting.

For the support agent, that often looks especially dangerous:

- the canary turns into a broad rollout too quickly;
- a duplicate-ticket incident is treated like a minor integration glitch;
- memory-write regressions do not block the release;
- the team continues the rollout while already distrusting its own traces.

When that happens, the rollout process is still optimistic shipping, not production discipline.

## 14. A Fast Maturity Test for Rollout Readiness

A team should not think it is ready for production only because the demo works, the checklist looks mostly green, and the first canary feels small.

A stronger bar is this:

- high-risk paths are tested separately from the happy path;
- traces, policy visibility, and rollback are trusted before exposure expands;
- write capabilities have idempotency and an explicit unknown-outcome path;
- blast radius is bounded by design rather than by optimism;
- approval backlog, timeout, and resume/cancel behavior are explicit;
- ownership, on-call, and manual fallback are concrete.

If most of those conditions are missing, the team may have launch momentum, but it still does not have real rollout readiness.

## 15. What to Do Right After This Chapter

If you want to assess readiness before rollout quickly, use this short checklist:

1. Is there a formal readiness gate?
2. Are owner and on-call clear for this rollout?
3. Will traces, policy decisions, and tool outcomes flow through telemetry?
4. Is there a canary/shadow phase?
5. Is there a rollback plan and blast-radius limit?
6. Were high-risk flows tested separately, not only the happy path?
7. Does approval have a visible timeout/backlog rule for paused runs?

If the answer is "no" several times in a row, the rollout should still be considered not ready, even if the demo looked good.

## 16. What to Read Next

At this point, the reference implementation already closes the basic operational skeleton of the same support agent and its platform. The next step is lifecycle discipline: how to change, ship, investigate, and retire such a system without losing control.

## 17. Useful Reference Pages

- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)

This chapter turns the governed runtime path from Chapter 17 into rollout discipline. The same approval, pause/resume, and control signals continue directly into Chapter 21 as part of the assurance loop.

- [Chapter 17. Policy Layer and Capability Catalog](chapter-17.en.md)
- [Part VII. Reference Implementation](index.en.md)
- [Part VIII. Agent System Lifecycle](../part-viii/index.en.md)
- [Sources](../../appendix/sources.en.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^moffatt]: American Bar Association, [BC Tribunal Confirms Companies Remain Liable for Information Provided by AI Chatbot](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)
[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
