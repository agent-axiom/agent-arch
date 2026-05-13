# Part III. Memory and Knowledge

At this point, the agent is no longer just reasoning, and no longer just approaching actions safely. In the same support case, the next temptation appears: give it memory so it no longer starts every run from zero and can hold onto user history.

!!! info "Short path through this part"
    If you want a fast pass, read it this way:

    - [Chapter 5](chapter-5.en.md): understand why memory is risky at all;
    - [Chapter 6](chapter-6.en.md): separate memory types by role;
    - [Chapter 7](chapter-7.en.md): decide how those records safely return to the prompt.

    Together, these three steps give you a memory layer you can discuss as an engineering system, not as an abstract “let's add memory”.

<div class="book-cover" markdown="1">

![Cover for the memory and knowledge part](../../assets/images/part-iii-memory.png)

</div>

## What This Part Solves

That is the right step, but it is also where many systems start quietly accumulating debt. The same support agent can easily turn useful state into a durable error source unless memory is designed as a controlled layer.

- they save everything into memory;
- they do not distinguish profile memory from working context;
- they pull untrusted text back into the prompt without checks;
- they write to memory directly in the hot path, where one mistake becomes persistent immediately.

In this part, we will look at how to make memory useful without turning it into a long-lived source of injections, leaks, and strange behavior.

## In This Part

- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](chapter-5.en.md)
- [Chapter 6. Short-Term, Long-Term, and Profile Memory](chapter-6.en.md)
  This chapter continues the same support case at the moment the team decides what should still be remembered after the run and what should never harden into memory.
- [Chapter 7. Retrieval, Compaction, and Background Updates](chapter-7.en.md)

## Where It Leads Next

After this part, the natural next move is [Part IV](../part-iv/index.en.md): how the same agent not only remembers context, but acts through controlled tools, sandboxing, and execution contracts.
