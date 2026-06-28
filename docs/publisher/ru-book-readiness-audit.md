# Аудит готовности русской рукописи к книге

Status: active book-readiness audit, second editorial pass.

Date: 2026-06-17.

Canonical manuscript:

- Full Google Doc manuscript: <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Local source assembly: `docs/publisher/ru-manuscript-full.md`
- Compressed/staging snapshot: <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

## Executive verdict

The manuscript has full source volume, but it is not yet a finished book.

Current local assembly metrics:

- about 112,800 words;
- 7 parts;
- 23 chapters;
- 4 appendices;
- local DOCX render smoke test: 437 pages;
- Google Docs pagination: about 432 pages.

The main risk is not missing volume anymore. The main risk is that a large
source-to-print assembly can still read like a curated documentation corpus
instead of a coherent authorial IT book.

The second editorial pass must optimize for:

- reader journey from demo-agent failure to production launch decision;
- stable chapter rhythm;
- removal of duplicated reference material;
- stronger practical examples without turning the book into a CLI manual;
- explicit boundary between printed book and online companion;
- consistent Russian terminology and authorial voice.

## Definition of a finished book

The manuscript can be treated as book-ready only when all of these are true:

- each chapter has one central question and one clear answer;
- each part changes the reader's mental model and prepares the next part;
- repeated chapter endings are intentional and compact;
- long schemas, command walkthroughs and reference outputs are in the companion;
- the running practical case is visible across the book;
- the final part leads to a launch decision, not just to a runtime description;
- appendices are working aids, not duplicate chapters;
- author bio, front matter, publisher styles, DOCX export QA and proofread are
  complete.

## High-level findings

### 1. Volume is uneven

Most chapters are in the 1.6k-6.1k word range, but chapter 20 is about 15.8k
words and chapter 21 is about 10.5k words. These two chapters currently carry
too much reference and lifecycle material and will dominate the second half of
the book unless compressed and re-shaped.

Action:

- keep the strategic argument in the printed chapter;
- move registry, lifecycle record, long runtime details and operational
  walkthroughs to the companion;
- preserve only the decision model, invariants, examples and checklists needed
  for reading the book without opening the companion.

### 2. Some chapters combine several source pages without enough synthesis

The source assembly preserved useful material, but several chapters still show
the stitching pattern. Chapter 5 contains policy, capability, lifecycle and
artifact-contract material. Chapter 8 includes both conceptual memory layers and
schema-like details. Chapter 20 combines assurance, artifacts, retirement,
observability, registry, incident response and incident schemas.

Action:

- write a chapter thesis at the top of each overloaded chapter;
- keep only material that proves that thesis;
- demote repeated schema/reference blocks to appendix or companion.

### 3. Repeated endings are too visible

The manuscript repeats these headings many times:

- `Что делать дальше` - 33 occurrences;
- `Что сделать сразу` - 27 occurrences;
- `Что читать дальше` - 14 occurrences;
- `Частые ошибки` - 11 occurrences;
- `Полезные справочные страницы` - 11 occurrences.

This can be a useful pedagogical device, but in the current assembly it reads
partly mechanical.

Action:

- keep one compact end-of-chapter pattern;
- rename or merge endings into `Итог`, `Практический минимум` and `Переход к
  следующей главе`;
- remove duplicated "read next" sections when the next chapter already follows
  naturally.

### 4. The running case needs stronger continuity

The support-triage case is present, but it does not always drive the explanation.
In a finished IT book, the case should act as a spine: every major architectural
layer should answer what changes in the same production system.

Action:

- add a short case reminder in each part introduction;
- use the same vocabulary for user, tenant, tool, approval, trace, rollout and
  incident;
- make each part show one new operational capability added to the same system.

### 5. The companion boundary must become stricter

The current manuscript already marks many heavy artifacts as companion material,
but the text still includes long implementation-adjacent blocks in some late
chapters.

Action:

- printed book: concepts, invariants, decisions, compact examples, failure modes;
- online companion: full CLI walkthroughs, schemas, generated outputs, registry
  operations, long YAML/JSON examples, package internals.

## Chapter-level worklist

