# 第 2 章：安全智能体的参考架构

!!! info "怎样读这一章"
    第一遍不用试着记住所有层的名字。

    更有用的是先完成三件事：

    - 顺着一个 support 请求走完整条路径；
    - 看清系统的行动权到底从哪里开始；
    - 记下几个必需层，因为没有它们，请求就不能安全地走到外部 side effect。

## 1. 不要先看层，要先看一个活生生的案例

继续沿用上一章里的支持智能体。

用户写道：

> 我已经等了三天权限开通。请帮我查一下状态，如果申请卡住了，就创建一个加急工单。

如果把这个任务想得过于简单，后面的流程看上去似乎很直白：

- 模型读消息；
- 选择合适的工具；
- 检查状态；
- 创建工单；
- 返回答复。

但 production 系统不能建立在这种“大致如此”的想象上。因为太多关键问题还没有被回答：

- 到底是谁在请求这个动作；
- 这个请求具有什么权限；
- 智能体到底能不能创建工单；
- 创建工单是否需要审批；
- 哪些上下文允许送进模型；
- 如果工具返回的是部分结果或不稳定结果，该怎么办；
- 发生事故以后，怎样把整条链路重新还原出来。

平台架构，正是从这些问题里长出来的。

## 2. 智能体的最小形状，以及为什么它还不够

一开始不用把整张图都装进脑子里。先分清两件事就够了：

- 智能体系统的最小核心；
- 让这个核心不再只是原型的 production 外层。

OpenAI 的实用指南有一个很好的起点：最小的 agent system 通常只有三样东西。[^openai-practical]

- `model`
- `tools`
- `instructions`

这是一个很好的起步框架，因为它能防止你过早过度设计。

但对 production 来说，这还不够。只要系统开始拥有：

- 对内部系统的访问；
- 私有数据；
- 长会话；
- 写路径动作；
- 审批；
- 多个团队和多种访问角色，

这个最小三元组就不再是架构了。它只是核心，而不是平台。

## 3. 一个请求应该怎样穿过系统

现在，把同一个支持案例当作一条架构路径来看。

### 3.1. 入口

消息不应该直接飞进模型。系统首先要把它变成一个标准化请求：

- 用户是谁；
- 请求属于哪个 tenant；
- 来自哪个入口渠道；
- 风险等级是什么；
- 属于哪个 session 和哪个 `trace_id`；
- 会被哪组策略约束。

换句话说，进入系统的不是“文本”，而是一个可管理的 execution context。

### 3.2. 控制层

接下来，系统必须先决定这次运行到底被允许做什么：

- 可以使用哪些模型；
- 可以调用哪些工具；
- 哪些动作必须先经过审批；
- 有哪些额度或限制；
- 当前环境里有哪些禁区。

这就是 control plane。它负责的不是“聪明”，而是系统有没有权利行动。

### 3.3. Runtime

然后请求才进入 runtime，在这里确定执行模式：

- 这里普通 workflow 就够；
- 这里需要 `single-agent loop`；
- 这里必须插入审批中断；
- 这里需要先 checkpoint，之后再继续。

一个好的 runtime 往往很“无聊”。它不是靠魔法取胜，而是靠可预测性取胜。

### 3.4. 模型层

只有这时模型才真正登场：

- 接收整理过的上下文；
- 决定下一步；
- 提议调用工具或者生成文本答复；
- 把结构化结果返回给 runtime。

这里最重要的区分是：模型可以提出动作建议，但它不应该是唯一决定“能不能执行”的地方。

### 3.5. 工具层

如果智能体想检查申请状态，或者创建工单，它不应该直接进入外部世界。那是 tool gateway 的工作：

- 检查 policy decision；
- 在需要时要求 approval；
- 隔离 side effects；
- 把结果返回给 runtime；
- 把事件写入 trace。

### 3.6. 追踪与评估

系统每走一步，都应该留下痕迹：

- 模型做了什么判断；
- 调用了哪个工具；
- 哪个 policy gate 生效了；
- 是否触发审批；
- 延迟在哪一步上升；
- 故障发生在什么位置。

如果没有这些东西，你拥有的不是平台，而是一个复杂黑箱。

## 4. 到了这里，再看整张图才真正有意义

如果你在这里仍然觉得这张图有点密，不用急着记住所有模块名称。先回答三个问题就够了：

- execution context 是从哪里形成的；
- 行动权到底放在哪里；
- 系统在哪里留下了足够支撑排障和发布决策的证据。

现在再回头看平台全图，就更容易理解它为什么存在。

<div class="diagram-card">
<p>安全智能体平台的参考结构图</p>

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

这张图里真正重要的不是层的“好看”，而是它们各自承担的角色：

