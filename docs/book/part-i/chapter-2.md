# Глава 2. Референсная архитектура безопасного агента

## 1. Зачем вообще нужна референсная схема

После первой главы у тебя уже должна была появиться интуиция, почему “просто умный агент” быстро становится хрупким. Следующий шаг более приземленный: понять, из каких слоев должна состоять система, если ты хочешь, чтобы она жила дольше одной презентации.

Именно для этого нужна референсная архитектура. Не как догма, а как baseline.

При этом полезно держать в голове очень простую стартовую рамку из практического гайда OpenAI: минимальная agent system обычно состоит из трех вещей.[^openai-practical]

- `model`, которая рассуждает и выбирает следующий шаг;
- `tools`, которые дают доступ к данным и действиям;
- `instructions`, которые объясняют системе, как именно себя вести.

Дальше к этой тройке уже наращиваются control plane, memory, policy и telemetry. Но если ты теряешь эту основу из вида, архитектура начинает раздуваться быстрее, чем становится понятнее.

## 2. Вид сверху: из чего состоит платформа

Ниже схема, на которую удобно опираться как на стартовую карту.

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

## 3. Что происходит на входе

Входящий запрос не должен просто “лететь в модель”. Сначала он должен превратиться в нормализованное событие с контекстом.

Минимально полезный набор:

- `tenant_id`;
- `principal`;
- класс риска;
- ссылка на политику доступа;
- идентификатор сессии;
- trace id.

Если говорить совсем коротко: **запрос должен входить в систему уже не как сообщение, а как управляемый execution context**.

## 4. Почему control plane важнее, чем кажется

Это тот слой, которого чаще всего не хватает в демо-архитектурах.

Он отвечает не за интеллект, а за право системы действовать:

- какие модели можно использовать;
- какие tools доступны;
- какие approvals нужны;
- какие лимиты действуют;
- какие правила активны в dev, staging и prod.

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

## 5. Где живет исполнение

Orchestration runtime выбирает паттерн выполнения:

- deterministic workflow для регламентных сценариев;
- routed workflow для выбора ветки;
- plan-and-execute для длинных задач;
- planner + subagents для независимых подзадач;
- HITL interrupts для операций с высоким риском.[^langgraph-hitl][^openai-builder]

Лучшее свойство хорошего runtime очень неожиданное: он должен быть скучным.

Чем больше в нем “магии”, тем сложнее предсказывать стоимость, поведение и отказ.

### 5.1. Почему single-agent first это зрелая стратегия

Практический гайд OpenAI отдельно полезен тем, что не романтизирует multi-agent как default choice.[^openai-practical] Сначала один агент, потом разделение, если на это есть реальные причины.

Обычно сигнал к разделению появляется, когда:

- одному run уже тесно в одном контексте;
- разные подзадачи требуют разных tools и разных guardrails;
- ownership начинает делиться между командами;
- параллелизм реально сокращает latency или снижает cognitive load.

Если этих признаков нет, один агент с хорошим workflow graph почти всегда проще отлаживать, дешевле сопровождать и легче объяснять security-команде.

## 6. Почему cognition plane не равен одной модели

Полезнее думать не в терминах “у нас есть одна мощная модель”, а в терминах набора управляемых компонентов:

- planner model;
- executor model;
- classifier/extractor model;
- structured output validator;
- fallback model.

Это помогает и с качеством, и со стоимостью, и с graceful degradation.[^vikulin][^openai-models]

## 7. Память, знания и tools нельзя мешать в одну кучу

Тут удобно разделять хотя бы три независимые вещи:

- **short-term state**: текущее состояние потока выполнения;
- **long-term memory**: факты, профили, эпизоды;
- **retrieval**: доступ к внешним знаниям.[^langgraph-memory]

И отдельно еще одну:

- **tool execution**: реальные действия во внешнем мире.

Это разделение кажется бюрократией ровно до первого серьезного инцидента.

## 8. Как выглядит путь запроса через систему

Ниже более “живая” схема движения запроса.

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

## 9. Минимальный кодовый принцип

Если хочется увидеть это в очень простой форме, то вот практический шаблон:

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

Смысл тут очень простой: модель может предложить действие, но право на исполнение живет не в модели, а в gateway и policy слое.

## 10. Практический вывод

Хорошая агентная платформа держится на нескольких скучных, но очень ценных вещах:

- явный входной контекст;
- control plane;
- отдельный runtime;
- отдельный tool gateway;
- traces и evals;
- approvals там, где это нужно.

Как только все это собрано, можно спокойно переходить к более нервной теме: где именно у такой системы проходит security perimeter.

## 11. Что читать дальше

- [Глава 1. Почему агенту нужна платформа, а не магия](chapter-1.md)
- [Часть II. Контур безопасности](../part-ii/index.md)
- [Глава 3. Контур безопасности и границы доверия](../part-ii/chapter-3.md)

[^vikulin]: [Дмитрий Викулин, «Архитектура надежных AI-агентов»](https://vikulin.ai/library/tpost/ai_agent_architecture)
[^langgraph-memory]: [LangGraph, Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
[^langgraph-hitl]: [LangChain Deep Agents, Human-in-the-loop](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop)
[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^openai-builder]: [OpenAI, Agent Builder](https://platform.openai.com/docs/guides/agent-builder)
[^openai-models]: [OpenAI, Models](https://developers.openai.com/api/docs/models)
