# Глава 16. Базовая схема рантайма

!!! info "Как читать эту главу"
    Полезно держать в голове не абстрактный вопрос “как устроен runtime”, а очень практичную задачу:

    - где именно должен жить run loop того же support-агента;
    - как не смешать policy, memory, execution и telemetry в один обработчик;
    - как собрать каркас, который выдержит не только демо, но и последующую выкладку.

    Если на эти вопросы нет ясного ответа, система обычно продолжает работать только до первого серьезного изменения или инцидента.

## 1. Зачем нужна эталонная схема рантайма, если у тебя уже есть архитектура

Архитектурные главы полезны, потому что они дают language и рамку. Но в какой-то момент почти у всех возникает один и тот же вопрос: “Хорошо, а как это должно выглядеть как система, которую реально можно собрать?”

В нашем сквозном support-кейсе это уже не теоретический вопрос. Агент умеет проверять статус пользователя, обращаться к памяти, открывать тикет через gateway и оставлять traces. Но без явной схемы runtime все эти шаги очень быстро расползаются по локальным хендлерам, ad hoc retries и случайным интеграционным обходам.

Вот тут и нужна эталонная схема рантайма.

Его задача не в том, чтобы стать единственной возможной реализацией. Его задача:

- зафиксировать основные модули;
- показать поток одного run;
- отделить обязательные слои от optional enhancements;
- дать команде отправную точку без лишней магии.

## 2. Минимально взрослый runtime уже состоит не из одной модели

Очень полезно сразу отказаться от образа “agent = один model call плюс tools”.

Минимально взрослый runtime обычно включает:

- ingress layer;
- run coordinator;
- policy hooks;
- memory access layer;
- tool/capability execution layer;
- telemetry emitter;
- result assembly.

То есть runtime это не “место, где вызывается LLM”. Это orchestrated loop вокруг модели.

## 3. Как выглядит базовый flow одного run

Для эталонной реализации удобно мыслить один запуск примерно так:

1. принять request и построить run context;
2. выполнить policy pre-checks;
3. собрать нужный контекст из memory/retrieval;
4. вызвать модель;
5. если нужен tool call, прогнать его через execution layer;
6. записать telemetry;
7. собрать финальный result;
8. запланировать background updates.

Это уже очень далеко от “просто чат с функциями”, и именно так и должно быть.

<div class="diagram-card">
<p>У базового runtime уже есть несколько обязательных control points</p>

``` mermaid
flowchart LR
    A["Ingress"] --> B["Run context"]
    B --> C["Policy pre-check"]
    C --> D["Memory / retrieval"]
    D --> E["Model step"]
    E --> F{"Tool needed?"}
    F -->|No| G["Result assembly"]
    F -->|Yes| H["Execution layer"]
    H --> I["Tool result"]
    I --> E
    G --> J["Telemetry + background tasks"]
```

</div>

## 4. Какие модули полезно держать отдельными сразу

Есть несколько границ, которые выгодно выделить в коде уже в первой версии:

- `runtime.py` или `orchestrator.py` для run loop;
- `policy.py` для policy decisions;
- `memory.py` для retrieval и memory writes;
- `catalog.py` для capability registry;
- `execution.py` для tool dispatch;
- `telemetry.py` для spans и structured events.

Когда все это слеплено в один большой handler, первые демо получаются быстро, но взросление системы становится болезненным почти сразу.

## 5. Не смешивай orchestration и business adapters

Одна из самых дорогих ошибок стартовой реализации: runtime напрямую знает слишком много про конкретные внешние системы.

Тогда orchestration code начинает содержать:

- условную логику по конкретным tools;
- знание об external payload shapes;
- локальные ретраи под конкретный API;
- ad hoc redaction;
- специальные обходы для отдельных интеграций.

Reference runtime должен показывать обратную идею: orchestration работает через contracts, а adapters живут на краю системы.

## 6. Пример минимальной структуры проекта

Ниже очень приземленный вариант стартовой структуры:

