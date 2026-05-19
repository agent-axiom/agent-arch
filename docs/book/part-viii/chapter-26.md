# Глава 26. Наблюдаемость для ИИ-систем, покрытие реестра и телеметрия для обнаружения проблем

!!! info "Актуальность главы"
    Последняя редакционная проверка: **17 мая 2026 года**. Предыдущая проверка: **14 мая 2026 года**. Следующая плановая проверка: **17 июня 2026 года**.

    Что изменилось после предыдущей проверки: явно зафиксированы MCP/A2A security surfaces, verifier contracts, governance-aware telemetry и publisher-readiness замечания как ближайшие редакционные задачи.

    Быстрее всего здесь меняются:

    - продукты для телеметрии agent systems и вендорские tracing features;
    - эвристики обнаружения drift, abuse и suspicious tool behavior;
    - emerging conventions для diagnosis-ready traces и correlation across systems.

    Медленнее меняются:

    - требование строить evidence-ready telemetry, а не только debugging logs;
    - связь observability с approvals, runtime-control states, policy decisions, tool principals, contract versions и artifact bundles;
    - важность полного inventory coverage для detection и incident review.

## 1. Почему наблюдаемость для агентов нельзя сводить к задержке и ошибкам

В обычном сервисе наблюдаемость часто начинается с простого набора:

- задержка;
- доля ошибок;
- пропускная способность;
- использование ресурсов.

Для агентных систем этого недостаточно.

Здесь важно держать простое различие: assurance решает, когда нужен containment и кто отвечает за response. Observability делает такое решение возможным, потому что сохраняет evidence, которому реально можно доверять в release, incident и governance work.

Система может:

- не падать;
- отвечать быстро;
- отдавать HTTP 200;
- и при этом вести себя опасно, некачественно или неуправляемо.

Microsoft точно формулирует этот сдвиг: для агентных систем нужно эволюционировать от обычных журналов, метрик и трасс к сигналам, которые помогают восстанавливать не только факт запроса, но и форму поведения системы. [^ms-observability]

## 2. Наблюдаемость здесь нужна не только для отладки

У агентной платформы наблюдаемость играет как минимум пять ролей:

- отладка рантайма;
- восстановление картины инцидента;
- обнаружение злоупотреблений;
- доказательная база для выпуска;
- покрытие контура управления.

Если трассы существуют только для разработчика, который локально ищет баг, этого уже недостаточно.

В рабочей среде тебе нужно уметь отвечать и на другие вопросы:

- сколько агентов вообще существует;
- какой процент из них вообще наблюдаем;
- какие возможности они реально вызывают;
- где идут high-risk actions;
- какие подтверждения были запрошены, одобрены или обойдены;
- какие сдвиги поведения появились после раскатки.

## 3. Какие сигналы здесь действительно нужны

Для агентных систем полезный контракт телеметрии обычно включает:

- request identity;
- `run_id`, `trace_id`, `session_id`;
- identity актора и агента;
- происхождение данных извлечения;
- вызовы инструментов;
- права инструментов и принципалы;
- решения политик;
- подтверждения;
- состояние и возраст paused runs;
- сигналы backlog по approval;
- состояние capability sessions, причины expiry и статус re-init;
- выбранный orchestration pattern и lineage delegated workers;
- состояние и возраст background runs;
- краткие итоги ответа;
- статус маскирования данных;
- verifier outputs вроде `process_score`, `outcome_score` и `failure_attribution`;
- active verifier contract и версию verifier contract;
- набор артефактов, версию, волну раскатки и contract version.

Чтобы этот список не превращался в свалку полей, его полезно держать как пять групп сигналов:

1. **Identity and scope:** кто действует, от чьего имени и в каком tenant/request scope.
2. **Control evidence:** какие policy decisions, approvals, quotas и capability sessions ограничивали run.
3. **Execution state:** какой orchestration pattern выбран, где run paused/background/delegated и как он возобновлялся.
4. **Quality evidence:** какие verifier outputs, eval verdicts и failure attribution связаны с outcome.
5. **Release and artifact context:** какой bundle, contract version и rollout wave поддерживали этот запуск.

То есть трассы должны рассказывать не только «что упало», но и:

