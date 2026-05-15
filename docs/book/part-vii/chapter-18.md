# Глава 18. Чеклист промышленного запуска

## 1. Начнем с момента, когда команда должна сказать “да” или “нет”

Продолжим тот же кейс поддержки.

Команда уже прошла длинный путь:

- описала архитектуру;
- встроила слой политик;
- развела память и исполнение инструментов;
- завела трассы и структурированные события;
- починила дублирующийся тикет после неудачной повторной попытки.

Теперь наступает самый неприятный вопрос:

> Можно ли выпускать этого агента хотя бы на первые 5% tenants?

Именно здесь обычно ломается разница между “мы многое построили” и “систему правда можно выкатывать”.

Именно в этом состоит главная задача этой главы. Она должна помочь читателю перейти еще через одну границу: от просто работающей и управляемой системы к системе, которую команда действительно готова выпускать в момент решения о запуске.

Даже если у тебя уже есть:

- аккуратный рантайм;
- слой политик;
- каталог возможностей;
- наблюдаемость и контур оценок,

это все еще не означает, что систему безопасно запускать в production.

Готовность к production отличается от “демо работает” одной вещью: ты должен понимать не только как система ведет себя в штатном сценарии, но и как она будет работать под давлением, при сбоях и в неприятных сценариях.

Для этого и нужен чеклист раскатки.

!!! info "Нужны rollout-артефакты?"
    Если тебе нужен проверяемый слой поверх текста главы, смотри [схему change review и rollout gate](../../appendix/change-rollout-schema.md) и [схему lifecycle-артефактов](../../appendix/lifecycle-artifact-schema.md).

## 2. Чеклист нужен не как бюрократия, а как защита от самообмана

Почти каждая команда хотя бы раз попадала в знакомую ситуацию:

- “в тестах все было нормально”;
- “мы думали, что approval точно сработает”;
- “мы не ожидали именно такого входа”;
- “если что, быстро откатим”.

Проблема здесь не в безответственности. Проблема в том, что агентные системы слишком легко создают ложное ощущение готовности.

Для того же агента поддержки опасность особенно понятна: если выкладка пойдет плохо, последствия быстро уйдут во внешний мир:

- появятся дублирующиеся тикеты;
- пользователи увидят неправильные статусы;
- команда поддержки получит лишний шум;
- расследование начнется уже после того, как побочные эффекты произошли.

Это не теоретический риск: даже пользовательский AI-сценарий может превратиться во внешний ущерб и обязательство компании, как показал кейс Moffatt v. Air Canada.[^moffatt]

Хороший чеклист запуска нужен не для галочек, а чтобы вытаскивать скрытые дыры до инцидента, а не после.

## 3. Что обязательно должно быть закрыто перед первой волной rollout

Именно так на практике и выглядит дисциплина rollout. Команда решает не то, “выглядит ли фича многообещающе”, а то, достаточно ли хорошо проверен каждый контур, от которого зависит релиз, чтобы система выдержала частичный сбой, паузу, drift и rollback.

Для агентной платформы обычно есть как минимум семь обязательных блоков:

- корректность рантайма;
- safety and policy;
- исполнение возможностей;
- наблюдаемость;
- готовность eval и SLO;
- операционная готовность;
- ownership and rollback plan.

Если хоть один из этих блоков по-настоящему не закрыт, система уже потенциально уязвима к неприятным сюрпризам. Rollout здесь стоит воспринимать как вопрос сходимости нескольких контуров, а не как один зеленый сигнал, принадлежащий одной команде.

Для нашего кейса поддержки это означает: прежде чем выпускать даже canary на 5%, команда должна быть готова ответить не только “работает ли happy path”, но и “что именно произойдет при частичном сбое”.

!!! example "Сквозной кейс: canary после дубля"
    Перед 5% rollout агента поддержки команда должна показать не только успешный статус-чек и создание тикета. Разбор должен показать, что duplicate-ticket regression gate пройден, `create_support_ticket` имеет idempotency strategy, `side_effect_unknown` останавливает запуск до reconcile, traces сохраняют outcome, а rollback owner уже назначен. Иначе canary проверяет надежду, а не готовность.

**Rollout case-spine note:** production checklist должен отдельно закрывать все три canonical cases. Support triage требует duplicate-ticket regression gate, approval coverage, idempotency strategy и rollback owner. Internal knowledge assistant требует retrieval freshness gate, source-grounding evals, tenant-boundary checks и memory-write review. Incident coordination требует escalation-drill evidence, notification delivery checks, responder handoff owner и post-incident regression plan перед canary.

## 4. Корректность рантайма

