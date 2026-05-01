# 生命周期工件 Schema

这一页把生命周期工件的最小契约层放在一起：变更记录、已批准工件包和退役计划。如果追踪 Schema 回答的是“发生了什么”，评测 Schema 回答的是“如何评估”，那生命周期工件 Schema 回答的就是“到底有哪些东西被批准、变更、替换或退役了”。

它也直接连接到书里的 [Evidence Spine：从请求到发布判断](../book/part-v/evidence-spine.zh.md)，因为生命周期工件本身就是后续判断和事故评审所依赖的那条受治理记录的一部分。

## 1. 为什么需要它

生产级智能体系统里有几类东西，不能只放在团队脑子里或者内部知识库里：

- 变更记录；
- 已批准工件包；
- 退役计划；
- 替换映射；
- 运行时控制 Schema 与契约版本链接；
- 运行期审批和生命周期决策；
- 当这些能力已进入运行时契约时，能力会话中断、过期与重新初始化规则；
- 当这些能力已进入运行时契约时，委派授权规则、主体绑定假设与撤销行为；
- 当发布或保障依赖验证器输出时，验证器契约、打分准则与证据链接规则；
- 当长时间运行的工作跨越上下文重置或角色交接边界时，结构化交接工件。

没有这一层，变更管理很快就会退化成口头协商。事故复盘也会变成“到底是谁大概改了策略或路由”的追溯游戏。

## 2. 核心实体

一个最小可用的生命周期层，围绕三个实体就够了：

- `change_record`
- `artifact_bundle`
- `retirement_plan`

这已经足够把设计评审、发布门禁、保障闭环和终止使用纪律串起来。

## 3. 变更记录

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
  - capability_session_contract
  - sandbox_profile_contract
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

而一旦系统里已经存在审批绑定运行、有状态能力会话或由 sandbox 支撑的执行，变更记录通常也应该能看出中断行为、过期处理、重新初始化语义、委派授权规则以及 sandbox profile contract 是否属于被审查的表面。

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
  sandbox_profile: sandbox-profile-v1
  capability_catalog: catalog-v5
  eval_dataset: eval-set-2026-04-07
  verifier_contract: verifier-v2
  contract_version: capability-contract-v5
review_evidence:
  sandbox_profile_reviewed:
    trace_event: sandbox_profile_reviewed
    workspace_manifest_ref: runtime-controls.yaml#runtime_controls.sandbox_profile.workspace
    permissions_profile: restricted-shell-network-denied
    network_secrets_posture: network:denied,secrets:none
    snapshot_policy: required_on_completion
    review_evidence_refs:
      - trace:trace-sandbox-review-001
      - eval:sandbox_profile_review
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

而一旦能力会话治理已经进入显式管理，工件包通常也应该把和它一同被批准的会话控制假设以及带有验证器约束的契约族说清楚，而不只是写一个契约版本：

- 过期策略；
- 重新初始化策略；
- 卡住或过期的能力会话状态由谁负责；
- 审批事件与会话事件之间应有怎样的链接；
- 委派授权模式；
- 主体绑定要求；
- 已暂停或进行中动作的撤销行为；
- 当发布或保障依赖验证器判断时，验证器契约版本、打分准则与证据链接期望；
- 当 release identity 包含由 sandbox 支撑的执行时，sandbox profile review evidence，包括 `sandbox_profile_reviewed` trace event、`workspace_manifest_ref` 以及指向 eval/rollout evidence 的链接。

## 5. 退役计划

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

它最有价值的地方，在于它逼着团队去考虑替换之后还会留下什么：

- 追踪；
- 审批；
- 已暂停运行状态；
- 后台路径负责人；
- 主体；
- 记忆；
- 已归档的工件包；
- 记录迭代范围、评测者批评或重置边界决策的结构化交接工件；
- 对审计或延迟操作员响应仍然有意义的过期能力会话状态。

## 6. 它和第八部分的关系

这个 Schema 直接支撑了几章核心内容：

