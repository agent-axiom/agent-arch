# Глава 11. Трассы, спаны и структурированные события

## 1. Начнем не с логов, а с расследования одного сбоя

Продолжим тот же support-кейс.

Пользователь пишет:

> Я уже третий день жду активации доступа. Проверьте статус и создайте срочный тикет, если заявка застряла.

Агент отвечает пользователю, что тикет создан. Через десять минут оператор видит в helpdesk уже **два** одинаковых тикета на одну и ту же проблему.

Теперь у команды очень приземленный вопрос:

- модель сама повторила вызов;
- retry сработал после timeout;
- инструмент вернул ambiguous result;
- side effect произошел до того, как рантайм увидел ошибку;
- или тикеты создали два разных runs.

Если у тебя есть только application logs и несколько метрик, ответ на этот вопрос обычно добывается долго и болезненно.

Именно поэтому observability для агентных систем нужно строить не вокруг "логов вообще", а вокруг возможности восстановить историю одного run.

## 2. Почему обычных логов почти всегда недостаточно

Когда система простая, действительно можно жить на плоских логах и паре метрик. Но агентная система почти всегда сложнее:

- один пользовательский запрос превращается в многошаговый run;
- внутри run есть planning, retrieval, prompt assembly, tool calls и policy gates;
- часть шагов может уходить в background;
- ошибка может проявиться не там, где она возникла.

Если смотреть на все это только через плоские логи, ты быстро теряешь причинно-следственную связь. Видно шум, но не видно историю выполнения.

Для нашего support-инцидента это означает простую вещь: без хорошей трассировки команда не поймет, кто именно создал дубль тикета и почему это произошло.

## 3. Trace это история одного run, span это осмысленный шаг

Здесь полезно закрепить простую модель:

- `trace` описывает весь путь запроса или run;
- `span` описывает отдельный значимый шаг внутри этого пути;
- `structured events` добавляют точные факты, которые не стоит прятать в свободный текст.

Для того же support-кейса один run может включать:

- policy evaluation;
- retrieval;
- model inference;
- tool execution;
- approval wait;
- background memory update.

Когда эта структура есть, команда перестает смотреть на систему как на хаотичную череду вызовов и начинает видеть цепочку наблюдаемых решений.

## 4. Как trace должен выглядеть в нашем support-сценарии

Ниже важно не просто показать красивую схему, а увидеть, где именно может возникнуть сбой.

<div class="diagram-card">
<p>Зрелый trace должен показывать не только модель, но и все ключевые control points</p>

``` mermaid
flowchart LR
    A["User request"] --> B["Run trace"]
    B --> C["Policy span"]
    B --> D["Retrieval span"]
    B --> E["Model span"]
    B --> F["Tool span: check status"]
    B --> G["Tool span: create ticket"]
    B --> H["Approval span"]
    B --> I["Memory update span"]
```

</div>

Если этот trace собран правильно, команда должна быстро увидеть:

- был ли второй tool call в том же run;
- был ли retry;
- каким был `idempotency_key`;
- на каком шаге появился `side_effect_unknown`;
- был ли approval;
- какой policy gate разрешил действие.

## 5. Что стоит делать отдельными spans

Не нужно делать отдельный span на каждую мелочь. Но и один giant span на весь run почти бесполезен.

Хорошее practical rule такое:

- отдельный span на orchestration step;
- отдельный span на retrieval;
- отдельный span на model call;
- отдельный span на каждый tool call;
- отдельный span на policy decision, если она влияет на поведение;
- отдельный span на human approval wait, если он есть.

Тогда trace остается читаемым и при этом показывает, где именно ушло время, деньги и надежность.

## 6. Structured events нужны там, где plain text только мешает

Частая ошибка: полезные operational facts уходят в человекочитаемый лог, а потом по ним невозможно строить аналитику или расследование.

Структурированные события особенно полезны для:

- policy decisions;
- tool outcomes;
- prompt assembly metadata;
- token usage;
- cost attribution;
- idempotency keys;
- tenant и principal context;
- memory writes.

То есть событие должно отвечать не на вопрос "что бы написать в лог", а на вопрос "что потом понадобится анализировать машинно?"

## 7. Хорошая trace model показывает control plane, а не только LLM latency

Если наблюдаемость сводится только к времени ответа модели, команда получает очень искаженную картину.

В реальности тот же support-run часто ломается в других местах:

- retrieval начал возвращать шум;
- policy engine слишком часто блокирует действия;
- approval wait растянулся;
- tool adapter деградировал;
- background updates забили очередь;
- prompt assembly раздула контекст;
- write tool вернул ambiguous outcome.

