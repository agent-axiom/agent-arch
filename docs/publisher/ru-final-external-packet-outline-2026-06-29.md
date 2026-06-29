# Final external packet outline

Date: 2026-06-29.

Status: outline for final editor/publisher delivery after author-owned fields,
live source verification and final proof export are closed. Do not treat this
as a sent packet yet.

## Packet goal

Give an external editor or publisher a clean manuscript package without the
internal iteration trail. The packet should show:

- one authoritative manuscript source;
- current DOCX proofs;
- what is ready for editorial review;
- which fields were author-owned and how they were closed;
- how source freshness and companion boundaries were checked.

## Required before sending

1. Fill or explicitly omit all author-owned fields:
   `Об авторе`, public links, role, verified experience, public projects,
   acknowledgements, title/subtitle/cover copy, companion URL and AI-use/legal
   wording.
2. Run live source verification using
   `docs/publisher/ru-live-source-verification-actions-2026-06-29.md`.
3. Update `docs/appendix/sources.md` with the current last-checked date only
   after live verification.
4. Update or remove stale review-date banners from print-facing chapters.
5. Re-export raw Google Docs DOCX and Template2000n DOCX after the author
   fields are filled.
6. Re-run render QA and record page counts and blank-like page checks.

## Send this

| Item | Current source | Send when |
| --- | --- | --- |
| Full Google Doc manuscript | <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI> | Always, after access check. |
| Template2000n DOCX proof | `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-ready-2026-06-28.docx` | Replace with post-author export before final publisher submission. |
| Raw Google Docs DOCX fallback | `docs/publisher/artifacts/agent-arch-ru-editorial-ready-2026-06-28.docx` | Replace with post-author export before final publisher submission. |
| Editor-facing brief | `docs/publisher/ru-editor-facing-brief-2026-06-28.md` | Update status if author fields are closed. |
| Clean handoff packet | `docs/publisher/ru-clean-editor-handoff-packet-2026-06-28.md` | Keep as process/status summary. |
| Author fields status | `docs/publisher/ru-author-open-fields-2026-06-28.md` and `docs/publisher/ru-author-query-packet-2026-06-28.md` | Send only if fields remain open; otherwise send a short closure note. |
| Mechanical scan report | `docs/publisher/ru-mechanical-scan-report-2026-06-29.md` | Send as QA evidence if editor asks how placeholders were controlled. |
| Source verification record | `docs/publisher/ru-source-verification-records-2026-06-28.md` | Send after records are filled. |
| Companion readiness note | `docs/publisher/ru-companion-readiness-pass-2026-06-28.md` | Send when public companion URL/version are known. |
| Render QA report | `docs/publisher/ru-publisher-style-pass-2026-06-28.render-qa.json` plus human summary | Replace with post-author render QA before final delivery. |

## Do not send by default

- Internal `ru-editorial-100-*.md` iteration logs.
- Rough assembly files for intermediate Google Doc construction.
- The old compressed/staging Google Doc as the manuscript source.
- Raw source maps unless the editor asks for traceability.
- Binary/generated artifacts that are not the selected final DOCX proofs.
- Unfilled publisher packet drafts with `[заполнить]` still present.

## Cover note checklist

Before sending, the cover note must state:

- this is the full Russian manuscript, not a compressed sample;
- current page counts for raw DOCX and Template2000n proof;
- the intended review type: substantive/structural edit first, not final
  typesetting;
- whether author-owned fields are closed or still listed separately;
- whether source verification is complete and on what date;
- where the online companion will live;
- what feedback is requested from the editor.

## Current state

As of 2026-06-29, the manuscript is suitable for trusted editorial review as a
clean working package. It is not yet a final publisher submission because
author-owned fields, live source verification and post-author final export QA
remain open.
