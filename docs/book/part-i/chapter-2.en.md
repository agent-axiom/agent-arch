# Chapter 2. Reference Architecture for a Safe Agent

## 1. Why a Reference Diagram Is Useful at All

After the first chapter, you should already have the intuition for why "just a smart agent" quickly becomes fragile. The next step is more grounded: understand which layers the system should contain if you want it to survive longer than one presentation.

That is what a reference architecture is for. Not as dogma, but as a baseline.

## 2. Top View: What the Platform Consists Of

Below is a diagram that works well as a starting map.

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

| Layer | Role | Why it is mandatory |
| --- | --- | --- |
| Interface layer | Chat, API, event ingestion, webhooks | Separates user channels from the runtime |
| Identity and session layer | User, service account, thread, tenant, request scope | Needed for IAM, audit, and isolation |
| Agent control plane | Policies, approvals, model policies, tool catalog, quotas | This is where controllability lives |
| Orchestration runtime | Workflow graph, planner, router, subagents, checkpoints | This is where the task is executed |
| Cognition plane | Model router, prompt compiler, structured outputs, validators | The model becomes a component, not the center of the world |
| Memory and knowledge plane | Short-term state, long-term memory, retrieval, summaries | Limits context sprawl |
| Tool execution plane | Sandboxed tools, MCP servers, connectors, side-effect isolation | Reduces blast radius |
| Telemetry and eval plane | Traces, metrics, logs, datasets, graders, regression gates | Makes quality measurable |

## 3. What Happens at Ingress

An incoming request should not simply "fly into the model." First it has to become a normalized event with context.

The minimally useful set:

- `tenant_id`;
- `principal`;
- risk class;
- access policy reference;
- session identifier;
- trace id.

In short: **the request should enter the system not as a message, but as a managed execution context**.

## 4. Why the Control Plane Matters More Than It Seems

This is the layer most demo architectures are missing.

It is responsible not for intelligence, but for the system's right to act:

- which models may be used;
- which tools are available;
- which approvals are required;
- which limits apply;
- which rules are active in dev, staging, and prod.

Example of policy-as-code:

```yaml
agent_policy:
  model_access:
    allowed_models: ["gpt-5.4", "gpt-5-mini", "claude-sonnet"]
    deny_if_contains: ["pci_raw", "prod_secrets"]
  tools:
    read_kb:
      approval: none
    jira_create_ticket:
      approval: manager
    prod_db_write:
      approval: security_and_owner
      allowed_environments: ["staging"]
  runtime:
    max_steps: 24
    max_parallel_subagents: 4
    require_checkpoint_every_step: true
```

## 5. Where Execution Lives

The orchestration runtime chooses the execution pattern:

- deterministic workflow for regulated scenarios;
- routed workflow for branch selection;
- plan-and-execute for long tasks;
- planner + subagents for independent subtasks;
- HITL interrupts for high-risk operations.[^langgraph-hitl][^openai-builder]

The best property of a good runtime is unexpectedly simple: it should be boring.

The more "magic" it contains, the harder it is to predict cost, behavior, and failure.

## 6. Why the Cognition Plane Is Not the Same as One Model

It is more useful to think not in terms of "we have one powerful model", but in terms of a set of manageable components:

- planner model;
- executor model;
- classifier/extractor model;
- structured output validator;
- fallback model.

That helps with quality, cost, and graceful degradation.[^vikulin][^openai-models]

## 7. Why Memory, Knowledge, and Tools Should Not Be Mixed Together

It is useful to separate at least three independent things:

- **short-term state**: the current execution state of the flow;
- **long-term memory**: facts, profiles, episodes;
- **retrieval**: access to external knowledge.[^langgraph-memory]

And separately, a fourth:

- **tool execution**: real actions in the outside world.

That separation feels bureaucratic only until the first serious incident.

## 8. What the Request Path Through the System Looks Like

Below is a more "live" view of how a request moves through the key control points.

<div class="diagram-card">
<p>Request path through the main control points</p>

``` mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant I as Interface
    participant C as Control plane
    participant R as Runtime
    participant T as Tool gateway
    participant A as Audit

    U->>I: Request
    I->>C: Normalization + principal + tenant + risk
    C->>R: Allowed execution context
    R->>C: Request for model/tool action
    C->>T: Policy check / approval / quotas
    T-->>R: Allowed result
    R->>A: Trace + step metadata
    R-->>U: Response
```

</div>

## 9. A Minimal Code Principle

If you want to see it in a very compact form, here is a practical template:

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

The point here is simple: the model may propose an action, but the right to execute lives not in the model, but in the gateway and policy layer.

## 10. Practical Takeaway

A good agent platform stands on several boring but very valuable things:

- explicit ingress context;
- a control plane;
- a separate runtime;
- a separate tool gateway;
- traces and evals;
- approvals where they are needed.

Once those are in place, you can move calmly to the more nervous topic: where exactly the security perimeter sits in such a system.

## 11. What to Read Next

- [Chapter 1. Why an Agent Needs a Platform, Not Magic](chapter-1.en.md)
- [Part II. Security Perimeter](../part-ii/index.en.md)
- [Chapter 3. Security Perimeter and Trust Boundaries](../part-ii/chapter-3.en.md)

[^vikulin]: [Dmitry Vikulin, "Architecture of Reliable AI Agents"](https://vikulin.ai/library/tpost/ai_agent_architecture)
[^langgraph-memory]: [LangGraph, Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
[^langgraph-hitl]: [LangChain Deep Agents, Human-in-the-loop](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop)
[^openai-builder]: [OpenAI, Agent Builder](https://platform.openai.com/docs/guides/agent-builder)
[^openai-models]: [OpenAI, Models](https://developers.openai.com/api/docs/models)
