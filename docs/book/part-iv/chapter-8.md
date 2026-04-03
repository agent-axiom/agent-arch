# Глава 8. Модель выполнения и каталог инструментов

## 1. Почему tool calling это не просто “модель выбрала функцию”

Когда агент начинает вызывать инструменты, многие команды сначала смотрят на это как на очень простую механику:

- описали tools;
- дали их модели;
- получили function call;
- выполнили действие.

На демо это работает. В production этого почти всегда недостаточно.

Проблема в том, что tool calling это не только вопрос “что модель захотела вызвать”. Это вопрос:

- какие действия вообще допустимы;
- в каком контексте они разрешены;
- кто отвечает за контракт вызова;
- где происходят валидация, retries и side effects;
- как система ведет себя при частичном сбое.

Поэтому execution model нужно проектировать как слой платформы, а не как тонкий helper вокруг LLM API.

## 2. Агент не должен ходить в инструменты напрямую

Одна из самых полезных архитектурных привычек: агент никогда не должен получать прямой доступ к реальным интеграциям.

Вместо этого у тебя должен быть execution layer, который:

- знает каталог доступных инструментов;
- валидирует входные аргументы;
- навешивает policy checks;
- разделяет read и write операции;
- управляет retries, timeouts и idempotency;
- пишет audit events.

Это особенно важно, когда tools начинают влиять на реальные системы: тикеты, CRM, базы данных, файлы, сообщения, платежи.

## 3. Tool catalog это интерфейс платформы, а не список случайных функций

Если смотреть на catalog как на “папку с вызовами”, он быстро превращается в мусорную свалку интеграций. Гораздо полезнее считать catalog публичным интерфейсом execution layer.

Хороший tool catalog обычно хранит:

- стабильное имя инструмента;
- описание его назначения;
- schema входных аргументов;
- risk class;
- side-effect level;
- allowed callers или capabilities;
- timeout, retry policy и idempotency expectations.

<div class="diagram-card">
<p>Модель должна разговаривать не с внешним миром напрямую, а с execution layer</p>

``` mermaid
flowchart LR
    A["Prompt + policy context"] --> B["Model"]
    B --> C["Tool request"]
    C --> D["Execution layer"]
    D --> E["Catalog lookup"]
    D --> F["Policy / validation"]
    D --> G["Retry / timeout / idempotency"]
    G --> H["External system"]
    H --> D
    D --> I["Structured tool result"]
    I --> B
```

</div>

## 4. Важно различать read tools и write tools

Это кажется очевидным, но на практике многие системы описывают их почти одинаково. А зря.

`read tools` обычно:

- менее опасны;
- чаще могут вызываться автоматически;
- полезны для grounding и retrieval;
- требуют контроля доступа, но не всегда требуют approval.

`write tools` обычно:

- создают side effects;
- требуют stronger validation;
- должны иметь явные rollback boundaries;
- часто требуют idempotency key и human approval.

Если read и write operations смешиваются в одну неявную категорию “tool call”, execution layer быстро теряет управляемость.

### 4.1. Полезная taxonomy: data, action, orchestration

В практическом гайде OpenAI есть еще одно полезное упрощение: tools удобно делить не только на `read` и `write`, но и по их роли в системе.[^openai-practical]

- `data tools` читают и возвращают контекст: поиск, retrieval, чтение CRM, чтение тикетов;
- `action tools` меняют внешний мир: создать тикет, отправить письмо, обновить запись;
- `orchestration tools` помогают самому runtime: передать задачу другому агенту, вызвать planner, запросить approval, сделать handoff.

Эти две оси хорошо работают вместе:

- `data tools` почти всегда ближе к `read`;
- `action tools` почти всегда ближе к `write`;
- `orchestration tools` могут быть и тем, и другим, но у них отдельный operational смысл.

Такой взгляд полезен, потому что помогает быстрее понять, где нужен жесткий контракт данных, где контроль side effects, а где дисциплина самого agent loop.

## 5. Контракт инструмента должен быть скучным и строгим

Одна из худших привычек в агентных системах: позволять модели импровизировать формат вызова.

В хорошем дизайне у инструмента есть контракт:

- четкие обязательные поля;
- понятные enum и ограничения;
- нормальные сообщения об ошибках;
- явный формат ответа;
- предсказуемое поведение при timeout или duplicate request.

Нормальная схема инструмента полезнее, чем “умный” description на пол-экрана.

