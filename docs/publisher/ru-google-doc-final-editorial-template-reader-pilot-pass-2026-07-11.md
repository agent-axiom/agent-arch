# RU Google Doc final editorial, template, and reader-pilot pass - 2026-07-11

Target Google Doc:
<https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4/edit?tab=t.0>

Final verified Google Docs revision:
`ALtnJHzcXr7ZgrY5147ZTSRH9pavH1UP4CJXs3Rqw8jxs6LhC8PZrzbABbAw_tRXFhJH0t9b3Kd6VXaS-4n17iDF2d7nO2IfkdK47HusmF0`

Repository source revision recorded in the manuscript:
`885bc9639d5c5c4f43adc62ca3c80be124787ccf`

## Implemented in the live Google Doc

- Replaced the obsolete eight-part, 27-chapter editorial outline with the
  actual seven-part, 23-chapter reader map.
- Removed the publication backlog, site-status prose, expired review dates,
  Material for MkDocs button residue, and stale Chapter 24-27 references.
- Added a final conclusion that returns to the duplicate-ticket incident and
  gives an eight-step implementation sequence.
- Split Chapter 2 into explicit instruction/scenario and
  coordinator/handoff routes without changing the canonical chapter count.
- Converted 44 reader-facing pseudo-bullets into real Google Docs lists while
  preserving 261 code/YAML lines as code.
- Converted 202 inline code spans from literal backticks to Courier New 9 pt;
  the final connector scan finds zero visible backticks.
- Added controlled page starts for parts, later chapters, the conclusion, and
  appendices; first chapters remain with their part headings.
- Finalized the author block as a fillable publisher form without inventing
  author facts and added a reader-facing safety/legal disclaimer.
- Froze the source set and access date at 11 July 2026 and recorded the exact
  repository URL and source revision.

## Technical and security corrections

- Corrected damaged executable identifiers and code examples, including
  capability, telemetry, rollout, handoff, and evaluation fields.
- Replaced platform-dependent `.venv/bin/python` commands with a reproducible
  Python 3.12+ / `uv` bootstrap pinned to the recorded source revision.
- Corrected the failed-run exercise so `support_ticket` and
  `failed_run_timeout` are inspected in the scenarios where their evidence
  actually exists.
- Clarified that `agent_runtime_ref` is a deterministic educational contract
  simulator, not a production sandbox, MCP executor, durable approval system,
  or release attestation service.
- Separated command success from task success while an approval remains
  pending and documented the demo CLI's exit-code limitation for CI gates.
- Strengthened the text around tenant isolation, approval binding, untrusted
  retrieval/tool output, evaluator injection, release attestations, egress,
  telemetry redaction, context reset, and statistical release thresholds.
- Removed the false equivalence between a second subagent attempt and an
  independent control signal.
- Completed a targeted Russian-language pass and repaired identifiers and
  grammar damaged by earlier automatic terminology replacement.

## Independent review incorporated

The frozen draft was checked from five independent perspectives:

- software architect: structure, transitions, argument, and recommendation;
- platform engineer: reproducible commands and repository/runtime fidelity;
- security engineer: false assurance, authorization, evidence, and isolation;
- technical editor: identifiers, chapter references, examples, and exercises;
- literary editor: reader address, editorial residue, grammar, and anglicisms.

Repeated findings were applied directly to the live manuscript. The most
important shared finding was that the material was strong but the obsolete
reader map and overclaimed reference runtime made the book feel less reliable
than its core argument.

## Final connector checks

- Document id, title, and tab: verified.
- Paragraphs: 10,084 total; 9,871 non-empty.
- Canonical structure: 7 parts, 23 chapters, 7 part exercises, 1 conclusion.
- Inline figures: 10 content references and 10 object definitions.
- Reader-facing pseudo-bullets: 0.
- Long exact duplicate paragraph groups: 0.
- Residue scan: no `TODO`, `TBD`, `[[FIG_...]]`, MkDocs buttons, obsolete
  Chapter 24-27 references, known flattened identifiers, or mixed-script
  corrupted identifiers.

## Template2000n and export QA

The supplied `Template2000n.dot` was used only as a style source. Its VBA
macros were not executed. A macro-free OOXML derivative was built from the
final Google Docs DOCX export.

- Styled DOCX:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-freeze-2026-07-11.docx`
- Styled DOCX SHA-256:
  `95b14a6689fedd1a46cb474d684ccc2e3324448ed9d0dbedc44bccede7bbf078`
- Text equality between raw Google Docs DOCX and styled DOCX: `true`.
- Approximate word count: 97,452.
- Live Google Docs PDF: 425 Letter pages.
- Template2000n DOCX render: 352 pages.
- All 777 rendered pages were scanned: no blank pages and no dark content
  touching page edges.
- Front matter, chapter starts, the Chapter 16 figures, conclusion, glossary,
  sources, runtime bootstrap, and final pages were visually inspected.

The page-count difference is caused by the denser publisher styles, not lost
content.

## Author-owned fields still required

- public author name/byline;
- short biography (50-70 words);
- extended biography (120-150 words);
- current role or independent positioning;
- one or two verifiable experience statements;
- website, GitHub, public profiles, and publisher contact;
- final cover/catalog wording;
- acknowledgements, or removal of that line;
- AI-use disclosure wording agreed with the publisher.

## Recommended next actions

1. Fill and fact-check the author-owned fields and publisher metadata.
2. Give the frozen DOCX to the publisher for tracked copy/proof edits; route
   semantic corrections back to the Google Doc.
3. Run one final source-link and product-version check immediately before the
   publisher handoff.
4. Use three external beta readers to validate Chapter 2, Chapter 20, and the
   repository exercises; apply only repeated, evidence-backed confusion.
5. Expand the reference runtime only when a stateful ticket fixture, durable
   approval resume, negative isolation tests, and verified release evidence
   can make the corresponding book claims executable.
