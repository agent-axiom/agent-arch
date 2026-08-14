# Эволюция русской издательской рукописи

Status: working ledger for manuscript assembly. This file tracks the book
manuscript itself, not the publisher cover materials.

## Current reality

На 2026-08-01 существующий Google Doc является полнообъёмной рабочей
издательской рукописью, а не сжатой редакционной сборкой.

В документе находятся:

- 8 частей и 28 глав;
- 8 лабораторных работ и итоговый проект;
- 11 таблиц и 56 иллюстраций;
- приложения, глоссарий, проверочные списки, источники и ссылки на эталонную
  среду исполнения;
- около 95 тысяч слов по метрике издательской производной.

Каноническая последовательность новых и изменённых фрагментов полностью
подтверждена итоговым чтением Google Doc. Оставшиеся ограничения относятся не к объёму
рукописи, а к авторским фактам, реальной внешней рецензии, независимой проверке
лабораторных работ и финальной корректуре издательства.

## Source volume

Репозиторий остается источником правды. Текущий русский объём:

- `docs/book/**/*.md` и `docs/appendix/**/*.md`, без `.en.md` и `.zh.md`;
- около **113 909 слов** по текущему `wc -w` на 2026-06-13;
- электронная структура и сопроводительные страницы остаются шире печатного
  маршрута;
- издательская структура: 8 частей, 28 глав, введение, заключение и приложения;
- текущая проверенная вёрстка: 456 страниц Google-ориентированной производной
  и 330 страниц производной `Template2000n`.

Электронный материал не копируется в печатную книгу механически. При
синхронизации удаляется веб-навигация, тяжёлые схемы и полный вывод CLI остаются
в онлайн-сопровождении, а новые инженерные тезисы встраиваются в причинную
линию соответствующих глав.

## Evolution stages

### Stage 0. Repository baseline and contract map

Status: done.

Done:

- зафиксирована русская source of truth модель;
- создана договорная карта 7 частей / 23 главы;
- создан source map из Markdown-файлов в печатные главы;
- заведено правило repository -> Google Doc sync.

Evidence:

- `docs/publisher/ru-manuscript-map.md`;
- `docs/publisher/ru-source-map.md`;
- `docs/publisher/ru-google-doc-workflow.md`.
- `docs/publisher/ru-editorial-roadmap.md`.

### Stage 1. Google Doc skeleton and first sample

Status: done and superseded by later full-manuscript assembly.

Done:

- создан Google Doc `Архитектура безопасных ИИ-агентов`;
- перенесена договорная структура;
- перенесена Chapter 1 как первый sample;
- Chapter 1 прошла первый русский издательский line edit;
- source Chapter 13 прошел первый technical sample line edit.

Historical limit at this stage:

- объем Google Doc тогда отражал только skeleton plus sample;
- этот checkpoint больше нельзя трактовать как текущий статус рукописи.

### Stage 2. Manuscript body assembly

Status: done for rough assembly and followed by structural, terminology,
cross-reference, companion-boundary and current-source print-readability passes.

Goal:

- перенести в Google Doc не только sample, а тело рукописи по договорной
  структуре;
- при переносе сразу отмечать print/companion boundary;
- сохранить Markdown как source of truth.

Batch order:

1. Введение + Часть I: print chapters 1-3. Status: rough assembly synced to
   Google Doc on 2026-06-13.
2. Часть II + Часть III: print chapters 4-9. Status: rough assembly synced to
   Google Doc on 2026-06-13.
3. Часть IV + Часть V: print chapters 10-16. Status: rough assembly synced to
   Google Doc on 2026-06-13.
4. Часть VI + Часть VII: print chapters 17-23. Status: rough assembly synced to
   Google Doc on 2026-06-13.
5. Приложения: glossary, checklists, incident/postmortem, curated sources and
   онлайн-сопровождение. Status: rough assembly synced to Google Doc on 2026-06-13.

Definition of done:

- Google Doc содержит все договорные главы хотя бы в rough assembly form;
- для каждой главы есть source path и companion boundary;
- в чеклисте видно, какие главы требуют line edit, compression или rewrite.

### Stage 3. Compression from web manuscript to print manuscript

Status: first-pass complete across the full contract manuscript.

Goal:

- сжать web-структуру 8/27 в договорную структуру 7/23;
- объединить практические страницы и appendix-heavy фрагменты в книжные главы;
- удалить или переформатировать web-only элементы.

Definition of done:

- каждая печатная глава имеет один связный текст;
- long schema/runtime/CLI material вынесен или помечен как companion-only;
- chapter endings не выглядят как повторяющийся web-template.

### Stage 4. Editorial pass

Status: structural pass completed across the full manuscript; deeper
cross-reference, terminology and line edit pass still pending.

Goal:

- пройти главы по voice, rhythm, terminology and evidence;
- сохранить практическую глубину, но убрать web-friction.

Definition of done:

- все 23 главы прошли first Russian editorial pass;
- glossary and terminology policy согласованы с текстом;
- sample Chapter 1 не отличается по качеству от остальных глав.

### Stage 5. Publisher formatting and external packet

Status: manuscript body exists; H2/H3 body-style cleanup is complete for the
current Google Doc proof; author/front-matter fields are isolated; current raw
and Template2000n official-style proof candidates render cleanly. Final
publisher submission is still blocked until author facts, final companion
metadata, publisher/editor acceptance of the Template2000n route, post-author
export/render QA and external proofread are closed.

Goal:

- применить стилевые файлы БХВ;
- подготовить DOCX/Google Doc export;
- только после этого использовать cover note and external packet.

Rule:

- `docs/publisher/ru-cover-note-draft.md` is parked until Stage 2 is complete
  enough to show manuscript volume.

Current 2026-07-03 packet:

- Template2000n acceptance gate:
  `docs/publisher/ru-template2000n-acceptance-gate-2026-07-03.md`;
- final editorial handoff plan:
  `docs/publisher/ru-final-editorial-handoff-plan-2026-07-03.md`;
- author fill packet:
  `docs/publisher/ru-author-editorial-fill-packet-2026-07-03.md`;
- Google Doc and DOCX handoff policy:
  `docs/publisher/ru-google-doc-docx-handoff-policy-2026-07-03.md`.
- final pre-author export/render pass:
  `docs/publisher/ru-final-preauthor-export-pass-2026-07-03.md`;
- pre-author publisher packet:
  `docs/publisher/ru-preauthor-publisher-submission-packet-2026-07-03.md`.

## Current next practical step

The main artifact is now the full Google Doc manuscript plus the current proof
pair: raw Google Docs export and Template2000n derivative.

Next implementation step:

1. fill author bio/front-matter fields and confirm companion/public metadata;
2. get publisher/editor acceptance of the Template2000n style route;
3. run external editor/proofreader review against the clean handoff packet;
4. backport any semantic Google Doc edits into Markdown;
5. re-export raw DOCX and rebuild Template2000n after author fields;
6. rerun render QA and prepare the final publisher submission packet.

2026-07-03 pre-author dry run:

- fresh raw DOCX exported from the current Google Doc;
- fresh Template2000n derivative rebuilt;
- render QA passed: raw 489 pages, Template2000n 361 pages, 0 blank-like pages;
- author-owned placeholders remain in front matter, so final publisher
  submission remains blocked.

2026-07-04 targeted editorial quality pass:

- Chapter 20 and Chapter 21 received short book-role bridge paragraphs in the
  full Google Doc and in `docs/publisher/ru-manuscript-full.md`;
- Google Doc readback verified both inserted paragraph anchors in the full
  manuscript, revision
  `ALtnJHynC5_zU9n9cmTvBjPl9UMeD7Uve6QHp3PDDm33ZwWHCfBekh00ktjv4-xnUtiwP6hL7W39I4iTLk77MaTY60Z8DnRkpVQxhi5p46U`;
- excessive anglicisms in `docs/publisher/ru-source-map.md` and
  `docs/publisher/ru-manuscript-map.md` were reduced where the English wording
  was an editorial label rather than a file name, protocol name or code field;
- first-page manuscript phrasing was also cleaned in `ru-manuscript-full.md` and
  synced to the Google Doc where exact text matches existed;
- repeated chapter-ending scan was recorded without pretending that full
  normalization is complete;
- next 100 editorial quality goals were recorded in
  `docs/publisher/ru-editorial-100-editorial-quality-iterations-2026-07-04.md`;
- no fresh DOCX export/render QA was produced in this pass, so the current page
  counts remain the 2026-07-03 pre-author proof counts until the next export.

## Assembly checkpoints

### 2026-06-13. Introduction and Part I rough assembly

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-i.md`

Google Doc content added:

- `Введение. Зачем эта книга нужна`;
- `Часть I. От demo-агента к платформе`;
- `Глава 2. Когда нужен агент: workflow, single-agent, multi-agent`;
- `Глава 3. Референсная архитектура безопасной агентной системы`.

Notes:

- Chapter 1 was already present as the edited sample and remains the anchor of
  Part I.
- Chapter 2 and Chapter 3 are rough print assemblies, not final line edits.
- Connector readback verified the inserted headings and body paragraph placement.
- At this checkpoint the next batch was Part IV and Part V, not publisher
  packet work.

### 2026-06-13. Part II and Part III rough assembly

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-ii-iii.md`

Google Doc content added:

- `Часть II. Безопасность и контур управления`;
- `Глава 4. Контур безопасности и границы доверия`;
- `Глава 5. Identity, session, policy layer и capability model`;
- `Глава 6. Инструментальный шлюз, подтверждения и журнал аудита`;
- `Часть III. Память, знания и контекст`;
- `Глава 7. Зачем агенту память и почему она опасна`;
- `Глава 8. Краткосрочная, долгосрочная и профильная память`;
- `Глава 9. Извлечение контекста, уплотнение и фоновые обновления`.

Notes:

- This batch adds the security/control and memory/context body, not final line
  edits.
- At this checkpoint Google Doc status text pointed to the next batch:
  Part IV + Part V.
- Connector readback verified target document identity, inserted headings,
  final Part III paragraph and heading/body paragraph styles after a follow-up
  style normalization pass.

### 2026-06-13. Part IV and Part V rough assembly

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-iv-v.md`

Google Doc content added:

- `Часть IV. Инструменты, выполнение и интеграция`;
- `Глава 10. Модель выполнения и каталог инструментов`;
- `Глава 11. Песочница выполнения и MCP как интеграционный контракт`;
- `Глава 12. Идемпотентность, повторы, лимиты и границы отката`;
- `Часть V. Надежность, наблюдаемость и оценки`;
- `Глава 13. Трассы, спаны и структурированные события`;
- `Глава 14. SLO для агентных систем`;
- `Глава 15. Офлайн- и онлайн-оценки и регрессионные шлюзы`;
- `Глава 16. Сквозная цепочка доказательств: от запроса к rollout`.

Notes:

- This batch adds execution/integration and reliability/evaluation body, not
  final line edits.
- Long schemas, YAML examples, CLI/runtime details and full event catalogs stay
  in онлайн-сопровождение for now.
- Google Doc status text now points to the next batch: Part VI + Part VII.
- Connector readback verified target document identity, inserted headings,
  final Chapter 16 paragraph and updated top status text.

### 2026-06-13. Part VI and Part VII rough assembly

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-vi-vii.md`

