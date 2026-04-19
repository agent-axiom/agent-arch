# 第五部分：可靠性与可观测性

到这里，我们已经有了架构、安全边界、记忆层和执行层。接下来，同一个支持智能体会进入下一阶段：光把它设计出来、上线出去已经不够，还要能在真实运行中稳稳地掌控它。

这一部分继续沿着同一条故事线推进：

- 在[第 11 章](chapter-11.zh.md)里，还原一次真实故障的原始路径；
- 在[第 12 章](chapter-12.zh.md)里，明确什么才算系统的 health budget 与 risk budget；
- 在[第 13 章](chapter-13.zh.md)里，产出 reviewable judgments，避免同类故障再次回到 rollout。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 11 章](chapter-11.zh.md)：先捕获一次真实故障的 raw run history；
    - [第 12 章](chapter-12.zh.md)：再定义系统允许消耗的 health budget 与 risk budget；
    - [第 13 章](chapter-13.zh.md)：最后把系统行为变成可供 rollout 使用的 reviewable eval judgments。

    这三步合在一起，说明 agent system 要通过三个不同层次从“某些东西能跑”走向受控运营：capture、health 与 judgment。

    它们也为本书接下来的一个关键补强做准备：单独的 Evidence Spine 页面，会把 request、policy、approval、traces、evals、incidents 与 rollout 连成一条统一的运行记录。

如果没有好的可观测性，再强的架构也会很快退化成猜测：

- 为什么某个 run 变贵了；
- 工作流到底在哪一层坏掉了；
- 哪个策略门禁触发了；
- 是哪个工具给出了坏结果；
- 为什么用户会收到这个具体回答。

这一部分会拆解如何构建追踪、SLO 和评测闭环，让智能体系统不只是“能上线”，而是真正可以在第一版演示之后继续稳定运营。

这里的 editorial boundary 也很重要。Tracing 是 raw capture layer；SLO 是 health-and-budget layer；evals 是 judgment layer。后面的章节会在这些基础之上继续展开 assurance、observability 与 governance，而不是过早把它们混成一团。

## 这一部分解决什么问题

这一部分向读者给出三个不同的承诺：

- 读完第 11 章后，你应该能还原真实的 run 路径，而不是只靠症状猜测；
- 读完第 12 章后，你应该能通过 SLO、cost、safety 和 escalation 说清楚明确的 health budgets 与 risk budgets；
- 读完第 13 章后，你应该能通过 offline evals、online signals 和 regression gates 产出 reviewable judgments。

## 本部分内容

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)
- [Evidence Spine：从请求到 rollout judgment](evidence-spine.zh.md)

## 这一部分之后去哪里

读完这一部分，接下来其实有两个自然步骤。

第一，本书需要一页单独的 Evidence Spine，让读者看清 traces、policy decisions、approvals、evals、incidents 与 rollout judgments 如何被维持成同一条运行记录。

第二，才是组织模型：谁拥有平台，谁拥有质量目标，以及谁来决定 rollout 能不能继续扩大。

这也是为什么 Part VI 会自然接在 Part V 后面。只要你已经能够捕获行为、定义可容忍的 budgets，并对 changes 做出 judgments，下一个问题就会变成 ownership：在真实组织里，究竟由谁来为这些承诺负责。
