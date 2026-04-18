# 第 9 章：沙箱执行与 MCP 作为集成契约

!!! info "怎样读这一章"
    这一章最好抓住一个具体转换点：

    - 智能体已经选好了 capability；
    - 智能体已经准备调用外部 tool 或 adapter；
    - 平台现在必须决定，这个动作到底能通过什么 transport 执行，以及它会被关在什么边界里。

    如果这个转换点没有被写清楚，sandbox 和 MCP 很快就会变成一组术语，而不是 execution discipline。

## 1. 为什么缺少沙箱的执行层很快就会变得过度信任

在贯穿全书的 support 场景里，这一点非常具体：智能体已经决定去查申请状态，或者通过外部系统创建工单。从这一刻开始，问题已经不再是“下一步怎样更聪明”，而是“系统到底通过哪一道边界才允许它执行这一步”。

一旦智能体获得了工具访问能力，下一个危险几乎总是同一个：系统边界开始模糊。

智能体已经可以：

- 读取数据；
- 启动操作；
- 调用外部服务；
- 接收来自不可预测环境的响应。

如果这一切都“原样执行”，没有隔离和契约，平台很快就会积累问题：

- 工具以意外格式返回不可信载荷；
- 集成调用卡住或超出资源预算；
- 副作用在预期策略路径之外发生；
- 一个设计糟糕的适配器拖垮整个运行时。

所以执行层不只是路由器，它还是沙箱边界。

## 2. Sandbox 不一定是容器，它首先是一组限制

一说到 “sandbox”，很多人立刻想到 Docker、VM 或独立进程。这些都可以是实现方式，但架构上更重要的是：沙箱定义了能力被允许做什么、不允许做什么。

好的沙箱通常会限制：

- 网络访问；
- 文件系统访问；
- secrets 访问；
- CPU 和 memory budgets；
- allowed syscalls 或 execution mode；
- 操作生命周期。

也就是说，沙箱回答的是：“如果工具或适配器的行为比预期更糟，会发生什么？”

这不仅仅是安全问题，也是 blast radius 控制。

### 2.1. 最好区分不同层级的隔离

在实践里，`sandbox` 这个词经常把几种完全不同的东西混在一起：

- `logical isolation`：策略检查、能力契约、允许清单；
- `process isolation`：独立进程、timeout、resource limits；
- `runtime isolation`：独立执行环境、受限文件系统、受控网络出口、最小化密钥。

这很重要，因为很多团队觉得自己“已经有沙箱了”，但实际上只有第一层。对低风险读取来说这有时够用，但对高风险执行来说，几乎总要更强的运行时边界。[^google-sandbox]

这里有个很实用的问题：**如果 capability 的行为比预期更糟，到底是什么在阻止它：逻辑、进程边界，还是执行环境本身？**

## 3. 不能把外部集成当成普通函数

一个常见错误是：把外部服务包成一个函数，然后让智能体把它当普通调用使用。

但真实集成几乎总是：

- 比本地代码更不稳定；
- 类型边界更脆弱；
- 依赖权限和环境；
- 可能返回部分成功或危险结果；
- 自带 latency 和 rate limits。

所以更好的做法是把集成视为带契约的 capability endpoint，而不是“方便的 helper method”。

## 4. MCP 的价值就在于契约层

MCP 有用，不是因为它“新潮”，而是因为它能在智能体和外部 capability 之间提供清晰的 contract boundary。

在好的设计里，MCP 会给你这些收益：

- 标准化描述 tools 和 resources 的方式；
- 独立的 server boundary；
- 更清晰的 capability lifecycle；
- adapter 可以放在核心 runtime 之外；
- 天然适合作为 policy checks、logging 和 isolation 的切入点。

当你有的不是一个 runtime + 一个 integration，而是一组能力时，这一点就尤其重要。

## 4.1. 最好不要把 MCP host、client 和 server 搞混

