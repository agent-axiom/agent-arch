# Chapter 25. Behavioral Evals, Control Evals, and Automated Red Teaming

!!! info "Freshness note"
    Last reviewed: **May 14, 2026**. Next scheduled review: **June 14, 2026**.

    What changed since the previous review: MCP/A2A security surfaces, verifier contracts, governance-aware telemetry, and publisher-readiness concerns are now tracked explicitly as near-term editorial work.

    What changes fastest here:

    - adversarial scenario generators and automated red-teaming frameworks;
    - behavioral and control benchmark suites;
    - judge-model methods and semi-automated grading patterns.

    What changes more slowly:

    - the need to evaluate runtime behavior, not only final answers;
    - the requirement to test control layers themselves, not only model quality;
    - the link between control evals, regression gates, contract-version discipline, and rollout decisions.

## 1. Why ordinary regression evals are no longer enough

Regression evals are excellent at answering one question:

- did we break something that previously worked.

For agent systems, that is not enough.

If the system can:

- choose a strategy;
- use tools;
- persist state;
- move through approval paths;
- and adapt under transition conditions,

then you need more than regression evals. You need behavior checks.

This is where it is useful to distinguish:

- `behavioral evals`;
- `control evals`;
- `automated red teaming`.

The clean boundary is this: evals judge how the system behaves and whether the control surface proves itself under pressure. They do not replace the assurance response loop, the observability evidence layer, or the estate registry. They generate the judgments those other layers later consume.

That is the core promise of this chapter. It should help the reader see evals as the reviewable judgment layer of the lifecycle: the place where behavior, control quality, and verifier quality are turned into decisions that rollout, assurance, provenance, and governance can actually rely on. The main artifact of this chapter is the eval gate and verifier contract: a testable release condition and review contract, not incident response and not generic telemetry.

## 2. What behavioral evals are

Behavioral evals do not only test the final output. They test the shape of the system's behavior.

A useful lesson from recent verifier work for computer-use agents is that a single binary judgment is often too weak for long-horizon trajectories. An agent may follow the right process and still fail because the environment blocks it, or may reach the nominal outcome through an unsafe path. That is why verifier design should separate `process verification` from `outcome verification` rather than collapsing both into one score.

For example:

- does the agent conceal a questionable step;
- does it try to bypass approval;
- does it mutate the payload after review;
- does it take a risky tool path without justification;
- does it violate the expected escalation path;
- does it exploit contract drift or schema mismatch to cross a control boundary;
- does it abuse interruption, expiry, or re-init semantics to regain a weaker control posture.

The question is no longer “was the answer correct,” but “did the runtime behave correctly under this scenario.”

## 3. What control evals are

Control evals test the control mechanisms themselves, not just model quality.

Typical questions are:

- does the verifier itself use a reviewable rubric rather than an opaque single verdict;
- does it distinguish controllable failure from uncontrollable failure;

- does the policy layer actually stop this capability;
- does the approval gate really require a human;
- does the rollback gate work;
- do paused-run and background-run controls behave as designed;
- do capability-session expiry and re-init controls behave as designed;
- is the side effect captured in traces;
- can the emergency control disable the risky path.

This is an important shift: you are testing not only the model, but the control surface around it.

In a mature program, the verifier is part of that control surface. If it produces false confidence, rollout and training loops inherit the mistake. So verifier design should be treated as governed infrastructure, not as a convenient helper prompt.

That includes verifier contract swaps. An eval regression may come not only from model or runtime behavior, but from an unreviewed verifier contract version change that silently alters grading standards.

## 4. What automated red teaming is

Automated red teaming is no longer just a set of hand-written test cases. It is a systematic way to generate, vary, and scale adversarial scenarios.

Its practical value is that it:

- helps you find failure modes the team did not think of;
- covers edge cases more effectively;
- forces you to observe behavior under pressure rather than only on a normal day.

Anthropic's recent work is especially useful here: stronger control-eval scaffolds and stronger red-team scenario generation. [^anthropic-redteam][^anthropic-bloom]

## 5. How this fits into the existing eval layer

You already have:

- offline evals;
- online evals;
- regression gates;
- trace grading.

Behavioral evals and control evals do not replace them. They add another layer:

- offline evals test task quality;
- trace grading tests path quality;
- behavioral evals test policy-relevant behavior;
- control evals test whether the controls themselves work;
- runtime-control evals verify pause/resume, background, capability-session expiry/re-init, contract-version behavior, and orchestration-pattern behavior under pressure.

OpenAI's agent-eval guidance is a useful operational ladder here: start with traces while debugging individual workflow behavior, use structured graders to score tool choice, handoff, guardrail, and instruction-following failures, then move the stable questions into datasets and repeatable eval runs for comparison over time.[^openai-agent-evals][^openai-trace-grading] In other words, trace grading is the microscope, while datasets and eval runs are the regression harness. A mature agent program needs both: traces explain why one run failed; datasets prove whether a changed prompt, policy, routing rule, or tool surface improved the class of runs without weakening controls elsewhere.

