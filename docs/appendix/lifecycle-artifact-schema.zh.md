# 生命周期工件规范

这一页把生命周期工件的最小契约层放在一起：变更记录、已批准工件包和退役计划。如果追踪模式回答的是“发生了什么”，评测模式回答的是“如何评估”，那生命周期工件规范回答的就是“到底有哪些东西被批准、变更、替换或退役了”。

它也直接连接到书里的 [Evidence Spine：从请求到 rollout judgment](../book/part-v/evidence-spine.zh.md)，因为生命周期工件本身就是后续 judgment 和 incident review 所依赖的那条受治理记录的一部分。

## 1. 为什么需要它

生产级智能体系统里有几类东西，不能只放在团队脑子里或者 wiki 里：

- 变更记录；
- 已批准工件包；
- 退役计划；
- 替换映射；
- runtime-control schemas 与 contract-version linkages；
- 运行期审批和生命周期决策；
- 当这些能力已进入 runtime contract 时，capability-session interruption、expiry 与 re-initialization rules；
- 当这些能力已进入 runtime contract 时，delegated authorization rules、principal-binding assumptions 与 revoke behavior；
- 当 release 或 assurance 依赖 verifier output 时，verifier contracts、grading rubrics 与 evidence-linkage rules。

没有这一层，变更管理很快就会退化成口头协商。事故复盘也会变成“到底是谁大概改了策略或路由”的追溯游戏。

## 2. 核心实体

一个最小可用的生命周期层，围绕三个实体就够了：

- `change_record`
- `artifact_bundle`
- `retirement_plan`

这已经足够把设计评审、发布门禁、保障闭环和终止使用纪律串起来。

## 3. Change record

`change_record` 用来描述一个具体变更，以及它的运行语义。

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
  - runtime_control_schema
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
- `eval_requirements` 把变更管理直接连到评测闭环；
- `rollback_unit` 迫使团队提前想清楚到底回滚什么；
- `status` 是运行事实，而不是流程摆设。

而一旦系统里已经存在 approval-bound 或 stateful capability sessions，change record 通常也应该能看出 interruption behavior、expiry handling、re-init semantics 与 delegated authorization rules 是否属于被审查的 surface。

## 4. 已批准工件包

`artifact_bundle` 记录一组在某个发布配置下被认为可信、并且彼此兼容的工件。在实践里，它同时也是赋予一次发布以受治理身份的契约表面。

```yaml
kind: artifact_bundle
bundle_id: bundle-2026-04-07-a
owner: platform-runtime
artifacts:
  model_route: gpt-5.4-tools
  policy_bundle: policy-v4
  approvals_bundle: approvals-v3
  controls_bundle: controls-v2
  runtime_control_schema: runtime-controls-v2
  capability_catalog: catalog-v5
  eval_dataset: eval-set-2026-04-07
  verifier_contract: verifier-v2
  contract_version: capability-contract-v5
status: approved
release_scope: canary
provenance:
  change_record: chg-2026-04-07-001
  reviewed_by:
    - safety-review
    - runtime-review
```

这一层的价值主要有三个：

- 它把“工件存在”与“工件被批准上线”分开；
- 它让发布身份变得可检查，而不是停留在隐式约定里；
- 它让事故复盘和回滚都更短、更明确。

而一旦 capability-session governance 已经进入显式管理，artifact bundle 通常也应该把和它一同被批准的 session-control assumptions 以及带有 verifier 约束的 contract family 说清楚，而不只是写一个 contract version：

- expiry policy；
- re-init policy；
- stuck 或 expired capability-session state 的 ownership；
- approval events 与 session events 之间应有怎样的 linkage；
- delegated authorization mode；
- principal-binding requirements；
- paused 或 in-flight actions 的 revoke behavior；
- 当 rollout 或 assurance 依赖 verifier judgments 时，verifier contract version、grading rubric 与 evidence-linkage expectations。

## 5. Retirement plan

`retirement_plan` 不只是给整个智能体下线用的。它同样适用于能力、策略包或工件族的受控替换。

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
  - expire_paused_runs
  - stop_background_routes
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

- 追踪；
- 审批；
- paused-run state；
- background-route ownership；
- 主体；
- 记忆；
- 已归档的工件包；
- 对审计或延迟 operator response 仍然有意义的 expired capability-session state。

## 6. 它和 Part VIII 的关系

这个 schema 直接支撑了几章核心内容：

- 第 20 章：变更管理；
- 第 21 章：保障发现结果作为生命周期输入；
- 第 22 章：已批准工件与来源证明；
- 第 23 章：替换与退役。

所以生命周期工件最好不要只写成纯文字文档，而应该作为可评审的 YAML 或 JSON 契约来管理。

## 7. 最小不变量

一个健康的生命周期工件层，至少应该保证：

- 每个高风险变更都有 `change_record`；
- 每次生产环境上线都指向一个 `artifact_bundle`；
- 每个 artifact bundle 都能作为具体的发布身份记录，而不只是松散的版本清单；
- 只要存在这些控制，每个 artifact bundle 都应关联 runtime-control schema 与 contract version；
- 当 release 或 assurance 依赖 graded outcomes 时，verifier contract lineage 与 contract-family identity 也必须可追溯；
- 每个已废弃工件都有 `retirement_plan` 或明确例外；
- 当存在这些路径时，retirement 或 replacement 必须说明 paused runs 和 expired capability-session state 会如何处理；
- 当这些控制存在时，delegated authorization ownership 与 revoke behavior 也必须能够对受影响 runs 被还原出来；
- 生命周期工件有负责人和版本；
- 事故复盘能还原 `change -> bundle -> run -> retirement`；
- 对 expired、paused 或 re-initialized capability paths 的 session-control ownership 也能被还原出来。

## 8. 最常见的断裂点

常见问题通常很像：

- 工件包只存在于“大家默认知道”，却不是正式工件；
- 变更记录和评测要求断开；
- 退役只存在于路线图，没有落到运行配置；
- 替换没有双运行语义；
- 历史状态没有保留负责人；
- 来源证明只到 git commit，进不了运行时工件包；
- replacement 发生时，paused-run 与 expired-session state 被遗忘，但 operator 其实还需要它们；
- verifier contract lineage 丢失了，尽管 rollout 或 assurance decisions 曾依赖它。

## 9. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 高风险变更是否有显式的变更记录？
- 你是否真的有已批准工件包，而不是“最新几个 YAML 文件”？
- 出现事故追踪时，你能反推出当时激活的工件包及其发布身份吗？
- 你能说清一次发布当时是在哪个带有 verifier 约束的 contract family 下被批准的吗？
- 已废弃能力和策略包是否有退役计划？
- 替换之后归档状态是否还有负责人？
- 生命周期工件层面的回滚单元是否清晰？

如果连续几个问题的答案都是“否”，那说明你的 SDLC 和上线流程也许已经不错，但生命周期层还没有真正补齐。

## 下一步做什么

- [追踪模式与事件目录](trace-schema.zh.md)
- [评测数据集模式与分级契约](eval-schema.zh.md)
- [策略包模式与审批契约](policy-bundle-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 20 章：智能体系统的变更管理](../book/part-viii/chapter-20.zh.md)
- [第 22 章：供应链、来源追踪与已批准工件](../book/part-viii/chapter-22.zh.md)
- [第 23 章：退役、替换与终止使用纪律](../book/part-viii/chapter-23.zh.md)
