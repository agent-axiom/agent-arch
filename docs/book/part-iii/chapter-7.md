# Глава 7. Retrieval, compaction и background updates

## 1. Память бесполезна, если ты не умеешь возвращать из нее нужное

После того как ты развел short-term, long-term и profile memory, возникает следующий практический вопрос: как именно агент должен доставать нужные записи обратно в prompt?

Именно здесь многие системы начинают деградировать:

- в prompt летит слишком много нерелевантного контекста;
- retrieval возвращает похожее, но не полезное;
- summaries растут, но не становятся понятнее;
- каждая новая итерация делает контекст только тяжелее.

То есть проблема уже не в том, что память есть. Проблема в том, что память стала слишком шумной и дорогой для чтения.

## 2. Retrieval это не поиск “всего похожего”, а отбор того, что помогает решить текущую задачу

У retrieval очень плохая привычка: если его не ограничить, он пытается быть слишком щедрым. В итоге в prompt попадает не самый полезный контекст, а самый похожий по embedding или keyword overlap.

Для production-систем полезнее думать так:

- retrieval не обязан возвращать много;
- retrieval обязан возвращать объяснимо;
- retrieval должен уважать tenant, source и trust boundaries;
- retrieval должен подчиняться budget по размеру контекста.

Нормальный retrieval pipeline почти всегда учитывает не только similarity, но и:

- tenant isolation;
- memory class;
- recency;
- confidence;
- provenance;
- policy filters.

## 3. Хороший prompt любит не полноту, а плотность сигнала

Очень соблазнительно думать, что “чем больше контекста, тем умнее агент”. На практике часто наоборот: чем больше мусора ты кладешь в prompt, тем слабее модель держит приоритеты.

Поэтому retrieval должен отвечать не на вопрос “что мы можем достать?”, а на вопрос “что сейчас повышает шанс на правильное решение?”.

Полезный practical rule:

- лучше 3 очень релевантных records, чем 20 условно похожих;
- лучше маленький summary с источником, чем длинный сырой документ;
- лучше отдельный profile hint, чем целая история предпочтений;
- лучше пустой retrieval, чем retrieval без доверия и объяснимости.

## 4. Compaction это не косметика, а способ удержать систему в рабочем состоянии

Если memory layer только растет, рано или поздно prompt assembly начинает работать как мусоросборник без правил. Именно поэтому compaction должен быть частью архитектуры, а не разовым cleanup-проектом.

Compaction может означать разные вещи:

- сжать несколько записей в summary;
- удалить устаревшие working notes;
- объединить дубликаты;
- заменить большой blob на нормализованный record плюс ссылку на источник;
- понизить приоритет старых записей вместо вечного хранения “на первом плане”.

<div class="diagram-card">
<p>Retrieval и compaction лучше мыслить как один цикл обслуживания памяти</p>

``` mermaid
flowchart TD
    A["New run"] --> B["Query memory"]
    B --> C["Apply filters and ranking"]
    C --> D["Assemble prompt context"]
    D --> E["Model + tools"]
    E --> F["Create new memory candidates"]
    F --> G["Background compaction and review"]
    G --> H["Normalized memory store"]
    H --> B
```

</div>

## 5. Не все обновления памяти должны происходить в hot path

Это один из самых полезных архитектурных сдвигов для агентных систем. В начале почти все пытаются сделать память “сразу готовой”: агент что-то увидел, сразу переписал summaries, сразу обновил profile, сразу сохранил knowledge.

Но это почти всегда слишком дорого и слишком рискованно.

Что обычно разумно оставить в hot path:

- минимальный session state;
- короткие working notes;
- безопасные transient records с понятным TTL;
- update, без которого текущий workflow реально ломается.

Что обычно лучше уводить в background:

- compaction длинных сессий;
- пересборку summaries;
- нормализацию facts;
- deduplication;
- review memory candidates перед persistent write.

Именно background updates позволяют сделать память аккуратной, а не просто быстрой.

## 6. Хорошая система разделяет retrieval query и maintenance jobs

В зрелой архитектуре почти всегда есть два разных контура:

