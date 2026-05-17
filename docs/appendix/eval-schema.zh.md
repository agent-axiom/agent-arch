# 评测数据集 Schema 与打分契约

这一页继续扩展两个相邻主题：

- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [Evidence Spine：从请求到发布判断](../book/part-v/evidence-spine.zh.md)

并把它们和可运行参考包连接起来：

- [参考包](reference-package.zh.md)

如果追踪 Schema 那一页回答的是“怎样描述一次运行里实际发生了什么”，这一页回答的就是“怎样把我们对系统的期待描述成评测工件”。

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

- 检索
- 审批
- 记忆
- 安全
- 多轮

但标签本身并不告诉你，什么才算“成功行为”。

所以评测数据集通常应该把下面几层分开：

- `labels` 作为场景类别；
- `expected_outcomes` 作为期望结果；
- `grading_rules` 作为检查逻辑；
- `verifier_outputs` 作为结构化的打分结果，并包含验证器身份与契约版本。

## 什么是分级契约

分级契约的作用，是消除“这只是一个例子”和“这是明确的通过标准”之间的模糊地带。

在实践里，这意味着一个场景最好明确说明：

- 到底评哪些字段；
- 使用哪种检查类型；
- 什么算通过/失败；
- 什么只是警告，什么是阻断性失败。

好的分级契约应该能回答：

“如果明天换一个评审者或换一套流水线，对同一个场景会不会得出同样的结论？”

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
- `sandbox_profile_review`

`failed_run_traceable` 会在发布评审开始要求失败运行演练时变得重要。它检查的不是一次退化路径有没有失败，而是这次失败是否仍然保留了可检查的状态、具体失败原因，例如 `failure_reason` 字段、追踪链接与受治理的发布身份。

`sandbox_profile_review` 对由 sandbox 支撑的路径很重要：它检查 workspace materialization、shell/filesystem permissions、network/secrets posture 与 snapshot/resume policy 是否被显式表示成可评审证据，而不是停留为隐含的 runtime settings。

也就是说，分级契约最好不要只盯着最终输出文本，也要检查系统行为。

## 它和追踪的关系

一个很实用的模型是：

- 追踪 Schema 描述实际运行行为；
- 评测数据集 Schema 描述期望行为；
- 分级契约负责把两者对齐。

也正是在这里，可观测性才不只是“事后回看”，而开始参与发布决策。

## 参考运行时现在已经支持什么

在 `agent_runtime_ref` 里，这条命令：

```bash
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

已经会产出一个小型结构化工件，其中包含：

- 多个会话场景；
- `labels`；
- `expected_outcomes`；
- 一个单独的失败运行演练场景，它会在会话导出和评测期望里保留失败状态与 `failure_reason`。

Bundled export contract 是有意保持具体的。Session eval config validation 也会用 `Session eval specs must be a mapping`、`Session eval spec must be a mapping`、`Session eval spec key must be a string`、`Session eval spec key must not be empty` 和 `Session eval spec keys must be unique` 把 malformed eval specs 与 failed eval results 区分开。

Export contract 是有意保持具体的：默认 `dataset_name` 是 `agent-runtime-ref-eval-seed`；top-level summary 包含 `session_count`、`session_ids`、`run_count`、`failed_runs`、`traceable_failed_runs`、`trace_ids`、`failed_trace_ids`、`idempotency_keys`、`approval_ids`、`approval_capability_names`、`pending_approval_ids`、`pending_approval_capability_names`、`approval_status_counts` 和 `latest_failure_reason`；approval-backed scenarios 也会在 `expected_outcomes` 中携带 `approval_status_counts`；built-in scenarios 包括 `failed_run_timeout`（带 `duplicate_ticket_eval_passed` label、`max_ticket_side_effects: 1` 和 blocking `duplicate_ticket_guard` grading rule）、带有 `memory_read`、`profile_lookup` 与 `grounded_answer` labels 的 `profile_memory`、带有 `multi_run`、`approval_then_memory` 与 `session_evals` labels、并把 `required_run_count` 作为 expected outcome 的 `mixed_session`，以及带有 `sandbox_profile_review` label、`sandbox_profile_reviewed` expected outcome 和 blocking `sandbox_profile_review` grading rule 的 `support_ticket`。

!!! example "重复工单线索的 eval gate"
    对于贯穿的 support-triage 案例，应该有一个专门 eval 复现 `create_ticket` 之后的超时，要求保留 `trace_id` 与 `idempotency_key`，期望恰好一个工单副作用或一次 `side_effect_unknown` 停止；如果新的 prompt/model/adapter 版本盲目重试并创建第二个工单，就阻断 rollout。

!!! note "Canonical eval cases"
    Eval dataset 不应该只覆盖 duplicate-ticket regression。**Support triage** 检查 approval gates、idempotency evidence、retry behavior 和 duplicate-ticket recovery。**Internal knowledge assistant** 检查 retrieval freshness、source attribution、memory provenance、access control 和 grounded answer quality。**Incident coordination** 检查 escalation timing、notification side effects、response ownership、handoff quality 和 post-incident learning regressions。

它还不是完整的工业级评测框架，但已经足够作为：

- 回归分级的种子；
- 场景对比的基础；
- 发布评审的输入；
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
- `verdict_id`
- `verifier_id`
- `verifier_contract_version`
- `input_refs`
- `verifier_evidence_refs`
- `blocking_decision`
- `comparison_baseline`
- `reviewer_override`
- `sandbox_profile_contract`
- `workspace_manifest_ref`
- `snapshot_policy`

这样评测工件才会真正变成发布纪律的一部分，而不是临时 JSON。

## 打分契约示例

下面是一个针对失败运行演练场景的可工作骨架：

```yaml
scenario_id: failed_run_timeout
labels:
  - failed_run
  - tool_timeout
  - failure_drill
