# Что нового

Эта страница нужна как короткий журнал крупных улучшений книги и опорного пакета. Она не заменяет историю Git, а помогает читателю быстро увидеть, насколько проект живой и какие слои уже появились.

_Актуально на 20 мая 2026 года._

!!! note "Обновление canonical cases"
    Крупный слой обновлений от 15 мая 2026 года — сквозная карта трех canonical cases. **Support triage**, **Internal knowledge assistant** и **Incident coordination** теперь видны в book chapters, public entry points, reference pages и appendix artifacts, а coverage guards защищают chapters и appendix pages от потери этих маршрутов.

!!! note "Обновление safe-agent схем"
    Обновления 17-19 мая 2026 года связали prose, appendices и guards для safe-agent архитектуры: MCP threat model и `mcp_server` contract, A2A handoff trust contract и trust-delegation artifact, defense-in-depth control map, verifier verdict record, governance action record, NIST AI RMF telemetry mapping, memory poisoning review fields и unified agent threat evidence теперь отражены в [trace schema](appendix/trace-schema.md), [eval schema](appendix/eval-schema.md) и [memory/retrieval schema](appendix/memory-retrieval-schema.md).

## Book

### Редакционная проверка от 14 мая 2026 года

Закрыт первый пакет замечаний издательского QA: decision frame в Главе 1 переведен из таблицы в устойчивый текстовый блок для HTML/PDF/plain-text extraction, а fast-moving главы, Sources и What’s New получили свежую дату редакционной проверки.

Почему это важно: внешняя поверхность книги теперь меньше зависит от особенностей рендера таблиц и честнее показывает, когда подвижные agent-security разделы были пересмотрены.

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

### Справочный слой с переиспользуемыми схемами

Книга теперь включает отдельные справочные страницы для:

- traces и каталог событий;
- eval-наборы данных и контракт оценивания;
- пакеты политик и approvals-контуры;
- ревью изменений и rollout-гейты;
- lifecycle-артефакты;
- контракты извлечения из памяти.

Почему это важно: теперь из объясняющих глав можно быстро переходить к проверяемым схемам и артефактам.

## Runtime

### Runnable reference runtime

В репозитории есть [`agent_runtime_ref`](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) — небольшой исполняемый пакет, который поддерживает:

- approvals и контекст делегированной авторизации;
- controls и проверку runtime-control в lifecycle;
- lifecycle-артефакты;
- экспорт сессий и replay-сводки;
- экспорт eval-наборов данных;
- экспорт trace с redaction, редактированными сводками, сохранением replay и версионированием схем.

Почему это важно: книга теперь опирается не только на описательные главы, но и на работающую эталонную реализацию.

## Practical Appendix

### Практическое приложение

Сайт уже включает:

- глоссарий;
- шпаргалки;
- кейсы;
- шаблоны политик;
- исследовательский фронтир;
- дорожная карта сообщества.

Почему это важно: у читателя есть быстрые входы в чеклисты, кейсы, глоссарий и практические материалы без обязательного линейного чтения всей книги.

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

Издательский проход качества идет, но еще не закрыт полностью.

Уже закрыто:

- черновые и плановые страницы исключены из опубликованного сайта и sitemap;
- добавлены метаданные OpenGraph/Twitter и социальная превью-картинка;
- проверены поисковый индекс, sitemap, robots, локальные ресурсы, якоря, alt-тексты и внешние ссылки;
- базовая навигация и резервные canonical redirects покрывают основные точки входа, которые люди копируют руками;
- запись о доступности публичных ссылок обновлена 20 мая 2026 года после того, как все девять ссылок из publisher packet вернули HTTP 200;
- реестр блокеров, журнал решений/исключений, ограничение длины строк и названия publisher packet устойчивы для печати и экспорта;
- карта ролей части VIII теперь устойчива для печати;
- README на трех языках теперь содержит чек-лист быстрой синхронизации публикации для `main` и `docs-prod`.

До статуса готовности к публикации еще остаются глубокая проверка EN/ZH-слоев, независимый QA HTML/PDF/экспорта, редакционная полировка глав-образцов и упаковка печатной рукописи/онлайн-компаньона под конкретного издателя.

Почему это важно: опубликованный сайт должен постепенно приближаться к аккуратному продукту для читателя, а не выглядеть как сырая сборка из Markdown-файлов.

## Что это дает читателю

- Можно читать книгу как практическое руководство.
- Можно использовать справочные страницы как инженерные заготовки.
- Можно запускать примерный исполняемый пакет, а не только читать Markdown-файлы.
- Можно опираться на свежие источники от OpenAI, Anthropic, Google, Microsoft и NIST.

## Куда идти дальше

- [С чего начать](start-here.md)
- [Справочный слой](reference.md)
- [План книги](book/plan.md)
- [Источники](appendix/sources.md)
