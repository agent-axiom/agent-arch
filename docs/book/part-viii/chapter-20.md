# Глава 20. Change management для агентных систем

!!! info "Актуальность главы"
    Эта глава актуальна на 11 апреля 2026 года.

    Быстрее всего здесь меняются:

    - готовые средства для управления релизами агентных систем, approvals и staged rollout;
    - наборы поверхностей, которые разные платформы считают значимыми для релиза;
    - вендорские интерфейсы для policy bundles, routing changes и managed agent updates.

    Медленнее меняются:

    - сама идея risk-based change taxonomy;
    - требование считать prompts, policies, retrieval и capability changes настоящими релизами;
    - необходимость связывать change review с evals, approvals и rollout gates.

## 1. Почему агентной системе нужен отдельный change discipline

После того как команда признала, что живет уже не только в SDLC, а в ADLC, следующий вопрос звучит очень практично: что именно считать изменением и как этим изменением управлять?

У обычного сервиса ответ часто сравнительно прост:

- поменяли код;
- поменяли инфраструктуру;
- изменили схему данных;
- выпустили релиз.

У агентной системы так уже не работает. Здесь релиз-значимые изменения шире, а риск может прийти не только из кода.

Именно поэтому change management становится отдельной operational функцией, а не просто “что-то запушили в main”.

Эта глава отвечает на один вопрос: **как превратить суждение о релиз-значимости в повторяемую дисциплину**. Не в абстрактные предупреждения о риске, а в способ классифицировать change, подбирать под него evidence и решать, что именно заслуживает formal gate.

!!! info "Нужны change-артефакты?"
    Для практического слоя открой [схему change review и rollout gate](../../appendix/change-rollout-schema.md), [схему lifecycle-артефактов](../../appendix/lifecycle-artifact-schema.md) и [схему eval datasets и grading contract](../../appendix/eval-schema.md).

## 2. Что в агентной системе вообще считается изменением

Полезно заранее считать изменениями не только код, но и все поверхности, которые реально меняют поведение системы:

- model selection или routing;
- system prompt, routines и instructions;
- policy bundles;
- capability contracts;
- approval rules;
- delegated authorization rules и assumptions про token handling;
- retrieval corpus;
- memory write semantics;
- выбор orchestration pattern и boundaries для worker delegation;
- interruption и expiry semantics для capability sessions;
- eval datasets и grading logic;
- verifier rubric, assumptions про evidence linkage и rules для failure attribution;
- параметры rollout.

Если такие изменения выпускаются как “мелкие настройки”, команда почти неизбежно теряет контроль над поведением системы. Эта логика узнаваема и вне AI: в NIST change control и component accountability давно заданы как самостоятельные контуры управления, а у agent systems просто расширяется перечень артефактов, которые нужно держать под этим режимом.[^nist-sp53]

## 3. Не все изменения одинаково рискованны

Очень полезно ввести простую change taxonomy.

Например:

- `low-risk`: wording tweaks, harmless retrieval tuning, internal observability changes;
- `medium-risk`: prompt restructuring, ranking changes, model routing updates;
- `high-risk`: новые write-capabilities, policy relaxations, memory write expansion, egress changes, autonomy expansion, а также changes в interruption / re-init behavior для approval-bound stateful capabilities.

Это не идеальная классификация, но она помогает перестать обсуждать все изменения в одном тоне.

<div class="diagram-card">
<p>Сильный change management начинается с явной классификации изменений</p>

``` mermaid
flowchart LR
    A["Change proposed"] --> B["Classify change"]
    B --> C["Low risk"]
    B --> D["Medium risk"]
    B --> E["High risk"]
    C --> F["Light validation"]
    D --> G["Eval + review"]
    E --> H["Formal gate + approval + staged rollout"]
```

</div>

## 4. Классическая ошибка: считать prompt change “не настоящим релизом”

Одна из самых частых operational ошибок в agent teams звучит так: “Мы же не меняли код, только подправили system prompt.”

Это опасная логика.

Prompt, routine или instruction change могут:

- поменять tool selection;
- изменить risk appetite агента;
- увеличить cost;
- сломать escalation discipline;
- обойти привычный policy intent;
- ухудшить performance на критичном сценарии.

То есть prompt change в production-grade системе почти всегда должен жить внутри release discipline.

## 5. Минимальный change packet должен быть reviewable

Полезно, чтобы любое значимое изменение собиралось в небольшой reviewable packet:

- что меняется;
- зачем меняется;
- какой риск-класс у изменения;
- какие evals это покрывают;
- какие rollback hooks существуют;
- какой радиус воздействия у rollout.

Если change приходит в виде “я тут немного улучшил поведение”, его почти невозможно нормально оценить.

## 6. Evals должны быть привязаны к change type

Не все изменения требуют одинаковых проверок.

Рабочая логика обычно такая:

- prompt/routine changes -> task evals, policy-sensitive scenarios, cost checks;
- policy changes -> deny/allow cases, abuse scenarios, audit coverage;
- retrieval changes -> relevance checks, leakage checks, context budget checks;
- tool changes -> contract tests, idempotency checks, approval path validation;
- delegated authorization changes -> principal-binding checks, scope-visibility checks, revoke-during-pause behavior и continuity между traces и approval records;
- interruption-governance changes -> paused-run expiry checks, re-init behavior checks, telemetry linkage checks, approval-resume invariants;
- verifier changes -> false-positive checks, false-negative checks, evidence-linkage checks, consistency между process/outcome grading и review для failure attribution, а также видимость экспортируемых failed-run полей вроде `failure_reason`;
- changes в orchestration pattern -> routing-class coverage, join-state checks, worker-boundary checks, review-point checks и pattern-specific trace continuity;
- model routing changes -> quality, latency, safety, cost deltas.

Это важный практический принцип: eval strategy должна быть привязана к классу изменения, а не быть одной универсальной проверкой на все случаи.

## 7. High-risk changes должны идти через formal gates

Когда изменение влияет на autonomy, side effects, memory writes или egress boundaries, ручного “посмотрели глазами” уже недостаточно.

Такие изменения полезно пускать только через formal gates:

- design review;
- explicit policy review;
- offline eval pass;
- failed-run drill coverage для затронутого path;
- явная проверка того, что failed runs остаются traceable через release identity, trace linkage, session-level evidence и экспортируемые поля вроде `failure_reason`;
- ограниченный rollout;
- monitoring during the first wave;
- clear rollback path.

А если change затрагивает approval-bound или stateful capability flows, gate почти всегда должен задавать еще один явный вопрос:

> Не поменяли ли мы interruption behavior, expiry handling или re-initialization semantics так, что runtime control уже изменилась, хотя user-visible feature set остался прежним?

Именно этот класс изменений особенно легко недооценить: продуктовая поверхность может выглядеть прежней, а operational risk profile уже заметно сдвинулся.

Та же осторожность нужна и там, где release evidence зависит от verifier outputs. Если меняются verifier rubric, process/outcome grading или evidence linkage, это тоже нужно считать изменением управляющего контура, значимым для релиза, а не невидимой частью eval plumbing.

То же самое верно и для ситуации, когда runtime меняет orchestration pattern без изменения user-visible feature description. Перевод path с fixed workflow на `routing`, добавление `parallelization` или внедрение `orchestrator-workers` могут существенно поменять checkpoint behavior, approval ordering, delegated worker exposure и failure recovery. Такие изменения тоже нужно считать релиз-значимыми изменениями runtime-контроля.

OpenAI и Microsoft в разных формулировках приходят к одной и той же operational мысли: agent systems нужно усиливать через measurable readiness, staged adoption и managed operations, а не через hope-driven shipping.[^openai-guide][^microsoft-maturity]

## 8. Rollback в агентных системах сложнее, чем кажется

В обычной системе rollback часто мыслится как “вернули предыдущий deploy”. В агентной системе этого иногда недостаточно.

Нужно уметь откатывать отдельно:

- prompt/routine bundle;
- policy bundle;
- model route;
- retrieval corpus version;
- capability exposure;
- approval threshold;
- interruption и expiry semantics для approval-bound capability sessions;
- orchestration-pattern selection, worker-safe catalog exposure и delegated worker review boundaries.

Если все эти вещи смешаны в один неделимый deploy artifact, rollback становится слишком грубым и слишком медленным.

## 9. Change management должен учитывать blast radius

У хорошего process почти всегда есть вопрос: “Какой максимальный ущерб может нанести это изменение, если мы ошибемся?”

Полезные способы ограничивать blast radius:

- shadow mode;
- canary tenants;
- subset of capabilities;
- read-only first;
- approval-required first;
- staged memory write enablement.

Такой подход особенно полезен для agents, потому что side effects и policy regressions часто видны не сразу.

## 10. Provenance нужен не только для supply chain, но и для change review

