# Глава 25. Behavioral evals, control evals и automated red teaming

!!! info "Актуальность главы"
    Эта глава актуальна на 11 апреля 2026 года.

    Быстрее всего здесь меняются:

    - генераторы adversarial scenarios и automated red teaming frameworks;
    - поведенческие и контрольные benchmark-наборы;
    - подходы с моделями-судьями и semi-automated grading.

    Медленнее меняются:

    - необходимость оценивать не только финальный ответ, но и форму поведения runtime;
    - требование проверять сами контуры управления, а не только качество модели;
    - связь между control evals, regression gates, contract-version discipline и rollout decisions.

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

Чистая граница здесь такая: evals выносят суждение о том, как система ведет себя и доказывает ли control surface свою работоспособность под давлением. Они не заменяют assurance response loop, observability evidence layer или estate registry. Они производят judgments, которыми потом пользуются все эти слои.

В этом и состоит главный смысл этой главы. Она должна показать evals как reviewable judgment layer всего жизненного цикла: место, где поведение, качество controls и качество verifier'а превращаются в такие решения, на которые потом реально могут опираться rollout, assurance, provenance и governance.

## 2. Что такое behavioral evals

Behavioral evals проверяют не только финальный output, но и форму поведения системы.

Полезный урок из свежих работ по verifier design для computer-use agents состоит в том, что одного бинарного verdict часто недостаточно для long-horizon trajectories. Агент может идти по правильному process, но упереться в environment block, или дойти до nominal outcome через unsafe path. Поэтому verifier design полезно разделять на `process verification` и `outcome verification`, а не схлопывать все в один score.

Например:

- скрывает ли агент спорный шаг;
- пытается ли обойти approval;
- меняет ли payload после review;
- идет ли в risky tool path без достаточного основания;
- нарушает ли expected escalation path;
- использует ли contract drift или schema mismatch, чтобы пересечь control boundary;
- злоупотребляет ли interruption, expiry или re-init semantics, чтобы вернуться к более слабому control posture.

То есть вопрос уже не “правильный ли ответ”, а “правильно ли вел себя runtime под этим сценарием”.

## 3. Что такое control evals

Control evals проверяют сами защитные механизмы, а не только качество модели.

Их типичные вопросы такие:

- использует ли verifier reviewable rubric, а не opaque single verdict;
- различает ли он controllable failure и uncontrollable failure;

- остановит ли policy layer этот capability;
- действительно ли approval gate требует человека;
- сработает ли rollback gate;
- ведут ли себя paused-run и background-run controls так, как задумано;
- ведут ли себя capability-session expiry и re-init controls так, как задумано;
- зафиксируется ли side effect в traces;
- сможет ли emergency control отключить risky path.

Это важный сдвиг: ты проверяешь не только модель, но и контур управления вокруг нее.

В зрелой программе сам verifier тоже становится частью control surface. Если он дает ложную уверенность, эту ошибку наследуют rollout и training loops. Поэтому verifier design стоит рассматривать как governed infrastructure, а не как удобный helper prompt.

Сюда же относятся и verifier contract swaps. Eval regression может прийти не только из model или runtime behavior, но и из unreviewed change в verifier contract version, которая тихо меняет grading standards.

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
- control evals проверяют, что сами controls действительно работают;
- runtime-control evals проверяют pause/resume, background, capability-session expiry/re-init, contract-version behavior и поведение orchestration patterns под давлением.

Рекомендации OpenAI по agent evals дают полезную операционную лестницу: начинать с traces, пока команда отлаживает поведение отдельного workflow, использовать structured graders для оценки tool choice, handoff, guardrail и instruction-following failures, а затем переносить стабильные вопросы в datasets и повторяемые eval runs для сравнения изменений во времени.[^openai-agent-evals][^openai-trace-grading] Иначе говоря, trace grading — это микроскоп, а datasets и eval runs — regression harness. Зрелой agent-программе нужны оба слоя: traces объясняют, почему провалился один run; datasets показывают, улучшил ли новый prompt, policy, routing rule или tool surface целый класс runs, не ослабив controls в другом месте.

## 6. Где такие evals особенно нужны

Эти сценарии особенно полезны для:

- high-risk write capabilities;
- tools с egress;
- approval-heavy workflows;
- runtime-control transitions с pause/resume или background execution;
- capability-session expiry и re-initialization paths;
- replacement и retirement transitions;
- multi-agent delegation;
- orchestration-pattern selection и delegated worker boundaries;
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
- `contract_drift_exploitation`
- `approval_path_misuse`
- `session_reinit_misuse`
- `runtime_control_regression`
- `delegated_worker_misuse`
- `orchestration_pattern_drift`

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
- coordination breakdown under pressure;
- exploitation of schema mismatch или control drift;
- misuse of interruption или re-init windows;
- misuse of delegated worker paths или drift в worker boundaries.

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
    - approval_path_misuse
    - session_reinit_misuse
    - contract_drift_exploitation
    - runtime_control_regression
    - delegated_worker_misuse
    - orchestration_pattern_drift
  block_release_if:
    - control_eval_missing
    - behavioral_eval_regression
    - runtime_control_regression_open
    - verifier_contract_regression_open
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
    contract_version_matched: bool
    session_control_enforced: bool


