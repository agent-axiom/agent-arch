# 参考包

现在仓库里已经有一个可运行的小型代码骨架：[agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref)。

它的目标不是变成生产级框架，而是作为本书 **第七和第八部分** 的最小代码锚点。

这个包被有意定位成实现锚点，而不是一个平行产品。它的价值在于，让读者能够看到本书论证背后的可运行结构，而不会把整个项目重新变成框架手册。

这一页**不**承诺的事情是：

- 它不会取代本书对这些层为何存在的解释；
- 它不会成为读者学习架构权衡的主要地方；
- 它也不会试图把整个仓库变成一个通用智能体框架。

这里是这个包的主说明页面。README 里只保留简短的上手说明，完整的命令行、配置和结构说明都集中放在这里。

一个实用的阅读路径是：

- 第 16 章看基线运行时与能力会话状态，
- 第 17 章看策略层与能力契约，
- [Evidence Spine](../book/part-v/evidence-spine.zh.md) 看从请求到发布判断的端到端治理记录，
- 第 18 章看围绕审批和运行时行为的发布门禁，
- 第 21 章看保障响应，
- 第 22 章配合生命周期 Schema 看受治理工件链接、发布身份、验证器契约谱系与委派授权来源证明，
- 第 23 到 27 章看能力会话周围的中断、过期、重新初始化、退役、可观测性、注册表负责人、验证器证据义务与委派授权生命周期控制。

## 里面有什么

- [runtime.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/runtime.py)
  核心 `AgentRuntime`，负责组装运行上下文、检索、模型步骤、工具执行和后台更新钩子。
- [policy.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/policy.py)
  一个带结构化决策的小型策略引擎。
- [catalog.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/catalog.py)
  带有运行语义、风险等级和出口契约元数据的能力注册表。
- [identity.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/identity.py)
  智能体的显式身份，以及运行时被允许使用的已批准能力清单。
- [config.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/config.py)
  用来加载智能体身份、已批准能力清单、策略、能力目录和上线策略的 YAML 加载器。
- [memory.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/memory.py)
  类型化记忆记录、来源证明、修订号以及按租户隔离的内存存储。
- [background.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/background.py)
  负责持久化记忆写入、基于来源证明的保存，以及压缩整理的后台维护路径。
- [execution.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/execution.py)
  一个按契约分发能力的简单执行层，同时考虑风险等级与出口策略。
- [telemetry.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/telemetry.py)
  用于结构化事件和跨度的内存遥测发射器。
- [rollout.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/rollout.py)
  上线前的最小就绪性闸门。
- [controls.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/controls.py)
  用于已批准注册表的持续控制与清单漂移检查。
- [approvals.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/approvals.py)
  用于高风险动作的审批门禁、暂停/恢复语义、简单人工评审队列，以及审批状态必须与能力会话状态保持一致的那层控制表面。

同一层运行时控制表面也天然适合承载委派授权假设：是谁委托了访问，这份授权能否跨过暂停/恢复继续有效，以及如果委派访问在动作完成前被撤销，运行时应该如何处理。

- [lifecycle.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/lifecycle.py)
  用于变更记录、工件包、发布身份记录、运行时控制 Schema、验证器契约谱系和退役计划的生命周期工件，以及这些状态的就绪检查。

## 如何运行

```bash
.venv/bin/python -m agent_runtime_ref
```

预期输出：

```json
{"result": "Ticket request accepted and ready for follow-up.", "status": "success", "events": 9, "memory_records": 4, "config_dir": ".../agent_runtime_ref/configs"}
```

通过显式子命令运行运行时：

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref simulate-run --simulate-failure tool_timeout
```

第二种形式是一个刻意保持很小的失败丰富场景。它让这个参考包能够展示，一条本来被允许的能力也可能以受治理的失败运行收尾，并留下明确的遥测，而不是被泛化成成功路径。`simulate-run` 会返回 `agent_id`、`config_dir`、`trace_id`、`session_id`、`status`、`result`、`events`、`memory_records`、`pending_approvals` 和可选的 `failure_reason`。

查看智能体身份与已批准能力清单：

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
```

