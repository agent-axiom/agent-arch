# Глава 16. Базовая схема среды исполнения

!!! info "Как читать эту главу"
    Полезно держать в голове не абстрактный вопрос “как устроена среда исполнения”, а очень практичную задачу:

    - где именно должен жить основной цикл того же агента поддержки;
    - как не смешать слой политик, память, исполнение и телеметрию в один обработчик;
    - как собрать каркас, который выдержит не только демо, но и последующую выкладку.

    Если на эти вопросы нет ясного ответа, система обычно продолжает работать только до первого серьезного изменения или инцидента.

## 1. Зачем нужна эталонная схема среды исполнения, если у тебя уже есть архитектура

Архитектурные главы полезны, потому что они дают язык и рамку. Но в какой-то момент почти у всех возникает один и тот же вопрос: “Хорошо, а как это должно выглядеть как система, которую реально можно собрать?”

Именно в этом состоит главная задача этой главы. Она должна помочь читателю перейти через важную границу: от согласия с аргументом книги к пониманию того, как этот аргумент превращается в работающую структуру системы.

В нашем сквозном сценарии разбора обращений поддержки это уже не теоретический вопрос. Агент умеет проверять статус пользователя, обращаться к памяти, открывать тикет через шлюз и оставлять трассы. Но без явной схемы среды исполнения все эти шаги очень быстро расползаются по локальным обработчикам, разовым повторам и случайным интеграционным обходам.

Вот тут и нужна эталонная схема среды исполнения.

Ее задача не в том, чтобы стать единственной возможной реализацией. Ее задача:

- зафиксировать основные модули;
- показать поток одного запуска;
- отделить обязательные слои от необязательных улучшений;
- дать команде отправную точку без лишней магии.

Поэтому эту главу полезно читать не только как главу про границы модулей, но и как главу про работающую структуру под давлением изменений. Настоящий вопрос в том, появилась ли у среды исполнения такая форма, которая выдержит новые политики, новые инструменты, длинные запуски, прерывания и давление поэтапного выпуска, не распадаясь снова на обработчики и исключения.

## 2. Минимально взрослая среда исполнения уже состоит не из одной модели

Очень полезно сразу отказаться от образа “агент = один вызов модели плюс инструменты”.

Минимально взрослая среда исполнения обычно включает:

- слой входа;
- координатор запуска;
- проверки политик;
- слой доступа к памяти;
- слой исполнения инструментов и возможностей;
- эмиттер телеметрии;
- сборку результата.

То есть среда исполнения — это не “место, где вызывается LLM”. Это управляемый цикл вокруг модели.

## 3. Как выглядит базовый поток одного запуска

Для эталонной реализации удобно мыслить один запуск примерно так:

1. принять запрос и построить контекст запуска;
2. выполнить предварительные проверки политик;
3. собрать нужный контекст из памяти и извлечения;
4. вызвать модель;
5. если нужен вызов инструмента, прогнать его через слой исполнения;
6. записать телеметрию;
7. собрать финальный результат;
8. запланировать фоновые обновления.

Это уже очень далеко от “просто чат с функциями”, и именно так и должно быть.

<div class="diagram-card">
<p>У базовой среды исполнения уже есть несколько обязательных контрольных точек</p>

``` mermaid
flowchart LR
    A["Вход"] --> B["Контекст запуска"]
    B --> C["Предварительная проверка политик"]
    C --> D["Память / извлечение"]
    D --> E["Шаг модели"]
    E --> F{"Нужен инструмент?"}
    F -->|Нет| G["Сборка результата"]
    F -->|Да| H["Слой исполнения"]
    H --> I["Результат инструмента"]
    I --> E
    G --> J["Телеметрия + фоновые задачи"]
```

</div>

## 4. Какие модули полезно держать отдельными сразу

Есть несколько границ, которые выгодно выделить в коде уже в первой версии:

- `runtime.py` или `orchestrator.py` для основного цикла;
- `policy.py` для решений политик;
- `memory.py` для извлечения и записей памяти;
- `catalog.py` для реестра возможностей;
- `execution.py` для вызова инструментов;
- `telemetry.py` для spans и structured events.

Когда все это слеплено в один большой обработчик, первые демо получаются быстро, но взросление системы становится болезненным почти сразу.

!!! example "Сквозной кейс: где живет защита от дублей"
    В среде исполнения для разбора обращений поддержки защита от дубля тикета не должна быть спрятана в адаптере службы поддержки. `runtime.py` должен управлять контекстом запуска и веткой повтора, `execution.py` — выполнять пишущую возможность через идемпотентный контракт, `telemetry.py` — фиксировать `side_effect_unknown`, а `policy.py` и шлюз поэтапного выпуска — решать, можно ли продолжать. Тогда один и тот же инцидент не расползается по обработчикам.

**Заметка о сквозных сценариях среды исполнения:** базовая среда исполнения должна поддерживать все три канонических сценария без локальных обходов. Разбор обращений поддержки требует пути пишущей возможности с проверками подтверждения, контрактом идемпотентности и телеметрией дублей тикета. Внутренний ассистент знаний требует пути извлечения с привязкой к источникам, клиентскими границами, проверками свежести и защищенными записями в память. Координация инцидентов требует пути эскалации с проверками роли реагирующего, отправкой уведомлений, обновлениями состояния инцидента и фоновыми задачами после инцидента.

## 5. Не смешивай оркестрацию и бизнес-адаптеры

Одна из самых дорогих ошибок стартовой реализации: среда исполнения напрямую знает слишком много про конкретные внешние системы.

Тогда код оркестрации начинает содержать:

- условную логику по конкретным инструментам;
- знание о внешних формах payload;
- локальные ретраи под конкретный API;
- разовое маскирование данных;
- специальные обходы для отдельных интеграций.

Эталонная среда исполнения должна показывать обратную идею: оркестрация работает через контракты, а адаптеры живут на краю системы.

## 6. Пример минимальной структуры проекта

Ниже очень приземленный вариант стартовой структуры:

```text
agent_runtime/
  orchestrator.py
  policy.py
  memory.py
  catalog.py
  execution.py
  telemetry.py
  models.py
  background.py
```

Это не “единственно правильная” структура. Но она уже помогает не свалить все в один файл и не смешать контрольные слои между собой.

## 7. Простой кодовый каркас оркестратора

Ниже не промышленная среда исполнения, а именно каркас-схема. Он показывает, как разделяются шаги запуска и где должны проходить ключевые контрольные точки.

```python
from dataclasses import dataclass


@dataclass
class RunRequest:
    user_input: str
    tenant_id: str
    principal_id: str


@dataclass
class RunResult:
    output_text: str
    status: str


def run_agent(request: RunRequest) -> RunResult:
    policy_check(request)
    context = retrieve_context(request)
    model_output = call_model(request, context)

    if model_output.get("tool_request"):
        tool_result = execute_tool(model_output["tool_request"])
        emit_event("tool_execution", tool_result)
        model_output = call_model(request, context + [tool_result])

    schedule_background_updates(request, model_output)
    return RunResult(output_text=model_output["text"], status="success")
```

Идея здесь очень простая: даже базовая среда исполнения уже должна явно показывать проверки политик, извлечение, исполнение инструментов и фоновые обновления как отдельные этапы.

