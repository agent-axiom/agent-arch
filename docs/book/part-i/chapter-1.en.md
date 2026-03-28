# Chapter 1. Modern Secure Architecture

## 1. From reliable agents to a secure platform

Dmitry Vikulin's article asks the right foundational question: what building blocks make up a reliable agent.[^vikulin] For 2026, that is no longer enough. In practice, leading teams converge on a different pattern:

- choose the **simplest executable pattern** first;
- move risky actions into a dedicated **control plane**;
- allow autonomy only where **policy, telemetry, and rollback boundaries** exist.[^anthropic][^openai-evals][^langgraph-durable]

That is why it is more useful to design a modern system not as "one smart agent" but as a **platform for safe agent execution**.

## 2. Architectural principles

### 2.1. Workflow by default, agency only where needed

Anthropic explicitly separates `workflows` and `agents` and recommends starting with the simpler option.[^anthropic] That leads to a strong platform principle:

- use a workflow when the execution path is known;
- use a single-agent loop when tool choice is needed inside a narrow boundary;
- use subagents when the task naturally decomposes into independent subtasks;
- if you cannot explain why autonomy is needed, you probably do not need it yet.

### 2.2. Every risky operation goes through a policy boundary

The model should not directly read secrets, write into critical systems, or make unrestricted external calls. Any access to models, memory, and tools should pass through gateways with shared checks:

- authentication and authorization;
- redaction and data classification;
- prompt injection checks;
- human approval for sensitive actions;
- full tracing of both the decision and the execution event.[^owasp][^anthropic-security][^nist-genai]

### 2.3. State must be explicit and resumable

Long-running agent tasks fail not only because of the model, but because state is lost. LangGraph documentation places durable execution and checkpoints at the center of the orchestration runtime.[^langgraph-durable] In practice this means:

- task state is stored outside the process;
- steps are idempotent;
- side effects are isolated;
- execution can resume after a failure or a pause for human approval.

### 2.4. Observability matters more than "magic"

OpenAI and other platforms increasingly center traces, evals, and trace grading, because without them the agent remains a black box.[^openai-sdk][^openai-evals] The production team must be able to see:

- what plan the agent produced;
- which tools were called;
- which context was sent to the model;
- where quality degraded;
- how much each step cost in latency and tokens.

## 3. Reference architecture

The table below can serve as a baseline for an enterprise safe-agent platform.

| Layer | Purpose | Why it is mandatory |
| --- | --- | --- |
| Interface layer | Chat, API, event ingestion, webhooks | Separates user channels from the runtime |
| Identity and session layer | User, service account, thread, tenant, request scope | Required for IAM, audit, and isolation |
| Agent control plane | Policies, approvals, model policies, tool catalog, quotas | This is where controllability lives |
| Orchestration runtime | Workflow graph, planner, router, subagents, checkpoints | This is where the task actually runs |
| Cognition plane | Model router, prompt compiler, structured outputs, validators | The model becomes a component, not the center of the world |
| Memory and knowledge plane | Short-term state, long-term memory, retrieval, summaries | Keeps context growth under control |
| Tool execution plane | Sandboxed tools, MCP servers, connectors, side-effect isolation | Reduces blast radius |
| Telemetry and eval plane | Traces, metrics, logs, datasets, graders, regression gates | Makes quality measurable |

## 4. How the layers interact

### 4.1. Interface layer

An incoming request should not go directly to the orchestrator. First it should receive:

- `tenant_id`;
- `principal`;
- a risk class;
- a link to the active access policy;
- a session and trace identifier.

This makes audit and incident investigation possible from the very first step.

### 4.2. Agent control plane

This is the key layer missing from most demo architectures. It is responsible not for intelligence itself, but for the **right to act intelligently**.

At minimum, it should contain:

- a model catalog with allowed use cases;
- a tool catalog with required approval levels;
- redaction and data loss prevention rules;
- budgets for cost, latency, and agent loop depth;
- environment policies for dev, staging, and prod.

Example policy-as-code:

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

### 4.3. Orchestration runtime

This layer chooses the execution pattern:

- deterministic workflow for regulated scenarios;
- routed workflow for branch selection;
- plan-and-execute for long tasks;
- planner + subagents for independent subtasks;
- HITL interrupts for high-risk operations.[^langgraph-hitl][^openai-builder]

The main engineering rule here is simple: the orchestration runtime should be **boring**. The more magic it contains, the harder it becomes to predict cost, behavior, and failure modes.

### 4.4. Cognition plane

This is not one large model, but a controlled set of components:

- planner model;
- executor model;
- classifier or extractor model;
- structured output validator;
- fallback model for degraded situations.