`inspect-agent` 会返回 `agent_id`、`display_name`、`owner_team`、`runtime_principal`、`approved_capabilities` 和 `catalog_capabilities`，让 inventory review 可以把 configured identity 与 capability catalog 对照起来。

查看与第八部分对应的生命周期工件，包括运行时控制链接和发布身份：

```bash
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref check-controls --signal policy_traces_present=false
.venv/bin/python -m agent_runtime_ref check-change --signal offline_eval_passed=false
.venv/bin/python -m agent_runtime_ref check-change --signal failed_run_drill_checked=false
.venv/bin/python -m agent_runtime_ref check-retirement --step revoke_egress=false
```

`inspect-lifecycle` 现在也会显示来自 `runtime-controls.yaml` 的 `sandbox_profile` 契约、`artifact_bundle.review_evidence`、`artifact_bundle.sandbox_profile_review_evidence`、`change.affected_surfaces`、`change.session_control_owner`、`change.emergency_freeze_owner`、`artifact_bundle.session_control_owner`、`retirement.session_control_owner`、`retirement.emergency_freeze_owner`、`failed_run_archive_targets`、`controls.failed_run_control_expectations`、`controls.failed_run_control_domains`、`controls.failed_run_control_count`、`controls.failed_run_control_summary`、`controls.failed_run_control_status`、`controls.failed_run_control_review_required`、`controls.failed_run_control_owner`、`controls.failed_run_control_source`、`controls.failed_run_control_last_review`、`controls.failed_run_control_next_review` 和 `controls.failed_run_control_release_binding`，这样操作员在同一个生命周期摘要里就能同时看到所有权、冻结责任、保留要求，以及追踪/来源证明控制。
同一份 runtime-control summary 由 `runtime-controls.yaml` 支撑，其中包括 `resume_allowed`、`allow_progress_events`、`allow_elicitation`、`expiry_policy` 和 `expiry_signal_owner`，因此可恢复的 capability sessions 会明确暴露 progress、elicitation 与 expiry assumptions。Delegated-authorization defaults 也保持显式：`authorization_mode` 是 `user_delegated_or_platform_owned`，`delegated_principal_policy` 是 `explicit_principal_binding_required`，`token_reuse_policy` 是 `reuse_within_valid_paused_run_only`，`on_authorization_revoke` 是 `cancel_or_reapprove`，`subagent_inheritance` 是 `denied_by_default`，resumable/reinit flows 使用 `resume_existing_session_if_valid`。
`check-change` 会返回 `change_id`、`ready`、`missing_signals`、`missing_failed_run_signals`、`rollout_strategy` 和 `risk_level`，这样退化路径发布评审的缺口就不会被埋在普通缺失信号列表里。
`check-retirement` 会返回 `system_id`、`ready`、`missing_steps`、`failed_run_archive_targets` 和 `replacement_mode`，这样操作员就能看到哪些遥测/会话/审批记录必须在退役之后继续保留下来，供后续退化路径评审使用。
`check-controls` 会返回 `healthy`、`missing_controls`、`failed_run_controls`、`preserved_failed_run_controls`、`failed_run_controls_healthy`、`blocking_findings` 和 `inventory_drift`，这样追踪/来源证明相关缺口就能和普通控制卫生分开审阅。它在 `controls.yaml` 中的 inputs 要求 `registry_reviewed`、`capability_owners_confirmed`、`memory_provenance_enforced` 和 `policy_traces_present`，而 `block_if` 会把 `direct_tool_access_present` 与 `unmanaged_runtime_present` 视为硬阻断项。

查看记忆记录：

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

现在 `inspect-memory` 会返回 `config_dir`、`count` 和 `records`；每条记录不只显示内容，也会显示 `provenance` 和 `revision`。
`dump-events` 现在会在退化路径演练的 JSON 输出里返回 `trace_id`、`status`、`result`、`event_count`、`events` 和 `failure_reason`。

导出一次运行的结构化事件：

