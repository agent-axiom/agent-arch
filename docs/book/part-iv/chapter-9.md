# Глава 9. Песочница выполнения и MCP как интеграционный контракт

!!! info "Как читать эту главу"
    Здесь полезно держать в голове один конкретный переход:

    - агент уже выбрал capability;
    - агент уже собирается пойти во внешний tool или adapter;
    - платформа должна решить, через какой transport это вообще может быть исполнено и в каких границах.

    Если этот переход не оформлен явно, sandbox и MCP быстро превращаются в набор слов, а не в рабочую execution discipline.

## 1. Почему слой выполнения без песочницы быстро становится слишком доверчивым

В нашем сквозном support-кейсе это выглядит очень приземленно: агент уже решил проверить статус заявки или создать тикет через внешнюю систему. С этого момента вопрос стоит уже не “какой следующий умный шаг”, а “через какой boundary система вообще разрешит этот шаг выполнить”.

Когда у агента появляется доступ к инструментам, следующая опасность почти всегда одна и та же: системная граница начинает размываться.

Агент уже умеет:

- читать данные;
- запускать операции;
- обращаться к внешним сервисам;
- получать ответы из непредсказуемой среды.

Если все это исполняется “как есть”, без изоляции и контрактов, платформа очень быстро получает проблемы:

- инструмент может вернуть недоверенный payload в неожиданном формате;
- интеграция может зависнуть или выйти за пределы ресурса;
- побочный эффект может произойти вне ожидаемого policy path;
- один плохо спроектированный адаптер может утащить за собой весь рантайм.

Именно поэтому слой выполнения почти всегда нужен не только как router, но и как sandbox boundary.

## 2. Sandbox это не обязательно контейнер, а прежде всего режим ограничений

Когда говорят “sandbox”, многие сразу думают о Docker, VM или отдельном процессе. Это возможные реализации, но архитектурно важнее другое: песочница задает пределы того, что может сделать capability.

Хороший sandbox обычно ограничивает:

- доступ к сети;
- доступ к файловой системе;
- доступ к секретам;
- CPU и memory budget;
- allowed syscalls или execution mode;
- время жизни операции.

То есть песочница отвечает на вопрос: “Что произойдет, если tool или adapter поведет себя хуже, чем мы ожидали?”

Это не только безопасность. Это еще и контроль blast radius.

### 2.1. Полезно различать уровни изоляции

На практике слово `sandbox` часто скрывает сразу несколько разных уровней.

- `logical isolation`: policy checks, capability contracts, allowlists;
- `process isolation`: отдельный процесс, timeout, resource limits;
- `runtime isolation`: отдельное исполняемое окружение, урезанный filesystem, ограниченный network egress, секреты по минимуму.

Это важно, потому что многие команды считают, что у них “есть sandbox”, хотя на деле у них есть только первый уровень. Для low-risk reads этого иногда хватает, но для high-risk execution почти всегда нужна более жесткая граница исполнения.[^google-sandbox]

Хороший practical question здесь такой: **если capability начнет вести себя хуже нормы, что именно ее остановит: логика, процесс или сама среда исполнения?**

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

## 4.1. Полезно не путать MCP host, client и server

Вокруг MCP часто возникает лишняя путаница, потому что слова кажутся знакомыми, а роли у них довольно конкретные.

Полезно держать в голове такую картину:

- `host` - это приложение или runtime, который управляет сессией и решает, к каким capability вообще подключаться;
- `client` - это протокольный компонент, который host создает для связи с конкретным MCP server;
- `server` - это boundary, который публикует tools, resources и другие capability surfaces, а затем возвращает структурированный результат.

Из этого следуют две очень практичные вещи:

- один host может одновременно держать несколько clients;
- один agent runtime может работать сразу с несколькими MCP servers, не смешивая их в один неразличимый integration blob.

Это кажется терминологической мелочью, но она полезна. MCP client - это не пользовательский интерфейс и не "сам агент". Это транспортный и контрактный слой между host и конкретным server boundary.

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

