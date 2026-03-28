# Архитектура Безопасных AI-Агентов

Это книга для тебя, если ты хочешь строить не “магических агентов из презентации”, а спокойные, управляемые и безопасные production-системы.

> За отправную точку я беру статью Дмитрия Викулина о надежных AI-агентах, а дальше расширяю ее до платформенного уровня: с governance, policy enforcement, human approval, observability, evals и эксплуатационными контурами.

[Открыть план книги](book/plan.md){ .md-button .md-button--primary }
[Перейти к первой части](book/part-i/index.md){ .md-button }
[Посмотреть источники](appendix/sources.md){ .md-button }

## Что внутри

- Архитектурные паттерны: workflow, router, planner, subagents, human-in-the-loop.
- Безопасность: IAM, policy-as-code, prompt injection defenses, sandboxing, data boundaries.
- Надежность: checkpoints, idempotency, retries, graceful degradation.
- Прозрачность: traces, metrics, evals, regression control.
- Платформенный подход: gateways, shared runtime, knowledge plane, tool plane, control plane.

## Главная идея

Самая частая ошибка в агентных системах простая: сначала все пытаются добиться автономности, и только потом вспоминают про управляемость. На практике лучше работает другой путь:

1. Сначала ты строишь **предсказуемый workflow**.
2. Потом добавляешь автономность **локально и измеримо**.
3. Все опасные действия пропускаешь через **policy, approval и tracing**.
4. Качество держишь не обещаниями модели, а **evals и telemetry**.

## С чего обычно лучше начинать

Ниже интерактивная карта приоритетов. Это не “истина в последней инстанции”, а удобная шпаргалка: если проект только стартует, сначала почти всегда выгоднее инвестировать в контроль, безопасность и наблюдаемость, а не в максимальную автономность.

<div class="plot-card" data-plot="agent-priority"></div>

## Как выглядит хорошая траектория

Если коротко, ламповая и рабочая траектория такая:

- сначала сделать хороший request path;
- затем ввести policy boundary;
- после этого подключить tools через gateway;
- и только потом расширять память, planner и уровень автономности.

## Почему для публикации выбран MkDocs

`MkDocs + Material for MkDocs` в 2026 году все еще выглядит прагматичным выбором: стек активно используется, быстро собирается, хорошо работает с Markdown-first книгами и естественно дружит с Python-окружением на `uv`.[^mkdocs][^material][^uv]

Если позже захочется больше кастомного UI и MDX-компонентов, хорошим следующим кандидатом будет `Astro Starlight`. Но для первой версии книги, которую важно быстро публиковать и спокойно поддерживать, Python-first стек проще и надежнее.[^starlight]

## Откуда собрана архитектура

- Исходная рамка по блокам агента: [vikulin.ai](https://vikulin.ai/library/tpost/ai_agent_architecture)
- Решение "workflow before agents": [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- Durable execution, memory и HITL: [LangGraph docs](https://docs.langchain.com/oss/javascript/langgraph)
- Tracing и agent evals: [OpenAI docs](https://developers.openai.com/api/docs/guides/agents-sdk)
- Risk management и security controls: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [OWASP Prompt Injection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

[^mkdocs]: [MkDocs User Guide](https://www.mkdocs.org/).
[^material]: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
[^uv]: [uv project guide](https://docs.astral.sh/uv/guides/projects/).
[^starlight]: [Starlight documentation](https://starlight.astro.build/).