```bash
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
.venv/bin/python -m agent_runtime_ref dump-events --simulate-failure tool_timeout
```

把事件导出为 JSONL，方便后续排查和回放：

```bash
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-events --simulate-failure upstream_unavailable --output artifacts/trace-demo-failed.jsonl
```

`export-events` 会返回 `output_path`、`trace_id`、`status`、`result`、`event_count`、`redact_fields` 和可选的 `failure_reason`，因此脱敏和退化路径证据会直接出现在命令摘要里。

如果你需要给外部人员查看脱敏后的导出结果，也可以在导出时直接隐藏敏感字段：

```bash
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl --redact-field user_input
```

从 JSONL 文件里查看某条追踪：

```bash
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
```

根据保存下来的追踪重新回放一次运行：

```bash
.venv/bin/python -m agent_runtime_ref replay-run --input artifacts/trace-demo.jsonl
```

`inspect-trace` 会返回 `trace_id`、`event_count` 和 `events`；`replay-run` 会返回 `source_trace_id`、`replay_trace_id`、`status`、`result` 和 `event_count`，让调查与重放都保留来源/运行谱系。

带信号覆盖的上线策略检查：

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

Rollout check 会返回 `ready`、`missing_required`、`blocking_signals` 和 `rollout_mode`，让自动化能够区分缺失的必需证据与明确阻断的信号。

检查持续控制和注册表漂移：

```bash
.venv/bin/python -m agent_runtime_ref check-controls --signal registry_reviewed=false
```

查看并处理演示用审批请求：

```bash
.venv/bin/python -m agent_runtime_ref inspect-approvals
.venv/bin/python -m agent_runtime_ref resolve-approval --decision approved --note "manager approved demo request"
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref inspect-session --simulate-failure tool_timeout
.venv/bin/python -m agent_runtime_ref session-eval-summary
.venv/bin/python -m agent_runtime_ref session-eval-summary --simulate-failure tool_timeout
.venv/bin/python -m agent_runtime_ref session-replay --user-input "Please create a ticket for this onboarding issue." --user-input "What language preference do you remember?"
.venv/bin/python -m agent_runtime_ref session-replay --simulate-failure tool_timeout --user-input "Please create a ticket for this issue."
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-session --simulate-failure tool_timeout --output artifacts/session-demo-failed.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --scenario failed_run_timeout --output artifacts/eval-failed-run.json
```

`inspect-approvals` 现在会返回 `trace_id`、`session_id`、`count` 和 `approvals`，其中包括 `authorization_mode`、`delegated_principal_id` 与 `delegated_scope` 等委派授权上下文，因此审批路径评审可以直接和会话证据对照。`resolve-approval` 在做出决定后会返回 `approval_id`、`status`、`reviewer`、`resolution_note` 和同样的委派上下文，这样行动身份谱系不会在闭合阶段丢失。
`inspect-session` 会显示会话级别的运行历史，以及关联的 `trace_id`。现在这里也能直接注入失败演练，而摘要会保留 `failed_runs`、`traceable_failed_runs`、`latest_failure_reason`，以及每次运行里的 `failure_reason`。
`session-eval-summary` 会返回这一组运行的紧凑摘要，其中也明确统计失败运行和 `traceable_failed_runs`，而不是又把结果压回只有 `success` 和 `denied` 两类。现在也可以直接在这里注入失败演练，摘要会立刻显示 `latest_failure_reason` 便于快速复盘。
`session-replay` 可以在同一个 `session_id` 里执行多个相关请求。现在这里也能直接注入失败演练，而回放摘要会连同每次运行里的 `failure_reason` 一起保留 `failed_runs`、`traceable_failed_runs` 与 `latest_failure_reason`。
`export-session` 会把整段会话保存成结构化 JSON，已经可以作为离线评测流程的种子数据。现在它也会保留委派授权上下文，例如 `authorization_mode`、`delegated_principal_id` 和 `delegated_scope`，同时在 CLI 命令摘要里直接显示失败演练的 `failed_runs`、`traceable_failed_runs` 与 `latest_failure_reason`。

