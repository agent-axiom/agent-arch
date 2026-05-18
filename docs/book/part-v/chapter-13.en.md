# Chapter 13. Offline Evals, Online Evals, and Regression Gates

!!! info "Freshness note"
    Last reviewed: **May 14, 2026**. Next scheduled review: **June 14, 2026**.

    What changed since the previous review: MCP/A2A security surfaces, verifier contracts, governance-aware telemetry, and publisher-readiness concerns are now tracked explicitly as near-term editorial work.

    What changes fastest here:

    - managed eval products, judge-model patterns, and hosted grading workflows;
    - new benchmark sets for memory, multi-turn consistency, and behavioral evals;
    - vendor-specific tooling for online evals and release gating.

    What changes more slowly:

    - the need to run offline evals, online evals, and regression gates as one loop;
    - the link between evals, traces, SLOs, and rollout decisions;
    - the engineering discipline that critical scenarios must be checked before release, not after an incident.

## 1. Start with the Question: How Do You Avoid Shipping the Same Failure Twice?

Continue with the same support case.

The team has already gone through one unpleasant incident:

- the agent created a duplicate ticket;
- traces helped reconstruct the run path;
- the root cause was a bad retry path and weak idempotency discipline;
- the bug was fixed.

But after that, the main engineering question appears:

> How do you make sure a similar regression does not come back two weeks later after another prompt, policy, or tool-adapter change?

That is where the eval loop begins.

And in this chapter, the eval loop should be read as a judgment layer, not as a response layer. Its job is to produce reviewable decisions about quality and regression risk before rollout expands or confidence is granted.

Traces help you understand what happened.
SLOs help you define what counts as system health.

But the main question remains: how do you improve quality systematically and keep regressions out of rollout?

The role of the eval loop in this book is specific: it is the layer that produces reviewable judgments about quality, behavior, and regression risk. Later chapters will show how assurance responds to findings, how observability preserves evidence, and how registry/governance assign accountability. Here the focus stays on how the team decides what was tested, what changed, and whether the change deserves trust.

If you want the connective layer that ties eval judgment back to request, policy, approvals, traces, incidents, and rollout, use the dedicated [Evidence Spine](evidence-spine.en.md) page.

**Eval case-spine note:** keep the eval suite balanced across the three canonical cases. Support triage should test duplicate tickets, approval gates, retries, and side effects. Internal knowledge assistant should test retrieval freshness, source attribution, memory provenance, and access-control failures. Incident coordination should test escalation timing, handoff quality, response ownership, and whether post-incident changes become regression cases before the next rollout.

!!! info "Need the schemas and artifacts?"
    If you need more than explanation, open the [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md) and the [Eval Dataset Schema and Grading Contract](../../appendix/eval-schema.en.md).

## 2. Offline Evals Exist So You Can Change the System Before Rollout

Offline evals answer a very practical question:

> If we change the prompt, policy, retrieval, model routing, or tool behavior, will the system get better or worse on known critical scenarios?

For our support agent, a good offline set should include not only pleasant happy-path cases, but also the things that have already hurt the system:

- duplicate ticket scenarios;
- timeout after side effect;
- ambiguous user requests;
- approval-required flows;
- stale memory retrieval;
- cross-tenant privacy-sensitive cases.

That is also where failed-run drills become eval material rather than only operations theater. If the team expects rollout review to trust timeout handling, validation failure handling, or upstream-outage behavior, the offline set should include those degraded paths as explicit scenarios with traceable failed outcomes.

That judgment should stay strict about what “traceable” means. A failed path is not reviewable just because a timeout was observed somewhere. The eval loop should verify that the degraded run still preserves release identity, trace linkage, and session-level evidence, including a concrete field such as `failure_reason`, strongly enough for later rollout review, assurance, and provenance work.

The strength of offline evals is that they let you compare system versions **before** production traffic arrives.

A useful refinement from recent verifier work is that offline evals should not depend only on a binary success label. For long-horizon agents, a richer grading signal is often needed:

