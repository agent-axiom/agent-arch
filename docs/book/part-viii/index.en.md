# Part VIII. Agent System Lifecycle

Up to this point, the book explained how to assemble the architecture, secure it, observe it, and roll changes out safely. But production discipline does not end at go-live.

Once an agent system lives longer than a single demo, a different class of questions appears:

- which changes should count as release-significant;
- how to respond to drift and findings;
- how to preserve the lineage of trusted artifacts;
- how to retire the system;
- how to keep control over the whole estate, not only one agent.

This part answers exactly those questions. It reads the agent system no longer as an architectural diagram, but as a governed lifecycle.

!!! example "Case thread in this part"
    The support-triage case now runs through the whole lifecycle arc: the duplicate-ticket fix becomes an ADLC change set, high-risk change packet, managed assurance finding, approved artifact bundle, retirement control for the old ticket writer, misalignment/control-eval scenario, detection-ready telemetry, and registry record with an owner. That lets the reader see that one incident should change not only code, but evidence, rollout, operations, and accountability.

!!! note "Canonical lifecycle cases"
    In this part, the three canonical cases split across different lifecycle questions. **Support triage** checks write-capability change packets, approvals, and duplicate-ticket recovery evidence. **Internal knowledge assistant** checks corpus ownership, freshness review, access control, and knowledge provenance. **Incident coordination** checks escalation authority, notification side effects, response ownership, and post-incident learning.

!!! info "Short path through this part"
    If you want a fast pass, read it this way:

    - [Chapter 19](chapter-19.en.md): move from SDLC to ADLC as a working frame;
    - [Chapter 20](chapter-20.en.md): decide which changes are release-significant;
    - [Chapter 21](chapter-21.en.md): see how findings turn into response;
    - [Chapter 22](chapter-22.en.md): lock down the lineage of trusted artifacts;
    - [Chapter 23](chapter-23.en.md): close the lifecycle through replacement and retirement;
    - [Chapters 24-27](chapter-24.en.md): extend the same contour into adversarial pressure, judgment, observability, and estate-wide accountability.

## What This Part Solves

- it shows the agent system as a governed lifecycle rather than a one-time launch;
- it separates release judgment from response, lineage, closure, and estate accountability;
- it gives the reader a language for change review, incidents, retirement, and sprawl;
- it helps the reader view a production agent estate as a system with ownership, not as a pile of controls.

## Role Map for This Part

Use this map to keep the late-book chapters from sounding like the same governance idea repeated under different names. The print-friendly version is intentionally short:

- **Lifecycle frame** holds state transitions from design to retirement. Its artifact is the ADLC state model; it is not a new name for SDLC only.
- **Change management** decides which changes require review and rollout gates. Its artifact is the [Change packet](../../appendix/change-rollout-schema.en.md); it is not general project management.
- **Assurance** turns findings into containment, remediation, and ownership. Its artifact is the [Finding and response record](../../appendix/incident-record-schema.en.md); it is not observability or eval scoring.
- **Provenance** preserves trusted artifact lineage and release identity. Its artifact is the [Approved artifact bundle](../../appendix/lifecycle-artifact-schema.en.md); it is not a generic evidence folder.
- **Retirement** closes or replaces systems without losing accountability. Its artifact is the [Retirement plan](../../appendix/lifecycle-artifact-schema.en.md); it is not deleting an old agent.
- **Misalignment and insider risk** names adversarial or incentive-driven misuse paths. Its artifact is the risk scenario and control plan; it is not a duplicate of prompt-injection guidance.
- **Behavioral/control evals** produce release judgments about behavior and controls. Their artifact is the [Eval gate and verifier contract](../../appendix/eval-schema.en.md); they are not incident response.
- **Observability** keeps the evidence substrate visible and queryable. Its artifact is the [Trace and telemetry coverage record](../../appendix/trace-schema.en.md); it is not the owner of governance decisions.
- **Inventory and registry** make the estate answerable through owners and lifecycle state. Their artifact is the [Registry record](../../appendix/registry-operations-handbook.en.md); they are not a loose spreadsheet of agents.

Read the chapters as a chain: lifecycle defines the states, change management controls movement, evals judge readiness, provenance records what was trusted, observability preserves evidence, assurance responds when evidence turns into risk, retirement closes old paths, and registry keeps the whole estate accountable. If two chapters sound like "governance," distinguish them by the artifact they are responsible for leaving after review.

## In This Part

- [Chapter 19. From SDLC to ADLC](chapter-19.en.md)
- [Chapter 20. Change Management for Agent Systems](chapter-20.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](chapter-21.en.md)
- [Chapter 22. Supply Chain, Provenance, and Approved Artifacts](chapter-22.en.md)
- [Chapter 23. Retirement, Replacement, and End-of-Life Discipline](chapter-23.en.md)
- [Chapter 24. Agentic Misalignment and Insider Risk](chapter-24.en.md)
- [Chapter 25. Behavioral Evals, Control Evals, and Automated Red Teaming](chapter-25.en.md)
- [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](chapter-26.en.md)
- [Chapter 27. Agent Inventory, Registry, and Sprawl Control](chapter-27.en.md)

## What You Should Take Away

- a more mature frame for release gates and change review;
- a clear distinction between judgment, response, lineage, observability, and accountability;
- a practical model for how an agent system changes, gets constrained, gets investigated, and eventually gets shut down over time.
