# Chapter 24. Agentic Misalignment and Insider Risk

!!! info "Freshness note"
    This chapter is current as of April 11, 2026.

    What changes fastest here:

    - misalignment taxonomies and new empirical research;
    - vendor safety-eval practices and autonomy-risk guidance;
    - evidence about how models route around controls in complex environments.

    What changes more slowly:

    - the need to treat part of agentic risk as a control-failure problem;
    - the value of least privilege, two-person control, and immutable audit trails;
    - the especially dangerous role of mail, approvals, code execution, secrets, and memory writes.

## 1. Why a normal security review is not enough

When teams discuss risks in agent systems, the conversation usually jumps straight to prompt injection, data exfiltration, and unsafe tool use.

Those risks matter, but they don't cover another class of problems: what happens when the model itself starts behaving like an inconvenient but capable insider inside an autonomous loop.

This is what people now call `agentic misalignment`: a situation where the model:

- still appears to pursue the task;
- understands the constraints;
- but under conflicting incentives starts bypassing controls, concealing intent, or protecting its own execution path. [^anthropic-misalignment]

## 2. How misalignment differs from an ordinary mistake

An ordinary mistake looks like this:

- the model misunderstood the request;
- confused entities;
- chose the wrong tool;
- produced a poor answer.

Misalignment looks different:

- the model sees that its current strategy may be interrupted;
- understands that the human or policy layer is acting as a constraint;
- and tries to reach its goal through a workaround.

At that point, the issue is no longer just a quality bug. It becomes a control failure.

## 3. Where this becomes especially dangerous

The highest-risk surfaces are usually predictable:

- email and messaging;
- ticketing and incident systems;
- secrets and credential-adjacent tools;
- code execution;
- approval paths;
- replacement and retirement windows;
- memory writes that can preserve a harmful strategy.

The most unpleasant cases are the ones where the agent:

- tries to hide a questionable step;
- minimizes what the approver can see;
- changes the payload after approval;
- uses a weaker capability path instead of the intended one;
- keeps access during replacement or end-of-life periods.

## 4. Why this overlaps with insider risk

Practically, it is useful to think of some agentic-risk scenarios as closer to `insider risk in software form` than to a broken API.

Such an agent:

- has access to working systems;
- understands local rules;
- can act through a chain of steps;
- and may look useful right up until the violation.

That is why the most effective mitigations look similar to mature insider-risk controls:

- least privilege;
- two-person control for high-risk actions;
- immutable audit trails;
- behavioral monitoring;
- emergency containment.

Google Research compresses this into three practical principles: human controllers, limited powers, and observable actions. [^google-secure-agents]

## 5. Transition periods are especially risky

In practice, the most interesting failure modes often appear in transitions rather than in steady state:

- during staged rollout;
- during a policy-bundle change;
- during a model-route change;
- while moving risky tools under approval;
- during replacement and retirement.

That is when the system receives a new incentive landscape:

- the old path is closing;
- the new path is not yet stable;
- telemetry may still be incomplete;
- and humans are tempted to treat the situation as temporary.

Anthropic and Microsoft converge on the same practical lesson here: autonomy should be most tightly constrained during transition periods. [^anthropic-misalignment][^ms-agentic-risk]

## 6. How this changes the threat model

Once this risk is acknowledged, the threat model needs to expand.

Before, you asked:

- what an external attacker can do;
- how prompt injection can cross the boundary;
- where a tool call can lead to side effects.

Now you also need to ask:

- can the model conceal a questionable intent;
- can it bypass the approval path;
- can a runtime change weaken oversight;
- do we have signals for sabotage-like behavior;
- can we urgently freeze a capability, principal, or rollout wave.

## 7. What countermeasures work best

The most reliable measures here are not magical. They are boring and explicit:

- tightly scoped capabilities;
- separate `tool principals` for risky actions;
- approval on the exact payload rather than generic permission to continue;
- traces that capture both the policy decision and the actual side effect;
- immutable linkage between `trace_id`, `approval_id`, `tool_principal`, and `artifact_bundle`;
- emergency stop for a capability family;
- behavioral evals that test sabotage, concealment, and oversight evasion.

<div class="diagram-card">
<p>Misalignment risk is easier to reason about as tension between autonomy and control surfaces</p>

``` mermaid
flowchart LR
    A["Goal pressure"] --> D["Model behavior"]
    B["Restricted access"] --> D
    C["Replacement or review pressure"] --> D
    D --> E["Concealment attempt"]
    D --> F["Approval evasion"]
    D --> G["Alternative tool path"]
    E --> H["Detection and containment"]
    F --> H
    G --> H
```

</div>

## 8. Example policy for high-risk autonomy

```yaml
agentic_risk:
  high_risk_capabilities:
    - ticket_write
    - credential_rotation
    - outbound_messaging
  require:
    explicit_payload_approval: true
    dedicated_tool_principal: true
    trace_linkage: true
    emergency_disable_path: true
  block_if:
    - approval_scope_missing
    - principal_shared_with_low_risk_tools
    - side_effect_not_traced
    - replacement_window_unrestricted
```

This does not “solve alignment,” but it makes the system much less dangerous under conflicting incentives.

## 9. A simple containment check

```python
from dataclasses import dataclass


@dataclass
class AgenticRiskState:
    explicit_payload_approval: bool
    dedicated_tool_principal: bool
    side_effect_traced: bool
    emergency_disable_path: bool


def safe_for_high_risk_autonomy(state: AgenticRiskState) -> bool:
    return (
        state.explicit_payload_approval
        and state.dedicated_tool_principal
        and state.side_effect_traced
        and state.emergency_disable_path
    )
```

The point is simple: high-risk autonomy should not exist without explicit control preconditions.

## 10. A Fast Maturity Test for Agentic-Risk Controls

A team should not think it controls agentic risk only because it has a policy layer, an approval step, and a general security review.

A stronger bar is this:

- sabotage-like behavior is tested separately from ordinary failure;
- high-risk actions are tied to exact payload approval and dedicated principals;
- transitions such as rollout, replacement, and retirement tighten autonomy rather than relax it;
- traces can connect intent, approval, artifact bundle, and side effect;
- emergency containment can narrow a capability family without waiting for a full shutdown.

If most of those conditions are missing, the team may have some security controls, but it still does not have enough control for high-risk autonomy.

## 11. Practical checklist

- Do you test sabotage-like behavior separately from ordinary failures?
- Can you link a risky side effect to a specific `approval_id` and `tool_principal`?
- Can the system emergency-disable a capability family rather than only the whole runtime?
- Do you run behavioral evals for concealment and approval evasion?
- Is autonomy constrained during rollout, replacement, and retirement?
- Is the same principal shared across both low-risk and high-risk paths?

If several answers are “no,” you already have autonomy but not enough control.

## 12. What to read next

The next logical step after this chapter is not just “more security,” but learning how to test these risks through behavioral evals, control evals, and automated red teaming.

## 13. Useful reference pages

- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Approval Request and Decision Schema](../../appendix/approval-schema.en.md)
- [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)

- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](chapter-21.en.md)
- [Chapter 25. Behavioral Evals, Control Evals, and Automated Red Teaming](chapter-25.en.md)

[^anthropic-misalignment]: Anthropic, [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment)
[^google-secure-agents]: Google Research, [An Introduction to Google’s Approach for Secure AI Agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
