# Trace Schema and Event Catalog

This page exists to bridge one practical gap: moving from a high-level observability discussion to an event structure that can actually be exported, inspected, and reused in eval workflows.

It connects two parts of the book:

- [Chapter 11. Traces, Spans, and Structured Events](../book/part-v/chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)
- [Evidence Spine: From Request to Rollout Judgment](../book/part-v/evidence-spine.en.md)

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
- `verifier contract identity`
- `verifier evidence linkage`

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

In the reference runtime, some of those fields still live inside `payload` to keep the structure small and easy to inspect. At the same time, serialized events now carry `schema_version` and `redacted_fields`, and the export path supports redaction for selected fields. The event loader validates this shape explicitly: `Telemetry path must be a string or path-like object`, `Telemetry event line is not valid JSON: {line_number}`, `Telemetry event must be a mapping`, `Telemetry event is missing required field: {required_field}`, `Telemetry event field must be a string: {field}`, `Telemetry event field must not be empty: {field}`, `Telemetry schema version is not supported: {schema_version}`, `Telemetry event payload must be a mapping`, `Telemetry event payload key must be a string`, `Telemetry event payload key must not be empty`, `Telemetry event payload keys must be unique`, `Telemetry event payload value must be a string: {payload_key}`, `Telemetry event redacted_fields must be a tuple`, `Telemetry event redacted_fields must be a list`, `Telemetry event redacted_fields entries must be strings`, `Telemetry redact field must not be empty`, and `Telemetry redact field is not present in events: {missing}`.

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

