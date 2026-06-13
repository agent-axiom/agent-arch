# Схема наборов для оценки и правил проверки

Эта страница продолжает две соседние темы:

- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
- [Схема трасс и каталог событий](trace-schema.md)
- [Сквозная цепочка доказательств: от запроса к решению о раскатке](../book/part-v/evidence-spine.md)

И связывает их со справочным пакетом:

- [Эталонный пакет](reference-package.md)

Если страница о схеме трасс отвечает на вопрос «как описывать то, что произошло внутри запуска», то эта страница отвечает на вопрос «как описывать то, чего мы ожидаем от системы на уровне оценочного артефакта».

## Зачем нужна явная схема набора для оценки

Очень многие команды говорят, что у них «есть evals», но на практике под этим часто скрывается:

- таблица из нескольких ручных примеров;
- подборка несвязанных примеров для подсказок;
- JSON без устойчивой структуры;
- смесь эталонного ответа, ожиданий и комментариев в одном поле.

Это неудобно сразу по трем причинам:

- сравнения между версиями становятся мутными;
- регрессионные шлюзы трудно автоматизировать;
- проверка трасс и проверка набора живут как две разные вселенные.

Поэтому полезно мыслить набор для оценки как контракт.

## Минимальная форма оценочного артефакта

Для агентных систем очень полезно, чтобы один элемент набора содержал хотя бы:

- `scenario_id`
- `labels`
- `user_inputs`
- `expected_outcomes`
- `risk_class`

Минимальный пример выглядит так:

```json
{
  "scenario_id": "support_ticket",
  "labels": ["write_path", "approval_required", "ticketing"],
  "user_inputs": [
    "Please create a ticket for this onboarding issue."
  ],
  "expected_outcomes": {
    "latest_status": "success",
    "approval_wait_runs": 1,
    "required_output_substrings": [
      "waiting for human approval"
    ]
  },
  "risk_class": "high"
}
```

Это уже намного полезнее, чем просто «вот пример запроса».

## Почему меток недостаточно без ожидаемых результатов

Метки помогают группировать сценарии:

- retrieval
- approval
- memory
- safety
- multi-turn

Но сами по себе метки ничего не говорят о том, что считается успешным поведением.

Поэтому набор для оценки почти всегда должен разделять:

- `labels` как описание класса сценария;
- `expected_outcomes` как описание ожидаемого результата;
- `grading_rules` как описание того, как именно это проверяется;
- `verifier_outputs` как структурированный результат проверки, включая идентификатор проверяющего и версию контракта.

## Что такое правила проверки

Правила проверки нужны, чтобы убрать двусмысленность между «примером» и «критерием прохождения».

Практически это означает, что у сценария должно быть явно указано:

- какие поля мы вообще оцениваем;
- какой тип проверки применяется;
- что считается успехом или провалом;
- что можно считать предупреждением, а что блокирующим нарушением.

Хорошие правила проверки отвечают на вопрос:

«Если завтра этот же сценарий проверит другой человек или другой конвейер, он придет к той же оценке?»

## Типы правил проверки

Для справочных оценок агентных систем полезно различать хотя бы такие правила:

- `status_equals`
- `contains_substring`
- `max_tool_calls`
- `approval_required`
- `policy_violation_absent`
- `memory_write_absent`
- `process_score_present`
- `outcome_score_present`
- `failure_attribution_valid`
- `failed_run_traceable`
- `sandbox_profile_review`
- `stop_condition_verified`

`failed_run_traceable` становится важным, как только проверка выпуска начинает требовать тренировки неудачных запусков. Оно проверяет, что деградировавший путь не просто завершился неуспешно, а сохранил проверяемый статус, конкретную причину сбоя, например в поле `failure_reason`, связь с трассой и управляемую идентичность выпуска.

`sandbox_profile_review` нужен для путей с опорой на песочницу: он проверяет, что подготовка рабочего пространства, права оболочки и файловой системы, позиция по сети и секретам и политика снимка/возобновления были явно представлены как проверяемые доказательства, а не остались неявными настройками среды выполнения.

`stop_condition_verified` нужен для путей запуска агента, где результат нельзя принимать по свободному тексту “готово”. Он проверяет, что у сценария есть явное условие завершения, механизм проверки, результат проверки, исполнитель проверки и ссылки на доказательства: вывод теста, трассу, снимок экрана, diff или другой артефакт.

То есть правила проверки лучше строить не только вокруг текста ответа, но и вокруг поведения системы.

## Как это связано с трассами

Полезная практическая модель такая:

- схема трасс описывает фактическое поведение запуска;
- схема набора для оценки описывает ожидаемое поведение;
- правила проверки сопоставляют одно с другим.

Именно в этой точке наблюдаемость становится не только способом смотреть назад, но и способом принимать решения о выпуске.

## Что уже умеет эталонная среда исполнения

В `agent_runtime_ref` команда:

```bash
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

уже дает небольшой структурированный артефакт с:

- несколькими сценариями сессий;
- `labels`;
- `expected_outcomes`;
- отдельным сценарием тренировки неудачного запуска, который сохраняет failed status и `failure_reason` в экспорте сессии и ожидаемых результатах оценки.

Контракт пакетного экспорта намеренно конкретен. Проверка конфигурации сессионных оценок также отделяет некорректно сформированные спецификации оценки от неуспешных результатов оценки через `Session eval specs must be a mapping`, `Session eval spec must be a mapping`, `Session eval spec key must be a string`, `Session eval spec key must not be empty` и `Session eval spec keys must be unique`.

Контракт экспорта намеренно конкретен: значение `dataset_name` по умолчанию — `agent-runtime-ref-eval-seed`; верхнеуровневая сводка (`top-level summary`) включает `session_count`, `session_ids`, `run_count`, `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts` и `latest_failure_reason`; сценарии с ожиданием подтверждения также несут `approval_status_counts` в `expected_outcomes`; встроенные сценарии включают `failed_run_timeout` с меткой `duplicate_ticket_eval_passed`, `max_ticket_side_effects: 1` и блокирующим правилом проверки `duplicate_ticket_guard`, `profile_memory` с метками `memory_read`, `profile_lookup` и `grounded_answer`, `mixed_session` с метками `multi_run`, `approval_then_memory` и `session_evals`, плюс `required_run_count` как ожидаемый результат, а также `support_ticket` с меткой `sandbox_profile_review`, ожидаемым результатом `sandbox_profile_reviewed` и блокирующим правилом проверки `sandbox_profile_review`.

!!! example "Шлюз оценки для цепочки дубля тикета"
    Для сквозного кейса разбора обращений поддержки отдельная оценка должна воспроизводить тайм-аут после `create_ticket`, требовать сохраненные `trace_id` и `idempotency_key`, ожидать ровно один побочный эффект тикета или остановку `side_effect_unknown`, и блокировать раскатку, если новая версия подсказки, модели или адаптера снова делает слепой повтор и создает второй тикет.

!!! note "Канонические сценарии оценок"
    Набор оценок должен покрывать не только регрессию дублей тикетов. **Триаж обращений поддержки** проверяет шлюзы подтверждения, доказательства идемпотентности, поведение повторов и восстановление после дубля тикета. **Внутренний ассистент знаний** проверяет свежесть поиска, привязку к источникам, происхождение памяти, контроль доступа и качество ответа с опорой на источники. **Координация инцидентов** проверяет сроки эскалации, побочные эффекты уведомлений, владение ответом, качество передачи управления и регрессии обучения после инцидента.

Это еще не полноценный промышленный контур оценки, но уже нормальная заготовка для:

- регрессионной проверки;
- сравнения сценариев;
- проверки раскатки;
- ручного расширения набора.

## Что стоит добавить в промышленную схему набора

Как только система становится серьезнее, полезно расширять схему полями карточки решения проверяющего (`verifier verdict record`):

- `dataset_version`
- `scenario_owner`
- `source_trace_ids`
- `grader_type`
- `blocking`
- `notes_for_review`
- `verifier_outputs`
- `failure_attribution`
- `verdict_id`
- `verifier_id`
- `verifier_contract_version`
- `input_refs`
- `verifier_evidence_refs`
- `blocking_decision`
- `comparison_baseline`
- `reviewer_override`
- `sandbox_profile_contract`
- `workspace_manifest_ref`
- `snapshot_policy`
- `stop_condition`
- `verification_command`
- `verification_result`
- `verifier_actor`
- `evidence_refs`

Тогда оценочный артефакт начинает жить не как временный JSON, а как часть дисциплины выпуска.

### Критерии приемки вердикта проверяющего

Вердикт проверяющего можно считать контрактом, а не комментарием ревьюера, только если он проходит несколько проверок:

- у него есть стабильные `verdict_id`, `verifier_id` и `verifier_contract_version`;
- входы (`input_refs`) и доказательства (`verifier_evidence_refs` или `evidence_refs`) указывают на трассы, сценарии и версии политик;
- `process_score`, `outcome_score` и `failure_attribution` разделены и не схлопнуты в один ярлык;
- `blocking_decision`, `comparison_baseline` и `reviewer_override` объясняют, почему выпуск блокируется, предупреждается или пропускается;
- `stop_condition`, `verification_command`, `verification_result` и `verifier_actor` фиксируют, как именно проверено завершение запуска.

## Пример правил проверки

Ниже рабочий пример для сценария тренировки неудачного запуска:

```yaml
scenario_id: failed_run_timeout
labels:
  - failed_run
  - tool_timeout
  - failure_drill