На этом уровне полезно задавать очень приземленные вопросы:

- проходит ли happy path;
- ограничено ли число tool hops;
- корректно ли обрабатываются empty / malformed inputs;
- не ломается ли запуск при пустом retrieval;
- безопасно ли ведет себя рантайм при model failure;
- отделены ли foreground и background actions.

Для нашего агента поддержки это значит, например:

- не создается ли тикет без подтвержденного `request_id`;
- умеет ли запуск безопасно завершиться, если статус заявки не найден;
- не продолжается ли background write после того, как foreground path уже признан failed.

Это базовый слой. Если он шатается, все следующие проверки уже менее полезны.

## 5. Готовность safety и policy

Перед rollout особенно важно проверить:

- есть ли pre-check и egress guardrails;
- видны ли решения политик в трассировке;
- high-risk actions действительно требуют approval;
- нет ли прямых путей доступа в обход gateway;
- memory writes ограничены policy;
- multi-tenant boundaries проверены на реальных сценариях.

Именно здесь команды чаще всего переоценивают готовность: policy может существовать в коде, но быть не встроенной во все нужные ветки.

Для кейса поддержки ключевой вопрос звучит так:

> Может ли агент создать тикет, прочитать статус или сохранить профильную запись хотя бы по одному пути, который не пройдет через policy и audit trail?

Если ответ “да” или “не уверены”, rollout еще рано.

## 6. Готовность capability

Каждую возможность, которая идет в production, полезно прогонять по короткому операционному шаблону:

- есть ли owner;
- ясен ли transport;
- есть ли timeout;
- есть ли retry policy;
- есть ли idempotency strategy;
- ясен ли unknown side effect path;
- есть ли telemetry для outcome.

Если возможность не проходит этот минимум, это еще не production-возможность, а просто удобная интеграция.

Для нашего агента поддержки `create_support_ticket` и `check_access_request_status` выглядят рядом в каталоге, но readiness у них разная:

- read capability может быть готов уже после нормального timeout и telemetry;
- write capability не готов без idempotency, outcome normalization и ясного rollback story.

<div class="diagram-card">
<p>Go-live готовность полезно мыслить как пересечение нескольких контуров, а не как один общий статус</p>

``` mermaid
flowchart LR
    A["Рантайм"] --> H["Готовность к production"]
    B["Безопасность"] --> H
    C["Возможности"] --> H
    D["Наблюдаемость"] --> H
    E["Eval и SLO"] --> H
    F["Готовность ops"] --> H
    G["Ownership и rollback"] --> H
```

</div>

## 7. Готовность observability и eval

Очень частая ошибка: выкатывать систему, надеясь потом “добавить нормальную трассировку”.

До production стоит убедиться, что:

- у каждого запуска есть `trace_id`;
- ключевые spans уже есть;
- policy decisions и tool outcomes видны;
- SLO заведены;
- offline evals проходят;
- для затронутых high-risk paths отдельно прогнаны failed-run drills;
- получившиеся failed paths остаются traceable через trace linkage, release identity, session-level evidence и экспортируемые поля вроде `failure_reason`;
- качество verifier'а reviewed там, где release evidence зависит от graded judgments;
- regression gate задокументирован;
- online monitoring готово к первым волнам выкладки.

Если этого нет, первый же инцидент превращается в расследование вслепую.

Для нашего агента поддержки это особенно важно, потому что первые canary tenants почти наверняка принесут неидеальные входы. Если на этих входах команда не увидит:

- какой путь выбрал агент;
- был ли duplicate tool call;
- какой `idempotency_key` использовался;
- какой policy gate сработал,

то первая волна выкладки уже превращается в лотерею.

## 8. Готовность approval path

Как только approval становится явным runtime path, готовность rollout должна включать и этот путь.

У команды могут быть правильные policy rules на бумаге, но система все равно не готова к production, если approval создает скрытые очереди, неясное ownership или бесконечно paused runs.

Перед rollout полезно проверить:

- измеряется ли approval latency;
- есть ли owner у approval queue;
- есть ли timeout или правило истечения ожидания для приостановленных запусков;
- есть ли видимый порог накопившейся очереди;
- определено ли поведение resume/cancel;
- есть ли запасной путь на случай, если human review недоступен;
- считается ли истечение capability-session видимым сигналом rollout, а не скрытым сбоем транспорта;
- определено ли поведение re-initialization, если stateful capability session уже нельзя безопасно продолжить.

Для того же агента поддержки это важно сразу. Если путь создания тикета ставится на паузу ожидания approval, команда должна знать, будет ли запуск ждать пять секунд, тридцать минут или вечно. Это не UX-деталь, а часть поведения системы в production.

