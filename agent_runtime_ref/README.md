# agent_runtime_ref

Small runnable reference runtime for Parts VII and VIII of the book.

## What it is

This package is not a production framework. It is a compact code anchor for:

- runtime structure
- policy and capability control
- approval pause/resume flow
- rollout gates
- lifecycle artifacts
- trace/session/eval exports

The full narrative lives in the book and appendix pages. This README is only a local developer quickstart.

For the record-linkage view across traces, approvals, evals, incidents, and rollout judgment, read [Evidence Spine: From Request to Rollout Judgment](../docs/book/part-v/evidence-spine.en.md).

## Quickstart

From the repository root:

```bash
python3 -m agent_runtime_ref
```

Other useful commands:

```bash
python3 -m agent_runtime_ref inspect-agent
python3 -m agent_runtime_ref inspect-memory --memory-class profile
python3 -m agent_runtime_ref inspect-approvals
python3 -m agent_runtime_ref inspect-lifecycle
python3 -m agent_runtime_ref inspect-session --simulate-failure tool_timeout
python3 -m agent_runtime_ref check-controls --signal policy_traces_present=false
python3 -m agent_runtime_ref check-change --signal failed_run_drill_checked=false
python3 -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
python3 -m agent_runtime_ref simulate-run --simulate-failure tool_timeout
python3 -m agent_runtime_ref dump-events --simulate-failure upstream_unavailable
python3 -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
python3 -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
python3 -m agent_runtime_ref export-events --simulate-failure upstream_unavailable --output /tmp/agent-runtime-failed-trace.jsonl
python3 -m agent_runtime_ref replay-run --input artifacts/trace-demo.jsonl
python3 -m agent_runtime_ref session-eval-summary --simulate-failure tool_timeout
python3 -m agent_runtime_ref session-replay --simulate-failure tool_timeout --user-input "Please create a ticket for this issue."
python3 -m agent_runtime_ref export-session --simulate-failure tool_timeout --output /tmp/agent-runtime-failed-session.json
python3 -m agent_runtime_ref export-eval-dataset --output /tmp/agent-runtime-eval.json
python3 -m agent_runtime_ref export-eval-dataset --scenario failed_run_timeout --output /tmp/agent-runtime-failed-eval.json
```

The failure-injection flags are intentionally small, but useful for the book's failure-rich runtime examples: they let the reference runtime execute explicit failed runs, emit `run_failed` trace events, and keep the concrete failure reason visible in runtime output and CLI JSON as `failure_reason` instead of collapsing everything into happy-path or approval-wait scenarios. Common deterministic overrides include `--config-dir`, `--agent-id`, `--tenant-id`, `--principal-id`, `--trace-id`, and `--session-id`; signal overrides accept boolean `key=value` pairs, reject empty keys with `Signal key must not be empty: {raw_signal!r}`, and reject unknown boolean text with `Unsupported boolean value in signal: {raw_signal!r}`. Specialized selectors include `--limit`, `--approval-id`, `--replay-trace-id`, `--trace-prefix`, and `--session-prefix`. Runtime CLI failure paths keep their operator-facing messages stable too: `Signal must use key=value format: {raw_signal!r}`, `CLI field is not supported: {field}={value}; expected one of: {expected}`, `CLI field must be non-negative: {field}`, `{label}.{key} is required`, `{label}.{key} must be positive`, `'{label}' must be a list`, `{label} config keys must be strings`, `{label} keys must be strings`, `{label} entries must be strings`, `{label} entries must not be empty`, `{label} entries must be unique`, `approvals.default_reviewer must be a string`, `approvals.default_reviewer is required`, `approvals.escalation_sla_minutes must be an integer`, `approvals.escalation_sla_minutes must be positive`, `Approval field must be a string: {field}`, `Approval field is required: {field}`, `Assessment signal key must be a string`, `Assessment signal key must not be empty`, `Assessment signal keys must be unique`, `Assessment signal value must be a boolean: {field}`, `Rollout readiness flag must be a boolean: {field}`, `Authorization mode is not supported: {authorization_mode}`, `Policy action is not supported: {action}`, `Policy memory kind must be a string`, `Policy memory kind must not be empty`, `Tool request capability name must be a string`, `Tool request capability name must not be empty`, `Tool request arguments must be a mapping`, `Tool request argument key must be a string`, `Tool request argument key must not be empty`, `Tool request argument value must be a string: {argument_key}`, `Tool request capability does not match catalog entry: {capability_name} != {capability.name}`, `Approval request not found: {approval_id}`, `Approval request is not pending: {approval_id}`, `No pending approval requests were generated for this run`, `Session field must be a string: {field}`, `Session status is not supported: {status}`, `Session tenant_id does not match existing session: {session_id}`, `Session principal_id does not match existing session: {session_id}`, `Session trace_id already exists: {trace_id}`, `Session field entries must be unique: {field}`, `Session field entries must be unique: session_id`, `Session not found: {session_id}`, `Telemetry event line is not valid JSON: {line_number}`, `Telemetry event must be a mapping`, `Telemetry event payload must be a mapping`, `Telemetry event redacted_fields must be a tuple`, `Telemetry event payload key must be a string`, `Telemetry event payload key must not be empty`, `Telemetry event payload keys must be unique`, `Telemetry event payload value must be a string: {payload_key}`, `redacted_fields entries must be strings`, `Telemetry event is missing required field: {required_field}`, `Telemetry event field must be a string: {field}`, `Telemetry event field must not be empty: {field}`, `Telemetry event field must not be empty: {required_field}`, `Telemetry event field must not be empty: event_type`, `Telemetry event field must not be empty: trace_id`, `Telemetry event field must not be empty: schema_version`, `Telemetry schema version is not supported: {schema_version}`, `Telemetry redact field must not be empty`, `Telemetry redact field is not present in events: {missing}`, `Trace ID not found in event file: {requested_trace_id}`, `Trace file does not contain any trace IDs`, `Trace file contains multiple trace IDs; pass --trace-id explicitly`, `Trace file does not contain a run_start event`, `Trace file contains multiple run_start events`, `Trace run_start event is missing replay fields: {missing_keys}`, `Trace run_start event has redacted replay fields: {redacted_keys}`, `Trace run_start replay field must be a string: {field}`, `Trace run_start replay field must not be empty: {field}`, `runtime_controls config must be a mapping`, `runtime_controls.sandbox_profile config must be a mapping`, `runtime_controls.sandbox_profile.{key} config must be a mapping`, `runtime_controls.sandbox_profile.workspace.entries must be a list`, `Sandbox profile workspace entries must be a list`, and `Model step must return ModelOutput`.

