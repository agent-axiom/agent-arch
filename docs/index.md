# Архитектура Безопасных AI-Агентов

Современная практическая книга для инженеров и лидеров платформ, которые хотят строить не демо-агентов, а управляемые production-системы.

> Эта книга берет за отправную точку статью Дмитрия Викулина о надежных AI-агентах и расширяет ее до платформенной архитектуры: с governance, policy enforcement, human approval, observability, evals и эксплуатационными контурами.

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

Самая частая ошибка в агентских системах: начинать с автономности, а не с управляемости. Практика Anthropic, OpenAI, LangGraph и корпоративных платформ Google показывает более устойчивый путь:

1. Сначала строится **предсказуемый workflow**.
2. Затем автономность добавляется **локально и измеримо**.
3. Все опасные действия проходят через **policy, approval и tracing**.
4. Качество держится не обещаниями модели, а **evals и telemetry**.

## Почему для публикации выбран MkDocs

`MkDocs + Material for MkDocs` в 2026 году не выглядит устаревшим стеком: он активно поддерживается, быстро собирается, хорошо работает с Markdown-first книгами и естественно сочетается с Python-окружением на `uv`.[^mkdocs][^material][^uv]

Альтернатива, если позже понадобится больше кастомных UI-компонентов и MDX, это `Astro Starlight`. Но для первой версии книги, которую важно быстро публиковать и поддерживать, Python-first стек проще и надежнее.[^starlight]

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

