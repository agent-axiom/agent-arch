# Practical Case Studies

This page answers a simple question: what does the book look like not as abstraction, but as a living system?

Below are three scenarios where architectural layers, guardrails, and orchestration choices can already be discussed as engineering decisions rather than elegant language.

If you need reusable policy artifacts rather than scenarios, go to [Policy Templates](policy-templates.en.md). If you want the next layer of book improvements, open the [Community Roadmap](community-roadmap.en.md).

!!! example "How to read this case now"
    The support triage case has become the book's running thread: start here, then watch the same duplicate-ticket failure move through trust boundaries, tool gateway, memory/retrieval, idempotency, traces, SLOs, eval gates, ownership, runtime, policy, rollout, ADLC, assurance, provenance, retirement, misalignment controls, telemetry, and registry.

!!! note "Canonical case alignment"
    These scenarios correspond to the three canonical cases from the book plan. **Support triage** is Case 1 for write capability, approvals, and duplicate-ticket recovery. **Internal knowledge assistant** is Case 2 for retrieval, memory, access control, freshness, and knowledge provenance. **Incident coordination** is Case 3 for traces, SLOs, escalation, notification side effects, response ownership, and post-incident learning.

## Cross-chapter route

Keep these cases beside the main text as coverage checks:

- **Chapter 1:** choice between workflow, single-agent loop, and multi-agent shape;
- **Chapter 2:** path through the reference architecture, control plane, and data boundaries;
- **Chapters 3-4:** trust boundaries, approvals, policies, and the agent's right to act;
- **Chapters 5-7:** memory, retrieval, freshness, knowledge provenance, and poisoning defense;
- **Chapters 8-10:** tool gateway, MCP/A2A, idempotency, retries, and rollback;
- **Chapter 13:** evals, verifier, and regression gates;
- **Chapter 18:** rollout readiness and pre-scale review;
- **Chapters 21-27:** lifecycle, assurance, provenance, retirement, telemetry, and registry.

## Industrial runtime patterns

These case studies are easier to read next to industrial examples. They do not mean the reader should copy a vendor product, but they show which production shapes are becoming recognizable.

### Cloudflare Agents SDK: agent as a named durable object

Cloudflare Agents SDK shows a pattern where an agent is not only a transient loop around a model, but an addressable `Agent` instance on top of a Durable Object: it has a stable name, durable SQL/key-value state, WebSocket connections, scheduled tasks, wakeups, and hibernation. The architectural lesson for the book is simple: when an agent is bound to a real-world entity — customer case, tenant workspace, incident room, device, project, or research dossier — the runtime should make it clear who owns state, which runs changed it, which scheduled tasks can wake the instance, and which traces prove safe resume.

The practical contract is: **stable name → durable state → wake/hibernate → scheduled/background work → approval gates → trace evidence**. That ties the chapters on memory, background updates, execution, traces, and rollout into one shape: a schedule should not be an invisible callback, a WebSocket UI should not expose all agent state, and an approval should live where the side effect actually happens.

### GitHub Copilot cloud agent: cloud coding agent contract

GitHub Copilot cloud agent shows a different production shape: the agent receives work from GitHub, an IDE, CLI, API, or integration; researches the repository; plans changes; pushes code to a separate branch; exposes session logs; and then opens a pull request for human review. The important point is not merely that “an agent writes code,” but that autonomy is packaged inside a familiar engineering lifecycle.

For this book, the useful contract is: **request/issue → isolated task session → branch → commits/logs → validation/security checks → human review → pull request**. The branch becomes the change boundary, session logs become the observability surface, the PR becomes the approval gate, and allowing GitHub Actions to run on the agent branch becomes a separate risk decision because workflows may reach secrets or write permissions. The same pattern should carry into other cloud coding agents: an autonomous worker may do preparatory work, but merge, privileged workflows, and production impact should remain reviewable control points.

## Case 1. Support triage

### What the system does

The agent receives an incoming customer request, gathers context, checks ticket history, and selects the next safe step:

- answer immediately;
- ask for clarification;
- create a ticket;
- escalate to a human.

### Why an agent is justified here

An agent makes sense here because:

