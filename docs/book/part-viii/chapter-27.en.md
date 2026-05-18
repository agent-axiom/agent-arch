# Chapter 27. Agent Inventory, Registry, and Sprawl Control

!!! info "Freshness note"
    Last reviewed: **May 14, 2026**. Next scheduled review: **June 14, 2026**.

    What changed since the previous review: MCP/A2A security surfaces, verifier contracts, governance-aware telemetry, and publisher-readiness concerns are now tracked explicitly as near-term editorial work.

    What changes fastest here:

    - platform features for inventory discovery, registry sync, and governance automation;
    - vendor approaches to classifying agents, assistants, and agent-like entities;
    - working practices for drift detection and policy enforcement across estates.

    What changes more slowly:

    - the need to separate inventory from registry;
    - the requirement for every production agent to have an owner, lifecycle state, capability record, and runtime-control ownership;
    - the importance of periodic review so sprawl does not turn into a blind spot.

## 1. Why nearly every successful agent program produces sprawl

As soon as the first agent systems prove useful, the same story usually begins:

- one team builds a support agent;
- another builds an internal knowledge agent;
- a third adds a workflow assistant;
- a fourth quickly assembles a narrow agent for a local task.

Each decision may be reasonable on its own. The problem starts later, when nobody can quickly answer:

- how many agents exist at all;
- which are truly production and which are “temporary”;
- who owns them;
- which capabilities they have;
- which identities, connectors, and tool principals they use;
- which of them are still alive;
- which of them still own paused approvals, background routes, deprecated contract paths, or stale verifier contracts.

That is the state worth calling `agent sprawl`.

The registry layer exists for one reason above all: to make the estate answerable.

It should be possible to ask of any production agent who owns it, which controls govern it, which evidence describes it, and who must act when it drifts.

That answerability is the center of gravity here. Registry does not own the evidence backbone or the telemetry substrate.

It owns the mapping from governed entities to owners, states, and accountability paths.

That is the core promise of this chapter.

It should help the reader see registry as the accountability layer of the estate: the place where governed entities stop being a blurry population of tools and assistants and become answerable production systems with owners, lifecycle state, and explicit responsibility. The main artifact of this chapter is the registry record: an entry that links agent identity, owner, lifecycle state, capabilities, runtime-control ownership, and evidence links.

## 2. Why sprawl is not only an organizational problem

At first glance, this looks like a management problem: too many entities, too much entropy.

In practice, sprawl quickly becomes a risk multiplier:

- orphaned agents continue to run without owners;
- deprecated agents keep access to systems and data;
- teams interpret approvals and policy boundaries differently;
- observability coverage becomes fragmented;
- inventory drift makes release gates and incident review less reliable.

Microsoft explicitly links incomplete inventory and agent sprawl to blind spots, inconsistent enforcement, and delayed detection.[^ms-inventory][^ms-agentic-risk]

The same basic discipline also aligns with NIST SP 800-53: inventory should be complete, maintained, and tied to accountability, or the control quickly becomes decorative.[^nist-sp53]

## 3. Inventory and registry are not the same layer

It is useful to distinguish:

- `agent inventory`
- `agent registry`

Inventory answers:

- which agent-like entities exist in the environment at all.

Registry answers a stricter question:

- which of them are recognized, classified, governed, and admitted into production contours.

So:

- inventory exists for completeness of visibility;
- registry exists for governance.

Without inventory, you do not know the full estate.
Without registry, you cannot confidently say which agents are approved, governed, and operationally answerable.

## 4. What a minimal agent record should contain

A minimal registry record for production-grade agent systems should usually include:

- `agent_id`;
- owner team;
- business purpose;
- lifecycle state;
- allowed capabilities;
- runtime identity;
- tool principals;
- approval requirements;
- paused-run, background-run, and capability-session ownership;
- observability status;
- verifier or eval-evidence status;
- active and deprecated verifier-contract linkage;
- artifact-bundle linkage;
- retirement-plan linkage.

To keep that record from becoming a long form for its own sake, read it as five groups:

1. **Identity:** `agent_id`, runtime identity, owner team, and business purpose.
2. **Lifecycle:** lifecycle state, retirement plan, and deprecated paths.
3. **Capabilities:** allowed capabilities, tool principals, and approval requirements.
4. **Runtime ownership:** who owns paused runs, background runs, and capability sessions.
5. **Evidence links:** observability status, verifier/eval evidence, verifier contracts, and artifact-bundle linkage.

This matters not because of “documentation,” but because it links the agent as an entity to:

- security controls;
- operational ownership;
- lifecycle decisions.

## 5. Lifecycle states matter more than teams expect

A simplistic “active / inactive” model stops working quickly.

At minimum, it is more useful to have:

- `proposed`
- `development`
- `pilot`
- `production`
- `restricted`
- `deprecated`
- `retired`

That makes it easier to:

- constrain autonomy before production;
- track deprecated agents;
- see which agents should not yet have full egress or full approval paths;
- handle replacement and retirement without gray zones.

