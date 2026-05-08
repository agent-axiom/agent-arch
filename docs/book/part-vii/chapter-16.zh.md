# 第 16 章：基础运行时蓝图

!!! info "怎样读这一章"
    不要把这一章当成抽象的运行时讨论，更有用的是抓住一个很实际的问题：

    - 同一个支持智能体的运行回路到底应该放在哪里；
    - 怎样避免把策略、记忆、执行和遥测全塞进一个处理器里；
    - 怎样搭出一套不仅能跑演示，也能撑住后续发布的骨架。

    如果这些问题没有清晰答案，系统通常只能撑到第一次较大的变更或事故发生之前。

## 1. 既然已经有架构，为什么还需要参考运行时

架构章节的价值在于给你语言和框架。但到了某个阶段，几乎所有人都会问同一个问题：“好，那这东西具体应该长成什么样，才能真的搭出来？”

这正是本章的独特承诺。它应该帮助读者跨过一条重要边界：从认同本书的论证，走到看见这套论证如何落成可运行结构。

在贯穿全书的支持场景里，这已经不是理论问题。智能体已经能查状态、读写记忆、通过网关开工单，还能产出追踪。可一旦没有明确的运行时形态，这些步骤就会很快散落到本地处理器、临时重试和偶然出现的集成绕路里。

这时候就需要参考运行时。

它的目标不是成为唯一可能的实现，而是：

- 固定核心模块；
- 展示一次运行的基本流转；
- 区分必需层和可选增强；
- 给团队一个没有多余魔法的起点。

因此，本章最好不要只被读成一章关于模块边界的说明，它也应该被读成一章关于在变更压力下仍能成立的可运行结构。真正的问题是，这个运行时现在是否已经有了一种形状，能够承受新策略、新工具、更长生命周期的运行、中断和 rollout 压力，而不会重新塌回一堆处理器和例外。

## 2. 最小成熟运行时早就不只是一个模型调用

一开始就应该放弃“智能体 = 一次模型调用 + 工具”这种画面。

一个最小成熟运行时通常已经包括：

- 入口层；
- 运行协调器；
- 策略钩子；
- 记忆访问层；
- 工具/能力执行层；
- 遥测发射器；
- 结果组装。

也就是说，运行时不是“调用 LLM 的地方”，而是围绕模型组织出来的一条编排回路。

## 3. 一次运行的基础流程长什么样

在参考实现里，你可以把一次 run 大致理解成这样：

1. 接收请求并构建运行上下文；
2. 执行策略预检查；
3. 从记忆/检索里取出相关上下文；
4. 调用模型；
5. 如果需要工具调用，就通过执行层执行；
6. 写入遥测；
7. 组装最终结果；
8. 安排后台更新。

这已经和“带函数调用的聊天”差得很远了，而且本来就应该如此。

<div class="diagram-card">
<p>即使是基础运行时，也已经有若干必须存在的控制点</p>

``` mermaid
flowchart LR
    A["入口"] --> B["运行上下文"]
    B --> C["策略预检查"]
    C --> D["记忆 / 检索"]
    D --> E["模型步骤"]
    E --> F{"需要工具？"}
    F -->|No| G["结果组装"]
    F -->|Yes| H["执行层"]
    H --> I["工具结果"]
    I --> E
    G --> J["遥测 + 后台任务"]
```

</div>

## 4. 第一版就值得拆开的模块

有几条边界非常值得一开始就在代码里明确出来：

- `runtime.py` 或 `orchestrator.py` 放运行回路；
- `policy.py` 放策略决策；
- `memory.py` 放检索和记忆写入；
- `catalog.py` 放能力注册表；
- `execution.py` 放工具分派；
- `telemetry.py` 放 span 和结构化事件。

如果这些都塞进一个大处理器里，前几个演示也许会很快，但系统几乎立刻就会变得难以演化。

!!! example "贯穿案例：防重复保护应该放在哪里"
    在支持分诊运行时里，防止重复工单的逻辑不应该藏在 helpdesk 适配器里。`runtime.py` 应该负责运行上下文和重试分支，`execution.py` 应该通过幂等契约执行写工具，`telemetry.py` 应该记录 `side_effect_unknown`，而 `policy.py` 加发布门应该决定运行是否可以继续。这样，同一个事故就不会散落到一堆处理器里。

