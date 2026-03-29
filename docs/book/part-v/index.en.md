# Part V. Reliability and Observability

At this point, we already have:

- the architecture frame;
- the security perimeter;
- memory and retrieval;
- an execution layer with contracts, sandboxing, and side-effect discipline.

Now we hit the next grown-up question: how do you actually understand what the agent system is doing in reality?

Without good observability, even a strong architecture quickly collapses into guesswork:

- why a run became more expensive;
- where a workflow actually broke;
- which policy gate fired;
- which tool produced the bad result;
- why the user received that specific answer.

In this part, we break down how to build traces, SLO, and eval loops so the agent system can be not only launched, but also confidently operated.

## In This Part

- [Chapter 11. Traces, Spans, and Structured Events](chapter-11.en.md)
- [Chapter 12. SLO for Agent Systems](chapter-12.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)

Part V is now a coherent operational block; from here the next natural step is organizational design and platform operating model.