| Chapter | Current words | Current risk | Book-ready action | Priority |
| --- | ---: | --- | --- | --- |
| Introduction | n/a | Too many meta sections before the promise of the book stabilizes. | Compress into one promise, one reader profile, one route and one structure note. | P0 |
| 1. Platform, not magic | 2,433 | Strong opening, but ending stack is too procedural. | Preserve as primary sample chapter; sharpen failure story and final thesis. | P0 |
| 2. When an agent is needed | 2,293 | Mixes workflow/SOP material with coordinator/handoff material. | Reframe as decision ladder: workflow first, agent loop second, multi-agent last. | P0 |
| 3. Reference architecture | 2,798 | Good role, but needs stronger bridge to security. | Add clear architecture map and make the output of the chapter explicit. | P1 |
| 4. Security perimeter | 2,406 | Sound structure, moderate risk of generic security prose. | Tie every control to agent-specific trust boundary. | P1 |
| 5. Identity, policy, capability | 7,242 | Overloaded and overlaps with chapter 22. | Keep identity/policy model here; move implementation and package detail to chapter 22 or companion. | P0 |
| 6. Tool gateway and audit | 2,973 | Good practical topic, but confirmation/audit schemas can grow too much. | Keep confirmation as interruptible workflow and audit as investigation artifact. | P1 |
| 7. Memory risk | 1,971 | Good focused chapter, slightly short for its importance. | Add concrete production failure and decision rules. | P1 |
| 8. Memory layers | 3,509 | Conceptual material plus schema material. | Keep layer model in print; move schema-heavy detail to companion. | P1 |
| 9. Retrieval and compaction | 1,761 | Short and potentially underdeveloped. | Add example of retrieval policy and background refresh without long code. | P1 |
| 10. Execution model | 2,330 | Good position, needs tighter relation to tool gateway. | Make tool catalog a contract, not a list of functions. | P1 |
| 11. Sandbox and MCP | 5,485 | High-value chapter, risk of protocol/reference sprawl. | Explain MCP as integration boundary; move protocol detail to companion. | P0 |
| 12. Idempotency and rollback | 2,265 | Useful but may read like checklist. | Add failure story with side effects, retries and rollback boundary. | P1 |
| 13. Traces and events | 4,435 | Strong technical sample potential. | Make it a clear evidence-chain chapter, not only observability reference. | P0 |
| 14. SLO | 2,414 | Needs strong agent-specific SLO framing. | Tie SLO to user harm, tool actions and regression gates. | P1 |
| 15. Evals and regression gates | 6,108 | Important but can become eval reference. | Keep decision model and example rubric; move large evaluator artifacts to companion. | P0 |
| 16. Evidence chain | 3,784 | Good synthesis role. | Make this the bridge from observability/evals to rollout governance. | P1 |
| 17. Platform and product teams | 1,595 | Short and possibly too organizational. | Add concrete ownership model and platform contract. | P1 |
| 18. Golden paths | 1,634 | Short, potentially underpowered. | Show how golden paths reduce unsafe agent sprawl. | P1 |
| 19. ADLC | 3,990 | Solid lifecycle chapter, but reference blocks must be controlled. | Keep lifecycle stages and artifacts; avoid schema catalog tone. | P1 |
| 20. Assurance, incidents, registry, retirement | 15,760 | Severely overloaded. | Split internally into four movements, compress aggressively, move records and schemas to companion. | P0 |
| 21. Runtime baseline | 10,491 | Reads too much like runtime manual. | Convert to narrative reference implementation chapter; move commands/configs to companion. | P0 |
| 22. Policy layer and capability catalog | 4,996 | Duplicates chapter 5. | Make this implementation-focused and remove conceptual repetition. | P0 |
| 23. Launch checklist | 4,289 | Strong final chapter, but checklist/templates may duplicate appendices. | Make final launch decision the climax; move reusable templates to appendix. | P0 |
| Appendices | n/a | Some duplicate late chapters and companion material. | Reduce to glossary, concise checklists, incident template and curated sources. | P1 |

## Second editorial pass order

### Batch 1. Reader contract and opening arc

Scope:

- Introduction;
- chapter 1;
- chapter 2;
- chapter 3.

Goal:

