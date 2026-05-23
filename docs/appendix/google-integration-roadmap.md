# План интеграции идей Google

Ниже я фиксирую отдельный план по тому, что именно имеет смысл взять из свежих материалов Google Cloud и аккуратно встроить в книгу. Идея простая: не дублировать уже написанные главы, а усилить их там, где у Google особенно сильны platform-grade аспекты.

## Почему вообще нужен отдельный план

У Google сейчас особенно полезны не общие разговоры про “агентов”, а четыре практические линии:

- production-ready platform view;
- sandboxed execution как инфраструктурный слой;
- agent identity, registry и governance;
- различение `MCP` и `A2A` как разных типов связности.

Это хорошо дополняет уже встроенные в книгу материалы OpenAI, Anthropic и LangGraph.

!!! note "Канонические сценарии Google-интеграции (Canonical Google integration cases)"
    Дорожная карта Google-интеграции (Google integration roadmap) полезнее, если проверять идеи платформенного уровня (platform-grade ideas) на трех канонических сценариях (canonical cases). **Триаж обращений поддержки (Support triage)** проверяет идентичность агента (agent identity), минимальные привилегии (least privilege), связь подтверждений и аудита (approval/audit linkage), профиль песочницы (sandbox profile), инструменты высокого риска (high-risk tools) и контроль дублей тикетов (duplicate-ticket controls). **Внутренний ассистент знаний (Internal knowledge assistant)** проверяет слои контекста (context layers), управление памятью (memory governance), политику поиска (retrieval policy), происхождение источников (source provenance) и доступ с учетом арендатора (tenant-aware access). **Координация инцидентов (Incident coordination)** проверяет управление реестром (registry governance), границы A2A (A2A boundaries), непрерывные контроли (continuous controls), шлюзы раскатки (rollout gates), трассы эскалации (escalation traces) и владение ответом (response ownership).

## План по шагам

### Шаг 1. Пять опор agent platform и context layers

Куда встраиваю:

- [Глава 2. Референсная архитектура безопасного агента](../book/part-i/chapter-2.md)

Что добавляю:

- рамку `framework -> model -> tools -> runtime -> trust`;
- context layers: static, session, turn, cached context;
- практический вывод про prompt budget и дисциплину контекста.

### Шаг 2. Agent identity и access boundaries

Куда встраиваю:

- [Глава 3. Контур безопасности и границы доверия](../book/part-ii/chapter-3.md)
- [Глава 4. Инструментальный шлюз, подтверждения и журнал аудита](../book/part-ii/chapter-4.md)

Что добавляю:

- machine identity и agent identity как отдельный слой;
- least privilege для tools, memory и external systems;
- связь identity с audit trail.

### Шаг 3. Memory governance и memory revisions

Куда встраиваю:

- [Глава 5. Зачем агенту память и почему она опасна](../book/part-iii/chapter-5.md)
- [Глава 6. Краткосрочная, долгосрочная и профильная память](../book/part-iii/chapter-6.md)

Что добавляю:

- явное различение read policy и write policy для memory;
- revisions и provenance для memory updates;
- мысль, что memory store сам по себе тоже должен быть управляемым subsystem.

### Шаг 4. Sandbox execution как инфраструктурный слой

Куда встраиваю:

- [Глава 9. Песочница выполнения и MCP как интеграционный контракт](../book/part-iv/chapter-9.md)

Что добавляю:

- различие logical isolation, process isolation и runtime isolation;
- ephemeral sandboxes;
- network egress controls и artifact discipline;
- практический checklist для high-risk tools.

### Шаг 5. MCP для tools, A2A для agents

Куда встраиваю:

- [Глава 9. Песочница выполнения и MCP как интеграционный контракт](../book/part-iv/chapter-9.md)
- отдельный практический блок в Part IV

Что добавляю:

- четкое разведение `MCP` и `A2A`;
- когда нужен capability contract, а когда межагентное взаимодействие;
- критерии, когда не стоит тащить multi-agent coordination слишком рано.

### Шаг 6. User simulator и continuous eval loop

Куда встраиваю:

- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)

Что добавляю:

- user simulator как отдельный паттерн evals;
- continuous grading поверх traces;
- связь eval loop с rollout gates.

### Шаг 7. Registry, approved inventory и organizational controls

Куда встраиваю:

- [Глава 14. Платформенная команда и продуктовые команды](../book/part-vi/chapter-14.md)
- [Глава 15. Золотые пути, общие шлюзы и антизоопарк-подходы](../book/part-vi/chapter-15.md)

Что добавляю:

- approved registry of agents, tools and connectors;
- platform inventory как часть governance;
- continuous controls вместо разовой ручной проверки.

### Шаг 8. Усиление reference implementation

Куда встраиваю:

- [Глава 16. Базовая схема рантайма](../book/part-vii/chapter-16.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
- `agent_runtime_ref`

Что добавляю:

- context layers в runtime;
- agent identity;
- memory provenance;
- sandbox profile;
- registry-like inventory of capabilities.

## Приоритет

Если брать по реальной полезности для читателя, порядок такой:

1. context layers;
2. identity;
3. sandbox infrastructure;
4. MCP vs A2A;
5. memory governance;
6. user simulator;
7. registry and continuous controls;
8. runtime uplift.

## Источники

- Google Cloud, [Achieve agentic productivity with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder)
- Google Cloud, [More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
- Google Cloud, [Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
- Google Cloud Architecture Center, [Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
- Google Cloud, [How Google secures AI Agents](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents)
- Google Cloud, [Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)
- Google Cloud, [Building Connected Agents with MCP and A2A](https://cloud.google.com/blog/topics/developers-practitioners/building-connected-agents-with-mcp-and-a2a)
- Google Cloud, [Recommended AI Controls framework](https://cloud.google.com/blog/products/identity-security/audit-smarter-introducing-our-recommended-ai-controls-framework)
