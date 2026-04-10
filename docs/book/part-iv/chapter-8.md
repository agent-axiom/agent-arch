# Глава 8. Модель выполнения и каталог инструментов

## 1. Начнем с того же support-кейса, но уже на write path

Продолжим тот же сценарий из первых глав.

Пользователь пишет:

> Я уже третий день жду активации доступа. Проверьте статус и создайте срочный тикет, если заявка застряла.

На первый взгляд задача кажется простой:

- агент читает сообщение;
- вызывает инструмент проверки статуса;
- если заявка действительно застряла, вызывает инструмент создания тикета;
- возвращает ответ.

На демо этого почти достаточно. В production именно здесь и начинаются самые дорогие ошибки.

Потому что теперь вопрос уже не только в том, **что модель захотела сделать**. Вопрос в другом:

- какой инструмент ей вообще разрешено вызвать;
- в каком tenant scope это допустимо;
- какие аргументы считаются валидными;
- где отделяются read и write операции;
- что делать, если внешний сервис завис после side effect;
- как потом доказать, был ли тикет создан один раз или дважды.

Именно поэтому вызов инструментов нужно проектировать не как функцию при модели, а как execution layer платформы.

## 2. Агент не должен ходить в инструменты напрямую

Одна из самых полезных инженерных привычек здесь очень скучная: агент никогда не должен получать прямой доступ к реальным интеграциям.

Вместо этого нужен слой выполнения, который:

- знает каталог доступных инструментов;
- валидирует входные аргументы;
- навешивает policy checks;
- отделяет read и write операции;
- управляет retries, timeouts и idempotency;
- пишет audit events.

Для того же support-кейса это означает, что модель не должна сама ходить в helpdesk API или IAM service. Она должна разговаривать только с execution layer.

## 3. Как один запрос проходит через execution layer

Посмотрим на тот же сценарий уже как на путь выполнения.

### 3.1. Сначала модель предлагает read tool

Чтобы понять, застряла ли заявка, агенту нужен инструмент проверки статуса. Это read path:

- он не должен менять внешний мир;
- ему нужен корректный tenant scope;
- он должен вернуть понятный структурированный результат.

### 3.2. Потом система решает, разрешен ли write tool

Если статус говорит, что заявка действительно застряла, следующим шагом может быть `create_ticket`. Но это уже write path:

- здесь появляется side effect;
- может потребоваться approval;
- нужен idempotency key;
- нужен более строгий audit trail.

### 3.3. Потом execution layer берет на себя неприятную реальность

Именно здесь появляются сценарии, о которых редко думают на демо:

- helpdesk ответил timeout после создания тикета;
- инструмент вернул частичный успех;
- модель повторила вызов после retry;
- внешний сервис вернул неожиданный payload;
- у runtime нет уверенности, произошел ли side effect.

Это уже не "tool calling". Это полноценная дисциплина выполнения.

<div class="diagram-card">
<p>Модель должна разговаривать не с внешним миром напрямую, а со слоем выполнения</p>

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

## 4. Каталог инструментов это интерфейс платформы, а не список случайных функций

Если смотреть на каталог как на "папку с вызовами", он быстро превращается в свалку интеграций. Гораздо полезнее считать его публичным интерфейсом execution layer.

Для нашего support-сценария в каталоге полезно явно видеть, что именно умеет агент:

- `check_access_request_status`
- `get_user_profile`
- `create_support_ticket`
- `request_human_approval`

У хорошего каталога обычно есть:

- стабильное имя инструмента;
- описание назначения;
- schema входных аргументов;
- risk class;
- side-effect level;
- allowed callers или capabilities;
- timeout, retry policy и idempotency expectations.

Это делает execution layer обозримым: команда видит не "что-то там может вызвать модель", а конкретный platform contract.

## 5. Важно различать read tools и write tools

Это кажется очевидным, но на практике многие системы описывают их почти одинаково. А зря.

Для того же support-агента `check_access_request_status` и `create_support_ticket` не просто два tools. Это два разных класса риска.

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

Если read и write operations смешиваются в одну неявную категорию "tool call", execution layer быстро теряет управляемость.

### 5.1. Еще одна полезная taxonomy: data, action, orchestration

В практическом гайде OpenAI есть еще одно полезное упрощение: tools удобно делить не только на `read` и `write`, но и по их роли в системе.[^openai-practical]

- `data tools` читают и возвращают контекст: проверка статуса, retrieval, чтение CRM;
- `action tools` меняют внешний мир: создать тикет, отправить письмо, обновить запись;
- `orchestration tools` помогают самому runtime: запросить approval, сделать handoff, вызвать planner.

Эти две оси хорошо работают вместе:

