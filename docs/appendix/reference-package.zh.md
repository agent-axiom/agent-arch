# 参考包

现在仓库里已经有一个可运行的小型代码骨架：[agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref)。

它的目标不是变成生产级框架，而是作为本书 **第七和第八部分** 的最小代码锚点。

这里是这个包的主说明页面。README 里只保留简短的上手说明，完整的命令行、配置和结构说明都集中放在这里。

一个实用的阅读路径是：

- 第 16 章看 baseline runtime 与 capability session state，
- 第 17 章看 policy layer 与 capability contracts，
- 第 18 章看围绕 approval 和 runtime behavior 的 rollout gates，
- 第 21 章看 assurance response，
- 第 22 章配合 lifecycle schema 看 governed artifact linkage、verifier-contract lineage 与 delegated authorization provenance，
- 第 23 到 27 章看 capability sessions 周围的 interruption、expiry、re-init、retirement、observability、registry ownership、verifier-evidence obligations 与 delegated-authorization lifecycle control。

## 里面有什么

- [runtime.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/runtime.py)
  核心 `AgentRuntime`，负责组装运行上下文、检索、模型步骤、工具执行和后台更新钩子。
- [policy.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/policy.py)
  一个带结构化决策的小型策略引擎。
- [catalog.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/catalog.py)
  带有运行语义、风险等级和出口契约元数据的能力注册表。
- [identity.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/identity.py)
  智能体的显式身份，以及运行时被允许使用的已批准能力清单。
- [config.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/config.py)
  用来加载智能体身份、已批准能力清单、策略、能力目录和上线策略的 YAML 加载器。
- [memory.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/memory.py)
  类型化记忆记录、来源证明、修订号以及按租户隔离的内存存储。
- [background.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/background.py)
  负责持久化记忆写入、基于来源证明的保存，以及压缩整理的后台维护路径。
- [execution.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/execution.py)
  一个按契约分发能力的简单执行层，同时考虑风险等级与出口策略。
- [telemetry.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/telemetry.py)
  用于结构化事件和跨度的内存遥测发射器。
- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
  上线前的最小就绪性闸门。
- [controls.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/controls.py)
  用于已批准注册表的持续控制与清单漂移检查。
- [approvals.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/approvals.py)
  用于高风险动作的审批门禁、pause/resume semantics、简单人工评审队列，以及 approval state 必须与 capability session state 保持一致的那层 control surface。

同一层 runtime-control surface 也天然适合承载 delegated authorization assumptions：是谁委托了访问，这份授权能否跨过 pause/resume 继续有效，以及如果 delegated access 在动作完成前被撤销，runtime 应该如何处理。
- [lifecycle.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/lifecycle.py)
  用于 change record、artifact bundle、runtime-control schemas、verifier-contract lineage 和 retirement plan 的生命周期工件，以及这些状态的就绪检查。

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
```

查看智能体身份与已批准能力清单：

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
```

查看与第八部分对应的生命周期工件，包括 runtime-control linkage：

```bash
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref check-change --signal offline_eval_passed=false
.venv/bin/python -m agent_runtime_ref check-retirement --step revoke_egress=false
```

查看记忆记录：

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

现在 `inspect-memory` 不只显示内容，也会显示 `provenance` 和 `revision`。

导出一次运行的结构化事件：

```bash
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
```

把事件导出为 JSONL，方便后续排查和回放：