Как только MCP перестает быть одной-двумя вручную подключенными интеграциями, возникает следующий вопрос: **кто вообще управляет MCP-поверхностью как частью платформы, а не как набором локальных удобств разработчиков?** Здесь полезен недавний материал Cloudflare, потому что он смещает акцент с “умеет ли агент говорить по MCP” на “как команда открывает, утверждает, маршрутизирует и аудирует MCP endpoints в масштабе”.[^cloudflare-mcp]

Обычно это довольно быстро ведет к явному MCP control plane:

- local ad hoc MCP servers для экспериментов;
- governed remote MCP servers для общих production-capabilities;
- discovery или portal layer для approved servers;
- identity enforcement на границе доступа;
- audit и DLP controls вокруг самого MCP path.

Это дает сразу несколько выгод:

- сбои в интеграции меньше влияют на центральный runtime;
- проще ограничить сеть, секреты и filesystem per capability;
- легче обновлять или заменять адаптер без переписывания orchestration layer;
- contracts становятся более явными;
- проще тестировать capability отдельно от логики агента.

Это особенно ценно, когда одни инструменты работают только на чтение, другие пишут во внешние системы, а третьи вообще выполняют код или shell-команды.

### 5.1. Enterprise MCP почти всегда требует control plane, а не только protocol

Именно здесь многие команды повторяют одну и ту же maturity mistake. Они стандартизируют protocol, но продолжают подключать MCP servers неформально: кто-то кидает endpoint в чат, кто-то копирует его в локальный config, и очень быстро уже нельзя ответить, какие MCP servers вообще approved, какие только экспериментальные, а какие тихо обходят normal review.

Более зрелая модель относится к remote MCP как к части platform control plane:

- платформа публикует approved MCP endpoints через registry или portal;
- owner каждой capability обозначен явно;
- authentication проходит через общий identity layer, а не прячется внутри каждого desktop client;
- policy и DLP checks могут наблюдать MCP traffic как управляемую поверхность;
- retirement MCP endpoint оформляется как обычное lifecycle event.

Как только identity становится центральной частью этой модели, появляется еще один важный вопрос: **кто именно авторизует MCP action и в чьем user context это происходит?** Managed OAuth boundary полезна здесь тем, что не дает каждому MCP server придумывать свою ad hoc credential story.

Обычно это означает следующее:

- user delegation выдается через governed identity layer;
- tokens короткоживущие и привязаны к конкретному principal;
- MCP server получает scoped access вместо широких постоянных секретов;
- платформа может revoke или rotate доступ без переписывания каждого adapter.

Эта же модель помогает понять, где **local MCP** все еще уместен: прототипирование, изолированные эксперименты или очень узкие team-local workflows. Но default для shared business capabilities обычно должен быть таким: **remote, governed, discoverable, auditable**.

### 5.2. Shadow MCP это новая версия shadow API problem

Когда MCP становится слишком легко подключать, у команды появляется новый вариант shadow IT: неучтенные MCP servers, через которые уже проходят реальные business actions, но ownership, review и control model у них остаются неоформленными.[^cloudflare-mcp]

У этого anti-pattern обычно быстро видны характерные признаки:

- capability потребляется из приватного config snippet, а не из approved catalog;
- никто не может назвать owner MCP server;
- auth живет в long-lived local secrets;
- нет общего audit trail, показывающего, какой agent использовал какой MCP endpoint;
- platform team узнает о сервере уже после инцидента.

Полезный platform checklist здесь очень простой:

- Этот MCP server есть в approved registry?
- Кто отвечает за его lifecycle и incident response?
- Какая identity boundary защищает доступ?
- Какой policy bundle управляет write actions и approvals?
- Какая telemetry доказывает, какой agent вызывал endpoint и в каком decision context?

Если на эти вопросы нет ответа, проблема уже не в том, что “интеграция плохо документирована”. Проблема в том, что платформа создала shadow capability path вне собственной модели управления.

Следующий хороший вопрос здесь такой: **может ли платформа восстановить authorization chain для этого MCP action?** В зрелой модели оператор должен уметь восстановить:

- какой user или service principal делегировал доступ;
- какой identity layer выпустил или проброкерил token;
- какой MCP server принял этот delegated scope;
- какой agent run использовал эту авторизацию для выполнения действия.

