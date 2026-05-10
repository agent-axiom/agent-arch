# Reference Package

The repository now includes a small runnable skeleton: [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref).

Its job is not to become a production framework. It exists as a minimal code anchor for **Parts VII and VIII** of the book.

This package is intentionally an implementation anchor, not a parallel product. Its value is that it lets the reader inspect runnable structure behind the book's argument without turning the project into a framework manual.

What this page does **not** promise:

- it does not replace the book's explanation of why the layers exist;
- it does not become the main place where architectural trade-offs are learned;
- it does not try to turn the repository into a general-purpose agent framework.

This is the canonical page for the package. The README keeps only a short quickstart, while the full CLI, config, and structure walkthrough lives here.

A practical reading path is:

- Chapter 16 for the baseline runtime and capability session state,
- Chapter 17 for policy layer and capability contracts,
- the [Evidence Spine](../book/part-v/evidence-spine.en.md) page for the end-to-end governed record from request to rollout judgment,
- Chapter 18 for rollout gates around approval and runtime behavior,
- Chapter 21 for assurance response,
- Chapter 22 and the lifecycle schema for governed artifact linkage, release identity, verifier-contract lineage, and delegated authorization provenance,
- Chapters 23-27 for interruption, expiry, re-init, retirement, observability, registry ownership, verifier-evidence obligations, and delegated-authorization lifecycle control around capability sessions.

!!! example "Runtime anchor for support-triage"
    The bundled `support-triage-ref` shows the same running case in executable form: agent identity, approved `search_docs`/`create_ticket` capabilities, approval wait, trace/session IDs, lifecycle checks, and eval export. That means the duplicate-ticket thread in the book can be reviewed not only as prose, but as a runnable contract surface.

## What Is Inside

- [runtime.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/runtime.py)
  The main `AgentRuntime`, which assembles run context, retrieval, the model step, tool execution, and the background update hook.
- [policy.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/policy.py)
  A small policy engine with structured decisions.
- [catalog.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/catalog.py)
  A capability registry with operational semantics, risk tier, and egress contract metadata.
- [identity.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/identity.py)
  Explicit agent identity and the approved capability inventory the runtime is allowed to use.
- [config.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/config.py)
  A YAML loader for agent identity, approved inventory, policy, capability catalog, and rollout policy.
- [memory.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/memory.py)
  Typed memory records, provenance, revisions, and a tenant-scoped in-memory store.
- [background.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/background.py)
  A background maintenance path for persistent memory writes, provenance-aware persistence, and compaction.
- [execution.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/execution.py)
  A simple capability dispatch layer through contract-aware execution, risk tiers, and egress policy.
- [telemetry.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/telemetry.py)
  An in-memory telemetry emitter for structured events and spans.
- [rollout.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/rollout.py)
  A minimal readiness gate before rollout.
- [controls.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/controls.py)
  Continuous controls and inventory drift checks for the approved registry.
- [approvals.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/approvals.py)
  Approval gates, pause/resume semantics, simple human review queues for high-risk actions, and the control surface where approval state has to stay aligned with capability session state.

That same runtime-control surface is also the natural place to keep delegated authorization assumptions explicit: which principal delegated access, whether that authorization may survive pause/resume, and what the runtime does if delegated access is revoked before the action completes.

- [lifecycle.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/lifecycle.py)
  Lifecycle artifacts for change records, artifact bundles, release-identity records, runtime-control schemas, verifier-contract lineage, and retirement plans, plus readiness checks for those states.

## How to Run It

```bash
.venv/bin/python -m agent_runtime_ref
```

Expected output:

```json
{"agent_id": "support-triage-ref", "request_agent_id": "support-triage-ref", "session_id": "session-demo-001", "tenant_id": "tenant-acme", "principal_id": "user-42", "authorization_mode": "platform_owned", "delegated_principal_id": "", "delegated_scope": "", "result": "Ticket request is waiting for human approval (apr-001).", "status": "success", "failure_reason": "", "trace_id": "trace-demo-001", "idempotency_keys": ["trace-demo-001"], "approval_ids": ["apr-001"], "approval_capability_names": ["create_ticket"], "approval_status_counts": {"pending": 1}, "event_types": ["run_start", "policy_precheck", "retrieval", "context_layers_built", "span", "tool_policy_decision", "approval_requested", "sandbox_profile_reviewed", "tool_execution", "memory_write_decision", "memory_persisted", "background_compaction", "background_update_scheduled", "run_complete"], "events": 14, "memory_records": 4, "memory_record_ids": ["mem-001", "mem-002", "mem-003", "mem-004"], "pending_approvals": 1, "pending_approval_ids": ["apr-001"], "pending_approval_capability_names": ["create_ticket"], "config_dir": ".../agent_runtime_ref/configs"}
```

