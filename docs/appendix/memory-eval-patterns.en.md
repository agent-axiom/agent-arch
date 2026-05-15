# Memory Eval Patterns for Agent Systems

Memory in agent systems fails differently from ordinary retrieval. Errors often show up not in one request, but across a sequence of runs, profile updates, and background writes.

That is why the memory layer benefits from explicit evaluation instead of hoping it will be covered indirectly by the general eval dataset.

## 1. Why memory evals deserve their own layer

Even when overall task success looks healthy, memory design can degrade quietly:

- the profile is filled with unnecessary or risky facts;
- a stale preference keeps influencing answers;
- the system remembers the wrong thing;
- the needed fact is not retrieved in a long session;
- background compaction distorts the meaning of a record.

That is why the memory layer needs its own evaluation logic.

## 2. Which error types should be covered

A minimal memory eval set usually needs at least:

!!! note "Canonical memory eval cases"
    The memory eval suite should test state quality differently for the three canonical cases. **Support triage** checks requester context carryover, ticket state retrieval, `idempotency_key` evidence, no-write decision, and duplicate-ticket regression. **Internal knowledge assistant** checks retrieval freshness, source attribution, tenant isolation, memory provenance, and grounded-answer quality. **Incident coordination** checks incident timeline recall, response ownership handoff, escalation status, noisy alert filtering, and post-incident lesson retention.

- incorrect write;
- missing write;
- unsafe write;
- stale retrieval;
- false retrieval;
- profile contradiction;
- over-retention;
- deletion failure.

That list is already useful even without a large benchmark.

## 3. What to evaluate in short-term memory

Short-term memory is usually tested for:

- retention of critical dialogue context;
- avoiding unnecessary carry-over to the next turn;
- resilience to noisy user turns;
- correct clarification behavior under ambiguity.

The problem here is often not storage itself, but how runtime decides what is worth carrying forward.

## 4. What to evaluate in profile and long-term memory

Profile memory and long-term memory need stricter checks:

- whether a fact deserved to be written at all;
- whether it was written into the right memory class;
- whether provenance can be explained;
- whether the record can be safely deleted or revised;
- whether a stale record still affects the answer path.

Contradiction and retention-hygiene evals are especially important here.

## 5. Long-horizon memory should be tested across runs

One common mistake is evaluating memory quality on a single isolated prompt.

Real failures usually emerge over sequences:

- a preference is written in run 1;
- retrieved incorrectly in run 4;
- overwritten by a conflicting fact in run 6;
- the stale profile still affects run 9.

That is why memory evals are more useful as multi-run scenarios than as single-turn checks.

## 6. Which fields are useful in a memory eval case

A minimally useful eval record often includes:

- `memory_class`
- `write_expected`
- `retrieval_expected`
- `allowed_to_persist`
- `expected_provenance`
- `revision_behavior`
- `deletion_behavior`

This helps separate “the answer was bad” from “memory semantics were violated.”

## 7. Why this matters for safety

Memory evals are not only for personalization. They also matter for safety:

- whether the system writes sensitive data without permission;
- whether it retains risky state for too long;
- whether it confuses user-specific data;
- whether a harmful memory path can be stopped quickly;
- whether provenance for persistent records can be proven.

Without this layer, memory incidents will look like vague model behavior even when the real problem is record lifecycle.

## 8. How memory evals relate to the general eval loop

Memory evals do not replace the [main eval chapter](../book/part-v/chapter-13.en.md). They add another plane:

- ordinary offline evals test task success;
- memory evals test state quality across runs;
- online signals help catch drift;
- incidents and postmortems update memory-specific cases.

In other words, the memory layer should be part of regression discipline as explicitly as tools or policy.

## 9. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Are there separate cases for write / no-write decisions?
- Is retrieval tested across longer run sequences?
- Are stale profile and contradiction cases included?
- Is provenance for persistent records evaluated?
- Are deletion and revision cases covered?
- Do memory incidents flow back into the eval dataset?

## What to Do Next

- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)
- [Memory Record and Retrieval Contract Schema](memory-retrieval-schema.en.md)
- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](../book/part-iii/chapter-5.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](../book/part-iii/chapter-7.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)
