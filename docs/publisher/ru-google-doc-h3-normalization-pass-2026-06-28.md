# Google Doc H3/body-style normalization pass

Date: 2026-06-28

Google Doc: <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Goal: close the residual long `Heading 3` body-style debt after the global H2
normalization pass while keeping Google Doc as the manuscript source of truth
and Template2000n as a derived publisher proof.

## Result

The full Google Doc manuscript was updated with style-only Google Docs
`batchUpdate` requests. No manuscript text was changed.

The pass demoted all 65 long body-like `Heading 3` paragraphs to normal text.
The final DOCX export now has zero non-empty `Heading 2` paragraphs longer than
220 characters and zero non-empty `Heading 3` paragraphs longer than 220
characters.

## Implemented plan

1. The previous H2-normalized DOCX export was used as the baseline:
   `docs/publisher/artifacts/agent-arch-ru-heading-normalized-2026-06-28.docx`.
2. Long H3 inventory was built from the baseline export.
3. All 65 long H3 candidates were classified as body-like prose; no structural
   chapter, part, appendix or numbered-section headings matched the long-H3
   candidate set.
4. Live Google Doc paragraph ranges were spot-validated against the first and
   last candidate before applying edits.
5. 65 guarded Google Docs `updateParagraphStyle` requests were applied with
   `requiredRevisionId`.
6. Fresh DOCX export after the pass was captured:
   `docs/publisher/artifacts/agent-arch-ru-h3-normalized-2026-06-28.docx`.
7. Raw render QA was completed.
8. Template2000n derivative was prepared:
   `docs/publisher/artifacts/agent-arch-ru-template2000n-h3-normalized-2026-06-28.docx`.
9. Template2000n render QA, reports and the next 100 editorial goals were
   prepared.

## Structural metrics

Baseline export:

- paragraphs: 8040;
- non-empty paragraphs: 6024;
- rough words: 97665;
- `normal`: 5502;
- `Heading 2`: 1758;
- `Heading 3`: 702;
- non-empty `Heading 3`: 578;
- long non-empty `Heading 2` paragraphs over 220 chars: 0;
- long non-empty `Heading 3` paragraphs over 220 chars: 65.

Final export:

- paragraphs: 8040;
- non-empty paragraphs: 6024;
- rough words: 97665;
- `normal`: 5567;
- `Heading 2`: 1758;
- `Heading 3`: 637;
- non-empty `Heading 3`: 513;
- long non-empty `Heading 2` paragraphs over 220 chars: 0;
- long non-empty `Heading 3` paragraphs over 220 chars: 0.

Text equality check: paragraph count and paragraph text sequence are identical
between the baseline and final raw DOCX exports. The only paragraph-style diff
is `Heading 3` -> `normal` for 65 paragraphs.

## Render QA

Raw Google Doc export:

- DOCX: `docs/publisher/artifacts/agent-arch-ru-h3-normalized-2026-06-28.docx`
- PDF render: `/private/tmp/agent_arch_ru_h3_normalized_2026_06_28_render/agent-arch-ru-h3-normalized-2026-06-28.pdf`
- Pages: 499
- Blank-like pages: 0
- Visual spot checks: page 1, page 62 and page 499 are readable and not clipped.

Template2000n derivative:

- DOCX: `docs/publisher/artifacts/agent-arch-ru-template2000n-h3-normalized-2026-06-28.docx`
- Source mapping: previous checked Template2000n paragraph-level proof,
  `docs/publisher/artifacts/agent-arch-ru-template2000n-heading-normalized-2026-06-28.docx`.
- PDF render: `/private/tmp/agent_arch_ru_template2000n_h3_normalized_2026_06_28_render/agent-arch-ru-template2000n-h3-normalized-2026-06-28.pdf`
- Pages: 315
- Blank-like pages: 0
- Visual spot checks: pages 1, 301 and 315 are readable and not clipped.

## Template2000n style metrics

- paragraphs: 8040;
- `Body Text`: 5787;
- `Heading 1`: 117;
- `Heading 2`: 994;
- `Heading 3`: 280;
- unstyled paragraphs: 862.

The current manuscript text is identical paragraph-by-paragraph between the
fresh raw Google Doc export and the Template2000n proof. Because this pass
changed only Google Doc paragraph styles and the Template2000n proof already
had zero long H3 debt, the checked Template2000n paragraph mapping was reused
as the derived publisher proof path for this iteration.

## Verification

- Raw DOCX zip integrity checked.
- Template2000n DOCX zip integrity checked.
- Raw render QA: 499 pages, 0 blank-like pages.
- Template2000n render QA: 315 pages, 0 blank-like pages.
- Render QA metrics recorded in
  `docs/publisher/ru-google-doc-h3-normalization-pass-2026-06-28.render-qa.json`.

## Author-owned fields still open

The manuscript still needs author-owned input before external editorial or
publisher handoff:

- `Об авторе`: real name/public name, role, verified experience, public
  projects, links and final publisher wording.
- Public online companion URL and release/version policy.
- Real author cases or anonymized implementation stories, if they should be
  included.
- Legal/compliance wording and AI tooling disclosure.
- Final metadata: title/subtitle decision, cover copy, acknowledgements and
  imprint-specific fields.

## Next work

The next 100 goals are recorded in
`docs/publisher/ru-editorial-100-h3-normalization-iterations-2026-06-28.md`.
The highest-value next pass is final editorial proofing after style cleanup:
author-owned fields, front matter, cross-references, glossary, companion routes,
publisher style application and final external-proof package.
