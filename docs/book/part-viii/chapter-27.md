# Глава 27. Инвентаризация агентов, реестр и борьба с разрастанием

!!! info "Актуальность главы"
    Последняя редакционная проверка: **17 мая 2026 года**. Предыдущая проверка: **14 мая 2026 года**. Следующая плановая проверка: **17 июня 2026 года**.

    Что изменилось после предыдущей проверки: MCP/A2A security surfaces, verifier contracts, governance-aware telemetry и publisher-readiness замечания теперь имеют конкретные contract coverage и docs-surface guards.

    Быстрее всего здесь меняются:

    - платформенные функции для обнаружения инвентаря агентов, синхронизации реестра и автоматизации управления;
    - вендорские подходы к классификации агентов, ассистентов и agent-like сущностей;
    - рабочие практики обнаружения drift и исполнения policy на уровне всего контура.

    Медленнее меняются:

    - необходимость различать инвентарь и реестр;
    - требование иметь owner, lifecycle state, capability record и runtime-control ownership у производственных агентов;
    - важность регулярной проверки, чтобы разрастание не превращалось в слепую зону.

## 1. Почему почти у каждой успешной агентской программы появляется разрастание

Как только первые агентские системы доказывают полезность, в организации обычно начинается одна и та же история:

- одна команда делает агента поддержки;
- другая делает внутреннего knowledge-агента;
- третья добавляет workflow-ассистента;
- четвертая быстро собирает узкоспециализированного агента под локальную задачу.

Сами по себе эти решения могут быть разумными. Проблема начинается позже, когда никто уже не может быстро ответить:

- сколько агентов вообще существует;
- какие из них работают в production, а какие “временные”;
- кто их owner;
- какие capabilities у них есть;
- какие identities, connectors и tool principals они используют;
- какие из них вообще еще живы;
- какие из них все еще держат paused approvals, background routes, deprecated contract paths или stale verifier contracts.

Именно это состояние и стоит называть разрастанием агентов (`agent sprawl`).

Слой реестра нужен здесь прежде всего для одной вещи: сделать весь контур подотчетным.

Для любого production-агента должно быть можно быстро ответить, кто его owner, какие controls им управляют и кто обязан действовать, если система начинает дрейфовать.

Эта глава отвечает на один вопрос: **как инвентарь и реестр превращают набор agent-like сущностей в подотчетный производственный контур**.

Здесь реестр важен не как еще один telemetry layer, а как слой ownership, lifecycle state и accountability. Главный артефакт этой главы — registry record: запись, которая связывает agent identity, owner, lifecycle state, capabilities, runtime-control ownership и evidence links.

## 2. Почему разрастание опасно не только организационно

На первый взгляд это кажется чисто управленческой проблемой: много сущностей, сложно поддерживать порядок.

Но на практике разрастание быстро превращается в усилитель риска:

- orphaned agents продолжают жить без owner;
- deprecated agents сохраняют доступ к systems и data;
- разные команды по-разному трактуют approvals и policy boundaries;
- observability coverage становится фрагментарной;
- drift инвентаря делает release gates и incident review менее надежными.

Microsoft прямо связывает это с security posture: неполный инвентарь и непрозрачные агентские контуры приводят к blind spots, inconsistent enforcement и delayed detection.[^ms-inventory][^ms-agentic-risk]

Та же базовая дисциплина хорошо совпадает с NIST SP 800-53: инвентарь должен быть полным, обновляемым и привязанным к accountability, иначе контроль быстро становится декоративным.[^nist-sp53]

## 3. Инвентарь и реестр — не одно и то же

Полезно различать два слоя:

- `agent inventory` — инвентарь агентов
- `agent registry` — реестр агентов

Инвентарь отвечает на вопрос:

- какие agent-like сущности вообще существуют в нашей среде.

Реестр отвечает на более строгий вопрос:

- какие из них признаны, классифицированы, управляются и допускаются в production contours.

То есть:

- инвентарь нужен для полноты видимости;
- реестр нужен для управления.

