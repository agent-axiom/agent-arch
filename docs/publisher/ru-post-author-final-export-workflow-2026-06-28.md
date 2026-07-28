# Post-author final export workflow

Date: 2026-06-28.

Status: ready-to-run workflow after author-owned fields are filled.

2026-07-03 update: the current style baseline is the Template2000n
official-style proof created from the attached `Template2000n.dot`. Use the
acceptance gate before final submission:

- `docs/publisher/ru-template2000n-acceptance-gate-2026-07-03.md`
- `docs/publisher/artifacts/agent-arch-ru-template2000n-official-style-pass-2026-07-03.docx`

## Preconditions

Do not run this as final submission until all are true:

- publisher/editor accepts the Template2000n macro-free style route or provides
  a replacement style route;
- author query packet is filled;
- short and long author bio are approved;
- title, subtitle and cover copy are approved;
- public companion URL, release version and errata route are approved;
- AI tooling disclosure is approved;
- legal/compliance disclaimer is approved;
- real/composite case policy is approved;
- acknowledgements are approved or removed;
- final publisher metadata is supplied or intentionally blank.

## Step 1. Update Google Doc front matter

Target document:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Replace the author-owned placeholder block under `Об авторе` with final text.

Rules:

- do not change chapter body text during this step;
- keep author bio, disclosure, disclaimer and companion metadata in front
  matter;
- preserve the current 7-part / 23-chapter manuscript structure;
- record the Google Doc revision after update.

## Step 2. Backport author/front-matter data to repository

Update:

- `docs/publisher/ru-author-open-fields-2026-06-28.md`
- `docs/publisher/ru-author-query-packet-2026-06-28.md`
- `docs/publisher/ru-clean-editor-handoff-packet-2026-06-28.md`
- `docs/publisher/ru-cover-note-draft.md`
- `docs/publisher/ru-submission-checklist.md`

If the Google Doc edit changes semantic manuscript prose, backport the change
to the relevant Markdown source before export.

## Step 3. Export raw Google Docs DOCX

Export the updated Google Doc as DOCX and save it as a new dated artifact:

- `docs/publisher/artifacts/agent-arch-ru-final-author-fields-YYYY-MM-DD.docx`

Record:

- Google Doc revision;
- export timestamp;
- file path;
- rough page count after render;
- blank-like page count.

## Step 4. Rebuild Template2000n proof

Use the latest accepted Template2000n style route as the style base and replace
only the text that changed in the raw export. If the publisher rejects the
macro-free route, follow the replacement route supplied by the publisher and
record it before creating the final proof.

Expected output:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-final-author-fields-YYYY-MM-DD.docx`

Text integrity gates:

- same paragraph count or documented intentional delta;
- same non-empty text sequence as raw export;
- no long H2/H3 body-style debt reintroduced.

## Step 5. Render QA

Run render QA for both proofs:

- raw Google Docs export;
- Template2000n derivative.

Required evidence:

- PDF generated;
- PNG page count matches PDF page count;
- blank-like pages below threshold are 0 or explained;
- visual spot checks: first page, minimum-density page, final page;
- DOCX archives pass `unzip -t`.

## Step 6. Update control reports

Create a dated report:

- `docs/publisher/ru-final-author-fields-export-pass-YYYY-MM-DD.md`
- `docs/publisher/ru-final-author-fields-export-pass-YYYY-MM-DD.render-qa.json`

Update:

- `docs/publisher/ru-google-doc-workflow.md`
- `docs/publisher/ru-manuscript-map.md`
- `docs/publisher/ru-manuscript-evolution.md`
- `docs/publisher/ru-editorial-roadmap.md`
- `docs/publisher/ru-submission-checklist.md`
- `docs/publisher/ru-clean-editor-handoff-packet-2026-06-28.md`

## Step 7. Run repository verification

Required commands:

```bash
python3 -m json.tool docs/publisher/ru-final-author-fields-export-pass-YYYY-MM-DD.render-qa.json
unzip -t docs/publisher/artifacts/agent-arch-ru-final-author-fields-YYYY-MM-DD.docx
unzip -t docs/publisher/artifacts/agent-arch-ru-template2000n-final-author-fields-YYYY-MM-DD.docx
git diff --check
uv run --group dev pytest
uv run --group docs mkdocs build --strict
```

## Step 8. Final external handoff decision

Only after all checks pass, mark the manuscript as one of:

- ready for external proofreader;
- ready for publisher copyedit;
- blocked by source fact-check;
- blocked by author/publisher metadata;
- blocked by companion release readiness.

## Current blocker

As of 2026-07-03, this workflow is prepared but not executed as final because
author-owned facts are not filled, publisher/editor acceptance of the
Template2000n route is not recorded and a post-author final export/render QA
pass has not been run.

## 2026-07-03 pre-author dry run

The workflow was executed as far as it can be executed without inventing
author-owned facts:

- current Google Doc front matter was read through the connector;
- author placeholders were confirmed in `Об авторе`;
- a fresh raw DOCX was exported:
  `docs/publisher/artifacts/agent-arch-ru-final-preauthor-raw-2026-07-03.docx`;
- a fresh Template2000n pre-author derivative was rebuilt:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-final-preauthor-2026-07-03.docx`;
- render QA passed for both artifacts: raw 489 pages and Template2000n 361
  pages, 0 blank-like pages;
- report:
  `docs/publisher/ru-final-preauthor-export-pass-2026-07-03.md`;
- pre-author publisher packet:
  `docs/publisher/ru-preauthor-publisher-submission-packet-2026-07-03.md`.

This dry run proves the export/style/render route is operational, but it does
not close the final workflow. The same steps must be repeated after the author
fields are filled or explicitly omitted.
