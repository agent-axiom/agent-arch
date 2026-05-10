# Chapter 2. Reference Architecture for a Safe Agent

!!! info "How to read this chapter"
    Do not try to memorize every layer name on the first pass.

    It is more useful to do three things:

    - follow one support request through the system;
    - see where the system gets the right to act;
    - write down the few mandatory layers without which the request cannot safely reach an external side effect.

## 1. Start Not with Layers, but with One Live Case

Take the same support agent from the previous chapter.

A user writes:

> I have been waiting three days for access activation. Please check the status and create an urgent ticket if the request is stuck.

If you look at the task too simplistically, the next steps can seem obvious:

- the model reads the message;
- selects the right tool;
- checks the status;
- creates a ticket;
- returns a reply.

But a production system cannot run on a hand-wavy version of that flow. Too many important questions remain unanswered:

- who is requesting the action;
- what rights this request has;
- whether the agent is allowed to create tickets at all;
- whether ticket creation requires approval;
- what context may be sent into the model;
- what to do if a tool returns a partial or unstable result;
- how to reconstruct the full path later during an incident.

This is exactly where platform architecture comes from. It does not come from a love of layers. It comes from the need to answer those questions before a risky write path exists.

## 2. The Minimal Shape of an Agent, and Why It Is Not Enough

It helps not to hold the full map in your head right away. At first, it is enough to distinguish two things:

- the minimal core of an agent system;
- the production overlay that turns that core into something safer than a prototype.

The OpenAI practical guide is useful because it starts from a very simple shape: a minimal agent system usually has three things.[^openai-practical]

- `model`
- `tools`
- `instructions`

That is a good starting frame. It helps because it prevents early overengineering.

But it stops being enough for production. The moment you add:

- access to internal systems;
- private data;
- long sessions;
- write-path actions;
- approvals;
- multiple teams and access roles,

the minimal triad stops being an architecture. It remains only the core around which a platform must be built.

This is the proof step after Chapter 1. The earlier claim was that agents need a platform. Here the reason becomes concrete: `model + tools + instructions` is enough to make a prototype behave, but not enough to explain rights, side effects, accountability, and recovery once the system touches reality.

## 2.1. What Belongs to the Runtime Architecture, and What Does Not

It is useful to draw one more boundary here, because teams very often mix runtime design, model training, and the product surface.

Things that usually belong to the runtime architecture of an agent include:

- `model`;
- `instructions`;
- `tools`;
- `memory`;
- planning routines or skills;
- `runtime`;
- guardrails and policies.

But a few things usually do not belong to runtime architecture:

- the training dataset and reward model belong to model development and training, not to the runtime;
- the user interface belongs to the product surface, not to the core agent logic;
- the context window is a property of the chosen model, not a separate architecture layer.

That distinction may sound theoretical, but it is very useful in practice. If tool routing, approval paths, or retrieval discipline start degrading, the cause usually lives in the runtime contour, not in the UI or the reward model.

## 3. How One Request Should Move Through the System

Now look at the same support case as an architectural path.

### 3.1. Ingress

The message should not go straight into the model. First, the system turns it into a normalized request:

- who the user is;
- which tenant the request belongs to;
- which channel it came from;
- what risk class it has;
- which session and `trace_id` it belongs to;
- which policy scope will govern the run.

In other words, what enters the system is not "text," but a managed execution context.

### 3.2. Control Layer

Next the system has to decide what this run is even allowed to do:

- which models may be used;
- which tools are available;
- which actions require approval;
- which limits apply;
- what is forbidden in the current environment.

This is the control plane. It is not responsible for "intelligence." It is responsible for the system's right to act.

### 3.3. Runtime

Then the request enters the runtime, where the execution pattern is chosen:

- a regular workflow is enough here;
- a `single-agent loop` is needed here;
- an approval interrupt is required here;
- this run must checkpoint and continue later.

A good runtime is boring. It does not impress through magic. It makes execution predictable.

### 3.4. Model Layer

Only after that does the model come into play:

- it receives curated context;
- decides the next step;
- proposes a tool call or a text response;
- returns a structured result to the runtime.

The important distinction is this: the model may propose actions, but it should not be the only place where execution rights are decided.

### 3.5. Tool Layer

If the agent wants to check a request status or create a ticket, it should not go into the outside world directly. That is the job of the tool gateway:

- it checks the policy decision;
- requires approval when needed;
- isolates side effects;
- returns the result to the runtime;
- writes an event to the trace.

### 3.6. Tracing and Evaluation

At each step, the system should leave a trail:

- what the model decided;
- which tool was called;
- which policy gate fired;
- whether approval was requested;
- where latency grew;
- where a failure happened.

Without that, you do not have a platform. You have a complicated black box.

## 4. Now the Full Map Makes Sense

If the map still feels dense at this point, do not try to memorize every block name. First answer only three questions:

