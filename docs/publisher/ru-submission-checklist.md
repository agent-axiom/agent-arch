# Чеклист готовности русской версии к издательству

Status: working gate for Russian publisher submission.

## Verdict scale

- **Ready:** можно отправлять редактору как издательский пакет.
- **Almost ready:** можно показывать доверенному редактору/агенту как предварительный пакет.
- **Not ready:** не отправлять как готовую рукопись; сначала закрыть блокеры.

Current status: **The 2026-07-14 editorial proof is synchronized between the
repository and the working Google Doc. It contains 7 parts, 28 chapters,
7 laboratory exercises, a final project and 54 images. The verified raw Google
Docs proof is 462 Letter pages; page 41 is an intentional recto transition
between Parts I and II. The macro-free Template2000n derivative is 379 Letter
pages with no blank-like pages. Text equality, image completeness, embedded
font registrations, chapter order, cross-references, fail-closed examples and
current tool identifiers are covered by automated checks. The package is ready
for publisher/editor review as a working manuscript. Final submission remains
blocked by author-owned fields, publisher decisions on format and illustrations,
and an independent external proofread after those fields are filled.**

## P0 gates before external submission

- [x] Целевая подача выбрана: Russian publisher package.
- [x] Рабочая Google Doc-рукопись создана и доступна для чтения/записи:
      <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>.
- [x] Полная Google Doc-рукопись создана native import из DOCX:
      <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>.
- [x] Для Russian package sample manifest указывает RU source paths, not `.en.md` paths.
- [x] Есть отдельная assembly map for print manuscript:
      `docs/publisher/ru-manuscript-map.md`.
- [x] Есть source map от договорной структуры к Markdown-источникам:
      `docs/publisher/ru-source-map.md`.
- [x] Есть ledger эволюции рукописи:
      `docs/publisher/ru-manuscript-evolution.md`.
- [x] Есть верхнеуровневая редакционная дорожная карта:
      `docs/publisher/ru-editorial-roadmap.md`.
- [x] Зафиксировано правило синхронизации repository -> Google Doc:
      `docs/publisher/ru-google-doc-workflow.md`.
- [x] Зафиксировано правило Google Doc vs raw DOCX vs Template2000n DOCX:
      `docs/publisher/ru-google-doc-docx-handoff-policy-2026-07-03.md`.
- [x] Publisher-facing packet v0.1 drafted:
      `docs/publisher/ru-publisher-packet-v0.1.md`.
- [x] Publisher-facing packet v0.1 compact block synced to the Google Doc.
- [x] Author/platform note template with fill-in fields added to packet v0.1.
- [x] Author/platform note compact template synced to the Google Doc.
- [x] Default first-packet sample scope fixed as Chapter 1 only.
- [x] Chapter 13 fixed as follow-up technical sample by request.
- [x] Russian cover note draft created:
      `docs/publisher/ru-cover-note-draft.md`.
