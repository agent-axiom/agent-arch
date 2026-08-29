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

**运行时案例主线说明（Runtime case-spine note）：**基线运行时（baseline runtime）应该支持三个规范案例（canonical cases），并留下追踪证据（trace evidence），而不依赖本地绕路。支持分诊（Support triage）需要带审批钩子（approval hooks）、幂等契约（idempotency contract）和重复工单遥测（duplicate-ticket telemetry）的写入能力路径（write-capability path）。内部知识助手（Internal knowledge assistant）需要带来源锚定（source grounding）、租户过滤器（tenant filters）、新鲜度检查（freshness checks）和受保护记忆写入（guarded memory writes）的检索路径。事故协调（Incident coordination）需要带响应者角色检查（responder-role checks）、通知分发（notification dispatch）、事故状态更新（incident-state updates）和事件后后台任务（post-incident background tasks）的升级路径。

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

OpenAI 2026 年 6 月关于 Codex 的研究，给这件事补上了市场证据，而不只是架构证据：agentic AI 正在把知识工作的单位从单次 interaction 变成 delegated long-horizon tasks；到 2026 年 5 月，80.6% 的 sampled individual Codex users 至少发起过一个被估计为超过 30 分钟人类工作的请求，70.2% 发起过超过 1 小时的请求，25.6% 发起过超过 8 小时的请求。[^openai-agents-transforming-work] 这些阈值是 model-estimated，所以应该当作 directional signal，而不是精确工时账本。但对 runtime 来说，它指向的是另一种控制面：不能只看单次请求 latency，还要看 task horizon estimate、agent runtime、parallel workstreams、checkpoint age 和 attention budget。OpenAI 关于 Codex-maxxing 的实践材料把同一个 operating pattern 说得更直接：把 ambitious goal 拆成可验证步骤，在多个 workstreams 之间保持上下文，并明确决定哪些 execution 可以委派给 Codex，哪些地方最需要 human oversight。[^openai-codex-maxxing]

这也应该成为基线运行时的思维方式。运行时从一开始就应该区分：

- `synchronous runs`，可以在一次 foreground pass 中安全完成；
- `background runs`，会在首次响应之后继续执行；
- `resumable runs`，会因为 approval、外部输入或延迟工作而暂停后再继续。

### 8.1. Harness vs runtime

LangChain 提供了一条有用边界：harness 给 agent prompts、tools、skills 和 reasoning loop，而 production runtime 负责让长时间工作跨 crash、deploy、human wait 和运营约束继续存活。[^langchain-production-runtime] 因此本书不应该把“好的 agent harness”和系统架构混在一起。Harness 可以提高行动质量，但 runtime 必须拥有 durable execution、checkpoint boundaries、带 provenance 管理的 memory、tenant isolation、human-in-the-loop waits、observability、sandbox boundaries，以及 MCP/A2A 这类开放 integration protocols。

Cloudflare/Flue 的材料把这条边界讲得更清楚：production agent stack 至少有三层，而不是两层。[^cloudflare-flue-platform] **Framework** 层提供 project structure、conventions、integrations、CLI 和 developer experience。**Harness** 层拥有 agentic loop：tool calls、context management、observations，以及朝任务完成推进的过程。**Runtime/platform** 层拥有上层无法伪造的 compute、state 和 storage primitives：durable execution、sandboxed dynamic code execution、durable filesystem/workspace state、dynamic workflows、bindings、credential isolation 和 recovery。这个区分很有用，因为很多团队即使买了或构建了 framework，仍然需要一个 platform contract 来处理 crash recovery、untrusted code、长时间等待和 filesystem state。

Project Think 把同一条经验整理成一条实用框架：**primitive -> failure mode -> runtime implication**。durable execution with fibers 处理 eviction 后的进度丢失；sub-agents 处理“一个 agent 持有全部 context”的 failure mode；persistent sessions 处理 client disconnect 和跨 surface 迁移；sandboxed code execution 处理不可信生成代码；execution ladder 帮助在 foreground run、background run、workflow 和 fiber 之间选择；self-authored extensions 只有在 runtime 保存 capability boundary、review evidence 和 rollback path 时才安全。[^cloudflare-project-think] 所以这不只是另一个 vendor example，而是本章的检查清单：每次命名一个 primitive，都应该同时命名相邻的 failure mode 和 runtime obligation。

最小 requirements table 可以这样写：

| Production requirement | Runtime primitive |
| --- | --- |
| Run survives crash or deploy | durable run record, checkpoint boundary, resume cursor |
| Human waits for hours or days | explicit wait state, approval/refusal record, timeout policy |
| Tool or workflow step is retried | idempotency key, lease/retry policy, duplicate-write guard |
| Agent resumes after external input | resume event, expected event schema, stale-event handling |
| Work crosses tenants or workspaces | tenant/principal context, scoped stores, policy decision trace |
| Operator investigates behavior | trace span ids, evidence refs, exported session/run record |
| Runtime exposes tools and subagents | capability catalog, sandbox profile, MCP/A2A boundary contract |