## 8. Длинные запуски — не необязательная надстройка, а часть базового контура

Частая ошибка рантайма в том, что команда молча предполагает: любой полезный запуск должен завершаться в одном синхронном запросе. Это верно только пока система остается заточенной под демо.

В реальном сценарии поддержки часть запусков по природе длиннее:

- ожидание подтверждения;
- ожидание инструментов с нестабильной задержкой;
- ожидание второго прохода модели после исполнения инструментов;
- ожидание отложенного продолжения или фонового обновления.

Свежий материал OpenAI полезен тем, что рассматривает фоновое исполнение как самостоятельную заботу среды исполнения, а не как обход проблем с ограничением времени.[^openai-background]

Их июньское исследование по Codex дает этому не только архитектурное, но и рыночное основание: agentic AI меняет единицу знания work с одиночного interaction на delegated long-horizon tasks, а к маю 2026 года 80,6% sampled individual Codex users уже давали хотя бы один запрос, оцененный как более 30 минут человеческой работы, 70,2% — более часа и 25,6% — более восьми часов.[^openai-agents-transforming-work] Эти пороги model-estimated, поэтому их нельзя читать как точный учет рабочего времени; но как directional signal они говорят о другом runtime surface: нужно измерять не только latency одного запроса, но и task horizon estimate, agent runtime, parallel workstreams, checkpoint age и attention budget. Практический материал OpenAI про Codex-maxxing формулирует тот же operating pattern проще: ambitious goal надо разбивать на проверяемые шаги, удерживать context across workstreams и явно решать, где execution можно делегировать Codex, а где нужен человеческий oversight.[^openai-codex-maxxing]

Именно так на это и стоит смотреть в базовой среде исполнения. Рантайм должен уже на старте различать:

- синхронные запуски, которые безопасно завершаются в одном активном проходе;
- фоновые запуски, которые продолжаются после первого ответа;
- возобновляемые запуски, которые ставятся на паузу из-за подтверждения, внешнего ввода или отложенной работы.

Таксономия схем рабочих процессов у Anthropic делает это еще острее, потому что разные схемы оркестрации создают разные потребности в контрольных точках.[^anthropic] У `prompt chaining` контрольная точка обычно нужна между фиксированными стадиями, у `routing` она часто нужна только на границе классификации и передачи, параллельное исполнение требует видимости состояния объединения, а схема `orchestrator-workers` требует состояния координации оркестратора и рабочих агентов, которое переживает частичное завершение.
### 8.1. Harness vs runtime

LangChain формулирует полезную границу: harness дает агенту prompts, tools, skills и рабочий цикл рассуждения, но production runtime отвечает за то, чтобы длинная работа переживала сбои, выкладки, ожидание человека и эксплуатационные ограничения.[^langchain-production-runtime] Поэтому в книге важно не смешивать “хорошую обвязку агента” с архитектурой системы. Harness может улучшать качество действий, но runtime должен владеть долговечным исполнением, checkpoint boundaries, памятью с управлением происхождением, изоляцией арендаторов, human-in-the-loop ожиданиями, наблюдаемостью, sandbox boundaries и открытыми integration protocols вроде MCP/A2A.

Материал Cloudflare/Flue делает эту границу еще точнее: production agent stack состоит как минимум из трех слоев, а не двух.[^cloudflare-flue-platform] Слой **framework** дает структуру проекта, conventions, integrations, CLI и developer experience. **Harness** владеет agentic loop: tool calls, context management, observations и движением к результату задачи. **Runtime/platform** владеет compute, state и storage primitives, которые верхние слои не могут сымитировать: durable execution, sandboxed dynamic code execution, durable filesystem/workspace state, dynamic workflows, bindings, credential isolation и recovery. Это различие полезно потому, что многие команды покупают или строят framework, но все равно нуждаются в platform contract для crash recovery, untrusted code, долгих ожиданий и filesystem state.

Project Think собирает ту же мысль в практичную рамку **primitive -> failure mode -> runtime implication**: durable execution with fibers закрывает потерю прогресса при eviction; sub-agents закрывают failure mode "один агент держит весь контекст"; persistent sessions закрывают обрыв клиента и перенос работы между поверхностями; sandboxed code execution закрывает небезопасное выполнение непроверенного кода; execution ladder помогает выбрать между foreground run, background run, workflow и fiber; self-authored extensions полезны только если runtime хранит capability boundary, review evidence и rollback path.[^cloudflare-project-think] Поэтому это не еще один vendor example, а хороший checklist для главы: если primitive назван, рядом должна быть названа failure mode и эксплуатационная обязанность runtime.

Минимальная таблица требований выглядит так:

| Production requirement | Runtime primitive |
| --- | --- |
| Run survives crash or deploy | durable run record, checkpoint boundary, resume cursor |
| Human waits for hours or days | explicit wait state, approval/refusal record, timeout policy |
| Tool or workflow step is retried | idempotency key, lease/retry policy, duplicate-write guard |
| Agent resumes after external input | resume event, expected event schema, stale-event handling |
| Work crosses tenants or workspaces | tenant/principal context, scoped stores, policy decision trace |
| Operator investigates behavior | trace span ids, evidence refs, exported session/run record |
| Runtime exposes tools and subagents | capability catalog, sandbox profile, MCP/A2A boundary contract |

Короткая формула: prompt/tool/skill layer отвечает за **что агент умеет делать**, а runtime layer отвечает за **как это исполнение остается управляемым, возобновляемым и расследуемым**. Если этой границы нет, команда обычно называет runtime “agent harness” и поздно обнаруживает, что crash recovery, multi-tenancy, approval sleep/resume и observability живут в разных местах и не имеют общего contract.

AWS AgentCore и GitHub security validation for third-party coding agents полезны как свежий production reference для того же contract.[^aws-agentcore-agentops][^aws-agentcore-coding-agents][^github-third-party-coding-agent-validation] AgentCore AgentOps делает видимыми traces, latency, token/cost metrics, session history, PII redaction и governance signals; пример hosting coding agents добавляет isolated session, persistent workspace, scoped credentials и возможность закрыть laptop, пока agent продолжает задачу в управляемой среде; GitHub validation показывает, что agent-generated code должен проходить platform-owned CodeQL, dependency risk и secret scanning gates до того, как результат считается готовым к review.

Переносимый production runtime contract поэтому стоит формулировать так: **isolated session → durable workspace → scoped credentials → egress/tool boundary → trace and cost ledger → PII redaction → platform security validation → human review artifact**. Для эталонного рантайма это не требование “использовать AWS” или “использовать GitHub”, а checklist: среда исполнения должна знать, где живет рабочее пространство, какие credentials были доступны, какие network/tool boundaries действовали, сколько стоил run, какие sensitive fields были отредактированы, какие security gates проверили staged output и какой artifact человек потом review-ит.

Cloudflare vulnerability harness добавляет к этой границе хороший прикладной пример.[^cloudflare-vulnerability-harness] Их security-audit skill стал не “большим агентом”, а pipeline со стадиями Recon, Hunt, Validate, Gapfill, Dedup, Trace, Feedback и Report. Важная runtime-деталь: каждая стадия пишет состояние в SQLite database, keyed by `run_id`, `repo` и `stage`, поэтому stage можно resume, retry или включить в более поздний run без потери уже найденных findings. Это именно runtime boundary: модель выполняет узкую работу, а harness хранит долговечный state, очереди, coverage cells, validation status и evidence.

