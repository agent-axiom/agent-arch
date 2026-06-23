# Full Template2000n publisher pass

Дата прохода: 2026-06-23.

Цель: сделать полный производный DOCX для издательской подготовки на базе текущего Google Doc, применить стили `Template2000n`, сохранить структуру списков, проверить рендер и зафиксировать ограничения перед редакторской сдачей.

## Артефакты

- Source Google Doc: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`.
- Fresh DOCX export: `/private/tmp/agent_arch_full_publisher_pass/current_manuscript.docx`.
- Fresh PDF export: `/private/tmp/agent_arch_full_publisher_pass/current_manuscript.pdf`.
- Publisher DOCX derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-full-2026-06-23.docx`.
- Style metrics: `docs/publisher/ru-template2000n-full-pass-2026-06-23.metrics.json`.
- Render QA metrics: `docs/publisher/ru-template2000n-full-pass-2026-06-23.render-qa.json`.
- Editorial 100-iteration audit metrics: `docs/publisher/ru-editorial-100-iteration-audit-2026-06-23.metrics.json`.

Google Doc не изменялся. Этот проход создал производный DOCX для издательского цикла.

## Пункт 1. Fresh export

Свежий экспорт Google Doc:

- DOCX: 730K;
- PDF: 647 страниц;
- Google Docs PDF page size: Letter, 612 x 792 pt;
- Drive modified time: `2026-06-22T19:15:18.224Z`.

Вывод: исходная Google Doc рукопись остается полнообъемной рукописью. Объем Google Docs PDF - 647 страниц.

## Пункт 2. Структурная нормализация

Производный DOCX собран от свежего Google DOCX export с сохранением исходного `numbering.xml`. Это важно: реальные списки не были превращены в ручные дефисы.

Правила нормализации:

- первые строки front matter получили publisher template styles;
- настоящие `Heading1-4` сохранены только для коротких заголовков, глав и приложений;
- длинные heading-like абзацы понижены до `BodyText`;
- code/YAML/CLI/trace-like строки переведены в `Программа`;
- numbered/bulleted paragraphs сохранили прямой `numPr`;
- основной текст переведен в `BodyText`.

Метрики:

| Метрика | Значение |
| --- | ---: |
| Текстовых абзацев | 7801 |
| Сохраненных/выделенных настоящих заголовков | 1121 |
| Псевдозаголовков, пониженных в body | 1172 |
| Code-like блоков, переведенных в `Программа` | 1010 |
| Списков в source DOCX | 2817 |
| Списков в target DOCX | 2817 |

Target style counts:

| Target style | Count |
| --- | ---: |
| `BodyText` | 3091 |
| `Style18` / `список` | 2574 |
| `Style16` / `Программа` | 1010 |
| `Heading3` | 692 |
| `Heading2` | 295 |
| `Heading4` | 68 |
| `Heading1` | 66 |
| `Style15` / `Прим_осн` | 3 |
| `Style13` / `лист_назв` | 1 |
| `Style14` / `Пред_заг` | 1 |

## Пункт 3. Template2000n application

`Template2000n` styles были перенесены в publisher DOCX derivative. Во время визуального QA обнаружен артефакт: `Heading1-5` в старом шаблоне содержали `numPr`, который после merge styles стал ссылаться на Google Docs bullet numbering. Это создавало черные маркеры перед заголовками.

Исправление:

- `numPr` удален только из copied `Heading1`, `Heading2`, `Heading3`, `Heading4`, `Heading5`;
- реальные списки сохранены, потому что прямой `numPr` source paragraphs не трогался.

## Пункт 4. Render QA

Рендер выполнен через Documents `render_docx.py`.

Итоговый publisher derivative:

- DOCX size: 741K;
- rendered PDF pages: 388;
- rendered PDF page size: Letter, 612 x 792 pt;
- PNG count: 388;
- PNG dimensions: 1547 x 2002;
- blank-like pages: 0;
- edge-risk pages: 0;
- low-ink pages: 0;
- high-ink pages: 0.

Визуально проверены contact-sheet страницы:

- начало: 1, 2, 3, 10;
- ранняя структура: 17, 18;
- середина: 50, 100, 150, 200, 250, 300, 350;
- приложения: 363, 369, 376, 384;
- конец: 388.

Marker pages по PDF text extraction:

| Маркер | Страницы |
| --- | --- |
| `Аннотация` | 1 |
| `Об авторе` | 2 |
| `Глава 1` | 17, 18, 20, 33, 96 |
| `Глава 10` | 18, 136, 158, 172, 193 |
| `Глава 20` | 18, 251, 256, 290, 379 |
| `Приложение 1` | 363 |
| `Приложение 2` | 369 |
| `Приложение 3` | 376 |
| `Приложение 4` | 384 |

## Пункт 5. QA report for издательство

Результат этого прохода можно использовать как publisher-style proof, но не как финальный подписанный макет.

Что улучшено:

- создан полный DOCX derivative под `Template2000n`;
- сохранены реальные списки;
- устранен artifact с bullet markers перед заголовками;
- обнаружены и понижены псевдозаголовки;
- code-like блоки отделены от обычного body text;
- получен renderable 388-page publisher proof.

Оставшиеся ограничения:

- Google Doc не был изменен; source manuscript остается прежним.
- В DOCX export Google Docs ссылки пришли как plain text: hyperlink restoration нужен отдельным pass.
- Титульный стиль `лист_назв` дает серую/рамочную строку; нужно подтвердить у издателя, что это ожидаемая часть шаблона.
- Полный человеческий proofread всех 388 страниц не выполнялся; был render QA + visual spot check.
- Авторские поля в блоке "Об авторе" остаются незаполненными.
- Содержательная редактура, fact-check и внешняя вычитка не заменяются этим style pass.

## Следующий редакционный контур

Следующий контур должен идти не от стилей, а от содержания:

1. пройти 100-iteration editorial backlog;
2. заполнить авторские поля;
3. восстановить/нормализовать ссылки;
4. принять решение по титульному стилю;
5. выполнить full proofread с редактором;
6. после редакторской правки повторить DOCX export, Template2000n pass и render QA.