- read path: быстро и безопасно достать контекст для текущего run;
- maintenance path: спокойно улучшить memory store без давления latency.

Это важно не только для производительности, но и для качества решений. Когда одна и та же цепочка одновременно:

- выполняет задачу;
- пересобирает summaries;
- пишет profile memory;
- чистит дубликаты;
- обновляет ranking metadata,

она очень быстро становится хрупкой и плохо объяснимой.

## 7. Пример policy для retrieval и background updates

Ниже очень практичный шаблон. Он не пытается быть универсальным, но хорошо показывает, какие решения стоит сделать явными.

```yaml
retrieval:
  max_records: 5
  max_tokens: 1800
  allowed_classes:
    - short_term
    - long_term
    - profile
  require_tenant_match: true
  min_confidence: 0.75
  deny_sources:
    - raw_external_html
    - unreviewed_summary

compaction:
  run_mode: background_only
  summary_max_tokens: 400
  deduplicate: true
  merge_similar_records: true
  drop_expired_short_term: true
```

Когда такие правила явны, команда уже не спорит о памяти на уровне ощущений. Она спорит о конкретных ограничениях и trade-offs.

## 8. Простой кодовый пример ranking перед prompt assembly

Ниже не “умный” retrieval engine, а специально понятный пример. Он показывает, что ранжирование полезно строить не только по похожести, но и по доверию, свежести и важности.

```python
from dataclasses import dataclass


@dataclass
class RetrievedRecord:
    text: str
    similarity: float
    confidence: float
    recency_weight: float
    trusted: bool


def score(record: RetrievedRecord) -> float:
    trust_bonus = 0.15 if record.trusted else -0.2
    return (
        record.similarity * 0.5
        + record.confidence * 0.25
        + record.recency_weight * 0.1
        + trust_bonus
    )


def select_for_prompt(records: list[RetrievedRecord], limit: int = 3) -> list[RetrievedRecord]:
    ranked = sorted(records, key=score, reverse=True)
    return ranked[:limit]
```

Такая логика грубая, но у нее есть важное достоинство: ее можно обсуждать, тестировать и постепенно заменять чем-то более точным без потери объяснимости.

## 9. Summaries должны помогать читать, а не скрывать происхождение данных

Очень часто команды используют summaries как способ “впихнуть больше памяти в меньше токенов”. Это нормально, но есть одна ловушка: summary не должен превращаться в новую анонимную истину.

Хороший summary:

- короче исходных записей;
- сохраняет provenance;
- не смешивает tenants;
- не теряет критические ограничения;
- помечен как derived artifact, а не raw fact.

Плохой summary:

- звучит уверенно, но неясно, откуда он взялся;
- объединяет конфликтующие facts;
- теряет дату и владельца данных;
- подсовывается модели как trusted instruction.

## 10. Что чаще всего ломается в retrieval-системах

Обычно проблемы повторяются:

- в prompt попадают дубликаты;
- retrieval не знает про class boundaries;
- ranking не учитывает trust;
- summaries становятся слишком общими;
- background jobs отсутствуют, и memory только пухнет;
- nobody knows why this exact chunk was retrieved.

Последний пункт особенно важен. Если ты не можешь объяснить, почему контекст оказался в prompt, система уже плохо управляется.

## 11. Practical checklist

Если хочешь быстро проверить свой retrieval layer, пройди по вопросам:

- Есть ли limit по количеству records и token budget?
- Учитывает ли ranking не только similarity, но и confidence, recency и trust?
- Разделены ли read path и maintenance path?
- Есть ли compaction как регулярный процесс, а не ручная уборка?
- Можно ли у summary увидеть provenance?
- Есть ли защита от retrieval через чужой tenant или неподходящий class?

Если на несколько вопросов подряд ответ “нет”, значит память у тебя уже есть, а вот memory discipline пока нет.

## 12. Что читать дальше

На этом базовая часть про память уже начинает складываться. Дальше логично либо углубиться в retention и deletion, либо перейти к части про инструменты и выполнение.

- [Глава 6. Short-term, long-term и profile memory](chapter-6.md)
- [Часть III. Память и знания](index.md)
- [Источники](../../appendix/sources.md)