Без инвентаря ты не знаешь полный контур.
Без реестра ты не можешь уверенно сказать, какие агенты считаются approved, управляемыми и операционно подотчетными.

## 4. Что должно быть в минимальной записи агента

Минимальная запись в реестре для производственной агентской системы обычно должна включать:

- `agent_id`;
- команду-владельца;
- бизнес-назначение;
- состояние жизненного цикла;
- разрешенные capabilities;
- runtime identity;
- tool principals;
- требования к approvals;
- ownership для paused runs, background runs и capability sessions;
- статус наблюдаемости;
- статус verifier или eval evidence;
- ссылки на active и deprecated verifier contracts;
- связь с artifact bundle;
- связь с retirement plan.

Чтобы такая запись не превращалась в длинную форму ради формы, ее удобно читать как пять групп:

1. **Identity:** `agent_id`, runtime identity, owner team и business purpose.
2. **Lifecycle:** lifecycle state, retirement plan и deprecated paths.
3. **Capabilities:** allowed capabilities, tool principals и approval requirements.
4. **Runtime ownership:** кто отвечает за paused runs, background runs и capability sessions.
5. **Evidence links:** observability status, verifier/eval evidence, verifier contracts и artifact bundle linkage.

Эта запись важна не ради “таблички”, а потому что она связывает агента как сущность с:

- security controls;
- операционным ownership;
- решениями жизненного цикла.

## 5. Какие состояния жизненного цикла нужны почти всегда

Слишком простая модель “active / inactive” быстро перестает работать.

Минимально полезнее иметь хотя бы такие состояния:

- `proposed`
- `development`
- `pilot`
- `production`
- `restricted`
- `deprecated`
- `retired`

Тогда становится легче:

- ограничивать autonomy до production;
- отслеживать deprecated-агентов;
- видеть, какие агенты еще не должны иметь full egress или полный путь approvals;
- управлять replacement и retirement без серой зоны.

## 6. Реестр полезен не только команде безопасности

Хороший реестр агентов нужен не только безопасности или управлению.

Он полезен и:

- platform team;
- продуктовым командам;
- SRE / operations;
- audit / compliance;
- incident responders.

Для platform team он показывает, какие patterns реально масштабируются.
Для operations — кто должен реагировать ночью.
Для incident response — какие агенты вообще могли участвовать в конкретном событии.

## 7. Разрастание часто начинается с “маленьких исключений”

На практике разрастание почти никогда не начинается как официальная стратегия.

Оно начинается с маленьких послаблений:

- “это всего лишь внутренний помощник”;
- “этот агент временный”;
- “пока без реестра, потом добавим”;
- “approval path здесь избыточен”;
- “telemetry потом подключим”.

Через несколько месяцев оказывается, что именно эти исключения и образуют самую непрозрачную часть контура.

Поэтому надежный default здесь простой:

- если сущность может действовать от имени организации, читать важный контекст или вызывать tools, она должна попадать хотя бы в инвентарь;
- если она идет в production contour, она должна попасть и в реестр.

## 8. Как реестр связан с наблюдаемостью

Глава про наблюдаемость уже показала, что покрытие инвентаря — часть доказательного слоя.

Реестр делает эту связь еще жестче:

- traces можно обогащать metadata из реестра;
- detections можно строить по lifecycle state;
- incidents можно фильтровать по owner, risk tier и approval mode;
- release evidence можно проверять не только по traces, но и по статусу записи в реестре и verifier-evidence linkage.

То есть реестр превращает наблюдаемость из “сырых событий” в управляемую операционную карту.

Но его не нужно путать с provenance. Provenance хранит, какой approved artifact set и какая version обосновывали поведение.

Реестр хранит, какая named production entity, какой owner и какой lifecycle state принадлежали этому path.

Именно здесь и проходит чистая граница между двумя главами. Observability сохраняет evidence.

Реестр привязывает evidence к named entities, owners, lifecycle states и accountability paths по всему контуру.

И это же граница с главой про provenance. Provenance отвечает, под какой утвержденной version или approved bundle система работала.

Реестр отвечает, какая production entity владела этим path и кто отвечает за него сейчас.

