# Глава 9. Sandbox execution и MCP как контракт интеграции

## 1. Почему execution layer без sandbox быстро становится слишком доверчивым

Когда у агента появляется доступ к инструментам, следующая опасность почти всегда одна и та же: system boundary начинает размываться.

Агент уже умеет:

- читать данные;
- запускать операции;
- обращаться к внешним сервисам;
- получать ответы из непредсказуемой среды.

Если все это исполняется “как есть”, без изоляции и контрактов, платформа очень быстро получает проблемы:

- tool может вернуть недоверенный payload в неожиданном формате;
- интеграция может зависнуть или выйти за пределы ресурса;
- side effect может произойти вне ожидаемого policy path;
- один плохо спроектированный adapter может утащить за собой весь runtime.

Именно поэтому execution layer почти всегда нужен не только как router, но и как sandbox boundary.

## 2. Sandbox это не обязательно контейнер, а прежде всего режим ограничений

Когда говорят “sandbox”, многие сразу думают о Docker, VM или отдельном процессе. Это возможные реализации, но архитектурно важнее другое: sandbox задает пределы того, что может сделать capability.

Хороший sandbox обычно ограничивает:

- доступ к сети;
- доступ к файловой системе;
- доступ к секретам;
- CPU и memory budget;
- allowed syscalls или execution mode;
- время жизни операции.

То есть sandbox отвечает на вопрос: “Что произойдет, если tool или adapter поведет себя хуже, чем мы ожидали?”

Это не только безопасность. Это еще и контроль blast radius.

## 3. Нельзя считать внешнюю интеграцию просто функцией

Обычная ошибка выглядит так: внешний сервис оборачивается в функцию, и дальше агент видит его как обычный вызов.

Но реальная интеграция почти всегда:

- нестабильнее локального кода;
- хуже типизирована;
- зависит от прав доступа и окружения;
- может вернуть частичный или опасный результат;
- имеет собственные latency и rate limits.

Поэтому полезнее относиться к интеграциям как к capability endpoints с контрактом, а не как к “удобным helper methods”.

## 4. MCP полезен именно как контрактный слой

MCP удобен не потому, что это модное слово, а потому что он помогает явно описать границу между агентом и внешней capability.

В хорошем дизайне MCP дает несколько полезных вещей:

- стандартизированный способ описывать tools и resources;
- отдельный server boundary;
- более явный lifecycle для подключения capability;
- возможность держать adapters вне основного agent runtime;
- понятную точку для policy checks, logging и isolation.

Это особенно полезно, когда у тебя не один agent runtime и не одна интеграция, а набор capabilities, которые хочется подключать системно, а не хаотично.

<div class="diagram-card">
<p>MCP удобен как слой контракта между runtime и внешними capability</p>

``` mermaid
flowchart LR
    A["Agent runtime"] --> B["Execution layer"]
    B --> C["Policy and validation"]
    C --> D["MCP client"]
    D --> E["MCP server"]
    E --> F["Typed adapter"]
    F --> G["External API / system"]
    G --> F
    F --> E
    E --> D
    D --> B
```

</div>

## 5. Зачем выносить adapters из core runtime

Это дает сразу несколько выгод:

- сбои в интеграции меньше влияют на центральный runtime;
- проще ограничить сеть, секреты и filesystem per capability;
- легче обновлять или заменять адаптер без переписывания orchestration layer;
- contracts становятся более явными;
- проще тестировать capability отдельно от логики агента.

Это особенно ценно, когда одни инструменты работают только на чтение, другие пишут во внешние системы, а третьи вообще выполняют код или shell-команды.

## 6. Не все capability требуют одинаковый уровень изоляции

Удобно разделить интеграции хотя бы на три класса:

- low-risk read capabilities;
- medium-risk business actions;
- high-risk execution capabilities.

Примеры:

- `read_kb` или `search_docs` можно исполнять мягче;
- `create_ticket` или `update_crm_record` требуют stricter policy и audit;
- `run_shell`, `exec_sql`, `deploy_job` требуют самого жесткого sandbox и approval.

