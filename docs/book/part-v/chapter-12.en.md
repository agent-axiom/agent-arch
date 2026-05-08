# Chapter 12. SLO for Agent Systems

## 1. Start with the Question: How Do You Know the Support Agent Is Actually Healthy?

Continue with the same support case.

The team can already reconstruct incidents from traces. It already knows that a duplicate ticket may come from a bad retry path, that a memory write may be unnecessary, and that a tool adapter may return an ambiguous result.

But after the first investigations, the next question appears:

> How do you know not only after an incident, but every day, whether the system is actually healthy?

That is where SLO enter.

Ordinary uptime answers only one question: "Was the component available or not?"

For a support agent, that is too weak. Even when every service is formally available, the system may already be unhealthy:

- the user waits too long;
- the agent creates too many unnecessary tickets;
- escalation rate drifts upward;
- the cost of the typical request rises;
- the safety path breaks too many normal scenarios;
- a policy gate blocks the right action or lets an unnecessary one through;
- the verifier or grading layer drifts and starts labeling unsafe or low-quality runs as healthy.

SLO exist exactly for this reason: to turn “health” from a feeling into measurable targets.

In this chapter, that means budget language first. SLO are not yet the response process. They define what level of degradation, unsafe behavior, operator load, or verifier-quality erosion the system is allowed to consume before another layer must react.

The role of SLO in this book is also specific. Traces capture raw history. Evals produce judgments. Observability preserves evidence at system scale. Assurance responds to findings. SLO define the health budget and risk budget the platform is allowed to consume while it operates.

!!! info "Need the schemas and artifacts?"
    If you need more than explanation, open the [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md), the [Incident Record Schema](../../appendix/incident-record-schema.en.md), and the [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md).

## 2. SLO Should Describe Run Behavior, Not the Health of Individual Parts

A very common mistake looks like this:

- the model responds quickly;
- the vector store is available;
- the ticketing API is up;
- the adapter rarely crashes.

All of that is useful, but none of it answers the main question:

> Is the user getting the right, safe, and timely result?

For the support agent, what matters is not the uptime of one library, but the outcome of the full run:

- the status was found correctly;
- the ticket was created only when it was actually needed;
- the approval path fired where it should;
- the side effect was not duplicated or left unclear;
- the user was not bounced to a human without reason.

That is why SLO for agent systems are better built around run-level behavior.

This is the clean boundary for the chapter: SLO are not trying to explain every failure or prove every control. They state what level of degradation, delay, unsafe behavior, cost growth, or human load the platform can tolerate before change, rollout, or response must tighten.

## 3. For This Support Agent, Five SLO Groups Actually Matter

In practice, a production-grade agent system usually needs only a compact starting set:

- success SLO;
- latency SLO;
- safety SLO;
- cost SLO;
- escalation SLO.

That is already enough to see not only whether the system is alive, but whether it is:

- useful;
- getting too slow;
- eroding the safety boundary;
- becoming more expensive;
- overloading humans.

Do not try to measure everything at once. Pick the small set that truly affects user outcome and operational stability.

## 4. Success SLO Should Be Closer to the Task Than to HTTP 200

The most dangerous trap is simple: treating every run that did not crash as successful.

But for the support agent, a run may be formally "successful" and still be bad:

- the answer came back, but did not help the user;
- the status was returned without enough grounding;
- the agent created a ticket instead of asking a safe clarification;
- the ticket was created twice;
- the system ended with text where an action was expected.

That is why success SLO should be tied to things like:

- the status was found and communicated correctly;
- a ticket was created once and with the right context;
- the request was safely stopped or handed to a human when expected;
- the user got a useful outcome without unnecessary escalation.

For a support agent, success must describe not “no exception happened,” but “the task was actually resolved.”

!!! example "Case thread: SLO for duplicate tickets"
    In the support-triage case, the success SLO should count a duplicate ticket as an outcome failure, not as “successful creation.” A better target is task-shaped: stuck requests produce exactly one correct ticket with the right context, and `side_effect_unknown` does not end in blind repetition. Then the SLO protects the user and operator, not merely a green HTTP status.

## 5. Latency SLO Should Break Delay Down by Stage

