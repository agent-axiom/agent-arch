# 评测数据集 Schema 与打分契约

这一页继续扩展两个相邻主题：

- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
- [追踪模式与事件目录](trace-schema.zh.md)
- [Evidence Spine：从请求到发布判断](../book/part-v/evidence-spine.zh.md)

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

## 把评测完整性作为一等控制

OpenAI 对 SWE-Bench Pro 的审计说明了为什么只有这个契约还不够：即使是很真实的 benchmark，如果任务本身坏了，也会产生噪声信号。[OpenAI 发现](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)，自动管线把 731 个 public split 任务中的 200 个标为损坏，而每个任务由五位资深工程师参与的人类标注活动识别出 249 个损坏任务。用本书的语言说，eval artifact 本身也需要质量保证，因为它会影响部署安全、研究优先级和 safety case 的论证。

最小缺陷分类可以直接进入 schema：

- `overly_strict_tests`：隐藏测试要求 prompt 没有要求的特定实现；
- `underspecified_prompt`：prompt 漏掉了 oracle 后续强制检查的要求；
- `low_coverage_tests`：测试覆盖不足，让不完整解法也能通过；
- `misleading_prompt`：prompt 指向的行为与测试或 gold patch 冲突。

因此，`verifier_outputs` 旁边还应该有独立的 `eval_audit_record`。它描述的不是智能体在某个场景里的表现，而是这个测量工件本身是否可靠：`source_task_id`、`oracle_type`、`defect_labels`、`agent_audit_refs`、`human_reviewer_count`、`human_agreement`、`reviewer_confidence` 和 `decision_impact`。

这里的实用模式不是“让 agent 给 eval 打分”。更可靠的形态是 **agent-assisted eval audit + independent human adjudication**：agent 帮助规模化检查 prompt、tests、traces 和 patches，但最终标签、置信度和对发布决策的影响仍然是一个独立的人类审查工件。

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
- `stop_condition_verified`
- `delegation_budget_respected`
- `single_vs_multi_agent_regression`

`failed_run_traceable` 会在发布评审开始要求失败运行演练时变得重要。它检查的不是一次退化路径有没有失败，而是这次失败是否仍然保留了可检查的状态、具体失败原因，例如 `failure_reason` 字段、追踪链接与受治理的发布身份。

`sandbox_profile_review` 对由沙箱（sandbox）支撑的路径很重要：它检查工作区物化（workspace materialization）、shell/文件系统权限（shell/filesystem permissions）、网络/密钥姿态（network/secrets posture）与快照/恢复策略（snapshot/resume policy）是否被显式表示成可评审证据，而不是停留为隐含的运行时设置（runtime settings）。

`stop_condition_verified` 用于那些不能只靠自由文本“完成”来接受结果的 agent-run paths。它检查场景是否带有明确 stop condition、verification mechanism、verification result、verifier actor，以及测试输出、trace、screenshot、diff 或其他 artifact 等 evidence link。

`delegation_budget_respected` 用于 manager/subagent paths。它检查 fanout 是否通过明确 gate，`subagent_count` 是否未超限，`context_handoff_size` 和 `token_budget` 是否仍在场景边界内，以及 `delegation_reason` 是否解释了为什么 single-agent path 不够。

`single_vs_multi_agent_regression` 用于比较模式。它检查 multi-agent 是否真的在 read-heavy breadth-first 工作中胜出，并且在 write-heavy shared-state 工作中因冲突动作、approvals、上下文丢失或 `merge_conflict_risk` 增长而失败或被拦截。

也就是说，分级契约最好不要只盯着最终输出文本，也要检查系统行为。

## 它和追踪的关系

一个很实用的模型是：

- 追踪模式描述实际运行行为；
- 评测数据集模式描述期望行为；
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

打包导出契约（Bundled export contract）是有意保持具体的。会话评测配置验证（Session eval config validation）也会用 `Session eval specs must be a mapping`、`Session eval spec must be a mapping`、`Session eval spec key must be a string`、`Session eval spec key must not be empty` 和 `Session eval spec keys must be unique` 把畸形评测规格（malformed eval specs）与失败的评测结果（failed eval results）区分开。

导出契约（Export contract）有意保持具体：默认 `dataset_name` 是 `agent-runtime-ref-eval-seed`；顶层摘要（top-level summary）包含 `session_count`、`session_ids`、`run_count`、`failed_runs`、`traceable_failed_runs`、`trace_ids`、`failed_trace_ids`、`idempotency_keys`、`approval_ids`、`approval_capability_names`、`pending_approval_ids`、`pending_approval_capability_names`、`approval_status_counts` 和 `latest_failure_reason`；审批支撑场景（approval-backed scenarios）也会在 `expected_outcomes` 中携带 `approval_status_counts`。内置场景（built-in scenarios）把已知的分派前失败与未知外部副作用分开：`failed_run_timeout` 证明分派前失败及其可追踪性，独立的 `unknown_effect_reconciliation` 产生 `side_effect_unknown`，期望一条 `reconciliation_runs` 记录，并承载 `duplicate_ticket_eval_passed` 标签（label）、`max_ticket_side_effects: 1` 限制和阻断型（blocking）`duplicate_ticket_guard` 打分规则（grading rule）。`profile_memory` 使用标签（labels）`memory_read`、`profile_lookup` 和 `grounded_answer`；`mixed_session` 使用 `multi_run`、`approval_then_memory`、`session_evals` 和 `required_run_count`；`support_ticket` 使用 `sandbox_profile_review`，并把 `sandbox_profile_reviewed` 作为预期结果（expected outcome）。

