# Google Doc chapter 13 trace evidence pass

Дата: 2026-06-26

Google Doc: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI

Цель прохода: выполнить 7-пунктовый editorial pass в рабочем Google Doc, превратить главу 13 из сжатой observability-сборки в более сильную главу про trace как цепочку доказательств после write-path, обновить DOCX-артефакты и подготовить следующие 100 редакционных итераций.

## Пункт 1. Проверка opening главы 13 после главы 12

Readback Google Doc подтвердил, что новая глава 13 начинается после выхода главы 12 и продолжает тот же сценарий `write-path`, `idempotency`, `side_effect_unknown`, rollback boundary и reconciliation.

Новый opening начинается с:

- `Глава 12 закончилась на write-path`;
- `В печатной главе trace не должен превращаться в полный каталог событий`;
- `1. Начнем не с логов, а с расследования одного сбоя`.

Смысловой переход стал таким: глава 12 объясняет, как runtime не должен слепо повторять опасную запись; глава 13 показывает, какие доказательства должны остаться после запуска, чтобы это можно было проверить.

## Пункт 2. Сжатие повторов trace/logs/events

В начале главы убран самостоятельный повтор observability-аргумента, который уже был подготовлен в предыдущих главах. Глава теперь быстрее переходит к расследованию сбоя с дублем тикета.

Ключевой тезис теперь формулируется так:

- logs остаются сырым материалом;
- trace описывает расследуемую историю одного запуска;
- structured events дают машинно проверяемые факты;
- полные event payloads не должны занимать основной печатный поток.

## Пункт 3. Нормализация терминов

Добавлено рабочее соглашение главы:

- `trace` - история одного запуска от входного намерения до исхода или остановки;
- `span` - осмысленный шаг внутри trace, где меняется ответственность, стоимость, риск или внешний эффект;
- `structured event` - машинночитаемый факт внутри trace или span;
- `session` - пользовательский или процессный контекст, который может породить несколько traces.

Это снижает риск, что `trace`, `span`, `event` и `session` будут использоваться как взаимозаменяемые слова.

## Пункт 4. Trace fields для write intent и control path

Раздел 8 заменен на минимальный набор полей для расследуемого trace. Поля разделены по смысловым группам:

- Identity: `trace_id`, `span_id`, `parent_span_id`, `run_id`, `session_id`, `tenant_id`, `principal_id`, `agent_id`;
- Intent: `intent_id`, `capability`, `risk_tier`, `requested_action`, `idempotency_key`;
- Control: `policy_decision_id`, `approval_id`, `approval_status`, `human_reviewer`, `policy_bundle_id`;
- Execution: `tool_name`, `tool_principal`, `external_request_id`, `result_class`, `duration_ms`, `retry_attempt`, `retry_budget_remaining`;
- Recovery: `side_effect_state`, `reconciliation_status`, `reconciliation_attempt_id`, `evidence_refs`, `final_verification_result`.

Локальный текстовый экспорт подтвердил, что эти поля находятся именно в body главы 13, а не только в ранних главах или приложениях.

## Пункт 5. Companion route для полных payloads

Добавлен отдельный route для главы 13:

`Companion route для главы 13: trace_envelope, span_contract, structured_event_catalog, tool_execution_event, policy_decision_event, approval_event, reconciliation_event, redaction_policy, event_schema_migration и trace_review_checklist.`

В печатной книге остаются минимальные excerpts: какие поля нужны для расследования, какие события обязательны и как trace связывает idempotency, policy, approval, tool outcome и reconciliation. Полные event schemas, JSON payload examples, OpenTelemetry mappings, exporter commands, validation messages, redaction rules, schema migration notes и dashboard examples должны жить в online companion.

## Пункт 6. Trace readiness checklist

Добавлен короткий checklist перед эксплуатацией:

1. Trace identity.
2. Write continuity.
3. Policy evidence.
4. Tool outcome.
5. Side-effect uncertainty.
6. Privacy boundary.
7. Schema stability.

Checklist фиксирует минимальную планку зрелости: по одному `trace_id` можно восстановить, что агент собирался сделать, кто разрешил действие, какой инструмент был вызван, какой внешний исход получен и какие доказательства остались после сверки.

## Пункт 7. Export and render QA

Созданы свежие DOCX-артефакты:

- raw Google Docs export: `docs/publisher/artifacts/agent-arch-ru-ch13-trace-pass-2026-06-26.docx`;
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch13-trace-pass-2026-06-26.docx`.

Raw export:

- page count: 616;
- blank-like pages: 0;
- zero-byte PNG pages: 0;
- targeted visual QA pages: 309, 312, 316, 320, 322;
- marker pages: body opening page 309, terminology page 312, trace fields page 316, readiness checklist page 320, companion route pages 321-322, body `Глава 14` page 322.

Template2000n derivative:

- page count: 308;
- blank-like pages: 0;
- zero-byte PNG pages: 0;
- targeted visual QA pages: 168, 171, 174, 175;
- marker pages: body opening page 168, terminology page 169, trace fields page 171, readiness checklist page 174, companion route and body `Глава 14` page 175.

Template2000n derivative был дополнительно поправлен на уровне OOXML: numbered question-list в opening главы 13 не должен становиться набором подзаголовков. После исправления список вопросов рендерится как список, а не как heading block.

## Что остается заполнить автору

Перед редакторской сдачей автор должен самостоятельно заполнить или подтвердить:

- `[Имя автора / публичное имя]`;
- `[текущая роль, специализация или независимое позиционирование]`;
- `[Имя автора]`;
- `[основная область: архитектура ИИ-агентов, платформенная инженерия, безопасность, продуктовая разработка, developer tooling]`;
- `Роль или должность`;
- `Ключевой опыт`;
- `Публичные проекты`;
- `Ссылки`;
- `Формулировка для издательства`;
- благодарности и dedication, если они нужны;
- публичный URL online companion;
- errata/contact channel;
- версию companion, соответствующую редакции книги.

## Следующий editorial focus

Следующие 100 итераций должны сместить фокус с локальной правки главы 13 на редакционную доводку главы 14, eval/rollout/lifecycle блоков, consistency pass, source/companion routing, author-owned front matter и final proof cycle.

