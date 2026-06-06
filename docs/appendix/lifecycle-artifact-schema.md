# Схема артефактов жизненного цикла

Эта страница собирает в одном месте минимальный контрактный слой для артефактов жизненного цикла: запись изменения, утвержденный пакет артефактов и план вывода из эксплуатации. Если схема трасс отвечает на вопрос "что произошло", а схема оценок отвечает на вопрос "как это оценивать", то схема артефактов жизненного цикла отвечает на вопрос "что именно было одобрено, изменено, заменено или выведено из эксплуатации".

!!! example "Артефакт жизненного цикла для цепочки дубля тикета"
    Для пакета разбора обращений поддержки нужно удерживать вместе не только `policy_bundle` и `eval_dataset`, но и доказательства защиты от дубля тикета: требование `idempotency_key`, запись подтверждения, трассу с `side_effect_unknown`, `duplicate_ticket_eval_passed` и шлюз раскатки. Тогда разбор инцидента восстанавливает одну цепочку `change -> bundle -> approval -> trace -> eval -> rollout`, а не ищет доказательства по разным страницам.

!!! note "Канонические сценарии жизненного цикла"
    Артефакты жизненного цикла должны удерживать разные цепочки артефактов для трех канонических сценариев. **Триаж обращений поддержки** связывает запись изменения, утвержденный пакет артефактов, запись подтверждения, трассу, набор оценок, шлюз раскатки и план вывода из эксплуатации для защиты от дубля тикета. **Внутренний ассистент знаний** связывает политику поиска, политику памяти, происхождение источников, проверку контроля доступа и план замены базы знаний. **Координация инцидентов** связывает политику эскалации, возможность уведомлений, карту владения ответом, артефакт передачи управления и план вывода из эксплуатации или замены обучения после инцидента.

Она напрямую связана и со страницей [Сквозная цепочка доказательств: от запроса к решению о раскатке](../book/part-v/evidence-spine.md), потому что артефакты жизненного цикла входят в ту управляемую запись, на которую потом опираются суждение и разбор инцидента.

## 1. Зачем это нужно

У агентной системы промышленного уровня есть несколько классов артефактов, которые нельзя держать только в голове команды или в wiki:

- записи изменений (change records);
- утвержденные пакеты артефактов (approved artifact bundles);
- планы вывода из эксплуатации (retirement plans);
- карты замены (replacement mappings);
- связи между схемами управления средой исполнения и версиями контрактов;
- рабочие подтверждения и решения жизненного цикла;
- правила прерывания, истечения и повторной инициализации сессий возможностей, если они уже входят в контракт времени выполнения;
- правила делегированного разрешения, допущения о привязке субъекта и поведение отзыва, если они уже входят в контракт времени выполнения;
- контракты проверяющего, рубрики оценивания и правила связи доказательств, если выпуск или заверение зависят от вывода проверяющего;
- структурированные артефакты передачи управления, если длинная работа пересекает границу сброса контекста или передачи роли.

Без этого управление изменениями быстро разваливается на устные договоренности. А разбор инцидента превращается в расследование того, кто и когда "примерно поменял policy или routing".

## 2. Базовые сущности

Минимальный слой жизненного цикла удобно строить вокруг трех сущностей:

- `change_record`
- `artifact_bundle`
- `retirement_plan`

Этого уже достаточно, чтобы связать проверку дизайна, шлюз выпуска, контур заверения и дисциплину завершения жизненного цикла.

## 3. Запись изменения

`change_record` описывает конкретное изменение и его операционный смысл.

Минимальные поля:

```yaml
kind: change_record
change_id: chg-2026-04-07-001
title: "Tighten outbound policy for ticket_write"
change_type: policy_update
risk_level: high
owner: platform-safety
affected_surfaces:
  - policy_bundle
  - capability_contract
  - runtime_control_schema
  - capability_session_contract
  - sandbox_profile_contract
  - rollout_rules
eval_requirements:
  - offline_regression
  - targeted_safety_eval
approval_requirements:
  - safety_review
  - platform_review
rollback_unit:
  - policy_bundle:v4
  - approvals_bundle:v3
status: approved
```

Что здесь особенно важно:

- `affected_surfaces` не дает делать вид, будто изменение маленькое;
- `eval_requirements` связывает change management с eval loop;
- `rollback_unit` заставляет заранее понимать, что именно откатывается;
- `status` нужен не как бюрократия, а как эксплуатационный факт.

А если в системе уже есть длительные сессии возможностей с привязкой к подтверждению или выполнение с опорой на песочницу, `change_record` почти всегда стоит делать достаточно явным, чтобы было видно, входили ли правила прерывания, обработки истечения, повторной инициализации, делегированного разрешения и контракт профиля песочницы в проверяемую поверхность.

## 4. Утвержденный пакет артефактов

`artifact_bundle` фиксирует набор артефактов, которые считаются доверенными и совместимыми друг с другом в конкретной конфигурации выпуска. На практике это еще и контрактная поверхность, которая задает управляемую идентичность выпуска.

Эталонная среда исполнения хранит этот контракт в `artifacts.yaml`: `bundle_name` — например, `support-triage-runtime-bundle` — `version`, `provenance_required`, `signed` и `session_control_owner` описывают идентичность пакета и подотчетность; ошибки в полях идентичности и происхождения явно падают с `bundle.version must be a string`, `bundle.version is required`, `'bundle.provenance_required' must be a boolean` и `'bundle.signed' must be a boolean`; `review_evidence` также может указывать на ссылки на доказательства вроде `trace:sandbox_profile_reviewed` и на цепочку доказательств `duplicate_ticket_guard`; а `artifacts` явно перечисляет файлы конфигурации релиза: `agent.yaml`, `capabilities.yaml`, `policy.yaml`, `memory.yaml`, `controls.yaml`, `approvals.yaml`, `runtime-controls.yaml`, `change.yaml`, `retirement.yaml`, `eval-dataset.json` и `runtime-control-bundle-metadata`.

```yaml
kind: artifact_bundle
bundle_id: bundle-2026-04-07-a
owner: platform-runtime
artifacts:
  model_route: gpt-5.4-tools
  policy_bundle: policy-v4
  approvals_bundle: approvals-v3
  controls_bundle: controls-v2
  runtime_control_schema: runtime-controls-v2
  sandbox_profile: sandbox-profile-v1
  capability_catalog: catalog-v5
  eval_dataset: eval-set-2026-04-07
  verifier_contract: verifier-v2
  contract_version: capability-contract-v5
review_evidence:
  sandbox_profile_reviewed:
    trace_event: sandbox_profile_reviewed
    workspace_manifest_ref: runtime-controls.yaml#runtime_controls.sandbox_profile.workspace
    permissions_profile: restricted-shell-network-denied
    network_secrets_posture: network:denied,secrets:none
    snapshot_policy: required_on_completion
    review_evidence_refs:
      - trace:trace-sandbox-review-001
      - eval:sandbox_profile_review
  duplicate_ticket_guard:
    idempotency_key_required: true
    eval_ref: eval:duplicate_ticket_eval_passed
    approval_ref: approval:apr-2026-04-07-001
    rollout_gate_ref: gate:gate-2026-04-07-001
status: approved
release_scope: canary
provenance:
  change_record: chg-2026-04-07-001
  reviewed_by:
    - safety-review
    - runtime-review
```

Этот слой полезен по трем причинам:

- он отделяет "есть артефакт" от "артефакт одобрен для релиза";
- он делает идентичность выпуска проверяемой, а не неявной договоренностью;
- он делает разбор инцидента и откат гораздо короче.

А когда управление сессией возможности уже оформлено явно, пакет почти всегда стоит делать достаточно подробным, чтобы было видно не только версию контракта, но и какие допущения управления сессией и семейство контрактов с ограничениями проверяющего были одобрены вместе с ним:

- политика истечения срока;
- политика повторной инициализации;
- владение застрявшим или истекшим состоянием сессии возможности;
- ожидания по связи между событиями подтверждения и событиями сессии;
- режим делегированного разрешения;
- требования к привязке субъекта;
- поведение отзыва для приостановленных или уже выполняющихся действий;
- версия контракта проверяющего, рубрика оценивания и ожидания по связи доказательств, если раскатка или заверение зависят от суждений проверяющего;
- доказательства разбора профиля песочницы, включая событие трассы `sandbox_profile_reviewed`, `workspace_manifest_ref` и ссылки на доказательства оценки/раскатки, если идентичность выпуска включает выполнение в песочнице.

