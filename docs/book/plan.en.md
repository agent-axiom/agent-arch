# Book Plan

This page is about the structure and status of the book. If you need a reading route, start with [Start Here](../start-here.en.md). If you need the publishing stack and site tooling, that lives on a [separate page](../appendix/stack.en.md).

!!! info "How to read the book by stability level"
    The book has two layers:

    - `Stable core`: Parts I-VII, especially Chapters 1-12 and 18. This is the baseline engineering discipline, and it changes comparatively slowly.
    - `Fast-moving layer`: Chapter 13, Part VIII, and the research-heavy appendix pages. These pages change more often because vendor tooling, eval practice, and threat patterns move faster.

    If you are reading the book for the first time, stay with the stable core first. If you need the newest operational contour, move to the faster layer afterward.

!!! example "Editorial thread: support-triage"
    In the current published layer, the support-triage case acts as the running editorial thread. It connects retrieval, tool execution, duplicate-ticket recovery, traces, SLOs, eval gates, ownership, runtime modules, capability policy, rollout gates, ADLC, assurance, provenance, retirement, misalignment controls, telemetry, and registry. This helps verify that the book structure does not fragment into isolated topics.

## Structure

### Part I. Foundations

Status: `Published`

Question of the part: when an agent is actually justified, and what a minimally mature architecture should look like if you build it not as a prompt trick, but as a system.

- Chapter 1. Why an agent needs a platform, not magic.
- Chapter 2. Reference Architecture for a Safe Agent.
- [Practice. Instructions, routines, and prompt templates](part-i/practical-routines.en.md)
- [Practice. Manager pattern vs handoffs](part-i/practical-manager-handoffs.en.md)

### Part II. Security Perimeter

Status: `Published`

Question of the part: where the real trust boundaries of an agent system live, and what should govern the right to act.

- Chapter 3. Security perimeter and trust boundaries.
- Chapter 4. Tool gateway, approval, and audit trail.

### Part III. Memory and Knowledge

Status: `Published`

Question of the part: how to make memory useful without turning it into an uncontrolled source of errors and leakage.

- Chapter 5. Why agents need memory and why it is dangerous.
- Chapter 6. Short-term, long-term, and profile memory.
- Chapter 7. Retrieval, Compaction, and Background Updates.

### Part IV. Tools and Execution

Status: `Published`

Question of the part: how to turn tool use and execution into a governed contract rather than a chaotic collection of calls.

- Chapter 8. Execution model and tool catalog.
- Chapter 9. Sandbox execution and MCP as an integration contract.
- Chapter 10. Idempotency, retries, rate limits, and rollback boundaries.
- [Practice. MCP and A2A as an integration layer](part-iv/practical-mcp-a2a.en.md)

### Part V. Reliability and Observability

Status: `Published`

Question of the part: how not to guess about system behavior after the first incident, but instead capture run history, define budgets, and produce reviewable judgments.

- Chapter 11. Traces, spans, and structured events.
- Chapter 12. SLO for agent systems.
- Chapter 13. Offline Evals, Online Evals, and Regression Gates.
- [Evidence Spine: From request to rollout judgment](part-v/evidence-spine.en.md)

### Part VI. Organizational Model

Status: `Published`

Question of the part: who owns the agent platform, who holds the quality bar, and how to avoid turning the organization into an agent zoo.

- Chapter 14. Platform team and product teams.
- Chapter 15. Golden paths, shared gateways, and anti-zoo patterns.

### Part VII. Reference Implementation

Status: `Published`

Question of the part: how to assemble runnable structure so the architectural model becomes an executable system.

- Chapter 16. Baseline runtime blueprint.
- Chapter 17. Policy layer and capability catalog.
- Chapter 18. Production rollout checklist.

### Part VIII. Agent System Lifecycle

Status: `Published`

Question of the part: how to live with an agent system for months, release changes, respond to failures, close old contours, and keep the whole estate under control.

- Chapter 19. From SDLC to ADLC.
- Chapter 20. Change management for agent systems.
- Chapter 21. Assurance loop: red teaming, detection, and response.
- Chapter 22. Supply chain, provenance, and approved artifacts.
- Chapter 23. Retirement, replacement, and end-of-life discipline.
- Chapter 24. Agentic misalignment and insider risk.
- Chapter 25. Behavioral evals, control evals, and automated red teaming.
- Chapter 26. AI-native observability, inventory coverage, and detection-ready telemetry.
- Chapter 27. Agent Inventory, Registry, and Sprawl Control.

## Publishing Roadmap

1. Tighten the entry surfaces and the opening act of the book.
2. Keep compressing late-book overlap and maintain chapter-role separation.
3. Strengthen the evidence base where the book makes its strongest claims.
4. Finish the editorial pass on the Russian source manuscript.
5. After the Russian layer stabilizes, sync the `.en` and `.zh` pages.

## What Is Already Done

- The site skeleton on MkDocs and Material.
- The full book structure and published core.
- The runnable `agent_runtime_ref` reference runtime.
- The reference layer with traces, evals, memory, approvals, and lifecycle schemas.
- Practical case studies, policy templates, checklists, and the glossary.

[Go to Part I](part-i/index.en.md){ .md-button .md-button--primary }
