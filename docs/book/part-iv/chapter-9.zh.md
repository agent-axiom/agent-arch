# 第 9 章：沙箱执行与 MCP 作为集成契约

!!! info "怎样读这一章"
    这一章最好抓住一个具体转换点：

    - 智能体已经选好了能力；
    - 智能体已经准备调用外部工具或适配器；
    - 平台现在必须决定，这个动作到底能通过什么传输方式执行，以及它会被关在什么边界里。

    如果这个转换点没有被写清楚，沙箱和 MCP 很快就会变成一组术语，而不是执行纪律。

## 1. 为什么缺少沙箱的执行层很快就会变得过度信任

在贯穿全书的支持场景里，这一点非常具体：智能体已经决定去查申请状态，或者通过外部系统创建工单。从这一刻开始，问题已经不再是“下一步怎样更聪明”，而是“系统到底通过哪一道边界才允许它执行这一步”。

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

## 2. 沙箱不一定是容器，它首先是一组限制

一说到“沙箱”，很多人立刻想到 Docker、VM 或独立进程。这些都可以是实现方式，但架构上更重要的是：沙箱定义了能力被允许做什么、不允许做什么。

好的沙箱通常会限制：

- 网络访问；
- 文件系统访问；
- 密钥访问；
- CPU 和内存预算；
- 允许的系统调用或执行模式；
- 操作生命周期。

也就是说，沙箱回答的是：“如果工具或适配器的行为比预期更糟，会发生什么？”

这不仅仅是安全问题，也是影响半径控制。

### 2.1. 最好区分不同层级的隔离

在实践里，`沙箱` 这个词经常把几种完全不同的东西混在一起：

- `logical isolation`：策略检查、能力契约、允许清单；
- `process isolation`：独立进程、超时、资源限制；
- `运行时隔离`：独立执行环境、受限文件系统、受控网络出口、最小化密钥。

这很重要，因为很多团队觉得自己“已经有沙箱了”，但实际上只有第一层。对低风险读取来说这有时够用，但对高风险执行来说，几乎总要更强的运行时边界。[^google-sandbox]

这里有个很实用的问题：**如果能力的行为比预期更糟，到底是什么在阻止它：逻辑、进程边界，还是执行环境本身？**

## 3. 不能把外部集成当成普通函数

一个常见错误是：把外部服务包成一个函数，然后让智能体把它当普通调用使用。

但真实集成几乎总是：

- 比本地代码更不稳定；
- 类型边界更脆弱；
- 依赖权限和环境；
- 可能返回部分成功或危险结果；
- 自带延迟和速率限制。

所以更好的做法是把集成视为带契约的能力端点，而不是“方便的助手方法”。

## 4. MCP 的价值就在于契约层

MCP 有用，不是因为它“新潮”，而是因为它能在智能体和外部能力之间提供清晰的契约边界。

在好的设计里，MCP 会给你这些收益：

- 标准化描述工具和资源的方式；
- 独立的 `server` 边界；
- 更清晰的能力生命周期；
- 适配器可以放在核心运行时之外；
- 天然适合作为策略检查、日志记录和隔离的切入点。

当你有的不是一个运行时 + 一个集成，而是一组能力时，这一点就尤其重要。

## 4.1. 最好不要把 MCP host、client 和 server 搞混

MCP 周围常常会出现一些没必要的混乱，因为这些词听起来都很熟，但它们在系统里的角色其实很具体。

一个更清晰的理解方式是：

- `host` 是拥有会话、并决定到底要连接哪些能力的应用或运行时；
- `client` 是 host 为了和某一个 MCP server 通信而创建出来的协议侧组件；
- `server` 是那个暴露工具、资源以及其他能力表面，并返回结构化结果的边界。

这会带来两个很实用的结论：

- 一个 host 可以同时持有多个 `client` 实例；
- 一个智能体运行时也可以同时和多个 MCP server 工作，而不是把它们揉成一个分不清边界的集成大泥团。

这看起来像术语细节，但其实很有帮助。MCP client 不是产品界面，也不是“智能体本体”。它是 host 和某个具体 server 边界之间的传输与契约层。

<div class="diagram-card">
<p>MCP 适合作为运行时和外部能力之间的契约层</p>

``` mermaid
flowchart LR
    A["智能体运行时"] --> B["执行层"]
    B --> C["策略与验证"]
    C --> D["MCP client"]
    D --> E["MCP server"]
    E --> F["类型化适配器"]
    F --> G["外部 API / 系统"]
    G --> F
    F --> E
    E --> D
    D --> B
```

</div>

## 5. 为什么要把适配器移出核心运行时

