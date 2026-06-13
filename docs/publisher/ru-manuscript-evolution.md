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
- rough assembly Части IV: Chapter 10, Chapter 11 and Chapter 12;
- rough assembly Части V: Chapter 13, Chapter 14, Chapter 15 and Chapter 16;
- rough assembly Части VI: Chapter 17, Chapter 18, Chapter 19 and Chapter 20;
- rough assembly Части VII: Chapter 21, Chapter 22 and Chapter 23;
- rough assembly приложений: glossary, checklists, incident/postmortem,
  curated sources and online companion.

Поэтому текущий Google Doc уже отражает договорный объем как rough manuscript
snapshot: skeleton, publisher packet, введение, Часть I, Часть II, Часть III,
Часть IV, Часть V, Часть VI, Часть VII и приложения. Это все еще не финальная
книга: compression/editorial pass начат с введения, Части I, Части II и
Части III, но остаются сверка ссылок, авторские поля, полный редакторский
проход и издательское оформление.

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

### Stage 1. Google Doc skeleton and first sample

Status: done, but not a full manuscript.

Done:

- создан Google Doc `Архитектура безопасных ИИ-агентов`;
- перенесена договорная структура;
- перенесена Chapter 1 как первый sample;
- Chapter 1 прошла первый русский издательский line edit;
- source Chapter 13 прошел первый technical sample line edit.

Limit:

- объем Google Doc пока отражает только skeleton plus sample;
- это нельзя трактовать как готовую или почти готовую книгу.

### Stage 2. Manuscript body assembly

Status: done for rough assembly; final manuscript quality still pending.

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

Status: in progress.

Goal:

- сжать web-структуру 8/27 в договорную структуру 7/23;
- объединить практические страницы и appendix-heavy фрагменты в книжные главы;
- удалить или переформатировать web-only элементы.

Definition of done:

- каждая печатная глава имеет один связный текст;
- long schema/runtime/CLI material вынесен или помечен как companion-only;
- chapter endings не выглядят как повторяющийся web-template.

### Stage 4. Editorial pass

Status: in progress for Introduction and Parts I-III; pending for the rest of
the manuscript.

Goal:

- пройти главы по voice, rhythm, terminology and evidence;
- сохранить практическую глубину, но убрать web-friction.

Definition of done:

- все 23 главы прошли first Russian editorial pass;
- glossary and terminology policy согласованы с текстом;
- sample Chapter 1 не отличается по качеству от остальных глав.

### Stage 5. Publisher formatting and external packet

Status: blocked until manuscript body exists and БХВ styles arrive.

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

1. continue compression/editorial pass with Part IV and Part V;
2. remove web-friction: repeated template endings, case-spine/internal labels,
   over-English headings and schema-heavy residue;
3. commit each manuscript assembly checkpoint without pushing unless explicitly
   requested.

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
