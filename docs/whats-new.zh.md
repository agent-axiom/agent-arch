# 最新进展

这一页是面向读者的简短更新日志，用来展示这本书和参考运行时最近有哪些重要增强。它不是 Git 历史记录（Git history）的替代品，而是让读者快速看到项目是否持续演进。

_更新于 2026 年 5 月 20 日。_

!!! note "规范案例更新"
    2026 年 5 月 15 日的主要更新，是贯穿全书的三个规范案例（canonical cases）地图。**支持分流（Support triage）**、**内部知识助手（Internal knowledge assistant）** 和 **事件协调（Incident coordination）** 现在已经出现在章节（book chapters）、公共入口（public entry points）、参考页（reference pages）和附录工件（appendix artifacts）中，并且覆盖率守卫（coverage guards）会防止章节（chapters）与附录页面（appendix pages）丢失这些路线。

!!! note "安全智能体架构（safe-agent）模式更新"
    2026 年 5 月 17 日到 2026 年 5 月 19 日的更新，把安全智能体架构（safe-agent architecture）的正文（prose）、附录（appendices）和防护检查（guards）连接了起来：MCP 威胁模型（MCP threat model）与 `mcp_server` 合约（contract）、A2A 交接信任合同（A2A handoff trust contract）与信任委派工件（trust-delegation artifact）、纵深防御控制图（defense-in-depth control map）、验证者裁决记录（verifier verdict record）、治理动作记录（governance action record）、NIST AI RMF 遥测映射（NIST AI RMF telemetry mapping）、记忆投毒审查字段（memory poisoning review fields）和统一智能体威胁证据（unified agent threat evidence）现在都反映在 [跟踪模式（trace schema）](appendix/trace-schema.zh.md)、[评测模式（eval schema）](appendix/eval-schema.zh.md) 与 [记忆/检索模式（memory/retrieval schema）](appendix/memory-retrieval-schema.zh.md) 中。

## 书籍

### 2026 年 5 月 14 日编辑质量检查（QA）

第一组出版就绪质量检查（QA）问题已经关闭：第 1 章的判断框架从表格改成了更适合 HTML/PDF 与纯文本抽取的文字块；变化较快的章节、参考来源页和最新进展页也更新了编辑审查日期。

为什么这很重要：外部阅读表面现在更少依赖表格渲染细节，也更清楚地说明了快速变化的智能体安全（agent-security）章节何时被复核。

### 第八部分：智能体系统生命周期

现在全书已经包含从软件开发生命周期到智能体开发生命周期（`SDLC→ADLC`）的迁移、变更管理、保障回路、供应链、退役、错位、行为评测、AI 原生（`AI-native`）可观测性与清单控制的完整内容。

为什么这很重要：现在这本书覆盖的不只是架构与上线，还覆盖了智能体系统发布后的生命周期管理。

### 第一到第五部分的生产轮廓更完整了

书里现在补上了更多连接架构、检索、执行和评测纪律的桥：

- 第一部分更明确地区分了运行时架构、训练层和产品表面；
- 第二部分加入了更清晰的提示注入（`prompt injection`）、越狱（`jailbreaking`）与动作幻觉（`action hallucination`）分类法；
- 第三部分加强了检索轮廓：语义鸿沟（`semantic gap`）、`HyDE`、RAG 优先（`RAG first`），以及持续预训练与 `SFT` 的区别；
- 第四部分补上了大工具目录、语义工具过滤（`semantic tool filtering`）和 MCP 主机/客户端/服务器（`MCP host/client/server`）角色的实践指导；
- 第五部分补强了延迟预算（`latency budget`）的产品视角，以及更实用的以 LLM 作为评审器（`LLM-as-a-judge`）表述。

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

- 审批与委派授权上下文（delegated authorization context）；
- 控制项与生命周期内的运行时控制检查（runtime-control inspection）；
- 生命周期工件；
- 会话导出与回放摘要（replay summaries）；
- 评测数据集导出；
- 带数据遮蔽（redaction）、遮蔽后摘要（redacted summaries）、回放保留（replay preservation）与模式版本控制（schema versioning）的追踪导出。

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

- 语义工具过滤（`semantic tool filtering`）；
- `HyDE` 与 RAG 和训练之间的取舍（`RAG vs training`）；
- 延迟预算（`latency budget`）与路由管线；
- 以 LLM 作为评审器（`LLM-as-a-judge`）与评审器校准；
- 提示注入（`prompt injection`）、越狱（`jailbreaking`）与动作幻觉（`action hallucination`）的区别。

为什么这很重要：这些新主题现在不只藏在单个章节里，也已经出现在读者真正会先打开的入口页上。

## 发布就绪度

### 发布前站点更干净了

面向出版的质量检查正在进行中，但还没有完全关闭。

已经完成：

- 草稿与规划页面已从发布站点和站点地图（sitemap）中排除；
- 添加了 OpenGraph/Twitter 元数据和社交预览图；
- 检查了搜索索引、站点地图（sitemap）、robots 文件、本地资源、锚点、图片替代文本（alt text）和外部链接；
- 基础导航和规范备用重定向（canonical fallback redirects）已覆盖人们最容易手动复制的主要入口；
- 公共链接可用性记录已在 2026 年 5 月 20 日刷新，出版材料包（publisher packet）中的九个链接全部返回 HTTP 200；
- 出版材料包（publisher packet）的阻塞项登记表、豁免/决策日志、行长限制与材料包标签（packet labels）现在都适合打印和导出；
- 第 VIII 部分角色图现在适合打印和导出；
- 三种语言的 README 都加入了面向 `main` 与 `docs-prod` 的快速同步发布检查清单。

在称为出版就绪之前，仍然需要完成深层 EN/ZH 清理、独立 HTML/PDF/导出质量检查（QA）、样章打磨，以及面向具体出版社的纸质稿件/在线配套材料包装。

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