В vendor-neutral contract такой harness должен иметь:

- `harness_run_id`, `target_repo`, `stage_name`, `stage_attempt`, `stage_status`;
- `coverage_cell` для пары area × attack class или другого проверяемого разреза;
- `finding_candidate_id`, `validator_verdict`, `dedup_key`, `judgment_status`;
- `model_provider` и `model_version` как переменные исполнения, а не основу архитектуры;
- `shallow_run_signal`, если stage подозрительно быстро завершился без findings, sibling tasks или gapfill work;
- `fix_gate_status`, включая targeted test before/after и clean fail→pass evidence;
- `human_review_ref` для любого изменения, которое может уйти в production.

Это делает harness model-agnostic и failure-aware. Если frontier model меняется, provider меняет caching или transient API error приходит текстом внутри `200 OK`, durable orchestration still has to classify, retry and preserve evidence instead of treating empty output as success.

Механизм сохранения состояния LangGraph показывает тот же принцип на уровне детализации контрольных точек: долговечное состояние организуется по потоку, контрольные точки сохраняются на границах надшага, а успешные записи узлов внутри упавшего надшага могут сохраняться как ожидающие записи, чтобы при продолжении не пересчитывать уже выполненные узлы.[^langgraph-persistence] Архитектурный вывод: контрольные точки — это не один логический флаг. Среда исполнения должна явно назвать курсор для продолжения, границу допустимого повторного проигрывания и частичные записи, которые нельзя продублировать после сбоя.

Google Agent Executor формулирует похожий слой уже как распределенный runtime primitive: agent execution graph должен переживать long-running jobs, disconnections, trajectory branching и restore из event log, а не зависеть от одного живого процесса.[^google-agent-executor] Для базовой среды исполнения это полезно как vendor-neutral требование: если пользователь закрывает клиент, оператор запускает альтернативную ветку или система восстанавливает agent state после сбоя, runtime обязан иметь session event log, snapshot/restore boundary, single-writer или session-consistency rule и явную модель ownership над активной веткой выполнения.

Их более поздняя работа про проектирование рабочей обвязки добавляет сюда еще один практический урок для рантайма: в длинных прикладных запусках часто нужно явно различать **сжатие контекста** и **сброс контекста**.[^anthropic-harness] Сжатие оставляет того же агента на укороченной истории, поэтому преемственность сохраняется, но тревожность из-за контекста и накопленный дрейф могут остаться. Сброс запускает нового агента с чистого листа и требует структурированный артефакт передачи, который переносит состояние, следующие шаги и контекст оценки. Это не просто прием для инструкции, а часть архитектуры рантайма, потому что как только сбросы входят в рабочую обвязку, платформа должна решить, какое состояние достаточно устойчиво, чтобы пережить сброс, и какой артефакт проверки получает следующий агент.

При этом артефакт передачи не становится артефактом авторизации. Среда исполнения должна сохранить [схему непрерывности контекста](../../appendix/continuity-envelope-schema.md), проверить отпечаток и происхождение, согласовать неизвестный внешний эффект, заново загрузить идентичность и версии контрактов из систем истины, а затем повторно авторизовать следующий вызов возможности. Успешное восстановление означает только то, что преемственность собрана заново; оно никогда не означает, что сводка разрешила действие.

В базовой реализации эту границу можно сделать явной через следующий протокол:

1. До сжатия остановиться на безопасной границе, записать журнал сессии, сохранить курсор рабочего процесса и незавершённые обязательства.
2. Сохранить управляющие поля без суммаризации, создать производную сводку, связать её с диапазоном исходных событий через `summary_sha256` и записать `context_compaction`.
3. После сброса загрузить конверт из управляемого хранилища и проверить схему, отпечаток, происхождение событий, арендатора, субъекта, область делегирования, политику, возможность, подтверждение, бюджет, песочницу и контрольную точку.
4. При неизвестном внешнем эффекте вернуть `blocked_on_reconciliation`; при любом расхождении записать `continuity_validation_failed` и остановиться.
5. Только после успешной проверки и, если она требовалась, сверки пересобрать одноразовое представление контекста, записать `context_rehydration` и заново выполнить проверку политики и авторизацию до следующего вызова возможности.

Из этого следует более общий вывод: в длинных агентных задачах должны сохраняться не только данные, но и **возврат на вложенную экспертизу**. Anthropic описывает это через initializer agent, feature list, progress file, git history, clean-state discipline и end-to-end проверки в начале следующей сессии.[^anthropic-harness] Архитектурно это не “память агента” в бытовом смысле, а набор проверяемых артефактов, которые позволяют свежему контекстному окну быстро унаследовать инженерное суждение прошлых проходов. Если такой слой отсутствует, каждая новая сессия заново тратит бюджет на ориентацию, чаще объявляет преждевременную победу и хуже различает уже выполненную работу, незаконченный инкремент и сломанное состояние.

То есть ограниченная автономия — это не только вопрос политики. Это еще и вопрос дизайна состояния среды исполнения: каждая разрешенная схема исполнения приносит с собой собственную семантику паузы, продолжения, сброса и завершения.

Если у рантайма нет явной формы для этих случаев, длинная работа почти всегда утекает в несистемные повторы, дублирующиеся запросы и скрытые переходы состояния.

### 8.2. Состояние сессии песочницы тоже является состоянием среды исполнения

У Sandbox Agents в OpenAI Agents SDK есть полезное разделение, которое стоит перенести в дизайн базовой среды исполнения: `Manifest` описывает контракт свежего рабочего пространства, а конкретный запуск может получить живую сессию песочницы, сериализованный `session_state` или стартовать из снимка `snapshot`.[^openai-sandbox-agents]

Материал OpenAI про computer environment для Responses API описывает тот же слой как агентный компьютер: модель предлагает действие, платформа исполняет shell command в изолированном контейнере, возвращает streamed observation, а следующий model turn решает, продолжать ли работу.[^openai-computer-environment] Важная архитектурная граница здесь в том, что model decision и command execution не одно и то же. Модель предлагает, но runtime отвечает за isolation, filesystem/artifact persistence, optional structured storage, restricted network access, timeout/cancellation и наблюдаемый вывод инструмента.

Для эталонного рантайма это означает, что состояние песочницы нельзя прятать внутри адаптера инструмента. Минимально полезная модель должна уметь хранить рядом с `run_id` и `trace_id` хотя бы:

- `sandbox_session_id`;
- `sandbox_manifest_version`;
- `sandbox_permissions_profile`;
- `snapshot_id`, если запуск стартовал из сохраненного рабочего пространства;
- список материализованных записей рабочего пространства или ссылку на проверенный манифест;
- признак, можно ли эту песочницу продолжить, сохранить снимком или нужно пересоздать.

Тогда длительная работа с файлами, командной оболочкой и памятью не превращается в непрозрачную папку на диске. Она становится частью того же слоя управления средой исполнения, где уже живут подтверждения, фоновые запуски, сессии возможностей и [доказательства трасс](../../appendix/trace-schema.md).

