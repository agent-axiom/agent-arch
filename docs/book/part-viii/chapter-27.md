# Глава 27. Agent inventory, registry и борьба с sprawl

!!! info "Актуальность главы"
    Эта глава актуальна на 11 апреля 2026 года.

    Быстрее всего здесь меняются:

    - платформенные функции для inventory discovery, registry sync и governance automation;
    - вендорские подходы к классификации agents, assistants и agent-like entities;
    - рабочие практики для drift detection и policy enforcement across estates.

    Медленнее меняются:

    - необходимость различать inventory и registry;
    - требование иметь owner, lifecycle state, capability record и runtime-control ownership у production-grade agents;
    - важность регулярного review, чтобы sprawl не превращался в blind spot.

## 1. Почему почти у каждой успешной agent-программы появляется sprawl

Как только первые agent systems доказывают полезность, в организации обычно начинается одна и та же история:

- одна команда делает support agent;
- другая делает internal knowledge agent;
- третья добавляет workflow assistant;
- четвертая быстро собирает узкоспециализированного агента под локальную задачу.

Сами по себе эти решения могут быть разумными. Проблема начинается позже, когда никто уже не может быстро ответить:

- сколько агентов вообще существует;
- какие из них production, а какие “временные”;
- кто их owner;
- какие capabilities у них есть;
- какие identities, connectors и tool principals они используют;
- какие из них вообще еще живы;
- какие из них все еще владеют paused approvals, background routes, deprecated contract paths или stale verifier contracts.

Именно это состояние и стоит называть `agent sprawl`.

## 2. Почему sprawl опасен не только организационно

На первый взгляд это кажется чисто управленческой проблемой: много сущностей, сложно поддерживать порядок.

Но на практике sprawl быстро превращается в risk multiplier:

- orphaned agents продолжают жить без owner;
- deprecated agents сохраняют доступ к systems и data;
- разные команды по-разному трактуют approvals и policy boundaries;
- observability coverage становится фрагментарной;
- inventory drift делает release gates и incident review менее надежными.

Microsoft прямо связывает это с security posture: неполная inventory и непрозрачные agent estates приводят к blind spots, inconsistent enforcement и delayed detection. [^ms-inventory][^ms-agentic-risk]

## 3. Inventory и registry — не одно и то же

Полезно различать два слоя:

- `agent inventory`
- `agent registry`

Inventory отвечает на вопрос:

- какие agent-like сущности вообще существуют в нашей среде.

Registry отвечает на более строгий вопрос:

- какие из них признаны, классифицированы, управляются и допускаются в production contours.

То есть:

- inventory нужен для полноты видимости;
- registry нужен для governance.

Без inventory ты не знаешь полный estate.
Без registry ты не можешь уверенно сказать, какие агенты считаются approved и governed.

## 4. Что должно быть в минимальной записи агента

Минимальный registry record для production-grade agent systems обычно должен включать:

- `agent_id`;
- owner team;
- business purpose;
- lifecycle state;
- allowed capabilities;
- runtime identity;
- tool principals;
- approval requirements;
- ownership для paused runs, background runs и capability sessions;
- observability status;
- статус verifier или eval evidence;
- linkage на active и deprecated verifier contracts;
- artifact bundle linkage;
- retirement plan linkage.

Эта запись важна не ради “таблички”, а потому что она связывает agent как сущность с:

- security controls;
- operational ownership;
- lifecycle decisions.

## 5. Какие lifecycle states нужны почти всегда

Слишком простая модель “active / inactive” быстро перестает работать.

Минимально полезнее иметь хотя бы такие states:

- `proposed`
- `development`
- `pilot`
- `production`
- `restricted`
- `deprecated`
- `retired`

Тогда становится легче:

- ограничивать autonomy до production;
- отслеживать deprecated agents;
- видеть, какие agents еще не должны иметь full egress или full approvals path;
- управлять replacement и retirement без серой зоны.

## 6. Registry полезен не только security-команде

Хороший agent registry нужен не только security или governance.

Он полезен и:

- platform team;
- product teams;
- SRE / operations;
- audit / compliance;
- incident responders.

Для platform team он показывает, какие patterns реально масштабируются.
Для operations — кто должен реагировать ночью.
Для incident response — какие agents вообще могли участвовать в конкретном событии.

## 7. Sprawl часто начинается с “маленьких исключений”

На практике zoo rarely starts as an official strategy.

Он начинается с маленьких послаблений:

- “это всего лишь внутренний помощник”;
- “этот agent временный”;
- “пока без registry, потом добавим”;
- “approval path здесь избыточен”;
- “telemetry потом подключим”.

Через несколько месяцев оказывается, что именно эти исключения и образуют самую непрозрачную часть estate.

Поэтому strong default здесь простой:

- если сущность может действовать от имени организации, читать важный контекст или вызывать tools, она должна попадать хотя бы в inventory;
- если она идет в production contour, она должна попасть и в registry.

## 8. Как registry связан с observability

Observability chapter уже показала, что inventory coverage — часть evidence layer.

Registry делает эту связь еще жестче:

- traces можно enrich'ить registry metadata;
- detections можно строить по lifecycle state;
- incidents можно фильтровать по owner, risk tier и approval mode;
- release evidence можно проверять не только по traces, но и по статусу registry record и verifier-evidence linkage.

То есть registry превращает observability из “сырых событий” в управляемую operational map.

## 8.1. Registry без continuous verification быстро становится красивым, но неточным

Здесь важно не переоценить сам реестр. Наличие registry еще не доказывает, что control layer действительно работает.

Если registry:

- не сверяется с реальным telemetry coverage;
- не проверяется против живых principals;
- не сопоставляется с active capabilities;
- не сверяется с verifier evidence, на которое опираются rollout или assurance;
- не участвует в retirement hygiene,