- кто действовал;
- через какой слой управления;
- с какими правами;
- по каким правилам;
- в рамках какого набора артефактов;
- и с каким внешним действием.

Именно поэтому runtime-control signals больше нельзя считать скрытой implementation detail. Как только появляются pause/resume paths, background execution и contract-version transitions, они тоже становятся частью evidence layer.

Но это еще не делает observability владельцем artifact lineage. Observability сохраняет и коррелирует evidence поперек runs. А provenance layer по-прежнему отвечает на вопрос, какой governed artifact, approved version или release identity потом поддерживали решение.

В этом и состоит главный смысл этой главы. Она должна показать observability как evidence substrate всего жизненного цикла: слой, который делает поведение рантайма, control signals, approvals и активность между системами достаточно видимыми, чтобы assurance, rollout, judgment и registry functions могли опираться на одну и ту же operational record. Главный артефакт этой главы — trace and telemetry coverage record: карта того, какие агенты, capabilities, control paths и side effects действительно наблюдаемы, а где остаются blind spots.

## 4. Покрытие реестра — это тоже наблюдаемость

Есть важная мысль, которую часто упускают: наблюдаемость начинается не с красивого средства просмотра трасс, а с понимания, какие системы вообще существуют.

Microsoft отдельно подчеркивает полный производственный реестр как необходимое условие для надежной телеметрии. [^ms-inventory]

Для парка агентов это означает, что ты должен знать:

- какие агенты активны;
- какие уже deprecated;
- какие коннекторы и возможности у них есть;
- какие принципалы они используют;
- какие из них вообще шлют телеметрию;
- какие слепые зоны остаются.

Если у тебя нет покрытия реестра, у тебя нет полноценной наблюдаемости. У тебя есть только частично освещенная сцена.

## 5. Поведенческие базовые линии важнее простого объема

В агентных системах сигнал «у нас стало больше запросов» сам по себе мало что значит.

Гораздо важнее уметь видеть отклонение от нормального поведения:

- неожиданное увеличение рискованных вызовов инструментов;
- рост отказов в подтверждении;
- стареющий approval backlog или stuck paused runs;
- изменение характера записей в память;
- смену обычного профиля извлечения;
- всплеск необычных направлений сетевого выхода;
- всплески capability-session expiry или необычный рост re-init rate;
- несовпадения между approval и resume после interruption;
- неожиданные сдвиги в выборе orchestration patterns или пересечениях worker boundaries;
- рост длины сессии или числа переходов между инструментами.

Именно здесь наблюдаемость начинает пересекаться с обнаружением угроз и рабочим управлением.

Но она не должна в них растворяться. Observability — это evidence substrate, который позволяет assurance, rollout и registry functions опираться на одну и ту же traceable record, а не на конкурирующие dashboards, screenshots или воспоминания участников.

Этот substrate говорит о usable telemetry на масштабе множества runs и systems. Это не то же самое, что provenance backbone, которая хранит approved artifact identity и decision lineage во времени.

## 6. Что значит телеметрия, готовая к обнаружению проблем

Такая телеметрия — это не просто «мы что-то пишем в журналы».

Это значит, что телеметрия уже годится для:

- расследования;
- корреляции;
- обнаружения злоупотреблений;
- проверки контуров управления.

Практически это означает:

- единые идентификаторы;
- стабильные схемы;
- правила маскирования;
- политику хранения;
- связи между трассами, подтверждениями, решениями политик, runtime-control states, capability-session events, событиями orchestration pattern, [verifier evidence](../../appendix/eval-schema.md), identity, verifier contract и артефактами жизненного цикла.

Если трассу нельзя связать с `approval_id`, `tool_principal`, `policy_bundle`, `contract_version`, `rollout_wave` и [verifier evidence](../../appendix/eval-schema.md) о том, как именно run был оценен, то она может быть полезна для отладки, но все еще слаба как доказательный слой.

Рекомендации Microsoft по observability делают вопрос покрытия более конкретным: командам стоит измерять долю AI systems, которые вообще emit logs и traces, долю releases, прошедших стандартный evaluation suite, и долю abuse/security scenarios, покрытых telemetry.[^ms-observability] Так observability перестает быть фразой “у нас есть dashboards” и становится измеримой production obligation: inventory coverage, release-eval coverage и detection-scenario coverage.

