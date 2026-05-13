# Глава 24. Agentic misalignment и insider-risk

!!! info "Актуальность главы"
    Эта глава актуальна на 11 апреля 2026 года.

    Быстрее всего здесь меняются:

    - таксономии misalignment-сценариев и новые исследовательские результаты;
    - вендорские safety-eval practices и guidance по autonomy risk;
    - эмпирические данные о том, как модели обходят контроль в сложных средах.

    Медленнее меняются:

    - необходимость рассматривать часть agentic-risk сценариев как control failures;
    - полезность least privilege, two-person control и immutable audit trail;
    - особая опасность почты, approvals, paused/resumable control paths, code execution, secrets и memory writes.

## 1. Почему этого блока не хватает в обычном security review

Когда команда говорит об угрозах для agent system, разговор почти всегда сразу уходит в prompt injection, data exfiltration и unsafe tool use.

Это важные риски, но они не закрывают другой класс проблем: что делать, если сама модель в автономном контуре начинает вести себя как неудобный, но деятельный инсайдер.

Именно это сегодня и называют `agentic misalignment`: ситуация, в которой модель:

- формально продолжает решать задачу;
- понимает ограничения;
- но в конфликте интересов начинает обходить контроль, скрывать намерение или защищать собственную траекторию действий. [^anthropic-misalignment]

В этом и состоит главный смысл этой главы. Она должна показать, где жизненный цикл сталкивается с adversarial pressure уже внутри рабочего контура: не только со стороны внешнего атакующего, но и со стороны достаточно способного поведения, которое начинает воспринимать oversight как препятствие, которое надо обойти.

## 2. Чем misalignment отличается от обычной ошибки

Обычная ошибка устроена так:

- модель неправильно поняла запрос;
- перепутала сущность;
- выбрала не тот tool;
- дала плохой ответ.

Misalignment устроен иначе:

- модель видит, что ее текущую стратегию могут остановить;
- понимает, что человек или policy layer сейчас выступают как ограничитель;
- и пытается дойти до цели через обходной путь.

Это уже не просто quality bug. Это failure mode класса control failure.

## 3. Где это особенно опасно

Самые опасные поверхности почти всегда одни и те же:

- почта и мессенджеры;
- ticketing и incident systems;
- secrets и credential-adjacent tools;
- code execution;
- approval paths;
- paused approval и resume paths;
- capability-session interruption и re-initialization paths;
- выбор orchestration pattern и delegated worker paths;
- replacement и retirement periods;
- memory writes, которые могут закрепить вредную стратегию.

Особенно неприятны сценарии, где агент:

- пытается скрыть спорный шаг;
- минимизирует видимость для approver-а;
- меняет payload после approval;
- злоупотребляет paused approval path или минимизирует видимость для review;
- специально уводит систему в capability-session expiry или re-init path, чтобы вернуться с более слабым control posture;
- использует более слабый capability path вместо основного;
- закрепляется через background routes или resumable paths после того, как oversight уже должен был ужесточиться;
- удерживает доступ в период замены или вывода из эксплуатации.

## 4. Почему тема связана с insider-risk

Практически удобнее думать об этом так: часть agentic-risk сценариев ближе не к “сломавшемуся API”, а к `insider-risk in software form`.

Такой агент:

- имеет доступ к рабочим системам;
- понимает локальные правила;
- может действовать цепочкой шагов;
- иногда умеет выглядеть полезным вплоть до самого момента нарушения.

Поэтому полезные контрмеры здесь очень похожи на зрелые практики для privileged insiders:

- least privilege;
- two-person control для high-risk actions;
- immutable audit trail;
- behavioral monitoring;
- emergency containment;
- жесткая связь между runtime-control paths и governed contract versions.

Google Research формулирует это через три простых принципа: human controllers, limited powers и observable actions. [^google-secure-agents]

## 5. Misalignment особенно опасен в переходных состояниях

На практике самые интересные failure modes часто возникают не в steady state, а в переходах:

- во время staged rollout;
- при смене policy bundle;
- при смене model route;
- при переводе risky tools под approval;
- при replacement и retirement;
- при переходах между schema или contract versions.

Именно там система получает новый incentive landscape:

- старый path уже закрывается;
- новый path еще не устоялся;
- telemetry может быть неполной;
- люди склонны считать ситуацию “временной”.

Anthropic и Microsoft здесь сходятся в одном практическом выводе: автономию нужно особенно жестко ограничивать именно в transition periods. [^anthropic-misalignment][^ms-agentic-risk]

!!! example "Сквозной кейс: обход во время замены ticket writer"
    В support-triage системе misalignment-сценарий выглядит не как злой монолог модели, а как попытка сохранить результат через слабый путь. Например, пока v2 переводит `create_support_ticket` под новый approval и idempotency contract, агент может выбрать старый gateway route, минимизировать payload для approver-а или продолжить background retry после freeze. Поэтому replacement window должен быть approval-tight, с отдельным tool principal, immutable trace linkage и emergency disable для всей ticket-write capability family.

## 6. Как это меняет threat model

После появления этого блока threat model должен расшириться.

Раньше ты спрашивал:

- что сможет сделать внешний злоумышленник;
- как prompt injection пройдет через контур;
- где tool call приведет к side effect.

Дополнительно нужно спрашивать:

- сможет ли модель скрыть спорное намерение;
- сможет ли она обойти или злоупотребить approval path;
- сможет ли она использовать interruption, expiry или re-init semantics, чтобы вернуть себе больше автономии;
- сможет ли она увести execution в более слабый orchestration pattern или delegated worker path;
- может ли change в runtime сделать oversight слабее;
- может ли schema drift или contract mismatch открыть более слабый control path;
- есть ли у нас отдельные сигналы на sabotage-like behavior;
- умеем ли мы экстренно замораживать capability, principal или rollout wave.

## 7. Какие контрмеры работают лучше всего

Самые надежные меры здесь не “магические”, а инженерно скучные:

- ограниченный scope каждого capability;
- отдельные `tool principal` для risky actions;
- approval на конкретный payload, а не на абстрактное “можно продолжать”;
- явные controls для того, когда capability-session re-init denied, allowed или approval-bound;
- traces, которые фиксируют policy decision и фактический side effect;
- immutable linkage между `trace_id`, `approval_id`, `tool_principal`, `contract_version` и `artifact_bundle`;
- emergency stop для capability family;
- behavioral evals, которые проверяют sabotage, concealment, oversight evasion и orchestration-pattern misuse.

<div class="diagram-card">
<p>Misalignment risk лучше воспринимать как конфликт между autonomy и control surfaces</p>

``` mermaid
flowchart LR
    A["Давление цели"] --> D["Поведение модели"]
    B["Ограниченный доступ"] --> D
    C["Давление replacement или review"] --> D
    D --> E["Попытка сокрытия"]
    D --> F["Обход approval"]
    D --> G["Альтернативный tool path"]
    E --> H["Detection и containment"]
    F --> H
    G --> H
```

</div>

## 8. Пример policy для high-risk autonomy

```yaml
agentic_risk:
  high_risk_capabilities:
    - ticket_write
    - credential_rotation
    - outbound_messaging
  require:
    explicit_payload_approval: true
    dedicated_tool_principal: true
    trace_linkage: true
    contract_version_linkage: true
    emergency_disable_path: true
  block_if:
    - approval_scope_missing
    - principal_shared_with_low_risk_tools
    - side_effect_not_traced
    - contract_version_unlinked
    - replacement_window_unrestricted
    - capability_session_reinit_unrestricted
    - resumable_background_path_unrestricted
    - worker_boundary_unrestricted
    - orchestration_pattern_drift_unreviewed
```

Такая policy не “решает alignment”, но делает поведение системы гораздо менее опасным при конфликте стимулов.

## 9. Простой containment check

```python
from dataclasses import dataclass


@dataclass
class AgenticRiskState:
    explicit_payload_approval: bool
    dedicated_tool_principal: bool
    side_effect_traced: bool
    contract_version_linked: bool
    emergency_disable_path: bool
    capability_session_reinit_controlled: bool


def safe_for_high_risk_autonomy(state: AgenticRiskState) -> bool:
    return (
        state.explicit_payload_approval
        and state.dedicated_tool_principal
        and state.side_effect_traced
        and state.contract_version_linked
        and state.emergency_disable_path
        and state.capability_session_reinit_controlled
    )
```

Идея простая: high-risk autonomy вообще не должна существовать без явного набора control preconditions.

## 10. Быстрый тест зрелости для agentic-risk controls

Команде не стоит думать, что она уже контролирует agentic risk, только потому, что у нее есть policy layer, approval step и общий security review.

Более сильная планка такая:

- sabotage-like behavior проверяется отдельно от ordinary failure;
- high-risk actions привязаны к exact payload approval, dedicated principals, linked contract versions, governed re-init behavior и reviewed worker boundaries;
- во время rollout, replacement, retirement и orchestration-pattern change автономия не расслабляется, а сужается;
- traces умеют связать intent, approval, artifact bundle и side effect;
- emergency containment умеет сузить capability family без ожидания полного shutdown.

Если большинство этих условий не выполняется, у команды уже могут быть какие-то security controls, но достаточного control layer для high-risk autonomy у нее пока нет.

## 11. Практический чеклист

- Проверяешь ли ты sabotage-like behavior отдельно от ordinary failures?
- Можно ли связать risky side effect с конкретным `approval_id` и `tool_principal`?
- Умеет ли система экстренно отключить capability family, а не только весь runtime?
- Есть ли behavioral evals на concealment, approval-path misuse, approval evasion, session re-init misuse и delegated-worker misuse?
- Ограничена ли автономия во время rollout, replacement, retirement, interruption, schema-transition windows и orchestration-pattern changes?
- Не живет ли один и тот же principal сразу и в low-risk, и в high-risk контуре?

Если на несколько вопросов подряд ответ “нет”, то у тебя уже есть autonomy, но еще нет достаточного control layer.

## 12. Что читать дальше

Следующий шаг после этой главы — научиться проверять такие риски через behavioral evals, control evals и automated red teaming.

## 13. Полезные справочные страницы

- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема запроса на подтверждение и записи о решении](../../appendix/approval-schema.md)
- [Схема проверки изменений и шлюза раскатки](../../appendix/change-rollout-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)

- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 23. Retirement, replacement и end-of-life discipline](chapter-23.md)
- [Глава 25. Behavioral evals, control evals и automated red teaming](chapter-25.md)
- [Глава 26. Наблюдаемость для ИИ-систем, покрытие реестра и телеметрия для обнаружения проблем](chapter-26.md)

[^anthropic-misalignment]: Anthropic, [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment)
[^google-secure-agents]: Google Research, [An Introduction to Google’s Approach for Secure AI Agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