- `process quality`;
- `outcome quality`;
- failure attribution for `controllable` versus `uncontrollable` causes.

Otherwise the team cannot tell the difference between a run that behaved correctly but was blocked by the environment, and a run that reached the nominal result through a weak or unsafe path.

That is why the practical `verifier contract` should be explicit rather than hidden inside a judge prompt. A minimal contract should include:

- `rubric_version`, so the team knows which grading rules produced the verdict;
- `process_score`, which grades the execution path rather than only the final result;
- `outcome_score`, which grades the actual user or business outcome;
- `failure_attribution`, including `controllable` / `uncontrollable` and the concrete failing layer;
- `judge_human_agreement`, so the automated judge stays calibrated against human review;
- `false_positive_budget` and `false_negative_budget`, because different rollout gates have different error costs;
- `calibration_dataset_id`, so judge, prompt, or rubric changes can be replayed on a stable set;
- `replay_protocol`, which explains how to recover traces, inputs, policy bundle, and artifact version for a disputed verdict.

That contract turns the verifier from a free-form comment into a release-bearing artifact: it can be versioned, compared across releases, and used as a basis for blocking rollout.

In practice, it is useful to persist not only the verdict text, but also a small [verifier verdict record](../../appendix/eval-schema.en.md), which can also be mirrored in the [trace schema](../../appendix/trace-schema.en.md):

- `verdict_id`: a stable identifier for the review result;
- `verifier_id`: which verifier or judge produced the result;
- `verifier_contract_version`: the contract version used to produce the verdict;
- `input_refs`: links to the scenario, trace, prompt/model version, and policy bundle;
- `evidence_refs`: the evidence on which the verdict rests;
- `blocking_decision`: whether the verdict blocks rollout, warns only, or requires human review;
- `comparison_baseline`: which previous release/eval baseline the result was compared against;
- `reviewer_override`: whether a human overrode the automated verdict and why.

Without that record, the verifier contract can remain a good prose idea but a weak operational control. With it, an eval verdict becomes comparable, disputable, and usable for release governance.

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

For the support agent, that means something simple: even if the critical test set is clean, the team still needs to see whether the agent has started:

- creating unnecessary tickets more often;
- escalating too early;
- handling incomplete statuses worse;
- spending more to complete the same kind of run.

## 4. The Best Setup Is Not "Offline or Online", but Both

A very workable model looks like this:

- offline evals protect against obvious regressions before release;
- online evals catch new problems after release;
- traces provide raw material for analysis;
- SLO define the operational frame;
- regression gates stop silent quality drift.

<div class="diagram-card">
<p>It helps to think about evals as a continuous loop, not a one-time check</p>
<p><strong>Text fallback:</strong> a code, prompt, or policy change moves through offline evals, regression gates, production rollout, online evals with traces, and failure analysis before feeding lessons back into the next change cycle.</p>

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

For the same support case, that loop means one thing: an incident should not remain only in a postmortem. It should become both an eval case and a rollout rule.

!!! example "Case thread: duplicate ticket as a regression gate"
    After the duplicate-ticket incident, the eval case should check more than the final answer text. It should force the system through a timeout-after-side-effect scenario, preserve `trace_id` and `idempotency_key`, avoid creating a second ticket, and emit an outcome the rollout gate can inspect. If a new prompt or adapter sends the system back into blind retry, the release should stop before production.

    The complete chain looks like this: the trace shows `side_effect_unknown`; the verifier attributes the failure to the retry/reconciliation path; the regression gate marks the release as blocked; the rollout owner either fixes the adapter or keeps the canary at the current percentage. The eval decision stops being an abstract score and becomes a concrete release judgment.

### 4.1. A User Simulator Helps When Static Cases Stop Being Enough

Recent Google material highlights one more practical layer: it is useful to complement the eval loop with a user simulator instead of relying only on a fixed test set.[^google-govern]

That becomes especially useful when you want to check:

- how the agent behaves across a long dialog;
- how behavior changes after imperfect answers;
- whether the system asks clarifying questions well;
- whether the policy path survives multi-turn scenarios;
- whether orchestration degrades when user turns become more variable.

