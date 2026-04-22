# Part V. Reliability and Observability

By this point, we already have the architecture, the security perimeter, memory, and the execution layer. Now the question changes: how do you operate the system after launch, when it can already fail in live use, get more expensive, drift, and break outside the happy path?

This part answers three practical questions:

- how to reconstruct the real path of one run;
- how to define what system health and acceptable risk actually mean;
- how to turn system behavior into judgments that rollout can use.

!!! info "Short path through this part"
    If you want a fast pass, read it this way:

    - [Chapter 11](chapter-11.en.md): reconstruct the raw history of one real failure;
    - [Chapter 12](chapter-12.en.md): define health and risk budgets;
    - [Chapter 13](chapter-13.en.md): turn system behavior into reviewable judgments;
    - [Evidence Spine](evidence-spine.en.md): see how those layers become one operational record.

<div class="book-cover" markdown="1">

![Cover for the reliability and observability part](../../assets/images/part-v.png)

</div>

## What This Part Solves

- after Chapter 11, you should be able to reconstruct the run path instead of guessing from symptoms;
- after Chapter 12, you should be able to express health and risk budgets through latency, cost, safety, and escalation;
- after Chapter 13, you should be able to produce reviewable judgments about quality and regression risk;
- after Evidence Spine, you should be able to see how traces, policy, approvals, evals, and rollout stay connected as one checkable chain.

## In This Part

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Chapter 12. SLO for Agent Systems](chapter-12.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)
- [Evidence Spine: From Request to Rollout Judgment](evidence-spine.en.md)

## Where It Leads Next

Once the system can capture behavior, define budgets, and produce judgments, the next question becomes ownership. That is why the natural next step after this part is [Part VI](../part-vi/index.en.md): who owns these promises inside the real organization?