简短说法是：prompt/tool/skill layer 负责定义 **agent 能做什么**，runtime layer 负责定义 **这次执行如何保持可治理、可恢复、可调查**。如果没有这条边界，团队通常会把整个系统都叫作 “agent harness”，然后很晚才发现 crash recovery、multi-tenancy、approval sleep/resume 和 observability 分散在不同地方，没有共同 contract。

在这条架构光谱较窄的一端，是本书作者的开源项目 Laconian：它的 `if` 是 Markdown-only behavioral skill。其可安装的 artifact 不包含 executable 或 tool-specific logic，也不会自行产生 external effects；任何 tool use 或 side effects 都属于 host task and runtime，而 benchmark machinery 留在该 runtime 所加载的 artifact 之外。[^laconian-runtime-boundary] 下文的 Cloudflare `security-audit` 案例位于另一端：一个由 durable multi-stage workflow 支撑的 skill-shaped entry point。

AWS AgentCore 和 GitHub security validation for third-party coding agents 可以作为同一个 contract 的新 production reference。[^aws-agentcore-agentops][^aws-agentcore-coding-agents][^github-third-party-coding-agent-validation] AgentCore AgentOps 把 traces、latency、token/cost metrics、session history、PII redaction 和 governance signals 变成可见对象；hosting coding agents 的例子补上 isolated session、persistent workspace、scoped credentials，以及用户关掉 laptop 后 agent 仍在 managed environment 里继续任务；GitHub validation 则说明，agent-generated code 在被视为 ready for review 之前，应该先经过 platform-owned CodeQL、dependency risk 和 secret scanning gates。

因此，可移植的 production runtime contract 可以写成：**isolated session → durable workspace → scoped credentials → egress/tool boundary → trace and cost ledger → PII redaction → platform security validation → human review artifact**。对参考运行时来说，这不是“必须用 AWS”或“必须用 GitHub”，而是一份 checklist：runtime 应该知道 workspace 在哪里、哪些 credentials 可用、哪些 network/tool boundaries 生效、这次 run 花费多少、哪些 sensitive fields 被 redacted、哪些 security gates 检查过 staged output，以及人类之后会 review 哪个 artifact。

Cloudflare 的 vulnerability harness 给这条边界补了一个很好的应用案例。[^cloudflare-vulnerability-harness] 它们的 security-audit skill 没有变成一个“大 agent”，而是变成了由 Recon、Hunt、Validate、Gapfill、Dedup、Trace、Feedback 和 Report 组成的 pipeline。关键的 runtime 细节是：每个 stage 都把状态写入 SQLite database，并用 `run_id`、`repo` 和 `stage` 做 key，因此 stage 可以 resume、retry，或者被后续 run 继续使用，而不会丢掉已经发现的 findings。这就是 runtime boundary：模型做窄任务，harness 拥有 durable state、queues、coverage cells、validation status 和 evidence。

在 vendor-neutral contract 中，这类 harness 应该携带：

- `harness_run_id`、`target_repo`、`stage_name`、`stage_attempt`、`stage_status`；
- `coverage_cell`，表示 area × attack-class 或其他可审查切片；
- `finding_candidate_id`、`validator_verdict`、`dedup_key`、`judgment_status`；
- `model_provider` 和 `model_version` 作为执行变量，而不是架构基础；
- `shallow_run_signal`，用于标记 stage 异常快速结束且没有 findings、sibling tasks 或 gapfill work；
- `fix_gate_status`，包括 targeted test before/after 和 clean fail→pass evidence；
- 对任何可能进入 production 的 change，都要有 `human_review_ref`。

这样 harness 才能做到 model-agnostic 和 failure-aware。如果 frontier model 改变、provider 调整 caching，或者 transient API error 作为文本出现在 `200 OK` response 中，durable orchestration 仍然必须 classify、retry 并保存 evidence，而不是把 empty output 当作 success。

Anthropic 的工作流分类又把这个问题压得更具体了，因为不同编排模式会带来不同的检查点需求。[^anthropic] `prompt chaining` 往往需要在固定阶段之间 checkpoint，`routing` 往往只需要在分类和交接边界 checkpoint，`parallelization` 需要汇合状态可见性，而 `orchestrator-workers` 需要能跨部分完成而存活的父/worker 协调状态。

LangGraph persistence 在 checkpoint granularity 层面说明了同一个原则：durable state 按 thread 组织，checkpoints 在 super-step 边界保存，而失败 super-step 中已经成功完成的 node writes 可以作为 pending writes 保留下来，这样 resume 时不需要重新执行已经成功的节点。[^langgraph-persistence] 架构结论是：“checkpointing” 不是一个 boolean。Runtime 应该明确命名用于 resume 的 cursor、允许 replay 的边界，以及故障之后不能重复提交的 partial writes。

Google Agent Executor 把相似的层描述成分布式 runtime primitive：agent execution graph 应该能跨 long-running jobs、disconnections、trajectory branching，并能从 event log restore，而不是依赖一个仍然存活的 process。[^google-agent-executor] 对基线运行时来说，这是一条 vendor-neutral 要求：如果用户关闭客户端、operator 启动替代分支，或者系统在故障后恢复 agent state，runtime 就需要 session event log、snapshot/restore boundary、single-writer 或 session-consistency rule，并且明确谁拥有当前活跃的 execution branch。

