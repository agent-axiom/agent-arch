# 第七部分：参考实现

到这里为止，我们已经按层搭建了同一套系统：

- 架构与信任边界；
- 记忆层；
- 执行层；
- 可观测性；
- 组织运行模型。

现在该把这些内容收拢成一个更完整的参考实现了。它不是“适用于所有场景的完美框架”，而是同一个支持智能体及其周边平台的一份实用蓝图，可以直接拿来作为起点继续演化。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 16 章](chapter-16.zh.md)：先看同一个 support agent 怎样收拢成一个统一的 runtime，而不是一堆分散的本地处理器；
    - [第 17 章](chapter-17.zh.md)：再看这个 runtime 怎样接入明确的策略层和能力目录；
    - [第 18 章](chapter-18.zh.md)：最后检查这套骨架是否已经能支撑有限发布和继续扩展。

    这三步合在一起，说明参考实现不是为了演示效果，而是为了把整套 production system 固定进代码里。

在这一部分里，我会逐步组装一个最小但成熟的平台：

- 基础 runtime；
- 安全与策略 hooks；
- capability 目录；
- telemetry 接线；
- 上线检查清单。

## 这一部分解决什么问题

- 把架构、记忆、执行与可观测性收拢成一个 runtime skeleton；
- 通过 policy layer 和 capability catalog 固定 contract core；
- 把 approval 与 governed capability access 变成 runtime 内显式行为，而不是旁路人工流程；
- 把这套骨架推进到 first rollout readiness；
- 把 Part VI 的 operating model 继续落实成可执行的 runtime 与 rollout shape。

也正是在这里，本书把前面那些抽象层真正落成 runnable system。它是前半本架构论证与后半本 lifecycle 论证之间的桥。

## 本部分内容

- [第 16 章：基础运行时蓝图](chapter-16.zh.md)
  这一章把同一个 support 场景推进到代码层：run loop 应该放在哪里，policy、memory 和 execution 怎样拆开，以及怎样避免逻辑散落在本地处理器里。
- [第 17 章：策略层与能力目录](chapter-17.zh.md)
  这一章把同一套骨架抬到契约层：哪些 capability 根本允许存在，哪里必须经过 approval，approval 的 pause/resume path 应该怎样工作，以及怎样避免把风险逻辑直接写死在 orchestration 里。
- [第 18 章：生产上线检查清单](chapter-18.zh.md)
  这一章用第一次受控 rollout 收束同一条故事线：support agent 是否已经能真正上线，approval/policy signals 是否可观测，以及在扩大范围前必须先看到什么。

## 这一部分之后去哪里

到这一部分，架构、安全、记忆、执行、可观测性和 approval control 已经能收拢成一个完整的运行骨架。但 production discipline 并不会在这里结束。

一旦同一个 agent 撑过第一次 rollout，接下来的问题就会自然分化成新的角色：

- change management 决定哪些 changes 属于 release-bearing；
- assurance 决定 drift 与 findings 出现后该如何 response；
- provenance 与 approved artifacts 保存实际部署内容的 evidence backbone；
- observability 从 runtime wiring 扩展成 estate 级的 evidence substrate；
- registry 与 governance 决定整个 estate 上的 accountability；
- retirement 在系统不应继续 active 时关闭整个 lifecycle。

这也是为什么参考实现之后，最自然的下一步就是 [第八部分：智能体系统生命周期](../part-viii/index.zh.md)。
