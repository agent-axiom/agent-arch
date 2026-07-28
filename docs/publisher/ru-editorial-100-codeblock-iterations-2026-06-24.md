# 100 code-block and proof iterations for редакционная подготовка

Дата прохода: 2026-06-24.

Назначение: продолжить backlog 301-400 после code-block normalization pass. Эти итерации 401-500 фокусируются на превращении рукописи из технически собранного Google Doc в редакционно устойчивую книгу: короткие печатные excerpts, companion-bound полные артефакты, осмысленные подписи, проверяемые источники, publisher proof QA и финальный handoff.

Исходная точка:

- Google Doc source: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
- fresh Google Docs export after code-block pass: 655 страниц, blank-like pages: 0;
- Template2000n-codeblock derivative: 409 страниц, blank-like pages: 0;
- literal Markdown fence markers в Google Doc не найдены;
- remaining debt: крупные YAML/code excerpts, generic listing labels, companion extraction, author-owned fields;
- предыдущий backlog: `docs/publisher/ru-editorial-100-applied-iterations-2026-06-24.md`;
- этот backlog: дополнительные итерации 401-500.

## Итерации 401-500

| # | Цель итерации | Критерий готовности | Следующий action |
| ---: | --- | --- | --- |
| 401 | Listing label inventory | Все `Листинг (YAML):` и `Листинг (Python):` привязаны к главам | Разделить на print/companion |
| 402 | Semantic captions pass | Generic labels заменены на смысловые подписи | Проверить readback |
| 403 | YAML print budget | Для каждого YAML-фрагмента задан лимит строк в печати | Сжать oversized excerpts |
| 404 | Python print budget | Python-фрагменты показывают идею, а не полную реализацию | Вынести полный код |
| 405 | CLI print budget | CLI-сессии оставлены только как короткие команды | Вынести длинные sessions |
| 406 | Trace/event print budget | Trace examples показывают evidence chain | Вынести полные events |
| 407 | Validation catalog compression | Каталоги сообщений превращены в 3-5 representative cases | Добавить companion route |
| 408 | Runtime config compression | Config dumps заменены на decision-oriented excerpts | Проверить главы 2-6 |
| 409 | Policy config compression | Policy examples оставляют только enforcement points | Проверить главы 5-10 |
| 410 | Registry schema compression | Registry fields показывают ownership model | Вынести full schema |
| 411 | Chapter 1 listing relevance | В главе нет листингов, не помогающих первому различению agent/chat | Сделать local edit |
| 412 | Chapter 2 listing relevance | Runtime boundary examples не перегружают поток | Сделать local edit |
| 413 | Chapter 3 listing relevance | Input-layer examples не выглядят vendor-specific | Сделать local edit |
| 414 | Chapter 4 listing relevance | Retrieval examples поддерживают trust-boundary thesis | Сделать local edit |
| 415 | Chapter 5 listing relevance | Threat-model material не превращается в checklist dump | Сделать local edit |
| 416 | Chapter 6 listing relevance | Tool gateway examples показывают policy surface | Сделать local edit |
| 417 | Chapter 7 listing relevance | Memory examples показывают risk and provenance | Сделать local edit |
| 418 | Chapter 8 listing relevance | Memory types не смешиваются с implementation fields | Сделать local edit |
| 419 | Chapter 9 listing relevance | Context retrieval snippets связаны с freshness and trust | Сделать local edit |
| 420 | Chapter 10 listing relevance | Catalog examples показывают execution contract | Сделать local edit |
| 421 | Chapter 11 listing relevance | Sandbox examples показывают containment boundary | Сделать local edit |
| 422 | Chapter 12 listing relevance | Idempotency examples показывают side-effect control | Сделать local edit |
| 423 | Chapter 13 listing relevance | Telemetry examples показывают trace/span/event separation | Сделать local edit |
| 424 | Chapter 14 listing relevance | SLO examples связаны с operational decisions | Сделать local edit |
| 425 | Chapter 15 listing relevance | Eval examples читаются как gate evidence | Сделать local edit |
| 426 | Chapter 16 listing relevance | Rollout examples показывают rollback and waves | Сделать local edit |
| 427 | Chapter 17 listing relevance | Org examples показывают ownership boundaries | Сделать local edit |
| 428 | Chapter 18 listing relevance | Golden-path examples не выглядят бюрократическим catalog dump | Сделать local edit |
| 429 | Chapter 19 listing relevance | ADLC examples показывают lifecycle decisions | Сделать local edit |
| 430 | Chapter 20 listing relevance | Closure examples связывают registry, incidents, retirement | Сделать local edit |
| 431 | Appendix 1 compression | Capability contract остается usable в печати | Full contract to companion |
| 432 | Appendix 2 compression | Readiness checklist не дублирует главы | Remove duplicates |
| 433 | Appendix 3 compression | Incident template не выглядит юридическим шаблоном | Add caveat |
| 434 | Appendix 4 compression | Companion appendix остается навигацией | Remove source dump |
| 435 | Companion route naming | Все вынесенные артефакты имеют стабильные route names | Update manifest |
| 436 | Companion version policy | Version tag указан единообразно | Author decision |
| 437 | Companion sync check | Каждый companion reference ведет к существующему artifact | Link audit |
| 438 | Companion missing-artifact log | Недостающие artifacts перечислены отдельно | Create backlog |
| 439 | Source-map sync | Repo source-map отражает текущие companion routes | Update source map |
| 440 | Publisher packet sync | Submission packet знает про compressed listings | Update packet |
| 441 | Visual QA page 326 | Former fence-marker page is checked after compression | Render proof |
| 442 | Visual QA low-ink pages | Low-ink pages имеют осмысленный текст | Page notes |
| 443 | Visual QA high-density pages | Самые плотные страницы читаются в Template2000n | Compress or split |
| 444 | Visual QA orphan captions | Подписи листингов не остаются одни внизу страницы | Page-break pass |
| 445 | Visual QA code wrapping | Code-like text не уходит за поля | Render proof |
| 446 | Visual QA list wrapping | Long bullets do not create awkward page breaks | Render proof |
| 447 | Visual QA front matter | Front matter не содержит служебных строк | Render proof |
| 448 | Visual QA final pages | Финальные приложения закрываются без пустого хвоста | Render proof |
| 449 | Raw export regression | Google Docs export сохраняет 0 blank-like pages | Render metrics |
| 450 | Template export regression | Template2000n proof сохраняет 0 blank-like pages | Render metrics |
| 451 | Terminology pass listing/caption | Caption vocabulary единообразен | Update terminology |
| 452 | Terminology pass companion | Companion, repository, route, artifact употребляются стабильно | Update terminology |
| 453 | Terminology pass contract | Contract, schema, policy, evidence разведены | Update terminology |
| 454 | Terminology pass trace | Trace, span, event, log не смешиваются | Update terminology |
| 455 | Terminology pass eval | Eval, verifier, validator, gate разведены | Update terminology |
| 456 | Terminology pass rollout | Rollout, deployment, release, rollback разведены | Update terminology |
| 457 | Typography inline code | Inline code не ломает русскую грамматику | Proofread pass |
| 458 | Typography quotes/dashes | Кавычки и тире приведены к издательскому стилю | Style pass |
| 459 | Typography list rhythm | Списки не выглядят как сгенерированные dumps | Style pass |
| 460 | Typography heading rhythm | Заголовки одинакового уровня имеют сопоставимую длину | Heading pass |
| 461 | Source freshness OpenAI | Современные утверждения проверены по official docs | Update notes |
| 462 | Source freshness Anthropic | Современные утверждения проверены по official docs | Update notes |
| 463 | Source freshness MCP | MCP statements проверены по primary sources | Update notes |
| 464 | Source freshness A2A | A2A statements проверены по primary sources | Update notes |
| 465 | Source freshness cloud vendors | Product names and features актуальны | Update notes |
| 466 | Source citation routing | Печатный текст не перегружен ссылками | Move details |
| 467 | Legal caveat pass | Книга не обещает compliance guarantee | Editorial caveat |
| 468 | Security safety pass | Атакующие примеры framed defensively | Editorial caveat |
| 469 | Privacy pass | Нет customer data, secrets, internal identifiers | Sensitive scan |
| 470 | Trademark pass | Product names used consistently | Publisher list |
| 471 | Author bio short | Short bio заполнена автором | Editorial polish |
| 472 | Author bio extended | Extended bio заполнена автором | Editorial polish |
| 473 | Author role | Роль автора согласована с публичным позиционированием | Update front matter |
| 474 | Author links | GitHub/site/blog/profile заполнены | Link audit |
| 475 | Author publisher wording | Формулировка для издательства согласована | Handoff |
| 476 | Author acknowledgments decision | Благодарности добавлены или явно исключены | Update front matter |
| 477 | Author dedication decision | Посвящение добавлено или явно исключено | Update front matter |
| 478 | Author errata decision | Публичный канал errata выбран | Update companion |
| 479 | Author companion decision | Canonical companion URL/tag выбран | Update companion |
| 480 | Author final factual approval | Автор подтвердил факты о себе and claims | Freeze bio |
| 481 | Chapter opening audit | Каждая глава начинается с решения, а не справочника | Add leads |
| 482 | Chapter closing audit | Каждая глава заканчивается переходом и действием | Add bridges |
| 483 | Part opening audit | Каждая часть объясняет свою роль в дуге книги | Add part intro |
| 484 | Part closing audit | Каждая часть фиксирует outcome | Add part outro |
| 485 | Book arc audit | Центральная мысль прослеживается от главы 1 до приложения | Handoff note |
| 486 | Reader persona audit | Architect/tech lead/security/platform видят свои задачи | Add targeted notes |
| 487 | Scenario continuity audit | Сквозные сценарии не исчезают после первых глав | Scenario map |
| 488 | Workshop usability audit | Читатель может провести командный review по книге | Add prompts |
| 489 | Executive summary audit | Руководитель видит decisions, ownership, risk | Add summaries |
| 490 | Engineer usability audit | Инженер видит contracts, checks, failure modes | Add examples |
| 491 | Security usability audit | Security видит threats, controls, evidence | Add notes |
| 492 | Platform usability audit | Platform видит registry, golden paths, lifecycle | Add notes |
| 493 | Product usability audit | Product видит rollout, owner tradeoffs, scope | Add notes |
| 494 | Incident usability audit | Incident team видит trace/evidence/rollback path | Add notes |
| 495 | Full DOCX integrity gate | Raw and Template DOCX open structurally | Zip test |
| 496 | Full render QA gate | Raw and Template render without blanks/edge risks | Render metrics |
| 497 | Docs build gate | Repo docs build with strict mode | `mkdocs build --strict` |
| 498 | Test gate | Repo test suite passes or gaps are documented | `pytest` |
| 499 | Commit and push gate | Branch contains only intended pass artifacts | Push branch |
| 500 | Final author report | Автор получает status, pages, risks, must-fill list | Handoff |

## Итог по итерациям 401-500

Главная цель следующего блока - перейти от технической нормализации к редакционной читабельности. Рукопись уже полнообъемная, Google Doc больше не содержит literal Markdown fence markers, а свежие proofs не имеют blank-like pages. Оставшаяся крупная работа - сократить dense listing layer, привязать полные артефакты к companion, заменить generic labels на смысловые captions и закрыть author-owned поля перед передачей редактору.