Explicit runtime execution via subcommand:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref simulate-run --simulate-failure tool_timeout
```

The second form is a deliberately small failure-rich scenario. It lets the package demonstrate how an otherwise allowed capability can still end as a governed failed run with explicit telemetry instead of disappearing behind a generic success path. `simulate-run` returns `agent_id`, `request_agent_id`, `config_dir`, `trace_id`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `event_types`, `session_id`, `tenant_id`, `principal_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `status`, `result`, `events`, `memory_records`, `memory_record_ids`, `pending_approvals`, `pending_approval_ids`, `pending_approval_capability_names`, and optional `failure_reason`. Common identity and trace overrides include `--config-dir`, `--agent-id`, `--tenant-id`, `--principal-id`, `--trace-id`, and `--session-id`, so examples can be made deterministic without editing configs. More specialized selectors include `--limit` for memory inspection, `--approval-id` for approval closure, `--replay-trace-id` for trace replay, `--trace-prefix` for session commands, and `--session-prefix` for eval dataset exports.

Inspect the agent identity and approved inventory:

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
```

`inspect-agent` returns `agent_id`, `display_name`, `owner_team`, `runtime_principal`, `approved_capabilities`, `catalog_capability_names`, `write_capabilities`, `write_capability_egress`, `approval_required_capabilities`, `approval_required_capability_bindings`, `idempotency_required_capabilities`, `idempotency_required_capability_bindings`, and `catalog_capabilities`, so inventory review can compare configured identity with the capability catalog. In the bundled `agent.yaml`, that identity is owned by `agent_platform`, runs as `svc-support-triage-ref`, and is approved only for `search_docs` and `create_ticket`; the capability catalog then marks `search_docs` as owned by `knowledge_platform` and bound to `svc-knowledge-reader`, while `create_ticket` is owned by `support_platform` and bound to `svc-ticket-writer`. Each `catalog_capabilities` entry also carries `name`, `owner`, `mode`, `transport`, `risk_tier`, `network_access`, `tool_principal`, `approval_required`, `idempotency_key_required`, and `allowed_egress`, so reviewers can see capability identity, duplicate-write posture, and egress posture in the same response. For the running duplicate-ticket thread, that means `create_ticket` is visible as support-owned, high-risk, brokered, bound to `svc-ticket-writer`, and requiring an idempotency key before a write can be safely retried or reconciled; `approval_required_capability_bindings` and `idempotency_required_capability_bindings` repeat that write-capability owner and tool-principal binding directly, and `write_capability_egress` repeats its brokered `tickets.internal` egress target, so operators do not have to scan the full catalog list first. The identity/catalog loaders validate this shape with errors such as `'agent' must be a mapping`, `agent.id must be a string`, `agent.id is required`, `agent.display_name is required`, `agent.owner_team is required`, `agent.runtime_principal is required`, `'approved_capabilities' must be a list`, `Agent inventory config must be a mapping`, `Agent identity config must be a mapping`, `approved_capabilities entries must be strings`, `approved_capabilities entries must not be empty`, `approved_capabilities entries must be unique`, `approved_capabilities lookup must be a string`, `'capabilities' must be a mapping`, `Capability spec for {name!r} must be a mapping`, `Capability names must be strings`, `Capability name must not be empty`, `Capability names must be unique`, `Capability catalog entries must be CapabilitySpec`, `capabilities.{capability_name}.{key} must be a string`, `capabilities.{capability_name}.{key} is required`, `{label}.{key} must be a string`, `{label} must be a string`, and `capabilities.{capability_name}.timeout_seconds must be positive`, `'{label}.{key}' must be an integer`, and `'{label}.{key}' must be a boolean`, `{label}.approval must be a string`, `{label}.approval must not be empty`, `{label}.approval is not supported: {approval}`, `'allowed_egress' must be a list`, `allowed_egress entries must be strings`, `allowed_egress entries must not be empty`, and `allowed_egress entries must be unique`.

Inspect lifecycle artifacts that mirror Part VIII, including runtime-control linkage, release identity, failed-run gate signals, and explicit failed-run gap reporting:

```bash
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref check-controls --signal policy_traces_present=false
.venv/bin/python -m agent_runtime_ref check-change --signal offline_eval_passed=false
.venv/bin/python -m agent_runtime_ref check-change --signal failed_run_drill_checked=false
.venv/bin/python -m agent_runtime_ref check-retirement --step revoke_egress=false
```

`inspect-lifecycle` now also surfaces the `sandbox_profile` contract from `runtime-controls.yaml`, including `sandbox_profile.workspace_entries` and `sandbox_profile_summary` (`workspace_paths`, `shell`, `network`, `secrets`, `snapshot`), plus `artifact_bundle.bundle_name`, `artifact_bundle.version`, `artifact_bundle.provenance_required`, `artifact_bundle.signed`, `artifact_bundle.review_evidence_keys`, `artifact_bundle.review_evidence` with `duplicate_ticket_guard`, `artifact_bundle.sandbox_profile_review_evidence`, `artifact_bundle.duplicate_ticket_guard_evidence`, `change.change_type`, `change.risk_level`, `change.rollout_strategy`, `change.affected_surfaces`, `change.required_signals`, `change.approval_roles`, `change.session_control_owner` (`support-ops`), `change.emergency_freeze_owner`, `artifact_bundle.session_control_owner`, `retirement.session_control_owner`, `retirement.emergency_freeze_owner`, `failed_run_archive_targets`, `controls.failed_run_control_expectations`, `controls.failed_run_control_domains`, `controls.failed_run_control_count`, `controls.failed_run_control_summary`, `controls.failed_run_control_status`, `controls.failed_run_control_review_required`, `controls.failed_run_control_owner`, `controls.failed_run_control_source`, `controls.failed_run_control_last_review`, `controls.failed_run_control_next_review`, `controls.failed_run_control_release_binding`, `controls.support_duplicate_control_expectations`, `controls.support_duplicate_control_domains`, `controls.support_duplicate_control_count`, `controls.support_duplicate_control_summary`, `controls.support_duplicate_control_status`, and `controls.support_duplicate_control_release_binding`, so operators can see ownership, freeze responsibility, retention, trace/provenance control, and duplicate-ticket evidence controls in the same lifecycle summary.
The same runtime-control summary is backed by `runtime-controls.yaml`, including `pause_allowed`, `resume_allowed`, `background_mode_allowed`, `max_wait_seconds`, `on_expiry`, `contract_version`, `capability_session_owner`, `capability_sessions`, `track_session_ids`, `resume_allowed`, `allow_progress_events`, `allow_elicitation`, `on_session_expiry: reinitialize_or_cancel`, `expiry_policy`, and `expiry_signal_owner`, so resumable capability sessions expose their progress, elicitation, and expiry assumptions rather than leaving them implicit. Its `delegated_authorization` defaults are explicit too: `authorization_mode` is `user_delegated_or_platform_owned`, `delegated_principal_policy` is `explicit_principal_binding_required`, `token_reuse_policy` is `reuse_within_valid_paused_run_only`, `on_authorization_revoke` is `cancel_or_reapprove`, `subagent_inheritance` is `denied_by_default`, and resumable/reinit flows use `resume_existing_session_if_valid`. The sandbox-profile loader validates those runtime-control shapes with `runtime_controls config must be a mapping`, `runtime_controls.sandbox_profile config must be a mapping`, `runtime_controls.sandbox_profile.{key} config must be a mapping`, `runtime_controls.sandbox_profile.workspace.entries must be a list`, and direct construction rejects malformed sandbox roots with `Sandbox profile config must be a mapping`, malformed sandbox sections with `Sandbox profile {key} config must be a mapping`, malformed sandbox evidence values with `Sandbox profile {section}.{key} must be a string`, or malformed workspace entries with `Sandbox profile workspace entries must be a list`.
`check-change` returns `change_id`, `ready`, `required_signals`, `approval_roles`, `missing_signals`, `failed_run_signals`, `missing_failed_run_signals`, `support_duplicate_signals`, `missing_support_duplicate_signals`, `support_duplicate_signals_ready`, `rollout_strategy`, and `risk_level`; its required signals include `duplicate_ticket_eval_passed`, so duplicate-ticket regression evidence is checked at change readiness as well as rollout readiness.
Lifecycle list loaders reject malformed, blank, and duplicate entries with `{key} must be a list`, `{key} entries must be strings`, `{key} entries must not be empty`, and `{key} entries must be unique`. `check-retirement` returns `system_id`, `ready`, `triggers`, `missing_steps`, `required_steps`, `archive_targets`, `failed_run_archive_targets`, `support_duplicate_archive_targets`, and `replacement_mode`, so operators can confirm which telemetry/session/approval/control-bundle records must survive retirement for later degraded-path and duplicate-ticket review.
`check-controls` returns `healthy`, `required_controls`, `blocked_findings_expected`, `missing_controls`, `failed_run_controls`, `preserved_failed_run_controls`, `failed_run_controls_healthy`, `support_duplicate_controls`, `preserved_support_duplicate_controls`, `support_duplicate_controls_healthy`, `blocking_findings`, and `inventory_drift`; the nested `inventory_drift` object exposes `has_drift`, `missing_from_catalog`, and `missing_from_inventory`, so trace/provenance-related control gaps and capability inventory mismatches can be reviewed separately from generic control hygiene. Its `controls.yaml` inputs require `registry_reviewed`, `capability_owners_confirmed`, `memory_provenance_enforced`, `policy_traces_present`, `duplicate_ticket_eval_passed`, and `idempotency_keys_present`, with validation shapes `'controls' must be a mapping`, `'controls.require' must be a list`, `'controls.block_if' must be a list`, `{label} entries must be strings`, `{label} entries must not be empty`, and `{label} entries must be unique`, while the controls policy normalizes them into `required_controls`; `block_if` treats `direct_tool_access_present` and `unmanaged_runtime_present` as hard blockers, is summarized as `blocked_findings_expected`, and becomes `blocking_findings` during evaluation.

Inspect memory records:

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

`inspect-memory` now returns `config_dir`, `count`, `memory_ids`, and `records`; each record shows not only content, but also `provenance` and `revision`.
`dump-events` now returns `trace_id`, `status`, `result`, `event_count`, `event_types`, `failure_reason`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys`, and `events` in its JSON output for degraded-path drills.

