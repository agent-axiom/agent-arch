# Part VIII. Agent System Lifecycle

Up to this point, the book explained how to assemble the architecture, secure it, observe it, and roll it out safely. But production discipline does not end with a rollout checklist.

As soon as the system lives longer than a single demo, a different class of questions appears:

- how agent initiatives enter delivery;
- how design review should work;
- which changes should be treated as risk-bearing;
- how to release model, prompt, policy, and tool changes;
- how to investigate incidents and when to retire a system.

This is where classical engineering discipline meets agent-specific behavior. That is why this part should start not with a “magical new process,” but with a transition from classical SDLC to ADLC.

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

## What you should have by the end

- a coherent lifecycle model for production-grade agent systems;
- a stronger frame for change reviews and release gates;
- a clear connection between evals, incidents, provenance, and ownership;
- a practical language for replacement, retirement, and end-of-life discipline;
- a stronger frame for sabotage-like behavior, control failures, and automated assurance;
- a clear model of observability as an evidence layer for inventory, detection, and governance.
