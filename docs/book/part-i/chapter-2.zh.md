# 第 2 章：安全智能体的参考架构

## 1. 为什么我们需要一张参考图

读完第一章后，你应该已经有了一个直觉：为什么“只是一个聪明的 agent”会很快变得脆弱。下一步更接地气一些：如果你希望系统不仅能撑过一次演示，而是真正长期工作，它到底应该由哪些层组成？

这就是 reference architecture 的意义。不是作为教条，而是作为 baseline。

## 2. 顶层视角：平台由什么组成

下面这张图可以作为很好的起始地图。

<div class="diagram-card">
<p>安全 agent platform 的参考结构图</p>

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

| 层 | 作用 | 为什么必需 |
| --- | --- | --- |
| Interface layer | Chat、API、event ingestion、webhooks | 把用户入口和 runtime 分开 |
| Identity and session layer | 用户、service account、thread、tenant、request scope | IAM、audit 和隔离都离不开它 |
| Agent control plane | Policies、approvals、model policies、tool catalog、quotas | 可控性就住在这里 |
| Orchestration runtime | Workflow graph、planner、router、subagents、checkpoints | 任务在这里执行 |
| Cognition plane | Model router、prompt compiler、structured outputs、validators | 模型变成一个组件，而不是世界中心 |
| Memory and knowledge plane | Short-term state、long-term memory、retrieval、summaries | 防止上下文无限膨胀 |
| Tool execution plane | Sandboxed tools、MCP servers、connectors、side-effect isolation | 降低 blast radius |
| Telemetry and eval plane | Traces、metrics、logs、datasets、graders、regression gates | 让质量可以被测量 |

## 3. 入口到底应该发生什么

一个进入系统的请求，不应该只是“直接飞进模型”。它首先要变成一个带上下文的标准化事件。

最低有用集合通常包括：

- `tenant_id`；
- `principal`；
- risk class；
- 访问策略引用；
- session 标识；
- trace id。

如果用一句话说：**请求进入系统时，应该已经不是一条消息，而是一个可管理的 execution context。**

## 4. 为什么 control plane 比看上去更重要

这是 demo 架构里最常缺失的一层。

它负责的不是智能，而是系统有没有权利行动：

- 可以用哪些模型；
- 哪些 tools 可用；
- 哪些操作需要 approval；
- 有哪些 limit；
- dev、staging、prod 各自启用哪些规则。

policy-as-code 示例：

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

## 5. 执行发生在哪里

Orchestration runtime 决定执行模式：

- deterministic workflow 用于规程明确的场景；
- routed workflow 用于选择不同分支；
- plan-and-execute 用于长任务；
- planner + subagents 用于可拆分的独立子任务；
- HITL interrupts 用于高风险操作。[^langgraph-hitl][^openai-builder]

一个好 runtime 最好的特性，反而很“无聊”：它应该足够 boring。

里面的“魔法”越多，成本、行为和失败方式就越难预测。

## 6. 为什么 cognition plane 不等于一个模型

更有用的想法不是“我们有一个很强的模型”，而是“我们有一组可管理的组件”：

- planner model；
- executor model；
- classifier/extractor model；
- structured output validator；
- fallback model。

这样想对质量、成本和 graceful degradation 都更有帮助。[^vikulin][^openai-models]

## 7. 为什么 memory、knowledge 和 tools 不能混成一团

至少要把三件东西分开：

- **short-term state**：当前执行流的状态；
- **long-term memory**：事实、profile、episodes；
- **retrieval**：访问外部知识。[^langgraph-memory]

再单独分出第四件：

- **tool execution**：在外部世界里真正发生的动作。

这种分层看上去像官僚主义，但一旦真的出了 serious incident，你会非常庆幸自己这么做了。

## 8. 请求如何穿过系统

下面是一张更“活”的图，展示请求怎么经过关键控制点。

<div class="diagram-card">
<p>请求穿过主要控制点的路径</p>

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

## 9. 一个最小代码原则

如果你想用最简化的方式看清它，这里有一个很实用的模板：

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

这里的核心意思很简单：模型可以提出动作建议，但真正的执行权不在模型里，而在 gateway 和 policy layer 里。

## 10. Practical Takeaway

一个好的 agent platform，通常站在几件很无聊但非常值钱的东西上：

- 显式的入口上下文；
- control plane；
- 独立的 runtime；
- 独立的 tool gateway；
- traces 和 evals；
- 在该有的地方加 approvals。

当这些都搭好之后，你就可以平静地进入下一个更敏感的话题：这样一个系统的 security perimeter 到底在哪里。

## 11. 接下来读什么

- [第 1 章：为什么智能体需要的是平台，而不是魔法](chapter-1.zh.md)
- [第二部分：安全边界](../part-ii/index.zh.md)
- [第 3 章：安全边界与信任边界](../part-ii/chapter-3.zh.md)

[^vikulin]: [Dmitry Vikulin，《可靠 AI Agents 的架构》](https://vikulin.ai/library/tpost/ai_agent_architecture)
[^langgraph-memory]: [LangGraph, Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
[^langgraph-hitl]: [LangChain Deep Agents, Human-in-the-loop](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop)
[^openai-builder]: [OpenAI, Agent Builder](https://platform.openai.com/docs/guides/agent-builder)
[^openai-models]: [OpenAI, Models](https://developers.openai.com/api/docs/models)
