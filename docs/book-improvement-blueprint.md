# Agent Arch Book Upgrade Blueprint

## Mission

Turn `agent-arch` from a strong architecture handbook / reference project into a finished, high-authority practical book that readers want to read through, revisit, cite, and recommend.

## Primary Diagnosis

The project already has a real spine:
- strong central thesis: agents need a platform, not magic
- serious operational scope: policy, approvals, memory, observability, evals, lifecycle
- runnable reference package and schemas

But the current manuscript still underperforms the idea in six ways:
1. argument density is lower than the confidence of the prose
2. there is too much architectural inventory and not enough causal narrative
3. genre identity is still blurred
4. role clarity between adjacent operational chapters must be continuously protected
5. evidence and bibliography are still too vendor-doc heavy
6. editorial finish is not yet at book level

## Target State

The book should become:
- an architecture and operating model for production agent systems
- with field-manual usefulness
- with selective reference artifacts
- but without reading like a docs dump

## Primary Reader

Senior engineer / tech lead / platform-minded builder moving from demo agents to production systems.

## Core Promise

After reading the book, the reader should stop thinking about agents as prompt tricks and start designing them as governed production systems with explicit trust boundaries, control surfaces, evidence backbone, evidence substrate, lifecycle discipline, and accountability.

## Non-Goals

This book is not primarily:
- a beginner prompt-engineering guide
- a framework-specific tutorial
- a security-only manual
- a documentation mirror of the runnable reference package
- a project dashboard that replaces the book's reader journey

## Strategic Workstreams

### 1. Manuscript identity and reader journey
Define:
- what this book is
- what it is not
- who it is for
- what transformation in thinking it delivers
- how Parts I-VIII progress as one reader journey

### 2. Evidence spine and operating continuity
Introduce one explicit end-to-end evidence spine that shows how the book's control surfaces operate as one governed model rather than adjacent topics.

It should walk one concrete run through:
- user request
- policy evaluation
- tool calls
- approvals
- trace events
- grading and evals
- incident review
- rollout decision

It should also define the minimal shared entity map across those layers:
- run_id
- trace_id
- approval_id
- policy_bundle_version
- artifact_id
- evaluation_result_id

Each connected chapter should make clear where it sits on that spine and what operational question it answers.

### 3. Case-driven narrative reinforcement
Introduce 2 to 3 recurring canonical scenarios and thread them through major chapters:
- Support triage
- Internal knowledge assistant
- Incident coordination

Each major chapter should show:
- how the scenario breaks at this maturity level
- what false fix teams often try
- what architectural layer actually resolves or contains the problem

### 4. Role-clarity, promise-shape hardening, and late-book de-duplication
Sharpen chapter jobs-to-be-done, especially across:
- Chapter 11: tracing as raw evidence capture
- Chapter 12: SLO as health and risk budgets
- Chapter 13: eval loop as judgment and regression discipline
- Chapter 19: lifecycle frame
- Chapter 20: release judgment for change-bearing systems
- Chapter 21: assurance as response to drift and findings
- Chapter 22: provenance/artifacts as evidence backbone
- Chapter 23: lifecycle closure and operational end-of-life
- Chapter 24: adversarial pressure inside the operational loop
- Chapter 25: reviewable judgment under adversarial pressure
- Chapter 26: observability as evidence substrate
- Chapter 27: inventory, registry, and sprawl control as estate accountability

Preserve the editorial geometry already found in the manuscript:
- Part V = capture, health, judgment
- Part VIII = lifecycle frame, release judgment, response, evidence backbone, lifecycle closure, adversarial pressure, judgment, evidence substrate, accountability

And harden promise shape at the same time:
- part indexes should read as reader outcomes, not topic lists
- chapter intros should say what distinct promise this layer makes
- overlap control should happen through role clarity plus visible reader promises, not only through topical separation

### 5. Evidence expansion
Broaden support beyond vendor docs with more:
- standards and frameworks
- postmortems and incident writeups
- academic work on multi-agent reliability, verifier design, HCI/HITL, provenance, safety cases, enterprise governance
- trade-off and failure-case references

### 6. Editorial hardening
Perform a dedicated book-level pass for:
- terminology consistency
- multilingual polish
- TOC and chapter-title consistency
- cross-links and heading rhythm
- repetition cleanup
- removal of draft-like phrasing
- protection of chapter role grammar so neighboring chapters do not collapse into each other
- protection of promise shape so entry/index pages do not drift back into inventory-style prose