MCP 周围常常会出现一些没必要的混乱，因为这些词听起来都很熟，但它们在系统里的角色其实很具体。

一个更清晰的理解方式是：

- `host` 是拥有会话、并决定到底要连接哪些 capabilities 的应用或 runtime；
- `client` 是 host 为了和某一个 MCP server 通信而创建出来的协议侧组件；
- `server` 是那个暴露 tools、resources 以及其他 capability surfaces，并返回结构化结果的 boundary。

这会带来两个很实用的结论：

- 一个 host 可以同时持有多个 clients；
- 一个 agent runtime 也可以同时和多个 MCP servers 工作，而不是把它们揉成一个分不清边界的 integration blob。

这看起来像术语细节，但其实很有帮助。MCP client 不是产品界面，也不是"agent 本体"。它是 host 和某个具体 server boundary 之间的 transport 与 contract layer。

<div class="diagram-card">
<p>MCP 适合作为 runtime 和外部 capabilities 之间的契约层</p>

``` mermaid
flowchart LR
    A["Agent runtime"] --> B["Execution layer"]
    B --> C["Policy and validation"]
    C --> D["MCP client"]
    D --> E["MCP server"]
    E --> F["Typed adapter"]
    F --> G["External API / system"]
    G --> F
    F --> E
    E --> D
    D --> B
```

</div>

## 5. 为什么要把 adapters 移出 core runtime

一旦 MCP 不再只是一个或两个手工接入的集成，问题就会升级为：**谁在把 MCP surface 当作平台资产来治理，而不是当作开发者本地便利工具？** Cloudflare 最近的材料很有价值，因为它把重点从“agent 会不会说 MCP”转向“团队怎样在规模化条件下发现、批准、路由和审计 MCP endpoints”。[^cloudflare-mcp]

这通常会把平台推向一个显式的 MCP control plane：

- 用于实验的 local ad hoc MCP servers；
- 用于共享生产能力的 governed remote MCP servers；
- 用于 approved servers 的 discovery / portal layer；
- 位于访问边界的 identity enforcement；
- 围绕 MCP path 本身的 audit 与 DLP controls。

这会带来很多直接收益：

- 单个 integration 的失败不容易拖垮 central runtime；
- 更容易按 capability 限制网络、secrets 和 filesystem；
- 不重写 orchestration 也能替换或升级某个 adapter；
- contracts 更清晰；
- capability 更容易独立测试。

当某些工具只读、某些会写外部系统、某些甚至执行代码或 shell 时，这一点尤其重要。

### 5.1. Enterprise MCP 需要的不只是 protocol，而是 control plane

很多团队都会在这里犯同一种成熟度错误。他们把 MCP 标准化成 protocol，却仍然用非正式方式接入服务器：有人把 endpoint 发进群聊，另一个团队把它复制进本地 config，很快就没人说得清哪些 MCP servers 是 approved，哪些只是实验性的，哪些则悄悄绕过了正常 review。

更成熟的模型会把 remote MCP 当作 platform control plane 的一部分：

- 平台通过 registry 或 portal 发布 approved MCP endpoints；
- capability owner 被明确标注；
- authentication 由统一 identity layer 中介，而不是藏在每个 desktop client 里；
- policy 与 DLP checks 可以把 MCP traffic 当作受治理表面来观察；
- MCP endpoint 的 retirement 被当作正常 lifecycle event 处理。

一旦 identity 成为中心问题，下一个设计问题就会出现：**到底是谁在为这次 MCP action 授权，它使用的是谁的 user context？** 这里需要 managed OAuth boundary，因为它能避免每个 MCP server 各自发明一套临时 credential story。

这通常意味着：

- user delegation 通过受治理的 identity layer 发放；
- token 是短生命周期的，并且可归因到具体 principal；
- MCP server 拿到的是 scoped access，而不是宽泛的长期 secrets；
- 平台可以在不重写每个 adapter 的情况下 revoke 或 rotate access。

