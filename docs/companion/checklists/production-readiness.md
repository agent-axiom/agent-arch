# Production readiness checklist

Status: release candidate checklist for adaptation.

Related chapter: 23.

Owner: platform owner or release owner.

Use case: final readiness review before an agentic capability moves beyond a
limited internal pilot or controlled canary.

Version: `v1.0-book-rc`, to be locked when the public companion URL and first
book release version are finalized.

What to adapt: organization-specific risk tiers, reviewer roles, evidence
retention rules, incident channels, rollout waves and compliance gates.

Limitations: this checklist is an engineering readiness aid. It does not
guarantee safety, regulatory compliance or operational approval without local
review.

## Minimum gates

- Capability contract is approved.
- Owner map is current.
- Risk tier is assigned.
- Policy bundle is versioned.
- Tool gateway enforces side-effect boundaries.
- Verifier has pre-call and post-call checks where needed.
- Trace includes run, session, capability, policy and tool evidence.
- Eval gate has current pass/fail rationale.
- Rollout wave has blast-radius limits.
- Stop criteria are explicit.
- Rollback or reconciliation path is tested.
- Incident channel is known.
- Registry lifecycle state is current.
- Open high-severity findings are closed or explicitly accepted.
- Next assurance review date is set.