Dump structured events for one run:

```bash
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
.venv/bin/python -m agent_runtime_ref dump-events --simulate-failure tool_timeout
```

Export events to JSONL for later inspection and replay:

```bash
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-events --simulate-failure upstream_unavailable --output artifacts/trace-demo-failed.jsonl
```

`export-events` returns `output_path`, `trace_id`, `session_id`, `tenant_id`, `principal_id`, `agent_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `status`, `result`, `event_count`, `event_types`, `redact_fields`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys`, and optional `failure_reason`, so redaction and degraded-path evidence are visible in the command summary.

If you need a redacted export for external review, you can hide sensitive fields at export time:

```bash
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl --redact-field user_input
```

Inspect a single trace from a JSONL file:

```bash
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
```

Replay a run from a saved trace:

```bash
.venv/bin/python -m agent_runtime_ref replay-run --input artifacts/trace-demo.jsonl
```

`dump-events` returns `status`, `result`, `failure_reason`, `trace_id`, `session_id`, `tenant_id`, `principal_id`, `agent_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `event_count`, `event_types`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys`, and `events`; `inspect-trace` returns `trace_id`, `session_id`, `tenant_id`, `principal_id`, `agent_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `status`, `output_preview`, `event_count`, `event_types`, `failure_reason`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys`, and `events`; `export-events` likewise summarizes `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, and `idempotency_keys` next to `redact_fields`, so approval lineage, approval capability lineage, approval status, and duplicate-write lineage are visible before an operator drills into individual payloads. `replay-run` returns `source_trace_id`, `replay_trace_id`, `source_session_id`, `replay_session_id`, `source_tenant_id`, `replay_tenant_id`, `source_principal_id`, `replay_principal_id`, `source_agent_id`, `replay_agent_id`, `source_authorization_mode`, `replay_authorization_mode`, `source_delegated_principal_id`, `replay_delegated_principal_id`, `source_delegated_scope`, `replay_delegated_scope`, `status`, `result`, `source_status`, `source_output_preview`, `source_failure_reason`, `replay_status`, `replay_output_preview`, `replay_failure_reason`, `event_count`, `event_types`, `source_event_count`, `source_event_types`, `replay_event_count`, `replay_event_types`, `idempotency_keys`, `source_idempotency_keys`, `replay_idempotency_keys`, `approval_ids`, `source_approval_ids`, `replay_approval_ids`, `pending_approval_ids`, `source_pending_approval_ids`, `replay_pending_approval_ids`, `approval_capability_names`, `source_approval_capability_names`, `replay_approval_capability_names`, `pending_approval_capability_names`, `source_pending_approval_capability_names`, `replay_pending_approval_capability_names`, `approval_status_counts`, `source_approval_status_counts`, and `replay_approval_status_counts`, so investigation and replay preserve source/run approval capability and status lineage while making the original and replay write keys comparable.

Rollout policy check with signal overrides:

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

The rollout check returns `ready`, `required_checks`, `blocked_checks`, `missing_required`, `support_duplicate_required`, `missing_support_duplicate_required`, `support_duplicate_required_ready`, `blocking_signals`, and `rollout_mode`; its required evidence includes `duplicate_ticket_eval_passed`, so automation can tell absent duplicate-ticket regression evidence apart from explicitly blocked signals; signal overrides accept boolean `key=value` pairs and reject unknown boolean text with `Unsupported boolean value in signal: {raw_signal!r}`. Runtime CLI failure paths keep their operator-facing messages stable too: `Config path must be a string or path-like object`, `Session output path must be a string or path-like object`, `Telemetry path must be a string or path-like object`, `CLI field must be a string: {field}`, `CLI field is required: {field}`, `CLI field is not supported: {field}={value}; expected one of: {expected}`, `CLI field must be an integer: {field}`, `CLI field must be non-negative: {field}`, `CLI field entries must be a sequence: {field}`, `CLI field entries must be unique: {field}`, `Runtime request must be RunRequest`, `Run request field must be a string: {field}`, `Run request field is required: {field}`, `Delegated authorization field is required: {field}`, `Signal must be a string`, `Signal must use key=value format: {raw_signal!r}`, `Signal key must not be empty: {raw_signal!r}`, `Background request must be RunRequest`, `Background context must be RunContext`, `Background model_output must be ModelOutput`, `Background context tool_results must be a list`, `Background context tool_results entries must be ToolResult`, `Background memory_store must be MemoryStore`, `Background policy must be PolicyEngine`, `Background telemetry must be TelemetryEmitter`, `Runtime catalog must be CapabilityCatalog`, `Runtime policy must be PolicyEngine`, `Runtime telemetry must be TelemetryEmitter`, `Runtime memory must be MemoryStore`, `Runtime approvals must be ApprovalQueue`, `Runtime sessions must be SessionStore`, `Runtime agent must be AgentIdentity`, `Runtime background must be BackgroundWorker`, `Approval queue policy must be ApprovalPolicy`, `Approval policy config must be a mapping`, `Capability catalog config must be a mapping`, `Controls policy config must be a mapping`, `Memory store config must be a mapping`, `Policy config must be a mapping`, `Rollout policy config must be a mapping`, `Telemetry event must be a mapping`, `Approval field must be a string: {field}`, `Approval field is required: {field}`, `Approval status is not supported: {status}`, `Approval decision is not supported: {decision}`, `Policy action is not supported: {action}`, `Policy field must be a string: {field}`, `Policy field is required: {field}`, `Tool capability must be CapabilitySpec`, `Tool request must be ToolRequest`, `Tool policy decision must be PolicyDecision`, `Policy precheck request must be RunRequest`, `Policy context must be RunContext`, `Policy tool request must be ToolRequest`, `Policy capability must be CapabilitySpec`, `Tool request capability name must be a string`, `Tool request capability name must not be empty`, `Tool request arguments must be a mapping`, `Tool request argument key must be a string`, `Tool request argument key must not be empty`, `Tool request argument keys must be unique`, `Tool request argument value must be a string: {argument_key}`, `Tool request capability does not match catalog entry: {capability_name} != {capability.name}`, `Tool result status must be a string`, `Tool result status must not be empty`, `Tool result payload must be a mapping`, `Tool result payload key must be a string`, `Tool result payload key must not be empty`, `Tool result payload keys must be unique`, `Tool result payload value must be a string: {payload_key}`, `Approval request not found: {approval_id}`, `Approval request is not pending: {approval_id}`, `No pending approval requests were generated for this run`, `Session field must be a string: {field}`, `Session field is required: {field}`, `Session status is not supported: {status}`, `Session tenant_id does not match existing session: {session_id}`, `Session principal_id does not match existing session: {session_id}`, `Session trace_id already exists: {trace_id}`, `Session field entries must be a sequence: {field}`, `Session field entries must be unique: {field}`, `Session field entries must be unique: session_id`, `Session runs must be a sequence`, `Session runs entries must be RunRecord`, `Session field entries must be a sequence: session_id`, `Session eval specs must be a mapping`, `Session not found: {session_id}`, `Telemetry event field must not be empty: event_type`, `Telemetry event field must not be empty: trace_id`, `Telemetry event field must not be empty: schema_version`, `Telemetry schema version is not supported: {schema_version}`, `Telemetry redact field must not be empty`, `Trace ID request must be a string`, `Trace ID not found in event file: {requested_trace_id}`, `Trace file contains multiple trace IDs; pass --trace-id explicitly`, `Trace file does not contain a run_start event`, `Model step must return ModelOutput`, `Model output text must be a string`, and `Model output tool_request must be ToolRequest`.

Continuous controls and registry drift check:

```bash
.venv/bin/python -m agent_runtime_ref check-controls --signal registry_reviewed=false
```

Inspect and resolve demo approval requests:

```bash
.venv/bin/python -m agent_runtime_ref inspect-approvals
.venv/bin/python -m agent_runtime_ref resolve-approval --decision approved --note "manager approved demo request"
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref inspect-session --simulate-failure tool_timeout
.venv/bin/python -m agent_runtime_ref session-eval-summary
.venv/bin/python -m agent_runtime_ref session-eval-summary --simulate-failure tool_timeout
.venv/bin/python -m agent_runtime_ref session-replay --user-input "Please create a ticket for this onboarding issue." --user-input "What language preference do you remember?"
.venv/bin/python -m agent_runtime_ref session-replay --simulate-failure tool_timeout --user-input "Please create a ticket for this issue."
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-session --simulate-failure tool_timeout --output artifacts/session-demo-failed.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --scenario failed_run_timeout --output artifacts/eval-failed-run.json
```

`inspect-approvals` now returns `trace_id`, `session_id`, `tenant_id`, `agent_id`, `count`, `approval_ids`, `pending_approval_ids`, `approval_capability_names`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys`, and `approvals`, including `tenant_id`, `agent_id`, capability-session lifecycle fields (`capability_session_id`, `capability_session_status`), delegated authorization context such as `authorization_mode`, `delegated_principal_id`, and `delegated_scope`, and `idempotency_key`, so approval review can be compared directly with session evidence and duplicate-write intent. `resolve-approval` returns `approval_id`, `approval_ids`, `trace_id`, `session_id`, `tenant_id`, `agent_id`, `capability_name`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `requested_by`, `status`, `reviewer`, `resolution_note`, `capability_session_id`, `capability_session_status`, the same delegated context, `idempotency_key`, `idempotency_keys`, and `approval_status_counts` after decision, so approval closure does not drop capability-session, acting-identity, or idempotency lineage.
`inspect-session` shows session-level run history and the linked `trace_id` values. Failed drills can now be injected there too, and the summary preserves `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `latest_failure_reason`, and per-run `output_text`, `failure_reason`, `request_agent_id`, `capability_session_id`, `capability_session_status`, and `idempotency_key`.
`session-eval-summary` returns a compact operational summary for the run series, including failed runs and `traceable_failed_runs` rather than collapsing everything into success-versus-denied. Failed drills can now be injected there directly too, and the summary surfaces `latest_failure_reason` for quick review.
`session-replay` lets you execute multiple related requests inside one `session_id`. Failed drills can now be injected there too, and the replay summary preserves `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, and `latest_failure_reason` alongside per-run `failure_reason` and `request_agent_id`.
`export-session` writes the session as structured JSON that can already serve as a seed for offline eval workflows. It now also preserves capability-session lifecycle fields (`capability_session_id`, `capability_session_status`), delegated authorization context such as `authorization_mode`, `delegated_principal_id`, and `delegated_scope`, `idempotency_key`, and `approval_id`, and the command summary now surfaces `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, and `latest_failure_reason` for failed drills.

The session and eval commands expose their summary fields explicitly: `inspect-session` returns `session_id`, `tenant_id`, `principal_id`, `trace_count`, `trace_ids`, `failed_trace_ids`, `latest_status`, `latest_failure_reason`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `summary`, and `runs`; `session-eval-summary` returns `session_id`, `total_runs`, `success_runs`, `approval_wait_runs`, `denied_runs`, `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `latest_status`, `latest_trace_id`, and `latest_failure_reason`; `session-replay` returns `session_id`, `run_count`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `latest_failure_reason`, `summary`, and `runs`; `export-session` returns `output_path`, `session_id`, `total_runs`, `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `latest_trace_id`, and `latest_failure_reason`; exported session JSON also carries top-level `total_runs`, `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `latest_failure_reason`, `latest_trace_id`, and the `session` identifier alongside the nested `summary`; and `export-eval-dataset` returns `dataset_name`, `output_path`, `session_count`, `session_ids`, `run_count`, `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `duplicate_ticket_scenarios`, `latest_failure_reason`, and `sessions` as a session ID list, while the exported eval dataset artifact carries top-level `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, and `latest_failure_reason`, and each exported eval session payload carries top-level `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, and `approval_status_counts` beside `summary.trace_ids`, `summary.failed_trace_ids`, `summary.idempotency_keys`, `summary.approval_ids`, `summary.approval_capability_names`, `summary.pending_approval_ids`, `summary.pending_approval_capability_names`, and `summary.approval_status_counts`, while each exported eval session payload also carries `session` and an `eval` block with `scenario`, `labels`, `expected_outcomes`, and `grading_rules`, and nested run records retain per-run `request_agent_id` and `user_input`; by default `dataset_name` is `agent-runtime-ref-eval-seed`, unless the caller passes `--dataset-name`; eval export also validates the internal `session_prefix` seed before generating session IDs, and session commands validate the internal `trace_prefix` seed before generating trace IDs.

The runtime now also treats failure-like tool paths, such as validation failures, as first-class run outcomes. Instead of pretending the run succeeded, it records a failed run, emits an explicit `run_failed` event plus terminal `run_complete.failure_reason` for failed or denied runs, and keeps both that status and the concrete failure reason visible as `failure_reason` in session export, trace inspection, replay summaries, and CLI output.
`export-eval-dataset` bundles several built-in session scenarios into one eval-ready JSON artifact, including a dedicated failed-run drill scenario carrying `duplicate_ticket_eval_passed`, `max_ticket_side_effects: 1`, and a blocking `duplicate_ticket_guard`, a profile lookup scenario (`profile_memory`) with `memory_read`, `profile_lookup`, and `grounded_answer` labels, a multi-run approval-plus-memory scenario (`mixed_session`) with `multi_run`, `approval_then_memory`, and `session_evals` labels plus `required_run_count` and `approval_status_counts` as expected outcomes, and an approval-backed `support_ticket` scenario with a `sandbox_profile_review` label, `sandbox_profile_reviewed` expected outcome, and blocking `sandbox_profile_review` grading rule, and its command summary now surfaces aggregate `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, and `latest_failure_reason` too.

