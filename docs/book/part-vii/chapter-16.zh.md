# 第 16 章：基础运行时蓝图

!!! info "怎样读这一章"
    不要把这一章当成抽象的 runtime 讨论，更有用的是抓住一个很实际的问题：

    - 同一个 support agent 的 run loop 到底应该放在哪里；
    - 怎样避免把 policy、memory、execution 和 telemetry 全塞进一个处理器里；
    - 怎样搭出一套不仅能跑 demo，也能撑住后续发布的骨架。

    如果这些问题没有清晰答案，系统通常只能撑到第一次较大的变更或事故发生之前。

## 1. 既然已经有架构，为什么还需要参考 runtime

架构章节的价值在于给你语言和框架。但到了某个阶段，几乎所有人都会问同一个问题：“好，那这东西具体应该长成什么样，才能真的搭出来？”

在贯穿全书的 support 场景里，这已经不是理论问题。智能体已经能查状态、读写记忆、通过 gateway 开工单，还能产出 traces。可一旦没有明确的 runtime 形态，这些步骤就会很快散落到本地处理器、临时 retry 和偶然出现的集成绕路里。

这时候就需要参考 runtime。

它的目标不是成为唯一可能的实现，而是：

- 固定核心模块；
- 展示一次 run 的基本流转；
- 区分必需层和可选增强；
- 给团队一个没有多余魔法的起点。

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

## 8. 从一开始就值得内置进去的东西

有些东西很容易让人想“以后再补”，但实际上最好第一天就放进去：

- 每个 run 都有 `trace_id`；
- tenant/principal context；
- policy decision hooks；
- capability registry，而不是 direct calls；
- structured telemetry；
- 一个基本的 background task hook。

如果 baseline 里没有这些，系统往往会在以后通过一次很痛苦的 retrofit 才补回来。

## 9. 第一版参考实现不必过度复杂化的部分

一开始你并不需要立刻上这些东西：

- 带很多模式的复杂 planner；
- 多阶段 memory compaction pipeline；
- 很复杂的 model routing；
- 完整 self-healing loop；
- 十几个 golden paths。

Reference runtime 的价值不在于功能最大化，而在于形态清晰。一个小而干净的实现，远比一个谁都看不懂的“万能机器”更有用。

## 10. 一个 runtime configuration 示例

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
```

它的价值在于让 runtime contract 保持显式，也更容易在不同环境之间迁移。

## 11. 第一版 runtime 最常见的崩坏点

非常典型的问题有：

- orchestration 和 adapters 黏在一起；
- policy checks 没有在每个必要路径上执行；
- memory 只是一个临时 helper；
- tool calls 绕过 catalog/gateway；
- 缺少 background updates；
- telemetry 是后补的。

也就是说，系统可能“能跑”，但 runtime 的形态已经开始阻碍成长。

## 12. 实用检查清单

如果你想快速检查自己的 baseline runtime，可以问：

- orchestration、policy、memory、execution 和 telemetry 是否已经是独立层？
- 是否存在统一的 run context，并带有 tenant/principal metadata？
- 是否有 capability registry，而不是 direct calls？
- tracing hooks 是否已经接进基础路径？
- 是否有安全的 background updates 接入点？
- 是否不用读十个文件就能解释清一次 run 的流程？

如果连续多个问题的答案都是“没有”，那你现在还没有 reference runtime，你只是把模型早期接进了产品里。

## 13. 接下来读什么

Part VII 的下一个自然步骤，是在这个 blueprint 上加上显式的 policy layer 和 capability catalog，让参考实现进一步接近一个可运行的 operational skeleton。

- [第 15 章：黄金路径、共享网关与反“动物园”模式](../part-vi/chapter-15.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.md)
