# 策略包 Schema 与审批契约

这一页把书里已经写过的几个主题连起来：

- [第 4 章：工具网关、审批与审计轨迹](../book/part-ii/chapter-4.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
- [第 20 章：智能体系统的变更管理](../book/part-viii/chapter-20.zh.md)
- [Evidence Spine：从请求到发布判断](../book/part-v/evidence-spine.zh.md)

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

所以最好把策略包视作一个一等工件。

## 建议扩展：凭据与身份绑定

动机：[LangChain Connections](https://www.langchain.com/blog/connections-managed-credentials-and-per-caller-identity-for-managed-deep-agents)。这是建议的内部契约，不是新增 OAuth 字段，也不是 reference runtime 已实现的解析器。`credential_owner`（`agent` 或 `user`）独立于 `credential_type`（`secret` 或 `oauth`）。

策略证据应包含非秘密引用 `connection_ref`、`credential_ref`、`deployment_ref`、`tenant_ref`、`requester_principal_ref`、`effective_principal_ref`，以及 `credential_owner`、`credential_type`、`policy_version`、`authorization_checked_at`。请求者来自已验证的入口上下文，实际主体来自可信的提供方绑定；模型不能通过工具参数指定它们。对于用户所有的凭据，解析器必须验证其属于当前用户和租户。若无法确定实际主体，应阻止要求该绑定的操作。秘密值和令牌不得进入轨迹、提示或缓存键。

未来实现的验收场景：

1. 保留全部四种 owner/type 组合，不因 OAuth 推断所有权；agent-owned OAuth 仍为共享身份。
2. 用户 A、B 调用同一连接：A 的私有结果与凭据不得泄露给 B；拒绝通过工具参数 `user_id` 替换身份。
3. 缺少用户授权：不执行依赖操作，也不回退到共享凭据。访问同意不能替代操作批准。
4. 暂停期间调用者或租户改变，或权限被撤销：未经重新验证，不复用旧凭据、缓存或 allow 决策。
5. 明确策略允许共享账户：审计分别记录请求者和实际主体，证据中不含凭据值。


## 建议扩展：部分 OAuth grant

这是生产契约建议，不表示 reference runtime 已实现这些字段。动机来自 [Cloudflare, From all-or-nothing to task-based OAuth consent](https://blog.cloudflare.com/task-based-oauth-consent/)。以下字段属于内部策略证据，并非新的标准 OAuth 字段。

- `requested_scopes`：本次授权请求的 scopes。
- `granted_scopes`：从经过验证的授权服务器响应或其他可信 provider 机制获得的实际集合；不能根据请求猜测，也不能假定所有 token 都是 JWT。
- `required_scopes`：所选操作的最低权限，不是同意界面的必需 scopes。
- `missing_scopes`：required 与 granted 的差集；非空时必须在副作用发生之前阻止操作。
- `grant_ref`、`authorization_checked_at`：非秘密的 grant 引用和检查时间；与 subject、task、tool、resource、policy version 一起支持决策审查。不得记录 token 本身。

示例（scope 名称和证据字段并非标准化定义）：

```yaml
oauth_scope_evidence:
  grant_ref: grant-42
  authorization_checked_at: "2026-09-08T00:00:00Z"
  requested_scopes: [tickets.read, tickets.write]
  granted_scopes: [tickets.read]
  required_scopes: [tickets.write]
  missing_scopes: [tickets.write]
  decision: deny
  reason: insufficient_granted_scope
```

scope 检查不能替代 resource/audience/expiry 验证、当前策略或独立的操作审批。如果无法可靠确定 grant，就停止敏感操作；不得以 requested 代替 granted。refresh/resume 后需要检查当前授权上下文，下游服务仍需自行执行授权检查。

该建议契约的验收场景：

1. 仅授予读取：生成独立获准的摘要，不调用写入工具，并明确结果只完成了一部分。
2. 缺失 scope 是整个任务必需的：说明原因并停止，不重试、不更换 credential、不暗中扩大访问权限。
3. scope 存在但 resource 或 task 超出策略：拒绝；广泛 grant 不能覆盖 task-scoped authority。
4. refresh/resume 后写权限消失：不得复用旧 allow 决策。
5. grant 未知或用户完全拒绝同意：不得基于 requested scopes 执行。操作审批不能替代 grant。

## 建议扩展：MCP 目录缓存

这是内部契约建议，不是 `agent_runtime_ref` 已实现的能力，也不是可直接使用的 FastMCP 配置。`ttlMs` 和 `cacheScope` 是 FastMCP 文档描述的服务器提示；下面其他字段是建议的标准化证据。来源：[LangChain: MCP in LangChain](https://www.langchain.com/blog/mcp-in-langchain-stateless-protocol-elicitation-and-more) / [FastMCP: Response caching](https://gofastmcp.com/clients/client#response-caching)。

```yaml
catalog_cache_evidence:
  target_id: support-mcp-prod
  protocol_version: "2026-07-28"
  request_fingerprint: tools-list-page-1
  partition_ref: verified-tenant-a-principal-7-authz-v3
  policy_version: support-policy-v8
  server_ttl_ms: 60000          # ttlMs
  server_cache_scope: public   # cacheScope
  local_max_ttl_ms: 30000
  effective_ttl_ms: 30000
  fetched_at: "2026-09-08T07:00:00Z"
  expires_at: "2026-09-08T07:00:30Z"
  catalog_digest_ref: catalog-snapshot-42
  cache_hit: true
  authorization_decision_ref: fresh-tool-call-decision-43
```

`partition_ref` 应从已验证的 tenant/principal 和访问上下文派生；密钥与 token 不得进入缓存键或日志。`target_id` 必须唯一标识服务器；`request_fingerprint` 标识列表方法及参数，包括分页或过滤条件。示例字符串仅作说明。`server_cache_scope` 记录收到的 `cacheScope`，不得扩大其含义。即使响应为 `public`，本地策略仍可要求更严格的隔离。

TTL 限制快照复用：有效期不得超过服务器 `ttlMs` 或本地上限。零 TTL 不允许复用；对于缺失或无效提示，这个保守契约要求从网络读取而不复用缓存。这是本地策略，不代表所有 SDK 的默认行为。如果无法刷新过期目录，不得用旧快照为敏感调用提供授权依据。在 FastMCP 中，`refresh` 从网络读取并更新缓存；`bypass` 既不读取缓存，也不存储响应。

建议契约的验收场景：

1. 同一 tenant 的两名用户权限不同：第一人的目录不得服务第二人。共享必须同时满足服务器标记 `public` 和本地策略允许。
2. TTL 到期前权限被撤销：当前授权检查拒绝调用；缓存命中不能复用旧 allow，依赖权限的可见性也应失效。
3. 检测到定义变化：刷新并重新检查 schema、风险和审批；不得自动将旧审批迁移到不同契约。
4. TTL 过期、为零或无效：从网络读取；服务器不可用不能成为绕过检查的理由。
5. principal、grant 或策略版本变化：更换分区或使缓存失效；metadata 和访问决策都不得跨越上下文边界。

## 建议扩展：复合资源授权

这是建议的内部契约，不是可直接使用的 Cloudflare 配置，也不是 `agent_runtime_ref` 已实现的功能。以下操作名称和标识符仅用于示例；访问边界来自 [Workers 角色文档](https://developers.cloudflare.com/workers/authorization/)。

```yaml
compound_authorization_evidence:
  principal_ref: verified-ci-principal
  task_ref: approved-route-change
  plan_ref: immutable-plan-42
  policy_version: deploy-policy-v3
  requirements:
    - action: worker.update
      resource_ref: account-a/worker-a
      required_access: Editor
      decision: allow
    - action: route.write
      resource_ref: account-a/zone-a
      required_access: Workers Routes Write
      decision: deny
  decision: deny
  reason: missing_zone_route_permission
```

适配器从规范化的账号、Worker 和受影响区域标识符推导 `requirements`，迁移路由时包括原区域和新区域。模型给出的列表不能证明完整性。每项检查使用同一主体当前已验证的权限；总体 `allow` 要求**所有**检查通过、符合任务范围，并在需要时获得独立审批。`unknown`、检查不可用或任一 `deny` 都阻止复合变更。审计保留原因与非秘密证据引用，不记录令牌。

预检查不会在多个 API 之间创建事务。首次修改前检查完整计划；每次调用前及暂停恢复后重新检查权限和目标，服务端仍保留自己的授权检查。计划变化需要新决策，并在必要时重新审批。如果部分调用后权限被撤销，应停止后续修改并核对真实效果；记录部分结果，恢复操作单独授权。不得承诺自动回滚或为完成任务扩大凭据权限。

建议检查（不是实际调用 Cloudflare 的结果）：

1. 权限仅覆盖 Worker A：即使操作名称相同，读取或修改 Worker B 也被拒绝。
2. `Metadata Read-Only` 允许 A 的遥测，但不允许读取代码；`Content Read-Only` 不允许部署。
3. `Editor` 允许符合策略的现有 A 更新，但不允许删除或创建新 Worker。
4. 不改变路由的部署无需区域权限；新增、修改或删除路由时，任一受影响区域缺少 `Workers Routes Write` 都必须在修改前阻止操作。
5. 复合操作的权限全部存在时，也只能批准任务范围内的已验证计划。审批后替换区域需要重新检查。
6. 步骤之间撤销权限会阻止下一步；已完成的效果记为部分结果，而非完整成功或保证已回滚。

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

!!! note "规范策略案例（Canonical policy cases）"
    策略包（policy bundle）不应该在三个规范案例（canonical cases）中长得完全一样。**支持分流（Support triage）** 需要写入能力审批策略（write-capability approval policy）、幂等证据（idempotency evidence）和重复工单恢复控制（duplicate-ticket recovery controls）。**内部知识助手（Internal knowledge assistant）** 需要检索策略（retrieval policy）、记忆写入规则（memory write rules）、新鲜度检查（freshness checks）、访问控制（access control）和知识来源（knowledge provenance）。**事件协调（Incident coordination）** 需要升级规则（escalation rules）、通知副作用（notification side effects）、响应归属（response ownership）和事件后学习门禁（post-incident learning gates）。

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
    - idempotency_key
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

!!! example "重复工单线索的策略契约"
    对支持分流（support-triage）来说，`create_ticket` 契约应该在审批请求里就要求 `idempotency_key`，而不是只在工具执行时才出现。这样，人工审批、网关（gateway）和追踪（trace）会看到同一个写入意图；策略包（policy bundle）可以在 `side_effect_unknown` 时禁止没有调和（reconciliation）的重试；发布复核（rollout review）检查的是受治理能力，而不是松散的工具调用。

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

也就是说，这个参考包已经活在一种模型里：策略、审批与运行时控制契约（runtime-control contracts）不再只是“附带设置”，而是绑定到具体包版本与发布控制面的受治理工件。可执行门禁（Executable gate）`check-controls` 也让控制包（control bundle）可审查：它会返回 `healthy`、`required_controls`、`blocked_findings_expected`、`missing_controls`、`failed_run_controls`、`preserved_failed_run_controls`、`failed_run_controls_healthy`、`support_duplicate_controls`、`preserved_support_duplicate_controls`、`support_duplicate_controls_healthy`、`blocking_findings` 和 `inventory_drift`，其中嵌套字段 `has_drift`、`missing_from_catalog` 与 `missing_from_inventory` 会把策略/控制失败（policy/control failures）和能力清单漂移（capability inventory drift）分开。

同一个门禁（gate）也会明确约束控制包（control bundle）的输入形状：控制配置验证（controls config validation）会报告 `Controls policy config must be a mapping`、`'controls' must be a mapping`、`'controls.require' must be a list`、`'controls.block_if' must be a list`、`controls.require entries must be strings`、`controls.require entries must not be empty`、`controls.require entries must be unique`、`controls.block_if entries must be strings`、`controls.block_if entries must not be empty` 和 `controls.block_if entries must be unique`；信号覆盖（signal overrides）会报告 `Assessment signals must be a mapping`、`Assessment signal key must be a string`、`Assessment signal key must not be empty`、`Assessment signal keys must be unique` 和 `Assessment signal value must be a boolean: {field}`。这样操作者可以区分畸形策略包（malformed policy bundle）与格式正确但评估失败的控制评估（control assessment）。

## 生产级模式还应该补什么

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

Microsoft Foundry 的 Open Trust Stack 在这里可以作为外部参照：policy 应该编译成具名 runtime checkpoints，而不是停留在 eval report 旁边的一段 prose。[^microsoft-open-trust-stack] 用可移植 YAML 表达时，可以长这样：

```yaml
control_checkpoints:
  - checkpoint: tool_execution
    policy_requirement: no_external_write_without_approval
    predicate: risk_tier == "high" and side_effect == "external_write"
    action: require_approval
    audit_fields:
      - checkpoint
      - policy_requirement
      - predicate_result
      - action
      - control_version
      - eval_case_id
      - trace_id
```

最小 contract surface 包括：`checkpoint`、`policy_requirement`、`predicate` 或 `judge`、`action`、`control_version`、`eval_case_id`、`trace_id` 和 `observed_signal`。Checkpoints 应该按 agent cycle 中的位置命名：`input`、`llm`、`state`、`tool_execution` 和 `output`。这样 failed eval 不只会指向 prompt diff，还能连到具体 runtime hook、audit event 和 regression case。

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

如果某项能力可以在由沙箱（sandbox）支撑的路径中执行，策略包也应该指向沙箱配置文件契约（sandbox profile contract），或显式要求它经过复核（review）；否则工作区（workspace）、shell/文件系统权限（shell/filesystem permissions）与快照/恢复行为（snapshot/resume behavior）会留在发布身份之外。

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

参考 runtime 在 `capabilities.yaml` 和 `policy.yaml` 中把这个连接具体化：capability entries 携带 `tool_principal`、`risk_tier`、`network_access`、`allowed_egress`、`timeout_seconds` 和 `idempotency_key_required`，policy entries 携带 `run_precheck`、`require_tenant`、`deny_if_principal_missing`，针对 `search_docs`、`create_ticket` 与 `run_shell` 的 capability decisions，memory-write `allow_kinds`（`validated_fact` 和 `session_summary`），以及 execution-level `allow_network_access`。Policy loader 会显式校验这个结构：`Policy config must be a mapping`, `'policy' must be a mapping`、`'run_precheck' must be a mapping`、`'run_precheck.require_tenant' must be a boolean`、`'run_precheck.deny_if_principal_missing' must be a boolean`、`'{label}' must be a boolean`、`'memory_write' must be a mapping`、`'allow_kinds' must be a list`、`memory_write.allow_kinds entries must be strings`、`memory_write.allow_kinds entries must not be empty`、`memory_write.allow_kinds entries must be unique`、`'execution' must be a mapping`、`'allow_network_access' must be a list`、`execution.allow_network_access entries must be strings`、`execution.allow_network_access entries must not be empty`、`execution.allow_network_access entries must be unique`、`Policy capability names must be strings`、`Policy capability name must not be empty`、`Policy capability names must be unique`、`Policy capability entries must be CapabilityPolicy`、`Policy precheck request must be RunRequest`、`Policy context must be RunContext`、`Policy tool request must be ToolRequest`、`Policy capability must be CapabilitySpec`、`'capabilities' must be a mapping`、`Policy action must be a string`、`Policy action is not supported: {action}`、`Policy field must be a string: {field}`、`Policy field is required: {field}`、`Policy decision must be a string`、`Policy decision is not supported: {decision}`、`Policy approver must be a string`、`Policy approver must not be empty: {capability_name}`、`Policy memory kind must be a string`、`Policy memory kind must not be empty` 和 `Policy for capability {name!r} must be a mapping`。

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

- [追踪模式与事件目录](trace-schema.zh.md)
- [评测数据集模式与打分契约](eval-schema.zh.md)
- [生命周期工件模式](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [按场景组织的策略模板与检查清单](policy-templates.zh.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^microsoft-open-trust-stack]: Microsoft Foundry Blog, [Build agents you can trust across any framework with open evals and a control standard](https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/).
