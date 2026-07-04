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

На 2026-06-28 свежий Google Docs export после H3/body-style normalization:

- Google Doc final revision:
  `ALtnJHw6vaLfM9UxyXN5JznqrcdZlswujEW24-EA9HTu2x8hawmbTG2yBEi0VVTw7GbNA2i0JzD2IRGuzVA8JHSR9mTbMrYi4MukvIiPr0w`;
- raw DOCX proof:
  `docs/publisher/artifacts/agent-arch-ru-h3-normalized-2026-06-28.docx`;
- Template2000n proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-h3-normalized-2026-06-28.docx`;
- raw render QA: 499 pages, 0 blank-like pages;
- Template2000n render QA: 315 pages, 0 blank-like pages;
- long non-empty `Heading 2` debt: 0;
- long non-empty `Heading 3` debt: 0;
- paragraph text equality preserved against the previous H2-normalized proof.

Следующие этапы после H3-normalization-pass: author-owned поля, финальная
вычитка, terminology/cross-reference polish, финальный publisher-style pass,
DOCX/export QA и внешняя вычитка.

На 2026-06-28 свежий Google Docs export после author/front-matter и
publisher-style proof pass:

- Google Doc final revision:
  `ALtnJHxghK0ux39XZSQMkGfFh_TqFc9QasJFxuerN_vYLBxxWKS036rEaQmQRW9mCVrBIR2uNFtXgg1EbDTdIopzLmiVbROaOd-e0Vj1GTQ`;
- raw editorial-ready proof:
  `docs/publisher/artifacts/agent-arch-ru-editorial-ready-2026-06-28.docx`;
- Template2000n editorial-ready proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-ready-2026-06-28.docx`;
- raw render QA: 499 pages, 0 blank-like pages;
- Template2000n render QA: 315 pages, 0 blank-like pages;
- paragraph text equality preserved between raw and Template2000n proofs;
- author-owned front-matter fields are isolated and clearly labelled.

Следующие этапы после clean handoff pass: заполнить author-owned факты,
провести внешнюю редактуру/вычитку, обновить companion metadata, повторить
raw/Template2000n export QA after author fields and prepare the final
publisher submission packet.

На 2026-06-28 подготовлен post-author workflow:

- `docs/publisher/ru-post-author-final-export-workflow-2026-06-28.md`;
- финальный Google Doc update, raw export and Template2000n rebuild не
  выполняются до получения author-owned фактов;
- новый next-goal ledger:
  `docs/publisher/ru-editorial-100-post-author-export-iterations-2026-06-28.md`.
Эволюция рукописи отслеживается отдельно:

- `docs/publisher/ru-manuscript-evolution.md`
- `docs/publisher/ru-editorial-roadmap.md`
- `docs/publisher/ru-book-readiness-audit.md`

На 2026-07-01 выполнен latest-practices sync pass:

- `docs/publisher/ru-manuscript-full.md` получил 13 late-practice sections из
  `docs/book/**`;
- полный Google Doc получил восемь недостающих print-oriented practice blocks;
- свежий plain-text readback Google Doc подтвердил 101,584 approximate words
  and each of the eight newly inserted practice headings exactly once;
- отчет прохода: `docs/publisher/ru-latest-practices-sync-pass-2026-07-01.md`;
- следующий блок целей:
  `docs/publisher/ru-editorial-100-latest-practices-sync-iterations-2026-07-01.md`.

Этот проход усиливает содержание рукописи, но не заменяет финальный
publisher-style DOCX export. Старые proof artifacts от 2026-06-28 нужно считать
предыдущими proof snapshots до нового export/render QA после author-owned fields
and style application.

На 2026-07-02 выполнен practice-polish proof pass после latest-practices sync:

- Google Doc revision after polish:
  `ALtnJHzfp6dC10EFS5o6ohijtZNURxfuA7ekf6CeXSwFg1YCzXmjCNOpESmN9VBBEEvbYrZJzansw1fJ8_TU-zsqxWG4y3Q97gUQtQz-Duk`;
- raw DOCX working proof:
  `docs/publisher/artifacts/agent-arch-ru-layout-style-pass-2026-07-02.docx`;
