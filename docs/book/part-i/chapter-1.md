# Глава 1. Современная безопасная архитектура

## 1. От надежного агента к безопасной платформе

Статья Дмитрия Викулина хорошо ставит стартовый вопрос: из каких блоков вообще состоит надежный агент.[^vikulin] Но если ты хочешь довести такую систему до production в 2026 году, этого уже мало. На практике у сильных команд сходится другая картина:

- сначала выбирается **самый простой исполнимый паттерн**;
- опасные действия выводятся в отдельный **control plane**;
- автономность допускается только там, где есть **policy, telemetry и rollback boundary**.[^anthropic][^openai-evals][^langgraph-durable]

Поэтому современную систему удобнее проектировать не как “одного умного агента”, а как **платформу безопасного агентного выполнения**. Это чуть менее романтично, но зато намного надежнее.

## 2. Принципы архитектуры

### 2.1. Workflow по умолчанию, агентность по необходимости

Anthropic прямо разделяет `workflows` и `agents` и рекомендует начинать с более простого варианта.[^anthropic] Это хороший базовый принцип для платформы:

- если путь выполнения известен, пиши workflow;
- если нужен выбор инструмента в пределах узкого контура, используйте single-agent loop;
- если задача естественно делится на независимые подзадачи, вводите subagents;
- если нельзя объяснить, зачем нужна автономность, значит она пока не нужна.

### 2.2. Все опасные операции идут через policy boundary

Модель не должна напрямую читать секреты, писать в критичные системы или отправлять внешние запросы. Любой доступ к модели, памяти и инструментам должен проходить через шлюзы с едиными проверками:

- аутентификация и авторизация;
- redaction и data classification;
- prompt injection checks;
- human approval для чувствительных действий;
- полное трассирование решения и факта выполнения.[^owasp][^anthropic-security][^nist-genai]

### 2.3. Состояние должно быть явным и возобновляемым

Долгие агентные задачи ломаются не только из-за модели, но и из-за потери состояния. LangGraph в своей документации прямо делает durable execution и checkpoints центральной частью orchestration runtime.[^langgraph-durable] Это означает:

- состояние задачи хранится вне процесса;
- шаги делаются идемпотентными;
- сайд-эффекты изолируются;
- выполнение можно возобновить после падения или паузы на human approval.

### 2.4. Observability важнее "магии"

OpenAI и другие платформы все сильнее смещают акцент на traces, evals и trace grading, потому что без них агент остается черным ящиком.[^openai-sdk][^openai-evals] Production-команда должна видеть:

- какой план построил агент;
- какие инструменты были вызваны;
- какой контекст был подан в модель;
- где именно качество деградировало;
- сколько стоил каждый шаг по latency и tokens.

Прежде чем идти дальше, полезно увидеть всю систему одним взглядом. Ниже не “идеальная схема на все случаи жизни”, а хороший baseline, от которого можно отталкиваться.

<div class="diagram-card">
<p>Референсная схема безопасной агентной платформы</p>

``` mermaid
flowchart TB
    user["Пользователь / API / Event"] --> interface["Interface layer"]
    interface --> identity["Identity & session layer"]
    identity --> control["Agent control plane"]
    control --> runtime["Orchestration runtime"]
    runtime --> cognition["Cognition plane"]
    runtime --> memory["Memory & knowledge plane"]
    runtime --> tools["Tool execution plane"]
    runtime --> telemetry["Telemetry & eval plane"]
    tools --> external["Внешние системы / MCP / SaaS"]
    memory --> stores["Vector DB / KB / profile memory"]
    control --> approval["Approval / policy / quotas"]
    telemetry --> audit["Traces / metrics / audit"]
```

</div>

## 3. Референсная архитектура

Ниже схема, которую можно брать как baseline для корпоративной платформы.

| Слой | Назначение | Почему обязателен |
| --- | --- | --- |
| Interface layer | Чат, API, event ingestion, webhooks | Отделяет пользовательские каналы от runtime |
| Identity and session layer | Пользователь, сервисный аккаунт, thread, tenant, request scope | Нужен для IAM, audit и изоляции |
| Agent control plane | Policies, approvals, model policies, tool catalog, quotas | Здесь живет управляемость |
| Orchestration runtime | Workflow graph, planner, router, subagents, checkpoints | Здесь исполняется задача |
| Cognition plane | Model router, prompt compiler, structured outputs, validators | Модель становится компонентом, а не центром мира |
| Memory and knowledge plane | Short-term state, long-term memory, retrieval, summaries | Ограничивает разрастание контекста |
| Tool execution plane | Sandboxed tools, MCP servers, connectors, side-effect isolation | Снижает blast radius |
| Telemetry and eval plane | Traces, metrics, logs, datasets, graders, regression gates | Делает качество измеримым |

