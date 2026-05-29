# Design: Russian publisher-readiness pass

## Goal

Turn the Russian web manuscript from a strong living documentation book into a publisher-facing manuscript package without losing the public site, reference runtime, or companion assets.

## Approved direction

The current site remains the broad public edition. The publisher-facing work creates a cleaner editorial layer around it:

1. a Russian publisher manuscript map;
2. a terminology policy for Russian prose;
3. a book/reference split for print;
4. a first editorial cleanup slice that proves the approach on high-impact surfaces.

## Scope for the first implementation slice

This first slice should not rewrite the whole book. It should establish the pattern and reduce obvious blockers:

- create a Russian terminology guide for publisher editing;
- create a Russian publisher manuscript map based on the existing 6-part / ~20-chapter packet shape;
- update publisher packet notes so RU submission is clearly distinct from EN submission;
- clean the most visible Russian entry surfaces and sample-candidate headings where safe;
- keep full schemas, CLI outputs, runtime details, and long reference catalogs in the online companion.

## Non-goals

- Do not attempt a full 27-chapter line edit in one pass.
- Do not delete web edition content.
- Do not remove technical terms that are standard and useful; define how they should appear.
- Do not touch unrelated existing edits in appendix case-study/source files.

## Editorial rules

- Prefer Russian prose for ordinary words: tools -> инструменты, agents -> агенты, deploy -> развертывание, stack -> набор/стек only when conventional.
- Keep protocol/product names and standard acronyms: MCP, A2A, SLO, CLI, YAML, JSON, GitHub Pages.
- For unstable terms, choose one primary Russian form and allow English only on first mention or in code/reference contexts.
- Replace service scaffolding such as `case-spine note` / `canonical cases` with reader-facing Russian labels.
- Move dense runtime/schema/validation detail out of print flow and into companion references.

## Deliverables

1. `docs/publisher/ru-terminology.md` — editorial term policy.
2. `docs/publisher/ru-manuscript-map.md` — publisher manuscript assembly map.
3. `docs/publisher/ru-submission-checklist.md` — readiness gates before sending to an editor.
4. Targeted updates to existing publisher packet docs when they currently imply EN-only samples.
5. Verification: docs surface tests, strict MkDocs build, and `git diff --check` for touched files.

## Risks

- Existing repo has unrelated uncommitted changes; implementation must avoid mixing them.
- Some tests intentionally assert bilingual marker strings. If editorial policy changes those surfaces, update tests deliberately.
- A complete publisher pass is larger than one slice; this work should create a repeatable path, not pretend the manuscript is finished.

## Success criteria

- A Russian publisher path is explicit and reviewable.
- The next editor can see what to edit, what to leave online, and how to treat terms.
- The first slice reduces visible blockers without destabilizing the multilingual site.
- Verification passes for the touched surface.