### 8.3. Именованный агент с состоянием как отдельная топология среды исполнения

Cloudflare Agents SDK показывает другую полезную базовую схему: агент может быть не только временным циклом исполнения, но и **именованным долговечным объектом среды исполнения**. В их модели каждый экземпляр агента работает поверх Durable Object: у него есть собственное долговечное состояние SQL/ключ-значение, WebSocket-соединения, запланированные задачи, возможность проснуться по событию и снова перейти в спящий режим, когда он простаивает.[^cloudflare-agents]

Их более свежая формулировка делает границу еще проще: агент — это **durable identity, not an always-on process**.[^cloudflare-long-running-agents] В архитектуре это важнее конкретной платформы. `agent_instance_id` должен переживать процесс, deploy, hibernation и разрыв соединения; активный процесс — только временный исполнитель события. Поэтому runtime contract должен явно показывать, что сохраняется как состояние именованного экземпляра, а что исчезает при eviction.

| Граница | Переживает restart/hibernation | Не переживает restart/hibernation |
| --- | --- | --- |
| Состояние агента | `this.state`, durable SQL/key-value tables, schema-migrated instance metadata | class fields, local variables, unstored closures |
| Работа во времени | scheduled tasks, queued/background work, fiber checkpoints, durable workflow steps | `setTimeout`, `setInterval`, open fetches, promise chains |
| Сессии и UI | connection state, persisted conversation/history refs, resumable stream cursor | open WebSocket frame, browser tab process, in-memory callback |
| Side effects | idempotency key, approval record, durable execution log, evidence refs | “already called” boolean in memory, partial tool call without ledger |

Практический инвариант: все, что может создать внешний побочный эффект после ожидания человека, сбоя или рестарта, должно иметь durable log, idempotency key и replay boundary. Иначе “продолжить после паузы” становится повторным выполнением с надеждой, что локальная память еще жива.

В книгу это стоит переносить не как рекомендацию “используйте именно Cloudflare”, а как архитектурную форму. Если агент привязан к стабильному имени реальной сущности — обращению клиента, проекту, устройству, рабочему пространству клиента, комнате, ветке обсуждения или исследовательскому досье, — среда исполнения должна явно разделять:

- `agent_instance_id`, который живет дольше одного run;
- `run_id`, который описывает конкретное выполнение;
- `session_id`, который описывает пользовательскую или транспортную сессию;
- долговечное состояние агента, которое переживает разрыв соединения, выкладку, спящий режим и фоновое пробуждение;
- внешнее хранилище знаний, которое не является частным изменяемым состоянием одного экземпляра.

Такая схема особенно полезна для чатов, голосовых агентов, рабочих процессов и агентов наблюдения, где пользователь ожидает преемственность, а не обмен запрос-ответ без состояния. Но она же добавляет риски, которые базовая среда исполнения должна сделать видимыми: изоляция клиентов для именованных экземпляров, утечки между WebSocket-сессиями, повторное проигрывание или продолжение после спящего режима, запланированные побочные эффекты без активного пользователя и миграции долговечного состояния при изменении версии агента.

Поэтому эталонный рантайм не обязан реализовывать Durable Objects, но ему нужна абстракция вроде хранилища экземпляров агента `AgentInstanceStore` и границы планировщика `SchedulerBoundary`: место, где видно, какой именованный экземпляр владеет состоянием, какие запуски его меняли, какие запланированные задачи могут его разбудить и какие трассы доказывают безопасное продолжение.

Сторона расписания особенно важна: Cloudflare показывает отложенные, запланированные, cron- и интервальные задачи, которые переживают перезапуск, сохраняются в SQLite и будят агента через сигналы Durable Object.[^cloudflare-schedule] Архитектурный вывод для книги: расписание нельзя оставлять невидимым обратным вызовом. Его нужно отражать как долговечную контрольную запись с экземпляром-владельцем, схемой полезной нагрузки, ключом идемпотентности, политикой пересечения запусков, временем следующего срабатывания и связью с трассой.

GitHub Copilot cloud agent automations показывают тот же boundary в repo-native форме: unattended work может стартовать от repository events или scheduled triggers, а не только от ручного запроса.[^github-copilot-automations] Если такая automation запускает Copilot cloud agent, runtime должен записывать `automation_id`, trigger source, owner, branch policy, allowed events, approval boundary и evidence refs. Copilot code review support for `AGENTS.md` добавляет соседний контракт: repo instructions становятся входом review agent и должны версионироваться как policy-bearing artifact, а не как устная договоренность.[^github-copilot-agents-md] BYOK в Copilot app расширяет provider-neutral control plane еще на provider routing: ключи, scopes и provider choice должны жить в управляемой модели доступа, а не в скрытой настройке отдельного пользователя.[^github-copilot-byok]

Сторона реального времени добавляет еще одну границу: состояние соединения не равно состоянию агента. В WebSocket-модели Cloudflare Agents у соединения есть собственный `id`, `uri`, состояние на уровне соединения, метки, обработчики жизненного цикла и возможность выключить протокольные сообщения вроде identity/state/MCP для конкретного соединения.[^cloudflare-websockets] Для базовой среды исполнения это означает, что широковещательные сообщения, присутствие пользователя, интерфейс подтверждения и потоковые обновления должны проходить через авторизацию в области соединения и трассируемую рассылку, а не напрямую читать все долговечное состояние агента.

В нейтральном к поставщикам виде этот паттерн можно назвать **долговечным актором агента**: стабильная идентичность, локальное долговечное состояние, возобновляемые сессии, пробуждения по расписанию и трассируемая передача управления к управляемым хранилищам. В локальном состоянии допустимо держать факты уровня экземпляра: курсор открытого рабочего процесса, настройки пользовательского интерфейса и сессии, позицию во внутренней очереди, последнее обработанное событие, метаданные расписания и небольшие кэшированные представления, которые можно пересобрать. Оно не должно незаметно становиться системой истины для профильной памяти пользователя, знаний арендатора, секретов, политик, аудиторских журналов или фактов между экземплярами. Эти данные должны жить в управляемых хранилищах с происхождением, сроками хранения, экспортом и контрактами контроля доступа.

Антипаттерн здесь — скрытая долговечная память: именованный агент копит приватное состояние, позже извлекает его или действует на его основе как на проверенное знание, а у операторов нет экспорта, аудиторского следа, пути миграции схемы или истории удаления. Долговечное состояние актора полезно только тогда, когда его владение и жизненный цикл явно описаны.

### 8.3. Оболочка агента и долговечный стержень рабочего процесса
### 8.4. Recoverable internal tasks / fibers

Cloudflare добавляет к этой топологии еще одну полезную грань: долговечная работа может жить не только как внешний workflow, но и как **recoverable internal task** внутри самого агента.[^cloudflare-fibers] В их API `runFiber()` регистрирует работу в SQLite, удерживает Durable Object живым во время выполнения, позволяет сохранять промежуточный снимок через `stash()` и вызывает `onFiberRecovered()` при следующей активации, если объект был вытеснен в середине задачи. `startFiber()` подходит для background work, который нужно принять durable, дедуплицировать через idempotency key, позже inspect/cancel и не держать открытым исходный запрос.