一旦 MCP 不再只是一个或两个手工接入的集成，问题就会升级为：**谁在把 MCP 表面当作平台资产来治理，而不是当作开发者本地便利工具？** Cloudflare 最近的材料很有价值，因为它把重点从“智能体会不会说 MCP”转向“团队怎样在规模化条件下发现、批准、路由和审计 MCP 端点”。[^cloudflare-mcp]

这通常会把平台推向一个显式的 MCP 控制平面：

- 用于实验的本地临时 MCP server；
- 用于共享生产能力的受治理的远程 MCP server；
- 用于已批准服务器的发现/门户层；
- 位于访问边界的身份执行；
- 围绕 MCP 路径本身的审计与 DLP 控制。

这会带来很多直接收益：

- 单个集成的失败不容易拖垮中心运行时；
- 更容易按能力限制网络、密钥和文件系统；
- 不重写编排也能替换或升级某个适配器；
- 契约更清晰；
- 能力更容易独立测试。

当某些工具只读、某些会写外部系统、某些甚至执行代码或 shell 时，这一点尤其重要。

### 5.1. 企业级 MCP 需要的不只是协议，而是控制平面

很多团队都会在这里犯同一种成熟度错误。他们把 MCP 标准化成协议，却仍然用非正式方式接入服务器：有人把端点发进群聊，另一个团队把它复制进本地配置，很快就没人说得清哪些 MCP server 已获批准，哪些只是实验性的，哪些则悄悄绕过了正常评审。

更成熟的模型会把远程 MCP 当作平台控制平面的一部分：

- 平台通过注册表或门户发布已批准的 MCP 端点；
- 能力负责人被明确标注；
- 身份认证由统一身份层中介，而不是藏在每个桌面客户端里；
- 策略与 DLP 检查可以把 MCP 流量当作受治理的表面来观察；
- MCP 端点的退役被当作正常生命周期事件处理。

一旦身份成为中心问题，下一个设计问题就会出现：**到底是谁在为这次 MCP 动作授权，它使用的是谁的用户上下文？** 这里需要托管 OAuth 边界，因为它能避免每个 MCP server 各自发明一套临时凭据故事。

这通常意味着：

- 用户委派通过受治理的身份层发放；
- token 是短生命周期的，并且可归因到具体主体；
- MCP server 拿到的是有范围的访问权，而不是宽泛的长期密钥；
- 平台可以在不重写每个适配器的情况下撤销或轮换访问权。

同一套模型也能解释 **本地 MCP** 什么时候仍然合理：原型验证、隔离实验，或者非常窄的团队本地工作流。但对共享业务能力来说，更合理的默认值通常应是：**远程、受治理、可发现、可审计**。

### 5.2. Shadow MCP 是影子 API 问题的新版本

当 MCP 变得非常容易接入时，团队也会得到一种新的 shadow IT 形式：未登记的 MCP server 已经承载真实业务动作，但其负责人、评审和控制模型却没有被正式化。[^cloudflare-mcp]

这个反模式往往有很明显的信号：

- 能力来自私人配置片段，而不是已批准目录；
- 没有人能说清 MCP server 的负责人；
- 认证依赖长期本地密钥；
- 没有统一审计轨迹可以说明哪个智能体调用了哪个 MCP 端点；
- 平台团队往往要到事故之后才知道它存在。

一个有用的平台清单可以很简单：

- 这个 MCP server 是否在已批准的注册表里？
- 谁负责它的生命周期与事故响应？
- 哪一层身份边界在保护访问？
- 哪个策略包管理写动作与审批？
- 哪些遥测字段能证明哪个智能体在什么决策上下文下调用了它？

如果这些问题答不上来，问题就已经不只是“集成文档不完整”，而是平台在自己的控制模型之外制造了一条影子能力路径。

这里还有一个很关键的追问：**平台能否重建这次 MCP 动作的授权链？** 在成熟模型里，操作员应该能追溯出：

- 是哪个用户或服务主体委托了访问；
- 是哪个身份层签发或代理了 token；
- 是哪个 MCP server 接受了这份委派作用域；
- 是哪个智能体运行使用这份授权执行了动作。

如果这条链路无法重建，那么平台的可审计性就比协议表面看起来要弱得多。

### 5.3. 短生命周期沙箱通常比常驻环境更好

Google 还有一个很有价值的提醒：对高风险能力来说，短生命周期的执行环境往往比常驻 worker 更健康。[^google-sandbox]

原因通常很直接：

- 状态更不容易在运行之间泄漏；
- 更容易限制密钥和临时文件的生命周期；
- 清理更容易解释；
- 一个脏适配器更不容易污染下一次任务。

