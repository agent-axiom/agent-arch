# Approval Request and Decision Schema

This page defines the minimal contract layer for human approval in agent systems: what an approval request looks like, what a decision record looks like, and what should remain in the audit trail after a high-risk action.

It also connects directly to the book's [Evidence Spine: From Request to Rollout Judgment](../book/part-v/evidence-spine.en.md), because approval is one of the records that keeps a governed run legible from request to rollout.

If the [policy bundle](policy-bundle-schema.en.md) answers “which rules are in force,” the approval schema answers “how the runtime hands final authority to a human.”

## 1. Why a separate approval schema matters

A very common failure mode looks like this:

- the policy says an action is high-risk;
- the runtime returns `approval_required`;
- the rest of the logic lives somewhere in a UI or in team folklore.

That loses:

- a stable request format;
- a reviewable decision record;
- a repeatable audit trail;
- the link between approval and a specific run or trace.

That is why the approval boundary should be a machine-readable contract, not just a button in an interface.

## 2. Core entities

A minimal schema usually works around three entities:

- `approval_request`
- `approval_decision`
- `approval_audit_record`

That is already enough to connect the policy layer, the runtime, the trace schema, and lifecycle artifacts.

## 3. Approval request

`approval_request` is created when the runtime reaches an action that should not continue automatically.

```yaml
kind: approval_request
approval_id: apr-2026-04-07-001
trace_id: trace-approval-001
session_id: session-approval-001
agent_id: support-triage-agent
tenant_id: tenant-acme
principal_id: user-42
capability: ticket_write
risk_tier: high
requested_action: create_incident_ticket
reason: write_path_requires_human_review
requested_fields:
  summary: "Open a Sev-2 onboarding incident"
  idempotency_key: ticket-req-2026-04-09-001
  target_system: jira
  destination: project://OPS
sandbox_context:
  sandbox_profile_contract: sandbox-profile-v1
  workspace_entries_reviewed: true
  permissions_profile: restricted-shell-network-denied
  network_secrets_posture: network:denied,secrets:none
  snapshot_policy: required_on_completion
required_role: oncall_manager
status: pending
```

The critical parts are:

- `trace_id` and `session_id` tie the approval to run history;
- `capability` and `requested_action` keep approval from becoming an abstract yes/no;
- `required_role` separates any reviewer from the correct approver;
- `requested_fields` preserve the exact payload a human is approving;
- `sandbox_context` matters for sandbox-backed actions, so the approver can see workspace materialization, permissions, and snapshot/resume policy instead of only the business payload.

## 4. Approval decision

`approval_decision` captures what the human actually decided and why.

```yaml
kind: approval_decision
approval_id: apr-2026-04-07-001
decision: approved
decided_by: oncall-manager-7
decided_at: 2026-04-07T11:42:00Z
role: oncall_manager
note: "Customer impact confirmed, proceed with ticket creation"
scope: single_request
expires_at: 2026-04-07T12:00:00Z
```

The important invariants are:

- the decision points to a specific `approval_id`;
- `decided_by` and `role` are audit-friendly;
- `scope` is explicit;
- `expires_at` is useful when approval should not live forever.

## 5. Approval audit record

`approval_audit_record` ties the decision to a real side effect, or to the refusal to produce one.

```yaml
kind: approval_audit_record
approval_id: apr-2026-04-07-001
trace_id: trace-approval-001
decision: approved
executed: true
executed_capability: ticket_write
tool_principal: svc-ticket-writer
idempotency_key: ticket-req-2026-04-09-001
result_status: success
linked_events:
  - approval_requested
  - approval_resolved
  - tool_called
  - tool_succeeded
```

This makes the flow operationally clear:

- the request was raised;
- it was approved or rejected;
- the action was or was not executed;
- the exact principal behind the side effect is visible.

## 6. How this connects to the trace schema

The approval schema should live next to the trace schema through events such as:

- `approval_requested`
- `approval_resolved`
- `tool_called`
- `tool_succeeded`
- `tool_failed`

That is why a good approval flow should be reconstructible both from a dedicated audit record and from the trace. Where approval is part of a failed-run drill or degraded path, that reconstruction should still meet session-export evidence such as `failure_reason`, not stop at the approval record alone.

