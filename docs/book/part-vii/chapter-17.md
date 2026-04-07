# Глава 17. Слой политик и каталог возможностей

## 1. Почему без слоя политик эталонный рантайм остается слишком наивным

Даже если у тебя уже есть аккуратный runtime loop, этого все равно недостаточно. Без явного policy layer система остается слишком доверчивой:

- нельзя надежно отличить допустимый run от недопустимого;
- tool calls трудно контролировать одинаково;
- memory writes живут на отдельных договоренностях;
- product-specific ограничения быстро просачиваются в orchestration code.

Поэтому следующий обязательный слой reference implementation это policy layer.

Его задача не в том, чтобы “тормозить систему”. Его задача в том, чтобы решения про доступ, риск и допустимость не были размазаны по случайным `if` в коде.

## 2. Policy layer должен отвечать на маленькие и понятные вопросы

Слабый policy layer пытается быть “умным мозгом системы”. Сильный policy layer делает наоборот: он решает ограниченный набор ясных вопросов.

Например:

- можно ли запускать этот run вообще;
- можно ли читать этот контекст;
- можно ли вызывать этот capability;
- нужен ли approval;
- можно ли записывать это в memory;
- можно ли вернуть этот результат наружу.

Когда эти вопросы оформлены явно, runtime становится объяснимее, а изменения в guardrails перестают быть хаотичными.

## 3. Capability catalog нужен не как реестр имен, а как контрактный слой

Очень легко скатиться к каталогу, который просто хранит список доступных tools. Но хороший catalog делает больше:

- описывает capability contract;
- хранит risk profile;
- указывает transport и execution mode;
- задает idempotency expectations;
- фиксирует ownership и lifecycle.

То есть capability catalog это не “inventory для удобства”, а центральная точка управления способностями платформы.

<div class="diagram-card">
<p>Слой политик и каталог возможностей вместе образуют договорное ядро эталонной реализации</p>

``` mermaid
flowchart LR
    A["Run request"] --> B["Runtime orchestrator"]
    B --> C["Policy layer"]
    B --> D["Capability catalog"]
    C --> E["Allow / deny / approve"]
    D --> F["Capability contract"]
    E --> G["Execution layer"]
    F --> G
```

</div>

## 4. Что полезно хранить в capability catalog

Практически useful набор полей обычно такой:

- capability name;
- owner;
- mode: read / write / high_risk;
- transport: mcp / gateway / sandboxed_exec;
- input schema;
- output shape;
- approval requirement;
- idempotency requirement;
- timeout and retry defaults.

С таким контрактом runtime уже может вести себя предсказуемо, а не подстраиваться под каждый capability ad hoc.

## 5. Policy decision должен быть объектом, а не просто bool

Очень полезная инженерная привычка: policy decision не должен сводиться к `True/False`.

Чаще полезнее возвращать что-то вроде:

- `allow`
- `deny`
- `approval_required`
- `sanitize_and_continue`
- `escalate`

И дополнительно:

- reason code;
- policy id;
- risk class;
- optional constraints.

Это резко повышает explainability и делает telemetry намного полезнее.

## 6. Пример policy contract

Ниже очень простой, но практичный шаблон:

```yaml
policy:
  run_precheck:
    require_tenant: true
    deny_if_principal_missing: true
  capabilities:
    search_docs:
      decision: allow
    create_ticket:
      decision: approval_required
      approver: manager
    run_shell:
      decision: deny
  memory_write:
    allow_kinds:
      - validated_fact
      - session_summary
```

Его сила не в полноте, а в явности. Ты можешь спорить с конкретным правилом и понимать, где оно применяется.

## 7. Пример capability catalog contract

Catalog полезно мыслить примерно так:

```yaml
capabilities:
  search_docs:
    owner: knowledge_platform
    mode: read
    transport: mcp
    timeout_seconds: 5
    approval: none
  create_ticket:
    owner: support_platform
    mode: write
    transport: gateway
    timeout_seconds: 15
    approval: manager
    idempotency_key_required: true
  run_shell:
    owner: platform_runtime
    mode: high_risk
    transport: sandboxed_exec
    timeout_seconds: 10
    approval: always
```

Такой catalog уже задает operational semantics, а не просто список имен.

## 8. Простой кодовый каркас policy decision

Ниже каркас, который показывает, что runtime получает не просто разрешение, а структурированное решение.

```python
from dataclasses import dataclass


@dataclass
class PolicyDecision:
    action: str
    reason: str
    policy_id: str


def evaluate_capability(name: str) -> PolicyDecision:
    if name == "search_docs":
        return PolicyDecision(action="allow", reason="low_risk_read", policy_id="cap_001")
    if name == "create_ticket":
        return PolicyDecision(action="approval_required", reason="write_action", policy_id="cap_014")
    return PolicyDecision(action="deny", reason="unsupported_capability", policy_id="cap_999")
```

Даже такой простой код уже задает правильную форму для telemetry, UI approval flows и расследований.

## 9. Простой кодовый каркас capability lookup

И еще один практичный кусок: runtime не должен знать capability details напрямую, он должен вытаскивать их из catalog.

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    mode: str
    transport: str
    timeout_seconds: int


def get_capability(name: str) -> CapabilitySpec | None:
    registry = {
        "search_docs": CapabilitySpec("search_docs", "read", "mcp", 5),
        "create_ticket": CapabilitySpec("create_ticket", "write", "gateway", 15),
    }
    return registry.get(name)
```

Это тоже выглядит скучно. И это отлично. Catalog layer как раз и должен быть скучным, стабильным и обозримым.

## 10. Где policy и catalog чаще всего ломаются

Проблемы здесь очень типовые:

- policy rules размазаны по runtime;
- capability contract неполный;
- ownership capability неясен;
- approval logic вшита прямо в orchestration;
- memory policy и execution policy живут как будто отдельно;
- catalog и real adapters расходятся по поведению.

Когда это происходит, reference implementation перестает быть reference и снова превращается в связку договоренностей.

## 11. Практический чеклист

Если хочешь быстро проверить этот слой, пройди по вопросам:

- Есть ли у тебя отдельный policy layer, а не набор `if` по коду?
- Возвращает ли policy structured decision?
- Есть ли единый capability catalog?
- Есть ли у capabilities owner, transport и risk semantics?
- Использует ли runtime catalog, а не прямые вызовы?
- Видны ли policy decisions в telemetry?

Если на несколько вопросов подряд ответ “нет”, skeleton у тебя уже есть, но contract core пока еще не собран.

## 12. Что читать дальше

Следующий логичный шаг в reference implementation: собрать production rollout checklist, чтобы из blueprint и contract core выйти в практический go-live framework.

## 13. Полезные справочные страницы

- [Схема policy bundle и approval contract](../../appendix/policy-bundle-schema.md)
- [Схема lifecycle-артефактов](../../appendix/lifecycle-artifact-schema.md)
- [Опорный пакет](../../appendix/reference-package.md)

- [Глава 16. Базовая схема рантайма](chapter-16.md)
- [Глава 18. Чеклист промышленного запуска](chapter-18.md)
- [Часть VII. Эталонная реализация](index.md)
- [Источники](../../appendix/sources.md)
