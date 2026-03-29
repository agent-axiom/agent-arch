# Глава 10. Idempotency, retries, rate limits и rollback boundaries

## 1. Почему самые дорогие сбои часто выглядят как “мы просто повторили вызов”

Когда агентная система начинает выполнять реальные действия, один из самых неприятных источников инцидентов оказывается очень прозаичным: повторный вызов.

Снаружи это часто выглядит безобидно:

- запрос завис;
- runtime решил повторить;
- интеграция ответила нестабильно;
- агент попытался “помочь” и отправил действие еще раз.

Но в реальном мире это означает:

- два одинаковых тикета;
- два письма одному клиенту;
- повторную оплату;
- повторную запись в CRM;
- несколько изменений одного и того же объекта.

То есть проблема не в рассуждении модели как таковом, а в том, что execution layer не умеет безопасно жить в мире частичных сбоев.

## 2. Idempotency это не nice-to-have, а базовая страховка

Idempotency нужна для простого вопроса: “Если система по ошибке повторит этот вызов, что произойдет?”

Для write operations хороший ответ должен быть одним из двух:

- повторный вызов не меняет результат;
- система может надежно распознать дубль и не создать side effect повторно.

Если такого свойства нет, любая нестабильность сети, таймаут или гонка между несколькими runs начинает стоить слишком дорого.

## 3. Retry без классификации ошибок только множит хаос

Очень плохая стратегия выглядит так: “если запрос не удался, повторить еще три раза”.

В production это опасно, потому что не все ошибки одинаковы:

- `validation_failure` почти никогда не нужно ретраить;
- `permission_denied` нельзя чинить количеством повторов;
- `retryable_failure` как раз может требовать backoff;
- `side_effect_unknown` требует осторожности, а не слепого повтора.

То есть retry policy должна зависеть не от эмоции “ну вдруг получится”, а от класса исхода.

## 4. Самый неприятный статус это side effect unknown

Есть особенно неприятная категория сбоев: ты уже не знаешь, произошел side effect или нет.

Примеры:

- timeout после отправки запроса во внешний сервис;
- соединение оборвалось после commit;
- адаптер упал, не сохранив подтверждение;
- внешний API ответил так, что итоговое состояние неясно.

Это именно тот случай, где naïve retry особенно опасен. Иногда правильное поведение тут не “повторить”, а:

- проверить текущее состояние во внешней системе;
- выполнить reconciliation;
- запросить человека;
- остановить workflow и зафиксировать неопределенность.

## 5. Rate limits это тоже часть safety design

Когда о rate limits думают только как о проблеме производительности, execution layer недооценивает их архитектурную роль.

На деле rate limits нужны еще и для того, чтобы:

- один runaway agent не заддосил внешнюю систему;
- циклический planning не превратился в лавину tool calls;
- high-cost capability не съедала весь бюджет;
- retry storm не убивал интеграцию.

Именно поэтому limit полезно задавать не только на уровне whole service, но и:

- per tool;
- per tenant;
- per workflow;
- per risk class.

## 6. Rollback boundary должна быть определена заранее

Очень опасно обнаруживать только в инциденте, что операция “вообще-то неоткатываемая”.

У каждого write-capability полезно заранее понимать:

- можно ли отменить действие;
- можно ли безопасно повторить действие;
- где проходит точка невозврата;
- какой compensating action допустим;
- когда нужен manual reconciliation.

То есть rollback boundary это не “потом посмотрим”. Это часть контракта инструмента и workflow.

<div class="diagram-card">
<p>После side effect execution layer должен различать safe retry, reconcile и stop paths</p>

``` mermaid
flowchart TD
    A["Tool request"] --> B["Execute write action"]
    B --> C{"Outcome known?"}
    C -->|Yes, success| D["Store result and continue"]
    C -->|Retryable failure| E["Retry with policy and backoff"]
    C -->|Unknown side effect| F["Reconcile or request human review"]
    C -->|Validation or permission failure| G["Stop and surface error"]
```

</div>