## 5. 不要把编排和业务适配器混在一起

早期实现里最贵的错误之一，就是运行时直接知道太多具体外部系统的细节。

这样一来编排代码很快就会塞进：

- 针对具体工具的分支逻辑；
- 外部载荷形状的知识；
- 针对某个 API 的本地重试；
- 临时脱敏；
- 针对某个集成的特殊绕路逻辑。

参考运行时应该传达相反的思想：编排通过契约工作，而适配器活在系统边缘。

## 6. 一个最小项目结构示例

下面是一个非常接地气的起步结构：

```text
agent_runtime/
  orchestrator.py
  policy.py
  memory.py
  catalog.py
  execution.py
  telemetry.py
  models.py
  background.py
```

这不是唯一正确的布局，但它已经足够帮助你避免把一切都塞进一个文件里，也避免把控制层混在一起。

## 7. 一个简单的编排器骨架

下面不是生产运行时，而是蓝图骨架。它展示的是 run steps 如何拆开，以及关键控制点应该放在哪里。

```python
from dataclasses import dataclass


@dataclass
class RunRequest:
    user_input: str
    tenant_id: str
    principal_id: str


@dataclass
class RunResult:
    output_text: str
    status: str


def run_agent(request: RunRequest) -> RunResult:
    policy_check(request)
    context = retrieve_context(request)
    model_output = call_model(request, context)

    if model_output.get("tool_request"):
        tool_result = execute_tool(model_output["tool_request"])
        emit_event("tool_execution", tool_result)
        model_output = call_model(request, context + [tool_result])

    schedule_background_updates(request, model_output)
    return RunResult(output_text=model_output["text"], status="success")
```

核心想法很简单：哪怕是基线运行时，也应该把策略、检索、工具执行和后台更新明确表现成独立阶段。

## 8. 长时间运行的任务不是可选外挂，而是基线的一部分

一个常见的运行时错误，是默认认为所有有用的运行都应该在一次同步请求里完成。只有在系统还停留在演示形态时，这种假设才成立。

在真实的支持场景里，有些 run 天然就是长生命周期的：

- 等待审批；
- 等待延迟不稳定的工具；
- 在工具执行之后等待第二次模型 pass；
- 等待延迟后续动作或后台更新。

OpenAI 最近关于后台模式的材料很有帮助，因为它把后台执行当成运行时的一等关注点，而不是超时问题的补丁。[^openai-background]

这也应该成为基线运行时的思维方式。运行时从一开始就应该区分：

- `synchronous runs`，可以在一次 foreground pass 中安全完成；
- `background runs`，会在首次响应之后继续执行；
- `resumable runs`，会因为 approval、外部输入或延迟工作而暂停后再继续。

Anthropic 的工作流分类又把这个问题压得更具体了，因为不同编排模式会带来不同的检查点需求。[^anthropic] `prompt chaining` 往往需要在固定阶段之间 checkpoint，`routing` 往往只需要在分类和交接边界 checkpoint，`parallelization` 需要汇合状态可见性，而 `orchestrator-workers` 需要能跨部分完成而存活的父/worker 协调状态。

LangGraph persistence 在 checkpoint granularity 层面说明了同一个原则：durable state 按 thread 组织，checkpoints 在 super-step 边界保存，而失败 super-step 中已经成功完成的 node writes 可以作为 pending writes 保留下来，这样 resume 时不需要重新执行已经成功的节点。[^langgraph-persistence] 架构结论是：“checkpointing” 不是一个 boolean。Runtime 应该明确命名用于 resume 的 cursor、允许 replay 的边界，以及故障之后不能重复提交的 partial writes。

他们后续关于 harness 设计的工作又补上了一个更实际的运行时经验：在长时间运行的应用工作里，往往必须明确区分 **compaction** 和 **上下文重置**。[^anthropic-harness] Compaction 会让同一个智能体在缩短后的历史上继续工作，因此连续性还在，但上下文焦虑和累计漂移也可能继续存在。Reset 则是启动一个全新的智能体，并依赖结构化的交接工件来携带状态、下一步动作和评估上下文。这不只是提示技巧，而是运行时架构的一部分，因为一旦 resets 成为 harness 的组成部分，平台就必须决定哪些状态足够耐久、能跨 reset 保留下来，以及下一个智能体会继承什么审查工件。

