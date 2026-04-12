# 从这里开始

如果你是第一次来到这本书，不需要从头到尾线性阅读。它不是小说，也不是“把整个 AI 世界都讲一遍”的综述。它更像一本实践手册，讨论的是如何构建安全、可控、可运营的 AI 智能体，而不是把项目变成一堆 prompt、脚本和侥幸心理。

这页存在的目的有两个：

- 让你快速判断这本书是否适合你；
- 帮你为自己的角色找到一条最短阅读路径。

如果你想先看这本书的总体主张，请回到[首页](index.zh.md)。如果你要看结构和当前完成度，请直接打开[全书计划](book/plan.zh.md)。如果你需要可复用的工程工件与契约页面，请进入[参考层](reference.zh.md)。

## 如果你只读一章

如果你想用最短时间理解这本书的核心论点，请先读[第 1 章：为什么智能体需要平台，而不是魔法](book/part-i/chapter-1.zh.md)。

那一章最清楚地说明了本项目的核心立场：智能体系统应该被设计成可控的运行系统，而不是一堆 prompt 外面套一层薄薄包装。

## 这到底是一本什么书

这不是某个框架的使用手册，不是模型排行榜，也不是一篇 AI 生态热点导览。

它是一本面向真实落地团队的实践型架构书，讨论的是如何在存在信任边界、审批、遥测、评测与运维责任的环境中部署智能体系统。

## 快速了解项目成熟度

- `Published core`：主要章节已经发布完成。
- `Expanding now`：入口页、参考页与导航体验仍在持续增强。
- `Assets ready`：检查清单、案例研究、模式与可运行参考运行时已经可以独立使用。

## 这本书适合谁

如果你属于下面这些角色，这本书会特别有帮助：

- 正在把智能体能力接入产品的工程师；
- 想搭建共享运行时和策略层的平台工程师；
- 需要分析信任边界和高风险执行路径的安全工程师；
- 试图让智能体系统具备生产纪律的技术负责人或架构师；
- 寻找实践型开放手册，而不是 AI 营销页面的开源贡献者。

如果你要的是一个冷静、成熟、可解释的系统，而不是“世界上最自主的智能体”，那你来对地方了。

## 30 分钟能带走什么

如果你时间不多，我建议按这个顺序读：

