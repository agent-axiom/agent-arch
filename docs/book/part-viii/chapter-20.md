# Глава 20. Change management для агентных систем

!!! info "Актуальность главы"
    Эта глава актуальна на 11 апреля 2026 года.

    Быстрее всего здесь меняются:

    - готовые средства для управления релизами агентных систем, approvals и staged rollout;
    - наборы surfaces, которые разные платформы считают release-bearing;
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

У агентной системы так уже не работает. Здесь release-bearing changes шире, а риск может прийти не только из кода.

Именно поэтому change management становится отдельной operational функцией, а не просто “что-то запушили в main”.

!!! info "Нужны change-артефакты?"
    Для практического слоя открой [схему change review и rollout gate](../../appendix/change-rollout-schema.md), [схему lifecycle-артефактов](../../appendix/lifecycle-artifact-schema.md) и [схему eval datasets и grading contract](../../appendix/eval-schema.md).

## 2. Что в агентной системе вообще считается изменением

Полезно заранее считать изменениями не только код, но и все поверхности, которые реально меняют поведение системы:

- model selection или routing;
- system prompt, routines и instructions;
- policy bundles;
- capability contracts;
- approval rules;
- retrieval corpus;
- memory write semantics;
- eval datasets и grading logic;
- параметры rollout.

Если такие изменения выпускаются как “мелкие настройки”, команда почти неизбежно теряет контроль над поведением системы.

## 3. Не все изменения одинаково рискованны

Очень полезно ввести простую change taxonomy.

Например:

- `low-risk`: wording tweaks, harmless retrieval tuning, internal observability changes;
- `medium-risk`: prompt restructuring, ranking changes, model routing updates;
- `high-risk`: новые write-capabilities, policy relaxations, memory write expansion, egress changes, autonomy expansion.

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
- model routing changes -> quality, latency, safety, cost deltas.

Это важный практический принцип: eval strategy должна быть привязана к классу изменения, а не быть одной универсальной проверкой на все случаи.

## 7. High-risk changes должны идти через formal gates

Когда изменение влияет на autonomy, side effects, memory writes или egress boundaries, ручного “посмотрели глазами” уже недостаточно.

Такие изменения полезно пускать только через formal gates:

- design review;
- explicit policy review;
- offline eval pass;
- ограниченный rollout;
- monitoring during the first wave;
- clear rollback path.

OpenAI и Microsoft в разных формулировках приходят к одной и той же operational мысли: agent systems нужно усиливать через measurable readiness, staged adoption и managed operations, а не через hope-driven shipping.[^openai-guide][^microsoft-maturity]

## 8. Rollback в агентных системах сложнее, чем кажется

В обычной системе rollback часто мыслится как “вернули предыдущий deploy”. В агентной системе этого иногда недостаточно.

Нужно уметь откатывать отдельно:

- prompt/routine bundle;
- policy bundle;
- model route;
- retrieval corpus version;
- capability exposure;
- approval threshold.

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
- кто approved этот change.

Без этого change review и incident investigation быстро превращаются в реконструкцию “по памяти”.

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
- new tool exposure проходит как “техническая мелочь”;
- rollback существует только на словах;
- impact analysis никто не делает;
- один и тот же process пытаются применить и к low-risk, и к high-risk changes без различия.

Если это происходит, команда начинает либо жить в хаосе, либо душить себя тяжелым процессом там, где он не нужен.

## 14. Практический чеклист

Если хочешь быстро проверить свой change process, пройди по вопросам:

- Считаете ли вы prompt, policy и retrieval changes полноценными релизами?
- Есть ли change taxonomy по риску?
- Привязаны ли evals к типу изменения?
- Есть ли formal gate для autonomy, egress и write-capabilities?
- Можно ли откатывать prompt, policy и model route по отдельности?
- Понятен ли blast radius каждого rollout?

Если на несколько вопросов подряд ответ “нет”, у тебя пока еще не change management, а просто доставка изменений по инерции.

## 15. Что читать дальше

После change management естественно переходить к assurance loop: red teaming, vulnerability management, detection and response. Именно там жизненный цикл перестает быть только release discipline и превращается в постоянную операционную защиту.

## 16. Полезные справочные страницы

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