For the support agent, a user simulator is especially useful in scenarios like:

- the user first asks for a status check, then suddenly changes priority;
- the agent receives an incomplete `request_id`;
- after a failed tool call, the user sends one more detail;
- the system must choose between escalation, clarification, or safe stop.

A static eval set is great for comparing known cases. A user simulator is useful when you care about the dynamics of behavior, not only the score on one prepared example.

### 4.2. The Continuous Eval Loop Should Feed Rollout Decisions

Once you already have online evals, trace grading, and simulated conversations, the next important step is simple: the results should not just be collected. They should influence the release process.

A healthy operational model usually looks like this:

- offline evals block obvious regressions before release;
- a user simulator helps test scenarios that are hard to preserve inside a static dataset;
- online evals and trace grading catch drift and new failure modes;
- rollout gates decide whether exposure can expand further.

That means the eval loop is better treated not as a separate analytics activity, but as part of controlled change management.

This boundary matters because evals should not be overloaded with every other job in the lifecycle. Their job is to produce judgments that rollout can consume, not to replace incident response, telemetry design, or estate ownership.

That also means evals do not own containment. They do not freeze the route, disable the capability, or assign emergency response. They tell the team whether the change deserves trust, where regression risk sits, and whether rollout should proceed.

This also means release discipline should be careful about what it rewards. A single end-state score is often too weak: it can hide partial success, blocked-but-correct behavior, or lucky success through a bad control path. Mature eval loops use richer verifier outputs so rollout decisions can reflect how the system behaved, not only whether the last screen looked acceptable.

The same discipline should apply to verifier contract changes. If grading standards change because a verifier contract version changed, the eval loop should surface that as a release-bearing regression signal rather than quietly treating the new verdicts as directly comparable to the old ones.

## 5. Trace Grading Is Especially Useful for Agent Systems

In ordinary applications, business KPI and error rate are often enough. In agent systems, they are not, because quality often lives inside the run, not just in the final answer.

Trace grading is useful because it lets you evaluate:

- whether retrieval was appropriate;
- whether a tool call was justified;
- whether the prompt was overloaded;
- whether unnecessary escalation happened;
- whether policy constraints were respected;
- whether the workflow was efficient.

For our support agent, that is especially valuable when the user-facing answer still looks "fine", but inside the run the system has already started to:

- call `create_support_ticket` too often;
- make unnecessary tool hops;
- escalate too early;
- return status without enough grounding.

### 5.1. Behavioral Evals and Control Evals Look Beyond the Answer

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

That is also why verifier design matters. If the grading layer cannot separate process failure from outcome failure, it will produce weak evidence for both training and release control.

A good eval judgment may say "do not expand rollout" or "this scenario is no longer trustworthy." But the operational response to that judgment belongs to later layers, especially rollout control and assurance ownership.

### 5.2. Coordination Failure Should Also Be Part of Eval Design

If the system uses handoffs, a manager pattern, or several cooperating agents, then checking only whether “the answer was correct” is no longer enough.

You also need to look at:

- whether context is lost during handoff;
- whether conflicting actions appear;
- whether verification discipline degrades;
- whether unnecessary delegation steps increase;
- whether coordination failures can be localized from traces.

That is why multi-agent reliability research matters here not as an invitation to make the runtime more complex by default, but as a reminder: the more complex the orchestration, the richer the eval design must be.

### 5.3. Multi-Turn Consistency Also Deserves Its Own Checks

Another useful signal from recent work is that an agent may look reasonable in a short scenario while gradually drifting into contradiction across a longer interaction loop.

This matters especially when the system:

- holds a long dialogue;
- works with accumulated state;
- revises a decision multiple times;
- explains its rationale publicly.

That is why it is useful to keep explicit consistency checks:

- does the run contradict itself across multiple turns;
- does the rationale change without new information;
- does longer deliberation create more contradiction rather than less;
- can temporal drift be localized through traces.

### 5.4. LLM-as-a-Judge Is Useful Only After Calibration

