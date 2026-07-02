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

Status: manuscript body exists; H2/H3 body-style cleanup is complete for the
current Google Doc proof; author/front-matter fields are isolated; current raw
and Template2000n proof candidates render cleanly. Final publisher submission
is still blocked until author facts, final companion metadata and external
proofread are closed.

Goal:

- применить стилевые файлы БХВ;
- подготовить DOCX/Google Doc export;
- только после этого использовать cover note and external packet.

Rule:

- `docs/publisher/ru-cover-note-draft.md` is parked until Stage 2 is complete
  enough to show manuscript volume.

## Current next practical step

The main artifact is now the full Google Doc manuscript plus the current proof
pair: raw Google Docs export and Template2000n derivative.

Next implementation step:

1. fill author bio/front-matter fields and confirm companion/public metadata;
2. run external editor/proofreader review against the clean handoff packet;
3. backport any semantic Google Doc edits into Markdown;
4. re-export raw DOCX and rebuild Template2000n after author fields;
5. rerun render QA and prepare the final publisher submission packet.

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
  confirmation, tool gateway, audit and trust boundaries.

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
  for Chapter 22 and the online companion.

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
