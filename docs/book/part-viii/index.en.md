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
    - [Chapter 21](chapter-21.en.md): treat drift, findings, and containment as one assurance response loop;
    - [Chapter 22](chapter-22.en.md): lock down provenance, approved artifacts, and contract lineage as the evidence backbone that preserves what was approved, what version was active, and which governed artifact set a later decision relied on;
    - [Chapter 23](chapter-23.en.md): close the lifecycle through replacement, retirement, and runtime-control shutdown;
    - [Chapters 24-27](chapter-24.en.md): extend the same discipline into adversarial pressure, eval judgment, observability evidence, and estate accountability.

    Read as one argument, this part continues the exact system assembled in Part VII: Chapter 19 provides the lifecycle frame, Chapter 20 turns release-bearing change into operational judgment, Chapter 21 makes assurance the response function, Chapter 22 fixes the evidence backbone, Chapter 23 closes the lifecycle, and Chapters 24-27 extend the same system into adversarial pressure, judgment, evidence substrate, and estate accountability.

## What This Part Solves

This part makes a sequence of reader promises:

- after the opening chapters, you should be able to see an agent system as a governed lifecycle rather than a one-time launch;
- after the middle chapters, you should be able to distinguish response, evidence backbone, lifecycle closure, adversarial pressure, judgment, observability substrate, and accountability as separate operational roles;
- by the end, you should be able to read a production agent estate as one managed contour rather than a loose pile of controls.

More concretely, this part:

- turns the reference implementation into a managed lifecycle;
- connects change management, assurance response, evidence lineage, eval judgment, observability evidence, runtime-control governance, interruption/expiry/re-init discipline, delegated authorization lineage, and estate accountability into one operational contour;
- separates stable engineering discipline from fast-moving vendor and research details.

If you read this part as one block, the sequence is straightforward:

- first, establish the frame by moving from SDLC to ADLC;
- then define which changes in an agent system are truly release-bearing;
- next, treat assurance as the operational response loop for drift, findings, and control failure;
- after that, lock down artifact discipline, provenance, and contract/schema governance as the evidence backbone that preserves release identity and decision lineage, rather than detection telemetry or estate ownership;
- then close the lifecycle through replacement, retirement, and runtime-control shutdown;
- and finally extend the same discipline into adversarial pressure, eval judgment, observability evidence, and whole-estate accountability.

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

## What you should have by the end

- a coherent lifecycle model for production-grade agent systems;
- a stronger frame for change reviews and release gates;
- a clear distinction between assurance response, provenance/evidence backbone, eval judgment, observability evidence, and estate accountability;
- a practical language for replacement, retirement, end-of-life discipline, and runtime-control shutdown;
- a stronger frame for sabotage-like behavior, control failures, contract drift, and adversarial assurance;
- a clear model of observability as an evidence layer rather than a generic telemetry bucket;
- a working frame for governing an entire agent estate rather than isolated agent systems;
- a clearer sense of how Part VIII works as one continuous operating model rather than a loose set of security chapters.
