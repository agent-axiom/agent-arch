# Google Doc applied pass 2026-06-24

Дата прохода: 2026-06-24.

Целевой документ: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`.

Название документа: `Архитектура безопасных ИИ-агентов — полная рукопись`.

Рабочий tab: `t.0`.

Revision после правок: `ALtnJHylPUTZQrNWZLCLS78JrNC-O65sp56zrtR8Ky1rcSMRIkPPsGwAJJYHQvUK-nvVhCHFsC4DVX3_0W8l4iUd86fAHmzOWZoHj0SFkkw`.

## Реализованные пункты

### 1. Target guard

Перед правками через Google Drive connector подтвержден целевой Google Doc:

- document id: `1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
- title: `Архитектура безопасных ИИ-агентов — полная рукопись`;
- tab id: `t.0`;
- исходный revision для batch write: `ALtnJHxZxCOu_7VEvscZzqF_p-RdxetrBJ9YM64IZ42NwDdy_4CisYkOR60IoCB1Y1uy3PdNCiyYLJi5Ung3Abh7Biwu2LucOL1XMMby5tY`.

Первое совпадение заголовков глав 6-10 находится в навигационном блоке, поэтому правки делались по вторым совпадениям заголовков в теле рукописи.

### 2. Applied content pass for chapters 6-10

В Google Doc добавлены пять lead-параграфов `Редакционный фокус` после реальных заголовков:

- `Глава 6. Инструментальный шлюз, подтверждения и журнал аудита`;
- `Глава 7. Зачем агенту память и почему она опасна`;
- `Глава 8. Краткосрочная, долгосрочная и профильная память`;
- `Глава 9. Извлечение контекста, уплотнение и фоновые обновления`;
- `Глава 10. Модель выполнения и каталог инструментов`.

Смысл прохода: удержать в начале каждой главы практическую редакционную рамку: что глава должна доказать, где находится граница ответственности и какие технические детали должны уходить в companion.

Readback через `find_document_text_range` подтвердил все пять вставок:

- `эта глава должна перевести tool calling из уровня демонстрации`;
- `эта глава должна объяснить память как управляемый риск`;
- `эта глава должна превратить короткую, долгосрочную и профильную память`;
- `эта глава должна показать retrieval как управляемую подачу контекста`;
- `эта глава должна закрепить модель выполнения вокруг каталога инструментов`.

### 3. Listing and companion-boundary sweep

В раздел `Как читать листинги и YAML` добавлено практическое следствие для глав 6-10:

> Практическое следствие для глав 6-10: в печатном тексте остаются короткие фрагменты интерфейса, контракта или политики, которые нужны для архитектурного решения. Если пример превращается в справочник полей, полный trace, CLI-сессию или catalogue dump, он должен быть представлен как companion route, а не как основной поток главы.

Readback подтвердил строку `Практическое следствие для глав 6-10`.

### 4. Fresh export and proof artifacts

Созданы артефакты:

- raw Google Docs export: `docs/publisher/artifacts/agent-arch-ru-applied-pass-2026-06-24.docx`;
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-applied-2026-06-24.docx`;
- render QA metrics: `docs/publisher/ru-google-doc-applied-pass-2026-06-24.render-qa.json`;
- next iteration backlog: `docs/publisher/ru-editorial-100-applied-iterations-2026-06-24.md`.

Raw Google Docs export:

- DOCX size: `749362` bytes;
- rendered pages: `656`;
- rendered PDF size: `4288542` bytes;
- blank-like pages: `[656]`;
- edge-risk count: `0`;
- visual spot check: page 1 clean, pages 121 and 372 are intentional short tail pages, page 656 is trailing blank.

Template2000n derivative:

- DOCX size: `760470` bytes;
- rendered pages: `411`;
- rendered PDF size: `5723306` bytes;
- blank-like pages: `[]`;
- edge-risk count: `0`;
- style mapping counts:
  - `BodyText`: 2865;
  - `Style18`: 2817;
  - `Heading3`: 835;
  - `Style16`: 576;
  - `Heading2`: 555;
  - `Heading1`: 92;
  - `Heading4`: 68;
  - `Style13`: 1;
  - `Style14`: 1.

Known proof issue: Template2000n page 326 contains an isolated Markdown fence marker `````yaml` after a heading. It is not a blank-page or edge-clipping defect, but it is a content/layout issue for the next code-block normalization pass.

Known style issue preserved from the publisher template bridge: page 1 still has a boxed title treatment. This must be confirmed or rejected by the publisher/template owner before final handoff.

## Author-owned fields still required

The following fields remain intentionally unresolved in the manuscript and must be filled by the author before external editorial delivery:

1. `[Имя автора / публичное имя]`.
2. `[текущая роль, специализация или независимое позиционирование]`.
3. `[Имя автора]`.
4. `[основная область: архитектура ИИ-агентов, платформенная инженерия, безопасность, продуктовая разработка, developer tooling — выбрать и уточнить]`.
5. `Роль или должность: [заполнить].`
6. `Ключевой опыт: [заполнить 1-2 проверяемые фразы без маркетинговых преувеличений].`
7. `Публичные проекты: [заполнить].`
8. `Ссылки: [GitHub / сайт / блог / профиль / companion — заполнить].`
9. `Формулировка для издательства: [заполнить или согласовать с редактором].`

Дополнительно нужно принять авторские решения:

- нужен ли блок благодарностей;
- нужна ли посвящение;
- какой канал errata считать публичным;
- какой companion URL и version tag считать каноническими для первой сдачи.

## Следующий практический шаг

Следующий applied pass должен закрыть `code-block normalization`:

- убрать или преобразовать literal Markdown fence markers в Google Doc;
- назначить человекочитаемые подписи листингам;
- оставить в печати только короткие excerpts;
- длинные YAML, CLI, trace/event catalogs и validation-message catalogs привязать к companion routes;
- повторить raw export + Template2000n render QA.