同一套模型也能解释 **local MCP** 什么时候仍然合理：原型验证、隔离实验，或者非常窄的 team-local workflows。但对共享 business capabilities 来说，更合理的默认值通常应是：**remote、governed、discoverable、auditable**。

### 5.2. Shadow MCP 是 shadow API problem 的新版本

当 MCP 变得非常容易接入时，团队也会得到一种新的 shadow IT 形式：未登记的 MCP servers 已经承载真实 business actions，但其 ownership、review 和 control model 却没有被正式化。[^cloudflare-mcp]

这个 anti-pattern 往往有很明显的信号：

- capability 来自私人 config snippet，而不是 approved catalog；
- 没有人能说清 MCP server 的 owner；
- auth 依赖 long-lived local secrets；
- 没有统一 audit trail 可以说明哪个 agent 调用了哪个 MCP endpoint；
- platform team 往往要到 incident 之后才知道它存在。

一个有用的 platform checklist 可以很简单：

- 这个 MCP server 是否在 approved registry 里？
- 谁负责它的 lifecycle 与 incident response？
- 哪一层 identity boundary 在保护访问？
- 哪个 policy bundle 管理 write actions 与 approvals？
- 哪些 telemetry 字段能证明哪个 agent 在什么 decision context 下调用了它？

如果这些问题答不上来，问题就已经不只是“集成文档不完整”，而是平台在自己的控制模型之外制造了一条 shadow capability path。

这里还有一个很关键的追问：**平台能否重建这次 MCP action 的 authorization chain？** 在成熟模型里，operator 应该能追溯出：

- 是哪个 user 或 service principal 委托了访问；
- 是哪个 identity layer 签发或代理了 token；
- 是哪个 MCP server 接受了这份 delegated scope；
- 是哪个 agent run 使用这份授权执行了动作。

如果这条链路无法重建，那么平台的 auditability 就比 protocol surface 看起来要弱得多。

### 5.3. Ephemeral sandboxes 通常比常驻环境更好

Google 还有一个很有价值的提醒：对高风险 capability 来说，短生命周期的执行环境往往比常驻 worker 更健康。[^google-sandbox]

原因通常很直接：

- 状态更不容易在 runs 之间泄漏；
- 更容易限制 secrets 和临时文件的生命周期；
- cleanup 更容易解释；
- 一个脏 adapter 更不容易污染下一次任务。

常驻 worker 有时会赢在 latency，但经常输在隔离性和可解释性上。所以面对 high-risk execution，更合理的默认立场通常是：**ephemeral first，只有在明确需要时才保留持久环境**。

## 6. Stateful MCP 会改变 runtime 必须追踪的东西

AWS 最近的另一个信号也很有价值：一旦 MCP clients 和 servers 开始支持更强的 stateful interaction patterns，MCP 就不再只是一个 stateless tool envelope，而会更像一种带 session 的 runtime protocol。[^aws-stateful-mcp]

这会在几个非常实际的地方改变 execution contract：

- runtime 需要维护的不只是 user run，还可能包括每次 MCP interaction 的独立 `session_id`；
- capability 可能在最终结果出现之前先发送 progress notifications；
- server 可能在流程中途请求 elicitation 或额外 user input；
- expiry 与 re-initialization 会变成正常 lifecycle 的一部分，而不再只是 edge case；
- telemetry 不仅要说明调用了哪个 tool，还要说明是哪一个 MCP session instance 承载了这段工作。

如果平台在这些模式已经出现后，仍然把 MCP 当成完全 stateless 的东西，那么 pause/resume logic、approval routing 和 trace reconstruction 很快就会变得比本来复杂得多。

### 6.1. Stateless MCP 和 Stateful MCP 需要不同契约

这里一个很有用的区分是：

- `stateless MCP`：一次 request，对应一次 response，几乎没有 session continuity；
- `stateful MCP`：一个有边界的 interaction session，包含 progress、中间提示，以及可能的 resume / re-init 语义。

