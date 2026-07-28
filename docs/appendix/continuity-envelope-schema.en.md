# Context Continuity Envelope Schema

This page defines the control contract for continuing an agent run after context compaction, a context reset, process recovery, or a role handoff.

The central invariant is deliberately strict:

> A compacted summary is a derived, untrusted view. It carries no authority.

The model's context window is a disposable projection of a session. The durable session event log, policy state, approval state, side-effect state, and checkpoints remain systems of record outside that window. A summary may help a model recover working context, but it must not grant a capability, extend an approval, change identity, erase an unresolved side effect, or silently weaken a user constraint.

!!! example "Canonical continuity case"
    In support triage, compaction happens after a ticket write times out. The summary says to continue, but the durable ledger says `side_effect_unknown`. Recovery must stop for reconciliation; it cannot infer from the summary that no ticket exists and retry the write.

## 1. Minimal envelope

```yaml
continuity_envelope:
  schema_version: continuity-envelope/v1
  envelope_id: ce-2026-07-21-001
  session_id: session-support-001
  source_trace_id: trace-support-042
  reset_reason: context_compaction

  objective: "Resolve the support request without creating a duplicate ticket."
  exact_constraint_refs:
    - event:user-constraint-017
  pending_obligations:
    - reconcile_ticket_write

  tenant_id: tenant-acme
  principal_id: user-42
  authorization_mode: user_delegated
  delegated_principal_id: user-42
  delegated_scope: tickets:create

  policy_version: policy-v4
  capability_name: create_ticket
  capability_version: create-ticket-v3

  approval_id: apr-017
  action_digest: sha256:approved-action
  approval_expires_at: 2026-07-21T18:00:00Z

  idempotency_key: ticket-intent-017
  side_effect_status: side_effect_unknown
  checkpoint_ref: checkpoint:support-042-step-6
  sandbox_snapshot_ref: snapshot:support-042
  budget_remaining: 7

  source_event_range:
    first: event-0001
    last: event-0142
  summary_sha256: sha256:compacted-view
  evidence_refs:
    - trace:trace-support-042
    - approval:apr-017

  requires_reauthorization: true
```

## 2. Fields that must not depend on prose summarization

| Field | Why it stays structured |
|---|---|
| `tenant_id`, `principal_id`, delegated identity and scope | Prevent identity or tenant drift |
| `policy_version`, `capability_version` | Detect changed control contracts |
| `approval_id`, `action_digest`, `approval_expires_at` | Bind the decision to one frozen action and lifetime |
| `idempotency_key`, `side_effect_status` | Prevent duplicate writes and blind retries |
| `checkpoint_ref`, `sandbox_snapshot_ref` | Resume from a named execution boundary |
| exact constraint references and pending obligations | Prevent negative requirements and unfinished work from disappearing |
| `source_event_range`, `summary_sha256`, `evidence_refs` | Make the derived view inspectable and reproducible |

The digest proves which summary was validated. It does not prove that the summary is complete, true, or authorized.

## 3. Compaction and reset protocol

Before compaction or reset:

1. Stop at a safe boundary and flush the session event log.
2. Persist the current checkpoint and unresolved obligations.
3. Record approval, idempotency, side-effect, identity, policy, capability, sandbox, and budget state without summarization.
4. Create the derived summary and bind it to the source event range with `summary_sha256`.
5. Emit `context_compaction` or a reset-boundary event.

After compaction or reset:

1. Load the envelope from governed storage, not from summary prose.
2. Verify schema version, summary digest, event lineage, tenant, principal, and contract versions.
3. Reject expired or revoked approval state.
4. If `side_effect_status` is `side_effect_unknown`, stop for reconciliation rather than retrying.
5. Only after validation and any required reconciliation succeed, rebuild the model's context view from the envelope and selected source events.
6. Emit `context_rehydration`.
7. Run policy and authorization checks again before the next capability call.

## 4. Decision semantics

