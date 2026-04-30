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
{"result": "Ticket request accepted and ready for follow-up.", "status": "success", "events": 9, "memory_records": 4, "config_dir": ".../agent_runtime_ref/configs"}
```

Explicit runtime execution via subcommand:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref simulate-run --simulate-failure tool_timeout
```

The second form is a deliberately small failure-rich scenario. It lets the package demonstrate how an otherwise allowed capability can still end as a governed failed run with explicit telemetry instead of disappearing behind a generic success path.

Inspect the agent identity and approved inventory:

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
```

Inspect lifecycle artifacts that mirror Part VIII, including runtime-control linkage, release identity, failed-run gate signals, and explicit failed-run gap reporting:

```bash
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref check-controls --signal policy_traces_present=false
.venv/bin/python -m agent_runtime_ref check-change --signal offline_eval_passed=false
.venv/bin/python -m agent_runtime_ref check-change --signal failed_run_drill_checked=false
.venv/bin/python -m agent_runtime_ref check-retirement --step revoke_egress=false
```

`inspect-lifecycle` now also surfaces the `sandbox_profile` contract from `runtime-controls.yaml`, `artifact_bundle.review_evidence`, `artifact_bundle.sandbox_profile_review_evidence`, `change.affected_surfaces`, `change.session_control_owner`, `change.emergency_freeze_owner`, `artifact_bundle.session_control_owner`, `retirement.session_control_owner`, `retirement.emergency_freeze_owner`, `failed_run_archive_targets`, `controls.failed_run_control_expectations`, `controls.failed_run_control_domains`, `controls.failed_run_control_count`, `controls.failed_run_control_summary`, `controls.failed_run_control_status`, `controls.failed_run_control_review_required`, `controls.failed_run_control_owner`, `controls.failed_run_control_source`, `controls.failed_run_control_last_review`, and `controls.failed_run_control_next_review`, so operators can see ownership, freeze responsibility, retention, and trace/provenance control in the same lifecycle summary.
`check-change` now also breaks out `missing_failed_run_signals`, so degraded-path rollout gaps stay visible as their own review category rather than hiding inside a generic missing-signal list.
`check-retirement` now also surfaces `failed_run_archive_targets`, so operators can confirm which telemetry/session/approval records must survive retirement for later degraded-path review.
`check-controls` now also breaks out `failed_run_controls`, names `preserved_failed_run_controls`, and reports `failed_run_controls_healthy`, so trace/provenance-related control gaps can be reviewed separately from generic control hygiene.

Inspect memory records:

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

`inspect-memory` now shows not only content, but also `provenance` and `revision`.
`dump-events` now also surfaces `failure_reason` in its JSON output for degraded-path drills.

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

Rollout policy check with signal overrides:

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

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

`inspect-approvals` now exposes delegated authorization context too, including `authorization_mode`, `delegated_principal_id`, and `delegated_scope`, so approval review can be compared directly with session evidence. `resolve-approval` returns the same context after decision, so approval closure does not drop acting-identity lineage.
`inspect-session` shows session-level run history and the linked `trace_id` values. Failed drills can now be injected there too, and the summary preserves `failed_runs`, `traceable_failed_runs`, `latest_failure_reason`, and per-run `failure_reason`.
`session-eval-summary` returns a compact operational summary for the run series, including failed runs and `traceable_failed_runs` rather than collapsing everything into success-versus-denied. Failed drills can now be injected there directly too, and the summary surfaces `latest_failure_reason` for quick review.
`session-replay` lets you execute multiple related requests inside one `session_id`. Failed drills can now be injected there too, and the replay summary preserves `failed_runs`, `traceable_failed_runs`, and `latest_failure_reason` alongside per-run `failure_reason`.
`export-session` writes the session as structured JSON that can already serve as a seed for offline eval workflows. It now also preserves delegated authorization context such as `authorization_mode`, `delegated_principal_id`, and `delegated_scope`, and the command summary now surfaces `failed_runs`, `traceable_failed_runs`, and `latest_failure_reason` for failed drills.

The runtime now also treats failure-like tool paths, such as validation failures, as first-class run outcomes. Instead of pretending the run succeeded, it records a failed run, emits an explicit `run_failed` event, and keeps both that status and the concrete failure reason visible as `failure_reason` in session export and CLI output.
`export-eval-dataset` bundles several built-in session scenarios into one eval-ready JSON artifact, including a dedicated failed-run drill scenario and an approval-backed `support_ticket` scenario with a blocking `sandbox_profile_review` grading rule, and its command summary now surfaces aggregate `failed_runs`, `traceable_failed_runs`, and `latest_failure_reason` too.

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

These are no longer just static examples. `config.py` can load those YAML files into agent identity, approved inventory, the runtime, context layers, the memory store, rollout policy, release-identity-bearing lifecycle artifacts, and other lifecycle state, so the package is now closer to a real operational skeleton.

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
