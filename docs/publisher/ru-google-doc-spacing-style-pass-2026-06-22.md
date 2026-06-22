# Проход по склейкам и абзацным стилям Google Doc

Дата: 2026-06-22.

Целевой Google Doc: `Архитектура безопасных ИИ-агентов — полная рукопись`.

Документ: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`

## Цель прохода

Стабилизировать редакционно-техническую форму рукописи после companion-компрессии:

- отличить реальные склейки заголовков и абзацев от артефактов plain-text extraction;
- исправить загрязнение heading-стилями в хвостовом приложении;
- подтвердить результат через DOCX/PDF export QA;
- зафиксировать состояние для следующего template/style pass.

## Что проверено

Свежий DOCX export был разобран на уровне `word/document.xml`.

Проверка показала, что часть подозрительных строк из plain-text extraction не является
реальными одноабзацными склейками. Главная подтвержденная проблема находилась в
`Приложение 4. Источники и online companion`: большой блок обычного текста,
нумерованных строк и справочных маршрутов получил стиль `Heading2`.

До правки в окне приложения 4 были heading-styled body paragraphs:

- body-абзацы `Книга описывает архитектурные принципы...` и
  `Печатная рукопись должна оставаться устойчивой...`;
- строки состава companion `1. Шаблоны...` - `6. Errata...`;
- маршруты `/README.md`, `/templates`, `/evals`, `/traces`, `/diagrams`,
  `/checklists`, `/cases`, `/errata`;
- body-абзацы про источники, errata, AI-tool transparency, exclusions и checklist;
- public/repo строки, которые должны быть обычным текстом, а не heading.

## Что изменено в Google Doc

В Google Doc выполнен стилевой `batchUpdate` без изменения текста:

- диапазон `751214-761361` в tab `t.0` нормализован в `NORMAL_TEXT`;
- настоящие подзаголовки приложения 4 возвращены в `HEADING_2`;
- `Приложение 4. Источники и online companion` сохранено как `Heading1`;
- `Зачем нужен online companion` сохранен как `Heading2`;
- обычные абзацы, чеклистовые строки и reference routes оставлены `NORMAL_TEXT`.

Новая Google Docs revision после правки:
`ALtnJHyRT04OJBT4gLkw5U8AK8I3BCI8C7htonEPMonmOtPwD9SMeCOyfC5DjyZlMNjqMfAtCKP1Kaq8lck6a03TdoE6QsWH0evRzPVJv5w`.

## DOCX structural readback

После правки свежий DOCX export показал:

- окно приложения 4: paragraphs `7713-7801`;
- `Heading2` в приложении 4: 15 строк;
- long heading-styled paragraphs в приложении 4: 0;
- `Книга описывает архитектурные принципы...`: `NORMAL_TEXT`;
- `Минимальный состав companion...`: `NORMAL_TEXT`;
- `1. Шаблоны capability contract...`: `NORMAL_TEXT`;
- `Полный список источников: docs/appendix/sources.md.`: `NORMAL_TEXT`;
- `Справочные маршруты:`, `Как пользоваться источниками`,
  `Как пользоваться reference package`, `Что остается в печатной рукописи` и
  `Что остается в companion`: `HEADING_2`.

## QA после экспорта

Финальный export QA выполнен после Google Doc style batch:

- DOCX export скачан во временный файл
  `/private/tmp/agent_arch_spacing_pass_20260622_after.docx`;
- `unzip -t /private/tmp/agent_arch_spacing_pass_20260622_after.docx`
  завершился без ошибок;
- PDF export скачан во временный файл
  `/private/tmp/agent_arch_spacing_pass_20260622_after.pdf`;
- `pdfinfo` показывает `Pages: 647`, формат `612 x 792 pts (letter)`,
  `Encrypted: no`, `PDF version: 1.4`;
- целевой PDF range приложения 4 определен как страницы `640-647`;
- `pdftoppm` отрендерил страницы `640-647` для targeted visual smoke-check;
- страница 641 подтверждает, что состав companion и repo structure читаются как
  body/list text, а не как крупный `Heading2`;
- страница 646 подтверждает, что compact routes, `agent_runtime_ref`, источники
  и печатные/companion подзаголовки визуально разделены;
- старое слитное имя runtime-пакета в хвостовом PDF-поиске не найдено.

Это targeted visual QA измененной зоны, а не полный постраничный visual review всех
647 страниц. Полный постраничный просмотр остается задачей финального
издательского pass после применения шаблонов БХВ.

## Локальные проверки repo

После добавления отчёта выполнены проверки:

- терминологический `rg` по устаревшему слитному имени runtime-пакета в `docs`,
  `README.ru.md`, `README.md` и `mkdocs.yml` не нашёл совпадений;
- `git diff --check` завершился без замечаний;
- `uv run --group dev pytest` завершился успешно: `948 passed`;
- `uv run --group docs mkdocs build --strict` завершился с кодом 0; в выводе
  остались только существующие informational сообщения о publisher-страницах вне
  `nav` и предупреждение Material for MkDocs.
