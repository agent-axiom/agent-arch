# Tool Failure Recovery Patterns for Agent Systems

Tool errors rarely end as a simple `error`. More often the team ends up in harder states:

- side effect unknown;
- partial success;
- stale reconciliation;
- a repeated call that is now more dangerous than the original error.

That is why agent systems benefit from an explicit recovery pattern layer instead of reducing everything to retry policy.

## 1. Why tool failure recovery deserves its own layer

When execution fails, the instinct is often “just retry.” But different tools produce different consequences:

- a read tool is usually safer to repeat;
- a write tool can create duplicates;
- a connector may perform the action but fail to return confirmation;
- a downstream system may end up in an intermediate state.

That is why recovery logic belongs in the contract layer.

## 2. Which outcome classes matter

A minimally useful taxonomy looks like this:

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_failure`
- `side_effect_unknown`
- `partial_side_effect`
- `manual_reconciliation_required`

If the execution layer does not distinguish these classes, the agent will almost inevitably make overly coarse recovery decisions.

## 3. What to do with `side_effect_unknown`

This is the most dangerous failure class.

!!! note "Canonical recovery cases"
    The recovery branch should distinguish failure surfaces for the three canonical cases. **Support triage** focuses on `side_effect_unknown`, idempotency lookup, duplicate-ticket prevention, manual reconciliation, and eval/rollout regression. **Internal knowledge assistant** focuses on stale retrieval, source lookup failure, access-denied recovery, memory write rollback, and grounded-answer recheck. **Incident coordination** focuses on notification partial delivery, escalation retry, owner handoff repair, emergency rollback decision, and post-incident learning capture.

Instead of naive retry, it is usually better to:

- check the current state in the external system;
- look up the object by idempotency key;
- move the capability into temporary restricted mode;
- request human review;
- record the uncertainty in traces and the incident record.

The goal is simple: do not multiply side effects before state is recovered.

## 4. What to do with `partial_side_effect`

Here the system has already changed the outside world, but failed before clean completion.

Useful strategies include:

- a compensating action, if one is acceptable;
- an explicit reconciliation step;
- stop and surface partial completion;
- a follow-up task instead of silent retry.

The key point is simple: partial success is not success, but it also does not mean the whole operation can safely start from zero.

## 5. When recovery should require a human

A human gate is especially useful when:

- the side effect is irreversible;
- reconciliation itself is risky;
- the external system cannot be queried reliably;
- the team is unsure which payload version was applied;
- retry could expand the blast radius.

In other words, human review is useful not only for the initial action, but also for some recovery paths.

## 6. Which fields belong in the tool contract

Recovery quality depends heavily on what the execution layer knows about the tool contract.

Minimally useful fields include:

- `idempotent`
- `retry_on`
- `reconcile_on_unknown`
- `requires_manual_recovery`
- `compensating_action`
- `external_lookup_key`

Without these fields, recovery decisions often become ad hoc.

## 7. What to inspect in traces

During recovery review, the team should quickly see:

- which status the tool returned;
- whether retry was attempted;
- which idempotency key was used;
- whether reconciliation lookup happened;
- which payload actually went into the write path;
- who made the final recovery decision.

If traces cannot answer these questions, recovery incidents will take too long to investigate.

## 8. How this relates to evals

Tool failure recovery should appear explicitly in the eval dataset:

- timeout after write;
- connector disconnect after commit;
- duplicate retry attempt;
- partial success requiring follow-up;
- manual approval for a recovery path.

This matters because many severe production incidents happen not on the happy path, but in the recovery branch.

## 9. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Does the execution layer distinguish `retryable_failure` from `side_effect_unknown`?
- Is there an explicit recovery path for partial success?
- Is the recovery decision visible in traces?
- Are there tools where retry is forbidden by default?
- Are recovery branches included in the eval dataset?
- Can a dangerous recovery path require human review?

## What to Do Next

- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](../book/part-iv/chapter-10.en.md)
- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Incident Record and Postmortem Linkage Schema](incident-record-schema.en.md)
- [Incident Response Playbook for Agent Systems](incident-response-playbook.en.md)
- [Postmortem Template for Agent Systems](postmortem-template.en.md)
