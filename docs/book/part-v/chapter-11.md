# Глава 11. Трассы, спаны и структурированные события

## 1. Почему обычных логов для агентной системы почти всегда недостаточно

Когда система простая, действительно можно жить на наборе application logs и паре метрик. Но агентная система почти всегда сложнее:

- один пользовательский request превращается в многошаговый run;
- внутри run есть planning, retrieval, prompt assembly, tool calls и policy gates;
- часть шагов может уходить в background;
- ошибка может проявиться не там, где она возникла.

Если все это смотреть только через “плоские” логи, ты быстро теряешь причинно-следственную связь. Видно шум, но не видно историю run.

Именно поэтому observability для агентных систем лучше начинать с traces, а не с надежды, что потом кто-нибудь разберется по grep.

## 2. Trace это история одного run, а span это его осмысленный шаг

Очень полезно закрепить простую модель:

- `trace` описывает весь путь запроса или run;
- `span` описывает отдельный шаг внутри этого пути;
- `structured events` добавляют точные факты, которые не стоит прятать в свободный текст.

Это особенно удобно для агентных систем, где один run может включать:

- policy evaluation;
- retrieval;
- model inference;
- tool execution;
- approval wait;
- background memory update.

Когда эта структура есть, команда начинает смотреть на систему не как на хаотичную череду вызовов, а как на цепочку наблюдаемых решений.

## 3. Что стоит делать отдельными spans

Не нужно делать отдельный span на каждую мелочь. Но и один giant span на весь run почти бесполезен.

Хороший practical rule:

- отдельный span на orchestration step;
- отдельный span на retrieval;
- отдельный span на model call;
- отдельный span на каждый tool call;
- отдельный span на policy decision, если она влияет на поведение;
- отдельный span на human approval wait, если он есть.

Тогда trace остается читаемым и при этом дает реальную картину, где именно ушло время, деньги и надежность.

<div class="diagram-card">
<p>У взрослого agent run trace должен показывать не только модель, но и все важные control points</p>

``` mermaid
flowchart LR
    A["User request"] --> B["Run trace"]
    B --> C["Policy span"]
    B --> D["Retrieval span"]
    B --> E["Model span"]
    B --> F["Tool span"]
    B --> G["Approval span"]
    B --> H["Memory update span"]
```

</div>

## 4. Structured events нужны там, где plain text только мешает

Частая ошибка: полезные operational facts уходят в человекочитаемый лог, а потом по ним невозможно строить аналитику или расследование.

Structured events особенно полезны для:

- policy decisions;
- tool outcomes;
- prompt assembly metadata;
- token usage;
- cost attribution;
- idempotency keys;
- tenant and principal context;
- memory writes.

То есть event должен отвечать не на вопрос “что бы написать в лог”, а на вопрос “что потом понадобится анализировать машинно?”

## 5. Хорошая trace model показывает control plane, а не только LLM latency

Если observability сводится только к времени ответа модели, команда получает очень искаженную картину.

На практике run часто ломается или деградирует в других местах:

- retrieval стал возвращать шум;
- policy engine начал слишком часто блокировать действия;
- approval wait растянулся;
- tool adapter деградировал;
- background updates забили очередь;
- prompt assembly раздула контекст.

Поэтому хорошая trace model должна покрывать весь control flow, а не только inference step.

## 6. Минимальный набор полей для trace и spans

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

Без этого observability быстро становится красивой, но не очень полезной.

## 7. Пример structured event для tool execution

Ниже очень простой шаблон, который хорошо показывает стиль мышления:

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

Такой event намного полезнее, чем строка вроде “ticket tool ok”.

## 8. Простой кодовый пример span emission

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

Этот пример нарочно простой. Его задача не заменить tracing SDK, а показать принцип: каждый шаг должен оставлять после себя структурированный след.

## 9. Что особенно важно не логировать как есть

Observability не должна превращаться в утечку данных.

Поэтому в traces и events нужно очень аккуратно обращаться с:

- полными prompt bodies;
- сырыми retrieved documents;
- секретами и токенами;
- PII;
- содержимым чувствительных tool payloads.

Практическое правило простое:

- логируй metadata и derived facts;
- логируй identifiers и hashes, где это помогает;
- полные чувствительные payloads не клади в общие telemetry pipelines без особой причины.

## 10. Что чаще всего ломается в agent observability

Проблемы здесь очень узнаваемы:

- trace покрывает только model call;
- tool calls не связаны с исходным run;
- policy decisions видны в коде, но не видны в telemetry;
- события есть, но без tenant/principal context;
- spans слишком крупные или слишком шумные;
- event schema меняется хаотично, и аналитика ломается.

Если это происходит, команда снова начинает жить на догадках и ручном чтении логов.

## 11. Практический чеклист

Если хочешь быстро проверить свою observability-модель, пройди по вопросам:

- Можно ли восстановить полный путь одного run по одному `trace_id`?
- Есть ли отдельные spans для retrieval, model calls, tool calls и policy gates?
- Логируются ли idempotency keys и policy decision ids?
- Есть ли tenant/principal context в telemetry?
- Можно ли увидеть, где run провел время и где выросла стоимость?
- Не утекают ли чувствительные payloads в traces?
- Стабильна ли schema structured events?

Если на несколько пунктов подряд ответ “нет”, observability у тебя пока декоративная, а не operational.

## 12. Что читать дальше

Следующий шаг здесь очень естественный: после traces и structured events нужно формализовать, что вообще считается “здоровой” агентной системой. То есть перейти к SLO.

- [Глава 10. Idempotency, retries, rate limits и rollback boundaries](../part-iv/chapter-10.md)
- [Глава 12. SLO для агентных систем](chapter-12.md)
- [Часть V. Надежность и observability](index.md)
- [Источники](../../appendix/sources.md)
