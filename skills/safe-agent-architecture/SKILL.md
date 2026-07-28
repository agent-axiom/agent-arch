---
name: "safe-agent-architecture"
description: "Use when designing, building, or reviewing safe AI agents and agentic systems."
version: "v1"
date: "2026-07-05T23:37:40.379Z"
---

# Safe Agent Architecture

Use this skill to turn an agent idea into a controlled system, not a clever demo.

Core principle: an agent needs a platform, not magic. Before writing code, make autonomy, authority, environment, memory, tools, evidence, rollout, and ownership explicit.

## Operating Rule

Never jump straight from a user request to framework boilerplate. First produce a **Safe Agent Architecture Brief**. Only write implementation code after the user has accepted the risk shape or explicitly asks for a prototype with known gaps.

If the user only asks for a quick sketch, keep the brief short. If the agent can read/write data, call external tools, browse, execute code, remember state, act for a user, or run in production, use the full workflow.

## Workflow

1. **Define the job**
   - What outcome should the agent produce?
   - What should remain a normal workflow, script, or UI instead of agent autonomy?
   - What is the minimum useful level of agency?

2. **Classify risk**
   - Use `references/risk-tiers.md`.
   - Treat write actions, external communication, code execution, money, identity, tenant data, memory writes, and incident operations as risk escalators.
   - Prefer the lowest agency tier that can solve the job.

3. **Draw boundaries before tools**
   - Identify actor identity, delegated authority, data classes, tool authorities, sandbox limits, network/secrets posture, and approval boundaries.
   - Use `references/tool-gateway.md` for tools, MCP/A2A, browser, code execution, and approvals.

4. **Design memory and retrieval as controlled subsystems**
   - Use `references/memory-retrieval.md`.
   - Separate short-term context, retrieved knowledge, long-term memory, profile state, and operational state.
   - Do not allow hot-path long-term memory writes without policy and review.

5. **Require observability by construction**
   - Define trace events for run start, retrieval, tool policy decision, tool execution, approval request/decision, memory write decision, verification result, failure, and run complete.
   - Do not rely on free-text logs as the primary evidence surface.

6. **Add evals and rollout gates before production**
   - Use `references/evals-rollout.md`.
   - Include offline evals, behavioral/control evals, tool/retrieval/memory regressions, deployment simulation when relevant, and post-release telemetry.
   - A rollout gate should be able to block expansion.

7. **Close the lifecycle loop**
   - Assign owner, incident path, rollback/disable path, postmortem evidence, deprecation/replacement plan, and registry/inventory entry.
   - If nobody owns the system after launch, the design is incomplete.

## Safe Agent Architecture Brief

Return this structure by default:

```markdown
## Safe Agent Architecture Brief

### 1. Job and Non-Goals
- Intended outcome:
- Non-agent alternative considered:
- What the agent must not do:

### 2. Risk Tier
- Tier:
- Escalators:
- Lowest sufficient agency level:

### 3. Actors and Authority
- Human actor:
- Agent identity:
- Delegated authority:
- Tenant/data boundary:

### 4. Tools and Action Surface
- Tools/capabilities:
- Read-only vs write:
- Approval required for:
- Tool gateway controls:
- Sandbox/network/secrets posture:

### 5. Memory and Retrieval
- Context sources:
- Retrieval filters:
- Memory write policy:
- Poisoning/replay protections:

### 6. Runtime Shape
- Single agent / workflow / manager-workers / handoff:
- Checkpoints and resumability:
- Idempotency/retry/rollback boundaries:

### 7. Evidence and Observability
- Required trace events:
- Audit records:
- Redaction/privacy constraints:

### 8. Evals and Rollout
- Offline eval cases:
- Behavioral/control evals:
- Deployment simulation/tool simulation:
- Rollout gate:
- Post-release telemetry:

### 9. Lifecycle
- Owner:
- Incident path:
- Disable/rollback path:
- Registry entry:
- Retirement plan:

### 10. First Implementation Slice
- Safest useful MVP:
- Explicitly deferred risks:
- Verification before calling it ready:
```

## Default Stance

- Prefer workflow before autonomy.
- Prefer read-only before write.
- Prefer explicit approvals before hidden delegation.
- Prefer fake data and sandbox execution before live side effects.
- Prefer one agent with good tools before multi-agent orchestration.
- Prefer traceable failure over silent success.
- Prefer rollout gates over hope.

## Red Flags

Stop and redesign if you see any of these:

- The agent can write to production without approval or idempotency.
- Tool descriptions, retrieved documents, memory, or web content are treated as trusted instructions.
- A tool has broad credentials because it was convenient.
- The design has no trace schema or audit trail for actions.
- Memory writes happen inside the main response path without policy.
- The team has demos but no evals, rollback, or owner.
- The agent can execute code or browse with ambient secrets.
- Multi-agent orchestration is chosen before a single-agent/workflow baseline is exhausted.

## When Asked To Implement

Before code, ask only the missing questions needed to classify risk and authority. Then propose the Safe Agent Architecture Brief and a smallest safe implementation slice.

When implementation proceeds:

- Keep tool adapters behind a gateway.
- Represent approvals and policy decisions as data, not comments.
- Emit structured events for every authority boundary.
- Add regression tests for idempotency, approval gating, retrieval filtering, memory writes, and rollout decisions as applicable.
- Do not claim production readiness until evals and a rollback/disable path exist.

## References

Load only the relevant reference file:

- `references/risk-tiers.md` for agency/risk classification.
- `references/tool-gateway.md` for tools, MCP/A2A, approvals, sandboxing, and action authority.
- `references/memory-retrieval.md` for knowledge, memory, provenance, tenant filters, and poisoning risks.
- `references/evals-rollout.md` for evals, deployment simulation, rollout gates, and telemetry.
- `references/templates.md` for copyable design/eval/release checklists.

## Common Mistakes

- Turning the book into a lecture instead of a design gate. Be brief, operational, and concrete.
- Treating safety as a final review. Safety boundaries define the runtime shape.
- Recommending a framework first. Framework choice follows the authority model.
- Saying "human in the loop" without specifying payload, approver role, scope, expiry, and audit record.
- Saying "observability" when the design only has logs. Require structured trace events and evidence links.
- Saying "evals" when the design only has a few prompts. Require scenario IDs, expected outcomes, risk labels, and release decisions.
