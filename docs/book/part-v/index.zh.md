# 第五部分：可靠性与可观测性

到这里，我们已经有了架构、安全边界、记忆层和执行层。现在问题变了：系统上线之后，怎样在它已经会犯错、会变贵、会漂移、也会在顺利路径之外出故障的情况下继续管理它？

这一部分回答三个很实际的问题：

- 怎样还原一次运行的真实路径；
- 怎样定义系统的健康与可接受风险；
- 怎样把系统行为变成发布可以依赖的判断。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 11 章](chapter-11.zh.md)：还原一次真实故障的原始历史；
    - [第 12 章](chapter-12.zh.md)：定义健康预算与风险预算；
    - [第 13 章](chapter-13.zh.md)：把系统行为变成可评审判断；
    - [Evidence Spine](evidence-spine.zh.md)：看清这些层怎样汇成一条运营记录。

!!! note "第五部分规范案例路线（Part V canonical case routes）"
    在可靠性/可观测性层（reliability/observability layer）中，三个规范案例（canonical cases）需要不同证据路线（evidence routes）。**支持分诊（Support triage）** 检查工单写入（ticket writes）的追踪覆盖（trace coverage）、重复工单回归（duplicate-ticket regression）和审批路径证据（approval-path evidence）。**内部知识助手（Internal knowledge assistant）** 检查检索质量（retrieval quality）、来源锚定判断（source-grounding judgment）、新鲜度预算（freshness budget）和记忆来源证据（memory-provenance evidence）。**事故协调（Incident coordination）** 检查升级延迟（escalation latency）、通知送达（notification delivery）、响应归属（response ownership）和事件后发布判断（post-incident rollout judgment）。

<div class="book-cover" markdown="1">

![可靠性与可观测性部分的封面](../../assets/images/part-v.png)

</div>

## 这一部分解决什么问题

- 读完第 11 章后，你应该能还原运行的路径，而不是靠症状猜测；
- 读完第 12 章后，你应该能用延迟、成本、安全和升级处理来表达健康预算与风险预算；
- 读完第 13 章后，你应该能对质量和回归风险产出可评审判断；
- 读完 Evidence Spine 后，你应该能看清追踪、策略、审批、评测和发布如何被串成一条可核查的链。

## 本部分内容

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)
- [Evidence Spine：从请求到发布判断](evidence-spine.zh.md)

## 这一部分之后去哪里

一旦系统已经能捕获行为、定义预算并产出判断，下一个问题就会变成负责人机制。这也是为什么这一部分后面自然接上[第六部分](../part-vi/index.zh.md)：在真实组织里，究竟由谁来持有这些承诺？
