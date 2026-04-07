# Trace Schema and Event Catalog

This page exists to bridge one practical gap: moving from a high-level observability discussion to an event structure that can actually be exported, inspected, and reused in eval workflows.

It connects two parts of the book:

- [Chapter 11. Traces, Spans, and Structured Events](../book/part-v/chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)

And the runnable package:

- [Reference Package](reference-package.en.md)

## Why an explicit trace schema matters

Without an explicit trace schema, teams usually end up in one of two bad states:

- events exist, but they are just ad hoc JSON blobs;
- events help with debugging, but they are weak inputs for grading, audit, or incident review.

That is why it is useful to separate:

- `trace envelope`
- `event catalog`
- `payload contracts`

Even in a small runtime.

## Minimal trace envelope

`agent_runtime_ref` currently uses an intentionally compact envelope:

```json
{
  "event_type": "run_start",
  "trace_id": "trace-demo-001",
  "payload": {
    "agent_id": "support-triage-ref",
    "tenant_id": "tenant-acme",
    "principal_id": "user-42",
    "session_id": "session-demo-001",
    "user_input": "Please create a ticket for this onboarding issue."
  }
}
```

The minimum useful field set is:

- `event_type`
- `trace_id`
- `payload`

In production, this usually needs to grow to include:

- `session_id`
- `agent_id`
- `tenant_id`
- `principal_id`
- `event_ts`
- `span_id`
- `parent_span_id`

In the reference runtime, some of those fields still live inside `payload` to keep the structure small and easy to inspect. At the same time, serialized events now carry `schema_version`, and the export path supports redaction for selected fields.

## How trace and session relate

For agent systems, one trace is usually not enough. You almost always need a longer context:

- one `trace_id` describes one run;
- one `session_id` links multiple runs together;
- a session-level summary can already support evals, rollout review, and postmortems.

That is why the package includes:

- `inspect-trace`
- `inspect-session`
- `session-eval-summary`
- `export-session`
- `export-eval-dataset`

## Reference runtime event catalog

Below is the current minimal event catalog.

| Event type | When it appears | Why it matters |
| --- | --- | --- |
| `run_start` | at the beginning of a run | captures input and actor identity |
| `context_layers_built` | after context assembly | shows which context layers actually entered the run |
| `tool_policy_decision` | before tool execution | records the policy gate and allow/deny/approval reason |
| `approval_requested` | on a high-risk write path | shows that execution moved into human review |
| `memory_persisted` | after a background write | records provenance and revision of a memory record |
| `run_complete` | at the end of a run | closes the run-level outcome |
| `span` | around individual calls | provides simple latency and status telemetry |

This is not meant to be a universal perfect catalog. It is a compact operational vocabulary that is already enough to support:

- trace inspection;
- regression seeds;
- session summaries;
- incident review.

## Why payload contracts matter

The problem is not that events are plain. The problem is that without contracts, payloads quickly turn into garbage.

For each event type, decide up front:

- which fields are required;
- which fields are stable;
- which fields can be added without breaking downstream tooling;
- which fields matter for grading;
- which fields matter for audit.

For example, `tool_policy_decision` should usually include at least:

- `capability_name`
- `decision`
- `reason`
- `risk_tier`
- `tool_principal`

And `memory_persisted` should usually include:

- `memory_class`
- `kind`
- `provenance`
- `revision`

## What the package already supports

You can inspect this directly:

```bash
.venv/bin/python -m agent_runtime_ref dump-events
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl --redact-field user_input
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

That matters because the same trace vocabulary now lives in three places at once:

- in the runtime;
- in the book;
- in eval-ready artifacts.

## What a production schema should add

The reference runtime is intentionally small, so a more mature system should quickly add:

- a timestamp on every event;
- explicit `span_id` and `parent_span_id`;
- a separate stable `run_id`;
- version fields for the schema;
- a split between `display payload` and `machine payload`;
- redaction rules for sensitive fields.

That is what turns an event stream from debug output into a real platform artifact.

## Practical checklist

If you want to know whether your trace schema is ready for more than local debugging, check these questions:

- Do you have a stable event catalog?
- Do you clearly separate `trace_id` and `session_id`?
- Is it clear which fields are required for each event type?
- Can you reconstruct the policy decision and tool path from a trace?
- Can you build an eval dataset from a session export?
- Do you have a plan for redaction and schema versioning?

If several answers are “no,” you probably have logging, but not yet a real trace schema.

## See Also

- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)
- [Policy Bundle Schema and Approval Contract](policy-bundle-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)
