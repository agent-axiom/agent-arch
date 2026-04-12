# Chapter 7. Retrieval, Compaction, and Background Updates

## 1. Memory Is Useless If You Cannot Pull the Right Things Back Out

Once you have separated short-term, long-term, and profile memory, the next practical question appears: how exactly should the agent bring the right records back into the prompt?

This is where many systems begin to degrade:

- too much irrelevant context flies into the prompt;
- retrieval returns similar but not useful records;
- summaries grow but do not become clearer;
- each new iteration only makes the context heavier.

So the problem is no longer that memory exists. The problem is that memory has become too noisy and too expensive to read.

## 2. Retrieval Is Not "Find Everything Similar," but "Select What Helps Solve the Current Task"

Retrieval has a bad habit: if you do not constrain it, it tries to be too generous. Then the prompt gets not the most useful context, but the most similar one by embedding or keyword overlap.

For production systems, it is more useful to think like this:

- retrieval does not have to return a lot;
- retrieval has to be explainable;
- retrieval must respect tenant, source, and trust boundaries;
- retrieval must obey the context-size budget.

A normal retrieval pipeline almost always takes into account not only similarity, but also:

- tenant isolation;
- memory class;
- recency;
- confidence;
- provenance;
- policy filters.

## 3. A Good Prompt Loves Signal Density, Not Completeness

It is very tempting to think "the more context, the smarter the agent." In practice, the opposite is often true: the more garbage you put into the prompt, the worse the model holds priorities.

That is why retrieval should answer not the question "what can we fetch?", but "what increases the chance of the right decision right now?"

A useful practical rule:

- better 3 highly relevant records than 20 vaguely similar ones;
- better a small summary with a source than a long raw document;
- better one profile hint than a whole preference history;
- better empty retrieval than retrieval with no trust and no explainability.

## 4. Compaction Is Not Cosmetic. It Is How You Keep the System Workable

If the memory layer only grows, sooner or later prompt assembly starts behaving like a garbage collector with no rules. That is why compaction should be part of the architecture, not a one-time cleanup project.

Compaction can mean different things:

- compress several records into a summary;
- remove outdated working notes;
- merge duplicates;
- replace a large blob with a normalized record plus a source link;
- lower the priority of old records instead of keeping them forever in the foreground.

<div class="diagram-card">
<p>It is useful to think of retrieval and compaction as one maintenance loop for memory</p>

``` mermaid
flowchart TD
    A["New run"] --> B["Query memory"]
    B --> C["Apply filters and ranking"]
    C --> D["Assemble prompt context"]
    D --> E["Model + tools"]
    E --> F["Create new memory candidates"]
    F --> G["Background compaction and review"]
    G --> H["Normalized memory store"]
    H --> B
```

</div>

## 5. Not All Memory Updates Belong in the Hot Path

This is one of the most useful architectural shifts for agent systems. At first, almost everyone tries to make memory "instantly ready": the agent sees something, immediately rewrites summaries, updates the profile, saves knowledge.

But that is almost always too expensive and too risky.

What usually belongs in the hot path:

- minimal session state;
- short working notes;
- safe transient records with clear TTL;
- an update without which the current workflow actually breaks.

What is usually better in the background:

- compaction of long sessions;
- rebuilding summaries;
- fact normalization;
- deduplication;
- review of memory candidates before persistent write.

Background updates are what let memory stay clean instead of merely fast.

## 6. A Good System Separates Retrieval Query and Maintenance Jobs

In a mature architecture, there are almost always two different loops:

- read path: quickly and safely fetch context for the current run;
- maintenance path: calmly improve the memory store without latency pressure.

This matters not only for performance, but also for decision quality. When one chain simultaneously:

- executes the task;
- rebuilds summaries;
- writes profile memory;
- cleans duplicates;
- updates ranking metadata,

it quickly becomes fragile and hard to explain.

## 6.1. Frontier memory is moving toward adaptive shaping, but production still needs discipline

Recent memory research pushes the architecture further: not only to store records and compact them occasionally, but to gradually reshape the memory layer around actual usage patterns.

That is promising because it points toward a smarter system:

