# Editor handoff packet: русская рукопись

Date: 2026-06-28.

Status: исторический рабочий handoff для редактора после первичного readiness
pass. Superseded by the clean packet:
`docs/publisher/ru-clean-editor-handoff-packet-2026-06-28.md`.

## Главная ссылка

- Google Doc:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Title: `Архитектура безопасных ИИ-агентов - полная рукопись`
- Current revision after handoff pass:
  `ALtnJHycqUJOlgHPJs2U9ylHl3Hb3yhnF1EbR9nU-226k7V7gsDB2qhrsoJHyuIcNkupHbgkOOZCTNgLuY7C4PZCthT9URSRwaB0eDeXCSo`

## Что передается редактору

Редактору можно читать текущий Google Doc как цельную рабочую рукопись:

- 7 частей;
- 23 главы;
- front matter, glossary, practical cases and appendices;
- авторский блок оставлен как заполняемый placeholder;
- online companion вынесен как отдельный слой для шаблонов, CLI, trace,
  eval datasets, changelog and errata.

Цель handoff: получить содержательную и структурную редактуру, а не финальную
версточную приемку. Финальная приемка DOCX возможна только после author fields,
global heading normalization, publisher style pass and external proofread.

## Текущий proof

Raw Google Docs export:

- DOCX:
  `docs/publisher/artifacts/agent-arch-ru-editor-handoff-pass-2026-06-28.docx`
- Rendered pages: 552.
- Blank-like pages: 0.
- Paragraphs in DOCX: 8040.
- Heading 1 paragraphs after cleanup: 26.
- Heading 2 paragraphs: 1393.
- Heading 3 paragraphs: 578.
- Remaining long H2 paragraphs flagged as style debt: 629.

Render metadata:

- `docs/publisher/ru-editor-handoff-readiness-pass-2026-06-28.render-qa.json`

## Что было исправлено в Google Doc

Выполнен точечный style-only batchUpdate:

1. Обычные body paragraphs в конце главы 3, перед `Часть II`, больше не
   оформлены как `Heading 1`.
2. Обычные body paragraphs в главе 20, перед `Часть VII`, больше не оформлены
   как `Heading 1`.
3. Настоящие H2/H3 subheads в этих диапазонах восстановлены.
4. H1 outline теперь показывает только крупные разделы, главы/части и
   front/back matter, а не обычный prose.

Смысловой текст не удалялся и не вставлялся. Операция меняла только paragraph
style.

## Что редактору смотреть в первую очередь

1. Читательская дуга: demo-agent failure -> platform responsibility -> safety
   and control -> memory/retrieval -> execution/runtime -> evidence/evals ->
   organization/ADLC -> launch.
2. Повторяемость глав: где одинаковые ending blocks помогают чтению, а где
   звучат механически.
3. Перегруженность некоторых технических глав: особенно 11, 13, 15, 20, 21.
4. Граница book/companion: печатная книга должна оставлять аргумент и
   минимальные артефакты, companion должен хранить полные YAML/CLI/trace/eval.
5. Авторский голос: убрать места, где текст читается как документационная
   сборка, а не как авторская IT-книга.

## Что пока не отдавать как финал

Не считать финальными:

- author bio and author/platform facts;
- title/subtitle/cover copy;
- final publisher metadata;
- public companion URL and release version;
- legal/compliance and AI-use disclosure wording;
- Template2000n/publisher-ready DOCX;
- final page count after publisher styles.

## Открытые риски

### P0: author-owned fields

Автор должен заполнить фактические сведения о себе, публичные ссылки,
подтверждаемые проекты, acknowledgements and publisher-facing wording.

### P0: global heading normalization

Raw export still has 629 long H2 paragraphs that look like ordinary body text.
This does not break the current H1 outline, but it must be fixed before final
publisher-ready DOCX and any automatic TOC/style mapping.

### P1: companion completeness

Companion skeleton now exists, but content still needs to be filled and
versioned for release: templates, checklists, errata, changelog, runtime
reference and source links.

### P1: final source verification

Fast-changing product/API/provider facts must be rechecked before publication.
This is especially important for OpenAI/model/provider-specific statements.

## Recommended editor workflow

1. Read front matter, chapter 1 and chapter 23 first to understand promise and
   final payoff.
2. Review chapters 20-21 as a late-book density risk.
3. Review one technical evidence chapter: chapter 13 or 15.
4. Leave comments in the Google Doc for structure, repetition, terminology and
   missing examples.
5. Keep layout/style comments separate from content comments until heading
   normalization and publisher-style pass are complete.

## Repository control files

- Roadmap: `docs/publisher/ru-editorial-roadmap.md`
- Workflow: `docs/publisher/ru-google-doc-workflow.md`
- Evolution ledger: `docs/publisher/ru-manuscript-evolution.md`
- Submission checklist: `docs/publisher/ru-submission-checklist.md`
- Author open fields: `docs/publisher/ru-author-open-fields-2026-06-28.md`
- Next 100 goals:
  `docs/publisher/ru-editorial-100-editor-handoff-iterations-2026-06-28.md`
