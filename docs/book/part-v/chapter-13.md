# Глава 13. Offline evals, online evals и regression gates

## 1. Почему traces и SLO сами по себе еще не улучшают систему

Когда у тебя уже появились traces и SLO, возникает естественное ощущение, что observability теперь “почти закрыта”. Но это только половина пути.

Traces помогают понять, что произошло.
SLO помогают определить, что считается здоровьем системы.

Но остается главный engineering-вопрос: как не выпускать ухудшения и как системно улучшать качество?

Вот здесь и начинается eval loop.

## 2. Offline evals нужны, чтобы менять систему до выката

Offline evals отвечают на очень практичный вопрос: “Если мы меняем prompt, policy, retrieval, model routing или tool behavior, станет ли система лучше или хуже на известных сценариях?”

Хорошие offline evals обычно строятся вокруг:

- curated task sets;
- golden answers или expected outcomes;
- policy-sensitive edge cases;
- tricky retrieval scenarios;
- high-risk tool workflows.

Их сила в том, что они позволяют сравнивать версии системы до production traffic.

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

## 5. Trace grading особенно полезен для агентных систем

В обычных приложениях часто хватает business KPI и error rate. В агентных системах этого мало, потому что качество часто сидит внутри run, а не только в финальном ответе.

Trace grading полезен тем, что позволяет оценивать:

- был ли retrieval уместным;
- был ли tool call оправдан;
- не был ли prompt перегружен;
- не случился ли unnecessary escalation;
- соблюдались ли policy constraints;
- был ли workflow efficient.

Это особенно ценно, когда финальный результат вроде бы “нормальный”, но система уже начала тихо дорожать, тормозить или рисковать безопасностью.

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

Именно сложные и неприятные сценарии чаще всего дают реальную инженерную пользу.

## 7. Regression gate должен быть формальным, а не “посмотрели глазами”

Команды часто говорят: “Мы протестировали, вроде стало не хуже”. Для production-grade агентной системы этого слишком мало.

Regression gate полезно строить как явный набор правил, например:

- не ухудшать success rate на critical eval set;
- не ухудшать safety metrics;
- не увеличивать cost per task beyond threshold;
- не увеличивать escalation rate;
- не ухудшать prompt budget или tool count per run сверх лимита.

Тогда решение о rollout перестает зависеть только от интуиции автора изменения.

## 8. Пример policy для eval gates

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

## 9. Простой кодовый пример regression decision

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

## 10. Online evals должны быть связаны с rollout strategy

Очень полезно не выкатывать большие изменения сразу на всех, а использовать:

- shadow mode;
- canary rollout;
- limited tenant exposure;
- model routing experiments;
- staged policy rollout.

Тогда online evals становятся не просто наблюдением “что-то пошло не так”, а контролируемым этапом выпуска.

## 11. Что чаще всего ломается в eval culture

Проблемы тут довольно типовые:

- offline evals слишком игрушечные;
- online evals не связаны с traces;
- regression gates смотрят только на success rate;
- safety regressions не блокируют rollout;
- cost regressions не считаются реальными regressions;
- dataset не обновляется, и система оптимизируется под старые случаи.

Если это происходит, eval loop превращается в ritual, а не в механизм улучшения.

## 12. Practical checklist

Если хочешь быстро проверить свой eval loop, пройди по вопросам:

- Есть ли curated offline eval set для критичных сценариев?
- Есть ли online eval signal, связанный с traces и SLO?
- Умеешь ли ты grade не только final answer, но и ход run?
- Есть ли formal regression gate перед rollout?
- Учитываются ли safety и cost, а не только task success?
- Обновляется ли eval dataset по следам реальных инцидентов?

Если на несколько вопросов подряд ответ “нет”, значит observability у тебя уже есть, а вот learning loop еще не собран.

## 13. Что читать дальше

Part V теперь уже выглядит как цельный operational блок: traces, SLO и eval loop. Дальше логично переходить к организационной модели, потому что такие платформы упираются не только в код, но и в устройство команды.

- [Глава 12. SLO для агентных систем](chapter-12.md)
- [Глава 14. Platform team vs product teams](../part-vi/chapter-14.md)
- [Часть V. Надежность и observability](index.md)
- [Источники](../../appendix/sources.md)
