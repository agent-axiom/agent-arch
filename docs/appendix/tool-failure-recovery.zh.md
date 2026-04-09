# 智能体系统的 Tool Failure Recovery Patterns

Tool 错误很少只是一个简单的 `error`。更常见的是团队会进入更麻烦的状态：

- side effect unknown；
- partial success；
- stale reconciliation；
- 一次比原始错误更危险的重复调用。

因此，智能体系统最好拥有显式的 recovery pattern layer，而不是把所有问题都压成 retry policy。

## 1. 为什么 tool failure recovery 应该单独存在

当 execution path 失败时，最自然的冲动往往是“再试一次”。但不同 tools 的后果完全不同：

- read tool 通常更安全地可重试；
- write tool 可能制造重复 side effects；
- connector 可能已经完成动作，却没返回确认；
- downstream system 也可能停在中间状态。

这就是为什么 recovery logic 应该进入 contract layer。

## 2. 哪些 outcome classes 最有用

一个最小可用的 taxonomy 通常包括：

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_failure`
- `side_effect_unknown`
- `partial_side_effect`
- `manual_reconciliation_required`

如果 execution layer 不区分这些状态，agent 几乎一定会做出过于粗糙的 recovery decisions。

## 3. 面对 `side_effect_unknown` 应该做什么

这是最危险的一类失败。

比起 naïve retry，通常更合理的是：

- 检查 external system 中的当前状态；
- 用 idempotency key 查找对象；
- 暂时把 capability 切进 restricted mode；
- 请求 human review；
- 在 traces 和 incident record 中明确记录“不确定”。

核心目标很简单：在恢复状态之前，不要继续放大 side effects。

## 4. 面对 `partial_side_effect` 应该做什么

这里的特点是：系统已经改变了外部世界，但没有完成 clean completion。

常见可用策略包括：

- compensating action，如果它是允许的；
- 显式的 reconciliation step；
- 停止并上抛 partial completion；
- 创建 follow-up task，而不是静默 retry。

关键点很简单：partial success 不是 success，但也不意味着可以安全地从头再来。

## 5. 什么时候 recovery 应该交给人

Human gate 特别适合这些情形：

- side effect 不可逆；
- reconciliation 本身也有风险；
- external system 无法被可靠查询；
- 团队不确定哪一版 payload 已被应用；
- retry 可能扩大 blast radius。

也就是说，人类审批不只适用于 initial action，也适用于某些 recovery paths。

## 6. Tool contract 里适合放哪些字段

Recovery quality 很大程度上取决于 execution layer 对 tool contract 了解多少。

最小有用字段通常包括：

- `idempotent`
- `retry_on`
- `reconcile_on_unknown`
- `requires_manual_recovery`
- `compensating_action`
- `external_lookup_key`

没有这些字段，recovery decisions 往往会变成 ad hoc 处理。

## 7. 在 traces 里应该能看到什么

在 recovery review 时，团队最好能快速看到：

- tool 返回了什么状态；
- 是否发生了 retry；
- 使用了哪个 idempotency key；
- 是否做过 reconciliation lookup；
- 真正进入 write path 的 payload 是什么；
- 最终 recovery decision 由谁做出。

如果 traces 不能回答这些问题，recovery incidents 往往会调查得很慢。

## 8. 它和 evals 的关系

Tool failure recovery 最好显式进入 eval dataset：

- write 之后超时；
- commit 之后 connector 断开；
- duplicate retry attempt；
- 需要后续处理的 partial success；
- 需要人工审批的 recovery path。

这很重要，因为很多严重的 production incidents 不是发生在 happy path，而是发生在 recovery branch。

## 9. 实用检查清单

- Execution layer 会区分 `retryable_failure` 和 `side_effect_unknown` 吗？
- partial success 是否有明确的 recovery path？
- traces 里能看到 recovery decision 吗？
- 是否存在默认禁止 retry 的 tools？
- eval dataset 是否包含 recovery branch？
- dangerous recovery path 能要求 human review 吗？

## 延伸阅读

- [第 10 章：幂等性、重试、速率限制与回滚边界](../book/part-iv/chapter-10.zh.md)
- [Trace Schema 与 Event Catalog](trace-schema.zh.md)
- [Incident Record 与 Postmortem Linkage Schema](incident-record-schema.zh.md)
- [智能体系统事故响应手册](incident-response-playbook.zh.md)
- [智能体系统 Postmortem 模板](postmortem-template.zh.md)
