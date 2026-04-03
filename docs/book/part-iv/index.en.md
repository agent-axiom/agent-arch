# Part IV. Tools and Execution

Up to this point, we already have three important layers:

- platform architecture;
- the security perimeter;
- memory and retrieval discipline.

Now it is time to move to the place where an agent stops being "smart text" and starts doing real work.

This is exactly where the most expensive mistakes usually appear:

- incorrect tool calls;
- unexpected side effects;
- unstable integrations;
- repeated actions without idempotency;
- overly loose access to external systems.

In this part, we break down how to design the execution layer so the agent does not talk to the world directly, but works through clear contracts, limits, and safe gateways.

## In This Part

- [Chapter 8. Execution Model and Tool Catalog](chapter-8.en.md)
- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](chapter-9.en.md)
- [Practice. MCP for Tools, A2A for Agents](practical-mcp-a2a.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](chapter-10.en.md)

Part IV is now a coherent execution block; next we move from tooling to system reliability and observability.