他们后续关于 harness 设计的工作又补上了一个更实际的运行时经验：在长时间运行的应用工作里，往往必须明确区分 **compaction** 和 **上下文重置**。[^anthropic-harness] Compaction 会让同一个智能体在缩短后的历史上继续工作，因此连续性还在，但上下文焦虑和累计漂移也可能继续存在。Reset 则是启动一个全新的智能体，并依赖结构化的交接工件来携带状态、下一步动作和评估上下文。这不只是提示技巧，而是运行时架构的一部分，因为一旦 resets 成为 harness 的组成部分，平台就必须决定哪些状态足够耐久、能跨 reset 保留下来，以及下一个智能体会继承什么审查工件。

但交接工件仍然不是授权工件。运行时应持久化[上下文连续性信封](../../appendix/continuity-envelope-schema.zh.md)，验证摘要指纹和事件沿袭，先核对任何状态未知的外部副作用，从权威系统重新加载身份与契约版本，再对下一次能力调用重新授权。成功的上下文复原只表示连续性已重建，绝不表示摘要批准了某项操作。

基线实现可以用以下顺序明确这条边界：

1. 压缩前，在安全边界停止，刷新只追加会话日志，保存工作流游标与未完成义务。
2. 不经摘要地保存控制字段，生成派生摘要，用 `summary_sha256` 将其绑定到源事件范围，并发出 `context_compaction`。
3. 重置后，从受治理存储加载信封，验证模式、摘要指纹、事件沿袭、租户、主体、委派范围、策略、能力、审批、预算、沙箱与检查点状态。
4. 如果外部副作用状态未知，返回 `blocked_on_reconciliation`；如果任一绑定变化，发出 `continuity_validation_failed` 并停止。
5. 只有在验证以及任何必要的副作用核对都成功后，才重建可丢弃的上下文视图、发出 `context_rehydration`，并在下一次能力调用前重新执行策略检查与授权。

所以有界自主不只是策略问题，也是一种运行时状态设计问题：每一种被允许的执行模式，都会带来自己的一套 pause、resume、reset 和完成语义。

如果运行时对这些情况没有显式形态，长时间工作最终通常都会泄漏成临时重试、重复请求和隐藏状态迁移。

### 8.2. 沙箱会话状态也是运行时状态

OpenAI Agents SDK 的 Sandbox Agents 做了一个很有用的区分，应该进入基线运行时设计：`Manifest` 描述 fresh workspace contract，而一次具体运行可以拿到 live sandbox session、序列化的 `session_state`，也可以从 `snapshot` 启动。[^openai-sandbox-agents]

OpenAI 关于 Responses API computer-environment 的文章把同一层描述成 agent computer：模型提出一个动作，平台在隔离容器里执行 shell command，把 streamed observation 返回给模型，然后下一个 model turn 决定是否继续。[^openai-computer-environment] 关键架构边界是：model decision 和 command execution 不是同一件事。模型提出动作；runtime 拥有 isolation、filesystem/artifact persistence、可选 structured storage、restricted network access、timeout/cancellation，以及可观测的 tool output。

更强的版本还应该记录每一个 **bounded tool-output cap** 和每一个 **concurrent tool session**。输出上限不是表面上的截断，而是 context budget 控制：保留有用 evidence，同时避免原始日志淹没下一轮模型上下文。并发会话也不只是更快执行；它们需要独立的 session ids、timeout/cancellation 状态、output envelopes 和 failure attribution，避免某个 shell、browser 或 data-processing 分支悄悄覆盖另一个分支的 observation。

对参考运行时来说，这意味着沙箱状态不应该消失在 tool adapter 里面。一个最小有用模型，至少应该在 `run_id` 和 `trace_id` 旁边追踪：

- `sandbox_session_id`；
- `sandbox_manifest_version`；
- `sandbox_permissions_profile`；
- 当运行从保存的 workspace 启动时的 `snapshot_id`；
- 已物化的 workspace entries，或指向已审查 manifest 的链接；
- 这个沙箱是否可以 resume、snapshot，还是必须重新创建。

这样，围绕文件、shell 和 memory 的长时间工作就不会变成磁盘上一团不透明目录。它会成为同一个 runtime-control 层的一部分，和 approvals、background runs、capability sessions、[追踪证据（trace evidence）](../../appendix/trace-schema.zh.md) 放在一起管理。

### 8.3. Stateful named agent instance 作为一种运行时拓扑

Cloudflare Agents SDK 展示了另一个有用的基线模式：智能体不一定只是 transient execution loop，也可以是一个**有名字的耐久运行时对象**。在这个模型里，每个 agent instance 都运行在 Durable Object 之上，拥有自己的 durable SQL/key-value state、WebSocket 连接、scheduled tasks，能在事件到来时醒来，也能在空闲时 hibernate。[^cloudflare-agents]

