# Book Plan

This version of the book is structured as an engineering playbook rather than a framework survey. Each part answers one practical question: what must exist in a production system for an agent to be useful, safe, and manageable?

## Structure

### Part I. Foundations

- What a modern agent is and how it differs from a workflow.
- Why secure architecture starts with a control plane, not with a smart prompt.
- A reference platform for safe agents.

Status: the first chapter is published.

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

## Publishing roadmap

1. Freeze the architectural frame and vocabulary.
2. Expand security into a dedicated layer, not a subsection.
3. Add reference diagrams and operational checklists.
4. Prepare a practical reference implementation.
5. Add eval examples and policy configs.

## What is already done

- GitHub Pages site scaffold.
- Book navigation and structure.
- First part with the reference architecture.
- Separate page on the publishing stack.
- Source base for the next chapters.

[Go to Part I](part-i/index.md){ .md-button .md-button--primary }
