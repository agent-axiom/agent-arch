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