Cloudflare 更新后的说法把边界讲得更清楚：agent 是 **durable identity, not an always-on process**。[^cloudflare-long-running-agents] 对架构来说，这比具体平台更重要。`agent_instance_id` 应该跨 process、deploy、hibernation 和 connection break 存活；活跃 process 只是下一次 event 的临时执行者。因此 runtime contract 应该明确说明：哪些东西作为 named-instance state 被保存，哪些东西在 eviction 后会消失。

| 边界 | 跨 restart/hibernation 保留 | 不跨 restart/hibernation 保留 |
| --- | --- | --- |
| Agent state | `this.state`、durable SQL/key-value tables、迁移过 schema 的 instance metadata | class fields、local variables、未保存的 closures |
| 跨时间工作 | scheduled tasks、queued/background work、fiber checkpoints、durable workflow steps | `setTimeout`、`setInterval`、open fetches、promise chains |
| Sessions 与 UI | connection state、持久化 conversation/history refs、resumable stream cursor | open WebSocket frame、browser tab process、in-memory callback |
| Side effects | idempotency key、approval record、durable execution log、evidence refs | memory 里的 “already called” boolean、没有 ledger 的 partial tool call |

实际不变量是：任何可能在等待人类、故障或重启之后创建外部副作用的动作，都需要 durable log、idempotency key 和 replay boundary。否则“暂停后继续”就会变成一次重新执行，只能寄希望于本地内存还活着。

把它放进本书时，重点不是“应该使用 Cloudflare”，而是保留这种架构形态。当智能体绑定到某个真实事物的稳定名字上——customer case、project、device、tenant workspace、room、thread 或 research dossier——运行时就应该明确区分：

- `agent_instance_id`，它比单次 run 活得更久；
- `run_id`，它描述一次具体执行；
- `session_id`，它描述用户可见会话或 transport session；
- durable agent state，它可以跨 disconnect、deploy、hibernation 和 background wake-up 保留下来；
- external knowledge store，它不是某一个 instance 的私有可变状态。

这个模式特别适合 chat、voice、workflow 和 monitoring agents，因为用户期待的是连续性，而不是 stateless request/response。但它也引入了基线运行时必须显式暴露的风险：named instances 的 tenant isolation、跨 WebSocket sessions 的泄漏、hibernation 之后的 replay/resume、没有活跃用户时的 scheduled side effects，以及 agent version 变化时的 durable-state migrations。

因此，参考运行时不必实现 Durable Objects，但需要类似 `AgentInstanceStore` 和 `SchedulerBoundary` 的抽象：一个能看清哪个 named instance 拥有哪些状态、哪些 runs 修改过它、哪些 scheduled tasks 可能唤醒它、哪些 traces 能证明安全恢复的位置。

Scheduling 这一侧尤其重要：Cloudflare 展示了 delayed、scheduled、cron 和 interval tasks，这些任务会跨 restart 保留，persist 到 SQLite，并通过 Durable Object alarms 唤醒 agent。[^cloudflare-schedule] 对本书的架构结论是：schedule 不应该只是不可见的 callback，而应该表示成 durable control record，带有 owner instance、payload schema、idempotency key、overlap policy、next fire time 和 trace linkage。

GitHub Copilot cloud agent automations 展示了同一边界的 repo-native 形态：unattended work 可以从 repository events 或 scheduled triggers 启动，而不只来自手动请求。[^github-copilot-automations] 如果 automation 启动 Copilot cloud agent，runtime 应该记录 `automation_id`、trigger source、owner、branch policy、allowed events、approval boundary 和 evidence refs。Copilot code review 对 `AGENTS.md` 的支持又补了一条相邻契约：repo instructions 会成为 review agent 的输入，因此应该像 policy-bearing artifact 一样版本化，而不是停留在口头约定。[^github-copilot-agents-md] Copilot app 的 BYOK 把 provider-neutral control plane 扩展到 provider routing：keys、scopes 和 provider choice 应该属于 governed access model，而不是隐藏的 per-user setting。[^github-copilot-byok]

GitHub Copilot code review 还有一个独立教训："better tools" 如果没有任务形状，反而会让 reviewer 变差。GitHub 的 case study 说明，宽泛的 Unix-style tool access 一开始给 review agent 太多读取仓库和消耗预算的路径，却没有给出足够结构来产生有用 finding。[^github-copilot-review-tools] 可移植契约是 **workflow-constrained review**：先通过 pull request evidence、diff-anchored review questions 和 narrow-before-read 缩窄 review，再允许 targeted tool use，并保存 `tool_trace`、`review_cost`、evidence ref 和 `quality_gate`。Review agent 应该证明某个工具检查了哪个 PR fact 或 diff hypothesis，而不是把长日志当成信心证据。

Real-time 这一侧又增加了一条边界：connection state 不等于 agent state。在 Cloudflare Agents WebSocket model 中，一个 connection 有自己的 `id`、`uri`、per-connection `state`、tags、lifecycle hooks，并且可以针对某个 connection 关闭 identity/state/MCP 等 protocol messages。[^cloudflare-websockets] 对 baseline runtime 来说，这意味着 broadcast、presence、approval UI 和 streaming updates 都应该经过 connection-scoped authorization 和可追踪的 fan-out，而不是直接暴露 agent 的整个 durable state。