Google Doc content added:

- `Часть VI. Организационная модель и жизненный цикл`;
- `Глава 17. Платформенная команда и продуктовые команды`;
- `Глава 18. Golden paths, общие шлюзы и борьба с агентным зоопарком`;
- `Глава 19. От SDLC к ADLC: жизненный цикл агентной системы`;
- `Глава 20. Assurance loop, реагирование на инциденты, registry и retirement`;
- `Часть VII. Эталонная реализация и промышленный запуск`;
- `Глава 21. Базовая схема runtime`;
- `Глава 22. Слой политик и каталог возможностей`;
- `Глава 23. Чеклист промышленного запуска`.

Notes:

- This batch adds organizational/lifecycle and reference implementation/launch
  body, not final line edits.
- Late lifecycle web material is compressed into print Chapter 20; full incident
  playbooks, registry operations, schemas and long checklists remain in online
  companion for now.
- Google Doc status text now points to the next batch: appendices and editorial
  compression.
- Connector readback verified target document identity, inserted headings,
  final Chapter 23 paragraph and updated top status text.

### 2026-06-13. Appendices rough assembly

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-appendices.md`

Google Doc content added:

- `Приложения`;
- `Приложение 1. Глоссарий`;
- `Приложение 2. Чеклисты`;
- `Приложение 3. Шаблон incident/postmortem`;
- `Приложение 4. Источники и онлайн-сопровождение`.

Notes:

- This batch adds the print appendix layer, not the full online reference
  catalog.
- Full trace/eval/approval/policy/memory/lifecycle/change/incident schemas,
  registry operations, long YAML examples, CLI walkthrough and source catalog
  remain in онлайн-сопровождение.
- Google Doc status text now points to compression/editorial pass.
- Connector readback verified target document identity, inserted appendix
  headings, final companion rule paragraph and updated top status text.

### 2026-06-13. Introduction and Part I first compression/editorial pass

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-i.md`

Google Doc content updated:

- `Введение. Зачем эта книга нужна`;
- `Часть I. От demo-агента к платформе` bridge;
- `Глава 2. Когда нужен агент: workflow, single-agent, multi-agent`;
- `Глава 3. Референсная архитектура безопасной агентной системы`.

Notes:

- Chapter 1 was preserved as the previously edited sample and was not
  overwritten.
- Introduction now explains book/companion split, audience and production-agent
  framing more directly.
- Chapter 2 now reads as a decision ladder from direct model calls to workflow,
  single-agent loops, coordinator patterns and explicit handoff.
- Chapter 3 now emphasizes failure-oriented architecture checks: identity,
  policy, context boundary, шлюз инструментов, trace evidence and rollout ownership.
- Google Doc stale service status was updated from the old Part IV/V next step
  to the current Part II/III editorial pass.

### 2026-06-14. Part II and Part III first compression/editorial pass

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-ii-iii.md`

Google Doc content updated:

- `Часть II. Безопасность и контур управления`;
- `Глава 4. Контур безопасности и границы доверия`;
- `Глава 5. Identity, session, policy layer и capability model`;
- `Глава 6. Инструментальный шлюз, подтверждения и журнал аудита`;
- `Часть III. Память, знания и контекст`;
- `Глава 7. Зачем агенту память и почему она опасна`;
- `Глава 8. Краткосрочная, долгосрочная и профильная память`;
- `Глава 9. Извлечение контекста, уплотнение и фоновые обновления`.

Notes:

- Part II now frames agent security as a question of trust boundaries and the
  right to convert intent into action.
- Chapter 5 now gives Russian explanations for policy layer and capability
  model while keeping the contract terms.
- Chapter 6 now emphasizes the шлюз инструментов as the central contract for turning
  model intent into a managed side effect.
- Part III now frames memory as durable state that requires provenance, TTL,
  trust level, read/write policy and rollback.
- Chapter endings were normalized from repeated `Что запомнить` to `Ключевой
  вывод` for this batch.
- Google Doc status text now points to the next compression/editorial batch:
  Part IV + Part V.

### 2026-06-14. Part IV and Part V first compression/editorial pass

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-iv-v.md`

Google Doc content updated:

- `Часть IV. Инструменты, выполнение и интеграция`;
- `Глава 10. Модель выполнения и каталог инструментов`;
- `Глава 11. Песочница выполнения и MCP как интеграционный контракт`;
- `Глава 12. Идемпотентность, повторы, лимиты и границы отката`;
- `Часть V. Надежность, наблюдаемость и оценки`;
- `Глава 13. Трассы, спаны и структурированные события`;
- `Глава 14. SLO для агентных систем`;
- `Глава 15. Офлайн- и онлайн-оценки и регрессионные шлюзы`;
- `Глава 16. Сквозная цепочка доказательств: от запроса к rollout`.

Notes:

- Tool gateway, MCP, SLO, evals and evidence chain are now introduced with
  Russian explanatory framing before retaining the technical English term.
- Repeated chapter endings were normalized to `Ключевой вывод`.
- Google Doc readback verified the updated top status, Part IV terminology
  changes and absence of the old `Что запомнить` marker.

### 2026-06-14. Part VI and Part VII first compression/editorial pass

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-vi-vii.md`

Google Doc content updated:

- `Часть VI. Организационная модель и жизненный цикл`;
- `Глава 17. Платформенная команда и продуктовые команды`;
- `Глава 18. Golden paths, общие шлюзы и борьба с агентным зоопарком`;
- `Глава 19. От SDLC к ADLC: жизненный цикл агентной системы`;
- `Глава 20. Assurance loop, реагирование на инциденты, registry и retirement`;
- `Часть VII. Эталонная реализация и промышленный запуск`;
- `Глава 21. Базовая схема runtime`;
- `Глава 22. Слой политик и каталог возможностей`;
- `Глава 23. Чеклист промышленного запуска`.

Notes:

- Organizational vocabulary now maps golden path, assurance loop, registry and
  retirement to explicit Russian concepts.
- ADLC and runtime sections were tightened so the final part reads as an
  operational launch model, not as package documentation.
- Google Doc readback verified that the old ownership wording and old ADLC
  wording were removed from the manuscript.

### 2026-06-14. Appendices first compression/editorial pass

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-appendices.md`

Google Doc content updated:

- `Приложения`;
- `Приложение 1. Глоссарий`;
- `Приложение 2. Чеклисты`;
- `Приложение 3. Шаблон incident/postmortem`;
- `Приложение 4. Источники и онлайн-сопровождение`.

Notes:

- Appendices now explicitly remain a short print companion rather than the full
  online reference package.
- Glossary wording was tightened around capability catalog, verifier and
  retirement.
- Google Doc readback verified updated appendix terminology and the final
  companion rule paragraph.

### 2026-06-14. High-level editorial roadmap

Status: roadmap created and synced to Google Doc as a working editorial block.

Local source:

- `docs/publisher/ru-editorial-roadmap.md`

Google Doc content updated:

- top status now points to structural, terminology, cross-reference and
  companion-boundary passes;
- service/front-matter area is explicitly marked as not part of the final
  manuscript delivery;
- a working editorial roadmap was added before the manuscript structure/body.

Notes:

- This is not a line edit. It is the high-level plan for the remaining
  publisher-prep work after the full first compression/editorial pass.
- БХВ formatting and DOCX/export QA remain blocked until style files arrive.

### 2026-06-14. Introduction and Part I structural pass

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-i.md`

Google Doc content updated:

- top status now says structural editorial pass started and Introduction /
  Part I completed;
- Introduction now states the reader contract explicitly: the book is a map of
  responsibility and control layers, not a collection of agent patterns;
- Part I bridge now has clear exit criteria before the security part;
- Chapter 2 now transitions into Chapter 3 instead of ending as a standalone
  taxonomy;
- Chapter 3 now closes Part I and hands off to Part II security.

Notes:

- This is a structural pass, not a full terminology or line edit.
- Next structural batch should cover Part II and Part III.

### 2026-06-14. Part II and Part III structural pass

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-ii-iii.md`

Google Doc content updated:

- top status now says Introduction and Parts I-III completed for structural
  pass;
- roadmap progress now marks Introduction and Parts I-III complete;
- Part II now frames security as a route through trust boundaries rather than
  a single model filter;
- Part II has explicit exit criteria: trust boundary, subject, policy decision,
  capability, approval and audit record;
- Chapter 6 now hands off from right-to-act controls to memory and context;
- Part III now separates memory write, retrieval and background maintenance as
  distinct contracts;
- Chapter 9 now hands off from context quality to tool execution and integration.

Notes:

- This is a structural pass, not a full terminology or line edit.
- Next structural batch should cover Part IV and Part V.

### 2026-06-14. Part IV and Part V structural pass

Status: synced to Google Doc.

Local assembly source:

- `docs/publisher/ru-manuscript-assembly-part-iv-v.md`

Google Doc content updated:

- top status now says Introduction and Parts I-V completed for structural pass;
- roadmap progress now marks Introduction and Parts I-V complete;
- Part IV now gives explicit exit criteria for tool execution: capability
  owner, contract, sandbox, idempotency key, limits, normalized outcome and
  recovery path;
- Chapter 12 now hands off from execution mechanics to evidence and rollout
  decisions;
- Part V now frames trace, SLO, evals and evidence chain as one decision
  system rather than separate observability topics;
- Chapter 16 now hands off from technical evidence to organizational ownership,
  lifecycle and launch governance.

Notes:

- This is a structural pass, not a full terminology or line edit.
- Next structural batch should cover Part VI, Part VII and appendices.

### 2026-06-14. Part VI, Part VII and appendices structural pass

Status: synced to Google Doc.

Local assembly sources:

- `docs/publisher/ru-manuscript-assembly-part-vi-vii.md`
- `docs/publisher/ru-manuscript-assembly-appendices.md`

Google Doc content updated:

- `Часть VI. Организационная модель и жизненный цикл`;
- `Глава 20. Assurance loop, реагирование на инциденты, registry и retirement`;
- `Часть VII. Эталонная реализация и промышленный запуск`;
- `Глава 23. Чеклист промышленного запуска`;
- `Приложения`;
- `Приложение 4. Источники и онлайн-сопровождение`.

Notes:

- Added exit criteria for Part VI and Part VII.
- Added the bridge from organizational lifecycle to reference runtime.
- Added appendix framing and final manuscript closure.
- This checkpoint completes the first structural pass across the whole
  manuscript. Remaining work is terminology, glossary alignment,
  cross-references, companion-boundary and later publisher styling.

### 2026-06-14. First terminology/glossary anchor batch

Status: synced to Google Doc.

Local sources updated:

- `docs/publisher/ru-terminology.md`
- `docs/publisher/ru-manuscript-assembly-part-vi-vii.md`
- `docs/publisher/ru-manuscript-assembly-appendices.md`

Google Doc content updated:

- `assurance loop` canonical Russian form changed to `контур заверения`;
- Part VI and Part VII headings and body anchors now prefer reader-facing
  Russian forms for runtime, inventory, registry discipline and retirement;