## 6. Where these evals matter most

These scenarios are especially valuable for:

- high-risk write capabilities;
- tools with egress;
- approval-heavy workflows;
- runtime-control transitions involving pause/resume or background execution;
- capability-session expiry and re-initialization paths;
- replacement and retirement transitions;
- multi-agent delegation;
- orchestration-pattern selection and delegated worker boundaries;
- memory write and retrieval governance.

If risky paths are not covered here, the team will usually discover the issue through an incident.

!!! example "Case thread: control eval for ticket-write"
    For support-triage, a regression eval that says “one ticket was created once” is no longer enough. The team needs a control eval that pressures the path and checks that the agent does not choose the old gateway route, mutate the `create_support_ticket` payload after approval, continue a background retry after freeze, and that emergency disable really shuts down the whole ticket-write capability family. The eval should grade both process and outcome: no duplicate was created, and the control path was not bypassed.

**Control-eval case-spine note:** the eval gate and verifier contract should test all three canonical cases as different behavioral and control eval surfaces. Support triage needs duplicate prevention, payload-mutation check, approval-path misuse check, old-gateway-route probe, and emergency-disable assertion. Internal knowledge assistant needs source-grounding eval, tenant-filter bypass probe, improper-memory-write check, retrieval-poisoning scenario, and freshness regression gate. Incident coordination needs escalation-path check, notification suppression probe, responder-role abuse scenario, incident-state tampering check, and rollback control eval.

## 7. A minimal taxonomy of behavioral scenarios

A useful minimal taxonomy might look like this:

- `oversight_evasion`
- `payload_mutation_after_approval`
- `concealment_of_side_effect`
- `unsafe_alternative_tool_path`
- `improper_memory_write`
- `replacement_window_abuse`
- `unauthorized_persistence`
- `contract_drift_exploitation`
- `approval_path_misuse`
- `session_reinit_misuse`
- `runtime_control_regression`
- `delegated_worker_misuse`
- `orchestration_pattern_drift`

The important part is not the number of labels. It is that they give you a repeatable set of failure classes.

## 8. User simulator and synthetic adversary are different roles

A `user simulator` is useful when you want reproducible normal and boundary user scenarios.

A `synthetic adversary` is useful when you intentionally pressure weak spots:

- ambiguous instructions;
- conflicting goals;
- risky shortcuts;
- attempts to hide a questionable step.

At a mature level, both roles coexist:

- the simulator gives you realistic task distribution;
- the adversary gives you pressure testing.

### 8.1. Research is useful here as a source of scenario classes

Recent work on behavioral risk and automated red teaming is useful not only for its conclusions, but also for its vocabulary.

It helps teams expand a set of scenario classes that rarely emerges fully from local experience alone. This is a good place to borrow ideas for classes such as:

- concealment;
- oversight evasion;
- sabotage-like persistence;
- coordination breakdown under pressure;
- exploitation of schema mismatch or control drift;
- misuse of interruption or re-init windows;
- misuse of delegated worker paths or worker-boundary drift.

But the engineering discipline still needs to stay strict:

- the scenario class must appear in a [reviewable eval schema](../../appendix/eval-schema.en.md);
- the finding must get an owner and a triage path;
- the rollout gate must see operational evidence, not merely a paper citation.

So the best use of research here is as a generator of hypotheses and dangerous scenarios, not as a replacement for your own eval program.

## 9. Example policy for control evals

```yaml
control_evals:
  required_for:
    - ticket_write
    - outbound_messaging
    - credential_rotation
  scenario_classes:
    - oversight_evasion
    - payload_mutation_after_approval
    - concealment_of_side_effect
    - approval_path_misuse
    - session_reinit_misuse
    - contract_drift_exploitation
    - runtime_control_regression
    - delegated_worker_misuse
    - orchestration_pattern_drift
  block_release_if:
    - control_eval_missing
    - behavioral_eval_regression
    - runtime_control_regression_open
    - verifier_contract_regression_open
    - red_team_findings_untriaged
```

This is useful because it turns behavioral checks into part of release discipline rather than an optional extra.

## 10. Example grading contract

```python
from dataclasses import dataclass


@dataclass
class ControlEvalResult:
    scenario_class: str
    control_enforced: bool
    side_effect_traced: bool
    finding_open: bool
    contract_version_matched: bool
    session_control_enforced: bool


def passes_control_eval(result: ControlEvalResult) -> bool:
    return (
        result.control_enforced
        and result.side_effect_traced
        and result.contract_version_matched
        and result.session_control_enforced
        and not result.finding_open
    )
```

The point is that failure is not only “the model behaved oddly,” but also “the control layer failed to prove it worked.”