用厂商中立（vendor-neutral）的说法，这个模式可以叫**持久化智能体 actor（durable agent actor）**：它有稳定身份、本地持久状态、可恢复会话、计划唤醒，以及到受治理存储（governed stores）的可追踪移交。本地状态可以保存实例作用域事实（instance-scoped facts），例如当前工作流游标（workflow cursor）、界面/会话偏好、实例队列位置、最后处理事件、计划元数据，以及可以重建的小型缓存视图。它不应该悄悄成为用户画像记忆、租户知识、密钥、策略、审计日志或跨实例事实的权威记录系统（system of record）。这些数据应该属于受治理存储，并带有来源、保留、导出和访问控制契约。

这里的反模式是隐藏的持久记忆（hidden durable memory）：一个有名字的智能体持续积累私有状态，之后把它当作已验证知识来检索或行动，但操作员看不到导出、审计轨迹、模式迁移路径或删除故事。持久 actor 状态只有在负责人机制和生命周期明确时才有价值。

### 8.4. 可恢复的内部任务与纤程（Recoverable internal tasks / fibers）

Cloudflare 给这类拓扑又补了一条有用边界：durable work 不一定只能作为外部 workflow 存在，也可以是 agent 自己内部的 **recoverable internal task**。[^cloudflare-fibers] 在它的 API 里，`runFiber()` 会把工作登记到 SQLite，在执行期间保持 Durable Object 存活，允许 agent 用 `stash()` 保存中间 checkpoint，并在对象中途被 evict 后的下一次激活中调用 `onFiberRecovered()`。`startFiber()` 则适合那些需要 durable accept、用 idempotency key 去重、之后能 inspect/cancel，并且不保持原始 request 打开的 background work。

Vendor-neutral 的结论是：baseline runtime 至少应该区分四层长时间工作：

- **synchronous run：** 当前 request/response loop 里的短工作；
- **background/resumable run：** 用户可见、可以放入后台、观察并恢复的 run；
- **durable workflow：** 带 retries、waits、approvals 和 external events 的多步骤 orchestration spine；
- **internal recoverable fiber：** agent 自己循环中的一段工作，通过 checkpoint 和 recovery hook 跨 eviction/restart 存活。

最后这一层的最小契约包括：`fiber_id`、`fiber_name`、`fiber_status`、`fiber_idempotency_key`、`fiber_checkpoint_ref` 或 `stash_snapshot`、`recovery_handler`、`cancellation_status`、`last_safe_step`、`owner_agent_instance_id` 和 `evidence_refs`。这个契约不能变成 hidden durable memory 或 system of record。Checkpoint 是为了安全继续 expensive task，不是为了悄悄保存 profile facts、tenant knowledge、secrets 或 policy state。

在[参考包](../../appendix/reference-package.zh.md)里，durable named-agent topology 仍然只是 contract surface，而不是完整 Durable Object/fiber 实现：session/run exports 预留了 `agent_instance_id`、`durable_state_version`、`scheduled_wakeup_id` 和 `resumable_stream_id`，production adapter 可以继续补充 `fiber_id`、`fiber_status`、`fiber_checkpoint_ref` 和 `last_safe_step` 等 fiber evidence。对小型 runtime 来说这些字段通常为空；本书要展示的是 durable named instance 和 recoverable internal task 的边界，而不是把 reference package 变成 vendor-specific SDK。

Cloudflare Agents SDK changelog 又给这条边界补了一层更运营化的形态：通过 `runAgentTool` 启动 **detached sub-agent run**、记录 **durable milestones**、用统一入口 `runTurn` 接收 turn，并在 `deploy/eviction/reconnect` 后恢复。[^cloudflare-agents-background-subagents] 这实际上命名了一个 failure class：deploy、Durable Object eviction、connection churn 或 hung stream 发生在 agent run 中途。只要有 durable backbone、`continuation_id`、`last_durable_checkpoint`、idempotency key 和 bounded reconcile path，runtime 就不应该把工作简单标成 `interrupted` 后丢掉。

Cloudflare 关于 outbound connections 的另一条 changelog 说明，即使是“活着的”stream 也是 runtime contract，而不只是网络细节。[^cloudflare-outbound-connections] Durable Object 现在会在存在 active outbound connection 或 outbound WebSocket 时保持活跃，但只在明确的 keepalive window 内成立。对架构来说，long-running LLM stream 需要 `stream_id`、`connection_keepalive_deadline`、`last_emitted_offset`、`resume_strategy` 和 fallback checkpoint。否则团队可能把 stream 当成 durable，而实际上超过限制或连接关闭后，普通 eviction model 会重新生效。

Delegated tools 还有相邻规则。当 sub-agent 通过 `clientTools` 和 `onClientToolCall` 获得 **client-provided tools** 时，这不只是 callback convenience。[^cloudflare-agents-recovery] Parent runtime 应该保存这些 tools 的 allowlist、owner/caller identity、argument schema、expiration 和 trace evidence。否则 delegated sub-agent 会拿到隐式 capability leaks。Recovery path 也应该修复未完成的 tool calls：stream stall watchdog 和 interrupted tool-call repair 应该让 run 回到 last durable checkpoint，而不是从 transcript memory 重复 side effect。

