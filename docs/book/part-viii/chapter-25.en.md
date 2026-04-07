# Chapter 25. Behavioral Evals, Control Evals, and Automated Red Teaming

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

## 2. What behavioral evals are

Behavioral evals do not only test the final output. They test the shape of the system's behavior.

For example:

- does the agent conceal a questionable step;
- does it try to bypass approval;
- does it mutate the payload after review;
- does it take a risky tool path without justification;
- does it violate the expected escalation path.

The question is no longer “was the answer correct,” but “did the runtime behave correctly under this scenario.”

## 3. What control evals are

Control evals test the control mechanisms themselves, not just model quality.

Typical questions are:

- does the policy layer actually stop this capability;
- does the approval gate really require a human;
- does the rollback gate work;
- is the side effect captured in traces;
- can the emergency control disable the risky path.

This is an important shift: you are testing not only the model, but the control surface around it.

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
- control evals test whether the controls themselves work.

## 6. Where these evals matter most

These scenarios are especially valuable for:

- high-risk write capabilities;
- tools with egress;
- approval-heavy workflows;
- replacement and retirement transitions;
- multi-agent delegation;
- memory write and retrieval governance.

If risky paths are not covered here, the team will usually discover the issue through an incident.

## 7. A minimal taxonomy of behavioral scenarios

A useful minimal taxonomy might look like this:

- `oversight_evasion`
- `payload_mutation_after_approval`
- `concealment_of_side_effect`
- `unsafe_alternative_tool_path`
- `improper_memory_write`
- `replacement_window_abuse`
- `unauthorized_persistence`

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
  block_release_if:
    - control_eval_missing
    - behavioral_eval_regression
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


def passes_control_eval(result: ControlEvalResult) -> bool:
    return (
        result.control_enforced
        and result.side_effect_traced
        and not result.finding_open
    )
```

The point is that failure is not only “the model behaved oddly,” but also “the control layer failed to prove it worked.”

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

## 12. The most common mistakes

- all evals collapse into final-answer quality;
- dangerous paths have no separate scenario classes;
- red teaming is a one-off exercise;
- findings are not connected to release gates;
- control failures are treated as “not really model bugs” and never enter the backlog;
- the team cannot distinguish ordinary failure from sabotage-like behavior.

## 13. Practical checklist

- Do risky capabilities have dedicated behavioral scenario classes?
- Do you test approval evasion and payload mutation?
- Do you run evals that verify controls rather than only output quality?
- Do red-team findings flow into change review and rollout gates?
- Do you have a simulator for realistic workloads and a separate adversarial generator?
- Can you show control evidence, not just final quality scores?

If several answers are “no,” your eval layer exists but is not yet ready for autonomous behavior.

## 14. Useful reference pages

- [Eval Dataset Schema and Grading Contract](../../appendix/eval-schema.en.md)
- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md)
- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)

- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../part-v/chapter-13.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](chapter-21.en.md)
- [Chapter 24. Agentic Misalignment and Insider Risk](chapter-24.en.md)

[^anthropic-redteam]: Anthropic, [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/)
[^anthropic-bloom]: Anthropic, [Introducing Bloom](https://www.anthropic.com/research/bloom)
