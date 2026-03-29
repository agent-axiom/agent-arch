# Part III. Memory and Knowledge

At this point, the agent is no longer just reasoning, and no longer just using tools safely. The next temptation appears: give it memory so that it does not start every run from zero.

That is the right step, but it is also where many systems start quietly accumulating debt:

- they save everything into memory;
- they do not distinguish profile memory from working context;
- they pull untrusted text back into the prompt without checks;
- they write to memory directly in the hot path, where one mistake becomes persistent immediately.

In this part, we will look at how to make memory useful without turning it into a long-lived source of injections, leaks, and strange behavior.

## In This Part

- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](chapter-5.en.md)
- [Chapter 6. Short-Term, Long-Term, and Profile Memory](chapter-6.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](chapter-7.en.md)

After that, it will make sense to go deeper into retention, deletion, and memory governance.
