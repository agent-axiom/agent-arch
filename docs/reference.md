# Справочный слой

Если книга объясняет, **почему** безопасная агентная система должна быть устроена именно так, то справочный слой показывает, **какие артефакты, схемы и правила должны у нее быть**.

Справочный слой полезен, если тебе нужно:

- быстро найти нужную контрактную страницу;
- подготовить design review или rollout review;
- вытащить готовые артефакты для своей команды;
- перейти от главы книги к более прикладной инженерной форме.

## С чего начать

Для короткого входа начни с этих страниц:

1. [Глоссарий терминов](appendix/glossary.md)
2. [Шпаргалки](appendix/cheat-sheets.md)
3. [Справочный пакет](appendix/reference-package.md)

## Схемы и контрактные страницы

- [Схема трасс и каталог событий](appendix/trace-schema.md)
- [Схема наборов для оценки и правил проверки](appendix/eval-schema.md)
- [Схема набора политик и контракта подтверждения](appendix/policy-bundle-schema.md)
- [Схема запроса на подтверждение и записи о решении](appendix/approval-schema.md)
- [Схема incident record и postmortem linkage](appendix/incident-record-schema.md)
- [Схема проверки изменений и шлюза раскатки](appendix/change-rollout-schema.md)
- [Схема артефактов жизненного цикла](appendix/lifecycle-artifact-schema.md)
- [Схема записей памяти и контракта извлечения](appendix/memory-retrieval-schema.md)
- [Causal debugging и root-cause analysis для agent systems](appendix/causal-debugging.md)
- [Memory eval patterns для agent systems](appendix/memory-eval-patterns.md)
- [Tool failure recovery patterns для agent systems](appendix/tool-failure-recovery.md)

## Практические страницы

- [Справочный пакет](appendix/reference-package.md)
- [Практические кейсы](appendix/case-studies.md)
- [Шаблоны политик и проверочные списки по кейсам](appendix/policy-templates.md)
- [Плейбук реагирования на инциденты в агентных системах](appendix/incident-response-playbook.md)
- [Handbook по agent registry и inventory operations](appendix/registry-operations-handbook.md)
- [Шаблон postmortem для агентных систем](appendix/postmortem-template.md)

## Быстрые маршруты по темам

Если тебе нужен не весь reference layer, а короткий вход в конкретный вопрос, начни так:

- Tool catalog, semantic tool filtering, read/write taxonomy: [Глава 8. Модель выполнения и каталог инструментов](book/part-iv/chapter-8.md)
- MCP host/client/server, capability transport, sandbox boundary: [Глава 9. Песочница выполнения и MCP как интеграционный контракт](book/part-iv/chapter-9.md)
- Semantic gap, HyDE, RAG vs training: [Глава 7. Извлечение контекста, уплотнение и фоновые обновления](book/part-iii/chapter-7.md)
- Latency budget, fast path / slow path, routed pipeline: [Глава 12. SLO для агентных систем](book/part-v/chapter-12.md)
- LLM-as-a-judge, calibration и judge-human agreement: [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](book/part-v/chapter-13.md)

## Для дальнейшего чтения

- [С чего начать](start-here.md)
- [План книги](book/plan.md)
- [Исследовательский фронтир: память, наблюдаемость и надежность multi-agent систем](appendix/research-frontier.md)
- [Источники](appendix/sources.md)