Vendor-neutral вывод такой: baseline runtime должен различать по крайней мере четыре уровня длительной работы:

- **synchronous run:** короткая работа в текущем request/response контуре;
- **background/resumable run:** user-visible run, который можно поставить в фон, наблюдать и возобновить;
- **durable workflow:** многошаговая orchestration spine с retries, waits, approvals и external events;
- **internal recoverable fiber:** часть собственного цикла агента, которая переживает eviction/restart через checkpoint и recovery hook.

Минимальный контракт для последнего уровня: `fiber_id`, `fiber_name`, `fiber_status`, `fiber_idempotency_key`, `fiber_checkpoint_ref` или `stash_snapshot`, `recovery_handler`, `cancellation_status`, `last_safe_step`, `owner_agent_instance_id` и `evidence_refs`. Этот контракт не должен превращаться в скрытую долговечную память или system of record. Checkpoint нужен, чтобы безопасно продолжить expensive task, а не чтобы незаметно хранить profile facts, tenant knowledge, secrets или policy state.

В [эталонном пакете](../../appendix/reference-package.md) durable named-agent topology пока отражена как contract surface, а не как полноценная Durable Object/fiber реализация: session/run exports оставляют поля `agent_instance_id`, `durable_state_version`, `scheduled_wakeup_id` и `resumable_stream_id`, а production adapter может расширить их fiber evidence вроде `fiber_id`, `fiber_status`, `fiber_checkpoint_ref` и `last_safe_step`. Для маленького runtime эти поля обычно пустые; книга показывает границу durable named instance и recoverable internal task, не превращая reference package в vendor-specific SDK.

Cloudflare Agents SDK changelog добавляет к этому более эксплуатационный слой: **detached sub-agent run** через `runAgentTool`, **durable milestones**, единый вход `runTurn` и recovery после `deploy/eviction/reconnect`.[^cloudflare-agents-background-subagents] Это полезно формулирует failure class: deploy, Durable Object eviction, connection churn или hung stream происходят во время агентного run. Runtime не должен бросать работу как `interrupted`, если есть durable backbone, `continuation_id`, `last_durable_checkpoint`, idempotency key и bounded reconcile path.

Отдельный changelog Cloudflare про outbound connections показывает, что даже "живой" stream является runtime contract, а не просто сетевой деталью.[^cloudflare-outbound-connections] Durable Object теперь остается активным, пока есть active outbound connection или outbound WebSocket, но только в пределах указанного keepalive window. Для архитектуры это означает: long-running LLM stream должен иметь `stream_id`, `connection_keepalive_deadline`, `last_emitted_offset`, `resume_strategy` и fallback checkpoint. Иначе команда может ошибочно считать stream долговечным, хотя после лимита или закрытия соединения снова действует обычная eviction-модель.

Для delegated tools есть соседнее правило. Когда sub-agent получает **client-provided tools** через `clientTools` и `onClientToolCall`, это не просто callback convenience.[^cloudflare-agents-recovery] Parent runtime должен хранить allowlist этих tools, owner/caller identity, argument schema, expiration и trace evidence. Иначе delegated sub-agent получает неявные capability leaks. Recovery path также должен чинить незавершенные tool calls: stream stall watchdog и interrupted tool-call repair должны возвращать run к последнему durable checkpoint, а не повторять side effect по памяти transcript.

### 8.5. Agent shell + durable workflow spine

Следующий полезный паттерн Cloudflare — не складывать всю долгую работу в один цикл событий агента. Агент может быть **границей взаимодействия с состоянием** (**stateful interaction boundary**): держать идентичность экземпляра, WebSocket- или HTTP-сессию, локальное состояние, пользовательские обратные вызовы и текущую картину диалога. Рабочий процесс при этом становится **долговечной границей выполнения** (**durable execution boundary**): хранит шаги, повторы, ожидание внешних событий, длительные шлюзы подтверждения и восстановление после падения.[^cloudflare-workflows]

<div class="diagram-card">
<p>Живой агент и долговечный рабочий процесс решают разные задачи</p>

``` mermaid
flowchart LR
    S["Сессия / хранилище состояния"] --> A["Оболочка среды выполнения агента"]
    A --> W["Долговечный стержень рабочего процесса"]
    W --> E["Инструмент / внешнее событие / шаг подтверждения"]
    W --> L["Журнал аудита и доказательств"]
    A --> U["Пользовательский поток / WebSocket"]
    E --> L
```

</div>

В эталонной схеме это означает: оболочка агента может сообщать прогресс, принимать новые сообщения и показывать интерфейс подтверждения, но долговечный рабочий процесс должен владеть тем, что нельзя потерять: идентификатором шага, ключом идемпотентности, политикой повторов и тайм-аутов, ожиданием внешнего события, решением подтверждения и ссылками на доказательства. Тогда перезапуск агента или разрыв WebSocket не превращает длинную работу в полупамятный пользовательский диалог.

В Cloudflare HITL API это выглядит как `waitForApproval()` внутри workflow: ожидание может длиться **months or longer** без живого agent process, а agent shell предоставляет `approveWorkflow()` и `rejectWorkflow()` для human decision. Для книги важен не API сам по себе, а boundary: pending approval, timeout, escalation и audit trail должны быть durable execution state.

Cloudflare Agents SDK v0.16.1 показывает тот же контракт на стороне Codemode runtime: модель получает один `codemode` tool, пишет код против typed globals, а runtime хранит durable execution log.[^cloudflare-agents-sdk-0161] Когда код доходит до approval-gated action, execution pauses и возвращает pending approval; после подтверждения уже завершенные calls replay из durable log, approved action выполняется, и тот же код продолжает работу. В vendor-neutral виде это хороший минимальный контракт для approval gate:

- `approval_id`, `approval_status`, `requested_action`, `risk_tier`, `approver_ref`;
- `execution_log_ref` с уже завершенными deterministic/tool calls;
- `replay_policy`, который отличает безопасный replay от повторного side effect;
- `idempotency_key` для действия после approval;
- `resume_cursor`, `timeout_policy` и `evidence_refs`.

Такой gate должен жить в durable workflow или runtime log, а не в UI callback. UI может показать кнопку подтверждения, но система исполнения должна владеть pending state, replay и продолжением после решения.

Dynamic Workflows у Cloudflare заостряют этот контракт еще сильнее: `run(event, step)` становится долговечным планом, где `step.do()` исполняет устойчивый шаг, `step.sleep()` или `step.sleepUntil()` делает ожидание явным, а `step.waitForEvent()` переносит внешний сигнал или human approval в саму модель исполнения.[^cloudflare-dynamic-workflows] Для agent runtime это важная граница: агент может выбрать или сгенерировать план, но платформа должна владеть replay, retry, sleep/wait состоянием, результатами уже завершенных шагов и тем, какие события безопасно продолжают работу.

Saga rollbacks в Cloudflare Workflows добавляют к этому важную failure-грань: компенсация должна жить рядом с forward step как metadata, а не в далеком `catch` block.[^cloudflare-workflow-rollbacks] Когда workflow падает терминально, runtime может найти все eligible `step.do()` calls с rollback handlers, передать им сохраненный `output` или `undefined`, выполнить компенсации в обратном `step-start` order и при restart восстановить нужные handlers через replay без повторения уже завершенных side effects. Для agent workflows это практичный контракт: если шаг резервирует деньги, inventory, account, deployment slot или внешнюю квоту, `compensation_ref` и `rollback_idempotency_key` должны быть частью step record с самого начала.

