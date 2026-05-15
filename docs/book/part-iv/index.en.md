# Part IV. Tools and Execution

Up to this point, we already have three important layers for the same support agent:

- platform architecture;
- the security perimeter;
- memory and retrieval discipline.

Now it is time to move to the place where an agent stops being "smart text" and starts doing real work: checking status, opening a ticket, involving a human, or stopping safely.

<div class="book-cover" markdown="1">

![Cover for the tools and execution part](../../assets/images/part-iv.png)

</div>

This is exactly where the most expensive mistakes usually appear:

- incorrect tool calls;
- unexpected side effects;
- unstable integrations;
- repeated actions without idempotency;
- overly loose access to external systems.

## What This Part Solves

In this part, we break down how to design the execution layer so the agent does not talk to the world directly, but works through clear contracts, limits, and safe gateways.

!!! info "Short path through this part"
    If you want a fast pass, read it this way:

    - [Chapter 8](chapter-8.en.md): understand how the runtime chooses the next step and capability;
    - [Chapter 9](chapter-9.en.md): see how that capability passes through a sandbox and a contract layer;
    - [Chapter 10](chapter-10.en.md): lock down how execution survives retries, timeouts, and uncertain side effects.

    Together, these three chapters give you an execution model you can discuss as a production layer, not as “the agent can call tools”.

!!! note "Part IV canonical case routes"
    In the execution layer, the three canonical cases split across different tool boundaries. **Support triage** checks ticket-write capability, approval gate, idempotency key, and duplicate-ticket recovery. **Internal knowledge assistant** checks retrieval adapter, source attribution, tenant boundary, and read-only MCP contract. **Incident coordination** checks escalation tool, notification side effects, incident state updates, and rollback boundary.

## In This Part

- [Chapter 8. Execution Model and Tool Catalog](chapter-8.en.md)
- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](chapter-9.en.md)
  This chapter continues the same support case at the moment the agent is about to reach an external system and the platform must determine transport, sandbox, and execution boundary.
- [Practice. MCP for Tools, A2A for Agents](practical-mcp-a2a.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](chapter-10.en.md)

## Where It Leads Next

The next move after this part is [Part V](../part-v/index.en.md): how to observe this execution model in production, define SLOs around it, and stop regressions from coming back through rollout.
