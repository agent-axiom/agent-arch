# Chapter 12. SLO for Agent Systems

## 1. Why Ordinary Uptime Is Not Enough for Agents

Once a system becomes agentic, the classic picture of "the service is up or down" stops covering reality.

Even when everything is technically available, an agent system may still be unhealthy:

- runs complete too slowly;
- cost per request drifts upward;
- tool calls fail more often;
- useful-answer rate drops;
- the system escalates to humans too often;
- a policy gate blocks normal scenarios too often.

That is why `99.9% uptime` is almost never enough. You need to measure not only component availability, but the quality of the full run.

## 2. SLO for Agents Should Describe System Behavior, Not Library Health

A common mistake is to take metrics from individual parts and mistake them for the health of the platform.

For example:

- model latency;
- vector store uptime;
- p95 of one API;
- adapter error counts.

All of those are useful, but they do not answer the main question: "Is the user getting a good result in reasonable time and in a safe form?"

That is why SLO for agent systems work better when built around run-level outcomes.

## 3. Which SLO Actually Matter

For a production-grade agent system, at least four groups usually matter:

- success SLO;
- latency SLO;
- safety SLO;
- cost SLO.

Sometimes you also add:

- escalation SLO;
- freshness SLO for retrieval;
- tool success SLO for critical capabilities.

The point is not to measure everything at once. The point is to choose a small set that truly affects user outcome and operational stability.

## 4. Success SLO Should Be Closer to the Task Than to HTTP 200

One of the most dangerous traps is to treat every run that "did not crash" as successful.

But user experience is not about that. A run may:

- complete formally while producing a useless answer;
- avoid exceptions but violate policy;
- return text where an action was expected;
- create a partial side effect and fail to finish the task.

So success SLO should be tied to something like:

- task completed;
- expected artifact produced;
- approved action completed;
- answer accepted without escalation.

That gets much closer to real system quality.

## 5. Latency SLO for Agents Should Be Broken Down by Stage

Overall p95 run latency is useful, but not enough by itself. Without stage-level visibility, you cannot see what actually drifted:

- retrieval;
- model inference;
- tool execution;
- approval wait;
- background queue pressure.

That is why a mature system usually tracks:

- end-to-end run latency;
- p95/p99 model spans;
- tool execution latency;
- queue wait time;
- approval delay, if approval is part of the product.

That turns latency SLO from a pretty number into a diagnostic tool.

## 6. Safety SLO Are Often More Important Than Pure Speed

For agent systems, safety is not only a policy rule. It is also an observable quality target.

Safety SLO may include:

- fraction of runs without policy violations;
- fraction of runs without cross-tenant retrieval;
- fraction of runs without sensitive egress incidents;
- fraction of write actions without unknown side effect;
- approval coverage for high-risk operations.

This is especially important when the team focuses too hard on "faster and cheaper" and starts eroding guardrails without noticing.

<div class="diagram-card">
<p>SLO for agent systems almost always live in several dimensions at once</p>

``` mermaid
flowchart LR
    A["Agent system health"] --> B["Success"]
    A --> C["Latency"]
    A --> D["Safety"]
    A --> E["Cost"]
    A --> F["Escalation"]
```

</div>

## 7. Cost SLO Help Stop Silent Degradation

Agent systems have an unpleasant property: cost can rise quietly without a visible outage.

For example:

- retrieval starts returning too much context;
- the planner adds unnecessary steps;
- the model calls tools more often;
- retries inflate the run;
- memory drags too many summaries into the prompt.

That is why cost SLO should at least look at:

- cost per successful run;
- tokens per run;
- tool calls per run;
- expensive-model usage rate.

Otherwise the system may remain "working" while becoming economically unreasonable.

## 8. Escalation SLO Prevent Overloading Humans

If your system has human-in-the-loop, that is not a free fallback.

A system that:

- requests approval too often;
- falls into manual reconciliation too often;
- asks humans to make decisions too often,

may look safe, but in practice it is just moving chaos onto operators.

That is why it helps to track:

- escalation rate;
- approval rate for high-risk flows;
- median time to human decision;
- fraction of runs completed without manual intervention.

## 9. Example SLO Policy for an Agent Platform

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
```

The exact numbers are not universal. The discipline is what matters: the team should agree on what system health means.

## 10. A Simple Health Classification Example

This small skeleton shows how one run can be evaluated across several dimensions, not just one metric.

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

The idea is simple but useful: a run can be formally successful and still be operationally bad.

## 11. What Usually Breaks in SLO for Agent Systems

The same problems show up again and again:

- success is measured through HTTP status;
- latency is measured only on model calls;
- cost is not part of the health model at all;
- safety is treated separately from reliability;
- human escalation is not considered part of system health;
- SLO exist on dashboards but do not influence rollout.

When that happens, SLO become dashboard decoration instead of a platform control mechanism.

## 12. Practical Checklist

If you want to quickly review your SLO, ask:

- Do you have a run-level definition of success?
- Do you see latency by stage, not only end-to-end?
- Do you have safety SLO, not only availability?
- Do you measure cost per useful outcome?
- Can you see how much load really goes to humans?
- Are rollout decisions tied to SLO instead of intuition alone?

If the answer is "no" several times in a row, the platform may already be observable, but it is not yet managed through quality targets.

## 13. What to Read Next

After SLO, the next natural step is eval loops: offline evals, online evals, trace grading, and regression gates. That is where observability turns into a continuous improvement loop.

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Part V. Reliability and Observability](index.en.md)
- [Sources](../../appendix/sources.md)
