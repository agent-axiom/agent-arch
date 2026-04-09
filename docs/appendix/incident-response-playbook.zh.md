# 智能体系统事故响应手册

当团队已经具备 traces、policy gates、approval paths 与 rollout rules，但还没有一条简明的事故处置路径时，这份手册就有用了。

它不替代关于 assurance、observability 或 change management 的章节。它把这些内容收束成一条可以执行的响应路径。

## 1. 什么算事故

对智能体系统来说，事故通常不只是宕机或质量下降，还包括：

- 在缺少必要审批路径时产生不可逆的 side effect；
- policy bypass 或错误的 gateway decision；
- 向未批准外部系统发起危险 egress；
- memory contamination 或错误的 persistent write；
- 绕过 evals 或 rollout gates 的 rollout escape；
- 可疑自治行为、类似破坏的行为，或试图隐藏动作的情况。

## 2. 前 15 分钟

前几分钟的目标不是完成全部 root-cause analysis，而是先控制影响并保留 evidence。

最小动作顺序通常是：

1. 停止或收窄 risky path。
2. 固定 trace 与 session 上下文。
3. 判断是否已经发生外部 side effect。
4. 判断是否需要禁用 capability、principal 或 connector。
5. 记录事故发生时生效的 bundle 与 rollout wave。

## 3. 必须立刻保留的内容

如果这些工件没有在最初几分钟保留下来，incident review 很快就会退化成靠记忆回溯：

- `trace_id`
- `session_id`
- `agent_id`
- `tool_principal`
- `approval_id`，如果涉及 approval path；
- `bundle_id`
- `change_id`
- `rollout_wave`
- policy decision events；
- approval decision events；
- 被读取或修改的 memory records；
- `allowed_egress` 信息以及实际的 network path。

## 4. 快速遏制动作

好的事故响应依赖预先设计好的 containment actions：

- 禁用单个 capability，而不是停掉整个 runtime；
- 把高风险动作切换成 mandatory approval mode；
- 临时暂停 memory writes；
- 撤销 connector credential 或 tool principal；
- 停止当前 rollout wave；
- 启用更严格的 policy bundle。

如果这些动作不存在，incident response 很快就会变成“谁有权临时关掉什么”的争论。

## 5. 最小分诊分类

最好在一开始就把事故归入某一类：

- `policy_bypass`
- `unauthorized_side_effect`
- `dangerous_egress`
- `memory_contamination`
- `approval_failure`
- `eval_escape`
- `agentic_misalignment`

这些分类不仅适合写进工单，也适合回流到 eval datasets、rollout gates 与 postmortem discipline。

## 6. 在 traces 与 events 里先查什么

在第一轮调查里，团队最好尽快回答这些问题：

- 哪个 input 或 retrieved context 触发了 risky path；
- 哪个 policy decision 放行了它；
- 到底是哪一个 principal 执行了动作；
- 是否存在 approval request、denial 或 bypass；
- 哪些 memory records 被读写；
- 这次 run 使用的是哪个 artifact bundle；
- 这是单次 run，还是 session / rollout wave 中更大的模式。

如果 traces 无法回答这些问题，那问题就不只在事故本身，也在 observability layer。

## 7. 什么时候该回滚，什么时候局部修复

并不是每次事故都需要 full rollback。只有在下面这些前提成立时，局部处置才可靠：

- blast radius 已经清楚；
- risky path 可以被单独隔离；
- active bundle 可以准确定位；
- rollout wave 可以在没有隐藏依赖的情况下停止。

如果团队无法把受影响的 surface 与系统其他部分可靠分开，full rollback 更常见。

## 8. Postmortem 应该写进什么

一份有用的智能体系统 postmortem 通常包括：

- 当时生效的是哪个 artifact bundle；
- 哪个 change review 与 rollout gate 放行了这条 path；
- 缺了哪些 checks 或 evals；
- 哪些 detection rules 没有生效；
- 采取了哪种 containment action；
- 接下来 policy、evals、rollout rules 或 inventory 要改什么。

好的 postmortem 不只是留下文档，还会更新 lifecycle artifacts。

## 9. 简短检查清单

- 能否快速禁用单个 capability？
- 能否恢复 `trace -> session -> bundle -> rollout wave`？
- 能否明确哪个 principal 执行了外部调用？
- approval path 及其 decision 是否可见？
- 能否临时暂停 memory writes？
- containment actions 的 owner 是否明确？
- incidents 是否会回流到 evals 与 rollout gates？

## 延伸阅读

- [Trace Schema 与 Event Catalog](trace-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](policy-bundle-schema.zh.md)
- [Approval Request 与 Decision Schema](approval-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](change-rollout-schema.zh.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.zh.md)
- [参考运行时包](reference-package.zh.md)
- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](../book/part-viii/chapter-21.zh.md)
- [第 23 章：Retirement、Replacement 与 End-of-Life Discipline](../book/part-viii/chapter-23.zh.md)
- [第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry](../book/part-viii/chapter-26.zh.md)