Session 与 eval 命令也会明确暴露摘要字段：`inspect-session` 返回 `session_id`、`tenant_id`、`principal_id`、`trace_count`、`latest_status`、`summary` 和 `runs`；`session-eval-summary` 返回 `session_id`、`total_runs`、`success_runs`、`approval_wait_runs`、`denied_runs`、`failed_runs`、`traceable_failed_runs`、`latest_status`、`latest_trace_id` 和 `latest_failure_reason`；`session-replay` 返回 `session_id`、`run_count`、`summary` 和 `runs`；`export-session` 返回 `output_path`、`session_id`、`total_runs`、`failed_runs`、`traceable_failed_runs`、`latest_trace_id` 和 `latest_failure_reason`；`export-eval-dataset` 返回 `dataset_name`、`output_path`、`session_count`、`run_count`、`failed_runs`、`traceable_failed_runs`、`latest_failure_reason` 和 `sessions`。

现在，运行时也会把工具路径中的失败类结果，例如验证失败，当成一等运行结局来处理。它不再假装这次运行仍然成功，而是记录失败运行、发出明确的 `run_failed` 事件，并在会话导出与 CLI 输出中通过 `failure_reason` 字段同时保留这个状态以及具体失败原因。
`export-eval-dataset` 会把几个内置会话场景打包成一个可直接用于评测的 JSON 工件，其中也包括一个单独的失败运行演练场景，以及带有阻断型 `sandbox_profile_review` 评分规则的带审批路径 support_ticket 场景，而命令摘要现在也会直接显示聚合后的 `failed_runs`、`traceable_failed_runs` 与 `latest_failure_reason`。

现在这条评测路径也应该和附录里的更丰富验证器契约一起理解：对于长周期场景，这个包要帮助读者看到，数据集未来可以承载 `process_score`、`outcome_score`、`failure_attribution` 与已链接的验证器证据，而不只是一个单薄结论。

这些命令现在也更清楚地体现了第 16、17 章里的一个关键区分：

- 用来串起多次运行的用户可见 `session_id`；
- 用于排查和审计的单次运行 `trace_id`；
- 以及能力侧可能暂停、过期、恢复或需要重新初始化的会话状态。

这个参考包依然刻意保持很小，但它现在已经反映出：一个受治理的运行时有时必须把这三层状态分别讲清楚，而不是把它们压进同一个不透明对象里。

它现在也适合作为承接 Anthropic 新型运行框架经验的锚点：长时间运行的应用工作可能需要显式的上下文重置、结构化交接工件，以及规划器/生成器/评估器的角色分离，而不是一条不间断的智能体循环。这个参考包并没有把整套运行框架都实现出来，但它已经把那些关键运行时接缝暴露出来了，让团队能看见重置安全的交接、迭代契约、评估器评审与恢复后的控制状态应该落在什么地方。

它现在也适合作为验证器感知治理的锚点：如果发布或保障依赖评测输出，运行时就应该保留足够的追踪、会话与工件链接，来解释不只是发生了什么，还包括验证器为什么会这样判定这次运行。

这种能力也应延伸到生命周期处理。一个受治理的参考运行时应该能说明某次发布当时启用了哪一版验证器契约和哪一个发布身份，在退役之后还必须保留哪些证据，才能为早先的发布或保障决策提供解释，以及当某些结构化交接工件决定了即将退役系统被允许做什么时，这些工件必须如何跨过上下文重置或角色交接继续保留下来。

现在它也体现了第四个运营关注点：动作究竟是在什么委派授权上下文下执行的。这个上下文现在会出现在运行遥测、审批记录和会话导出里，让运行时不仅能解释发生了什么，还能解释它是在谁的委派身份与范围下发生的。

一个会真正读取用户画像记忆的请求：

```bash
.venv/bin/python -m agent_runtime_ref simulate-run --user-input "What language preference do you remember?"
```

## 如何验证

```bash
uv run ruff check .
uv run ty check
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing
```

## 示例配置

