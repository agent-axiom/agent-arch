# Example: production readiness checklist for support ticket capability

Status: example for adaptation.

Related chapter: 23.

Owner: `agent-platform` release owner.

Use case: readiness review before moving `create_support_ticket` from internal
pilot to controlled canary.

Version: `v1.0-book-example`.

Limitations: synthetic example. Replace risk, owners, evidence links and
organization-specific gates before use.

## Minimum gates

- [x] Capability contract is approved.
- [x] Owner map is current.
- [x] Risk tier is assigned.
- [x] Policy bundle is versioned.
- [x] Tool gateway enforces side-effect boundaries.
- [x] Verifier has pre-call and post-call checks where needed.
- [x] Trace includes run, session, capability, policy and tool evidence.
- [x] Eval gate has current pass/fail rationale.
- [x] Rollout wave has blast-radius limits.
- [x] Stop criteria are explicit.
- [x] Rollback or reconciliation path is tested.
- [x] Incident channel is known.
- [x] Registry lifecycle state is current.
- [ ] Open high-severity findings are closed or explicitly accepted.
- [ ] Next assurance review date is set.

## Example decision

Decision: hold until the two unchecked items are closed.

Reason: the capability has executable trace/session/eval evidence, but the
release owner has not yet recorded high-severity finding status and the next
assurance review date.