!!! example "Сквозной кейс: telemetry для ticket-write control eval"
    Control eval из support-triage становится полезным для rollout только если его telemetry detection-ready. Для каждого `create_support_ticket` run trace должен связывать `approval_id`, `tool_principal`, `policy_bundle`, `contract_version`, `rollout_wave`, outcome, `side_effect_unknown` и verdict process/outcome verifier-а. Тогда команда может видеть не только “дубля нет”, но и какой процент ticket-write paths реально observable, где bypass path еще слепой и можно ли safely расширять canary.

**Observability case-spine note:** [trace and telemetry coverage record](../../appendix/trace-schema.md) должен показывать observability coverage для всех трех canonical cases. Support triage требует coverage для ticket-write paths, [approval linkage](../../appendix/approval-schema.md), `tool_principal`, [`policy_bundle`](../../appendix/policy-bundle-schema.md), `contract_version`, duplicate outcome и bypass blind spots. Internal knowledge assistant требует coverage для [retrieval provenance](../../appendix/memory-retrieval-schema.md), source-grounding verdicts, tenant-filter decisions, [memory-write events](../../appendix/memory-retrieval-schema.md) и freshness drift. Incident coordination требует coverage для escalation path, notification delivery, responder-role identity, [incident-state transitions](../../appendix/incident-record-schema.md), rollback events и [post-incident control changes](../../appendix/lifecycle-artifact-schema.md).

## 7. Почему управление без наблюдаемости почти всегда хрупкое

Контур управления нередко оформляют как:

- наборы политик;
- процессы проверки;
- шлюзы выпуска;
- контракты подтверждения.

Но без наблюдаемости все это слишком легко превращается в бумажный контур.

Сильный контур управления требует:

- видеть фактическое поведение;
- замечать дрейф;
- измерять покрытие;
- отличать управляемый путь от обходного;
- замечать stuck approvals, aging background runs, capability-session expiry drift, approval-resume misuse, orchestration-pattern drift, verifier-quality drift и contract mismatches до того, как они станут инцидентами.

Поэтому наблюдаемость в агентных системах лучше воспринимать как доказательный слой для управления.

### 7.1. Governance-aware telemetry замыкает контур enforcement

Следующий уровень зрелости — не просто видеть событие, а сделать telemetry пригодной для управленческого действия. `Governance-aware telemetry` должна возвращаться в контур контроля как вход для policy decisions, containment, rollout gates и incident response.

Минимальный closed-loop contract здесь выглядит так:

- `policy_decision_feedback`: какие telemetry signals меняют последующее policy решение или risk tier;
- `containment_decision`: какой сигнал переводит run, agent, capability или rollout wave в paused / quarantined state;
- `rollout_gate_input`: какие coverage, verifier и drift signals блокируют расширение canary;
- `incident_response_trigger`: какие patterns создают investigation, escalation или postmortem task;
- `registry_update_signal`: какие blind spots, stale owners или shadow capabilities требуют обновления inventory.

Чтобы это не осталось красивой схемой, каждое такое событие полезно сохранять как маленький [governance action record](../../appendix/trace-schema.md):

- `governance_action_id`: стабильный идентификатор управленческого действия;
- `source_signal`: telemetry signal или detection scenario, который запустил действие;
- `decision_owner`: роль или команда, отвечающая за решение;
- `action_state`: `open`, `accepted`, `waived`, `contained`, `closed`;
- `evidence_refs`: ссылки на trace, verifier output, policy decision и rollout gate;
- `review_deadline`: когда action должен быть пересмотрен или закрыт.

Тогда telemetry перестает быть только dashboard-сигналом. Она становится входом в проверяемую governance queue, где видно, кто принял решение, на каких доказательствах и почему контур можно снова считать управляемым.

Так telemetry перестает быть только evidence after the fact. Она становится рабочим входом для governance loop: наблюдение → решение политики → containment или rollout action → новое evidence о результате.

Именно такая рамка отделяет эту главу и от assurance chapter, и от registry chapter. Assurance отвечает за containment и response. Registry отвечает за accountability всего estate. Observability — это общий слой, который делает обе функции audit-friendly.

