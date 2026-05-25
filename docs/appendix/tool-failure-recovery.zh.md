# 智能体系统的工具失败恢复模式

工具错误很少只是一个简单的 `error`。更常见的是团队会进入更麻烦的状态：

- 副作用是否发生无法确认；
- 部分成功；
- 过期的对账结果；
- 一次比原始错误更危险的重复调用。

因此，智能体系统最好拥有显式的恢复模式层，而不是把所有问题都压成重试策略。

## 1. 为什么工具失败恢复应该单独存在

当执行路径失败时，最自然的冲动往往是“再试一次”。但不同工具的后果完全不同：

- 读取工具通常更安全地可重试；
- 写入工具可能制造重复副作用；
- 连接器可能已经完成动作，却没返回确认；
- 下游系统也可能停在中间状态。

这就是为什么恢复逻辑应该进入契约层。

## 2. 哪些结果类别最有用

一个最小可用的分类通常包括：

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_failure`
- `side_effect_unknown`
- `partial_side_effect`
- `manual_reconciliation_required`

如果执行层不区分这些状态，智能体几乎一定会做出过于粗糙的恢复决策。

## 3. 面对 `side_effect_unknown` 应该做什么

这是最危险的一类失败。

!!! note "规范恢复案例（Canonical recovery cases）"
    恢复分支（recovery branch）应该区分三个规范案例（canonical cases）的失败表面（failure surfaces）。**支持分流（Support triage）** 关注 `side_effect_unknown`、幂等性查找（idempotency lookup）、重复工单预防（duplicate-ticket prevention）、人工核对（manual reconciliation）和评测/发布回归（eval/rollout regression）。**内部知识助手（Internal knowledge assistant）** 关注陈旧检索（stale retrieval）、来源查找失败（source lookup failure）、拒绝访问恢复（access-denied recovery）、记忆写入回滚（memory write rollback）和有依据回答复查（grounded-answer recheck）。**事件协调（Incident coordination）** 关注通知部分送达（notification partial delivery）、升级重试（escalation retry）、负责人交接修复（owner handoff repair）、紧急回滚决策（emergency rollback decision）和事件后学习捕获（post-incident learning capture）。

比起天真重试，通常更合理的是：

- 检查外部系统中的当前状态；
- 用幂等键查找对象；
- 暂时把能力切进受限模式；
- 请求人工评审；
- 在追踪和事故记录中明确记录“不确定”。

核心目标很简单：在恢复状态之前，不要继续放大副作用。

## 4. 面对 `partial_side_effect` 应该做什么

这里的特点是：系统已经改变了外部世界，但没有完成干净收尾。

常见可用策略包括：

- 补偿动作，如果它是允许的；
- 显式的对账步骤；
- 停止并上抛部分完成状态；
- 创建后续任务，而不是静默重试。

关键点很简单：部分成功不是成功，但也不意味着可以安全地从头再来。

## 5. 什么时候恢复应该交给人

人工门禁特别适合这些情形：

- 副作用不可逆；
- 对账本身也有风险；
- 外部系统无法被可靠查询；
- 团队不确定哪一版载荷已被应用；
- 重试可能扩大影响半径。

也就是说，人类审批不只适用于初始动作，也适用于某些恢复路径。

## 6. 工具契约里适合放哪些字段

恢复质量很大程度上取决于执行层对工具契约了解多少。

最小有用字段通常包括：

- `idempotent`
- `retry_on`
- `reconcile_on_unknown`
- `requires_manual_recovery`
- `compensating_action`
- `external_lookup_key`

没有这些字段，恢复决策往往会变成临时处理。

## 7. 在追踪里应该能看到什么

在恢复评审时，团队最好能快速看到：

- 工具返回了什么状态；
- 是否发生了重试；
- 使用了哪个幂等键；
- 是否做过对账查询；
- 真正进入写入路径的载荷是什么；
- 最终恢复决策由谁做出。

如果追踪不能回答这些问题，恢复事故往往会调查得很慢。

## 8. 它和评测的关系

工具失败恢复最好显式进入评测数据集：

- 写入之后超时；
- 提交之后连接器断开；
- 重复的重试尝试；
- 需要后续处理的部分成功；
- 需要人工审批的恢复路径。

这很重要，因为很多严重的生产事故不是发生在顺利路径，而是发生在恢复分支。

## 9. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 执行层会区分 `retryable_failure` 和 `side_effect_unknown` 吗？
- 部分成功是否有明确的恢复路径？
- 追踪里能看到恢复决策吗？
- 是否存在默认禁止重试的工具？
- 评测数据集是否包含恢复分支？
- 危险恢复路径能要求人工评审吗？

## 下一步做什么

- [第 10 章：幂等性、重试、速率限制与回滚边界](../book/part-iv/chapter-10.zh.md)
- [追踪模式与事件目录](trace-schema.zh.md)
- [事故记录与事后复盘链接模式](incident-record-schema.zh.md)
- [智能体系统事故响应手册](incident-response-playbook.zh.md)
- [智能体系统事后复盘模板](postmortem-template.zh.md)