- Template2000n working proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-layout-style-pass-2026-07-02.docx`;
- render QA: raw 507 pages and Template2000n 371 pages, 0 blank-like pages;
- report:
  `docs/publisher/ru-google-doc-layout-style-pass-2026-07-03.md`;
- render QA metadata:
  `docs/publisher/ru-google-doc-layout-style-pass-2026-07-03.render-qa.json`;
- next-goal ledger:
  `docs/publisher/ru-editorial-100-layout-style-proof-iterations-2026-07-03.md`.

Этот proof является актуальным working DOCX для редакционного чтения после
layout/style cleanup. Он не является финальной publisher-ready сдачей:
author-owned поля, внешняя вычитка, publisher-approved style application and
final raw/Template2000n render QA остаются открытыми.

На 2026-07-03 выполнен legacy outline/style cleanup в существующем Google Doc:

- Google Doc revision after cleanup:
  `ALtnJHwG2y0y6xdziVEBWf1jHm7r6i_bkXLaj0f_p_1raU2fzYu7XbniNYm86oBYvk_aFiwhUgAkAa8LnjW7E-hl6iMi5fJR-77zzvllovI`;
- raw DOCX working proof:
  `docs/publisher/artifacts/agent-arch-ru-legacy-outline-style-pass-2026-07-03.docx`;
- Template2000n working proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-legacy-outline-style-pass-2026-07-03.docx`;
- render QA: raw 489 pages and Template2000n 351 pages, 0 blank-like pages;
- report:
  `docs/publisher/ru-google-doc-legacy-outline-style-pass-2026-07-03.md`;
- render QA metadata:
  `docs/publisher/ru-google-doc-legacy-outline-style-pass-2026-07-03.render-qa.json`;
- next-goal ledger:
  `docs/publisher/ru-editorial-100-legacy-outline-style-iterations-2026-07-03.md`.

Этот proof сокращает ложный outline noise: heading paragraphs reduced from
1352 to 1152 without changing the 6105 non-empty paragraph text sequence.
Google Doc remains the manuscript source of truth; local DOCX files are proof
and publisher-style derivative artifacts.

На 2026-07-03 выполнен Template2000n official-style pass с приложенным
`Template2000n.dot`:

- raw DOCX working proof:
  `docs/publisher/artifacts/agent-arch-ru-publisher-style-raw-2026-07-03.docx`;
- Template2000n official-style working proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-official-style-pass-2026-07-03.docx`;
- render QA: raw 489 pages and Template2000n official-style 357 pages, 0
  blank-like pages;
- report:
  `docs/publisher/ru-google-doc-template2000n-official-style-pass-2026-07-03.md`;
- render QA metadata:
  `docs/publisher/ru-google-doc-template2000n-official-style-pass-2026-07-03.render-qa.json`;
- next-goal ledger:
  `docs/publisher/ru-editorial-100-template2000n-official-style-iterations-2026-07-03.md`.

`Template2000n.dot` is a legacy Word 2000 binary template. The pass did not run
VBA/macros: the `.dot` was converted to a DOCX style source, then styles/theme
were applied conservatively while preserving raw manuscript numbering and text
sequence.

На 2026-07-03 зафиксирован final editorial handoff layer:

- final editorial handoff plan:
  `docs/publisher/ru-final-editorial-handoff-plan-2026-07-03.md`;
- Template2000n acceptance gate:
  `docs/publisher/ru-template2000n-acceptance-gate-2026-07-03.md`;
- author fill packet for the current proof:
  `docs/publisher/ru-author-editorial-fill-packet-2026-07-03.md`;
- Google Doc and DOCX handoff policy:
  `docs/publisher/ru-google-doc-docx-handoff-policy-2026-07-03.md`;
- next 100 final handoff goals:
  `docs/publisher/ru-editorial-100-final-handoff-iterations-2026-07-03.md`.

Policy summary: repository remains the semantic source of truth, Google Doc is
the working editorial manuscript, raw DOCX is a dated export baseline, and the
Template2000n DOCX is a regenerated publisher-style proof candidate.

На 2026-07-03 выполнен final pre-author export/render pass:

- raw DOCX:
  `docs/publisher/artifacts/agent-arch-ru-final-preauthor-raw-2026-07-03.docx`;
- Template2000n pre-author DOCX:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-final-preauthor-2026-07-03.docx`;
- render QA: raw 489 pages and Template2000n pre-author 361 pages, 0
  blank-like pages;
