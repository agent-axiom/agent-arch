# Глава 17. Слой политик и каталог возможностей

!!! info "Как читать эту главу"
    Полезно держать в голове не абстрактную тему “policy layer”, а очень практичную задачу:

    - кто решает, можно ли тому же support-агенту вообще запустить этот run;
    - кто определяет, можно ли читать контекст, открывать тикет или писать в память;
    - где эти решения должны жить, чтобы они не расползлись по orchestration code.

    Если ответы на эти вопросы спрятаны в случайных ветках кода, runtime уже собран, но contract core системы все еще отсутствует.

## 1. Почему без слоя политик справочный рантайм остается слишком наивным

Даже если у тебя уже есть аккуратный цикл рантайма, этого все равно недостаточно. Без явного слоя политик система остается слишком доверчивой:

В нашем сквозном support-кейсе это проявляется сразу после главы 16. Runtime уже умеет принять запрос, собрать контекст, вызвать модель и дойти до gateway. Но в момент, когда агент собирается открыть срочный тикет, записать сводку в память или запросить еще один внешний шаг, системе нужен не просто loop, а явное решение о допустимости и риске.

- нельзя надежно отличить допустимый run от недопустимого;
- вызовы инструментов трудно контролировать одинаково;
- записи в память живут на отдельных договоренностях;
- продуктовые ограничения быстро просачиваются в код оркестрации.

Поэтому следующий обязательный слой справочной реализации - слой политик.

Его задача не в том, чтобы “тормозить систему”. Его задача в том, чтобы решения про доступ, риск и допустимость не были размазаны по случайным `if` в коде.

!!! info "Нужен контрактный слой?"
    Для более прикладной формы открой [схему policy bundle и approval contract](../../appendix/policy-bundle-schema.md), [схему approval request и decision record](../../appendix/approval-schema.md) и [справочный пакет](../../appendix/reference-package.md).

## 2. Слой политик должен отвечать на маленькие и понятные вопросы

Слабый слой политик пытается быть “умным мозгом системы”. Сильный слой политик делает наоборот: он решает ограниченный набор ясных вопросов.

Например:

- можно ли запускать этот run вообще;
- можно ли читать этот контекст;
- можно ли вызывать эту capability;
- нужен ли approval;
- можно ли записывать это в память;
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

Практически полезный набор полей обычно такой:

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

Это скучный слой. И это хорошо. Catalog layer как раз и должен быть стабильным и обозримым.

## 10. Частые ошибки

Проблемы здесь очень типовые:

- policy rules размазаны по runtime;
- capability contract неполный;
- ownership capability неясен;
- approval logic вшита прямо в orchestration;
- memory policy и execution policy живут как будто отдельно;
- catalog и real adapters расходятся по поведению.

Когда это происходит, справочная реализация перестает быть опорой и снова превращается в связку договоренностей.

## 11. Быстрый тест зрелости для policy layer и capability catalog

Команде не стоит думать, что она уже собрала contract core своей agent system, только потому, что у нее есть несколько policy checks и список tools.

Более сильная планка такая:

- policy decisions существуют как явные объекты, а не как размазанные booleans;
- capability contracts несут ownership, transport, risk и approval semantics;
- runtime code зависит от catalog, а не от direct calls и ad hoc exceptions;
- memory policy, execution policy и approval policy принадлежат одному видимому control surface;
- telemetry умеет показать не только что произошло, но и какой policy и capability contract этим управлял.

Если большинство этих условий не выполняется, runtime уже может существовать, но contract core у системы пока не собран.

## 12. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли у тебя отдельный policy layer, а не набор `if` по коду?
- Возвращает ли policy structured decision?
- Есть ли единый capability catalog?
- Есть ли у capabilities owner, transport и risk semantics?
- Использует ли runtime catalog, а не прямые вызовы?
- Видны ли policy decisions в telemetry?

Если на несколько вопросов подряд ответ “нет”, skeleton у тебя уже есть, но contract core пока еще не собран.

## 13. Что делать дальше

Сначала сделай policy decisions и capability contracts явными, а потом проверь, готова ли эта же система к первому rollout.

Следующий логичный шаг в опорной реализации - собрать production rollout checklist, чтобы из blueprint и contract core выйти в практический go-live framework.

- [Глава 16. Базовая схема рантайма](chapter-16.md)
- [Глава 18. Чеклист промышленного запуска](chapter-18.md)
- [Часть VII. Эталонная реализация](index.md)
- [Источники](../../appendix/sources.md)

## 14. Полезные справочные страницы

- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)
- [Справочный пакет](../../appendix/reference-package.md)

- [Глава 16. Базовая схема рантайма](chapter-16.md)
- [Глава 18. Чеклист промышленного запуска](chapter-18.md)
- [Часть VII. Эталонная реализация](index.md)
- [Источники](../../appendix/sources.md)
