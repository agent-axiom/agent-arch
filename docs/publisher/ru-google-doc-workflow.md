# Workflow синхронизации русской рукописи с Google Docs

Status: рабочее правило для издательской подготовки.

Google Docs:

- Full manuscript: `Архитектура безопасных ИИ-агентов — полная рукопись`
- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Book-readiness editorial map:
  `Архитектура безопасных ИИ-агентов — редакционная карта готовой книги`
- <https://docs.google.com/document/d/1XoU_nWZkpKGU7SxZ0pgmE_dfcNNggQokZsbzind7kXc>
- Current publisher manuscript: `Архитектура безопасных ИИ-агентов`
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

На 2026-07-05 выполнен visual/edit pass, который добавляет визуальный слой и
закрывает текущий свежий export/render checkpoint:

- final known Google Doc revision:
  `ALtnJHxx8GXfQQfPMrGfG7STCXtscwWkhPzWpj1AJa-vee0UADj3vnwYNiZkKG2wGfd2Xkdsizblmxq8xb8YyumfJxKOb8ujAWDn1wNGphY`;
- fresh raw DOCX export:
  `docs/publisher/artifacts/agent-arch-ru-google-doc-visual-edit-2026-07-05.docx`;
- Template2000n derivative:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-visual-edit-2026-07-05.docx`;
- render QA: raw 501 pages, Template2000n 366 pages, 0 blank-like pages in
  both proofs;
- visual layer: 12 embedded PNG diagrams, with captions and alt text;
- report:
  `docs/publisher/ru-google-doc-visual-edit-pass-2026-07-05.md`;
- next 100 visual/edit goals:
  `docs/publisher/ru-editorial-100-visual-edit-iterations-2026-07-05.md`.

New limitation: the current proof is stronger for editor discussion because it
has visualizations and companion compression, but final submission still
requires author-owned fields, public companion metadata, external proofread and
a repeat post-author export/render cycle.

На 2026-07-05 выполнен dedup/source sync pass после проверки репозитория и
рукописи:

- final known Google Doc revision:
  `ALtnJHxPfoLV8Xo2Bi9Tjzkn9e4ANu0le4z32bKytX-eSe9EQsghl9yz1iYpWetbvzg-cctjMEpJM-iOrrJ7nePO-B5PQO3FAkM1b7tKqJ0`;
- Google Doc дополнен двумя блоками: Chapter 15 control evaluations /
  automated adversarial testing and Chapter 20 agentic goal misalignment /
  insider-style risk;
- local full Markdown assembly reduced from 92 to 0 exact duplicate paragraph
  groups with 35+ words;
- integrity follow-up corrected stale chapter cross-references and removed
  visible mixed suffix forms from the current DOCX/Google Doc proof;
- reader-recommendability follow-up added production scenes, continuity
  bridges, maturity bridges and chapter takeaways;
- three-reader-profiles follow-up added explicit architect, manager/CTO and
  developer reading routes plus part-level outcomes and chapter forwarding
  hooks;
- page-turner/workshop follow-up added a through-line block, seven part-level
  team workshop blocks and 23 concrete next actions after chapters;
- case/thesis follow-up made the support-agent storyline explicit, added seven
  part-level case episodes and 23 short phrases for readers to quote or
  forward;
- skeptic-response follow-up added a constructive objection/answer layer:
  `С кем спорит эта книга`, seven `Типичное возражение` blocks and 23
  `Что ответить скептику` chapter responses;
- mindset-shift follow-up added the reader-transformation layer:
  `Как изменится ваше мышление после книги`, seven
  `До этой части / После этой части` blocks and 23 `Смена мышления`
  chapter responses;
- narrative-flow follow-up added 23 natural chapter opening paragraphs and 23
  natural closing bridges after `Что сделать после чтения`, without adding a
  new repeated rubric;
- reader-delight polish follow-up added 13 short natural prose paragraphs:
  one introduction recommendation-language paragraph, seven part-level
  conflict paragraphs and five selected chapter `aha` pivots, without adding a
  new repeated rubric;
- raw DOCX uploaded back to the same Drive file:
  `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`;
- Template2000n derivative:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`;
- render QA: raw 529 pages, Template2000n 384 pages, 0 blank-like pages in
  both proofs;
