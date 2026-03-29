# Глава 12. SLO для агентных систем

## 1. Почему обычного uptime для агентов недостаточно

Когда система становится агентной, классическая картина “сервис доступен или недоступен” перестает покрывать реальность.

Даже если все технически работает, агентная система может быть нездоровой:

- run завершается слишком медленно;
- стоимость одного запроса уехала вверх;
- tool calls стали чаще ошибаться;
- доля полезных ответов просела;
- система слишком часто уходит в human escalation;
- policy gate стал блокировать нормальные сценарии.

То есть одного `99.9% uptime` здесь почти никогда недостаточно. Нужно измерять не только доступность компонента, но и качество работы целого run.

## 2. SLO для агента должны описывать поведение системы, а не отдельных библиотек

Очень частая ошибка: брать метрики отдельных частей и выдавать их за health всей платформы.

Например:

- latency модели;
- uptime vector store;
- p95 у конкретного API;
- количество ошибок в adapter.

Все это полезно, но само по себе не отвечает на главный вопрос: “Пользователь получает хороший результат в разумное время и в безопасной форме?”

Поэтому SLO для агентных систем лучше строить вокруг run-level outcomes.

## 3. Какие SLO обычно реально имеют смысл

Для production-grade агентной системы чаще всего полезны хотя бы четыре группы:

- success SLO;
- latency SLO;
- safety SLO;
- cost SLO.

Иногда добавляют еще:

- escalation SLO;
- freshness SLO для retrieval;
- tool success SLO для критичных capabilities.

Важно не пытаться измерить все сразу. Лучше выбрать небольшой набор, который действительно влияет на пользовательский результат и operational stability.

## 4. Success SLO должен быть ближе к задаче, а не к HTTP 200

Одна из самых опасных ловушек: считать успешным любой run, который “не упал”.

Но пользовательский опыт совсем не про это. Run может:

- завершиться формально успешно, но дать бесполезный ответ;
- пройти без exception, но нарушить policy;
- вернуть текст вместо нужного действия;
- создать частичный side effect и не довести задачу до конца.

Поэтому success SLO стоит связывать с чем-то вроде:

- task completed;
- expected artifact produced;
- approved action completed;
- answer accepted without escalation.

Это уже гораздо ближе к реальному качеству системы.

## 5. Latency SLO для агента нужно считать по этапам, а не только целиком

Общий p95 по run очень полезен, но его одного мало. Если ты не видишь вклад этапов, то не поймешь, что именно уехало:

- retrieval;
- model inference;
- tool execution;
- approval wait;
- background queue pressure.

Поэтому у зрелой системы обычно есть:

- end-to-end run latency;
- p95/p99 для model spans;
- tool execution latency;
- queue wait time;
- approval delay, если approval часть продукта.

Так latency SLO превращается из красивой цифры в рабочий инструмент диагностики.

## 6. Safety SLO очень часто важнее чистой скорости

Для агентных систем безопасность это не только правило в policy engine, но и наблюдаемая цель качества.

Safety SLO могут включать:

- долю runs без policy violations;
- долю runs без cross-tenant retrieval;
- долю runs без sensitive egress incidents;
- долю write-actions без unknown side effect;
- coverage approval для high-risk операций.

Это особенно важно, когда команда слишком сильно фокусируется на “быстрее и дешевле” и начинает незаметно размывать guardrails.

<div class="diagram-card">
<p>SLO для агентных систем почти всегда живут в нескольких измерениях одновременно</p>

``` mermaid
flowchart LR
    A["Agent system health"] --> B["Success"]
    A --> C["Latency"]
    A --> D["Safety"]
    A --> E["Cost"]
    A --> F["Escalation"]
```

</div>

## 7. Cost SLO помогает остановить тихую деградацию

У агентных систем есть неприятная особенность: стоимость может расти тихо и без видимого инцидента.

Например:

- retrieval возвращает слишком много контекста;
- planner делает лишние шаги;
- модель стала чаще вызывать tools;
- retries незаметно раздули run;
- память стала тащить в prompt лишние summaries.

Поэтому cost SLO полезно строить как минимум на:

- cost per successful run;
- tokens per run;
- tool calls per run;
- expensive model usage rate.

Иначе система может оставаться “рабочей”, но перестать быть экономически вменяемой.

## 8. Escalation SLO помогают не перегрузить людей

Если у тебя есть human-in-the-loop, это не бесплатный fallback.

Система, которая:

- слишком часто требует approval;
- слишком часто уходит в manual reconciliation;
- слишком часто просит человека принять решение,

может выглядеть безопасной, но на деле просто перекладывает хаос на операторов.

Поэтому полезно отслеживать:

- escalation rate;
- approval rate для high-risk flows;
- median time to human decision;
- долю runs, завершенных без manual intervention.

## 9. Пример SLO policy для agent platform

Ниже не “канонический” шаблон, а просто хороший способ мыслить о целях явно:

```yaml
slo:
  success:
    successful_run_rate: ">= 97%"
  latency:
    run_p95_ms: "<= 12000"
    tool_span_p95_ms: "<= 2500"
  safety:
    policy_violation_rate: "< 0.2%"
    unknown_side_effect_rate: "< 0.05%"
  cost:
    avg_tokens_per_run: "<= 18000"
    avg_cost_per_successful_run_usd: "<= 0.12"
  escalation:
    manual_intervention_rate: "< 8%"
```

Главное здесь не точные числа, а сама дисциплина. Команда должна договориться, что именно считается здоровьем системы.

## 10. Простой кодовый пример health classification

Ниже каркас, который показывает, как run можно оценивать не по одной метрике, а по набору измерений.

```python
from dataclasses import dataclass


@dataclass
class RunHealth:
    successful: bool
    latency_ms: int
    policy_violated: bool
    cost_usd: float


def classify_run_health(run: RunHealth) -> str:
    if run.policy_violated:
        return "safety_failure"
    if not run.successful:
        return "task_failure"
    if run.latency_ms > 12_000:
        return "slow_success"
    if run.cost_usd > 0.12:
        return "expensive_success"
    return "healthy"
```

Это простая идея, но полезная: один и тот же run может быть формально успешным и при этом operationally плохим.

## 11. Что чаще всего ломается в SLO для агентных систем

Типовые проблемы очень повторяемы:

- success считают через HTTP status;
- latency меряют только по model call;
- cost вообще не попадает в health model;
- safety живет отдельно от reliability;
- human escalation не считается частью system health;
- SLO написаны, но ни на что не влияют в rollout.

Если это происходит, SLO превращаются в декорацию для дашборда, а не в механизм управления платформой.

## 12. Practical checklist

Если хочешь быстро проверить свои SLO, пройди по вопросам:

- Есть ли у тебя run-level definition of success?
- Видишь ли ты latency по основным этапам, а не только целиком?
- Есть ли safety SLO, а не только availability?
- Измеряешь ли ты cost per useful outcome?
- Видно ли, сколько нагрузки реально уходит на людей?
- Привязаны ли rollout decisions к SLO, а не только к intuition?

Если на несколько вопросов подряд ответ “нет”, платформа у тебя, возможно, уже наблюдаемая, но пока еще не управляемая через цели качества.

## 13. Что читать дальше

После SLO очень естественно перейти к eval loops: offline evals, online evals, trace grading и regression gates. Именно там observability превращается в постоянный контур улучшения.

- [Глава 11. Traces, spans и structured events](chapter-11.md)
- [Глава 13. Offline evals, online evals и regression gates](chapter-13.md)
- [Часть V. Надежность и observability](index.md)
- [Источники](../../appendix/sources.md)
