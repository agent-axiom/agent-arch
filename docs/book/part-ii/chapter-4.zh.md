# 第 4 章：工具网关、审批与审计轨迹

!!! info "怎样读这一章"
    这一章最好抓住一个具体瞬间，而不是把它当成通用安全清单：

    - 智能体已经形成了判断；
    - 智能体已经准备调用工具；
    - 系统现在必须决定，这个判断到底能不能被放行成外部副作用。

    如果这个转换点没有被严格设计，前面几章搭起来的架构层很快就会失去意义。

## 1. 真正昂贵的事故通常发生在哪里

智能体系统里最贵的失败，通常不是模型“想错了”，而是系统已经进入了动作阶段：

- 写了东西；
- 发了东西；
- 改了东西；
- 把数据导出去了。

这也是为什么执行边界比很多人想象得更重要。

在贯穿全书的支持场景里，这个问题非常具体：智能体已经查完申请状态，现在准备创建一个加急工单。在这之前，系统还主要是在“内部出错”。从这一刻开始，它要真正改动外部世界了。

## 2. 工具网关应该足够无聊、足够严格

一个好的工具网关只有一个很简单的任务：不要让智能体把漂亮的推理变成无法控制的副作用。

最低要求：

- 只接受被允许的工具；
- 验证参数；
- 知道这次操作的风险等级；
- 能在副作用发生前拦下调用；
- 把危险操作送去人工审批；
- 同时记录决策和执行事实。

下面是一个很实用的工具执行策略模板：

```yaml
tools:
  read_kb:
    risk: low
    approval: none
    allowed_roles: ["agent_runtime"]
  create_ticket:
    risk: medium
    approval: manager
    allowed_roles: ["agent_runtime"]
  prod_db_write:
    risk: critical
    approval: security_and_owner
    allowed_roles: []
    environments: ["staging"]
```

这段 YAML 里没什么“聪明”的东西，而这正是它好的地方。安全边界喜欢可见、可审查的规则。

!!! example "贯穿案例：受控的 `create_ticket`"
    在支持分诊案例里，`read_kb` 可以保持为低风险读取，但 `create_ticket` 是第一个真正的写入边界。网关应该先保存智能体的意图，校验工单参数，绑定行动者和租户上下文，按策略请求审批，然后才允许副作用真正发生。

**Gateway case-spine note：**同一条边界在三个 canonical cases 中会呈现不同形态。Support triage 考验 `create_ticket` 这样的 governed writes；Internal knowledge assistant 考验 scoped reads、source visibility 和 retrieval limits；Incident coordination 考验 escalation tools、notification tools，以及谁可以声明或更新 incident state。只理解其中一种形态的 gateway 仍然太窄。

### 2.1. 网关不只要知道工具，还要知道行动者

如果网关只校验工具名称和参数，那还不够。它还必须知道：**到底是谁在尝试调用这个能力**。

一个最低可用的网关请求模型，通常应该包含：

- `actor_id`；
- `actor_type`；
- `tenant_id`；
- `requested_capability`；
- `risk_class`；
- `approval_state`。

这样网关的判断就不再只是“这个工具可不可以用”，而是“这个工具能不能被这个行动者在这个上下文里调用”。

这正是身份从 IAM 表里的一条记录，变成可执行访问边界的时刻。[^google-secure-agents][^google-ai-controls]

## 3. 人工审批应该是一个正常流程

有些动作，智能体就不该自己完成：

- 修改生产数据；
- 向外部渠道发送消息；
- 财务相关操作；
- 访问敏感文档；
- 任何爆炸半径很高的动作。

对于这些操作，你需要的不只是一个“需要审批”开关，而是一条完整的确认流程。

<div class="diagram-card">
<p>高风险动作的审批流程大致是这样</p>

``` mermaid
sequenceDiagram
    autonumber
    participant R as 智能体运行时
    participant P as 策略引擎
    participant H as 人工审批人
    participant T as 工具网关
    participant A as 审计轨迹

    R->>P: 请求高风险动作
    P-->>R: 需要审批
    R->>H: 带上下文请求审批
    H-->>R: 批准 / 拒绝
    R->>T: 仅在批准后执行
    T->>A: 持久化动作与审批记录
```

</div>

不同产品会用不同方式实现这一点，但有用的平台通常不应该只有一种 approval pattern。Cloudflare Agents SDK 明确区分 durable workflow approval、AI chat tools 的 approval、client-side tool confirmation、MCP elicitation，以及通过 state/WebSocket 完成的轻量确认。[^cloudflare-hitl] 这是一个很好的实践提示：approval boundary 应该和 side effect 真正发生的位置一致。