- report:
  `docs/publisher/ru-google-doc-dedup-source-sync-pass-2026-07-05.md`.
- latest follow-up report:
  `docs/publisher/ru-reader-delight-polish-pass-2026-07-06.md`.
- latest 100-goal ledger:
  `docs/publisher/ru-editorial-100-reader-delight-polish-iterations-2026-07-06.md`.

New limitation: this checkpoint improves source coverage and duplicate hygiene,
but it is still a working manuscript proof. Final submission still requires
author-owned fields, public companion metadata, external proofread and a repeat
post-author export/render cycle.

На 2026-07-20 выполнена развивающая редактура с адресной синхронизацией
существующего Google Doc:

- целевой файл и вкладка `t.0` подтверждены доверенным чтением до записи;
- пакет из 782 операций применён атомарно с контролем исходной ревизии;
- 172 из 172 изменённых целевых абзацев подтверждены итоговым выравниванием;
- сохранены 28 глав, 8 лабораторных работ, 39 именованных шагов и 56
  встроенных изображений;
- у трёх итоговых абзацев лабораторий снят случайно унаследованный
  `pageBreakBefore`;
- финальная ревизия Google Doc:
  `ALtnJHyvucObEw3NQ_K_IpvncJvfdH6V1pUAx_E8-DwKKk_frxdhOOafSA4S2E-P104DRv5E-g_mRx8IWg4cNo9ir3wEI-YUhiexXHuXvvM`;
- свежий DOCX-экспорт:
  `docs/publisher/artifacts/agent-arch-ru-google-doc-synced-developmental-edit-2026-07-20.docx`;
- локальная PDF-проверка экспорта: 488 страниц, без пустых технических страниц,
  обрезки и наложений;
- отчёт:
  `docs/publisher/ru-developmental-editing-pass-2026-07-20.md`.

Прямой нативный PDF-экспорт Google вернул HTTP 403 для этого крупного
документа, поэтому контрольная PDF получена из свежего DOCX-экспорта той же
ревизии. Это ограничение транспорта экспорта, а не рукописи.

На 2026-07-22 выполнен проход готовности к издательской передаче:

- канонический Markdown и обе локальные издательские производные пересобраны
  детерминированно;
- во введении восстановлена учебная последовательность, добавлена
  самопроверка, исправлены ссылки на главы и терминология;
- в главе 21 добавлена матрица поверхностей доверия и доказательств выпуска;
- в Google Doc исправлены пять повреждённых склеек, снят стиль заголовка с 40
  пустых абзацев и удалены пустые абзацы перед главами и в конце документа;
- итоговая доверенная проверка сохранила 56 встроенных изображений и не нашла
  защищённых элементов, требующих специального маршрута редактирования;
- финальная ревизия Google Doc:
  `AIroW34T21uKswdfPb9meuhJEG_xfKqHE4_Whg2C4JbnXWmjD51Iz_ORM6K9ZIwXmVGreawtWYjW_b5rP-aApsKSwzTPfFmi2xBrRxQ4Lhw`;
- свежий DOCX-экспорт:
  `docs/publisher/artifacts/agent-arch-ru-google-doc-live-submission-readiness-2026-07-22.docx`;
- локальная PDF-проверка свежего экспорта: 485 страниц Letter, пустых
  технических страниц нет;
- Google-ориентированная производная: 436 страниц, производная
  `Template2000n`: 317 страниц, пустых технических страниц нет;
- отчёт: `docs/publisher/ru-submission-readiness-pass-2026-07-22.md`.

На 2026-07-23 выполнена финальная читательская редактура:

- в каноническом Markdown исправлены остаточные логические склейки,
  грамматические несогласования и избыточные англицизмы; термины предметной
  области сохранены там, где русская замена была бы менее точной;
- редактура закреплена детерминированной функцией сборщика и 89
  регрессионными проверками;