The baseline runtime commands document their top-level JSON fields too: `inspect-agent` returns `agent_id`, `display_name`, `owner_team`, `runtime_principal`, `approved_capabilities`, and `catalog_capabilities` with nested `name`, `owner`, `risk_tier`, `network_access`, `tool_principal`, and `allowed_egress`; the bundled capability owners are `knowledge_platform` for `search_docs` and `support_platform` for `create_ticket`; identity/catalog config validation keeps the same shape explicit (`'agent' must be a mapping`, `agent.id must be a string`, `agent.id is required`, `agent.display_name is required`, `agent.owner_team is required`, `agent.runtime_principal is required`, `'approved_capabilities' must be a list`, `approved_capabilities entries must be strings`, `approved_capabilities lookup must be a string`, `approved_capabilities entries must not be empty`, `approved_capabilities entries must be unique`, `'capabilities' must be a mapping`, and `Capability spec for {name!r} must be a mapping`, `Capability names must be strings`, `Capability name must not be empty`, `Capability names must be unique`, `capabilities.{capability_name}.{key} must be a string`, `capabilities.{capability_name}.{key} is required`, `{label}.{key} must be a string`, `{label} must be a string`, `{label} is required`, `capabilities.{capability_name}.timeout_seconds must be positive`, `'{label}.{key}' must be an integer`, `'{label}.{key}' must be a boolean`, `{label}.approval must be a string`, `{label}.approval must not be empty`, `{label}.approval is not supported: {approval}`, `'allowed_egress' must be a list`, `allowed_egress entries must be strings`, `allowed_egress entries must not be empty`, and `allowed_egress entries must be unique`); `simulate-run` returns `agent_id`, `config_dir`, `trace_id`, `session_id`, `status`, `result`, `events`, `memory_records`, `pending_approvals`, and optional `failure_reason`; `export-events` returns `output_path`, `trace_id`, `status`, `result`, `event_count`, `redact_fields`, and optional `failure_reason`; `inspect-trace` returns `trace_id`, `event_count`, and `events`; and `replay-run` returns `source_trace_id`, `replay_trace_id`, `status`, `result`, and `event_count`.

