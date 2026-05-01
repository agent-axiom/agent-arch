# Memory Record and Retrieval Contract Schema

This page defines the minimal contract layer for memory and retrieval in agent systems: what a memory record looks like, which fields a retrieval query should contain, and which guarantees are needed so memory does not turn into an unmanaged source of leakage, noise, and false confidence.

If the [trace schema and event catalog](trace-schema.en.md) answer “how this appears in telemetry,” and the [lifecycle artifact schema](lifecycle-artifact-schema.en.md) answers “what counts as a governed operational artifact,” then the memory-retrieval schema answers “which records and filters are actually allowed inside the memory layer.”

## 1. Why a separate schema layer matters

A very common memory failure mode looks like this:

- the agent remembered something;
- retrieval returned something;
- the team can no longer answer with confidence:
  - what kind of record it was;
  - where it came from;
  - who was allowed to read it;
  - under which rules it entered the prompt.

That is why it is useful to describe the memory layer not as “we have a vector store,” but as typed records and typed retrieval rules.

## 2. Core entities

A minimal layer here works well around three entities:

- `memory_record`
- `retrieval_query`
- `retrieval_result`

That is already enough to connect Chapters 5-7, the policy layer, the trace schema, and the reference runtime.

## 3. Memory record

`memory_record` describes one concrete entry inside the memory layer.

```yaml
kind: memory_record
record_id: mem-tenant-acme-001
tenant_id: tenant-acme
memory_class: profile
key: preferred_language
value: English
source: user_confirmed_preference
provenance: user_confirmed_preference
revision: 1
trust_level: high
created_at: 2026-04-07T12:00:00Z
retention: long_term
```

The key parts are:

- `tenant_id` prevents retrieval from crossing tenant boundaries;
- `memory_class` distinguishes `short_term`, `long_term`, and `profile`;
- `source` and `provenance` help separate observations from validated facts;
- `revision` keeps history from being silently overwritten;
- `trust_level` stops all records from being treated as equal.

## 4. Retrieval query

`retrieval_query` describes not only a text search, but the full operational context of reading memory.

```yaml
kind: retrieval_query
trace_id: trace-001
session_id: session-001
tenant_id: tenant-acme
principal_id: user-42
purpose: answer_generation
allowed_classes:
  - profile
  - long_term
filters:
  trust_min: medium
  max_age_days: 90
  require_provenance: true
limit: 5
```

This is useful because retrieval becomes not “magic search,” but a normal gated read path.

## 5. Retrieval result

`retrieval_result` captures what the runtime actually decided to return into context.

```yaml
kind: retrieval_result
trace_id: trace-001
session_id: session-001
selected_records:
  - record_id: mem-tenant-acme-001
    memory_class: profile
    trust_level: high
    provenance: user_confirmed_preference
  - record_id: mem-tenant-acme-177
    memory_class: long_term
    trust_level: medium
    provenance: validated_service_rule
selection_reason:
  - profile_match
  - tenant_match
  - trust_filter_passed
excluded_records: 12
```

That makes it possible to explain:

- why these records entered the prompt;
- which restrictions were applied;
- how many records were filtered out.

## 6. How this connects to the policy layer

The memory read path and memory write path almost never should live under identical rules:

- the write path cares more about validation, provenance, and retention;
- the read path cares more about tenant boundaries, trust filters, and class restrictions.

That is why a strong memory schema usually sits next to policy-as-code.

## 7. How this connects to the trace schema

The [trace schema](trace-schema.en.md) already contains events and fields that support memory discipline:

- `context_layers_built`
- `memory_persisted`
- `memory_class`
- `provenance`
- `revision`

That means the memory-retrieval contract is useful not only by itself, but also as the basis for understandable telemetry.

## 8. How this connects to the reference package

The [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) package already contains operational primitives for this model:

- [memory.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/memory.py)
- [background.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/background.py)
- [configs/memory.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/memory.yaml)
- CLI:
  - `inspect-memory`

The bundled `memory.yaml` keeps this concrete through `seed_records`; each seed record carries a stable `memory_id` plus `tenant_id`, `memory_class`, `kind`, `content`, `source`, `confidence`, `provenance`, and `revision`, so the demo can show both retrieval filtering and record lineage.

That is useful because the book not only explains the memory contract, but also shows a runnable skeleton.

## 9. Minimal invariants

A healthy memory-retrieval layer usually enforces:

- every record has `tenant_id` and `memory_class`;
- persistent records carry `provenance` and `revision`;
- retrieval is always bounded by classes and size;
- the retrieval query knows who is reading and why;
- the retrieval result can be reconstructed from the trace;
- summaries are not treated as truth by default.

## 10. What usually breaks

The common failure modes are very recognizable:

- retrieval returns “similar” but not “useful”;
- memory records are not separated by trust level;
- summaries silently overwrite more reliable facts;
- retrieval ignores tenant boundaries;
- the prompt receives too much context without filters;
- provenance exists only on paper and not in runtime.

## 11. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Does every record have `tenant_id`, `memory_class`, `provenance`, and `revision`?
- Are memory read policy and memory write policy distinct?
- Is retrieval bounded by trust, class, and size?
- Can you explain why a given record entered the prompt?
- Is there protection against retrieval across another tenant?
- Are memory decisions visible in trace and session export?

If the answer is “no” several times in a row, you already have memory, but not yet real memory discipline.

## What to Do Next

- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](../book/part-iii/chapter-5.en.md)
- [Chapter 6. Short-Term, Long-Term, and Profile Memory](../book/part-iii/chapter-6.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](../book/part-iii/chapter-7.en.md)