- appendix glossary anchors now define capability, principal, tenant,
  lifecycle and шлюз инструментов in Russian-first form.

Notes:

- This is not the full terminology pass across the whole manuscript.
- Remaining terminology work should continue through Parts I-V, then verify
  glossary consistency, cross-references and companion-boundary language.

### 2026-06-15. Second terminology anchor batch

Status: synced to Google Doc.

Local sources updated:

- `docs/publisher/ru-manuscript-assembly-part-i.md`
- `docs/publisher/ru-manuscript-assembly-part-ii-iii.md`
- `docs/publisher/ru-manuscript-assembly-part-iv-v.md`

Google Doc content updated:

- Introduction and Part I now prefer Russian-first forms for environment,
  workflow, policy layer, шлюз инструментов, rollout gates and trace;
- Parts II-III now prefer Russian-first forms for identity, session, policy
  layer, capability model, шлюз инструментов and audit record;
- Parts IV-V now prefer Russian-first forms for execution layer, шлюз инструментов,
  trace, span, rollout decision and evidence chain.

Notes:

- English lookup terms remain at first explanation or in field/code names.
- Remaining terminology work should verify consistency chapter-by-chapter and
  then move into cross-reference and companion-boundary passes.

### 2026-06-15. P1 terminology and appendix consistency batch

Status: synced to Google Doc.

Local sources updated:

- `docs/publisher/ru-manuscript-assembly-part-vi-vii.md`
- `docs/publisher/ru-manuscript-assembly-appendices.md`
- `docs/publisher/ru-editorial-roadmap.md`
- `docs/publisher/ru-submission-checklist.md`

Google Doc content updated:

- Parts VI-VII now use Russian-first reader-facing language for ADLC artifacts,
  supported paths, assurance loop, реагирование на инциденты, registry, retirement,
  reference runtime and launch checklist;
- appendices now use the same vocabulary in glossary entries, review
  checklists, incident/postmortem template and companion map;
- stale `case-spine note` and `canonical cases` service labels were checked
  across assembled manuscript sources and are not present in reader-facing prose.

Notes:

- English remains only for first-use lookup terms, code-like identifiers,
  established security practices or source titles.
- Next editorial work should move from terminology into cross-reference,
  companion-link stability, print readability and final proofread.

### 2026-06-15. Current-source editorial readiness pass

Status: synced to Google Doc.

Local sources updated:

- `docs/publisher/ru-submission-checklist.md`
- `docs/publisher/ru-editorial-roadmap.md`
- `docs/publisher/ru-google-doc-workflow.md`
- `docs/publisher/ru-publisher-packet-v0.1.md`
- `docs/publisher/ru-cover-note-draft.md`
- `docs/publisher/ru-manuscript-assembly-appendices.md`

Google Doc content updated:

- manuscript status now reflects full Introduction, Parts I-VII and appendices
  in the Google Doc;
- service/body boundary is explicit: working blocks above `Начало основного
  текста книги` are not part of the final manuscript unless promoted into front
  matter;
- companion map now includes the public site and source repository links;
- checklist and roadmap mark cross-reference, companion-boundary,
  print-readability and current-source proofread gates complete.

Notes:

- Author fields remain intentionally open because they require factual input
  from the author.
- Publisher style files from БХВ and DOCX/export QA remain deferred until the
  style package arrives.
- Final external proofread should happen after the export shape is stable.

### 2026-06-15. Volume gap correction

Status: synced to Google Doc status blocks.

Finding:

- Google Doc page count and local word counts show that the document contains a
  compressed structural assembly, not a full publisher manuscript.
- Local publisher assembly files contain about 17k words, while the Russian
  source corpus under `docs/book` and `docs/appendix` contains about 114k words
  excluding `.en.md` and `.zh.md` variants.
- The contract map targets 425-497 pages before real layout QA, so a 71-page
  Google Doc cannot be treated as a near-final manuscript.

Correction:

- Status language must distinguish `7/23 structure is present` from `full book
  volume is ready`.
- The next practical workstream is manuscript expansion from Markdown sources,
  not publisher email preparation.
- Terminology, cross-reference, companion-boundary and proofread passes must be
  repeated after expansion.

### 2026-06-15. Full source-to-print manuscript import

Status: synced to full Google Doc.

Local sources updated:

- `docs/publisher/ru-manuscript-full.md`
- `docs/publisher/ru-submission-checklist.md`
- `docs/publisher/ru-google-doc-workflow.md`
- `docs/publisher/ru-editorial-roadmap.md`
- `docs/publisher/ru-publisher-packet-v0.1.md`
- `docs/publisher/ru-cover-note-draft.md`

Google Docs:

- Full manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- The older 71-page document is retained only as compressed/staging snapshot:
  <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

Evidence:

- full manuscript Markdown contains 109,250 words after structural cleanup;
- generated DOCX rendered to 437 pages in smoke QA, with no blank/near-blank
  page PNGs detected;
- Google Docs readback confirmed the full 7/23 structure marker, Chapter 1,
  Chapter 13, Chapter 23, appendices, and public companion link;
- Google Docs readback no longer finds the old `Часть VIII` / Chapter 24
  structure markers.

Notes:

- This closes the volume gap: the Google Doc is no longer a compressed
  editorial assembly.
- This does not close final publisher submission gates: author fields, БХВ
  styles, export DOCX QA and external proofread remain open.

### 2026-06-17. Book-readiness second pass started

Status: active editorial pass after full-volume import.

Local sources updated:

- `docs/publisher/ru-book-readiness-audit.md`
- `docs/publisher/ru-editorial-roadmap.md`
- `docs/publisher/ru-submission-checklist.md`
- `docs/publisher/ru-google-doc-workflow.md`
- `docs/publisher/ru-manuscript-map.md`

Google Docs:

- Book-readiness editorial map:
  <https://docs.google.com/document/d/1XoU_nWZkpKGU7SxZ0pgmE_dfcNNggQokZsbzind7kXc>
- Full manuscript remains:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Finding:

- Full volume is not the same as finished book quality.
- Current manuscript assembly has about 112.8k words, 23 chapters and 4
  appendices.
- Chapter 20 is the largest structural risk: about 15.8k words and 113
  subheadings.
- Chapter 21 is the second largest risk: about 10.5k words and too much
  runtime/manual material for a printed chapter.
- Chapters 5 and 22 need an overlap pass so conceptual policy/capability
  material and reference implementation material do not repeat each other.
- Repeated endings such as `Что сделать сразу`, `Что делать дальше` and
  `Что читать дальше` need normalization into a compact book rhythm.

Decision:

- Treat the full Google Doc as the canonical working manuscript.
- Treat `docs/publisher/ru-book-readiness-audit.md` and the Google Docs
  editorial map as the active control layer for the second editorial pass.
- Do not claim publisher-ready status until the book-readiness pass, author
  fields, publisher styles, export QA and external proofread are complete.

### 2026-06-17. Introduction reader-contract rewrite

Status: synced to full Google Doc manuscript.

Local source added:

- `docs/publisher/ru-book-ready-introduction.md`

Google Doc update:

- Replaced the old duplicated introduction block in the full manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Verification:

- New text found in Google Docs readback: `Эта книга начинается с различия`.
- Old duplicated intro marker no longer found:
  `Введение фиксирует читательский контракт`.
- Old route duplicate no longer found: `Маршрут на 30 минут`.
- `Часть I. От demo-агента к платформе` remains immediately after the
  rewritten introduction.

Notes:

- This starts book-readiness batch 1.
- Next batch 1 tasks are Chapter 1 sample line edit, Chapter 2 decision-ladder
  rebuild and Chapter 3 bridge into Part II.

### 2026-06-18. Chapter 1 sample-chapter line edit

Status: synced to full Google Doc manuscript.

Local source added:

- `docs/publisher/ru-book-ready-chapter-1.md`

Google Doc update:

- Replaced the full Chapter 1 body in the full manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Editorial intent:

- keep Chapter 1 as the primary sample chapter;
- remove web/admonition rhythm and repeated proof-model tail sections;
- make the chapter read as one argument: demo failure -> missing platform
  layers -> workflow-first decision rule -> practical operating minimum;
- preserve the support-triage case as the opening running scenario;
- make the transition into Chapter 2 explicit.

Verification:

- New Chapter 1 marker found in Google Docs readback:
  `Эта глава нужна, чтобы поставить главный инженерный фильтр`.
- Old Chapter 1-specific section no longer found:
  `Что Викулин поставил правильно`.
- Chapter 2 heading remains after the replaced Chapter 1 range:
  `Глава 2. Когда нужен агент: рабочий процесс, одиночный агентный цикл,
  многоагентная схема`.

Notes:

- Next batch 1 task is Chapter 2 decision-ladder rebuild.

### 2026-06-18. Chapter 2 decision-ladder rebuild

Status: synced to full Google Doc manuscript.

Local source added:

- `docs/publisher/ru-book-ready-chapter-2.md`

Google Doc update:

- Replaced the full Chapter 2 body in the full manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Editorial intent:

- make Chapter 2 the practical continuation of Chapter 1;
- rebuild the chapter around the execution-form ladder: direct model call,
  workflow, single-agent loop, coordinator and handoff;
- remove the stitched SOP/YAML and coordinator/handoff reference blocks from
  the main chapter body;
- make Chapter 3 the next step: platform layers required after the execution
  form is chosen.

Verification:

- New Chapter 2 marker found in Google Docs readback:
  `В этой главе мы пройдем лестницу выбора`.
- Old stitched YAML marker no longer found: `routines:`.
- Manual insertion typo marker no longer found: `системойой`.
- Chapter 3 heading remains after the replaced Chapter 2 range:
  `Глава 3. Референсная архитектура безопасной агентной системы`.

Notes:

- Next batch 1 task is Chapter 3 bridge into Part II.

### 2026-06-18. Chapter 3 bridge into Part II

Status: synced to full Google Doc manuscript.

Local source added:

- `docs/publisher/ru-book-ready-chapter-3-bridge.md`

Google Doc update:

- Replaced the old service/proof tail at the end of Chapter 3 with a compact
  bridge into Part II:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Editorial intent:

- keep Chapter 3 focused on the platform architecture map;
- remove stale internal transition text and the repeated proof-model tail;
- make the transition to safety/control explicit: identity, policy,
  confirmation, шлюз инструментов, audit and trust boundaries.

Verification:

- New bridge marker found in Google Docs readback:
  `С этой точки начинается часть II`.
- Old stale transition no longer found: `переходи к Главе 3`.
- Part II heading remains immediately after the Chapter 3 bridge:
  `Часть II. Безопасность и контур управления`.

Notes:

- Book-readiness batch 1 is complete: introduction, Chapter 1, Chapter 2 and
  Chapter 3 bridge are now synced to the full Google Doc manuscript.
- Next workstream is batch 2: safety/control and Chapter 5/22 overlap.

### 2026-06-18. Chapter 5 identity/policy/capability rewrite

Status: synced to full Google Doc manuscript.

Local source added:

- `docs/publisher/ru-book-ready-chapter-5.md`

Google Doc update:

- Replaced the overloaded Chapter 5 body in the full manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Editorial intent:

- make Chapter 5 the conceptual control-model chapter, not an early runtime
  implementation reference;
