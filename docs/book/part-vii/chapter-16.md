# Глава 16. Базовая схема рантайма

!!! info "Как читать эту главу"
    Полезно держать в голове не абстрактный вопрос “как устроен runtime”, а очень практичную задачу:

    - где именно должен жить run loop того же support-агента;
    - как не смешать policy, memory, execution и telemetry в один обработчик;
    - как собрать каркас, который выдержит не только демо, но и последующую выкладку.

    Если на эти вопросы нет ясного ответа, система обычно продолжает работать только до первого серьезного изменения или инцидента.

## 1. Зачем нужна эталонная схема рантайма, если у тебя уже есть архитектура

Архитектурные главы полезны, потому что они дают language и рамку. Но в какой-то момент почти у всех возникает один и тот же вопрос: “Хорошо, а как это должно выглядеть как система, которую реально можно собрать?”

Именно в этом состоит главная задача этой главы. Она должна помочь читателю перейти через важную границу: от согласия с аргументом книги к пониманию того, как этот аргумент превращается в работающую структуру системы.

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

## 8. Длинные run не optional add-on, а часть baseline

Частая ошибка рантайма в том, что команда молча предполагает: любой полезный run должен завершаться в одном синхронном запросе. Это верно только пока система остается demo-shaped.

В реальном support-кейсе часть запусков по природе длиннее:

- ожидание approval;
- ожидание tools с нестабильной latency;
- ожидание второго model pass после tool execution;
- ожидание deferred follow-up или background update.

Свежий материал OpenAI полезен тем, что рассматривает background execution как first-class concern рантайма, а не как обход timeout-проблем.[^openai-background]

Именно так на это и стоит смотреть в baseline runtime. Рантайм должен уже на старте различать:

- `synchronous runs`, которые безопасно завершаются в одном foreground pass;
- `background runs`, которые продолжаются после первого ответа;
- `resumable runs`, которые ставятся на паузу из-за approval, внешнего ввода или отложенной работы.

Таксономия workflow-паттернов у Anthropic делает это еще острее, потому что разные orchestration patterns создают разные checkpoint-needs.[^anthropic] У `prompt chaining` checkpoint обычно нужен между фиксированными стадиями, у `routing` он часто нужен только на границе классификации и handoff, `parallelization` требует видимости join-state, а `orchestrator-workers` требует parent/worker coordination state, который переживает частичное завершение.

То есть bounded autonomy это не только вопрос policy. Это еще и вопрос дизайна runtime state: каждый разрешенный execution pattern приносит с собой собственную семантику pause, resume и completion.

Если у рантайма нет явной формы для этих случаев, длинная работа почти всегда утекает в ad hoc retries, дублирующиеся запросы и скрытые переходы состояния.

## 9. Stateful tool sessions тоже должны входить в baseline

Как только execution layer начинает работать с stateful MCP-подобными capability, у baseline runtime появляется еще одна обязательная граница: **состояние user-visible run не равно состоянию capability session**.[^aws-stateful-mcp]

Это важно потому, что один пользовательский run теперь может включать:

- один runtime `run_id`;
- один или несколько MCP `session_id` для внешних capability;
- progress notifications до финального ответа;
- elicitation или промежуточные запросы, которые ставят run на паузу до нового ввода;
- re-initialization, если capability session истекла до завершения run.

Если все это слепить в один непрозрачный state object, оператор уже не сможет объяснить, что именно resumed, что expired и что надо retry заново.

### 9.1. Runtime должен относиться к capability session lifecycle как к first-class state

Минимально зрелый runtime обычно уже должен уметь хранить хотя бы:

- `run_id`;
- `trace_id`;
- `capability_session_id`;
- `capability_session_status`;
- `expires_at`;
- `resume_token` или другой continuation handle;
- `approval_state`, если stateful tool flow был поставлен на паузу из-за approval.

Это не означает, что каждому tool нужен тяжелый session model. Это означает, что у рантайма должно быть место, где такой session state можно выразить, когда protocol этого требует.

### 9.2. Progress и elicitation должны входить в ту же модель resume-control

Еще один полезный вывод из stateful MCP guidance: progress events и elicitation requests нельзя считать экзотическим побочным каналом. Они должны входить в ту же runtime control model, что approvals и background resumption.

Это становится еще важнее, когда runtime поддерживает несколько orchestration patterns. Progress из ветки `parallelization`, из worker, делегированного через `orchestrator-workers`, или из gated-стадии `prompt chaining` не должен пропадать внутри pattern-specific adapters. Он должен попадать в одну общую control surface для status, resumption, expiry и operator visibility.

На практике baseline runtime выигрывает от одной общей модели состояний для:

- `in_progress` работы, которая еще жива внутри capability session;
- пауз `waiting_for_input` или `waiting_for_approval`;
- `resumable` работы, которую можно продолжить в той же capability session;
- `reinitialize_required` работы, где capability session истекла и ее нужно поднять заново перед продолжением.

