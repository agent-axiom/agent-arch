# Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы

!!! info "Актуальность главы"
    Эта глава актуальна на 11 апреля 2026 года.

    Быстрее всего здесь меняются:

    - готовые сервисы для оценки, подходы с моделями-судьями и управляемые контуры проверки;
    - новые наборы тестов для памяти, многотуровой согласованности и поведенческих оценок;
    - вендорские инструменты для online evals и выпуска через формальные шлюзы.

    Медленнее меняются:

    - необходимость держать offline evals, online evals и regression gates как единый контур;
    - привязка оценки к traces, SLO и rollout decisions;
    - инженерная дисциплина: критичные сценарии должны проверяться до релиза, а не после инцидента.

## 1. Начнем с вопроса: как не выпустить тот же сбой второй раз

Продолжим тот же support-кейс.

Команда уже пережила неприятный инцидент:

- агент создал дублирующийся тикет;
- traces помогли восстановить путь run;
- проблема оказалась в неудачном retry path и слабой idempotency discipline;
- баг починили.

Но после этого возникает главный engineering-вопрос:

> Как сделать так, чтобы похожее ухудшение не вернулось через две недели после очередного изменения prompt, policy или tool adapter?

Вот здесь и начинается eval loop.

Traces помогают понять, что произошло.
SLO помогают определить, что считается здоровьем системы.

Но остается главный вопрос: как системно улучшать качество и не выпускать regressions обратно в rollout?

!!! info "Нужны схемы и артефакты?"
    Если тебе нужны не только объяснения, но и рабочие схемы, открой [схему трасс и каталог событий](../../appendix/trace-schema.md) и [схему eval-наборов и контракта на проверку](../../appendix/eval-schema.md).

## 2. Offline evals нужны, чтобы менять систему до выката

Офлайн-оценки отвечают на очень практичный вопрос:

> Если мы меняем prompt, policy, retrieval, model routing или tool behavior, станет ли система лучше или хуже на известных критичных сценариях?

Для нашего support-агента хороший offline set должен включать не только приятные happy path cases, но и вещи, которые уже били по системе:

- duplicate ticket scenarios;
- timeout после side effect;
- ambiguous user request;
- approval-required flow;
- stale memory retrieval;
- cross-tenant privacy-sensitive case.

Сила offline evals в том, что они позволяют сравнивать версии системы **до** production traffic.

## 3. Online evals нужны, потому что реальный мир всегда шире тестового набора

Даже очень хорошие offline evals не покрывают все, что происходит в production:

- пользователи задают новые типы задач;
- распределение входов меняется;
- внешние системы деградируют;
- retrieval база растет;
- policy rules начинают вести себя иначе на новых данных.

Поэтому online evals нужны не как замена offline, а как второй контур:

- оценивать реальное поведение на живом трафике;
- ловить drift;
- замечать silent regressions;
- смотреть, как система ведет себя в настоящих operational условиях.

Для support-агента это означает простую вещь: даже если critical test set чистый, команда все равно должна видеть, не начал ли агент:

- чаще создавать лишние тикеты;
- чаще эскалировать без необходимости;
- хуже работать с неполными статусами;
- дороже проходить тот же run.

## 4. Лучшая связка это не “offline или online”, а оба контура сразу

Очень рабочая модель выглядит так:

- offline evals защищают от очевидных regressions до релиза;
- online evals ловят новые проблемы после релиза;
- traces дают сырье для анализа;
- SLO задают operational рамку;
- regression gates не дают ухудшениям пройти незаметно.

<div class="diagram-card">
<p>Eval loop полезно мыслить как постоянный контур, а не как разовую проверку</p>

``` mermaid
flowchart LR
    A["Code / prompt / policy change"] --> B["Offline evals"]
    B --> C["Regression gates"]
    C --> D["Production rollout"]
    D --> E["Online evals + traces"]
    E --> F["Failure analysis and grading"]
    F --> A
```

</div>

Для того же support-кейса этот контур означает: incident не должен оставаться только в postmortem. Он должен превращаться в eval case и в rollout rule.

## 4.1. User simulator полезен там, где статичных кейсов уже мало

Свежие материалы Google хорошо подсвечивают еще один практический слой: evaluation loop полезно дополнять user simulator, а не полагаться только на фиксированный набор тестов.[^google-govern]

