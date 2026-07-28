# Runtime reference companion: traces and events

Статус: companion-материал к русской издательской рукописи.

Эта страница хранит техническую карту trace/event surfaces для `agent_runtime_ref`. В книге trace объясняется как доказательная модель: кто действовал, какая policy сработала, какое approval было нужно, какой tool был вызван, что вернул verifier и почему rollout можно или нельзя расширять. Здесь остаются поля, команды и проверяемые события.

## Где смотреть исходники

- Telemetry model: `agent_runtime_ref/telemetry.py`
- Runtime execution: `agent_runtime_ref/runtime.py`, `agent_runtime_ref/execution.py`
- CLI export: `agent_runtime_ref/__main__.py`
- Тесты trace/export: `tests/test_agent_runtime_ref.py`
- Печатная привязка: главы 13-15 и глава 23

## Минимальный event chain

Для рискованного write-path trace должен восстанавливать цепочку:

```yaml
required_events:
  - run_start
  - policy_precheck
  - capability_selected
  - tool_policy_decision
  - approval_requested
  - approval_resolved
  - tool_execution
  - verification_result
  - run_complete
```

Если запуск завершился отказом или неизвестным side effect, trace должен сохранить failure reason и recovery context, а не только финальный статус.

## Поля, которые нельзя терять

```yaml
trace_core_fields:
  trace_id: required
  session_id: required_for_multi_run
  tenant_id: required_for_isolation
  agent_id: required
  principal_id: required
  capability_name: required_when_tool_related
  idempotency_key: required_for_write_path
  approval_id: required_when_approval_related
  capability_session_id: required_when_capability_session_exists
  delegated_principal_id: required_when_user_delegated
  schema_version: required_for_exports
```

## Export workflow

```bash
.venv/bin/python -m agent_runtime_ref dump-events
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/events.jsonl
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/events.jsonl
```

Проверка отказа:

```bash
.venv/bin/python -m agent_runtime_ref export-events \
  --simulate-failure tool_timeout \
  --output artifacts/events-timeout.jsonl

.venv/bin/python -m agent_runtime_ref inspect-trace \
  --input artifacts/events-timeout.jsonl
```

## Example artifacts

Generated trace examples:

- `docs/companion/artifacts/trace-demo.jsonl`
- `docs/companion/artifacts/trace-failed-tool-timeout.jsonl`
- `docs/companion/artifacts/trace-post-dispatch-timeout.jsonl`

Verification commands:

```bash
uv run python -m agent_runtime_ref inspect-trace \
  --input docs/companion/artifacts/trace-demo.jsonl

uv run python -m agent_runtime_ref inspect-trace \
  --input docs/companion/artifacts/trace-failed-tool-timeout.jsonl

uv run python -m agent_runtime_ref inspect-trace \
  --input docs/companion/artifacts/trace-post-dispatch-timeout.jsonl
```

The two degraded traces distinguish a known pre-dispatch failure from an
unknown post-dispatch effect. The latter requires reconciliation and must not be
retried blindly.

## Redaction and schema versioning

Trace export должен поддерживать:

- `schema_version`;
- redaction selected fields;
- redacted summaries;
- replay preservation;
- validation errors for unsupported schema versions;
- explicit trace id selection when a file contains multiple trace ids.

## Validation messages

Полный validation-message catalog должен жить в companion, потому что он быстро меняется и перегружает печатную книгу. В книге достаточно назвать классы ошибок:

- missing required trace field;
- unsupported schema version;
- trace id not found;
- ambiguous trace id;
- missing run_start;
- malformed event payload;
- unsupported tool result shape.

## Связь с evals and rollout

Trace становится полезным для release decision только когда он связан с eval gate:

```yaml
trace_to_release_chain:
  source_trace: trace-support-042
  incident_class: duplicate_ticket_after_timeout
  eval_gate: support_duplicate_ticket_after_timeout
  verifier_contract: support-write-safety-v1
  rollout_judgment: chg-support-write-path-2026-06
```

Эта цепочка должна быть видна в companion-материалах и защищена тестами поверхности.