常驻 worker 有时会赢在延迟，但经常输在隔离性和可解释性上。所以面对高风险执行，更合理的默认立场通常是：**短生命周期优先，只有在明确需要时才保留持久环境**。

## 6. Stateful MCP 会改变运行时必须追踪的东西

AWS 最近的另一个信号也很有价值：一旦 MCP client 和 server 开始支持更强的有状态交互模式，MCP 就不再只是一个无状态工具封套，而会更像一种带会话的运行时协议。[^aws-stateful-mcp]

这会在几个非常实际的地方改变执行契约：

- 运行时需要维护的不只是用户运行，还可能包括每次 MCP 交互的独立 `session_id`；
- 能力可能在最终结果出现之前先发送进度通知；
- 服务器可能在流程中途请求补充请求或额外用户输入；
- 过期与重新初始化会变成正常生命周期的一部分，而不再只是边缘情况；
- 遥测不仅要说明调用了哪个工具，还要说明是哪一个 MCP 会话实例承载了这段工作。

如果平台在这些模式已经出现后，仍然把 MCP 当成完全无状态的东西，那么暂停/恢复逻辑、审批路由和追踪重建很快就会变得比本来复杂得多。

### 6.1. Stateless MCP 和 Stateful MCP 需要不同契约

这里一个很有用的区分是：

- `stateless MCP`：一次请求，对应一次响应，几乎没有会话连续性；
- `stateful MCP`：一个有边界的交互会话，包含进度、中间提示，以及可能的恢复/重新初始化语义。

第二种模式通常要求平台提供更多控制：

- 会话生命周期负责人；
- 过期处理；
- 可恢复规则；
- 面向进度和补充请求事件的遥测；
- 能描述暂停后是否可自动恢复、还是必须重新审批的策略字段。

这并不意味着 `stateless MCP` 过时了。它只是说明，平台不应该假装这两种模式在运营上完全一样。

### 6.2. Progress、elicitation 和 expiry 是运行时事件，不是传输细节

AWS 关于有状态 MCP 的方向还有一个很有价值的运营教训：难点不只是保存一个会话句柄。[^aws-stateful-mcp] 更难的是，当能力发出进度、请求更多输入，或在工作完成前先过期时，运行时应该如何响应。

这通常会迫使平台至少把下面四类情况定义清楚：

- `progress_update`：能力仍在工作，运行时应该暴露存活状态，而不是把它误判成卡死；
- `elicitation_requested`：能力不能继续，直到用户或操作员提供更多输入；
- `session_expired`：原来的能力会话已经不能安全恢复；
- `reinitialized_session`：运行时有意识地重新打开了一个新的能力会话，但仍把它挂在同一个更高层用户运行下。

这些并不是小小的传输细节。它们会直接塑造审批、遥测和操作员响应的行为。

### 6.3. 好的 MCP 契约必须解释中断之后会发生什么

如果一个有状态能力在中途暂停，平台不应该临时拼凑恢复逻辑。

至少应该把这些规则写清楚：

- 同一个能力会话在人工审批之后是否还能恢复；
- 过期是取消运行，还是触发重新初始化；
- 下一步是否需要重新策略评估；
- 当能力侧会话被轮换时，运行时是否仍然保持同一个用户可见运行；
- 在排障时，遥测如何把旧能力会话和新能力会话关联起来。

如果这些问题没有答案，团队即使“技术上支持”有状态 MCP，运营上仍然解释不清中断之后到底发生了什么。

## 7. 不是所有能力都需要同等级别的隔离

把集成至少分成三类会很有帮助：

- 低风险读取能力；
- 中风险业务动作；
- 高风险执行能力。

例如：

- `read_kb` 或 `search_docs` 可以用较轻的执行限制；
- `create_ticket` 或 `update_crm_record` 需要更严格的策略和审计；
- `run_shell`、`exec_sql`、`deploy_job` 需要最强的沙箱和审批。

如果所有工具都被放进同一种宽松执行画像，平台要么不安全，要么很快就会因副作用产生事故。

## 7. 能力契约不应只包含输入/输出

很多团队对输入 schema 还能描述得不错，但运营契约常常完全缺失。而实践中，这部分往往更关键。

最好明确写出：

- 认证模式；
- 访问是平台拥有还是用户委派；
- token 生命周期与续期规则；
- 每项能力的作用域边界；
- 委派授权需要记录哪些日志字段；
- 如果委派访问在会话中途被撤销，运行时应该怎么处理。

- read 或 write 属性；
- 网络策略；
- 密钥作用域；
- 允许环境；
- 超时预算；
- 重试策略；
- 审批要求；
- 日志记录和脱敏规则。

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

这已经不只是函数描述，而是能力的行为契约。

