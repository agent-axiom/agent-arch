# RU shareable manuscript pass

Дата: 2026-07-09.

Статус: реализовано в Markdown-источнике и синхронизировано с рабочим Google
Doc. Локальные проверки, commit и push фиксируются ниже после выполнения.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit>

Final known Google Doc revision after sync:

- `ALtnJHzZr7VI02Br2rAaV9XrskgaxvU9N9oa0I6SzFJ-_mRbW4V-yjK4aptCYF8Ba9oSyXhs5DiwIXVR1LJnG84vIODhXdrez0YJxIAo0xE`

## Цель

Сделать рукопись интереснее, практичнее и более рекомендабельной для читателя,
который после чтения должен хотеть переслать книгу друзьям и коллегам как
рабочий способ обсуждать безопасных агентов.

## Что реализовано в Markdown

1. **Досье сквозного кейса.** Добавлен блок `Досье сквозного кейса` с
   продуктовой целью, участниками, критичными возможностями, главным риском и
   доказательствами готовности.
2. **Сцены-открытия частей.** Добавлены семь коротких производственных сцен,
   по одной перед каждой частью книги.
3. **Wrong/right контрасты.** Добавлен блок `Неправильно / промышленно` с
   восемью практическими сравнениями для команды.
4. **Практика в репозитории.** Усилен маршрут от книги к companion-файлам,
   trace/eval artifacts и `uv run pytest tests/test_agent_runtime_ref.py`.
5. **Командные артефакты.** Добавлен блок `Пять артефактов, которые удобно
   переслать команде`.

## Проверки Google Doc

Target document confirmed:

- document id: `1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`
- title: `Архитектура безопасных ИИ-агентов — полная рукопись.docx`
- tab: `t.0`

Connector marker checks after sync:

- `Досье сквозного кейса`: 1 occurrence.
- `Семь сцен-открытий частей`: 1 occurrence.
- `Мини-маршрут на один вечер`: 1 occurrence.
- `Практика в репозитории после чтения`: 1 occurrence.
- `Неправильно / промышленно`: 1 occurrence.
- `Пять артефактов, которые удобно переслать команде`: 1 occurrence.

Note: in Markdown the seven part-opening scenes are placed at the start of the
seven parts. In Google Doc they were synced as one consolidated
`Семь сцен-открытий частей` block because exact part headings appear twice in
the live document and single-heading replacement would not be safe.

## Локальные проверки

Выполненные проверки перед commit/push:

- `git diff --check` — passed.
- `uv run pytest tests/test_docs_surface.py tests/test_agent_runtime_ref.py` —
  948 passed.
- `uv run --group docs mkdocs build --strict` — passed.

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
