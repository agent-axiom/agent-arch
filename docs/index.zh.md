# 安全 AI 智能体架构

这本书面向那些想构建真实生产级智能体系统的人，而不是只做一个看起来聪明的演示。

> 它以 Dmitry Vikulin 关于可靠 AI 智能体的文章为起点，进一步扩展为平台级视角：策略执行、人工审批、可观测性、评测体系、运维纪律与生命周期管理。

[从这里开始](start-here.zh.md){ .md-button .md-button--primary }
[查看全书计划](book/plan.zh.md){ .md-button }
[查看参考运行时](appendix/reference-package.zh.md){ .md-button }

<div class="book-cover" markdown="1">

![本书封面](assets/images/hero-home.png)

</div>

## 这本书适合谁

- 正在把智能体能力接入真实产品的工程师。
- 正在搭建共享运行时、策略、注册表、审批与可观测性层的平台团队。
- 需要看到信任边界与高风险执行路径的安全工程师。
- 更关心工程纪律而不是“智能体表演”的技术负责人和架构师。

## 你今天就能带走什么

- 一条从“先工作流后智能体”走向受控自治的实践路径。
- 关于策略层、审批、记忆、评测、可观测性与生命周期的章节。
- 一个可运行的参考运行时，包含会话导出、评测数据集导出、审批、控制项和生命周期工件。
- 一组参考页，覆盖追踪模式、评测模式、策略包、审批、发布门禁、记忆检索和生命周期工件。
- 可以直接复用的案例研究、检查清单和策略模板。

## 项目当前状态

- `Published core`：全书八个部分已经完整发布。
- `Expanding now`：入口页、参考层与站点导航仍在持续增强。
- `Reference assets available`：模式、检查清单、案例研究与可运行参考运行时已经可用。

## 三条实用阅读路径

### 如果你在做产品型智能体

1. [第 1 章：为什么智能体需要平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第 3 章：安全边界与信任边界](book/part-ii/chapter-3.zh.md)
3. [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
4. [第 13 章：离线评测、在线评测与回归门禁](book/part-v/chapter-13.zh.md)

### 如果你在做平台或基础设施

1. [第 2 章：安全智能体的参考架构](book/part-i/chapter-2.zh.md)
2. [第 4 章：工具网关、审批与审计轨迹](book/part-ii/chapter-4.zh.md)
3. [第 17 章：策略层与能力目录](book/part-vii/chapter-17.zh.md)
4. [第 20 章：智能体系统的变更管理](book/part-viii/chapter-20.zh.md)

### 如果你更关注安全、控制与运维

1. [第 21 章：保障闭环：红队演练、检测与响应](book/part-viii/chapter-21.zh.md)
2. [第 22 章：供应链、来源链与已批准工件](book/part-viii/chapter-22.zh.md)
3. [第 26 章：面向 AI 的可观测性、清单覆盖率与可检测遥测](book/part-viii/chapter-26.zh.md)
4. [第 27 章：智能体清单、注册表与蔓延控制](book/part-viii/chapter-27.zh.md)

## 这个项目已经具备什么

- 完整的 `ru / en / zh` 三语内容。
- 带有 `pytest` 覆盖的可运行 [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) 包。
- 一套完整的参考层，涵盖模式与契约页面。
- 包含案例、速查清单、术语表与路线图的实践型附录。

## 核心工程观点

智能体系统最常见的错误很简单：先追求自治，再补可控性。更稳妥的路径通常是：

1. 先构建**可预测的工作流**。
2. 再按局部、可度量的方式加入自治。
3. 所有高风险动作都经过**策略、审批与追踪**。
4. 用**评测、遥测与生命周期纪律**维持质量。

## 参考层在哪里

如果你需要的是可复用的工程产物，先看这些页面：

- [追踪模式与事件目录](appendix/trace-schema.zh.md)
- [评测数据集模式与评分契约](appendix/eval-schema.zh.md)
- [策略包模式与审批契约](appendix/policy-bundle-schema.zh.md)
- [生命周期工件模式](appendix/lifecycle-artifact-schema.zh.md)
- [记忆记录与检索契约模式](appendix/memory-retrieval-schema.zh.md)

## 继续阅读

[从这里开始](start-here.zh.md){ .md-button .md-button--primary }
[打开参考页面](appendix/trace-schema.zh.md){ .md-button }
[查看来源](appendix/sources.zh.md){ .md-button }
