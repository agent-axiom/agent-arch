# Эволюция русской издательской рукописи

Status: working ledger for manuscript assembly. This file tracks the book
manuscript itself, not the publisher cover materials.

## Current reality

На 2026-06-14 Google Doc **не является финальной рукописью книги**.

Текущий Google Doc содержит:

- служебный титульный блок;
- правила синхронизации;
- compact publisher packet;
- договорную структуру 7 частей / 23 главы;
- служебные следующие шаги;
- first compression/editorial pass введения;
- first compression/editorial pass Части I: Chapter 1, Chapter 2 and Chapter 3;
- first compression/editorial pass Части II: Chapter 4, Chapter 5 and Chapter 6;
- first compression/editorial pass Части III: Chapter 7, Chapter 8 and Chapter 9;
- first compression/editorial pass Части IV: Chapter 10, Chapter 11 and Chapter 12;
- first compression/editorial pass Части V: Chapter 13, Chapter 14, Chapter 15 and Chapter 16;
- first compression/editorial pass Части VI: Chapter 17, Chapter 18, Chapter 19 and Chapter 20;
- first compression/editorial pass Части VII: Chapter 21, Chapter 22 and Chapter 23;
- first compression/editorial pass приложений: glossary, checklists, incident/postmortem,
  curated sources and online companion.

Поэтому текущий Google Doc уже отражает договорный объем как manuscript
snapshot после первого compression/editorial pass: skeleton, publisher packet,
введение, Часть I, Часть II, Часть III, Часть IV, Часть V, Часть VI, Часть VII
и приложения. Это все еще не финальная книга: остаются сверка ссылок,
терминологический проход, авторские поля, углубленная line edit and publisher
formatting.

## Source volume

Репозиторий остается источником правды. Текущий русский source-объем:

- `docs/book/**/*.md` и `docs/appendix/**/*.md`, без `.en.md` и `.zh.md`;
- около **113 909 слов** по текущему `wc -w` на 2026-06-13;
- web-структура: 8 частей, 27 глав, практические страницы и приложения;
- print target: 7 частей, 23 главы, введение и приложения;
- договорный ориентир по плану-проспекту: 425-497 страниц до фактической
  версточной проверки.

Этот объем нельзя просто скопировать в Google Doc один к одному. Web-рукопись
надо собрать в печатную рукопись: сжать, убрать web-only navigation, вынести
runtime/schema-heavy материал в online companion и привести главы к книжному
ритму.

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
   online companion. Status: rough assembly synced to Google Doc on 2026-06-13.

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

Status: manuscript body exists; publisher formatting is blocked until БХВ
styles arrive and author fields are filled.

Goal:

- применить стилевые файлы БХВ;
- подготовить DOCX/Google Doc export;
- только после этого использовать cover note and external packet.

Rule:

- `docs/publisher/ru-cover-note-draft.md` is parked until Stage 2 is complete
  enough to show manuscript volume.

## Current next practical step

Stop treating the publisher packet as the main artifact.

Next implementation step:

1. run terminology, glossary, cross-reference and companion-boundary passes;
2. keep working/publisher service blocks outside the final manuscript body;
3. fill author bio fields and apply БХВ styles when they arrive;
4. prepare print/readability QA only after style files and export shape are clear;
5. keep commits local unless explicitly requested to push.

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
  in online companion for now.
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
- `Глава 20. Assurance loop, incident response, registry и retirement`;
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
- `Приложение 4. Источники и online companion`.

Notes:

- This batch adds the print appendix layer, not the full online reference
  catalog.
- Full trace/eval/approval/policy/memory/lifecycle/change/incident schemas,
  registry operations, long YAML examples, CLI walkthrough and source catalog
  remain in online companion.
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
  policy, context boundary, tool gateway, trace evidence and rollout ownership.
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
- Chapter 6 now emphasizes the tool gateway as the central contract for turning
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
- `Глава 20. Assurance loop, incident response, registry и retirement`;
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
- `Приложение 4. Источники и online companion`.

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
- `Глава 20. Assurance loop, incident response, registry и retirement`;
- `Часть VII. Эталонная реализация и промышленный запуск`;
- `Глава 23. Чеклист промышленного запуска`;
- `Приложения`;
- `Приложение 4. Источники и online companion`.

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
  lifecycle and tool gateway in Russian-first form.

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
  workflow, policy layer, tool gateway, rollout gates and trace;
- Parts II-III now prefer Russian-first forms for identity, session, policy
  layer, capability model, tool gateway and audit record;
- Parts IV-V now prefer Russian-first forms for execution layer, tool gateway,
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
  supported paths, assurance loop, incident response, registry, retirement,
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
