# Part I. Foundations

The first part answers the question that decides whether the rest of the book will even make sense: what should a **modern secure agent architecture** look like if it is designed not as a toy, but as a platform product?

!!! info "Short path through Part I"
    If time is tight, take this route:

    - [Chapter 1](chapter-1.en.md): decide whether you need an agent at all or a normal workflow is enough;
    - [Chapter 2](chapter-2.en.md): follow one request through the reference architecture;
    - [Part II](../part-ii/index.en.md): see where the real trust boundaries live.

    That is already enough to discuss the system as an engineering contour, not as an idea.

## What This Part Solves

- It explains why an agent is not the same thing as an LLM and why the LLM makes only part of the decisions.
- It shows why security cannot be a wrapper added after the MVP, but has to be built into the runtime.
- It argues that most production use cases benefit less from maximum autonomy than from the right combination of `workflow + guarded autonomy`.
- It frames multi-agent design as a control and ownership decision, not an aesthetic one.[^anthropic][^langgraph-multi]
- It quietly sets up the whole reader journey that follows: trust boundaries, memory discipline, execution contracts, evidence capture, health budgets, judgment loops, ownership, runtime embodiment, and lifecycle governance.

## A Fast Self-Check Before You Move On

Before moving into the security perimeter, a reader should already be able to answer four basic questions about their own system:

- Why is this an agent and not just a workflow?
- Where does the right to act actually live?
- Which layers are mandatory before the first risky write path?
- What should stay single-agent for now, and what would justify a split later?

If those answers are still vague, Part I should be treated as a working frame to revisit, not only as introductory theory.

## What You Should Have by the End

By the end of Part I, the reader should have:

- a reference platform diagram for safe agents;
- criteria for when an agent is actually needed and when a workflow is the better choice;
- criteria for choosing between workflow, single-agent, and subagents;
- a list of mandatory layers without which the system will be fragile;
- a vocabulary for discussing architecture with platform, security, and product teams.

## In This Part

- [Chapter 1. Why an Agent Needs a Platform, Not Magic](chapter-1.en.md)
- [Chapter 2. Reference Architecture for a Safe Agent](chapter-2.en.md)
  This chapter continues the same support case from Chapter 1 and shows how one request moves through the platform layers.
- [Practice. Instructions, routines, and prompt templates](practical-routines.en.md)
- [Practice. Manager pattern vs handoffs](practical-manager-handoffs.en.md)
- [Why this publishing stack was chosen](../../appendix/stack.en.md)
- [Bibliography and sources](../../appendix/sources.en.md)

## Where It Leads Next

After this part, the reader should already have a working frame: whether an agent is justified here, what the baseline platform looks like, and where its real trust boundaries begin.

That naturally creates the next question: if this architecture is real, where exactly does it become dangerous? The next logical move is [Part II](../part-ii/index.en.md), where the same request crosses the security perimeter, the tool gateway, and the approval boundary.

From there, the book keeps widening the same argument in order:

- Part II locates trust and action boundaries;
- Part III makes memory part of the operating model;
- Part IV turns execution into contracts and governed tool use;
- Part V introduces capture, health, and judgment;
- Part VI assigns ownership;
- Part VII turns the model into runnable structure;
- Part VIII governs the system through change, response, evidence, and accountability.

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^langgraph-multi]: [LangChain, Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
