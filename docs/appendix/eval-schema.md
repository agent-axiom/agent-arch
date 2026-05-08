# Схема наборов для оценки и правил проверки

Эта страница продолжает две соседние темы:

- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
- [Схема трасс и каталог событий](trace-schema.md)
- [Сквозная цепочка доказательств: от запроса к решению о rollout](../book/part-v/evidence-spine.md)

И связывает их со справочным пакетом:

- [Справочный пакет](reference-package.md)

Если страница о схеме трасс отвечает на вопрос «как описывать то, что произошло внутри запуска», то эта страница отвечает на вопрос «как описывать то, чего мы ожидаем от системы на уровне оценочного артефакта».

## Зачем нужна явная схема набора для оценки

Очень многие команды говорят, что у них «есть evals», но на практике под этим часто скрывается:

- таблица из нескольких ручных примеров;
- набор несвязанных prompt-cases;
- JSON без устойчивой структуры;
- смесь ground truth, ожиданий и комментариев в одном поле.

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
- `verifier_outputs` как структурированный результат проверки, включая verifier identity и contract version.

## Что такое правила проверки

Правила проверки нужны, чтобы убрать двусмысленность между «примером» и «критерием прохождения».

Практически это означает, что у сценария должно быть явно указано:

- какие поля мы вообще оцениваем;
- какой тип проверки применяется;
- что считается pass/fail;
- что можно считать warning, а что блокирующим нарушением.

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

`failed_run_traceable` становится важным, как только release review начинает требовать failed-run drills. Оно проверяет, что деградировавший path не просто завершился неуспешно, а сохранил inspectable status, конкретную причину сбоя, например в поле `failure_reason`, trace linkage и управляемую release identity.

`sandbox_profile_review` нужен для sandbox-backed paths: он проверяет, что workspace materialization, shell/filesystem permissions, network/secrets posture и snapshot/resume policy были явно представлены как reviewable evidence, а не остались неявными runtime settings.

То есть правила проверки лучше строить не только вокруг текста ответа, но и вокруг поведения системы.

## Как это связано с трассами

Полезная практическая модель такая:

- схема трасс описывает фактическое поведение запуска;
- схема набора для оценки описывает ожидаемое поведение;
- правила проверки сопоставляют одно с другим.

Именно в этой точке наблюдаемость становится не только способом смотреть назад, но и способом принимать решения о выпуске.

## Что уже умеет справочный рантайм

В `agent_runtime_ref` команда:

```bash
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

уже дает небольшой структурированный артефакт с:

- несколькими сценариями сессий;
- `labels`;
- `expected_outcomes`;
- отдельным failed-run drill scenario, который сохраняет failed status и `failure_reason` в session export и eval expectations.

Bundled export contract намеренно конкретный: default `dataset_name` — `agent-runtime-ref-eval-seed`; top-level summary включает `session_count`, `run_count`, `failed_runs`, `traceable_failed_runs` и `latest_failure_reason`; built-in scenarios включают `failed_run_timeout`, `profile_memory` с labels `memory_read`, `profile_lookup` и `grounded_answer`, `mixed_session` с labels `multi_run`, `approval_then_memory` и `session_evals`, плюс `required_run_count` как expected outcome, а также `support_ticket` с label `sandbox_profile_review`, expected outcome `sandbox_profile_reviewed` и blocking `sandbox_profile_review` grading rule.

!!! example "Eval gate для duplicate-ticket thread"
    Для сквозного support-triage кейса отдельный eval должен воспроизводить timeout после `create_ticket`, требовать сохраненные `trace_id` и `idempotency_key`, ожидать ровно один ticket side effect или `side_effect_unknown` stop, и блокировать rollout, если новая prompt/model/adapter версия снова делает blind retry и создает второй тикет.

Это еще не полноценный промышленный контур оценки, но уже нормальная заготовка для:

- регрессионной проверки;
- сравнения сценариев;
- проверки раскатки;
- ручного расширения набора.

## Что стоит добавить в промышленную схему набора

Как только система становится серьезнее, полезно расширять схему такими полями:

- `dataset_version`
- `scenario_owner`
- `source_trace_ids`
- `grader_type`
- `blocking`
- `notes_for_review`
- `verifier_outputs`
- `failure_attribution`
- `verifier_id`
- `verifier_contract_version`
- `verifier_evidence_refs`
- `sandbox_profile_contract`
- `workspace_manifest_ref`
- `snapshot_policy`

Тогда оценочный артефакт начинает жить не как временный JSON, а как часть дисциплины выпуска.

## Пример правил проверки

Ниже рабочий skeleton для failed-run drill scenario:

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
verifier_outputs:
  verifier_id: fara-process-review
  verifier_contract_version: verifier-v2
  process_score: 0.92
  outcome_score: 0.35
  failure_attribution: uncontrollable_environment
  verifier_evidence_refs:
    - trace:trace_123
    - screenshot:step_7
```

Смысл здесь в том, что правила проверки оценивают не только финальный текст, но и правильную рабочую форму поведения, включая то, остается ли конкретное failed condition достаточно видимым для последующего разбора.

Это особенно важно для long-horizon agents, где binary pass/fail verdict часто скрывает разницу между корректным поведением с blocked outcome и unsafe behavior, которое случайно закончилось nominal success.

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
- требовать `sandbox_profile_review` в rollout, но не иметь grading rule, который проверяет workspace, permissions и snapshot/resume evidence.

Все это делает культуру оценки хрупкой.

## Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- У каждого сценария есть стабильный `scenario_id`?
- Метки отделены от ожидаемых результатов?
- Есть ли правила проверки, а не только описания от руки?
- Можно ли оценивать не только текст, но и поведение?
- Умеет ли verifier выдавать отдельно `process_score`, `outcome_score` и `failure_attribution`?
- Можно ли понять, какой verifier identity и contract version породили этот grading output?
- Есть ли отдельное правило для sandbox-backed paths, которое проверяет sandbox profile contract, workspace entries, permissions и snapshot/resume evidence?
- Поддерживаются ли многошаговые сессии?
- Есть ли версионирование набора и владелец?

Если несколько ответов подряд «нет», значит у тебя пока есть набор примеров, но еще нет полноценной схемы для оценки.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Справочный пакет](reference-package.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
