# Late-Book Overlap Audit

## Scope

Primary overlap risk was concentrated in:
- Chapter 11
- Chapter 12
- Chapter 13
- Chapter 19
- Chapter 20
- Chapter 21
- Chapter 22
- Chapter 23
- Chapter 24
- Chapter 25
- Chapter 26
- Chapter 27
- Part V and Part VIII framing pages
- appendix schemas and reference-package pages that echo the same governance concepts

## Core diagnosis

The late manuscript is strong in content but was at risk of repeating the same control/governance logic through slightly different lenses:
- tracing
- SLO
- eval loop
- assurance
- behavioral/control evals
- observability
- provenance
- registry
- lifecycle governance

This is useful material, but the jobs-to-be-done need sharper walls.

The newer editorial answer is not only topical separation. It is role clarity plus promise shape: each chapter and part intro should state a distinct reader outcome, so overlap becomes easier to detect and harder to reintroduce by accident.

That same protection now has to apply across genre boundaries too. The book should carry argument and reader transformation, while appendix/reference/package surfaces should anchor, support, and prove. If support pages drift into retelling the same late-book argument, overlap returns in a different costume.

## Current status

A substantial editorial separation pass has now landed.

Already tightened in manuscript:
- Chapter 11 as raw evidence capture
- Chapter 12 as health and risk budget layer
- Chapter 13 as eval judgment layer
- Chapter 19 as lifecycle frame
- Chapter 20 as release judgment layer
- Chapter 21 as assurance response loop
- Chapter 22 as evidence backbone / lineage layer
- Chapter 23 as lifecycle closure layer
- Chapter 24 as adversarial-pressure layer
- Chapter 25 as judgment under adversarial pressure
- Chapter 26 as evidence substrate / detection-ready visibility
- Chapter 27 as estate accountability layer
- Part V reframed around capture, health, judgment
- Part VIII reframed around lifecycle frame, release judgment, response, evidence backbone, lifecycle closure, adversarial pressure, judgment, evidence substrate, accountability

So this audit should now be read as a checkpoint: which overlaps have been reduced, which still need watching, and where promise-shape now helps keep the separation stable.

## Recommended chapter jobs-to-be-done

### Chapter 11
Job: capture raw run history and structured evidence at the execution level.

Should not dominate:
- estate-wide observability claims
- eval judgments
- assurance response logic

### Chapter 12
Job: define health and risk budgets for the running system.

Should not dominate:
- detailed eval mechanics
- tracing implementation details
- broad assurance/governance prose

### Chapter 13
Job: explain how systems learn from failure and prevent recurrence through offline evals, online signals, and regression gates.

Should not dominate:
- adversarial assurance
- registry/governance inventory
- broad lifecycle control

### Chapter 21
Job: explain how findings, drift, and signals become operational response and assurance action.

Should not dominate:
- generic eval pedagogy already covered in Chapter 13
- full observability substrate design
- whole-estate inventory governance

### Chapter 25
Job: explain how behavioral and control evals probe dangerous or deceptive behavior beyond ordinary regression testing.

Should not dominate:
- general online/offline eval framing already in Chapter 13
- full observability architecture
- registry and ownership machinery

### Chapter 26
Job: explain observability as the evidence substrate that makes investigation, control verification, and governance possible.

Should not dominate:
- registry as the main governance layer
- assurance as the main response loop
- generic eval theory

### Chapter 27
Job: explain how inventory, registry, and sprawl control govern an estate of agents, capabilities, principals, and contracts.

Should not dominate:
- observability implementation details except where registry depends on them
- detailed eval mechanics
- broad provenance theory already in Chapter 22

## Severity-ranked overlap findings

### Closed or substantially reduced
1. Chapter 13 and Chapter 25 were blurred around richer grading, verifier outputs, and regression discipline. This is now substantially reduced by explicit judgment-layer framing in both chapters, with Chapter 13 owning the eval loop and Chapter 25 owning adversarial/control pressure.
2. Chapter 21 and Chapter 26 were blurred around signals, drift, evidence, and detection. This is now substantially reduced by explicit response-loop versus evidence-substrate framing.
3. Chapter 26 and Chapter 27 were blurred when telemetry coverage, inventory coverage, and registry governance were all presented as evidence/control surfaces. This is now substantially reduced by explicit evidence versus accountability framing.
4. Chapter 22 and Chapter 26 were blurred around evidence language. This is now substantially reduced by explicit provenance-as-governed-lineage versus observability-as-evidence-substrate framing.
5. Part V and Part VIII framing previously explained too many neighboring concepts at once. This is now substantially reduced by mirrored editorial geometry in both indexes and by turning those indexes into reader-promise pages instead of topic lists.

### Still medium risk
6. Chapter 19 and Chapter 20 can still blur if lifecycle-frame language collapses back into generic change-management language.
7. Chapter 22, Chapter 23, Chapter 27, and appendix lifecycle/reference pages can still repeat lineage / closure / ownership language.
8. Reference-package and schema pages can still drift from anchoring into retelling.
9. Chapter 11 and Chapter 26 must keep a clean boundary between raw trace capture and estate-scale observability evidence.
10. Chapter 12 and Chapter 21 can still blur if health-budget language drifts into response procedure language.
11. Chapter 24 and Chapter 25 can still blur if adversarial-pressure material drifts back into generic eval pedagogy.
12. Part indexes and chapter intros can still regress from outcome promises back into dense inventory-style summaries if future edits accumulate too much topical detail.

## Surgical guidance

### Keep in Chapter 11
- raw run history
- spans and structured events
- capture discipline
- machine-readable execution evidence

### Keep in Chapter 12
- health budgets
- risk budgets
- acceptable degradation
- cost, safety, latency, escalation as operating constraints

### Keep in Chapter 13
- judgment loop
- regression prevention
- dataset refresh from failure
- online/offline relationship

### Keep in Chapter 21
- finding triage
- drift signals
- remediation and assurance response
- operational escalation logic

### Keep in Chapter 25
- adversarial scenarios
- behavioral/control eval design
- oversight evasion / misuse / sabotage-like patterns
- verifier design in the context of dangerous long-horizon judgments

### Keep in Chapter 26
- traces, telemetry, linkage, evidence visibility
- detection-ready data model
- observability conditions for trustworthy control verification

### Keep in Chapter 27
- estate view
- ownership, registry, inventory, sprawl
- who is governed, not just what happened in one run

## Smallest high-impact rewrite sequence

1. keep Part V and Part VIII indexes aligned with the new role grammar and reader-promise shape
2. protect Chapter 11 vs Chapter 26 from collapsing back into one observability blob
3. protect Chapter 12 vs Chapter 21 from collapsing back into one health/response blob
4. trim Chapter 22 / Chapter 27 / appendix repetition where accountability and lineage language starts to duplicate
5. trim reference-package repetition where it retells, not anchors
6. keep planning docs synchronized so the manuscript does not drift back to topic accumulation language