| 层 | 负责什么 | 缺了会怎样 |
| --- | --- | --- |
| Interface layer | Chat、API、webhooks、events | 否则入口渠道和执行逻辑会混在一起 |
| Identity and session layer | 用户、服务账号、tenant、request scope | 否则 IAM、审计和隔离都会失效 |
| Agent control plane | 策略、审批、限额、目录 | 否则系统会在缺乏控制的情况下行动 |
| Orchestration runtime | Workflow graph、planner、checkpoints | 否则一旦流程变复杂，执行就会散掉 |
| Cognition plane | Model router、prompt assembly、validators | 否则模型会重新变成“世界中心” |
| Memory and knowledge plane | 状态、记忆、retrieval | 否则上下文会无纪律地膨胀 |
| Tool execution plane | Gateway、sandbox、side-effect isolation | 否则 blast radius 太大 |
| Telemetry and eval plane | Traces、metrics、datasets、regression gates | 否则质量无法被测量和调查 |

## 5. Production 平台的五个支柱

Google Cloud 最近的材料还给出了一条很实用的补充框架：不要围绕“一个聪明智能体”思考，而要围绕 production 平台的五个支柱思考。[^google-five-pillars]

- `framework`
- `model`
- `tools`
- `runtime`
- `trust`

这个框架之所以有价值，是因为它很快就能戳破自我安慰。

如果你只有：

- 一个强模型；
- 一个不错的 prompt；
- 几个工具，

但没有 `runtime` 和 `trust`，那你依然没有平台。你只有原型。

## 6. 哪些架构决策必须显式做出来

有些决策，最好在一开始就明确，而不是“先做着看”。

### 6.1. 你的 context layers 到底有哪些

Google 通过 context layers 来约束 prompt assembly，这一点非常实用。[^google-agent-overview][^google-govern]

在实践里，通常至少要分出：

- `static context`：角色、策略、allowed capabilities、固定 instructions；
- `session context`：跨会话持续存在的上下文；
- `turn context`：只属于当前请求的上下文；
- `cached context`：按需注入的上下文。

实用规则很简单：进入 prompt 的不应该是“所有能拿到的数据”，而应该是“用途和生命周期都清楚的数据”。

### 6.2. 行动权到底放在哪里

模型不应该直接拥有执行外部 side effect 的权力。

真正的行动权应该存在于下面这个组合里：

- policy engine；
- approval logic；
- tool gateway。

这就是 control plane 如此重要的原因：它把“模型建议这样做”和“系统被允许这样做”清楚地分开。

### 6.3. 什么时候才值得拆成多个智能体

OpenAI 的 practical guide 有一点很对：不要把 `multi-agent` 当成默认答案。[^openai-practical]

通常只有在这些信号出现时，拆分才是合理的：

- 一个 run 的上下文已经太拥挤；
- 子任务需要不同的工具和不同的 guardrails；
- ownership 已经分到不同团队；
- 并行执行确实能降低 latency 或 cognitive load。

如果这些信号不存在，一个带良好 workflow graph 的单智能体通常更简单，也更可靠。

## 7. 什么东西绝对不要混在一起

至少有四样东西，从一开始就值得分开：

- **short-term state**：当前执行状态；
- **long-term memory**：事实、画像、episodes；
- **retrieval**：对外部知识的访问；[^langgraph-memory]
- **tool execution**：在外部世界里真正发生的动作。

系统还小的时候，这种分离看起来可能像官僚主义。等第一起 serious incident 真的发生，它就会看起来像工程卫生。

## 8. 一个最小代码原则

如果你想用最紧凑的方式看清这个设计，下面这个模板就够了：

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

这里的核心只有一句话：模型可以提议动作，但真正的执行权在 gateway 和 policy layer，不在模型里。

## 9. 这一章真正要带走什么

简短地说，一个好的智能体平台建立在几件很“无聊”、但极其值钱的东西上：

- 显式的入口上下文；
- control plane；
- 独立的 runtime；
- 独立的 tool gateway；
- 独立的 traces 和 evals；
- 只在确实需要的地方加 approvals。

架构之所以重要，不是因为图更好看，而是因为它能阻止系统在第一次真正复杂起来的时候散架。

## 10. 读完这一章立刻该做什么

如果你现在就在设计一个智能体系统，先写下至少这五件事：

1. 你的 execution context 从哪里开始？
2. 行动权放在哪里？
3. 第一版 runtime pattern 是什么？
4. 哪些 side effects 只能通过 gateway？
5. 团队第一天就必须在 trace 里看见哪些字段？

如果这些东西已经写清楚了，架构就开始存在了。如果没有，那你现在还只有一个“智能体想法”。

## 11. 接下来读什么

- [第 1 章：为什么智能体需要的是平台，而不是魔法](chapter-1.zh.md)
- [第二部分：安全边界](../part-ii/index.zh.md)
- [第 3 章：安全边界与信任边界](../part-ii/chapter-3.zh.md)

[^langgraph-memory]: [LangGraph, Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^google-five-pillars]: [Google Cloud, Achieve agentic productivity with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder)
[^google-agent-overview]: [Google Cloud, Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
