# Google Doc frontier architecture enrichment pass

Date: 2026-07-09.

Status: first applied pass completed in the active Google Doc. This is not a
final publisher export: author-owned fields, external proofread, DOCX export,
Template2000n style pass and render QA remain separate stages.

Google Doc:

- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

Final known Google Doc revision after this pass:

- `ALtnJHyywtnkO1z-TJPX1zCSChx4VNNHsmbLdVW77_Dm03IBoC6JEi_OoFuZtNINBvhpqFePU1Ja3BquU4ckuFtmjQJP036XfJKDX8p_w00`

## Goal

Bring the newest electronic-version material into the manuscript in a way that
improves the book's core argument, not as a loose appendix.

The pass uses the new `safe-agent-architecture` material, recent eval schema
updates, reference-package updates and research-frontier updates as source
signals.

## Fresh source material reviewed

1. `skills/safe-agent-architecture/SKILL.md`
2. `skills/safe-agent-architecture/references/risk-tiers.md`
3. `skills/safe-agent-architecture/references/tool-gateway.md`
4. `skills/safe-agent-architecture/references/memory-retrieval.md`
5. `skills/safe-agent-architecture/references/evals-rollout.md`
6. `docs/appendix/eval-schema.md`
7. `docs/appendix/reference-package.md`
8. `docs/appendix/research-frontier.md`

## What was added to the Google Doc

Inserted a new front-of-book section after the opening thesis and before the
navigation block:

- `Сквозная рамка безопасной архитектуры агента`

The section adds the book-level operating frame that was missing from the
compressed editorial assembly:

1. A safe-agent architecture brief as the design gate before framework choice.
2. Agency/risk ladder from answer-only assistant to delegated multi-agent
   runtime.
3. Tool gateway framing: tools as authority, not plain functions.
4. MCP/A2A threat model notes: tool poisoning, rug pull, tool shadowing,
   confused deputy, over-scoped tokens and delegated authority drift.
5. Memory and retrieval as governed subsystems, including poisoning and
   tenant/access regressions.
6. Brain / Hands / Session split for managed and durable agents.
7. Eval integrity audit as a first-class safety control.
8. Deployment/tool simulation checks and rollout-gate readiness.
9. Multi-agent reliability warning: start with one agent plus good tools, move
   to multi-agent only when the evidence justifies the extra coordination cost.

## Google Doc verification

Connector readback confirmed:

- target document id: `1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4`;
- tab: `t.0`;
- title: `Архитектура безопасных ИИ-агентов`;
- inserted main heading is present as `HEADING_2`;
- inserted internal headings are present as `HEADING_3`;
- the inserted block starts at document index `1878`;
- the following existing navigation block still follows the new section.

Document size signal from connector indexes:

- before pass: final observed text index approximately `834381`;
- after pass: final observed text index approximately `842689`;
- applied growth: approximately `8308` Google Docs text index units.

PDF export was attempted and succeeded at the connector level, but the connector
returned a large inline base64 payload in this session. Page count was therefore
not extracted in this pass. Structural verification was done through the Google
Docs connector readback instead.

## Editorial mapping for the next integration passes

Priority 1, book-level integration:

1. Chapter 1 / introduction: make the safe-agent architecture brief the
   recurring decision artifact for the whole book.
2. Part I: add the agency/risk ladder and make "lowest sufficient agency" a
   recurring design principle.
3. Part II and Part IV: expand the tool gateway, approval payload and MCP/A2A
   threat-model material inside the security and tool chapters.
4. Part III: enrich memory and retrieval chapters with state separation,
   freshness, provenance, memory-write policy and poisoning evals.
5. Part V: expand eval chapters with eval integrity audit, defect taxonomy,
   deployment simulation and tool-simulation fidelity.
6. Part VII and VIII: make Brain / Hands / Session and durable identity
   separation visible in runtime and lifecycle chapters.

Priority 2, reader-interest integration:

1. Add short case callouts that reuse the three canonical scenarios:
   support triage, internal knowledge assistant and incident coordination.
2. Add visual placeholders for the risk ladder, tool gateway boundary, eval
   integrity loop, Brain / Hands / Session split and multi-agent delegation map.
3. Turn multi-agent reliability into a narrative warning: more agents mean more
   surfaces for specification drift, conflict, lost context and weak review.
4. Add a practical "architecture review checklist" that a reader can use after
   finishing the book.

Priority 3, reference hygiene:

1. Keep long schemas, CLI output and exhaustive field lists in the companion
   layer instead of bloating the main manuscript.
2. Keep accepted technical identifiers such as `trace_id`, `session_id`,
   `run_failed`, `eval_audit_record` and `agent_instance_id` unchanged.
3. Replace avoidable prose anglicisms with Russian equivalents in later
   terminology passes.
4. Re-run duplicate and repeated-source checks after the chapter-level
   integration pass.

## Author-owned fields still required

The author still needs to fill or explicitly omit:

- public author name/byline;
- short and long author bio;
- role/public positioning;
- verified experience claims;
- public project links;
- public companion URL/version;
- acknowledgements;
- legal/compliance disclaimer;
- AI-use disclosure if required by the publisher;
- final publisher metadata and cover copy.