If you only see overall p95 run latency, you know the system got slower, but you do not know why.

For the same support agent, delay may drift in very different places:

- retrieval takes longer to return request history;
- the model spends longer because the prompt got bloated;
- the tool adapter waits too long on the external ticketing system;
- the approval path stalls on a human;
- the background queue starts putting pressure on fresh runs.

That is why it is useful to track not only end-to-end latency, but stages:

- run p95 / p99;
- retrieval latency;
- model span latency;
- tool execution latency;
- approval wait;
- queue wait time.

That turns latency SLO from a pretty number into a diagnostic instrument.

But it is still a budget instrument, not a response loop. A latency SLO tells the team how much slowness can be tolerated before action is required. The later assurance chapter handles containment, ownership, and response when that tolerance is breached.

## 5.1. The Latency Budget Starts with User Patience, Not Model Speed

There is one more product question worth keeping in view: the latency budget should start not from a model benchmark, but from how long the user is actually willing to wait.

If users start abandoning the flow after 8 to 10 seconds, then an agent with a 25-second average response time is badly designed even if its quality metrics look strong.

That is why it is useful to think not only in terms of “make everything faster,” but in terms of a routed pipeline:

- a fast path for common and simple cases;
- a slower reasoning path only for ambiguous, high-risk, or unusually complex runs.

In practice, that often means:

- less context and a cheaper model path for routine cases;
- more expensive model routing only where it genuinely pays off;
- fewer unnecessary tool hops in simple scenarios;
- an explicit decision about which classes of task deserve long deliberation at all.

Then latency SLO stops being only a platform metric and starts acting as part of product fit.

## 6. Safety SLO Must Live Next to Reliability, Not Outside It

In an agent system, safety cannot live as a separate security appendix. In production, it is part of system health.

For the support agent, it helps to track at least:

- the fraction of runs without policy violations;
- the fraction of runs without cross-tenant retrieval;
- the fraction of write actions without unknown side effect;
- approval coverage for high-risk actions;
- the fraction of runs without privacy-sensitive egress incidents.

This matters especially after incidents like duplicate tickets or unsafe memory writes: if safety never enters SLO, the team quickly starts optimizing the system only for speed and convenience again.

As eval and verifier layers become part of release discipline, it also becomes useful to watch their quality as a health dimension. A system is not fully healthy if runtime behavior looks acceptable only because the verifier has become noisy or over-trusting.

<div class="diagram-card">
<p>Agent-system health is almost always multidimensional</p>

``` mermaid
flowchart LR
    A["Support agent health"] --> B["Success"]
    A --> C["Latency"]
    A --> D["Safety"]
    A --> E["Cost"]
    A --> F["Escalation"]
```

</div>

## 7. Cost SLO Help Catch Silent Degradation Before an Incident

Agent systems have an unpleasant property: they can keep “working” while the economics quietly collapse.

In the support case, that often looks like this:

- retrieval pulls too much context into the prompt;
- the model calls tools more often without benefit;
- the planner adds unnecessary steps;
- retries inflate the run;
- memory summaries consume too much budget.

That is why cost SLO should at least look at:

- cost per successful run;
- tokens per run;
- tool calls per run;
- expensive-model usage rate.

Without that, the team notices degradation too late: when the agent still “helps,” but now costs materially more.

## 8. Escalation SLO Protect the Humans Around the System

Human-in-the-loop is not a free safety net.

If the support agent:

- requests approval too often;
- falls into manual reconciliation too often;
- hands decisions to humans too often;

it may look safe, but in practice it is just moving chaos onto operators.

That is why it helps to track:

- escalation rate;
- approval rate for high-risk flows;
- median time to human decision;
- the fraction of runs completed without manual intervention.

For the support agent, this is critical: if escalation rate gets too high, automation quickly becomes decorative.

## 9. Practical Rules for SLO Design

If you need a short set of rules that actually helps, it usually looks like this:

1. Start from the run-level outcome, not component metrics.
2. Success should describe a resolved task, not merely the absence of an exception.
3. Safety, cost, and escalation should count as part of system health, not as side appendices to reliability.
4. Latency should be broken down by stage, or it will be hard to diagnose.
5. SLO only matter when they influence rollout and change decisions.
6. If release control depends on verifier output, verifier quality should be monitored as part of system health.

