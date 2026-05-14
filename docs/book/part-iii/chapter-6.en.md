# Chapter 6. Short-Term, Long-Term, and Profile Memory

!!! info "How to read this chapter"
    It helps not to hold all definitions at once, but to keep one simple question in mind:

    - what from this run matters right now;
    - what may be useful later;
    - what really belongs to durable user preference rather than random noise.

    When those three categories are mixed together, the memory layer stops helping and starts quietly damaging the system.

## 1. Why the Single Word "Memory" Only Gets in the Way

In the running support case, this becomes very concrete. After one run, the team may feel tempted to save everything:

- intermediate checking steps;
- a temporary case summary;
- the user's communication language;
- random observations that should not survive a single run at all.

This is exactly where memory types stop being vocabulary and become an architectural decision.

As soon as memory appears in a system, the team feels tempted to use one word for everything that does not fit into the current prompt. That is a convenient abstraction for conversation, but a bad abstraction for architecture.

In practice, you almost always have at least three different layers:

- `short-term memory` for the current run or a short chain of steps;
- `long-term memory` for durable knowledge, summaries, and facts;
- `profile memory` for preferences, roles, and habits of a specific user or account.

!!! example "Case thread: classifying support state"
    In the support-triage case, the current ticket status belongs in short-term memory, a normalized post-run note may become long-term memory, and the user's preferred communication language may belong in profile memory. The raw sentence "always create urgent tickets" should belong to none of them unless a policy-backed review explicitly validates it.

**Memory case-spine note:** the three canonical cases stress different memory failures. Support triage tests whether temporary ticket state is kept separate from durable notes and profile preferences. Internal knowledge assistant tests source provenance, freshness, tenant boundaries, and retrieval semantics. Incident coordination tests whether handoff summaries, response roles, and post-incident lessons are preserved without turning transient incident noise into permanent truth.

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

### 4.1. Durable Agent State Is Not Memory

Cloudflare Agents SDK highlights another boundary: a stateful agent instance may have persistent state that is automatically saved, survives restarts and hibernation, and synchronizes across WebSocket clients.[^cloudflare-state] That is a useful runtime capability, but it should not automatically be treated as long-term memory or profile memory.

`state` answers “what condition is this named agent instance in right now”: a game score, open case, current workflow, client-visible settings, or last-active marker. `memory` answers “what information should later be retrieved, summarized, or reused as knowledge.” If those roles are mixed, runtime state starts entering retrieval as if it were validated knowledge, while memory records get used as mutable UI/session state.

The practical rule is simple: durable state should have an owner instance, schema version, serialization constraints, and sync policy; a memory record should have a class, provenance, tenant boundary, retention rule, and retrieval semantics. Both layers may live in durable storage, but their operational contracts are different.

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

### 6.1. Each Layer Needs Its Own Revision Rules

Another useful step toward a mature architecture is this: different memory classes should have different update and correction rules.

For example:

- `short-term memory` can often just be replaced or dropped;
- `long-term memory` is usually safer to update through a new revision than by silently overwriting the old one;
- `profile memory` often needs especially careful merges, because it is easy to corrupt personalization.

If revisions do not exist at all, later you only see "the current state of the record," but you no longer understand:

- who changed it;
- why it changed;
- which version existed before;
- whether the update was validated or was just a side effect of one more run.

### 6.2. Provenance Should Be Designed Together with Memory Classes

Provenance is better designed together with memory classes, not bolted on later.[^google-agent-overview]

In practice, this means:

- `long_term` records should almost always have a source link or source id;
- `profile` records need an explainable reason why the system decided that this is a stable preference;
- `short_term` records can have lighter provenance, but the runtime should still understand where they came from.

Here is a compact example:

```yaml
memory_classes:
  short_term:
    revision_mode: replace
    provenance: minimal_runtime_metadata
  long_term:
    revision_mode: append_revision
    provenance: source_link_required
  profile:
    revision_mode: merge_with_history
    provenance: explicit_signal_or_review
```

That moves the discussion from "where do we store text" to "what is the history of this knowledge, and how much should we trust it."

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

## 11. Common Mistakes

Usually the problems look like this:

- profile memory starts replacing authorization;
- long-term memory fills with noise;
- short-term memory becomes too large and too expensive;
- retrieval returns records without regard to class;
- nobody can explain why exactly this fragment ended up in the answer.

None of that is a "model defect." Those are memory-layer architecture defects.

## 12. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Do you understand how short-term memory differs from long-term memory?
- Does profile memory have separate semantics, not just a separate table?
- Can you explain the TTL for each record type?
- Is it clear which memory layer enters the prompt directly and which only through retrieval?
- Do long-term records have provenance?
- Can a record be safely deleted or corrected?

If these questions are hard to answer, the memory architecture should be simplified and separated by role.

## 13. What to Do Next

First separate memory classes and retention rules, then move to retrieval, compaction, and background updates.

The next step in this part is very natural: after memory types, we need to look at how the agent pulls the right fragments back into the prompt and why compaction is sometimes more important than "more retrieval."

- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](chapter-5.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](chapter-7.en.md)
- [Part III. Memory and Knowledge](index.en.md)
- [Sources](../../appendix/sources.en.md)

[^cloudflare-state]: [Cloudflare Agents SDK, Store and sync state](https://developers.cloudflare.com/agents/api-reference/store-and-sync-state/)

[^google-agent-overview]: [Google Cloud, Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