Это особенно полезно, когда ты хочешь проверить:

- как агент ведет себя в длинном диалоге;
- как меняется поведение после неидеальных ответов;
- умеет ли система корректно переспрашивать;
- не ломается ли policy path в многоходовом сценарии;
- не деградирует ли orchestration при вариативных пользовательских репликах.

Для support-агента user simulator особенно полезен в сценариях вроде:

- пользователь сначала просит проверить статус, потом резко меняет приоритет;
- агент получает неполный `request_id`;
- после неудачного tool call пользователь присылает новую деталь;
- система должна выбрать: эскалировать, переспросить или безопасно остановиться.

Static eval set хорош для сравнения known cases. User simulator полезен там, где тебе важна динамика поведения, а не только итоговый score на одном заранее подготовленном примере.

## 4.2. Continuous eval loop должен замыкаться в rollout decisions

Когда online evals, trace grading и simulated conversations уже есть, следующий важный шаг очень простой: результаты должны не просто собираться, а влиять на release process.

Хорошая operational схема обычно выглядит так:

- offline evals блокируют явные regressions до релиза;
- user simulator помогает проверить сценарии, которые трудно удержать в статичном dataset;
- online evals и trace grading ловят drift и новые failure modes;
- rollout gates решают, можно ли расширять выкладку дальше.

То есть eval loop полезно мыслить не как “отдельную аналитическую активность”, а как часть управляемого change management.

## 5. Trace grading особенно полезен для агентных систем

В обычных приложениях часто хватает business KPI и error rate. В агентных системах этого мало, потому что качество часто сидит внутри run, а не только в финальном ответе.

Trace grading полезен тем, что позволяет оценивать:

- был ли retrieval уместным;
- был ли tool call оправдан;
- не был ли prompt перегружен;
- не случился ли unnecessary escalation;
- соблюдались ли policy constraints;
- был ли workflow efficient.

Для нашего support-агента это особенно ценно, когда ответ пользователю вроде бы “нормальный”, но внутри уже видно, что система:

- слишком часто вызывает `create_support_ticket`;
- ходит в лишние tools;
- слишком рано уходит в escalation;
- возвращает статус без достаточного grounding.

## 5.1. Behavioral evals и control evals проверяют не только ответ, но и поведение системы

По мере того как agent systems получают больше autonomy, становится полезно оценивать не только “справился ли run с задачей”, но и “какое поведение система продемонстрировала по пути”.

Именно здесь появляются:

- behavioral evals;
- control evals;
- automated red teaming.

Они полезны для сценариев, где обычный regression set слишком плоский:

- agent избегает oversight;
- слишком настойчиво сохраняет state;
- пытается обойти approval path;
- делает лишние tool hops;
- координация между несколькими agents начинает разваливаться.

То есть eval layer должен проверять не только final answer quality, но и failure modes поведения.

## 5.2. Coordination failure тоже должна быть частью eval design

Если система использует handoffs, manager pattern или несколько cooperating agents, то обычной проверки “ответ был правильным” уже мало.

Нужно отдельно смотреть:

- теряется ли контекст при handoff;
- не появляются ли conflicting actions;
- не деградирует ли verification discipline;
- не растет ли число лишних delegation steps;
- можно ли локализовать coordination failure по traces.

Именно поэтому multi-agent reliability research полезен здесь не как призыв срочно усложнять runtime, а как напоминание: чем сложнее orchestration, тем богаче должен быть eval design.

## 5.3. Multi-turn consistency тоже стоит проверять отдельно

Еще один полезный сигнал свежих работ: agent может выглядеть разумно в коротком сценарии и при этом постепенно входить в противоречие с самим собой в длинной interaction loop.

Это особенно важно, когда система:

- ведет длинный диалог;
- работает с накопленным state;
- несколько раз пересматривает решение;
- публично объясняет свои rationale.

Поэтому полезно держать отдельные consistency checks:

- не противоречит ли run самому себе через несколько turns;
- не меняется ли rationale без новой информации;
- не начинает ли длинная deliberation плодить больше contradiction, а не меньше;
- можно ли локализовать temporal drift по traces.