## 5. План вывода из эксплуатации

`retirement_plan` нужен не только для полного выключения агента, но и для управляемой замены возможности, набора политик или семейства артефактов. Эталонный загрузчик также явно фиксирует идентичность замены: испорченные поля замены падают с `retirement.replacement_mode must be a string` и `retirement.replacement_mode is required`, рядом с уже описанной проверкой для `retirement.system_id`.

```yaml
kind: retirement_plan
retirement_id: retire-2026-04-ticket-write-v1
target: capability:ticket_write_v1
trigger: deprecated_capability
replacement: capability:ticket_write_v2
phases:
  - freeze_new_rollouts
  - dual_run
  - traffic_shift
  - expire_paused_runs
  - stop_background_routes
  - revoke_principal
  - archive_artifacts
historical_state:
  traces: retain_90_days
  approvals: retain_180_days
  memory: review_before_delete
status: planned
owner: platform-operations
```

Сильная сторона этого артефакта в том, что он заставляет думать не только о замене, но и о следах прежней системы:

- трассы;
- подтверждения;
- paused-run state;
- ownership фоновых маршрутов;
- субъекты доступа;
- память;
- архивированные пакеты артефактов;
- структурированные артефакты передачи управления, в которых фиксировались границы спринта, замечания проверяющего или решения на границе сброса контекста;
- состояние истекших capability-session, если оно все еще важно для аудита или отложенного ответа оператора.

## 6. Как это связано с частью VIII

Эта схема напрямую поддерживает несколько глав:

- Глава 20: управление изменениями;
- Глава 21: выводы заверения, которые становятся входом жизненного цикла;
- Глава 22: утвержденные артефакты и происхождение;
- Глава 23: переход на заменяющую поверхность и вывод из эксплуатации.

Именно поэтому артефакты жизненного цикла полезно держать не как документацию только в виде прозы, а как проверяемый YAML- или JSON-контракт.

Эталонная среда исполнения отражает эту форму в `retirement.yaml`: `system_id` и `replacement_mode` идентифицируют выводимую из эксплуатации поверхность, причём эталонный пакет использует `staged_replacement` для управляемой передачи управления, `triggers` объясняют, почему начинается вывод из эксплуатации (`deprecated_runtime`, `replacement_ready` и `unsafe_capability_pattern`), `required_steps` включает меры контроля вроде `freeze_rollout`, `disable_risky_capabilities`, `stop_memory_write`, `expire_paused_runs`, `stop_background_routes`, `freeze_reinitialization`, `revoke_egress`, `archive_audit_state` и `set_retired_status`, а `session_control_owner`, `emergency_freeze_owner` и `archive_targets` явно фиксируют владение и сохраняемые доказательства. Архивный список называет `telemetry_jsonl`, `session_exports`, `approval_history`, `paused_run_state`, `capability_session_state` и `runtime_control_bundle` — именно записи, которые должны оставаться доступными для ревью после вывода из эксплуатации. Краткая исполняемая сводка `check-retirement` возвращает `system_id`, `ready`, `triggers`, `missing_steps`, `required_steps`, `archive_targets`, `failed_run_archive_targets`, `support_duplicate_archive_targets` и `replacement_mode`, чтобы оператор видел и незавершенные шаги вывода из эксплуатации, и точные пакеты доказательств, которые переживают вывод из эксплуатации ради разбора деградировавших путей и защиты от дубля тикета; испорченные переопределения шагов вывода из эксплуатации падают с `Assessment signals must be a mapping`, `Assessment signal key must be a string`, `Assessment signal key must not be empty`, `Assessment signal keys must be unique` и `Assessment signal value must be a boolean: {field}`.

