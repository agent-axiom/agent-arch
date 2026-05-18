# 从这里开始

如果你第一次来到这本书，先问自己一个问题：你需要的是一个看起来厉害的演示智能体，还是一个能承受生产现实的系统？

这本书是写给第二种情况的。最适合把它读成一个完整论证：智能体系统怎样从提示堆出来的原型，长成带有信任边界、策略层、审批、可观测性、评测和生命周期纪律的受治理系统。

构建智能体很枯燥，但结果令人震撼：围绕信任边界、追踪、审批和发布建立纪律，才能把演示变成可以安全改进的系统。

!!! info "Draft localization preview"
    这份中文版本当前定位为 draft localization preview：内容可用于阅读和评审，但还不是 finished Chinese edition。请优先把它看作社区预览；正式出版前还需要统一术语、母语编辑和 print/PDF 导出检查。

这页只做一件事：帮你尽快选出阅读路线。

## 如果你只读一章

如果你想用最短时间进入本书的核心论点，请先读[第 1 章：为什么智能体需要的是平台，而不是魔法](book/part-i/chapter-1.zh.md)。

那一章把主张说得很直接：生产级智能体系统不能被建成“模型加几个工具”，它必须被设计成一个受治理的运行系统。

## 这是什么样的书

这不是某个框架的指南，也不是 AI 功能目录。这是一本实践型架构书，写给那些需要在真实环境里运行智能体的团队：那里有写入路径、人工审批、访问边界、遥测、评测，以及明确的运维负责人机制。

## 30 分钟路线

如果时间很少，就先读这条路径：

1. [第 1 章：为什么智能体需要的是平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第 3 章：安全边界与信任边界](book/part-ii/chapter-3.zh.md)
3. [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
4. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
5. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

走完这条路径后，你至少应该已经形成一个工作框架，能回答：

- 智能体的真实信任边界在哪里；
- 安全工具执行应该长什么样；
- 为什么没有追踪、SLO 和评测时，单靠“聪明模型”不够；
- 第一次认真发布之前到底需要什么。

!!! example "如果你想跟随贯穿案例"
    可以一路跟着 support-triage 故事走：它从检索和安全工具执行开始，经过重复工单恢复、traces、SLO 和评测门，然后继续进入 rollout、ADLC、保障、来源谱系、退役、失配控制、telemetry 和 registry。如果你想看到的是一条从事故到平台契约的路径，而不是一组抽象层，这是最好的路线。

!!! note "Canonical case routes"
    阅读路线旁边要同时保留三个 canonical cases 作为覆盖检查。**Support triage** 承载 write capabilities、approvals 和 duplicate-ticket recovery。**Internal knowledge assistant** 突出 retrieval、memory、freshness 和 knowledge provenance。**Incident coordination** 检查 traces、escalation、notification side effects、response ownership 和 post-incident learning。

## 按角色阅读

### 如果你是产品工程师

1. [第一部分：基础](book/part-i/index.zh.md)
2. [第二部分：安全边界](book/part-ii/index.zh.md)
3. [第四部分：工具与执行](book/part-iv/index.zh.md)
4. [第七部分：参考实现](book/part-vii/index.zh.md)

这条路线适合从智能体想法快速走到可运行架构。

### 如果你是平台工程师

1. [第 2 章：安全智能体的参考架构](book/part-i/chapter-2.zh.md)
2. [第三部分：记忆与知识](book/part-iii/index.zh.md)
3. [第四部分：工具与执行](book/part-iv/index.zh.md)
4. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
5. [第七部分：参考实现](book/part-vii/index.zh.md)

这条路线适合那些在搭平台骨架、而不只是给一个模型包壳的团队。

### 如果你是安全工程师

1. [第二部分：安全边界](book/part-ii/index.zh.md)
2. [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](book/part-iii/chapter-5.zh.md)
3. [第 9 章：沙箱执行与 MCP 作为集成契约](book/part-iv/chapter-9.zh.md)
4. [第 10 章：幂等性、重试、速率限制与回滚边界](book/part-iv/chapter-10.zh.md)
5. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

这条路线适合那些不仅要看模型风险，还要看真实执行风险的人。

### 如果你是负责人或架构师

1. [第 1 章：为什么智能体需要的是平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
3. [第六部分：组织模型](book/part-vi/index.zh.md)
4. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

这条路线适合那些不想只交付演示，而是要把项目放进真实运营纪律的人。

## 如果你想先看代码和工件

如果可执行支撑比线性阅读更重要，就先看这里：

- [参考包](appendix/reference-package.zh.md)
- [第 16 章：基础运行时蓝图](book/part-vii/chapter-16.zh.md)
- [第 17 章：策略层与能力目录](book/part-vii/chapter-17.zh.md)
- [参考页面](reference.zh.md)

如果你现在就需要运行时骨架、策略契约、记忆路径、遥测和发布工件，这条路线会更合适。

## 如果你要快速解决一个具体问题

### 安全工具执行

- [第 4 章：工具网关、审批与审计轨迹](book/part-ii/chapter-4.zh.md)
- [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
- [第 9 章：沙箱执行与 MCP 作为集成契约](book/part-iv/chapter-9.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](book/part-iv/chapter-10.zh.md)

### 记忆与检索

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](book/part-iii/chapter-5.zh.md)
- [第 6 章：短期记忆、长期记忆与用户画像记忆](book/part-iii/chapter-6.zh.md)
- [第 7 章：检索、压缩与后台更新](book/part-iii/chapter-7.zh.md)
- [记忆记录与检索契约模式](appendix/memory-retrieval-schema.zh.md)

### 可观测性、评测与发布

- [第 11 章：追踪、跨度与结构化事件](book/part-v/chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](book/part-v/chapter-13.zh.md)
- [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)
- [第 20 章：智能体系统的变更管理](book/part-viii/chapter-20.zh.md)

### Safe-agent schema spine

- [追踪 Schema 与事件目录](appendix/trace-schema.zh.md)
- [评测数据集 Schema 与打分契约](appendix/eval-schema.zh.md)
- [记忆记录与检索契约 Schema](appendix/memory-retrieval-schema.zh.md)
- [参考页面](reference.zh.md)

如果需要快速检查 MCP threat model、A2A handoff trust contract、verifier verdict record、governance action record、memory poisoning review fields 和 unified agent threat evidence，可以走这条路线。

## 读书时旁边还可以打开什么

- [全书计划](book/plan.zh.md)
- [为什么会有这本书](appendix/why-this-book.zh.md)
- [术语表](appendix/glossary.zh.md)
- [速查表](appendix/cheat-sheets.zh.md)
- [参考来源](appendix/sources.zh.md)

如果这本书对你来说，比另一页关于“自主性”的 AI 落地页更接近真实工程，那你来对地方了。