Без этих различий expiry session обычно выглядит как случайная ошибка, хотя на деле это нормальное lifecycle event.

## 10. Что важно встроить в baseline с самого начала

Есть вещи, которые кажется соблазнительным “добавить потом”, но на деле их лучше заложить сразу:

- `trace_id` на каждый run;
- tenant/principal context;
- policy decision hooks;
- capability registry вместо direct calls;
- structured telemetry;
- basic background task hook;
- явную модель статусов run вроде `queued / in_progress / completed / failed / canceled`;
- способ poll / resume / cancel для длинной работы без изобретения второго скрытого рантайма.

Если этого нет в baseline, потом система обычно дорастает до них через болезненный retrofit.

## 11. Минимальный каркас для background и resumable work

Даже baseline runtime должен иметь простой способ представлять работу, которая живет дольше первого запроса.

```python
from dataclasses import dataclass


@dataclass
class RunHandle:
    run_id: str
    status: str


def start_run(request: RunRequest) -> RunHandle:
    run_id = create_run_record(request)
    enqueue_run(run_id)
    return RunHandle(run_id=run_id, status="queued")


def continue_run(run_id: str):
    run = load_run(run_id)
    if run.status in {"canceled", "completed", "failed"}:
        return run

    update_status(run_id, "in_progress")
    result = execute_run_steps(run)
    update_status(run_id, result.status)
    return result
```

Смысл здесь не в усложнении. Смысл в том, чтобы длинная работа была достаточно явной: операторы могли ее наблюдать, клиенты могли ее опрашивать, а runtime мог ее продолжать или отменять без догадок.

## 12. Что можно не усложнять в первой reference версии

На старте не обязательно сразу добавлять:

- сложный planner с множеством режимов;
- многоступенчатую memory compaction pipeline;
- сложную стратегию model routing;
- полный self-healing loop;
- десяток golden paths.

Reference runtime полезен не максимальной мощностью, а ясностью формы. Лучше небольшая, но чистая реализация, чем “универсальный комбайн”, который никто не понимает.

## 13. Пример конфигурации рантайма

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
  background:
    enabled: true
    resumable_runs: true
    allow_cancel: true
  capability_sessions:
    track_session_ids: true
    emit_progress_events: true
    support_reinit_on_expiry: true
```

Это полезно, потому что помогает держать contract runtime явным и переносимым между средами.

## 13. Частые ошибки

Очень типовые проблемы:

- orchestration и adapters слеплены вместе;
- policy checks вызываются не на каждом нужном пути;
- memory подключена как случайный helper;
- tool calls идут мимо catalog/gateway;
- background updates отсутствуют;
- telemetry добавлена как afterthought;
- длинная работа спрятана за ретраями, а не смоделирована явно;
- background execution вроде бы есть, но операторы не могут нормально делать poll, resume или cancel.

То есть система вроде бы “работает”, но shape runtime уже мешает ее взрослению.

## 14. Быстрый тест зрелости для baseline runtime

Команде не стоит думать, что у нее уже есть reference runtime, только потому, что у нее есть working agent, несколько модулей и успешные демо.

Более сильная планка такая:

- orchestration, policy, memory, execution и telemetry видимы как отдельные слои;
- run context с самого начала несет identity и control metadata;
- capability execution идет через contracts, а не через direct adapter calls;
- tracing и background hooks встроены в base path, а не появляются как retrofit;
- длинная работа имеет явную модель статусов и продолжения, а не прячется в скрытых ретраях;
- один run можно объяснить как устойчивый skeleton, а не как рассыпанную local logic.

Если большинство этих условий не выполняется, у команды уже может быть implementation, но реального baseline runtime blueprint у нее пока нет.

## 15. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Видны ли отдельные слои orchestration, policy, memory, execution и telemetry?
- Есть ли единый run context с tenant/principal metadata?
- Есть ли capability registry вместо прямых вызовов?
- Встроены ли tracing hooks в базовый путь?
- Есть ли безопасная точка для background updates?
- Можно ли длинную работу явно поставить в очередь, наблюдать, продолжить и отменить?
- Можно ли объяснить поток одного run без чтения десяти файлов сразу?

Если на несколько вопросов подряд ответ “нет”, у тебя пока не эталонный рантайм, а просто ранняя интеграция модели в продукт.

## 16. Что делать дальше

Сначала зафиксируй shape runtime, а потом добавляй поверх него policy layer и capability contracts.

Следующий логичный шаг в части VII: сделать поверх этой схемы явный слой политик и каталог возможностей, чтобы эталонная реализация стала уже почти эксплуатационным каркасом.

- [Глава 15. Золотые пути, общие шлюзы и антизоопарк-подходы](../part-vi/chapter-15.md)
- [Глава 17. Слой политик и каталог возможностей](chapter-17.md)
- [Часть VII. Эталонная реализация](index.md)
- [Источники](../../appendix/sources.md)

[^openai-background]: [OpenAI, Background mode](https://developers.openai.com/api/docs/guides/background)