- summaries can evolve;
- memory classes can become richer;
- the store can better reflect recurring tasks.

But this is exactly where it is important not to skip operational discipline.

Until a team has stable:

- provenance rules;
- revision semantics;
- reviewable memory writes;
- traceable maintenance jobs;
- a rollback path for derived artifacts,

adaptive memory shaping is better treated as a research direction, not as a default production pattern.

Practically, this means something simple: evolving memory is worth studying, but the live system contour should still rest on explainable retrieval, controlled compaction, and verifiable record provenance.

## 7. Example Policy for Retrieval and Background Updates

Here is a very practical template. It does not try to be universal, but it shows well which decisions are worth making explicit.

```yaml
retrieval:
  max_records: 5
  max_tokens: 1800
  allowed_classes:
    - short_term
    - long_term
    - profile
  require_tenant_match: true
  min_confidence: 0.75
  deny_sources:
    - raw_external_html
    - unreviewed_summary

compaction:
  run_mode: background_only
  summary_max_tokens: 400
  deduplicate: true
  merge_similar_records: true
  drop_expired_short_term: true
```

When rules like that are explicit, the team stops arguing about memory at the level of intuition. It argues about real constraints and trade-offs.

## 8. A Simple Code Example of Ranking Before Prompt Assembly

Below is not a "smart" retrieval engine, but a deliberately readable example. It shows that ranking is useful to build not only on similarity, but also on trust, freshness, and importance.

```python
from dataclasses import dataclass


@dataclass
class RetrievedRecord:
    text: str
    similarity: float
    confidence: float
    recency_weight: float
    trusted: bool


def score(record: RetrievedRecord) -> float:
    trust_bonus = 0.15 if record.trusted else -0.2
    return (
        record.similarity * 0.5
        + record.confidence * 0.25
        + record.recency_weight * 0.1
        + trust_bonus
    )


def select_for_prompt(records: list[RetrievedRecord], limit: int = 3) -> list[RetrievedRecord]:
    ranked = sorted(records, key=score, reverse=True)
    return ranked[:limit]
```

That logic is rough, but it has one important virtue: you can discuss it, test it, and gradually replace it with something more precise without losing explainability.

## 9. Summaries Should Help Reading, Not Hide Data Provenance

Teams often use summaries as a way to "fit more memory into fewer tokens." That is fine, but there is one trap: a summary must not turn into a new anonymous truth.

A good summary:

- is shorter than the original records;
- keeps provenance;
- does not mix tenants;
- does not lose critical constraints;
- is marked as a derived artifact, not a raw fact.

A bad summary:

- sounds confident, but no one knows where it came from;
- merges conflicting facts;
- loses date and data owner;
- is fed to the model as a trusted instruction.

## 10. Common Mistakes

The same problems repeat:

- duplicates get into the prompt;
- retrieval ignores class boundaries;
- ranking ignores trust;
- summaries become too generic;
- background jobs are missing and memory only inflates;
- nobody knows why this exact chunk was retrieved.

The last point is especially important. If you cannot explain why a piece of context landed in the prompt, then the system is already poorly controlled.

## 11. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Is there a limit on record count and token budget?
- Does ranking consider not only similarity, but also confidence, recency, and trust?
- Are the read path and maintenance path separated?
- Is compaction a regular process, not manual cleaning?
- Can you see provenance on a summary?
- Is there protection against retrieval across another tenant or the wrong class?

If the answer is "no" several times in a row, then you already have memory, but you do not yet have memory discipline.

## 12. What to Do Next

At this point, the basic part about memory is already coming together. From here it makes sense either to go deeper into retention and deletion, or to move to the section about tools and execution.

- [Chapter 6. Short-Term, Long-Term, and Profile Memory](chapter-6.en.md)
- [Research Frontier: Memory, Observability, and Multi-Agent Reliability](../../appendix/research-frontier.en.md)
- [Chapter 8. Execution Model and Tool Catalog](../part-iv/chapter-8.en.md)
- [Part III. Memory and Knowledge](index.en.md)
- [Sources](../../appendix/sources.en.md)
