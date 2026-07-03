# Чеклист готовности русской версии к издательству

Status: working gate for Russian publisher submission.

## Verdict scale

- **Ready:** можно отправлять редактору как издательский пакет.
- **Almost ready:** можно показывать доверенному редактору/агенту как предварительный пакет.
- **Not ready:** не отправлять как готовую рукопись; сначала закрыть блокеры.

Current status: **Full manuscript volume assembled and imported to Google Docs.
H2/H3 body-style cleanup is complete, author/front-matter fields are isolated,
Google Doc companion/source-status wording is synchronized, full source URL
availability pass evidence is recorded, the 2026-06-30 targeted source
follow-up has resolved the actionable blocked URL cleanup, and OpenReview has
been demoted out of primary evidence. The current proof pair is the 2026-07-03
raw Google Docs export at 489 pages and Template2000n official-style derivative
at 357 pages, both with 0 blank-like pages. The current handoff layer records a
Template2000n acceptance gate, author fill packet, Google Doc/DOCX policy and
final editorial handoff plan. It can be handed to a trusted editor as a clean
working manuscript and style proof candidate, but do not send as final
publisher submission yet: the manuscript still needs author-owned facts, final
companion metadata, publisher/editor acceptance of the style route, post-author
export QA and external proofread.**

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
- [ ] Repeated chapter endings are normalized into a compact book rhythm.
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
- [x] `tools`, `agents`, `rollout`, `runtime`, `review`, `registry`, `inventory`, `assurance`, `retirement`, and `end-of-life` follow the terminology policy.
- [x] Repeated maturity-check endings are intentionally templated rather than accidentally repetitive.
- [x] Dense CLI/runtime details are moved to online companion or summarized.
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
- [x] OpenReview metadata is manually verified or those records are demoted
      before final publisher submission.
- [ ] Final semantic source pass over fast-moving platform claims is complete
      after author/source Google Doc sync.
- [ ] Independent external proofread is completed after the export shape is stable.
- [x] Final `mkdocs build --strict` passes.
- [x] Final docs surface tests pass.
- [x] `git diff --check` is clean.

## Recommended first external packet

Include:

1. One-page Russian positioning memo.
2. Договорная структура 7 частей / 23 главы.
3. Source map from repository Markdown to publisher manuscript chapters.
4. Cover note draft from `docs/publisher/ru-cover-note-draft.md`.
5. Chapter 1 sample from `docs/book/part-i/chapter-1.md`.
6. Chapter 13 sample from `docs/book/part-v/chapter-13.md` only if the editor asks for technical depth.
7. Companion-site description.
8. Author bio and platform note.
9. Status note: public web manuscript exists; full publisher manuscript is now
   assembled in Google Doc and remains blocked by author fields, final
   publisher styles, export QA after styles and final external proofread.

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
