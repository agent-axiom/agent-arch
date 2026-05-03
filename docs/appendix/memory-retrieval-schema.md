# Схема записей памяти и контракта извлечения

Эта страница собирает в одном месте минимальный контрактный слой для памяти и извлечения в агентных системах: какие поля должны быть у записи памяти и запроса на извлечение и какие гарантии нужны, чтобы память не превращалась в неуправляемый источник утечек, шума и ложной уверенности.

Если [схема трасс и каталог событий](trace-schema.md) отвечает на вопрос «как это видно в телеметрии», а [схема lifecycle-артефактов](lifecycle-artifact-schema.md) отвечает на вопрос «что считается управляемым рабочим артефактом», то эта схема отвечает на вопрос «какие именно записи и фильтры вообще допустимы в слое памяти».

## 1. Зачем нужен отдельный слой схем

Очень частая ошибка с памятью устроена так:

- агент что-то запомнил;
- извлечение что-то вернуло;
- дальше команда уже не может уверенно ответить:
  - что это была за запись;
  - откуда она взялась;
  - кто имел право ее читать;
  - по каким правилам она попала в prompt.

Поэтому слой памяти полезно описывать не как «у нас есть vector store», а как набор типизированных записей и типизированных правил извлечения.

## 2. Базовые сущности

Минимальный слой здесь удобно строить вокруг трех сущностей:

- `memory_record`
- `retrieval_query`
- `retrieval_result`

Этого уже достаточно, чтобы связать главы 5-7, слой политик, схему трасс и справочный рантайм.

## 3. Запись памяти

`memory_record` описывает одну конкретную запись в слое памяти.

```yaml
kind: memory_record
record_id: mem-tenant-acme-001
tenant_id: tenant-acme
memory_class: profile
key: preferred_language
value: English
source: user_confirmed_preference
provenance: user_confirmed_preference
revision: 1
trust_level: high
created_at: 2026-04-07T12:00:00Z
retention: long_term
```

Что здесь важно:

- `tenant_id` не дает извлечению пересекать границы арендаторов;
- `memory_class` позволяет отличать `short_term`, `long_term` и `profile`;
- `source` и `provenance` помогают не путать наблюдение и подтвержденный факт;
- `revision` нужен, чтобы не терять историю тихими перезаписями;
- `trust_level` помогает не ставить все записи в один ряд.

## 4. Запрос на извлечение

`retrieval_query` описывает не просто текстовый запрос, а полный рабочий контекст чтения памяти.

```yaml
kind: retrieval_query
trace_id: trace-001
session_id: session-001
tenant_id: tenant-acme
principal_id: user-42
purpose: answer_generation
allowed_classes:
  - profile
  - long_term
filters:
  trust_min: medium
  max_age_days: 90
  require_provenance: true
limit: 5
```

Здесь особенно важно то, что извлечение становится не «магическим поиском», а нормальным управляемым контуром чтения.

## 5. Результат извлечения

`retrieval_result` фиксирует, что именно рантайм решил вернуть в контекст.

```yaml
kind: retrieval_result
trace_id: trace-001
session_id: session-001
selected_records:
  - record_id: mem-tenant-acme-001
    memory_class: profile
    trust_level: high
    provenance: user_confirmed_preference
  - record_id: mem-tenant-acme-177
    memory_class: long_term
    trust_level: medium
    provenance: validated_service_rule
selection_reason:
  - profile_match
  - tenant_match
  - trust_filter_passed
excluded_records: 12
```

Это важно потому, что потом можно объяснить:

- почему именно эти записи попали в prompt;
- какие ограничения сработали;
- сколько записей было отброшено.

## 6. Как это связано со слоем политик

Контур чтения памяти и контур записи памяти почти никогда не должны жить по одним и тем же правилам:

- контур записи больше смотрит на validation, provenance и retention;
- контур чтения больше смотрит на границы арендаторов, фильтры доверия и ограничения по классам.

Поэтому хорошая схема памяти почти всегда живет рядом с политиками как кодом.

## 7. Как это связано со схемой трасс

В [схеме трасс](trace-schema.md) уже есть события и поля, которые поддерживают дисциплину памяти:

- `context_layers_built`
- `memory_persisted`
- `memory_class`
- `provenance`
- `revision`

То есть контракт памяти и извлечения полезен не только сам по себе, но и как основа для понятной телеметрии.

## 8. Как это связано со справочным пакетом

В [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) уже есть рабочие примитивы для этой модели:

- [memory.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/memory.py)
- [background.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/background.py)
- [configs/memory.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/memory.yaml)
- CLI:
  - `inspect-memory`

Встроенный `memory.yaml` делает это конкретным через `seed_records`: каждая seed record несёт стабильный `memory_id`, а также `tenant_id`, `memory_class`, `kind`, `content`, `source`, `confidence`, `provenance` и `revision`; bundled kinds — `language_preference`, `validated_fact` и `working_note`, чтобы demo показывало и retrieval filtering, и lineage записи. Reference seeds (`mem-001`, `mem-002` и `mem-003`) намеренно покрывают sources `trusted_profile`, `trusted_service` и `session_state`, включая provenance вроде `ephemeral_session_note`, чтобы retrieval examples показывали разные trust и persistence levels. Non-profile seed content также включает policy-like fact `Support tickets must use the support queue and include requester_id.` и working note `Recent runtime demo used create_ticket as the main write capability.` Loader тоже валидирует эту форму: `'memory' must be a mapping`, `'seed_records' must be a list`, `Memory record #{idx} must be a mapping`, `Memory record #{idx} field is required: {key}`, `Memory record #{idx} confidence must be between 0 and 1` и `Memory record #{idx} revision must be positive`.

Книга не только описывает этот контракт, но и показывает исполняемый каркас.

## 9. Минимальные инварианты

У здорового слоя памяти и извлечения обычно есть такие инварианты:

- каждая запись имеет `tenant_id` и `memory_class`;
- постоянные записи имеют `provenance` и `revision`;
- извлечение всегда ограничено по классам и объему;
- запрос на извлечение знает, кто читает и зачем;
- результат извлечения можно восстановить по трассе;
- summaries не считаются truth by default.

## 10. Что чаще всего ломается

Типовые проблемы здесь очень узнаваемы:

- извлечение возвращает «похожее», но не «полезное»;
- записи памяти не различаются по уровню доверия;
- summaries тихо перезаписывают более надежные данные;
- извлечение игнорирует границы арендатора;
- prompt получает слишком много контекста без фильтров;
- происхождение есть только на бумаге, но не в рантайме.

## 11. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли у каждой записи `tenant_id`, `memory_class`, `provenance` и `revision`?
- Отличаются ли политика чтения памяти и политика записи?
- Ограничено ли извлечение по доверию, классам и объему?
- Можно ли объяснить, почему конкретная запись попала в prompt?
- Есть ли защита от чтения через чужой tenant?
- Видно ли решения о памяти в трассе и экспорте сессии?

Если на несколько вопросов подряд ответ «нет», значит память у тебя уже есть, а вот дисциплины работы с ней пока нет.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Справочный пакет](reference-package.md)
- [Глава 5. Зачем агенту память и почему она опасна](../book/part-iii/chapter-5.md)
- [Глава 6. Краткосрочная, долгосрочная и профильная память](../book/part-iii/chapter-6.md)
- [Глава 7. Извлечение контекста, уплотнение и фоновые обновления](../book/part-iii/chapter-7.md)
