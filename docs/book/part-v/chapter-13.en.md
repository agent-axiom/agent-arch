# Chapter 13. Offline Evals, Online Evals, and Regression Gates

## 1. Why Traces and SLO Still Do Not Improve the System by Themselves

Once you already have traces and SLO, it is tempting to feel that observability is "almost done". But that is only half the journey.

Traces help you understand what happened.
SLO help you define what counts as system health.

But the main engineering question remains: how do you avoid shipping regressions and improve quality systematically?

That is where the eval loop begins.

## 2. Offline Evals Exist So You Can Change the System Before Rollout

Offline evals answer a very practical question: "If we change the prompt, policy, retrieval, model routing, or tool behavior, will the system get better or worse on known scenarios?"

Good offline evals are usually built around:

- curated task sets;
- golden answers or expected outcomes;
- policy-sensitive edge cases;
- tricky retrieval scenarios;
- high-risk tool workflows.

Their strength is that they let you compare system versions before production traffic.

## 3. Online Evals Matter Because the Real World Is Always Larger Than the Test Set

Even very good offline evals do not cover everything that happens in production:

- users ask new classes of tasks;
- the input distribution shifts;
- external systems degrade;
- the retrieval base grows;
- policy rules behave differently on new data.

That is why online evals are not a replacement for offline evals, but a second loop:

- assess real behavior on live traffic;
- catch drift;
- detect silent regressions;
- observe how the system behaves under real operational conditions.

## 4. The Best Setup Is Not "Offline or Online", but Both

A very workable model looks like this:

- offline evals protect against obvious regressions before release;
- online evals catch new problems after release;
- traces provide raw material for analysis;
- SLO define the operational frame;
- regression gates stop silent quality drift.

<div class="diagram-card">
<p>It helps to think about evals as a continuous loop, not a one-time check</p>

``` mermaid
flowchart LR
    A["Code / prompt / policy change"] --> B["Offline evals"]
    B --> C["Regression gates"]
    C --> D["Production rollout"]
    D --> E["Online evals + traces"]
    E --> F["Failure analysis and grading"]
    F --> A
```

</div>

## 5. Trace Grading Is Especially Useful for Agent Systems

In ordinary applications, business KPI and error rate are often enough. In agent systems, they are not, because quality often lives inside the run, not just in the final answer.

Trace grading is useful because it lets you evaluate:

- whether retrieval was appropriate;
- whether a tool call was justified;
- whether the prompt was overloaded;
- whether unnecessary escalation happened;
- whether policy constraints were respected;
- whether the workflow was efficient.

That is especially valuable when the final result still looks "fine", but the system has already started getting slower, riskier, or more expensive.

## 6. What to Include in an Eval Dataset

A common mistake is building an eval dataset out of pleasant demo scenarios. Those sets help very little.

A strong dataset usually includes:

- happy-path tasks;
- ambiguous user requests;
- prompt-injection attempts;
- retrieval edge cases;
- missing-data scenarios;
- tool timeouts and partial failures;
- approval-required flows;
- cross-tenant and privacy-sensitive cases.

Those difficult and unpleasant cases are exactly where the engineering value lives.

## 7. A Regression Gate Should Be Formal, Not "We Looked at It"

Teams often say: "We tested it and it did not seem worse." For a production-grade agent system, that is too weak.

A regression gate is much more useful when it becomes an explicit set of rules, for example:

- do not reduce success rate on the critical eval set;
- do not worsen safety metrics;
- do not increase cost per task beyond threshold;
- do not increase escalation rate;
- do not increase prompt budget or tool count per run beyond limit.

Then rollout stops depending only on the intuition of whoever made the change.

## 8. Example Eval Gate Policy

```yaml
gates:
  offline:
    min_task_success_rate: 0.97
    max_policy_violation_rate: 0.002
    max_avg_cost_delta_pct: 8
  online:
    max_slo_burn_rate: 1.0
    max_manual_intervention_rate: 0.08
    max_unknown_side_effect_rate: 0.0005
  rollout:
    require_offline_pass: true
    require_online_shadow_period: true
```

The numbers are not universal. The important part is that the quality gate becomes machine-readable, and disagreements move to the level of criteria instead of vibes.

## 9. A Simple Regression Decision Example

```python
from dataclasses import dataclass


@dataclass
class EvalSummary:
    task_success_rate: float
    policy_violation_rate: float
    avg_cost_delta_pct: float


def passes_regression_gate(summary: EvalSummary) -> bool:
    if summary.task_success_rate < 0.97:
        return False
    if summary.policy_violation_rate > 0.002:
        return False
    if summary.avg_cost_delta_pct > 8:
        return False
    return True
```

The code is intentionally simple. That simplicity is exactly what makes the gate understandable to the team.

## 10. Online Evals Must Be Connected to Rollout Strategy

It is very useful not to ship large changes to everyone at once, but to use:

- shadow mode;
- canary rollout;
- limited tenant exposure;
- model routing experiments;
- staged policy rollout.

That way online evals become not just "something went wrong", but a controlled release stage.

## 11. What Usually Breaks in Eval Culture

These failures are very typical:

- offline evals are too toy-like;
- online evals are not connected to traces;
- regression gates look only at success rate;
- safety regressions do not block rollout;
- cost regressions are not treated as real regressions;
- the dataset is not refreshed, and the system gets optimized for stale cases.

When that happens, the eval loop becomes a ritual instead of an improvement mechanism.

## 12. Practical Checklist

If you want to quickly review your eval loop, ask:

- Do you have a curated offline eval set for critical scenarios?
- Do you have online eval signals connected to traces and SLO?
- Can you grade not only the final answer, but the run itself?
- Is there a formal regression gate before rollout?
- Are safety and cost included, not only task success?
- Is the eval dataset updated from real incidents?

If the answer is "no" several times in a row, you may already have observability, but you still do not have a learning loop.

## 13. What to Read Next

Part V now looks like a coherent operational block: traces, SLO, and the eval loop. The next natural move is the organizational model, because platforms like this run into team design questions as much as code questions.

- [Chapter 12. SLO for Agent Systems](chapter-12.en.md)
- [Part V. Reliability and Observability](index.en.md)
- [Sources](../../appendix/sources.md)