## 4. Как эти слои взаимодействуют

### 4.1. Interface layer

Входящий запрос не должен сразу попадать в оркестратор. Сначала он получает:

- `tenant_id`;
- `principal`;
- класс риска;
- ссылку на политику доступа;
- идентификатор сессии и трассы.

Это делает аудит и разбор инцидентов возможными уже с первого шага.

Если хочется совсем короткой инженерной формулы, то вот она: **каждый запрос должен войти в систему уже не “просто сообщением”, а нормализованным событием с контекстом доступа и трассировки**.

### 4.2. Agent control plane

Это главный слой, которого не хватает в большинстве "демо-архитектур". Он отвечает не за интеллект, а за **право выполнять интеллектом действия**.

Минимально здесь должны жить:

- каталог моделей с разрешенными use cases;
- каталог инструментов и требуемые уровни approval;
- правила redaction и data loss prevention;
- лимиты по бюджету, latency и глубине агентного цикла;
- environment policies: dev, staging, prod.

Пример policy-as-code:

```yaml
agent_policy:
  model_access:
    allowed_models: ["gpt-5.4", "gpt-5-mini", "claude-sonnet"]
    deny_if_contains: ["pci_raw", "prod_secrets"]
  tools:
    read_kb:
      approval: none
    jira_create_ticket:
      approval: manager
    prod_db_write:
      approval: security_and_owner
      allowed_environments: ["staging"]
  runtime:
    max_steps: 24
    max_parallel_subagents: 4
    require_checkpoint_every_step: true
```

А вот так тот же принцип обычно выглядит в runtime-коде:

```python
from dataclasses import dataclass


@dataclass
class ToolRequest:
    tool_name: str
    actor_id: str
    risk_class: str
    payload: dict


def execute_tool(request: ToolRequest, policy_engine, approval_service, gateway):
    decision = policy_engine.evaluate(request)
    if not decision.allowed:
        raise PermissionError(decision.reason)

    if decision.requires_approval:
        approval_service.require_human_signoff(request, decision)

    return gateway.call(request.tool_name, request.payload)
```

Смысл у этого куска кода очень приземленный: модель может что-то предложить, но **право исполнить действие все равно живет не в модели, а в policy/gateway слое**.

### 4.3. Orchestration runtime

Этот слой выбирает паттерн исполнения:

- deterministic workflow для регламентных сценариев;
- routed workflow для выбора ветки;
- plan-and-execute для длинных задач;
- planner + subagents для независимых подзадач;
- HITL interrupts для операций с высоким риском.[^langgraph-hitl][^openai-builder]

Ключевая инженерная мысль: orchestration runtime должен быть **скучным**. Чем больше в нем "магии", тем сложнее предсказывать стоимость, поведение и отказ.

Это один из тех советов, которые сначала звучат слишком простыми, а потом внезапно экономят тебе месяцы жизни.

### 4.4. Cognition plane

Здесь не одна "большая модель", а управляемый набор компонентов:

- planner model;
- executor model;
- classifier/extractor model;
- structured output validator;
- fallback model на случай деградации.

Такая каскадная схема соответствует практике model routing и graceful degradation: дорогой reasoning используется там, где он реально нужен, а не на каждом шаге.[^vikulin][^openai-models]

### 4.5. Memory and knowledge plane

Современная память агента делится минимум на две зоны:

- **short-term state**: текущее состояние потока выполнения, tool results, промежуточные решения;
- **long-term memory**: пользовательские факты, профили, эпизоды, доменные артефакты.[^langgraph-memory]

Важно не смешивать память и knowledge retrieval:

- память хранит то, что система решила запомнить;
- retrieval достает релевантные документы из внешнего knowledge store;
- compaction и summarization уменьшают шум в активном контексте.

### 4.6. Tool execution plane

Инструмент нельзя считать "простым function call". Это отдельная зона риска.

Безопасный tool plane включает:

- sandbox или ограниченный execution environment;
- allowlist инструментов и параметров;
- запрет прямого сетевого доступа там, где он не нужен;
- отдельные секреты на каждый connector;
- идемпотентные адаптеры для систем с побочными эффектами.

Anthropic в документации по Claude Code отдельно подчеркивает архитектуру permissions, isolated contexts и manual approval для чувствительных сетевых и shell-операций.[^anthropic-security]

### 4.7. Telemetry and eval plane