所以有界自主不只是策略问题，也是一种运行时状态设计问题：每一种被允许的执行模式，都会带来自己的一套 pause、resume、reset 和完成语义。

如果运行时对这些情况没有显式形态，长时间工作最终通常都会泄漏成临时重试、重复请求和隐藏状态迁移。

### 8.1. 沙箱会话状态也是运行时状态

OpenAI Agents SDK 的 Sandbox Agents 做了一个很有用的区分，应该进入基线运行时设计：`Manifest` 描述 fresh workspace contract，而一次具体运行可以拿到 live sandbox session、序列化的 `session_state`，也可以从 `snapshot` 启动。[^openai-sandbox-agents]

对参考运行时来说，这意味着沙箱状态不应该消失在 tool adapter 里面。一个最小有用模型，至少应该在 `run_id` 和 `trace_id` 旁边追踪：

- `sandbox_session_id`；
- `sandbox_manifest_version`；
- `sandbox_permissions_profile`；
- 当运行从保存的 workspace 启动时的 `snapshot_id`；
- 已物化的 workspace entries，或指向已审查 manifest 的链接；
- 这个沙箱是否可以 resume、snapshot，还是必须重新创建。

这样，围绕文件、shell 和 memory 的长时间工作就不会变成磁盘上一团不透明目录。它会成为同一个 runtime-control 层的一部分，和 approvals、background runs、capability sessions、trace evidence 放在一起管理。

### 8.2. Stateful named agent instance 作为一种运行时拓扑

Cloudflare Agents SDK 展示了另一个有用的基线模式：智能体不一定只是 transient execution loop，也可以是一个**有名字的耐久运行时对象**。在这个模型里，每个 agent instance 都运行在 Durable Object 之上，拥有自己的 durable SQL/key-value state、WebSocket 连接、scheduled tasks，能在事件到来时醒来，也能在空闲时 hibernate。[^cloudflare-agents]

把它放进本书时，重点不是“应该使用 Cloudflare”，而是保留这种架构形态。当智能体绑定到某个真实事物的稳定名字上——customer case、project、device、tenant workspace、room、thread 或 research dossier——运行时就应该明确区分：

- `agent_instance_id`，它比单次 run 活得更久；
- `run_id`，它描述一次具体执行；
- `session_id`，它描述用户可见会话或 transport session；
- durable agent state，它可以跨 disconnect、deploy、hibernation 和 background wake-up 保留下来；
- external knowledge store，它不是某一个 instance 的私有可变状态。

这个模式特别适合 chat、voice、workflow 和 monitoring agents，因为用户期待的是连续性，而不是 stateless request/response。但它也引入了基线运行时必须显式暴露的风险：named instances 的 tenant isolation、跨 WebSocket sessions 的泄漏、hibernation 之后的 replay/resume、没有活跃用户时的 scheduled side effects，以及 agent version 变化时的 durable-state migrations。

因此，参考运行时不必实现 Durable Objects，但需要类似 `AgentInstanceStore` 和 `SchedulerBoundary` 的抽象：一个能看清哪个 named instance 拥有哪些状态、哪些 runs 修改过它、哪些 scheduled tasks 可能唤醒它、哪些 traces 能证明安全恢复的位置。

Scheduling 这一侧尤其重要：Cloudflare 展示了 delayed、scheduled、cron 和 interval tasks，这些任务会跨 restart 保留，persist 到 SQLite，并通过 Durable Object alarms 唤醒 agent。[^cloudflare-schedule] 对本书的架构结论是：schedule 不应该只是不可见的 callback，而应该表示成 durable control record，带有 owner instance、payload schema、idempotency key、overlap policy、next fire time 和 trace linkage。

Real-time 这一侧又增加了一条边界：connection state 不等于 agent state。在 Cloudflare Agents WebSocket model 中，一个 connection 有自己的 `id`、`uri`、per-connection `state`、tags、lifecycle hooks，并且可以针对某个 connection 关闭 identity/state/MCP 等 protocol messages。[^cloudflare-websockets] 对 baseline runtime 来说，这意味着 broadcast、presence、approval UI 和 streaming updates 都应该经过 connection-scoped authorization 和可追踪的 fan-out，而不是直接暴露 agent 的整个 durable state。

