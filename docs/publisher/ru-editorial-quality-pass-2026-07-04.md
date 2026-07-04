# Редакционный quality pass русской рукописи

Date: 2026-07-04.

Status: applied to repository control files and targeted Google Doc body
paragraphs. This is not a fresh DOCX export/render pass.

Canonical Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- title: `Архитектура безопасных ИИ-агентов — полная рукопись`
- tab: `t.0`
- post-edit revision:
  `ALtnJHynC5_zU9n9cmTvBjPl9UMeD7Uve6QHp3PDDm33ZwWHCfBekh00ktjv4-xnUtiwP6hL7W39I4iTLk77MaTY60Z8DnRkpVQxhi5p46U`

## 1. Placeholders and service blocks

Result: no accidental manuscript placeholders were found in the book body.

Known author-owned fields remain intentionally open:

- `[Имя автора / публичное имя]`;
- `[текущая роль или независимое позиционирование]`;
- `[1 короткая фраза о релевантном опыте]`;
- `Публичные проекты и ссылки: [заполнить].`

These fields must be filled by the author or explicitly omitted before final
publisher submission.

## 2. Heading and TOC risk

Markdown heading scan did not find overlong H2/H3 headings created by the
current pass.

The remaining TOC risk is not a Markdown-source problem. It is a proof/style
layer risk: final DOCX export still needs human TOC review after author fields
and the next styled export.

## 3. Chapters 20 and 21 density

Chapter 20 remains the densest lifecycle chapter:

- `ru-manuscript-full.md`: about 16,155 words, 113 H3 headings, 928 bullet or
  numbered lines and 17 code blocks.
- editorial issue: useful material, but it can still read like a compressed
  operations reference.

Chapter 21 is more book-shaped but still implementation-heavy:

- `ru-manuscript-full.md`: about 9,611 words, 23 H3 headings, 200 bullet or
  numbered lines and 25 code blocks.
- editorial issue: implementation value is high, but code/config material must
  stay visibly subordinate to the architectural argument.

Applied changes:

- added a two-paragraph chapter-role bridge to Chapter 20 in
  `docs/publisher/ru-manuscript-full.md`;
- added a two-paragraph chapter-role bridge to Chapter 21 in
  `docs/publisher/ru-manuscript-full.md`;
- inserted matching bridge paragraphs into the full Google Doc body before the
  first subsection of Chapter 20 and before the existing introduction of
  Chapter 21;
- verified Google Doc readback for both inserted paragraphs.

Important sync note: the current Google Doc chapter body is newer than parts of
`ru-manuscript-full.md` around Chapters 20-21. The next source-stabilization
pass should reconcile the local full manuscript source with the Google Doc
book-ready body before the next DOCX export.

## 4. Repeated endings

Scan result:

- `Что делать дальше`: 20 H3 occurrences;
- repeated final H3 headings: 11 chapters close with `Что делать дальше`;
- several other closing labels repeat intentionally: `Что читать дальше`,
  `Полезные справочные страницы`, `Что сделать сразу`.

Decision:

- keep the repeated closing blocks as a deliberate navigation rhythm for now;
- do not expand them into long web-style tails;
- on the next prose pass, normalize them part by part into shorter transitions
  when a chapter already has enough closing guidance.

## 5. Anglicism pass

Applied careful replacements in `docs/publisher/ru-source-map.md`,
`docs/publisher/ru-manuscript-map.md`, `docs/publisher/ru-manuscript-full.md`
and targeted Google Doc text:

- `workflow, single-agent, multi-agent` -> `рабочий процесс, одиночный агентный
  цикл, многоагентная схема`;
- `rollout` -> `поэтапный выпуск`;
- `runtime` in chapter titles/tasks -> `среда исполнения`;
- `Assurance loop, incident response, registry и retirement` -> `Контур
  заверения, реагирование на инциденты, реестр и вывод из эксплуатации`;
- `Companion boundary` / `online companion` -> `граница онлайн-приложения` /
  `онлайн-приложение`;
- `sample`, `failure story`, `line edit`, `tool gateway`, `production launch
  checklist` and similar editorial labels were replaced with Russian wording.
- first-page manuscript phrasing such as `source-to-print`, `DOCX/export QA`,
  `companion-материалы`, `prompt tricks`, `production architecture`,
  `demo-агент`, `reference package` and `incident/postmortem template` was
  replaced where the text was prose rather than a file name or code reference.

Intentionally not changed:

- file names and paths such as `agent_runtime_ref`, `change-rollout-schema.md`,
  `policy-templates.md`, `Template2000n.dot`;
- command names, YAML keys, JSON fields and API error strings;
- stable protocol names and abbreviations such as `MCP`, `A2A`, `ADLC`, `SLO`,
  `DOCX`, `CLI` where replacing them would reduce precision.

## 6. Next 100 iterations

Created:

- `docs/publisher/ru-editorial-100-editorial-quality-iterations-2026-07-04.md`

The new ledger continues the existing numbering from 3701 to 3800 and focuses
on source/Google Doc convergence, chapter 20-21 compression, repeated endings,
terminology, final export QA and author-owned fields.

## Current blocker summary

The manuscript is stronger after this pass, but it is still not a final
publisher submission. Remaining blockers:

- author bio/byline/public links/current role are not filled;
- publisher/editor acceptance of the macro-free Template2000n route is not
  recorded;
- external proofread is still needed;
- post-author Google Doc export, Template2000n rebuild and render QA still need
  to be rerun;
- local full manuscript source and the Google Doc body should be reconciled
  before the next final export.