Минимальный production-набор:

- distributed traces на каждый запуск;
- spans на вызовы моделей, retrieval и tools;
- стоимость и latency по каждому шагу;
- dataset с эталонными задачами;
- regression gates перед выкладкой нового prompt/policy/model combo.[^openai-evals][^openai-trace]

Если этого нет, команда не управляет агентом, а просто наблюдает за его поведением.

Ниже еще одна полезная картинка: как именно запрос проходит через систему, если ты строишь ее аккуратно.

<div class="diagram-card">
<p>Путь запроса через ключевые точки контроля</p>

``` mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant I as Interface
    participant C as Control plane
    participant R as Runtime
    participant T as Tool gateway
    participant A as Audit

    U->>I: Запрос
    I->>C: Нормализация + principal + tenant + risk
    C->>R: Разрешенный execution context
    R->>C: Запрос на model/tool action
    C->>T: Policy check / approval / quotas
    T-->>R: Разрешенный результат
    R->>A: Trace + step metadata
    R-->>U: Ответ
```

</div>

## 5. Где именно живет безопасность

Безопасность в агентной системе не должна концентрироваться в одном "guardrail service". Она распределяется по нескольким точкам:

| Точка контроля | Что проверяет |
| --- | --- |
| Pre-ingress filters | Явно опасный ввод, секреты, запрещенные вложения |
| Prompt assembly | Смешение инструкций и данных, untrusted content boundaries |
| Model gateway | Model allowlist, budget, moderation, routing |
| Retrieval gateway | Права на документы, tenant isolation, metadata filters |
| Tool gateway | Parameter validation, approval, side-effect class |
| Egress filters | Data leakage, PII, unsafe outbound content |
| Observability backend | Audit trail и расследование инцидентов |

Такой подход хорошо согласуется с рекомендациями OWASP по prompt injection prevention и с рамкой NIST AI RMF / GenAI Profile, где управление риском встроено во весь жизненный цикл, а не добавляется поверх.[^owasp][^nist-rmf][^nist-genai]

## 6. Референсный operating model

Чтобы платформа не превратилась в зоопарк, разделите ответственность так:

- platform team владеет gateways, policies, telemetry, golden templates;
- product teams владеют конкретными агентами и бизнес-логикой;
- security team задает risk classes, approval rules и контрольные точки;
- evaluation owner отвечает за наборы задач, graders и регрессионный контроль.

Google в корпоративных агентных платформах делает акцент именно на centralized visibility, governance и managed access, а не только на orchestration.[^google-agentspace][^google-agent-builder]

## 7. Практический вывод

Современный production-агент это не "LLM с инструментами". Это система, где:

1. оркестрация намеренно упрощена;
2. автономность ограничена политиками;
3. память отделена от retrieval;
4. инструменты исполняются через изолированный gateway;
5. каждый шаг виден через traces и evals;
6. человек может остановить или подтвердить опасное действие.

Если убрать любой из этих пунктов, ты почти наверняка получишь либо хрупкое демо, либо небезопасную систему.

## 8. Что читать дальше

- [План книги](../plan.md)
- [Часть I. Основания](index.md)
- [Выбор стека публикации](../../appendix/stack.md)
- [Источники и библиография](../../appendix/sources.md)

[^vikulin]: [Дмитрий Викулин, «Архитектура надежных AI-агентов»](https://vikulin.ai/library/tpost/ai_agent_architecture)
[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^anthropic-security]: [Anthropic, Claude Code Security](https://docs.anthropic.com/en/docs/claude-code/security)
[^owasp]: [OWASP, LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
[^nist-rmf]: [NIST, AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
[^nist-genai]: [NIST, AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
[^langgraph-durable]: [LangGraph, Durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
[^langgraph-memory]: [LangGraph, Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
[^langgraph-hitl]: [LangChain Deep Agents, Human-in-the-loop](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop)
[^openai-sdk]: [OpenAI, Agents SDK](https://developers.openai.com/api/docs/guides/agents-sdk)
[^openai-evals]: [OpenAI, Agent evals](https://platform.openai.com/docs/guides/agent-evals)
[^openai-trace]: [OpenAI, Trace grading](https://platform.openai.com/docs/guides/trace-grading)
[^openai-builder]: [OpenAI, Agent Builder](https://platform.openai.com/docs/guides/agent-builder)
[^openai-models]: [OpenAI, Models](https://developers.openai.com/api/docs/models)
[^google-agentspace]: [Google Agentspace](https://cloud.google.com/products/agentspace)
[^google-agent-builder]: [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder)
