# 最新进展

这一页是面向读者的简短更新日志，用来展示这本书和参考运行时最近有哪些重要增强。它不是 Git 历史的替代品，而是让读者快速看到项目是否持续演进。

_更新于 2026 年 5 月 18 日。_

!!! note "Canonical case update"
    2026 年 5 月 15 日的主要更新，是贯穿全书的三个 canonical cases 地图。**Support triage**、**Internal knowledge assistant** 和 **Incident coordination** 现在已经出现在 book chapters、public entry points、reference pages 和 appendix artifacts 中，并且 coverage guards 会防止 chapters 与 appendix pages 丢失这些路线。

!!! note "Safe-agent schema update"
    2026 年 5 月 17-18 日的更新，把 safe-agent architecture 的 prose、appendices 和 guards 连接了起来：MCP threat model、A2A handoff trust contract、verifier verdict record、governance action record、memory poisoning review fields 和 unified agent threat evidence 现在都反映在 [trace schema](appendix/trace-schema.zh.md)、[eval schema](appendix/eval-schema.zh.md) 与 [memory/retrieval schema](appendix/memory-retrieval-schema.zh.md) 中。

## 书籍

### 2026 年 5 月 14 日编辑 QA

第一组出版就绪 QA 问题已经关闭：第 1 章的判断框架从表格改成了更适合 HTML/PDF/纯文本抽取的文字块；变化较快的章节、参考来源页和最新进展页也更新了编辑审查日期。

为什么这很重要：外部阅读表面现在更少依赖表格渲染细节，也更清楚地说明了快速变化的 agent-security 章节何时被复核。

### 第八部分：智能体系统生命周期

现在全书已经包含 `SDLC→ADLC`、变更管理、保障回路、供应链、退役、错位、行为评测、AI 原生可观测性与清单控制的完整内容。

为什么这很重要：现在这本书覆盖的不只是架构与上线，还覆盖了智能体系统发布后的生命周期管理。

### 第一到第五部分的生产轮廓更完整了

书里现在补上了更多连接架构、检索、执行和评测纪律的桥：

- 第一部分更明确地区分了运行时架构、训练层和产品表面；
- 第二部分加入了更清晰的 `prompt injection`、`jailbreaking` 与 `action hallucination` 分类法；
- 第三部分加强了检索轮廓：`semantic gap`、`HyDE`、`RAG first`，以及持续预训练与 `SFT` 的区别；
- 第四部分补上了大工具目录、`semantic tool filtering` 和 `MCP host/client/server` 角色的实践指导；
- 第五部分补强了 `latency budget` 的产品视角，以及更实用的 `LLM-as-a-judge` 表述。

为什么这很重要：这本书现在覆盖的不只是基础平台层，也更贴近日常生产团队在设计评审、评测回路和发布之间反复遇到的问题。

## 参考层

### 可复用的参考层

站点现在已经包含以下参考页：

- 追踪与事件目录；
- 评测数据集与评分契约；
- 策略包与审批；
- 变更评审与发布门禁；
- 生命周期工件；
- 记忆检索契约。

为什么这很重要：读者现在可以从解释性章节直接跳到可审阅的模式与契约工件。

## 运行时

### 可运行的参考运行时

仓库中的 [`agent_runtime_ref`](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) 现在支持：

- 审批与 delegated authorization context；
- 控制项与 lifecycle runtime-control inspection；
- 生命周期工件；
- 会话导出与 replay summaries；
- 评测数据集导出；
- 带 redaction、redacted summaries、replay preservation 与 schema versioning 的追踪导出。

为什么这很重要：这本书现在不只依赖叙述性章节，也有可运行的参考实现作为支撑。

## 实践附录

### 更强的实践附录

站点已经包含：

- 术语表；
- 速查清单；
- 案例研究；
- 策略模板；
- 研究前沿页面；
- 社区路线图。

为什么这很重要：读者现在可以不按线性顺序通读全书，也能直接进入检查清单、案例研究、术语表与实践工件。

## 导航

### 入口页更强了

已更新：

- [从这里开始](start-here.zh.md)；
- [参考层](reference.zh.md)；
- [速查清单](appendix/cheat-sheets.zh.md)。

这些页面现在更容易把读者带到下面这些主题：

- `semantic tool filtering`；
- `HyDE` 与 `RAG vs training`；
- `latency budget` 与路由管线；
- `LLM-as-a-judge` 与评审器校准；
- `prompt injection`、`jailbreaking` 与 `action hallucination` 的区别。

为什么这很重要：这些新主题现在不只藏在单个章节里，也已经出现在读者真正会先打开的入口页上。

## 发布就绪度

### 发布前站点更干净了

在下一次部署之前，面向发布的质量检查已经启动，并向前推进了一步：

- 草稿与规划页面已从发布站点和 sitemap 中排除；
- 添加了 OpenGraph/Twitter metadata 和社交预览图；
- 检查了搜索索引、sitemap、robots、本地资源、锚点、图片 alt 文本和外部链接；
- 三种语言的 README 都加入了面向 `main` 与 `docs-prod` 的 fast-forward 发布检查清单。

这并不意味着面向出版的质量层已经完全关闭：深层 EN/ZH QA、rendering/export QA、sample-chapter polish，以及 manuscript/online companion 的包装仍然需要继续推进。

为什么这很重要：发布出来的站点应该持续接近一个打磨过的读者产品，而不是一堆 Markdown 文件的原始构建结果。

## 这对读者意味着什么

- 你可以把这本书当作手册使用。
- 你可以把参考页当作工程起点复用。
- 你可以运行示例运行时，而不仅仅是阅读 Markdown 文档。
- 你可以把架构建立在 OpenAI、Anthropic、Google、Microsoft 与 NIST 的近年资料之上。

## 继续阅读

- [从这里开始](start-here.zh.md)
- [参考层](reference.zh.md)
- [全书计划](book/plan.zh.md)
- [参考来源](appendix/sources.zh.md)
