# Google Doc quality sync and terminology pass

Date: 2026-07-04.

Status: completed as a targeted manuscript quality-sync pass. This is not a
final publisher export because author-owned fields, fresh post-terminology DOCX
export and external proofread are still open.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

## Implemented plan

1. Checked the current Google Doc revision and treated it as the active
   editorial manuscript.
2. Attempted a fresh binary DOCX export. The authenticated connector returned
   the DOCX as an oversized inline binary response, while the unauthenticated
   export URL returned `401`; therefore no new raw DOCX could be safely saved
   locally in this pass.
3. Rebuilt a new Template2000n derivative from the latest valid raw Google Docs
   DOCX export using the attached `Template2000n.dot` through the macro-free
   style route.
4. Rendered the raw and styled DOCX proofs to PDF/PNG and ran blank-like page
   checks.
5. Reduced excessive English editorial terms in the Google Doc and repository
   manuscript/support maps while leaving code identifiers, protocol names and
   accepted technical terms intact.
6. Updated the repository checkpoint, render metadata and next 100 editorial
   goals.

## Google Doc terminology update

Revision before terminology update:

- `ALtnJHynC5_zU9n9cmTvBjPl9UMeD7Uve6QHp3PDDm33ZwWHCfBekh00ktjv4-xnUtiwP6hL7W39I4iTLk77MaTY60Z8DnRkpVQxhi5p46U`

Revision after terminology update:

- `ALtnJHwPMvOVdwcrz2tbGM0rdze_Ped9LzfMOgWtZCTtkIG1K5pXx008c-6ckzYavZt9Wn-LtRrB9r16Q37qcoztxBoKsxdBLmi6LKr_EW4`

Applied guarded `replaceAllText` changes: `316` total:

- `293` terminology replacements;
- `23` grammatical corrections after the broad `tool call`/`human review`
  terminology replacements.

Examples of replacements:

- `online companion` -> `онлайн-сопровождение`;
- `companion route` -> `маршрут сопроводительных материалов`;
- `tool gateway` -> `шлюз инструментов`;
- `policy gateway` -> `шлюз политик`;
- `incident response` -> `реагирование на инциденты`;
- `rollout-план` -> `план поэтапного выпуска`;
- `workflow` phrases in regular prose -> `рабочий процесс` phrases;
- `tool call` in regular prose -> `вызов инструмента`.

Readback checks after the update found no remaining exact matches for:

- `online companion`;
- `policy gateway`;
- `tool gateway`;
- `incident response`.

## DOCX artifacts

Latest valid raw Google Docs export used as the raw proof baseline:

- `docs/publisher/artifacts/agent-arch-ru-final-preauthor-raw-2026-07-03.docx`
- bytes: `687813`
- SHA-256: `1e7654ba0dbfa195b691ef2f1c9f8394cbf3463d18061b0c829b30b2ba696b30`

New Template2000n quality-sync derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-quality-sync-2026-07-04.docx`
- bytes: `695009`
- SHA-256: `b4f7e8b2ec2d43e27530122e56a4740d28a81a995ed81e4b7748cf9d305c2e9e`
- paragraphs: `8179`
- non-empty paragraphs: `6105`
- approximate words: `99587`
- no-style body paragraphs mapped to `Body Text`: `4953`
- raw/styled paragraph text equality: preserved

Build tool added:

- `docs/publisher/tools/build_template2000n_derivative.py`

The `.dot` file was converted with headless LibreOffice using an isolated
temporary user profile. No Template2000n macros were executed.

## Render QA

Raw proof:

- pages: `489`
- blank-like pages: `0`
- contact sheet:
  `/tmp/agent-arch-ru-quality-sync-raw-contact-2026-07-04.png`

Template2000n quality-sync derivative:

- pages: `357`
- blank-like pages: `0`
- contact sheet:
  `/tmp/agent-arch-ru-template2000n-quality-sync-contact-2026-07-04.png`

Both contact sheets were visually checked for first page, final page and
lowest-density pages. No obvious blank page, clipping or overlap was observed
in the sampled pages.

Machine-readable QA:

- `docs/publisher/ru-google-doc-quality-sync-pass-2026-07-04.render-qa.json`
- `docs/publisher/ru-template2000n-quality-sync-2026-07-04.metrics.json`

## Repository updates

Updated:

- `docs/publisher/ru-manuscript-full.md`;
- `docs/publisher/ru-terminology.md`;
- `docs/publisher/ru-source-map.md`;
- `docs/publisher/ru-manuscript-map.md`;
- `docs/publisher/ru-manuscript-evolution.md`;
- `docs/publisher/ru-submission-checklist.md`;
- `docs/publisher/ru-google-doc-workflow.md`.

Added:

- `docs/publisher/tools/apply_ru_terminology_replacements.py`;
- `docs/publisher/tools/build_template2000n_derivative.py`;
- `docs/publisher/tools/render_qa_metrics.py`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-quality-sync-2026-07-04.docx`;
- `docs/publisher/ru-editorial-100-quality-sync-export-iterations-2026-07-04.md`.

## Remaining author-owned fields

The author still needs to fill or explicitly omit:

- public author name/byline;
- short and long author bio;
- role/public positioning;
- verified experience claims;
- public project links;
- companion/online-support URL, versioning, changelog and errata route;
- acknowledgements;
- legal/compliance disclaimer wording if publisher requires it;
- AI-use disclosure wording if publisher requires it;
- final title, subtitle, cover copy and imprint metadata.

## Decision

The Google Doc manuscript is cleaner after the terminology pass, and the
repository now has a fresh Template2000n quality-sync proof with render QA.
Because the Google Doc changed after the latest raw DOCX baseline, the next
publisher-critical step is a fresh authenticated raw DOCX export from the
updated Google Doc, then a repeat Template2000n build and render QA.
