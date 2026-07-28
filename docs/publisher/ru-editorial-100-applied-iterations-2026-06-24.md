# 100 applied editorial iterations for редакционная подготовка

Дата прохода: 2026-06-24.

Назначение: продолжить backlog 201-300 после applied pass по главам 6-10. Эти итерации 301-400 фокусируются на доведении Google Doc до редакционно пригодной рукописи: code-block normalization, главы 11-20, приложения, proof QA, авторские поля и handoff.

Исходная точка:

- Google Doc source: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
- свежий Google Docs export после applied edits: 656 страниц, включая одну trailing blank-like page;
- Template2000n-applied derivative: 411 страниц, blank-like pages: 0;
- известный proof issue: page 326 показывает isolated Markdown fence marker `````yaml`;
- предыдущий backlog: `docs/publisher/ru-editorial-100-applied-iterations-2026-06-23.md`;
- этот backlog: дополнительные итерации 301-400.

## Итерации 301-400

| # | Цель итерации | Критерий готовности | Следующий action |
| ---: | --- | --- | --- |
| 301 | Code-block inventory in Google Doc | Все literal fence markers посчитаны и привязаны к главам | Разделить на keep/convert/move |
| 302 | Убрать isolated fence markers | В proof нет страниц с одинокими ```yaml/```python | Повторить render QA |
| 303 | Нормализовать YAML block captions | Каждый YAML excerpt имеет человекочитаемую подпись | Пройти главы 1-10 |
| 304 | Нормализовать Python block captions | Каждый Python excerpt объясняет архитектурный смысл | Пройти главы 1-10 |
| 305 | Нормализовать CLI block captions | CLI приведены только как companion route или короткий excerpt | Пройти приложения |
| 306 | Разделить code excerpts и reference dumps | В книге нет длинных validation-message catalogs | Вынести в companion |
| 307 | Проверить page 326 regression | Page 326 больше не содержит одиночный fence marker | Зафиксировать метрики |
| 308 | Проверить all low-ink Template pages | Low-ink pages являются осмысленными хвостами | Добавить page notes |
| 309 | Проверить raw trailing blank | Понять, вызвана ли страница 656 лишними пустыми абзацами | Убрать trailing blanks |
| 310 | Проверить final Google Doc paragraphs | В конце документа нет серии пустых абзацев | Повторить export |
| 311 | Applied focus blocks 11-13 | Главы 11-13 имеют практический lead | Connector readback |
| 312 | Applied focus blocks 14-16 | Главы 14-16 имеют практический lead | Connector readback |
| 313 | Applied focus blocks 17-20 | Главы 17-20 имеют практический lead | Connector readback |
| 314 | Проверить главу 11 на sandbox boundary | Sandbox объяснен как containment boundary | Добавить bridge к MCP |
| 315 | Проверить главу 12 на idempotency | Idempotency связана с side-effect safety | Уточнить rollback language |
| 316 | Проверить главу 13 на telemetry vocabulary | Trace, span, event не смешиваются | Терминологический pass |
| 317 | Проверить главу 14 на SLO realism | SLO не обещают недостижимую reliability | Добавить caveat |
| 318 | Проверить главу 15 на eval gates | Eval gates связаны с release decisions | Уточнить evidence |
| 319 | Проверить главу 16 на rollout evidence | Rollout читается как управляемая цепочка | Добавить transition |
| 320 | Проверить главу 17 на org model | Роли platform/security/product разведены | Owner map pass |
| 321 | Проверить главу 18 на golden paths | Golden path не выглядит бюрократией | Добавить anti-zoo framing |
| 322 | Проверить главу 19 на ADLC | ADLC определен до сложных практик | Добавить early definition |
| 323 | Проверить главу 20 на closure | Registry, incidents, retirement связаны | Сжать повторы |
| 324 | Собрать one-page book arc | Вся книга объяснима одной логической дугой | Добавить в handoff |
| 325 | Cross-reference pass 6-10 | Ссылки между memory/retrieval/tool catalog корректны | Пройти 11-16 |
| 326 | Cross-reference pass 11-16 | Sandbox, idempotency, trace, eval, rollout связаны | Пройти 17-20 |
| 327 | Cross-reference pass 17-20 | Org/lifecycle chapters замыкают arc | Пройти приложения |
| 328 | Appendix 1 contract audit | Capability contract не перегружен полями | Упростить |
| 329 | Appendix 2 readiness audit | Checklist проверяет запуск, а не общие намерения | Уточнить вопросы |
| 330 | Appendix 3 incident audit | Incident template связан с trace/evidence | Уточнить поля |
| 331 | Appendix 4 companion audit | Companion appendix остается навигацией | Сократить справочник |
| 332 | Проверить public companion link | Везде одна каноническая метка и URL | Hyperlink audit |
| 333 | Проверить repo link policy | В теле книги нет длинных blob/tree URLs | Replace or link label |
| 334 | Проверить source freshness flags | Быстро меняющиеся факты помечены | Official docs check |
| 335 | Проверить legal/compliance caveats | Нет обещаний юридической пригодности | Уточнить disclaimer |
| 336 | Проверить AI transparency note | Использование AI-инструментов описано честно | Author review |
| 337 | Проверить bibliography strategy | Источники разделены на primary/practice/learning/author | Source appendix pass |
| 338 | Проверить glossary need | Решить, нужен ли отдельный глоссарий | Согласовать с редактором |
| 339 | Терминологический pass capability | Capability не переводится случайно | Normalize |
| 340 | Терминологический pass gateway | Tool gateway и policy gateway разведены | Normalize |
| 341 | Терминологический pass verifier | Verifier, validator, evaluator не смешаны | Normalize |
| 342 | Терминологический pass trace | Trace/span/event употребляются устойчиво | Normalize |
| 343 | Терминологический pass rollout | Rollout/release/deployment разведены | Normalize |
| 344 | Терминологический pass retirement | Retirement, decommission, disable разведены | Normalize |
| 345 | Проверить русский-английский баланс | Английские термины остаются именами контрактов | Style pass |
| 346 | Проверить пунктуацию inline code | Inline code не ломает русскую фразу | Typography pass |
| 347 | Проверить списки после import | Списки не стали псевдомаркерами | Template render |
| 348 | Проверить numbered steps | Нумерованные процедуры не сбиваются | Template render |
| 349 | Проверить tables/forms need | Таблицы используются только для сопоставимых данных | Convert overused tables |
| 350 | Проверить diagrams | Mermaid/source diagrams не выглядят как сырой Markdown | Convert or companion |
| 351 | Проверить chapter openings | Первые страницы глав имеют тезис, не справочник | Add lead |
| 352 | Проверить chapter endings | Концовки глав ведут к следующему решению | Add bridge |
| 353 | Проверить repeated scenarios | Сквозные сценарии не теряются | Scenario map |
| 354 | Проверить workshop prompts | В главах есть материал для командного ревью | Add prompts |
| 355 | Проверить executive readability | Руководитель видит решения и ответственность | Add summaries |
| 356 | Проверить engineer usability | Инженер видит контракты и проверки | Add excerpts |
| 357 | Проверить security usability | Security видит threats and controls | Add risk notes |
| 358 | Проверить product usability | Product видит rollout/owner tradeoffs | Add owner notes |
| 359 | Проверить platform usability | Platform видит registry/golden paths | Add platform notes |
| 360 | Проверить incident usability | Incident team видит trace/evidence flow | Add response notes |
| 361 | Author fill pass 1 | Short bio заполнена автором | Review wording |
| 362 | Author fill pass 2 | Extended bio заполнена автором | Review factuality |
| 363 | Author fill pass 3 | Public links заполнены | Link check |
| 364 | Author fill pass 4 | Publisher bio согласована | Handoff |
| 365 | Author decision acknowledgments | Решение принято и отражено в doc | Add/remove section |
| 366 | Author decision dedication | Решение принято и отражено в doc | Add/remove section |
| 367 | Author decision errata channel | Канал обратной связи выбран | Update companion appendix |
| 368 | Author decision companion version | Version tag выбран | Update companion appendix |
| 369 | Publisher style check title | Boxed title accepted or removed | Template owner |
| 370 | Publisher style check headings | Heading ladder соответствует шаблону | Template pass |
| 371 | Publisher style check code | Code style readable after normalization | Render QA |
| 372 | Publisher style check lists | Lists visually stable | Render QA |
| 373 | Publisher style check page breaks | Нет orphan headings/listing captions | Render QA |
| 374 | Publisher style check first 20 pages | Front matter looks clean | Visual QA |
| 375 | Publisher style check final 20 pages | Appendices close cleanly | Visual QA |
| 376 | Full raw export QA | Google Docs export has no unexpected blanks | Render metrics |
| 377 | Full Template QA | Template proof has no blank/edge/orphan pages | Render metrics |
| 378 | HTML/export structure check | Links and headings survive export | Export check |
| 379 | DOCX zip integrity | Both DOCX artifacts open structurally | Zip test |
| 380 | Metadata audit | DOCX metadata has no unwanted author/tool leaks | Metadata scrub |
| 381 | Accessibility audit headings | Heading order is coherent | a11y pass |
| 382 | Accessibility audit links | Links have meaningful labels | a11y pass |
| 383 | Accessibility audit tables | Tables have header semantics where needed | a11y pass |
| 384 | Accessibility audit images | Images/diagrams have captions or alt plan | a11y pass |
| 385 | Build source sync note | Repo reports state which source is authoritative | Update packet |
| 386 | Submission packet update | Artifact list and known issues current | Update packet |
| 387 | Editor cover note | Editor sees scope, status, asks, known risks | Update packet |
| 388 | Known risks list | Code fences, title style, author fields tracked | Update packet |
| 389 | Must-fill list | Author-owned fields are visible in report | Update packet |
| 390 | Companion handoff | Routes and versioning rules listed | Update packet |
| 391 | Regression service lines | No internal service lines in front matter | find text |
| 392 | Regression focus blocks | Expected focus blocks 1-20 present | find text |
| 393 | Regression listing rule | Listing rules present and not duplicated | find text |
| 394 | Regression raw URLs | Long raw GitHub URLs absent from Google Doc | find text |
| 395 | Regression code fences | Literal fence markers normalized or tracked | find text |
| 396 | Regression blank pages | Page counts and blank-like pages recorded | Render QA |
| 397 | Repository verification | JSON, DOCX zips, diff checks pass | Local checks |
| 398 | Test suite verification | `uv run --group dev pytest` passes | CI confidence |
| 399 | Docs build verification | `uv run --group docs mkdocs build --strict` passes | CI confidence |
| 400 | Commit, push, final report | Remote branch contains applied pass and report | User handoff |

## Итог по итерациям 301-400

Главная цель следующего блока работ — убрать следы Markdown-сборки из Google Doc и publisher proof. Пока рукопись уже полнообъемная и логически связанная, но code-block normalization остается самым заметным техническим долгом перед внешней редактурой.