- where the execution context is formed;
- where the right to act lives;
- where the system leaves enough evidence for investigation and release decisions;
- which orchestration pattern the runtime actually chose for this class of work.

Only now does it become useful to show the whole platform from above.

<div class="diagram-card">
<p>Reference diagram of a safe agent platform</p>

``` mermaid
flowchart TB
    user["User / API / Event"] --> interface["Interface layer"]
    interface --> identity["Identity & session layer"]
    identity --> control["Agent control plane"]
    control --> runtime["Orchestration runtime"]
    runtime --> cognition["Cognition plane"]
    runtime --> memory["Memory & knowledge plane"]
    runtime --> tools["Tool execution plane"]
    runtime --> telemetry["Telemetry & eval plane"]
    tools --> external["External systems / MCP / SaaS"]
    memory --> stores["Vector DB / KB / profile memory"]
    control --> approval["Approval / policy / quotas"]
    telemetry --> audit["Traces / metrics / audit"]
```

</div>

The important thing in this diagram is not the elegance of the layers. It is that each layer answers a failure question the prototype cannot answer on its own:

| Layer | What it does | Why it hurts to skip it |
| --- | --- | --- |
| Interface layer | Chat, API, webhooks, events | Otherwise channels get mixed with execution logic |
| Identity and session layer | User, service account, tenant, request scope | Otherwise IAM, audit, and isolation break down |
| Agent control plane | Policies, approvals, limits, catalogs | Otherwise the system acts without real control |
| Orchestration runtime | Workflow graph, planner, checkpoints | Otherwise execution falls apart as soon as it becomes complex |
| Cognition plane | Model router, prompt assembly, validators | Otherwise the model becomes the center of the world |
| Memory and knowledge plane | State, memory, retrieval | Otherwise context grows without discipline |
| Tool execution plane | Gateway, sandbox, side-effect isolation | Otherwise blast radius gets too large |
| Telemetry and eval plane | Traces, metrics, datasets, regression gates | Otherwise quality cannot be measured or investigated |

## 5. The Five Pillars of a Production Platform

Recent Google Cloud material is useful because it offers another practical frame: not "one smart agent," but five pillars of a production platform.[^google-five-pillars]

- `framework`
- `model`
- `tools`
- `runtime`
- `trust`

This frame is valuable for a very practical reason. It cuts through self-deception.

If you only have:

- a strong model;
- a good prompt;
- a few tools,

but no `runtime` and no `trust`, you still do not have a platform. You have a prototype.

## 6. Which Architectural Decisions Should Be Explicit

Even early on, some decisions should be made explicitly, not implicitly.

### 6.1. Which Context Layers Exist

Google is right to discipline prompt assembly through context layers.[^google-agent-overview][^google-govern]

In practice, it is usually enough to separate:

- `static context`: role, policies, allowed capabilities, fixed instructions;
- `session context`: what lives across the session;
- `turn context`: what belongs only to the current request;
- `cached context`: what should be injected selectively.

The practical rule is simple: the prompt should contain not all available data, but only data with a clear purpose and a clear lifetime.

### 6.2. Where the Right to Act Lives

The model should not have the direct right to execute an external side effect.

That right should live in the combination of:

- policy engine;
- approval logic;
- tool gateway.

This is why the control plane matters so much: it separates "the model proposed" from "the system is allowed to do it."

### 6.3. When to Split into Multiple Agents

The OpenAI practical guide is right not to romanticize `multi-agent` as the default choice.[^openai-practical] Microsoft’s newer architecture guidance is useful here because it makes the escalation path more explicit: teams should first ask whether the problem is still a direct model call, then whether one agent with tools is enough, and only then move into multi-agent orchestration.[^microsoft-orchestration]

That discipline matters because every extra agent introduces:

- another context boundary;
- another coordination path;
- another latency hop;
- another failure surface;
- another ownership and policy boundary.

Splitting is usually justified when:

- one run is already too crowded for a single context;
- subtasks require different tools and different guardrails;
- ownership is split across teams;
- parallelism genuinely reduces latency or cognitive load;
- security boundaries differ enough that one agent should not carry all permissions.

If those signs are absent, one agent with a good workflow graph is almost always simpler and more reliable.

A practical escalation ladder is:

1. `direct model call` for single-step work;
2. `single agent with tools` for one domain with dynamic actions;
3. `multi-agent orchestration` only when specialization, security separation, or parallel decomposition clearly justify the extra runtime complexity.

Anthropic's pattern catalog helps make that ladder less abstract because it names the intermediate workflow shapes teams usually need before full agent autonomy.[^anthropic] In practice, the missing question is often not "do we need an agent?" but "which smaller orchestration pattern already solves this safely enough?"

That usually means checking for these options first:

- `prompt chaining` when the task can be decomposed into fixed serial steps with gates between them;
- `routing` when incoming requests fall into a few classes that deserve different prompts, tools, or downstream paths;
- `parallelization` when confidence or latency improves by splitting independent checks;
- `orchestrator-workers` only when the subtasks are not knowable in advance and must be delegated dynamically;
- `evaluator-optimizer` when iterative critique materially improves the artifact.

This matters architecturally because these are not just prompting tricks. Each pattern changes where checkpoints, approvals, retries, trace boundaries, and ownership should sit in the runtime.

That ladder is useful because it turns architecture into an explicit anti-overengineering discipline. The question is not "can we split this into several agents?" but "what is the lowest-complexity form that still behaves reliably in production?"

## 7. A Fast Maturity Test for Architecture Complexity

A team should not conclude that its architecture is mature only because it already has an agent, some tools, and a layered diagram.

A stronger bar is this:

- the team can explain why the current problem is still a direct model call, a single agent with tools, or a multi-agent system;
- each step up that ladder is justified by real operational pressure rather than novelty;
- extra agents introduce clear specialization or control benefits rather than vague sophistication;
- the architecture removes ambiguity about where action rights, side effects, and approvals live;
- the resulting runtime is still explainable to operators during incidents.

If those conditions are missing, the system may look architected on slides while still being overcomplicated in practice.

## 8. What Should Never Be Mixed Together

There are at least four things worth separating from the beginning:

- **short-term state**: the current execution state;
- **long-term memory**: facts, profiles, episodes;
- **retrieval**: access to external knowledge;[^langgraph-memory]
- **tool execution**: real actions in the outside world.

This separation can look bureaucratic while the system is still small. After the first serious incident, it starts to look like hygiene.

## 9. A Minimal Code Principle

If you want to see the full idea in very compact form, the template looks like this:

```python
from dataclasses import dataclass


@dataclass
class ToolRequest:
    tool_name: str
    actor_id: str
    risk_class: str
    payload: dict


def execute_tool(request: ToolRequest, policy_engine, approval_service, gateway):
    decision = policy_engine.evaluate(request)
    if not decision.allowed:
        raise PermissionError(decision.reason)

    if decision.requires_approval:
        approval_service.require_human_signoff(request, decision)

    return gateway.call(request.tool_name, request.payload)
```

The point is one line long: the model may suggest an action, but the right to execute lives in the gateway and the policy layer, not in the model.

## 10. A Fast Architecture Review for Your Own System

If you already have an agent or agent-like workflow in production, use this chapter as a short review checklist.

You should be able to answer these questions clearly:

- Where is the request normalized into managed execution context?
- Where does the system decide what is allowed?
- Which actions require approval, and where is that enforced?
- Which side effects go only through a gateway or sandbox?
- Which fields are guaranteed to appear in traces?
- What happens after retries, partial failures, or restarts?

If those answers live only in prompts, conventions, or team memory, the architecture is still too implicit.

## 11. What to Take Away from This Chapter

In short, a good agent platform stands on several boring but valuable things:

- explicit ingress context;
- a control plane;
- a separate runtime;
- a separate tool gateway;
- separate traces and evals;
- approvals where they are truly needed.

Architecture is useful not because it makes the diagram prettier. It is useful because it stops the system from falling apart at the first real complication.

## 12. What to Do Right After This Chapter

If you are designing an agent system right now, write down at least this:

1. Where exactly does your execution context begin?
2. Where does the right to act live?
3. Which runtime pattern are you starting with?
4. Which side effects go only through a gateway?
5. Which fields must the team see in traces from day one?

If those things are already written down, an architecture is beginning to exist. If not, you still only have an agent idea.

## 13. Evidence Model for This Chapter

This chapter combines several kinds of evidence:

- **Stable claims:** identity, policy, approval, tool execution, memory, and telemetry should not collapse into the prompt.
- **Vendor practice:** OpenAI, Google Cloud, Microsoft, and Anthropic all describe agents as systems that combine models, tools, instructions, orchestration, and governance rather than as raw model calls.
- **Runtime practice:** gateways, policy engines, approval services, and trace schemas are concrete ways to make the right to act inspectable.
- **Author interpretation:** the exact layer names are less important than the separation of rights, side effects, state, and evidence.
- **Fast-moving area:** productized agent builders and orchestration frameworks will evolve; the review questions at the end should remain useful across those changes.

## 14. What to Read Next

- [Chapter 1. Why an Agent Needs a Platform, Not Magic](chapter-1.en.md)
- [Part II. Security Perimeter](../part-ii/index.en.md)
- [Chapter 3. Security Perimeter and Trust Boundaries](../part-ii/chapter-3.en.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^langgraph-memory]: [LangGraph, Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^google-five-pillars]: [Google Cloud, Achieve agentic productivity with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder)
[^google-agent-overview]: [Google Cloud, Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
[^microsoft-orchestration]: [Microsoft Azure Architecture Center, AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