В vendor-neutral контракте каждый durable step поэтому должен иметь `step_id`, `step_type`, `idempotency_key`, `input_schema`, `output_ref`, `retry_policy`, `wait_event_type`, `approval_ref`, `compensation_ref`, `rollback_idempotency_key`, `rollback_retry_policy`, `timeout_policy` и `evidence_refs`. Иначе “workflow” снова становится просто длинной функцией с надеждой на retry, а не управляемой execution spine.

### 8.6. Временная deploy-identity и handoff человеку

Cloudflare Temporary Accounts добавляют к durable workflow еще один практичный паттерн: агент может получить **temporary account** для деплоя, а затем человек может claim-нуть результат в нормальную учетную запись.[^cloudflare-temporary-accounts] Это не просто developer convenience. Архитектурно это lease-модель для агентного deploy: агент получает ограниченную идентичность, выполняет deployment step, оставляет доказательства, а ownership затем переходит к человеку или команде.

В vendor-neutral runtime contract такая возможность должна быть видна явно:

- `temporary_principal_id` и `principal_issuer`;
- `lease_ttl`, `scope`, `allowed_deploy_targets` и `egress_policy`;
- `deployment_artifact_ref`, `deployment_url`, `rollback_ref` и `evidence_refs`;
- `claim_status`, `claimed_by`, `claim_deadline` и `unclaimed_cleanup_policy`;
- `approval_ref` для перехода из temporary deploy в owned production surface.

Главное правило: temporary account не должен становиться новым долговечным сервисным пользователем. Это рабочий lease для конкретного агентного шага, с коротким сроком жизни, ограниченной областью, trace linkage и понятным состоянием после завершения: claimed, expired, revoked или cleaned up. Если claim/handoff не моделируется, агентный deploy легко превращается в “живой ресурс без владельца”, который прошел мимо нормального lifecycle registry.

### 8.7. Autonomy ladder как контракт среды исполнения

Материал Anthropic Institute про recursive self-improvement полезен для этой главы не как прогноз, а как практическая лестница автономии.[^anthropic-rsi] Чем больше AI-система участвует в собственном улучшении, тем меньше достаточно спрашивать “может ли агент выполнить задачу”. Runtime должен явно фиксировать, **кто владеет каждым шагом автономии**:

- `who sets the goal`: человек, продуктовая политика, внешний event или сам агент;
- `who approves the plan`: владелец capability, reviewer, policy gate или автоматический контроллер;
- `who accepts the result`: пользователь, verifier, eval gate, CI или rollout owner;
- `who chooses the next problem`: человек, backlog rule, incident trigger, hill-climbing loop или сам агентный контур улучшения.

Эта **Autonomy ladder** хорошо стыкуется с предыдущими разделами главы. Для короткого synchronous run достаточно, чтобы цель и результат были human-owned. Для background/resumable run уже нужен владелец плана, timeout и проверяемое завершение. Для event-driven loop нужно отдельно ограничить trigger source и область действия. Для hill-climbing loop, который меняет prompts, tools, rubrics, memory/context или harness config, нужен release gate: агент может предложить изменение, но не должен сам бесконтрольно выбирать следующую задачу, менять собственную рабочую обвязку и принимать результат как успешный.

Минимальная запись рантайма поэтому должна хранить не только `run_id` и статус, но и autonomy boundary: `goal_setter`, `plan_approver`, `result_acceptor`, `next_problem_selector`, `allowed_self_modification_scope`, `required_human_review` и `evidence_refs`. Тогда рост автономии становится управляемой миграцией по ступеням, а не незаметным переходом от “агент помогает человеку” к “агент сам выбирает, что улучшать дальше”.

### 8.8. Проверяемое завершение как обязанность среды исполнения

Один практический урок из Claude Code переносится почти напрямую в базовую среду исполнения: автономному агенту нужен не только цикл действий, но и цикл проверки.[^anthropic-claude-code-best-practices] Если рантайм знает только “агент вернул финальный ответ”, оператор снова становится единственным контуром качества. Если же рантайм хранит условие завершения и результат проверки, запуск можно безопаснее оставлять без постоянного наблюдения.

Минимально полезная модель запуска поэтому должна уметь не только исполнять инструменты, но и фиксировать:

- `stop_condition`: какое проверяемое условие должно быть истинным перед завершением;
- `verification_command` или другой проверяемый механизм;
- `verification_result`: pass, fail, warning или blocked;
- `verifier_actor`: сам агент, детерминированный gate, отдельный verifier/subagent или человек;
- `evidence_refs`: ссылки на тестовый вывод, трассу, снимок экрана, diff или другой артефакт.

Это не обязательно значит, что каждый запуск должен тащить полный CI. Но рантайм должен иметь место для доказательства завершения. Иначе “done” остается свободным текстом, который плохо подходит для регрессионных шлюзов, ревью раскатки и последующего расследования.

## 9. Сессии инструментов с состоянием тоже должны входить в базовый контур

Как только слой исполнения начинает работать с MCP-подобными возможностями с состоянием, у базовой среды исполнения появляется еще одна обязательная граница: **состояние видимого пользователю запуска не равно состоянию сессии возможности**.[^aws-stateful-mcp]

Это важно потому, что один пользовательский запуск теперь может включать:

- один `run_id` среды исполнения;
- один или несколько MCP `session_id` для внешних возможностей;
- уведомления о ходе выполнения до финального ответа;
- промежуточные запросы данных, которые ставят запуск на паузу до нового ввода;
- повторную инициализацию, если сессия возможности истекла до завершения запуска.

Если все это слепить в один непрозрачный объект состояния, оператор уже не сможет объяснить, что именно продолжилось, что истекло и что надо повторить заново.

### 9.1. Среда исполнения должна относиться к сессии возможности как к состоянию первого класса

Минимально зрелый рантайм обычно уже должен уметь хранить хотя бы:

- `run_id`;
- `trace_id`;
- `capability_session_id`;
- `capability_session_status`;
- `expires_at`;
- `resume_token` или другой дескриптор продолжения;
- `approval_state`, если поток инструмента с состоянием был поставлен на паузу из-за подтверждения.

Это не означает, что каждому инструменту нужна тяжелая модель сессии. Это означает, что у рантайма должно быть место, где такое состояние сессии можно выразить, когда протокол этого требует.

### 9.2. Ход выполнения и промежуточные запросы должны входить в ту же модель управления продолжением

Еще один полезный вывод из материалов о MCP-состоянии: события хода выполнения и промежуточные запросы данных нельзя считать экзотическим побочным каналом. Они должны входить в ту же модель управления средой исполнения, что подтверждения и фоновое продолжение.

Это становится еще важнее, когда рантайм поддерживает несколько схем оркестрации. Ход выполнения из ветки параллельного исполнения, из рабочего агента, делегированного через схему `orchestrator-workers`, или из стадии `prompt chaining` со шлюзом не должен пропадать внутри адаптеров, привязанных к конкретной схеме. Он должен попадать в одну общую поверхность управления для статуса, продолжения, истечения и видимости для оператора.

