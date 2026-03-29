# Chapter 6. Short-Term, Long-Term, and Profile Memory

## 1. Why the Single Word "Memory" Only Gets in the Way

As soon as memory appears in a system, the team feels tempted to use one word for everything that does not fit into the current prompt. That is a convenient abstraction for conversation, but a bad abstraction for architecture.

In practice, you almost always have at least three different layers:

- `short-term memory` for the current run or a short chain of steps;
- `long-term memory` for durable knowledge, summaries, and facts;
- `profile memory` for preferences, roles, and habits of a specific user or account.

If those layers are not separated, the agent starts to:

- return too much old noise into the prompt;
- confuse user preferences with facts about the world;
- save transient observations as durable truth;
- break explainability because it is no longer clear where a given context fragment came from.

## 2. Short-Term Memory Is a Desk, Not an Archive

It is easiest to think of short-term memory as the agent's desk. It is not "history forever," but the thing that helps the agent not lose the current thread.

Usually it contains:

- an intermediate plan;
- results of recent tool calls;
- temporary hypotheses;
- selected context chunks for the current run;
- state for a multi-step workflow.

A good short-term memory has three properties:

- it is bounded in size;
- it has a short lifetime;
- it can be lost after the task finishes without pain.

If "forever records" start living in short-term memory, that is already a sign that you do not have a data model. You just have an overloaded buffer.

## 3. Long-Term Memory Is Not for Everything, but for Durable Knowledge

Long-term memory is needed where the value of a record survives one dialog or one workflow.

That may include:

- a confirmed fact about a business entity;
- a summary of a previous session;
- accumulated knowledge about a long-running case;
- an extracted and normalized note for future retrieval.

But there is an important filter: if a record cannot reasonably be used later without the full original context, then it probably does not belong in long-term memory.

This is where teams often overestimate the value of raw saves. In long-term memory it is usually better to store meaningful typed records, not an endless stream of everything.

## 4. Profile Memory Is Not a Knowledge Base

Profile memory is especially easy to corrupt because it sounds harmless. It feels like it is "just user preferences." But in production, profile memory quickly becomes a sensitive layer.

It usually includes:

- communication language;
- response format;
- working role;
- allowed action channels;
- stable interface or interaction preferences.

The important distinction is that profile memory answers the question "how should the system work with this person," not "what is true in the world."

If the agent starts putting arbitrary facts there, profile memory turns into a muddy mix of personalization, rumors, and accidental observations.

<div class="diagram-card">
<p>Different memory types solve different problems and should not collapse into one storage</p>

``` mermaid
flowchart LR
    A["Current run"] --> B["Short-term memory"]
    A --> C["Long-term memory"]
    A --> D["Profile memory"]
    B --> E["Planner state"]
    B --> F["Recent tool outputs"]
    C --> G["Validated facts"]
    C --> H["Session summaries"]
    D --> I["Preferences"]
    D --> J["User constraints"]
```

</div>

## 5. A Good Architecture Gives Each Layer Its Own Question

This helps a lot during design:

- `short-term memory`: what do we need to remember right now to avoid losing the task?
- `long-term memory`: what is worth saving because it will matter later?
- `profile memory`: what about this user or account is actually stable and useful?

If a record answers none of those questions, maybe it does not need to be saved at all.

## 6. Each Layer Needs Its Own Read and Write Rules

The most common architectural mistake here is that one pipeline reads and writes all memory types in exactly the same way. That is almost always wrong.

For example:

- short-term memory can be read more freely, but stored for a very short time;
- long-term memory should require provenance and tenant checks;
- profile memory should be especially strict about privacy, consent, and explainability.

A normal system knows not only **what** it stores, but also **how exactly** each category gets into the prompt.

```yaml
memory_classes:
  short_term:
    ttl: "2h"
    read_path: "runtime_only"
    write_policy: "immediate"
  long_term:
    ttl: "90d"
    read_path: "retrieval_with_filters"
    write_policy: "validated_only"
  profile:
    ttl: "365d"
    read_path: "personalization_only"
    write_policy: "explicit_or_high_confidence"
```

That YAML does not have to be the final implementation. But it forces the team to make an important decision: memory cannot be managed at the level of "well, it is just text in a database."

## 7. What Usually Belongs in Short-Term Memory

A useful practical rule: short-term memory should help the agent act now, not become a source of long-term truth.

Good candidates:

- the current plan;
- subtask status;
- results of the last two or three tool calls;
- working notes about what has already been checked;
- temporary candidate summaries.

Bad candidates:

- "forever" user preferences;
- uncleaned raw documents;
- huge logs;
- sensitive data without TTL;
- unconfirmed facts that will later be repeated as truth.

## 8. What Usually Belongs in Long-Term Memory

Long-term memory exists for reusing knowledge, not for archiving all activity.

Reasonable things to store there:

- confirmed facts;
- careful summaries with provenance;
- states of long-running cases;
- normalized knowledge records;
- links to documents rather than giant raw payloads copied whole.

A very useful principle: in long-term memory it is often better to store a compact record and a link to the source, rather than try to turn memory storage into a permanent dump of all content.

## 9. What Usually Belongs in Profile Memory

Profile memory is useful when it helps the agent become easier to work with, without starting to make decisions for the user based on shaky guesses.

Good examples:

- "prefers short answers";
- "usually works in Russian";
- "requires confirmation for changes to production data";
- "receives reports at the end of the day."

Bad examples:

- conclusions about motivation or personality;
- random assumptions from one session;
- sensitive personal data without a clear reason;
- guesses that later get used as facts.

## 10. A Simple Code Template for Routing Memory Records

Below is a very simple example that shows the core idea: a record is classified first, and only then sent to the appropriate storage.

```python
from dataclasses import dataclass


@dataclass
class MemoryRecord:
    kind: str
    content: str
    confidence: float


def select_memory_bucket(record: MemoryRecord) -> str | None:
    if record.kind in {"plan_step", "tool_result", "working_note"}:
        return "short_term"
    if record.kind in {"validated_fact", "session_summary", "case_state"} and record.confidence >= 0.8:
        return "long_term"
    if record.kind in {"language_preference", "format_preference", "approval_preference"}:
        return "profile"
    return None
```

This example is intentionally very direct. In practice the rules will be richer, but the core idea should remain the same: memory is classified first, not dumped blindly into one shared container.

## 11. Where Teams Most Often Break

Usually the problems look like this:

- profile memory starts replacing authorization;
- long-term memory fills with noise;
- short-term memory becomes too large and too expensive;
- retrieval returns records without regard to class;
- nobody can explain why exactly this fragment ended up in the answer.

None of that is a "model defect." Those are memory-layer architecture defects.

## 12. Practical Checklist

If you want to review your design quickly, ask:

- Do you understand how short-term memory differs from long-term memory?
- Does profile memory have separate semantics, not just a separate table?
- Can you explain the TTL for each record type?
- Is it clear which memory layer enters the prompt directly and which only through retrieval?
- Do long-term records have provenance?
- Can a record be safely deleted or corrected?

If these questions are hard to answer, the memory architecture should be simplified and separated by role.

## 13. What to Read Next

The next step in this part is very natural: after memory types, we need to look at how the agent pulls the right fragments back into the prompt and why compaction is sometimes more important than "more retrieval."

- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](chapter-5.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](chapter-7.en.md)
- [Part III. Memory and Knowledge](index.en.md)
- [Sources](../../appendix/sources.en.md)