```text
agent_runtime/
  orchestrator.py
  policy.py
  memory.py
  catalog.py
  execution.py
  telemetry.py
  models.py
  background.py
```

Это не “единственно правильная” структура. Но она уже помогает не свалить все в один файл и не смешать контрольные слои между собой.

## 7. Простой кодовый каркас orchestrator

Ниже не production runtime, а именно blueprint-каркас. Он показывает, как разделяются шаги run и где должны проходить ключевые control points.

```python
from dataclasses import dataclass


@dataclass
class RunRequest:
    user_input: str
    tenant_id: str
    principal_id: str


@dataclass
class RunResult:
    output_text: str
    status: str


def run_agent(request: RunRequest) -> RunResult:
    policy_check(request)
    context = retrieve_context(request)
    model_output = call_model(request, context)

    if model_output.get("tool_request"):
        tool_result = execute_tool(model_output["tool_request"])
        emit_event("tool_execution", tool_result)
        model_output = call_model(request, context + [tool_result])

    schedule_background_updates(request, model_output)
    return RunResult(output_text=model_output["text"], status="success")
```

Идея здесь очень простая: даже базовый runtime уже должен явно показывать policy, retrieval, tool execution и background updates как отдельные этапы.

## 8. Что важно встроить в baseline с самого начала

Есть вещи, которые кажется соблазнительным “добавить потом”, но на деле их лучше заложить сразу:

- `trace_id` на каждый run;
- tenant/principal context;
- policy decision hooks;
- capability registry вместо direct calls;
- structured telemetry;
- basic background task hook.

Если этого нет в baseline, потом система обычно дорастает до них через болезненный retrofit.

## 9. Что можно не усложнять в первой reference версии

На старте не обязательно сразу добавлять:

- сложный planner с множеством режимов;
- многоступенчатую memory compaction pipeline;
- сложную стратегию model routing;
- полный self-healing loop;
- десяток golden paths.

Reference runtime полезен не максимальной мощностью, а ясностью формы. Лучше небольшая, но чистая реализация, чем “универсальный комбайн”, который никто не понимает.

## 10. Пример конфигурации рантайма

Ниже пример конфигурации, которая задает shape runtime, не вшивая все решения в код:

```yaml
runtime:
  max_tool_hops: 3
  require_trace_id: true
  enable_background_updates: true
  default_model: gpt-5.4
  policy:
    precheck_required: true
  telemetry:
    emit_structured_events: true
  execution:
    gateway_required: true
```

Это полезно, потому что помогает держать contract runtime явным и переносимым между средами.

## 11. Что чаще всего ломается в первых runtime-реализациях

Очень типовые проблемы:

- orchestration и adapters слеплены вместе;
- policy checks вызываются не на каждом нужном пути;
- memory подключена как случайный helper;
- tool calls идут мимо catalog/gateway;
- background updates отсутствуют;
- telemetry добавлена как afterthought.

То есть система вроде бы “работает”, но shape runtime уже мешает ее взрослению.

## 12. Практический чеклист

Если хочешь быстро проверить свой baseline runtime, пройди по вопросам:

- Видны ли отдельные слои orchestration, policy, memory, execution и telemetry?
- Есть ли единый run context с tenant/principal metadata?
- Есть ли capability registry вместо прямых вызовов?
- Встроены ли tracing hooks в базовый путь?
- Есть ли безопасная точка для background updates?
- Можно ли объяснить поток одного run без чтения десяти файлов сразу?

Если на несколько вопросов подряд ответ “нет”, у тебя пока не эталонный рантайм, а просто ранняя интеграция модели в продукт.

## 13. Что читать дальше

Следующий логичный шаг в части VII: сделать поверх этой схемы явный слой политик и каталог возможностей, чтобы эталонная реализация стала уже почти эксплуатационным каркасом.

- [Глава 15. Золотые пути, общие шлюзы и антизоопарк-подходы](../part-vi/chapter-15.md)
- [Глава 17. Слой политик и каталог возможностей](chapter-17.md)
- [Часть VII. Эталонная реализация](index.md)
- [Источники](../../appendix/sources.md)
