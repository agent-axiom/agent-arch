# Google Doc listing-caption pass 2026-06-25

Дата прохода: 2026-06-25.

Целевой документ: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`.

Название документа: `Архитектура безопасных ИИ-агентов — полная рукопись`.

Рабочий tab: `t.0`.

Revision после правок: `ALtnJHyQo9UCen1Ox6JZo_9gbKZmWFrhdB5sOnlejOOpCxBrUdTOldz9jyx8i9simIl2ZariU18kfwCiPqJx4QXniQ-LEpL66Lqe24qKH5Q`.

## Реализованные пункты

### 1. Target guard and listing inventory

Перед правками через Google Drive connector подтвержден целевой Google Doc:

- document id: `1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
- title: `Архитектура безопасных ИИ-агентов — полная рукопись`;
- tab id: `t.0`;
- исходный revision для batch write: `ALtnJHx8rYGtnrjMg9ktpn0uzJr-ax5Hul3f6SKJI7VX5aIxsDe7J746gD13SmpLfPI1SnBbVGcg6gKOlK_2PGIDqSbk0l8EC62o0F6TztY`.

Инвентаризация свежего raw DOCX export показала 28 generic listing labels:

- 27 labels `Листинг (YAML):`;
- 1 label `Листинг (Python):`.

Основные кластеры:

- глава 12: write intent, idempotency, outcome matrix, retry, rollback, reconciliation, approval, durable step, trace events, eval scenario;
- глава 15: incident question, trace review, timeline, identity invariants, tool-policy review, approval review, span usage, tool result, verification result, regression candidate;
- глава 14: user story and SLO map;
- главы 17-18: ownership map and golden path;
- часть VII: runtime skeleton, Python skeleton, capability release contract, rollout decision record.

### 2. Classification and caption map

Все 28 labels классифицированы как печатные captions, а не как самостоятельные заголовки. Правило прохода:

- caption должен объяснять, зачем reader видит фрагмент;
- caption должен указывать архитектурный смысл, а не только формат `YAML` или `Python`;
- для длинных excerpts caption должен явно напоминать, что полный контракт или реализация принадлежит companion.

### 3. Google Doc caption update

Generic labels заменены на смысловые captions в Google Doc.

Примеры замен:

- `Листинг 12.1 — write-intent как печатный excerpt перед внешним действием.`
- `Листинг 12.10 — eval scenario для timeout after write.`
- `Листинг 15.6 — approval review с тем же trace/session/idempotency context.`
- `Листинг 15.10 — regression candidate из incident trace.`
- `Листинг 21.1 — runtime skeleton contract; полный контракт держать в companion.`
- `Листинг 21.2 — Python skeleton для контрольного run path; полная реализация в companion.`
- `Листинг 22.1 — rollout decision record как короткий release-gate artifact.`

Большой batch на 56 request items вернул HTTP 500 и не применился. После readback-проверки правка была выполнена пятью меньшими batch update groups, от конца документа к началу, чтобы сохранить валидность ранее рассчитанных lower-index ranges.

Readback после правок подтвердил:

- `Листинг (YAML):` не найден;
- `Листинг (Python):` не найден;
- representative captions `Листинг 12.1`, `Листинг 15.10`, `Листинг 21.2`, `Листинг 22.1` найдены в целевом Google Doc.

### 4. Fresh export and Template2000n proof

Созданы артефакты:

- raw Google Docs export: `docs/publisher/artifacts/agent-arch-ru-listing-caption-pass-2026-06-25.docx`;
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-listing-caption-pass-2026-06-25.docx`;
- render QA metrics: `docs/publisher/ru-google-doc-listing-caption-pass-2026-06-25.render-qa.json`;
- next iteration backlog: `docs/publisher/ru-editorial-100-listing-caption-iterations-2026-06-25.md`.

Raw Google Docs export:

- DOCX size: `750004` bytes;
- rendered pages: `655`;
- rendered PDF size: `4285292` bytes;
- blank-like pages: `[]`;
- edge-risk count: `0`;
- semantic listing captions in exported DOCX: `28`;
- generic listing labels in exported DOCX: `0`.

Template2000n derivative:

- DOCX size: `757138` bytes;
- rendered pages: `345`;
- rendered PDF size: `5936205` bytes;
- blank-like pages: `[]`;
- edge-risk count: `0`;
- style mapping counts:
  - `BodyText`: 4259;
  - `Style18`: 3035;
  - `Style16`: 1379;
  - `Heading3`: 571;
  - `Heading2`: 353;
  - `Heading4`: 70;
  - `Style20`: 28;
  - `Heading1`: 25;
  - `Style13`: 1;
  - `Style14`: 1.

Visual spot checks:

- page 1: title/front matter readable; Template2000n boxed title treatment remains and still needs publisher confirmation;
- page 87: dense prose page has no clipping or edge risk, but confirms that long field-name sequences still need editorial compression;
- page 286: Python listing caption and code block render in listing/code style after fixing Template derivative mapping;
- page 345: final page contains final companion guidance and is not blank.

### 5. Report and next 100 iterations

Подготовлен backlog 501-600. Его основная цель - перейти от captions к actual excerpt compression:

- сократить dense field-name sequences;
- вынести full YAML/contracts/CLI/trace catalogs в companion;
- проверить, что каждый listing в печатной книге остается representative excerpt;
- восстановить route mapping между captions и companion artifacts;
- повторить export/render QA после сокращения.

### 6. Repository verification

Этот проход должен быть зафиксирован отдельным commit и push в текущую ветку. В commit входят только новые артефакты listing-caption pass и не входят ранее существовавшие незакоммиченные publisher-файлы.

### 7. Handoff boundary

Этот pass не закрывает всю редакторскую подготовку. Он закрывает label/caption слой и proof-regression после замены generic labels. Следующий содержательный pass должен уже сокращать сами dense excerpts и companion-bound reference material.

## Author-owned fields still required

Следующие поля остаются намеренно незаполненными и должны быть заполнены автором перед внешней редакционной передачей:

1. `[Имя автора / публичное имя]`.
2. `[текущая роль, специализация или независимое позиционирование]`.
3. `[Имя автора]`.
4. `[основная область: архитектура ИИ-агентов, платформенная инженерия, безопасность, продуктовая разработка, developer tooling — выбрать и уточнить]`.
5. `Роль или должность: [заполнить].`
6. `Ключевой опыт: [заполнить 1-2 проверяемые фразы без маркетинговых преувеличений].`
7. `Публичные проекты: [заполнить].`
8. `Ссылки: [GitHub / сайт / блог / профиль / companion — заполнить].`
9. `Формулировка для издательства: [заполнить или согласовать с редактором].`

Дополнительно нужны авторские решения:

- нужен ли блок благодарностей;
- нужно ли посвящение;
- какой канал errata считать публичным;
- какой companion URL и version tag считать каноническими для первой сдачи.

## Следующий практический шаг

Следующий applied pass должен закрыть actual listing compression:

- пройти все 28 captions и их ближайшие code/YAML blocks;
- для каждого listing оставить только строки, необходимые для архитектурного решения;
- полный runnable/config/reference материал вынести в companion routes;
- убрать длинные field-name sequences из основного потока;
- повторить raw export, Template2000n derivative и render QA.
