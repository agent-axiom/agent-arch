# Book Plan

This version of the book is structured as an engineering playbook rather than a framework survey. Each part answers one practical question: what must exist in a production system for an agent to be useful, safe, and manageable?

This page focuses on structure and status. For a role-based reading path, open [Start Here](../start-here.en.md). For the publishing-stack explanation, use the dedicated [Publishing Stack](../appendix/stack.en.md) page.

!!! info "How to read the book by stability level"
    The book has two layers:

    - `Stable core`: Parts I-VII, especially Chapters 1-12 and 18. These change more slowly because they describe baseline engineering discipline.
    - `Fast-moving layer`: Chapter 13, Part VIII, and the research-heavy appendix pages. These change faster because vendor tooling and research move faster.

    If you are reading the book for the first time, start with the stable core. If you need the newest production contour, move to the fast-moving layer afterward.

## Structure

The manuscript now has a more explicit internal geometry. It is not only a sequence of topics, but a sequence of roles the reader learns to distinguish.

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

- Chapter 11: traces, spans, and structured events as raw evidence capture.
- Chapter 12: SLOs for agent systems as health and risk budgets.
- Chapter 13: offline evals, online evals, trace grading, and regression gates as judgment discipline.

Note: the core ideas in Part V are relatively stable, but Chapter 13 moves faster than Chapters 11 and 12.

Editorial shape: Part V now works as one three-step block, capture -> health -> judgment.

### Part VI. Organizational Model

- Platform team vs product teams.
- Templates, golden paths, shared gateways.
- How not to turn an agent platform into a zoo.

Editorial shape: Part VI is the ownership bridge. It decides who owns the layers that Part V defined technically and that Part VII will embody in code.

### Part VII. Reference Implementation

- Base runtime.
- Security policies.
- Tool catalog.
- Production rollout checklist.

Editorial shape: Part VII is the embodiment bridge, where architecture, policy, ownership, and rollout become runnable structure.

### Part VIII. Agent System Lifecycle

- Chapter 19. From SDLC to ADLC.
- Chapter 20. Change Management for Agent Systems.
- Chapter 21. Assurance Loop: Red Teaming, Detection, and Response.
- Chapter 22. Supply Chain, Provenance, and Approved Artifacts.
- Chapter 23. Retirement, Replacement, and End-of-Life Discipline.
- Chapter 24. Agentic Misalignment and Insider Risk.
- Chapter 25. Behavioral Evals, Control Evals, and Automated Red Teaming.
- Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry.
- Chapter 27. Agent Inventory, Registry, and Sprawl Control.

Status: Part VIII is now assembled as a lifecycle block reinforced with current topics around sabotage-like behavior, control-heavy evals, AI-native observability, and agent-estate governance.

Note: this is the fastest-moving block in the book. The principles are stable, but tooling, benchmarks, vendor guidance, and threat patterns change more often.

Editorial shape: Part VIII now works as a mirrored late-book contour, response -> evidence backbone -> judgment under pressure -> evidence substrate -> accountability -> retirement.

## Publishing roadmap

1. Freeze the architectural frame and vocabulary.
2. Expand security into a dedicated layer, not a subsection.
3. Add reference diagrams and operational checklists.
4. Prepare a practical reference implementation.
5. Add eval examples and policy configs.
6. Strengthen the book with decision frameworks: when to use an agent, when a workflow is enough, and when not to move into multi-agent too early.
7. Preserve editorial role clarity so adjacent operational chapters do not collapse back into overlap.

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