1. [第 1 章：为什么智能体需要平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第 3 章：安全边界与信任边界](book/part-ii/chapter-3.zh.md)
3. [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
4. [第 11 章：追踪、跨度与结构化事件](book/part-v/chapter-11.zh.md)
5. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

读完这五章，你就已经能得到：

- 一套可工作的架构框架；
- 一套信任边界模型；
- 对安全工具执行的基本理解；
- 一套可观测性基线；
- 一套生产上线纪律。

## 按角色推荐阅读路径

### 如果你是产品工程师

建议按这个顺序读：

1. [第一部分：基础](book/part-i/index.zh.md)
2. [第二部分：安全边界](book/part-ii/index.zh.md)
3. [第四部分：工具与执行](book/part-iv/index.zh.md)
4. [第七部分：参考实现](book/part-vii/index.zh.md)

这条路径的目标，是尽快从一个智能体想法走到可运行的架构。

### 如果你是平台工程师

建议按这个顺序读：

1. [第 2 章：安全智能体的参考架构](book/part-i/chapter-2.zh.md)
2. [第三部分：记忆与知识](book/part-iii/index.zh.md)
3. [第四部分：工具与执行](book/part-iv/index.zh.md)
4. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
5. [第七部分：参考实现](book/part-vii/index.zh.md)

这条路径的目标，是搭出平台级骨架，而不只是一个智能体外壳。

### 如果你是安全工程师

建议按这个顺序读：

1. [第二部分：安全边界](book/part-ii/index.zh.md)
2. [第 5 章：为什么智能体需要记忆，以及它为何危险](book/part-iii/chapter-5.zh.md)
3. [第 9 章：沙箱执行与 MCP 作为集成契约](book/part-iv/chapter-9.zh.md)
4. [第 10 章：幂等性、重试、速率限制与回滚边界](book/part-iv/chapter-10.zh.md)
5. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

这条路径的目标，是不仅理解提示风险，还要真正理解执行风险。

### 如果你是负责人或架构师

建议按这个顺序读：

1. [第 1 章：为什么智能体需要平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
3. [第六部分：组织模型](book/part-vi/index.zh.md)
4. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

这条路径的目标，是理解如何避免一个智能体项目在运营和归属层面失控。

## 如果你更想先看代码

如果可运行工件比线性阅读更重要，可以从这里开始：

- [参考包](appendix/reference-package.zh.md)
- [第 16 章：基础运行时蓝图](book/part-vii/chapter-16.zh.md)
- [第 17 章：策略层与能力目录](book/part-vii/chapter-17.zh.md)

这些内容已经能给你：

- 最小运行时；
- 策略层；
- 能力目录；
- 记忆路径；
- 遥测；
- 发布检查。

## 如果你更想看模板和项目方向

建议先看这些页面：

- [全书计划](book/plan.zh.md)
- [为什么会有这本书](appendix/why-this-book.zh.md)
- [术语表](appendix/glossary.zh.md)
- [速查清单](appendix/cheat-sheets.zh.md)
- [实战案例](appendix/case-studies.zh.md)
- [按场景组织的 Policy Templates 与 Checklists](appendix/policy-templates.zh.md)
- [社区路线图](appendix/community-roadmap.zh.md)
- [参考来源](appendix/sources.zh.md)

这是最快理解项目未来方向，以及它如何服务更大社区的方式。

## 我需要快速解决什么问题

### 我需要安全的工具执行

- [第 4 章：工具网关、审批与审计轨迹](book/part-ii/chapter-4.zh.md)
- [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
- [第 9 章：沙箱执行与 MCP 作为集成契约](book/part-iv/chapter-9.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](book/part-iv/chapter-10.zh.md)

### 我需要设计记忆与检索纪律

- [第 5 章：为什么智能体需要记忆，以及它为何危险](book/part-iii/chapter-5.zh.md)
- [第 6 章：短期记忆、长期记忆与用户画像记忆](book/part-iii/chapter-6.zh.md)
- [第 7 章：检索、压缩与后台更新](book/part-iii/chapter-7.zh.md)
- [Memory Record 与 Retrieval Contract Schema](appendix/memory-retrieval-schema.zh.md)

### 我需要可观测性与评测

- [第 11 章：追踪、跨度与结构化事件](book/part-v/chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](book/part-v/chapter-13.zh.md)
- [Trace Schema 与 Event Catalog](appendix/trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](appendix/eval-schema.zh.md)

### 我需要上线治理与发布控制

- [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)
- [第 20 章：智能体系统的 Change Management](book/part-viii/chapter-20.zh.md)
- [第 22 章：Supply Chain、Provenance 与 Approved Artifacts](book/part-viii/chapter-22.zh.md)
- [第 27 章：Agent Inventory、Registry 与 Sprawl 控制](book/part-viii/chapter-27.zh.md)

## 这本书和别的内容有什么不同

这本书的立场很明确：

- workflow 比魔法更重要；
- 安全比炫目的 demo 更重要；
- execution layer 比“聪明的 tool calling”更重要；
- observability 比“好像能跑”更重要；
- platform thinking 比一堆局部 agent hacks 更重要。

所以这不是一本关于“最自主智能体”的书，而是一本关于成熟、安全、可解释 agent platform 的书。

## 下一步去哪里

如果你想马上开始：

- [打开全书计划](book/plan.zh.md){ .md-button .md-button--primary }
- [进入第一部分](book/part-i/index.zh.md){ .md-button }
- [查看参考运行时包](appendix/reference-package.zh.md){ .md-button }

如果你想参与贡献：

- [Contributing guide](https://github.com/agent-axiom/agent-arch/blob/main/CONTRIBUTING.md)
- [社区路线图](appendix/community-roadmap.zh.md)
