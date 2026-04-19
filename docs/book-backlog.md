# Book Backlog for *Agent Architecture*

## Goal
Make the book:
- more evidence-driven;
- more useful for architectural choice;
- stronger as an operational handbook;
- easier to enter and navigate;
- closer to production reality, not only to a “correct” architectural model.

---

## Prioritization Principles
- P0, maximum increase in usefulness and quality without a full rewrite.
- P1, makes the book deeper and intellectually stronger.
- P2, expands audience, improves long-term value, and adds polish.

---

# P0, Critical improvements

## 1. End-to-end evidence spine
Problem, tracing, evals, approvals, incidents, and rollout currently read as strong but partly separated entities.

What to do:
- Add a dedicated page or chapter, Evidence Spine.
- Show one end-to-end run path:
  - user request
  - policy evaluation
  - tool calls
  - approvals
  - trace events
  - grading and evals
  - incident review
  - rollout decision
- Introduce a shared entity and relationship map:
  - run_id
  - trace_id
  - approval_id
  - policy_bundle_version
  - artifact_id
  - evaluation_result_id

Result:
- The reader understands not only the separate layers, but how they operate as one operational model.

Definition of Done:
- One dedicated page exists with a diagram and narrative walkthrough.
- All related chapters link to it.
- There is at least one end-to-end artifact-level example.

---

## 2. Failure-rich runtime scenarios
Problem, the reference and runtime layer becomes much more useful if it shows not only the happy path, but also failures.

What to do:
- Add scenarios to `agent_runtime_ref`:
  - denied-by-policy
  - approval requested and denied
  - duplicate tool call or retry ambiguity
  - wrong tenant or scope mismatch
  - stale memory retrieval
  - partial execution with compensating action
- For each scenario, show:
  - expected behavior
  - observable signals
  - operator debugging path
  - remediation pattern

Result:
- The runtime reference becomes an operating-learning tool, not just an architecture demo.

Definition of Done:
- At least 5 failure scenarios exist.
- Each has a trace or event sample.
- Each has expected operator notes or a runbook.

---

## 3. Editorial cleanup and navigation
Problem, strong material loses value through heavy navigation and an uneven editorial layer.

What to do:
- Remove mixed language inside one locale.
- Normalize heading style.
- Separate page types with explicit labels:
  - Core Chapter
  - Reference
  - Checklist
  - Case Study
  - Appendix
- Add at the start of every chapter:
  - what the reader will learn;
  - who the chapter is for;
  - what to read next.

Result:
- The book reads less like an evolving knowledge base and more like a coherent technical work.

Definition of Done:
- All chapter entry pages use one consistent format.
- Every chapter has an After this chapter you will be able to block.
- Every chapter has a Read next block.

---

## 4. Outcome-driven chapter structure
Problem, the book is often strong in thesis, but does not always help the reader move to a decision.

What to do:
- Add to each chapter:
  - Key decisions enabled by this chapter
  - Common failure modes
  - What not to overbuild yet
- Add a short decision summary at the end of each chapter.

Result:
- The book helps not only with understanding, but with architectural decision-making.

Definition of Done:
- All key chapters have a standard final block.
- At least 8 chapters are converted to this format.

---

# P1, Depth and evidence strengthening

## 5. Comparative architecture decision guide
Problem, the book explains a preferred architecture well, but is weaker at helping readers choose honestly among alternatives.

What to do:
- Add a dedicated chapter:
  - How to Choose the Smallest Viable Agent Architecture
- Compare common options:
  - deterministic workflow
  - workflow + bounded agent step
  - single-agent loop
  - orchestrated graph
  - handoff-based multi-agent
  - multi-agent collaboration
- For each option, cover:
  - when it fits;
  - when it does not fit;
  - latency cost;
  - debugging cost;
  - blast radius;
  - auditability;
  - operator burden.

Result:
- The book stops being only architecture doctrine and becomes a choice tool.

Definition of Done:
- One full comparative chapter exists.
- At least 5 common architecture patterns are covered.
- A decision rubric or scorecard exists.

---

## 6. Economics of control
Problem, the control layer is well argued, but the cost of control is less visible.

What to do:
- Add a chapter:
  - The Cost of Control
- Cover trade-offs:
  - approval latency vs safety
  - full tracing vs storage and complexity
  - sandboxing vs delivery speed
  - strict policy gating vs operator friction
  - multi-step governance vs product throughput
- Introduce concepts:
  - minimum viable control
  - justified control
  - control overkill

Result:
- The book becomes more mature and honest about engineering economics.

Definition of Done:
- One dedicated chapter or large appendix exists.
- Each control mechanism has when worth it and when overkill criteria.
- There are at least 3 contrasting examples.

---

## 7. Full postmortem case studies
Problem, compact cases help, but they do not deliver the depth of true production postmortems.

What to do:
- Add 3 to 5 large postmortem cases:
  - duplicate external action
  - approval bypass
  - wrong context or tenant leak
  - incident coordination drift
  - memory contamination or stale retrieval
- Case format:
  - context
  - timeline
  - symptoms
  - false leads
  - evidence
  - root cause
  - technical fix
  - org or process fix
  - lessons learned

Result:
- The book gains evidence depth and real operational value.

Definition of Done:
- At least 3 full case studies exist.
- Each contains a timeline and an evidence trail.
- Each ends with an architecture delta and a process delta.

---

## 8. Conflict-heavy cases, not only good-design cases
Problem, cases should teach choice under constraint conflict, not only a preferred model.

What to do:
- Add cases where the answer is genuinely contested:
  - approval before write vs rollback strategy
  - memory write vs retrieval-only
  - one agent vs orchestrated graph
  - shared runtime vs hard tenant isolation
  - centralized policy vs team-local overrides

Result:
- The case layer starts teaching architectural thinking, not only preferred patterns.

Definition of Done:
- At least 2 conflict-heavy cases are added.
- Each one explicitly covers alternatives and cost of choice.

---

# P2, Audience expansion and long-term durability

## 9. Minimal path for small teams
Problem, the book is strong for platform and security-minded readers, but heavy for small teams or early-stage teams.

What to do:
- Add a dedicated track:
  - MVP Without Regret
- Include:
  - what is mandatory from version one;
  - what to defer;
  - minimum tracing;
  - minimum approval model;
  - minimum eval loop;
  - signs that it is time to move to a more mature architecture.

Result:
- The book becomes more useful beyond mature platform teams.

Definition of Done:
- One compact guided path exists.
- A build now vs defer later list exists.
- A migration path from MVP to mature system exists.

---

## 10. Evidence tiers in sources
Problem, the sources list is strong, but it is not always clear what evidentiary weight each source type should carry.

What to do:
- Mark sources with categories:
  - Standards
  - Security guidance
  - Vendor architecture docs
  - Research papers
  - Operational practices
  - Opinionated essays
- Add a note that different sources carry different decision weight.
