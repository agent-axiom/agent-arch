# Chapter 27. Agent Inventory, Registry, and Sprawl Control

!!! info "Freshness note"
    This chapter is current as of April 11, 2026.

    What changes fastest here:

    - platform features for inventory discovery, registry sync, and governance automation;
    - vendor approaches to classifying agents, assistants, and agent-like entities;
    - working practices for drift detection and policy enforcement across estates.

    What changes more slowly:

    - the need to separate inventory from registry;
    - the requirement for every production agent to have an owner, lifecycle state, and capability record;
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
- which of them are still alive.

That is the state worth calling `agent sprawl`.

## 2. Why sprawl is not only an organizational problem

At first glance, this looks like a management problem: too many entities, too much entropy.

In practice, sprawl quickly becomes a risk multiplier:

- orphaned agents continue to run without owners;
- deprecated agents keep access to systems and data;
- teams interpret approvals and policy boundaries differently;
- observability coverage becomes fragmented;
- inventory drift makes release gates and incident review less reliable.

Microsoft explicitly links incomplete inventory and agent sprawl to blind spots, inconsistent enforcement, and delayed detection. [^ms-inventory][^ms-agentic-risk]

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
Without registry, you cannot confidently say which agents are approved and governed.

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
- observability status;
- artifact-bundle linkage;
- retirement-plan linkage.

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
- release evidence can be checked not only through traces, but also through registry status.

So registry turns observability from “raw events” into a governed operational map.

## 8.1. A registry without continuous verification becomes neat but inaccurate

It is important not to overestimate the registry itself. The existence of a registry does not prove that the control layer actually works.

If the registry:

- is not reconciled with real telemetry coverage;
- is not checked against live principals;
- is not matched against active capabilities;
- does not participate in retirement hygiene,

then it quickly becomes a tidy but partially fictional picture of the estate.

That is why a mature registry is better understood not as a static catalog, but as a continuously verified control surface.

## 9. How registry connects to approvals and policies

Registry should not duplicate the policy bundle or approval contract.

Its job is different:

- to show which policy bundle and approval mode belong to a given agent;
- to show whether the agent is entitled to a specific capability set;
- to show which lifecycle state the agent is currently in.

Without that linkage, it becomes easy to end up in a state where:

- policy changed;
- approval flow changed;
- traces improved;
- but nobody knows which agents were supposed to use those controls.

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
  policy_bundle: policy-v4
  approval_mode: required_for_high_risk
  observability:
    trace_enabled: true
    inventory_covered: true
  artifacts:
    bundle_id: bundle-2026-04-07-a
  retirement_plan: retire-support-v1
```

That record is already enough to connect the agent to ownership, controls, and lifecycle.

## 11. Example registry health check

```python
from dataclasses import dataclass


@dataclass
class AgentRegistryState:
    has_owner: bool
    has_lifecycle_state: bool
    has_policy_linkage: bool
    has_observability: bool


def registry_ready(state: AgentRegistryState) -> bool:
    return (
        state.has_owner
        and state.has_lifecycle_state
        and state.has_policy_linkage
        and state.has_observability
    )
```

The logic is straightforward: an agent without an owner, lifecycle state, and observability linkage should not count as production-ready.

## 12. The most common failure modes

- agents exist in production but not in inventory;
- inventory exists but lifecycle states are not maintained;
- registry knows nothing about principals and approvals;
- deprecated agents still have access to tool paths;
- multiple registries drift apart;
- the platform team knows one set of agents while the security team knows another.

## 13. Practical checklist

- Can you quickly name the number of active, deprecated, and retired agents?
- Does every production agent have an owner?
- Is the registry record linked to a policy bundle, approval mode, and bundle ID?
- Can inventory show which agents do not emit telemetry?
- Can you quickly find orphaned or deprecated agents with live principals?
- Do you distinguish between “discovered” and “approved for production”?

If several answers are “no,” you already have an agent estate but not yet agent governance.

## 14. Useful reference pages

- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Approval Request and Decision Schema](../../appendix/approval-schema.en.md)
- [Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)
- [Research Frontier: Memory, Observability, and Multi-Agent Reliability](../../appendix/research-frontier.en.md)

- [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](chapter-26.en.md)
- [Chapter 23. Retirement, Replacement, and End-of-Life Discipline](chapter-23.en.md)

[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