Загрузчики артефактов жизненного цикла отделяют испорченные входы состояния релиза от проваленных проверок: `change config must be a mapping`, `artifact bundle config must be a mapping` и `retirement config must be a mapping` отклоняют неверные корни; `change config keys must be strings`, `artifact bundle config keys must be strings` и `retirement config keys must be strings` отклоняют нестроковые YAML-ключи; `change.change_id must be a string`, `change.change_id is required`, `change.session_control_owner is required`, `change.emergency_freeze_owner is required`, `bundle.bundle_name must be a string`, `bundle.bundle_name is required`, `bundle.session_control_owner is required`, `retirement.system_id must be a string`, `retirement.system_id is required`, `retirement.session_control_owner is required` и `retirement.emergency_freeze_owner is required` отклоняют потерю идентичности и владения; списки вроде `required_signals`, `artifacts` и `archive_targets` отклоняют неправильные значения через `{key} must be a list`, `{key} entries must be strings`, `{key} entries must not be empty` и `{key} entries must be unique`; доказательства ревью артефактов отклоняют испорченные карты доказательств через `artifact bundle review_evidence config must be a mapping`, `artifact bundle review_evidence config keys must be strings`, `artifact bundle review_evidence key must not be empty` и `artifact bundle review_evidence keys must be unique`.

## 7. Минимальные инварианты

Если делать совсем коротко, у слоя артефактов жизненного цикла должны быть такие инварианты:

- каждое высокорисковое изменение имеет `change_record`;
- каждый производственный шлюз раскатки указывает на `artifact_bundle`;
- каждый artifact bundle может служить конкретной записью об идентичности выпуска, а не просто рыхлым списком версий;
- каждый artifact bundle связывает runtime-control schema и contract version, если такие controls существуют;
- lineage verifier contract и идентичность семейства контрактов можно восстановить, если release или assurance зависят от graded outcomes;
- sandbox profile review evidence можно восстановить из bundle, trace или eval artifact, если rollout требовал `sandbox_profile_reviewed`;
- у deprecated artifact есть `retirement_plan` или явное исключение;
- вывод из эксплуатации или путь замены объясняет, что происходит с paused runs, handoff artifacts и expired capability-session state, если такие контуры вообще есть;
- delegated authorization ownership и revoke behavior можно восстановить для затронутых runs, если такие controls существуют;
- lifecycle artifacts имеют owner и version;
- incident review может восстановить связку `change -> bundle -> run -> retirement`;
- session-control ownership можно восстановить для expired, paused или re-initialized capability paths.

## 8. Что чаще всего ломается

Проблемы обычно очень узнаваемые:

- bundle собирается "на словах", а не как артефакт;
- change records живут отдельно от eval requirements;
- retirement есть в roadmap, но не в operational config;
- замена делается без семантики двойного прогона;
- historical state не имеет retention owner;
- provenance заканчивается на уровне git commit и не доходит до runtime bundle;
- paused-run и expired-session state теряются при замене, хотя они еще могут быть нужны операторам;
- lineage verifier contract теряется, хотя от него зависели rollout или assurance decisions;
- bundle указывает `sandbox_profile`, но не хранит ссылку на review evidence по workspace, permissions и snapshot/resume policy.

## 9. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли у высокорисковых изменений явные записи изменений?
- Есть ли утвержденный пакет артефактов, а не просто список последних YAML-файлов?
- Можно ли по трассе инцидента восстановить активный пакет и его идентичность выпуска?
- Можно ли понять, под каким семейством контрактов с verifier-ограничениями выпуск был одобрен?
- Если пакет включает `sandbox_profile`, можно ли найти доказательства разбора для рабочей области, прав и политики снимков/возобновления?
- Есть ли план вывода из эксплуатации для устаревших возможностей и наборов политик?
- Есть ли владелец у архивного состояния после замены?
- Понятна ли единица отката на уровне артефактов жизненного цикла?

Если на несколько вопросов подряд ответ "нет", у тебя уже может быть хороший SDLC и даже хороший rollout, но слой жизненного цикла пока еще не собран до конца.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Эталонный пакет](reference-package.md)
- [Глава 20. Управление изменениями в агентных системах](../book/part-viii/chapter-20.md)
- [Глава 22. Цепочка поставки, происхождение и доверенные артефакты](../book/part-viii/chapter-22.md)
- [Глава 23. Вывод из эксплуатации, замена и дисциплина завершения жизненного цикла](../book/part-viii/chapter-23.md)
