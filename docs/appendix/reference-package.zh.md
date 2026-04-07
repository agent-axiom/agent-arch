# 参考包

现在仓库里已经有一个可运行的小型代码骨架：[agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref)。

它的目标不是变成生产级框架，而是作为本书 **第七和第八部分** 的最小代码锚点。

这里是这个包的唯一主说明页面。README 里只保留简短的 quickstart，完整的 CLI、配置和结构说明都集中放在这里。

## 里面有什么

- [runtime.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/runtime.py)
  核心 `AgentRuntime`，负责组装运行上下文、检索、模型步骤、工具执行和后台更新钩子。
- [policy.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/policy.py)
  一个带结构化决策的小型策略引擎。
- [catalog.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/catalog.py)
  带有运行语义、风险等级和 egress 契约元数据的能力注册表。
- [identity.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/identity.py)
  智能体的显式身份，以及运行时被允许使用的已批准能力清单。
- [config.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/config.py)
  用来加载智能体身份、已批准能力清单、策略、能力目录和上线策略的 YAML 加载器。
- [memory.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/memory.py)
  类型化记忆记录、来源证明、修订号以及按租户隔离的内存存储。
- [background.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/background.py)
  负责持久化记忆写入、基于 provenance 的保存和压缩整理的后台维护路径。
- [execution.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/execution.py)
  一个通过契约感知执行来分发能力的简单层，同时考虑风险等级与 egress 策略。
- [telemetry.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/telemetry.py)
  用于结构化事件和跨度的内存遥测发射器。
- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
  上线前的最小就绪性闸门。
- [controls.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/controls.py)
  用于已批准注册表的 continuous controls 与 inventory drift 检查。
- [approvals.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/approvals.py)
  用于高风险动作的 approval gates 与简单 human review queue。
- [lifecycle.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/lifecycle.py)
  用于 change record、artifact bundle 和 retirement plan 的 lifecycle artifacts，以及这些状态的 readiness checks。

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

查看与 Part VIII 对应的 lifecycle artifacts：

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

把事件导出为 JSONL，方便后续排查和重放：

```bash
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
```

如果你需要给外部人员查看 redacted export，也可以在导出时直接隐藏敏感字段：

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

检查 continuous controls 和注册表 drift：

```bash
.venv/bin/python -m agent_runtime_ref check-controls --signal registry_reviewed=false
```

查看并处理 demo approval requests：

```bash
.venv/bin/python -m agent_runtime_ref inspect-approvals
.venv/bin/python -m agent_runtime_ref resolve-approval --decision approved --note "manager approved demo request"
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref session-eval-summary
.venv/bin/python -m agent_runtime_ref session-replay --user-input "Please create a ticket for this onboarding issue." --user-input "What language preference do you remember?"
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

`inspect-session` 会显示 session 级别的运行历史，以及关联的 `trace_id`。
`session-eval-summary` 会返回这一组运行的紧凑 operational summary。
`session-replay` 可以在同一个 `session_id` 里执行多个相关请求。
`export-session` 会把整段 session 保存成结构化 JSON，已经可以作为 offline eval 流程的种子数据。
`export-eval-dataset` 会把几个内置 session 场景打包成一个可直接用于 eval 的 JSON artifact。

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

在 [configs](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs) 目录里有 runtime 和 lifecycle 的起步文件：

- [agent.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/agent.yaml)
- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)
- [controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/controls.yaml)
- [approvals.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/approvals.yaml)
- [change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)
- [artifacts.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/artifacts.yaml)
- [retirement.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/retirement.yaml)

它们现在已经不只是静态示例了。`config.py` 可以把这些 YAML 加载进智能体身份、已批准能力清单、运行时、context layers、记忆存储、上线策略和 lifecycle artifacts，所以这个包已经更接近真实的运行骨架。

## 为什么它有用

这本书现在不只依赖文档里的文字说明，也依赖真实的代码骨架：

- 更容易在文件和契约的层面讨论架构；
- 更容易继续往这个包里加示例；
- 更容易从章节直接走到可运行的原型；
- 更容易展示配置驱动的路径，而不只是硬编码演示；
- 更容易把参考运行时和记忆、检索、后台更新这些章节连起来。
- 更容易讨论每条记忆是从哪里来的，以及它当前属于哪一个 revision。

现在还有一个很实用的改进：

- `inspect-memory` 可以直接展示预置记忆，以及按 `tenant` 和 `memory_class` 过滤后的结果；
- `dump-events` 可以在不读源代码的情况下，直接看到一次运行的结构化追踪；
- `export-events` 可以把这条追踪保存成 JSONL，便于脱离进程分析；
- `export-events` 现在会带上 `schema_version`，也支持按字段做 export-time redaction；
- `inspect-trace` 可以读取并筛选保存下来的追踪；
- `replay-run` 可以根据保存的 `run_start` 事件重新回放一次运行。
