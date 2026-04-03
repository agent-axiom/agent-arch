# Part I. Foundations

The first part answers the main question: what should a **modern secure agent architecture** look like if it is designed not as a toy, but as a platform product.

## What must be understood before implementation

- An agent is not the same as an LLM. The LLM makes only part of the decisions.
- Security cannot be a wrapper added after the MVP. It must be embedded into the runtime.
- Most production use cases benefit less from maximum autonomy than from the right combination of `workflow + guarded autonomy`.
- Multi-agent design is useful not for aesthetics but for context isolation, team ownership, and parallelism.[^anthropic][^langgraph-multi]

## Outcome of this part

By the end of Part I, the reader should have:

- a reference platform diagram for safe agents;
- criteria for when an agent is actually needed and when a workflow is the better choice;
- criteria for choosing between workflow, single-agent, and subagents;
- a list of mandatory layers without which the system will be fragile;
- a vocabulary for discussing architecture with platform, security, and product teams.

## Navigation

- [Chapter 1. Why agents need a platform, not magic](chapter-1.md)
- [Chapter 2. Reference architecture for a safe agent](chapter-2.md)
- [Practice. Instructions, routines, and prompt templates](practical-routines.md)
- [Practice. Manager pattern vs handoffs](practical-manager-handoffs.md)
- [Why this publishing stack was chosen](../../appendix/stack.md)
- [Bibliography and sources](../../appendix/sources.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^langgraph-multi]: [LangChain, Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
