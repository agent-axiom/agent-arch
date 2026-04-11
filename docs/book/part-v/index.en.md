# Part V. Reliability and Observability

At this point, we already have the architecture, the security perimeter, memory, and the execution layer. Now the same support agent enters the next phase: it is no longer enough to design and launch it. You need to operate it confidently in the real world.

This part continues the same story:

- in [Chapter 11](chapter-11.en.md), you reconstruct the path of a real failure;
- in [Chapter 12](chapter-12.en.md), you define what system health actually means;
- in [Chapter 13](chapter-13.en.md), you close the learning loop so the same failure does not re-enter rollout.

Without good observability, even a strong architecture quickly collapses into guesswork:

- why a run became more expensive;
- where a workflow actually broke;
- which policy gate fired;
- which tool produced the bad result;
- why the user received that specific answer.

In this part, we break down how to build traces, SLO, and eval loops so the agent system can be not only launched, but also operated steadily after the first impressive demo.

## In This Part

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Chapter 12. SLO for Agent Systems](chapter-12.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)

The next natural step after this part is organizational design: who owns the platform, who owns quality targets, and who decides whether rollout can expand.
