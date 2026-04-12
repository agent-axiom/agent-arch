# Handbook for Agent Registry and Inventory Operations

Once an organization has several agent systems, a chapter about inventory is not enough. The team needs a short operating model: who maintains the registry, how drift is detected, when an agent is considered orphaned, and what happens to deprecated entries.

This handbook collects that minimum in one place.

## 1. What should always exist

Even a small agent program should have two layers:

- `inventory` for the full list of agent-like entities;
- `registry` for the entities that are recognized, classified, and admitted into the production contour.

If there is only a registry, the team usually underestimates shadow agents and local experiments.
If there is only inventory without a registry, nobody can say confidently what is actually approved.

## 2. Who should own this layer

Registry work usually fails when ownership is vague.

A minimally useful split looks like this:

- the platform team owns the registry shape and verification rules;
- the product owner owns business purpose and lifecycle state;
- the safety or governance owner owns policy and approval linkage;
- operations owns the incident contact and retirement hygiene.

One team may hold several of these roles. The important part is that the roles are explicit.

## 3. What an agent record should contain

A minimal record is easiest to review against one template:

- `agent_id`
- owner team;
- business purpose;
- lifecycle state;
- risk tier;
- runtime identity;
- allowed capabilities;
- policy bundle;
- approval mode;
- observability coverage;
- bundle linkage;
- retirement linkage.

Without that, the registry quickly turns into a list of names without operational meaning.

## 4. When an agent must enter inventory

A strong default usually looks like this:

- if the entity can call tools;
- if it reads organizational context;
- if it acts on behalf of an employee or service;
- if it participates in a production workflow;

it should enter inventory at least.

Exceptions are better made explicit than left as quiet assumptions.

## 5. When an agent must enter the registry

The registry usually needs to include entities that:

- run in the production contour;
- have access to sensitive tools or external systems;
- can create side effects;
- participate in staged rollout;
- require audit-ready ownership.

That is why the registry matters for governance, approvals, and reliable incident response.

## 6. How often the registry should be checked

Registry drift appears not because the idea is weak, but because the operating rhythm is weak.

A minimal cadence is usually:

- on every rollout update;
- on every high-risk change review;
- on a regular inventory review;
- on every retirement or replacement event;
- after incident review, when hidden agents or stale records are discovered.

If the registry is not updated at these points, drift is almost guaranteed.

## 7. Which drift signals matter most

Not all drift is equally dangerous. Start by catching:

- an active agent without an owner;
- an agent in `production` that does not appear in traces or registry-linked telemetry;
- a deprecated agent with a live principal;
- a capability present in runtime but missing from allowed inventory;
- an approval mode in the registry that does not match the policy bundle;
- a retired bundle that still appears in live runs.

That is already enough for a minimal continuous verification loop.

## 8. When to move a record to restricted, deprecated, or retired

It is useful to change lifecycle state early:

- `restricted` when the capability set or approval mode is temporarily narrowed;
- `deprecated` when a replacement is chosen and new rollout waves should avoid the old path;
- `retired` when the principal is revoked, rollout is stopped, and historical state has moved into retention mode.

The most common mistake is simple: the agent is effectively gone, but the registry still presents it as production-ready.

## 9. What to check during incident response

During incident review, the registry matters because it should answer a few direct questions quickly:

- which agent participated in the event;
- who owns it;
- which lifecycle state it had;
- which policy bundle and approval mode were supposed to be active;
- which bundle linkage and retirement status were attached to the record.

If the registry cannot answer these questions quickly, it is not helping operations much.

## 10. Minimal weekly review

A short review can be built around a few questions:

- Are there new agent-like entities outside inventory?
- Are there orphaned records?
- Are there `production` agents without telemetry coverage?
- Are there deprecated entries with live principals?
- Are there mismatches between the registry, policy bundle, and rollout state?

This review is best kept short, but regular.

## 11. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Does every active agent have an owner?
- Are inventory and registry separated?
- Does lifecycle state change during rollout and retirement?
- Is the registry linked to policy bundle and approval mode?
- Is the registry verified against live telemetry?
- Do deprecated agents lose principals and tool access?
- Do incidents improve registry hygiene?

## What to Do Next

- [Incident Response Playbook for Agent Systems](incident-response-playbook.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Change Review and Rollout Gate Schema](change-rollout-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](../book/part-viii/chapter-26.en.md)
- [Chapter 27. Agent Inventory, Registry, and Anti-Sprawl Discipline](../book/part-viii/chapter-27.en.md)
