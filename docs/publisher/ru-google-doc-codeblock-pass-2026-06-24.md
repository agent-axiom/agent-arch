# Google Doc code-block normalization pass 2026-06-24

Дата прохода: 2026-06-24.

Целевой документ: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`.

Название документа: `Архитектура безопасных ИИ-агентов — полная рукопись`.

Рабочий tab: `t.0`.

Revision после правок: `ALtnJHx8rYGtnrjMg9ktpn0uzJr-ax5Hul3f6SKJI7VX5aIxsDe7J746gD13SmpLfPI1SnBbVGcg6gKOlK_2PGIDqSbk0l8EC62o0F6TztY`.

## Реализованные пункты

### 1. Target guard and code-fence inventory

Перед правками через Google Drive connector подтвержден целевой Google Doc:

- document id: `1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
- title: `Архитектура безопасных ИИ-агентов — полная рукопись`;
- tab id: `t.0`;
- исходный revision для batch write: `ALtnJHylPUTZQrNWZLCLS78JrNC-O65sp56zrtR8Ky1rcSMRIkPPsGwAJJYHQvUK-nvVhCHFsC4DVX3_0W8l4iUd86fAHmzOWZoHj0SFkkw`.

Инвентаризация подтвердила, что самый заметный дефект Template2000n proof был связан не с пустой страницей, а с literal Markdown fence marker в теле рукописи.

### 2. Google Doc code-fence normalization

В Google Doc выполнена batch-нормализация Markdown fence markers:

- ` ```yaml` преобразовано в `Листинг (YAML):` - 27 совпадений;
- ` ```python` преобразовано в `Листинг (Python):` - 1 совпадение;
- generic closing fences ` ``` ` удалены - 28 совпадений;
- ` ```mermaid`, ` ```bash`, ` ```json`, ` ```text` не имели совпадений в текущей версии документа.

Readback через `find_document_text_range` подтвердил:

- ` ```yaml` отсутствует;
- ` ```python` отсутствует;
- generic ` ``` ` отсутствует;
- `Листинг (YAML):` присутствует;
- `Листинг (Python):` присутствует.

### 3. Trailing blank source cleanup

Финальный семантический абзац документа начинается с текста:

> Практическое правило: если материал помогает понять архитектурное решение...

После него был обнаружен короткий хвостовой диапазон пустого содержимого. Диапазон после финального абзаца удален с revision guard.

Readback подтвердил, что финальный семантический абзац сохранен, а literal fence markers в документе больше не находятся.

### 4. Fresh export and Template2000n proof

Созданы артефакты:

- raw Google Docs export: `docs/publisher/artifacts/agent-arch-ru-codeblock-pass-2026-06-24.docx`;
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-codeblock-pass-2026-06-24.docx`;
- render QA metrics: `docs/publisher/ru-google-doc-codeblock-pass-2026-06-24.render-qa.json`;
- next iteration backlog: `docs/publisher/ru-editorial-100-codeblock-iterations-2026-06-24.md`.

Raw Google Docs export:

- DOCX size: `749310` bytes;
- rendered pages: `655`;
- rendered PDF size: `4284587` bytes;
- blank-like pages: `[]`;
- edge-risk count: `0`;
- visual spot check: page 1 clean, page 121 and page 372 are intentional short tail pages, final page contains content and is not blank.

Template2000n derivative:

- DOCX size: `760560` bytes;
- rendered pages: `409`;
- rendered PDF size: `5697700` bytes;
- blank-like pages: `[]`;
- edge-risk count: `0`;
- style mapping counts:
  - `Style18`: 2815;
  - `BodyText`: 2794;
  - `Heading3`: 810;
  - `Style16`: 664;
  - `Heading2`: 539;
  - `Heading1`: 90;
  - `Heading4`: 68;
  - `Style13`: 1;
  - `Style14`: 1.

Visual spot checks:

- page 326: isolated Markdown fence marker removed; page now contains code/listing content;
- page 394: low-ink tail page contains rollout text and is not blank;
- page 409: final page contains final reference package content and is not blank.

### 5. Editorial backlog 401-500

Подготовлены следующие 100 итераций для доведения рукописи до редакционно сильного состояния. Основной фокус следующего блока: не просто удалить Markdown следы, а переработать крупные YAML/code excerpts так, чтобы печатная книга читалась как архитектурный текст, а полные контракты, логи, каталоги сообщений и CLI-сессии жили в companion.

### 6. Repository handoff

Этот проход должен быть зафиксирован отдельным commit и push в текущую рабочую ветку. В коммит входят только новые артефакты code-block pass и не включаются уже существующие незакоммиченные изменения по другим publisher-файлам.

## Remaining editorial debt

Code-fence markers удалены, но это не означает, что все листинги готовы к печати. Следующий editorial pass должен решить содержательную проблему:

- длинные YAML-фрагменты нужно сжать до архитектурно необходимых excerpts;
- полные контракты, validation-message catalogs, trace/event catalogs и CLI-сессии нужно вынести или явно привязать к companion routes;
- подписи `Листинг (YAML):` и `Листинг (Python):` нужно заменить на осмысленные caption-like формулировки;
- страницы с высокой плотностью технического текста нужно проверить в Template2000n proof на читабельность.

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

Следующий applied pass должен закрыть содержательную переработку listing layer:

- пройти все `Листинг (YAML):` и `Листинг (Python):`;
- заменить generic labels на конкретные caption-like подписи;
- оставить в печати только representative snippets;
- вынести полные artifacts в companion или явно пометить их как companion-bound;
- повторить raw export + Template2000n render QA.