第二种模式通常要求平台提供更多控制：

- session lifecycle ownership；
- expiry handling；
- resumability rules；
- 面向 progress 和 elicitation events 的 telemetry；
- 能描述暂停后是否可自动恢复、还是必须重新审批的 policy fields。

这并不意味着 stateless MCP 过时了。它只是说明，平台不应该假装这两种模式在 operational 上完全一样。

### 6.2. Progress、elicitation 和 expiry 是 runtime events，不是 transport trivia

AWS 关于 stateful MCP 的方向还有一个很有价值的 operational lesson：难点不只是保存一个 session handle。[^aws-stateful-mcp] 更难的是，当 capability 发出 progress、请求更多输入，或在工作完成前先过期时，runtime 应该如何响应。

这通常会迫使平台至少把下面四类情况定义清楚：

- `progress_update`：capability 仍在工作，runtime 应该暴露 liveness，而不是把它误判成卡死；
- `elicitation_requested`：capability 不能继续，直到 user 或 operator 提供更多 input；
- `session_expired`：原来的 capability session 已经不能安全 resume；
- `reinitialized_session`：runtime 有意识地重新打开了一个新的 capability session，但仍把它挂在同一个更高层 user run 下。

这些并不是小小的 transport details。它们会直接塑造 approval、telemetry 和 operator response 的行为。

### 6.3. 好的 MCP contract 必须解释 interruption 之后会发生什么

如果一个 stateful capability 在中途暂停，平台不应该临时拼凑 recovery logic。

至少应该把这些规则写清楚：

- 同一个 capability session 在 human approval 之后是否还能 resume；
- expiry 是取消 run，还是触发 re-initialization；
- 下一步是否需要 fresh policy evaluation；
- 当 capability-side session 被轮换时，runtime 是否仍然保持同一个 user-visible run；
- 在排障时，telemetry 如何把旧 capability session 和新 capability session 关联起来。

如果这些问题没有答案，团队即使“技术上支持” stateful MCP，运营上仍然解释不清 interruption 之后到底发生了什么。

## 7. 不是所有 capability 都需要同等级别的隔离

把集成至少分成三类会很有帮助：

- low-risk read capabilities；
- medium-risk business actions；
- high-risk execution capabilities。

例如：

- `read_kb` 或 `search_docs` 可以用较轻的执行限制；
- `create_ticket` 或 `update_crm_record` 需要更严格的 policy 和 audit；
- `run_shell`、`exec_sql`、`deploy_job` 需要最强的 sandbox 和 approval。

如果所有工具都被放进同一种宽松 execution profile，平台要么不安全，要么很快就会因 side effects 产生事故。

## 7. Capability contract 不应只包含 input/output

很多团队对 input schema 还能描述得不错，但 operational contract 常常完全缺失。而实践中，这部分往往更关键。

最好明确写出：

- authentication mode；
- 访问是 platform-owned 还是 user-delegated；
- token lifetime 与 renewal rules；
- 每个 capability 的 scope boundaries；
- delegated authorization 需要记录哪些日志字段；
- 如果 delegated access 在 session 中途被撤销，runtime 应该怎么处理。

- read 或 write 属性；
- network policy；
- secret scope；
- allowed environments；
- timeout budget；
- retry policy；
- approval requirement；
- logging 和 redaction rules。

```yaml
capabilities:
  search_docs:
    transport: mcp
    mode: read
    network: internal_only
    secrets: none
    timeout_seconds: 8
    approval: none
  create_ticket:
    transport: mcp
    mode: write
    network: internal_only
    secrets: service_account_helpdesk
    timeout_seconds: 15
    approval: manager_for_high_priority
    session_mode: stateful
    progress_events: true
    elicitation: manager_or_requester
    on_session_expiry: reinitialize_or_cancel
  run_shell:
    transport: sandboxed_exec
    mode: high_risk
    network: denied
    filesystem: workspace_only
    secrets: none
    timeout_seconds: 10
    approval: always
```

