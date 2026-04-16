# Chapter 1. Why an Agent Needs a Platform, Not Magic

## 1. Start with a Failure, Not with Magic

Imagine a familiar story.

A team builds an internal support agent:

- the agent reads a customer email;
- finds the relevant knowledge-base article;
- creates a ticket;
- asks for human approval when needed.

In a demo, everything looks great. The agent responds quickly, picks tools with confidence, and feels almost autonomous.

The problems appear later:

- in one scenario, the agent pulls an internal note into the user-facing reply;
- in another, it creates the same ticket twice after a retry;
- in a third, the operator cannot tell why the agent escalated the case at all;
- during the first incident, the team cannot quickly reconstruct what context went into the model or which step actually failed.

This is the central point of the whole book: most of the time, what breaks is not the model's "intelligence." What breaks is the engineering system around it.

## 2. What These Systems Usually Lack

When a team thinks about an agent as "an LLM plus a few tools," it almost always underbuilds the most expensive layers:

- explicit trust boundaries;
- a control layer for risky actions;
- approval rules;
- idempotency and rollback boundaries;
- step-level observability;
- a clear lifecycle for change.

That is why an agent can look impressive at first and then become expensive, fragile, and hard to operate.

For that reason, it is more useful to think about a safe agent system not as one smart assistant, but as a platform for controlled execution.

## 3. What Vikulin Framed Well, and What Is No Longer Enough

Dmitry Vikulin's article asks the right starting question: what building blocks does a reliable agent consist of?[^vikulin] That is a good foundation.

But for a production system, a list of blocks is no longer enough. In practice, strong teams move fairly quickly to a stricter engineering frame:

- first they choose the simplest executable pattern;
- risky actions are moved into a separate control layer;
- autonomy is allowed only where policies, tracing, and rollback boundaries already exist.[^anthropic][^openai-evals][^langgraph-durable]

In other words, the question is no longer only what an agent is made of. The question is how to make its behavior controllable under load, across long sessions, and on real write paths.

## 4. Default to Workflow, Not to Agency

This is one of the most useful practical principles in the entire topic.

Anthropic draws a fairly direct distinction between `workflows` and `agents` and recommends starting with the simpler option.[^anthropic] OpenAI reaches a very similar conclusion: an agent is justified only when it buys real useful flexibility, not when it merely makes the system sound modern.[^openai-practical]

Translated into engineering language, the rule is simple:

- if the execution path is known in advance, build a workflow;
- if the system needs a constrained choice of next step inside a narrow boundary, use a `single-agent loop`;
- if the task naturally splits into independent subtasks with different contexts and owners, only then consider `multi-agent`.

This is conservative advice. That is also why it works.

One of Anthropic's most useful practical points is that teams should resist framework-first thinking in the early phase.[^anthropic] If a direct API call plus a small amount of orchestration already solves the task, adding another abstraction layer too early usually makes debugging, prompt inspection, and operational ownership worse, not better.

## 5. When an Agent Is Actually Justified

An agent should be justified by the shape of the task, not by style.

Good signs include:

- the system must make a series of non-obvious decisions while working;
- the rules are too branchy and too expensive to maintain as rigid code;
- the valuable signal lives in unstructured data such as emails, documents, notes, or web content;
- the cost of manual routing is already higher than the cost of controlled agency;
- the task changes often enough that constantly rewriting a deterministic workflow is too expensive.

The signs in favor of an ordinary workflow look different:

- the steps are almost always the same;
- transitions are easy to formalize;
- write-path mistakes are costly;
- explainability and repeatability matter more than flexible reasoning;
- "agent autonomy" sounds appealing, but adds little real value.

## 6. Decision Rules: Workflow, Single-Agent, or Multi-Agent

This is the most useful short frame to start with.