如果 approval 属于 long-running workflow，它需要 timeout、escalation 和 durable resume。如果它是 browser/client-side tool，运行时必须知道一部分检查和结果来自 client boundary。如果它是 MCP elicitation，approval 就不只是 yes/no 开关，而更像带有自己 schema 的 structured input request。

一个好的审批流程总是会保存：

- 谁发起了这个动作；
- 风险等级是什么；
- 系统具体打算做什么；
- 谁批准了；
- 什么时间批准的；
- 是否覆盖了某个策略门禁。

## 4. 输出侧同样需要保护

很多团队会认真过滤输入数据，却几乎不考虑输出侧。这是个错误。

泄漏最常发生在出口：

- 智能体在回答里多贴了一段文档内容；
- 它把敏感文本送进了外部工具；
- 它把私有数据写进了日志；
- 它把别的租户的结果返回给了当前用户。

一个最小出口检查清单：

- 在需要的地方脱敏 PII；
- 遮盖密钥和令牌；
- 校验检索内容的租户归属；
- 限制出站目的地；
- 记录所有敏感出站动作。

## 5. 审计轨迹必须足够支持调查

仅仅“打开追踪”是不够的。对安全来说，你需要一条能让你重建事件历史的轨迹。

对于一次高风险运行，最好至少保留：

- 输入请求 ID；
- 主体和租户；
- 策略决策；
- 提示组装元数据；
- 经过安全脱敏的工具调用参数；
- 审批记录；
- 最终的出口事件。

如果事故发生后，团队只能看到“模型调用了工具 X”，那这场调查基本已经输掉一半了。

### 5.1. 审计轨迹里到底要连起什么

好的审计轨迹不只是存事件，它还要把事件之间的关系连起来：

- 哪个主体发起了运行；
- 哪个策略决策打开或拦住了动作；
- 哪个审批人批准了例外；
- 哪个工具主体真正去了外部系统；
- 最终产生了什么响应或副作用。

正是这种“可连接性”，才把日志变成调查材料，而不是一堆松散消息的仓库。

换句话说，一条审计轨迹至少应该回答四个问题：

1. 谁发起了动作？
2. 谁允许它继续执行？
3. 它到底以哪个身份离开了系统？
4. 它最终造成了什么响应或副作用？

如果这些问题里有任何一个回答不上来，那你大概率还没有真正的审计轨迹，而只是有一些可观测性，却没有足够的问责性。[^google-ai-controls]

## 6. 安全边界本质上是一组习惯

大家总会想找一个神奇库，仿佛它能“自动做安全”。但现实里，边界更像是一组习惯：

- 明确标记不可信数据；
- 不给智能体运行时多余权限；
- 工具只能通过网关；
- 危险动作必须审批；
- 关键步骤都进入审计轨迹；
- 系统不仅要会执行，也要会拒绝。

这才是智能体平台上成熟安全的样子。

## 7. 常见错误

这里反复出现的错误基本都是同一类：

- 为了“临时”集成去绕过网关；
- 审批提得太晚，危险动作已经几乎要执行了；
- 出口规则只存在于团队默契里，没有写成显式契约表面；
- 审计轨迹里缺少策略决策、主体或审批上下文；
- 写动作和读动作被按同一种风险来描述。

## 8. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 智能体有没有独立的身份模型？
- 可信指令和不可信内容是否分开了？
- 所有工具是否都经过网关？
- 有没有允许列表和参数校验？
- 高风险动作有没有审批流程？
- 有没有出口过滤？
- 审计轨迹是否足够支撑调查？
- 追踪里能不能看到到底哪个策略门禁被触发了？
- 能不能看到到底是哪个主体执行了外部调用？

如果连续几个问题答案都是“否”，那说明你现在读到这一章，时间正合适。

## 9. 下一步做什么

先把真实的执行边界和审批点画清楚，再把同一个请求继续带进记忆层和后续系统层。

- [第 3 章：安全边界与信任边界](chapter-3.zh.md)
- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](../part-iii/chapter-5.zh.md)
- [第二部分：安全边界](index.zh.md)
- [参考资料](../../appendix/sources.zh.md)

[^cloudflare-hitl]: [Cloudflare Agents SDK, Human in the Loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/)

[^google-secure-agents]: [Google Cloud, How Google secures AI Agents](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents)
[^google-ai-controls]: [Google Cloud, Recommended AI Controls framework](https://cloud.google.com/blog/products/identity-security/audit-smarter-introducing-our-recommended-ai-controls-framework)