Поэтому хорошая trace model должна покрывать весь control flow, а не только inference step.

## 8. Минимальный набор полей для trace и spans

Чтобы система действительно была пригодна для расследований, полезно иметь как минимум:

- `trace_id`
- `span_id`
- `parent_span_id`
- `run_id`
- `tenant_id`
- `principal_id`
- `agent_id` или workflow id
- `status`
- `duration_ms`
- `model_name`, если был model call
- `tool_name`, если был tool call
- `policy_decision_id`, если был gate

Для расследования support-инцидента этого уже достаточно, чтобы связать между собой runtime, tool gateway и конкретный внешний side effect.

## 9. Пример structured event для tool execution

Ниже очень простой шаблон, который показывает правильный стиль мышления:

```yaml
event_type: tool_execution
trace_id: trc_01HXYZ
span_id: spn_02ABC
run_id: run_9842
tenant_id: tenant_acme
tool_name: create_ticket
status: success
duration_ms: 842
idempotency_key: act_77f1
policy_decision_id: pol_441
side_effect: created
```

Такой event намного полезнее, чем строка вроде "ticket tool ok".

### 9.1. Для того же кейса особенно важны еще четыре поля

Если цель не просто смотреть дашборды, а реально расследовать сбои, к этому шаблону обычно стоит добавить:

- `approval_id`
- `tool_principal`
- `request_id` или другой business object id
- `result_class`

Именно они часто позволяют различить:

- duplicate tool call;
- late retry;
- чужой tenant scope;
- ambiguous external response.

## 10. Простой кодовый пример span emission

Ниже каркас, который показывает самую идею: span должен не просто стартовать и завершаться, а фиксировать тип шага и outcome в структуре, пригодной для анализа.

```python
from dataclasses import dataclass
from time import monotonic


@dataclass
class SpanResult:
    name: str
    status: str
    duration_ms: int


def traced_step(name: str, fn):
    started = monotonic()
    try:
        fn()
        status = "success"
    except Exception:
        status = "failure"
        raise
    finally:
        duration_ms = int((monotonic() - started) * 1000)
        emit_span(SpanResult(name=name, status=status, duration_ms=duration_ms))


def emit_span(result: SpanResult) -> None:
    print({"span_name": result.name, "status": result.status, "duration_ms": result.duration_ms})
```

Этот пример нарочно простой. Его задача не заменить tracing SDK, а показать принцип: каждый важный шаг должен оставлять после себя структурированный след.

## 11. Что особенно важно не логировать как есть

Observability не должна превращаться в утечку данных.

Поэтому в traces и events нужно очень аккуратно обращаться с:

- полными prompt bodies;
- сырыми retrieved documents;
- секретами и токенами;
- PII;
- содержимым чувствительных tool payloads.

Практическое правило простое:

- логируй metadata и derived facts;
- логируй identifiers и hashes там, где это помогает;
- полные чувствительные payloads не клади в общие telemetry pipelines без особой причины.

## 12. Что чаще всего ломается в agent observability

Проблемы здесь очень узнаваемы:

- trace покрывает только model call;
- tool calls не связаны с исходным run;
- policy decisions видны в коде, но не видны в telemetry;
- события есть, но без tenant/principal context;
- spans слишком крупные или слишком шумные;
- event schema меняется хаотично, и аналитика ломается.

Если это происходит, команда снова начинает жить на догадках и ручном чтении логов.

## 13. Что делать сразу после этой главы

Если хочешь быстро проверить свою observability-модель, пройди по вопросам:

1. Можно ли восстановить полный путь одного run по одному `trace_id`?
2. Есть ли отдельные spans для retrieval, model calls, tool calls и policy gates?
3. Логируются ли idempotency keys и policy decision ids?
4. Есть ли tenant/principal context в telemetry?
5. Можно ли увидеть, где run провел время и где выросла стоимость?
6. Не утекают ли чувствительные payloads в traces?
7. Стабильна ли schema structured events?

Если на несколько пунктов подряд ответ "нет", observability у тебя пока декоративная, а не operational.

## 14. Что читать дальше

Следующий шаг здесь очень естественный: после traces и structured events нужно формализовать, что вообще считается "здоровой" агентной системой. То есть перейти к SLO.

- [Глава 10. Идемпотентность, повторы, лимиты запросов и границы отката](../part-iv/chapter-10.md)
- [Глава 12. SLO для агентных систем](chapter-12.md)
- [Часть V. Надежность и observability](index.md)
- [Источники](../../appendix/sources.md)
