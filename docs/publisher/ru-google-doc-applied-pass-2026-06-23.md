# Google Doc applied pass

Дата прохода: 2026-06-23.

Назначение: выполнить следующий практический applied-pass уже в рабочем Google Doc, а не только в локальных отчетах. Этот проход закрывает пять пунктов текущего плана: front matter cleanup, link restoration, content pass по главам 1-5, code/examples pass, fresh export + Template2000n derivative + render QA.

## Target document

- Working Google Doc: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`
- Title: `Архитектура безопасных ИИ-агентов — полная рукопись`
- Tab: `t.0`
- Staging snapshot `1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4` не редактировался.

## Пункт 1. Author/front matter cleanup

Реализовано в Google Doc:

- удалены три служебные строки из тела рукописи:
  - `Статус: полнообъемная source-to-print сборка из русских Markdown-источников репозитория.`
  - `Источник правды: agent-axiom/agent-arch, русские файлы docs/book/ и docs/appendix/.`
  - `Примечание для издательского цикла: авторские поля, стили БХВ, DOCX/export QA и финальная внешняя вычитка остаются отдельными этапами.`
- удаление выполнено одним guarded batchUpdate по диапазону `79-387`;
- readback подтвердил: после подзаголовка теперь сразу идет `Аннотация`;
- блок `Об авторе` сохранен как author-owned заготовка, placeholders не выдумывались.

Следующий action: автор заполняет фактическую биографию, публичные ссылки, role/positioning, key experience и издательскую формулировку.

## Пункт 2. Link restoration

Реализовано в Google Doc:

- заменены длинные `github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref` occurrences на `см. online companion`;
- заменены длинные `github.com/.../blob/main/agent_runtime_ref/...` file URLs на `см. online companion`;
- публичная строка companion заменена на короткую метку `Публичная версия companion: online companion.`;
- публичная строка репозитория заменена на короткую метку `Исходный репозиторий: agent-axiom/agent-arch.`;
- на две публичные строки в приложении применены активные hyperlinks:
  - `https://agent-axiom.github.io/agent-arch/`;
  - `https://github.com/agent-axiom/agent-arch`.

Connector result:

- internal long URL replacements: 14;
- public label replacements: 2;
- targeted public link ranges found and linked;
- check for raw `https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref` after pass returned no match.

Следующий action: после авторского подтверждения companion URL выполнить финальный hyperlink audit для всех форматов: Google Doc, DOCX, PDF, EPUB.

## Пункт 3. Content pass по главам 1-5

Реализовано в Google Doc:

- добавлены пять lead-блоков `Редакционный фокус` после реальных заголовков глав 1-5;
- first occurrences в карте книги не трогались; вставки сделаны по second occurrence реальных chapter headings;
- readback подтвердил наличие всех пяти новых блоков.

Добавленные фокусы:

1. Глава 1: центральная линия книги - платформа ответственности вокруг модели.
2. Глава 2: отличие agent use case от обычной workflow automation.
3. Глава 3: reference architecture как карта ответственностей, а не рецепт стека.
4. Глава 4: безопасность через границы доверия, а не каталог атак.
5. Глава 5: identity, session, policy и capability catalog как язык допуска к действиям.

Следующий action: продолжить такой же content pass для глав 6-10, затем сделать cross-reference pass между частями.

## Пункт 4. Code/examples pass

Реализовано в Google Doc:

- в разделе `Как читать листинги и YAML` добавлен блок `Редакционное правило для листингов`;
- правило фиксирует критерий: в печати остается только фрагмент, который помогает понять архитектурную границу, контракт, риск или проверку;
- полные YAML, CLI transcripts, trace payload, event catalogs и validation-message catalogs должны жить в online companion.

Следующий action: сделать chapter-level sweep по длинным listings: оставить архитектурные excerpts в книге, а полные воспроизводимые материалы вынести в companion.

## Пункт 5. Fresh export + Template2000n + render QA

Реализовано:

- выполнен fresh DOCX export из обновленного Google Doc;
- fresh export сохранен как `docs/publisher/artifacts/agent-arch-ru-applied-pass-2026-06-23.docx`;
- fresh Google Docs export отрендерен: 654 PNG pages, PDF size 4.1M;
- обнаружена одна trailing blank-like page в сыром Google Docs export: page 654;
- собран новый publisher derivative с Template2000n style definitions:
  - `docs/publisher/artifacts/agent-arch-ru-template2000n-applied-2026-06-23.docx`;
  - paragraph count: 7804;
  - preserved lists: 2817;
  - heading numbering artifact prevention: `numPr` removed from `Heading1-5` styles;
- Template2000n-applied proof отрендерен: 419 PNG pages, PDF size 5.6M;
- Template2000n-applied raster QA:
  - blank-like pages: 0;
  - edge-risk pages: 0;
  - high-ink pages: 0;
  - low-ink sample pages: 198, 403, 419;
  - visual spot check: page 1 and page 419.

Сравнение объемов:

| Artifact | Pages | Notes |
| --- | ---: | --- |
| Previous Google Docs PDF source | 647 | Before this applied pass. |
| Fresh Google Docs export after edits | 654 | Includes one trailing blank-like page. |
| Previous Template2000n derivative | 388 | Before this applied pass. |
| New Template2000n-applied derivative | 419 | Includes applied edits and no blank-like pages. |

Следующий action: после следующих текстовых правок повторить fresh export + Template2000n derivative + render QA и отдельно устранить trailing blank page in raw Google Docs export if it remains.

## Что остается author-owned

Автор должен заполнить:

1. `[Имя автора / публичное имя]`.
2. `[текущая роль, специализация или независимое позиционирование]`.
3. `[Имя автора]`.
4. `[основная область: архитектура ИИ-агентов, платформенная инженерия, безопасность, продуктовая разработка, developer tooling - выбрать и уточнить]`.
5. `Роль или должность: [заполнить].`
6. `Ключевой опыт: [заполнить 1-2 проверяемые фразы без маркетинговых преувеличений].`
7. `Публичные проекты: [заполнить].`
8. `Ссылки: [GitHub / сайт / блог / профиль / companion - заполнить].`
9. `Формулировка для издательства: [заполнить или согласовать с редактором].`

Дополнительно автор должен решить:

- нужна ли благодарность или посвящение;
- какой final companion URL считать каноническим;
- какой errata/contact route публиковать;
- какие публичные проекты можно связывать с книгой;
- какая биография идет в книгу, а какая только в metadata/cover note.

## Следующий practical sequence

1. Applied content pass для глав 6-10.
2. Sweep длинных listings в главах 1-10.
3. Author fill.
4. Final link/hyperlink audit.
5. Fresh export + Template2000n + render QA after each large content batch.