!!! example "Сквозной кейс: support-triage в реестре"
    После всех исправлений support-triage должен быть не просто “агентом поддержки”, а registry record с owner, lifecycle state, allowed capabilities, `create_support_ticket` tool principal, approval mode, observability status, eval-evidence linkage и retirement plan для старого ticket writer. Тогда duplicate-ticket сигнал можно привязать не только к trace или artifact bundle, но и к named production entity: кто владеет path, кто расширяет canary, кто отключает write capability и кто отвечает за deprecated route.

**Registry case-spine note:** каждый canonical case должен становиться [named registry record](../../appendix/registry-operations-handbook.md), а не только примером в прозе. Support triage требует write-capability owners, [approval mode](../../appendix/approval-schema.md) и [retirement plan](../../appendix/lifecycle-artifact-schema.md) для deprecated ticket paths. Internal knowledge assistant требует [corpus owners](../../appendix/memory-retrieval-schema.md), freshness review, tenant scope и [retrieval-policy linkage](../../appendix/memory-retrieval-schema.md). Incident coordination требует incident-role owners, escalation authority, notification channels и [lifecycle state](../../appendix/lifecycle-artifact-schema.md) для emergency-only capabilities.

### 8.1. Реестр без непрерывной сверки быстро становится красивым, но неточным

Здесь важно не переоценить сам реестр. Наличие реестра еще не доказывает, что control layer действительно работает.

Если реестр:

- не сверяется с реальным telemetry coverage;
- не проверяется против живых principals;
- не сопоставляется с active capabilities;
- не сверяется с [verifier evidence](../../appendix/eval-schema.md), на которое опираются rollout или assurance;
- не участвует в retirement hygiene,

то он довольно быстро превращается в аккуратную, но частично вымышленную картину контура.

Поэтому зрелый реестр лучше мыслить не как статический каталог, а как контрольную поверхность, которую непрерывно сверяют с живым контуром.

## 9. Как реестр связан с подтверждениями и политиками

Реестр не должен дублировать policy bundle или approval contract.

Его задача другая:

- показать, какие policy bundle и approval mode относятся к данному агенту;
- показать, имеет ли агент право на определенный capability set;
- показать, какие approved MCP servers, discovery sources и auth modes входят в управляемую capability surface этого агента;
- показать, в каком lifecycle state агент сейчас живет.

Если у тебя нет этой связки, то легко возникает состояние, в котором:

- policy обновили;
- approval flow поменяли;
- traces стали богаче;
- но никто не знает, какие именно агенты вообще должны этим пользоваться.

Это становится еще важнее, когда approvals и long-running work превращаются в явные runtime paths.

Тогда реестр должен помогать отвечать на вопросы:

- какие агенты вообще имеют право ставить run на approval pause;
- какие агенты могут продолжать работу в background mode;
- какие агенты могут re-initialize stateful capability sessions и в каком approval mode;
- кто owner у stuck paused runs;
- кто owner у aging background runs;
- кто owner у capability-session expiry drift и emergency freeze actions;
- какой contract version должны соблюдать их approval и capability payloads;
- какой verifier или grading contract считается доверенным для их high-risk eval evidence;
- не ссылаются ли где-то в контуре на deprecated verifier contracts;
- не появились ли shadow MCP endpoints вне approved registry.

Иначе контур может выглядеть управляемым, но при этом скрывать операционную неоднозначность.

Поэтому реестр — это не столько слой про release lineage, сколько слой операционной подотчетности.

Это карта ownership на уровне всего контура, которая удерживает decisions, incidents и drift привязанными к правильной сущности.

Обычно именно эта неоднозначность первой и бьет по incident response.

У команды уже могут быть telemetry, policies и approvals, но она все равно теряет время на самом базовом вопросе контура: какая именно production entity отвечает за этот path прямо сейчас?

## 10. Пример минимальной записи в реестре агентов

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
  mcp_surface:
    approved_servers:
      - support-registry/ticketing-mcp
    discovery_sources:
      - platform_registry
    auth_mode: managed_oauth
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