Если эта цепочка не восстанавливается, auditability у платформы слабее, чем кажется по одному protocol surface.

### 5.3. Ephemeral sandboxes лучше постоянных сред почти во всем

Еще одна полезная мысль из Google: для рискованных capability очень выгодно проектировать краткоживущие execution environments.[^google-sandbox]

Почему это обычно лучше:

- меньше шансов, что состояние протечет между runs;
- проще ограничивать lifetime секретов и временных файлов;
- легче объяснить cleanup после выполнения;
- ниже риск, что один грязный adapter испортит следующую задачу.

Постоянные воркеры иногда выигрывают по latency, но почти всегда проигрывают по изоляции и объяснимости. Поэтому default stance для high-risk execution обычно должна быть такой: **ephemeral first, persistence only by explicit need**.

## 6. Stateful MCP меняет то, что runtime вообще обязан отслеживать

Еще один полезный свежий сигнал дает AWS: как только MCP clients и servers начинают поддерживать stateful interaction patterns, MCP перестает быть просто stateless tool envelope и начинает вести себя как sessioned runtime protocol.[^aws-stateful-mcp]

Это меняет execution contract сразу в нескольких практических местах:

- runtime уже может хранить не только user run, но и отдельный `session_id` для MCP interaction;
- capability может присылать progress notifications до финального результата;
- server может запросить elicitation или дополнительный user input посередине flow;
- expiry и re-initialization становятся нормальной частью lifecycle, а не редким edge case;
- telemetry должна уметь объяснить не только, какой tool был вызван, но и какая MCP session instance несла этот шаг.

Если платформа продолжает считать MCP полностью stateless и после появления таких паттернов, то pause/resume logic, approval routing и trace reconstruction быстро становятся намного сложнее, чем должны быть.

### 6.1. Stateless MCP и Stateful MCP требуют разных контрактов

Полезное различие здесь очень простое:

- `stateless MCP`: один request, один response, почти без session continuity;
- `stateful MCP`: ограниченная interaction session с progress, промежуточными запросами и возможностью resume или re-init.

Вторая модель почти всегда требует от платформы большего:

- ownership session lifecycle;
- правила обработки expiry;
- resumability rules;
- telemetry для progress и elicitation events;
- policy fields, которые фиксируют, можно ли resumed session продолжать автоматически или нужно повторное approval.

Это не делает stateless MCP устаревшим. Это лишь означает, что платформа не должна притворяться, будто оба режима operationally одинаковы.

### 6.2. Progress, elicitation и expiry - это runtime events, а не транспортные мелочи

Полезный operational lesson из AWS stateful MCP direction состоит в том, что сложность не заканчивается на хранении session handle.[^aws-stateful-mcp] Более трудный вопрос в том, как runtime должен реагировать, когда capability шлет progress, запрашивает дополнительный input или истекает до завершения работы.

Это почти всегда заставляет платформу явно определить поведение хотя бы для четырех случаев:

- `progress_update`: capability все еще работает, и runtime должен показать liveness, не считая вызов зависшим;
- `elicitation_requested`: capability не может продолжить, пока user или operator не даст дополнительный input;
- `session_expired`: прежнюю capability session уже нельзя безопасно resume;
- `reinitialized_session`: runtime осознанно поднял новую capability session, но связал ее с тем же user-visible run.

Это не мелкие transport details. Именно они формируют, как дальше ведут себя approval, telemetry и operator response.

### 6.3. Хороший MCP contract должен объяснять, что происходит после interruption

Если stateful capability ставится на паузу посередине flow, платформа не должна импровизировать recovery logic на месте.

Полезно явно зафиксировать хотя бы такие правила:

- может ли та же capability session продолжиться после human approval;
- приводит ли expiry к cancel run или к re-initialization;
- требует ли следующий шаг fresh policy evaluation;
- сохраняет ли runtime тот же user-visible run, если capability-side session была заменена;
- как telemetry связывает старую и новую capability sessions при расследовании.

Без этих ответов команда может формально поддерживать stateful MCP, но все равно не сумеет объяснить, что реально произошло после interruption.

## 7. Не все capability требуют одинаковый уровень изоляции

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

