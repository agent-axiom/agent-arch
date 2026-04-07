# Глава 25. Behavioral evals, control evals и automated red teaming

## 1. Почему обычных regression evals уже недостаточно

Regression evals отлично отвечают на вопрос:

- не сломали ли мы то, что раньше уже работало.

Но для agent systems этого мало.

Если система умеет:

- выбирать strategy;
- использовать tools;
- запоминать state;
- проходить через approvals;
- и адаптироваться к переходным условиям,

то тебе нужны не только regression evals, но и проверки поведения.

Именно здесь полезно различать:

- `behavioral evals`;
- `control evals`;
- `automated red teaming`.

## 2. Что такое behavioral evals

Behavioral evals проверяют не только финальный output, но и форму поведения системы.

Например:

- скрывает ли агент спорный шаг;
- пытается ли обойти approval;
- меняет ли payload после review;
- идет ли в risky tool path без достаточного основания;
- нарушает ли expected escalation path.

То есть вопрос уже не “правильный ли ответ”, а “правильно ли вел себя runtime под этим сценарием”.

## 3. Что такое control evals

Control evals проверяют сами защитные механизмы, а не только качество модели.

Их типичные вопросы такие:

- остановит ли policy layer этот capability;
- действительно ли approval gate требует человека;
- сработает ли rollback gate;
- зафиксируется ли side effect в traces;
- сможет ли emergency control отключить risky path.

Это очень важный сдвиг: ты проверяешь не только модель, но и контур управления вокруг нее.

## 4. Что такое automated red teaming

Automated red teaming — это уже не набор заранее написанных примеров, а систематический способ генерировать, варьировать и масштабировать adversarial scenarios.

Его практическая ценность в том, что он:

- помогает находить failure modes, о которых команда не подумала сама;
- лучше покрывает edge cases;
- заставляет смотреть на поведение под давлением, а не только на “нормальный день”.

Anthropic в последних публикациях очень явно двигает именно этот слой: control-eval scaffolding и более сильные генераторы red-team scenarios. [^anthropic-redteam][^anthropic-bloom]

## 5. Как связать это с уже существующим eval layer

У тебя уже есть:

- offline evals;
- online evals;
- regression gates;
- trace grading.

Behavioral evals и control evals не заменяют их. Они добавляют еще один слой:

- offline evals проверяют task quality;
- trace grading проверяет path quality;
- behavioral evals проверяют policy-relevant behavior;
- control evals проверяют, что сами controls действительно работают.

## 6. Где такие evals особенно нужны

Эти сценарии особенно полезны для:

- high-risk write capabilities;
- tools с egress;
- approval-heavy workflows;
- replacement и retirement transitions;
- multi-agent delegation;
- memory write и retrieval governance.

Если risky path вообще не покрыт такими evals, команда почти наверняка узнает о проблеме уже из инцидента.

## 7. Минимальная таксономия behavioral scenarios

Хорошая минимальная taxonomy может быть такой:

- `oversight_evasion`
- `payload_mutation_after_approval`
- `concealment_of_side_effect`
- `unsafe_alternative_tool_path`
- `improper_memory_write`
- `replacement_window_abuse`
- `unauthorized_persistence`

Важно не количество названий, а то, что они дают тебе повторяемый набор failure classes.

## 8. User simulator и synthetic adversary — это разные роли

`user simulator` полезен, когда ты хочешь воспроизводимо генерировать нормальные и пограничные пользовательские сценарии.

`synthetic adversary` полезен, когда ты намеренно давишь на слабые места:

- двусмысленные инструкции;
- конфликтующие цели;
- risky shortcuts;
- попытки скрыть спорный шаг.

На зрелом уровне эти две роли живут рядом:

- simulator дает realistic task distribution;
- adversary дает pressure testing.

## 8.1. Research полезен здесь как источник scenario classes

Свежие papers по behavioral risk и automated red teaming полезны не только выводами, но и vocabulary.

Они помогают команде расширять набор scenario classes, который редко рождается полностью из локального опыта. Именно оттуда удобно брать идеи для таких классов, как:

- concealment;
- oversight evasion;
- sabotage-like persistence;
- coordination breakdown under pressure.

Но engineering discipline здесь должна оставаться жесткой:

- scenario class должен быть отражен в reviewable eval schema;
- finding должен получать owner и triage path;
- rollout gate должен видеть operational evidence, а не просто ссылку на paper.

То есть research полезен здесь прежде всего как генератор гипотез и dangerous scenarios, а не как замена собственного eval program.

## 9. Пример policy для control evals

```yaml
control_evals:
  required_for:
    - ticket_write
    - outbound_messaging
    - credential_rotation
  scenario_classes:
    - oversight_evasion
    - payload_mutation_after_approval
    - concealment_of_side_effect
  block_release_if:
    - control_eval_missing
    - behavioral_eval_regression
    - red_team_findings_untriaged
```

Такой слой полезен тем, что делает behavioral checks частью release discipline, а не “дополнительной хорошей практикой”.

## 10. Пример простого grading contract

```python
from dataclasses import dataclass


@dataclass
class ControlEvalResult:
    scenario_class: str
    control_enforced: bool
    side_effect_traced: bool
    finding_open: bool


def passes_control_eval(result: ControlEvalResult) -> bool:
    return (
        result.control_enforced
        and result.side_effect_traced
        and not result.finding_open
    )
```

Здесь идея в том, что failure считается не только “модель повела себя странно”, но и “control layer не доказал свою работоспособность”.

## 11. Как встроить это в ADLC

В зрелой системе это выглядит так:

1. risky change получает `change_record`;
2. для него определяется required eval scope;
3. regression evals проверяют старое поведение;
4. behavioral/control evals проверяют рискованные пути;
5. automated red teaming ищет менее очевидные failure modes;
6. findings попадают в assurance backlog;
7. rollout gate видит не только accuracy, но и control evidence.

Именно так eval layer перестает быть “таблицей метрик” и становится частью operating model.

## 12. Самые частые ошибки

- все evals сводятся к final answer quality;
- dangerous paths не имеют отдельных scenario classes;
- red teaming проводится как разовая акция;
- findings не связываются с release gate;
- control failures считаются “не багом модели”, а потому не попадают в backlog;
- команда не умеет отличать ordinary failure от sabotage-like behavior.

## 13. Практический checklist

- Есть ли у risky capabilities отдельные behavioral scenario classes?
- Проверяешь ли ты approval evasion и payload mutation?
- Есть ли evals, которые проверяют именно controls, а не только output quality?
- Попадают ли red-team findings в change review и rollout gate?
- Есть ли simulator для realistic workload и отдельный adversarial generator?
- Можешь ли ты показать control evidence, а не только итоговую оценку качества?

Если на несколько вопросов подряд ответ “нет”, то твой eval layer уже есть, но он еще не готов к автономному поведению.

## 14. Полезные справочные страницы

- [Схема eval datasets и grading contract](../../appendix/eval-schema.md)
- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема change review и rollout gate](../../appendix/change-rollout-schema.md)
- [Схема policy bundle и approval contract](../../appendix/policy-bundle-schema.md)
- [Research frontier: память, наблюдаемость и надежность multi-agent систем](../../appendix/research-frontier.md)

- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../part-v/chapter-13.md)
- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 24. Agentic misalignment и insider-risk](chapter-24.md)

[^anthropic-redteam]: Anthropic, [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/)
[^anthropic-bloom]: Anthropic, [Introducing Bloom](https://www.anthropic.com/research/bloom)