- separate identity, session, policy decisions and capability model from raw
  tool/config details;
- preserve the support-triage, knowledge-assistant and incident-coordination
  scenarios as the practical spine;
- leave `policy.yaml`, runnable package inspection and implementation fields
  for Chapter 22 and the онлайн-сопровождение.

Verification:

- New Chapter 5 marker found in Google Docs readback:
  `Эта глава собирает четыре понятия в один контур`.
- Chapter 6 heading remains after the replaced Chapter 5 range:
  `Глава 6. Инструментальный шлюз, подтверждения и журнал аудита`.
- Old Chapter 22 implementation marker still exists only later in the document,
  which confirms the conceptual material was not deleted from the implementation
  part by accident.

Notes:

- Batch 2 is in progress. The next task is to make Chapter 22 explicitly
  implementation-focused and remove remaining conceptual repetition there.

### 2026-06-18. Chapter 22 implementation-focused rewrite

Status: synced to full Google Doc manuscript.

Local source added:

- `docs/publisher/ru-book-ready-chapter-22.md`

Google Doc update:

- Replaced the full Chapter 22 body in the full manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Editorial intent:

- make Chapter 22 the executable reference-implementation counterpart to the
  conceptual Chapter 5;
- focus the chapter on `policy.yaml`, `capabilities.yaml`, runtime inspection,
  trace evidence and write-path failure behavior;
- remove the repeated argument that policy/capability form the conceptual right
  to action;
- keep long CLI walkthroughs, validation errors, YAML variants and loader
  internals in the companion.

Verification:

- New Chapter 22 marker found in Google Docs readback:
  `Глава 22 не должна повторять аргумент о праве на действие`.
- Chapter 23 heading remains after the replaced Chapter 22 range:
  `Глава 23. Чеклист промышленного запуска`.

Notes:

- The Chapter 5/22 overlap is resolved. The next second-pass target is the
  overloaded late-book runtime/lifecycle material in Chapters 20 and 21.

### 2026-06-28. Editor handoff readiness pass

Status: synced to full Google Doc manuscript.

Google Doc update:

- Applied a targeted style-only batchUpdate to the full Google Doc manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Two ordinary body ranges that had inherited `Heading 1` were normalized back
  to normal text:
  - chapter 3 bridge/practicum range before `Часть II`;
  - chapter 20 assurance-loop range before `Часть VII`.
- True structural subheads in those ranges were restored as H2/H3.

Artifacts added:

- `docs/publisher/artifacts/agent-arch-ru-editor-handoff-pass-2026-06-28.docx`
- `docs/publisher/ru-editor-handoff-packet-2026-06-28.md`
- `docs/publisher/ru-editor-handoff-readiness-pass-2026-06-28.md`
- `docs/publisher/ru-editor-handoff-readiness-pass-2026-06-28.render-qa.json`
- `docs/publisher/ru-author-open-fields-2026-06-28.md`
- `docs/publisher/ru-editorial-100-editor-handoff-iterations-2026-06-28.md`

Proof metrics:

- Raw Google Docs export render: 552 pages.
- Blank-like pages: 0.
- DOCX paragraph count: 8040.
- Heading 1 paragraphs after cleanup: 26.
- Heading 2 paragraphs: 1393.
- Heading 3 paragraphs: 578.
- Long H2 paragraphs flagged as remaining style debt: 629.

Decision:

- The manuscript is suitable for controlled editor handoff as a working Google
  Doc, but not for final publisher-ready DOCX delivery.
- Before final export, run a global heading normalization pass that demotes
  long body-like H2 paragraphs while preserving the real chapter/section
  hierarchy.
- Keep Template2000n as a derived proof route after heading normalization, not
  as the live Google Doc source.

### 2026-06-28. Global heading normalization pass

Status: synced to full Google Doc manuscript.

Google Doc update:

- Applied three guarded style-only Google Docs `batchUpdate` batches to the full
  manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Demoted 629 long body-like `Heading 2` paragraphs to normal text.
- Preserved manuscript text and paragraph count.

Artifacts added:

- `docs/publisher/artifacts/agent-arch-ru-heading-normalization-baseline-2026-06-28.docx`
- `docs/publisher/artifacts/agent-arch-ru-heading-normalized-2026-06-28.docx`
- `docs/publisher/artifacts/agent-arch-ru-template2000n-heading-normalized-2026-06-28.docx`
- `docs/publisher/ru-google-doc-heading-normalization-pass-2026-06-28.md`
- `docs/publisher/ru-google-doc-heading-normalization-pass-2026-06-28.render-qa.json`
- `docs/publisher/ru-editorial-100-heading-normalization-iterations-2026-06-28.md`

Proof metrics:

- Raw Google Docs export render: 504 pages.
- Raw blank-like pages: 0.
- Template2000n render: 315 pages.
- Template2000n blank-like pages: 0.
- Non-empty `Heading 2` paragraphs after cleanup: 764.
- Long non-empty `Heading 2` paragraphs after cleanup: 0.

Decision:

- The H2/body pollution that blocked a credible publisher-style proof is closed.
- The next formatting pass should target long H3/body-like paragraphs before
  final publisher-ready DOCX delivery.

### 2026-06-28. H3/body-style normalization pass

Status: synced to full Google Doc manuscript.

Google Doc update:

- Applied one guarded style-only Google Docs `batchUpdate` batch to the full
  manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Demoted 65 long body-like `Heading 3` paragraphs to normal text.
- Preserved manuscript text and paragraph count.

Artifacts added:

- `docs/publisher/artifacts/agent-arch-ru-h3-normalized-2026-06-28.docx`
- `docs/publisher/artifacts/agent-arch-ru-template2000n-h3-normalized-2026-06-28.docx`
- `docs/publisher/ru-google-doc-h3-normalization-pass-2026-06-28.md`
- `docs/publisher/ru-google-doc-h3-normalization-pass-2026-06-28.render-qa.json`
- `docs/publisher/ru-editorial-100-h3-normalization-iterations-2026-06-28.md`

Proof metrics:

- Raw Google Docs export render: 499 pages.
- Raw blank-like pages: 0.
- Template2000n render: 315 pages.
- Template2000n blank-like pages: 0.
- Long non-empty `Heading 2` paragraphs after cleanup: 0.
- Long non-empty `Heading 3` paragraphs after cleanup: 0.

Decision:

- Long H2/H3 body-style debt is closed for the current proof.
- Remaining publisher blockers are author-owned fields, final proofread,
  publisher style application, DOCX/export QA after styles and external
  proofread.

### 2026-07-01. Latest practices sync pass

Status: synced to local full manuscript and full Google Doc working manuscript.

Local manuscript update:

- Added 13 late practical sections from `docs/book/**` to
  `docs/publisher/ru-manuscript-full.md`.
- Verified that each of the 13 control practice headings appears exactly once
  in the local full manuscript.
- Inserted source volume: 2360 lines, with heading levels demoted one level for
  publisher-manuscript hierarchy.

Google Doc update:

- Added eight missing late practice blocks in print-oriented form to the full
  Google Doc manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Fresh plain-text readback: 1,266,284 bytes, 766,889 characters and 101,584
  approximate words.
- Each of the eight newly inserted Google Doc practice headings appears exactly
  once in the readback export.

Artifacts added:

- `docs/publisher/ru-latest-practices-sync-pass-2026-07-01.md`
- `docs/publisher/ru-editorial-100-latest-practices-sync-iterations-2026-07-01.md`

Decision:

- The working manuscript is materially stronger for substantive/editorial
  review because late source practices are now represented in both local and
  Google Doc manuscript layers.
- The pass is not a final publisher export. The 2026-06-28 DOCX proofs are now
  previous proof snapshots; a fresh DOCX/export QA pass is needed after
  author-owned fields, publisher style application and final proofread.

### 2026-07-02. Practice-polish working proof pass

Status: synced to full Google Doc working manuscript and recorded as a fresh
raw DOCX proof.

Google Doc update:

- Polished wording in the late practice blocks that were added during the
  2026-07-01 latest-practices sync.
- Replaced arrow-heavy or hybrid headings with print-readable headings:
  `trace, SLO, eval и rollout`; `золотой путь (golden path)`; `trace, eval
  gate, rollout wave и containment`.
- Preserved the deliberate distinction between the complete local source
  assembly and the more print-oriented Google Doc practice blocks.

Artifacts added:

- `docs/publisher/artifacts/agent-arch-ru-practice-polished-working-proof-2026-07-02.docx`
- `docs/publisher/ru-google-doc-practice-polish-proof-pass-2026-07-02.md`
- `docs/publisher/ru-google-doc-practice-polish-proof-pass-2026-07-02.render-qa.json`
- `docs/publisher/ru-author-fields-after-practice-polish-2026-07-02.md`
- `docs/publisher/ru-editorial-100-practice-polish-proof-iterations-2026-07-02.md`

Proof metrics:

- Google Doc readback: approximately 101,715 words.
- Local full manuscript: approximately 123,082 words.
- Raw Google Docs export render: 513 pages.
- Raw blank-like pages: 0.
- Known layout issue: page 338 contains a one-line checklist carryover with a
  large blank area and should be fixed in the next publisher-style/layout pass.

Decision:

- The current Google Doc and 2026-07-02 raw DOCX proof are the best working
  editor-review artifacts after practice polish.
- Final publisher submission remains blocked until author-owned fields,
  external proofread, publisher styles, page-level layout cleanup and final
  raw/Template2000n render QA are complete.

### 2026-07-03. Layout/style proof pass

Status: synced to full Google Doc working manuscript and recorded as fresh raw
and Template2000n working proofs.

Google Doc update:

- Fixed the known page-338 checklist carryover from the practice-polish proof.
- Added a page break before the SLO practice that previously risked an orphan
  heading.
- Demoted five late-practice body ranges from heading styles to normal text.
- Promoted three late practice headings to `Heading 2` so all 14 practice
  sections are navigable.

Artifacts added:

- `docs/publisher/artifacts/agent-arch-ru-layout-style-pass-2026-07-02.docx`
- `docs/publisher/artifacts/agent-arch-ru-template2000n-layout-style-pass-2026-07-02.docx`
- `docs/publisher/ru-google-doc-layout-style-pass-2026-07-03.md`
- `docs/publisher/ru-google-doc-layout-style-pass-2026-07-03.render-qa.json`
- `docs/publisher/ru-editorial-100-layout-style-proof-iterations-2026-07-03.md`

Proof metrics:

- Raw proof render: 507 pages, 0 blank-like pages.
- Template2000n derivative render: 371 pages, 0 blank-like pages.
- Raw non-empty text equals the previous practice-polish proof non-empty text.
- Raw paragraph text equals the Template2000n derivative paragraph text.

Decision:

- The current Google Doc and the two 2026-07-02 DOCX proofs are the best
  working layout/style proof artifacts for editorial review.
- Final publisher submission remains blocked until author-owned fields,
  external proofread, publisher-approved style requirements and final export QA
  are closed.

### 2026-07-04. Quality-sync terminology and Template2000n pass

Status: synced to the full Google Doc working manuscript for terminology
cleanup and recorded as a new styled DOCX proof from the latest valid raw DOCX
baseline.