- 第 20 章：变更管理；
- 第 21 章：保障发现结果作为生命周期输入；
- 第 22 章：已批准工件与来源证明；
- 第 23 章：替换与退役。

所以生命周期工件最好不要只写成纯文字文档，而应该作为可评审的 YAML 或 JSON 契约来管理。

Reference runtime 在 `retirement.yaml` 中映射了这个结构：`system_id` 和 `replacement_mode` 标识 retiring surface，`triggers` 说明为什么启动 retirement，`required_steps` 包含 `freeze_rollout`、`disable_risky_capabilities`、`stop_memory_write`、`expire_paused_runs`、`stop_background_routes`、`freeze_reinitialization`、`revoke_egress`、`archive_audit_state` 和 `set_retired_status` 等 controls，而 `session_control_owner`、`emergency_freeze_owner` 与 `archive_targets` 明确保留 ownership 和 retained evidence。

## 7. 最小不变量

一个健康的生命周期工件层，至少应该保证：

- 每个高风险变更都有 `change_record`；
- 每次生产环境上线都指向一个 `artifact_bundle`；
- 每个工件包都能作为具体的发布身份记录，而不只是松散的版本清单；
- 只要存在这些控制，每个工件包都应关联运行时控制 Schema 与契约版本；
- 当发布或保障依赖打分结果时，验证器契约谱系与契约族身份也必须可追溯；
- 当 rollout 要求 `sandbox_profile_reviewed` 时，必须能从 bundle、trace 或 eval artifact 还原 sandbox profile review evidence；
- 每个已废弃工件都有 `retirement_plan` 或明确例外；
- 当存在这些路径时，退役或替换必须说明已暂停运行、交接工件和过期能力会话状态会如何处理；
- 当这些控制存在时，委派授权负责人和撤销行为也必须能够对受影响运行被还原出来；
- 生命周期工件有负责人和版本；
- 事故复盘能还原 `change_id→bundle_id→run_id→retirement_id`；
- 对过期、已暂停或重新初始化能力路径的会话控制负责人也能被还原出来。

## 8. 最常见的断裂点

常见问题通常很像：

- 工件包只存在于“大家默认知道”，却不是正式工件；
- 变更记录和评测要求断开；
- 退役只存在于路线图，没有落到运行配置；
- 替换没有双运行语义；
- 历史状态没有保留负责人；
- 来源证明只到 Git 提交，进不了运行时工件包；
- 替换发生时，已暂停运行与过期会话状态被遗忘，但操作员其实还需要它们；
- 验证器契约谱系丢失了，尽管发布或保障决策曾依赖它；
- bundle 写了 `sandbox_profile`，却没有保留 workspace、permissions 与 snapshot/resume policy 的 review-evidence link。

## 9. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 高风险变更是否有显式的变更记录？
- 你是否真的有已批准工件包，而不是“最新几个 YAML 文件”？
- 出现事故追踪时，你能反推出当时激活的工件包及其发布身份吗？
- 你能说清一次发布当时是在哪个带有验证器约束的契约族下被批准的吗？
- 如果 bundle 包含 `sandbox_profile`，能不能找到 workspace、permissions 与 snapshot/resume policy 的 review evidence？
- 已废弃能力和策略包是否有退役计划？
- 替换之后归档状态是否还有负责人？
- 生命周期工件层面的回滚单元是否清晰？

如果连续几个问题的答案都是“否”，那说明你的软件交付生命周期和上线流程也许已经不错，但生命周期层还没有真正补齐。

## 下一步做什么

- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [评测数据集 Schema 与打分契约](eval-schema.zh.md)
- [策略包 Schema 与审批契约](policy-bundle-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 20 章：智能体系统的变更管理](../book/part-viii/chapter-20.zh.md)
- [第 22 章：供应链、来源追踪与已批准工件](../book/part-viii/chapter-22.zh.md)
- [第 23 章：退役、替换与终止使用纪律](../book/part-viii/chapter-23.zh.md)