- incoming messages are unstructured;
- the decision depends on a combination of text, account history, and policy;
- the path is not fixed, but it also does not require full autonomy.

This is a good candidate for `workflow + guarded agent loop`.

### Recommended shape

- one main triage agent;
- read-heavy tools for customer profile and ticket history;
- a write tool only for `create_ticket`;
- an approval boundary for sensitive actions;
- structured decision output for every run.

### Main risks

- prompt injection through the customer message;
- leakage of neighboring tenant context;
- unnecessary write action during unstable integrations;
- too much freedom in the triage agent.

### What matters most in the architecture

- strict separation of instructions from customer text;
- no direct helpdesk API access for the agent;
- stop conditions stored in the triage routine;
- logging of all write intents and approvals.

### Operational minimum

- **Success criteria:** the answer or ticket is created once, in the right tenant context, with an explainable basis.
- **Failure criteria:** unnecessary write action, neighboring-context leakage, lost approval, or no recoverable trace.
- **Minimum telemetry:** `session_id`, `trace_id`, selected action, retrieval sources, policy decision, approval state, and idempotency key.
- **Minimum eval dataset:** normal request, ambiguous request, prompt-injection attempt, retry after timeout, and duplicate-ticket scenario.
- **Approval model:** simple ticket creation can proceed under policy; priority changes, escalations, mass notifications, and retries after unknown side effects require fresh approval.
- **Memory policy:** long-term memory must not store customer text as trusted fact; only validated tenant-scoped preferences with provenance, TTL, and cleanup support are allowed.
- **Tool risk profile:** profile and history reads are low risk; ticket creation is medium risk with idempotency; status, priority, or recipient changes are high risk with approval.
- **MCP/A2A exposure:** the support MCP server must be in the approved registry and filter returned values; A2A handoff to support must not transfer write authority without a separate decision.
- **Rollout gate:** canary shows no duplicate writes, and the verifier confirms tenant isolation and the correct approval path.
- **Example incident:** a timeout after `create_ticket` leaves `side_effect_unknown`, and a retry attempts to create a second ticket.
- **Postmortem questions:** where did idempotency fail, who saw the approval state, why did the trace not stop the retry, and which eval should block the regression now?
- **Retirement condition:** the old ticket-write path is closed, pending approvals have expired, the tool principal is revoked, and the registry points only to the new write contract.

### Where to read in the book

- [Chapter 3. Security Perimeter and Trust Boundaries](../book/part-ii/chapter-3.en.md)
- [Chapter 8. Execution Model and Tool Catalog](../book/part-iv/chapter-8.en.md)
- [Practice. Instructions, Routines, and Prompt Templates](../book/part-i/practical-routines.en.md)

## Case 2. Internal knowledge assistant

### What the system does

This agent helps employees find knowledge across documentation, runbooks, tickets, and internal wiki pages.

It:

- understands the question;
- performs retrieval;
- assembles a grounded answer;
- shows sources;
- and when confidence is low, limits the answer instead of inventing.

### Why one agent is often enough here

In this case, many teams move into multi-agent too early. Usually they do not need to.

Most of the time, it is enough to have:

- one agent loop;
- a strong retrieval pipeline;
- a separate policy layer;
- explicit marking of untrusted content;
- quality gates for answer generation.

### Main risks

- retrieval noise;
- role-inappropriate access to documents;
- leakage from private knowledge zones;
- hallucinations under weak grounding.

### What matters most in the architecture

- tenant- and role-scoped retrieval;
- short-term state separated from long-term memory;
- source references in the output;
- traces for retrieval and answer assembly.

### Operational minimum

