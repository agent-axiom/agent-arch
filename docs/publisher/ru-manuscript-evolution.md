# Эволюция русской издательской рукописи

Status: working ledger for manuscript assembly. This file tracks the book
manuscript itself, not the publisher cover materials.

## Current reality

На 2026-06-13 Google Doc **не является полной рукописью книги**.

Текущий Google Doc содержит:

- служебный титульный блок;
- правила синхронизации;
- compact publisher packet;
- договорную структуру 7 частей / 23 главы;
- служебные следующие шаги;
- rough assembly введения;
- rough assembly Части I: Chapter 1, Chapter 2 and Chapter 3;
- rough assembly Части II: Chapter 4, Chapter 5 and Chapter 6;
- rough assembly Части III: Chapter 7, Chapter 8 and Chapter 9.

Поэтому текущий Google Doc уже начал набирать тело рукописи, но это все еще не
полная книга. Это assembly snapshot: skeleton, publisher packet, введение,
Часть I, Часть II и Часть III.

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

Status: active.

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
3. Часть IV + Часть V: print chapters 10-16. Status: next batch.
4. Часть VI + Часть VII: print chapters 17-23.
5. Приложения: glossary, checklists, incident/postmortem, curated sources and
   online companion.

Definition of done:

- Google Doc содержит все договорные главы хотя бы в rough assembly form;
- для каждой главы есть source path и companion boundary;
- в чеклисте видно, какие главы требуют line edit, compression или rewrite.

### Stage 3. Compression from web manuscript to print manuscript

Status: pending.

Goal:

- сжать web-структуру 8/27 в договорную структуру 7/23;
- объединить практические страницы и appendix-heavy фрагменты в книжные главы;
- удалить или переформатировать web-only элементы.

Definition of done:

- каждая печатная глава имеет один связный текст;
- long schema/runtime/CLI material вынесен или помечен как companion-only;
- chapter endings не выглядят как повторяющийся web-template.

### Stage 4. Editorial pass

Status: pending.

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

1. assemble Part IV + Part V body into the Google Doc;
2. update this ledger with exact chapter statuses;
3. commit the manuscript assembly checkpoint;
4. continue batch by batch until the Google Doc reflects book volume, not only
   a sample package.

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
- Next batch should continue with Part IV and Part V, not publisher packet work.

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
- Google Doc status text now points to the next batch: Part IV + Part V.
- Connector readback verified target document identity, inserted headings,
  final Part III paragraph and heading/body paragraph styles after a follow-up
  style normalization pass.