## 9. 有状态工具会话也应该属于基线

一旦执行层开始接入类似有状态 MCP 能力，基线运行时就会多出一条必须明确的边界：**用户可见运行的状态，不等于能力会话的状态**。[^aws-stateful-mcp]

这很重要，因为一个用户看到的运行现在可能同时包含：

- 一个 runtime `run_id`；
- 一个或多个面向外部能力的 MCP `session_id`；
- 在最终答案出现前先发出的进度通知；
- 由于 elicitation 或中间提示而暂停、等待更多输入的运行；
- 能力会话在运行完成前过期时触发的重新初始化。

如果这些状态都被压进一个不透明对象里，操作员就很难解释：到底什么被恢复了，什么已过期，什么必须重新重试。

### 9.1. 运行时应该把能力会话生命周期当作一等状态

一个最小成熟运行时通常至少应该能追踪：

- `run_id`
- `trace_id`
- `capability_session_id`
- `capability_session_status`
- `expires_at`
- `resume_token` 或其他 continuation handle
- 当有状态工具流因审批暂停时的 `approval_state`

这并不意味着每个工具都要有沉重的会话模型。它只是意味着：当协议需要时，运行时必须有地方表达这类状态。

### 9.2. 进度和 elicitation 应该进入同一套恢复控制模型

stateful MCP guidance 的另一个重要含义是：进度事件和 elicitation 请求不应被当成奇怪的旁路信号。它们应该和审批、后台恢复一起进入同一套运行时控制模型。

当运行时开始支持多种编排模式时，这一点会更重要。来自 `parallelization` 分支的 progress、由 `orchestrator-workers` 委派出去的 worker 进度，或者来自 gated `prompt chaining` 阶段的 progress，都不应该被困在模式专用适配器里。它们应该进入同一个共享控制面，用来支撑状态、恢复、过期和操作员可见性。

在实践里，基线运行时很适合为这些状态使用统一规则：

- 能力会话内仍然存活的 `in_progress` 工作；
- `waiting_for_input` 或 `waiting_for_approval` 这样的暂停；
- 可以在同一个能力会话中继续的 `resumable` 工作；
- 能力会话已过期、继续前必须重建的 `reinitialize_required` 工作。

如果没有这些区分，会话过期往往会被误看成随机故障，而不是正常生命周期事件。

## 10. 从一开始就值得内置进去的东西

有些东西很容易让人想“以后再补”，但实际上最好第一天就放进去：

- 每个运行都有 `trace_id`；
- 租户/principal 上下文；
- 策略决策钩子；
- 能力注册表，而不是直接调用；
- 结构化遥测；
- 一个基本的后台任务钩子；
- 一套显式的运行状态模型，比如 `queued/in_progress/completed/failed/canceled`；
- 一种对长时间工作做 poll/resume/cancel 的方式，而不是偷偷长出第二套隐藏运行时。

如果基线里没有这些，系统往往会在以后通过一次很痛苦的改造才补回来。

## 11. 一个用于后台与可恢复工作的最小骨架

即使是基线运行时，也应该有一种简单方式来表达那些活得比第一次请求更久的工作。

```python
from dataclasses import dataclass


@dataclass
class RunHandle:
    run_id: str
    status: str


def start_run(request: RunRequest) -> RunHandle:
    run_id = create_run_record(request)
    enqueue_run(run_id)
    return RunHandle(run_id=run_id, status="queued")


def continue_run(run_id: str):
    run = load_run(run_id)
    if run.status in {"canceled", "completed", "failed"}:
        return run

    update_status(run_id, "in_progress")
    result = execute_run_steps(run)
    update_status(run_id, result.status)
    return result
```

重点不在复杂，而在显式。长生命周期工作必须清楚到操作员能观察、客户端能轮询、运行时能恢复或取消，而不是靠猜。

## 12. 第一版参考实现不必过度复杂化的部分

一开始你并不需要立刻上这些东西：

- 带很多模式的复杂规划器；
- 多阶段记忆压缩流水线；
- 很复杂的模型路由；
- 完整自愈回路；
- 十几个黄金路径。