| If the task looks like this | Start with this | Why |
| --- | --- | --- |
| The path is mostly known in advance | `workflow` | Cheaper to operate, easier to test, easier to explain |
| The system needs a constrained choice of next step or tool | `single-agent loop` | Adds flexibility without early complexity explosion |
| There are independent subtasks, different contexts, and different owners | `multi-agent` | Separates responsibility and context |

There is one more practical rule:

- if you cannot explain in one paragraph why this should be an agent, it probably should not be one yet;
- if you cannot explain why this should be `multi-agent`, it is almost certainly premature.

## 7. What Teams Most Often Get Wrong at the Start

The same early mistakes keep repeating:

- choosing an agent before describing the workflow clearly enough;
- calling anything with more than one step `multi-agent`;
- adding a framework before the team can clearly explain the underlying prompts, tool contracts, and failure paths;
- debating prompts and models before defining trust boundaries, approvals, and observability;
- measuring success by the demo, not by what happens after the first retry, the first timeout, and the first incident.

If the system still has no answer to those questions, debate about "more capable agency" is almost always premature.

## 8. Why the "Magic" Breaks Earlier Than It Seems

As long as the scenario is short and safe, things can genuinely look fine. Then the system acquires:

- long context;
- external systems;
- private data;
- approvals;
- multiple access roles;
- expensive side effects.

At that point the main problems are no longer just about "answer quality." They shift into something else:

- cost becomes unpredictable;
- behavior starts to drift;
- results become hard to reproduce;
- incidents become hard to investigate;
- the team is no longer sure it actually controls the write path.

This is where an "agent" stops being just an LLM with tools and becomes a full engineering system.

## 9. Four Principles Worth Building On

### 8.1. Control Matters More Than Autonomy

First build a predictable execution path. Only then expand freedom gradually.

### 8.2. Safety Cannot Be Bolted On

If policy, identity, and approvals are not embedded into the runtime, later you will not be evolving the system. You will be repairing the architecture under pressure.

### 8.3. State Must Be Explicit

Long-running tasks should not lose steps, approvals, or side effects just because a process restarted or a request was replayed.

### 8.4. Observability Matters More Than Impression

If the agent "looks smart" but you have no traces, evals, or step metadata, then you do not control the system.[^openai-sdk][^openai-evals]

## 10. What a Production Team Should Always See

The minimally useful set is very concrete:

- what plan the agent constructed;
- which tools were called;
- what context was sent into the model;
- where quality degraded;
- which approvals were requested;
- whether the runtime followed a fixed workflow, a constrained loop, or a delegated multi-agent path;
- how much each step cost in latency and tokens.

The moment this list disappears from view, the agent starts turning into a black box.

## 11. What to Do Right After This Chapter

If you are designing an agent system right now, do not start with the prompt. Start with three questions:

1. Where is an ordinary workflow enough?
2. Which actions are truly risky and require a separate control layer?
3. Which signals must the team see on day one of production?

If you do not yet have answers to those questions, it is too early to debate "how autonomous" the system should be. First you need an execution platform.

## 12. Short Practical Takeaway

If you remember only one idea from this chapter, let it be this:

> A good agent product starts not with maximum autonomy, but with a predictable platform where autonomy is added gradually.

That is why the next chapter is not about "smartness" in the abstract. It is about the architecture of that platform: which layers need to exist so the system can be launched, observed, and evolved safely.

## 13. What to Read Next

- [Part I. Foundations](index.en.md)
- [Chapter 2. Reference Architecture for a Safe Agent](chapter-2.en.md)
- [Book Plan](../plan.en.md)

[^vikulin]: [Dmitry Vikulin, "Architecture of Reliable AI Agents"](https://vikulin.ai/library/tpost/ai_agent_architecture)
[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^langgraph-durable]: [LangGraph, Durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^openai-sdk]: [OpenAI, Agents SDK](https://developers.openai.com/api/docs/guides/agents-sdk)
[^openai-evals]: [OpenAI, Agent evals](https://platform.openai.com/docs/guides/agent-evals)