- [x] Chapter 1 working sample loaded into the Google Doc manuscript.
- [x] Chapter 1 first Russian publisher line edit applied and synced to the Google Doc.
- [x] Терминологическая политика применена к Chapter 1 and source Chapter 13 samples.
- [x] Chapter 1 passed first Russian line edit.
- [x] Source Chapter 13 passed first Russian line edit.
- [x] Introduction and Part I rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-part-i.md`.
- [x] Introduction and Part I rough assembly synced to the Google Doc.
- [x] Part II and Part III rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-part-ii-iii.md`.
- [x] Part II and Part III rough assembly completed in Google Doc.
- [x] Part IV and Part V rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-part-iv-v.md`.
- [x] Part IV and Part V rough assembly completed in Google Doc.
- [x] Part VI and Part VII rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-part-vi-vii.md`.
- [x] Part VI and Part VII rough assembly completed in Google Doc.
- [x] Appendices rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-appendices.md`.
- [x] Appendices rough assembly completed in Google Doc.
- [x] Google Doc contains the full 7-part / 23-chapter structure including
      appendices.
- [x] Google Doc contains full manuscript volume expanded from the Markdown
      source corpus, not only compressed chapter assembly.
- [x] Full source-to-print manuscript Markdown created:
      `docs/publisher/ru-manuscript-full.md`.
- [x] Full manuscript DOCX render smoke QA completed for current Google Docs
      import artifact: 437 rendered pages, no blank/near-blank PNGs detected.
- [x] Introduction and Part I first compression/editorial pass completed in
      local assembly and synced to Google Doc.
- [x] Part II and Part III first compression/editorial pass completed in local
      assembly and synced to Google Doc.
- [x] Part IV and Part V first compression/editorial pass completed in local
      assembly and synced to Google Doc.
- [x] Part VI and Part VII first compression/editorial pass completed in local
      assembly and synced to Google Doc.
- [x] Appendices first compression/editorial pass completed in local assembly
      and synced to Google Doc.
- [x] Текущая web-структура 8/27 сжата в договорную структуру 7/23.
- [x] Book/reference split is explicit: runtime/schema details moved or marked as companion-only in the manuscript.
- [x] High-level roadmap for structural, terminology, cross-reference and
      companion-boundary passes is created.
- [x] Book-readiness audit created after full volume assembly:
      `docs/publisher/ru-book-readiness-audit.md`.
- [x] Introduction and Part I structural pass completed and synced to Google
      Doc.
- [x] Part II and Part III structural pass completed and synced to Google Doc.
- [x] Part IV and Part V structural pass completed and synced to Google Doc.
- [x] Part VI, Part VII and appendices structural pass completed and synced to
      Google Doc.
- [x] First terminology/glossary anchor batch completed for Part VI, Part VII
      and appendices.
- [x] Second terminology anchor batch completed for Introduction and Parts I-V.
- [ ] Book-readiness second pass is complete across introduction, all 23
      chapters and appendices.
- [x] Introduction reader contract is rewritten and synced to the full Google
      Doc manuscript from `docs/publisher/ru-book-ready-introduction.md`.
- [x] Chapter 1 sample chapter is line-edited for book-readiness and synced to
      the full Google Doc manuscript from
      `docs/publisher/ru-book-ready-chapter-1.md`.
- [x] Chapter 2 is rebuilt around the workflow -> agent loop -> coordinator ->
      handoff decision ladder and synced to the full Google Doc manuscript from
      `docs/publisher/ru-book-ready-chapter-2.md`.
- [x] Chapter 3 now has a compact bridge into Part II from
      `docs/publisher/ru-book-ready-chapter-3-bridge.md`.
- [x] Chapter 5 is rewritten as a conceptual identity/session/policy/capability
      chapter and synced to the full Google Doc manuscript from
      `docs/publisher/ru-book-ready-chapter-5.md`.
- [x] Chapter 22 is rewritten as the implementation-focused policy/catalog
      runtime chapter and synced to the full Google Doc manuscript from
      `docs/publisher/ru-book-ready-chapter-22.md`.
- [ ] Overloaded chapters 20 and 21 are compressed/restructured after
      full-volume assembly.
- [x] Chapters 20 and 21 received a first density/bridge pass in the full
      Google Doc and repository manuscript source:
      `docs/publisher/ru-editorial-quality-pass-2026-07-04.md`.
- [ ] Repeated chapter endings are normalized into a compact book rhythm.
- [x] Repeated chapter-ending pattern scan completed and recorded:
      `docs/publisher/ru-editorial-quality-pass-2026-07-04.md`.
- [ ] Running practical case is visibly carried through every part.
- [x] Editor handoff readiness pass completed in the full Google Doc:
      H1 outline cleaned, raw DOCX proof exported, render QA recorded.
- [x] Global heading normalization pass completed for remaining long H2 body
      paragraphs before final publisher-ready DOCX.
- [x] H3/body-style cleanup completed before final publisher-ready DOCX.
- [ ] Author bio / credential framing fields are filled by the author.
- [x] Стилевые файлы БХВ получены и применены или явно отложены.

## P1 gates before serious editor review

- [x] Working/publisher service blocks are separated from manuscript body for
      final delivery.
- [x] First structural editorial pass is complete across all parts.
- [ ] Second book-readiness pass is complete across all parts.
- [x] `case-spine note` and `canonical cases` are removed from Russian reader-facing prose or turned into Russian reader-facing labels.
- [x] Russian headings avoid unnecessary English terms.
- [x] Excessive anglicism pass completed for manuscript/source maps:
      `docs/publisher/ru-editorial-quality-pass-2026-07-04.md`.
- [x] `tools`, `agents`, `rollout`, `runtime`, `review`, `registry`, `inventory`, `assurance`, `retirement`, and `end-of-life` follow the terminology policy.
- [x] Repeated maturity-check endings are intentionally templated rather than accidentally repetitive.
- [x] Dense CLI/runtime details are moved to онлайн-сопровождение or summarized.
- [x] All Mermaid diagrams have print-safe fallback prose or captions.
- [x] Long tables and code blocks are reviewed for PDF/print readability.
- [x] Public companion links are stable.

## P2 gates before final manuscript delivery

- [ ] Full Russian proofread completed after manuscript expansion.
- [x] Cross-references checked after print assembly.
- [x] Glossary matches the terminology policy.
- [x] Bibliography/source catalog is curated for book use rather than web completeness.
- [x] Figure captions are complete for current manuscript scope.
- [x] Code examples have consistent formatting and line length for current manuscript scope.
- [ ] БХВ style package is applied to the final export shape.
- [ ] DOCX/export QA is completed after publisher style application.
- [x] Current raw Google Docs export QA completed for editor handoff proof:
      552 pages, 0 blank-like pages.
- [x] Current raw Google Docs export QA completed after heading normalization:
      504 pages, 0 blank-like pages.
- [x] Current Template2000n proof QA completed after heading normalization:
      315 pages, 0 blank-like pages.
- [x] Current raw Google Docs export QA completed after H3/body-style cleanup:
      499 pages, 0 blank-like pages.
- [x] Current Template2000n proof QA completed after H3/body-style cleanup:
      315 pages, 0 blank-like pages.
- [x] Author/front-matter fields are isolated in Google Doc and local report.
- [x] Current raw editorial-ready proof exported after author/front-matter pass:
      499 pages, 0 blank-like pages.
- [x] Current Template2000n editorial-ready proof created after author/front-matter pass:
      315 pages, 0 blank-like pages.
- [x] Current raw Google Docs export QA completed after layout/style cleanup:
      507 pages, 0 blank-like pages.
- [x] Current Template2000n proof QA completed after layout/style cleanup:
      371 pages, 0 blank-like pages.
- [x] Known page-338 checklist carryover fixed in the current working proof.
- [x] Late-practice heading/body style cleanup completed for the current
      working proof.
- [x] Current raw Google Docs export QA completed after legacy outline cleanup:
      489 pages, 0 blank-like pages.
- [x] Current Template2000n proof QA completed after legacy outline cleanup:
      351 pages, 0 blank-like pages.
- [x] Legacy false outline noise reduced in the current working proof:
      heading paragraphs reduced from 1352 to 1152 without text loss.
- [x] Attached Template2000n.dot style package applied to a fresh Google Docs
      DOCX export through a macro-free DOCX style route.
- [x] Template2000n acceptance gate created:
      `docs/publisher/ru-template2000n-acceptance-gate-2026-07-03.md`.
- [x] Final editorial handoff plan created:
      `docs/publisher/ru-final-editorial-handoff-plan-2026-07-03.md`.
- [x] Final handoff implementation pass recorded:
      `docs/publisher/ru-final-handoff-implementation-pass-2026-07-03.md`.
- [x] Author editorial fill packet created for current proof:
      `docs/publisher/ru-author-editorial-fill-packet-2026-07-03.md`.
- [x] Current raw Google Docs export QA completed after Template2000n official
      style pass: 489 pages, 0 blank-like pages.
- [x] Current Template2000n official-style proof QA completed:
      357 pages, 0 blank-like pages.
- [x] Final pre-author raw Google Docs export QA completed:
      489 pages, 0 blank-like pages.
- [x] Final pre-author Template2000n proof QA completed:
      361 pages, 0 blank-like pages.
- [x] Final pre-author export pass recorded:
      `docs/publisher/ru-final-preauthor-export-pass-2026-07-03.md`.
- [x] Pre-author publisher packet created:
      `docs/publisher/ru-preauthor-publisher-submission-packet-2026-07-03.md`.
- [x] 2026-07-04 editorial quality pass recorded with Google Doc readback:
      `docs/publisher/ru-editorial-quality-pass-2026-07-04.md`.
- [x] Next 100 editorial quality goals created:
      `docs/publisher/ru-editorial-100-editorial-quality-iterations-2026-07-04.md`.
- [ ] Publisher/editor acceptance of the macro-free Template2000n style route
      is confirmed.
- [x] Clean editor handoff packet created:
      `docs/publisher/ru-clean-editor-handoff-packet-2026-06-28.md`.
- [x] Author query packet created:
      `docs/publisher/ru-author-query-packet-2026-06-28.md`.
- [x] Editor-facing brief created:
      `docs/publisher/ru-editor-facing-brief-2026-06-28.md`.
- [x] Companion readiness pass created:
      `docs/publisher/ru-companion-readiness-pass-2026-06-28.md`.
- [x] Companion templates/checklist promoted to release-candidate headers.
- [x] Companion example artifacts generated for trace, failed trace, session
      and eval dataset review.
- [x] Print-facing appendix/chapter routes link to companion examples and
      trace/eval artifacts for the support-ticket case.
- [x] Final fact-check backlog created:
      `docs/publisher/ru-final-fact-check-backlog-2026-06-28.md`.
- [x] Source verification packet created:
      `docs/publisher/ru-source-verification-packet-2026-06-28.md`.
- [x] Source verification batch records created:
      `docs/publisher/ru-source-verification-records-2026-06-28.md`.
- [x] Live source verification action packet created:
      `docs/publisher/ru-live-source-verification-actions-2026-06-29.md`.
- [x] Representative P0 live source verification pass completed:
      `docs/publisher/ru-live-source-verification-pass-2026-06-29.md`.
- [x] Full source catalog URL availability pass completed:
      `docs/publisher/ru-full-source-verification-pass-2026-06-29.md`.
- [x] Source URL availability evidence TSV generated:
      `docs/publisher/ru-source-url-live-check-2026-06-29.tsv`.
- [x] Targeted source follow-up pass completed:
      `docs/publisher/ru-source-follow-up-pass-2026-06-30.md`.
- [x] Targeted source follow-up evidence TSV generated:
      `docs/publisher/ru-source-follow-up-live-check-2026-06-30.tsv`.
- [x] OpenReview primary-evidence blocker closed by demotion:
      `docs/publisher/ru-openreview-demotion-pass-2026-06-30.md`.
- [x] Google Doc companion/source-status sync pass completed:
      `docs/publisher/ru-google-doc-companion-source-sync-pass-2026-06-29.md`.
- [x] Author-owned final input blockers isolated:
      `docs/publisher/ru-author-owned-final-inputs-2026-06-29.md`.
- [x] Author intake ready pass recorded:
      `docs/publisher/ru-author-intake-ready-pass-2026-06-29.md`.
- [x] Author input closure packet prepared:
      `docs/publisher/ru-author-input-closure-packet-2026-06-30.md`.
- [x] Pre-author finalization pass recorded:
      `docs/publisher/ru-pre-author-finalization-pass-2026-07-01.md`.
- [x] Final placeholder/source readiness pass recorded:
      `docs/publisher/ru-final-placeholder-source-readiness-pass-2026-07-01.md`.
- [x] Pre-author export gate recorded:
      `docs/publisher/ru-pre-author-export-gate-2026-07-01.md`.
- [x] Pre-author final export readiness recorded:
      `docs/publisher/ru-pre-author-final-export-readiness-2026-06-29.md`.
- [x] Final export readiness after source pass recorded:
      `docs/publisher/ru-final-export-readiness-after-source-pass-2026-06-29.md`.
- [x] Pre-final export readiness after targeted source follow-up recorded:
      `docs/publisher/ru-pre-final-export-readiness-after-follow-up-2026-06-30.md`.
- [x] Final editor packet skeleton prepared:
      `docs/publisher/ru-final-editor-packet-skeleton-2026-06-30.md`.
- [x] Sendable editor packet state recorded:
      `docs/publisher/ru-sendable-editor-packet-state-2026-06-29.md`.
- [x] External packet readiness pass recorded:
      `docs/publisher/ru-external-packet-readiness-pass-2026-06-29.md`.
- [x] Mechanical placeholder/link scan report created:
      `docs/publisher/ru-mechanical-scan-report-2026-06-29.md`.
- [x] Final external packet outline created:
      `docs/publisher/ru-final-external-packet-outline-2026-06-29.md`.
- [x] Editor comment intake workflow created:
      `docs/publisher/ru-editor-comment-intake-workflow-2026-06-28.md`.
- [x] Final placeholder/link scan workflow created:
      `docs/publisher/ru-final-placeholder-link-scan-workflow-2026-06-28.md`.
- [x] Post-author final export workflow created:
      `docs/publisher/ru-post-author-final-export-workflow-2026-06-28.md`.
- [x] Next 100 external-packet readiness goals created:
      `docs/publisher/ru-editorial-100-external-packet-iterations-2026-06-29.md`.
- [x] Next 100 source/author/finalization goals created:
      `docs/publisher/ru-editorial-100-source-author-finalization-iterations-2026-06-29.md`.
- [x] Next 100 final editorial goals created:
      `docs/publisher/ru-editorial-100-final-editorial-iterations-2026-06-29.md`.
- [x] Next 100 author/source/export goals created:
      `docs/publisher/ru-editorial-100-author-source-export-iterations-2026-06-30.md`.
- [x] Next 100 final packet goals created:
      `docs/publisher/ru-editorial-100-final-packet-iterations-2026-06-30.md`.
- [x] Next 100 pre-author-to-final goals created:
      `docs/publisher/ru-editorial-100-pre-author-finalization-iterations-2026-07-01.md`.
- [x] Next 100 final handoff goals created:
      `docs/publisher/ru-editorial-100-final-handoff-iterations-2026-07-03.md`.
- [x] Next 100 post-preauthor goals created:
      `docs/publisher/ru-editorial-100-post-preauthor-iterations-2026-07-03.md`.
- [x] Next 100 editorial quality goals created:
      `docs/publisher/ru-editorial-100-editorial-quality-iterations-2026-07-04.md`.
- [x] Next 100 quality-sync/export goals created:
      `docs/publisher/ru-editorial-100-quality-sync-export-iterations-2026-07-04.md`.
- [x] Google Doc quality-sync terminology pass recorded:
      `docs/publisher/ru-google-doc-quality-sync-pass-2026-07-04.md`.
- [x] Template2000n quality-sync proof rendered: 357 pages, 0 blank-like pages.
- [x] OpenReview metadata is manually verified or those records are demoted
      before final publisher submission.
- [x] Fresh post-terminology raw DOCX export is saved from the updated Google
      Doc.
- [x] Template2000n post-terminology proof rendered: 359 pages, 0 blank-like
      pages.
- [x] Post-terminology render QA report created:
      `docs/publisher/ru-google-doc-post-terminology-export-pass-2026-07-04.render-qa.json`.
- [x] Current 2026-07-14 Google Docs proof exported: 462 pages, 28 chapters,
      54 images; page 41 is an intentional recto transition.
- [x] Current 2026-07-14 Template2000n proof rendered: 379 pages, 0 blank-like
      pages, no clipped page content.
- [x] Template2000n semantic styles, image alt text and print-safe PNG media
      verified for the current editorial proof.
- [x] Current semantic source pass over the electronic book additions is
      synchronized to the repository manuscript and Google Doc.
- [x] Font audit completed: Template2000n requests Times New Roman and Courier
      New; the headless LibreOffice proof uses metric-compatible Liberation
      substitutes, while six embedded Roboto Mono/Noto symbol registrations are
      preserved in both DOCX files.
- [ ] Independent external proofread is completed after the export shape is stable.
- [x] Final `mkdocs build --strict` passes.
- [x] Final docs surface tests pass.
- [x] `git diff --check` is clean.

## Recommended first external packet

Include:

1. One-page Russian positioning memo.
2. Актуальная структура 7 частей / 28 глав и пояснение расхождения с исходным
   планом-проспектом на 23 главы.
3. Source map from repository Markdown to publisher manuscript chapters.
4. Cover note draft from `docs/publisher/ru-cover-note-draft.md`.
5. Chapter 1 sample from `docs/book/part-i/chapter-1.md`.
6. Chapter 13 sample from `docs/book/part-v/chapter-13.md` only if the editor asks for technical depth.
7. Companion-site description.
8. Author bio and platform note.
9. Status note: public web manuscript exists; full publisher manuscript is
   updated in Google Doc; pre-author Template2000n and export QA are complete;
   author fields, post-author final export and external proofread remain open.

Before sending:

- do not use the external cover note until the author fields are filled;
- fill every `[заполнить]` field in `docs/publisher/ru-publisher-packet-v0.1.md`;
- replace the cover-note author placeholder with the final short author line;
- keep Chapter 13 out of the first packet unless the editor explicitly asks for technical depth;
- verify Google Doc access for the editor.

Working packet source:

- `docs/publisher/ru-publisher-packet-v0.1.md`
- `docs/publisher/ru-cover-note-draft.md`

Do not include:

- full schema appendices;
- full CLI reference;
- generated site files;
- internal editorial backlog;
- raw source catalog unless requested.