## 5.4. LLM-as-a-judge полезен только при калибровке

По мере роста eval layer почти неизбежно появляется еще один соблазн: использовать judge-model и считать, что теперь grading можно масштабировать почти автоматически.

Это полезный инструмент, но только если не перепутать его с источником истины.

Для agent systems у judge почти всегда есть одно важное ограничение: ему редко достаточно видеть только финальный текст ответа. Если grading должен отражать реальный outcome, judge полезно давать доступ к тому, что действительно описывает поведение системы:

- trace fragments;
- tool outcomes;
- approval events;
- structured grading fields;
- внешние state checks там, где они доступны.

Иначе система легко начинает получать "хороший score" за красивый текст при плохом фактическом результате.

Еще одна practical rule здесь очень важна: если согласованность judge с человеком низкая, первым шагом обычно должно быть не расширение dataset, а разбор disagreement cases и правка rubric или judge prompt.

Один из полезных сигналов здесь - `Cohen's kappa`, но важнее самого числа обычно форма расхождения: где именно judge недопонимает policy violation, tool misuse или ambiguous outcome.

Еще один частый источник самообмана: judge prompt, откалиброванный под сильную модель, может заметно хуже переноситься на более слабую. Поэтому при смене judge-model calibration стоит проверять заново, а не считать старый prompt автоматически переносимым.

И последнее правило совсем простое: если ты оцениваешь изменение prompt, не меняй одновременно и prompt, и model. Иначе потом нельзя будет сделать честный причинный вывод о том, что именно улучшило или ухудшило систему.

## 6. Что стоит включать в eval dataset

Очень частая ошибка: eval dataset состоит из приятных demo-сценариев. Такие наборы почти не помогают.

Хороший dataset обычно включает:

- happy path задачи;
- ambiguous user requests;
- prompt injection attempts;
- retrieval edge cases;
- missing-data scenarios;
- tool timeout и partial failure cases;
- approval-required flows;
- cross-tenant and privacy-sensitive cases.

Для support-агента это означает, что в dataset должны лежать не только “проверить статус и ответить”, но и:

- “создать тикет, но tool вернул ambiguous result”;
- “пользователь прислал срочную фразу, которую нельзя слепо сохранять как preference”;
- “retrieval вернул конфликтующие статусы”;
- “approval path должен остановить write action”.

Именно сложные и неприятные сценарии чаще всего дают реальную инженерную пользу.

## 6.1. Memory layer тоже должен входить в eval dataset явно

Отдельно полезно проверять не только ответ, но и качество state across runs.

Это означает cases на:

- write / no-write decisions;
- stale profile retrieval;
- contradiction между profile records;
- unsafe persistence;
- deletion и revision behavior;
- long-horizon memory drift.

Иначе memory incidents будут попадать в postmortems, но не будут возвращаться в regression discipline.

## 7. Regression gate должен быть формальным, а не “посмотрели глазами”

Команды часто говорят: “Мы протестировали, вроде стало не хуже”. Для production-grade агентной системы этого слишком мало.

Regression gate полезно строить как явный набор правил, например:

- не ухудшать success rate на critical eval set;
- не ухудшать safety metrics;
- не увеличивать cost per task beyond threshold;
- не увеличивать escalation rate;
- не ухудшать prompt budget или tool count per run сверх лимита.

Для support-агента это означает, что регрессом считается не только “агент стал чаще ошибаться”, но и:

- он стал чаще дублировать попытки write tool;
- чаще уходит в unnecessary escalation;
- чаще пишет лишнее в memory;
- стал дороже решать тот же класс задач.

Тогда решение о rollout перестает зависеть только от интуиции автора изменения.

## 8. Практические правила для eval loop

Если нужен короткий engineering-каркас, обычно достаточно таких правил:

1. Каждый заметный incident должен превращаться в eval case и rollout rule.
2. Offline и online evals должны жить вместе: один контур ловит regressions до релиза, другой после релиза.
3. Trace grading стоит держать на критичных write paths и policy-sensitive flows, а не только на happy path.
4. Dataset нужно обновлять по реальным failures, а не только по старым demo cases.
5. Regression gate должен быть машиночитаемым и блокировать не только quality regressions, но и safety, cost и escalation regressions.

