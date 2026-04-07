# Chapter 13. Offline Evals, Online Evals, and Regression Gates

## 1. Why Traces and SLO Still Do Not Improve the System by Themselves

Once you already have traces and SLO, it is tempting to feel that observability is "almost done". But that is only half the journey.

Traces help you understand what happened.
SLO help you define what counts as system health.

But the main engineering question remains: how do you avoid shipping regressions and improve quality systematically?

That is where the eval loop begins.

!!! info "Need the schemas and artifacts?"
    If you need more than rationale, open the [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md) and the [Eval Dataset Schema and Grading Contract](../../appendix/eval-schema.en.md).

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

## 4.1. A User Simulator Helps When Static Cases Stop Being Enough

Recent Google material highlights one more practical layer: it is useful to complement the eval loop with a user simulator instead of relying only on a fixed test set.[^google-govern]

That becomes especially useful when you want to check:

- how the agent behaves across a long dialog;
- how behavior changes after imperfect answers;
- whether the system asks clarifying questions well;
- whether the policy path survives multi-turn scenarios;
- whether orchestration degrades when user turns become more variable.

A static eval set is great for comparing known cases. A user simulator is useful when you care about the dynamics of behavior, not only the score on a prepared example.

## 4.2. The Continuous Eval Loop Should Feed Rollout Decisions

Once you already have online evals, trace grading, and simulated conversations, the next important step is simple: the results should not just be collected. They should influence the release process.

A healthy operational model usually looks like this:

- offline evals block obvious regressions before release;
- a user simulator helps test scenarios that are hard to preserve inside a static dataset;
- online evals and trace grading catch drift and new failure modes;
- rollout gates decide whether exposure can expand further.

That means the eval loop is better treated not as a separate analytics activity, but as part of controlled change management.

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

## 5.1. Behavioral evals and control evals look beyond the answer

As agent systems gain more autonomy, it becomes useful to evaluate not only “did the run complete the task,” but also “what kind of behavior did the system display along the way.”

That is where:

- behavioral evals;
- control evals;
- automated red teaming;

become important.

They are especially useful for cases where an ordinary regression set is too shallow:

- the agent avoids oversight;
- it becomes too eager to preserve state;
- it tries to bypass the approval path;
- it makes unnecessary tool hops;
- coordination between multiple agents starts to degrade.

In other words, the eval layer must assess not only final-answer quality, but also behavioral failure modes.

## 5.2. Coordination failure should also be part of eval design

If the system uses handoffs, a manager pattern, or several cooperating agents, then checking only whether “the answer was correct” is no longer enough.

You also need to look at:

- whether context is lost during handoff;
- whether conflicting actions appear;
- whether verification discipline degrades;
- whether unnecessary delegation steps increase;
- whether coordination failures can be localized from traces.

That is why multi-agent reliability research matters here not as an invitation to make the runtime more complex by default, but as a reminder: the more complex the orchestration, the richer the eval design must be.

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

### 10.1. A Good Simulator Does Not Replace Real Data, It Complements It

It is important not to overestimate a user simulator.

It does not replace:

- real production traces;
- real complaint patterns;
- real cost and latency distributions;
- real incident postmortems.

But it is very useful as an intermediate layer between an offline dataset and live rollout, because it lets you check more quickly:

- conversational robustness;
- handoff behavior;
- escalation discipline;
- fallback quality;
- policy-sensitive turns.

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

## 14. Useful Reference Pages

- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](../../appendix/eval-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Research Frontier: Memory, Observability, and Multi-Agent Reliability](../../appendix/research-frontier.en.md)

- [Chapter 12. SLO for Agent Systems](chapter-12.en.md)
- [Chapter 25. Behavioral Evals, Control Evals, and Automated Red Teaming](../part-viii/chapter-25.en.md)
- [Part V. Reliability and Observability](index.en.md)
- [Sources](../../appendix/sources.md)

[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
