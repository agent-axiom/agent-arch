# Reference Package

В репозитории теперь есть небольшой runnable skeleton: [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref).

Его задача не в том, чтобы стать production framework. Он нужен как минимальная кодовая опора для **Part VII** книги.

## Что внутри

- [runtime.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/runtime.py)
  Основной `AgentRuntime`, который собирает run context, retrieval, model step, tool execution и background update hook.
- [policy.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/policy.py)
  Маленький policy engine со structured decisions.
- [catalog.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/catalog.py)
  Capability registry с operational semantics.
- [execution.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/execution.py)
  Простой dispatch capability через contract-aware execution.
- [telemetry.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/telemetry.py)
  In-memory telemetry emitter для structured events и spans.
- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
  Минимальный readiness gate перед rollout.

## Как запустить

```bash
.venv/bin/python -m agent_runtime_ref
```

Ожидаемый результат:

```json
{"result": "Ticket request accepted and ready for follow-up.", "rollout_ready": true}
```

## Как проверить

```bash
uv run ruff check .
uv run ty check
.venv/bin/python -m unittest discover -s tests
```

## Примерные конфиги

В [configs](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs) лежат три стартовых файла:

- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/capabilities.yaml)
- [rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)

Это не runtime loader и не финальный standard. Это просто компактные примеры того, как policy, catalog и rollout readiness выглядят в явной конфигурации.

## Зачем это полезно

Книга теперь опирается не только на Markdown-объяснения, но и на реальный кодовый skeleton:

- легче обсуждать архитектуру на уровне файлов и контрактов;
- легче расширять package следующими примерами;
- легче перейти от главы к runnable prototype.