That same line now also reaches the rollout/change side of the package: the demo `change.yaml` includes `failed_run_drill_checked` and `sandbox_profile_reviewed` gate signals so degraded paths and sandbox profile changes are part of release review, not afterthoughts. `check-rollout` reports `ready`, `missing_required`, `blocking_signals`, and `rollout_mode` after normalizing rollout blockers into `blocked_checks` so release automation can distinguish missing evidence from explicitly blocking signals. `inspect-lifecycle` now surfaces failed-run gate signals, `background_mode_allowed`, `capability_session_owner`, `capability_sessions.track_session_ids`, `on_session_expiry: reinitialize_or_cancel`, and the `sandbox_profile` contract from `runtime-controls.yaml`, `artifact_bundle.review_evidence`, `artifact_bundle.sandbox_profile_review_evidence`, `change.affected_surfaces`, `change.session_control_owner` (`support-ops`), `change.emergency_freeze_owner`, `artifact_bundle.session_control_owner`, `retirement.session_control_owner`, `retirement.emergency_freeze_owner`, and `failed_run_archive_targets` directly, adds `controls.failed_run_control_expectations`, `controls.failed_run_control_domains`, `controls.failed_run_control_count`, `controls.failed_run_control_summary`, `controls.failed_run_control_status`, `controls.failed_run_control_review_required`, `controls.failed_run_control_owner`, `controls.failed_run_control_source`, `controls.failed_run_control_last_review`, `controls.failed_run_control_next_review`, and `controls.failed_run_control_release_binding` for the trace/provenance side of lifecycle review, `check-change` reports `change_id`, `ready`, `missing_signals`, `missing_failed_run_signals`, `rollout_strategy`, and `risk_level`, `check-retirement` reports `system_id`, `ready`, `missing_steps`, `failed_run_archive_targets`, and `replacement_mode`, and `check-controls` now reports `healthy`, `missing_controls`, `failed_run_controls`, `preserved_failed_run_controls`, `failed_run_controls_healthy`, `blocking_findings`, and `inventory_drift`, so operators can see lifecycle and control-plane expectations without opening the YAML first.

The eval export now also includes a dedicated failed-run scenario, the profile lookup scenario `profile_memory` with `memory_read`, `profile_lookup`, and `grounded_answer` labels, the multi-run approval-plus-memory scenario `mixed_session` with `multi_run`, `approval_then_memory`, `session_evals`, and `required_run_count`, and the approval-backed `support_ticket` scenario with a blocking `sandbox_profile_review` grading rule, so the same reference package can demonstrate not only failed traces, but failed-run judgment artifacts, memory retrieval, approval waits, and session summaries with `traceable_failed_runs`. That path is now covered by the local pytest suite too, so the package's degraded-path examples are executable rather than only described, and the same failed condition is surfaced consistently through `failure_reason` in session export and CLI output. The `export-eval-dataset` command summary now also returns aggregate `failed_runs`, `traceable_failed_runs`, and `latest_failure_reason`, so operators can confirm degraded-path coverage without opening the JSON artifact first.

The same is now true for `inspect-session`, `session-eval-summary`, `session-replay`, and `export-session`: failed drills can be replayed directly into session-level inspection surfaces, and the command summaries surface `failed_runs`, `traceable_failed_runs`, and the latest failure reason instead of leaving the operator to inspect raw JSON first. Runtime requests reject malformed or blank operator input with `Run request field must be a string: {field}` and `Run request field is required: {field}` before telemetry or session evidence is written, and user-delegated runs reject missing acting identity with `Delegated authorization field is required: {field}`. Those session surfaces also keep per-run `output_text` and delegated-authorization context next to failed-run evidence, so operators can review result text, failure cause, and acting identity in one place. `inspect-approvals` now follows that same line by returning `trace_id`, `session_id`, `count`, and `approvals` with capability-session lifecycle fields plus delegated authorization context, and `resolve-approval` returns `approval_id`, `status`, `reviewer`, `resolution_note`, `capability_session_id`, `capability_session_status`, `authorization_mode`, `delegated_principal_id`, and `delegated_scope` after a decision so approval lineage stays visible through closure as well.
The adjacent session and eval commands now document their top-level summaries too: `inspect-session` returns `session_id`, `tenant_id`, `principal_id`, `trace_count`, `latest_status`, `summary`, and `runs`; `session-eval-summary` returns `session_id`, `total_runs`, `success_runs`, `approval_wait_runs`, `denied_runs`, `failed_runs`, `traceable_failed_runs`, `latest_status`, `latest_trace_id`, and `latest_failure_reason`; `session-replay` returns `session_id`, `run_count`, `summary`, and `runs`; `export-session` returns `output_path`, `session_id`, `total_runs`, `failed_runs`, `traceable_failed_runs`, `latest_trace_id`, and `latest_failure_reason`; and `export-eval-dataset` returns `dataset_name`, `output_path`, `session_count`, `run_count`, `failed_runs`, `traceable_failed_runs`, `latest_failure_reason`, and `sessions`; its default `dataset_name` is `agent-runtime-ref-eval-seed` unless `--dataset-name` overrides it.

## Tests

Project test config lives at the repository root in `pyproject.toml`.

Install dev dependencies first, for example with `uv`:

```bash
uv sync --group dev
uv run pytest
```

Or with pip:

```bash
python3 -m pip install -e .
python3 -m pip install pytest pytest-cov
python3 -m pytest
```

## Reading path

- Chapter 17, policy layer and capability contracts
- Chapter 18, rollout gates around approval and runtime behavior
- Chapter 21, assurance response
- Chapter 22, artifact and lifecycle linkage
