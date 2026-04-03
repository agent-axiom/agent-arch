# Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky

## 1. Why an Agent Without Memory Quickly Hits a Ceiling

If an agent has no memory, every new run starts almost from a blank page. That is acceptable for simple tasks, but it breaks quickly in real life:

- the agent does not remember user preferences;
- it forgets what it did a minute ago;
- it keeps pulling the same facts again and again;
- it cannot continue a long process carefully.

So memory feels like the natural next step. And that is true. But here there is an important fork: memory can make the agent more useful, or it can make the whole system much less predictable.

## 2. Memory Is Not One Box, but Several Different Layers

When a team says "let's add memory," several different things are usually mixed together:

- short-lived working run context;
- user profile and stable preferences;
- extracted facts about the world and business entities;
- summaries of previous sessions;
- execution artifacts such as trace notes or tool outputs.

If all of this is pushed into one place, chaos begins very quickly. So the first rule is simple: do not design memory as one abstract storage. Design it as a set of different boundaries with different lifetimes, trust levels, and write rules.

<div class="diagram-card">
<p>It is more useful to think about agent memory as several layers, not one database</p>

``` mermaid
flowchart TD
    A["User request"] --> B["Session context"]
    B --> C["Planner / runtime"]
    C --> D["Short-term working memory"]
    C --> E["Profile memory"]
    C --> F["Knowledge retrieval"]
    D --> G["Prompt assembly"]
    E --> G
    F --> G
    G --> H["Model response"]
```

</div>

## 3. The Main Mistake: Treating Memory as Mere Convenience

Memory has one unpleasant property: it survives an individual run. Which means a write error lives longer than an error in one model answer.

If the agent once:

- saved a false fact as a "user preference";
- wrote a piece of untrusted text into profile memory;
- pulled a sensitive document fragment into a summary;
- inserted something into the retrieval store that should never be returned to that tenant,

then the problem becomes persistent. You do not always see it in a single trace. It starts surfacing later, in other dialogs, other prompts, and sometimes for other users.

That is why the memory write path should be treated as a security-sensitive path, not as a "small technical detail."

## 4. Memory Has Its Own Trust Boundaries

It is very useful to see memory not as neutral storage, but as a trust boundary.

There are at least four different data sources:

- trusted system annotations;
- validated outputs of internal services;
- user-provided content;
- content coming from external tools or documents.

Those are not the same. If you save them without source labeling, later the runtime will be unable to understand what can be used as instruction-grade context and what can only be used as reference.

A normal rule looks like this:

- trusted metadata may participate in policy decisions;
- user content should not suddenly become system instruction;
- retrieved text should be treated as untrusted until proven otherwise;
- summaries also have provenance and are not "truth by default."

## 5. The Most Dangerous Path: Writing Memory Directly in the Hot Path Without a Filter

Teams often do this: the model replies, the runtime immediately calls `save_memory()`, and from that point it is treated as convenient automation. In the short term, it looks nice. In the long term, problems almost always appear.

Why that is dangerous:

- the write happens under latency pressure;
- nobody validates what is considered memory-worthy;
- there is no normalization or cleanup step;
- there is no tenant-isolation policy;
- it becomes hard to explain why the fact ended up in memory at all.

That is why even for very "smart" agents it is useful to follow a boring principle: by default, writing to long-term memory should either be explicitly allowed by policy, or moved into a background pipeline.

Here is a simple example of that logic:

```python
from dataclasses import dataclass


@dataclass
class MemoryCandidate:
    kind: str
    tenant_id: str
    content: str
    source: str
    contains_pii: bool = False


def should_persist(candidate: MemoryCandidate) -> bool:
    if candidate.kind not in {"profile_preference", "validated_fact", "session_summary"}:
        return False
    if candidate.source not in {"trusted_service", "approved_summarizer"}:
        return False
    if candidate.contains_pii:
        return False
    return True
```

