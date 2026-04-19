# Part V. Reliability and Observability

At this point, we already have the architecture, the security perimeter, memory, and the execution layer. Now the same support agent enters the next phase: it is no longer enough to design and launch it. You need to operate it confidently in the real world.

This part continues the same story:

- in [Chapter 11](chapter-11.en.md), you reconstruct the raw path of a real failure;
- in [Chapter 12](chapter-12.en.md), you define what system health and risk budgets actually mean;
- in [Chapter 13](chapter-13.en.md), you produce reviewable judgments so the same failure does not re-enter rollout.

!!! info "Short path through this part"
    If you want a fast pass, read it this way:

    - [Chapter 11](chapter-11.en.md): capture the raw run history of one real failure;
    - [Chapter 12](chapter-12.en.md): define the health and risk budgets the system is allowed to consume;
    - [Chapter 13](chapter-13.en.md): turn behavior into reviewable eval judgments for rollout.

    Together, this shows how an agent system moves from “something works” to controlled operation through three distinct layers: capture, health, and judgment.

    It also sets up the next structural addition to the book: an explicit Evidence Spine page that will connect request, policy, approval, traces, evals, incidents, and rollout into one governed operating record.

Without good observability, even a strong architecture quickly collapses into guesswork:

- why a run became more expensive;
- where a workflow actually broke;
- which policy gate fired;
- which tool produced the bad result;
- why the user received that specific answer.

In this part, we break down how to build traces, SLO, and eval loops so the agent system can be not only launched, but also operated steadily after the first impressive demo.

The editorial boundary matters here. Tracing is the raw capture layer. SLO are the health-and-budget layer. Evals are the judgment layer. Later chapters in the book will build assurance, observability, and governance on top of those foundations rather than collapsing them together too early.

## What This Part Solves

This part makes three distinct promises to the reader:

- after Chapter 11, you should be able to reconstruct the real run path instead of guessing from symptoms;
- after Chapter 12, you should be able to state explicit health and risk budgets through SLO, cost, safety, and escalation;
- after Chapter 13, you should be able to produce reviewable judgments through offline evals, online signals, and regression gates.

## In This Part

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Chapter 12. SLO for Agent Systems](chapter-12.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)

## Where It Leads Next

The next natural step after this part is twofold.

First, the book now needs one explicit Evidence Spine bridge so the reader can see how traces, policy decisions, approvals, evals, incidents, and rollout judgments stay connected as one operational record.

Second, it needs organizational design: who owns the platform, who owns quality targets, and who decides whether rollout can expand.

That is why Part VI follows naturally from Part V. Once you can capture behavior, define tolerated budgets, and judge changes, the next question is ownership: who is responsible for those promises in the real organization.
