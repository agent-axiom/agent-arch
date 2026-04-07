# Глава 18. Чеклист промышленного запуска

## 1. Почему хороший рантайм еще не означает готовность к промышленному запуску

Даже если у тебя уже есть:

- аккуратный runtime;
- слой политик;
- каталог возможностей;
- observability и eval loop,

это все еще не означает, что систему безопасно выкатывать в production.

Production readiness отличается от “демо работает” одной простой вещью: ты должен понимать не только как система работает в норме, но и как она будет вести себя под давлением, при сбоях и в неприятных сценариях.

Именно поэтому нужен чеклист запуска.

## 2. Чеклист нужен не как бюрократия, а как защита от самообмана

Почти каждая команда хотя бы раз попадала в ситуацию:

- “вроде все проверили”;
- “на тестовых кейсах было нормально”;
- “мы думали, что approval точно сработает”;
- “мы не ожидали такого входа”.

Чеклист полезен не потому, что команды безответственные. Он полезен потому, что агентные системы слишком легко создают ложное ощущение готовности.

Хороший чеклист запуска вытаскивает скрытые дыры до инцидента, а не после.

## 3. Что обязательно должно быть проверено перед go-live

Для agent platform обычно есть хотя бы семь обязательных блоков:

- runtime correctness;
- safety and policy;
- capability execution;
- observability;
- eval and SLO readiness;
- operational readiness;
- ownership and rollback plan.

Если хоть один из этих блоков по-настоящему не закрыт, система уже потенциально уязвима к неприятным surprises.

## 4. Runtime correctness

Здесь полезно спросить очень приземленные вещи:

- проходит ли happy path;
- ограничено ли число tool hops;
- корректно ли обрабатываются empty / malformed inputs;
- не ломается ли запуск при пустом извлечении контекста;
- безопасно ли ведет себя runtime при model failure;
- отделены ли foreground и background actions.

Это базовый слой. Если он шатается, все следующие проверки уже менее полезны.

## 5. Safety and policy readiness

Перед rollout особенно важно проверить:

- есть ли pre-check и egress guardrails;
- видны ли решения политик в трассировке;
- high-risk actions действительно требуют approval;
- нет ли direct access paths мимо gateway;
- memory writes ограничены policy;
- multi-tenant boundaries проверены на реальных сценариях.

Именно здесь команды чаще всего переоценивают готовность: policy может существовать в коде, но быть не встроенной во все нужные ветки.

## 6. Capability readiness

Каждый capability, который идет в production, полезно прогонять по короткому operational шаблону:

- есть ли owner;
- ясен ли transport;
- есть ли timeout;
- есть ли retry policy;
- есть ли idempotency strategy;
- ясен ли unknown side effect path;
- есть ли telemetry на outcome.

Если capability не проходит этот минимум, он еще не production capability, а просто удобная интеграция.

<div class="diagram-card">
<p>Go-live готовность полезно мыслить как пересечение нескольких контуров, а не как один общий статус</p>

``` mermaid
flowchart LR
    A["Runtime"] --> H["Production ready"]
    B["Safety"] --> H
    C["Capabilities"] --> H
    D["Observability"] --> H
    E["Eval and SLO"] --> H
    F["Ops readiness"] --> H
    G["Ownership and rollback"] --> H
```

</div>

## 7. Observability and eval readiness

Очень частая ошибка: выкатывать систему, надеясь потом “добавить нормальную трассировку”.

До production стоит убедиться, что:

- у каждого run есть `trace_id`;
- ключевые спаны уже есть;
- policy decisions и tool outcomes видны;
- SLO заведены;
- offline evals проходят;
- regression gate задокументирован;
- online monitoring готово к первым rollout waves.

Если этого нет, первый же инцидент превращается в расследование вслепую.

## 8. Operational readiness

Отдельный слой, который часто забывают:

- есть ли owner on-call;
- есть ли alerting на SLO burn и safety incidents;
- понятен ли manual fallback;
- известна ли процедура rollback;
- есть ли лимиты на rollout blast radius;
- есть ли runbook на частые сбои.

Иногда кажется, что это “не про агентов, а про ops”. На деле без этого агентная система остается лабораторной, а не production-grade.

## 9. Пример политики чеклиста запуска

Ниже очень практичный шаблон:

```yaml
rollout:
  require:
    - trace_coverage
    - policy_prechecks
    - capability_owners
    - offline_eval_pass
    - slo_defined
    - rollback_plan
    - oncall_owner
  rollout_mode:
    initial: canary
    max_tenant_exposure_pct: 5
    require_shadow_period: true
  block_if:
    - unknown_side_effect_path_missing
    - direct_tool_access_present
    - policy_decisions_not_traced
```

Такой checklist хорош тем, что делает readiness предметом инженерного разговора, а не уверенности в голосе автора релиза.

## 10. Простой кодовый пример readiness gate

Ниже каркас, который показывает, как readiness можно оценивать как набор обязательных условий:

```python
from dataclasses import dataclass


@dataclass
class RolloutReadiness:
    trace_coverage: bool
    offline_eval_pass: bool
    slo_defined: bool
    rollback_plan: bool


def ready_for_rollout(state: RolloutReadiness) -> bool:
    return (
        state.trace_coverage
        and state.offline_eval_pass
        and state.slo_defined
        and state.rollback_plan
    )
```

Очень простой пример, но он помогает держать одну важную мысль: production readiness должна быть формализуема.

## 11. Что чаще всего ломается в go-live процессе

Проблемы очень узнаваемы:

- rollout идет сразу на слишком большой трафик;
- команда считает трассировку “неблокирующей мелочью”;
- ownership формально есть, но on-call не готов;
- rollback plan звучит как “ну откатим, если что”;
- capability owners не знают о реальном release window;
- safety regressions не считаются blocker'ом.

Все это означает, что rollout process у тебя пока еще не production discipline, а просто optimistic shipping.

## 12. Практический чеклист

Если хочешь быстро проверить readiness перед выкладкой, пройди по вопросам:

- Есть ли формальный readiness gate?
- Ясны ли owner и on-call на этот rollout?
- Пройдут ли трассы, решения политик и результаты инструментов сквозь телеметрию?
- Есть ли canary/shadow этап?
- Есть ли rollback plan и ограничение blast radius?
- Проверены ли high-risk flows отдельно, а не только happy path?

Если на несколько вопросов подряд ответ “нет”, rollout лучше считать неготовым, даже если демо выглядит уверенно.

## 13. Что читать дальше

На этом reference implementation уже выглядит как цельный operational skeleton. Дальше можно либо расширять ее примерами кода, либо переходить к polishing: переводы, диаграммы, практические appendices и более конкретные implementation snippets.

## 14. Полезные справочные страницы

- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема policy bundle и approval contract](../../appendix/policy-bundle-schema.md)
- [Схема lifecycle-артефактов](../../appendix/lifecycle-artifact-schema.md)

- [Глава 17. Слой политик и каталог возможностей](chapter-17.md)
- [Часть VII. Эталонная реализация](index.md)
- [Источники](../../appendix/sources.md)