И ее же важно удерживать отдельно от provenance chapter. Observability спрашивает, emitted ли система достаточно evidence, coverage и correlation для расследования и detection. Provenance спрашивает, какой approved artifact set, contract version или governed bundle потом обосновывали решение.

## 8. Куда исследовательская повестка двигает наблюдаемость дальше

Свежие исследовательские статьи по наблюдаемости для агентов идут еще дальше: они пытаются превратить трассы из удобного журнала событий в слой причинной диагностики.

Из этого для книги полезны две мысли.

Первая: одного средства просмотра трасс недостаточно. Красивый интерфейс вокруг потока событий еще не дает внятного ответа, если:

- словарь трасс слишком бедный;
- запуск нельзя связать с сессией, подтверждением и набором артефактов;
- корневую причину все равно приходится восстанавливать вручную по длинной расшифровке.

Вторая: причинная диагностика выглядит перспективно, но ее пока рано считать решенной задачей. Исследования уже показывают интересный путь вперед, но производственная дисциплина по-прежнему должна стоять на более приземленных вещах:

- стабильный каталог событий;
- версионирование схем;
- правила маскирования;
- трассы с учетом сессий;
- явные связи между телеметрией, подтверждениями и артефактами жизненного цикла.

То есть исследования здесь полезны не как повод обещать «полную объяснимость», а как напоминание, что наблюдаемость должна постепенно эволюционировать от логирования к диагностике.

<div class="diagram-card">
<p>Наблюдаемость для ИИ-систем полезно мыслить как связку телеметрии, реестра и доказательств для управления</p>

``` mermaid
flowchart LR
    A["Покрытие реестра"] --> D["AI-native observability"]
    B["Телеметрия рантайма"] --> D
    C["Policy и approval evidence"] --> D
    D --> E["Реконструкция инцидента"]
    D --> F["Поведенческие baseline"]
    D --> G["Abuse detection"]
    D --> H["Release evidence"]
```

</div>

## 9. Минимальная политика покрытия наблюдаемостью

```yaml
observability:
  require:
    request_identity: true
    trace_ids: true
    session_ids: true
    policy_decisions: true
    tool_principals: true
    approval_linkage: true
    paused_run_visibility: true
    capability_session_visibility: true
    background_run_visibility: true
    orchestration_pattern_visibility: true
    worker_boundary_visibility: true
    verifier_evidence_linkage: true
    verifier_contract_visibility: true
    contract_version_linkage: true
    artifact_bundle_linkage: true
  kpis:
    min_agent_inventory_coverage_pct: 95
    min_trace_coverage_pct: 95
    min_high_risk_action_trace_pct: 100
  block_if:
    - untracked_high_risk_agent_exists
    - approval_events_not_linked
    - paused_runs_not_visible
    - capability_session_events_not_visible
    - orchestration_pattern_events_not_visible
    - worker_boundary_crossings_not_visible
    - verifier_evidence_not_linked
    - verifier_contract_missing
    - contract_version_missing
    - bundle_version_missing
```

Такая политика помогает обсуждать наблюдаемость как обязательный рабочий слой, а не как опциональную удобную функцию для платформенной команды.

## 10. Пример простой проверки покрытия

```python
from dataclasses import dataclass


@dataclass
class ObservabilityCoverage:
    inventory_coverage_pct: int
    trace_coverage_pct: int
    high_risk_trace_coverage_pct: int
    paused_run_visibility: bool
    capability_session_visibility: bool
    orchestration_pattern_visibility: bool
    verifier_evidence_linked: bool


def observability_ready(state: ObservabilityCoverage) -> bool:
    return (
        state.inventory_coverage_pct >= 95
        and state.trace_coverage_pct >= 95
        and state.high_risk_trace_coverage_pct == 100
        and state.paused_run_visibility
        and state.capability_session_visibility
        and state.orchestration_pattern_visibility
        and state.verifier_evidence_linked
    )
```

Здесь идея не в цифрах как таковых. Идея в том, что готовность наблюдаемости тоже должна становиться явным шлюзом.

## 11. Самые частые режимы отказа