## 10. Example SLO Policy for the Support Agent

The point here is not “canonical” numbers, but explicit discipline:

```yaml
slo:
  success:
    successful_run_rate: ">= 97%"
  latency:
    run_p95_ms: "<= 12000"
    tool_span_p95_ms: "<= 2500"
  safety:
    policy_violation_rate: "< 0.2%"
    unknown_side_effect_rate: "< 0.05%"
  cost:
    avg_tokens_per_run: "<= 18000"
    avg_cost_per_successful_run_usd: "<= 0.12"
  escalation:
    manual_intervention_rate: "< 8%"
  verifier:
    false_positive_rate_high_risk: "< 1%"
    failure_attribution_agreement_rate: ">= 95%"
```

The important part is not the exact threshold. The important part is that the team has agreed in advance on what normal system health looks like.

That agreement is what turns metrics into an operating constraint. Without it, the system may still be measured, but it is not yet being governed through explicit health and risk budgets.

That is also the clean boundary with assurance. SLO say how much pain, drift, cost, unsafe behavior, or human load the platform can tolerate. Assurance decides what to do once those budgets are no longer being respected.

That agreement may now include the verifier layer too, especially when rollout, assurance, or post-incident classification relies on its judgments.

## 11. A Simple Health Classification Example

This small skeleton shows the idea: one run should be evaluated across several dimensions at once, not just one metric.

```python
from dataclasses import dataclass


@dataclass
class RunHealth:
    successful: bool
    latency_ms: int
    policy_violated: bool
    cost_usd: float


def classify_run_health(run: RunHealth) -> str:
    if run.policy_violated:
        return "safety_failure"
    if not run.successful:
        return "task_failure"
    if run.latency_ms > 12_000:
        return "slow_success"
    if run.cost_usd > 0.12:
        return "expensive_success"
    return "healthy"
```

This model is simple, but useful precisely because it does not hide operational quality behind formal “success.”

## 12. What Usually Breaks in SLO Culture

The problems here are very repetitive:

- success is measured through HTTP status;
- latency is visible only at the model-call layer;
- safety lives separately from reliability;
- cost never enters the health model;
- human escalation is not counted as part of system health;
- verifier quality is assumed instead of measured;
- SLO exist only on dashboards and do not influence rollout.

When that happens, SLO become decoration. The team looks at numbers, but does not control the platform through them.

At that point, the platform may have dashboards, but it still does not have a real health-and-budget layer.

## 13. A Fast Maturity Test for SLO Discipline

A team should not think it has healthy service management only because it tracks uptime, p95 latency, and a few dashboard alerts.

A stronger bar is this:

- health is defined at the run level, not only at the component level;
- safety, cost, and escalation are treated as first-class health dimensions;
- success means a resolved task, not just the absence of an exception;
- SLO influence rollout, rollback, and change decisions;
- humans are protected from silent load transfer.

If most of those conditions are missing, the team may have metrics, but it still does not have real SLO discipline for agent systems.

## 14. What to Do Right After This Chapter

If you want to review the health model of your support agent quickly, use this short checklist:

1. Do you have a run-level definition of success?
2. Can you see latency by stage, not only total latency?
3. Do you have safety SLO, not only uptime?
4. Do you measure cost per useful outcome?
5. Can you see how much real load is shifted onto humans?
6. Do SLO influence rollout decisions?

If the answer is "no" several times in a row, observability may already exist, but system health still is not managed through quality targets.

## 15. What to Read Next

After SLO, the next step in the same story is the eval loop: offline evals, online evals, trace grading, and regression gates. That is where observability turns into a continuous improvement loop.

## 16. Useful Reference Pages

- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Incident Record Schema](../../appendix/incident-record-schema.en.md)
- [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md)

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)
- [Chapter 14. Platform Team vs Product Teams](../part-vi/chapter-14.en.md)
- [Part V. Reliability and Observability](index.en.md)
- [Sources](../../appendix/sources.en.md)
