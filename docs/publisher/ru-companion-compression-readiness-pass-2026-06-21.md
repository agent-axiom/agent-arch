# Companion, Compression, And Readiness Pass

Дата: 2026-06-21

Google Doc: <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Документ: "Архитектура безопасных ИИ-агентов — полная рукопись"

Цель прохода: выполнить следующий редакционный production-pass по пяти пунктам: отделить книгу от companion-материалов, добавить читательскую рамку для длинных технических блоков, стабилизировать маршрут по частям, подготовить рукопись к будущему DOCX/style mapping и провести publisher-readiness QA.

## Выполненные пункты

1. Companion extraction pass.
   - В Google Doc добавлен раздел "Как устроен online companion".
   - В разделе зафиксировано, что печатная книга оставляет решения, критерии, риски и минимальные формы контрактов.
   - В companion должны уходить полные YAML-конфиги, CLI-транскрипты, event catalogs, validation-message catalogs, datasets, exporter commands, длинные payload и рабочие diff-описания.

2. Смысловая компрессия.
   - Добавлен раздел "Первое чтение и углубление".
   - Рукопись теперь явно объясняет два режима чтения: линейное чтение как маршрут архитектурных решений и повторное чтение как инструмент ревью конкретной capability.

3. Стабилизация структуры.
   - Добавлен раздел "Маршрут по частям" в блок "Как устроена логика книги".
   - Зафиксирована роль частей I-VII и приложений: словарь, границы, данные, runtime, наблюдаемость, организационная модель, практические шаблоны и companion-материалы.

4. DOCX/style readiness.
   - Исправлен style defect в Google Doc: тело "Терминологического соглашения" переведено из heading-style в обычный body text.
   - Пустые heading-параграфы во front matter сброшены в `NORMAL_TEXT`.
   - Повторно подтверждено, что `Template2000n.dot` является старым бинарным Word 2000 `.dot` с VBA; напрямую применять его к live Google Doc не нужно.
   - Текущий рабочий путь остается таким: Google Doc как рукопись, DOCX export как следующий контролируемый этап, Template2000n как источник style mapping.

5. Publisher-readiness QA.
   - Connector readback подтвердил наличие новых разделов:
     - "Как устроен online companion";
     - "Первое чтение и углубление";
     - "Маршрут по частям".
   - Connector readback подтвердил, что "Редакционный паспорт готовности рукописи" отсутствует.
   - PDF export выполнен.
   - DOCX export выполнен и проверен как валидный zip/package.

## Export QA

PDF:

- файл проверки: `/private/tmp/agent_arch_readiness_pass_20260621.pdf`
- renderer: Google Docs / Skia PDF
- формат страницы: Letter, 612 x 792 pt
- страниц: 696

DOCX:

- файл проверки: `/private/tmp/agent_arch_readiness_pass_20260621.docx`
- тип: Microsoft Word 2007+
- `unzip -t`: ошибок архива нет

Точечная визуальная проверка PDF:

- стр. 2: терминологическое соглашение отображается как обычный текст перед "Об авторе";
- стр. 7: блок "Как устроен online companion" читается перед "Границы ответственности";
- стр. 9: блок "Первое чтение и углубление" читается перед "Для кого эта книга";
- стр. 10: блок "Маршрут по частям" отображается как список внутри раздела логики книги.

Отрендеренные PNG:

- `/private/tmp/agent_arch_readiness_p2-002.png`
- `/private/tmp/agent_arch_readiness_p7-007.png`
- `/private/tmp/agent_arch_readiness_p9-009.png`
- `/private/tmp/agent_arch_readiness_p10-010.png`

## Ограничения

Это targeted readiness pass, а не полная финальная вычитка всех 696 страниц.

Что остается следующим этапом:

- пройти главы и приложения на физический перенос длинных reference-package блоков в online companion;
- заменить plain numbered paragraphs в front matter на native numbered list там, где это нужно для DOCX;
- продолжить сокращение накопительных фрагментов, особенно в приложениях и reference-package секциях;
- после согласования стилей применить Template2000n style mapping к экспортированному DOCX в отдельной рабочей копии;
- выполнить полный DOCX/PDF render QA после style mapping.
