# Part VII. Reference Implementation

Up to this point, we assembled the same system layer by layer:

- architecture and trust boundaries;
- memory;
- execution layer;
- observability;
- operating model.

Now it is time to turn that into a more coherent reference implementation. Not an "ideal framework for every use case", but a practical blueprint of the same support agent and surrounding platform that you can use as a starting point and evolve further.

!!! info "Short path through this part"
    If you want a fast pass, read it this way:

    - [Chapter 16](chapter-16.en.md): see how the same support agent becomes one runtime instead of a pile of local handlers;
    - [Chapter 17](chapter-17.en.md): see how that runtime gets an explicit policy layer and capability catalog;
    - [Chapter 18](chapter-18.en.md): check whether that skeleton is ready for a limited rollout and further growth.

    Together, this shows that the reference implementation is not for demo value. It is for fixing the production system in code.

In this part, I gradually assemble a minimally mature platform:

- a baseline runtime;
- security and policy hooks;
- a capability catalog;
- telemetry wiring;
- a rollout checklist.

## In This Part

- [Chapter 16. Baseline Runtime Blueprint](chapter-16.en.md)
  This chapter continues the same support case at the code layer: where the run loop should live, how to separate policy, memory, and execution, and how not to spread logic across local handlers.
- [Chapter 17. Policy Layer and Capability Catalog](chapter-17.en.md)
  This chapter lifts the same skeleton into the contract layer: which capabilities are allowed at all, where approval is required, and how not to hardcode risk logic into orchestration.
- [Chapter 18. Production Rollout Checklist](chapter-18.en.md)
  This chapter closes the same story through the first limited rollout: whether the support agent is ready for real deployment and what must already be visible before scaling.

After this part, it becomes clear how architecture, safety, memory, execution, and observability form one operational skeleton. But production discipline does not stop there: once the same agent survives its first rollout, the next questions are about change management, assurance, provenance, and retirement.

That is why the next natural step after the reference implementation is [Part VIII. Agent System Lifecycle](../part-viii/index.en.md).
