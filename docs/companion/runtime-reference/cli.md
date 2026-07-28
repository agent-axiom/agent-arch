# Runtime reference companion: CLI

Статус: companion-материал к русской издательской рукописи.

Эта страница хранит команды и ожидаемые поверхности CLI для `agent_runtime_ref`. В печатной книге остаются причины, риски и архитектурные решения; здесь остаются команды, которые удобно запускать, обновлять и проверять вместе с репозиторием.

## Где смотреть исходники

- CLI entrypoint: `agent_runtime_ref/__main__.py`
- README: `agent_runtime_ref/README.md`, `README.ru.md`
- Тесты CLI: `tests/test_agent_runtime_ref.py`
- Печатная привязка: главы 21-23 и приложение про online companion

## Базовая проверка

```bash
uv run pytest
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing
```

Если используется локальная виртуальная среда:

```bash
.venv/bin/python -m agent_runtime_ref
.venv/bin/python -m agent_runtime_ref simulate-run
```

## Команды обзора runtime

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
.venv/bin/python -m agent_runtime_ref inspect-memory
.venv/bin/python -m agent_runtime_ref inspect-approvals
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
```

Эти команды должны отвечать на разные вопросы:

- `inspect-agent`: какая identity, principal и approved inventory используются;
- `inspect-memory`: какие memory records доступны и как работает фильтрация;
- `inspect-approvals`: какие approvals созданы, ожидают решения или закрыты;
- `inspect-session`: какие runs связаны с session и trace ids;
- `inspect-lifecycle`: какие lifecycle artifacts связаны с runtime и rollout.

## Команды trace export

```bash
.venv/bin/python -m agent_runtime_ref dump-events
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/events.jsonl
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/events.jsonl
```

Для проверки отказа:

```bash
.venv/bin/python -m agent_runtime_ref export-events \
  --simulate-failure tool_timeout \
  --output artifacts/events-timeout.jsonl

.venv/bin/python -m agent_runtime_ref inspect-trace \
  --input artifacts/events-timeout.jsonl
```

## Команды session and eval export

```bash
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref inspect-session --simulate-failure tool_timeout
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset \
  --scenario failed_run_timeout \
  --output artifacts/eval-failed-run.json
```

## Example artifacts in this companion

The current companion includes generated examples that can be inspected from
the repository root:

```bash
uv run python -m agent_runtime_ref inspect-trace \
  --input docs/companion/artifacts/trace-demo.jsonl

uv run python -m agent_runtime_ref inspect-trace \
  --input docs/companion/artifacts/trace-failed-tool-timeout.jsonl

uv run python -m agent_runtime_ref inspect-trace \
  --input docs/companion/artifacts/trace-post-dispatch-timeout.jsonl

python3 -m json.tool docs/companion/artifacts/session-failed-tool-timeout.json
python3 -m json.tool docs/companion/artifacts/eval-failed-run-timeout.json
python3 -m json.tool docs/companion/artifacts/eval-unknown-effect-reconciliation.json
```

## Что считать успешной CLI-поверхностью

CLI годится для companion, если команда:

- возвращает структурированный JSON, а не только человекочитаемый текст;
- сохраняет `trace_id`, `session_id`, `tenant_id`, `agent_id` и `idempotency_key`, если они относятся к сценарию;
- показывает approval status и pending approval ids для write-path;
- умеет экспортировать артефакт в файл, который можно положить в eval или incident review;
- имеет тест, который защищает поля от случайного исчезновения.

## Что остается в книге

В печатной книге достаточно показать, зачем эти команды нужны:

- runtime должен быть наблюдаемым без чтения исходников;
- trace export превращает запуск в доказательство;
- session export помогает связать несколько runs в один разбор;
- eval export делает инцидент материалом для regression gate.

Полные ключи, варианты CLI и ожидаемые payload лучше держать здесь.