That eval path should now be read together with the richer verifier contract in the appendix: for long-horizon scenarios, the package is meant to illustrate how a dataset can eventually carry `process_score`, `outcome_score`, `failure_attribution`, and linked verifier evidence rather than a single thin verdict.

Together, those commands now help illustrate an important runtime distinction from Chapters 16 and 17:

- the user-visible `session_id` that groups related runs,
- the per-run `trace_id` used for investigation,
- and the capability-side session state that may pause, expire, resume, or require re-initialization.

The package is still deliberately small, but it now reflects that a governed runtime may need to explain all three without collapsing them into one opaque object.

That same package is also a good place to connect the newer Anthropic harness lesson to runnable structure: long-running application work may need explicit context resets, structured handoff artifacts, and separated planner/generator/evaluator roles rather than one uninterrupted agent loop. The reference package does not implement that full harness, but it now makes the required runtime seams visible enough that a team can see where reset-safe handoff, sprint contracts, evaluator review, and resumed control state would have to live.

It is also a useful anchor for verifier-aware governance: if rollout or assurance depends on eval output, the runtime should preserve enough trace, session, and artifact linkage to explain not only what happened, but why a verifier judged the run the way it did.

That should extend through lifecycle handling too. A governed reference runtime should be able to explain which verifier contract and release identity were active for a release, what evidence must still be retained after retirement to justify earlier rollout or assurance decisions, and which structured handoff artifacts must survive context resets or role handoffs when those artifacts shaped what the retired system was allowed to do.

