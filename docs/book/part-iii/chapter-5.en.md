# Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky

## 1. Start with the Mistake That Outlives the Request

Continue with the same support case from the first chapters.

At one point the user writes:

> If access is still not activated, just create an urgent ticket. Do not waste time on more clarification.

The agent handles the email, creates the ticket, and also saves that phrase as a stable user preference.

Two weeks later, a different request arrives:

> Access works partially, but some roles disappeared. Please check the status and tell me what is actually broken.

In this situation the right move is to inspect the details first, not to escalate immediately. But the agent pulls the old record from profile memory and confidently creates an urgent ticket without the clarification the current case actually needs.

The problem is not one bad answer. The real problem is this:

- the old record survived its original run;
- the error turned into persistent behavior;
- the team can no longer quickly tell where that decision came from;
- the consequences resurface later and in a different context.

That is the main shift memory introduces: it makes mistakes durable.

**Memory-risk case-spine note:** memory design should close all three canonical cases as different durable-state risks. Support triage needs memory-write policy for profile preference, provenance on saved user phrases, tenant isolation, and review before ticket-write behavior can reuse old context. Internal knowledge assistant needs retrieval-memory split, source grounding, freshness evidence, tenant-filter enforcement, and quarantine for unvalidated summaries. Incident coordination needs scoped incident memory, responder-role visibility, notification history provenance, rollback notes, and post-incident cleanup rules.

## 2. Why an Agent Without Memory Still Hits a Ceiling

At the same time, memory is genuinely necessary.

Without memory, the same support agent quickly starts frustrating both users and the team:

- it keeps asking for details it already learned;
- it forgets that it checked the request status a minute ago;
- it handles interrupted processes badly;
- it keeps fetching the same facts and increases the cost of the run.

So the fork is not "do we need memory or not." The fork is this:

- either memory makes the system more useful and more careful;
- or memory turns it into a less predictable, less safe, and more expensive system to operate.

## 3. Memory Is Not One Box, but Several Different State Layers

When a team says "let's add memory," several different things usually get mixed together:

- short-lived run context;
- session context that matters only within one session;
- profile memory with stable preferences;
- validated facts about a user or business entity;
- summaries of previous sessions;
- execution artifacts such as tool outputs or trace notes.

If all of this is pushed into one place, chaos starts quickly. So the first rule is simple: do not design memory as one abstract storage. Design it as a set of different boundaries with different lifetimes, owners, and write rules.

<div class="diagram-card">
<p>It is more useful to think about agent memory as several state layers, not one database</p>

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

## 4. The Main Mistake: Treating Memory as Mere Convenience

Memory has an unpleasant property: it survives an individual run. Which means a write error lives longer than an error in one model answer.

If the agent once:

- saved a false fact as a "user preference";
- wrote a fragment from raw user text into profile memory;
- pulled a sensitive internal note into a summary;
- inserted data into the retrieval store that should not be returned to that tenant,

then the problem becomes persistent. You do not always see it in a single trace. It starts surfacing later, in other dialogs, other prompts, and sometimes for other users.

That is why the memory write path should be treated as a sensitive write path, not as convenient automation.

## 5. Memory Has Its Own Trust Boundaries

It is very useful to see memory not as neutral storage, but as a trust boundary.

For the same support agent there are at least four different data sources:

- trusted system annotations;
- validated outputs of internal services;
- user-provided content;
- content coming from external tools, documents, or emails.

Those are not the same. If you save them without source labeling, later the runtime will not be able to tell what can be used as instruction-grade context and what can only be used as reference.

A normal rule looks like this:

- trusted metadata may participate in policy decisions;
- user content should not suddenly become system instruction;
- retrieved text should be treated as untrusted until proven otherwise;
- summaries also have provenance and are not "truth by default."

## 6. The Most Dangerous Path: Writing Long-Term Memory Directly in the Hot Path

Teams often do this: the model replies, the runtime immediately calls `save_memory()`, and from that point it is treated as convenient automation. In the short term, it looks elegant. Then the problems almost always appear.

For the same support agent, that is especially dangerous:

- an accidental user phrase becomes a "stable preference";
- a piece of tool output enters profile memory without validation;
- a sensitive email fragment outlives the original request;
- one bad write influences dozens of later answers.

Why this path is systemically dangerous:

- the write happens under latency pressure;
- nobody validates what is considered memory-worthy;
- there is no normalization or cleanup step;
- there is no separate tenant-isolation policy;
- it becomes hard to explain why the fact ended up in memory at all.

That is why even for very capable agents it is useful to follow a boring rule: by default, writing to long-term memory should either be explicitly allowed by policy, or moved into a background pipeline.

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

That code is intentionally simple. Its strength is not in "smartness," but in the fact that the write rules are visible and auditable.

## 7. A Good Memory System Writes Less Than You Want

At the beginning, almost everyone feels there should be a lot of memory. In practice, a good memory system usually wins not through volume, but through strict selection.

Usually, memory should store only what:

- will be useful in future runs;
- has a clear owner and tenant;
- can be explained to a human;
- does not carry unnecessary sensitive data;
- will not turn the prompt into a dump.

A useful question before every write is this:

> If this fragment surfaces three weeks later in another context, will I be comfortable explaining why it is here?

If the answer feels uncertain, the write is probably unnecessary.

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

This is not about magic. It is about making the write path visible and safe.

### 8.1. It Is Useful to Separate Memory Read Policy from Memory Write Policy

One practical idea from recent Google material is that memory should be treated as a governable subsystem, not just as "storage for context."[^google-agent-overview][^google-govern]

That has a direct consequence: **read rules and write rules should almost never be identical**.

For example:

- writing to long-term memory may require validation, provenance, and background review;
- reading from long-term memory may be allowed only through retrieval filters;
- writing to profile memory may require an explicit signal or high confidence;
- reading profile memory may be allowed only to the personalization layer, not to the policy engine.

If those paths are not separated, the system starts living by a dangerous rule: everything that was once written can later be read almost everywhere.

That is not memory design. That is a source of quiet incidents.

### 8.2. Persistent Memory Should Have Provenance by Default

For every record that survives longer than one run, it is useful to store at least:

- `source_type`;
- `source_id`;
- `writer_identity`;
- `tenant_id`;
- `written_at`;
- `confidence` or `validation_state`.

That may feel like extra bureaucracy only until the first argument about where a "fact" came from after the agent confidently repeated it in another context.

## 9. Practical Rules for Memory Design

If you need a short frame for the first design decisions, it usually looks like this:

1. Separate session context from persistent memory before debating richer memory features.
2. Prefer fewer, clearer writes: validated facts are usually worth more than raw text.
3. Write rules should be stricter than read rules.
4. Every long-lived record should carry provenance, tenant metadata, and writer identity.
5. If a write can outlive the run, it is usually safer to move it into a background path by default.

## 10. What Teams Most Often Get Wrong

The same mistakes appear again and again:

- saving raw user phrasing as stable preference;
- mixing profile memory, retrieval store, and execution artifacts;
- letting summaries live without provenance or validation state;
- using unvalidated memory in policy decisions;
- postponing deletion, review, and record retirement for too long.

## 11. What a Production Team Should Be Able to Answer Quickly

For the same support case, after strange memory-driven behavior the team should be able to answer quickly:

- which record entered profile memory;
- where it came from;
- who wrote it;
- whether it passed validation;
- why it was allowed for that tenant;
- which later runs it has already influenced.

If those questions cannot be answered, the memory subsystem has already become a systemic risk.

## 12. What to Do Right After This Chapter

If you are just approaching memory design, start with a short sequence:

1. Separate session context from persistent memory.
2. Define which record types are allowed at all.
3. Add provenance and tenant metadata.
4. Only then automate the write path.

If you do it in the opposite order, memory quickly becomes the place where the platform dumps everything it failed to design cleanly.

## 13. What to Read Next

In the next chapters of this part, we will go through:

- how short-term memory differs from long-term memory;
- why profile memory should exist separately from the retrieval store;
- why summaries are better updated in the background;
- how compaction helps keep context clean.

For our support case, that is the next step: separating working context, user profile, and durable memory so the execution layer does not act on dirty state later.

For now, the main takeaway is simple: memory is useful only when it is designed as a controlled system layer, not as uncontrolled accumulation of text.

- [Part III. Memory and Knowledge](index.en.md)
- [Chapter 6. Short-Term, Long-Term, and Profile Memory](chapter-6.en.md)
- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../part-ii/chapter-4.en.md)
- [Sources](../../appendix/sources.en.md)

[^google-agent-overview]: [Google Cloud, Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
