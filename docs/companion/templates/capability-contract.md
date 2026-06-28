# Capability contract template

Status: release candidate template for adaptation.

Related chapters: 5, 6, 10, 22, 23.

Intended user: platform owner, capability owner, security reviewer and product
team lead preparing a capability for controlled agent use.

What to adapt: risk tiers, approval roles, data classification, tenant
boundaries, trace fields, metrics, incident channel and lifecycle states.

Limitations: this is an architecture and review aid, not a legal, compliance or
procurement template. Teams must adapt it to their internal control framework
and jurisdiction.

## Identity

- Capability name:
- Version:
- Owner:
- Risk tier:
- Lifecycle state:

## Scope

- What this capability does:
- What this capability does not do:
- Allowed users or delegated subjects:
- Tenant or workspace boundary:

## Inputs and outputs

- Input fields:
- Trusted sources:
- Untrusted sources:
- Output fields:
- Side effects:

## Policy and verification

- Pre-call policy checks:
- Required approvals:
- Pre-call verifier:
- Post-call verifier:
- Unsafe or uncertain result handling:

## Observability

- Required trace fields:
- Audit fields:
- Metrics:
- Incident channel:

## Release and retirement

- Rollout constraints:
- Stop criteria:
- Rollback or reconciliation path:
- Retirement conditions:
