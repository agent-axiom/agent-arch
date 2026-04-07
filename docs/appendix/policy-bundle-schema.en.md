# Policy Bundle Schema and Approval Contract

This page connects several topics already covered in the book:

- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../book/part-ii/chapter-4.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)
- [Chapter 20. Change Management for Agent Systems](../book/part-viii/chapter-20.en.md)

And it is grounded in the runnable package:

- [Reference Package](reference-package.en.md)

If the trace schema and eval schema pages answer:

- how to describe actual behavior;
- how to describe expected behavior;

then this page answers the third question:

- how to describe the governing rules that stand between reasoning and side effects.

## Why a policy bundle should be treated as an artifact

One of the most common mistakes in agent systems looks like this:

- policy rules partly live in prompts;
- partly in gateway code;
- partly in an approval UI;
- partly in the team’s memory.

That may work while the system is small. But as soon as change management, audit, and staged rollout appear, the policy layer becomes too blurry.

That is why it is useful to package a `policy bundle` as a first-class artifact.

## What a policy bundle is

Here, it is useful to define a `policy bundle` as a related set of rules that ships together:

- runtime policy;
- tool policy;
- approval policy;
- memory write rules;
- escalation rules;
- egress rules.

The point is not that everything must live in one YAML file. The point is that the bundle should be:

- versioned;
- reviewable;
- traceable;
- releasable.

## Minimal policy bundle structure

A minimally useful bundle can look like this:

```yaml
bundle:
  bundle_id: policy-support-triage-2026-04-07
  version: 2026.04.07
  owner_team: platform-safety
  applies_to:
    agent_ids: ["support-triage-ref"]
  artifacts:
    - policy.yaml
    - approvals.yaml
    - controls.yaml
```

This is not yet the rules themselves. It is the envelope that answers:

"What exactly do we currently treat as the policy artifact for this agent system?"

## Why the approval contract should not hide inside prose

Approval logic is often described only in words:

- “high-risk actions need confirmation”;
- “manager approves ticket creation”;
- “security signs off on dangerous actions”.

That is not enough.

It is useful to make the approval contract explicit:

- who may approve;
- which action class requires approval;
- which fields must appear in the approval request;
- which decisions are allowed;
- what happens after rejection;
- what must remain in the audit trail.

## Example approval contract

Here is a workable skeleton:

```yaml
approval_contract:
  capability: create_ticket
  risk_tier: high
  required_reviewers:
    - manager
  request_fields:
    - trace_id
    - session_id
    - requested_by
    - reason
    - tool_arguments_redacted
  allowed_decisions:
    - approved
    - rejected
  on_reject: stop_run
```

The point is simple: approval should be a machine-readable operational contract, not just a checkbox in a UI.

## How the policy bundle connects to the lifecycle

From Part VIII, two ideas matter most here:

- policy changes are release-bearing changes;
- the policy bundle should participate in change management as a full artifact.

That means the team should answer not only:

"What policy do we have in general?"

but also:

"Which exact policy bundle version was active during this rollout or incident?"

## How the policy bundle connects to traces

The connection is very practical:

- the trace shows which policy decision actually fired;
- the policy bundle shows where that decision came from;
- the approval contract shows what the human gate should have looked like.

Without that trio, investigation quickly turns into guesswork.

## What the reference runtime already supports

In `agent_runtime_ref`, there are already:

- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [approvals.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/approvals.yaml)
- [controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/controls.yaml)
- [change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)

So the package already lives in a model where policy and approvals are not “secondary settings”, but governed artifacts.

## What a production schema should add

As soon as the system grows up, it is useful to add at least:

- `bundle_version`
- `artifact_lineage`
- `change_id`
- `approval_contracts`
- `deprecated_rules`
- `redaction_policy`

That turns the policy layer from a set of files into a real release surface.

## Why the policy bundle and capability catalog should not drift apart

There is a bad extreme where the policy bundle lives separately, the capability catalog lives separately, and approval rules live separately, with weak links between them.

Then problems appear quickly:

- a capability exists in the catalog, but has no approval contract;
- policy refers to a capability name that no longer exists;
- audit sees a decision, but cannot connect it to a bundle version.

So the practical rule is simple:

- the capability catalog describes what the system can do;
- the policy bundle describes how and under which conditions that capability may be used;
- the approval contract describes where reasoning must stop and hand control to a human.

## Practical checklist

If you want to know whether your policy artifact layer is mature enough, ask:

- Do you have a versioned policy bundle?
- Can you connect the bundle to rollout and incident review?
- Is the approval contract machine-readable, or only described in prose?
- Is it clear which fields an approval request must contain?
- Is there a stable link between the policy bundle and the capability catalog?
- Can you tell which policy version was active for a given trace?

If several answers are “no,” your policy layer exists, but is not yet shaped as a full operational artifact.

## See Also

- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Policy Templates and Checklists by Use Case](policy-templates.en.md)
