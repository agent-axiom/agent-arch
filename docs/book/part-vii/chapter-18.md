# Глава 18. Чеклист промышленного запуска

## 1. Начнем с момента, когда команда должна сказать “да” или “нет”

Продолжим тот же support-кейс.

Команда уже прошла длинный путь:

- описала архитектуру;
- встроила policy layer;
- развела memory и tool execution;
- завела traces и structured events;
- починила дублирующийся тикет после неудачного retry.

Теперь наступает самый неприятный вопрос:

> Можно ли выпускать этого агента хотя бы на первые 5% tenant-ов?

Именно здесь обычно ломается разница между “мы многое построили” и “систему правда можно выкатывать”.

Даже если у тебя уже есть:

- аккуратный runtime;
- слой политик;
- каталог возможностей;
- observability и eval loop,

это все еще не означает, что систему безопасно запускать в production.

Production readiness отличается от “демо работает” одной вещью: ты должен понимать не только как система ведет себя в happy path, но и как она будет работать под давлением, при сбоях и в неприятных сценариях.

Именно поэтому нужен rollout checklist.

!!! info "Нужны rollout-артефакты?"
    Если тебе нужен reviewable слой поверх текста главы, смотри [схему change review и rollout gate](../../appendix/change-rollout-schema.md) и [схему lifecycle-артефактов](../../appendix/lifecycle-artifact-schema.md).

## 2. Чеклист нужен не как бюрократия, а как защита от самообмана

Почти каждая команда хотя бы раз попадала в знакомую ситуацию:

- “в тестах все было нормально”;
- “мы думали, что approval точно сработает”;
- “мы не ожидали именно такого входа”;
- “если что, быстро откатим”.

Проблема здесь не в безответственности. Проблема в том, что агентные системы слишком легко создают ложное ощущение готовности.

Для того же support-агента опасность особенно понятна: если выкладка пойдет плохо, последствия быстро уйдут во внешний мир:

- появятся дублирующиеся тикеты;
- пользователи увидят неправильные статусы;
- support-команда получит лишний шум;
- расследование начнется уже после того, как side effects произошли.

Хороший чеклист запуска нужен не для галочек, а чтобы вытаскивать скрытые дыры до инцидента, а не после.

## 3. Что обязательно должно быть закрыто перед первой волной rollout

Для agent platform обычно есть как минимум семь обязательных блоков:

- runtime correctness;
- safety and policy;
- capability execution;
- observability;
- eval and SLO readiness;
- operational readiness;
- ownership and rollback plan.

Если хоть один из этих блоков по-настоящему не закрыт, система уже потенциально уязвима к неприятным surprises.

Для нашего support-кейса это означает: прежде чем выпускать даже canary на 5%, команда должна быть готова ответить не только “работает ли happy path”, но и “что именно произойдет при частичном сбое”.

## 4. Runtime correctness

На этом уровне полезно задавать очень приземленные вопросы:

- проходит ли happy path;
- ограничено ли число tool hops;
- корректно ли обрабатываются empty / malformed inputs;
- не ломается ли запуск при пустом retrieval;
- безопасно ли ведет себя runtime при model failure;
- отделены ли foreground и background actions.

Для нашего support-агента это значит, например:

- не создается ли тикет без подтвержденного `request_id`;
- умеет ли run безопасно завершиться, если статус заявки не найден;
- не продолжается ли background write после того, как foreground path уже признан failed.

Это базовый слой. Если он шатается, все следующие проверки уже менее полезны.

## 5. Safety and policy readiness

Перед rollout особенно важно проверить:

- есть ли pre-check и egress guardrails;
- видны ли решения политик в трассировке;
- high-risk actions действительно требуют approval;
- нет ли прямых путей доступа в обход gateway;
- memory writes ограничены policy;
- multi-tenant boundaries проверены на реальных сценариях.

Именно здесь команды чаще всего переоценивают готовность: policy может существовать в коде, но быть не встроенной во все нужные ветки.