Очень практичный rollout gate звучит так:

> Понимаем ли мы, сколько запусков сейчас стоит на паузе approval, как долго они уже ждут, что система сделает, если вовремя никто не ответит, и что рантайм сделает, если underlying capability session истечет еще раньше?

Если ответ отрицательный, значит approval все еще работает как неуправляемый боковой канал.

### 8.1. Interruptions в stateful capability тоже должны входить в rollout readiness

Как только approval сочетается со stateful MCP или другой resumable capability session, rollout readiness уже обязана включать interruption semantics напрямую.

Это означает, что команда должна уметь отвечать хотя бы на такие вопросы:

- сколько запусков ждут human approval, пока capability session еще жива;
- сколько уже прошло через capability-session expiry и теперь требуют re-init;
- сохраняет ли re-initialization тот же user-visible run id или создает новую operational thread;
- запускает ли шаг после re-init fresh policy decision;
- может ли telemetry связать исходное paused state с resumed или reinitialized state.

Без этих ответов rollout может выглядеть здоровым на слое approval, но уже деградировать глубже, на слое capability-session.

Таксономия workflow-паттернов у Anthropic добавляет сюда еще одно rollout-измерение.[^anthropic] Рантайм должен учитывать выбранный паттерн workflow и считать изменения orchestration pattern поведением, значимым для релиза, а не невидимой деталью реализации.

Их более поздняя работа про harness design делает rollout-вывод еще жестче.[^anthropic-harness] Как только система опирается на разделение planner/generator/evaluator, sprint contracts и структурированные handoff artifacts между длинными сессиями, rollout уже нельзя оценивать только по финальному пользовательскому результату. Команда должна отдельно проверять, сохраняют ли resets, evaluator feedback и handoff artifacts тот же release contract на протяжении многочасового выполнения.

Перед rollout команда должна уметь явно сказать:

- использует ли path теперь `routing`, хотя раньше там был fixed workflow;
- приносит ли `parallelization` новый риск вокруг join-state, duplicate-read или approval-ordering;
- добавляет ли `orchestrator-workers` delegated worker surfaces, worker-safe catalogs или новые review points;
- вставляет ли `prompt chaining` новые checkpoints, в которых меняются expiry, pause или retry semantics.

Это важно, потому что смена паттерна меняет поведение системы в production, даже если пользовательская функция на словах остается той же.

То же самое верно и для delegated authorization. Если runtime поддерживает user-delegated access, readiness rollout должна включать еще и такие вопросы:

- сохраняют ли traces `authorization_mode`, delegated principal и delegated scope;
- удерживают ли approval records тот же authorization context, что и исходный run;
- показывает ли session export, под какой delegated identity вообще выполнялось действие;
- что делает runtime, если delegated access отзывают, пока запуск стоит на паузе.

Иначе команда может казаться готовой по policy и approval, но все еще не сумеет объяснить, кто именно авторизовал write path в production.

## 9. Операционная готовность

Отдельный слой, который часто забывают:

- есть ли ответственный on-call;
- есть ли alerting на выгорание SLO и safety incidents;
- понятен ли ручной fallback;
- известна ли процедура rollback;
- есть ли лимиты на радиус воздействия rollout;
- есть ли runbook на частые сбои.

Иногда кажется, что это “не про агентов, а про ops”. На деле без этого агентная система остается лабораторной, а не готовой к production.

Для кейса поддержки manual fallback должен быть особенно конкретным:

- кто принимает трафик после отключения агента;
- как остановить write path;
- как пометить сомнительные тикеты, созданные в canary wave;
- кто и как чистит последствия неудачного rollout.

## 10. Практические правила для готовности к rollout

Если нужен короткий операционный каркас, обычно достаточно таких правил:

1. Ни один rollout не должен начинаться без trace coverage, rollback plan и понятного owner.
2. Ни один write capability не должен идти в canary без idempotency, outcome normalization и policy visibility.
3. High-risk flows нужно проверять отдельно от happy path.
4. Canary, shadow и blast-radius limits должны быть частью design, а не аварийной импровизацией.
5. Approval queues, возраст paused runs и backlog human review должны считаться rollout signals, а не невидимым операционным шумом.
6. Изменения в выборе orchestration pattern должны рассматриваться как runtime-control changes и проходить явный review до rollout.
7. Если release evidence зависит от verifier judgments, rollout надо останавливать, когда команда больше не доверяет качеству verifier'а или linkage его evidence.
8. Если команда уже не доверяет traces, approval handling или evals, rollout надо останавливать, а не “донаблюдать в проде”.

