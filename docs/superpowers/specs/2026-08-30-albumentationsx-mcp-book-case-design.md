# AlbumentationsX MCP Author Case Design

## Goal

Add a transparent, evidence-backed author case to the book that uses
AlbumentationsX MCP to show when MCP is the right abstraction for a bounded
domain capability. The case should teach architectural judgment, describe
verifiable strengths, disclose the author's relationship to the project, and
avoid reading like product promotion.

> **Integration note (30 August 2026).** After rebasing onto the post-PR #57
> manuscript pipeline, AWS remains `S123`; the AlbumentationsX evidence uses
> `S124`/`S125`. The publisher transform runs after the 23 August passes and
> preserves the newer protocol-choice bridge. The final print case is 123 words
> inside a 4,985-word Chapter 11. Any older identifiers or pass ordering in the
> historical implementation notes are superseded by this integrated contract.

## Editorial Decision

Place the case in the practical MCP-versus-A2A section, immediately after the
sentence that concludes that MCP fits systematic external capabilities and
before the section about when A2A is needed.

Use this heading in Russian:

> ### 2.1. Авторский кейс: AlbumentationsX MCP — возможность, а не отдельный агент

The English and Chinese headings should preserve both meanings: this is an
author-owned project, and the architectural lesson is capability versus agent.
The web edition must use a level-three subsection. The print manuscript must
use a bold microheading so Chapter 11 does not exceed its heading-density gate.

## Disclosure And Voice

The opening sentence must state that AlbumentationsX MCP is an open-source
community integration developed by the author of the book. It must also state
that it is not an official AlbumentationsX product or a replacement for the
Python API. This matches the terminology used by the official AlbumentationsX
integration guide.

Use a neutral technical voice. Present implementation properties and the
architectural lessons they support. Do not use adoption language, comparative
superlatives, marketing copy, or an endorsement-style call to action.

## Case Structure

The online case should be 180–220 Russian words, with equivalent informational
density in English and Chinese. It should contain three short movements:

1. **Purpose and boundary.** Explain that the server lets an MCP host inspect
   datasets, validate augmentation pipelines, render small local previews,
   collect concrete visual feedback, compare variants, and export a reviewed
   pipeline. It is a domain capability and does not own an autonomous goal,
   policy, or operational role; therefore MCP is the appropriate abstraction,
   not A2A.
2. **Verifiable strengths.** Describe bounded input roots, a separate artifact
   root, preflight validation, request-size limits, deterministic seeds and
   preview traces, capability profiles, contract snapshots, and golden MCP
   evaluations. Tie these properties to least privilege, reproducibility,
   controlled tool discovery, and interface-drift detection.
3. **Limits and lesson.** State that least privilege requires an explicitly
   narrow `allowed-root`; preview acceptance is a workflow convention rather
   than a hard authorization gate; and the young project is not evidence of
   broad production adoption. Close on the transferable lesson: a useful MCP
   server combines a narrow domain contract, enforceable execution limits,
   reproducible artifacts, and honest evidence boundaries.

The case must remain prose-only. It must not add a code listing, table, figure,
or installation tutorial.

## Claims And Evidence

Pin repository claims to release `v1.21.1` and commit
`171e2ca44830a16c363c8e3614825f2a0d2215b8`. Cite all three source roles:

- the official AlbumentationsX MCP integration guide for community status,
  scope, host workflow, and safety guidance;
- the `v1.21.1` release page for the version represented by the case;
- commit-pinned repository files for concrete implementation and verification
  properties. Do not use moving `main` links for those claims.

The following claims are allowed when kept within their exact scope:

- input paths are resolved and restricted to configured allowed roots;
- generated preview artifacts are stored beneath a configured artifact root;
- preview requests have schema and cardinality limits and can be validated
  before rendering;
- preview manifests retain seeds, applied-transform traces, artifact metadata,
  and hashes that support reproducibility and inspection;
- capability profiles expose bounded views of one declared MCP surface;
- public MCP and output contracts have snapshot guards and golden evaluation
  coverage;
- the published project supports local AlbumentationsX review workflows and
  does not train models, fetch remote images, overwrite datasets, or execute
  arbitrary user-supplied Python.

The following claims are prohibited:

- that the project is an official AlbumentationsX product;
- that it is enterprise-grade, independently security-audited, battle-tested,
  widely adopted, or proven safe;
- that its workflow guidance is equivalent to enforced authorization;
- that passing tests proves external adoption or production readiness;
- that the default launch configuration is least-privilege without an explicit
  narrow root configuration.

## Files And Synchronization

Update the three online practical pages together:

- `docs/book/part-iv/practical-mcp-a2a.md`
- `docs/book/part-iv/practical-mcp-a2a.en.md`
- `docs/book/part-iv/practical-mcp-a2a.zh.md`

Add localized footnotes and source entries in the corresponding Russian,
English, and Chinese source appendices. Use the repository's existing source
style and keep the pinned project source distinct from the official
AlbumentationsX integration guide.

The source appendices are:

- `docs/appendix/sources.md`
- `docs/appendix/sources.en.md`
- `docs/appendix/sources.zh.md`

For the publisher edition, add a deterministic final editorial pass to
`docs/publisher/tools/revise_ru_manuscript.py`, after the existing
`apply_technical_book_polish_2026_08_02()` pass. The pass should replace or
compress the generic "when MCP is needed" prose in publisher Chapter 11 and
insert a 120–160-word Russian print version of the author case. Its net change
to Chapter 11 must be zero words or negative. Regenerate
`docs/publisher/ru-manuscript-editorial-2026-07-13.md` through the existing
publisher workflow; do not patch DOCX or PDF binaries manually.

The print version must preserve the chapter's current structural budgets:

- fewer than 5,000 words;
- no more than 17 level-four headings;
- unchanged listing, table, figure, inline-diagram, and image counts.

Existing unrelated publisher edits, generated artifacts, and `.tmp` content in
the working tree must not be modified, staged, or committed.

This change does not add the case to `docs/book/part-iv/chapter-9*.md` or the
case-studies appendix. The practical section and its print projection are the
single editorial home for the case.

## Verification

Add focused documentation tests that prove:

1. all three online languages contain the localized author disclosure,
   AlbumentationsX MCP name, capability-versus-agent lesson, strengths, limits,
   and localized source links;
2. the Russian, English, and Chinese pages do not drift on the case's required
   semantic markers;
3. publisher regeneration is deterministic and the generated Chapter 11
   contains the author disclosure and all required source roles;
4. Chapter 11 remains below its word and heading limits;
5. listing, table, figure, diagram, and image counts remain unchanged;
6. the strict MkDocs build and the relevant documentation and publisher tests
   pass.

The focused assertions belong in `tests/test_docs_surface.py` and
`tests/test_ru_manuscript_revision.py`. Existing publisher rendering tests
remain regression coverage; add new DOCX-specific assertions only if the
implementation changes rendered structure, which this design prohibits.

## Acceptance Criteria

The change is complete when a reader can answer four questions directly from
the case:

1. Why is AlbumentationsX MCP a capability rather than an autonomous agent?
2. Which concrete controls make its local preview workflow bounded and
   reproducible?
3. Which limitations prevent the case from being read as a security or
   adoption guarantee?
4. What relationship does the book's author have to the project?

The final text must answer all four without promotional language, unsupported
maturity claims, or silent multilingual and publisher drift.