在 [configs](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref/configs) 目录里有运行时和生命周期的起步文件：

- [agent.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/agent.yaml)
- [policy.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/rollout.yaml)
- [controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/controls.yaml)
- [approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- [change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
  现在变更门禁里还有显式的 `failed_run_drill_checked` 和 `sandbox_profile_reviewed` 信号，避免高风险发布评审把退化路径或 sandbox profile 变更当成检查范围之外的东西。
- [artifacts.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/artifacts.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)
- [retirement.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/retirement.yaml)

它们现在已经不只是静态示例。`config.py` 可以把这些 YAML 加载进智能体身份、已批准能力清单、运行时、上下文层、记忆存储、上线策略、带有发布身份的生命周期工件以及其他生命周期状态，所以这个包已经更接近真实的运行骨架。

其中运行时控制包现在也被用来显式承载审批与会话治理规则，包括暂停/恢复、后台处理、过期、重新初始化策略、能力会话负责人，以及用户运行与能力侧会话之间的契约边界。

### 最小 sandbox profile

如果这个包以后扩展到由 sandbox 支撑的执行，正确起点不是一套庞大的新子系统，而是一个把 workspace 和权限显式化的小 profile：

```yaml
sandbox_profile:
  manifest_version: 1
  workspace:
    entries:
      - path: repo
        source: local_dir
        read_only: false
      - path: task.md
        source: inline_file
        read_only: true
  capabilities:
    filesystem: true
    shell: restricted
    memory: read_write
    skills: read_only
  permissions:
    network: denied
    secrets: none
    run_as: sandbox_user
  state:
    resume: allowed
    snapshot: required_on_completion
    persist_session_state: true
```

这个例子不会把参考运行时变成完整的沙箱编排器。它只是固定第 9 章和第 16 章要求真实由 sandbox 支撑的 runtime 暴露出来的契约表面：manifest、permissions、workspace materialization、session state，以及 snapshot/resume policy 都应该可以被 review。

## 为什么它有用

这本书现在不只依赖文档里的文字说明，也依赖真实的代码骨架：

- 更容易在文件和契约的层面讨论架构；
- 更容易继续往这个包里补充示例；
- 更容易从章节直接走到可运行的原型；
- 更容易展示配置驱动的路径，而不只是硬编码的演示；
- 更容易把参考运行时和记忆、检索、后台更新以及运行时控制治理这些章节连起来；
- 更容易讨论每条记忆是从哪里来的、它当前属于哪一个修订版，以及当时生效的是哪一个契约/运行时控制版本；
- 更容易把发布身份、验证器契约谱系与退役义务和运行时控制、工件决策放在一起看清楚；
- 更容易把审批状态、运行时会话状态、能力会话状态与验证器证据区分开来，同时仍保持它们之间的治理关联。

现在还有几项很实用的能力：

- `inspect-memory` 可以直接展示预置记忆，以及按 `tenant` 和 `memory_class` 过滤后的结果；
- `dump-events` 可以在不读源代码的情况下直接看到一次运行的结构化追踪；
- `export-events` 可以把这条追踪保存成 JSONL，便于脱离进程分析；
- `export-events` 现在会带上 `schema_version`，也支持按字段在导出时脱敏；
- 带有审批路径的 `export-events` 路径会发出 `sandbox_profile_reviewed`，让 trace evidence 与 lifecycle bundle 和 eval grading rule 对齐；
- `inspect-trace` 可以读取并筛选保存下来的追踪；
- `replay-run` 可以根据保存的 `run_start` 事件重新回放一次运行。

阅读这个包最简单的方式是：

- 用本书理解架构、顺序与运营模型论证；
- 用这个包查看可运行结构、配置表面与检查示例；
- 用附录 Schema 理解运行时想要明确表达的契约边界。

## 下一步做什么

- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [评测数据集 Schema 与打分契约](eval-schema.zh.md)
- [策略包 Schema 与审批契约](policy-bundle-schema.zh.md)
- [生命周期工件 Schema](lifecycle-artifact-schema.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
