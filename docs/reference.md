# Справочный слой

Если книга объясняет, **почему** безопасная агентная система должна быть устроена именно так, то справочный слой показывает, **какие артефакты, схемы и правила должны у нее быть**.

Этот слой намеренно вспомогательный, а не основной. Он нужен, чтобы закреплять аргумент книги в виде переиспользуемых инженерных материалов, а не заменять собой сам ход чтения книги.

Справочный слой полезен, если тебе нужно:

- быстро найти нужную контрактную страницу;
- подготовить архитектурное ревью или ревью раскатки;
- вытащить готовые артефакты для своей команды;
- перейти от главы книги к более прикладной инженерной форме.

Если ты только входишь в проект, лучше сначала читать книгу. Сюда стоит приходить тогда, когда тебе уже нужны поддерживающие схемы, чеклисты и контрактные страницы, которые стоят за основным аргументом.

Чего этот слой **не** обещает:

- он не заменяет сам читательский путь книги;
- он не объясняет основной причинно-следственный аргумент главу за главой;
- он не должен быть главным местом, где читатель осваивает компромиссы и границы между слоями.

## С чего начать

Для короткого входа начни с этих страниц:

1. [Глоссарий терминов](appendix/glossary.md)
2. [Шпаргалки](appendix/cheat-sheets.md)
3. [Эталонный пакет](appendix/reference-package.md)

!!! example "Артефактный маршрут support-triage"
    Если читаешь книгу через кейс support-triage, в справочном слое держи рядом страницы про traces, eval dataset, policy bundle, approval record, incident record, change rollout, lifecycle artifacts и registry operations. Именно эти контракты превращают duplicate-ticket incident из рассказа в проверяемый набор артефактов.

!!! note "Canonical case artifacts"
    Три canonical cases дают разные входы в справочный слой. **Support triage** опирается на approval record, policy bundle, trace schema и duplicate-ticket recovery evidence. **Internal knowledge assistant** требует memory/retrieval contract, freshness checks, access control и knowledge provenance. **Incident coordination** связывает incident record, escalation evidence, notification side effects, response ownership и post-incident learning.

## Схемы и контрактные страницы

- [Схема трасс и каталог событий](appendix/trace-schema.md)
- [Схема наборов для оценки и правил проверки](appendix/eval-schema.md)
- [Схема набора политик и контракта подтверждения](appendix/policy-bundle-schema.md)
- [Схема запроса на подтверждение и записи о решении](appendix/approval-schema.md)
- [Схема записи об инциденте и связи с postmortem](appendix/incident-record-schema.md)
- [Схема проверки изменений и шлюза раскатки](appendix/change-rollout-schema.md)
- [Схема артефактов жизненного цикла](appendix/lifecycle-artifact-schema.md)
- [Схема записей памяти и контракта извлечения](appendix/memory-retrieval-schema.md)
- [Причинная отладка и анализ первопричин для агентных систем](appendix/causal-debugging.md)
- [Паттерны оценки памяти для агентных систем](appendix/memory-eval-patterns.md)
- [Паттерны восстановления после сбоев инструментов в агентных системах](appendix/tool-failure-recovery.md)

## Практические страницы

- [Эталонный пакет](appendix/reference-package.md)
- [Практические кейсы](appendix/case-studies.md)
- [Шаблоны политик и проверочные списки по кейсам](appendix/policy-templates.md)
- [Плейбук реагирования на инциденты в агентных системах](appendix/incident-response-playbook.md)
- [Практическое руководство по registry агентов и inventory operations](appendix/registry-operations-handbook.md)
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

Самое простое правило такое:

- книгу используй для аргумента и последовательности;
- справочный слой используй для вспомогательных артефактов и прикладных деталей реализации.
