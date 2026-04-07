# 生命周期工件规范

这一页把生命周期工件的最小契约层放在一起：change record、approved artifact bundle 和 retirement plan。如果 trace schema 回答的是“发生了什么”，eval schema 回答的是“如何评估”，那 lifecycle artifact schema 回答的就是“到底有哪些东西被批准、变更、替换或退役了”。

## 1. 为什么需要它

生产级 agent system 里有几类东西，不能只放在团队脑子里或者 wiki 里：

- change records；
- 已批准工件包；
- retirement plans；
- replacement mappings；
- 运行期审批和生命周期决策。

没有这一层，change management 很快就会退化成口头协商。incident review 也会变成“到底是谁大概改了 policy 或 routing”的追溯游戏。

## 2. 核心实体

一个最小可用的生命周期层，围绕三个实体就够了：

- `change_record`
- `artifact_bundle`
- `retirement_plan`

这已经足够把 design review、release gate、assurance loop 和终止使用纪律串起来。

## 3. Change record

`change_record` 用来描述一个具体变更，以及它的 operational semantics。

最小字段可以是：

```yaml
kind: change_record
change_id: chg-2026-04-07-001
title: "Tighten outbound policy for ticket_write"
change_type: policy_update
risk_level: high
owner: platform-safety
affected_surfaces:
  - policy_bundle
  - capability_contract
  - rollout_rules
eval_requirements:
  - offline_regression
  - targeted_safety_eval
approval_requirements:
  - safety_review
  - platform_review
rollback_unit:
  - policy_bundle:v4
  - approvals_bundle:v3
status: approved
```

这里最关键的是：

- `affected_surfaces` 不允许团队假装这是一个“小改动”；
- `eval_requirements` 把 change management 直接连到 eval loop；
- `rollback_unit` 迫使团队提前想清楚到底回滚什么；
- `status` 是 operational fact，而不是流程摆设。

## 4. 已批准工件包

`artifact_bundle` 记录一组在某个发布配置下被认为可信、并且彼此兼容的工件。

```yaml
kind: artifact_bundle
bundle_id: bundle-2026-04-07-a
owner: platform-runtime
artifacts:
  model_route: gpt-5.4-tools
  policy_bundle: policy-v4
  approvals_bundle: approvals-v3
  controls_bundle: controls-v2
  capability_catalog: catalog-v5
  eval_dataset: eval-set-2026-04-07
status: approved
release_scope: canary
provenance:
  change_record: chg-2026-04-07-001
  reviewed_by:
    - safety-review
    - runtime-review
```

这一层的价值主要有两个：

- 它把“工件存在”与“工件被批准上线”分开；
- 它让 incident review 和 rollback 都更短、更明确。

## 5. Retirement plan

`retirement_plan` 不只是给整个 agent 下线用的。它同样适用于 capability、policy bundle 或工件族的受控替换。

```yaml
kind: retirement_plan
retirement_id: retire-2026-04-ticket-write-v1
target: capability:ticket_write_v1
trigger: deprecated_capability
replacement: capability:ticket_write_v2
phases:
  - freeze_new_rollouts
  - dual_run
  - traffic_shift
  - revoke_principal
  - archive_artifacts
historical_state:
  traces: retain_90_days
  approvals: retain_180_days
  memory: review_before_delete
status: planned
owner: platform-operations
```

它最有价值的地方，在于它逼着团队去考虑 replacement 之后还会留下什么：

- traces；
- approvals；
- principals；
- memory；
- 已归档的工件包。

## 6. 它和 Part VIII 的关系

这个 schema 直接支撑了几章核心内容：

- Chapter 20：change management；
- Chapter 21：assurance findings 作为生命周期输入；
- Chapter 22：approved artifacts 与 provenance；
- Chapter 23：replacement 与 retirement。

所以生命周期工件最好不要只写成纯文字文档，而应该作为可评审的 YAML 或 JSON 契约来管理。

## 7. 最小不变量

一个健康的生命周期工件层，至少应该保证：

- 每个 high-risk change 都有 `change_record`；
- 每次生产环境上线都指向一个 `artifact_bundle`；
- 每个已废弃工件都有 `retirement_plan` 或明确例外；
- 生命周期工件有 owner 和 version；
- incident review 能还原 `change -> bundle -> run -> retirement`。

## 8. 最常见的断裂点

常见问题通常很像：

- 工件包只存在于“大家默认知道”，却不是正式工件；
- change record 和 eval requirements 断开；
- retirement 只存在于 roadmap，没有落到 operational config；
- replacement 没有 dual-run semantics；
- historical state 没有 retention owner；
- provenance 只到 git commit，进不了 runtime 工件包。

## 9. 实用检查清单

你可以快速问自己：

- high-risk changes 是否有显式的 change records？
- 你是否真的有已批准工件包，而不是“最新几个 YAML 文件”？
- 出现 incident trace 时，你能反推出当时激活的 bundle 吗？
- deprecated capabilities 和 policy bundles 是否有 retirement plan？
- replacement 之后 archived state 是否还有 owner？
- 生命周期工件层面的 rollback unit 是否清晰？

如果连续几个问题的答案都是“否”，那说明你的 SDLC 和上线流程也许已经不错，但生命周期层还没有真正补齐。

## 延伸阅读

- [Trace Schema 与 Event Catalog](trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](eval-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](policy-bundle-schema.zh.md)
- [Reference Package](reference-package.zh.md)
- [Chapter 20. Agent Systems 的 Change Management](../book/part-viii/chapter-20.zh.md)
- [Chapter 22. Supply Chain、Provenance 与 Approved Artifacts](../book/part-viii/chapter-22.zh.md)
- [Chapter 23. Retirement、Replacement 与 End-of-Life Discipline](../book/part-viii/chapter-23.zh.md)