## 9. Пример policy для eval gates

Ниже очень практичный шаблон:

```yaml
gates:
  offline:
    min_task_success_rate: 0.97
    max_policy_violation_rate: 0.002
    max_avg_cost_delta_pct: 8
  online:
    max_slo_burn_rate: 1.0
    max_manual_intervention_rate: 0.08
    max_unknown_side_effect_rate: 0.0005
  rollout:
    require_offline_pass: true
    require_online_shadow_period: true
```

Эти числа не универсальны. Но сама идея важна: quality gate должен быть машиночитаемым и спорить с ним нужно на уровне критериев, а не ощущений.

## 10. Простой кодовый пример regression decision

Ниже каркас, который показывает идею: решение о rollout привязывается к измеримым порогам, а не к общему впечатлению.

```python
from dataclasses import dataclass


@dataclass
class EvalSummary:
    task_success_rate: float
    policy_violation_rate: float
    avg_cost_delta_pct: float


def passes_regression_gate(summary: EvalSummary) -> bool:
    if summary.task_success_rate < 0.97:
        return False
    if summary.policy_violation_rate > 0.002:
        return False
    if summary.avg_cost_delta_pct > 8:
        return False
    return True
```

Код очень простой, но именно такая простота делает gate понятным для команды.

## 11. Онлайн-оценки должны быть связаны со стратегией выкладки

Очень полезно не выкатывать большие изменения сразу на всех, а использовать:

- shadow mode;
- canary rollout;
- limited tenant exposure;
- model routing experiments;
- staged policy rollout.

Тогда online evals становятся не просто наблюдением “что-то пошло не так”, а контролируемым этапом выпуска.

Для того же support-агента это означает: если новый adapter или новый prompt изменяет поведение на сложных status cases, команда должна увидеть это в canary или shadow, а не после broad rollout.

### 11.1. Хороший simulator не заменяет реальные данные, а дополняет их

Важно не переоценивать user simulator.

Он не заменяет:

- реальные production traces;
- реальные complaint patterns;
- реальные cost and latency distributions;
- реальные incident postmortems.

Но он очень полезен как промежуточный слой между offline dataset и живым rollout, потому что позволяет быстрее проверить:

- conversational robustness;
- handoff behavior;
- escalation discipline;
- fallback quality;
- policy-sensitive turns.

## 12. Что чаще всего ломается в eval culture

Проблемы тут довольно типовые:

- offline evals слишком игрушечные;
- онлайн-оценки не связаны с трассировкой;
- regression gates смотрят только на success rate;
- safety regressions не блокируют rollout;
- cost regressions не считаются реальными regressions;
- dataset не обновляется, и система оптимизируется под старые случаи.

Если это происходит, eval loop превращается в ritual, а не в механизм улучшения.

## 13. Что делать сразу после этой главы

Если хочешь быстро проверить свой eval loop, пройди по короткому списку:

1. Есть ли curated offline eval set для критичных сценариев?
2. Есть ли сигнал онлайн-оценки, связанный с трассировкой и SLO?
3. Умеешь ли ты grade не только final answer, но и ход run?
4. Есть ли formal regression gate перед rollout?
5. Учитываются ли safety и cost, а не только task success?
6. Обновляется ли eval dataset по следам реальных инцидентов?

Если на несколько вопросов подряд ответ “нет”, значит observability у тебя уже есть, а вот learning loop еще не собран.

## 14. Что читать дальше

Часть V к этому моменту уже собирает эксплуатационный контур целиком: трассировку, SLO и цикл оценки. Следующий логичный слой здесь уже организационный, потому что такие платформы упираются не только в код, но и в устройство команды.

## 15. Полезные справочные страницы

- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема наборов для оценки и правил проверки](../../appendix/eval-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)
- [Research frontier: память, наблюдаемость и надежность multi-agent систем](../../appendix/research-frontier.md)

- [Глава 12. SLO для агентных систем](chapter-12.md)
- [Глава 25. Behavioral evals, control evals и automated red teaming](../part-viii/chapter-25.md)
- [Глава 14. Платформенная команда и продуктовые команды](../part-vi/chapter-14.md)
- [Часть V. Надежность и observability](index.md)
- [Источники](../../appendix/sources.md)

[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