`dump-events`, `export-events`, and `inspect-trace` also keep the command response usable as a triage surface rather than just a raw JSONL dump: they expose `session_id`, `tenant_id`, `principal_id`, `agent_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `status`, `result`, `output_preview`, `failure_reason`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, and non-empty `idempotency_keys` before an operator has to manually scan every `approval_requested` or `tool_execution` payload. `replay-run` then reports `source_idempotency_keys` and `replay_idempotency_keys` separately, making it explicit that replay is a new run with its own duplicate-write key rather than a silent reuse of the original write.

Trace replay validates this evidence before it can seed a new run: `Trace ID request must be a string`, `Trace ID not found in event file: {requested_trace_id}`, `Trace file does not contain any trace IDs`, `Trace file contains multiple trace IDs; pass --trace-id explicitly`, `Trace file does not contain a run_start event`, `Trace file contains multiple run_start events`, `Trace run_start event is missing replay fields: {missing_keys}`, `Trace run_start event has redacted replay fields: {redacted_keys}`, `Trace run_start replay field must be a string: {field}`, and `Trace run_start replay field must not be empty: {field}`.

## Reference runtime event catalog

Below is the current minimal event catalog.

| Event type | When it appears | Why it matters |
| --- | --- | --- |
| `run_start` | at the beginning of a run | captures input and actor identity |
| `policy_precheck` | immediately after run admission | records the policy precheck action, reason, and policy ID |
| `agent_threat_evidence` | when a threat-model control leaves evidence | links threat class to trace/evidence identifiers |
| `retrieval` | when memory context is fetched | records the source and number of retrieved records |
| `context_layers_built` | after context assembly | shows which context layers actually entered the run; internally `RunContext` keeps `retrieved_context` and `retrieved_records` before any `tool_request` is handled |
| `tool_policy_decision` | before tool execution | records the policy gate and allow/deny/approval reason |
| `mcp_tool_risk_review` | during MCP tool/server risk review | links threat class, registry evidence, scope review, and quarantine state |
| `tool_execution` | after a capability call or approval handoff | records capability status and tool-principal context |
| `a2a_handoff` | when one agent delegates work to another agent | records delegation chain, authorization, and failure-attribution context |
| `approval_requested` | on a high-risk write path | shows that execution moved into human review |
| `sandbox_profile_reviewed` | when a sandbox-backed path is reviewed | records workspace, permissions, and snapshot/resume evidence review |
| `memory_write_decision` | before background memory persistence | records whether a candidate memory write was allowed or denied |
| `memory_persisted` | after a background write | records provenance and revision of a memory record |
| `background_compaction` | after background memory maintenance | records tenant-level compaction results |
| `background_update_scheduled` | after background work is queued or completed | records background update status for the run |
| `run_failed` | when a tool failure becomes the run outcome | preserves explicit failed-run traceability |
| `governance_action` | when a telemetry signal triggers a policy, containment, rollout, or registry decision | links a governance action record to trace evidence |
| `run_complete` | at the end of a run | closes the run-level outcome |
| `span` | around individual calls | provides simple latency and status telemetry |

This is not meant to be a universal perfect catalog. It is a compact operational vocabulary that is already enough to support:

A stronger production vocabulary should also make room for verifier-aware evidence, so traces can later explain not only what the runtime did, but also what evidence a verifier used to judge process quality, outcome quality, or failure attribution.

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

For `agent_threat_evidence`, preserve the evidence markers from the unified agent threat model so threat rows can be checked against traces, not prose only:

- `prompt_boundary_event`
- `retrieval_source_id`
- `memory_record_id`
- `delegation_trace_id`
- `tenant_id`
- `cost_budget_event`
- `decision_trace_id`

For example, `tool_policy_decision` should usually include at least:

- `capability_name`
- `decision`
- `reason`
- `risk_tier`
- `tool_principal`

For `mcp_tool_risk_review`, production traces should record MCP threat-model evidence, not only the final allow/deny decision:

- `threat_class`
- `mcp_server_id`
- `capability_name`
- `tool_contract_version`
- `registry_owner`
- `scope_review`
- `quarantine_state`
- `evidence_refs`

Keep `threat_class` on the MCP threat model vocabulary: `tool poisoning`, `rug pull attack`, `tool shadowing`, `confused deputy`, `over-scoped tokens`, `data exfiltration through legitimate channels`, `supply-chain attack`, `replay/tampering`, `sandbox escape`.

For `a2a_handoff`, the payload should preserve the trust contract, not only the delegated message text:

- `agent_identity`
- `delegation_chain`
- `allowed_collaboration_graph`
- `inter_agent_authorization`
- `policy_inheritance`
- `non_repudiation`
- `failure_attribution`

!!! example "Trace for the duplicate-ticket thread"
    In the support-triage case, `tool_policy_decision`, `approval_requested`, `tool_execution`, and the final outcome should be tied by one `trace_id`, `session_id`, `approval_id`, `tool_principal`, and `idempotency_key`. If `create_ticket` times out and the side-effect status is unknown, the trace should show `side_effect_unknown` instead of masking the run as successful or repeating the write without reconciliation.

!!! note "Canonical trace cases"
    The three canonical cases need different trace emphases. **Support triage** ties approval events, `idempotency_key`, tool side effects, and duplicate-ticket recovery evidence. **Internal knowledge assistant** should preserve retrieval spans, memory access, source attribution, freshness checks, and access control decisions. **Incident coordination** should show escalation timeline, notification side effects, response ownership, handoff events, and post-incident learning.

For a sandbox-backed run, reserve fields that link the trace to the execution boundary:

- `sandbox_session_id`
- `sandbox_manifest_version`
- `sandbox_permissions_profile`
- `snapshot_id`
- `workspace_manifest_ref`

If rollout or eval requires `sandbox_profile_review`, the trace should also be able to point to review evidence, not only state fields:

- `sandbox_profile_contract`
- `workspace_entries_reviewed`
- `permissions_profile`
- `network_secrets_posture`
- `snapshot_policy`
- `reviewed_by`
- `review_evidence_refs`

If the system relies on verifier-aware evals, it is also useful to define an event or linked payload contract for verifier evidence, for example:

- `verdict_id`
- `verifier_id`
- `verifier_contract_version`
- `input_refs`
- `process_score`
- `outcome_score`
- `failure_attribution`
- `blocking_decision`
- `comparison_baseline`
- `reviewer_override`
- `evidence_refs`

For `governance_action`, record the fields that turn telemetry into a governance action rather than only a dashboard signal:

- `governance_action_id`
- `source_signal`
- `decision_owner`
- `action_state`
- `evidence_refs`
- `review_deadline`

Keep `source_signal` on a constrained vocabulary aligned with governance-aware telemetry: `policy_decision_feedback`, `containment_decision`, `rollout_gate_input`, `incident_response_trigger`, `registry_update_signal`.

For `memory_write_decision` in memory poisoning review, the trace should preserve the same review fields as the memory schema:

- `write_trust_boundary`
- `activation_policy`
- `contamination_scope`
- `policy_influence`
- `provenance_check`
- `quarantine_state`
- `rollback_ref`

And `memory_persisted` should usually include:

- `memory_class`
- `kind`
- `provenance`
- `revision`

The current reference payloads also use operational metadata fields such as `runtime_principal`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `policy_id`, `static_items`, `session_items`, `retrieved_items`, `tool_items`, `approval_id`, `reviewer`, `capability_session_id`, `capability_session_status`, `tool_status`, `output_preview`, `memory_id`, `revision_mode`, `compacted_records`, `persisted_records`, `tool_results`, `span_name`, and `duration_ms`. Tool request/result model validation is part of the same trace boundary: malformed tool calls fail with `Tool request capability name must be a string`, `Tool request capability name must not be empty`, `Tool request arguments must be a mapping`, `Tool request argument key must be a string`, `Tool request argument key must not be empty`, `Tool request argument keys must be unique`, `Tool request argument value must be a string: {argument_key}`, and malformed tool results fail with `Tool result status must be a string`, `Tool result status must not be empty`, `Tool result payload must be a mapping`, `Tool result payload key must be a string`, `Tool result payload key must not be empty`, `Tool result payload keys must be unique`, and `Tool result payload value must be a string: {payload_key}`.

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
- redaction rules for sensitive fields;
- an explicit way to link traces to verifier evidence, screenshots, or grading artifacts;
- a stable way to record which verifier contract version produced the grading output;
- sandbox state fields for runs that materialize a workspace, use shell/filesystem capabilities, or continue from a snapshot;
- an event or linked payload for `sandbox_profile_reviewed`, so rollout/eval evidence for workspace, permissions, and snapshot/resume policy is traceable.

That is what turns an event stream from debug output into a real platform artifact.

## What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Do you have a stable event catalog?
- Do you clearly separate `trace_id` and `session_id`?
- Is it clear which fields are required for each event type?
- Can you reconstruct the policy decision and tool path from a trace?
- Can you build an eval dataset from a session export?
- Can you link a trace to verifier evidence used in grading or rollout review?
- If rollout requires `sandbox_profile_review`, is there trace evidence for workspace entries, permissions, and snapshot/resume policy?
- Can you tell which verifier contract version produced that grading output?
- Do you have a plan for redaction and schema versioning?

If several answers are “no,” you probably have logging, but not yet a real trace schema.

## What to Do Next

- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)
- [Policy Bundle Schema and Approval Contract](policy-bundle-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)