## 6. Registry is useful beyond security teams

A good agent registry is not just for security or governance.

It is also useful to:

- the platform team;
- product teams;
- SRE and operations;
- audit and compliance;
- incident responders.

For the platform team, it shows which patterns actually scale.
For operations, it shows who should respond at night.
For incident response, it shows which agents could have participated in a given event.

## 7. Sprawl often starts with “small exceptions”

In reality, a zoo rarely starts as an official strategy.

It starts with small exceptions:

- “this is only an internal helper”;
- “this agent is temporary”;
- “skip the registry for now, we’ll add it later”;
- “approval is overkill here”;
- “we’ll wire telemetry later”.

A few months later, those exceptions have become the least visible part of the estate.

That is why a strong default is simple:

- if an entity can act on behalf of the organization, read sensitive context, or call tools, it should at least enter inventory;
- if it enters a production contour, it should also enter the registry.

## 8. How registry connects to observability

The observability chapter already showed that inventory coverage is part of the evidence layer.

Registry makes this connection even tighter:

- traces can be enriched with registry metadata;
- detections can be built around lifecycle state;
- incidents can be filtered by owner, risk tier, and approval mode;
- release evidence can be checked not only through traces, but also through registry status and verifier-evidence linkage.

So registry turns observability from “raw events” into a governed operational map.

But it should not be confused with provenance. Provenance preserves which approved artifact set and version justified behavior.

Registry preserves which named production entity, owner, and lifecycle state that behavior belonged to.

That is also the clean boundary between the two chapters. Observability preserves evidence.

Registry assigns that evidence to named entities, owners, lifecycle states, and accountability paths across the estate.

And that is the boundary from the provenance chapter too. Provenance answers what governed version or approved bundle the system ran under.

Registry answers which production entity owned that path and who is accountable for it now.

!!! example "Case thread: support-triage in the registry"
    After all the fixes, support-triage should not be merely “the support agent.” It should be a registry record with an owner, lifecycle state, allowed capabilities, `create_support_ticket` tool principal, approval mode, observability status, eval-evidence linkage, and retirement plan for the old ticket writer. Then a duplicate-ticket signal can be attached not only to a trace or artifact bundle, but to a named production entity: who owns the path, who expands the canary, who disables the write capability, and who is accountable for the deprecated route.

**Registry case-spine note:** every canonical case should become a named registry record, not a story in prose. Support triage needs write-capability owners, approval mode, and retirement plan for deprecated ticket paths. Internal knowledge assistant needs corpus owners, freshness review, tenant scope, and retrieval-policy linkage. Incident coordination needs incident-role owners, escalation authority, notification channels, and lifecycle state for emergency-only capabilities.

### 8.1. A registry without continuous verification becomes neat but inaccurate

It is important not to overestimate the registry itself. The existence of a registry does not prove that the control layer actually works.

If the registry:

- is not reconciled with real telemetry coverage;
- is not checked against live principals;
- is not matched against active capabilities;
- is not reconciled with [verifier evidence](../../appendix/eval-schema.en.md) used in rollout or assurance;
- does not participate in retirement hygiene,

then it quickly becomes a tidy but partially fictional picture of the estate.

That is why a mature registry is better understood not as a static catalog, but as a continuously verified control surface.

## 9. How registry connects to approvals and policies

Registry should not duplicate the policy bundle or approval contract.

Its job is different:

- to show which policy bundle and approval mode belong to a given agent;
- to show whether the agent is entitled to a specific capability set;
- to show which approved MCP servers, discovery sources, and auth modes belong to that agent's governed capability surface;
- to show which lifecycle state the agent is currently in.

Without that linkage, it becomes easy to end up in a state where:

- policy changed;
- approval flow changed;
- traces improved;
- but nobody knows which agents were supposed to use those controls.

This gets even more important once approval and long-running work become explicit runtime paths.

Then the registry should help answer:

- which agents are allowed to pause for approval;
- which agents may continue work in background mode;
- which agents may re-initialize stateful capability sessions, and under what approval mode;
- who owns stuck paused runs;
- who owns aging background runs;
- who owns capability-session expiry drift and emergency freeze actions;
- which contract version their approval and capability payloads are expected to follow;
- which verifier or grading contract is trusted for their high-risk eval evidence;
- whether deprecated verifier contracts are still referenced anywhere in the estate;
- whether shadow MCP endpoints have appeared outside the approved registry.

Otherwise, the estate may look governed while still hiding operational ambiguity.

Registry is therefore less about preserving release lineage than about preserving operational answerability.

It is the estate-level ownership map that keeps decisions, incidents, and drift attached to the right entity.

That ambiguity is usually what hurts first in incidents.

Teams may have telemetry, policies, and approvals, but still lose time on the most basic estate question: which exact production entity is accountable for this path right now?

## 10. Example of a minimal agent registry record