то он довольно быстро превращается в аккуратную, но частично вымышленную картину estate.

Поэтому зрелый registry лучше мыслить не как статический каталог, а как continuously verified control surface.

## 9. Как registry связан с approvals и policies

Registry не должен дублировать policy bundle или approval contract.

Его задача другая:

- показать, какие policy bundle и approval mode относятся к данному agent;
- показать, имеет ли agent право на определенный capability set;
- показать, в каком lifecycle state агент сейчас живет.

Если у тебя нет этой связки, то легко возникает состояние, в котором:

- policy обновили;
- approval flow поменяли;
- traces стали богаче;
- но никто не знает, какие именно agents вообще должны этим пользоваться.

Это становится еще важнее, когда approval и long-running work превращаются в явные runtime paths.

Тогда registry должен помогать отвечать на вопросы:

- какие agents вообще имеют право ставить run на approval pause;
- какие agents могут продолжать работу в background mode;
- какие agents могут re-initialize stateful capability sessions и в каком approval mode;
- кто owner у stuck paused runs;
- кто owner у aging background runs;
- кто owner у capability-session expiry drift и emergency freeze actions;
- какой contract version должны соблюдать их approval и capability payloads;
- какой verifier или grading contract считается доверенным для их high-risk eval evidence;
- не ссылаются ли где-то в estate на deprecated verifier contracts.

Иначе estate может выглядеть governed, но при этом скрывать операционную неоднозначность.

## 10. Пример минимального agent registry record

```yaml
agent:
  agent_id: support-triage-ref
  owner_team: customer-platform
  business_purpose: support_ticket_triage
  lifecycle_state: production
  runtime_identity: agent://support-triage-ref
  tool_principals:
    - svc-ticket-writer
  allowed_capabilities:
    - ticket_read
    - ticket_write
  policy_bundle: policy-v4
  approval_mode: required_for_high_risk
  runtime_controls:
    approval_pause_allowed: true
    background_mode_allowed: true
    capability_session_mode: stateful
    reinit_policy: approval_bound
    paused_run_owner: support-ops
    capability_session_owner: support-ops
    contract_version: capability-contract-v3
  observability:
    trace_enabled: true
    inventory_covered: true
    verifier_evidence_linked: true
  verifier_contract: verifier-v2
  deprecated_verifier_contracts:
    - verifier-v1
  artifacts:
    bundle_id: bundle-2026-04-07-a
  retirement_plan: retire-support-v1
```

Такой record уже достаточно полезен, чтобы связывать agent с ownership, controls, lifecycle и verifier-aware evidence expectations.

На масштабе estate это еще и помогает отвечать на вопрос, который команды часто упускают: какие verifier contracts сейчас активны, какие уже deprecated и какие agents все еще зависят от старых версий.

## 11. Пример registry health check

```python
from dataclasses import dataclass


@dataclass
class AgentRegistryState:
    has_owner: bool
    has_lifecycle_state: bool
    has_policy_linkage: bool
    has_observability: bool
    has_runtime_control_linkage: bool
    has_capability_session_owner: bool


def registry_ready(state: AgentRegistryState) -> bool:
    return (
        state.has_owner
        and state.has_lifecycle_state
        and state.has_policy_linkage
        and state.has_observability
        and state.has_runtime_control_linkage
        and state.has_capability_session_owner
    )
```

Здесь логика простая: agent без owner, lifecycle state и observability linkage вообще не должен считаться production-ready entity.

## 12. Самые частые failure modes

- agents есть в проде, но отсутствуют в inventory;
- inventory существует, но lifecycle states не поддерживаются;
- registry не знает про principals и approvals;
- deprecated agents остаются с доступом к tool paths;
- registry record не показывает, кто отвечает за paused approvals или aging background runs;
- contract versions дрейфуют, пока registry все еще указывает на устаревшие control assumptions;
- разные реестры расходятся между собой;
- platform team знает одних агентов, а security team — других.

## 13. Быстрый тест зрелости для agent governance

Команде не стоит думать, что она контролирует свой agent estate, только потому, что у нее есть registry spreadsheet и примерное число развернутых agents.

Более сильная планка такая:

- inventory и registry живут как разные control surfaces;
- у каждого production agent есть owner, lifecycle state и policy linkage;
- telemetry coverage можно непрерывно сверять с registry;
- paused approvals, ownership фоновых запусков и contract versions входят в registry control surface;
- deprecated и orphaned agents можно найти до того, как они станут blind spots;
- governance умеет различать discovered entities и approved production agents.

Если большинство этих условий не выполняется, у команды уже могут быть visibility fragments, но реального agent governance у нее пока нет.

## 14. Практический checklist

- Можешь ли ты быстро назвать число active, deprecated и retired agents?
- У каждого production agent есть owner?
- Связан ли registry record с policy bundle, approval mode, runtime-control ownership и bundle_id?
- Видно ли из inventory, какие agents не шлют telemetry?
- Можно ли быстро найти orphaned или deprecated agents с живыми principals?
- Есть ли у тебя distinction между “обнаружен” и “одобрен для production”?

Если несколько ответов подряд “нет”, то agent estate у тебя уже есть, а agent governance еще нет.

## 15. Полезные справочные страницы

- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)
- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема запроса на подтверждение и записи о решении](../../appendix/approval-schema.md)
- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Research frontier: память, наблюдаемость и надежность multi-agent систем](../../appendix/research-frontier.md)

- [Глава 23. Retirement, replacement и end-of-life discipline](chapter-23.md)
- [Глава 24. Agentic misalignment и insider-risk](chapter-24.md)
- [Глава 26. AI-native observability, inventory coverage и detection-ready telemetry](chapter-26.md)

[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
