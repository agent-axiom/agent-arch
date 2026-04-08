# Схема eval datasets и grading contract

Эта страница продолжает две соседние темы:

- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
- [Схема трасс и каталог событий](trace-schema.md)

И связывает их с runnable package:

- [Справочный пакет](reference-package.md)

Если страница про trace schema отвечает на вопрос “как описывать то, что произошло внутри run”, то эта страница отвечает на вопрос “как описывать то, что мы хотим от системы на уровне eval artifact”.

## Зачем нужна явная схема eval dataset

Очень многие команды говорят, что у них “есть evals”, но на практике под этим часто скрывается:

- таблица из нескольких ручных примеров;
- набор несвязанных prompt cases;
- JSON без стабильной структуры;
- смесь ground truth, ожиданий и комментариев в одном поле.

Это неудобно сразу по трем причинам:

- сравнения между версиями становятся мутными;
- regression gates трудно автоматизировать;
- trace grading и dataset grading живут как две разные вселенные.

Поэтому полезно думать об eval dataset как о контракте.

## Минимальная форма eval artifact

Для agent systems очень полезно, чтобы один dataset item содержал хотя бы:

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

Это уже гораздо полезнее, чем просто “вот пример запроса”.

## Почему labels недостаточно без expected outcomes

Labels помогают группировать сценарии:

- retrieval
- approval
- memory
- safety
- multi-turn

Но сами по себе labels ничего не говорят о том, что считается успешным поведением.

Поэтому eval dataset почти всегда должен разделять:

- `labels` как описание класса сценария;
- `expected_outcomes` как описание того, что должно получиться;
- `grading_rules` как описание того, как именно это проверяется.

## Что такое grading contract

Grading contract нужен, чтобы убрать двусмысленность между “примером” и “критерием прохождения”.

Практически это означает, что у сценария должно быть явно указано:

- какие поля мы вообще оцениваем;
- какой тип проверки применяется;
- что считается pass/fail;
- что можно считать warning, а что блокирующим нарушением.

Хороший grading contract отвечает на вопрос:

“Если завтра этот же сценарий проверит другой человек или другой pipeline, он придет к той же оценке?”

## Типы grading rules

Для reference-grade agent evals полезно различать хотя бы такие правила:

- `status_equals`
- `contains_substring`
- `max_tool_calls`
- `approval_required`
- `policy_violation_absent`
- `memory_write_absent`

То есть grading contract лучше строить не только вокруг текста ответа, но и вокруг поведения системы.

## Как это связано с traces

Полезная практическая модель такая:

- trace schema описывает фактическое поведение run;
- eval dataset schema описывает ожидаемое поведение;
- grading contract сопоставляет одно с другим.

Именно в этой точке observability становится не только способом смотреть назад, но и способом принимать release decisions.

## Что уже умеет reference runtime

В `agent_runtime_ref` команда:

```bash
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

уже дает небольшой structured artifact с:

- несколькими session scenarios;
- `labels`;
- `expected_outcomes`.

Это еще не полный industrial eval framework, но уже нормальная заготовка под:

- regression grading;
- scenario comparison;
- rollout review;
- ручное расширение eval set.

## Что стоит добавить в production dataset schema

Как только система становится серьезнее, полезно расширять dataset schema такими полями:

- `dataset_version`
- `scenario_owner`
- `source_trace_ids`
- `grader_type`
- `blocking`
- `notes_for_review`

Тогда eval artifact начинает жить не как временный JSON, а как часть release discipline.

## Пример grading contract

Ниже рабочий skeleton:

```yaml
scenario_id: support_ticket
labels:
  - write_path
  - approval_required
grading_rules:
  - type: status_equals
    expected: success
    blocking: true
  - type: contains_substring
    expected: waiting for human approval
    blocking: true
  - type: approval_required
    expected: true
    blocking: true
```

Смысл здесь в том, что contract оценивает не только финальный текст, но и правильную operational форму поведения.

## Почему multi-run sessions особенно важны

Для agent systems eval item довольно часто должен описывать не один запрос, а короткую серию связанных шагов.

Например:

1. пользователь просит создать ticket;
2. потом спрашивает, что агент помнит о его предпочтениях;
3. потом уточняет следующий шаг.

Если dataset не умеет описывать такую серию, ты неплохо тестируешь single-turn behavior, но слабо тестируешь session behavior.

Именно поэтому session exports и eval dataset exports полезно проектировать совместно.

## Чего не стоит делать

Есть несколько типичных ошибок:

- смешивать scenario metadata и grading logic в одном текстовом поле;
- хранить только happy path;
- не фиксировать expected outcomes явно;
- оценивать только финальный ответ и игнорировать policy/tool behavior;
- не версионировать dataset;
- не связывать dataset items с trace evidence или incident history.

Все это делает eval culture хрупкой.

## Практический чеклист

Если хочешь быстро понять, зрелая ли у тебя схема eval artifacts, пройди по вопросам:

- У каждого scenario есть стабильный `scenario_id`?
- Labels отделены от expected outcomes?
- Есть ли grading rules, а не только описания руками?
- Можно ли оценивать не только текст, но и behavior?
- Поддерживаются ли multi-run sessions?
- Есть ли dataset versioning и owner?

Если несколько ответов подряд “нет”, значит у тебя пока есть набор примеров, но еще нет нормальной eval dataset schema.

## См. также

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема policy bundle и approval contract](policy-bundle-schema.md)
- [Схема lifecycle-артефактов](lifecycle-artifact-schema.md)
- [Справочный пакет](reference-package.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