### 8.5. 智能体外壳 + 持久工作流主线（Agent shell + durable workflow spine）

Cloudflare 的下一个有用模式是：不要把所有长时间工作都塞进同一个智能体事件循环（agent event loop）。智能体可以是**有状态交互边界（stateful interaction boundary）**：负责实例身份、WebSocket/HTTP 会话、本地状态、用户回调和当前对话视图。工作流则成为**持久执行边界（durable execution boundary）**：负责步骤、重试、等待外部事件、长时间审批门禁，以及故障后的恢复。[^cloudflare-workflows]

<div class="diagram-card">
<p>实时 agent 与 durable workflow 解决的是不同问题</p>

``` mermaid
flowchart LR
    S["Session / state store"] --> A["Agent runtime shell"]
    A --> W["Durable workflow spine"]
    W --> E["Tool / external event / approval step"]
    W --> L["Audit + evidence log"]
    A --> U["User-facing stream / WebSocket"]
    E --> L
```

</div>

在参考形态里，agent shell 可以报告进度、接收新消息并展示审批界面，但 durable workflow 应该拥有不能丢失的东西：step id、idempotency key、retry/timeout policy、external-event wait、approval decision 和 evidence refs。这样，agent 重启或 WebSocket 断开就不会把长时间工作变成只靠半截用户对话记住的状态。

在 Cloudflare HITL API 中，这表现为 workflow 里的 `waitForApproval()`：等待可以持续 **months or longer**，而不需要 live agent process；agent shell 则提供 `approveWorkflow()` 和 `rejectWorkflow()` 来接收 human decision。对本书来说，重点不是 API 名称，而是边界：pending approval、timeout、escalation 和 audit trail 必须是 durable execution state。

Cloudflare Agents SDK v0.16.1 在 Codemode runtime 侧展示了同一个契约：模型只拿到一个 `codemode` tool，对 typed globals 写代码，而 runtime 保存 durable execution log。[^cloudflare-agents-sdk-0161] 当代码到达 approval-gated action 时，execution pauses 并返回 pending approval；审批通过后，已经完成的 calls 从 durable log replay，approved action 被执行，同一段代码继续运行。用厂商中立（vendor-neutral）的说法，这是 approval gate 的一个有用最小契约：

- `approval_id`、`approval_status`、`requested_action`、`risk_tier`、`approver_ref`；
- 指向已完成 deterministic/tool calls 的 `execution_log_ref`；
- 区分 safe replay 与重复 side effect 的 `replay_policy`；
- approval 之后动作使用的 `idempotency_key`；
- `resume_cursor`、`timeout_policy` 和 `evidence_refs`。

这个 gate 应该属于 durable workflow 或 runtime log，而不是 UI callback。UI 可以显示审批按钮，但 pending state、replay 和 decision 之后的继续执行必须由执行系统拥有。

Cloudflare Dynamic Workflows 进一步强调了同一契约：`run(event, step)` 变成 durable plan，`step.do()` 执行耐久步骤，`step.sleep()` 或 `step.sleepUntil()` 让等待显式化，`step.waitForEvent()` 把外部信号或 human approval 放进执行模型本身。[^cloudflare-dynamic-workflows] 对 agent runtime 来说，这是一条边界：agent 可以选择或生成计划，但平台必须拥有 replay、retry、sleep/wait state、已经完成的 step results，以及哪些 events 可以安全恢复工作。

Cloudflare Workflows 的 saga rollbacks 补上了同一边界的 failure 侧：compensation 应该作为 metadata 放在 forward step 旁边，而不是藏在远处的 `catch` block 里。[^cloudflare-workflow-rollbacks] 当 workflow 进入 terminal failure，runtime 可以找到带 rollback handlers 的 eligible `step.do()` calls，把 persisted `output` 或 `undefined` 传给 handler，按 reverse `step-start` order 执行补偿，并在 restart 后通过 replay 重建需要的 handlers，而不会重复已完成的 side effects。对 agent workflows 来说，这是一条实用契约：如果某个 step 预留了 money、inventory、account、deployment slot 或 external quota，`compensation_ref` 和 `rollback_idempotency_key` 就应该从一开始属于 step record。

因此在 vendor-neutral contract 里，每个 durable step 都应该有 `step_id`、`step_type`、`idempotency_key`、`input_schema`、`output_ref`、`retry_policy`、`wait_event_type`、`approval_ref`、`compensation_ref`、`rollback_idempotency_key`、`rollback_retry_policy`、`timeout_policy` 和 `evidence_refs`。否则 “workflow” 又会变成一段寄希望于 retry 的长函数，而不是受治理的 execution spine。

### 8.6. 临时部署身份与人类 handoff

Cloudflare Temporary Accounts 给 durable workflows 又补了一个实用模式：agent 可以获得一个用于部署的 **temporary account**，之后人类再把结果 claim 到正常账户里。[^cloudflare-temporary-accounts] 这不只是 developer convenience。从架构上看，它是 agent deployment 的 lease model：agent 获得有边界的身份，执行 deployment step，留下 evidence，然后 ownership 转移给人类或团队。

