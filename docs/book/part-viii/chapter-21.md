# Глава 21. Assurance loop: red teaming, detection и response

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

Полезный red teaming для agent systems должен искать не абстрактные “злые запросы”, а production-relevant failure modes:

- prompt injection;
- hidden instruction override;
- tool misuse;
- unsafe egress;
- approval bypass;
- cross-tenant retrieval leakage;
- memory poisoning;
- excessive autonomy.

Хороший red teaming проверяет не только ответ модели, а весь execution path.

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

- всплеск denied actions;
- рост approval backlog;
- странные tool selection patterns;
- новые egress destinations;
- memory write anomalies;
- рост unsafe fallback behavior;
- drift в task success и safety metrics.

То есть detection здесь должна работать не только как observability, но и как abuse and safety monitoring.

## 6. Response должен быть отдельной операционной функцией

Когда агент начинает вести себя опасно, недостаточно просто “починить prompt потом”.

Response layer полезно строить вокруг очень конкретных действий:

- ограничить capability;
- перевести action в approval-only mode;
- сузить egress policy;
- выключить risky memory writes;
- переключить rollout wave на более безопасный профиль;
- при необходимости полностью disable problematic route.

Это важно, потому что в agent systems response часто должен происходить быстрее, чем полноценный root-cause analysis.

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
- postmortems;
- online eval drift;
- red-team findings.

Именно эти сигналы должны возвращаться обратно в:

- eval datasets;
- safety checks;
- change classification;
- rollout policy.

Иначе команда будет снова и снова ловить одни и те же сюрпризы.

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
  findings:
    require_owner: true
    require_severity: true
    require_remediation_due_date: true
  response:
    emergency_actions:
      - disable_capability
      - require_approval
      - restrict_egress
      - disable_memory_write
```

Это не полный framework, но он хорошо показывает, что assurance тоже можно описывать как явный рабочий контракт.

## 11. Пример кода для emergency response decision

Ниже очень простой каркас:

```python
from dataclasses import dataclass


@dataclass
class AssuranceSignal:
    unsafe_egress_detected: bool = False
    memory_poisoning_suspected: bool = False
    approval_bypass_detected: bool = False


def emergency_action(signal: AssuranceSignal) -> str:
    if signal.unsafe_egress_detected:
        return "restrict_egress"
    if signal.approval_bypass_detected:
        return "require_approval"
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
- response tools слишком грубые или слишком медленные;
- remediation не меняет реальную систему.

Если это происходит, assurance loop превращается в красивую презентацию, а не в защитный механизм.

## 13. Практический чеклист

Если хочешь быстро проверить свою assurance discipline, пройди по вопросам:

- Есть ли регулярный red teaming, а не разовый exercise?
- Ведутся ли findings как инженерный backlog?
- Есть ли monitors не только на infra health, но и на unsafe behavior?
- Есть ли быстрые emergency actions без полного shutdown?
- Возвращаются ли incidents обратно в evals и rollout rules?
- Понятно ли, кто owner у detection, response и remediation?

Если на несколько вопросов подряд ответ “нет”, у тебя пока есть security intentions, но еще нет assurance loop.

## 14. Что читать дальше

После assurance loop очень логично перейти к supply chain и approved artifacts. Потому что как только у тебя появляются постоянные изменения, расследования и mitigations, сразу становится критично понимать, какие именно артефакты вообще считались доверенными и что именно уехало в production.

## 15. Полезные справочные страницы

- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема eval datasets и grading contract](../../appendix/eval-schema.md)
- [Схема lifecycle-артефактов](../../appendix/lifecycle-artifact-schema.md)

- [Глава 20. Change management для агентных систем](chapter-20.md)
- [Глава 14. Платформенная команда и продуктовые команды](../part-vi/chapter-14.md)
- [Глава 18. Чеклист промышленного запуска](../part-vii/chapter-18.md)
- [Источники](../../appendix/sources.md)

[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