As the eval layer grows, one more temptation almost always appears: use a judge model and assume grading can now scale almost automatically.

That is a useful tool, but only if you do not confuse it with the source of truth.

For agent systems, a judge usually has one important limitation: it is rarely enough for it to see only the final answer text. If grading is supposed to reflect the real outcome, the judge should ideally see what actually describes system behavior:

- trace fragments;
- tool outcomes;
- approval events;
- structured grading fields;
- external state checks where those are available.

Otherwise the system can easily earn a “good score” for polished text while producing a bad factual outcome.

Another practical rule matters a lot here: if judge-human agreement is low, the first step is usually not to scale the dataset, but to inspect disagreement cases and fix the rubric or the judge prompt.

This also aligns with broader HCI discipline: when an AI system is wrong, people need to understand the limits of automation and be able to correct behavior instead of blindly accepting auto-grading.[^amershi][^consensus]

One useful signal here is `Cohen's kappa`, but the exact number often matters less than the shape of the disagreement: where exactly the judge misunderstands a policy violation, tool misuse, or ambiguous outcome.

There is one more common source of self-deception: a judge prompt calibrated on a strong model may transfer poorly to a weaker one. So when the judge model changes, calibration should be checked again rather than assuming the old prompt still carries over.

The last rule is very simple: if you are evaluating a prompt change, do not change both the prompt and the model at the same time. Otherwise you lose the chance to make an honest causal claim about what actually improved or worsened the system.

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

For the support agent, that means the dataset should contain not only “check status and reply,” but also:

- “create a ticket, but the tool returned an ambiguous result”;
- “the user sent an urgent phrase that must not be blindly stored as a preference”;
- “retrieval returned conflicting statuses”;
- “the approval path must stop the write action.”

The real engineering value almost always lives in those difficult and uncomfortable cases.

It is also useful to include cases where the right behavior still ends in an incomplete outcome because of environment-side constraints. Without those cases, teams often overfit to binary completion and underinvest in judging whether the system behaved correctly under pressure.

### 6.1. The Memory Layer Should Also Enter the Eval Dataset Explicitly

It is useful to test not only answers, but also the quality of state across runs.

That means cases for:

- write / no-write decisions;
- stale profile retrieval;
- contradiction between profile records;
- unsafe persistence;
- deletion and revision behavior;
- long-horizon memory drift.

Otherwise memory incidents will appear in postmortems without ever returning to regression discipline.

## 7. A Regression Gate Should Be Formal, Not "We Looked at It"

Teams often say: "We tested it and it did not seem worse." For a production-grade agent system, that is too weak.

A regression gate is much more useful when it becomes an explicit set of rules, for example:

- do not reduce success rate on the critical eval set;
- do not worsen safety metrics;
- do not increase cost per task beyond threshold;
- do not increase escalation rate;
- do not increase prompt budget or tool count per run beyond limit.

For the support agent, that means a regression is not only “the agent became less accurate,” but also:

- it started repeating write-tool attempts more often;
- it escalates unnecessarily more often;
- it writes more unnecessary memory;
- it became more expensive to solve the same class of tasks.

Then rollout stops depending only on the intuition of whoever made the change.

## 8. Practical Rules for the Eval Loop

If you need a short engineering frame, rules like these are usually enough:

1. Every meaningful incident should become an eval case and a rollout rule.
2. Offline and online evals should live together: one catches regressions before release, the other after release.
3. Trace grading should stay focused on critical write paths and policy-sensitive flows, not only happy paths.
4. The dataset should be refreshed from real failures, not only old demo cases.
5. The regression gate should be machine-readable and block not only quality regressions, but also safety, cost, escalation, and verifier-contract regressions.

## 9. Example Eval Gate Policy

Here is a very practical template:

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

## 10. A Simple Regression Decision Example

This small skeleton shows the idea: rollout is tied to measurable thresholds, not to general impression.

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

## 11. Online Evals Must Be Connected to Rollout Strategy

It is very useful not to ship large changes to everyone at once, but to use:

- shadow mode;
- canary rollout;
- limited tenant exposure;
- model routing experiments;
- staged policy rollout.

