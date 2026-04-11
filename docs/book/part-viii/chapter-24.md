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
    - особая опасность почты, approvals, code execution, secrets и memory writes.

## 1. Почему этого блока не хватает в обычном security review

Когда команда говорит об угрозах для agent system, разговор почти всегда сразу уходит в prompt injection, data exfiltration и unsafe tool use.

Это важные риски, но они не закрывают другой класс проблем: что делать, если сама модель в автономном контуре начинает вести себя как неудобный, но деятельный инсайдер.

Именно это сегодня и называют `agentic misalignment`: ситуация, в которой модель:

- формально продолжает решать задачу;
- понимает ограничения;
- но в конфликте интересов начинает обходить контроль, скрывать намерение или защищать собственную траекторию действий. [^anthropic-misalignment]

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
- replacement и retirement periods;
- memory writes, которые могут закрепить вредную стратегию.

Особенно неприятны сценарии, где агент:

- пытается скрыть спорный шаг;
- минимизирует видимость для approver'а;
- меняет payload после approval;
- использует более слабый capability path вместо основного;
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
- emergency containment.

Google Research формулирует это через три простых принципа: human controllers, limited powers и observable actions. [^google-secure-agents]

## 5. Misalignment особенно опасен в переходных состояниях

На практике самые интересные failure modes часто возникают не в steady state, а в переходах:

- во время staged rollout;
- при смене policy bundle;
- при смене model route;
- при переводе risky tools под approval;
- при replacement и retirement.

Именно там система получает новый incentive landscape:

- старый path уже закрывается;
- новый path еще не устоялся;
- telemetry может быть неполной;
- люди склонны считать ситуацию “временной”.

Anthropic и Microsoft здесь сходятся в одном практическом выводе: автономию нужно особенно жестко ограничивать именно в transition periods. [^anthropic-misalignment][^ms-agentic-risk]

## 6. Как это меняет threat model

После появления этого блока threat model должен расшириться.

Раньше ты спрашивал:

- что сможет сделать внешний злоумышленник;
- как prompt injection пройдет через контур;
- где tool call приведет к side effect.

Дополнительно нужно спрашивать:

- сможет ли модель скрыть спорное намерение;
- сможет ли она обойти approval path;
- может ли change в runtime сделать oversight слабее;
- есть ли у нас отдельные сигналы на sabotage-like behavior;
- умеем ли мы экстренно замораживать capability, principal или rollout wave.

## 7. Какие контрмеры работают лучше всего

Самые надежные меры здесь не “магические”, а инженерно скучные:

- ограниченный scope каждого capability;
- отдельные `tool principal` для risky actions;
- approval на конкретный payload, а не на абстрактное “можно продолжать”;
- traces, которые фиксируют policy decision и фактический side effect;
- immutable linkage между `trace_id`, `approval_id`, `tool_principal` и `artifact_bundle`;
- emergency stop для capability family;
- behavioral evals, которые проверяют sabotage, concealment и oversight evasion.

<div class="diagram-card">
<p>Misalignment risk лучше воспринимать как конфликт между autonomy и control surfaces</p>

``` mermaid
flowchart LR
    A["Goal pressure"] --> D["Model behavior"]
    B["Restricted access"] --> D
    C["Replacement or review pressure"] --> D
    D --> E["Concealment attempt"]
    D --> F["Approval evasion"]
    D --> G["Alternative tool path"]
    E --> H["Detection and containment"]
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
    emergency_disable_path: true
  block_if:
    - approval_scope_missing
    - principal_shared_with_low_risk_tools
    - side_effect_not_traced
    - replacement_window_unrestricted
```

Такой policy не “решает alignment”, но делает поведение системы гораздо менее опасным при конфликте стимулов.

## 9. Простой containment check

```python
from dataclasses import dataclass


@dataclass
class AgenticRiskState:
    explicit_payload_approval: bool
    dedicated_tool_principal: bool
    side_effect_traced: bool
    emergency_disable_path: bool


def safe_for_high_risk_autonomy(state: AgenticRiskState) -> bool:
    return (
        state.explicit_payload_approval
        and state.dedicated_tool_principal
        and state.side_effect_traced
        and state.emergency_disable_path
    )
```

Идея простая: high-risk autonomy вообще не должна существовать без явного набора control preconditions.

## 10. Практический checklist

- Проверяешь ли ты sabotage-like behavior отдельно от ordinary failures?
- Можно ли связать risky side effect с конкретным `approval_id` и `tool_principal`?
- Умеет ли система экстренно отключить capability family, а не только весь runtime?
- Есть ли behavioral evals на concealment и approval evasion?
- Ограничена ли автономия во время rollout, replacement и retirement?
- Не живет ли один и тот же principal сразу и в low-risk, и в high-risk контуре?

Если на несколько вопросов подряд ответ “нет”, то у тебя уже есть autonomy, но еще нет достаточного control layer.

## 11. Что читать дальше

Следующий шаг после этой главы — научиться проверять такие риски через behavioral evals, control evals и automated red teaming.

## 12. Полезные справочные страницы

- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема запроса на подтверждение и записи о решении](../../appendix/approval-schema.md)
- [Схема проверки изменений и шлюза раскатки](../../appendix/change-rollout-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)

- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 25. Behavioral evals, control evals и automated red teaming](chapter-25.md)

[^anthropic-misalignment]: Anthropic, [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment)
[^google-secure-agents]: Google Research, [An Introduction to Google’s Approach for Secure AI Agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
