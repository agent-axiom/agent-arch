# Example: support ticket capability contract

Status: example for adaptation.

Related chapters: 5, 6, 10, 22, 23.

Intended user: platform owner, support-platform owner, security reviewer and
product team lead.

Limitations: synthetic example. Replace risk tier, owners, approvals, data
classification and incident routes before use.

## Identity

- Capability name: `create_support_ticket`
- Version: `v1.0-book-example`
- Owner: `support-platform`
- Risk tier: `high`
- Lifecycle state: `canary`

## Scope

- What this capability does: creates one support ticket from an approved
  support-triage intent.
- What this capability does not do: does not close tickets, refund money,
  change account state or notify external customers.
- Allowed users or delegated subjects: authenticated support employees and
  approved support-triage agent runs.
- Tenant or workspace boundary: one tenant workspace per request; cross-tenant
  writes are denied.

## Inputs and outputs

- Input fields: `requester_id`, `tenant_id`, `summary`, `severity`,
  `idempotency_key`.
- Trusted sources: authenticated user session, approved policy bundle,
  support system catalog.
- Untrusted sources: retrieved documents, user-provided free text, tool output
  notes.
- Output fields: `ticket_id`, `status`, `created_at`, `idempotency_key`.
- Side effects: one ticket write in the support system.

## Policy and verification

- Pre-call policy checks: tenant match, capability allowed, risk tier, write
  permission, idempotency key present.
- Required approvals: manager approval for high-severity or external-impact
  tickets.
- Pre-call verifier: summary does not contain hidden instructions or unsupported
  action.
- Post-call verifier: exactly one ticket side effect or explicit safe stop.
- Unsafe or uncertain result handling: stop, preserve trace and require manual
  reconciliation.

## Observability

- Required trace fields: `trace_id`, `session_id`, `tenant_id`, `agent_id`,
  `principal_id`, `capability_name`, `idempotency_key`, `approval_id`.
- Audit fields: requester, reviewer, policy bundle, tool adapter version.
- Metrics: approval wait time, duplicate-ticket guard pass/fail, unknown side
  effect count.
- Incident channel: `#support-agent-incidents`.

## Release and retirement

- Rollout constraints: internal pilot, then canary by tenant group.
- Stop criteria: duplicate ticket, missing approval, unknown side effect
  reported as success, tenant-boundary violation.
- Rollback or reconciliation path: freeze capability, reconcile by
  `idempotency_key`, rerun failed-run eval before resume.
- Retirement conditions: owner missing, policy bundle stale, replacement
  workflow approved, unresolved high-severity finding.