!!! example "重复工单线索的评测门禁（eval gate）"
    对于贯穿的支持分诊（support-triage）案例，应该有一个专门评测（eval）复现 `create_ticket` 之后的超时，要求保留 `trace_id` 与 `idempotency_key`，期望恰好一个工单副作用或一次 `side_effect_unknown` 停止；如果新的提示词/模型/适配器（prompt/model/adapter）版本盲目重试并创建第二个工单，就阻断发布（rollout）。

!!! example "上下文压缩连续性矩阵"
    每个长程场景都运行两次：一次使用完整历史，一次通过[上下文连续性信封](continuity-envelope-schema.zh.md)。用 `summary_sha256` 绑定压缩视图，并要求压缩后的安全判断相同或更严格。阻断变体必须覆盖用户否定约束、被修改的摘要、过期或撤销的审批、策略与能力版本变化、租户或主体漂移、未完成义务以及 `side_effect_unknown`。如果压缩路径直接授权、重试结果未知的写入，或无法把 `context_compaction` 关联到 `context_rehydration` 或 `continuity_validation_failed`，评测即失败。

!!! note "规范评测案例（Canonical eval cases）"
    评测数据集（eval dataset）不应该只覆盖重复工单回归（duplicate-ticket regression）。**支持分流（Support triage）** 检查审批门禁（approval gates）、幂等证据（idempotency evidence）、重试行为（retry behavior）和重复工单恢复（duplicate-ticket recovery）。**内部知识助手（Internal knowledge assistant）** 检查检索新鲜度（retrieval freshness）、来源归因（source attribution）、记忆来源（memory provenance）、访问控制（access control）和有依据回答质量（grounded answer quality）。**事件协调（Incident coordination）** 检查升级时序（escalation timing）、通知副作用（notification side effects）、响应归属（response ownership）、交接质量（handoff quality）和事件后学习回归（post-incident learning regressions）。

它还不是完整的工业级评测框架，但已经足够作为：

- 回归分级的种子；
- 场景对比的基础；
- 发布评审的输入；
- 手工扩展评测集的起点。

## 生产级数据集模式还应该补什么

随着系统变得更严肃，模式最好继续补充这些验证器裁决记录（verifier verdict record）字段：

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
- `stop_condition`
- `verification_command`
- `verification_result`
- `verifier_actor`
- `evidence_refs`
- `eval_audit_record`
- `oracle_type`
- `defect_labels`
- `agent_audit_refs`
- `human_reviewer_count`
- `human_agreement`
- `reviewer_confidence`
- `decision_impact`

这样评测工件才会真正变成发布纪律的一部分，而不是临时 JSON。

### 验证器裁决验收条件（Verifier verdict acceptance criteria）

只有通过下面几项检查，验证器裁决才算契约，而不是评审者的一段意见：

- 它有稳定的 `verdict_id`、`verifier_id` 与 `verifier_contract_version`；
- 输入（`input_refs`）和证据（`verifier_evidence_refs` 或 `evidence_refs`）指向追踪、场景和策略版本；
- `process_score`、`outcome_score` 与 `failure_attribution` 分开记录，而不是压成一个标签；
- `blocking_decision`、`comparison_baseline` 与 `reviewer_override` 解释发布是阻断、警告还是放行；
- `stop_condition`、`verification_command`、`verification_result` 与 `verifier_actor` 记录运行结束是如何被检查的。

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
  - type: stop_condition_verified
    expected:
      stop_condition: no duplicate ticket side effect after timeout replay
      verification_command: .venv/bin/pytest tests/test_docs_surface.py
      verification_result: pass
      verifier_actor: deterministic_gate
      evidence_refs:
        - trace:trace_123
        - artifact:pytest-output
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
- 不审计任务、oracle 和 hidden tests 本身的质量；
- 不把数据集条目和追踪证据或事故历史关联起来；
- 把验证器输出压成一个薄弱的单一判断，没有过程/结果拆分和失败归因；
- 在发布（rollout）中要求 `sandbox_profile_review`，却没有打分规则（grading rule）去检查工作区（workspace）、权限（permissions）与快照/恢复证据（snapshot/resume evidence）。
- 允许智能体在没有 `stop_condition_verified`、也没有会话后可检查证据的情况下结束任务。

这样会让评测文化变得很脆弱。

## 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 每个场景是否都有稳定的 `scenario_id`？
- 标签和期望结果是否分开？
- 有没有分级规则，而不只是人工描述？
- 能不能评估行为，而不只是文本？
- 是否有 `eval_audit_record`，记录 defect labels、oracle type、reviewer confidence 和 decision impact？
- 验证器能不能单独输出 `process_score`、`outcome_score` 和 `failure_attribution`？
- 能不能看出是哪一个验证器身份与契约版本产出了这份打分输出？
- 是否有专门面向由沙箱（sandbox）支撑的路径的规则，用来检查沙箱配置文件契约（sandbox profile contract）、工作区条目（workspace entries）、权限（permissions）与快照/恢复证据（snapshot/resume evidence）？
- 是否有规则在接受运行结束前检查停止条件、验证命令/结果、验证器角色与证据引用？
- 支不支持多轮会话？
- 有没有数据集版本管理和负责人？

如果连续几个答案都是“没有”，那你现在更像是拥有一组例子，而不是拥有真正的评测数据集模式。

## 下一步做什么

- [追踪模式与事件目录](trace-schema.zh.md)
- [策略包模式与审批契约](policy-bundle-schema.zh.md)
- [生命周期工件模式](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
