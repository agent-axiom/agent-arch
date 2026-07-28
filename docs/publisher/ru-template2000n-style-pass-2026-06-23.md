# Template2000n style bridge pass

Дата прохода: 2026-06-23.

Цель: проверить издательский шаблон `Template2000n.dot`, сопоставить его стили с текущей рукописью Google Doc и подготовить безопасный путь к будущему полному DOCX-style pass без изменения исходного Google Doc.

## Исходные артефакты

- Шаблон издательства: `/Users/if/Downloads/Telegram Desktop/Template2000n.dot`.
- Конвертированный шаблон для анализа: `/private/tmp/template2000n_inspect/Template2000n.docx`.
- Google Doc рукописи: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`.
- DOCX-экспорт рукописи для анализа: `/private/tmp/agent_arch_template_pass/current_manuscript.docx`.
- PDF-экспорт рукописи для контроля объёма: `/private/tmp/agent_arch_template_pass/current_manuscript.pdf`.
- Пробный DOCX-фрагмент: `/private/tmp/agent_arch_template_pass/template2000n_trial_fragment.docx`.

Google Doc не изменялся. Все DOCX/PDF/PNG артефакты этого прохода созданы во временном каталоге.

## Текущий объём рукописи

PDF-экспорт Google Doc через Google Docs renderer:

- страниц: 647;
- формат страницы: Letter, 612 x 792 pt;
- источник: Google Doc `Архитектура безопасных ИИ-агентов - полная рукопись`;
- modified time по Drive: `2026-06-22T19:15:18.224Z`.

Это подтверждает, что текущий Google Doc остаётся полнообъёмной рукописью, а не 70-страничной compressed assembly.

## Анализ Template2000n.dot

`Template2000n.dot` - старый бинарный Word template:

- формат: Composite Document File V2 / Word 9.0;
- кодировка: Windows code page 1251;
- размер: 105K;
- последняя дата сохранения в метаданных: 2005-07-20;
- исходный шаблон в метаданных: `Template2000.dot`.

LibreOffice headless сначала упал на создании профиля пользователя, поэтому конвертация выполнена с отдельными writable `HOME` и `UserInstallation` в `/private/tmp`. После этого `.dot` успешно конвертирован в DOCX.

Инвентаризация стилей после конвертации:

- paragraph styles: 35;
- character styles: 34;
- numbering styles: 16;
- содержимого в самом шаблоне почти нет: один пустой `Normal`-параграф.

Ключевые paragraph styles шаблона:

| Назначение | Style ID | Имя стиля | Основные признаки |
| --- | --- | --- | --- |
| Обычный текст | `Normal` | `Normal` | Times New Roman, 10 pt |
| Основной книжный текст | `BodyText` | `Body Text` | based on `Normal`, after 80 twips |
| Заголовок 1 | `Heading1` | `Heading 1` | 20 pt, bold, outline 0 |
| Заголовок 2 | `Heading2` | `Heading 2` | 16 pt, bold, outline 1 |
| Заголовок 3 | `Heading3` | `Heading 3` | 14 pt, bold, outline 2 |
| Заголовок 4 | `Heading4` | `Heading 4` | 12 pt, bold, outline 3 |
| Титульная строка | `Style13` | `лист_назв` | 9 pt, bold, boxed/bordered visual treatment in render |
| Предварительный заголовок | `Style14` | `Пред_заг` | bold italic |
| Примечание | `Style15` | `Прим_осн` | 9 pt |
| Программа/код | `Style16` | `Программа` | Courier New, 9 pt |
| Список | `Style18` | `список` | list/body-like |
| Список B | `Style19` | `СписокБ` | list/body-like |
| Подпись рисунка | `Style17` | `Рис_подпись` | 8 pt italic |
| Заголовок таблицы | `Style20` | `Таб_заг` | 9.5 pt italic |
| Заголовок ячейки | `0` | `Таб_заг_0` | 9 pt bold |
| Текст таблицы | `Style21` | `Таб_осн` | 9 pt |
| Врезка | `Style23` | `Врезка_осн` | based on `Normal` |
| Заголовок врезки | `Style24` | `Врезка_заг` | bold |
| Эпиграф | `Style27` | `Эпиграф` | 8 pt italic |

Ключевые character styles:

- `Courier` - Courier New, 9 pt;
- `Ссылка` - italic link-like style;
- `Курсив` - Times New Roman italic;
- `Полужирный` - Times New Roman bold.

## Анализ текущего DOCX-экспорта рукописи

DOCX-экспорт Google Doc содержит:

- текстовых абзацев: 7801;
- таблиц: 0;
- numbered/bulleted paragraphs: 2817;
- явных `w:hyperlink` в DOCX: 0.

Реальное использование стилей:

| Style ID | Count | Комментарий |
| --- | ---: | --- |
| `Normal/implicit` | 5089 | Основной текст, списки, часть code-like строк |
| `Heading2` | 1272 | Смешаны настоящие H2 и длинные обычные абзацы |
| `Heading3` | 1120 | Смешаны настоящие H3 и фрагменты справочного текста |
| `Heading1` | 250 | Главы/приложения, но также часть длинных абзацев |
| `Heading4` | 70 | Локальные подзаголовки |

Выявленный риск: Google Doc сейчас содержит много псевдозаголовков.

- `Heading2`, похожих на обычные длинные абзацы: 763;
- `Heading3`, похожих на обычные длинные абзацы: 129;
- `Heading1`, похожих на обычные длинные абзацы: 155;
- code/YAML-like строк, пришедших как heading styles: 411.

Это означает, что полный издательский pass нельзя делать механическим правилом `HeadingN -> Heading N`. Нужен guard: длинные предложения, абзацы с точкой и code-like строки должны уходить в body/code styles, даже если исходный экспорт пометил их как heading.

## Style mapping

| Элемент рукописи | Текущий DOCX / Google Doc | Стиль Template2000n | Правило |
| --- | --- | --- | --- |
| Название книги | первый `Normal/implicit` paragraph | `лист_назв` или отдельный согласованный title style | Использовать осторожно: render показывает рамочную линию вокруг title |
| Подзаголовок | второй `Normal/implicit` paragraph | `Пред_заг` | Подходит для subtitle, но требует проверки с издателем |
| Статус/source notes | первые служебные абзацы | `Прим_осн` | Служебный блок перед сдачей лучше убрать или перенести в editorial notes |
| Главы, приложения, крупные блоки | `Heading1` | `Heading 1` | Только если строка короткая и реально является заголовком |
| Разделы | `Heading2` | `Heading 2` | Применять после pseudo-heading guard |
| Подразделы | `Heading3` | `Heading 3` | Применять после pseudo-heading guard |
| Локальные подзаголовки | `Heading4` | `Heading 4` | Оставить для настоящих 4-level headings; избегать глубже H4 |
| Основной текст | `Normal/implicit` | `Body Text` | Основной стиль полной книги |
| Маркированные/нумерованные списки | `numPr` + visible list text | `список`, `СписокБ`, `СписокБ2` | Списки нужно переносить как настоящие Word lists, не как дефисы/ручные номера |
| Code/YAML/CLI/trace fields | mostly `Normal/implicit`, sometimes headings | `Программа` paragraph + `Courier` character | Полные длинные листинги лучше переносить в companion; в книге оставлять минимальные фрагменты |
| Inline code | plain runs | `Courier` character | Для `trace_id`, `capability_id`, путей, имён файлов, CLI команд |
| URL/source references | plain text after Google export | `Ссылка` character или publisher hyperlink style | Google DOCX export не дал `w:hyperlink`, поэтому ссылки нужно восстанавливать отдельным pass |
| Таблицы | отсутствуют в текущем export | `Таб_заг`, `Таб_заг_0`, `Таб_осн` | Если таблицы появятся, строить с явной геометрией и повторяемыми header rows |
| Врезки/заметки | обычный текст | `Врезка_заг`, `Врезка_осн` | Использовать дозированно для предупреждений, readiness notes, production caveats |
| Подписи рисунков | отсутствуют сейчас | `Рис_подпись`, `Caption` | При появлении диаграмм captions должны быть реальными стилями |
| Эпиграфы | отсутствуют сейчас | `Эпиграф` | Не использовать без редакторского решения |

## Правила для полного издательского pass

1. Сначала нормализовать структуру, потом применять стили.
2. Не считать `Heading1/2/3` истинным заголовком без проверки длины, пунктуации и соседнего контекста.
3. Все code-like строки переводить в `Программа`, даже если текущий DOCX экспортировал их как heading.
4. Lists должны остаться настоящими Word lists; manual `-` допустим только если это часть печатной цитаты или literal example.
5. URL и references нужно отдельно восстанавливать как hyperlinks или согласованные печатные source entries.
6. Длинные YAML/CLI/reference package walkthrough не держать в теле книги: они должны жить в online companion, а в рукописи оставаться как короткие архитектурные excerpts.
7. Приложения использовать тот же heading ladder, но с явным префиксом `Приложение N`.
8. Перед full pass сделать копию DOCX и не импортировать обратно в Google Doc без отдельного решения.
9. Стилевой pass должен создавать publisher DOCX derivative, а Google Doc остаётся source manuscript для содержательной редакции.

## Trial DOCX style pass

Фрагмент:

- начало рукописи: 115 текстовых абзацев;
- начало `Приложение 4. Источники и online companion`: 89 текстовых абзацев;
- итоговый DOCX: `/private/tmp/agent_arch_template_pass/template2000n_trial_fragment.docx`.

Применённые правила в trial pass:

| Source style | Target style | Count |
| --- | --- | ---: |
| `Normal/implicit` | `Body Text` | 128 |
| `Heading2` | `Heading 2` | 42 |
| `Normal/implicit` | `список` | 11 |
| `Heading2` | `Body Text` | 9 |
| `Heading1` | `Heading 1` | 5 |
| `Normal/implicit` | `Прим_осн` | 3 |
| `Normal/implicit` | `Программа` | 3 |
| `Normal/implicit` | `лист_назв` | 1 |
| `Normal/implicit` | `Пред_заг` | 1 |
| `Heading3` | `Heading 3` | 1 |

Render QA:

- renderer: Documents skill `render_docx.py`;
- output: `/private/tmp/agent_arch_template_pass/rendered_trial`;
- PDF pages: 17;
- PDF page size: A4, 595.304 x 841.89 pt;
- visual spot check: contact sheet + pages 1, 12, 16;
- результат: кириллица читается, явного clipping/overlap нет, heading ladder работает.

Замечания по trial render:

- `лист_назв` даёт видимую рамочную/пунктирную линию вокруг title; перед полной обработкой нужно решить с издателем, это ожидаемое оформление или артефакт старого шаблона.
- Основной текст получается плотным и книжным; для 647-страничного Google Doc полный publisher DOCX может стать заметно меньше по страницам, потому что шаблон A4 + 10 pt плотнее Google Docs Letter layout.
- В trial pass списки были перенесены как стилизованные абзацы; для full pass нужно сохранить/создать real Word numbering definitions.

## Рекомендованный следующий практический этап

Сделать отдельный publisher DOCX derivative для всей рукописи:

1. Экспортировать свежий DOCX из Google Doc.
2. Запустить структурный нормализатор:
   - pseudo-heading guard;
   - code-like detector;
   - list preservation;
   - URL/link restoration plan;
   - appendix heading normalization.
3. Применить Template2000n styles.
4. Отрендерить полный DOCX в PDF/PNG и проверить:
   - начало книги;
   - начало и конец каждой части;
   - все приложения;
   - страницы с code-like blocks;
   - страницы со списками;
   - последние страницы.
5. Сформировать отдельный QA report для издательства: page count, style counts, unresolved issues, known editorial placeholders.

До этого не стоит применять шаблон напрямую к Google Doc: текущая рукопись должна оставаться содержательным source of truth, а издательский DOCX - производным артефактом.