Для support-кейса ключевой вопрос звучит так:

> Может ли агент создать тикет, прочитать статус или сохранить профильную запись хотя бы по одному пути, который не пройдет через policy и audit trail?

Если ответ “да” или “не уверены”, rollout еще рано.

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

Для нашего support-агента `create_support_ticket` и `check_access_request_status` выглядят рядом в каталоге, но readiness у них разная:

- read capability может быть готов уже после нормального timeout и telemetry;
- write capability не готов без idempotency, outcome normalization и ясного rollback story.

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
- ключевые spans уже есть;
- policy decisions и tool outcomes видны;
- SLO заведены;
- offline evals проходят;
- regression gate задокументирован;
- online monitoring готово к первым волнам выкладки.

Если этого нет, первый же инцидент превращается в расследование вслепую.

Для нашего support-агента это особенно важно, потому что первые canary tenants почти наверняка принесут неидеальные входы. Если на этих входах команда не увидит:

- какой path выбрал агент;
- был ли duplicate tool call;
- какой `idempotency_key` использовался;
- какой policy gate сработал,

то первая волна выкладки уже превращается в лотерею.

## 8. Operational readiness

Отдельный слой, который часто забывают:

- есть ли owner on-call;
- есть ли alerting на SLO burn и safety incidents;
- понятен ли manual fallback;
- известна ли процедура rollback;
- есть ли лимиты на радиус воздействия rollout;
- есть ли runbook на частые сбои.

Иногда кажется, что это “не про агентов, а про ops”. На деле без этого агентная система остается лабораторной, а не production-grade.

Для support-кейса manual fallback должен быть особенно конкретным:

- кто принимает трафик после отключения агента;
- как остановить write path;
- как пометить сомнительные тикеты, созданные в canary wave;
- кто и как чистит последствия неудачного rollout.

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

Очень простой пример, но он помогает удерживать одну важную мысль: production readiness должна быть формализуема.

## 11. Что чаще всего ломается в процессе запуска

Проблемы очень узнаваемы:

- rollout идет сразу на слишком большой трафик;
- команда считает трассировку “неблокирующей мелочью”;
- ownership формально есть, но on-call не готов;
- rollback plan звучит как “ну откатим, если что”;
- capability owners не знают о реальном release window;
- safety regressions не считаются blocker'ом.

Для support-агента это часто выглядит особенно опасно:

- canary слишком быстро становится broad rollout;
- duplicate ticket incident считается “мелкой интеграционной проблемой”;
- memory write regressions не блокируют релиз;
- команда продолжает rollout, хотя уже не доверяет собственным traces.

Если это происходит, rollout process у тебя пока еще не production discipline, а просто слишком самоуверенный выпуск изменений.

## 12. Что делать сразу после этой главы

Если хочешь быстро проверить readiness перед выкладкой, пройди по вопросам:

1. Есть ли формальный readiness gate?
2. Ясны ли owner и on-call на этот rollout?
3. Пройдут ли traces, решения политик и результаты инструментов сквозь телеметрию?
4. Есть ли canary/shadow этап?
5. Есть ли rollback plan и ограничение blast radius?
6. Проверены ли high-risk flows отдельно, а не только happy path?

Если на несколько вопросов подряд ответ “нет”, rollout лучше считать неготовым, даже если демо прошло хорошо.

## 13. Что читать дальше

На этом эталонная реализация уже закрывает базовый operational skeleton того же support-агента и его платформы. Следующий естественный шаг — lifecycle discipline: как менять, выпускать, расследовать и выводить из эксплуатации такую систему без потери управляемости.

## 14. Полезные справочные страницы

- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)

- [Глава 17. Слой политик и каталог возможностей](chapter-17.md)
- [Часть VII. Эталонная реализация](index.md)
- [Часть VIII. Жизненный цикл агентной системы](../part-viii/index.md)
- [Источники](../../appendix/sources.md)
