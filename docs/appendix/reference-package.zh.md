# 参考包

现在仓库里已经有一个可运行的小型代码骨架：[agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref)。

它的目标不是变成生产级框架，而是作为本书 **第七部分** 的最小代码锚点。

## 里面有什么

- [runtime.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/runtime.py)
  核心 `AgentRuntime`，负责组装运行上下文、检索、模型步骤、工具执行和后台更新钩子。
- [policy.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/policy.py)
  一个带结构化决策的小型策略引擎。
- [catalog.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/catalog.py)
  带有运行语义的能力注册表。
- [config.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/config.py)
  用来加载策略、能力目录和上线策略的 YAML 加载器。
- [memory.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/memory.py)
  类型化记忆记录、检索和按租户隔离的内存存储。
- [background.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/background.py)
  负责持久化记忆写入和压缩整理的后台维护路径。
- [execution.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/execution.py)
  一个通过契约感知执行来分发能力的简单层。
- [telemetry.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/telemetry.py)
  用于结构化事件和跨度的内存遥测发射器。
- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
  上线前的最小就绪性闸门。

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

查看记忆记录：

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

导出一次运行的结构化事件：

```bash
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
```

带信号覆盖的上线策略检查：

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

一个会真正读取用户画像记忆的请求：

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

它们现在已经不只是静态示例了。`config.py` 可以把这些 YAML 加载进运行时、策略引擎、记忆存储和上线策略，所以这个包已经更接近真实的运行骨架。

## 为什么它有用

这本书现在不只依赖文档里的文字说明，也依赖真实的代码骨架：

- 更容易在文件和契约的层面讨论架构；
- 更容易继续往这个包里加示例；
- 更容易从章节直接走到可运行的原型；
- 更容易展示配置驱动的路径，而不只是硬编码演示；
- 更容易把参考运行时和记忆、检索、后台更新这些章节连起来。

现在还有一个很实用的改进：

- `inspect-memory` 可以直接展示预置记忆，以及按 `tenant` 和 `memory_class` 过滤后的结果；
- `dump-events` 可以在不读源代码的情况下，直接看到一次运行的结构化追踪。
