# Risk Tiers and Agency Levels

Use this file to classify the agent before designing tools or code.

## Agency Levels

1. **Answer-only assistant**
   - Produces text.
   - No tools, no memory writes, no side effects.

2. **Read-only tool user**
   - Can retrieve, search, inspect, summarize, or query.
   - No writes to external systems.
   - Needs source grounding and access control.

3. **Drafting assistant**
   - Creates proposed changes, messages, tickets, documents, or plans.
   - Human explicitly applies or sends.
   - Needs provenance and review payloads.

4. **Gated actor**
   - Can perform write actions after approval or policy gate.
   - Needs approval records, idempotency, audit trail, and rollback/disable path.

5. **Autonomous actor**
   - Can act without per-action human approval inside a defined bounded domain.
   - Needs strong policy, eval gates, telemetry, owner, incident playbook, and constrained blast radius.

6. **Multi-agent or delegated runtime**
   - Can spawn, delegate, hand off, coordinate, or run long tasks.
   - Needs parent/worker boundaries, budget controls, shared state rules, merge/reconciliation policy, and delegation traces.

Default: choose the lowest level that solves the job.

## Risk Escalators

Raise the risk tier when any of these appear:

- Production writes or customer-visible actions.
- Money, billing, legal, employment, healthcare, security, or incident response.
- External messages, emails, posts, tickets, deployments, account changes, or notifications.
- Code execution, browser automation, filesystem access, network access, or secrets.
- Cross-tenant data, privileged data, PII, regulated records, or confidential internal data.
- Long-term memory writes, profile updates, or background knowledge updates.
- MCP/A2A/remote tools, delegated agents, or third-party integrations.
- Long-running tasks, resumable sessions, scheduled work, or background execution.

## Minimum Controls by Tier

| Tier | Minimum controls |
| --- | --- |
| Answer-only | Clear non-goals, source limits when needed |
| Read-only | Access filters, source grounding, retrieval trace |
| Drafting | Human apply/send step, provenance, diff/review payload |
| Gated actor | Tool gateway, approval schema, idempotency, audit trail |
| Autonomous actor | Policy bundle, eval gate, telemetry, rollback/disable path, owner |
| Multi-agent/delegated | Delegation trace, worker-safe tools, budget limits, join/reconciliation policy |

## Output

Always state:

- selected tier;
- escalators found;
- why a lower tier is insufficient or why it is enough;
- controls required before moving up a tier.
