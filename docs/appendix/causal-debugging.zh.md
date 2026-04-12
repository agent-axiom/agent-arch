# 智能体系统中的 Causal Debugging 与 Root-Cause Analysis

当团队已经具备 traces、session summaries 和 incident records 后，下一个问题就不只是“哪里坏了”，而是“到底是什么导致了这个结果”。

普通日志回答的是“发生了什么”。Causal debugging 回答的是“哪个步骤、哪条边、哪种隐藏依赖真正把系统带到了坏结果”。

## 1. 为什么普通 tracing 还不够

在智能体系统中，一次长链路 run 可能同时包含：

- retrieval；
- model step；
- tool call；
- approval path；
- memory write；
- handoff 或 orchestration step。

如果团队把这些事件只当作一条平铺的时间线来读，就能看到顺序，但往往看不清：

- 哪个步骤真正起了决定作用；
- 哪个错误是 primary，哪个只是 secondary；
- 故障从哪里开始级联；
- 哪些现象是根因，哪些只是后果。

这就是普通 trace review 的上限。

## 2. 这里的 causal debugging 指什么

在实际工程里，causal debugging 通常意味着：

- 圈定 suspect path；
- 恢复事件之间的依赖关系；
- 把 trigger 与 downstream noise 分开；
- 找出真正能改变 outcome 的 corrective action。

这在 agent systems 中尤其重要，因为一次 risky run 可能带来：

- 多余的 tool call；
- 错误的 approval request；
- memory contamination；
- rollback；
- incident escalation；
- 有误导性的 postmortem conclusion。

## 3. 哪些节点几乎总是重要

即使是最小的 causal graph，通常也应该能表达：

- user input 或 external trigger；
- retrieved context；
- model decision；
- policy decision；
- approval event；
- tool execution；
- memory write；
- final outcome。

并不是每次 incident 都会涉及所有节点。但如果一张图连这些关系都表达不了，diagnosis 很快就会太粗。

## 4. 团队应该能问哪些问题

有用的 causal debugging 不是先画图，而是先问对问题：

- 哪个最初的步骤把 run 带进了 risky path；
- 哪个 decision 改变了 trajectory；
- policy gate 是根因，还是只是没能拦住问题；
- 哪个 tool call 是 trigger，哪个只是 cascade effect；
- 哪个 corrective action 能改变 root cause，而不是只压住 symptom。

如果问不出这些问题，root-cause analysis 很快就会滑向“模型表现异常”。

## 5. 它和 traces、structured events 的关系

Causal debugging 不替代 [Trace Schema 与 Event Catalog](trace-schema.zh.md)，它建立在其上。

好的 trace layer 已经提供：

- `trace_id`
- `session_id`
- event types；
- policy decisions；
- approval outcomes；
- tool execution；
- memory events。

但 causal debugging 还需要再往前走一步：把这些事件看成依赖网络，而不是简单的列表。

## 6. 哪些地方最容易出现“假原因”

常见陷阱包括：

- 团队把最后一个 failed tool call 当成根因，但真正 trigger 在 retrieved context；
- blame 落在 model step 上，但实际问题是 stale policy bundle；
- approval denial 被当成 failure，但它其实是正确的 containment behavior；
- noisy retries 掩盖了第一个 bad decision；
- memory write 看起来像 root cause，但它只是后期 side effect。

所以“最后一个奇怪事件”和“真正根因”通常不是一回事。

## 7. 做 root-cause analysis 时要保留什么

最小的 artifact 集通常包括：

- `trace_id`
- `session_id`
- `bundle_id`
- `change_id`
- `rollout_wave`
- active policy bundle；
- active approval mode；
- `tool_principal`；
- touched memory records；
- linked incident 或 postmortem id。

如果这些连接不存在，团队往往会花比修系统更长的时间去争论原因。

## 8. 它和 multi-agent reliability 的关系

在 multi-agent 场景里，causal debugging 更重要，因为系统里还会多出：

- handoff edges；
- delegated tasks；
- conflicting agent states；
- 节点之间模糊的责任边界。

这并不意味着每支团队都要做完整的 causal graph engine。但 orchestration 越复杂，就越需要能定位：

- coordination path 是在哪里断的；
- 哪次 handoff 丢了关键 context；
- 哪个 agent 才是真正的 source of failure。

## 9. Root-cause analysis 之后应该改什么

好的 root-cause analysis 通常应该落到这些变化之一：

- update policy bundle；
- add or tighten eval case；
- narrow capability exposure；
- refine approval scope；
- update rollout gate；
- fix retrieval filtering；
- pause 或 revise memory write path。

如果 diagnosis 最终没有落到 artifact updates，它也许有洞见，但 operational 价值不强。

## 10. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 团队能区分 trigger 和 cascade effects 吗？
- 团队能区分 bad decision 与正确的 containment 吗？
- traces 里能看见 policy、approval 与 tool edges 吗？
- active bundle 和 rollout wave 能恢复出来吗？
- 能明确哪种 corrective action 会改变 root cause 吗？
- 团队会不会把 root cause 简化成“模型失败了”而没有继续定位？

## 下一步做什么

- [Trace Schema 与 Event Catalog](trace-schema.zh.md)
- [Incident Record 与 Postmortem Linkage Schema](incident-record-schema.zh.md)
- [智能体系统 Postmortem 模板](postmortem-template.zh.md)
- [智能体系统事故响应手册](incident-response-playbook.zh.md)
- [第 11 章：追踪、跨度与结构化事件](../book/part-v/chapter-11.zh.md)
- [第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry](../book/part-viii/chapter-26.zh.md)