## 8. 沙箱执行应该返回执行事实，而不只是输出

如果沙箱只返回 stdout 或载荷，你就丢掉了一半的隔离层价值。

为了调查和控制，最好还能返回：

- 退出状态；
- 超时标志；
- 资源使用摘要；
- 副作用不确定性；
- 脱敏日志；
- 策略决策 ID。

这样执行层才能解释得更成熟：不是“命令失败了”，而是“操作在 8 秒后超时中止、网络被禁止、副作用未确认”。

### 8.1. 网络出口应该有自己单独的规则

很多事故发生，不是因为能力“坏了”，而是因为它能去到没人预期的目的地。

所以网络出口最好不要只当作沙箱的附属字段，而要被当成独立的契约表面：

- `denied`；
- `internal_only`；
- `allowlisted_external`；
- `brokered_via_gateway`。

如果这里没有显式规则，事后通常很难解释：为什么某个工具明明“没违反规则”，却突然跑去访问了外部目标。

对生产级平台来说，一个不错的默认值通常是：

- 只读内部工具：`internal_only`；
- 外部 API 适配器：`allowlisted_external`；
- 代码执行和类 shell 工具：默认 `denied`。

### 8.2. 把沙箱 manifest 当作执行契约

OpenAI 最近的 Sandbox Agents 文档给这个问题补了一种很实用的形态：沙箱不应只被描述成“容器”或“隔离环境”，而应通过显式的 `Manifest`、capabilities、permissions、workspace entries、snapshot 和 session state 来描述。[^openai-sandbox-agents]

这和本章的执行契约可以直接对齐。平台至少要回答四个问题：

- 哪些文件、仓库、mounts 和 environment 会被物化进启动 workspace；
- 哪些沙箱原生能力可用：filesystem、shell、memory、skills、compaction；
- 命令、文件修改和文件读取使用哪些 permissions 与 `run_as` 身份；
- 继续执行时到底使用 live `sandbox_session`、序列化的 `session_state`，还是从 `snapshot` 启动的新会话。

这样的 manifest 不能替代策略层。它让执行边界变得可审查：reviewer 可以看到什么进入了 workspace、智能体拿到了哪些权限，以及这项工作是否能安全地 resume 或 snapshot。

## 9. 一个简单的能力分发示例

这个小骨架展示的核心思想是：传输和执行画像来自能力契约，而不是由模型临时决定。

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

这些问题现在会在两个层面重复出现：单个适配器层面，以及整个 MCP 资产层面。

这些问题一再重复：

- 某项能力拿到了超出必要范围的网络访问权；
- 密钥对过多适配器可见；
- 工具结果把原始外部载荷直接拖进提示；
- 超时存在，但副作用不确定性没有被建模；
- MCP server 接上了，但策略和审计根本没延伸进去；
- 沙箱名义上存在，但没有限制任何关键东西。

所以沙箱不能只是打勾功能，它必须成为执行设计的一部分。

## 11. 现在就该做什么

先过一遍这份短清单，把所有回答为“否” 的地方单独记下来：

- 适配器是否和核心运行时分开？
- 是否存在每项能力的执行画像？
- 网络、文件系统和密钥是否被约束？
- 是否清楚到底使用的是逻辑隔离、进程隔离还是运行时隔离？
- 传输是否显式：`direct`、MCP、`sandboxed_exec`？
- 系统是否区分可信结果和部分可信结果？
- 业务载荷之外是否保留执行事实？
- 对高风险执行是否使用了短生命周期沙箱？
- 能否解释为什么某项能力会在这次运行中被允许？

如果这些答案很模糊，那说明能力层还只是“一堆好用的集成”，而不是受管理的平台层。

## 12. 下一步做什么

先把执行画像和隔离边界固定下来，再进入重试、速率限制和回滚边界。

这一部分下一个自然主题是：幂等性、重试、速率限制和回滚边界。经过沙箱和能力契约之后，这才是把执行模型变成生产级的关键。

- [第 8 章：执行模型与工具目录](chapter-8.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](chapter-10.zh.md)
- [第四部分：工具与执行](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^cloudflare-mcp]: [Cloudflare, Build and deploy Remote Model Context Protocol (MCP) servers to Cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)

[^aws-stateful-mcp]: [AWS, Introducing stateful MCP client capabilities on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-stateful-mcp-client-capabilities-on-amazon-bedrock-agentcore-runtime/)

[^google-sandbox]: [Google Cloud, Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)

[^openai-sandbox-agents]: OpenAI Agents SDK, [Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/)、[Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/)、[Sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/) 与 [Agent memory](https://openai.github.io/openai-agents-python/sandbox/memory/)
