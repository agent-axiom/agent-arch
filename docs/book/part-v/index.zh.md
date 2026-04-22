# 第五部分：可靠性与可观测性

到这里，我们已经有了架构、安全边界、记忆层和执行层。现在问题变了：系统上线之后，怎样在它已经会犯错、会变贵、会漂移、也会在 happy path 之外出故障的情况下继续管理它？

这一部分回答三个很实际的问题：

- 怎样还原一次 run 的真实路径；
- 怎样定义系统的健康与可接受风险；
- 怎样把系统行为变成 rollout 可以依赖的 judgments。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 11 章](chapter-11.zh.md)：还原一次真实故障的原始历史；
    - [第 12 章](chapter-12.zh.md)：定义 health budgets 与 risk budgets；
    - [第 13 章](chapter-13.zh.md)：把系统行为变成 reviewable judgments；
    - [Evidence Spine](evidence-spine.zh.md)：看清这些层怎样汇成一条运营记录。

<div class="book-cover" markdown="1">

![可靠性与可观测性部分的封面](../../assets/images/part-v.png)

</div>

## 这一部分解决什么问题

- 读完第 11 章后，你应该能还原 run 的路径，而不是靠症状猜测；
- 读完第 12 章后，你应该能用 latency、cost、safety 和 escalation 来表达 health budgets 与 risk budgets；
- 读完第 13 章后，你应该能对质量和回归风险产出 reviewable judgments；
- 读完 Evidence Spine 后，你应该能看清 traces、policy、approvals、evals 和 rollout 如何被串成一条可核查的链。

## 本部分内容

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)
- [Evidence Spine：从请求到 rollout judgment](evidence-spine.zh.md)

## 这一部分之后去哪里

一旦系统已经能捕获行为、定义 budgets 并产出 judgments，下一个问题就会变成 ownership。这也是为什么这一部分后面自然接上[第六部分](../part-vi/index.zh.md)：在真实组织里，究竟由谁来持有这些承诺？