## 7. Хороший execution contract хранит operational semantics явно

Недостаточно знать только schema входа и форму ответа. Для опасных операций контракт должен хранить operational semantics:

- idempotent ли действие;
- нужен ли idempotency key;
- какие ошибки retryable;
- где предел retries;
- какие лимиты на частоту вызова;
- что делать при unknown outcome;
- возможен ли rollback или compensating action.

Ниже очень практичный шаблон:

```yaml
tools:
  create_ticket:
    mode: write
    idempotent: true
    idempotency_key_required: true
    retry:
      max_attempts: 3
      backoff: exponential
      retry_on: ["retryable_failure"]
    rate_limit:
      per_tenant_per_minute: 20
    rollback:
      strategy: "none"
      reconcile_on_unknown: true

  send_email:
    mode: write
    idempotent: false
    idempotency_key_required: false
    retry:
      max_attempts: 1
      retry_on: []
    rate_limit:
      per_user_per_hour: 10
    rollback:
      strategy: "manual_only"
      reconcile_on_unknown: true
```

Такой YAML помогает команде заранее признать неприятную правду: не все действия одинаково безопасны для автоматизации.

## 8. Простой кодовый пример decision logic для retries

Ниже не production-grade policy engine, а понятный каркас. Его задача показать, что retry должен зависеть от класса исхода, а не быть общим reflex.

```python
from dataclasses import dataclass


@dataclass
class ExecutionOutcome:
    status: str
    attempts: int
    max_attempts: int


def next_step(outcome: ExecutionOutcome) -> str:
    if outcome.status in {"validation_failure", "permission_denied"}:
        return "stop"
    if outcome.status == "retryable_failure" and outcome.attempts < outcome.max_attempts:
        return "retry_with_backoff"
    if outcome.status == "side_effect_unknown":
        return "reconcile"
    if outcome.status == "success":
        return "continue"
    return "escalate"
```

Важен не код сам по себе, а то, что у системы появляется явная operational decision table.

## 9. Idempotency key должен быть частью протокола, а не опциональной договоренностью

Если write tool формально “поддерживает idempotency”, но ключ:

- не обязателен;
- по-разному генерируется в разных местах;
- не доживает до retry path;
- не логируется,

то это почти не настоящая idempotency.

Хорошая практика:

- генерировать ключ на уровне workflow или action boundary;
- передавать его через весь execution path;
- логировать его в audit trail;
- использовать для reconciliation и расследований.

## 10. Что чаще всего ломается в execution reliability

Проблемы здесь довольно типовые:

- retries идут на ошибки, которые нельзя ретраить;
- неизвестный outcome трактуется как обычный failure;
- rate limits ставят только на входе, но не на tools;
- rollback обещан, но фактически не существует;
- idempotency key забывается между planner и adapter;
- агент получает слишком много свободы в повторных попытках.

Все это означает одно: execution layer еще не дорос до production-grade модели отказов.

## 11. Practical checklist

Если хочешь быстро проверить reliability execution layer, пройди по вопросам:

- Есть ли у write tools явная idempotency strategy?
- Различает ли система `retryable_failure` и `side_effect_unknown`?
- Привязаны ли retries к policy, а не к общему helper?
- Есть ли rate limits per tool или per tenant?
- Понимаешь ли ты rollback boundary для каждого опасного действия?
- Может ли runtime делать reconciliation вместо слепого повтора?
- Видно ли idempotency key в traces и audit logs?

Если на несколько вопросов подряд ответ “нет”, то следующая нестабильность интеграции почти наверняка превратится в дубль, шум или ручной разбор инцидента.

## 12. Что читать дальше

Part IV уже закрывает базовый execution layer: contracts, sandbox, capability transport и дисциплину вокруг side effects. Дальше очень логично переходить к observability и reliability на уровне всей агентной системы.

- [Глава 9. Sandbox execution и MCP как контракт интеграции](chapter-9.md)
- [Часть IV. Инструменты и выполнение](index.md)
- [Источники](../../appendix/sources.md)