参考运行时的价值不在于功能最大化，而在于形态清晰。一个小而干净的实现，远比一个谁都看不懂的“万能机器”更有用。

## 13. 一个运行时配置示例

下面是一个通过配置定义运行时形态、而不是把所有决定都写死在代码里的例子：

```yaml
runtime:
  max_tool_hops: 3
  require_trace_id: true
  enable_background_updates: true
  default_model: gpt-5.4
  policy:
    precheck_required: true
  telemetry:
    emit_structured_events: true
  execution:
    gateway_required: true
  background:
    enabled: true
    resumable_runs: true
    allow_cancel: true
  capability_sessions:
    track_session_ids: true
    emit_progress_events: true
    support_reinit_on_expiry: true
```

它的价值在于让运行时契约保持显式，也更容易在不同环境之间迁移。

## 14. 常见错误

非常典型的问题有：

- 编排和适配器黏在一起；
- 策略检查没有在每个必要路径上执行；
- 记忆只是一个临时助手；
- 工具调用绕过目录/网关；
- 缺少后台更新；
- 遥测是后补的；
- 长时间工作被藏在重试后面，而不是被显式建模；
- 后台执行明明存在，但操作员却无法干净地 poll、resume 或 cancel。

也就是说，系统可能“能跑”，但运行时的形态已经开始阻碍成长。

## 15. 给基线运行时做一次快速成熟度测试

团队不应该只因为已经有一个可工作的智能体、几个模块和一些成功演示，就觉得自己已经有了参考运行时。

更高的标准应该是：

- orchestration、策略、记忆、执行和遥测是清晰分开的层；
- 运行上下文从一开始就携带身份与控制元数据；
- 能力执行通过契约走，而不是 direct adapter calls；
- 追踪和后台钩子在基础路径里就存在，而不是靠后期改造；
- 长时间工作拥有显式的状态与延续模型，而不是藏在隐式 retries 里；
- 一次运行可以被解释成稳定的 skeleton，而不是散落的本地逻辑。

如果这些条件大多不成立，那团队也许已经有一个实现，但还没有真正的基线运行时蓝图。

## 16. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- orchestration、策略、记忆、执行和遥测是否已经是独立层？
- 是否存在统一的 run context，并带有租户/principal 元数据？
- 是否有能力注册表，而不是直接调用？
- 追踪钩子是否已经接进基础路径？
- 是否有安全的后台更新接入点？
- 长时间工作能否被显式排队、观察、恢复和取消？
- 是否不用读十个文件就能解释清一次 run 的流程？

如果连续多个问题的答案都是“没有”，那你现在还没有参考运行时，你只是把模型早期接进了产品里。

## 17. 下一步做什么

先把运行时形态固定下来，再在这个骨架上加策略层和能力契约。

第七部分的下一个自然步骤，是在这个蓝图上加上显式的 policy layer 和能力目录，让参考实现进一步接近一个可运行的运行骨架。

- [第 15 章：黄金路径、共享网关与反动物园模式](../part-vi/chapter-15.zh.md)
- [第 17 章：策略层与能力目录](chapter-17.zh.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^anthropic]: Anthropic, [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents).

[^aws-stateful-mcp]: [AWS, Introducing stateful MCP client capabilities on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-stateful-mcp-client-capabilities-on-amazon-bedrock-agentcore-runtime/)

[^openai-background]: [OpenAI, Background mode](https://developers.openai.com/api/docs/guides/background)

[^langgraph-persistence]: [LangGraph, Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).

[^cloudflare-websockets]: [Cloudflare Agents SDK, WebSockets](https://developers.cloudflare.com/agents/api-reference/websockets/)

[^cloudflare-schedule]: [Cloudflare Agents SDK, Schedule tasks](https://developers.cloudflare.com/agents/api-reference/schedule-tasks/)

[^cloudflare-agents]: [Cloudflare, Build Agents on Cloudflare](https://developers.cloudflare.com/agents/)

[^openai-sandbox-agents]: OpenAI Agents SDK, [Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/)、[Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/)、[Sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/) 与 [Agent memory](https://openai.github.io/openai-agents-python/sandbox/memory/)
