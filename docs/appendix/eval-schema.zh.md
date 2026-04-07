# Eval Dataset Schema 与 Grading Contract

这一页继续扩展两个相邻主题：

- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
- [Trace Schema 与 Event Catalog](trace-schema.zh.md)

并把它们和可运行 package 连接起来：

- [参考包](reference-package.zh.md)

如果 trace schema 那一页回答的是“怎样描述一次 run 里实际发生了什么”，这一页回答的就是“怎样把我们对系统的期待描述成 eval artifact”。

## 为什么需要显式的 eval dataset schema

很多团队说自己“有 evals”，但现实里常常只是：

- 一张手工表格，里面有几个例子；
- 一组互不相连的 prompt cases；
- 没有稳定结构的 JSON；
- 把 ground truth、期望结果和评审意见混在一个字段里。

这会带来三个问题：

- 不同版本之间很难清晰比较；
- regression gates 很难自动化；
- trace grading 和 dataset grading 像两个互不相连的世界。

所以最好把 eval dataset 当成一种 contract。

## 最小 eval artifact 结构

对 agent systems 来说，一个 dataset item 至少最好包含：

- `scenario_id`
- `labels`
- `user_inputs`
- `expected_outcomes`
- `risk_class`

最小例子可以像这样：

```json
{
  "scenario_id": "support_ticket",
  "labels": ["write_path", "approval_required", "ticketing"],
  "user_inputs": [
    "Please create a ticket for this onboarding issue."
  ],
  "expected_outcomes": {
    "latest_status": "success",
    "approval_wait_runs": 1,
    "required_output_substrings": [
      "waiting for human approval"
    ]
  },
  "risk_class": "high"
}
```

这已经比“这里有一个示例提示词”有用得多。

## 为什么只有 labels 还不够

Labels 的作用是把 scenario 分组：

- retrieval
- approval
- memory
- safety
- multi-turn

但 labels 本身并不告诉你，什么才算“成功行为”。

所以 eval dataset 通常应该把下面几层分开：

- `labels` 作为场景类别；
- `expected_outcomes` 作为期望结果；
- `grading_rules` 作为检查逻辑。

## 什么是 grading contract

Grading contract 的作用，是消除“这只是一个例子”和“这是明确的通过标准”之间的模糊地带。

在实践里，这意味着一个 scenario 最好明确说明：

- 到底评哪些字段；
- 使用哪种检查类型；
- 什么算 pass/fail；
- 什么只是 warning，什么是 blocking failure。

好的 grading contract 应该能回答：

“如果明天换一个评审者或换一套 pipeline，对同一个 scenario 会不会得出同样的结论？”

## 常见的 grading rule 类型

对于 reference-grade 的 agent evals，至少可以先区分这些规则：

- `status_equals`
- `contains_substring`
- `max_tool_calls`
- `approval_required`
- `policy_violation_absent`
- `memory_write_absent`

也就是说，grading contract 最好不要只盯着最终输出文本，也要检查系统行为。

## 它和 traces 的关系

一个很实用的模型是：

- trace schema 描述实际 run behavior；
- eval dataset schema 描述期望 behavior；
- grading contract 负责把两者对齐。

也正是在这里，observability 才不只是“事后回看”，而开始参与 release decisions。

## reference runtime 现在已经支持什么

在 `agent_runtime_ref` 里，这条命令：

```bash
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

已经会产出一个小型结构化 artifact，其中包含：

- 多个 session scenarios；
- `labels`；
- `expected_outcomes`。

它还不是完整的工业级 eval framework，但已经足够作为：

- regression grading 的种子；
- scenario comparison 的基础；
- rollout review 的输入；
- 手工扩展 eval set 的起点。

## production dataset schema 还应该补什么

随着系统变得更严肃，schema 最好继续补充这些字段：

- `dataset_version`
- `scenario_owner`
- `source_trace_ids`
- `grader_type`
- `blocking`
- `notes_for_review`

这样 eval artifact 才会真正变成 release discipline 的一部分，而不是临时 JSON。

## grading contract 示例

下面是一个可工作的 skeleton：

```yaml
scenario_id: support_ticket
labels:
  - write_path
  - approval_required
grading_rules:
  - type: status_equals
    expected: success
    blocking: true
  - type: contains_substring
    expected: waiting for human approval
    blocking: true
  - type: approval_required
    expected: true
    blocking: true
```

重点在于，这个 contract 评估的不只是最终文本，也包括行为是否呈现出了正确的 operational shape。

## 为什么 multi-run sessions 很重要

对 agent systems 来说，一个 eval item 往往不该只描述单次请求，而应该能描述一个短的相关步骤序列。

例如：

1. 用户先要求创建 ticket；
2. 然后再问 agent 记得哪些偏好；
3. 接着继续问下一步。

如果 dataset 无法表达这种序列，那你能测试 single-turn behavior，却很难真正测试 session behavior。

所以 session exports 和 eval dataset exports 最好从一开始就一起设计。

## 不要这样做

下面这些错误非常常见：

- 把 scenario metadata 和 grading logic 混在一个文本字段里；
- 只保留 happy path；
- 不显式声明 expected outcomes；
- 只评最终答案，不看 policy 或 tool behavior；
- 不给 dataset 做 versioning；
- 不把 dataset items 和 trace evidence 或 incident history 关联起来。

这样会让 eval culture 变得很脆弱。

## 实用检查清单

如果你想快速判断自己的 eval artifact schema 是否足够成熟，可以问自己：

- 每个 scenario 是否都有稳定的 `scenario_id`？
- labels 和 expected outcomes 是否分开？
- 有没有 grading rules，而不只是人工描述？
- 能不能评估 behavior，而不只是文本？
- 支不支持 multi-run sessions？
- 有没有 dataset versioning 和 owner？

如果连续几个答案都是“没有”，那你现在更像是拥有一组例子，而不是拥有真正的 eval dataset schema。

## 延伸阅读

- [Trace Schema 与 Event Catalog](trace-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](policy-bundle-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