That code is intentionally very simple. Its strength is not in "smartness," but in the fact that the write rules are visible and auditable.

## 6. A Good Memory System Writes Less Than You Want

At the beginning, almost everyone feels that there should be a lot of memory. In practice, a good memory system usually wins not through volume, but through strictness of selection.

Usually, memory should store only what:

- will be useful in future runs;
- has a clear owner and tenant;
- can be explained to a human;
- does not carry unnecessary sensitive data;
- will not turn the prompt into a dump.

A very useful question before every write is: "If this fragment surfaces three weeks later in another context, will I be comfortable explaining why it is here?"

If the answer feels uncertain, the write is probably unnecessary.

## 7. Memory Affects Not Only Quality, but Also Safety

That is why memory is not just a UX topic:

- it affects data leakage;
- it changes the prompt-injection surface;
- it creates long-lived mistakes;
- it complicates incident investigation;
- it raises the bar for provenance, retention, and deletion.

In a well-built platform, the memory subsystem usually has:

- separate record types;
- retention rules;
- clear ownership;
- provenance metadata;
- deletion and correction mechanisms;
- policy gates before persistent writes.

That is not "chat history" anymore. That is a real architecture layer.

## 8. A Minimal Policy for Writing Into Memory

If you want to start without overcomplicating things, it is useful to think about memory write policy roughly like this:

```yaml
memory:
  allowed_kinds:
    - profile_preference
    - validated_fact
    - session_summary
  deny_sources:
    - raw_user_prompt
    - external_html
    - unvalidated_tool_output
  require_tenant_id: true
  reject_if_contains:
    - secrets
    - access_tokens
    - payment_card_data
  write_mode:
    profile_preference: background_review
    validated_fact: immediate_if_trusted
    session_summary: background_only
```

Again, this is not about magic. It is about making the write path visible and safe.

## 8.1. It Is Useful to Separate Memory Read Policy from Memory Write Policy

One practical idea from recent Google material is that memory should be treated as a governable subsystem, not just as "storage for context."[^google-agent-overview][^google-govern]

That has a direct consequence: **read rules and write rules should almost never be identical**.

For example:

- writing to long-term memory may require validation, provenance, and background review;
- reading from long-term memory may be allowed only through retrieval filters;
- writing to profile memory may require an explicit signal or high confidence;
- reading profile memory may be allowed only to the personalization layer, not to the policy engine.

If those paths are not separated, the system starts living by a dangerous rule: everything that was once written can later be read almost everywhere.

That is not memory design. That is a source of quiet incidents.

## 8.2. Persistent Memory Should Have Provenance by Default

For every record that survives longer than one run, it is useful to store at least:

- `source_type`;
- `source_id`;
- `writer_identity`;
- `tenant_id`;
- `written_at`;
- `confidence` or `validation_state`.

That may feel like extra bureaucracy only until the first argument about where a "fact" came from after the agent confidently repeated it in another context.

## 9. Where to Start If You Have No Memory Yet

If you are only approaching this topic, a good order is:

1. First separate session context and persistent memory.
2. Then define which record types are allowed at all.
3. After that, add provenance and tenant metadata.
4. Only then automate the write path.

If you do it in the opposite order, memory quickly becomes the place where the platform dumps everything it failed to design cleanly.

## 10. What to Read Next

In the next chapters of this part, we will calmly go through:

- how short-term memory differs from long-term memory;
- why profile memory should exist separately from the retrieval store;
- why summaries are better updated in the background;
- how compaction helps keep context clean.

For now, the main takeaway is simple: memory is useful only when it is designed as a controlled system layer, not as uncontrolled accumulation of text.

- [Part III. Memory and Knowledge](index.en.md)
- [Chapter 6. Short-Term, Long-Term, and Profile Memory](chapter-6.en.md)
- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../part-ii/chapter-4.en.md)
- [Sources](../../appendix/sources.en.md)

[^google-agent-overview]: [Google Cloud, Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