在 vendor-neutral runtime contract 中，这种能力应该被显式建模：

- `temporary_principal_id` 和 `principal_issuer`；
- `lease_ttl`、`scope`、`allowed_deploy_targets` 和 `egress_policy`；
- `deployment_artifact_ref`、`deployment_url`、`rollback_ref` 和 `evidence_refs`；
- `claim_status`、`claimed_by`、`claim_deadline` 和 `unclaimed_cleanup_policy`；
- 从 temporary deploy 转入 owned production surface 的 `approval_ref`。

核心规则是：temporary account 不能变成新的长期 service user。它只是某个 agent step 的 work lease，具有短生命周期、窄 scope、trace linkage 和清晰结束状态：claimed、expired、revoked 或 cleaned up。如果 claim/handoff 没有被建模，agent deployment 很容易悄悄创建一个没有 owner 的 live resource，并绕过正常 lifecycle registry。

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


def continue_run(run_id: str, worker_id: str):
    run = claim_run(
        run_id,
        worker_id=worker_id,
        eligible_statuses={"queued", "waiting"},
        lease_seconds=30,
    )
    if run is None:
        return load_run(run_id)

    result = execute_run_steps(run, idempotency_scope=run.run_id)
    return complete_run(
        run_id,
        result=result,
        expected_version=run.version,
    )