- пакет из 259 содержательных операций применён к существующему Google Doc
  атомарно с контролем исходной ревизии; все 107 целевых фрагментов
  подтверждены доверенным чтением;
- отдельным пакетом нормализованы стили 123 изменённых абзацев и восстановлены
  полужирные, курсивные и моноширинные фрагменты;
- для шкалы готовности включено удержание с последующим абзацем, поэтому все
  пять уровней остаются на одной странице;
- сохранены 56 встроенных изображений, 10 таблиц и структура из 8 частей,
  28 глав, 8 лабораторных работ и итогового проекта;
- финальная ревизия Google Doc:
  `AIroW36L1-ayGgTHn0N-t7AALAAwVm90AlugNlc48mvIZsC_sZUl1i72cm80Yh1OhSHNaLa1_145bK-Nxcc2zyVAzkgiPpK7fS5N1p8lNyI`;
- свежий DOCX-экспорт Google Doc:
  `docs/publisher/artifacts/agent-arch-ru-google-doc-live-final-reader-copyedit-2026-07-23.docx`;
- локальная PDF-проверка свежего экспорта: 493 страницы, пустых технических
  страниц нет;
- Google-ориентированная производная: 448 страниц, производная
  `Template2000n`: 324 страницы, пустых технических страниц нет;
- отчёт: `docs/publisher/ru-final-reader-copyedit-2026-07-23.md`.

На 2026-07-27 выполнена редакционная полировка по стандартам сильной
технической литературы:

- убраны служебные редакторские пометы, ослаблены повторяющиеся вводные
  формулы и уточнено распределение материала между главами 17–19;
- глава 23 открывается сценой вывода системы из эксплуатации, а материал о
  гарантиях и заверении больше не дублирует соседние главы;
- обновлены локальные ссылки на исполняемые примеры, список источников разделён
  на цитируемые работы и дополнительное чтение;
- сформированы предметный указатель из 64 терминов, карта результатов обучения
  для 28 глав и пакет внешней технической рецензии;
- 486 содержательных и 640 структурно-стилевых операций применены к
  существующему Google Doc с контролем ревизии; 157 изменённых абзацев и 105
  внешних ссылок подтверждены итоговым чтением;
- сохранены 56 изображений, 10 таблиц, 28 глав, 8 лабораторных работ и 30
  смысловых разрывов страниц;
- финальная ревизия Google Doc:
  `AIroW36zOf2ZNRM-XL1tdd9LEuHsKy-qYN8botKOL9dlIezh0tQp_2J2mIN70uICM8a0nxtHH5ARYrY2_3iLbsgS8CJUm0ayFLnmCVV1Tlc`;
- свежий DOCX-экспорт Google Doc при локальном рендеринге занимает 489
  страниц, нативный PDF Google Docs — 457 страниц; оба варианта проверены
  постранично, пустых технических страниц, обрезки, наложений и потерянных
  рисунков не обнаружено;
- Google-ориентированная производная занимает 446 страниц, производная
  `Template2000n` — 321 страницу;
- все шрифты нативного PDF встроены; локальные издательские DOCX проходят
  аудит доступности без замечаний высокого и среднего уровня;
- Google Docs не сохраняет альтернативные описания иллюстраций в DOCX-экспорте.
  Для однократного восстановления описаний в самом документе подготовлен
  `docs/publisher/tools/set_google_doc_image_alt_text.gs`; его первый запуск
  требует интерактивного подтверждения разрешений Google;
- отчёт: `docs/publisher/ru-technical-book-polish-2026-07-27.md`.

На 2026-07-29 выполнена синхронизация с актуальной онлайн-книгой и эталонной
средой исполнения:

- целевой файл и вкладка `t.0` подтверждены доверенным чтением до записи;
- крупное обновление применено пакетами с контролем исходной ревизии;
- все 8820 целевых непустых абзацев найдены в итоговом живом документе;
- 56 дополнительных абзацев соответствуют изображениям, пропущенных целевых
  абзацев нет;
