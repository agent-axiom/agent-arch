# 策略包 Schema 与审批契约

这一页把书里已经写过的几个主题连起来：

- [第 4 章：工具网关、审批与审计轨迹](../book/part-ii/chapter-4.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
- [第 20 章：智能体系统的变更管理](../book/part-viii/chapter-20.zh.md)
- [Evidence Spine：从请求到发布判断](../book/part-v/evidence-spine.zh.md)

同时它也依赖可运行的参考包：

- [参考包](reference-package.zh.md)

如果追踪 Schema 和评测 Schema 那两页回答的是：

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

所以最好把策略包视作一个一等工件。

## 什么是策略包

这里可以把策略包理解为一组作为整体发布的相关规则：

- 运行时策略；
- 工具策略；
- 审批策略；
- 用于暂停/恢复与后台路径的运行时控制规则；
- 记忆写入规则；
- 升级规则；
- 出口规则；
- 面向高风险评测与发布证据的可信验证器契约期望。

重点不在于所有内容必须塞进一个 YAML 文件，而在于这个包应该是：

- 可版本化；
- 可评审；
- 可追溯；
- 可发布。

## 最小策略包结构

一个最小可用的包可以长这样：

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

“这个包参与定义的是哪一个发布身份？”

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
- 一次运行是否可以暂停、恢复、过期或取消；
- 审计轨迹里必须留下什么。

## 审批契约示例

下面是一个可工作的骨架：

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

重点很简单：审批应该是机器可读的运行契约，而不只是界面上的一颗按钮。而当审批本身会影响发布时，这个契约也应该明确写出它所属的包版本和发布身份。

## 策略包和生命周期的关系

从第八部分看，这里最重要的是两点：

- 策略变更属于影响发布的变更；
- 策略包应该作为完整工件进入变更管理。

也就是说，团队不应该只回答：

“我们原则上有什么策略？”

还应该回答：

“这个发布或事故发生时，到底是哪一个策略包版本在生效？”

而一旦运行时把包当作受治理的发布表面，接下来的问题也就不可避免了：

“这个策略包参与构成的是哪一个发布身份？”

## 策略包和追踪的关系

它们之间的关系非常直接：

- 追踪告诉你，哪一个策略决策真正触发了；
- 策略包告诉你，这个决策来自哪里；
- 审批契约告诉你，人工门禁本来应该长什么样；
- 发布身份告诉调查者，这个决策究竟属于哪一个受治理的发布表面。

少了这四者的联动，调查很快就会变成猜测。

## 参考运行时现在已经支持什么

在 `agent_runtime_ref` 里，现在已经有：

- [policy.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/policy.yaml)
- [approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- [controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/controls.yaml)
- [change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)

也就是说，这个参考包已经活在一种模型里：策略、审批与 runtime-control contracts 不再只是“附带设置”，而是绑定到具体包版本与发布控制面的受治理工件。

## 生产级 Schema 还应该补什么

一旦运行时开始包含有状态 MCP 与可恢复能力会话，策略包就不能只描述能力原则上能不能用，还必须描述这些在线会话是如何被治理的。

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

这些字段可以避免一种危险情况：策略包在静态层面批准了能力，但把真实会话生命周期留在控制模型之外。

Anthropic 的工作流分类又补上了一个很有用的契约维度。[^anthropic] 成熟的策略包不应只说明能力原则上能不能用，还应说明它可以出现在哪些编排模式里。

这时很快就会需要补上这些字段：

- `allowed_orchestration_patterns`
- `disallowed_orchestration_patterns`
- `worker_inheritance_policy`
- `worker_capability_subset`
- `review_required_before_worker_write`

这些字段能让受治理契约回答这样的问题：

- 某个能力能不能进入 `prompt chaining`、`routing` 或 `parallelization`；
- `orchestrator-workers` 里的委派工作器是否继承审批或委派授权上下文；
- 工作器是否可以再请求额外能力，还是只能使用受限子集；
- 在任何写入能力被执行前，工作器输出是否必须先经过评审。

它们也能防止第二类漂移：委派审批路径已经存在于产品行为里，但还没有被表示成受治理的契约。

一旦系统变得更成熟，策略包很快就应该继续补充：

- `bundle_version`
- `artifact_lineage`
- `change_id`
- `release_identity`
- `approval_contracts`
- `runtime_control_schema`
- `sandbox_profile_contract`
- `sandbox_profile_review_required`
- `contract_version`
- `deprecated_rules`
- `redaction_policy`

如果某项能力可以在由 sandbox 支撑的路径中执行，策略包也应该指向 sandbox profile contract，或显式要求它经过 review；否则 workspace、shell/filesystem permissions 与 snapshot/resume behavior 会留在发布身份之外。

这会把策略层从“一堆配置文件”提升成真正的发布面。

## 为什么策略包和能力目录不能彼此漂移

有一种很糟糕的状态是：策略包、能力目录和审批规则各自分开存在，而且它们之间的链接很弱。

然后很快就会出现问题：

- 目录里有能力，但没有对应的审批契约；
- 策略还在引用已经不存在的能力名称；
- 审计看到了决策，却没法把它和具体包版本关联起来。

所以实用规则很简单：

- 能力目录描述系统能做什么；
- 策略包描述这些能力在什么条件下、通过哪些编排模式可以被调用；
- 审批契约描述推理应该在何处停下并把控制权交给人；
- 授权契约描述动作究竟是在谁的身份与委派范围下执行；
- MCP 治理契约描述能力是否来自已批准注册表、MCP 服务器由谁负责、由哪种认证模式保护，以及发现影子 MCP 路径时该如何处理；
- 验证器契约策略描述哪些验证器契约可以被信任用于高风险打分、发布证据或保障决策。

Reference runtime 在 `capabilities.yaml` 和 `policy.yaml` 中把这个连接具体化：capability entries 携带 `tool_principal`、`risk_tier`、`network_access`、`allowed_egress`、`timeout_seconds` 和 `idempotency_key_required`，policy entries 携带 `run_precheck`、`require_tenant`、`deny_if_principal_missing`，针对 `search_docs`、`create_ticket` 与 `run_shell` 的 capability decisions，memory-write `allow_kinds`（`validated_fact` 和 `session_summary`），以及 execution-level `allow_network_access`。Policy loader 会显式校验这个结构：`'policy' must be a mapping`、`'run_precheck' must be a mapping`、`'run_precheck.require_tenant' must be a boolean`、`'run_precheck.deny_if_principal_missing' must be a boolean`、`'{label}' must be a boolean`、`'memory_write' must be a mapping`、`'allow_kinds' must be a list`、`memory_write.allow_kinds entries must not be empty`、`'execution' must be a mapping`、`'allow_network_access' must be a list`、`execution.allow_network_access entries must not be empty`、`Policy capability name must not be empty`、`Policy decision is not supported: {decision}`、`Policy approver must not be empty: {capability_name}` 和 `Policy for capability {name!r} must be a mapping`。

## 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 是否有带版本的策略包？
- 能不能把策略包和发布、事故复盘关联起来？
- 审批契约是机器可读的，还是只写在说明文字里？
- 审批请求必须带哪些字段，是否清楚？
- 策略包和能力目录之间是否有稳定关联？
- 能不能知道某条追踪对应的是哪个策略版本和哪一个发布身份？
- 是否明确写出了哪些验证器契约可以被信任用于高风险打分或发布证据？

如果连续几个答案都是“不能”，那说明你的策略层虽然存在，但还没有被塑造成完整的运行工件。

## 下一步做什么

- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [评测数据集 Schema 与打分契约](eval-schema.zh.md)
- [生命周期工件 Schema](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [按场景组织的策略模板与检查清单](policy-templates.zh.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
