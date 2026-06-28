# Google Doc global heading normalization pass

Date: 2026-06-28

Google Doc: <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Goal: remove the remaining long `Heading 2` body-style debt from the full
Russian manuscript while keeping Google Doc as the source of truth and
Template2000n as a derived publisher proof.

## Result

The full Google Doc manuscript was updated with style-only Google Docs
`batchUpdate` requests. No manuscript text was changed.

The pass demoted all 629 long body-like `Heading 2` paragraphs to normal text.
The final DOCX export now has zero non-empty `Heading 2` paragraphs longer than
140 characters.

## Implemented plan

1. Fresh DOCX export was captured before edits:
   `docs/publisher/artifacts/agent-arch-ru-heading-normalization-baseline-2026-06-28.docx`.
2. H1/H2/H3 inventory was built from the baseline export.
3. Long H2 candidates were classified as body-like: no structural long H2
   matched chapter, part, appendix or numbered-section patterns.
4. 556 grouped Google Docs `updateParagraphStyle` requests were applied in
   three guarded batches with `requiredRevisionId`.
5. Fresh DOCX export after the pass was captured:
   `docs/publisher/artifacts/agent-arch-ru-heading-normalized-2026-06-28.docx`.
6. Raw render QA was completed.
7. Template2000n derivative was prepared:
   `docs/publisher/artifacts/agent-arch-ru-template2000n-heading-normalized-2026-06-28.docx`.
8. Template2000n render QA, reports and the next 100 editorial goals were
   prepared.

## Structural metrics

Baseline export:

- paragraphs: 8040;
- non-empty `Heading 1`: 26;
- non-empty `Heading 2`: 1393;
- non-empty `Heading 3`: 578;
- long non-empty `Heading 2` paragraphs over 140 chars: 629.

Final export:

- paragraphs: 8040;
- non-empty `Heading 1`: 26;
- non-empty `Heading 2`: 764;
- non-empty `Heading 3`: 578;
- long non-empty `Heading 2` paragraphs over 140 chars: 0.

The raw Google Docs export still contains empty service heading paragraphs:
`Heading 1`: 1, `Heading 2`: 994, `Heading 3`: 124. They are export artifacts
and were not changed in this pass.

Residual style debt for the next pass:

- 65 long `Heading 3` paragraphs over 220 chars remain. They do not affect the
  H2 debt targeted by this pass, but they should be reviewed before the final
  publisher-ready export.

## Render QA

Raw Google Doc export:

- DOCX: `docs/publisher/artifacts/agent-arch-ru-heading-normalized-2026-06-28.docx`
- PDF render: `/private/tmp/agent_arch_ru_heading_normalized_2026_06_28_render/agent-arch-ru-heading-normalized-2026-06-28.pdf`
- Pages: 504
- Blank-like pages: 0
- Visual spot checks: page 1, page 99 and page 504 are readable and not clipped.

Template2000n derivative:

- DOCX: `docs/publisher/artifacts/agent-arch-ru-template2000n-heading-normalized-2026-06-28.docx`
- Source mapping: previous checked Template2000n paragraph-level proof,
  `docs/publisher/artifacts/agent-arch-ru-template2000n-ch23-launch-checklist-pass-2026-06-28.docx`.
- PDF render: `/private/tmp/agent_arch_template2000n_heading_normalized_2026_06_28_render/agent-arch-ru-template2000n-heading-normalized-2026-06-28.pdf`
- Pages: 315
- Blank-like pages: 0
- Visual spot checks: pages 265, 274 and 315 are readable and not clipped.

## Template2000n style metrics

- paragraphs: 8040;
- `BodyText`: 5787;
- `Heading1`: 117;
- `Heading2`: 994;
- `Heading3`: 280;
- unstyled paragraphs: 862;
- paragraph-level `numPr` remaining: 0.

The current manuscript text is identical paragraph-by-paragraph to the previous
chapter 23 proof. Because this pass changed only Google Doc paragraph styles,
the checked Template2000n paragraph mapping was reused as the derived publisher
proof path for this iteration.

## Verification

- Raw DOCX zip integrity checked.
- Template2000n DOCX zip integrity checked.
- Raw render QA: 504 pages, 0 blank-like pages.
- Template2000n render QA: 315 pages, 0 blank-like pages.
- Render QA metrics recorded in
  `docs/publisher/ru-google-doc-heading-normalization-pass-2026-06-28.render-qa.json`.

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
`docs/publisher/ru-editorial-100-heading-normalization-iterations-2026-06-28.md`.
The highest-value next pass is H3/body-style review, then final second-pass
proofreading across overloaded late chapters and front matter.

Follow-up completed on 2026-06-28:
`docs/publisher/ru-google-doc-h3-normalization-pass-2026-06-28.md`.