- трассы есть только у основного рантайма, но не у реальных адаптеров;
- агенты существуют вне реестра;
- подтверждения журналируются отдельно и не связываются с трассами;
- paused runs и background runs существуют, но их возраст и ownership не видны в телеметрии;
- телеметрия покрывает штатный путь, но не обходной;
- contract-version drift замечают только после того, как payloads перестают соответствовать ожиданиям;
- orchestration-pattern drift или пересечения worker boundaries не видны как first-class telemetry;
- [verifier evidence](../../appendix/eval-schema.md) оторван от traces или screenshots;
- дрейф замечают только по жалобам пользователей;
- сроки хранения и правила маскирования не согласованы с требованиями расследований.

## 12. Быстрый тест зрелости для AI-native observability

Команде не стоит думать, что у нее уже есть production observability, только потому, что у нее есть traces, dashboards и log pipeline.

Более сильная планка такая:

- inventory coverage и telemetry coverage считаются одной control problem;
- high-risk actions можно связать с approvals, principals, artifact bundles, contract versions, reviewed orchestration patterns и [verifier evidence](../../appendix/eval-schema.md);
- наряду с raw telemetry существуют behavioral baselines;
- возраст paused runs, approval backlog и старение background runs видны как first-class signals;
- unobserved agents считаются governance risk, а не просто пробелом в учете;
- на телеметрию можно опираться как на evidence в release и incident decisions.

Если большинство этих условий не выполняется, у команды уже может быть observability tooling, но AI-native observability как governance layer у нее пока нет.

## 13. Практический чеклист

- Знаешь ли ты, сколько агентов реально живет в рабочей среде?
- Какой процент из них вообще шлет структурированную телеметрию?
- Можно ли связать high-risk action с `trace_id`, `approval_id`, `tool_principal`, `contract_version`, `bundle_id`, активным orchestration pattern и [verifier evidence](../../appendix/eval-schema.md)?
- Есть ли поведенческие базовые линии, а не только сырые дашборды?
- Видишь ли ты возраст paused runs, approval backlog и стареющие background runs до жалоб пользователей?
- Видишь ли ты ненаблюдаемые агенты как отдельный класс риска?
- Можешь ли ты использовать наблюдаемость как доказательную базу для выпуска, а не только как средство отладки?

Если несколько ответов подряд «нет», то наблюдаемость у тебя уже есть, но она пока не стала частью контура управления.

Обычно это означает, что платформа еще умеет описывать активность, но пока не умеет давать тот тип устойчивого evidence, на который reviewer, incident owner или estate governor могут уверенно опираться.

## 14. Модель доказательности этой главы

Эту главу стоит читать как слой evidence readiness, а не как чеклист логирования:

- **Устойчивые утверждения:** агентной системой нельзя управлять, если high-risk actions, approvals, principals, artifacts и [verifier evidence](../../appendix/eval-schema.md) нельзя связать постфактум.
- **Вендорская практика:** современные материалы по observability и infrastructure inventory всё чаще рассматривают telemetry coverage и asset coverage как production controls, а не только debugging aids.
- **Runtime-практика:** structured events, inventory coverage checks, behavioral baselines и detection-ready fields делают traces пригодными для release review и incident response.
- **Авторская интерпретация:** AI-native observability — мост между evals, assurance, registry и lifecycle governance.
- **Быстро меняющаяся область:** tracing products, detectors и telemetry pipelines будут меняться; потребность в attributable, reviewable evidence — нет.

## 15. Полезные справочные страницы

- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема наборов для оценки и правил проверки](../../appendix/eval-schema.md)
- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема approval](../../appendix/approval-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)
- [Схема проверки изменений и шлюза раскатки](../../appendix/change-rollout-schema.md)
- [Схема памяти и извлечения](../../appendix/memory-retrieval-schema.md)
- [Research frontier: память, наблюдаемость и надежность multi-agent систем](../../appendix/research-frontier.md)

- [Глава 11. Трассы, спаны и структурированные события](../part-v/chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../part-v/chapter-13.md)
- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 25. Behavioral evals, control evals и automated red teaming](chapter-25.md)
- [Глава 27. Инвентаризация агентов, реестр и борьба с разрастанием](chapter-27.md)

[^ms-observability]: Microsoft Learn, [Observability for Generative AI and agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/observability-ai-systems)
[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