It also reflects a fourth operational concern: the delegated authorization context under which the action ran. That context now appears in run telemetry, approval records, and session export so the runtime can explain not only what happened, but under whose delegated identity and scope it happened.

A request that actually reads profile memory:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run --user-input "What language preference do you remember?"
```

## How to Verify It

```bash
uv run ruff check .
uv run ty check
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing
```

## Sample Configs

There are starter files for both runtime and lifecycle in [configs](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref/configs):

- [agent.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/agent.yaml)
- [policy.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/rollout.yaml)
- [controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/controls.yaml)
- [approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- [change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
  The change gate now includes explicit `failed_run_drill_checked` and `sandbox_profile_reviewed` signals so high-risk rollout review does not treat degraded paths or sandbox profile changes as out-of-scope.
- [artifacts.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/artifacts.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)
- [retirement.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/retirement.yaml)

These are no longer just static examples. `config.py` can load those YAML files into agent identity, approved inventory, the runtime, context layers, the memory store, rollout policy, release-identity-bearing lifecycle artifacts, and other lifecycle state, so the package is now closer to a real operational skeleton. The generic loaders keep malformed YAML shapes explicit too: `Config at {config_path!s} must be a mapping at the top level`, `{label} config must be a mapping`, and `{key} must be a list`.

The runtime-control bundle is also now meant to represent approval and session-governance rules explicitly, including pause/resume, background handling, expiry, re-init policy, capability-session ownership, delegated authorization assumptions, and the contract boundary between a user run and a capability-side session.

### A Minimal Sandbox Profile

If the package grows toward sandbox-backed execution, the right starting point is not a large new subsystem. It is a small profile that makes workspace and permissions explicit:

```yaml
sandbox_profile:
  manifest_version: 1
  workspace:
    entries:
      - path: repo
        source: local_dir
        read_only: false
      - path: task.md
        source: inline_file
        read_only: true
  capabilities:
    filesystem: true
    shell: restricted
    memory: read_write
    skills: read_only
  permissions:
    network: denied
    secrets: none
    run_as: sandbox_user
  state:
    resume: allowed
    snapshot: required_on_completion
    persist_session_state: true