Google Doc update:

- Applied 293 guarded exact terminology replacements to reduce excessive
  English editorial terms in ordinary prose, then 23 grammatical corrections
  for broad `tool call`/`human review` replacements.
- Kept code identifiers, protocol names and accepted technical terms intact.
- Readback found no exact `online companion`, `policy gateway`, `tool gateway`
  or `incident response`.

Artifacts added:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-quality-sync-2026-07-04.docx`
- `docs/publisher/ru-google-doc-quality-sync-pass-2026-07-04.md`
- `docs/publisher/ru-google-doc-quality-sync-pass-2026-07-04.render-qa.json`
- `docs/publisher/ru-template2000n-quality-sync-2026-07-04.metrics.json`
- `docs/publisher/ru-editorial-100-quality-sync-export-iterations-2026-07-04.md`
- `docs/publisher/tools/build_template2000n_derivative.py`
- `docs/publisher/tools/render_qa_metrics.py`
- `docs/publisher/tools/apply_ru_terminology_replacements.py`

Proof metrics:

- Raw baseline render: 489 pages, 0 blank-like pages.
- Template2000n quality-sync render: 357 pages, 0 blank-like pages.
- Raw paragraph text equals the Template2000n derivative paragraph text.
- Body paragraphs mapped to `Body Text`: 4953.

Decision:

- The Google Doc is cleaner after terminology cleanup, and the repository has a
  fresh styled proof for editor discussion.
- Final publisher submission remains blocked until a fresh authenticated raw
  DOCX export is saved from the updated Google Doc, author-owned fields are
  filled or explicitly omitted, and external proofread is complete.

### 2026-07-04. Post-terminology raw export and Template2000n proof

Status: the previous fresh-export blocker is closed for the current Google Doc
revision.

Google Doc update:

- Added a follow-up direct cleanup after the broad terminology pass: fixed
  `rollout wave`, broken `вызов инструментаing` forms, remaining
  `Online companion` / `Companion route` wording and several online-support
  падежные errors.
- Final Google Doc revision for this checkpoint:
  `ALtnJHzZWz2-IJ7JpxskwAFAeTHIK5wTRmKA_MrDjFTgOlPIbOMvFgV7Go8Trlwx1WPtElObAQ1OmEI0Tbg7i8I4NJ5RyfZdmR8apePtOyc`.

Artifacts added:

- `docs/publisher/artifacts/agent-arch-ru-post-terminology-raw-2026-07-04.docx`
- `docs/publisher/artifacts/agent-arch-ru-template2000n-post-terminology-2026-07-04.docx`
- `docs/publisher/ru-google-doc-post-terminology-export-pass-2026-07-04.md`
- `docs/publisher/ru-google-doc-post-terminology-export-pass-2026-07-04.render-qa.json`
- `docs/publisher/ru-template2000n-post-terminology-2026-07-04.metrics.json`
- `docs/publisher/ru-editorial-100-post-terminology-export-iterations-2026-07-04.md`

Proof metrics:

- Fresh raw Google Docs export: 493 pages, 0 blank-like pages.
- Template2000n post-terminology derivative: 359 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Approximate words: 99884.
- Body paragraphs mapped to `Body Text`: 4957.

Decision:

- The best current publisher-facing proof is now
  `docs/publisher/artifacts/agent-arch-ru-template2000n-post-terminology-2026-07-04.docx`.
- Final publisher submission remains blocked by author-owned fields,
  independent external proofread and any publisher style requirements received
  after this checkpoint.

### 2026-07-05. Visual/edit manuscript pass

Status: synced to the full Google Doc working manuscript and recorded as the
current visual/edit DOCX proof pair.

Google Doc update:

- Added 12 Russian-language diagrams as an editor-facing visualization block in
  the Google Doc, with captions and alt text.
- Updated the Markdown manuscript source with the same diagrams placed at the
  relevant chapter points.
- Fixed outdated cross-references to the reference-architecture and launch
  checklist chapters.
- Demoted repeated reference-package reset headings and compressed long
  CLI/API/reference paragraphs into companion routes.
- Final Google Doc revision for this checkpoint:
  `ALtnJHxx8GXfQQfPMrGfG7STCXtscwWkhPzWpj1AJa-vee0UADj3vnwYNiZkKG2wGfd2Xkdsizblmxq8xb8YyumfJxKOb8ujAWDn1wNGphY`.

Artifacts added:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-visual-edit-2026-07-05.docx`
- `docs/publisher/artifacts/agent-arch-ru-template2000n-visual-edit-2026-07-05.docx`
- `docs/publisher/ru-google-doc-visual-edit-pass-2026-07-05.md`
- `docs/publisher/ru-google-doc-visual-edit-pass-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-visual-edit-2026-07-05.metrics.json`
- `docs/publisher/ru-companion-cli-api-reference-2026-07-05.md`
- `docs/publisher/ru-editorial-100-visual-edit-iterations-2026-07-05.md`
- `docs/publisher/visuals/*.png`

Proof metrics:

- Fresh raw Google Docs export: 501 pages, 0 blank-like pages.
- Template2000n visual/edit derivative: 366 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Approximate words: 100045.
- Embedded images: 12 PNG files in both DOCX artifacts.
- Long paragraphs with 250+ words: 0 in both DOCX artifacts.

Decision:

- The best current publisher-facing proof is now
  `docs/publisher/artifacts/agent-arch-ru-template2000n-visual-edit-2026-07-05.docx`.
- Final publisher submission remains blocked by author-owned fields, public
  companion metadata, independent external proofread and publisher/editor
  acceptance of the final style route.

### 2026-07-05. Dedup/source sync pass

Status: synced to the working Google Doc and recorded as the current
dedup/source-sync proof pair.

Google Doc update:

- Added the Chapter 15 control-evaluation block based on
  `docs/book/part-viii/chapter-25.md`.
- Added the Chapter 20 agentic goal-misalignment / insider-risk block based on
  `docs/book/part-viii/chapter-24.md`.
- Replaced the Drive file content with a cleaned raw DOCX while preserving the
  same Google Doc URL.
- Final Google Doc revision for this checkpoint:
  `ALtnJHwGtFDgVCf6_JsoFEjMfHn75ueCJlj2C8HpZzRnob5wivqplwPUQFb9RaPzwK16ayiEdl36eAkPEbYcOhGd7FuUd0sIj_W2fBRp6tw`.

Repository/source update:

- `docs/publisher/ru-manuscript-full.md` now has 111785 words and 0 exact
  duplicate paragraph groups with 35+ words after removing large repeated
  reference/package,
  policy/catalog, incident-template and checklist sections.
- Integrity follow-up corrected stale cross-references to the renumbered
  chapters and removed visible mixed suffix forms from the current DOCX/Google
  Doc proof.
- `docs/publisher/ru-source-map.md` now records the Chapter 24/25 source
  contributions.

Artifacts added:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- `docs/publisher/ru-google-doc-dedup-source-sync-pass-2026-07-05.md`
- `docs/publisher/ru-google-doc-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.metrics.json`

Proof metrics:

- Raw Google Doc DOCX: 513 pages, 0 blank-like pages.
- Template2000n derivative: 370 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Approximate words: 103124.
- Long paragraphs with 250+ words: 0 in raw DOCX.

Decision:

- The best current publisher-facing proof is now
  `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`.
- Final publisher submission remains blocked by author-owned fields, public
  companion metadata, independent external proofread and publisher/editor
  acceptance of the final style route.

### 2026-07-05. Reader recommendability pass

Status: synced to the working Google Doc and recorded as the current
reader-facing proof pair.

Implemented changes:

- strengthened the opening reader promise;
- added part-level story checkpoints where the compressed DOCX structure
  exposes the part heading;
- added 6 production failure scenes to Chapters 1-6;
- added 10 continuity bridges across Chapters 7-16;
- added 6 maturity bridges across Chapters 17-22 and a final assembly block in
  Chapter 23;
- added 23 chapter takeaway blocks;
- recorded 100 controlled editorial micro-iterations in
  `docs/publisher/ru-editorial-100-reader-recommendability-iterations-2026-07-05.md`.

Proof metrics:

- Raw Google Doc DOCX: 513 pages, 0 blank-like pages.
- Template2000n derivative: 370 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Approximate words: 103124.
- Final known Google Doc revision:
  `ALtnJHwGtFDgVCf6_JsoFEjMfHn75ueCJlj2C8HpZzRnob5wivqplwPUQFb9RaPzwK16ayiEdl36eAkPEbYcOhGd7FuUd0sIj_W2fBRp6tw`.

Report:

- `docs/publisher/ru-reader-recommendability-pass-2026-07-05.md`


### 2026-07-05. Three reader profiles recommendability pass

Status: synced to the working Google Doc and recorded as the current
reader-facing proof pair.

Implemented changes:

- added explicit reader routes for technical leads/architects, engineering
  managers/CTOs and practicing developers;
- added seven part-level profile outcome blocks, one for each major part;
- added 23 chapter forwarding hooks that explain why a chapter is worth
  sending to a team;
- restored the short book-structure section after moving profile blocks to the
  real part headings;
- added the missing Part V Heading 1 in the raw DOCX proof before Chapter 13;
- recorded 100 controlled editorial micro-iterations in
  `docs/publisher/ru-editorial-100-three-reader-profiles-iterations-2026-07-05.md`.

Proof metrics:

- Raw Google Doc DOCX: 516 pages, 0 blank-like pages.
- Template2000n derivative: 375 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Builder approximate words: 104217.
- Structural DOCX word-token count: 105370.
- Final known Google Doc revision:
  `ALtnJHyZy1LMv4XzR_qTR0FPFlSJ4unAgE-dDg43jHDi7XQoDGg0pXZh6Yx8pPMYboRV2KnwARZezcDLxlbWlO8ccbxfz1FKybyFJZ2Zu7k`.

Report:

- `docs/publisher/ru-three-reader-profiles-recommendability-pass-2026-07-05.md`


### 2026-07-05. Page-turner workshop pass

Status: synced to the working Google Doc and recorded as the current
reader-facing proof pair.

Implemented changes:

- added the introduction block `Сквозная дуга книги`, which frames the book as
  one engineering story from a useful demo to a governed system of actions;
- added seven `Командная сессия части` blocks with workshop format, artifact,
  success signal and red flag;
- added 23 `Что сделать после чтения` actions after chapter forwarding hooks;
- rebuilt the Template2000n derivative from the updated raw DOCX;
- uploaded the updated raw DOCX back to the same Google Doc ID;
- recorded 100 controlled editorial micro-iterations in
  `docs/publisher/ru-editorial-100-page-turner-workshop-iterations-2026-07-05.md`.

Proof metrics:

- Raw Google Doc DOCX: 519 pages, 0 blank-like pages.
- Template2000n derivative: 377 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Builder approximate words: 105103.
- Local Markdown word-token count: 113868.
- Final known Google Doc revision:
  `ALtnJHzDDo0-WoZ_Tzj_JPnk4GkxKpxtZZ6XGYVPp1qNx9jNzOmJzeQxUxlLtAi29eTJYnQ1MHIyHouDx9ufBBlUXzBnOZ-DY3bgnQXPlXc`.