```

`claim_run` 必须原子地获取租约并推进记录版本，每个外部步骤也必须
使用该运行的幂等范围。这样两个 worker 不会并发恢复同一个运行，
`expected_version` 也会拒绝陈旧的完成请求。

重点不在复杂，而在显式。长生命周期工作必须清楚到操作员能观察、客户端能轮询、运行时能恢复或取消，而不是靠猜。

## 12. 第一版参考实现不必过度复杂化的部分

一开始你并不需要立刻上这些东西：

- 带很多模式的复杂规划器；
- 多阶段记忆压缩流水线；
- 很复杂的模型路由；
- 完整自愈回路；
- 十几个黄金路径。

参考运行时的价值不在于功能最大化，而在于形态清晰。一个小而干净的实现，远比一个谁都看不懂的“万能机器”更有用。

### 12.1. Runtime 是 session、harness 和 hands 的拆分

检验 reference runtime 成熟度的另一个办法，是问它的部件能否彼此独立替换。在 managed-agent 形状里，session、harness 和 hands 被拆成接口，而不是同一个进程里的实现细节。[^anthropic-managed-agents] Anthropic 把这称为 decoupling brain from hands：model/harness 可以失败或变化，sandbox/tool executor 可以被重新创建，而 session log 仍然是外部 durable record，新 harness 可以通过 `wake(sessionId)` 继续接手。

对 reference package 来说，这意味着：

- session 保持为 append-only evidence log，并且能在 executor 故障后继续存在；
- harness 可以作为 control loop 被替换，而不需要迁移用户 workspace；
- sandbox/tools 作为 contained hands 工作，并带有显式的 network、filesystem、secrets 和 snapshot profiles；
- debug 通过 trace、lifecycle summary 和 sandbox profile 完成，而不是直接进入持有用户数据的环境。

这也和本章前面的内容相配：background execution、resumable runs 和 capability sessions 不再是“容器里的长请求”，而是 session state、control loop 和 contained execution surface 之间受治理的绑定。成熟度测试很简单：平台能不能替换 model、harness、sandbox 或某个 hand capability，同时不丢失 session history、audit trail，以及 operator 解释发生了什么的能力。

这里的实用契约比“保留历史”更严格。**session 不是 context window**：它是外部日志和状态 API，harness 从中组装下一轮 prompt，但它本身不需要完整塞进模型上下文。最小 runtime 接口可以是：

- session API：`wake(sessionId)`、`getEvents()` 和 `emitEvent(id, event)`，用于读取 durable log 并写入新的决策；
- hands API：`execute(name, input)` 用于调用具体 capability，`provision({resources})` 用于按 policy profile 发放 sandbox/tool 资源；
- failure contract：sandbox、tool executor、policy proxy 或 resource provision 的失败，应该作为普通 `tool-call error` 返回给 harness，而不是隐藏的进程崩溃；
- secret boundary：tokens 永远不应该被 sandbox 直接拿到；sandbox 拿到的是 brokered capability，而不是 raw credentials。

这样，brain 可以犯错，hands 可以失败，session 可以同时幸存，而 replay 看到的不是“模型失败”这种笼统结论，而是具体边界：资源不足、policy 拒绝 capability、sandbox 没启动，或者 tool 返回了受控错误。这让 managed-agent 拆分不仅可扩展，也可调查。


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

[^aws-agentcore-agentops]: AWS, [AgentOps: Operationalize agentic AI at scale with Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/agentops-operationalize-agentic-ai-at-scale-with-amazon-bedrock-agentcore/)

[^aws-agentcore-coding-agents]: AWS, [It’s safe to close your laptop now: Hosting coding agents on Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/its-safe-to-close-your-laptop-now-hosting-coding-agents-on-amazon-bedrock-agentcore/)

[^github-third-party-coding-agent-validation]: GitHub Changelog, [Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/)

[^openai-background]: [OpenAI, Background mode](https://developers.openai.com/api/docs/guides/background)

[^openai-agents-transforming-work]: OpenAI, [How agents are transforming work](https://openai.com/index/how-agents-are-transforming-work/)

[^openai-codex-maxxing]: OpenAI, [Codex-maxxing for long-running work](https://openai.com/index/codex-maxxing-long-running-work/)

[^langgraph-persistence]: [LangGraph, Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

[^google-agent-executor]: Google, [Introducing Agent Executor: a new runtime for AI agents](https://developers.googleblog.com/en/introducing-agent-executor-a-new-runtime-for-ai-agents/).

[^langchain-production-runtime]: LangChain, [The Runtime Behind Production Deep Agents](https://www.langchain.com/blog/runtime-behind-production-deep-agents).

[^anthropic-harness]: Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

[^anthropic-managed-agents]: Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents).

[^laconian-runtime-boundary]: Laconian，固定在 revision `669c45e849f75c99f81af19561d09cf24664e935`：[`skills/if/SKILL.md`](https://github.com/agent-axiom/laconian/blob/669c45e849f75c99f81af19561d09cf24664e935/skills/if/SKILL.md)与[`docs/design.md`](https://github.com/agent-axiom/laconian/blob/669c45e849f75c99f81af19561d09cf24664e935/docs/design.md)。

[^cloudflare-vulnerability-harness]: Cloudflare Blog, [Build your own vulnerability harness](https://blog.cloudflare.com/build-your-own-vulnerability-harness/).

[^cloudflare-flue-platform]: Cloudflare Blog, [Bringing more agent harnesses and frameworks to Cloudflare, starting with Flue](https://blog.cloudflare.com/agents-platform-flue-sdk/).

[^cloudflare-project-think]: Cloudflare Blog, [Project Think: building the next generation of AI agents on Cloudflare](https://blog.cloudflare.com/project-think/).

[^cloudflare-websockets]: [Cloudflare Agents SDK, WebSockets](https://developers.cloudflare.com/agents/api-reference/websockets/)

[^cloudflare-fibers]: [Cloudflare Agents SDK, Durable execution with fibers](https://developers.cloudflare.com/agents/runtime/execution/durable-execution/)

[^cloudflare-outbound-connections]: Cloudflare Changelog, [Outbound connections keep Durable Objects alive](https://developers.cloudflare.com/changelog/post/2026-06-19-outbound-connections-keep-dos-alive/)

[^cloudflare-workflows]: [Cloudflare Agents SDK, Workflows](https://developers.cloudflare.com/agents/concepts/workflows/)

[^cloudflare-dynamic-workflows]: Cloudflare Blog, [Introducing Dynamic Workflows: durable execution that follows the user, not the other way around](https://blog.cloudflare.com/dynamic-workflows/)

[^cloudflare-workflow-rollbacks]: Cloudflare Blog, [How we built saga rollbacks for Cloudflare Workflows](https://blog.cloudflare.com/rollbacks-for-workflows/)

[^cloudflare-schedule]: [Cloudflare Agents SDK, Schedule tasks](https://developers.cloudflare.com/agents/api-reference/schedule-tasks/)

[^cloudflare-agents]: [Cloudflare, Build Agents on Cloudflare](https://developers.cloudflare.com/agents/)

[^cloudflare-long-running-agents]: [Cloudflare Agents SDK, Long-running agents](https://developers.cloudflare.com/agents/concepts/agentic-patterns/long-running-agents/)

[^cloudflare-agents-sdk-0161]: Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/post/2026-06-16-agents-sdk-v0161/)
[^cloudflare-agents-background-subagents]: Cloudflare Changelog, [Agents SDK adds background sub-agents and a unified turn entry point](https://developers.cloudflare.com/changelog/product-group/ai/)
[^cloudflare-agents-recovery]: Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/product-group/ai/)

[^cloudflare-temporary-accounts]: Cloudflare Changelog, [Temporary Accounts: From agent deployments to claimed accounts](https://developers.cloudflare.com/changelog/2026-06-22-temporary-accounts/)

[^github-copilot-automations]: GitHub Changelog, [Schedule and automate tasks with Copilot cloud agent](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/)

[^github-copilot-agents-md]: GitHub Changelog, [Copilot code review: AGENTS.md support and UI improvements](https://github.blog/changelog/2026-06-18-copilot-code-review-agents-md-support-and-ui-improvements/)

[^github-copilot-byok]: GitHub Changelog, [GitHub Copilot app support for BYOK](https://github.blog/changelog/2026-06-23-github-copilot-app-support-for-byok/)

[^github-copilot-review-tools]: GitHub Blog, [Better tools made Copilot code review worse. Here's how we actually improved it](https://github.blog/ai-and-ml/github-copilot/better-tools-made-copilot-code-review-worse-heres-how-we-actually-improved-it/)

[^openai-sandbox-agents]: OpenAI Agents SDK, [Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/)、[Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/)、[Sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/) 与 [Agent memory](https://openai.github.io/openai-agents-python/sandbox/memory/)

[^openai-computer-environment]: OpenAI, [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/)
