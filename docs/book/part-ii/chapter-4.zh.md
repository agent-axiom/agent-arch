# 第 4 章：Tool Gateway、Approval 与 Audit Trail

!!! info "怎样读这一章"
    这一章最好抓住一个具体瞬间，而不是把它当成通用安全清单：

    - 智能体已经形成了判断；
    - 智能体已经准备调用 tool；
    - 系统现在必须决定，这个判断到底能不能被放行成外部 side effect。

    如果这个转换点没有被严格设计，前面几章搭起来的架构层很快就会失去意义。

## 1. 真正昂贵的 incident 通常发生在哪里

agent systems 里最贵的失败，通常不是模型“想错了”，而是系统已经进入了动作阶段：

- 写了东西；
- 发了东西；
- 改了东西；
- 把数据导出去了。

这也是为什么 execution boundary 比很多人想象得更重要。

在贯穿全书的 support 场景里，这个问题非常具体：智能体已经查完申请状态，现在准备创建一个加急工单。在这之前，系统还主要是在“内部出错”。从这一刻开始，它要真正改动外部世界了。

## 2. Tool gateway 应该足够无聊、足够严格

一个好的 tool gateway 只有一个很简单的任务：不要让 agent 把漂亮的推理变成无法控制的 side effect。

最低要求：

- 只接受被允许的工具；
- 验证参数；
- 知道这次操作的 risk class；
- 能在 side effect 发生前拦下调用；
- 把危险操作送去 human approval；
- 同时记录决策和执行事实。

下面是一个很实用的 tool execution policy 模板：

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

这段 YAML 里没什么“聪明”的东西，而这正是它好的地方。Security perimeter 喜欢可见、可审查的规则。

### 2.1. Gateway 不只要知道 tool，还要知道 actor

如果 gateway 只校验 tool 名称和参数，那还不够。它还必须知道：**到底是谁在尝试调用这个 capability**。

一个最低可用的 gateway request model，通常应该包含：

- `actor_id`；
- `actor_type`；
- `tenant_id`；
- `requested_capability`；
- `risk_class`；
- `approval_state`。

这样 gateway 的判断就不再只是“这个 tool 可不可以用”，而是“这个 tool 能不能被这个 actor 在这个上下文里调用”。

这正是 identity 从 IAM 表里的一条记录，变成可执行访问边界的时刻。[^google-secure-agents][^google-ai-controls]

## 3. Human approval 应该是一个正常流程

有些动作，agent 就不该自己完成：

- 修改 production 数据；
- 向外部渠道发送消息；
- 财务相关操作；
- 访问敏感文档；
- 任何 blast radius 很高的动作。

对于这些操作，你需要的不只是一个 “approval required” 开关，而是一条完整的确认流程。

<div class="diagram-card">
<p>高风险动作的 approval flow 大致是这样</p>

``` mermaid
sequenceDiagram
    autonumber
    participant R as Agent runtime
    participant P as Policy engine
    participant H as Human approver
    participant T as Tool gateway
    participant A as Audit trail

    R->>P: Request risky action
    P-->>R: Approval required
    R->>H: Ask for approval with context
    H-->>R: Approve / reject
    R->>T: Execute only if approved
    T->>A: Persist action + approval record
```

</div>

一个好的 approval flow 总是会保存：

- 谁发起了这个动作；
- 风险等级是什么；
- 系统具体打算做什么；
- 谁批准了；
- 什么时间批准的；
- 是否 override 了某个 policy gate。

## 4. 输出侧同样需要保护

很多团队会认真过滤输入数据，却几乎不考虑输出侧。这是个错误。

泄漏最常发生在 egress：

- agent 在回答里多贴了一段文档内容；
- 它把敏感文本送进了外部 tool；
- 它把私有数据写进了日志；
- 它把别的 tenant 的结果返回给了当前用户。

一个最小 egress checklist：

- 在需要的地方 redact PII；
- mask 掉 secrets 和 tokens；
- 校验 retrieved content 的 tenant ownership；
- 限制 outbound destinations；
- 记录所有敏感 outbound actions。

## 5. Audit trail 必须足够支持调查

仅仅“打开 tracing”是不够的。对安全来说，你需要一条能让你重建事件历史的 trail。

对于一次高风险 run，最好至少保留：

- 输入 request id；
- principal 和 tenant；
- policy decision；
- prompt assembly metadata；
- 经过安全脱敏的 tool call arguments；
- approval records；
- 最终的 egress event。

如果 incident 发生后，团队只能看到“模型调用了 tool X”，那这场调查基本已经输掉一半了。

### 5.1. Audit trail 里到底要连起什么

好的 audit trail 不只是存事件，它还要把事件之间的关系连起来：

- 哪个 principal 发起了 run；
- 哪个 policy decision 打开或拦住了动作；
- 哪个 approver 批准了例外；
- 哪个 tool principal 真正去了外部 system；
- 最终产生了什么 response 或 side effect。

正是这种“可连接性”，才把日志变成调查材料，而不是一堆松散消息的仓库。

换句话说，一个 audit trail 至少应该回答四个问题：

1. 谁发起了动作？
2. 谁允许它继续执行？
3. 它到底以哪个 identity 离开了系统？
4. 它最终造成了什么 response 或 side effect？

如果这些问题里有任何一个回答不上来，那你大概率还没有真正的 audit trail，而只是有一些 observability，却没有足够的 accountability。[^google-ai-controls]

## 6. Security perimeter 本质上是一组习惯

大家总会想找一个神奇库，仿佛它能“自动做安全”。但现实里，perimeter 更像是一组习惯：

- 明确标记 untrusted data；
- 不给 agent runtime 多余权限；
- tools 只能通过 gateway；
- 危险动作必须 approval；
- 关键步骤都进入 audit trail；
- 系统不仅要会执行，也要会拒绝。

这才是 agent platform 上成熟安全的样子。

## 7. 实用检查清单

如果你想快速评估当前 perimeter，可以过一遍这个清单：

- agent 有没有独立的 identity model？
- trusted instructions 和 untrusted content 是否分开了？
- 所有 tools 是否都经过 gateway？
- 有没有 allowlist 和参数校验？
- high-risk 动作有没有 approval flow？
- 有没有 egress filtering？
- audit trail 是否足够支撑调查？
- traces 里能不能看到到底哪个 policy gate 被触发了？
- 能不能看到到底是哪个 principal 执行了外部调用？

如果连续几个问题答案都是 “no”，那说明你现在读到这一章，时间正合适。

## 8. 下一步做什么

先把真实的 execution boundary 和 approval points 画清楚，再把同一个请求继续带进 memory layer 和后续系统层。

- [第 3 章：安全边界与信任边界](chapter-3.zh.md)
- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](../part-iii/chapter-5.zh.md)
- [第二部分：安全边界](index.zh.md)
- [参考资料](../../appendix/sources.zh.md)

[^google-secure-agents]: [Google Cloud, How Google secures AI Agents](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents)
[^google-ai-controls]: [Google Cloud, Recommended AI Controls framework](https://cloud.google.com/blog/products/identity-security/audit-smarter-introducing-our-recommended-ai-controls-framework)
