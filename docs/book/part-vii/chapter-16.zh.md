# 第 16 章：基础运行时蓝图

!!! info "怎样读这一章"
    不要把这一章当成抽象的 runtime 讨论，更有用的是抓住一个很实际的问题：

    - 同一个 support agent 的 run loop 到底应该放在哪里；
    - 怎样避免把 policy、memory、execution 和 telemetry 全塞进一个处理器里；
    - 怎样搭出一套不仅能跑 demo，也能撑住后续发布的骨架。

    如果这些问题没有清晰答案，系统通常只能撑到第一次较大的变更或事故发生之前。

## 1. 既然已经有架构，为什么还需要参考 runtime

架构章节的价值在于给你语言和框架。但到了某个阶段，几乎所有人都会问同一个问题：“好，那这东西具体应该长成什么样，才能真的搭出来？”

这正是本章的 distinct promise。它应该帮助读者跨过一条重要边界：从认同本书的论证，走到看见这套论证如何落成 runnable structure。

在贯穿全书的 support 场景里，这已经不是理论问题。智能体已经能查状态、读写记忆、通过 gateway 开工单，还能产出 traces。可一旦没有明确的 runtime 形态，这些步骤就会很快散落到本地处理器、临时 retry 和偶然出现的集成绕路里。

这时候就需要参考 runtime。

它的目标不是成为唯一可能的实现，而是：

- 固定核心模块；
- 展示一次 run 的基本流转；
- 区分必需层和可选增强；
- 给团队一个没有多余魔法的起点。

因此，本章最好不要只被读成一章关于模块边界的说明，它也应该被读成一章关于在变更压力下仍能成立的 runnable structure。真正的问题是，这个 runtime 现在是否已经有了一种形状，能够承受新 policy、新 tools、更长生命周期的 runs、interrupts 和 rollout pressure，而不会重新塌回一堆 handlers 和 exceptions。

## 2. 最小成熟 runtime 早就不只是一个模型调用

一开始就应该放弃“agent = 一次模型调用 + tools”这种画面。

一个最小成熟的 runtime 通常已经包括：

- ingress 层；
- run coordinator；
- policy hooks；
- memory access layer；
- tool/capability execution layer；
- telemetry emitter；
- result assembly。

也就是说，runtime 不是“调用 LLM 的地方”，而是围绕模型组织出来的一条 orchestration loop。

## 3. 一次 run 的基础流程长什么样

在参考实现里，你可以把一次 run 大致理解成这样：

1. 接收 request 并构建 run context；
2. 执行 policy pre-checks；
3. 从 memory/retrieval 里取出相关上下文；
4. 调用模型；
5. 如果需要 tool call，就通过 execution layer 执行；
6. 写 telemetry；
7. 组装最终结果；
8. 安排 background updates。

这已经和“带函数调用的聊天”差得很远了，而且本来就应该如此。

<div class="diagram-card">
<p>即使是基础 runtime，也已经有若干必须存在的 control points</p>

``` mermaid
flowchart LR
    A["Ingress"] --> B["Run context"]
    B --> C["Policy pre-check"]
    C --> D["Memory / retrieval"]
    D --> E["Model step"]
    E --> F{"Tool needed?"}
    F -->|No| G["Result assembly"]
    F -->|Yes| H["Execution layer"]
    H --> I["Tool result"]
    I --> E
    G --> J["Telemetry + background tasks"]
```

</div>

## 4. 第一版就值得拆开的模块

有几条边界非常值得一开始就在代码里明确出来：

- `runtime.py` 或 `orchestrator.py` 放 run loop；
- `policy.py` 放 policy decisions；
- `memory.py` 放 retrieval 和 memory writes；
- `catalog.py` 放 capability registry；
- `execution.py` 放 tool dispatch；
- `telemetry.py` 放 spans 和 structured events。

如果这些都塞进一个大 handler 里，前几个 demo 也许会很快，但系统几乎立刻就会变得难以演化。

## 5. 不要把 orchestration 和业务 adapter 混在一起

早期实现里最贵的错误之一，就是 runtime 直接知道太多具体外部系统的细节。

这样一来 orchestration code 很快就会塞进：

- 针对具体 tools 的分支逻辑；
- 外部 payload shape 的知识；
- 针对某个 API 的本地 retry；
- 临时 redaction；
- 针对某个集成的特殊绕路逻辑。

参考 runtime 应该传达相反的思想：orchestration 通过 contracts 工作，而 adapters 活在系统边缘。

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

## 7. 一个简单的 orchestrator skeleton

下面不是 production runtime，而是 blueprint skeleton。它展示的是 run steps 如何拆开，以及关键 control points 应该放在哪里。

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