- **Success criteria:** the answer is grounded in allowed sources, shows citations, and honestly limits confidence.
- **Failure criteria:** answer without sources, role-inappropriate access, mixed short-term state and long-term memory, or hallucinated policy.
- **Minimum telemetry:** query, retrieval scope, source IDs, confidence signal, denied sources, and answer-grounding verdict.
- **Minimum eval dataset:** known answer, insufficient context, role-denied document, conflicting sources, and stale knowledge.
- **Approval model:** reading allowed sources needs no approval; memory writes, retrieval-scope expansion, and sensitive answers require policy approval or human review.
- **Memory policy:** short-term state is cleared after the session; long-term memory stores only validated facts with provenance, TTL, tenant scope, and no writes from untrusted text.
- **Tool risk profile:** retrieval from the approved corpus is low risk; memory writes and corpus updates are medium risk; access expansion and tenant-filter changes are high risk.
- **MCP/A2A exposure:** MCP retrieval must return source identifiers and access labels; A2A expert handoff may share the question and selected citations, not the full hidden session context.
- **Rollout gate:** regression set confirms grounding, role isolation, and correct low-confidence behavior.
- **Example incident:** the agent answers from a stale runbook without citations and exposes a document outside the employee's role.
- **Postmortem questions:** why did retrieval scope expand, which source was trusted, where should the low-confidence stop have fired, and which eval covers stale knowledge?
- **Retirement condition:** the stale corpus, embeddings, and memory-write rules are disabled, and the replacement corpus passes provenance and access review.

### Where to read in the book

- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](../book/part-iii/chapter-5.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](../book/part-iii/chapter-7.en.md)
- [Chapter 11. Traces, Spans, and Structured Events](../book/part-v/chapter-11.en.md)

## Case 3. Incident coordination

### What the system does

The agent helps during an incident:

- gathers monitoring signals;
- enriches them with context;
- creates an incident thread;
- proposes the next runbook step;
- transfers the task to the right role.

This is no longer just a chat assistant. It is an operational system component.

### Why orchestration discipline matters especially here

This is where teams often make one of two mistakes:

- one overloaded manager agent;
- or handoffs introduced too early, with responsibility getting lost.

A good starting shape is usually:

- manager pattern for intake and coordination;
- handoffs only where a real role boundary begins;
- all write actions going through capability contracts.

### Main risks

- false confidence under noisy alerts;
- repeated side effects;
- loss of audit trail during handoffs;
- overly broad runtime permissions.

### What matters most in the architecture

- one trace for the entire incident run;
- explicit ownership at every handoff;
- idempotency for ticketing and notifications;
- human approval for risky remediation actions.

### Operational minimum

- **Success criteria:** the incident has one trace, the right owner, and one agreed next step.
- **Failure criteria:** duplicate notifications, lost handoff responsibility, risky remediation without approval, or split-brain across channels.
- **Minimum telemetry:** alert source, incident thread ID, handoff owner, runbook step, write intents, approvals, and notification idempotency keys.
- **Minimum eval dataset:** noisy alert, duplicate notification, wrong-owner handoff, missing runbook context, and risky remediation request.
- **Approval model:** thread creation and next-step suggestions can run under policy; escalation, external notifications, and remediation actions require the incident owner or on-call approver.
- **Memory policy:** incident working memory lives until post-incident review closes; only approved lessons, runbook updates, and artifact links persist long term.
- **Tool risk profile:** reading alerts and runbooks is low risk; creating the thread and notifying the team is medium risk; remediation actions and external notifications are high risk.
- **MCP/A2A exposure:** monitoring and notification MCP tools need narrow tokens; A2A responder handoff requires a correlation ID, delegation depth, and accountability-return rule.
- **Rollout gate:** dry run shows one trace chain, no duplicate side effects, and human approval for high-risk steps.
- **Example incident:** a noisy alert starts two parallel handoffs and sends duplicate notifications into different channels.
- **Postmortem questions:** where did split-brain enter the process, who owned each step, which idempotency keys were missing, and which dry run should have caught the duplicate?
- **Retirement condition:** the emergency-only path is closed, temporary tokens and notification channels are revoked, and the registry keeps only active roles and runbooks.

### Where to read in the book

- [Practice. Manager Pattern vs Handoffs](../book/part-i/practical-manager-handoffs.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](../book/part-iv/chapter-10.en.md)
- [Chapter 18. Production Rollout Checklist](../book/part-vii/chapter-18.en.md)

## What to Do Next

The best way to read them is not sequentially, but as a map:

- first choose the case closest to your task;
- then walk through the linked chapters;
- then come back and check whether your design is becoming more complex than it needs to be.

If the book is going to be useful to the community, these pages should eventually grow the fastest: they turn architecture into engineering leverage.