```bash
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
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
.venv/bin/python -m agent_runtime_ref session-eval-summary
.venv/bin/python -m agent_runtime_ref session-replay --user-input "Please create a ticket for this onboarding issue." --user-input "What language preference do you remember?"
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

`inspect-session` 会显示会话级别的运行历史，以及关联的 `trace_id`。
`session-eval-summary` 会返回这一组运行的紧凑摘要。
`session-replay` 可以在同一个 `session_id` 里执行多个相关请求。
`export-session` 会把整段会话保存成结构化 JSON，已经可以作为离线评测流程的种子数据。现在它也会保留 delegated authorization context，例如 `authorization_mode`、`delegated_principal_id` 和 `delegated_scope`。
`export-eval-dataset` 会把几个内置会话场景打包成一个可直接用于评测的 JSON 工件。

现在这条 eval path 也应该和 appendix 里的 richer verifier contract 一起理解：对于 long-horizon scenarios，这个包要帮助读者看到，dataset 未来可以承载 `process_score`、`outcome_score`、`failure_attribution` 与 linked verifier evidence，而不只是一个单薄 verdict。

这些命令现在也更清楚地体现了第 16、17 章里的一个关键区分：

- 用来串起多次 runs 的用户可见 `session_id`；
- 用于排查和审计的单次运行 `trace_id`；
- 以及 capability 一侧可能 pause、expire、resume 或需要 re-initialization 的 session state。

这个参考包依然刻意保持很小，但它现在已经反映出：一个受治理的 runtime 有时必须把这三层状态分别讲清楚，而不是把它们压进同一个不透明对象里。

它现在也适合作为 verifier-aware governance 的锚点：如果 rollout 或 assurance 依赖 eval output，runtime 就应该保留足够的 trace、session 与 artifact linkage，来解释不只是发生了什么，还包括 verifier 为什么会这样判定这次 run。

这种能力也应延伸到 lifecycle handling。一个受治理的 reference runtime 应该能说明某次 release 当时启用了哪一版 verifier contract，以及在 retirement 之后还必须保留哪些 evidence，才能为早先的 rollout 或 assurance decisions 提供解释。

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

在 [configs](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs) 目录里有运行时和生命周期的起步文件：

- [agent.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/agent.yaml)
- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)
- [controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/controls.yaml)
- [approvals.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/approvals.yaml)
- [change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)
- [artifacts.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/artifacts.yaml)
- [runtime-controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/runtime-controls.yaml)
- [retirement.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/retirement.yaml)

它们现在已经不只是静态示例。`config.py` 可以把这些 YAML 加载进智能体身份、已批准能力清单、运行时、上下文层、记忆存储、上线策略和生命周期工件，所以这个包已经更接近真实的运行骨架。

其中 runtime-control bundle 现在也被用来显式承载 approval 与 session-governance 规则，包括 pause/resume、background handling、expiry、re-init policy、capability-session ownership，以及 user run 与 capability-side session 之间的契约边界。

## 为什么它有用

这本书现在不只依赖文档里的文字说明，也依赖真实的代码骨架：

- 更容易在文件和契约的层面讨论架构；
- 更容易继续往这个包里补充示例；
- 更容易从章节直接走到可运行的原型；
- 更容易展示配置驱动的路径，而不只是硬编码的演示；
- 更容易把参考运行时和记忆、检索、后台更新以及 runtime-control governance 这些章节连起来；
- 更容易讨论每条记忆是从哪里来的、它当前属于哪一个 revision，以及当时生效的是哪一个 contract/runtime-control version；
- 更容易把 verifier-contract lineage 与 retirement obligations 和 runtime-control、artifact decisions 放在一起看清楚；
- 更容易把 approval state、runtime session state、capability session state 与 verifier evidence 区分开来，同时仍保持它们之间的治理关联。

现在还有几项很实用的能力：

- `inspect-memory` 可以直接展示预置记忆，以及按 `tenant` 和 `memory_class` 过滤后的结果；
- `dump-events` 可以在不读源代码的情况下直接看到一次运行的结构化追踪；
- `export-events` 可以把这条追踪保存成 JSONL，便于脱离进程分析；
- `export-events` 现在会带上 `schema_version`，也支持按字段在导出时脱敏；
- `inspect-trace` 可以读取并筛选保存下来的追踪；
- `replay-run` 可以根据保存的 `run_start` 事件重新回放一次运行。

## 下一步做什么

- [追踪模式与事件目录](trace-schema.zh.md)
- [评测数据集模式与分级契约](eval-schema.zh.md)
- [策略包模式与审批契约](policy-bundle-schema.zh.md)
- [生命周期工件规范](lifecycle-artifact-schema.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