Report:

- `docs/publisher/ru-page-turner-workshop-pass-2026-07-05.md`


### 2026-07-05. Case thesis pass

Status: synced to the working Google Doc and recorded as the current
reader-facing proof pair.

Implemented changes:

- added `Сквозной производственный кейс` to make the support-agent story the
  explicit recurring case of the book;
- added seven `Эпизод сквозного кейса` blocks, one per main part;
- added 23 `Фраза для пересказа` lines inside chapter takeaway blocks;
- rebuilt the Template2000n derivative from the updated raw DOCX;
- uploaded the updated raw DOCX back to the same Google Doc ID;
- recorded 100 controlled editorial micro-iterations in
  `docs/publisher/ru-editorial-100-case-thesis-iterations-2026-07-05.md`.

Proof metrics:

- Raw Google Doc DOCX: 522 pages, 0 blank-like pages.
- Template2000n derivative: 379 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Builder approximate words: 105808.
- Local Markdown word-token count: 114574.
- Final known Google Doc revision:
  `ALtnJHyYapbkiUC6iu1GxFan0C6cwyoMIHWVI320Wi1XqXC0-S6pZYCU543zoWAUmarcQdnT2TyRrpBWXhpeyd74AxV5wI19jHeRRlqYp9U`.

Report:

- `docs/publisher/ru-case-thesis-pass-2026-07-05.md`


### 2026-07-05. Skeptic response pass

Status: synced to the working Google Doc and recorded as the current
reader-facing proof pair.

Implemented changes:

- added `С кем спорит эта книга` after the recurring production case in the
  introduction;
- added seven `Типичное возражение` blocks, one per main part;
- added 23 `Что ответить скептику` responses inside chapter takeaway blocks;
- removed one local Markdown-only duplicate of the minimal sandbox profile
  from appendix-level source material;
- rebuilt the Template2000n derivative from the current raw DOCX;
- uploaded the updated raw DOCX back to the same Google Doc ID;
- recorded 100 controlled editorial micro-iterations in
  `docs/publisher/ru-editorial-100-skeptic-response-iterations-2026-07-05.md`.

Proof metrics:

- Raw Google Doc DOCX: 525 pages, 0 blank-like pages.
- Template2000n derivative: 379 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Builder approximate words: 106615.
- Local Markdown word-token count: 115986.
- Final known Google Doc revision:
  `ALtnJHyKPoEL5XDwXyqfgL2sILc_-RIQ9xR63ygk_d-R7C8YnZawqrJCyP3_rwneb23SCZJhRxPPeCYvWaiyyaDlNYaxZVt95Y5PJZhwFTc`.

Report:

- `docs/publisher/ru-skeptic-response-pass-2026-07-05.md`


### 2026-07-05. Mindset shift pass

Status: synced to the working Google Doc and recorded as the current
reader-facing proof pair.

Implemented changes:

- added `Как изменится ваше мышление после книги` after the skeptic framing
  block in the introduction;
- added seven `До этой части / После этой части` blocks, one per main part;
- added 23 `Смена мышления` lines inside chapter takeaway blocks;
- checked the new mindset layer against existing takeaway, quote,
  skeptic-response, forwarding-hook and next-action layers for repetition;
- rebuilt the Template2000n derivative from the current raw DOCX;
- uploaded the updated raw DOCX back to the same Google Doc ID;
- recorded 100 controlled editorial micro-iterations in
  `docs/publisher/ru-editorial-100-mindset-shift-iterations-2026-07-05.md`.

Proof metrics:

- Raw Google Doc DOCX: 528 pages, 0 blank-like pages.
- Template2000n derivative: 382 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Builder approximate words: 107312.
- Local Markdown word-token count: 116676.
- Final known Google Doc revision:
  `ALtnJHxrm9Lz5_KVTxgVu1rd4I8eRo4ogBBZeZ86-vzl9YMxYGtRZQOjb-_hrGWKrSYh9_GWLhF8aE1LeXRTHMipWROizAGGFNOdCD7XaqE`.

Report:

- `docs/publisher/ru-mindset-shift-pass-2026-07-05.md`


### 2026-07-05. Narrative flow pass

Status: synced to the working Google Doc and recorded as the current
reader-facing proof pair.

Implemented changes:

- audited all 23 chapter starts and endings for reading momentum;
- added 23 natural opening paragraphs after chapter headings, without adding a
  new repeated rubric;
- added 23 natural closing bridge paragraphs after `Что сделать после чтения`
  blocks, so each chapter now carries the reader into the next topic;
- reduced avoidable English terms in the newly added prose where Russian
  wording preserved technical precision;
- rebuilt the Template2000n derivative from the current raw DOCX;
- uploaded the updated raw DOCX back to the same Google Doc ID;
- recorded 100 controlled editorial micro-iterations in
  `docs/publisher/ru-editorial-100-narrative-flow-iterations-2026-07-05.md`.

Proof metrics:

- Raw Google Doc DOCX: 529 pages, 0 blank-like pages.
- Template2000n derivative: 384 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Builder approximate words: 108388.
- Local Markdown word-token count: 117140.
- Final known Google Doc revision:
  `ALtnJHyYmvc0DNBG3DsCu0b3ZJGroROB9YOU0y9ABHXwicj9f1Ordm3aldjp6sJyf--dtyyp6RCLeh6-gnyRoJdhuZX_M9wE-82ZKjMVmSg`.

Report:

- `docs/publisher/ru-narrative-flow-pass-2026-07-05.md`


### 2026-07-06. Reader delight polish pass

Status: synced to the working Google Doc and recorded as the current
reader-facing proof pair.

Implemented changes:

- audited reader fatigue and high-leverage polish points;
- added one introduction paragraph that gives readers language for
  recommending the book inside a team;
- added seven short part-level conflict paragraphs after the existing
  `До этой части / После этой части` blocks;
- added five selected chapter `aha` pivots in Chapters 2, 5, 12, 16 and 23;
- avoided adding a new repeated rubric or another 23-item layer;
- rebuilt the Template2000n derivative from the current raw DOCX;
- uploaded the updated raw DOCX back to the same Google Doc ID;
- recorded 100 controlled editorial micro-iterations in
  `docs/publisher/ru-editorial-100-reader-delight-polish-iterations-2026-07-06.md`.

Proof metrics:

- Raw Google Doc DOCX: 529 pages, 0 blank-like pages.
- Template2000n derivative: 384 pages, 0 blank-like pages.
- Raw/styled paragraph text equality: preserved.
- Builder approximate words: 108797.
- Local Markdown word-token count: 117549.
- Final known Google Doc revision:
  `ALtnJHxPfoLV8Xo2Bi9Tjzkn9e4ANu0le4z32bKytX-eSe9EQsghl9yz1iYpWetbvzg-cctjMEpJM-iOrrJ7nePO-B5PQO3FAkM1b7tKqJ0`.

Report:

- `docs/publisher/ru-reader-delight-polish-pass-2026-07-06.md`


### 2026-07-13. Полная редакционная доработка и Template2000n

Статус: изменения внесены в существующий Google Doc, свежие DOCX/PDF выгружены,
издательский DOCX со стилями Template2000n собран и проверен постранично.

Реализовано:

- переписано введение и удалены повторяющиеся редакционные и справочные слои;
- исправлена иерархия заголовков, терминология, ссылки и техническая семантика
  статусов трассы;
- 24 Mermaid-блока заменены на печатные иллюстрации;
- 49 изображениям добавлен альтернативный текст, девять PNG освобождены от
  альфа-канала;
- основной текст, код, списки, таблицы, рисунки, подписи и врезки сопоставлены
  с семантическими стилями Template2000n;
- выполнены структурная, доступностная, шрифтовая и постраничная проверки.

Метрики:

- 27 глав, семь лабораторных работ, 49 изображений;
- приблизительный объём: 91 436 слов;
- Google Docs PDF: 434 страницы, формат Letter;
- Template2000n PDF: 359 страниц, формат Letter;
- пустых технических страниц и обрезки: 0;
- равенство 11 825 текстовых узлов и комплектность 49 изображений подтверждены;
- зафиксированная ревизия Google Doc:
  `ALtnJHy2UcWKg2VST6U6V6bNBBb_zQHKaMu8qvg8rAsRTPXThoIM1s6KEfO6PTswW661LQTib8c3ctMDp2_SlD4ZUu6niARLRamrRRTbkik`.

Отчёт:

- `docs/publisher/ru-manuscript-remediation-pass-2026-07-13.md`


### 2026-07-14. Синхронизация с электронной книгой и финальный proof pass

Статус: изменения перенесены в существующий Google Doc, возвращены в
канонический Markdown и проверены в raw- и Template2000n-производных.

Реализовано:

- структура стабилизирована на 7 частях и 28 главах;
- новая глава 20, причинный разбор, контрольный контур, метрики и
  отказобезопасные перехватчики согласованы с электронной книгой и эталонным
  пакетом;
- исправлены перекрестные ссылки и единое имя `create_ticket`;
- восемь схем перестроены для книжной полосы;
- листинг перехватчиков уплотнен после визуальной проверки;
- локальные карты, чеклист и пакет издательских решений обновлены фактическими
  показателями.

Метрики:

- 28 глав, 7 лабораторных работ, итоговый проект, 54 изображения;
- приблизительный объем сборщика: 98 260 слов;
- Google Docs PDF: 462 страницы Letter;
- Template2000n PDF: 379 страниц Letter;
- raw-страница 41 подтверждена как осознанный переход на правую полосу;
- в Template2000n пустых технических страниц нет;
- текстовый слой и комплектность изображений сохранены;
- финальная ревизия Google Doc:
  `ALtnJHzvtsCG0eT_3bT0M01Er0g4aEVzFKOu9czWuWQKeHNGsXBZeBTJFr_PVXoSZrsnBKQfEZ9xSdfWt2TKlI5qAzHwvlYhbzJ4JzIS-XU`.

Отчет:

- `docs/publisher/ru-electronic-book-sync-pass-2026-07-14.md`


### 2026-07-16. Проход по лучшим практикам технической литературы

Статус: доработки внесены в канонический Markdown и существующий Google Doc;
raw- и Template2000n-производные пересобраны и проверены.

Реализовано:

- добавлены восемь маршрутов частей и дополнительная иерархия плотных глав;
- устранен повтор границы доказательств и переписано открытие главы 23;
- все 28 глав получили проверяемые источники и пояснения по их чтению;
- 38 технических блоков получили последовательные подписи листингов;
- добавлены критерии самостоятельной проверки по восьми частям;
- библиография очищена от видимых URL, составных записей и повторов;
- добавлены две редакционные схемы, общее число изображений доведено до 56;
- визуальный аудит переведен на фактический комплект изображений вместо
  устаревшего жесткого ограничения.

Метрики:

- 8 частей, 28 глав, 8 лабораторных работ и итоговый проект;
- приблизительный объем: 92 770 слов;
- raw-производная: 463 страницы, Template2000n: 330 страниц;
- пустых технических страниц: 0;
- текст, порядок 56 медиафайлов и 6 регистраций встроенных шрифтов сохранены;
- 1029 тестов репозитория и 23 чистых прогона лабораторных команд успешны;
- финальная ревизия Google Doc:
  `ALtnJHxUN-Xew7E0UvuwTEMs4CB5YSca-CnXM-9a-gKmoAmmCW0iKzgimn3l_8xio6GSPhcFMn8q6itdqaKAhU8Wp-J3hrI3v8Gdj9Hgje0`.

Отчет:

- `docs/publisher/ru-technical-book-best-practices-pass-2026-07-16.md`


### 2026-07-17. Финальная техническая корректура и нормализация Google Doc

Статус: правки внесены в канонический Markdown и существующий Google Doc;
raw- и Template2000n-производные пересобраны и проверены постранично.

Реализовано:

- восстановлены корректные списки и устранены два перегруженных перечнями
  раздела в главах 19 и 22;
- исправлены потерянный заголовок, восемь подписей YAML, терминология и
  избыточные англицизмы;
- длинные предложения разделены, лабораторная работа 8 получила четыре шага
  и явные ожидаемые результаты;
- редактура закреплена воспроизводимым проходом генератора и регрессионным
  тестом;
- в Google Doc 1064 буквальных маркера преобразованы в нативные списки;
- проверяющий рисунков научился работать с обычной и нулевой нумерацией
  страниц Poppler.

Метрики:

- 8 частей, 28 глав, 8 лабораторных работ, итоговый проект и 56 изображений;
- приблизительный объем по метрике Template2000n: 90 653 слова;
- raw-производная: 442 страницы, Template2000n: 317 страниц;
- пустых технических страниц: 0;
- все 56 рисунков находятся внутри страницы, 25 нумерованных подписей стоят
  непосредственно после рисунков;
- 1049 тестов репозитория и 23 чистых прогона лабораторных команд успешны;
- в Google Doc 3711 нативных элементов списка и 0 буквальных маркеров `•`;
- финальная ревизия Google Doc:
  `ALtnJHwL3wj7ZKwAguGSYFFAHgzv_Bvk1UJITxwAt40WejA8SU6tPNi7LTEFub2TfnQNui8nPrjhzd7tJy2Pg4OKWFQOtyY63rvFmnATW8Q`.

Отчет:

- `docs/publisher/ru-advanced-bookcraft-final-polish-2026-07-17.md`


### 2026-07-18. Редакционная готовность и защищенная синхронизация Google Docs

Статус: существующий Google Doc обновлен точечными операциями с контролем
ревизии; канонический Markdown и обе издательские производные пересобраны и
проверены.

Реализовано:

- перегруженные списками фрагменты глав 19, 22, 24 и 25 преобразованы в
  объясняющие группы без потери содержания;
- добавлены три разбора решений и нативная таблица главы 9;
- все 28 глав получили адресуемые ссылки у итоговых тезисов;
- восстановлен отсутствовавший исполняемый маршрут главы 3;
- удален глобальный дословный повтор сверки внешнего состояния;
- таблицы локальных DOCX получили повтор заголовка и запрет разрыва строк;
- сводная библиография подтверждена как набор `S001`-`S104` без повторяющихся
  URL.

Метрики:

- Google Doc: 458 страниц, 91 860 слов, 56 изображений и 3 нативные таблицы;
- 8 частей, 28 глав, 8 лабораторных работ и итоговый проект;
- raw-производная: 443 страницы, Template2000n: 320 страниц;
- пустых технических страниц: 0;
- 56 из 56 рисунков прошли проверку размещения и соответствия источнику;
- 20 из 20 структурных проверок Google Doc и 1054 теста репозитория успешны;
- финальная ревизия Google Doc:
  `ALtnJHxf3zrwgQ8oFT97bICdDOqrGiK4rMaypdFXcy9UMnLi6_y797nw5cr9_bRZOmhaZP3n0LbUBVDzuY_f4pnGgIket_wIb3ZolPN7ugk`.

Отчет:

- `docs/publisher/ru-editorial-readiness-pass-2026-07-18.md`


### 2026-07-18. Реализация замечаний многоагентной технической рецензии

Статус: блокирующие технические и издательские замечания реализованы локально,
перенесены в существующий Google Doc и проверены повторной сборкой. Авторский
блок и внешняя проверка реальными людьми намеренно не объявлены завершёнными.

Реализовано:

- введены устойчивое намерение записи, post-dispatch unknown effect и
  блокировка до сверки;
- подтверждения получили долговечное хранилище, полный отпечаток действия,
  срок, nonce, запрет самоодобрения и путь возобновления;
- структурная целостность доказательств отделена от доверенной аттестации,
  вывод из эксплуатации переведён в закрытый по умолчанию режим;
- добавлен трёхсостояний регрессионный шлюз с контролем выборки и критических
  нарушений;
- лабораторная работа 8 стала накопительной, а рубрика итогового проекта
  получила безусловные критерии-блокеры;
- в локальные DOCX добавлены оглавление, фолиация, `ru-RU`, подписи всех
  девяти таблиц и минимальная читаемая ширина столбцов;
- точечные изменения синхронизированы в существующий Google Doc с контролем
  ревизии.

Метрики:

- Google Doc, контрольный Word/LibreOffice-экспорт: 493 страницы Letter,
  0 пустых технических страниц;
- raw-производная: 446 страниц, Template2000n: 323 страницы;
- приблизительный объём локальной производной: 91 882 слова;
- 56 изображений и 9 таблиц сохранены в локальных производных;
- 1082 теста репозитория, 16 издательских тестов и 23 чистых лабораторных
  запуска успешны;
- обе PDF-производные содержат одинаковое дерево из 583 закладок;
- финальная ревизия Google Doc:
  `ALtnJHxMA-Q4BAMiUXU7IZ1PopfOCybckh1EzBqwmavS9hNG8coR5-Hy-jIlR5oM1AA7PZjsRJx6E3Nf-ZfB96L0ox_8Z0_Pf6XzUU5fAcs`.

Отчёты:

- `docs/publisher/ru-multi-agent-technical-review-2026-07-18.md`;
- `docs/publisher/ru-multi-agent-remediation-2026-07-18.md`;
- `docs/publisher/ru-editorial-readiness-pass-2026-07-18.md`.


### 2026-07-20. Развивающая редактура и синхронизация Google Docs

Статус: финальный детерминированный проход применён к каноническому Markdown,
обеим издательским производным и существующему Google Doc. История файла и
редакторские комментарии сохранены.

Реализовано:

- устранён остаточный ритм редакционной сборки, а плотные главы собраны в
  крупные учебные акты;
- матрица выбора формы исполнения перенесена из главы 1 в главу 2;
- восемь лабораторных работ получили 39 именованных шагов, наблюдения и явные
  формулировки доказанного результата;
- в DOCX добавлены 107 устойчивых закладок и 175 внутренних ссылок;
- 172 из 172 изменённых абзацев подтверждены итоговым чтением Google Doc;
- устранены три случайных принудительных разрыва перед итогами лабораторий;
- свежий экспорт Google Doc полностью отрисован и проверен постранично.

Метрики:

- 8 частей, 28 глав, 8 лабораторных работ, 56 изображений и 9 таблиц;
- приблизительный объём: 91 604 слова;
- Google-ориентированная производная: 437 страниц;
- производная `Template2000n`: 320 страниц;
- свежий экспорт существующего Google Doc: 488 страниц;
- пустых технических страниц, обрезки и наложений не обнаружено;
- 1087 тестов репозитория и 23 чистых запуска лабораторных команд успешны;
- финальная ревизия Google Doc:
  `ALtnJHyvucObEw3NQ_K_IpvncJvfdH6V1pUAx_E8-DwKKk_frxdhOOafSA4S2E-P104DRv5E-g_mRx8IWg4cNo9ir3wEI-YUhiexXHuXvvM`.

Отчёт:

- `docs/publisher/ru-developmental-editing-pass-2026-07-20.md`.


### 2026-07-22. Готовность рукописи к издательской передаче

Статус: каноническая сборка, существующий Google Doc и две локальные
издательские производные синхронизированы и проверены. Авторские поля и
реальная внешняя рецензия намеренно не объявлены завершёнными.

Реализовано:

- введение приведено к последовательности «маршрут читателя — самопроверка —
  сокращения — структура книги»;
- устранены остаточные ошибки ссылок на главы, терминологии и пять повреждённых
  склеек в Google Doc;
- глава 21 получила матрицу поверхностей доверия и доказательств выпуска;
- пустые заголовочные абзацы преобразованы в обычный текст, удалены пустые
  абзацы перед главами и в конце Google Doc;
- контрольный тег рукописи обновлён до
  `ru-manuscript-editorial-2026-07-22`;
- свежий экспорт существующего Google Doc отрисован после всех правок.

Метрики:

- 8 частей, 28 глав, 8 лабораторных работ, итоговый проект, 56 изображений и
  10 таблиц в локальной издательской сборке;
- приблизительный объём: 91 661 слово;
- Google-ориентированная производная: 436 страниц;
- производная `Template2000n`: 317 страниц;
- свежий экспорт существующего Google Doc: 485 страниц Letter;
- пустых технических страниц во всех трёх проверенных PDF нет;
- 1096 тестов репозитория и 23 чистых запуска лабораторных команд успешны;
- финальная ревизия Google Doc:
  `AIroW34T21uKswdfPb9meuhJEG_xfKqHE4_Whg2C4JbnXWmjD51Iz_ORM6K9ZIwXmVGreawtWYjW_b5rP-aApsKSwzTPfFmi2xBrRxQ4Lhw`.

Отчёт:

- `docs/publisher/ru-submission-readiness-pass-2026-07-22.md`.


### 2026-07-29. Синхронизация с актуальной онлайн-книгой

Статус: канонический Markdown, существующий Google Doc, эталонная среда
исполнения и обе локальные издательские производные синхронизированы и
проверены.

Реализовано:

- добавлены ортогональные состояния, контракт памяти, угрозы сетей агентов,
  маршрут бюджета, регрессии вне модели и изоляция оценочной песочницы;
- добавлены AgentRx, воронка подтверждения уязвимости, сохранение доказательств
  при усечении и параллельных сессиях инструментов;
- источники расширены до `S115`;
- новые книжные контракты материализованы в эталонной среде исполнения,
  отрицательных лабораторных сценариях и регрессионных тестах;
- 8820 из 8820 целевых непустых абзацев подтверждены в живом Google Doc;
- локальные DOCX/PDF пересобраны с сохранением 56 изображений, 10 таблиц,
  текста и внедрённых шрифтов.

Метрики:

- около 95 тысяч слов;
- Google-ориентированная производная: 453 страницы;
- производная `Template2000n`: 327 страниц;
- пустых страниц, блоков за полями и символов замены нет;
- 1285 тестов репозитория и 23 чистых запуска лабораторных команд успешны;
- финальная ревизия Google Doc:
  `AIroW37NwVSClQSSYb85bVaTYYACE8Aqb6aH6XOkFCe1A1H14ur34HHhJRFMT2ZzDBGtc3w0uyZb4VMrOhKLxXrqHcIcnHvzC766M4EUyEM`.

Отчёт:

- `docs/publisher/ru-online-manuscript-sync-2026-07-29.md`.