核心想法很简单：哪怕是 baseline runtime，也应该把 policy、retrieval、tool execution 和 background updates 明确表现成独立阶段。

## 8. 长时间运行的 run 不是 optional add-on，而是 baseline 的一部分

一个常见的 runtime 错误，是默认认为所有有用的 run 都应该在一次同步请求里完成。只有在系统还停留在 demo 形态时，这种假设才成立。

在真实的 support 场景里，有些 run 天然就是长生命周期的：

- 等待 approval；
- 等待 latency 不稳定的工具；
- 在 tool execution 之后等待第二次 model pass；
- 等待 deferred follow-up 或 background update。

OpenAI 最近关于 background mode 的材料很有帮助，因为它把 background execution 当成 runtime 的 first-class concern，而不是超时问题的补丁。[^openai-background]

这也应该成为 baseline runtime 的思维方式。runtime 从一开始就应该区分：

- `synchronous runs`，可以在一次 foreground pass 中安全完成；
- `background runs`，会在首次响应之后继续执行；
- `resumable runs`，会因为 approval、外部输入或延迟工作而暂停后再继续。

Anthropic 的 workflow taxonomy 又把这个问题压得更具体了，因为不同 orchestration patterns 会带来不同的 checkpoint needs。[^anthropic] `prompt chaining` 往往需要在固定阶段之间 checkpoint，`routing` 往往只需要在分类和 handoff 边界 checkpoint，`parallelization` 需要 join-state 可见性，而 `orchestrator-workers` 需要能跨部分完成而存活的 parent/worker coordination state。

他们后续关于 harness design 的工作又补上了一个更实际的 runtime 经验：在长时间运行的 application work 里，往往必须明确区分 **compaction** 和 **context reset**。[^anthropic-harness] Compaction 会让同一个 agent 在缩短后的历史上继续工作，因此 continuity 还在，但 context anxiety 和累计 drift 也可能继续存在。Reset 则是启动一个全新的 agent，并依赖结构化的 handoff artifact 来携带状态、下一步动作和 evaluation context。这不只是 prompt 技巧，而是 runtime architecture 的一部分，因为一旦 resets 成为 harness 的组成部分，平台就必须决定哪些状态足够耐久、能跨 reset 保留下来，以及下一个 agent 会继承什么 review artifact。

所以 bounded autonomy 不只是 policy 问题，也是一种 runtime-state 设计问题：每一种被允许的 execution pattern，都会带来自己的一套 pause、resume、reset 和 completion semantics。

如果 runtime 对这些情况没有显式形态，长时间工作最终通常都会泄漏成 ad hoc retries、重复请求和隐藏状态迁移。

## 9. Stateful tool sessions 也应该属于 baseline

一旦 execution layer 开始接入类似 stateful MCP 的 capability，baseline runtime 就会多出一条必须明确的边界：**user-visible run 的状态，不等于 capability session 的状态**。[^aws-stateful-mcp]

这很重要，因为一个用户看到的 run 现在可能同时包含：

- 一个 runtime `run_id`；
- 一个或多个面向外部 capability 的 MCP `session_id`；
- 在最终答案出现前先发出的 progress notifications；
- 由于 elicitation 或中间提示而暂停、等待更多输入的 run；
- capability session 在 run 完成前过期时触发的 re-initialization。

如果这些状态都被压进一个不透明对象里，operator 就很难解释：到底什么被 resumed 了，什么 expired 了，什么必须重新 retry。

### 9.1. Runtime 应该把 capability session lifecycle 当作 first-class state

一个最小成熟 runtime 通常至少应该能追踪：

- `run_id`
- `trace_id`
- `capability_session_id`
- `capability_session_status`
- `expires_at`
- `resume_token` 或其他 continuation handle
- 当 stateful tool flow 因审批暂停时的 `approval_state`

这并不意味着每个 tool 都要有沉重的 session model。它只是意味着：当 protocol 需要时，runtime 必须有地方表达这类状态。

### 9.2. Progress 和 elicitation 应该进入同一套 resume-control model

stateful MCP guidance 的另一个重要含义是：progress events 和 elicitation requests 不应被当成奇怪的旁路信号。它们应该和 approvals、background resumption 一起进入同一套 runtime control model。

当 runtime 开始支持多种 orchestration patterns 时，这一点会更重要。来自 `parallelization` 分支的 progress、由 `orchestrator-workers` 委派出去的 worker progress，或者来自 gated `prompt chaining` 阶段的 progress，都不应该被困在 pattern-specific adapters 里。它们应该进入同一个共享 control surface，用来支撑 status、resumption、expiry 和 operator visibility。