```yaml
tools:
  create_ticket:
    description: "Create a support ticket in the internal helpdesk"
    kind: "write"
    risk: "medium"
    idempotent: true
    timeout_seconds: 15
    input_schema:
      required: ["title", "queue", "requester_id"]
      properties:
        title: {type: string, maxLength: 200}
        queue: {type: string, enum: ["support", "security", "ops"]}
        requester_id: {type: string}
        description: {type: string}
```

Это выглядит прозаично. И это хорошо. Чем меньше магии в contract layer, тем устойчивее инструментальная часть системы.

## 6. Execution layer должен нормализовать ошибки

Еще один частый провал: каждый внешний сервис возвращает свои ошибки в своем стиле, а агенту пробрасывают это почти без обработки.

В итоге модель получает хаотичный поток:

- где-то HTTP 500;
- где-то `"failed": true`;
- где-то HTML-страницу;
- где-то stack trace;
- где-то пустой ответ.

Execution layer должен уметь превращать это в нормальные типы исходов:

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_denied`
- `side_effect_unknown`

Это резко повышает explainability и позволяет агенту принимать более взрослые решения: повторить, спросить подтверждение, эскалировать человеку или безопасно остановиться.

## 7. Idempotency и retries нельзя додумывать потом

Почти каждая реальная интеграция рано или поздно дает тебе хотя бы один неприятный сценарий:

- timeout после того, как side effect уже случился;
- дубль вызова после retry;
- частичный успех;
- race condition между двумя runs;
- внешний сервис ответил позже expected window.

Если idempotency не заложена в execution design, агент очень быстро начинает делать то, что в обычных системах и так больно чинить: повторно создавать тикеты, дублировать письма, несколько раз менять один и тот же объект.

## 8. Простой кодовый шаблон для execution layer

Ниже не production runtime, а каркас, который показывает правильное разделение ответственности: lookup, validate, execute, normalize result.

```python
from dataclasses import dataclass


@dataclass
class ToolSpec:
    name: str
    kind: str
    timeout_seconds: int
    idempotent: bool


@dataclass
class ToolResult:
    status: str
    payload: dict


def execute_tool(spec: ToolSpec, args: dict) -> ToolResult:
    if spec.kind not in {"read", "write"}:
        return ToolResult(status="validation_failure", payload={"reason": "unknown tool kind"})

    if spec.kind == "write" and "idempotency_key" not in args:
        return ToolResult(status="validation_failure", payload={"reason": "missing idempotency key"})

    # In production this call would go through policy checks, a gateway, and typed adapters.
    return ToolResult(status="success", payload={"tool": spec.name})
```

Важно не то, насколько этот пример “богатый”. Важно, что инструмент не исполняется напрямую из решения модели.

## 9. Tool results тоже нужно проектировать, а не просто возвращать как есть

Если tool result слишком сырой, у модели снова появляется пространство для опасной импровизации.

Хороший result:

- краткий;
- структурированный;
- не тащит лишний технический шум;
- содержит machine-readable status;
- не прячет неопределенность.

Плохой result:

- возвращает всю внешнюю payload простыней;
- смешивает user-facing текст и системные детали;
- не различает “ничего не найдено” и “система упала”;
- не говорит, произошел ли side effect.

## 10. Каталог инструментов должен эволюционировать медленно

Если tools меняются каждый день без совместимости и версионирования, агентная система начинает вести себя как клиент на нестабильном private API.

Поэтому у catalog layer полезны такие привычки:

- versioned contracts;
- deprecation policy;
- owner на каждый инструмент;
- тесты на schema и result shape;
- capability review перед добавлением новых write tools.

Это скучная платформа, а не романтическая импровизация. Именно поэтому она работает.

## 11. Практический чеклист

Если хочешь быстро проверить свой execution layer, пройди по вопросам:

- Есть ли у тебя отдельный tool catalog, а не просто набор функций?
- Разделены ли read и write tools?
- Есть ли schema validation для аргументов?
- Нормализуются ли ошибки внешних систем?
- Учтены ли timeout, retries и idempotency?
- Видно ли, произошел side effect или нет?
- Есть ли owner и contract lifecycle у каждого инструмента?

Если на несколько пунктов подряд ответ “нет”, агент у тебя уже умеет вызывать tools, но execution model пока еще незрелая.

## 12. Что читать дальше

Следующие естественные темы в этой части: sandbox execution, MCP как контракт интеграции и правила для retries и rollback boundaries.

- [Глава 7. Извлечение контекста, уплотнение и фоновые обновления](../part-iii/chapter-7.md)
- [Глава 9. Sandbox execution и MCP как контракт интеграции](chapter-9.md)
- [Часть IV. Инструменты и выполнение](index.md)
- [Источники](../../appendix/sources.md)

[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