!!! example "Approval record for the duplicate-ticket thread"
    In the support-triage case, the approver should see `idempotency_key` beside the payload before pressing approve. If `create_ticket` later times out, the audit record preserves the same key next to `approval_id`, `trace_id`, and `tool_principal`, so review can distinguish one approved write intent from a repeated side effect after blind retry.

## 7. How this connects to the policy bundle

The policy bundle answers:

- which capability requires approval;
- who is allowed to approve;
- which risk tiers exist;
- which actions are forbidden without a human gate.

The approval schema answers a different layer:

- what the request looks like;
- what exactly the human approves;
- how the decision is stored;
- how that decision is tied to execution.

## 8. Connection to the reference package

The [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) package already includes operational primitives that support this model:

- [approvals.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/approvals.py)
- [configs/approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- CLI:
  - `inspect-approvals`
  - `resolve-approval`

`inspect-approvals` returns `trace_id`, `session_id`, `count`, and `approvals`; each approval entry keeps `approval_id`, `capability_name`, `requested_by`, `reviewer`, `reason`, `status`, `capability_session_id`, `capability_session_status`, `authorization_mode`, `delegated_principal_id`, and `delegated_scope`. `resolve-approval` returns `approval_id`, `status`, `reviewer`, `resolution_note`, `capability_session_id`, `capability_session_status`, `authorization_mode`, `delegated_principal_id`, and `delegated_scope`, so the runnable demo keeps approval lineage, capability-session state, and delegated authority visible before and after decision.

The bundled `approvals.yaml` also makes the approval operating policy explicit and validates that top-level shape with `'approvals' must be a mapping`: `default_reviewer`, `escalation_sla_minutes`, and `delegated_authorization` settings such as `reviewer_required_for_user_delegation`, `require_principal_binding`, `require_scope_visibility`, `on_scope_revoked`, and `subagent_inheritance` describe who reviews delegated actions, what evidence must stay visible, and whether delegation can pass into subagents. Its policy loader keeps reviewer and escalation evidence type-safe with `approvals.default_reviewer must be a string`, `approvals.default_reviewer is required`, `approvals.escalation_sla_minutes must be an integer`, and `approvals.escalation_sla_minutes must be positive`. Approval/session lineage also rejects unsupported delegated-authorization evidence with `Authorization mode is not supported: {authorization_mode}` and unsupported approval or capability-session states with `Approval status is not supported: {status}` instead of storing unknown modes or statuses beside approvals or session exports. The reference policy sets subagent inheritance to `explicit_only`, so delegated authority never flows into a child agent unless the approval path names it explicitly.

That makes approval not only explainable, but actually executable in the demo runtime.

## 9. Minimal invariants

At minimum, a mature approval layer should enforce:

- every request has a stable `approval_id`;
- approval is tied to `trace_id` and `session_id`;
- the approved payload is explicit;
- approver and role remain in the audit trail;
- side effects can be linked to one concrete approval decision;
- expired approval is not reused silently.

## 10. What usually breaks

The common failure modes are easy to recognize:

- the approval request does not contain the real action payload;
- the approver sees too little context;
- the decision lives only in the UI and never reaches the trace;
- the runtime does not distinguish “approved once” from “approved forever”;
- sandbox-backed approval hides the sandbox profile, workspace entries, or permissions;
- the side effect runs with a payload different from the approved one;
- nobody can later reconstruct who approved the risky action.

## 11. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Does the approval request have an explicit `approval_id`?
- Is approval tied to `trace_id` and `session_id`?
- Does the approver see the exact payload that will later be executed?
- If the action is sandbox-backed, does the approver see the sandbox profile contract, workspace entries, permissions, and snapshot/resume policy?
- Are `decided_by`, `role`, and `decision scope` retained?
- Can approval be linked to the real tool execution?
- Is there an audit-friendly record for both approved and rejected paths?

If the answer is “no” several times in a row, you may have a human gate in principle, but not yet a full approval contract.

## What to Do Next

- [Policy Bundle Schema and Approval Contract](policy-bundle-schema.en.md)
- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../book/part-ii/chapter-4.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)