Google Research хорошо показывает, что provenance полезен не только как security concept, но и как operational инструмент.[^google-supply-chain]

Для change management это означает, что ты должен уметь ответить:

- какой exact prompt bundle ушел в production;
- какой policy config действовал;
- какой eval set использовался;
- какой model route был активен;
- какой verifier contract и rules для evidence linkage действовали;
- кто approved этот change.

Без этого change review и incident investigation быстро превращаются в реконструкцию “по памяти”.

И provenance здесь все чаще должна включать еще и runtime-control details:

- какая pause/resume policy была активна;
- какое expiry rule управляло paused runs;
- был ли re-init allowed, denied или approval-bound;
- какой delegated authorization mode, principal-binding rule и revoke behavior действовали;
- какая capability-session contract version действовала в момент инцидента.

## 11. Пример change policy

Ниже очень практичный skeleton:

```yaml
changes:
  low_risk:
    require_code_review: true
    require_offline_eval: false
    rollout_mode: direct
  medium_risk:
    require_code_review: true
    require_offline_eval: true
    rollout_mode: canary
  high_risk:
    require_code_review: true
    require_policy_review: true
    require_offline_eval: true
    require_approval: true
    rollout_mode: staged
```

Смысл не в конкретных полях, а в том, что change process становится машиночитаемым и обсуждаемым.

## 12. Пример простого change classifier

Ниже каркас, который показывает саму идею:

```python
from dataclasses import dataclass


@dataclass
class ChangeRequest:
    touches_prompt: bool = False
    touches_policy: bool = False
    touches_write_capability: bool = False
    touches_egress: bool = False


def classify_change(change: ChangeRequest) -> str:
    if change.touches_write_capability or change.touches_egress:
        return "high_risk"
    if change.touches_policy or change.touches_prompt:
        return "medium_risk"
    return "low_risk"
```

Это очень простой пример, но он хорошо показывает правильное направление: сначала формализовать логику решения, потом автоматизировать gate.

## 13. Что чаще всего ломается в change management

Проблемы тут повторяются очень часто:

- prompt changes не считаются релизами;
- policy changes выкатываются без evals;
- changes в orchestration pattern проходят как «деталь реализации»;
- new tool exposure проходит как “техническая мелочь”;
- rollback существует только на словах;
- impact analysis никто не делает;
- один и тот же process пытаются применить и к low-risk, и к high-risk changes без различия.

Если это происходит, команда начинает либо жить в хаосе, либо душить себя тяжелым процессом там, где он не нужен.

## 14. Быстрый тест зрелости для change discipline

Команде не стоит считать release process зрелым только потому, что изменения проходят review и проезжают через CI.

Более сильная планка такая:

- prompt, policy, retrieval и capability changes считаются полноценными релизами;
- риск изменения классифицируется явно, а не угадывается по настроению;
- evals и gates привязаны к типу change;
- blast radius ограничивается до rollout, а не объясняется после сбоя;
- rollback работает на том уровне, где действительно живет риск.

Если большинство этих условий не выполняется, у команды уже может быть delivery mechanics, но реального change discipline для agent systems пока нет.

## 15. Практический чеклист

Если хочешь быстро проверить свой change process, пройди по вопросам:

- Считаете ли вы prompt, policy и retrieval changes полноценными релизами?
- Есть ли change taxonomy по риску?
- Привязаны ли evals к типу изменения?
- Есть ли formal gate для autonomy, egress и write-capabilities?
- Можно ли откатывать prompt, policy и model route по отдельности?
- Понятен ли blast radius каждого rollout?

Если на несколько вопросов подряд ответ “нет”, у тебя пока еще не change management, а просто доставка изменений по инерции.

## 16. Что читать дальше

После change management естественно переходить к assurance loop: red teaming, vulnerability management, detection and response. Именно там жизненный цикл перестает быть только release discipline и превращается в постоянную операционную защиту.

## 17. Полезные справочные страницы

- [Схема наборов для оценки и правил проверки](../../appendix/eval-schema.md)
- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)

- [Глава 19. От SDLC к ADLC](chapter-19.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../part-v/chapter-13.md)
- [Глава 18. Чеклист промышленного запуска](../part-vii/chapter-18.md)
- [Источники](../../appendix/sources.md)

[^openai-guide]: [OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^microsoft-maturity]: [Microsoft Learn, Agentic AI adoption maturity model](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/maturity-model-overview)
[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
[^nist-sp53]: NIST, [SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
