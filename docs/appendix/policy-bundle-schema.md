# Схема набора политик и контракта подтверждения

Эта страница связывает несколько уже написанных тем:

- [Глава 4. Инструментальный шлюз, подтверждения и журнал аудита](../book/part-ii/chapter-4.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
- [Глава 20. Управление изменениями в агентных системах](../book/part-viii/chapter-20.md)
- [Сквозная цепочка доказательств: от запроса к решению о rollout](../book/part-v/evidence-spine.md)

И опирается на эталонный пакет:

- [Эталонный пакет](reference-package.md)

Если страницы о схеме трасс и схеме оценки отвечают на вопросы:

- как описывать фактическое поведение;
- как описывать ожидаемое поведение;

то эта страница отвечает на третий вопрос:

- как описывать управляющие правила, которые стоят между рассуждением и внешним действием.

## Почему набор политик полезно мыслить как артефакт

Одна из самых частых ошибок в агентных системах устроена так:

- правила частично живут в инструкции;
- частично в коде шлюза;
- частично в интерфейсе подтверждения;
- частично в голове команды.

Пока система маленькая, это может работать. Но как только появляется управление изменениями, аудит и поэтапная раскатка, такой слой политик становится слишком размытым.

Поэтому полезно собирать набор политик как отдельный артефакт.

## Предлагаемое расширение: привязка credential к идентичности

Мотивация: [LangChain Connections](https://www.langchain.com/blog/connections-managed-credentials-and-per-caller-identity-for-managed-deep-agents). Это внутренний предлагаемый контракт, не новые поля OAuth и не реализованный resolver reference runtime. `credential_owner` (`agent` или `user`) независим от `credential_type` (`secret` или `oauth`).

В решение политики включайте несекретные ссылки `connection_ref`, `credential_ref`, `deployment_ref`, `tenant_ref`, `requester_principal_ref`, `effective_principal_ref`, а также `credential_owner`, `credential_type`, `policy_version` и `authorization_checked_at`. Инициатор берётся из проверенного входного контекста, фактический субъект — из доверенной привязки провайдера; модель не может назначать их аргументами инструмента. Для user-owned credential resolver обязан проверить принадлежность текущему пользователю и tenant. Если фактический субъект не установлен, операция, требующая такой привязки, блокируется. Не храните значения секретов или токены в trace, prompt или ключах кэша.

Проверочные сценарии для будущей реализации:

1. Все четыре сочетания owner/type сохраняются без вывода владельца из наличия OAuth; agent-owned OAuth остаётся общей идентичностью.
2. Пользователи A и B вызывают один connection: приватные результаты и credential A не доступны B; подмена `user_id` аргументом инструмента отклоняется.
3. Нет пользовательского grant: зависимая операция не выполняется; fallback на общий credential запрещён. Consent на доступ не заменяет approval действия.
4. После паузы изменился caller/tenant или доступ отозван: старый credential, кэш и решение allow не переиспользуются без новой проверки.
5. Общая учётная запись используется по явной политике: аудит хранит отдельно инициатора и фактического субъекта; значения credential не попадают в доказательства.


## Предлагаемое расширение: частичный OAuth grant

Это проект промышленного контракта, а не утверждение о поддержке этих полей эталонным runtime. Мотивация — [Cloudflare, From all-or-nothing to task-based OAuth consent](https://blog.cloudflare.com/task-based-oauth-consent/); перечисленные ниже поля относятся к внутреннему policy evidence, а не к новым стандартным полям OAuth.

- `requested_scopes`: scopes конкретного запроса авторизации.
- `granted_scopes`: фактический набор из проверенного ответа сервера авторизации или другого доверенного механизма провайдера; не результат угадывания по тексту запроса и не предположение, что любой токен является JWT.
- `required_scopes`: минимальный набор для выбранной операции; не обязательные scopes consent UI.
- `missing_scopes`: разность required и granted; непустой набор запрещает операцию до side effect.
- `grant_ref`, `authorization_checked_at`: несекретная ссылка на grant и время проверки; вместе с subject, task, tool, resource и policy version позволяют восстановить решение. Сам токен в audit не записывается.

Условный пример (имена scopes и поля evidence иллюстративны):

```yaml
oauth_scope_evidence:
  grant_ref: grant-42
  authorization_checked_at: "2026-09-08T00:00:00Z"
  requested_scopes: [tickets.read, tickets.write]
  granted_scopes: [tickets.read]
  required_scopes: [tickets.write]
  missing_scopes: [tickets.write]
  decision: deny
  reason: insufficient_granted_scope
```

Проверка scopes не заменяет resource/audience/expiry validation, текущую политику и отдельное подтверждение действия. Если grant нельзя достоверно определить, чувствительная операция останавливается; нельзя подставлять requested вместо granted. После refresh/resume проверяется актуальный контекст, а окончательная авторизация остается и на стороне сервиса.

Сценарии приемки предлагаемого контракта:

1. Выданы только права чтения: независимая разрешенная сводка создается, вызов записи не происходит; результат помечен как частичный.
2. Недостающий scope обязателен для всей задачи: остановка с явной причиной, без повторных попыток, другого credential и скрытого запроса расширения.
3. Scope есть, но ресурс или задача вне политики: отказ; широкий grant не отменяет task-scoped authority.
4. После refresh/resume право записи исчезло: прежний allow не переиспользуется.
5. Grant неизвестен либо пользователь полностью отказал: нет перехода к выполнению на основании requested scopes. Action approval не заменяет grant.

## Предлагаемое расширение: кэш каталога MCP

Это внутренний проект контракта, не реализованная возможность `agent_runtime_ref` и не готовая конфигурация FastMCP. `ttlMs` и `cacheScope` — серверные подсказки, описанные FastMCP; остальные поля ниже — предлагаемая нормализация evidence. Источники: [LangChain: MCP in LangChain](https://www.langchain.com/blog/mcp-in-langchain-stateless-protocol-elicitation-and-more) / [FastMCP: Response caching](https://gofastmcp.com/clients/client#response-caching).

```yaml
catalog_cache_evidence:
  target_id: support-mcp-prod
  protocol_version: "2026-07-28"
  request_fingerprint: tools-list-page-1
  partition_ref: verified-tenant-a-principal-7-authz-v3
  policy_version: support-policy-v8
  server_ttl_ms: 60000          # ttlMs
  server_cache_scope: public   # cacheScope
  local_max_ttl_ms: 30000
  effective_ttl_ms: 30000
  fetched_at: "2026-09-08T07:00:00Z"
  expires_at: "2026-09-08T07:00:30Z"
  catalog_digest_ref: catalog-snapshot-42
  cache_hit: true
  authorization_decision_ref: fresh-tool-call-decision-43
```

`partition_ref` выводится из проверенного tenant/principal и контекста доступа; секреты и токены не входят в ключи или журнал. `target_id` должен однозначно определять сервер, а `request_fingerprint` — метод и параметры списка, включая страницу или фильтр. Строки в примере иллюстративны. `server_cache_scope` сохраняет полученное значение `cacheScope` без расширения его смысла. Даже при `public` локальная политика может сохранить более строгую изоляцию.

TTL ограничивает повторное использование снимка: эффективный срок не должен превышать серверный `ttlMs` и локальный предел. Нулевой TTL не дает повторного использования; при отсутствующих или некорректных подсказках этот консервативный контракт требует сетевого чтения без переиспользования кэша. Это локальная политика, а не утверждение о всех значениях по умолчанию SDK. Если обновить просроченный каталог нельзя, не превращай старый снимок в основание для чувствительного вызова. В FastMCP `refresh` читает сеть и обновляет кэш; `bypass` не использует кэш и не сохраняет ответ.

Сценарии приемки предлагаемого контракта:

1. Два пользователя одного tenant с разными правами: каталог первого не обслуживает второго. Общий ответ допустим только при серверном `public` и разрешающей локальной политике.
2. Право отозвано до истечения TTL: актуальная авторизация запрещает вызов; cache hit не переиспользует старый allow, а зависимая от прав видимость инвалидируется.
3. Обнаружена смена определения: refresh, повторная проверка схемы, риска и approval; старое подтверждение не переносится автоматически на другой контракт.
4. TTL истек, равен нулю или подсказка некорректна: сетевое чтение; недоступность сервера не разрешает обход проверки.
5. Смена principal, grant или policy version: другая partition либо инвалидация; ни metadata, ни решение доступа не пересекают границу контекста.

## Предлагаемое расширение: составная авторизация ресурсов

Это предлагаемый внутренний контракт, не готовая конфигурация Cloudflare и не реализованная функция `agent_runtime_ref`. Названия операций и идентификаторы ниже условные; источник разграничения — [роли Workers](https://developers.cloudflare.com/workers/authorization/).

```yaml
compound_authorization_evidence:
  principal_ref: verified-ci-principal
  task_ref: approved-route-change
  plan_ref: immutable-plan-42
  policy_version: deploy-policy-v3
  requirements:
    - action: worker.update
      resource_ref: account-a/worker-a
      required_access: Editor
      decision: allow
    - action: route.write
      resource_ref: account-a/zone-a
      required_access: Workers Routes Write
      decision: deny
  decision: deny
  reason: missing_zone_route_permission
```

Адаптер формирует `requirements` из канонических идентификаторов аккаунта, Worker и всех затронутых зон, включая старую и новую при переносе маршрута. Список не задаётся моделью как доказательство полноты. Каждая проверка использует текущие подтверждённые права того же субъекта; итоговый `allow` требует успеха **всех** проверок, соблюдения границ задачи и отдельного approval, если он нужен. `unknown`, недоступная проверка или хотя бы один `deny` блокируют составное изменение. В аудите сохраняются причины и несекретные ссылки на свидетельства, но не токены.

Предварительная проверка не создаёт транзакцию между API. До первого изменения проверяется весь план; непосредственно перед отдельным вызовом и после паузы права и целевые ресурсы проверяются заново, а сервис сохраняет собственную авторизацию. Смена плана требует нового решения и, при необходимости, подтверждения. Если права отозваны после части вызовов, дальнейшие изменения останавливаются, фактические эффекты сверяются; частичный исход фиксируется, а восстановление проходит отдельную авторизацию. Нельзя обещать автоматический откат или расширять credential ради завершения.

Предлагаемые проверки (не результаты выполненных вызовов Cloudflare):

1. Доступ выдан к Worker A: чтение или изменение Worker B отклоняется даже при одинаковом имени операции.
2. `Metadata Read-Only` позволяет телеметрию A, но не чтение кода; `Content Read-Only` не позволяет деплой.
3. `Editor` допускает обновление существующего A в рамках политики, но не удаление или создание нового Worker.
4. Деплой без изменения маршрута не требует зоны; добавление, изменение или удаление маршрута без `Workers Routes Write` хотя бы на одну затронутую зону блокируется до изменений.
5. Все права составной операции присутствуют: разрешение возможно только для проверенного плана и разрешённой задачи. Подмена зоны после approval требует новой проверки.
6. Отзыв прав между шагами: следующий шаг запрещён; выполненная часть отражена как частичный результат, а не полный успех или гарантированно отменённая операция.

## Что такое набор политик

Под набором политик здесь удобно понимать набор связанных правил, который выпускается как единое целое:

- политика среды выполнения;
- политика инструментов;
- политика подтверждений;
- правила управления средой выполнения для паузы, возобновления и фоновых путей;
- правила записи в память;
- правила эскалации;
- правила исходящего сетевого доступа;
- ожидания относительно доверенных контрактов проверяющего для оценок высокого риска и доказательств раскатки.

Смысл не в том, что все должно лежать в одном YAML-файле. Смысл в том, что такой набор должен быть:

- версионируемым;
- проверяемым;
- трассируемым;
- пригодным к выпуску.

!!! note "Канонические сценарии политик"
    Пакет политик не должен выглядеть одинаково во всех трех канонических сценариях. **Триаж обращений поддержки** требует политики подтверждения для записывающей возможности, доказательств идемпотентности и средств восстановления после дубля тикета. **Внутренний ассистент знаний** требует политики поиска, правил записи в память, проверок свежести, контроля доступа и происхождения знаний. **Координация инцидентов** требует правил эскалации, побочных эффектов уведомлений, владения ответом и шлюзов обучения после инцидента.

## Минимальная структура набора политик

Минимально полезный набор может выглядеть так:

```yaml
bundle:
  bundle_id: policy-support-triage-2026-04-07
  version: 2026.04.07
  owner_team: platform-safety
  applies_to:
    agent_ids: ["support-triage-ref"]
  artifacts:
    - policy.yaml
    - approvals.yaml
    - controls.yaml
  contract_version: capability-contract-v3
  release_identity: release-support-triage-2026-04-07-canary
```

Это еще не сами правила. Это оболочка, которая отвечает на вопрос:

«Что именно мы сейчас считаем артефактом политики для этой агентной системы?»

А когда управление выпуском становится по-настоящему значимым, она должна отвечать и на следующий вопрос:

«В определении какой идентичности выпуска участвует этот набор?»

## Почему контракт подтверждения нельзя прятать внутри описательного текста

Очень часто логика подтверждения описывается словами:

- «если риск высокий, нужно подтверждение»;
- «руководитель одобряет создание тикета»;
- «команда безопасности подтверждает опасные действия».

Этого недостаточно.

Контракт подтверждения полезно делать явным:

- кто может одобрять;
- какой класс действий требует подтверждения;
- какие поля должны попасть в запрос на подтверждение;
- какие решения допустимы;
- что происходит после reject;
- можно ли приостановить запуск, возобновить его, дать ему истечь или отменить;
- что должно остаться в журнале аудита.

## Пример контракта подтверждения

Ниже рабочий каркас:

```yaml
approval_contract:
  capability: create_ticket
  risk_tier: high
  bundle_version: 2026.04.07
  release_identity: release-support-triage-2026-04-07-canary
  required_reviewers:
    - manager
  request_fields:
    - trace_id
    - session_id
    - idempotency_key
    - requested_by
    - reason
    - tool_arguments_redacted
  allowed_decisions:
    - approved
    - rejected
  runtime_controls:
    pause_allowed: true
    max_wait_seconds: 1800
    on_expiry: cancel_run
  on_reject: stop_run
```

Смысл тут простой: подтверждение должно быть не галочкой в интерфейсе, а машиночитаемым рабочим контрактом. А если подтверждение влияет на выпуск, такой контракт должен еще и явно показывать, к какой версии набора и к какой идентичности выпуска относится человеческое решение.

!!! example "Контракт политики для цепочки дубля тикета"
    Для кейса разбора обращений поддержки контракт `create_ticket` должен требовать `idempotency_key` уже в запросе на подтверждение, а не только во время выполнения инструмента. Тогда человек, шлюз и трасса видят одно и то же намерение записи, набор политик может запретить повтор без сверки при `side_effect_unknown`, а проверка раскатки оценивает управляемую возможность, а не свободный вызов инструмента.

## Как набор политик связан с жизненным циклом

Из Части VIII здесь особенно важны две мысли:

- изменения политик — это значимые изменения выпуска;
- набор политик должен участвовать в управлении изменениями как полноценный артефакт.

То есть для команды полезно отвечать не только на вопрос:

«Какая политика у нас в принципе?»

Но и на вопрос:

«Какая именно версия набора политик была активна в момент этой раскатки или инцидента?»

А если среда выполнения уже обращается с наборами как с управляемыми поверхностями выпуска, неизбежно появляется и следующий вопрос:

«В формировании какой идентичности выпуска участвовал этот набор политик?»

## Как набор политик связан с трассами

Связь очень практическая:

- трасса показывает, какое решение политики реально сработало;
- набор политик показывает, откуда это решение взялось;
- контракт подтверждения показывает, как должен был выглядеть человеческий шлюз;
- идентичность выпуска показывает, к какой именно управляемой поверхности выпуска относилось это решение.

Без этой связки из четырех элементов расследование быстро превращается в угадайку.

## Что уже умеет эталонная среда исполнения

В `agent_runtime_ref` сейчас уже есть:

- [policy.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/policy.yaml)
- [approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- [controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/controls.yaml)
- [change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)

То есть пакет уже живет в модели, где политики, подтверждения и контракты управления средой выполнения не просто побочные настройки, а отдельные управляемые артефакты. Исполняемый шлюз `check-controls` делает набор средств управления тоже проверяемым: он возвращает `healthy`, `required_controls`, `blocked_findings_expected`, `missing_controls`, `failed_run_controls`, `preserved_failed_run_controls`, `failed_run_controls_healthy`, `support_duplicate_controls`, `preserved_support_duplicate_controls`, `support_duplicate_controls_healthy`, `blocking_findings` и `inventory_drift`, где вложенные поля `has_drift`, `missing_from_catalog` и `missing_from_inventory` отделяют отказы политик и средств управления от дрейфа каталога возможностей.

И здесь эта же среда явно фиксирует форму входного набора средств управления: проверка конфигурации средств управления сообщает `Controls policy config must be a mapping`, `'controls' must be a mapping`, `'controls.require' must be a list`, `'controls.block_if' must be a list`, `controls.require entries must be strings`, `controls.require entries must not be empty`, `controls.require entries must be unique`, `controls.block_if entries must be strings`, `controls.block_if entries must not be empty` и `controls.block_if entries must be unique`; переопределения сигналов сообщают `Assessment signals must be a mapping`, `Assessment signal key must be a string`, `Assessment signal key must not be empty`, `Assessment signal keys must be unique` и `Assessment signal value must be a boolean: {field}`. Поэтому оператор может отличить испорченный набор политик от провалившейся, но корректно сформированной оценки средств управления.

## Production extension: правила политики траектории

Проверка одного вызова не ловит ограничения, зависящие от всей
последовательности. Для таких случаев промышленную схему полезно расширить
декларативным разделом `trajectory_policy`. Ниже минимальная переносимая форма,
а не YAML-конфигурация, которую уже загружает `AgentRuntime`:

```yaml
trajectory_policy:
  policy_id: transfer-trajectory
  policy_version: 2026.08.23
  history_contract:
    source: trusted_immutable_snapshot
    expected_history_ref: required_on_request
    expected_history_version: required_on_request
    required_integrity: verified
    required_status: current
    request_snapshot_identity: [tenant_id, subject_id]
    snapshot_policy_identity: [policy_id, policy_version]
    on_absent_malformed_missing_corrupt_stale_or_unverified: deny
  request_fingerprint:
    algorithm: sha256_canonical_json
    include:
      - action
      - tenant_id
      - subject_id
      - expected_history_ref
      - expected_history_version
      - sequence_number
      - window_id
      - policy_id
      - policy_version
      - sorted_significant_fingerprints
      - sorted_counter_deltas
    caller_supplied_value_allowed: false
  numeric_contract:
    type: decimal
    minimum: "0"
    maximum: "999999999999.999999"
    maximum_scale: 6
    local_precision: 32
    trap_rounding_and_decimal_errors: true
    on_arithmetic_error: deny
  collection_contract:
    maximum_fingerprints_per_request_or_snapshot: 16
    maximum_counters_per_request_or_snapshot: 32
  rules:
    - kind: value_binding
      rule_id: destination-binding
      fingerprint_name: destination
    - kind: cumulative_limit
      rule_id: daily-amount-limit
      counter_name: amount
      limit: "100.00"
      window_id: from_request_and_snapshot
      required_window_state: open
    - kind: required_predecessor
      rule_id: destination-confirmed-first
      predecessor: confirm_destination
    - kind: required_approval
      rule_id: transfer-approval
      approval_scope: transfer
      bind_to: request_fingerprint
  decisions:
    - allow
    - deny
    - approval_required
```

Минимальные declarative rule kinds имеют узкий смысл:

- `value_binding` сравнивает fingerprint текущего поля с fingerprint того же
  поля в доверенной истории;
- `cumulative_limit` складывает сохранённый счётчик и текущую дельту только в
  совпадающем открытом окне с точной арифметикой из `numeric_contract`;
- `required_predecessor` требует именованный более ранний шаг в
  `observed_sequence`;
- `required_approval` ищет активную запись нужного `approval_scope`, связанную
  с текущим `request_fingerprint`.

`request_fingerprint` не является свободным полем request. Исполняемый контракт
канонически сериализует перечисленную identity запроса, сортирует fingerprints
и counter deltas по имени, нормализует Decimal без потери точности и вычисляет
SHA-256. Поэтому approval от прежних action, tenant/subject, history ref/version,
sequence, window или policy id/version не авторизует изменённый запрос.

Значения счётчиков принимаются только как конечные неотрицательные `Decimal` со
scale не более 6 и значением не более `999999999999.999999`. Сложение выполняется
в локальном `Decimal` context с precision 32 и traps для округления и
арифметических ошибок, поэтому поведение не зависит от глобального context.
Выход суммы за диапазон или иная arithmetic failure закрыто дают `deny` с
причиной `counter_arithmetic_error`; в telemetry попадает состояние
`arithmetic_error`, а не число.

Запрос и снимок истории содержат не более 16 отпечатков и 32 счётчиков каждый.
Эти границы проверяются при создании объектов и не позволяют формально
допустимому запросу переполнить строковые сводки обязательного события аудита.
Максимальные разрешённые наборы укладываются в лимит 8192 символов для каждого
поля телеметрии даже при несовпадающих именах в запросе и снимке.

Для `required_approval` binding проверяется до состояния записи. Любая
`rejected`, `revoked` или `expired` запись требуемого scope, связанная именно с
текущим `request_fingerprint`, закрыто даёт `deny` с причиной
`required_approval_inactive`, даже если рядом есть `approved`. Записи того же
scope для другого request не отменяют текущий binding: при отсутствии записи
для текущего fingerprint результатом будет `approval_required` с причиной
`approval_binding_mismatch`. Перед `allow` агрегированное `approval_state`
обязано согласовываться с однородным состоянием связанных записей; отсутствие
записей при агрегированном `approved`, смешанные `approved`/`pending` или иное
расхождение дают `deny` с причиной `approval_state_mismatch`.

Исполняемый учебный контракт в `agent_runtime_ref/trajectory.py` отражает эту
семантику frozen dataclasses, но намеренно не парсит приведённый YAML и не
подключён к `AgentRuntime`. `TrajectoryRequest` содержит `action`,
`tenant_id`, `subject_id`, `expected_history_ref`, `expected_history_version`,
`sequence_number`, `fingerprints`, `counters` и `window_id`. Доверенный
`TrajectorySnapshot` содержит как минимум `history_ref`, `history_version`,
`tenant_id`, `subject_id`, `policy_id`, `policy_version`, `integrity`, `status`,
`observed_sequence`, нормализованные `fingerprints`, `counters`, `window_id`,
`window_state`, `approval_records` и `approval_state`. Каждая запись
подтверждения хранит `approval_id`, `scope`, связанный с вычисленным запросом
`request_fingerprint` и `state`; сырые реквизиты и секреты в snapshot или
событие решения не входят.

Evaluator получает request и готовый snapshot явными аргументами. Он не читает
историю из model context, prompt, памяти модели или compaction summary. `None`
на публичной границе даёт `deny/history_missing`, а mapping или объект чужого
типа — `deny/history_malformed`; их содержимое не отражается в решении. Затем он
закрыто отклоняет missing, corrupt, stale и unverified history, несовпадение
history ref/version, request/snapshot identity, snapshot/policy identity, номера
последовательности или окна и детерминированно проверяет rules в объявленном
порядке. Результат несёт `policy_id`, `policy_version`,
`rule_id`, `reason`, `history_ref`, `history_version`, `sequence_summary`,
`sequence_ref`, `fingerprints`, `counters`, `window_id`, `window_state`,
`approval_state` и `decision`; точная форма события описана в
[схеме трасс](trace-schema.md).

Само значение `integrity: verified` является входным утверждением доверенного
поставщика snapshot. Production-контур обязан отдельно проверять подпись,
происхождение и актуальность, а также обеспечивать транзакционную фиксацию
версии, счётчиков, решения и внешнего эффекта. Учебная функция этого не делает.

Идентификаторы исполняемого контракта ограничены lowercase ASCII slug длиной до
64 символов; history references — lowercase URI-like значениями длиной до 256
символов без whitespace/control characters. Финальный строковый telemetry
payload также проверяется allowlist и лимитом длины. Это только structural
safeguard: доверенный provider обязан отдельно не допускать семантические
секреты внутри формально допустимых identifiers, references и hashes.

Валидация исполняемого контракта использует следующие стабильные сообщения:
`Trajectory field must be a string: {field}`,
`Trajectory field is required: {field}`,
`Trajectory identifier is invalid: {field}`,
`Trajectory reference is invalid: {field}`,
`Trajectory telemetry value is invalid: {field}`,
`Trajectory field must be an integer: {field}`,
`Trajectory integer must not be negative: {field}`,
`Trajectory integer must be positive: {field}`,
`Trajectory field is not supported: {field}={normalized}`,
`Trajectory fingerprint must be sha256: {field}`,
`Trajectory counter value must be a Decimal: {field}`,
`Trajectory counter value must be finite: {field}`,
`Trajectory counter value must not be negative: {field}`,
`Trajectory counter scale exceeds maximum: {field}`,
`Trajectory counter value exceeds maximum: {field}`,
`Trajectory {label} must be a tuple`,
`Trajectory {label} entries must be {item_type.__name__}`,
`Trajectory {label} must contain at most {maximum} entries`,
`Trajectory {label} names must be unique`,
`Trajectory approval record IDs must be unique`,
`Trajectory counter limit must be positive: {counter_name}`,
`Trajectory policy must contain at least one rule`,
`Trajectory rules entries must be trajectory rule objects`,
`Trajectory rule IDs must be unique`,
`Trajectory fingerprint request must be TrajectoryRequest`,
`Trajectory fingerprint policy must be TrajectoryPolicy`,
`Trajectory request must be TrajectoryRequest`,
`Trajectory policy must be TrajectoryPolicy`.

## Что должна добавить промышленная схема

Как только в среде выполнения появляются MCP с состоянием и возобновляемые сессии возможностей, набор политик уже должен описывать не только допустимость возможности “в принципе”, но и то, как управляется ее живой жизненный цикл сессии.

Здесь почти сразу становятся полезны такие поля:

- `trusted_verifier_contracts`
- `verifier_contract_required_for_high_risk`
- `on_untrusted_verifier_contract`
- `capability_session_mode`
- `resume_policy`
- `on_session_expiry`
- `progress_event_policy`
- `elicitation_policy`
- `reinit_requires_approval`
- `approval_mode`
- `approval_delegate`
- `classifier_verdict_policy`
- `escalate_to_human_if`
- `subagent_handoff_policy`
- `authorization_mode`
- `delegated_principal_policy`
- `token_reuse_policy`
- `on_authorization_revoke`
- `mcp_discovery_source`
- `mcp_server_owner`
- `mcp_auth_mode`
- `shadow_mcp_handling`

Именно они не дают ситуации, когда набор политик формально одобряет возможность, но оставляет ее реальный жизненный цикл сессии вне контроля.

Microsoft Foundry Open Trust Stack полезен здесь как внешний ориентир: политика должна компилироваться в именованные runtime checkpoints, а не оставаться prose рядом с eval report.[^microsoft-open-trust-stack] В переносимом YAML это может выглядеть так:

```yaml
control_checkpoints:
  - checkpoint: tool_execution
    policy_requirement: no_external_write_without_approval
    predicate: risk_tier == "high" and side_effect == "external_write"
    action: require_approval
    audit_fields:
      - checkpoint
      - policy_requirement
      - predicate_result
      - action
      - control_version
      - eval_case_id
      - trace_id
```

Минимальный contract surface: `checkpoint`, `policy_requirement`, `predicate` или `judge`, `action`, `control_version`, `eval_case_id`, `trace_id` и `observed_signal`. Checkpoints стоит называть по местам агентного цикла: `input`, `llm`, `state`, `tool_execution` и `output`. Тогда failed eval можно связать не только с prompt diff, но и с конкретным runtime hook, audit event и regression case.

Таксономия паттернов рабочих процессов у Anthropic добавляет сюда еще одно полезное контрактное измерение.[^anthropic] По мере взросления набор политик должен описывать не только то, разрешена ли возможность вообще, но и в каких схемах оркестрации она допустима.

Здесь быстро становятся полезны и такие поля, как:

- `allowed_orchestration_patterns`
- `disallowed_orchestration_patterns`
- `worker_inheritance_policy`
- `worker_capability_subset`
- `review_required_before_worker_write`

Именно они помогают управляемому контракту отвечать на вопросы:

- можно ли вызывать возможность внутри `prompt chaining`, `routing` или `parallelization`;
- наследуют ли делегированные исполнители в схеме `orchestrator-workers` контекст подтверждения или делегированной авторизации;
- может ли исполнитель запросить дополнительные возможности или работает только с ограниченным подмножеством;
- должен ли результат исполнителя пройти проверку до того, как будет выполнена любая записывающая возможность.

Заодно они помогают избежать и второго дрейфа: когда путь подтверждения с делегированием уже существует в поведении продукта, но все еще не представлен как управляемый контракт.

Как только система взрослеет, для набора политик почти сразу полезно добавить:

- `bundle_version`
- `artifact_lineage`
- `change_id`
- `release_identity`
- `approval_contracts`
- `runtime_control_schema`
- `sandbox_profile_contract`
- `sandbox_profile_review_required`
- `contract_version`
- `deprecated_rules`
- `redaction_policy`

Если возможность может выполняться через путь с песочницей, набор политик также должен ссылаться на контракт профиля песочницы или явно требовать его разбора, иначе рабочая область, права оболочки и файловой системы и поведение снимка/возобновления останутся вне идентичности выпуска.

Это превращает слой политик из набора файлов в полноценную поверхность выпуска.

## Почему набор политик и каталог возможностей нельзя разводить слишком далеко

Есть плохая крайность: набор политик живет отдельно, каталог возможностей отдельно, правила подтверждения отдельно, и между ними нет устойчивых ссылок.

Тогда быстро появляются проблемы:

- возможность есть в каталоге, но для нее нет контракта подтверждения;
- политика знает имя возможности, которой уже нет;
- аудит видит решение, но не может связать его с версией набора.

Поэтому практическое правило простое:

- каталог возможностей описывает, что система умеет;
- набор политик описывает, как, при каких условиях и в каких схемах оркестрации это можно использовать;
- контракт подтверждения описывает, где система обязана остановиться и уступить человеку;
- контракт авторизации описывает, от чьей идентичности и с какой делегированной областью действия вообще может быть выполнено действие;
- контракт управления MCP описывает, из какого утвержденного реестра пришла возможность, кто владеет MCP-сервером, каким режимом авторизации она защищена и что делать, если обнаружен теневой путь MCP;
- политика контрактов проверяющего описывает, каким контрактам проверяющего вообще можно доверять для оценивания высокого риска, доказательств раскатки и решений по заверению.

Эталонная среда исполнения делает этот стык конкретным в `capabilities.yaml` и `policy.yaml`: записи возможностей содержат `tool_principal`, `risk_tier`, `network_access`, `allowed_egress`, `timeout_seconds` и `idempotency_key_required`, а policy-записи содержат `run_precheck`, `require_tenant`, `deny_if_principal_missing`, решения по возможностям для `search_docs`, `create_ticket` и `run_shell`, записываемые в память `allow_kinds` (`validated_fact` и `session_summary`) и исполнительный уровень `allow_network_access`. И здесь загрузчик политик явно валидирует эту структуру: `Policy config must be a mapping`, `'policy' must be a mapping`, `'run_precheck' must be a mapping`, `'run_precheck.require_tenant' must be a boolean`, `'run_precheck.deny_if_principal_missing' must be a boolean`, `'{label}' must be a boolean`, `'memory_write' must be a mapping`, `'allow_kinds' must be a list`, `memory_write.allow_kinds entries must be strings`, `memory_write.allow_kinds entries must not be empty`, `memory_write.allow_kinds entries must be unique`, `'execution' must be a mapping`, `'allow_network_access' must be a list`, `execution.allow_network_access entries must be strings`, `execution.allow_network_access entries must not be empty`, `execution.allow_network_access entries must be unique`, `Policy capability names must be strings`, `Policy capability name must not be empty`, `Policy capability names must be unique`, `Policy capability entries must be CapabilityPolicy`, `Policy precheck request must be RunRequest`, `Policy context must be RunContext`, `Policy tool request must be ToolRequest`, `Policy capability must be CapabilitySpec`, `'capabilities' must be a mapping`, `Policy action must be a string`, `Policy action is not supported: {action}`, `Policy field must be a string: {field}`, `Policy field is required: {field}`, `Policy decision must be a string`, `Policy decision is not supported: {decision}`, `Policy approver must be a string`, `Policy approver must not be empty: {capability_name}`, `Policy memory kind must be a string`, `Policy memory kind must not be empty` и `Policy for capability {name!r} must be a mapping`.

## Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли версионированный набор политик?
- Можно ли связать его с раскаткой и разбором инцидента?
- Контракт подтверждения машиночитаем или только описан словами?
- Ясно ли, какие поля обязан содержать запрос на подтверждение?
- Есть ли связь между набором политик и каталогом возможностей?
- Можно ли понять, какая версия политики и какая идентичность выпуска были активны в момент трассы?
- Явно ли описано, каким контрактам проверяющего можно доверять для оценивания высокого риска или доказательств раскатки?

Если несколько ответов подряд «нет», значит слой политик у тебя пока существует, но еще не оформлен как полноценный рабочий артефакт.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Эталонный пакет](reference-package.md)
- [Шаблоны политик и проверочные списки по кейсам](policy-templates.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^microsoft-open-trust-stack]: Microsoft Foundry Blog, [Build agents you can trust across any framework with open evals and a control standard](https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/).