- report:
  `docs/publisher/ru-final-preauthor-export-pass-2026-07-03.md`;
- QA metadata:
  `docs/publisher/ru-final-preauthor-export-pass-2026-07-03.render-qa.json`;
- pre-author publisher packet:
  `docs/publisher/ru-preauthor-publisher-submission-packet-2026-07-03.md`;
- next 100 post-preauthor goals:
  `docs/publisher/ru-editorial-100-post-preauthor-iterations-2026-07-03.md`.

Google Doc front matter was checked through connector readback. The `Об авторе`
block still contains author-owned placeholders, so this pass is intentionally
pre-author and not final publisher submission.

На 2026-07-04 выполнен quality-sync/terminology pass в текущем Google Doc:

- Google Doc revision after terminology cleanup:
  `ALtnJHwPMvOVdwcrz2tbGM0rdze_Ped9LzfMOgWtZCTtkIG1K5pXx008c-6ckzYavZt9Wn-LtRrB9r16Q37qcoztxBoKsxdBLmi6LKr_EW4`;
- excessive English editorial terms were reduced with 293 guarded exact
  replacements, followed by 23 grammatical corrections;
- readback found no exact `online companion`, `policy gateway`, `tool gateway`
  or `incident response`;
- new Template2000n quality-sync proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-quality-sync-2026-07-04.docx`;
- render QA: raw baseline 489 pages and Template2000n quality-sync 357 pages,
  0 blank-like pages;
- report:
  `docs/publisher/ru-google-doc-quality-sync-pass-2026-07-04.md`;
- next 100 quality-sync/export goals:
  `docs/publisher/ru-editorial-100-quality-sync-export-iterations-2026-07-04.md`.

Important limitation: the current Google Doc changed after the latest saved raw
DOCX baseline. The next publisher-critical proof cycle must start with a fresh
authenticated raw DOCX export from the updated Google Doc.

На 2026-07-04 выполнен post-terminology export pass, который закрывает это
ограничение для текущей ревизии Google Doc:

- final Google Doc revision:
  `ALtnJHzZWz2-IJ7JpxskwAFAeTHIK5wTRmKA_MrDjFTgOlPIbOMvFgV7Go8Trlwx1WPtElObAQ1OmEI0Tbg7i8I4NJ5RyfZdmR8apePtOyc`;
- fresh raw DOCX export:
  `docs/publisher/artifacts/agent-arch-ru-post-terminology-raw-2026-07-04.docx`;
- Template2000n derivative:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-post-terminology-2026-07-04.docx`;
- render QA: raw 493 pages, Template2000n 359 pages, 0 blank-like pages in
  both proofs;
- report:
  `docs/publisher/ru-google-doc-post-terminology-export-pass-2026-07-04.md`;
- next 100 post-terminology/export goals:
  `docs/publisher/ru-editorial-100-post-terminology-export-iterations-2026-07-04.md`.

New limitation: the current proof is suitable for editor discussion, but final
submission still requires author-owned fields, external proofread and a repeat
post-author export/render cycle.

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
  walkthrough в онлайн-сопровождении;
- применить `docs/publisher/ru-terminology.md`.

## Текущий стиль

До финального подтверждения издательского style route:

- Google Doc использует простой native Google Docs style;
- Template2000n pre-author proof существует как DOCX derivative;
- таблицы используются только для настоящих сопоставимых данных;
- схемы переносятся только если они нужны печатному чтению.

Если издательство подтверждает текущий Template2000n route:

- закрыть author-owned поля;
- принять редакторские правки;
- повторить свежий raw export, Template2000n style pass and render QA перед
  финальной сдачей.

Если издательство не подтверждает текущий route:

- зафиксировать replacement route в
  `docs/publisher/ru-template2000n-acceptance-gate-2026-07-03.md`;
- не использовать текущий styled DOCX как финальную сдачу;
- повторить style pass and render QA по route, который подтвердит издательство.

## Проверки перед внешней отправкой

- `git diff --check`;
- `uv run pytest`;
- `uv run mkdocs build --strict`;
- чтение Google Doc через Drive API после крупного переноса;
- raw DOCX render QA после каждой крупной Google Doc правки;
- Template2000n/publisher-style render QA после global heading normalization.