Если ко всем инструментам применить одинаково мягкий execution profile, платформа будет либо небезопасной, либо очень быстро столкнется с инцидентами по side effects.

## 7. Контракт capability должен включать не только input/output

Часто schema инструмента описана неплохо, а вот operational contract нигде не зафиксирован. Но именно он часто критичен.

Полезно явно задавать:

- read или write nature;
- network policy;
- secret scope;
- allowed environments;
- timeout budget;
- retry policy;
- approval requirement;
- logging and redaction rules.

Ниже пример такого профиля:

```yaml
capabilities:
  search_docs:
    transport: mcp
    mode: read
    network: internal_only
    secrets: none
    timeout_seconds: 8
    approval: none
  create_ticket:
    transport: mcp
    mode: write
    network: internal_only
    secrets: service_account_helpdesk
    timeout_seconds: 15
    approval: manager_for_high_priority
  run_shell:
    transport: sandboxed_exec
    mode: high_risk
    network: denied
    filesystem: workspace_only
    secrets: none
    timeout_seconds: 10
    approval: always
```

Это уже не просто описание функции. Это описание поведенческого контракта capability.

## 8. Sandbox execution должен возвращать не только output, но и execution facts

Если sandbox возвращает только stdout или payload, ты теряешь половину ценности слоя изоляции.

Для расследования и управления полезно возвращать:

- exit status;
- timeout flag;
- resource usage summary;
- side effect uncertainty;
- redacted logs;
- policy decision id.

Тогда execution layer может объяснить не просто “команда не сработала”, а более взрослое: “операция была прервана по timeout после 8 секунд, сеть была запрещена, side effect не подтвержден”.

## 9. Простой кодовый пример capability dispatch

Ниже каркас, который показывает саму идею: transport и execution profile выбираются по capability contract, а не определяются логикой модели на лету.

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    transport: str
    mode: str
    timeout_seconds: int


def dispatch_capability(spec: CapabilitySpec, args: dict) -> dict:
    if spec.transport == "mcp":
        return {"status": "success", "transport": "mcp", "capability": spec.name}
    if spec.transport == "sandboxed_exec" and spec.mode == "high_risk":
        return {"status": "approval_required", "capability": spec.name}
    return {"status": "validation_failure", "reason": "unsupported capability profile"}
```

Это простой пример, но он закрепляет правильную мысль: способ исполнения задается платформой, а не придумывается моделью каждый раз заново.

## 10. Что чаще всего ломается в sandbox и capability layer

Типовые проблемы очень повторяемы:

- capability получает больше network access, чем нужно;
- secrets доступны слишком широкому набору adapters;
- tool result тащит сырые внешние payloads в prompt;
- timeout есть, но side effect uncertainty не моделируется;
- MCP server добавили, но policy и audit туда не дотянули;
- sandbox есть формально, но не ограничивает ничего важного.

Именно поэтому sandbox не должен быть checkbox-функцией. Он должен быть частью execution design.

## 11. Practical checklist

Если хочешь быстро проверить capability layer, пройди по вопросам:

- Отделены ли adapters от core runtime?
- Есть ли per-capability execution profile?
- Ограничены ли network, filesystem и secrets?
- Явно ли описан transport: direct, MCP, sandboxed exec?
- Понимает ли система, когда result trustworthy, а когда только partially trusted?
- Есть ли execution facts помимо business payload?
- Можно ли объяснить, почему capability была разрешена именно в этом run?

Если ответы расплывчаты, capability layer у тебя пока больше похож на набор удобных интеграций, чем на управляемую платформу.

## 12. Что читать дальше

Следующая естественная тема в этой части: idempotency, retries, rate limits и rollback boundaries. После sandbox и capability contracts именно она превращает execution model в production-grade слой.

- [Глава 8. Execution model и каталог инструментов](chapter-8.md)
- [Часть IV. Инструменты и выполнение](index.md)
- [Источники](../../appendix/sources.md)
