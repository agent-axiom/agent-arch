# RU Google Doc frontier, deduplication, and identifier repair pass - 2026-07-11

Target Google Doc:
<https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4/edit?tab=t.0>

Final checked Google Doc revision:
`ALtnJHyv4HfRItN27cdocxtXJVB_NAbzFKqXkSX7nbwo6-1dZFezuMIwTkjAAd1nktXq4OGT40_HxsjMA1meVio63evcltdgdA7F6oISbcw`

Final exported PDF used for QA:
`/tmp/agent-arch-google-doc-final-2026-07-11-v5.pdf`

PDF SHA-256:
`e5ec4f1900381da4b366c43763f01b6fee6675337394e83a9e2d103f7bab2353`

## Upstream material reviewed

- `d6a2770f` - versioned risk posture gate pattern;
- `f02f6329` - IDE agent work queue pattern;
- `4308389e` - governed agent execution loop pattern.

The relevant concepts were integrated into the live manuscript without merging
the unrelated upstream document-history changes into this publisher branch.

## Implemented in the Google Doc

- Added a versioned risk posture contract with policy version, assessment
  coverage date, reviewer evidence, release decision, and post-release
  monitoring.
- Added the governed execution loop as both narrative guidance and a trace
  contract linking the bounded workspace, tool and network policy, approvals,
  staged output, validation gates, and monitoring.
- Added the IDE agent work queue as an operator-visible work item contract with
  session identity, model policy, usage budget, browser context, permissions,
  feedback, and artifacts.
- Replaced the duplicated Chapter 22 assembly with a concise implementation
  chapter about the policy layer and capability catalog.
- Removed the repeated reference-package block, policy-template assembly,
  incident-schema assembly, repeated freshness notes, and the duplicated visual
  appendix. The exact-paragraph scan now finds zero duplicate groups at 180 or
  more characters.
- Replaced the five in-flow figures with localized versions and kept them in
  Chapters 3, 9, 13, and 16. Captions are configured to remain with the figure.
- Removed one literal HTML fragment, repaired two source-appendix sentence
  joins, and updated the source-review date to 11 July 2026.
- Completed a focused Russian-language pass while preserving standard product
  names, acronyms, and executable identifiers.
- Reconciled manuscript identifiers against `agent_runtime_ref`, tests,
  `docs/book`, and `docs/appendix`: 759 canonical identifier forms were
  restored across 1,943 replacements. The final scan finds no remaining
  unambiguous flattened identifiers such as `traceid` or `idempotencykey`.

## Practical verification

The current branch successfully executed the manuscript practice path:

- `python -m agent_runtime_ref --help`;
- `simulate-run`, `dump-events`, `export-events`, and `inspect-trace`;
- `export-eval-dataset --scenario failed_run_timeout`;
- `inspect-agent`, `inspect-approvals`, and `resolve-approval`;
- `check-controls --signal registry_reviewed=false` with the expected blocked
  control result.

## Google Doc and PDF QA

- Target identity: document id `1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4`,
  title `Архитектура безопасных ИИ-агентов`, tab `t.0`.
- Connector readback: 9,906 paragraphs; text and structure revisions match.
- Seven practical exercises are present as `HEADING_1`, parts I-VII.
- Ten inline images remain; all five new localized chapter figures resolve to
  their repository assets.
- No `TODO`, `TBD`, `[[FIG_...]]`, literal `<strong>`, removed visual-appendix
  heading, or known flattened identifier markers remain.
- Google Docs export: 419 tagged Letter pages, 5,874,709 bytes, no encryption.
- All 419 pages were rasterized. Automated checks found no near-blank pages, no
  low-ink pages, and no dark content touching the page edges.
- Key pages containing the new material and figures were visually inspected at
  120 dpi, including pages 151, 194, 212-213, 242, 274, 349-353, 359-361,
  396, and 419.

## Repository checks

- `git diff --check` - passed.
- `uv run pytest tests/test_docs_surface.py tests/test_agent_runtime_ref.py` -
  948 passed.
- `uv run --group docs mkdocs build --strict` - passed.

## Author-owned fields still required

The only explicit manuscript placeholders are in `Об авторе`. The author must
provide:

- public author name/byline;
- current role or independent positioning;
- one or two verified sentences about relevant experience;
- website, GitHub/public profiles, and publisher contact;
- final short wording for the cover or catalog card.

## Next editorial actions

1. Fill the author-owned fields and freeze front matter.
2. Apply the final publisher template and run a DOCX/PDF typography pass,
   especially for inline code, backticks, long code blocks, and list spacing.
3. Run an independent technical and copy edit against the frozen Google Doc.
4. Conduct a small reader pilot with an architect, a platform engineer, and a
   security engineer; turn repeated confusion into targeted edits and evals.
5. Freeze source URLs, glossary, legal/compliance wording, and publisher
   metadata before submission.
