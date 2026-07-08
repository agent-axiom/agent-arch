# Шпаргалки

Эта страница нужна для быстрых рабочих проверок. Если тебе не хочется перечитывать целую часть книги перед ревью дизайна, запуском агента или обсуждением с командой, начни отсюда.

!!! note "Канонические сценарии для проверочных списков (Canonical checklist cases)"
    Используй эти блоки проверок как быстрый маршрут (fast route) для трех канонических сценариев (canonical cases). **Триаж обращений поддержки (Support triage)** начинается с безопасности (safety), шлюза инструментов (tool gateway), согласований (approval), идемпотентности (idempotency) и проверок раскатки (rollout checks). **Внутренний ассистент знаний (Internal knowledge assistant)** начинается с памяти (memory), поиска (retrieval), привязки к источникам (source grounding), границ арендатора (tenant boundary) и проверок наблюдаемости (observability checks). **Координация инцидентов (Incident coordination)** начинается с раскатки, наблюдаемости, разбора инцидента (incident review), владения ответом (response ownership) и обучения после инцидента (post-incident learning checks).

## Safety checklist

- Есть ли у агента явные trust boundaries между вводом пользователя, памятью, инструментами и внешними системами?
- Различаете ли вы prompt injection, jailbreak и action hallucination, а не сводите все к одной “LLM risk” категории?
- Есть ли policy gate перед каждым чувствительным действием, а не только перед вызовом модели?
- Разделены ли low-risk и high-risk инструменты?
- Есть ли approval gate для действий с необратимым side effect?
- Зафиксированы ли allowed egress destinations и network access profile?
- Пишется ли audit trail для policy decisions, approvals и tool execution?
- Есть ли понятный stop condition для run loop?

Читать дальше:

- [Глава 3. Контур безопасности и границы доверия](../book/part-ii/chapter-3.md)
- [Глава 4. Инструментальный шлюз, подтверждения и журнал аудита](../book/part-ii/chapter-4.md)

## Memory checklist

- Разделены ли short-term, long-term и profile memory?
- Учитывает ли retrieval semantic gap между пользовательским языком и языком документов?
- Если вы используете query rewriting или HyDE, ясно ли, что это retrieval aid, а не новый источник “фактов”?
- Есть ли разные правила для memory read и memory write?
- Хранится ли provenance у persistent records?
- Есть ли policy для того, что разрешено записывать в память?
- Есть ли compaction или background maintenance path?
- Ограничен ли retrieval по объему и релевантности?
- Пытаетесь ли вы сначала улучшить RAG и freshness corpus, прежде чем идти в training?
- Есть ли понятная deletion или revision strategy?

Читать дальше:

- [Глава 5. Зачем агенту память и почему она опасна](../book/part-iii/chapter-5.md)
- [Глава 7. Извлечение контекста, уплотнение и фоновые обновления](../book/part-iii/chapter-7.md)

## Rollout checklist

- Есть ли owner у агента, а не только команда “вообще”?
- Есть ли минимальный eval baseline до запуска?
- Есть ли rollout gate с safety, observability и approval requirements?
- Понятно ли, какие сценарии считаются blocking failures?
- Зафиксирован ли latency budget с точки зрения пользователя, а не только p95 модели?
- Есть ли runbook на отказ, denial и approval backlog?
- Есть ли канал для incident review и postmortem?
- Можно ли быстро отключить high-risk capability без полной остановки системы?

Читать дальше:

- [Глава 12. SLO для агентных систем](../book/part-v/chapter-12.md)
- [Глава 18. Чеклист промышленного запуска](../book/part-vii/chapter-18.md)

## Runtime durability checklist

