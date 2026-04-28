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
  用于高风险动作的审批门禁、暂停 / 恢复语义、简单人工评审队列，以及审批状态必须与能力会话状态保持一致的那层控制表面。

同一层运行时控制表面也天然适合承载委派授权假设：是谁委托了访问，这份授权能否跨过暂停 / 恢复继续有效，以及如果委派访问在动作完成前被撤销，运行时应该如何处理。

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

第二种形式是一个刻意保持很小的失败丰富场景。它让这个参考包能够展示，一条本来被允许的能力也可能以受治理的失败运行收尾，并留下明确的遥测，而不是被泛化成成功路径。

查看智能体身份与已批准能力清单：

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
```

查看与第八部分对应的生命周期工件，包括运行时控制链接和发布身份：

```bash
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref check-controls --signal policy_traces_present=false
.venv/bin/python -m agent_runtime_ref check-change --signal offline_eval_passed=false
.venv/bin/python -m agent_runtime_ref check-change --signal failed_run_drill_checked=false
.venv/bin/python -m agent_runtime_ref check-retirement --step revoke_egress=false
```

`inspect-lifecycle` 现在也会显示 `failed_run_archive_targets`、`controls.failed_run_control_expectations`、`controls.failed_run_control_domains`、`controls.failed_run_control_count`、`controls.failed_run_control_summary`、`controls.failed_run_control_status`、`controls.failed_run_control_review_required`、`controls.failed_run_control_owner`、`controls.failed_run_control_source`、`controls.failed_run_control_last_review` 和 `controls.failed_run_control_next_review`，这样操作员在同一个生命周期摘要里就能同时看到退化路径治理的保留侧面与追踪 / 来源证明控制侧面。
`check-change` 现在也会单独给出 `missing_failed_run_signals`，这样退化路径发布评审的缺口就不会被埋在普通缺失信号列表里。
`check-retirement` 现在也会显示 `failed_run_archive_targets`，这样操作员就能看到哪些遥测 / 会话 / 审批记录必须在退役之后继续保留下来，供后续退化路径评审使用。
`check-controls` 现在也会单独给出 `failed_run_controls`，同时列出 `preserved_failed_run_controls` 并输出 `failed_run_controls_healthy`，这样追踪 / 来源证明相关缺口就能和普通控制卫生分开审阅。

查看记忆记录：

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

现在 `inspect-memory` 不只显示内容，也会显示 `provenance` 和 `revision`。
`dump-events` 现在也会在 degraded-path drills 的 JSON 输出里返回 `failure_reason`。

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

带信号覆盖的上线策略检查：

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

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

`inspect-approvals` 现在也会显示 delegated authorization context，包括 `authorization_mode`、`delegated_principal_id` 与 `delegated_scope`，因此 approval path review 可以直接和 session evidence 对照。`resolve-approval` 在做出决定后也会返回同样的上下文，这样 acting-identity lineage 不会在 closure 阶段丢失。
`inspect-session` 会显示会话级别的运行历史，以及关联的 `trace_id`。现在这里也能直接注入 failed drill，而摘要会保留 `failed_runs`、`traceable_failed_runs`、`latest_failure_reason`，以及每次运行里的 `failure_reason`。
`session-eval-summary` 会返回这一组运行的紧凑摘要，其中也明确统计 failed runs 和 `traceable_failed_runs`，而不是又把结果压回只有 success 和 denied 两类。现在也可以直接在这里注入 failed drill，摘要会立刻显示 `latest_failure_reason` 便于快速复盘。
`session-replay` 可以在同一个 `session_id` 里执行多个相关请求。现在这里也能直接注入 failed drill，而 replay summary 会连同每次运行里的 `failure_reason` 一起保留 `failed_runs`、`traceable_failed_runs` 与 `latest_failure_reason`。
`export-session` 会把整段会话保存成结构化 JSON，已经可以作为离线评测流程的种子数据。现在它也会保留 delegated authorization context，例如 `authorization_mode`、`delegated_principal_id` 和 `delegated_scope`，同时在 CLI 命令摘要里直接显示 failed drills 的 `failed_runs`、`traceable_failed_runs` 与 `latest_failure_reason`。

现在，runtime 也会把工具路径中的失败类结果，例如 validation failure，当成一等运行结局来处理。它不再假装这次 run 仍然成功，而是记录 failed run、发出明确的 `run_failed` 事件，并在 session export 与 CLI output 中通过 `failure_reason` 字段同时保留这个状态以及具体失败原因。
`export-eval-dataset` 会把几个内置会话场景打包成一个可直接用于评测的 JSON 工件，其中也包括一个单独的 failed-run drill scenario，而命令摘要现在也会直接显示聚合后的 `failed_runs`、`traceable_failed_runs` 与 `latest_failure_reason`。

现在这条 eval path 也应该和 appendix 里的 richer verifier contract 一起理解：对于 long-horizon scenarios，这个包要帮助读者看到，dataset 未来可以承载 `process_score`、`outcome_score`、`failure_attribution` 与 linked verifier evidence，而不只是一个单薄 verdict。

这些命令现在也更清楚地体现了第 16、17 章里的一个关键区分：

- 用来串起多次 runs 的用户可见 `session_id`；
- 用于排查和审计的单次运行 `trace_id`；
- 以及 capability 一侧可能 pause、expire、resume 或需要 re-initialization 的 session state。

这个参考包依然刻意保持很小，但它现在已经反映出：一个受治理的 runtime 有时必须把这三层状态分别讲清楚，而不是把它们压进同一个不透明对象里。

它现在也适合作为承接 Anthropic 新 harness 经验的锚点：长时间运行的 application work 可能需要显式的 context resets、结构化 handoff artifacts，以及 planner/generator/evaluator 的角色分离，而不是一条不间断的 agent loop。这个参考包并没有把整套 harness 都实现出来，但它已经把那些关键 runtime seams 暴露出来了，让团队能看见 reset-safe handoff、sprint contracts、evaluator review 与 resumed control state 应该落在什么地方。

它现在也适合作为 verifier-aware governance 的锚点：如果 rollout 或 assurance 依赖 eval output，runtime 就应该保留足够的 trace、session 与 artifact linkage，来解释不只是发生了什么，还包括 verifier 为什么会这样判定这次 run。

这种能力也应延伸到 lifecycle handling。一个受治理的 reference runtime 应该能说明某次 release 当时启用了哪一版 verifier contract 和哪一个 release identity，在 retirement 之后还必须保留哪些 evidence，才能为早先的 rollout 或 assurance decisions 提供解释，以及当某些结构化 handoff artifacts 决定了即将退役系统被允许做什么时，这些工件必须如何跨过 context reset 或角色交接继续保留下来。

现在它也体现了第四个 operational concern：动作究竟是在什么 delegated authorization context 下执行的。这个上下文现在会出现在 run telemetry、approval records 和 session export 里，让 runtime 不仅能解释发生了什么，还能解释它是在谁的 delegated identity 与 scope 下发生的。

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
  现在 change gate 里还有一个显式的 `failed_run_drill_checked` 信号，避免 high-risk rollout review 把退化路径当成检查范围之外的东西。
- [artifacts.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/artifacts.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)
- [retirement.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/retirement.yaml)

它们现在已经不只是静态示例。`config.py` 可以把这些 YAML 加载进智能体身份、已批准能力清单、运行时、上下文层、记忆存储、上线策略、带有 release identity 的生命周期工件以及其他生命周期状态，所以这个包已经更接近真实的运行骨架。

其中 runtime-control bundle 现在也被用来显式承载 approval 与 session-governance 规则，包括 pause/resume、background handling、expiry、re-init policy、capability-session ownership，以及 user run 与 capability-side session 之间的契约边界。

## 为什么它有用

这本书现在不只依赖文档里的文字说明，也依赖真实的代码骨架：

- 更容易在文件和契约的层面讨论架构；
- 更容易继续往这个包里补充示例；
- 更容易从章节直接走到可运行的原型；
- 更容易展示配置驱动的路径，而不只是硬编码的演示；
- 更容易把参考运行时和记忆、检索、后台更新以及 runtime-control governance 这些章节连起来；
- 更容易讨论每条记忆是从哪里来的、它当前属于哪一个 revision，以及当时生效的是哪一个 contract/runtime-control version；
- 更容易把 release identity、verifier-contract lineage 与 retirement obligations 和 runtime-control、artifact decisions 放在一起看清楚；
- 更容易把 approval state、runtime session state、capability session state 与 verifier evidence 区分开来，同时仍保持它们之间的治理关联。

现在还有几项很实用的能力：

- `inspect-memory` 可以直接展示预置记忆，以及按 `tenant` 和 `memory_class` 过滤后的结果；
- `dump-events` 可以在不读源代码的情况下直接看到一次运行的结构化追踪；
- `export-events` 可以把这条追踪保存成 JSONL，便于脱离进程分析；
- `export-events` 现在会带上 `schema_version`，也支持按字段在导出时脱敏；
- `inspect-trace` 可以读取并筛选保存下来的追踪；
- `replay-run` 可以根据保存的 `run_start` 事件重新回放一次运行。

阅读这个包最简单的方式是：

- 用本书理解 architecture、sequence 与 operating-model argument；
- 用这个包查看 runnable structure、config surfaces 与 inspection examples；
- 用 appendix schemas 理解 runtime 想要明确表达的 contract boundaries。

## 下一步做什么

- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [评测数据集 Schema 与打分契约](eval-schema.zh.md)
- [策略包 Schema 与审批契约](policy-bundle-schema.zh.md)
- [生命周期工件 Schema](lifecycle-artifact-schema.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
