# Chapter 1. Why an Agent Needs a Platform, Not Magic

## 1. Where the Usual Mistake Starts

When people build an agent system for the first time, they almost always feel the same temptation:

- take a strong model;
- connect a couple of tools;
- write an ambitious prompt;
- and see how "autonomous" the agent becomes.

Sometimes that even works in a demo. But the moment you start thinking about production, an unpleasant truth shows up: the main problem is not how smart the agent is. The main problem is how controllable it is.

## 2. What Vikulin Framed Well, and What Is No Longer Enough

Dmitry Vikulin's article frames the starting question well: what building blocks does a reliable agent actually consist of?[^vikulin] That is a good place to begin. But if you want to bring the system into real use, a list of blocks is no longer enough.

In practice, strong teams quickly move to a different picture:

- first they choose the **simplest executable pattern**;
- dangerous actions are moved into a separate **control plane**;
- autonomy is allowed only where **policy, telemetry, and rollback boundaries** already exist.[^anthropic][^openai-evals][^langgraph-durable]

Because of that, it is more useful to design a modern system not as "one smart agent", but as a platform for safe agent execution.

## 3. Workflow by Default, Agency by Necessity

Anthropic is quite direct about separating `workflows` from `agents` and recommends starting with the simpler option.[^anthropic] This is one of the most useful practical principles in the whole topic.

If you translate that into engineering language, it sounds like this:

- if the execution path is known, write a workflow;
- if tool choice is needed inside a narrow boundary, use a single-agent loop;
- if the task naturally splits into independent subtasks, introduce subagents;
- if you cannot explain why autonomy is needed, then you probably do not need it yet.

That advice is a bit boring, but it works surprisingly well.

## 4. When an Agent Is Actually Needed, and When It Is Not

One of the healthiest ideas in OpenAI's practical guide is that an agent is not justified just because the task sounds modern.[^openai-practical]

An agent starts to make sense when at least one of these is true:

- the system must make a series of non-obvious decisions while working;
- the rules are too branchy and too expensive to maintain as rigid code;
- the useful signal lives inside unstructured data such as emails, documents, notes, or web content.

If the situation looks different, a workflow is often the more honest choice:

- the steps are almost always the same;
- transitions are easy to formalize;
- explainability and repeatability matter more than flexible reasoning;
- the write-path risk is high, while the value of autonomy is weak.

A practical rule of thumb:

- `workflow` is best when the path is known in advance;
- `single-agent loop` is best when the path is flexible but the boundary is narrow;
- `multi-agent` is worth it only when one loop is already too crowded in terms of context, ownership, or parallelism.

In short: agency should buy you useful flexibility, not replace a clear design with a fashionable one.

## 5. Why the "Magic" Breaks Earlier Than It Seems

There are several reasons why relying only on a smart model becomes expensive very quickly:

- unpredictable cost;
- behavioral drift;
- weak auditability;
- poor repeatability of results;
- hard incident investigation.

The most unpleasant part is that the problem is often not visible right away. As long as the scenario is short and safe, everything looks fine. Then you add:

- long context;
- external systems;
- private data;
- approvals;
- different access roles,

and the system suddenly stops being "just an LLM with tools."

## 6. Four Principles Worth Building On

### 5.1. Control Before Autonomy

First you build a predictable path, and only then expand the agent's freedom.

### 5.2. Safety Cannot Live on the Side

If policy, identity, and approvals are not embedded into the runtime, later you will be fixing the architecture in emergency mode instead of evolving it.

### 5.3. State Must Be Explicit

Long tasks should not lose steps, approvals, or side effects just because someone restarted a process.

### 5.4. Observability Matters More Than Impression

If the agent "looks smart" but you have no traces, evals, or step metadata, then you simply do not control the system.[^openai-sdk][^openai-evals]

## 7. What a Production Team Should Always See

The minimally useful set looks like this:

- what plan the agent built;
- which tools were called;
- what context was passed into the model;
- where quality degraded;
- how much each step cost in latency and tokens.

The moment this list disappears from view, the agent starts turning into a black box.

## 8. Short Practical Takeaway

If you remember only one idea from this chapter, let it be this:

> A good agent product starts not with maximum autonomy, but with a predictable platform where autonomy is added gradually.

That is why the next chapter is not about "smartness", but about platform architecture: which layers need to exist so that all of this can be operated safely at all.

## 9. What to Read Next

- [Part I. Foundations](index.en.md)
- [Chapter 2. Reference Architecture for a Safe Agent](chapter-2.en.md)
- [Book Plan](../plan.en.md)

[^vikulin]: [Dmitry Vikulin, "Architecture of Reliable AI Agents"](https://vikulin.ai/library/tpost/ai_agent_architecture)
[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^langgraph-durable]: [LangGraph, Durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^openai-sdk]: [OpenAI, Agents SDK](https://developers.openai.com/api/docs/guides/agents-sdk)
[^openai-evals]: [OpenAI, Agent evals](https://platform.openai.com/docs/guides/agent-evals)