- сохранены 56 встроенных объектов, 10 таблиц и структура из 8 частей,
  28 глав, 8 лабораторных работ и итогового проекта;
- финальная ревизия Google Doc:
  `AIroW37NwVSClQSSYb85bVaTYYACE8Aqb6aH6XOkFCe1A1H14ur34HHhJRFMT2ZzDBGtc3w0uyZb4VMrOhKLxXrqHcIcnHvzC766M4EUyEM`;
- Google-ориентированная производная занимает 453 страницы, производная
  `Template2000n` — 327 страниц;
- постраничный, геометрический, визуальный, шрифтовой и доступностный контроль
  обеих производных пройден;
- отчёт: `docs/publisher/ru-online-manuscript-sync-2026-07-29.md`.

На 2026-08-01 выполнен редакционный проход и актуализация MCP:

- 36 абзацных изменений применены к существующему файлу с контролем исходной
  ревизии;
- аналитическая рубрика итогового проекта добавлена как одиннадцатая нативная
  таблица;
- сохранены 56 встроенных объектов, структура частей, глав и лабораторных
  работ;
- финальная ревизия Google Doc:
  `AIroW35prHNueHFHV7x6PXl80jsvBh8iIQaxj34qE3kzRDNQtyxCDYC-3_kE8gnZ-W_JynXfSDaZNTub8fcjw6hz0RHJcTHP2SH19n-5KTY`;
- Google-ориентированная производная занимает 456 страниц, производная
  `Template2000n` — 330 страниц;
- отчёт: `docs/publisher/ru-editorial-pass-2026-08-01.md`.

На 2026-08-01 выполнен читательский проход и адресная синхронизация:

- во введение добавлен единый маршрут по задаче, в приложение 2 — навигатор
  по симптому и каталог повторно используемых решений;
- маршруты восьми частей, открытия глав 5, 11 и 26, развязка главы 28 и
  пояснения рядом с 13 схемами приведены к единой причинной линии;
- лабораторные работы получили общий цикл обучения и исполняемый сборщик
  накопительного манифеста доказательств;
- 61 адресный фрагмент применён к существующему Google Doc атомарным пакетом
  из 591 нативной операции с контролем исходной ревизии;
- итоговое чтение подтвердило 8 935 из 8 935 целевых непустых абзацев;
- сохранены вкладка `t.0`, 56 встроенных объектов и 11 таблиц;
- финальная ревизия Google Doc:
  `AIroW37DrV8dNIYvUEV4d5pOla46Wwq6WopW3RWy18Hy0wJwUNzmMRpRfxpU-LXjQBCZv9zKOxq82sIury9MhmTP3x55NmDU2pjFkh8ELnk`;
- свежий DOCX-экспорт Google Doc:
  `docs/publisher/artifacts/agent-arch-ru-google-doc-live-reader-experience-2026-08-01.docx`;
- локальная PDF-проверка свежего экспорта: 506 страниц Letter, пустых
  технических страниц, обрезки и наложений нет;
- Google-ориентированная производная занимает 481 страницу, производная
  `Template2000n` — 355 страниц;
- отчёт: `docs/publisher/ru-reader-experience-pass-2026-08-01.md`;
- манифест выпуска:
  `docs/publisher/ru-reader-experience-pass-2026-08-01.manifest.json`.

На 2026-08-03 выполнен финальный проход качества и синхронизация практического
маршрута:

- все 8 943 целевых непустых абзаца подтверждены в существующем Google Doc;
- сохранены 56 встроенных изображений, а число нативных таблиц доведено до 12;
- нативный макет Google Docs содержит 489 страниц;
- практические команды закреплены на коммите
  `6bc14de644039c7fea8ef5c521e4b499a7b42982` и проверены в чистом клоне;
- финальная ревизия Google Doc:
  `AIroW34LHT1P5xt9PZ71GfKc2rxmlgPfs36cI6Qc3sv9RBCO-4uYU1KRCJ4_KnNuyPqYqT9e2IPfyGch4pMOjQ91N7Zh2qEg3ttUiUxhUCk`;
