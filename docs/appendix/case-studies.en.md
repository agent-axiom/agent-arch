# Practical Case Studies

This page answers a simple question: what does the book look like not as abstraction, but as a living system?

Below are three scenarios where architectural layers, guardrails, and orchestration choices can already be discussed as engineering decisions rather than elegant language.

If you need reusable policy artifacts rather than scenarios, go to [Policy Templates](policy-templates.en.md). If you want the next layer of book improvements, open the [Community Roadmap](community-roadmap.en.md).

!!! example "How to read this case now"
    The support triage case has become the book's running thread: start here, then watch the same duplicate-ticket failure move through trust boundaries, tool gateway, memory/retrieval, idempotency, traces, SLOs, eval gates, ownership, runtime, policy, rollout, ADLC, assurance, provenance, retirement, misalignment controls, telemetry, and registry.

!!! note "Canonical case alignment"
    These scenarios correspond to the three canonical cases from the book plan. **Support triage** is Case 1 for write capability, approvals, and duplicate-ticket recovery. **Internal knowledge assistant** is Case 2 for retrieval, memory, access control, freshness, and knowledge provenance. **Incident coordination** is Case 3 for traces, SLOs, escalation, notification side effects, response ownership, and post-incident learning.

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
- **Rollout gate:** canary shows no duplicate writes, and the verifier confirms tenant isolation and the correct approval path.
- **Example incident:** a timeout after `create_ticket` leaves `side_effect_unknown`, and a retry attempts to create a second ticket.
- **Postmortem questions:** where did idempotency fail, who saw the approval state, why did the trace not stop the retry, and which eval should block the regression now?

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
- **Rollout gate:** regression set confirms grounding, role isolation, and correct low-confidence behavior.
- **Example incident:** the agent answers from a stale runbook without citations and exposes a document outside the employee's role.
- **Postmortem questions:** why did retrieval scope expand, which source was trusted, where should the low-confidence stop have fired, and which eval covers stale knowledge?

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
- **Rollout gate:** dry run shows one trace chain, no duplicate side effects, and human approval for high-risk steps.
- **Example incident:** a noisy alert starts two parallel handoffs and sends duplicate notifications into different channels.
- **Postmortem questions:** where did split-brain enter the process, who owned each step, which idempotency keys were missing, and which dry run should have caught the duplicate?

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