Такая запись уже достаточно полезна, чтобы связывать агента с ownership, controls, lifecycle и verifier-aware evidence expectations.

На уровне контура это еще и помогает отвечать на вопрос, который команды часто упускают: какие verifier contracts сейчас активны, какие уже deprecated и какие агенты все еще зависят от старых версий.

## 11. Пример проверки здоровья реестра

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

Здесь логика простая: агент без owner, lifecycle state и observability linkage вообще не должен считаться production-ready entity.

## 12. Самые частые режимы отказа

- агенты есть в проде, но отсутствуют в инвентаре;
- инвентарь существует, но lifecycle states не поддерживаются;
- реестр не знает про principals и approvals;
- deprecated-агенты остаются с доступом к tool paths;
- запись в реестре не показывает, кто отвечает за paused approvals или aging background runs;
- contract versions дрейфуют, пока реестр все еще указывает на устаревшие control assumptions;
- разные реестры расходятся между собой;
- platform team знает одних агентов, а security team — других.

## 13. Быстрый тест зрелости для управления агентами

Команде не стоит думать, что она контролирует свой агентский контур только потому, что у нее есть spreadsheet с реестром и примерное число развернутых агентов.

Более сильная планка такая:

- инвентарь и реестр живут как разные контуры управления;
- у каждого production-агента есть owner, lifecycle state и policy linkage;
- telemetry coverage можно непрерывно сверять с реестром;
- paused approvals, ownership фоновых запусков и contract versions входят в контур управления реестром;
- deprecated и orphaned agents можно найти до того, как они станут blind spots;
- управление умеет различать discovered entities и approved production agents.

Если большинство этих условий не выполняется, у команды уже могут быть фрагменты видимости, но реального управления агентами у нее пока нет.

В этот момент реестр все еще ведет себя как loose catalog.

Зрелый реестр ведет себя скорее как accountability layer, который непрерывно сверяет production entities, control ownership и lifecycle truth.

## 14. Практический чеклист

- Можешь ли ты быстро назвать число active, deprecated и retired agents?
- У каждого production-агента есть owner?
- Связана ли запись в реестре с policy bundle, approval mode, runtime-control ownership и `bundle_id`?
- Видно ли из инвентаря, какие агенты не шлют telemetry?
- Можно ли быстро найти orphaned или deprecated-агентов с живыми principals?
- Есть ли у тебя различие между “обнаружен” и “одобрен для production”?

Если несколько ответов подряд “нет”, то агентский контур у тебя уже есть, а управления агентами еще нет.

## 15. Модель доказательности этой главы

Эту главу стоит читать как accountability layer, а не как spreadsheet инвентаризации:

- **Устойчивые утверждения:** governance агентов требует больше, чем discovery; каждому production agent нужны ownership, lifecycle state, policy linkage и observable control status.
- **Вендорская практика:** guidance по infrastructure inventory и agentic risk сходится к continuous asset coverage, ownership и control accountability.
- **Runtime-практика:** registry records, lifecycle artifacts, policy bundles, approval modes, principal status и telemetry coverage делают agent estate проверяемым.
- **Авторская интерпретация:** registry — закрывающий слой, который связывает observability, policy, lifecycle и retirement в одну accountable production entity.
- **Быстро меняющаяся область:** agent builders, registries и discovery mechanisms будут меняться; различие между discovered entities и approved production agents — нет.

## 16. Полезные справочные страницы

- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)
- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема запроса на подтверждение и записи о решении](../../appendix/approval-schema.md)
- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема наборов для оценки и правил проверки](../../appendix/eval-schema.md)
- [Схема памяти и извлечения](../../appendix/memory-retrieval-schema.md)
- [Research frontier: память, наблюдаемость и надежность multi-agent систем](../../appendix/research-frontier.md)

- [Глава 23. Retirement, replacement и end-of-life discipline](chapter-23.md)
- [Глава 24. Agentic misalignment и insider-risk](chapter-24.md)
- [Глава 26. Наблюдаемость для ИИ-систем, покрытие реестра и телеметрия для обнаружения проблем](chapter-26.md)

[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
[^nist-sp53]: NIST, [SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
