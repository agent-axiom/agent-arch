# Part VIII. Agent System Lifecycle

Up to this point, the book explained how to assemble the architecture, secure it, observe it, and roll it out safely. But production discipline does not end with a rollout checklist.

In the running support case, this means the system already has a working runtime, policy layer, capability catalog, and limited rollout. Now the question changes: how do you live with that system for months, change it without losing control, and decide when to stop, replace, or retire it.

As soon as the system lives longer than a single demo, a different class of questions appears:

- how agent initiatives enter delivery;
- how design review should work;
- which changes should be treated as risk-bearing;
- how to release model, prompt, policy, and tool changes;
- how to investigate incidents and when to retire a system.

This is where classical engineering discipline meets agent-specific behavior. That is why this part should start not with a “magical new process,” but with a transition from classical SDLC to ADLC.

!!! info "Short path through this part"
    If you want a fast pass, read it this way:

    - [Chapter 19](chapter-19.en.md): establish the frame through the move from SDLC to ADLC;
    - [Chapter 20](chapter-20.en.md): define which agent changes are truly release-bearing;
    - [Chapter 21](chapter-21.en.md) and [Chapter 22](chapter-22.en.md): assemble assurance, provenance, and artifact discipline;
    - [Chapter 23](chapter-23.en.md): close the lifecycle through replacement and retirement.

    Chapters 24-27 extend the same contour through misalignment, behavioral evals, AI-native observability, and agent-estate governance.

If you read this part as one block, the sequence is straightforward:

- first, establish the frame by moving from SDLC to ADLC;
- then define which changes in an agent system are truly release-bearing;
- next, build an assurance loop around red teaming, detection, and response;
- after that, lock down artifact discipline and provenance;
- and finally close the lifecycle through replacement and retirement.

## In this part

- [Chapter 19. From SDLC to ADLC](chapter-19.en.md)
- [Chapter 20. Change Management for Agent Systems](chapter-20.en.md)
- [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](chapter-21.en.md)
- [Chapter 22. Supply Chain, Provenance, and Approved Artifacts](chapter-22.en.md)
- [Chapter 23. Retirement, Replacement, and End-of-Life Discipline](chapter-23.en.md)
- [Chapter 24. Agentic Misalignment and Insider Risk](chapter-24.en.md)
- [Chapter 25. Behavioral Evals, Control Evals, and Automated Red Teaming](chapter-25.en.md)
- [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](chapter-26.en.md)
- [Chapter 27. Agent Inventory, Registry, and Sprawl Control](chapter-27.en.md)

## What you should have by the end

- a coherent lifecycle model for production-grade agent systems;
- a stronger frame for change reviews and release gates;
- a clear connection between evals, incidents, provenance, and ownership;
- a practical language for replacement, retirement, and end-of-life discipline;
- a stronger frame for sabotage-like behavior, control failures, and automated assurance;
- a clear model of observability as an evidence layer for inventory, detection, and governance;
- a working frame for governing an entire agent estate rather than isolated agent systems.
