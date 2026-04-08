# Схема memory records и retrieval contract

Эта страница собирает в одном месте минимальный контрактный слой для памяти и retrieval в agent systems: какие поля должны быть у memory record и retrieval query и какие гарантии нужны, чтобы память не превращалась в неуправляемый источник утечек, шума и ложной уверенности.

Если [схема трасс и каталог событий](trace-schema.md) отвечает на вопрос "как это видно в telemetry", а [схема lifecycle-артефактов](lifecycle-artifact-schema.md) отвечает на вопрос "что считается управляемым рабочим артефактом", то эта схема отвечает на вопрос "какие именно записи и фильтры вообще допустимы в memory layer".

## 1. Зачем нужен отдельный слой схем

Очень частая ошибка с памятью устроена так:

- агент что-то запомнил;
- retrieval что-то вернул;
- дальше команда уже не может уверенно ответить:
  - что это была за запись;
  - откуда она взялась;
  - кто имел право ее читать;
  - по каким правилам она попала в prompt.

Поэтому memory layer полезно описывать не как "у нас есть vector store", а как набор типизированных записей и типизированных правил retrieval.

## 2. Базовые сущности

Минимальный слой здесь удобно строить вокруг трех сущностей:

- `memory_record`
- `retrieval_query`
- `retrieval_result`

Этого уже достаточно, чтобы связать главы 5-7, policy layer, trace schema и reference runtime.

## 3. Memory record

`memory_record` описывает одну конкретную запись в memory layer.

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

- `tenant_id` не дает retrieval пересекать границы арендаторов;
- `memory_class` позволяет отличать `short_term`, `long_term` и `profile`;
- `source` и `provenance` помогают не путать "наблюдение" и "подтвержденный факт";
- `revision` нужен, чтобы не терять историю тихими перезаписями;
- `trust_level` помогает не ставить все записи в один ряд.

## 4. Retrieval query

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

Здесь особенно полезно то, что retrieval становится не "магическим поиском", а нормальным gated read path.

## 5. Retrieval result

`retrieval_result` фиксирует, что именно runtime решил вернуть в контекст.

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

## 6. Как это связано с policy layer

Memory read path и memory write path почти никогда не должны жить по одним и тем же правилам:

- write path больше смотрит на validation, provenance и retention;
- read path больше смотрит на tenant boundaries, trust filters и class restrictions.

Поэтому хорошая схема памяти почти всегда живет рядом с policy-as-code.

## 7. Как это связано с trace schema

В [trace schema](trace-schema.md) уже есть события и поля, которые поддерживают memory discipline:

- `context_layers_built`
- `memory_persisted`
- `memory_class`
- `provenance`
- `revision`

То есть memory-retrieval contract полезен не только сам по себе, но и как основа для понятной telemetry.

## 8. Как это связано с reference package

В [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) уже есть operational primitives для этой модели:

- [memory.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/memory.py)
- [background.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/background.py)
- [configs/memory.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/memory.yaml)
- CLI:
  - `inspect-memory`

Книга не только описывает memory contract, но и показывает runnable skeleton.

## 9. Минимальные инварианты

У здорового memory-retrieval слоя обычно есть такие инварианты:

- каждая запись имеет `tenant_id` и `memory_class`;
- persistent records имеют `provenance` и `revision`;
- retrieval всегда ограничен по классам и объему;
- retrieval query знает, кто читает и зачем;
- retrieval result можно восстановить по trace;
- summaries не считаются truth by default.

## 10. Что чаще всего ломается

Типовые проблемы здесь очень узнаваемы:

- retrieval возвращает "похожее", но не "полезное";
- memory records не различаются по trust level;
- summaries тихо перезаписывают более надежные данные;
- retrieval игнорирует tenant boundary;
- prompt получает слишком много контекста без фильтров;
- provenance есть только на бумаге, но не в runtime.

## 11. Практический чеклист

Если хочешь быстро проверить memory layer, пройди по вопросам:

- Есть ли у каждой записи `tenant_id`, `memory_class`, `provenance` и `revision`?
- Отличаются ли memory read policy и memory write policy?
- Ограничен ли retrieval по trust, class и объему?
- Можно ли объяснить, почему конкретная запись попала в prompt?
- Есть ли защита от retrieval через чужой tenant?
- Видно ли memory decisions в trace и session export?

Если на несколько вопросов подряд ответ "нет", значит память у тебя уже есть, а вот memory discipline пока еще нет.

## См. также

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема eval datasets и grading contract](eval-schema.md)
- [Схема lifecycle-артефактов](lifecycle-artifact-schema.md)
- [Опорный пакет](reference-package.md)
- [Глава 5. Зачем агенту память и почему она опасна](../book/part-iii/chapter-5.md)
- [Глава 6. Short-term, long-term и profile memory](../book/part-iii/chapter-6.md)
- [Глава 7. Retrieval, compaction и background updates](../book/part-iii/chapter-7.md)