```yaml
agent:
  agent_id: support-triage-ref
  owner_team: customer-platform
  business_purpose: support_ticket_triage
  lifecycle_state: production
  runtime_identity: agent://support-triage-ref
  tool_principals:
    - svc-ticket-writer
  allowed_capabilities:
    - ticket_read
    - ticket_write
  mcp_surface:
    approved_servers:
      - support-registry/ticketing-mcp
    discovery_sources:
      - platform_registry
    auth_mode: managed_oauth
  policy_bundle: policy-v4
  approval_mode: required_for_high_risk
  runtime_controls:
    approval_pause_allowed: true
    background_mode_allowed: true
    capability_session_mode: stateful
    reinit_policy: approval_bound
    paused_run_owner: support-ops
    capability_session_owner: support-ops
    contract_version: capability-contract-v3
  observability:
    trace_enabled: true
    inventory_covered: true
    verifier_evidence_linked: true
  verifier_contract: verifier-v2
  deprecated_verifier_contracts:
    - verifier-v1
  artifacts:
    bundle_id: bundle-2026-04-07-a
  retirement_plan: retire-support-v1
```

That record is already enough to connect the agent to ownership, controls, lifecycle, and verifier-aware evidence expectations.

At estate scale, this also helps answer a registry question that teams otherwise miss: which verifier contracts are active, which are deprecated, and which agents still depend on the old ones.

## 11. Example registry health check

```python
from dataclasses import dataclass


@dataclass
class AgentRegistryState:
    has_owner: bool
    has_lifecycle_state: bool
    has_policy_linkage: bool
    has_observability: bool
    has_runtime_control_linkage: bool
    has_capability_session_owner: bool


def registry_ready(state: AgentRegistryState) -> bool:
    return (
        state.has_owner
        and state.has_lifecycle_state
        and state.has_policy_linkage
        and state.has_observability
        and state.has_runtime_control_linkage
        and state.has_capability_session_owner
    )
```

The logic is straightforward: an agent without an owner, lifecycle state, and observability linkage should not count as production-ready.

## 12. The most common failure modes

- agents exist in production but not in inventory;
- inventory exists but lifecycle states are not maintained;
- registry knows nothing about principals and approvals;
- deprecated agents still have access to tool paths;
- registry records do not say who owns paused approvals or aging background runs;
- contract versions drift while registry still points to obsolete control assumptions;
- multiple registries drift apart;
- the platform team knows one set of agents while the security team knows another.

## 13. A Fast Maturity Test for Agent Governance

A team should not think it has control of its agent estate only because it has a registry spreadsheet and a rough count of deployed agents.

A stronger bar is this:

- inventory and registry are treated as different control surfaces;
- every production agent has an owner, lifecycle state, and policy linkage;
- telemetry coverage can be checked against the registry continuously;
- paused approvals, background-run ownership, and contract versions are part of the registry control surface;
- deprecated and orphaned agents can be found before they become blind spots;
- governance can distinguish discovered entities from approved production agents.

If most of those conditions are missing, the team may have visibility fragments, but it still does not have real agent governance.

At that point, the registry is still acting like a loose catalog.

A mature registry acts more like an accountability layer that continuously reconciles production entities, control ownership, and lifecycle truth.

## 14. Practical checklist

- Can you quickly name the number of active, deprecated, and retired agents?
- Does every production agent have an owner?
- Is the registry record linked to a policy bundle, approval mode, runtime-control ownership, and bundle ID?
- Can inventory show which agents do not emit telemetry?
- Can you quickly find orphaned or deprecated agents with live principals?
- Do you distinguish between “discovered” and “approved for production”?

If several answers are “no,” you already have an agent estate but not yet agent governance.

## 15. Evidence Model for This Chapter

This chapter should be read as an accountability layer, not as an inventory spreadsheet:

- **Stable claims:** agent governance requires more than discovery; each production agent needs ownership, lifecycle state, policy linkage, and observable control status.
- **Vendor practice:** infrastructure inventory and agentic-risk guidance both point toward continuous asset coverage, ownership, and control accountability.
- **Runtime practice:** registry records, lifecycle artifacts, policy bundles, approval modes, principal status, and telemetry coverage make the agent estate reviewable.
- **Author interpretation:** registry is the closing layer that ties observability, policy, lifecycle, and retirement into one accountable production entity.
- **Fast-moving area:** agent builders, registries, and discovery mechanisms will change; the distinction between discovered entities and approved production agents should not.

## 16. Useful reference pages

- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Approval Request and Decision Schema](../../appendix/approval-schema.en.md)
- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Research Frontier: Memory, Observability, and Multi-Agent Reliability](../../appendix/research-frontier.en.md)

- [Chapter 23. Retirement, Replacement, and End-of-Life Discipline](chapter-23.en.md)
- [Chapter 24. Agentic Misalignment and Insider Risk](chapter-24.en.md)
- [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](chapter-26.en.md)

[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
[^nist-sp53]: NIST, [SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