### 2026-08-01. Редакционный проход и актуализация MCP

Статус: канонический Markdown, существующий Google Doc, три локализации
электронной книги и обе издательские производные синхронизированы.

Реализовано:

- уточнены границы решения политики, управляющего действия, непрерывности,
  проверки с ограниченным набором доказательств и платных возможностей;
- MCP приведён к ядру без состояния версии 2026-07-28, а прикладное состояние
  отделено от протокольной сессии;
- расширены непрерывная оценка, продуктовые метрики, реестры и итоговая рубрика;
- источники расширены до `S122`;
- 36 абзацных изменений и новая нативная таблица перенесены в существующий
  Google Doc с контролем ревизии;
- локальные DOCX/PDF пересобраны с сохранением текста, 56 изображений,
  11 таблиц и внедрённых шрифтов.

Метрики:

- около 95 759 слов;
- Google-ориентированная производная: 456 страниц;
- производная `Template2000n`: 330 страниц;
- пустых страниц, блоков за полями и символов замены нет;
- 1292 теста репозитория и строгая сборка трёх локализаций успешны;
- финальная ревизия Google Doc:
  `AIroW35prHNueHFHV7x6PXl80jsvBh8iIQaxj34qE3kzRDNQtyxCDYC-3_kE8gnZ-W_JynXfSDaZNTub8fcjw6hz0RHJcTHP2SH19n-5KTY`.

Отчёт:

- `docs/publisher/ru-editorial-pass-2026-08-01.md`.


### 2026-08-01. Читательский проход и повторная синхронизация Google Docs

Статус: канонический Markdown, существующий Google Doc и две издательские
производные синхронизированы и проверены как единый выпуск.

Реализовано:

- введён единый маршрут по задаче и навигатор по наблюдаемому симптому;
- маршруты частей переписаны как переходы состояния сквозного случая, а
  открытия глав 5, 11 и 26 начинаются с конкретного решения;
- лаборатории объединены одним циклом обучения, добавлен исполняемый сборщик
  накопительного манифеста доказательств;
- итоговая рубрика и листинги приведены к фактическим контрактам среды
  исполнения;
- 46 генерируемых схем перерисованы для печатной читаемости, а рядом с 13
  изображениями добавлен явный смысловой вывод;
- 8 935 из 8 935 целевых абзацев подтверждены в живом Google Doc после
  атомарной адресной синхронизации;
- локальные DOCX/PDF пересобраны с сохранением 56 изображений, 11 таблиц,
  альтернативных описаний и внедрённых шрифтов.

Метрики:

- приблизительно 96 984 слова;
- Google-ориентированная производная: 481 страница;
- производная `Template2000n`: 355 страниц;
- свежий экспорт существующего Google Doc: 506 страниц Letter;
- пустых страниц, блоков за полями и символов замены нет;
- 1 303 теста и 23 чистых запуска лабораторных команд успешны;
- строгая сборка трёх локализаций успешна;
- финальная ревизия Google Doc:
  `AIroW37DrV8dNIYvUEV4d5pOla46Wwq6WopW3RWy18Hy0wJwUNzmMRpRfxpU-LXjQBCZv9zKOxq82sIury9MhmTP3x55NmDU2pjFkh8ELnk`.

Отчёт и манифест:

- `docs/publisher/ru-reader-experience-pass-2026-08-01.md`;
- `docs/publisher/ru-reader-experience-pass-2026-08-01.manifest.json`.


### 2026-08-02. Повторная редакционная полировка и синхронизация Google Docs

Статус: канонический Markdown, существующий Google Doc и две издательские
производные синхронизированы и проверены как единый выпуск.

Реализовано:

- исправлена подмена SHA коммита тегом и удалены хрупкие позиционные ссылки;
- сокращены перегруженные предложения и уплотнена иерархия глав 5, 11, 15,
  24 и 26;
- устойчивый контракт именованного агента отделён от снимка конкретной
  облачной реализации;
- все печатные строки кода ограничены 81 символом без изменения исполняемости
  лабораторных команд;
- 128 адресных фрагментов перенесены в существующий Google Doc атомарным
  пакетом из 919 операций;
- контрольным пакетом из 17 операций исправлены уровни четырёх заголовков и
  добавлены 13 ссылок на новые источники; всего выполнено 936 операций;
- 9 006 из 9 006 целевых абзацев подтверждены в правильном порядке;
- сохранены вкладка `t.0`, 56 рисунков и 11 таблиц.

Метрики:

- приблизительно 96 603 слова;
- Google-ориентированная производная: 482 страницы;
- производная `Template2000n`: 356 страниц;
- свежий DOCX-экспорт существующего Google Doc: 507 страниц Letter;
- пустых страниц, блоков за полями и символов замены нет;
- 1 306 тестов и 23 чистых запуска лабораторных команд успешны;
- строгая сборка трёх локализаций успешна;
- финальная ревизия Google Doc:
  `AIroW37ly0XavWwYVe43xKRMJkhCxJCCXoFPpWp6IsMcEr6yBZlEc-9mWtQgQXyQQm1-Gmv00Jd_8vku18WRcVLAH0Av4TmNMOUgF4Fhar8`.

Отчёт и манифест:

- `docs/publisher/ru-technical-book-polish-pass-2026-08-02.md`;
- `docs/publisher/ru-technical-book-polish-pass-2026-08-02.manifest.json`.

### 2026-08-02. Единая Mermaid-система иллюстраций

Статус: все схемы рукописи переведены на воспроизводимый визуальный конвейер и
повторно проверены в издательской верстке `Template2000n`.

Реализовано:

- Mermaid стал источником правды для всех 56 схем: 29 встроенных, 25
  нумерованных и двух редакционных;
- введён единый визуальный язык `agent-arch-book-v1`, общий для SVG и печатных
  PNG 300 dpi;
- перегруженные и узкие схемы перекомпонованы без потери контрольных ветвей,
  решений и связей с доказательствами;
- генератор проверяет полноту манифестов, уникальность имён, минимальный
  печатный кегль и допустимые пропорции;
- таблицы выровнены и защищены от разрыва строк, а столбцы с длинными
  техническими идентификаторами получили достаточную ширину;
- основная и `Template2000n`-версии пересобраны с байтовым совпадением 56
  изображений и равенством текста.

Метрики:

- приблизительно 96 603 слова;
- 358 страниц в PDF-производной `Template2000n`;
- минимальный расчётный печатный кегль схем: 8,56 пункта;
- минимальное отношение ширины схемы к высоте: 0,742;
- 56 из 56 изображений находятся в пределах страницы;
- пустых страниц и замечаний проверки доступности нет.

Артефакты контроля:

- `docs/publisher/ru-visual-style-guide-2026-08-02.md`;
- `docs/publisher/ru-visual-build-2026-08-02.json`;
- `docs/publisher/ru-template2000n-unified-visuals-2026-08-02.visual-audit.json`;
- `docs/publisher/ru-template2000n-unified-visuals-2026-08-02.render-qa.json`.

Синхронизация Google Docs:

- перед изменением создана отдельная резервная копия рукописи;
- контрольная замена одного рисунка проверена на копии;
- в основной документ одним атомарным пакетом из 112 операций перенесены все
  56 Mermaid-рендеров с рассчитанными размерами;
- итоговый readback подтвердил 56 объектов, их прежние позиции, ожидаемые
  размеры и источники из коммита
  `8d2d014e0174297b56195182b14451545902f430`; расхождений нет;
- итоговая ревизия Google Doc:
  `AIroW35cq93T87bpUoVL__T_XZAJQfiSGUuxDMb_28OJF6wXPcHaEZ7WgouPngoO4FrAiUjpsV2F6x7t51j6rDsA8cxaMg7b8g0eIesKNZc`.

Отчёт:

- `docs/publisher/ru-google-doc-mermaid-sync-2026-08-02.md`.

### 2026-08-03. Структурная редактура и повторная синхронизация

Статус: канонический Markdown, существующий Google Doc и обе издательские
производные синхронизированы и проверены как единый выпуск.

Реализовано:

- главы 5, 11, 15, 18, 24 и 26 получили однозначные зоны ответственности;
- повторные определения сокращены до переходов без потери технических
  контрактов;
- число автономных псевдозаголовков снижено с 225 до 34;
- команды отделены от объяснений и ожидаемых результатов;
- источники разделены на отдельные абзацы с восстановлением внешних ссылок;
- 305 адресных изменений перенесены в существующий Google Doc 11 пакетами из
  2 943 нативных операций;
- обратное чтение подтвердило 8 844 из 8 844 целевых абзацев;
- сохранены 56 изображений и 12 таблиц.

Метрики:

- приблизительно 94 690 слов;
- Google-ориентированная производная: 465 страниц;
- производная `Template2000n`: 347 страниц;
- пустых страниц и замечаний проверки доступности нет;
- 1 335 тестов и 21 чистый запуск лабораторных команд успешны;
- финальная ревизия Google Doc:
  `AIroW34BIqLlxqyR7lQFvoH2tr9RC3xMQbLeVUbowLhnbIiLXZZEPOWAyWjM_VBNon89r55HZiEeX_Dg5zUlVSRf22nuw0gtqO3tWwDH9MY`.

Отчёт:

- `docs/publisher/ru-editorial-structure-pass-2026-08-03.md`.

### 2026-08-14. Online Companion и проверяемые закрытые отказы

Статус: канонический Markdown, существующий Google Doc, практическое
сопровождение и обе издательские производные синхронизированы.

Реализовано:

- в начало и справочную часть рукописи добавлены прямые ссылки на Online
  Companion, а в печатный маршрут - декодируемый QR-код;
- практикум дополнен сценариями недопустимого транспорта для высокого риска,
  устаревшего завершения запуска и решения без владельца;
- воспроизводимая практика закреплена на коммите
  `ecc5aa3cbb48eff00514a24575c64b6e68e3ffe4`;
- публичные глубокие ссылки и точные пути исходников сведены в один маршрут;
- обновлён пакет для реальных технических рецензентов и независимых
  бета-читателей;
- 487 текстовых и стилевых операций, три операции вставки QR-кода и одна
  контролируемая замена SHA применены к существующему Google Doc;
- обратное чтение подтвердило 8 755 из 8 755 целевых абзацев;
- сохранены 57 изображений и 12 таблиц.
- 57 заголовков и 57 альтернативных описаний перенесены в нативный Google Doc;
  обратное чтение не выявило пропущенных или повторяющихся описаний.

Метрики:

- приблизительно 94 923 слова;
- Google-ориентированная производная: 465 страниц;
- производная `Template2000n`: 345 страниц;
- пустых страниц и замечаний проверки доступности нет;
- 1 344 теста и 21 чистый запуск лабораторных команд успешны;
- строгая сборка трёх локализаций успешна;
- финальная ревизия Google Doc:
  `AIroW34bwyJcxIARZcLNTlYvMm8m2v70FpG6aA-cyJlxHLxA1r1QPtVLf022orIET3BzYCup93kq87fFR2oGM8cDHVJWh7VD6duLxK54QE8`.

Отчёт:

- `docs/publisher/ru-publication-readiness-pass-2026-08-14.md`.
