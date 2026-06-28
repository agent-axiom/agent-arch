# Example: support ticket timeout incident record

Status: example for adaptation.

Related chapters: 13, 16, 20, 23.

Intended user: incident commander, platform owner, security reviewer,
capability owner and postmortem facilitator.

Limitations: synthetic example. Replace incident roles, impact, retention and
notification rules before use.

## Identity

- Incident ID: `inc-support-ticket-timeout-001`
- Date/time: `YYYY-MM-DDTHH:MM:SSZ`
- Reporter: `support-platform-oncall`
- Incident commander: `agent-platform-lead`
- Affected agent: `support-triage-ref`
- Affected capability: `create_support_ticket`

## Evidence freeze

- Trace ID: `trace-demo-001`
- Session ID: `session-demo-001`
- Run ID: `run-failed-tool-timeout`
- Change ID: `chg-support-ticket-canary-001`
- Rollout wave: `internal canary`
- Policy bundle: `support-write-policy-v1`
- Model route: `book-example-model-route`
- Approval record: none; failure occurred before approval-backed write.

## Impact

- User impact: support ticket was not created automatically.
- Data impact: no cross-tenant data movement observed in the example trace.
- Tool or side-effect impact: ticket side effect is treated as unknown until
  reconciliation by `idempotency_key`.
- Business impact: manual support follow-up required.
- Severity: `medium` in this synthetic example.

## Timeline

- Detection: runtime emitted `run_failed` with `tool_timeout`.
- First containment: canary held; write capability frozen for affected tenant.
- Investigation milestones: trace inspected; eval dataset updated; support
  system checked by idempotency key.
- Resolution: manual reconciliation completed; retry policy reviewed.

## Containment and recovery

- Action taken: stopped automatic retries after unknown side effect.
- Owner: `support-platform-oncall`
- Scope: affected canary tenants only.
- Rollback or reconciliation: reconcile by `idempotency_key`; rerun
  failed-run eval before resume.
- Residual risk: external support system timeout semantics still require
  operator review.

## Corrective actions

- New eval case: `failed_run_timeout`.
- Policy/verifier update: block success outcome when side effect is unknown.
- Tool gateway update: preserve timeout failure reason in trace and session
  export.
- Registry or lifecycle update: mark capability as canary-held until eval
  passes.
- Documentation update: companion failed-run example refreshed.
- Follow-up owner and date: `agent-platform`, `YYYY-MM-DD`.