- Google-ориентированная производная занимает 478 страниц, производная
  `Template2000n` — 355 страниц; пустых технических страниц нет;
- отчёт: `docs/publisher/ru-final-quality-pass-2026-08-03.md`.

Позднее 2026-08-03 выполнена структурная редактура плотных глав:

- главы 5, 11, 15, 18, 24 и 26 получили однозначные зоны ответственности;
- повторные определения заменены короткими переходами, а автономные
  псевдозаголовки сведены с 225 до 34;
- источники разделены на отдельные абзацы с сохранением внешних гиперссылок;
- 305 адресных изменений применены 11 пакетами из 2 943 операций;
- обратное чтение подтвердило все 8 844 целевых абзаца в правильном порядке;
- сохранены 56 встроенных изображений и 12 таблиц;
- итоговая ревизия Google Doc:
  `AIroW34BIqLlxqyR7lQFvoH2tr9RC3xMQbLeVUbowLhnbIiLXZZEPOWAyWjM_VBNon89r55HZiEeX_Dg5zUlVSRf22nuw0gtqO3tWwDH9MY`;
- Google-ориентированная производная занимает 465 страниц, производная
  `Template2000n` - 347 страниц; пустых технических страниц нет;
- отчёт: `docs/publisher/ru-editorial-structure-pass-2026-08-03.md`.

На 2026-08-14 выполнен проход готовности к публикации:

- все 8 755 целевых непустых абзацев подтверждены в существующем Google Doc;
- сохранены 12 нативных таблиц, число встроенных изображений увеличено с 56
  до 57 за счёт печатного QR-кода Online Companion;
- 487 текстовых и стилевых операций применены атомарно, QR-код добавлен тремя
  операциями, закреплённая ревизия практикума заменена в двух местах;
- практический маршрут закреплён на коммите
  `ecc5aa3cbb48eff00514a24575c64b6e68e3ffe4`;
- проект Apps Script обновлён и успешно перенёс 57 уникальных заголовков и
  альтернативных описаний изображений; обратное чтение не выявило пропусков;
- итоговая ревизия Google Doc:
  `AIroW34bwyJcxIARZcLNTlYvMm8m2v70FpG6aA-cyJlxHLxA1r1QPtVLf022orIET3BzYCup93kq87fFR2oGM8cDHVJWh7VD6duLxK54QE8`;
- Google-ориентированная производная занимает 465 страниц, производная
  `Template2000n` - 345 страниц; пустых технических страниц нет;
- отчёт: `docs/publisher/ru-publication-readiness-pass-2026-08-14.md`.

На 2026-08-17 выполнен редакционный проход по стандартам технической
литературы:

- 13 адресных изменений перенесены в существующий Google Doc атомарным
  пакетом из 124 операций с контролем ревизии;
- обратное чтение подтвердило 8 760 из 8 760 целевых абзацев; 57 отличий
  относятся только к позициям встроенных изображений;
- сохранены вкладка `t.0`, 12 нативных таблиц, структура заголовков и списков,
  57 изображений, их заголовки и альтернативные описания;
- итоговая ревизия Google Doc:
  `AIroW35kpIPbUF0HE8OC54JeYCAfxF-YUU9qGlcqFSTUWy-rvWyF6mtI5B2JszBX1Fr2WVXApiCB9L1QHutrQA8wyY6Xi4ROPqUx3JEjVx8`;
- Google-ориентированная производная занимает 466 страниц, производная
  `Template2000n` - 345 страниц; пустых технических страниц нет;
- отчёт: `docs/publisher/ru-technical-book-polish-pass-2026-08-17.md`.

Альтернативные описания 57 изображений присутствуют в локальных издательских
DOCX и нативном Google Doc. Воспроизводимый сценарий переноса хранится в
`docs/publisher/tools/set_google_doc_image_alt_text.gs`.

Число страниц относится к локальному рендерингу LibreOffice. Нативная
пагинация Google Docs может отличаться, поэтому целостность синхронизации
проверяется последовательностью абзацев, таблицами и встроенными объектами, а
не совпадением числа страниц.

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