### 7. Book vs reference separation
Keep in chapters:
- ideas
- trade-offs
- failure mechanics
- operating model

Push to appendix/reference/runtime where appropriate:
- schemas
- configs
- exhaustive examples
- implementation details that interrupt reading flow

## Review-Driven Remediation Plan, 14 May 2026

This plan turns the external editorial review into a controlled implementation queue. Items are ordered by reader trust first, then by architectural authority, then by publisher readiness.

### P0. Trust-breaking surface defects

1. **Canonical routing.** Keep `/book`, `/en/book`, and `/zh/book` redirect coverage explicit in `canonical-redirects.js` and tests; verify generated 404 fallback behavior after every build.
2. **Deep localization cleanup.** Treat Russian leftovers in EN/ZH nav, book, appendix, and reference pages as blocking defects; keep regression tests for known leak strings such as `Глава`, `План интеграции идей Google`, and `Схема`.
3. **ZH positioning.** Until a full Chinese editorial pass is scheduled, describe ZH as a draft localization preview rather than a publisher-ready edition.
4. **Rendering/export QA.** Prioritize extraction-safe surfaces in Chapter 1, Chapter 13, the Reference page, and Chapter 26. Prefer prose cards or explicit fallbacks over dense tables where the frame must survive HTML, PDF, print, and plain-text extraction.
5. **Freshness metadata.** Fast-moving chapters and source/status pages must carry `last reviewed`, `next review`, and a short change note.

First implementation slice: Chapter 1 decision frame, freshness metadata for Chapter 13 / Part VIII / Sources / What’s New, and regression tests for those surfaces.

### P1. Safe-agent practice upgrades

1. Add a mini-section that treats **MCP as a security boundary**, not only an integration convenience.
2. Add a mini-section on **A2A governance and agent-to-agent trust**: identity, delegation, capability discovery, audit, and policy enforcement between agents.
3. Add a compact **agent-system threat model matrix** covering prompt injection, indirect injection, RAG poisoning, memory poisoning, tool abuse, confused deputy, excessive agency, data exfiltration, denial of wallet, cascading multi-agent failure, and supply-chain compromise.
4. Strengthen the verifier contract with rubric version, process score, outcome score, failure attribution, judge-human agreement, false-positive / false-negative budget, calibration dataset, and replay protocol.
5. Extend Chapter 26 from observability toward **governance-aware telemetry**: telemetry that feeds containment, rollout gates, policy decisions, and incident response.

### P2. Book-shape improvements

1. Make Chapter 1 the sample chapter: clean opening, stable decision frame, stronger ending, and a diagram/fallback pair that survives export.
2. Thread the three canonical cases — Support triage, Internal knowledge assistant, Incident coordination — through trust boundaries, memory, tool gateway, evals, rollout, registry, and retirement.
3. Compress Part VIII with a role map: lifecycle governance = state transitions; assurance = containment/response; provenance = lineage; observability = evidence substrate; evals = release judgment; registry = ownership/accountability.
4. Restructure the Reference Package page into quick start, architecture map, CLI examples, config contracts, advanced lifecycle/controls, and runtime internals.
5. Add a chapter-ending template: what to remember, common mistakes, what to check in your system, companion assets, and what to read next.

### P3. Publisher package

1. Create a publisher-ready TOC separate from the web TOC.
2. Split manuscript content from online companion material.
3. Prepare a one-page positioning memo: title, subtitle, reader, problem, why now, unique angle, comparable titles, author credibility, status, and companion assets.
4. Run print/PDF readiness: figures, captions, Mermaid fallbacks, tables, code blocks, long lines, anchors, glossary, and cross-references.
5. Establish book release discipline: community edition, Russian manuscript, EN editorial draft, and publisher proposal package.

### Implementation status, 19 May 2026

