# 智能体系统 Postmortem 模板

这个模板不是为了生成一份“好看”的文档，而是为了确保 incident review 最终会落到具体的 corrective actions、lifecycle updates 与 eval discipline 变化上。

最好在 containment phase 之后使用它，也就是 traces、approvals、rollout data 与 active bundle 都已经恢复出来之后。

## 1. 简要摘要

- `incident_id`：
- 日期与时间：
- Severity：
- Status：
- Owner：
- 事故摘要：

## 2. 发生了什么

- 参与的是哪个 agent 或 workflow：
- 哪个 user input、retrieved context 或 external trigger 启动了这条路径：
- 发生了什么 risky action 或 failure：
- 是否产生了真实 side effect：

这一节的目的，是简短且不带解释地固定事件链本身。

## 3. 当时哪些 artifacts 在生效

- `trace_id`：
- `session_id`：
- `bundle_id`：
- `change_id`：
- `rollout_wave`：
- `policy_bundle`：
- `approval_mode`：
- `tool_principal`：

如果这个部分很难快速补齐，问题就不只是 incident 本身，也在 observability 或 lifecycle layer。

## 4. Containment actions

- 最初几分钟采取了哪些动作：
- 哪些能力、路径或模式被禁用、收窄或转入 restricted mode：
- 是否需要 rollback：
- 是否撤销了 principals、connectors 或 capabilities：

这里最好区分：

- 临时遏制；
- 永久修正。

## 5. Root cause

- 事故的直接原因是什么：
- 哪些 contributing factors 放大了问题：
- 哪个 gate、review 或 assumption 失效了：
- 问题主要落在 policy、approvals、rollout、memory、observability 还是 inventory：

这一节应当通向系统性解释，而不是简单写成“模型出错了”。

## 6. Control layer 哪些地方失效了

- 哪个 policy decision 放过了 risky path：
- 是否存在 approval bypass、missing approval 或错误的 approval scope：
- 哪些 checks 或 evals 没有拦住问题：
- 哪些 detection rules 没有触发，或者触发得太晚：

这一节不仅要描述错误，还要描述缺失的 guardrail。

## 7. Blast radius

- 哪些 users、systems 或 data 受到了影响：
- 是否触达 external systems：
- 是否影响了 memory records：
- 这是单次 run，还是 rollout wave / session family 中更大的模式：

## 8. Corrective actions

对每个动作，最好固定：

- 动作本身；
- owner；
- 截止时间；
- 会更新哪个 artifact。

常见 corrective actions 包括：

- update policy bundle；
- tighten approval mode；
- update eval dataset；
- add targeted regression；
- update rollout gate；
- retire capability or principal；
- update registry record；
- add detection rule。

## 9. Lifecycle artifacts 要更新什么

- 如果需要 correction release，新的 `change_id` 是什么：
- 如果 release configuration 变了，新的 `bundle_id` 是什么：
- 是否需要新的 `retirement_plan`：
- 是否需要更新 registry 或 inventory：
- 是否需要调整 incident taxonomy 或 postmortem rubric：

这一节的价值在于把 postmortem 连接到可治理的 artifacts，而不仅仅是任务系统里的待办项。

## 10. Evals 与 rollout 要更新什么

- 哪些案例应进入 eval dataset：
- 要补哪些 behavioral 或 control evals：
- rollout gate criteria 是否需要调整：
- canary scope 或 approval threshold 是否需要修改：

如果 incidents 不回流到 evals 和 rollout rules，团队往往会重复同一类故障。

## 11. YAML 简版模板

```yaml
postmortem:
  incident_id: inc-2026-04-09-001
  severity: sev2
  owner: platform-operations
  active_artifacts:
    trace_id: trace-2026-04-09-001
    session_id: session-2026-04-09-001
    bundle_id: bundle-2026-04-07-a
    change_id: chg-2026-04-07-001
    rollout_wave: canary
  root_cause:
    primary: approval_scope_too_broad
    contributing:
      - missing_targeted_eval
      - stale_rollout_gate
  corrective_actions:
    - owner: platform-safety
      action: tighten_approval_policy
      due: 2026-04-12
    - owner: runtime-team
      action: add_regression_eval
      due: 2026-04-13
  lifecycle_updates:
    change_id: chg-2026-04-09-003
    bundle_id: bundle-2026-04-09-b
```

## 12. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- Postmortem 里是否有精确的 `incident_id`？
- 是否恢复了 `trace_id`、`session_id`、`bundle_id` 与 `change_id`？
- 是否写明了 contributing factors，而不只是 root cause？
- 是否记录了 control gaps？
- 是否给出了带 owner 和截止时间的 corrective actions？
- 是否明确了要更新哪些 lifecycle artifacts？
- Incident 是否回流到了 evals 与 rollout criteria？

## 下一步做什么

- [智能体系统事故响应手册](incident-response-playbook.zh.md)
- [Incident Record 与 Postmortem Linkage Schema](incident-record-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](change-rollout-schema.zh.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.zh.md)
- [智能体 registry 与 inventory 运维手册](registry-operations-handbook.zh.md)
- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](../book/part-viii/chapter-21.zh.md)