На практике базовая среда исполнения выигрывает от одной общей модели состояний для:

- `in_progress` работы, которая еще жива внутри сессии возможности;
- пауз `waiting_for_input` или `waiting_for_approval`;
- `resumable` работы, которую можно продолжить в той же сессии возможности;
- `reinitialize_required` работы, где сессия возможности истекла и ее нужно поднять заново перед продолжением.

Без этих различий истечение сессии обычно выглядит как случайная ошибка, хотя на деле это нормальное событие жизненного цикла.

## 10. Что важно встроить в базовый контур с самого начала

Есть вещи, которые кажется соблазнительным “добавить потом”, но на деле их лучше заложить сразу:

- `trace_id` на каждый запуск;
- контекст клиента и принципала;
- обработчики решений политики;
- реестр возможностей вместо прямых вызовов;
- структурированную телеметрию;
- базовую точку подключения фоновых задач;
- явную модель статусов запуска вроде `queued / in_progress / completed / failed / canceled`;
- способ опросить, продолжить или отменить длинную работу без изобретения второго скрытого рантайма.

Если этого нет в базовой версии, потом система обычно дорастает до этого через болезненную переделку.

## 11. Минимальный каркас для фоновой и возобновляемой работы

Даже базовая среда исполнения должна иметь простой способ представлять работу, которая живет дольше первого запроса.

```python
from dataclasses import dataclass


@dataclass
class RunHandle:
    run_id: str
    status: str


def start_run(request: RunRequest) -> RunHandle:
    run_id = create_run_record(request)
    enqueue_run(run_id)
    return RunHandle(run_id=run_id, status="queued")


def continue_run(run_id: str):
    run = load_run(run_id)
    if run.status in {"canceled", "completed", "failed"}:
        return run

    update_status(run_id, "in_progress")
    result = execute_run_steps(run)
    update_status(run_id, result.status)
    return result
```

Смысл здесь не в усложнении. Смысл в том, чтобы длинная работа была достаточно явной: операторы могли ее наблюдать, клиенты могли ее опрашивать, а рантайм мог ее продолжать или отменять без догадок.

## 12. Что можно не усложнять в первой эталонной версии

На старте не обязательно сразу добавлять:

- сложный planner с множеством режимов;
- многоступенчатый конвейер сжатия памяти;
- сложную стратегию маршрутизации модели;
- полный контур самовосстановления;
- десяток золотых путей.

Эталонный runtime полезен не максимальной мощностью, а ясностью формы. Лучше небольшая, но чистая реализация, чем “универсальный комбайн”, который никто не понимает.

### 12.1. Runtime как разделение session, harness и hands

Еще один способ проверить зрелость эталонного runtime — спросить, можно ли заменить его части независимо. В managed-agent форме session, harness и hands разделены как интерфейсы, а не как детали одного процесса.[^anthropic-managed-agents] Anthropic называет это разделением brain и hands: model/harness может падать или меняться, sandbox/tool executor может быть пересоздан, а session log остается внешним durable record, из которого новый harness может проснуться через `wake(sessionId)`.

Для эталонного пакета это означает:

- session остается append-only evidence log и переживает сбой исполнителя;
- harness можно менять как control loop без миграции пользовательского workspace;
- sandbox/tools работают как contained hands с явным профилем сети, файловой системы, secrets и snapshot;
- debug происходит через trace, lifecycle summary и sandbox profile, а не через прямой доступ к окружению с пользовательскими данными.

Эта форма хорошо сочетается с предыдущими разделами главы: фоновое исполнение, resumable runs и capability sessions становятся не «долгим запросом внутри контейнера», а управляемой связкой session state, control loop и contained execution surface. Тест зрелости простой: можно ли заменить модель, harness, sandbox или конкретную hand capability без потери session history, audit trail и права оператора понять, что произошло.

Практический контракт здесь жестче, чем просто “держать историю”. **session не является context window**: это внешний журнал и API состояния, из которого harness собирает очередной prompt, но который не обязан целиком помещаться в модель. Минимальный runtime-интерфейс выглядит так:

- session API: `wake(sessionId)`, `getEvents()` и `emitEvent(id, event)` для чтения durable log и записи новых решений;
- hands API: `execute(name, input)` для вызова конкретной capability и `provision({resources})` для выдачи sandbox/tool ресурсов по policy profile;
- failure contract: отказ sandbox, tool executor, policy proxy или resource provision должен возвращаться harness как обычный `tool-call error`, а не как скрытый crash процесса;
- secret boundary: tokens are never reachable from the sandbox; sandbox получает brokered capability, а не raw credentials.

Тогда brain может ошибиться, hands могут отказать, session может пережить оба события, а replay видит не “модель не справилась”, а конкретную границу: не хватило ресурса, policy отказала capability, sandbox не поднялся или tool вернул управляемую ошибку. Это делает managed-agent разделение не только масштабируемым, но и расследуемым.


## 13. Пример конфигурации рантайма

Ниже пример конфигурации, которая задает форму рантайма, не вшивая все решения в код:

```yaml
runtime:
  max_tool_hops: 3
  require_trace_id: true
  enable_background_updates: true
  default_model: gpt-5.4
  policy:
    precheck_required: true
  telemetry:
    emit_structured_events: true
  execution:
    gateway_required: true
  background:
    enabled: true
    resumable_runs: true
    allow_cancel: true
  capability_sessions:
    track_session_ids: true
    emit_progress_events: true
    support_reinit_on_expiry: true
```

Это полезно, потому что помогает держать контракт рантайма явным и переносимым между средами.

## 14. Частые ошибки

Очень типовые проблемы:

- оркестрация и адаптеры слеплены вместе;
- проверки политик вызываются не на каждом нужном пути;
- память подключена как случайный помощник;
- вызовы инструментов идут мимо реестра и шлюза;
- фоновые обновления отсутствуют;
- телеметрия добавлена по остаточному принципу;
- длинная работа спрятана за ретраями, а не смоделирована явно;
- фоновое исполнение вроде бы есть, но операторы не могут нормально опрашивать, продолжать или отменять работу.

То есть система вроде бы “работает”, но форма рантайма уже мешает ее взрослению.

## 15. Быстрый тест зрелости для базовой среды исполнения

Команде не стоит думать, что у нее уже есть эталонный рантайм, только потому, что у нее есть рабочий агент, несколько модулей и успешные демо.

Более сильная планка такая:

- оркестрация, политики, память, исполнение и телеметрия видимы как отдельные слои;
- контекст запуска с самого начала несет идентичность и контрольные метаданные;
- исполнение возможностей идет через контракты, а не через прямые вызовы адаптеров;
- трассировка и фоновые точки подключения встроены в базовый путь, а не появляются как переделка;
- длинная работа имеет явную модель статусов и продолжения, а не прячется в скрытых ретраях;
- один запуск можно объяснить как устойчивый каркас, а не как рассыпанную локальную логику.

Если большинство этих условий не выполняется, у команды уже может быть реализация, но реального чертежа базовой среды исполнения у нее пока нет.

