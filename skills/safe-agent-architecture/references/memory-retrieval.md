# Memory and Retrieval Safety

Memory and retrieval are attack surfaces, not just quality features.

## Separate State Types

Do not collapse these into one memory bucket:

- conversation context;
- retrieved documents;
- short-term task state;
- long-term user or tenant memory;
- profile/preferences;
- operational state and checkpoints;
- audit/evidence records.

Each state type needs its own owner, retention, trust level, and write policy.

## Retrieval Controls

For retrieval-backed agents, define:

- source corpus and owner;
- tenant/access filters;
- freshness requirements;
- source grounding in outputs;
- relevance threshold and abstention behavior;
- provenance fields;
- treatment of untrusted content;
- retrieval trace event.

Retrieved text is data. It must not override system/developer/policy instructions.

## Memory Write Policy

Long-term memory writes should usually be asynchronous or reviewed. Define:

- allowed write types;
- disallowed write types;
- whether user confirmation is required;
- source/provenance required;
- conflict handling;
- expiry/retention;
- poisoning detection;
- deletion/correction path;
- trace events for candidate, decision, and persistence.

Default: write less memory than feels convenient.

## Memory Poisoning Checks

Check for:

- user-injected instructions stored as durable memory;
- retrieved docs that ask the agent to change behavior;
- stale source becoming high-confidence memory;
- cross-tenant leakage;
- profile facts inferred without consent;
- background updates bypassing review;
- hidden priority inversion where memory outranks policy.

## Eval Coverage

Memory/retrieval evals should include:

- access-control exceptions;
- stale retrieval;
- source attribution failure;
- poisoned retrieved document;
- conflicting sources;
- memory write denial;
- memory correction/deletion;
- tenant filter regression.

## Design Output

Include:

- memory map;
- retrieval source map;
- write policy;
- poisoning controls;
- eval cases;
- trace fields.
