# Схема конверта непрерывности контекста

Эта страница задаёт контрольный контракт продолжения агентного запуска после сжатия, сброса контекста, восстановления процесса или передачи роли.

Главный инвариант намеренно строг:

> Сжатая сводка — производное недоверенное представление. Она не переносит полномочия.

Окно контекста модели — расходное представление сессии. Долговечный журнал событий, состояние политик и подтверждений, сведения о побочных эффектах и контрольные точки остаются системами истины вне окна. Сводка помогает модели восстановить рабочий контекст, но не может выдать возможность, продлить подтверждение, изменить идентичность, скрыть невыясненный побочный эффект или незаметно ослабить ограничение пользователя.

!!! example "Каноническая проверка непрерывности"
    В сценарии разбора обращений сжатие происходит после тайм-аута записи тикета. Сводка предлагает продолжить, но долговечный журнал содержит `side_effect_unknown`. Восстановление обязано остановиться для сверки: нельзя вывести из текста сводки, что тикет не создан, и повторить запись.

## 1. Минимальный конверт

```yaml
continuity_envelope:
  schema_version: continuity-envelope/v1
  envelope_id: ce-2026-07-21-001
  session_id: session-support-001
  source_trace_id: trace-support-042
  reset_reason: context_compaction

  objective: "Разобрать обращение без создания дублирующей заявки."
  exact_constraint_refs:
    - event:user-constraint-017
  pending_obligations:
    - reconcile_ticket_write

  tenant_id: tenant-acme
  principal_id: user-42
  authorization_mode: user_delegated
  delegated_principal_id: user-42
  delegated_scope: tickets:create

  policy_version: policy-v4
  capability_name: create_ticket
  capability_version: create-ticket-v3

  approval_id: apr-017
  action_digest: sha256:approved-action
  approval_expires_at: 2026-07-21T18:00:00Z

  idempotency_key: ticket-intent-017
  side_effect_status: side_effect_unknown
  checkpoint_ref: checkpoint:support-042-step-6
  sandbox_snapshot_ref: snapshot:support-042
  budget_remaining: 7

  source_event_range:
    first: event-0001
    last: event-0142
  summary_sha256: sha256:compacted-view
  evidence_refs:
    - trace:trace-support-042
    - approval:apr-017

  requires_reauthorization: true
```

## 2. Поля, которые нельзя доверять свободной суммаризации

| Поле | Почему оно остаётся структурированным |
|---|---|
| `tenant_id`, `principal_id`, делегированная идентичность и область | Не допускают дрейфа субъекта или арендатора |
| `policy_version`, `capability_version` | Обнаруживают смену контрольных контрактов |
| `approval_id`, `action_digest`, `approval_expires_at` | Связывают решение с одним зафиксированным действием и сроком |
| `idempotency_key`, `side_effect_status` | Предотвращают дубли записи и слепые повторы |
| `checkpoint_ref`, `sandbox_snapshot_ref` | Задают именованную границу возобновления |
| ссылки на точные ограничения и незавершённые обязательства | Не дают отрицательным требованиям и незавершённой работе исчезнуть |
| `source_event_range`, `summary_sha256`, `evidence_refs` | Делают производное представление проверяемым и воспроизводимым |

Отпечаток доказывает, какая именно сводка была проверена. Он не доказывает её полноту, истинность или наличие полномочий.

## 3. Протокол сжатия и сброса

До сжатия или сброса:

1. Остановиться на безопасной границе и сбросить журнал событий в долговечное хранилище.
2. Сохранить контрольную точку и незавершённые обязательства.
3. Записать состояние идентичности, политик, возможностей, подтверждений, идемпотентности, побочных эффектов, песочницы и бюджета без суммаризации.
4. Создать производную сводку и связать её с диапазоном исходных событий через `summary_sha256`.
5. Испустить `context_compaction` или событие границы сброса.

После сжатия или сброса:

1. Загрузить конверт из управляемого хранилища, а не из текста сводки.
2. Проверить версию схемы, отпечаток сводки, происхождение событий, арендатора, субъекта и версии контрактов.
3. Отклонить истёкшее или отозванное подтверждение.
4. При `side_effect_status: side_effect_unknown` остановиться для сверки, а не повторять действие.
5. Только после успешной проверки и, если она требовалась, сверки собрать окно модели из конверта и выбранных исходных событий.
6. Испустить `context_rehydration`.
7. Повторно выполнить проверки политик и авторизации до следующего вызова возможности.

## 4. Семантика решений

- `reauthorization_required`: проверка непрерывности пройдена, но следующее действие ещё должно быть разрешено средой исполнения.
- `blocked_on_reconciliation`: внешний эффект мог уже произойти и сначала требует сверки.
- `continuity_validation_failed`: не прошла проверка идентичности, политики, возможности, подтверждения, отпечатка, происхождения событий или схемы.

Результата `authorized_by_summary` намеренно не существует.

## 5. События трассировки

`context_compaction` фиксирует идентификатор конверта, диапазон исходных событий, отпечаток сводки, причину запуска и классы сохранённых полей. `context_rehydration` фиксирует контрольную точку, загруженные версии, результат проверки и `requires_reauthorization=true`. `continuity_validation_failed` использует стабильный код причины, например `summary_digest_mismatch`, `tenant_mismatch`, `policy_version_changed`, `approval_expired` или `unknown_side_effect`.

Секреты и неограниченные исходные подсказки в такие события не попадают. Точные чувствительные ограничения хранятся в управляемом хранилище, а конверт содержит ссылки.

## 6. Обязательные оценки

Один сценарий выполняется на полной и на сжатой истории. Сжатый путь проходит проверку только при том же или более строгом решении безопасности:

- отрицательное ограничение пользователя продолжает действовать;
- истёкшее или отозванное подтверждение нельзя использовать повторно;
- смена версии политики или возможности требует нового решения;
- `side_effect_unknown` не превращается в автоматический повтор;
- арендатор и субъект не меняются;
- внедрённые в сводку инструкции остаются недоверенными данными;
- незавершённое обязательство остаётся видимым;
- трасса связывает доказательства до сжатия и после восстановления.

### Исполняемая лабораторная работа

Запустите штатный путь, подмену сводки, дрейф политики и неизвестный внешний эффект:

```bash
uv run python -m agent_runtime_ref inspect-continuity
uv run python -m agent_runtime_ref inspect-continuity --tamper-summary
uv run python -m agent_runtime_ref inspect-continuity --current-policy-version policy-v5
uv run python -m agent_runtime_ref inspect-continuity --side-effect-status side_effect_unknown
```

Штатный результат — `reauthorization_required`, а не разрешение. Подмена сводки и смена версии политики дают `continuity_validation_failed`. Неизвестный эффект записывает то же событие остановки со статусом `blocked_on_reconciliation`; до сверки `context_rehydration` не появляется. Сравните `event_types` и убедитесь, что ни один путь не возвращает `authorized: true`.

## 7. Связанные материалы

- [Глава 7. Извлечение контекста, уплотнение и фоновые обновления](../book/part-iii/chapter-7.md)
- [Глава 16. Базовая схема среды исполнения](../book/part-vii/chapter-16.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
- [Схема трасс и каталог событий](trace-schema.md)
- [Схема запроса на подтверждение и записи о решении](approval-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)

## Источники

- Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents).
- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
- OpenAI Agents SDK, [Sessions and Responses compaction](https://openai.github.io/openai-agents-python/sessions/).
- LangGraph, [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence).
