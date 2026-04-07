# Что нового

Эта страница нужна как короткий журнал крупных улучшений книги и опорного пакета. Она не заменяет git history, а помогает читателю быстро увидеть, насколько проект живой и какие слои уже появились.

_Актуально на 8 апреля 2026 года._

## Book

### Часть VIII про жизненный цикл агентной системы

Теперь в книге есть цельный блок про `SDLC -> ADLC`, change management, assurance loop, supply chain, retirement, misalignment, behavioral evals, AI-native observability и inventory control.

Почему это важно:
- теперь книга закрывает не только архитектуру и запуск, но и жизнь системы после релиза.

## Reference

### Справочный слой с reusable schemas

Книга теперь включает отдельные reference pages для:

- traces и event catalog;
- eval datasets и grading contract;
- policy bundles и approvals;
- change review и rollout gates;
- lifecycle artifacts;
- memory retrieval contracts.

Почему это важно:
- теперь из объясняющих глав можно быстро переходить к reviewable схемам и артефактам.

## Runtime

### Runnable reference runtime

В репозитории есть [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) — небольшой исполняемый пакет, который поддерживает:

- approvals;
- controls;
- lifecycle artifacts;
- session export;
- eval dataset export;
- trace export с redaction и schema versioning.

Почему это важно:
- книга теперь опирается не только на narrative chapters, но и на runnable reference implementation.

## Practical Appendix

### Практический appendix

Сайт уже включает:

- glossary;
- cheat sheets;
- case studies;
- policy templates;
- research frontier;
- community roadmap.

Почему это важно:
- у читателя есть быстрые входы в чеклисты, кейсы, glossary и practical assets без обязательного линейного чтения всей книги.

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