## 11. Пример политики чеклиста запуска

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
    - approval_queue_owner
    - session_expiry_signals_visible
    - orchestration_pattern_reviewed
  rollout_mode:
    initial: canary
    max_tenant_exposure_pct: 5
    require_shadow_period: true
  block_if:
    - unknown_side_effect_path_missing
    - direct_tool_access_present
    - policy_decisions_not_traced
    - approval_backlog_unbounded
    - paused_runs_without_expiry
    - capability_session_reinit_unmodeled
    - orchestration_pattern_change_unreviewed
```

Такой checklist хорош тем, что делает готовность предметом инженерного разговора, а не уверенности в голосе автора релиза.

## 12. Простой кодовый пример gate готовности

Ниже каркас, который показывает, как готовность можно оценивать как набор обязательных условий:

```python
from dataclasses import dataclass


@dataclass
class RolloutReadiness:
    trace_coverage: bool
    offline_eval_pass: bool
    slo_defined: bool
    rollback_plan: bool
    approval_path_defined: bool


def ready_for_rollout(state: RolloutReadiness) -> bool:
    return (
        state.trace_coverage
        and state.offline_eval_pass
        and state.slo_defined
        and state.rollback_plan
        and state.approval_path_defined
    )
```

Очень простой пример, но он помогает удерживать одну важную мысль: готовность к production должна быть формализуемой.

## 13. Что чаще всего ломается в процессе запуска

Проблемы очень узнаваемы:

- rollout идет сразу на слишком большой трафик;
- команда считает трассировку “неблокирующей мелочью”;
- ownership формально есть, но on-call не готов;
- rollback plan звучит как “ну откатим, если что”;
- capability owners не знают о реальном release window;
- safety regressions не считаются blocker'ом;
- paused runs накапливаются, потому что у approval queue нет owner;
- approval latency становится видимой только тогда, когда пользователи уже ждут.

Для агента поддержки это часто выглядит особенно опасно:

- canary слишком быстро становится broad rollout;
- duplicate ticket incident считается “мелкой интеграционной проблемой”;
- memory write regressions не блокируют релиз;
- команда продолжает rollout, хотя уже не доверяет собственным traces.

Если это происходит, rollout process у тебя пока еще не стал производственной дисциплиной, а остается просто слишком самоуверенным выпуском изменений.

## 14. Быстрый тест зрелости для готовности к rollout

Команде не стоит думать, что она готова к production, только потому, что демо работает, checklist в целом зеленый, а первый canary кажется маленьким.

Более сильная планка такая:

- high-risk paths проверены отдельно от happy path;
- traces, policy visibility и rollback действительно заслуживают доверия до расширения rollout;
- write capabilities имеют idempotency и явный unknown-outcome path;
- blast radius ограничен дизайном, а не оптимизмом команды;
- backlog approval, timeout и resume/cancel behavior заданы явно;
- ownership, on-call и manual fallback описаны конкретно.

Если большинство этих условий не выполняется, у команды уже может быть инерция запуска, но реальной готовности к rollout у нее пока нет.

## 15. Что делать сразу после этой главы

Если хочешь быстро проверить readiness перед выкладкой, пройди по короткому списку:

1. Есть ли формальный gate готовности?
2. Ясны ли owner и on-call на этот rollout?
3. Пройдут ли traces, решения политик и результаты инструментов сквозь телеметрию?
4. Есть ли canary/shadow этап?
5. Есть ли rollback plan и ограничение blast radius?
6. Проверены ли high-risk flows отдельно, а не только happy path?
7. Есть ли у approval видимое правило timeout/backlog для paused runs?

Если на несколько вопросов подряд ответ “нет”, rollout лучше считать неготовым, даже если демо прошло хорошо.

## 16. Что читать дальше

На этом эталонная реализация уже закрывает базовый операционный каркас того же агента поддержки и его платформы. Следующий шаг здесь уже lifecycle discipline: как менять, выпускать, расследовать и выводить из эксплуатации такую систему без потери управляемости.

## 17. Полезные справочные страницы

- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)

Эта глава превращает управляемый runtime path из главы 17 в дисциплину rollout. Те же approval, pause/resume и control signals затем прямо продолжаются в главе 21 уже как часть assurance loop.

- [Глава 17. Слой политик и каталог возможностей](chapter-17.md)
- [Часть VII. Эталонная реализация](index.md)
- [Часть VIII. Жизненный цикл агентной системы](../part-viii/index.md)
- [Источники](../../appendix/sources.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^moffatt]: American Bar Association, [BC Tribunal Confirms Companies Remain Liable for Information Provided by AI Chatbot](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