grading_rules:
  - type: status_equals
    expected: failed
    blocking: true
  - type: contains_substring
    expected: tool_timeout
    blocking: true
  - type: failed_run_traceable
    expected: true
    blocking: true
  - type: sandbox_profile_review
    expected:
      sandbox_profile_contract: sandbox-profile-v1
      workspace_entries_reviewed: true
      permissions_profile: restricted-shell-network-denied
      network_secrets_posture: network:denied,secrets:none
      snapshot_policy: required_on_completion
    blocking: true
verifier_outputs:
  verdict_id: verdict_failed_run_timeout_2026_05
  verifier_id: fara-process-review
  verifier_contract_version: verifier-v2
  input_refs:
    - scenario:failed_run_timeout
    - trace:trace_123
    - policy_bundle:policy-bundle-v3
  process_score: 0.92
  outcome_score: 0.35
  failure_attribution: uncontrollable_environment
  blocking_decision: warning_only
  comparison_baseline: release-2026-05-previous
  reviewer_override: none
  verifier_evidence_refs:
    - trace:trace_123
    - screenshot:step_7
```

重点在于，这个契约评估的不只是最终文本，也包括行为是否呈现出了正确的运行形态，以及具体失败条件是否仍然足够可见，便于后续审查。

这对长周期智能体尤其重要，因为二元通过/失败判断往往会掩盖这样一种差异：一种是行为正确但结果被环境阻断，另一种是行为不安全却碰巧拿到了名义上的成功。

## 为什么多运行会话很重要

对智能体系统来说，一个评测条目往往不该只描述单次请求，而应该能描述一个短的相关步骤序列。

例如：

1. 用户先要求创建工单；
2. 然后再问智能体记得哪些偏好；
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
- 把验证器输出压成一个薄弱的单一判断，没有过程/结果拆分和失败归因；
- 在 rollout 中要求 `sandbox_profile_review`，却没有 grading rule 去检查 workspace、permissions 与 snapshot/resume evidence。

这样会让评测文化变得很脆弱。

## 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 每个场景是否都有稳定的 `scenario_id`？
- 标签和期望结果是否分开？
- 有没有分级规则，而不只是人工描述？
- 能不能评估行为，而不只是文本？
- 验证器能不能单独输出 `process_score`、`outcome_score` 和 `failure_attribution`？
- 能不能看出是哪一个验证器身份与契约版本产出了这份打分输出？
- 是否有专门面向由 sandbox 支撑的路径的规则，用来检查 sandbox profile contract、workspace entries、permissions 与 snapshot/resume evidence？
- 支不支持多轮会话？
- 有没有数据集版本管理和负责人？

如果连续几个答案都是“没有”，那你现在更像是拥有一组例子，而不是拥有真正的评测数据集 Schema。

## 下一步做什么

- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [策略包 Schema 与审批契约](policy-bundle-schema.zh.md)
- [生命周期工件 Schema](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
