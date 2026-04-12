# Part I. Foundations

The first part answers the main question: what should a **modern secure agent architecture** look like if it is designed not as a toy, but as a platform product.

!!! info "Short path through Part I"
    If time is tight, take this route:

    - [Chapter 1](chapter-1.md): decide whether you need an agent at all or a normal workflow is enough;
    - [Chapter 2](chapter-2.md): follow one request through the reference architecture;
    - [Part II](../part-ii/index.en.md): see where the real trust boundaries live.

    That is already enough to discuss the system as an engineering contour, not as an idea.

## What This Part Solves

- An agent is not the same as an LLM. The LLM makes only part of the decisions.
- Security cannot be a wrapper added after the MVP. It must be embedded into the runtime.
- Most production use cases benefit less from maximum autonomy than from the right combination of `workflow + guarded autonomy`.
- Multi-agent design is useful not for aesthetics but for context isolation, team ownership, and parallelism.[^anthropic][^langgraph-multi]

## What You Should Have by the End

By the end of Part I, the reader should have:

- a reference platform diagram for safe agents;
- criteria for when an agent is actually needed and when a workflow is the better choice;
- criteria for choosing between workflow, single-agent, and subagents;
- a list of mandatory layers without which the system will be fragile;
- a vocabulary for discussing architecture with platform, security, and product teams.

## In This Part

- [Chapter 1. Why agents need a platform, not magic](chapter-1.en.md)
- [Chapter 2. Reference architecture for a safe agent](chapter-2.en.md)
  This chapter continues the same support case from Chapter 1 and shows how one request moves through the platform layers.
- [Practice. Instructions, routines, and prompt templates](practical-routines.en.md)
- [Practice. Manager pattern vs handoffs](practical-manager-handoffs.en.md)
- [Why this publishing stack was chosen](../../appendix/stack.md)
- [Bibliography and sources](../../appendix/sources.en.md)

## Where It Leads Next

After this part, the reader should already have a working frame: whether an agent is justified here, what the baseline platform looks like, and where its real trust boundaries begin.

The next logical move is [Part II](../part-ii/index.en.md): take that same request and inspect how it crosses the security perimeter, the tool gateway, and the approval boundary.

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^langgraph-multi]: [LangChain, Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