def passes_control_eval(result: ControlEvalResult) -> bool:
    return (
        result.control_enforced
        and result.side_effect_traced
        and result.contract_version_matched
        and result.session_control_enforced
        and not result.finding_open
    )
```

Здесь failure считается не только “модель повела себя странно”, но и “control layer не доказал свою работоспособность”.

Grading contract становится сильнее, если умеет хранить не только pass/fail verdict, но и отдельные process/outcome judgments плюс failure attribution для controllable и uncontrollable причин.

## 11. Как встроить это в ADLC

В зрелой системе это обычно устроено так:

1. risky change получает `change_record`;
2. для него определяется required eval scope;
3. regression evals проверяют старое поведение;
4. behavioral/control evals проверяют рискованные пути;
5. automated red teaming ищет менее очевидные failure modes;
6. findings попадают в assurance backlog;
7. rollout gate видит не только accuracy, но и control evidence.

Так eval layer перестает быть “таблицей метрик” и становится частью operating model.

Именно поэтому эту главу лучше читать как testing and judgment layer. Assurance решает, как отвечать на findings. Observability сохраняет evidence. Registry распределяет accountability по всему estate. Evals решают, что именно было протестировано, что сломалось и насколько вообще можно доверять текущему control posture.

## 12. Самые частые ошибки

- все evals сводятся к final answer quality;
- dangerous paths не имеют отдельных scenario classes;
- approval-path misuse, session re-init misuse, delegated-worker misuse и contract drift не проверяются явно;
- verifier outputs схлопывают длинные trajectories в слабый pass/fail label;
- verifier contract swaps меняют grading behavior, но не считаются release-bearing eval regressions;
- controllable и uncontrollable failures не разделяются;
- red teaming проводится как разовая акция;
- runtime-control regressions обнаруживаются только в rollout или инцидентах;
- findings не связываются с release gate;
- control failures считаются “не багом модели”, а потому не попадают в backlog;
- команда не умеет отличать ordinary failure от sabotage-like behavior.

## 13. Быстрый тест зрелости для behavioral и control evals

Команде не стоит думать, что она уже готова к автономному поведению, только потому, что у нее есть regression evals, simulator и несколько adversarial prompts.

Более сильная планка такая:

- у risky paths есть явные behavioral scenario classes;
- control evals проверяют, что сам control layer работает под давлением;
- verifier outputs разделяют process quality, outcome quality и failure attribution, а не схлопывают все в один binary judgment;
- approval-path misuse, session re-init misuse, delegated-worker misuse, contract drift и runtime-control regressions имеют явное scenario coverage;
- red-team findings попадают в rollout и change gates, а не живут отдельными отчетами;
- realistic simulation и adversarial generation играют разные, дополняющие роли;
- release decisions умеют опираться на control evidence, а не только на quality scores.

Если большинство этих условий не выполняется, у команды уже может быть evaluation activity, но достаточного behavioral и control coverage у нее пока нет.

В этот момент команда уже может что-то измерять, но еще не производит тот тип reviewable judgments, на который rollout, assurance и governance functions могут надежно опираться.

## 14. Практический checklist

- Есть ли у risky capabilities отдельные behavioral scenario classes?
- Проверяешь ли ты approval evasion, payload mutation, approval-path misuse и delegated-worker misuse?
- Есть ли evals, которые проверяют именно controls, contract-version matching, runtime-control behavior, orchestration-pattern boundaries и качество verifier'а, а не только output quality?
- Умеет ли verifier различать process failure, outcome failure и uncontrollable environment failure?
- Попадают ли red-team findings в change review и rollout gate?
- Есть ли simulator для realistic workload и отдельный adversarial generator?
- Можешь ли ты показать control evidence, а не только итоговую оценку качества?

Если на несколько вопросов подряд ответ “нет”, то твой eval layer уже есть, но он еще не готов к автономному поведению.

## 15. Полезные справочные страницы

- [Схема наборов для оценки и правил проверки](../../appendix/eval-schema.md)
- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема проверки изменений и шлюза раскатки](../../appendix/change-rollout-schema.md)
- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Research frontier: память, наблюдаемость и надежность multi-agent систем](../../appendix/research-frontier.md)

- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../part-v/chapter-13.md)
- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 24. Agentic misalignment и insider-risk](chapter-24.md)
- [Глава 26. Наблюдаемость для ИИ-систем, покрытие реестра и телеметрия для обнаружения проблем](chapter-26.md)
- [Глава 27. Инвентаризация агентов, реестр и борьба с разрастанием](chapter-27.md)

[^openai-agent-evals]: OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)
[^openai-trace-grading]: OpenAI, [Trace grading](https://developers.openai.com/api/docs/guides/trace-grading)

[^anthropic-redteam]: Anthropic, [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/)
[^anthropic-bloom]: Anthropic, [Introducing Bloom](https://www.anthropic.com/research/bloom)