- `data tools` почти всегда ближе к `read`;
- `action tools` почти всегда ближе к `write`;
- `orchestration tools` могут быть и тем, и другим, но у них отдельный operational смысл.

## 6. Контракт инструмента должен быть скучным и строгим

Одна из худших привычек в агентных системах: позволять модели импровизировать формат вызова.

В хорошем дизайне у инструмента есть контракт:

- четкие обязательные поля;
- понятные enum и ограничения;
- нормальные сообщения об ошибках;
- явный формат ответа;
- предсказуемое поведение при timeout или duplicate request.

Для нашего support-кейса это может выглядеть так:

```yaml
tools:
  check_access_request_status:
    description: "Read the current status of an access request"
    kind: "read"
    risk: "low"
    timeout_seconds: 10
    input_schema:
      required: ["request_id", "tenant_id"]
      properties:
        request_id: {type: string}
        tenant_id: {type: string}

  create_support_ticket:
    description: "Create a support ticket in the internal helpdesk"
    kind: "write"
    risk: "medium"
    idempotent: true
    timeout_seconds: 15
    input_schema:
      required: ["title", "queue", "requester_id", "tenant_id", "idempotency_key"]
      properties:
        title: {type: string, maxLength: 200}
        queue: {type: string, enum: ["support", "security", "ops"]}
        requester_id: {type: string}
        tenant_id: {type: string}
        idempotency_key: {type: string}
        description: {type: string}
```

Это выглядит прозаично. И это хорошо. Чем меньше магии в контрактном слое, тем устойчивее инструментальная часть системы.

## 7. Execution layer должен нормализовать ошибки

Еще один частый провал: каждый внешний сервис возвращает свои ошибки в своем стиле, а агенту пробрасывают это почти без обработки.

Для того же support-кейса это легко превращается в хаос:

- IAM service вернул HTTP 500;
- helpdesk ответил `"created": true`, но не прислал `ticket_id`;
- старый интеграционный адаптер вернул HTML;
- timeout случился уже после side effect;
- downstream API ответил пустым телом.

Execution layer должен превращать это в нормальные типы исходов:

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_denied`
- `side_effect_unknown`

Это резко повышает explainability и позволяет агенту принимать более взрослые решения: повторить, запросить approval, эскалировать человеку или безопасно остановиться.

## 8. Idempotency и retries нельзя додумывать потом

Почти каждая реальная интеграция рано или поздно дает хотя бы один неприятный сценарий:

- timeout после того, как side effect уже случился;
- дубль вызова после retry;
- partial success;
- race condition между двумя runs;
- внешний сервис ответил позже expected window.

Если idempotency не заложена в execution design, агент очень быстро начинает делать то, что в обычных системах и так больно чинить: повторно создавать тикеты, дублировать письма, несколько раз менять один и тот же объект.

Для support-кейса практическое правило простое: любой write tool, который может создавать тикет, обновлять запись или отправлять сообщение, должен иметь явную idempotency strategy до первого production rollout.

## 9. Простой кодовый шаблон для execution layer

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

Важно не то, насколько этот пример "богатый". Важно, что инструмент не исполняется напрямую из решения модели.

## 10. Tool results тоже нужно проектировать, а не просто возвращать как есть

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
- не различает "ничего не найдено" и "система упала";
- не говорит, произошел ли side effect.

## 11. Каталог инструментов должен эволюционировать медленно

Если tools меняются каждый день без совместимости и версионирования, агентная система начинает вести себя как клиент на нестабильном private API.

Поэтому у catalog layer полезны такие привычки:

- versioned contracts;
- deprecation policy;
- owner на каждый инструмент;
- тесты на schema и result shape;
- capability review перед добавлением новых write tools.

Это скучная платформа, а не романтическая импровизация. Именно поэтому она работает.

## 12. Что делать сразу после этой главы

Если хочешь быстро проверить свой execution layer, пройди по короткому списку:

1. Есть ли у тебя отдельный tool catalog, а не просто набор функций?
2. Разделены ли read и write tools?
3. Есть ли schema validation для аргументов?
4. Нормализуются ли ошибки внешних систем?
5. Учтены ли timeout, retries и idempotency?
6. Видно ли, произошел side effect или нет?
7. Есть ли owner и contract lifecycle у каждого инструмента?

Если на несколько пунктов подряд ответ "нет", агент у тебя уже умеет вызывать tools, но execution model пока еще незрелая.

## 13. Что читать дальше

Следующие естественные темы в этой части: sandbox execution, MCP как контракт интеграции и правила для retries и rollback boundaries.

- [Глава 7. Извлечение, сжатие и фоновые обновления](../part-iii/chapter-7.md)
- [Часть IV. Инструменты и выполнение](index.md)
- [Источники](../../appendix/sources.md)

[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