This cascading design matches model-routing and graceful-degradation practice: expensive reasoning is used only where it is actually needed.[^vikulin][^openai-models]

### 4.5. Memory and knowledge plane

Modern agent memory is split into at least two zones:

- **short-term state**: current execution state, tool results, intermediate decisions;
- **long-term memory**: user facts, profiles, episodes, domain artifacts.[^langgraph-memory]

It is important not to mix memory with retrieval:

- memory stores what the system decided to remember;
- retrieval fetches relevant documents from an external knowledge store;
- compaction and summarization reduce noise in the active context.

### 4.6. Tool execution plane

A tool should not be treated as a simple function call. It is a separate risk zone.

A safe tool plane includes:

- a sandbox or restricted execution environment;
- an allowlist of tools and parameters;
- no direct network access where it is not needed;
- separate secrets per connector;
- idempotent adapters for systems with side effects.

Anthropic documentation for Claude Code separately highlights permissions, isolated contexts, and manual approval for sensitive network and shell operations.[^anthropic-security]

### 4.7. Telemetry and eval plane

The minimum production set:

- distributed traces for every run;
- spans for model calls, retrieval, and tools;
- cost and latency per step;
- a dataset of reference tasks;
- regression gates before shipping a new prompt, policy, or model combination.[^openai-evals][^openai-trace]

Without this, the team is not controlling the agent. It is merely observing it.

## 5. Where security actually lives

Security in an agent system should not be concentrated in one "guardrail service". It must be distributed across several control points:

| Control point | What it checks |
| --- | --- |
| Pre-ingress filters | Explicitly dangerous input, secrets, forbidden attachments |
| Prompt assembly | Mixing of instructions and data, untrusted content boundaries |
| Model gateway | Model allowlist, budget, moderation, routing |
| Retrieval gateway | Document permissions, tenant isolation, metadata filters |
| Tool gateway | Parameter validation, approval, side-effect class |
| Egress filters | Data leakage, PII, unsafe outbound content |
| Observability backend | Audit trail and incident investigation |

This aligns well with OWASP guidance for prompt injection prevention and with the NIST AI RMF / GenAI Profile, where risk management is embedded throughout the lifecycle rather than attached on top.[^owasp][^nist-rmf][^nist-genai]

## 6. Reference operating model

To avoid turning the platform into a zoo, divide ownership this way:

- the platform team owns gateways, policies, telemetry, and golden templates;
- product teams own the specific agents and business logic;
- the security team defines risk classes, approval rules, and control points;
- the evaluation owner maintains task sets, graders, and regression control.

Google enterprise agent platforms emphasize centralized visibility, governance, and managed access, not only orchestration.[^google-agentspace][^google-agent-builder]

## 7. Practical conclusion

A modern production agent is not "an LLM with tools". It is a system where:

1. orchestration is intentionally simplified;
2. autonomy is constrained by policy;
3. memory is separated from retrieval;
4. tools execute through an isolated gateway;
5. every step is visible through traces and evals;
6. a human can stop or approve risky actions.

Remove any of these, and you get either a fragile demo or an unsafe system.

## 8. Where to read next

- [Book plan](../plan.md)
- [Part I. Foundations](index.md)
- [Publishing stack](../../appendix/stack.md)
- [Sources and bibliography](../../appendix/sources.md)

[^vikulin]: [Dmitry Vikulin, "Architecture of Reliable AI Agents"](https://vikulin.ai/library/tpost/ai_agent_architecture)
[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^anthropic-security]: [Anthropic, Claude Code Security](https://docs.anthropic.com/en/docs/claude-code/security)
[^owasp]: [OWASP, LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
[^nist-rmf]: [NIST, AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
[^nist-genai]: [NIST, AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
[^langgraph-durable]: [LangGraph, Durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
[^langgraph-memory]: [LangGraph, Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
[^langgraph-hitl]: [LangChain Deep Agents, Human-in-the-loop](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop)
[^openai-sdk]: [OpenAI, Agents SDK](https://developers.openai.com/api/docs/guides/agents-sdk)
[^openai-evals]: [OpenAI, Agent evals](https://platform.openai.com/docs/guides/agent-evals)
[^openai-trace]: [OpenAI, Trace grading](https://platform.openai.com/docs/guides/trace-grading)
[^openai-builder]: [OpenAI, Agent Builder](https://platform.openai.com/docs/guides/agent-builder)
[^openai-models]: [OpenAI, Models](https://developers.openai.com/api/docs/models)
[^google-agentspace]: [Google Agentspace](https://cloud.google.com/products/agentspace)
[^google-agent-builder]: [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder)

