# Практика. Manager pattern vs handoffs

## 1. Почему этот выбор вообще важен

Как только команда доходит до multi-agent темы, почти сразу появляется соблазн сделать "красивую" схему:

- один агент планирует;
- другой ищет;
- третий пишет;
- четвертый проверяет;
- и все это выглядит очень впечатляюще на диаграмме.

Проблема в том, что между красивой диаграммой и устойчивой системой лежит большая разница.

На практике один из самых полезных вопросов звучит так:

> Нам здесь нужен manager pattern или handoffs?

Это не эстетический вопрос. Это вопрос:

- кто держит глобальный контекст;
- где живет ответственность за следующий шаг;
- как ограничивать blast radius;
- как потом расследовать сбои.

Практический гайд OpenAI полезен здесь тем, что рекомендует не романтизировать multi-agent по умолчанию, а сначала понять, где на самом деле живет координация и где должна жить ответственность.[^openai-practical]

## 2. Что такое manager pattern

`manager pattern` означает, что у тебя есть один центральный orchestrator, который:

- держит общую цель run;
- решает, какого specialist вызвать;
- получает результаты обратно;
- собирает финальный ответ или следующий план.

Это похоже на модель "менеджер вызывает специалистов как инструменты".

Плюсы manager pattern:

- единая точка контроля;
- проще держать global policy;
- удобнее вести audit trail;
- легче ограничивать budget и max steps.

Минусы:

- manager быстро разрастается в bottleneck;
- в нем скапливается слишком много контекста;
- система может стать хрупкой, если manager ошибается в routing logic.

## 3. Что такое handoff pattern

`handoff pattern` означает, что текущий агент может передать управление другому агенту, и тот уже временно становится "главным" для своей части задачи.

Это ближе к модели "задача переходит к следующему ответственному".

Плюсы handoffs:

- чище разделяются роли и ownership;
- проще изолировать контекст;
- легче строить domain-specialized behaviors;
- меньше риск, что один центральный orchestrator станет перегруженным.

Минусы:

- сложнее видеть глобальную картину run;
- сложнее строить единый audit narrative;
- handoff boundaries нужно проектировать очень аккуратно;
- выше риск потерять state, intent или constraints при передаче.

## 4. Самый полезный практический принцип

Если коротко, то:

- `manager pattern` лучше, когда тебе нужен единый координационный центр;
- `handoffs` лучше, когда задача естественно переходит между разными ролями или доменами.

То есть вопрос не "что современнее", а "где у нас должна жить ответственность".

## 5. Когда manager pattern почти всегда уместен

Manager pattern обычно хорошо работает, если:

- задача короткая или средняя по длине;
- нужен единый budget control;
- tools и policy почти одинаковы для всех подзадач;
- команда хочет максимальную explainability;
- есть один основной runtime owner.

Типичные примеры:

- support triage;
- research assistant с единым финальным ответом;
- internal copilot, который вызывает несколько read-heavy capabilities;
- agent, где specialist-агенты по сути похожи на typed tools.

Здесь manager pattern часто оказывается самым скучным и самым правильным решением.

## 6. Когда handoffs лучше

Handoffs обычно выигрывают, если:

- задача реально проходит через разные domain boundaries;
- каждая роль требует своего контекста и своих guardrails;
- ownership между командами уже разделен;
- полезно локально "сузить голову" текущего агента;
- следующий этап работы больше похож на передачу ответственности, чем на вызов helper-функции.

Типичные примеры:

- sales qualification -> solution agent -> legal review agent;
- incident intake -> security investigation -> remediation coordinator;
- onboarding flow, где этапы принадлежат разным business units.

Тут handoff часто естественнее, чем central manager, который делает вид, что понимает все одинаково хорошо.

## 7. Где системы ломаются чаще всего

У обеих схем есть типовые failure modes.

У manager pattern:

- manager тащит слишком много контекста;
- specialist-агенты становятся слишком тонкими и бессмысленными;
- routing живет в prompt вместо явной policy;
- central orchestrator превращается в single point of confusion.

У handoffs:

- теряются ограничения и intent при передаче;
- следующий агент получает слишком мало или слишком много state;
- неясно, кто отвечает за final outcome;
- trace становится рваным и трудным для чтения.

Поэтому главный вопрос не "какая схема мощнее", а "какую схему ты сможешь эксплуатировать спокойно".

## 8. Простая decision table

Ниже хороший стартовый ориентир.

| Ситуация | Что чаще лучше |
| --- | --- |
| Нужен единый контроль steps, cost и policy | `manager pattern` |
| Роли и домены естественно разделены | `handoffs` |
| Specialist похож на capability tool | `manager pattern` |
| У следующего участника свой context boundary | `handoffs` |
| Важнее единый audit story | `manager pattern` |
| Важнее локальная автономия role-specific agent | `handoffs` |

Эта таблица не заменяет дизайн, но очень хорошо снимает часть лишней романтики.

## 9. Как не ошибиться слишком рано

Самая здоровая стратегия обычно выглядит так:

1. сначала single-agent loop;
2. потом manager pattern, если нужна координация нескольких specialist paths;
3. и только потом handoffs, если уже видно реальные domain boundaries.

Это не догма. Но это хорошая защита от преждевременной сложности.

## 10. Кодовый эскиз: manager pattern

```python
def run_manager(task: str, specialists: dict[str, callable]) -> dict:
    plan = ["research", "draft", "review"]
    results: dict[str, dict] = {}

    for step in plan:
        worker = specialists[step]
        results[step] = worker(task=task, prior_results=results)

    return {"status": "success", "results": results}
```

Здесь manager не "умничает" бесконечно. Он держит план, вызывает specialists и собирает результат.

## 11. Кодовый эскиз: handoff pattern

```python
def handoff(state: dict, next_agent: callable) -> dict:
    transfer_packet = {
        "goal": state["goal"],
        "constraints": state["constraints"],
        "relevant_context": state["relevant_context"],
    }
    return next_agent(transfer_packet)
```

Тут главное не сам вызов, а то, что handoff должен передавать не весь хаос state, а аккуратно собранный transfer packet.

## 12. Что особенно важно для безопасности

Если ты используешь manager pattern, проверь:

- не получает ли manager слишком широкие права;
- не обходит ли он approval boundary "от имени всех";
- не становится ли он точкой, через которую утекут все tenant contexts.

Если ты используешь handoffs, проверь:

- сохраняются ли policy constraints при передаче;
- не теряется ли classification risk;
- не уходит ли untrusted context в следующий agent без маркировки;
- видно ли в trace, кто именно принял управление.

То есть безопасность здесь не "поверх оркестрации". Она часть самой orchestration semantics.

## 13. Практический чеклист

Если хочешь быстро проверить выбор orchestration pattern, пройди по вопросам:

- Кто владеет глобальной целью run?
- Кто отвечает за final outcome?
- Где живет budget control?
- Где живут stop conditions?
- Можно ли из traces понять, кто кому передал задачу и почему?
- Не слишком ли рано ты ушел в handoffs, когда manager pattern был бы проще?
- Не стал ли manager центральным монстром, который делает все сразу?

Если ответы мутные, значит схема пока архитектурно не дозрела.

## 14. Что читать дальше

- [Практика. Instructions, routines и prompt templates](practical-routines.md)
- [Глава 2. Референсная архитектура безопасного агента](chapter-2.md)
- [Часть IV. Инструменты и выполнение](../part-iv/index.md)
- [Источники](../../appendix/sources.md)

[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