- **P0:** closed for the known review defects. Canonical book redirects are configured and tested; known EN/ZH Russian leak strings are guarded; ZH entry surfaces disclose draft-localization status; Chapter 1/2 extraction safety and fast-moving freshness metadata are tested.
- **P1:** closed for the named safe-agent upgrades and their schema spine. MCP threat model and `mcp_server` contract, A2A handoff trust contract and trust-delegation artifact, unified agent threat evidence, defense-in-depth control map, verifier verdict record, governance action record, NIST AI RMF telemetry mapping, and memory poisoning review fields are documented across RU/EN/ZH and reflected in [trace schema](appendix/trace-schema.md), [eval schema](appendix/eval-schema.md), and [memory/retrieval schema](appendix/memory-retrieval-schema.md) with docs-surface tests.
- **P2:** mostly closed for the reviewed book-shape items. Chapter 1 now has a sample-chapter ending template; the plan defines the three canonical case spines; Part VIII role-map material is print-friendly; the Reference Package has a reader-route contract. Remaining P2 work should be evidence-backed polish only, not another broad restructuring pass.
- **P3:** publisher packet is drafted and internally gated. The packet now includes publisher-ready TOC, print/companion split, positioning memo, refreshed public-link record, sample export manifest, print/PDF readiness gate, release discipline, author-bio input brief, target-editor formatting brief, copy-edit handoff, print-friendly blocker register, and waiver/decision log.
- **Still blocked before external submission:** author bio/credential framing, independent sample copy-edit, target-specific sample decision, and target editor/imprint formatting. These require human/editorial input or explicit author waiver.

## Priority Order

### Phase A. Strategy
1. Book identity memo
2. Reader journey map
3. overlap audit across late chapters
4. chapter surgery plan

### Phase B. Structural revision
5. sharpen opening and framing chapters
6. build the end-to-end evidence spine page and cross-links
7. reinforce recurring cases
8. protect Part V role clarity
9. protect Part VIII role clarity
10. harden promise shape across entry surfaces, part indexes, and planning docs

### Phase C. Authority and finish
11. expand evidence base
12. editorial polish pass
13. final book/reference boundary cleanup

## Established editorial geometry

This is no longer just a hypothesis. It is now a working manuscript constraint.

### Part V
- Chapter 11 = raw evidence capture
- Chapter 12 = health and risk budgets
- Chapter 13 = reviewable judgment and regression discipline

### Part VIII
- Chapter 19 = lifecycle frame
- Chapter 20 = release judgment
- Chapter 21 = assurance response
- Chapter 22 = evidence backbone and lineage
- Chapter 23 = lifecycle closure
- Chapter 24 = adversarial pressure
- Chapter 25 = judgment under adversarial pressure
- Chapter 26 = evidence substrate and detection-ready visibility
- Chapter 27 = estate accountability through inventory, registry, and sprawl control

### Rewrite rule
When a rewrite makes one chapter sound like its neighbor, prefer restoring role clarity over adding more content.

When an index, intro, or planning page starts sounding like a topic inventory instead of a reader outcome, rewrite toward promise shape rather than adding more summary text.

## Working Deliverables

1. `book-identity-memo.md`
2. `reader-journey-map.md`
3. `late-book-overlap-audit.md`
4. `chapter-surgery-plan.md`
5. later: chapter-by-chapter rewrite tickets
6. evidence-spine page and insertion map
7. failure-rich runtime scenario set and operator notes

## Subagent Ticket Set

### Ticket A. Research Scout: evidence expansion map
Goal:
- identify the strongest source classes missing from the book-level argument
- focus on postmortems, academic work, HCI/HITL, provenance, safety cases, enterprise governance

Expected output:
- source clusters
- why each cluster matters
- insertion points
- commit slices

### Ticket B. Consistency Auditor: overlap and genre audit
Goal:
- inspect Parts V, VII, VIII and appendix/reference surfaces for overlap, role confusion, and repeated concepts
- document the highest-risk chapter boundaries and the guardrails that keep them from collapsing back together

Expected output:
- chapter-level jobs-to-be-done
- severity-ranked overlap findings
- keep-lists / boundary guardrails for the riskiest chapter pairs
- what to cut, merge, or sharpen

### Ticket C. Consistency Auditor: opening and reader-journey audit
Goal:
- inspect Part I plus transitions into later parts
- determine whether the book currently creates a compelling read-through arc

Expected output:
- opening weaknesses
- missing transitions
- recommended restructuring

### Ticket D. Manual synthesis in main session
Goal:
- merge subagent findings into a concrete rewrite program
- produce editorial roadmap and execution order

## Success Criteria

We should consider this phase successful when we have:
- a stable identity for the book
- a clear primary reader
- a reader journey that can be explained in one page
- a concrete overlap-reduction plan
- a stronger evidence strategy
- one explicit evidence spine that connects runtime, policy, approval, eval, incident review, and rollout
- a chapter rewrite queue that improves the book as a book, not just as a website
- visible promise-shape consistency across homepage, start-here, part indexes, and planning docs
- a stable separation where the book owns argument and transformation, while support layers own reusable artifacts and implementation anchors
