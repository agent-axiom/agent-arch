# Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries

## 1. Why the Most Expensive Failures Often Look Like "We Just Repeated the Call"

Once an agent system starts performing real actions, one of the ugliest incident sources turns out to be very mundane: a repeated call.

From the outside it often looks harmless:

- the request hung;
- the runtime retried;
- the integration was unstable;
- the agent tried to "help" and sent the action again.

In the real world that means:

- two identical tickets;
- two emails to the same customer;
- a repeated charge;
- a duplicate CRM write;
- several modifications to the same object.

So the problem is not the model's reasoning by itself. The problem is that the execution layer cannot live safely in a world of partial failure.

## 2. Idempotency Is Not Nice-to-Have, It Is Basic Insurance

Idempotency exists for one simple question: "If the system repeats this call by mistake, what happens?"

For write operations, a good answer should be one of two things:

- the repeated call does not change the outcome;
- the system can reliably detect the duplicate and avoid creating the side effect twice.

Without that property, any network instability, timeout, or race between runs becomes too expensive.

## 3. Retry Without Error Classification Multiplies Chaos

A very bad strategy looks like this: "if the request failed, retry it three times".

In production that is dangerous, because not all failures are equal:

- `validation_failure` almost never deserves a retry;
- `permission_denied` cannot be fixed by repetition;
- `retryable_failure` may require backoff;
- `side_effect_unknown` requires caution, not blind repetition.

So retry policy should depend on outcome class, not on the feeling of "maybe it will work now".

## 4. The Worst Status Is `side_effect_unknown`

There is one especially painful category of failure: you no longer know whether the side effect happened.

Examples:

- timeout after the request was sent to the external service;
- connection loss after commit;
- adapter crash before confirmation was stored;
- an external API response that leaves final state unclear.

This is exactly where naive retry is most dangerous. Sometimes the right behavior is not "retry", but:

- check current state in the external system;
- run reconciliation;
- involve a human;
- stop the workflow and explicitly record the uncertainty.

## 4.1. The recovery branch should also be designed explicitly

Recent work on tool-failure cases reinforces another practical point: the recovery path should rarely be left as improvisation inside the execution layer.

It is useful to define in advance:

- which outcome classes require reconcile rather than retry;
- where partial success should create a follow-up task;
- when recovery itself requires approval;
- which branches must appear in the eval dataset;
- where a dangerous recovery path should stop instead of “trying one more time”.

Many severe incidents happen not on the happy path, but in a poorly designed recovery branch.

## 5. Rate Limits Are Also Part of Safety Design

When teams think about rate limits only as a performance problem, the execution layer underestimates their architectural role.

In reality, rate limits also protect against:

- one runaway agent DDoS-ing an external system;
- cyclic planning turning into a storm of tool calls;
- high-cost capabilities consuming the whole budget;
- retry storms killing an integration.

That is why limits are useful not only at the whole-service level, but also:

- per tool;
- per tenant;
- per workflow;
- per risk class.

## 6. Rollback Boundaries Must Be Defined in Advance

It is dangerous to discover only during an incident that an operation is "not actually reversible".

For every write capability, it helps to know in advance:

- can the action be undone;
- can the action be safely repeated;
- where the point of no return is;
- what compensating action is acceptable;
- when manual reconciliation is required.

Rollback boundary is not "we will decide later". It is part of the tool and workflow contract.

<div class="diagram-card">
<p>After a side effect, the execution layer must distinguish safe retry, reconcile, and stop paths</p>

``` mermaid
flowchart TD
    A["Tool request"] --> B["Execute write action"]
    B --> C{"Outcome known?"}
    C -->|Yes, success| D["Store result and continue"]
    C -->|Retryable failure| E["Retry with policy and backoff"]
    C -->|Unknown side effect| F["Reconcile or request human review"]
    C -->|Validation or permission failure| G["Stop and surface error"]
```

</div>

## 7. A Good Execution Contract Stores Operational Semantics Explicitly

Knowing only the input schema and response shape is not enough. For dangerous operations, the contract must also store operational semantics:

- whether the action is idempotent;
- whether an idempotency key is required;
- which failures are retryable;
- what the retry limit is;
- what rate limits apply;
- what to do on unknown outcome;
- whether rollback or compensating action exists.

```yaml
tools:
  create_ticket:
    mode: write
    idempotent: true
    idempotency_key_required: true
    retry:
      max_attempts: 3
      backoff: exponential
      retry_on: ["retryable_failure"]
    rate_limit:
      per_tenant_per_minute: 20
    rollback:
      strategy: "none"
      reconcile_on_unknown: true

  send_email:
    mode: write
    idempotent: false
    idempotency_key_required: false
    retry:
      max_attempts: 1
      retry_on: []
    rate_limit:
      per_user_per_hour: 10
    rollback:
      strategy: "manual_only"
      reconcile_on_unknown: true
```

The value of that YAML is that it forces the team to admit an uncomfortable truth: not every action is equally safe to automate.

## 8. A Simple Retry Decision Example

This is not a production policy engine, but a simple skeleton. Its job is to show that retry must depend on outcome class, not on a generic reflex.

```python
from dataclasses import dataclass


@dataclass
class ExecutionOutcome:
    status: str
    attempts: int
    max_attempts: int


def next_step(outcome: ExecutionOutcome) -> str:
    if outcome.status in {"validation_failure", "permission_denied"}:
        return "stop"
    if outcome.status == "retryable_failure" and outcome.attempts < outcome.max_attempts:
        return "retry_with_backoff"
    if outcome.status == "side_effect_unknown":
        return "reconcile"
    if outcome.status == "success":
        return "continue"
    return "escalate"
```

The important thing is not the code itself, but the fact that the system now has an explicit operational decision table.

## 9. The Idempotency Key Must Be Part of the Protocol

If a write tool "supports idempotency" only on paper, but the key:

- is optional;
- is generated differently in different layers;
- does not survive the retry path;
- is not logged,

then it is hardly real idempotency.

Good practice:

- generate the key at workflow or action boundary;
- carry it through the full execution path;
- log it in audit trails;
- use it for reconciliation and investigations.

## 10. Common Mistakes

Typical failures repeat:

- retries are sent to errors that should never be retried;
- unknown outcomes are treated like ordinary failures;
- rate limits exist only at ingress, not on tools;
- rollback is promised but does not actually exist;
- the idempotency key is lost between planner and adapter;
- the agent has too much freedom in repeated attempts.

All of this means the execution layer has not yet grown into a production-grade failure model.

## 11. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Do write tools have an explicit idempotency strategy?
- Does the system distinguish `retryable_failure` from `side_effect_unknown`?
- Are retries bound to policy rather than a generic helper?
- Are there per-tool or per-tenant rate limits?
- Do you understand the rollback boundary for every risky action?
- Can the runtime reconcile instead of blindly retrying?
- Are idempotency keys visible in traces and audit logs?

If the answer is "no" several times in a row, the next unstable integration will almost certainly turn into duplication, noise, or a manual incident review.

## 12. What to Do Next

Part IV now closes the basic execution layer: contracts, sandboxing, capability transport, and side-effect discipline. The next logical move is reliability and observability at the whole agent-system level.

- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](chapter-9.en.md)
- [Part IV. Tools and Execution](index.en.md)
- [Sources](../../appendix/sources.en.md)