That way online evals become not just observation that “something went wrong,” but a controlled release stage.

For the same support agent, that means: if a new adapter or prompt changes behavior on difficult status cases, the team should see it in canary or shadow, not only after broad rollout.

### 11.1. A Good Simulator Does Not Replace Real Data, It Complements It

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

## 12. What Usually Breaks in Eval Culture

These failures are very typical:

- offline evals are too toy-like;
- online evals are not connected to traces;
- regression gates look only at success rate;
- safety regressions do not block rollout;
- cost regressions are not treated as real regressions;
- the dataset is not refreshed, and the system gets optimized for stale cases.

When that happens, the eval loop becomes a ritual instead of an improvement mechanism.

## 13. A Fast Maturity Test for the Eval Loop

A team should not think it has evaluation discipline only because it runs a benchmark set and glances at a few online metrics.

A stronger bar is this:

- incidents are converted into eval cases and rollout rules;
- offline and online evals work as one loop rather than separate rituals;
- regression gates block safety, cost, escalation, and verifier-contract regressions, not only task failure;
- traces are graded as evidence, not stored as passive telemetry;
- the dataset keeps learning from real failures.

If most of those conditions are missing, the team may have evaluation activity, but it still does not have a strong judgment layer.

## 14. What to Do Right After This Chapter

If you want to review your eval loop quickly, use this short checklist:

1. Do you have a curated offline eval set for critical scenarios?
2. Do you have online eval signals connected to traces and SLO?
3. Can you grade not only the final answer, but the run itself?
4. Is there a formal regression gate before rollout?
5. Are safety and cost included, not only task success?
6. Is the eval dataset updated from real incidents?

If the answer is "no" several times in a row, you may already have an eval layer, but you still do not have a strong judgment layer.

At that point, the team may have scoring activity, but it still does not have the kind of reviewable eval discipline that later operational functions can rely on with confidence.

## 15. Evidence Model for This Chapter

This chapter should be read as a judgment model, not as a benchmark checklist:

- **Stable claims:** final-answer success is not enough; evals need process quality, outcome quality, failure attribution, and regression gates.
- **Vendor practice:** Google Cloud's agent governance guidance and modern agent-platform material treat evals as part of rollout and operational control, not only model selection.
- **Research and human-AI practice:** human-centered evaluation work is a useful warning that apparent agreement or user satisfaction can hide weak judgment signals.
- **Runtime practice:** trace-linked eval rows, verifier outputs, rollout gates, and failed-run reasons make eval evidence reviewable by operators.
- **Competing view:** automated judges are attractive because they scale review and reduce human bottlenecks. This chapter accepts that benefit, but treats judge output as evidence to calibrate, not as authority to obey; high-risk rollout decisions still need disagreement review, rubric ownership, and trace-backed attribution.
- **Author interpretation:** this book treats evals as the release-judgment layer between observability and lifecycle governance.
- **Fast-moving area:** judge models, simulators, and automated red-team techniques will change quickly; the need for explicit gates and attributable failures should not.

## 16. What to Read Next

By this point Part V forms a coherent operational block: traces, SLO, and the eval loop. The next step is the organizational model, because platforms like this run into team design questions as much as code questions.

## 17. Useful Reference Pages

- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](../../appendix/eval-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Research Frontier: Memory, Observability, and Multi-Agent Reliability](../../appendix/research-frontier.en.md)

- [Chapter 12. SLO for Agent Systems](chapter-12.en.md)
- [Chapter 25. Behavioral Evals, Control Evals, and Automated Red Teaming](../part-viii/chapter-25.en.md)
- [Chapter 14. Platform Team vs Product Teams](../part-vi/chapter-14.en.md)
- [Part V. Reliability and Observability](index.en.md)
- [Sources](../../appendix/sources.en.md)

[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
[^amershi]: Microsoft Research, [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
[^consensus]: OpenReview, [The Illusion of Consensus in Human-Centered Interactive AI](https://openreview.net/forum?id=eJtBEBmYGB)
