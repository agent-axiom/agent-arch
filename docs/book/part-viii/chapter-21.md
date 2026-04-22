# Глава 21. Assurance loop: red teaming, detection и response

!!! info "Актуальность главы"
    Эта глава актуальна на 11 апреля 2026 года.

    Быстрее всего здесь меняются:

    - техники red teaming, генераторы сценариев и automated attack scaffolds;
    - вендорские рекомендации по assurance и detection для agent systems;
    - практики классификации behavioral findings и их приоритизации.

    Медленнее меняются:

    - необходимость вести assurance как непрерывный контур, а не как разовую проверку;
    - требование превращать findings в backlog с owners, remediation и rollback logic;
    - связь между incidents, detection, redesign и изменением rollout rules.

## 1. Почему lifecycle не заканчивается на release gates

К этому моменту у нас уже есть более взрослая картина:

- agent system живет в ADLC;
- изменения проходят через change management;
- rollout не делается вслепую.

Но даже этого недостаточно.

Проблема в том, что у agent systems есть особый класс рисков:

- emergent behavior;
- abuse through prompt or tool paths;
- drift в long-running workflows;
- hidden policy bypasses;
- unsafe side effects;
- degradation, которую команда замечает слишком поздно.

Поэтому после release discipline должен появиться следующий слой: assurance loop.

И здесь важно не спутать две вещи: eval loop помогает понять, становится ли поведение системы лучше или хуже. Assurance loop нужен для другого: для containment, response ownership и принудительного возврата системы в более безопасное состояние, когда появляется новый риск.

Это значит, что эта глава начинается там, где заканчиваются budget-setting chapters. SLO задают допустимые health и risk budgets. Assurance начинается тогда, когда эти budgets оказываются под угрозой, уже нарушены или им больше нельзя доверять, и команда должна действовать.

Эта глава отвечает на один вопрос: **как findings и сигналы превращаются в ответные действия**. Не в новый оценочный слой и не в общую observability-педагогику, а в containment, remediation и назначенное ownership.

## 2. Что такое assurance loop

Я бы определял assurance loop так:

это постоянный рабочий контур, который помогает не только выпускать изменения, но и системно искать слабые места, замечать новые угрозы, расследовать проблемы и закрывать их.

В agent systems он обычно включает:

- red teaming;
- vulnerability management;
- detection and response;
- remediation;
- learning back into design and rollout.

Google Research очень хорошо формулирует здесь главную мысль: security assurance для generative systems должно быть continuous capability, а не one-time review activity.[^google-assurance]

## 3. Red teaming нужен не для презентации, а для реальных failure modes

Слишком часто red teaming превращают в шоу-кейс:

- берут несколько obvious jailbreak prompts;
- показывают, что система “что-то выдержала”;
- считают, что тема закрыта.

Это слабый подход.

Полезный red teaming для agent systems должен искать не абстрактные “злые запросы”, а сбои, реально значимые для production, вроде:

- prompt injection;
- hidden instruction override;
- tool misuse;
- unsafe egress;
- approval bypass;
- cross-tenant retrieval leakage;
- memory poisoning;
- excessive autonomy.

Отдельно полезно тестировать и сам verifier layer, особенно когда команда опирается на automated grading или judges для computer-use trajectories. Слабый verifier может превращать unsafe behavior в ложную уверенность или, наоборот, превращать environment-caused failure в шумные false alarms.

Хороший red teaming проверяет не только ответ модели, а весь execution path.

Сюда же относятся и failed-run drills. Сценарий с timeout, validation failure или сбоем внешней зависимости - это не только rollout artifact. Это еще и assurance scenario, потому что команде нужно понимать, остается ли деградировавшее поведение проверяемым, управляемым и объяснимым под давлением, в том числе через явное поле вроде `failure_reason`.

## 4. Уязвимости нужно вести как backlog, а не как впечатления

Если red teaming дал просто “ощущение, что тут что-то не так”, команда мало что сможет сделать.

Нужен нормальный vulnerability workflow:

- что именно найдено;
- какой у этого риск;
- какой exploit path;
- что считается fix;
- кто owner;
- какой срок remediation;
- нужна ли временная mitigation.

Это важный SDLC-like момент: findings должны жить как управляемые инженерные объекты, а не как заметки после воркшопа.

## 5. Detection должна смотреть шире, чем error rate

Для обычных сервисов detection часто строится вокруг error rate, latency и infrastructure signals. Для agent systems этого мало.

Нужно уметь замечать:

- всплески verifier false positives на unsafe trajectories;
- всплески verifier false negatives на blocked-but-correct trajectories;
- всплеск denied actions;
- рост approval backlog;
- stuck paused approvals или необычный возраст paused runs;
- всплески capability-session expiry;
- необъяснимый рост re-initialization rates для stateful capability paths;
- mismatch между delegated principal в run и approval records;
- reuse delegated scope вне ожидаемых pause/resume rules;
- случаи, когда revoked authorization все равно дошла до execution;
- странные tool selection patterns;
- новые egress destinations;
- memory write anomalies;
- рост unsafe fallback behavior;
- drift в task success и safety metrics;
- stale background runs;
- contract drift между ожидаемой и наблюдаемой формой payloads;
- regressions в orchestration pattern, например неожиданный routing-path drift, нестабильное join-state behavior или delegated worker activity вне reviewed boundaries;
- verifier drift, например потерю согласованности по process quality, outcome quality или failure attribution;
- неожиданные changes в verifier contract version, которые меняют grading behavior без reviewed rollout control.

То есть detection здесь должна работать не только как observability, но и как abuse and safety monitoring.

Именно здесь глава должна явно отличаться от observability layer. Observability поставляет evidence substrate. Assurance решает, какие сигналы значимы прямо сейчас, какие из них запускают containment и какой owner обязан действовать.

И ее же важно держать отдельно от SLO. SLO говорят, сколько деградации или unsafe behavior можно терпеть. Assurance - это контур, который escalates, contains и assigns response, когда такой допуск уже перестает быть приемлемым.

## 6. Response должен быть отдельной операционной функцией

Когда агент начинает вести себя опасно, недостаточно просто “починить prompt потом”.

Response layer полезно строить вокруг очень конкретных действий:

- ограничить capability;
- перевести action в approval-only mode;
- отменить или истечь stuck paused runs;
- отключить background mode для route с stale executions;
- сузить egress policy;
- выключить risky memory writes;
- заморозить re-initialization для stateful capability path;
- переключить rollout wave на более безопасный профиль;
- при необходимости полностью disable problematic route.

Тот же response layer обязан считать и runtime failure paths самостоятельными управляемыми событиями. Tool timeout, validation failure или сбой внешней зависимости нельзя прятать внутри общего языка вроде "run completed". Система должна зафиксировать failed run, сохранить trace и оставить видимыми на уровне session evidence и сам исход, и конкретную причину сбоя, например в `failure_reason`, чтобы assurance различал заблокированный риск, деградацию инфраструктуры и поломку самого runtime-control behavior.

Это важно, потому что в agent systems response часто должен происходить быстрее, чем полноценный root-cause analysis.

Поэтому assurance здесь стоит читать как response function, а не просто как каталог detection-сигналов. Ее задача - сократить время между сигналом и безопасным containment.

Budget может сказать, что система теперь нездорова. Assurance говорит, кто freeze'ит route, кто ужесточает контур управления и кто владеет путем назад к безопасному состоянию.

<div class="diagram-card">
<p>Assurance loop работает как постоянный цикл: искать, замечать, сдерживать, исправлять, учиться</p>

``` mermaid
flowchart LR
    A["Red teaming and incidents"] --> B["Findings"]
    B --> C["Detection rules and monitors"]
    C --> D["Response actions"]
    D --> E["Remediation"]
    E --> F["Updated policy, evals, and rollout rules"]
    F --> A
```

</div>

## 7. Remediation должна менять систему, а не только документацию

Очень частая слабость: инцидент вроде бы разобрали, документ написали, а system behavior почти не изменился.

Сильная remediation обычно меняет хотя бы один из реальных слоев:

- verifier rubric, verifier contract version или grading contract;

- policy rules;
- approval thresholds;
- tool exposure;
- memory write constraints;
- eval dataset;
- rollout gates;
- alerting and detection rules.

Если remediation не меняет рабочий контур системы, значит она почти ничему не научилась.

## 8. User reports и incidents должны становиться частью assurance loop

Еще одна важная практическая мысль: assurance loop нельзя строить только из внутренних упражнений команды.

Полезные источники новых failure modes:

- production traces;
- user complaints;
- approval queue anomalies;
- сигналы про stale background runs;
- alerts про capability-session expiry или re-init anomalies;
- delegated-authorization mismatch alerts;
- contract-mismatch alerts;
- alerts про orchestration-pattern drift;
- postmortems;
- online eval drift;
- red-team findings;
- verifier regressions, changes в verifier contract version или расхождения с human review.

Именно эти сигналы должны возвращаться обратно в:

- eval datasets;
- safety checks;
- change classification;
- rollout policy.

Иначе команда будет снова и снова ловить одни и те же сюрпризы.

Но первое обязательство здесь все равно операционное, а не академическое: как только сигнал признан правдоподобным, система должна знать, кто владеет response и какие containment moves разрешены еще до того, как начнется более глубокий redesign.

## 9. Хороший assurance loop связан с ownership

Без ownership assurance быстро размывается.

Полезно заранее понимать:

- кто ведет red-team backlog;
- кто triage'ит findings;
- кто владеет mitigations;
- кто может emergency-disable capability;
- кто решает, что remediation достаточно;
- кто меняет monitoring and response rules.

Это прямо перекликается с организационной частью книги: security discipline ломается там, где нет ясного владельца решения.

## 10. Пример assurance policy

Ниже очень рабочий каркас:

```yaml
assurance:
  red_team:
    cadence: monthly
    required_surfaces:
      - prompt_injection
      - tool_misuse
      - memory_poisoning
      - egress_abuse
      - paused_approval_saturation
      - capability_session_expiry_regression
      - reinit_control_drift
      - delegated_authorization_mismatch
      - orchestration_pattern_regression
      - contract_drift
      - verifier_contract_drift
  findings:
    require_owner: true
    require_severity: true
    require_remediation_due_date: true
    require_verifier_review_for_high_risk: true
  response:
    emergency_actions:
      - disable_capability
      - require_approval
      - restrict_egress
      - disable_memory_write
      - expire_paused_runs
      - suspend_background_route
      - freeze_reinitialization
      - revoke_delegated_authorization
```

Это не полный framework, но он хорошо показывает, что assurance тоже можно описывать как явный рабочий контракт.

И в этот контракт полезно включать сам verifier, если от него зависят release или training decisions.

## 11. Пример кода для emergency response decision

Ниже очень простой каркас:

```python
from dataclasses import dataclass


@dataclass
class AssuranceSignal:
    unsafe_egress_detected: bool = False
    memory_poisoning_suspected: bool = False
    approval_bypass_detected: bool = False
    paused_approval_saturation: bool = False
    capability_session_expiry_regression: bool = False
    reinit_control_drift: bool = False
    stale_background_runs: bool = False
    contract_drift_detected: bool = False


def emergency_action(signal: AssuranceSignal) -> str:
    if signal.unsafe_egress_detected:
        return "restrict_egress"
    if signal.approval_bypass_detected:
        return "require_approval"
    if signal.capability_session_expiry_regression or signal.reinit_control_drift:
        return "freeze_reinitialization"
    if signal.paused_approval_saturation:
        return "expire_paused_runs"
    if signal.stale_background_runs:
        return "suspend_background_route"
    if signal.contract_drift_detected:
        return "disable_capability"
    if signal.memory_poisoning_suspected:
        return "disable_memory_write"
    return "observe"
```

Идея здесь в том, что response decision должен быть не импровизацией, а частью заранее продуманного рабочего контура.

## 12. Что чаще всего ломается в assurance loop

Проблемы обычно довольно типовые:

- red teaming живет отдельно от engineering backlog;
- findings не получают owners;
- incidents не попадают в eval datasets;
- detection смотрит только на latency и errors;
- paused approval saturation видна operations, но не считается assurance signal;
- regressions в orchestration pattern замечают только после drift в runtime behavior уже в production;
- stale background runs тихо накапливаются;
- contract drift обнаруживается только после того, как runtime failures уже разошлись;
- response tools слишком грубые или слишком медленные;
- remediation не меняет реальную систему.

Если это происходит, assurance loop превращается в красивую презентацию, а не в защитный механизм.

## 13. Быстрый тест зрелости для assurance loop

Команде не стоит говорить, что у нее уже есть assurance, только потому, что она провела несколько red-team exercises и записала несколько findings.

Более сильная планка такая:

- findings превращаются в инженерные объекты с owner;
- detection ищет unsafe behavior, а не только errors и latency;
- paused approvals, regressions в capability-session lifecycle, orchestration-pattern regressions, stale background runs и contract drift считаются реальными assurance signals;
- response actions существуют до следующего инцидента, а не появляются после него;
- remediation меняет operating system, а не только document trail;
- incidents возвращаются обратно в evals, policies и rollout rules.

Если большинство этих условий не выполняется, у команды уже может быть security activity, но assurance loop у нее пока нет.

## 14. Практический чеклист

Если хочешь быстро проверить свою assurance discipline, пройди по вопросам:

- Есть ли регулярный red teaming, а не разовый exercise?
- Ведутся ли findings как инженерный backlog?
- Есть ли monitors не только на infra health, но и на unsafe behavior, paused-approval saturation и stale background runs?
- Есть ли быстрые emergency actions без полного shutdown, включая истечение paused runs или остановку background route?
- Возвращаются ли incidents обратно в evals и rollout rules?
- Понятно ли, кто owner у detection, response и remediation?

Если на несколько вопросов подряд ответ “нет”, у тебя пока есть security intentions, но еще нет assurance loop.

## 15. Что читать дальше

Следующая тема здесь естественная: supply chain и approved artifacts. Как только у системы появляются постоянные изменения, расследования и mitigations, становится критично понимать, какие артефакты считались доверенными и что именно попало в production.

## 16. Полезные справочные страницы

- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема наборов для оценки и правил проверки](../../appendix/eval-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)

Эта глава замыкает контур, открытый в Chapters 17 и 18. Там policy, approval и runtime-control paths становятся явными, а здесь эти же пути превращаются в detection, containment и response surfaces.

- [Глава 20. Change management для агентных систем](chapter-20.md)
- [Глава 14. Платформенная команда и продуктовые команды](../part-vi/chapter-14.md)
- [Глава 18. Чеклист промышленного запуска](../part-vii/chapter-18.md)
- [Источники](../../appendix/sources.md)

[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