## 16. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Видны ли отдельные слои оркестрации, политик, памяти, исполнения и телеметрии?
- Есть ли единый контекст запуска с метаданными клиента и принципала?
- Есть ли реестр возможностей вместо прямых вызовов?
- Встроены ли точки подключения трассировки в базовый путь?
- Есть ли безопасная точка для фоновых обновлений?
- Можно ли длинную работу явно поставить в очередь, наблюдать, продолжить и отменить?
- Можно ли объяснить поток одного запуска без чтения десяти файлов сразу?

Если на несколько вопросов подряд ответ “нет”, у тебя пока не эталонный рантайм, а просто ранняя интеграция модели в продукт.

!!! summary "Шаблон завершения главы"
    **Что запомнить:** эталонная среда исполнения нужна как проверяемая форма архитектуры, а не как обязательный промышленный программный каркас.

    **Типичные ошибки:** смешивать оркестрацию с бизнес-адаптерами; не поддерживать долгие запуски и возобновление; оставлять сессии инструментов вне контроля.

    **Что проверить в своей системе:** где хранится состояние запуска; как возобновляется прерванная работа; какие контракты отделяют оркестратор, политику, инструменты и телеметрию.

    **Сопутствующие материалы:** используй эталонный пакет, схему трассировки и практические кейсы как способ проверить архитектуру на исполнимость.

    **Что читать дальше:** переходи к Главе 17, чтобы добавить слой политик, каталог возможностей и путь подтверждения.

## 17. Что делать дальше

Сначала зафиксируй форму рантайма, а потом добавляй поверх него слой политик и контракты возможностей.

Следующий логичный шаг в части VII: сделать поверх этой схемы явный слой политик и каталог возможностей, чтобы эталонная реализация стала уже почти эксплуатационным каркасом.

- [Глава 15. Золотые пути, общие шлюзы и антизоопарк-подходы](../part-vi/chapter-15.md)
- [Глава 17. Слой политик и каталог возможностей](chapter-17.md)
- [Часть VII. Эталонная реализация](index.md)
- [Источники](../../appendix/sources.md)

[^anthropic-claude-code-best-practices]: Anthropic, [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices).

[^anthropic]: Anthropic, [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents).

[^aws-stateful-mcp]: [AWS, Introducing stateful MCP client capabilities on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-stateful-mcp-client-capabilities-on-amazon-bedrock-agentcore-runtime/)

[^aws-agentcore-agentops]: AWS, [AgentOps: Operationalize agentic AI at scale with Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/agentops-operationalize-agentic-ai-at-scale-with-amazon-bedrock-agentcore/)

[^aws-agentcore-coding-agents]: AWS, [It’s safe to close your laptop now: Hosting coding agents on Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/its-safe-to-close-your-laptop-now-hosting-coding-agents-on-amazon-bedrock-agentcore/)

[^github-third-party-coding-agent-validation]: GitHub Changelog, [Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/)

[^openai-background]: [OpenAI, Background mode](https://developers.openai.com/api/docs/guides/background)

[^openai-agents-transforming-work]: OpenAI, [How agents are transforming work](https://openai.com/index/how-agents-are-transforming-work/)

[^openai-codex-maxxing]: OpenAI, [Codex-maxxing for long-running work](https://openai.com/index/codex-maxxing-long-running-work/)

[^langgraph-persistence]: [LangGraph, Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

[^google-agent-executor]: Google, [Introducing Agent Executor: a new runtime for AI agents](https://developers.googleblog.com/en/introducing-agent-executor-a-new-runtime-for-ai-agents/).

[^langchain-production-runtime]: LangChain, [The Runtime Behind Production Deep Agents](https://www.langchain.com/blog/runtime-behind-production-deep-agents).

[^anthropic-harness]: Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

[^anthropic-managed-agents]: Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents).

[^anthropic-rsi]: Anthropic Institute, [When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement).

[^cloudflare-vulnerability-harness]: Cloudflare Blog, [Build your own vulnerability harness](https://blog.cloudflare.com/build-your-own-vulnerability-harness/).

[^cloudflare-flue-platform]: Cloudflare Blog, [Bringing more agent harnesses and frameworks to Cloudflare, starting with Flue](https://blog.cloudflare.com/agents-platform-flue-sdk/).

[^cloudflare-project-think]: Cloudflare Blog, [Project Think: building the next generation of AI agents on Cloudflare](https://blog.cloudflare.com/project-think/).

[^cloudflare-websockets]: [Cloudflare Agents SDK, WebSockets](https://developers.cloudflare.com/agents/api-reference/websockets/)

[^cloudflare-fibers]: [Cloudflare Agents SDK, Durable execution with fibers](https://developers.cloudflare.com/agents/runtime/execution/durable-execution/)

[^cloudflare-outbound-connections]: Cloudflare Changelog, [Outbound connections keep Durable Objects alive](https://developers.cloudflare.com/changelog/post/2026-06-19-outbound-connections-keep-dos-alive/)

[^cloudflare-workflows]: [Cloudflare Agents SDK, Workflows](https://developers.cloudflare.com/agents/concepts/workflows/)

[^cloudflare-dynamic-workflows]: Cloudflare Blog, [Introducing Dynamic Workflows: durable execution that follows the user, not the other way around](https://blog.cloudflare.com/dynamic-workflows/)

[^cloudflare-workflow-rollbacks]: Cloudflare Blog, [How we built saga rollbacks for Cloudflare Workflows](https://blog.cloudflare.com/rollbacks-for-workflows/)

[^cloudflare-schedule]: [Cloudflare Agents SDK, Schedule tasks](https://developers.cloudflare.com/agents/api-reference/schedule-tasks/)

[^cloudflare-agents]: [Cloudflare, Build Agents on Cloudflare](https://developers.cloudflare.com/agents/)

[^cloudflare-long-running-agents]: [Cloudflare Agents SDK, Long-running agents](https://developers.cloudflare.com/agents/concepts/agentic-patterns/long-running-agents/)

[^cloudflare-agents-sdk-0161]: Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/post/2026-06-16-agents-sdk-v0161/)
[^cloudflare-agents-background-subagents]: Cloudflare Changelog, [Agents SDK adds background sub-agents and a unified turn entry point](https://developers.cloudflare.com/changelog/product-group/ai/)
[^cloudflare-agents-recovery]: Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/product-group/ai/)

[^cloudflare-temporary-accounts]: Cloudflare Changelog, [Temporary Accounts: From agent deployments to claimed accounts](https://developers.cloudflare.com/changelog/2026-06-22-temporary-accounts/)

[^github-copilot-automations]: GitHub Changelog, [Schedule and automate tasks with Copilot cloud agent](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/)

[^github-copilot-agents-md]: GitHub Changelog, [Copilot code review: AGENTS.md support and UI improvements](https://github.blog/changelog/2026-06-18-copilot-code-review-agents-md-support-and-ui-improvements/)

[^github-copilot-byok]: GitHub Changelog, [GitHub Copilot app support for BYOK](https://github.blog/changelog/2026-06-23-github-copilot-app-support-for-byok/)

[^openai-sandbox-agents]: OpenAI Agents SDK, [Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/), [Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/), [Sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/) и [Agent memory](https://openai.github.io/openai-agents-python/sandbox/memory/)

[^openai-computer-environment]: OpenAI, [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/)