- Есть ли стабильный `agent_instance_id`, если агент привязан к делу, комнате, проекту, устройству или tenant workspace?
- Разделены ли `agent_instance_id`, `run_id`, `session_id`, `trace_id` и connection/websocket state?
- Хранится ли `durable_state_version`, чтобы resume не продолжал устаревшее или “похожее” состояние?
- Есть ли idempotency/correlation key для webhook, email, Slack command и других programmatic turns?
- Можно ли увидеть, какие scheduled tasks могут разбудить agent instance, с каким payload schema, timezone и overlap policy?
- Проверен ли recovery path для прерванного tool call, background run или recoverable internal task?
- Есть ли inspect/cancel/status API для фоновой работы, а не только progress-сообщения пользователю?
- Пишутся ли lifecycle events: accept, sleep/hibernate, wake, resume, cancel, recover, state migration?
- Не превращается ли local durable state в скрытую profile memory, tenant knowledge, secrets или audit log?
- Есть ли migration/deletion/export story для durable state, если меняется версия агента или закрывается workspace?

Читать дальше:

- [Глава 16. Базовая схема среды исполнения](../book/part-vii/chapter-16.md)
- [Глава 10. Идемпотентность, повторы, лимиты запросов и границы отката](../book/part-iv/chapter-10.md)
- [Схема трассировки](trace-schema.md)

## Observability checklist

- Есть ли trace_id у каждого запуска?
- Есть ли базовые spans для retrieval, model step, tool execution, approval и memory write?
- Есть ли structured events, а не только сырые логи?
- Видно ли, какой policy decision принял gateway?
- Видно ли, какой tool principal исполнил side effect?
- Можно ли отличить success, denied, approval_wait и failure?
- Есть ли способ агрегировать runs в session-level или eval-level summaries?
- Если используется LLM-as-a-judge, откалиброван ли judge против human review и outcome checks?
- Не меняете ли вы одновременно model и prompt там, где нужен причинный вывод по eval results?

Читать дальше:

- [Глава 11. Трассы, спаны и структурированные события](../book/part-v/chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)

## Orchestration pattern checklist

- Можно ли решить задачу прямым вызовом модели вместо agent loop?
- Если нужен agent loop, достаточно ли одного агента с инструментами и лимитами итераций?
- Что именно оправдывает multi-agent: доменная граница, параллельные независимые ветки или отдельная security boundary?
- Для `sequential` понятны ли порядок, зависимость шагов и rollback при ошибке раннего шага?
- Для `concurrent` есть ли budget, aggregation policy и conflict-resolution rule?
- Для `group chat` понятно ли, кто owner результата и как ограничивается transcript/context growth?
- Для `handoff` есть ли transfer packet с goal, constraints, owner, policy context и trace link?
- Для `magentic`/динамической оркестрации есть ли hard limits, route trace, stop condition и отдельное eval coverage?
- Зафиксированы ли latency/cost/security/debuggability trade-offs до запуска?

Читать дальше:

- [Практика. Координатор и передача управления](../book/part-i/practical-manager-handoffs.md)
- [Глава 15. Золотые пути, общие шлюзы и антизоопарк-подходы](../book/part-vi/chapter-15.md)

## Tool gateway checklist

- У каждой capability есть owner, risk tier и approved inventory status?
- Ясно ли, read это tool или write tool?
- Не показываете ли вы модели слишком большой каталог tools вместо узкого релевантного поднабора?
- Есть ли execution profile: sandbox, network access, allowed egress?
- Проверяет ли gateway actor identity и policy до execution?
- Есть ли idempotency semantics и retry policy?
- Понятно ли, когда нужен approval, а когда tool может исполниться автоматически?
- Есть ли audit trail на каждое внешнее действие?
- Понимает ли команда роли MCP host, client и server, а не смешивает их в одну “интеграцию”?

Читать дальше:

- [Глава 8. Модель выполнения и каталог инструментов](../book/part-iv/chapter-8.md)
- [Глава 9. Песочница выполнения и MCP как интеграционный контракт](../book/part-iv/chapter-9.md)
- [Глава 10. Идемпотентность, повторы, лимиты запросов и границы отката](../book/part-iv/chapter-10.md)

## Что делать дальше

- Перед design review: быстро пройти safety, memory и tool gateway блоки.
- Перед запуском: пройти rollout и observability блоки.
- Во время incident review: использовать observability и safety блоки как каркас разбора.

- [С чего начать](../start-here.md)
- [Глоссарий терминов](glossary.md)
- [Шаблоны политик и проверочные списки по кейсам](policy-templates.md)
