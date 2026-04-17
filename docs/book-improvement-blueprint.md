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
4. late-book chapter boundaries are not sharp enough
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

After reading the book, the reader should stop thinking about agents as prompt tricks and start designing them as governed production systems with explicit control surfaces, evidence loops, and lifecycle discipline.

## Non-Goals

This book is not primarily:
- a beginner prompt-engineering guide
- a framework-specific tutorial
- a security-only manual
- a documentation mirror of the runnable reference package

## Strategic Workstreams

### 1. Manuscript identity and reader journey
Define:
- what this book is
- what it is not
- who it is for
- what transformation in thinking it delivers
- how Parts I-VIII progress as one reader journey

### 2. Case-driven narrative reinforcement
Introduce 2 to 3 recurring canonical scenarios and thread them through major chapters:
- support triage agent
- internal enterprise knowledge assistant
- high-risk action / approval-bound agent

Each major chapter should show:
- how the scenario breaks at this maturity level
- what false fix teams often try
- what architectural layer actually resolves or contains the problem

### 3. Late-book de-duplication
Sharpen chapter jobs-to-be-done, especially across:
- Chapter 13: eval loop as learning system
- Chapter 21: assurance as response to drift and findings
- Chapter 25: behavioral/control evals as adversarial validation
- Chapter 26: observability as evidence substrate
- Chapter 27: registry/inventory as estate governance

### 4. Evidence expansion
Broaden support beyond vendor docs with more:
- standards and frameworks
- postmortems and incident writeups
- academic work on multi-agent reliability, verifier design, HCI/HITL, provenance, safety cases, enterprise governance
- trade-off and failure-case references

### 5. Editorial hardening
Perform a dedicated book-level pass for:
- terminology consistency
- multilingual polish
- TOC and chapter-title consistency
- cross-links and heading rhythm
- repetition cleanup
- removal of draft-like phrasing

### 6. Book vs reference separation
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

## Priority Order

### Phase A. Strategy
1. Book identity memo
2. Reader journey map
3. overlap audit across late chapters
4. chapter surgery plan

### Phase B. Structural revision
5. sharpen opening and framing chapters
6. reinforce recurring cases
7. de-duplicate late lifecycle/evals/observability/governance cluster

### Phase C. Authority and finish
8. expand evidence base
9. editorial polish pass
10. final book/reference boundary cleanup

## Working Deliverables

1. `book-identity-memo.md`
2. `reader-journey-map.md`
3. `late-book-overlap-audit.md`
4. `chapter-surgery-plan.md`
5. later: chapter-by-chapter rewrite tickets

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

Expected output:
- chapter-level jobs-to-be-done
- overlap findings
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
- a chapter rewrite queue that improves the book as a book, not just as a website
