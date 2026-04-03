# Practical Case Studies

This page answers a simple question: what does the book look like not as abstraction, but as a living system?

Below are three scenarios where architectural layers, guardrails, and orchestration choices can already be discussed as engineering decisions rather than elegant language.

## Case 1. Support Triage Agent

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

### Where to read in the book

- [Chapter 3. Security Perimeter and Trust Boundaries](../book/part-ii/chapter-3.en.md)
- [Chapter 8. Execution Model and Tool Catalog](../book/part-iv/chapter-8.en.md)
- [Practice. Instructions, Routines, and Prompt Templates](../book/part-i/practical-routines.en.md)

## Case 2. Internal Knowledge Agent

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

### Where to read in the book

- [Chapter 5. Why Agents Need Memory and Why It Is Dangerous](../book/part-iii/chapter-5.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](../book/part-iii/chapter-7.en.md)
- [Chapter 11. Traces, Spans, and Structured Events](../book/part-v/chapter-11.en.md)

## Case 3. Incident Coordination Agent

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

### Where to read in the book

- [Practice. Manager Pattern vs Handoffs](../book/part-i/practical-manager-handoffs.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](../book/part-iv/chapter-10.en.md)
- [Chapter 18. Production Rollout Checklist](../book/part-vii/chapter-18.en.md)

## How to use these case studies

The best way to read them is not sequentially, but as a map:

- first choose the case closest to your task;
- then walk through the linked chapters;
- then come back and check whether your design is becoming more complex than it needs to be.

If the book is going to be useful to the community, these pages should eventually grow the fastest: they turn architecture into engineering leverage.