- make the promise of the book clear in the first 10 pages;
- turn part I into a persuasive transition from demo-agent to platform;
- preserve chapter 1 as the primary sample.

Expected output:

- shorter front matter;
- stronger chapter openings;
- compact endings;
- explicit bridge to security and governance.

### Batch 2. Safety and control model

Scope:

- chapters 4-6;
- chapter 22 overlap notes.

Goal:

- separate conceptual security model from runtime implementation details;
- make identity, policy, capability and tool gateway one coherent control stack.

Expected output:

- chapter 5 compressed;
- chapter 22 receives implementation material instead of repeating the model;
- repeated policy/catalog explanations removed.

Progress:

- 2026-06-18: Chapter 5 rewritten as the conceptual identity/session/policy/
  capability chapter and synced to the full Google Doc manuscript from
  `docs/publisher/ru-book-ready-chapter-5.md`. Chapter 22 remains the next
  implementation-focused overlap target.
- 2026-06-18: Chapter 22 rewritten as the implementation-focused
  `policy.yaml` / `capabilities.yaml` / inspection / trace-evidence chapter
  and synced to the full Google Doc manuscript from
  `docs/publisher/ru-book-ready-chapter-22.md`. The chapter 5/22 overlap is now
  resolved at the manuscript level.

### Batch 3. Memory and execution

Scope:

- chapters 7-12.

Goal:

- keep memory and tools practical without becoming schema reference;
- make execution, sandbox and MCP read as one integration story.

Expected output:

- schema-heavy sections moved to companion notes;
- chapter 11 focused on boundary and risk;
- chapter 12 strengthened with side-effect failure story.

### Batch 4. Evidence, evals and rollout

Scope:

- chapters 13-16.

Goal:

- make trace, SLO, evals and rollout one evidence chain;
- preserve chapter 13 or 15 as technical sample candidates.

Expected output:

- less repetition across trace/eval/rollout chapters;
- explicit release decision model by the end of chapter 16.

### Batch 5. Organization and lifecycle

Scope:

- chapters 17-20.

Goal:

- turn late lifecycle material into a readable management and assurance arc;
- reduce chapter 20 from a bundle of reference pages into one chapter.

Expected output:

- chapter 20 compressed and restructured;
- registry, incident and retirement records moved or summarized;
- organization chapters strengthened with concrete ownership examples.

### Batch 6. Reference implementation and launch

Scope:

- chapters 21-23;
- appendices.

Goal:

- convert runtime material from manual to book chapter;
- make launch checklist the final synthesis;
- keep appendices short and useful.

Expected output:

- chapter 21 no longer reads as CLI walkthrough;
- chapter 23 becomes the final readiness gate;
- appendices contain only working aids and curated sources.

## Immediate implementation queue

1. Rewrite the introduction into a compact reader contract. Status:
   completed in `docs/publisher/ru-book-ready-introduction.md` and synced to
   the full Google Doc manuscript on 2026-06-17.
2. Line-edit chapter 1 as the first public sample chapter. Status:
   completed in `docs/publisher/ru-book-ready-chapter-1.md` and synced to the
   full Google Doc manuscript on 2026-06-18.
3. Rebuild chapter 2 around the workflow -> agent loop -> multi-agent decision
   ladder. Status: completed in `docs/publisher/ru-book-ready-chapter-2.md`
   and synced to the full Google Doc manuscript on 2026-06-18.
4. Add a short bridge at the end of chapter 3 into the safety/control part.
   Status: completed in `docs/publisher/ru-book-ready-chapter-3-bridge.md`
   and synced to the full Google Doc manuscript on 2026-06-18.
5. Compress chapter 5 by moving repeated policy/catalog implementation detail
   to chapter 22 or companion notes.
6. Restructure chapter 20 before spending time on small line edits in late
   chapters.
7. Convert chapter 21 from runtime manual to reference implementation narrative.
8. Run a final proofread only after these structural changes are done.

## Tracking rule

Every book-readiness change must be reflected in both places:

1. the canonical local source or publisher Markdown file;
2. the full Google Doc manuscript or a dedicated Google Doc editorial artifact.

Do not treat a Google Doc-only prose change as final until it has a matching
repository change or an explicit ledger entry.