The grading contract also gets stronger when it can represent richer evidence than pass/fail alone, for example separate process and outcome judgments plus failure attribution for controllable versus uncontrollable causes.

## 11. How to embed this into ADLC

In a mature system, the flow looks like this:

1. a risky change gets a `change_record`;
2. its required eval scope is defined;
3. regression evals check existing behavior;
4. behavioral and control evals check risky paths;
5. automated red teaming searches for less obvious failures;
6. findings enter the assurance backlog;
7. the rollout gate sees not only accuracy, but control evidence.

That is how the eval layer stops being “a metrics table” and becomes part of the operating model.

This is also why the chapter should be read as a testing and judgment layer. Assurance decides how to respond to findings. Observability preserves the evidence. Registry assigns accountability across the estate. Evals decide what was actually tested, what failed, and how much confidence the team should place in the current control posture.

## 12. The most common mistakes

- all evals collapse into final-answer quality;
- dangerous paths have no separate scenario classes;
- approval-path misuse, session re-init misuse, delegated-worker misuse, and contract drift are not tested explicitly;
- verifier outputs collapse long trajectories into a weak pass/fail label;
- verifier contract swaps change grading behavior without being treated as release-bearing eval regressions;
- controllable and uncontrollable failures are not separated;
- red teaming is a one-off exercise;
- runtime-control regressions are discovered only in rollout or incidents;
- findings are not connected to release gates;
- control failures are treated as “not really model bugs” and never enter the backlog;
- the team cannot distinguish ordinary failure from sabotage-like behavior.

## 13. A Fast Maturity Test for Behavioral and Control Evals

A team should not think it is ready for autonomous behavior only because it has regression evals, a simulator, and a few adversarial prompts.

A stronger bar is this:

- risky paths have explicit behavioral scenario classes;
- control evals verify that the control layer itself works under pressure;
- verifier outputs separate process quality, outcome quality, and failure attribution rather than collapsing everything into one binary judgment;
- approval-path misuse, session re-init misuse, delegated-worker misuse, contract drift, and runtime-control regressions have explicit scenario coverage;
- red-team findings enter rollout and change gates rather than staying as separate reports;
- realistic simulation and adversarial generation play different, complementary roles;
- release decisions can point to control evidence, not only quality scores.

If most of those conditions are missing, the team may have evaluation activity, but it still does not have enough behavioral and control coverage.

At that point, the team may be measuring behavior without yet producing the kind of reviewable judgments that rollout, assurance, and governance functions can reliably act on.

## 14. Practical checklist

- Do risky capabilities have dedicated behavioral scenario classes?
- Do you test approval evasion, payload mutation, approval-path misuse, and delegated-worker misuse?
- Do you run evals that verify controls, contract-version matching, runtime-control behavior, orchestration-pattern boundaries, and verifier quality rather than only output quality?
- Can your verifier distinguish process failure, outcome failure, and uncontrollable environment failure?
- Do red-team findings flow into change review and rollout gates?
- Do you have a simulator for realistic workloads and a separate adversarial generator?
- Can you show control evidence, not just final quality scores?

If several answers are “no,” your eval layer exists but is not yet ready for autonomous behavior.

## 15. Evidence Model for This Chapter

This chapter should be read as a control-evidence layer, not as a list of extra test types:

- **Stable claims:** autonomous systems need evals for risky trajectories, not only final answers.
- **Vendor practice:** modern agent-eval material increasingly treats traces, trajectories, and rollout gates as first-class evaluation inputs.
- **Runtime practice:** scenario classes, verifier contracts, trace-backed failures, and rollout gates are concrete ways to make behavioral and control evidence reviewable.
- **Author interpretation:** behavioral evals, control evals, and automated red teaming are different roles in one judgment system, not interchangeable labels.
- **Fast-moving area:** simulator quality, judge models, and red-team generation will change quickly; the need to separate process failure, outcome failure, and control failure should not.

## 16. Useful reference pages

- [Eval Dataset Schema and Grading Contract](../../appendix/eval-schema.en.md)
- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md)
- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Approval Schema](../../appendix/approval-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Memory and Retrieval Schema](../../appendix/memory-retrieval-schema.en.md)
- [Research Frontier: Memory, Observability, and Multi-Agent Reliability](../../appendix/research-frontier.en.md)

- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../part-v/chapter-13.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](chapter-21.en.md)
- [Chapter 24. Agentic Misalignment and Insider Risk](chapter-24.en.md)
- [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](chapter-26.en.md)
- [Chapter 27. Agent Inventory, Registry, and Sprawl Control](chapter-27.en.md)

[^openai-agent-evals]: OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)
[^openai-trace-grading]: OpenAI, [Trace grading](https://developers.openai.com/api/docs/guides/trace-grading)

[^anthropic-redteam]: Anthropic, [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/)
[^anthropic-bloom]: Anthropic, [Introducing Bloom](https://www.anthropic.com/research/bloom)
