# Что нового

Эта страница нужна как короткий журнал крупных улучшений книги и опорного пакета. Она не заменяет git history, а помогает читателю быстро увидеть, насколько проект живой и какие слои уже появились.

_Актуально на 29 апреля 2026 года._

## Book

### Часть VIII про жизненный цикл агентной системы

Теперь в книге есть цельный блок про `SDLC -> ADLC`, change management, assurance loop, supply chain, retirement, misalignment, behavioral evals, AI-native observability и inventory control.

Почему это важно: теперь книга закрывает не только архитектуру и запуск, но и жизнь системы после релиза.

### Усилен production contour в частях I-V

В книгу добавлены более точные мосты между архитектурой, retrieval, execution и eval discipline:

- в части I теперь явнее отделены runtime-архитектура, training layer и product surface;
- в части II добавлена более четкая taxonomy для `prompt injection`, `jailbreak` и `action hallucination`;
- в части III усилен retrieval contour: `semantic gap`, `HyDE`, `RAG first`, различие между continued pretraining и `SFT`;
- в части IV добавлены practical rules для больших tool catalogs, `semantic tool filtering` и явные роли `MCP host / client / server`;
- в части V усилены продуктовый взгляд на `latency budget` и practical framing для `LLM-as-a-judge`.

Почему это важно: книга стала лучше закрывать не только базовые platform layers, но и повседневные вопросы production-команды, которые обычно всплывают между design review, eval loop и rollout.

## Reference

### Справочный слой с reusable schemas

Книга теперь включает отдельные reference pages для:

- traces и event catalog;
- eval datasets и grading contract;
- policy bundles и approvals;
- change review и rollout gates;
- lifecycle artifacts;
- memory retrieval contracts.

Почему это важно: теперь из объясняющих глав можно быстро переходить к reviewable схемам и артефактам.

## Runtime

### Runnable reference runtime

В репозитории есть [`agent_runtime_ref`](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) — небольшой исполняемый пакет, который поддерживает:

- approvals и delegated authorization context;
- controls и lifecycle runtime-control inspection;
- lifecycle artifacts;
- session export и replay summaries;
- eval dataset export;
- trace export с redaction, redacted summaries, replay preservation и schema versioning.

Почему это важно: книга теперь опирается не только на narrative chapters, но и на runnable reference implementation.

## Practical Appendix

### Практический appendix

Сайт уже включает:

- glossary;
- cheat sheets;
- case studies;
- policy templates;
- research frontier;
- community roadmap.

Почему это важно: у читателя есть быстрые входы в чеклисты, кейсы, glossary и practical assets без обязательного линейного чтения всей книги.

## Navigation

### Усилены входные страницы

Обновлены:

- [С чего начать](start-here.md);
- [Справочный слой](reference.md);
- [Шпаргалки](appendix/cheat-sheets.md).

Теперь они лучше подсвечивают короткие маршруты для тем вроде:

- `semantic tool filtering`;
- `HyDE` и `RAG vs training`;
- `latency budget` и routed pipelines;
- `LLM-as-a-judge` и judge calibration;
- различие между `prompt injection`, `jailbreak` и `action hallucination`.

Почему это важно: новые темы стали заметны не только внутри отдельных глав, но и на уровне reader entry points.

## Publish readiness

### Перед публикацией усилен сайт

Перед следующим деплоем начат и заметно продвинут publisher-facing проход качества:

- draft/planning страницы исключены из опубликованного сайта и sitemap;
- добавлены OpenGraph/Twitter metadata и social preview image;
- проверены search index, sitemap, robots, локальные assets, anchors, alt text и внешние ссылки;
- README на трех языках теперь содержит fast-forward publish checklist для `main` и `docs-prod`.

Это не означает, что publisher-facing слой полностью закрыт: еще остаются глубокая EN/ZH-проверка, rendering/export QA, sample-chapter polish и упаковка manuscript/online companion.

Почему это важно: опубликованный сайт должен постепенно приближаться к аккуратному reader-facing продукту, а не выглядеть как сырая сборка из Markdown-файлов.

## Что это дает читателю

- Можно читать книгу как handbook.
- Можно использовать reference pages как инженерные заготовки.
- Можно запускать примерный runtime, а не только читать Markdown.
- Можно опираться на свежие источники от OpenAI, Anthropic, Google, Microsoft и NIST.

## Куда идти дальше

- [С чего начать](start-here.md)
- [Справочный слой](reference.md)
- [План книги](book/plan.md)
- [Источники](appendix/sources.md)
