# RU case-driven reader pass

Дата: 2026-07-08.

Статус: реализовано в Markdown-источнике и синхронизировано с рабочим Google
Doc.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit>

Final known Google Doc revision after this pass:

- `ALtnJHyYW6fQ0qGMYUCvDvxPe-XeGIyad3TCc04jbFpVBsadXNCqxgJc2XA7J1mKVrJ5R-rTr38Sx9BRFGlXU1ZwcaMG41O-OI4OFSx0Fmk`

## Цель

Сделать рукопись интереснее и рекомендабельнее для читателя, который после
книги должен захотеть переслать ее коллегам как рабочий способ обсуждать
безопасных агентов.

## Что реализовано

1. **Сквозной кейс как мини-сериал.** Добавлен блок `Семь серий сквозного
   кейса`, связывающий семь частей книги с постепенным взрослением агента
   поддержки.
2. **Сцены в ключевых главах.** Усилены главы 12 и 16: повтор с неизвестным
   побочным эффектом и спор о расширении волны выпуска стали более живыми.
3. **Практическое действие после чтения.** Добавлен раздел `Как применить книгу
   после чтения` с маршрутами за 7 дней, за 30 дней и на архитектурном ревью.
4. **Фразы для пересказа.** Добавлены 15 коротких фраз, которые читатель может
   использовать в разговоре с командой.
5. **100 редакционных итераций.** Зафиксирован отдельный отчет:
   `docs/publisher/ru-editorial-100-case-driven-reader-iterations-2026-07-08.md`.

## Что изменилось для читателя

Рукопись стала меньше похожа на большой справочник и сильнее похожа на
практическую историю: один агент поддержки проходит путь от эффектного демо до
управляемого launch gate. Финал теперь не просто закрывает книгу, а предлагает
читателю применить материал за неделю, за месяц или на архитектурном ревью.

## Проверки Google Doc

- Target document confirmed: `1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`,
  tab `t.0`.
- `Семь серий сквозного кейса`: connector verification found 1 occurrence.
- `Как применить книгу после чтения`: connector verification found 1 occurrence.
- `15 фраз, которые удобно переслать коллегам`: connector verification found 1
  occurrence.
- `Сильная сцена этой главы — не экран с зеленым тестом`: connector verification
  found 1 occurrence.

## Локальные проверки

Выполненные проверки перед commit/push:

- `git diff --check` — passed.
- `uv run pytest tests/test_docs_surface.py tests/test_agent_runtime_ref.py` —
  948 passed.
- `uv run --group docs mkdocs build --strict` — passed.
- Google Doc connector readback по ключевым вставкам — passed.

## Author-owned fields still required

Автору остается заполнить:

- публичное имя автора и byline;
- короткую и длинную биографию;
- роль, публичное позиционирование и проверяемый опыт;
- публичные ссылки;
- публичный URL online companion и версионирование;
- благодарности;
- legal/compliance disclaimer;
- AI-use disclosure, если потребуется издательству;
- финальные publisher metadata и cover copy.