grading_rules:
  - type: status_equals
    expected: failed
    blocking: true
  - type: contains_substring
    expected: tool_timeout
    blocking: true
  - type: failed_run_traceable
    expected: true
    blocking: true
  - type: sandbox_profile_review
    expected:
      sandbox_profile_contract: sandbox-profile-v1
      workspace_entries_reviewed: true
      permissions_profile: restricted-shell-network-denied
      network_secrets_posture: network:denied,secrets:none
      snapshot_policy: required_on_completion
    blocking: true
  - type: stop_condition_verified
    expected:
      stop_condition: no duplicate ticket side effect after timeout replay
      verification_command: .venv/bin/pytest tests/test_docs_surface.py
      verification_result: pass
      verifier_actor: deterministic_gate
      evidence_refs:
        - trace:trace_123
        - artifact:pytest-output
    blocking: true
verifier_outputs:
  verdict_id: verdict_failed_run_timeout_2026_05
  verifier_id: fara-process-review
  verifier_contract_version: verifier-v2
  input_refs:
    - scenario:failed_run_timeout
    - trace:trace_123
    - policy_bundle:policy-bundle-v3
  process_score: 0.92
  outcome_score: 0.35
  failure_attribution: uncontrollable_environment
  blocking_decision: warning_only
  comparison_baseline: release-2026-05-previous
  reviewer_override: none
  verifier_evidence_refs:
    - trace:trace_123
    - screenshot:step_7
```

Смысл здесь в том, что правила проверки оценивают не только финальный текст, но и правильную рабочую форму поведения, включая то, остается ли конкретное условие сбоя достаточно видимым для последующего разбора.

Это особенно важно для агентов с длинным горизонтом действий, где двоичная оценка успеха или провала часто скрывает разницу между корректным поведением с заблокированным итогом и небезопасным поведением, которое случайно закончилось номинальным успехом.

## Почему особенно важны многошаговые сессии

Для агентных систем элемент набора довольно часто должен описывать не один запрос, а короткую серию связанных шагов.

Например:

1. пользователь просит создать ticket;
2. потом спрашивает, что агент помнит о его предпочтениях;
3. потом уточняет следующий шаг.

Если набор не умеет описывать такую серию, ты неплохо проверяешь одиночный запрос, но слабо проверяешь поведение на уровне сессии.

Именно поэтому экспорт сессий и экспорт наборов для оценки полезно проектировать совместно.

## Чего не стоит делать

Есть несколько типичных ошибок:

- смешивать metadata сценария и логику проверки в одном текстовом поле;
- хранить только happy path;
- не фиксировать ожидаемые результаты явно;
- оценивать только финальный ответ и игнорировать поведение политики и инструментов;
- не версионировать набор;
- не связывать элементы набора с данными трасс или историей инцидентов;
- схлопывать verifier output в один слабый verdict без process/outcome split и failure attribution;
- требовать `sandbox_profile_review` в rollout, но не иметь grading rule, который проверяет workspace, permissions и snapshot/resume evidence;
- позволять агенту завершать задачу без `stop_condition_verified` и без доказательства, которое можно проверить после сессии.

Все это делает культуру оценки хрупкой.

## Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- У каждого сценария есть стабильный `scenario_id`?
- Метки отделены от ожидаемых результатов?
- Есть ли правила проверки, а не только описания от руки?
- Можно ли оценивать не только текст, но и поведение?
- Умеет ли verifier выдавать отдельно `process_score`, `outcome_score` и `failure_attribution`?
- Можно ли понять, какой идентификатор проверяющего и версия контракта породили эту итоговую оценку?
- Есть ли отдельное правило для путей с опорой на песочницу, которое проверяет контракт профиля песочницы, элементы рабочего пространства, права доступа и доказательства по снимку/возобновлению?
- Есть ли правило, которое проверяет stop condition, verification command/result, verifier actor и evidence refs для завершения запуска?
- Поддерживаются ли многошаговые сессии?
- Есть ли версионирование набора и владелец?

Если несколько ответов подряд «нет», значит у тебя пока есть набор примеров, но еще нет полноценной схемы для оценки.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Эталонный пакет](reference-package.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
