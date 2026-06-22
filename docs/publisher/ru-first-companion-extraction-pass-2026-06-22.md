# First Companion Extraction Pass

Дата: 2026-06-22

Google Doc: <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Документ: "Архитектура безопасных ИИ-агентов — полная рукопись"

Цель прохода: выполнить первый реальный physical extraction справочного материала из печатной рукописи в companion-модель, не теряя логическую нить книги.

## 1. Inventory Bloated Blocks

Найден главный кандидат первого выноса: хвостовая reference-package область эталонной среды выполнения.

Подтвержденные Google Doc anchors:

- `Примерные конфиги`
- `Запрос, который действительно читает профильную память`
- `Минимальный профиль песочницы`
- `Паттерн долговечного агентного исполнителя`
- `Паттерн агентной оболочки и долговечного стержня процесса`
- `Буквальные маркеры среды выполнения также включают evalgate`

Этот участок работал как reference dump/changelog, а не как печатная глава.

## 2. Companion Manifest

Создан локальный manifest выноса:

- `docs/publisher/ru-companion-extraction-manifest-2026-06-22.md`

В manifest зафиксировано:

- что выносится;
- почему это должно жить в companion;
- что остается в печатной книге;
- какие companion-артефакты нужны дальше.

## 3. First Extraction Pass In Google Doc

В Google Doc удален диапазон от абзаца:

- `Контракты конфигов — раздел «Примерные конфиги».`

до абзаца:

- `Буквальные маркеры среды выполнения также включают evalgate и sessionidempotency_summary...`

Вместо него вставлен компактный печатный блок:

- `Companion: эталонный пакет runtime`

Смысл нового блока:

- печатная книга оставляет архитектурную роль эталонного пакета;
- config lists, CLI-команды, eval datasets, trace/event catalogs, sandbox profile, durable-runner patterns и process-spine backlog уходят в companion;
- читателю явно объясняется критерий: книга отвечает на "зачем и где границы", companion отвечает на "как запустить и проверить".

Connector readback:

- новый блок найден;
- `Минимальный профиль песочницы` не найден;
- `Паттерн долговечного агентного исполнителя` не найден;
- `Буквальные маркеры среды выполнения также включают evalgate` не найден.

## 4. Front Matter Cleanup

В начале рукописи:

- удален дублирующий подзаголовок `Полная издательская рукопись русской версии.`;
- блок `Что получит читатель` переведен из plain-numbered paragraphs в native numbered list;
- текстовый префикс `1. Архитектурный словарь` больше не находится как обычный текст;
- сам пункт `Архитектурный словарь для обсуждения агентных систем` сохранен.

## 5. Export QA

PDF:

- файл проверки: `/private/tmp/agent_arch_extraction_pass_20260622.pdf`
- renderer: Google Docs / Skia PDF
- формат страницы: Letter, 612 x 792 pt
- страниц после прохода: 679
- предыдущий экспорт перед extraction pass: 696 страниц
- сокращение: 17 страниц

DOCX:

- файл проверки: `/private/tmp/agent_arch_extraction_pass_20260622.docx`
- тип: Microsoft Word 2007+
- `unzip -t`: ошибок архива нет

PDF marker check:

- `Companion: эталонный пакет runtime` найден на стр. 679;
- `Минимальный профиль песочницы` не найден;
- `Буквальные маркеры среды выполнения также включают evalgate` не найден;
- `Что получит читатель` найден на стр. 1.

Spot visual QA:

- стр. 1: title/front matter без дублирующего подзаголовка, `Что получит читатель` отображается как нумерованный список;
- стр. 679: compact companion bridge отображается вместо длинного reference dump.

PNG:

- `/private/tmp/agent_arch_extraction_p1-001.png`
- `/private/tmp/agent_arch_extraction_p679-679.png`

## Ограничения

Это первый physical extraction pass, а не полная миграция всех companion-материалов.

Остается дальше:

- продолжить вынос длинных source/reference sections из глав 11-15 и главы 23;
- создать реальные companion files в репозитории по manifest;
- пройти источники и приложения на предмет длинных списков, которые лучше жить в online companion;
- сделать полный DOCX/style pass после согласования издательских стилей.
