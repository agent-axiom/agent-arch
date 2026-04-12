# Cheat Sheets

这页是给实际工作快速使用的。如果你不想在设计评审、上线前检查或团队讨论前重读整整一部分内容，就先看这里。

## Safety checklist

- 用户输入、记忆、工具和外部系统之间是否有明确的 trust boundaries？
- 每个敏感动作之前是否都有 policy gate，而不只是模型调用前有？
- low-risk 和 high-risk 工具是否清晰分开？
- 对于不可逆 side effect，是否有 approval gate？
- 是否定义了 allowed egress destinations 和 network access profile？
- policy decisions、approvals 和 tool execution 是否都写入了 audit trail？
- run loop 是否有清晰的 stop condition？

继续阅读：

- [第 3 章：安全边界与信任边界](../book/part-ii/chapter-3.zh.md)
- [第 4 章：工具网关、审批与审计链路](../book/part-ii/chapter-4.zh.md)

## Memory checklist

- short-term、long-term 和 profile memory 是否已经分开？
- memory read 和 memory write 是否有不同治理规则？
- persistent records 是否带有 provenance？
- 是否有明确 policy 来限制哪些内容可以写入 memory？
- 是否存在 compaction 或 background maintenance path？
- retrieval 是否被体量和相关性约束？
- 是否有清晰的 deletion 或 revision strategy？

继续阅读：

- [第 5 章：为什么智能体需要记忆，以及它为何危险](../book/part-iii/chapter-5.zh.md)
- [第 7 章：检索、压缩与后台更新](../book/part-iii/chapter-7.zh.md)

## Rollout checklist

- 这个 agent 是否有明确 owner，而不只是“某个团队”？
- 上线前是否有最低 eval baseline？
- 是否有包含 safety、observability 和 approval requirements 的 rollout gate？
- 哪些场景算 blocking failures，是否已经定义清楚？
- 对 failure、denial 和 approval backlog 是否有 runbook？
- 是否有 incident review 和 postmortem 机制？
- 是否能快速关闭 high-risk capability，而不需要停掉整个系统？

继续阅读：

- [第 12 章：智能体系统的 SLO](../book/part-v/chapter-12.zh.md)
- [第 18 章：生产上线检查清单](../book/part-vii/chapter-18.zh.md)

## Observability checklist

- 每个 run 是否都有 trace_id？
- retrieval、model step、tool execution、approval 和 memory write 是否都有 baseline spans？
- 是否有 structured events，而不只是原始日志？
- 是否能看出 gateway 做了什么 policy decision？
- 是否能看出哪个 tool principal 执行了 side effect？
- 是否能区分 success、denied、approval_wait 和 failure？
- 是否能把 runs 聚合成 session-level 或 eval-level summary？

继续阅读：

- [第 11 章：追踪、跨度与结构化事件](../book/part-v/chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)

## Tool gateway checklist

- 每个 capability 是否都有 owner、risk tier 和 approved inventory status？
- 是否清楚它是 read tool 还是 write tool？
- 是否定义了 execution profile：sandbox、network access、allowed egress？
- gateway 是否会在 execution 前检查 actor identity 和 policy？
- 是否定义了 idempotency semantics 和 retry policy？
- 是否明确什么时候需要 approval，什么时候可以自动执行？
- 每个外部动作是否都有 audit trail？

继续阅读：

- [第 8 章：执行模型与工具目录](../book/part-iv/chapter-8.zh.md)
- [第 9 章：沙箱执行与 MCP 作为集成契约](../book/part-iv/chapter-9.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](../book/part-iv/chapter-10.zh.md)

## 下一步做什么

- 在 design review 前：快速过一遍 safety、memory 和 tool gateway。
- 在上线前：重点过一遍 rollout 和 observability。
- 在 incident review 中：把 observability 和 safety 当成复盘框架。

- [从这里开始](../start-here.zh.md)
- [术语表](glossary.zh.md)
- [按场景组织的 Policy Templates 与 Checklists](policy-templates.zh.md)
