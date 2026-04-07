# Book Plan

This version of the book is structured as an engineering playbook rather than a framework survey. Each part answers one practical question: what must exist in a production system for an agent to be useful, safe, and manageable?

This page is for structure and status. If you want a role-based reading path, open [Start Here](../start-here.en.md). If you want the publishing-stack rationale, it lives on the dedicated [Publishing Stack](../appendix/stack.en.md) page.

## Structure

### Part I. Foundations

- What a modern agent is and how it differs from a workflow.
- Why secure architecture starts with a control plane, not with a smart prompt.
- A reference platform for safe agents.

Status: the first chapter is published.

What I am strengthening next in this part:

- how to decide whether you need an agent at all or a conventional workflow is enough;
- why `single-agent first` is usually healthier than starting with a multi-agent zoo;
- how to turn instructions, SOPs, and playbooks into routines rather than chaotic prompt paragraphs.

Practical layer already added:

- [Practice. Instructions, routines, and prompt templates](part-i/practical-routines.md)
- [Practice. Manager pattern vs handoffs](part-i/practical-manager-handoffs.md)

### Part II. Security Perimeter

- Agent identity and machine IAM.
- Policy-as-code for models, memory, and tools.
- Prompt injection, data exfiltration, secret leakage, tool abuse.
- Human approval for risky operations.

### Part III. Memory and Knowledge

- Short-term vs long-term memory.
- Retrieval, compaction, summaries, profile memory.
- When memory belongs in the hot path and when it should be background work.

### Part IV. Tools and Execution

- Tool gateway and sandbox execution.
- MCP and contract-based integration with external systems.
- Idempotency, retries, rate limits, rollback boundaries.

What I am strengthening next in this part:

- a practical taxonomy of tools: `data`, `action`, `orchestration`;
- explicit run loop exit conditions;
- criteria for when a single-agent loop should become manager pattern or handoffs.

### Part V. Reliability and Observability

- Traces, spans, structured events.
- SLOs for agent systems.
- Offline evals, online evals, trace grading, regression gates.

### Part VI. Organizational Model

- Platform team vs product teams.
- Templates, golden paths, shared gateways.
- How not to turn an agent platform into a zoo.

### Part VII. Reference Implementation

- Base runtime.
- Security policies.
- Tool catalog.
- Production rollout checklist.

### Part VIII. Agent System Lifecycle

- Chapter 19. From SDLC to ADLC.
- Chapter 20. Change Management for Agent Systems.
- Chapter 21. Assurance Loop: Red Teaming, Detection, and Response.
- Chapter 22. Supply Chain, Provenance, and Approved Artifacts.
- Next: retirement.

Status: the transition, change-management, assurance, and artifact-governance chapters are now added.

## Publishing roadmap

1. Freeze the architectural frame and vocabulary.
2. Expand security into a dedicated layer, not a subsection.
3. Add reference diagrams and operational checklists.
4. Prepare a practical reference implementation.
5. Add eval examples and policy configs.
6. Strengthen the book with decision frameworks: when to use an agent, when a workflow is enough, and when not to move into multi-agent too early.

## What is already done

- GitHub Pages site scaffold.
- Book navigation and structure.
- First part with the reference architecture.
- The first set of practical case studies for production-like scenarios.
- The first set of reusable policy templates and checklists by use case.
- A new lifecycle part that links classical SDLC to ADLC.
- Separate page on the publishing stack.
- Source base for the next chapters.

[Go to Part I](part-i/index.md){ .md-button .md-button--primary }