```

This example does not turn the reference runtime into a full sandbox orchestrator. It fixes the contract surface that Chapters 9 and 16 require from a real sandbox-backed runtime: manifest, permissions, workspace materialization, session state, and snapshot/resume policy should be visible to review.

## Why This Is Useful

The book now relies not only on Markdown explanations, but also on a real code skeleton:

- it is easier to discuss architecture at the level of files and contracts;
- it is easier to extend the package with more examples;
- it is easier to move from a chapter to a runnable prototype;
- it is easier to show a config-driven path instead of only a hardcoded demo;
- it is easier to connect the reference runtime to the chapters about memory, retrieval, background updates, and runtime-control governance;
- it is easier to discuss where each memory record came from, which revision it represents, and which contract/runtime-control version was active;
- it is easier to keep release identity, verifier-contract lineage, and retirement obligations visible alongside runtime-control and artifact decisions;
- it is easier to make approval state, runtime session state, capability session state, and verifier evidence visible as separate but linked control concepts.

There is also a practical usability win now:

- `inspect-memory` shows seeded memory and filtering by `tenant` and `memory_class`;
- `dump-events` shows the structured trace of one run without reading the source code;
- `export-events` persists that trace as JSONL for external inspection;
- `export-events` now includes `schema_version` and supports export-time redaction for selected fields;
- the approval-backed `export-events` path emits `sandbox_profile_reviewed`, so trace evidence matches the lifecycle bundle and eval grading rule;
- `inspect-trace` reads and filters saved traces;
- `replay-run` reconstructs a run from the saved `run_start` event.

The simplest way to read this package is:

- use the book for architecture, sequence, and operating-model argument;
- use this package for runnable structure, config surfaces, and inspection examples;
- use the appendix schemas to understand the contract boundaries the runtime is trying to make explicit.

## What to Do Next

- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)
- [Policy Bundle Schema and Approval Contract](policy-bundle-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)


Runtime literal markers also include `eval_gate` and `session_idempotency_summary` for eval and idempotency evidence parity.
