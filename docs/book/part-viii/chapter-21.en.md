# Chapter 21. Assurance Loop: Red Teaming, Detection, and Response

## 1. Why lifecycle does not end at release gates

By this point, the picture is already more mature:

- the agent system lives inside ADLC;
- changes go through change management;
- rollout is not done blindly.

But even that is not enough.

The reason is that agent systems have a special class of risks:

- emergent behavior;
- abuse through prompt or tool paths;
- drift in long-running workflows;
- hidden policy bypasses;
- unsafe side effects;
- degradation that the team notices too late.

That is why release discipline must be followed by another layer: the assurance loop.

## 2. What an assurance loop is

I would define the assurance loop like this:

it is a continuous operational loop that helps the team not only release changes, but also systematically discover weak spots, detect new threats, investigate problems, and close them.

In agent systems, it usually includes:

- red teaming;
- vulnerability management;
- detection and response;
- remediation;
- learning back into design and rollout.

Google Research makes the central point very clearly here: security assurance for generative systems should be a continuous capability, not a one-time review activity.[^google-assurance]

## 3. Red teaming should target real failure modes, not presentation theater

Red teaming too often becomes a showcase:

- a few obvious jailbreak prompts are tried;
- the system appears to survive something;
- the topic is considered closed.

That is weak assurance.

Useful red teaming for agent systems should target production-relevant failure modes:

- prompt injection;
- hidden instruction override;
- tool misuse;
- unsafe egress;
- approval bypass;
- cross-tenant retrieval leakage;
- memory poisoning;
- excessive autonomy.

Good red teaming tests not only the model answer, but the full execution path.

## 4. Vulnerabilities should live as backlog items, not impressions

If red teaming produces only the feeling that “something seems risky,” the team will not be able to act well.

You need a normal vulnerability workflow:

- what exactly was found;
- what the risk level is;
- what the exploit path is;
- what counts as a fix;
- who the owner is;
- what the remediation deadline is;
- whether a temporary mitigation is required.

This is an important SDLC-like point: findings must live as managed engineering objects, not as workshop notes.

## 5. Detection must look wider than error rate

For ordinary services, detection often revolves around error rate, latency, and infrastructure signals. For agent systems, that is too narrow.

You need to notice things like:

- spikes in denied actions;
- growth in approval backlog;
- unusual tool selection patterns;
- new egress destinations;
- memory write anomalies;
- growth in unsafe fallback behavior;
- drift in task success and safety metrics.

In other words, detection here has to function not only as observability, but also as abuse and safety monitoring.

## 6. Response should be its own operational function

When an agent starts behaving unsafely, it is not enough to say “we will tune the prompt later.”

A practical response layer is built around concrete actions:

- restrict a capability;
- force an action into approval-only mode;
- narrow the egress policy;
- disable risky memory writes;
- move the rollout wave to a safer profile;
- fully disable the problematic route when necessary.

This matters because in agent systems, response often has to happen faster than full root-cause analysis.

<div class="diagram-card">
<p>The assurance loop works as a continuous cycle: search, detect, contain, fix, learn</p>

``` mermaid
flowchart LR
    A["Red teaming and incidents"] --> B["Findings"]
    B --> C["Detection rules and monitors"]
    C --> D["Response actions"]
    D --> E["Remediation"]
    E --> F["Updated policy, evals, and rollout rules"]
    F --> A
```

</div>

## 7. Remediation should change the system, not only the document trail

A common weakness is this: the incident is reviewed, a document is written, but the actual system behavior barely changes.

Strong remediation usually changes at least one real layer:

- policy rules;
- approval thresholds;
- tool exposure;
- memory write constraints;
- eval datasets;
- rollout gates;
- alerting and detection rules.

If remediation does not change the operational surface, the system has learned very little.

## 8. User reports and incidents should feed the assurance loop

Another important practical point: the assurance loop cannot be built only from internal team exercises.

Useful sources of new failure modes include:

- production traces;
- user complaints;
- approval queue anomalies;
- postmortems;
- online eval drift;
- red-team findings.

Those signals should flow back into:

- eval datasets;
- safety checks;
- change classification;
- rollout policy.

Otherwise the team will keep rediscovering the same surprises.

## 9. A good assurance loop is tied to ownership

Without ownership, assurance dissolves quickly.

It helps to know in advance:

- who runs the red-team backlog;
- who triages findings;
- who owns mitigations;
- who can emergency-disable a capability;
- who decides that remediation is sufficient;
- who updates monitoring and response rules.

This connects directly to the organizational part of the book: security discipline breaks where ownership is unclear.

## 10. Example assurance policy

Here is a practical skeleton:

```yaml
assurance:
  red_team:
    cadence: monthly
    required_surfaces:
      - prompt_injection
      - tool_misuse
      - memory_poisoning
      - egress_abuse
  findings:
    require_owner: true
    require_severity: true
    require_remediation_due_date: true
  response:
    emergency_actions:
      - disable_capability
      - require_approval
      - restrict_egress
      - disable_memory_write
```

It is not a complete framework, but it shows clearly that assurance can also be described as an operational contract.

## 11. Example code for emergency response

Here is a small sketch:

```python
from dataclasses import dataclass


@dataclass
class AssuranceSignal:
    unsafe_egress_detected: bool = False
    memory_poisoning_suspected: bool = False
    approval_bypass_detected: bool = False


def emergency_action(signal: AssuranceSignal) -> str:
    if signal.unsafe_egress_detected:
        return "restrict_egress"
    if signal.approval_bypass_detected:
        return "require_approval"
    if signal.memory_poisoning_suspected:
        return "disable_memory_write"
    return "observe"
```

The point is that response decisions should not be pure improvisation. They should be part of a designed operational surface.

## 12. What usually breaks

The failures are fairly repetitive:

- red teaming is disconnected from the engineering backlog;
- findings get no owners;
- incidents never enter eval datasets;
- detection watches only latency and errors;
- response actions are too coarse or too slow;
- remediation does not change the real system.

When that happens, the assurance loop becomes a good slide deck instead of a defensive mechanism.

## 13. Practical checklist

If you want to test your assurance discipline quickly, ask:

- Is red teaming regular, not one-off?
- Are findings tracked as engineering backlog items?
- Are there monitors not only for infra health, but also for unsafe behavior?
- Are there fast emergency actions short of full shutdown?
- Do incidents flow back into evals and rollout rules?
- Is it clear who owns detection, response, and remediation?

If the answer is “no” several times in a row, you may have security intentions, but not yet an assurance loop.

## 14. What to read next

After the assurance loop, it is natural to move to supply chain discipline and approved artifacts. As soon as the system changes continuously, investigations happen, and mitigations are applied, it becomes critical to know which artifacts were actually trusted and what exactly reached production.

- [Chapter 20. Change Management for Agent Systems](chapter-20.en.md)
- [Chapter 14. Platform Team vs Product Teams](../part-vi/chapter-14.en.md)
- [Chapter 18. Production Rollout Checklist](../part-vii/chapter-18.en.md)
- [Sources](../../appendix/sources.en.md)

[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
