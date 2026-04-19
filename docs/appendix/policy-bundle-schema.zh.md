# 策略包模式与审批契约

这一页把书里已经写过的几个主题连起来：

- [第 4 章：工具网关、审批与审计链路](../book/part-ii/chapter-4.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
- [第 20 章：智能体系统的变更管理](../book/part-viii/chapter-20.zh.md)

同时它也依赖可运行的参考包：

- [参考包](reference-package.zh.md)

如果追踪模式和评测模式那两页回答的是：

- 如何描述实际行为；
- 如何描述期望行为；

那么这一页回答的就是第三个问题：

- 如何描述位于推理和副作用之间的治理规则。

## 为什么要把策略包当成工件

在智能体系统里，一个很常见的问题是：

- 策略规则一部分藏在提示里；
- 一部分在网关代码里；
- 一部分在审批界面里；
- 一部分只存在于团队脑子里。

系统还小时也许能勉强运转，但一旦进入变更管理、审计和分阶段上线，这种策略层就会变得太模糊。

所以最好把 `policy bundle` 视作一个一等工件。

## 什么是策略包

这里可以把 `policy bundle` 理解为一组作为整体发布的相关规则：

- 运行时策略；
- 工具策略；
- 审批策略；
- 用于 pause/resume 与 background paths 的 runtime-control rules；
- 记忆写入规则；
- 升级规则；
- 出口规则；
- 面向 high-risk eval 与 rollout evidence 的 trusted verifier-contract expectations。

重点不在于所有内容必须塞进一个 YAML 文件，而在于这个 bundle 应该是：

- 可版本化；
- 可评审；
- 可追溯；
- 可发布。

## 最小 policy bundle 结构

一个最小可用的 bundle 可以长这样：

```yaml
bundle:
  bundle_id: policy-support-triage-2026-04-07
  version: 2026.04.07
  owner_team: platform-safety
  applies_to:
    agent_ids: ["support-triage-ref"]
  artifacts:
    - policy.yaml
    - approvals.yaml
    - controls.yaml
  contract_version: capability-contract-v3
  release_identity: release-support-triage-2026-04-07-canary
```

这里还不是具体规则本身，而是一个信封结构，用来回答：

“对于这套智能体系统，我们到底把哪些东西视为当前的策略工件？”

而一旦发布级治理开始重要，它也应该继续回答：

“这个 bundle 参与定义的是哪一个发布身份？”

## 为什么审批契约不能只写在叙述文字里

审批逻辑经常只是这样被描述：

- “高风险动作需要确认”；
- “经理负责批准建单”；
- “危险动作需要安全团队签字”。

这远远不够。

更好的做法是把审批契约写清楚：

- 谁可以批准；
- 哪类动作需要审批；
- 审批请求必须带哪些字段；
- 允许哪些决策；
- 拒绝之后会发生什么；
- 一次 run 是否可以 pause、resume、expire 或 cancel；
- 审计轨迹里必须留下什么。

## 审批契约示例

下面是一个可工作的 skeleton：

```yaml
approval_contract:
  capability: create_ticket
  risk_tier: high
  bundle_version: 2026.04.07
  release_identity: release-support-triage-2026-04-07-canary
  required_reviewers:
    - manager
  request_fields:
    - trace_id
    - session_id
    - requested_by
    - reason
    - tool_arguments_redacted
  allowed_decisions:
    - approved
    - rejected
  runtime_controls:
    pause_allowed: true
    max_wait_seconds: 1800
    on_expiry: cancel_run
  on_reject: stop_run
```

重点很简单：审批应该是机器可读的运行契约，而不只是界面上的一颗按钮。而当审批本身会影响发布时，这个契约也应该明确写出它所属的 bundle version 和 release identity。

## policy bundle 和 lifecycle 的关系

从 Part VIII 里，这里最重要的是两点：

- 策略变更属于影响发布的变更；
- 策略包应该作为完整工件进入变更管理。

也就是说，团队不应该只回答：

“我们原则上有什么 policy？”

还应该回答：

“这个发布或事故发生时，到底是哪一个策略包版本在生效？”

而一旦 runtime 把 bundle 当作受治理的发布表面，接下来的问题也就不可避免了：

“这个策略包参与构成的是哪一个发布身份？”

## policy bundle 和 traces 的关系

它们之间的关系非常直接：

- 追踪告诉你，哪一个策略决策真正触发了；
- 策略包告诉你，这个决策来自哪里；
- 审批契约告诉你，人工门禁本来应该长什么样。

少了这三者的联动，调查很快就会变成猜测。

## reference runtime 现在已经支持什么

在 `agent_runtime_ref` 里，现在已经有：

- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [approvals.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/approvals.yaml)
- [controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/controls.yaml)
- [change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)

也就是说，这个参考包已经活在一种模型里：策略和审批不再只是“附带设置”，而是受治理的工件。

## 生产级模式还应该补什么

一旦 runtime 开始包含 stateful MCP 与 resumable capability sessions，policy bundle 就不能只描述 capability 原则上能不能用，还必须描述这些 live session 是如何被治理的。

这时几乎立刻就会需要补上这些字段：

- `trusted_verifier_contracts`
- `verifier_contract_required_for_high_risk`
- `on_untrusted_verifier_contract`
- `capability_session_mode`
- `resume_policy`
- `on_session_expiry`
- `progress_event_policy`
- `elicitation_policy`
- `reinit_requires_approval`
- `approval_mode`
- `approval_delegate`
- `classifier_verdict_policy`
- `escalate_to_human_if`
- `subagent_handoff_policy`
- `authorization_mode`
- `delegated_principal_policy`
- `token_reuse_policy`
- `on_authorization_revoke`
- `mcp_discovery_source`
- `mcp_server_owner`
- `mcp_auth_mode`
- `shadow_mcp_handling`

这些字段可以避免一种危险情况：policy bundle 在静态层面批准了 capability，但把真实 session lifecycle 留在控制模型之外。

Anthropic 的 workflow taxonomy 又补上了一个很有用的 contract 维度。[^anthropic] 成熟的 policy bundle 不应只说明 capability 原则上能不能用，还应说明它可以出现在哪些 orchestration patterns 里。

这时很快就会需要补上这些字段：

- `allowed_orchestration_patterns`
- `disallowed_orchestration_patterns`
- `worker_inheritance_policy`
- `worker_capability_subset`
- `review_required_before_worker_write`

这些字段能让 governed contract 回答这样的问题：

- 某个 capability 能不能进入 `prompt chaining`、`routing` 或 `parallelization`；
- `orchestrator-workers` 里的 delegated workers 是否继承 approval 或 delegated authorization context；
- worker 是否可以再请求额外 capabilities，还是只能使用受限 subset；
- 在任何 write-capability 被执行前，worker output 是否必须先经过 review。

它们也能防止第二类漂移：delegated approval path 已经存在于产品行为里，但还没有被表示成受治理的 contract。

一旦系统变得更成熟，策略包很快就应该继续补充：

- `bundle_version`
- `artifact_lineage`
- `change_id`
- `release_identity`
- `approval_contracts`
- `runtime_control_schema`
- `contract_version`
- `deprecated_rules`
- `redaction_policy`

这会把策略层从“一堆配置文件”提升成真正的发布面。

## 为什么 policy bundle 和 capability catalog 不能彼此漂移

有一种很糟糕的状态是：policy bundle、capability catalog 和 approval rules 各自分开存在，而且它们之间的链接很弱。

然后很快就会出现问题：

- catalog 里有 capability，但没有对应的 approval contract；
- policy 还在引用已经不存在的 capability name；
- audit 看到了 decision，却没法把它和具体 bundle version 关联起来。

所以 practical rule 很简单：

- 能力目录描述系统能做什么；
- 策略包描述这些能力在什么条件下、通过哪些 orchestration patterns 可以被调用；
- 审批契约描述推理应该在何处停下并把控制权交给人；
- authorization contract 描述动作究竟是在谁的 identity 与 delegated scope 下执行；
- MCP governance contract 描述 capability 是否来自 approved registry、MCP server 由谁负责、由哪种 auth mode 保护，以及发现 shadow MCP path 时该如何处理；
- verifier contract policy 描述哪些 verifier contracts 可以被信任用于 high-risk grading、rollout evidence 或 assurance decisions。

## 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 是否有带版本的策略包？
- 能不能把策略包和发布、事故复盘关联起来？
- 审批契约是机器可读的，还是只写在说明文字里？
- 审批请求必须带哪些字段，是否清楚？
- 策略包和能力目录之间是否有稳定关联？
- 能不能知道某条追踪对应的是哪个策略版本和哪一个发布身份？
- 是否明确写出了哪些 verifier contracts 可以被信任用于 high-risk grading 或 rollout evidence？

如果连续几个答案都是“不能”，那说明你的策略层虽然存在，但还没有被塑造成完整的运行工件。

## 下一步做什么

- [追踪模式与事件目录](trace-schema.zh.md)
- [评测数据集模式与分级契约](eval-schema.zh.md)
- [生命周期工件规范](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [按场景组织的 Policy Templates 与 Checklists](policy-templates.zh.md)
