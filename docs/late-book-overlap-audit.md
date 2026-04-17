# Late-Book Overlap Audit

## Scope

Primary overlap risk is concentrated in:
- Chapter 13
- Chapter 21
- Chapter 25
- Chapter 26
- Chapter 27
- Part VIII framing pages
- appendix schemas and reference-package pages that echo the same governance concepts

## Core diagnosis

The late manuscript is strong in content but at risk of repeating the same control/governance logic through slightly different lenses:
- eval loop
- assurance
- behavioral/control evals
- observability
- provenance
- registry
- lifecycle governance

This is useful material, but the jobs-to-be-done need sharper walls.

## Recommended chapter jobs-to-be-done

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

### High severity
1. Chapter 13 and Chapter 25 can blur when both discuss richer grading, verifier outputs, and regression discipline.
2. Chapter 21 and Chapter 26 can blur when both discuss signals, drift, evidence, and detection.
3. Chapter 26 and Chapter 27 can blur when telemetry coverage, inventory coverage, and registry governance are all presented as evidence/control surfaces.

### Medium severity
4. Chapter 22, Chapter 27, and appendix lifecycle/reference pages can repeat provenance / ownership / contract lineage language.
5. Part VIII framing may try to explain too many late-book concepts at once.

### Low severity
6. Reference-package pages sometimes restate chapter claims instead of only anchoring them.

## Surgical guidance

### Keep in Chapter 13
- learning loop
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

1. tighten Part VIII framing so each late chapter has one sentence of unique responsibility
2. line-edit Chapter 13 and Chapter 25 to reduce conceptual echo
3. line-edit Chapter 21 and Chapter 26 to distinguish response loop vs evidence substrate
4. line-edit Chapter 26 and Chapter 27 to distinguish telemetry visibility vs estate governance
5. trim reference-package repetition where it retells, not anchors
