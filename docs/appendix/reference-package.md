# Опорный пакет

В репозитории теперь есть небольшой runnable skeleton: [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref).

Его задача не в том, чтобы стать production framework. Он нужен как минимальная кодовая опора для **Part VII** книги.

## Что внутри

- [runtime.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/runtime.py)
  Основной `AgentRuntime`, который собирает run context, retrieval, model step, tool execution и background update hook.
- [policy.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/policy.py)
  Маленький policy engine со structured decisions.
- [catalog.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/catalog.py)
  Capability registry с operational semantics.
- [config.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/config.py)
  YAML loader для policy, capability catalog и rollout policy.
- [memory.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/memory.py)
  Typed memory records, retrieval и tenant-scoped in-memory store.
- [background.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/background.py)
  Background maintenance path для persistent memory writes и compaction.
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
{"result": "Ticket request accepted and ready for follow-up.", "status": "success", "events": 9, "memory_records": 4, "config_dir": ".../agent_runtime_ref/configs"}
```

Явный запуск runtime через subcommand:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
```

Просмотр memory records:

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

Вывод structured events для одного run:

```bash
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
```

Проверка rollout policy с переопределением сигналов:

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

Запрос, который реально читает profile memory:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run --user-input "What language preference do you remember?"
```

## Как проверить

```bash
uv run ruff check .
uv run ty check
.venv/bin/python -m unittest discover -s tests
```

## Примерные конфиги

В [configs](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs) лежат четыре стартовых файла:

- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)

Теперь это уже не просто статические примеры. `config.py` умеет загружать эти YAML-файлы в runtime, policy engine, memory store и rollout policy, поэтому package стал ближе к реальному operational skeleton.

## Почему это полезно

Книга теперь опирается не только на Markdown-объяснения, но и на реальный кодовый skeleton:

- легче обсуждать архитектуру на уровне файлов и контрактов;
- легче расширять package следующими примерами;
- легче перейти от главы к runnable prototype;
- легче показать config-driven path, а не только hardcoded demo;
- легче связать reference runtime с главами про memory, retrieval и background updates.

Отдельно полезно то, что теперь package можно не только запускать, но и инспектировать снаружи:

- `inspect-memory` показывает seeded memory и фильтрацию по `tenant` и `memory_class`;
- `dump-events` показывает structured trace для одного run без чтения исходников.
