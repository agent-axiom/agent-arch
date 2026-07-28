# Example: support ticket release decision record

Status: example for adaptation.

Related chapters: 15, 16, 19, 20, 23.

Intended user: release owner, platform owner, verifier/eval owner, security
reviewer and accountable product owner.

Limitations: synthetic example. Replace owners, dates, evidence links and risk
acceptance language before use.

## Change

- Change ID: `chg-support-ticket-canary-001`
- Agent or capability: `support-triage-ref` / `create_support_ticket`
- Owner: `agent-platform`
- Risk tier: `high`
- Release wave: `internal canary`
- Decision date: `YYYY-MM-DD`

## Evidence

- Eval summary: `eval-failed-run-timeout.json` passes duplicate-ticket guard.
- Trace sample: `trace-failed-tool-timeout.jsonl` shows failed run is explicit
  and traceable.
- Policy bundle: `support-write-policy-v1`
- Verifier result: no blind retry after unknown side effect.
- Known findings: companion URL/version not relevant to runtime decision;
  no high-severity runtime blocker in this example.
- Open risks: support-system timeout behavior still requires manual
  reconciliation path.

## Decision

- Decision: approve with constraints.
- Constraints: canary only; manager approval required for write path; rollback
  owner on call during observation window.
- Observation window: 48 hours or 100 write-path attempts, whichever comes
  first.
- Stop criteria: duplicate ticket, missing approval, untraceable failure,
  unknown side effect reported as success.
- Rollback owner: `support-platform-oncall`.
- Next review: after observation window.

## Rationale

- Why this decision is acceptable: the known timeout failure has a traceable
  failed-run path and regression dataset.
- What would change the decision: missing idempotency key, new unreviewed tool
  adapter, failed duplicate-ticket eval or missing approval trace.
- Who accepted residual risk: product owner and platform owner for the canary
  window only.