在实践里，baseline runtime 很适合为这些状态使用统一规则：

- capability session 内仍然存活的 `in_progress` 工作；
- `waiting_for_input` 或 `waiting_for_approval` 这样的暂停；
- 可以在同一个 capability session 中继续的 `resumable` 工作；
- capability session 已过期、继续前必须重建的 `reinitialize_required` 工作。

如果没有这些区分，session expiry 往往会被误看成随机故障，而不是正常 lifecycle event。

## 10. 从一开始就值得内置进去的东西

有些东西很容易让人想“以后再补”，但实际上最好第一天就放进去：

- 每个 run 都有 `trace_id`；
- tenant/principal context；
- policy decision hooks；
- capability registry，而不是 direct calls；
- structured telemetry；
- 一个基本的 background task hook；
- 一套显式的 run status model，比如 `queued / in_progress / completed / failed / canceled`；
- 一种对长时间工作做 poll / resume / cancel 的方式，而不是偷偷长出第二套隐藏 runtime。

如果 baseline 里没有这些，系统往往会在以后通过一次很痛苦的 retrofit 才补回来。

## 11. 一个用于 background 与 resumable work 的最小 skeleton

即使是 baseline runtime，也应该有一种简单方式来表达那些活得比第一次请求更久的工作。

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

重点不在复杂，而在显式。长生命周期工作必须清楚到 operator 能观察、client 能轮询、runtime 能恢复或取消，而不是靠猜。

## 12. 第一版参考实现不必过度复杂化的部分

一开始你并不需要立刻上这些东西：

- 带很多模式的复杂 planner；
- 多阶段 memory compaction pipeline；
- 很复杂的 model routing；
- 完整 self-healing loop；
- 十几个 golden paths。

Reference runtime 的价值不在于功能最大化，而在于形态清晰。一个小而干净的实现，远比一个谁都看不懂的“万能机器”更有用。

## 13. 一个 runtime configuration 示例

下面是一个通过配置定义 runtime 形态、而不是把所有决定都写死在代码里的例子：

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

它的价值在于让 runtime contract 保持显式，也更容易在不同环境之间迁移。

## 14. 常见错误

非常典型的问题有：

- orchestration 和 adapters 黏在一起；
- policy checks 没有在每个必要路径上执行；
- memory 只是一个临时 helper；
- tool calls 绕过 catalog/gateway；
- 缺少 background updates；
- telemetry 是后补的；
- 长时间工作被藏在 retries 后面，而不是被显式建模；
- background execution 明明存在，但 operator 却无法干净地 poll、resume 或 cancel。

也就是说，系统可能“能跑”，但 runtime 的形态已经开始阻碍成长。

## 15. 给 baseline runtime 做一次快速成熟度测试

团队不应该只因为已经有一个 working agent、几个模块和一些成功 demo，就觉得自己已经有了 reference runtime。

更高的标准应该是：

- orchestration、policy、memory、execution 和 telemetry 是清晰分开的层；
- run context 从一开始就携带 identity 与 control metadata；
- capability execution 通过 contracts 走，而不是 direct adapter calls；
- tracing 和 background hooks 在 base path 里就存在，而不是靠后期 retrofit；
- 长时间工作拥有显式的状态与 continuation model，而不是藏在隐式 retries 里；
- 一次 run 可以被解释成稳定的 skeleton，而不是散落的 local logic。

如果这些条件大多不成立，那团队也许已经有一个 implementation，但还没有真正的 baseline runtime blueprint。

## 16. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- orchestration、policy、memory、execution 和 telemetry 是否已经是独立层？
- 是否存在统一的 run context，并带有 tenant/principal metadata？
- 是否有 capability registry，而不是 direct calls？
- tracing hooks 是否已经接进基础路径？
- 是否有安全的 background updates 接入点？
- 长时间工作能否被显式排队、观察、恢复和取消？
- 是否不用读十个文件就能解释清一次 run 的流程？

如果连续多个问题的答案都是“没有”，那你现在还没有 reference runtime，你只是把模型早期接进了产品里。

## 17. 下一步做什么

先把 runtime shape 固定下来，再在这个骨架上加 policy layer 和 capability contracts。

Part VII 的下一个自然步骤，是在这个 blueprint 上加上显式的 policy layer 和 capability catalog，让参考实现进一步接近一个可运行的 operational skeleton。

- [第 15 章：黄金路径、共享网关与反动物园模式](../part-vi/chapter-15.zh.md)
- [第 17 章：策略层与能力目录](chapter-17.zh.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^openai-background]: [OpenAI, Background mode](https://developers.openai.com/api/docs/guides/background)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
