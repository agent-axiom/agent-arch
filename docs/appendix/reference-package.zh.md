# 参考包

现在仓库里已经有一个可运行的小型 skeleton：[agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref)。

它的目标不是变成 production framework，而是作为本书 **Part VII** 的最小代码锚点。

## 里面有什么

- [runtime.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/runtime.py)
  核心 `AgentRuntime`，负责组装 run context、retrieval、model step、tool execution 和 background update hook。
- [policy.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/policy.py)
  一个带 structured decisions 的小型 policy engine。
- [catalog.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/catalog.py)
  带有 operational semantics 的 capability registry。
- [config.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/config.py)
  用来加载 policy、capability catalog 和 rollout policy 的 YAML loader。
- [memory.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/memory.py)
  Typed memory records、retrieval 和按 tenant 隔离的 in-memory store。
- [background.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/background.py)
  负责 persistent memory writes 和 compaction 的 background maintenance path。
- [execution.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/execution.py)
  一个通过 contract-aware execution 做 capability dispatch 的简单层。
- [telemetry.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/telemetry.py)
  用于 structured events 和 spans 的 in-memory telemetry emitter。
- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
  rollout 前的最小 readiness gate。

## 如何运行

```bash
.venv/bin/python -m agent_runtime_ref
```

预期输出：

```json
{"result": "Ticket request accepted and ready for follow-up.", "status": "success", "events": 9, "memory_records": 4, "config_dir": ".../agent_runtime_ref/configs"}
```

通过显式 subcommand 运行 runtime：

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
```

查看 memory records：

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

导出一次 run 的 structured events：

```bash
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
```

带 signal override 的 rollout policy 检查：

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

一个会真正读取 profile memory 的请求：

```bash
.venv/bin/python -m agent_runtime_ref simulate-run --user-input "What language preference do you remember?"
```

## 如何验证

```bash
uv run ruff check .
uv run ty check
.venv/bin/python -m unittest discover -s tests
```

## 示例配置

在 [configs](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs) 目录里有四个起步文件：

- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)

它们现在已经不只是静态示例了。`config.py` 可以把这些 YAML 加载进 runtime、policy engine、memory store 和 rollout policy，所以这个 package 已经更接近真实的 operational skeleton。

## 为什么它有用

这本书现在不只依赖 Markdown 解释，也依赖真实的代码 skeleton：

- 更容易在文件和 contracts 的层面讨论架构；
- 更容易继续往 package 里加示例；
- 更容易从章节直接走到 runnable prototype；
- 更容易展示 config-driven path，而不只是 hardcoded demo；
- 更容易把 reference runtime 和 memory、retrieval、background updates 这些章节连起来。

现在还有一个很实用的改进：

- `inspect-memory` 可以直接展示 seeded memory，以及按 `tenant` 和 `memory_class` 过滤后的结果；
- `dump-events` 可以在不读源代码的情况下，直接看到一次 run 的 structured trace。