这已经不只是函数描述，而是 capability 的行为契约。

## 8. Sandbox execution 应该返回 execution facts，而不只是 output

如果 sandbox 只返回 stdout 或 payload，你就丢掉了一半的隔离层价值。

为了调查和控制，最好还能返回：

- exit status；
- timeout flag；
- resource usage summary；
- side effect uncertainty；
- redacted logs；
- policy decision id。

这样 execution layer 才能解释得更成熟：不是“命令失败了”，而是“操作在 8 秒后超时中止、网络被禁止、side effect 未确认”。

### 8.1. Network egress 应该有自己单独的规则

很多事故发生，不是因为 capability “坏了”，而是因为它能去到没人预期的目的地。

所以 network egress 最好不要只当作 sandbox 的附属字段，而要被当成独立的 contract surface：

- `denied`；
- `internal_only`；
- `allowlisted_external`；
- `brokered_via_gateway`。

如果这里没有显式规则，事后通常很难解释：为什么某个 tool 明明“没违反规则”，却突然跑去访问了外部目标。

对 production-grade 平台来说，一个不错的默认值通常是：

- 只读内部工具：`internal_only`；
- external API adapters：`allowlisted_external`；
- code execution 和 shell-like tools：默认 `denied`。

## 9. 一个简单的 capability dispatch 示例

这个小 skeleton 展示的核心思想是：transport 和 execution profile 来自 capability contract，而不是由模型临时决定。

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    transport: str
    mode: str
    timeout_seconds: int


def dispatch_capability(spec: CapabilitySpec, args: dict) -> dict:
    if spec.transport == "mcp":
        return {"status": "success", "transport": "mcp", "capability": spec.name}
    if spec.transport == "sandboxed_exec" and spec.mode == "high_risk":
        return {"status": "approval_required", "capability": spec.name}
    return {"status": "validation_failure", "reason": "unsupported capability profile"}
```

它非常简单，但把一个正确前提固定下来：执行方式由平台决定，而不是模型每次重新发明。

## 10. 常见错误

这些问题现在会在两个层面重复出现：单个 adapter 层面，以及整个 MCP estate 层面。

这些问题一再重复：

- 某个 capability 拿到了超出必要范围的 network access；
- secrets 对过多 adapters 可见；
- tool result 把原始外部 payload 直接拖进 prompt；
- timeout 存在，但 side effect uncertainty 没有被建模；
- MCP server 接上了，但 policy 和 audit 根本没延伸进去；
- sandbox 名义上存在，但没有限制任何关键东西。

所以 sandbox 不能只是 checkbox-feature，它必须成为 execution design 的一部分。

## 11. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- adapters 是否和 core runtime 分开？
- 是否存在 per-capability execution profile？
- network、filesystem 和 secrets 是否被约束？
- 是否清楚到底使用的是 logical、process 还是 runtime isolation？
- transport 是否显式：direct、MCP、sandboxed exec？
- 系统是否区分 trustworthy 和 partially trusted result？
- business payload 之外是否保留 execution facts？
- 对 high-risk execution 是否使用了 ephemeral sandboxes？
- 能否解释为什么某个 capability 会在这个 run 中被允许？

如果这些答案很模糊，那说明 capability layer 还只是“一堆好用的集成”，而不是受管理的平台层。

## 12. 下一步做什么

先把 execution profile 和 isolation boundaries 固定下来，再进入重试、速率限制和回滚边界。

这一部分下一个自然主题是：幂等性、重试、速率限制和回滚边界。经过 sandbox 和 capability contracts 之后，这才是把 execution model 变成 production-grade 的关键。

- [第 8 章：执行模型与工具目录](chapter-8.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](chapter-10.zh.md)
- [第四部分：工具与执行](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-sandbox]: [Google Cloud, Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)
