# Workflow синхронизации русской рукописи с Google Docs

Status: рабочее правило для издательской подготовки.

Google Docs:

- Full manuscript: `Архитектура безопасных ИИ-агентов — полная рукопись`
- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Book-readiness editorial map:
  `Архитектура безопасных ИИ-агентов — редакционная карта готовой книги`
- <https://docs.google.com/document/d/1XoU_nWZkpKGU7SxZ0pgmE_dfcNNggQokZsbzind7kXc>
- Compressed/staging snapshot: `Архитектура безопасных ИИ-агентов`
- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

## Source of truth

Репозиторий остается источником правды для содержания:

- русские главы: `docs/book/**/*.md`;
- приложения: `docs/appendix/**/*.md`;
- издательские карты и чеклисты: `docs/publisher/*.md`;
- исполняемый companion: `agent_runtime_ref/**`.

Google Doc является рабочей издательской рукописью:

- удобен для чтения, редакторских комментариев и последующего DOCX-экспорта;
- не заменяет git history и Markdown diff;
- не является местом, где живут окончательные смысловые изменения без обратной
  синхронизации в репозиторий.
- может содержать временные рабочие блоки перед основным текстом; эти блоки
  не включаются в финальную сдачу, пока явно не перенесены в front matter.

На 2026-06-15 полная рукопись собрана в
`docs/publisher/ru-manuscript-full.md`, экспортирована в Google Docs-targeted
DOCX, проверена render smoke QA на 437 страницах и импортирована как native
Google Doc:
<https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>.
Старый 71-страничный Google Doc оставлен как compressed/staging snapshot и
содержит ссылку на полный документ.

На 2026-06-28 свежий Google Docs export после editor handoff readiness pass:

- Google Doc revision:
  `ALtnJHycqUJOlgHPJs2U9ylHl3Hb3yhnF1EbR9nU-226k7V7gsDB2qhrsoJHyuIcNkupHbgkOOZCTNgLuY7C4PZCthT9URSRwaB0eDeXCSo`;
- raw DOCX proof:
  `docs/publisher/artifacts/agent-arch-ru-editor-handoff-pass-2026-06-28.docx`;
- render QA: 552 pages, 0 blank-like pages;
- H1 outline normalized: two body ranges in chapter 3 / chapter 20 were
  returned from `Heading 1` to normal text, with true H2/H3 subheads restored;
- remaining style risk: 629 long `Heading 2` paragraphs in the raw export need
  a dedicated global heading normalization pass before final publisher-ready
  DOCX.

Следующие этапы после handoff-pass: author-owned поля, global heading
normalization, повторная вычитка, terminology/cross-reference polish, финальный
Template2000n/publisher-style pass, DOCX/export QA и внешняя вычитка.

На 2026-06-28 свежий Google Docs export после global heading normalization:

- Google Doc final revision:
  `ALtnJHzNhgv8hnqRh5oLPZThYvoczugICZiF6hYYJONYVWXqOJNwaqd3-DNNZS0b0vTU3eViqETu4lXKcvyq2eSe4cYMqn8xVAQKc_5Hla4`;
- raw DOCX proof:
  `docs/publisher/artifacts/agent-arch-ru-heading-normalized-2026-06-28.docx`;
- Template2000n proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-heading-normalized-2026-06-28.docx`;
- raw render QA: 504 pages, 0 blank-like pages;
- Template2000n render QA: 315 pages, 0 blank-like pages;
- long non-empty `Heading 2` debt: 0.

Следующие этапы после heading-normalization-pass: H3/body-style cleanup,
author-owned поля, финальная вычитка, terminology/cross-reference polish,
финальный publisher-style pass, DOCX/export QA и внешняя вычитка.
Эволюция рукописи отслеживается отдельно:

- `docs/publisher/ru-manuscript-evolution.md`
- `docs/publisher/ru-editorial-roadmap.md`
- `docs/publisher/ru-book-readiness-audit.md`

## Правило изменения текста

1. Смысловая правка сначала делается или фиксируется в Markdown.
2. После этого соответствующий фрагмент переносится в Google Doc.
3. Если правка родилась в Google Doc во время редакторского прохода, она
   возвращается в Markdown перед следующей сборкой.
4. Изменения стиля, переносов, служебных заголовков и издательского оформления
   могут жить только в Google Doc/DOCX, если они не меняют смысл.

## Правило сборки глав

Для каждой договорной главы используется `docs/publisher/ru-source-map.md`.

Перед переносом главы в Google Doc:

- проверить источники;
- удалить web-only navigation;
- превратить admonitions в печатные врезки или обычный prose;
- оставить длинные schemas, CLI output, validation errors и полный runtime
  walkthrough в online companion;
- применить `docs/publisher/ru-terminology.md`.

## Временный стиль

До получения стилевых файлов БХВ:

- Google Doc использует простой native Google Docs style;
- титул и заголовки оформляются без декоративных линий;
- таблицы используются только для настоящих сопоставимых данных;
- схемы переносятся только если они нужны печатному чтению.

После получения стилевых файлов БХВ:

- обновить DOCX/Google Doc formatting strategy;
- проверить соответствие требованиям издательства;
- отдельно проверить экспортный DOCX перед финальной сдачей.

## Проверки перед внешней отправкой

- `git diff --check`;
- `uv run pytest`;
- `uv run mkdocs build --strict`;
- чтение Google Doc через Drive API после крупного переноса;
- raw DOCX render QA после каждой крупной Google Doc правки;
- Template2000n/publisher-style render QA после global heading normalization.