- `reauthorization_required`: continuity validation passed, but the runtime still has to authorize the next action.
- `blocked_on_reconciliation`: an external effect may already have happened and must be checked first.
- `continuity_validation_failed`: identity, policy, capability, approval, digest, event lineage, or schema validation failed.

There is intentionally no `authorized_by_summary` result.

## 5. Trace events

`context_compaction` should record the envelope id, source event range, summary digest, trigger, and preserved-field classes. `context_rehydration` should record the checkpoint, versions reloaded, validation result, and `requires_reauthorization=true`. `continuity_validation_failed` should use a stable reason code such as `summary_digest_mismatch`, `tenant_mismatch`, `policy_version_changed`, `approval_expired`, or `unknown_side_effect`.

Do not put secrets or unrestricted raw prompts in these events. Keep exact sensitive constraints in governed storage and place references in the envelope.

## 6. Required evals

Run the same scenario against full history and compacted history. The compacted path passes only when it preserves the same or stricter safety decision:

- a negative user constraint is still enforced;
- expired or revoked approval cannot be reused;
- a changed policy or capability version forces a new decision;
- `side_effect_unknown` never becomes an automatic retry;
- tenant and principal cannot change;
- injected instructions inside a summary remain untrusted data;
- an unresolved obligation remains visible;
- the trace links pre-compaction and post-rehydration evidence.

### Executable reference exercise

Run the safe path, a changed-summary path, and an unknown-side-effect path:

```bash
uv run python -m agent_runtime_ref inspect-continuity
uv run python -m agent_runtime_ref inspect-continuity --tamper-summary
uv run python -m agent_runtime_ref inspect-continuity --side-effect-status side_effect_unknown
```

The command also accepts `--summary`, `--trace-id`, `--session-id`, `--policy-version`, `--current-policy-version`, and `--approval-status`. The last policy option populates the `current_policy_version` value loaded from the policy system of record. Use different policy values to reproduce `policy_version_changed`; use `--approval-status revoked` to prove that a revoked approval cannot cross the boundary. The side-effect states are `not_started`, `side_effect_committed`, and `side_effect_unknown`. The `--tamper-summary` switch uses the CLI's `store_true` action and changes the presented summary only after the envelope digest has been recorded.

The default result is `reauthorization_required`, never authorization. The tampered path emits `continuity_validation_failed`. An unknown effect emits the same stop event with status `blocked_on_reconciliation` and must be reconciled through the original `idempotency_key` before any retry; it does not emit `context_rehydration` yet.

## 7. Related material

### Runtime validation errors

The reference implementation exposes the following stable operator-facing errors:

```text
Continuity approval status is not supported: {self.approval_status}
Continuity authorization mode is not supported: {self.authorization_mode}
Continuity envelope must be ContinuityEnvelope
Continuity envelope must require reauthorization
Continuity field is required: delegated_principal_id
Continuity field is required: delegated_scope
Continuity field is required: {field}
Continuity field must be a string: {field}
Continuity reauthorization flag must be a boolean
Continuity schema version is not supported: {self.schema_version}
Continuity side-effect status is not supported: {self.side_effect_status}
Continuity state must be ContinuityState
Continuity summary digest must use sha256
Continuity timestamp is invalid: {field}
Continuity timestamp must include a timezone: {field}
Continuity validation time must be a datetime
Continuity validation time must include a timezone
```

These errors report malformed control artifacts. They are not instructions to repair state from summary prose; the runtime must reload or recreate a governed artifact.

- [Chapter 7. Retrieval, Compaction, and Background Updates](../book/part-iii/chapter-7.en.md)
- [Chapter 16. Baseline Runtime Blueprint](../book/part-vii/chapter-16.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)
- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Approval Request and Decision Schema](approval-schema.en.md)
- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)

## Sources

- Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents).
- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
- OpenAI Agents SDK, [Sessions and Responses compaction](https://openai.github.io/openai-agents-python/sessions/).
- LangGraph, [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence).