- режим authentication;
- platform-owned это доступ или user-delegated;
- время жизни token и правила renewal;
- scope boundaries per capability;
- что именно логируется про delegated authorization;
- что происходит, если delegated access отзывают посередине session.

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
    session_mode: stateful
    progress_events: true
    elicitation: manager_or_requester
    on_session_expiry: reinitialize_or_cancel
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

### 8.1. Network egress deserves its own rule set

Очень много инцидентов происходит не потому, что capability “сломалась”, а потому, что она смогла уйти в неожиданное место.

Поэтому network egress полезно описывать не как частность sandbox, а как отдельный contract surface:

- `denied`;
- `internal_only`;
- `allowlisted_external`;
- `brokered_via_gateway`.

Если это не зафиксировано явно, потом почти невозможно объяснить, почему конкретный tool внезапно сходил наружу, хотя формально “ничего не нарушал”.

Для production-grade платформы хороший default обычно такой:

- read-only internal tools: `internal_only`;
- external API adapters: `allowlisted_external`;
- code execution и shell-like tools: `denied` по умолчанию.

### 8.2. Sandbox manifest как контракт исполнения

Свежие документы OpenAI по Sandbox Agents добавляют к этой картине полезную практическую форму: sandbox стоит описывать не только словами “контейнер” или “изолированная среда”, а через явный `Manifest`, capabilities, permissions, workspace entries, snapshot и session state.[^openai-sandbox-agents]

Это хорошо ложится на execution contracts из этой главы. Для платформы важны как минимум четыре вопроса:

- какие файлы, репозитории, mounts и environment попадают в стартовый workspace;
- какие sandbox-native capabilities доступны: filesystem, shell, memory, skills, compaction;
- какие permissions и `run_as` действуют для команд, правок и чтения файлов;
- что происходит при продолжении: используется live `sandbox_session`, serialized `session_state` или fresh session из `snapshot`.

Такой manifest не заменяет policy layer. Он делает границу исполнения проверяемой: review может увидеть, что именно материализуется в workspace, какие права получает агент и можно ли безопасно resume/snapshot эту работу.

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

## 10. Частые ошибки

Теперь типовые проблемы повторяются уже на двух уровнях: на уровне отдельного adapter и на уровне всего MCP estate.

Типовые проблемы очень повторяемы:

- capability получает больше network access, чем нужно;
- secrets доступны слишком широкому набору adapters;
- tool result тащит сырые внешние payloads в prompt;
- timeout есть, но side effect uncertainty не моделируется;
- MCP server добавили, но policy и audit туда не дотянули;
- sandbox есть формально, но не ограничивает ничего важного.

Именно поэтому sandbox не должен быть checkbox-функцией. Он должен быть частью execution design.

## 11. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Отделены ли adapters от core runtime?
- Есть ли per-capability execution profile?
- Ограничены ли network, filesystem и secrets?
- Ясно ли, какой уровень изоляции используется: logical, process или runtime?
- Явно ли описан transport: direct, MCP, sandboxed exec?
- Понимает ли система, когда result trustworthy, а когда только partially trusted?
- Есть ли execution facts помимо business payload?
- Используются ли ephemeral sandboxes там, где есть high-risk execution?
- Можно ли объяснить, почему capability была разрешена именно в этом run?

Если ответы расплывчаты, capability layer у тебя пока больше похож на набор удобных интеграций, чем на управляемую платформу.

## 12. Что делать дальше

Сначала зафиксируй execution profile и isolation boundaries, а потом переходи к retries, rate limits и rollback boundaries.

Следующая естественная тема в этой части: idempotency, retries, rate limits и rollback boundaries. После sandbox и capability contracts именно она превращает execution model в production-grade слой.

- [Глава 8. Модель выполнения и каталог инструментов](chapter-8.md)
- [Глава 10. Идемпотентность, повторы, лимиты запросов и границы отката](chapter-10.md)
- [Часть IV. Инструменты и выполнение](index.md)
- [Источники](../../appendix/sources.md)

[^google-sandbox]: [Google Cloud, Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)

[^openai-sandbox-agents]: OpenAI Agents SDK, [Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/) и [Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/)
