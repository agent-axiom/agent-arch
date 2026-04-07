# 实战案例

这一页回答一个很直接的问题：这本书落到真实系统里，到底会长成什么样？

下面有三个场景。在这些场景里，架构层、guardrails 和 orchestration choices 已经可以被讨论成工程决策，而不只是漂亮的表述。

如果你需要的不是场景，而是可以直接复用的 policy artifacts，请去看[Policy Templates](policy-templates.zh.md)。如果你想看这本书接下来还要补什么，则看[社区路线图](community-roadmap.zh.md)。

## 案例 1：Support Triage Agent

### 系统做什么

这个 agent 接收客户请求，收集上下文，检查历史工单，然后选择下一个安全动作：

- 直接回复；
- 请求补充信息；
- 创建工单；
- 转交人工。

### 为什么这里值得用 agent

这里适合 agent，因为：

- 输入消息是非结构化的；
- 决策依赖文本、客户历史和 policy 的组合；
- 路径不是完全固定的，但也不需要完全自治。

这是一个很典型的 `workflow + guarded agent loop` 场景。

### 推荐形态

- 一个主 triage agent；
- 读取 customer profile 和 ticket history 的 read-heavy tools；
- 只保留一个 `create_ticket` write tool；
- 敏感动作前设置 approval boundary；
- 每次 run 都输出结构化 decision。

### 主要风险

- 客户文本里的 prompt injection；
- 相邻 tenant context 泄漏；
- 在不稳定集成中触发多余 write action；
- triage agent 自由度过大。

### 架构里最重要的点

- 严格把 instructions 和客户文本分开；
- 不让 agent 直接访问 helpdesk API；
- 把 stop conditions 放进 triage routine；
- 记录所有 write intents 和 approvals。

### 书里对应阅读

- [第 3 章：安全边界与信任边界](../book/part-ii/chapter-3.zh.md)
- [第 8 章：执行模型与工具目录](../book/part-iv/chapter-8.zh.md)
- [实践篇：Instructions、Routines 与 Prompt Templates](../book/part-i/practical-routines.zh.md)

## 案例 2：Internal Knowledge Agent

### 系统做什么

这个 agent 帮员工在文档、runbooks、工单和内部 wiki 里找到知识。

它会：

- 理解问题；
- 做 retrieval；
- 生成 grounded answer；
- 给出来源；
- 如果置信度低，就收敛回答，而不是瞎编。

### 为什么这里往往一个 agent 就够了

这个场景里，很多团队会过早走向 multi-agent。大多数时候其实没必要。

通常只需要：

- 一个 agent loop；
- 一个好的 retrieval pipeline；
- 独立 policy layer；
- 明确标记 untrusted content；
- answer generation 的质量闸门。

### 主要风险

- retrieval noise；
- 越权访问文档；
- 私有知识区泄漏；
- grounding 不足时的幻觉。

### 架构里最重要的点

- tenant 和 role 维度的 retrieval scope；
- short-term state 和 long-term memory 分开；
- 输出里有 source references；
- retrieval 和 answer assembly 都有 traces。

### 书里对应阅读

- [第 5 章：为什么智能体需要记忆，以及它为何危险](../book/part-iii/chapter-5.zh.md)
- [第 7 章：检索、压缩与后台更新](../book/part-iii/chapter-7.zh.md)
- [第 11 章：追踪、跨度与结构化事件](../book/part-v/chapter-11.zh.md)

## 案例 3：Incident Coordination Agent

### 系统做什么

这个 agent 在事故处理中帮助团队：

- 收集监控信号；
- 用上下文补全它们；
- 创建 incident thread；
- 提议下一个 runbook step；
- 把任务交给正确角色。

这已经不只是一个 chat assistant，而是一个 operational system component。

### 为什么这里尤其需要 orchestration discipline

这个场景特别容易犯两种错误：

- 做出一个过载的 manager agent；
- 或者太早引入 handoffs，结果责任被弄丢。

通常比较好的起点是：

- intake 和 coordination 用 manager pattern；
- 只有真正进入另一条 role boundary 时才做 handoff；
- 所有 write actions 都走 capability contracts。

### 主要风险

- noisy alerts 下的虚假确定性；
- 重复 side effects；
- handoff 过程里 audit trail 丢失；
- runtime permissions 过宽。

### 架构里最重要的点

- 整个 incident run 共享一条 trace；
- 每次 handoff 都有明确 ownership；
- ticketing 和 notifications 有 idempotency；
- risky remediation actions 需要 human approval。

### 书里对应阅读

- [实践篇：Manager Pattern vs Handoffs](../book/part-i/practical-manager-handoffs.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](../book/part-iv/chapter-10.zh.md)
- [第 18 章：生产上线检查清单](../book/part-vii/chapter-18.zh.md)

## 如何使用这些案例

最好不要把它们当连续章节来读，而是把它们当地图：

- 先选一个最像你自己任务的案例；
- 再顺着它的链接去读对应章节；
- 然后回来看一遍，检查自己的设计是不是已经被你自己过度复杂化了。

如果这本书真的要对社区有用，这类页面最终应该增长得最快，因为它们能把架构真正变成工程上的支点。
