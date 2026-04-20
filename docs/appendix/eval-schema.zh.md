# 评测数据集模式与分级契约

这一页继续扩展两个相邻主题：

- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
- [追踪模式与事件目录](trace-schema.zh.md)
- [Evidence Spine：从请求到 rollout judgment](../book/part-v/evidence-spine.zh.md)

并把它们和可运行参考包连接起来：

- [参考包](reference-package.zh.md)

如果追踪模式那一页回答的是“怎样描述一次运行里实际发生了什么”，这一页回答的就是“怎样把我们对系统的期待描述成评测工件”。

## 为什么需要显式的评测数据集模式

很多团队说自己“有评测”，但现实里常常只是：

- 一张手工表格，里面有几个例子；
- 一组互不相连的提示案例；
- 没有稳定结构的 JSON；
- 把标准答案、期望结果和评审意见混在一个字段里。

这会带来三个问题：

- 不同版本之间很难清晰比较；
- 回归门禁很难自动化；
- 追踪分级和数据集分级像两个互不相连的世界。

所以最好把评测数据集当成一种契约。

## 最小评测工件结构

对智能体系统来说，一个数据集条目至少最好包含：

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

## 为什么只有标签还不够

标签的作用是把场景分组：

- retrieval
- approval
- memory
- safety
- multi-turn

但标签本身并不告诉你，什么才算“成功行为”。

所以评测数据集通常应该把下面几层分开：

- `labels` 作为场景类别；
- `expected_outcomes` 作为期望结果；
- `grading_rules` 作为检查逻辑；
- `verifier_outputs` 作为结构化的分级结果，并包含 verifier identity 与 contract version。

## 什么是分级契约

分级契约的作用，是消除“这只是一个例子”和“这是明确的通过标准”之间的模糊地带。

在实践里，这意味着一个场景最好明确说明：

- 到底评哪些字段；
- 使用哪种检查类型；
- 什么算 pass/fail；
- 什么只是 warning，什么是 blocking failure。

好的分级契约应该能回答：

“如果明天换一个评审者或换一套 pipeline，对同一个 scenario 会不会得出同样的结论？”

## 常见的分级规则类型

对于参考级的智能体评测，至少可以先区分这些规则：

- `status_equals`
- `contains_substring`
- `max_tool_calls`
- `approval_required`
- `policy_violation_absent`
- `memory_write_absent`
- `process_score_present`
- `outcome_score_present`
- `failure_attribution_valid`
- `failed_run_traceable`

最后这一条会在 release review 开始要求 failed-run drills 时变得重要。它检查的不是一次退化路径有没有失败，而是这次失败是否仍然保留了可检查的 status、trace linkage 与受治理的 release identity。

也就是说，分级契约最好不要只盯着最终输出文本，也要检查系统行为。

## 它和 traces 的关系

一个很实用的模型是：

- 追踪模式描述实际运行行为；
- 评测数据集模式描述期望行为；
- 分级契约负责把两者对齐。

也正是在这里，可观测性才不只是“事后回看”，而开始参与发布决策。

## reference runtime 现在已经支持什么

在 `agent_runtime_ref` 里，这条命令：

```bash
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

已经会产出一个小型结构化 artifact，其中包含：

- 多个 session scenarios；
- `labels`；
- `expected_outcomes`。

它还不是完整的工业级评测框架，但已经足够作为：

- 回归分级的种子；
- scenario comparison 的基础；
- rollout review 的输入；
- 手工扩展评测集的起点。

## 生产级数据集模式还应该补什么

随着系统变得更严肃，模式最好继续补充这些字段：

- `dataset_version`
- `scenario_owner`
- `source_trace_ids`
- `grader_type`
- `blocking`
- `notes_for_review`
- `verifier_outputs`
- `failure_attribution`
- `verifier_id`
- `verifier_contract_version`
- `verifier_evidence_refs`

这样评测工件才会真正变成发布纪律的一部分，而不是临时 JSON。

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
verifier_outputs:
  verifier_id: fara-process-review
  verifier_contract_version: verifier-v2
  process_score: 0.92
  outcome_score: 0.35
  failure_attribution: uncontrollable_environment
  verifier_evidence_refs:
    - trace:trace_123
    - screenshot:step_7
```

重点在于，这个契约评估的不只是最终文本，也包括行为是否呈现出了正确的运行形态。

这对 long-horizon agents 尤其重要，因为二元 pass/fail verdict 往往会掩盖这样一种差异：一种是行为正确但 outcome 被环境阻断，另一种是行为不安全却碰巧拿到了 nominal success。

## 为什么 multi-run sessions 很重要

对智能体系统来说，一个评测条目往往不该只描述单次请求，而应该能描述一个短的相关步骤序列。

例如：

1. 用户先要求创建 ticket；
2. 然后再问 agent 记得哪些偏好；
3. 接着继续问下一步。

如果数据集无法表达这种序列，那你能测试单轮行为，却很难真正测试会话行为。

所以会话导出和评测数据集导出最好从一开始就一起设计。

## 不要这样做

下面这些错误非常常见：

- 把场景元数据和分级逻辑混在一个文本字段里；
- 只保留顺利路径；
- 不显式声明期望结果；
- 只评最终答案，不看策略或工具行为；
- 不给数据集做版本管理；
- 不把数据集条目和追踪证据或事故历史关联起来；
- 把 verifier output 压成一个薄弱的单一 verdict，没有 process/outcome split 和 failure attribution。

这样会让 eval culture 变得很脆弱。

## 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 每个场景是否都有稳定的 `scenario_id`？
- 标签和期望结果是否分开？
- 有没有分级规则，而不只是人工描述？
- 能不能评估行为，而不只是文本？
- verifier 能不能单独输出 `process_score`、`outcome_score` 和 `failure_attribution`？
- 能不能看出是哪一个 verifier identity 与 contract version 产出了这份 grading output？
- 支不支持多轮会话？
- 有没有数据集版本管理和负责人？

如果连续几个答案都是“没有”，那你现在更像是拥有一组例子，而不是拥有真正的评测数据集模式。

## 下一步做什么

- [追踪模式与事件目录](trace-schema.zh.md)
- [策略包模式与审批契约](policy-bundle-schema.zh.md)
- [生命周期工件规范](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
