# Шаблоны политик и проверочные списки по кейсам

Эта страница превращает кейсы из книги в стартовые заготовки для реальной работы.

Здесь нет идеи "вот универсальная политика на все случаи жизни". Наоборот: смысл в том, чтобы показать, как слой политик начинает отличаться в зависимости от сценария.

Если тебе сначала нужен живой контекст, начни с [практических кейсов](case-studies.md). Если нужен список следующих улучшений книги, смотри [дорожную карту для сообщества](community-roadmap.md).

## Как читать эти шаблоны

Смотри на них не как на готовый продовый YAML, а как на каркас:

- что система считает рискованным;
- где проходит граница подтверждения;
- как отделяются read и write actions;
- какие условия остановки и правила эскалации нужны;
- какие трассы и сигналы аудита стоит считать обязательными.

## Шаблон 1. Агент разбора обращений поддержки

### Что должна обеспечивать политика

Для разбора обращений поддержки тебе обычно нужно:

- безопасно читать customer context;
- не делать write actions без нужной уверенности;
- не отдавать модельный ответ "как будто все уже решено", если нужен человек;
- явно ограничить создание тикетов и чувствительные обновления.

### Пример каркаса политики

```yaml
agent:
  name: support_triage
  allowed_models: ["gpt-5.4", "gpt-5-mini"]
  max_steps: 12
  stop_conditions:
    - enough_information_to_answer
    - requires_human_review
    - write_requires_approval

tools:
  read_customer_profile:
    mode: read
    tenant_scoped: true
    approval: none

  read_ticket_history:
    mode: read
    tenant_scoped: true
    approval: none

  create_ticket:
    mode: write
    approval: manager
    idempotency_key_required: true
    retry_on: ["retryable_failure"]

output:
  require_structured_decision: true
  require_escalation_reason: true
```

### Проверочный список

- У read tools есть tenant scope?
- Agent умеет не только отвечать, но и честно эскалировать?
- `create_ticket` не вызывается без явного approval policy?
- В trace видно, почему был выбран write path?
- Есть ли stop condition на недостаточную уверенность?

## Шаблон 2. Внутренний агент знаний

### Что должна обеспечивать политика

В сценарии агента знаний главный риск не в побочных эффектах, а в доступе и качестве опоры на источники.

Тебе обычно нужно:

- разграничить доступ по роли;
- ограничить retrieval только допустимыми источниками;
- не давать агенту смешивать untrusted content с instructions;
- требовать source references в ответе.

### Пример каркаса политики

```yaml
agent:
  name: internal_knowledge
  allowed_models: ["gpt-5.4", "gpt-5-mini"]
  max_steps: 8
  stop_conditions:
    - answer_ready
    - insufficient_grounding
    - access_denied

retrieval:
  role_scoped: true
  tenant_scoped: true
  max_documents: 8
  require_source_labels: true

output:
  require_sources: true
  deny_if_no_grounding: true
  deny_sensitive_snippets_without_access: true
```

### Проверочный список

- Role-based filtering реально работает на retrieval path?
- Agent возвращает источники, а не только красивый текст?
- Есть ли policy на слабое grounding?
- Нельзя ли через retrieval вытащить чужой knowledge zone?
- Видно ли в traces, какие документы были реально использованы?

## Шаблон 3. Агент координации инцидентов

### Что должна обеспечивать политика

В incident-сценарии политика должна управлять не только доступом, но и orchestration discipline.

Обычно тебе нужно:

- держать единый trace на весь run;
- фиксировать ownership на handoffs;
- ограничивать risky remediation;
- не давать noisy input превращаться в лишние side effects.

### Пример каркаса политики

```yaml
agent:
  name: incident_coordinator
  allowed_models: ["gpt-5.4"]
  max_steps: 20
  orchestration:
    pattern: manager_with_controlled_handoffs
    require_handoff_reason: true
    require_current_owner: true

tools:
  create_incident_thread:
    mode: write
    approval: oncall_lead
    idempotency_key_required: true

  notify_team:
    mode: write
    approval: oncall_lead
    idempotency_key_required: true

  suggest_remediation:
    mode: advisory
    approval: none

  execute_remediation:
    mode: write
    approval: security_and_service_owner
    disabled_by_default: true

audit:
  require_trace_per_run: true
  require_handoff_log: true
  require_write_intent_log: true
```

### Проверочный список

- У каждого handoff есть owner и reason?
- Risky remediation не включена по умолчанию?
- Ticketing и notifications защищены idempotency?
- В incident trace видно полный путь принятия решений?
- Noisy alert не может сам по себе вызвать dangerous write path?

## Универсальный проверочный список для слоя политик

Независимо от кейса, полезно пройти по этим вопросам:

- Понимаешь ли ты, где в системе `read`, `write` и `advisory` действия?
- Есть ли у risky actions отдельный approval boundary?
- Видно ли в policy, где агент должен остановиться, а не продолжать reasoning?
- Не живут ли ключевые правила только внутри prompt?
- Может ли security-команда прочитать policy artifacts без знания всех деталей prompt engineering?

Если ответ "нет" на несколько пунктов подряд, значит policy layer у тебя еще слишком неявный.

## Куда идти дальше

- [Практические кейсы](case-studies.md)
- [Глава 3. Контур безопасности и границы доверия](../book/part-ii/chapter-3.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
