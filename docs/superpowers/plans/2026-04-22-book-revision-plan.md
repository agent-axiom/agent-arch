# Book Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the manuscript from a strong architecture handbook into a tighter, more authoritative book by increasing argument density, cutting metadiscourse, improving evidence quality, and finishing the editorial layer.

**Architecture:** Work in six passes: freeze editorial constraints, rewrite entry surfaces, strengthen the opening act, compress late-book framing, upgrade evidence, then run a dedicated polish pass. Keep the existing editorial geometry intact: Part V = capture/health/judgment and Part VIII = lifecycle frame/release judgment/response/evidence backbone/lifecycle closure/adversarial pressure/judgment/evidence substrate/accountability.

**Tech Stack:** Markdown, MkDocs Material, Mermaid, `rg`, `sed`, `mkdocs build`

---

### Task 1: Freeze Editorial Constraints Before Rewrites

**Files:**
- Review: `docs/book-improvement-blueprint.md`
- Review: `docs/chapter-surgery-plan.md`
- Review: `docs/late-book-overlap-audit.md`
- Review: `docs/book-identity-memo.md`
- Review: `docs/reader-journey-map.md`

- [ ] **Step 1: Re-read the constraint documents and extract the five non-negotiables**

Capture these as the rewrite guardrails:
- the book must carry argument and reader transformation
- appendix/reference pages must support, not retell
- Part V must stay capture -> health -> judgment
- Part VIII must keep distinct late-book roles
- entry pages must read as reader promises, not inventory lists

- [ ] **Step 2: Run the drift scans before editing prose**

Run:

```bash
rg -n "нужна отдельная связующая страница|должна показать|в этом и состоит главная задача|editorial boundary|operational contour|evidence backbone|evidence substrate" docs
```

Expected:
- a concrete list of pages where the manuscript talks about its own structure more than the subject

- [ ] **Step 3: Mark the no-regression rules for the rewrite pass**

Use these rules during every edit:
- do not reintroduce “future tense” for pages that already exist
- do not let chapter intros repeat neighboring chapter jobs
- do not add schema detail when a causal explanation is enough
- do not sync translations yet; stabilize Russian source pages first

- [ ] **Step 4: Commit the constraint checkpoint**

```bash
git add docs/book-improvement-blueprint.md docs/chapter-surgery-plan.md docs/late-book-overlap-audit.md docs/book-identity-memo.md docs/reader-journey-map.md docs/superpowers/plans/2026-04-22-book-revision-plan.md
git commit -m "docs: add book revision plan and editorial constraints"
```

### Task 2: Rewrite Entry Surfaces So the Book Opens Like a Book

**Files:**
- Modify: `docs/index.md`
- Modify: `docs/start-here.md`
- Modify: `docs/book/plan.md`
- Modify: `docs/appendix/why-this-book.md`

- [ ] **Step 1: Tighten the homepage around one promise**

Rewrite `docs/index.md` so the first screen answers only four questions:
- what this book is
- who it is for
- what change in thinking it produces
- where to start

Cut:
- long navigational inventory near the top
- repeated restatements of project maturity
- wording that sounds like a project site instead of a book

- [ ] **Step 2: Keep `start-here.md`, but shorten it by removing repeated internal geometry**

In `docs/start-here.md` keep:
- the core audience fit
- the 30-minute path
- role-based routes

Cut or compress:
- repeated explanations of “book vs reference layer”
- repeated role grammar that already belongs deeper in the manuscript
- any sentence that names internal architecture of the book before the reader needs it

Verification command:

```bash
rg -n "evidence backbone|evidence substrate|accountability всего estate|эта страница нужна" docs/start-here.md docs/index.md docs/book/plan.md docs/appendix/why-this-book.md
```

Expected:
- only essential hits remain

- [ ] **Step 3: Make `book/plan.md` a status page, not a second manifesto**

Keep:
- structure
- publication status
- roadmap

Remove or shorten:
- prose that re-argues the book’s identity
- repeated framing that belongs in `start-here.md` and `why-this-book.md`

- [ ] **Step 4: Turn `why-this-book.md` into the shortest clean statement of the genre**

Aim for:
- one clear contrast with framework docs
- one clear contrast with vendor docs
- one clear contrast with security checklists
- one clear statement of the promised reader transformation

- [ ] **Step 5: Build the site to catch broken links after the entry-surface rewrite**

Run:

```bash
mkdocs build -q
```

Expected:
- exit code `0`

- [ ] **Step 6: Commit the entry-surface rewrite**

```bash
git add docs/index.md docs/start-here.md docs/book/plan.md docs/appendix/why-this-book.md
git commit -m "docs: tighten book entry surfaces"
```

### Task 3: Strengthen Part I So the Opening Act Proves the Thesis

**Files:**
- Modify: `docs/book/part-i/index.md`
- Modify: `docs/book/part-i/chapter-1.md`
- Modify: `docs/book/part-i/chapter-2.md`

- [ ] **Step 1: Make Part I about one dominant question**

Rewrite the opening of `docs/book/part-i/index.md` around:

> What kind of system are you actually building when you stop treating the agent as a prompt trick?

Keep the route guidance, but reduce checklist energy.

- [ ] **Step 2: Tighten Chapter 1 into a sharper first-act argument**

In `docs/book/part-i/chapter-1.md`:
- keep the support-case failure opening
- add 1 stronger contrast between demo success and operational failure
- compress repeated lists of “what teams do wrong”
- preserve the workflow vs single-agent vs multi-agent decision rule

Mandatory fixes:
- correct the subsection numbering bug around section 9 / `8.1-8.4`
- remove any sentence that says the same thing as the previous paragraph with different vocabulary

- [ ] **Step 3: Make Chapter 2 read as the first proof, not just the first walkthrough**

In `docs/book/part-i/chapter-2.md`:
- preserve the architecture walkthrough
- make each layer answer one failure from Chapter 1
- ensure the reader can say “this is why the platform thesis is true,” not only “these are the parts”

- [ ] **Step 4: Verify that Part I does not relapse into framework-doc mode**

Run:

```bash
rg -n "каталог|слой|контур|схема|архитектура" docs/book/part-i/index.md docs/book/part-i/chapter-1.md docs/book/part-i/chapter-2.md
```

Expected:
- these words still exist, but the pages are visibly driven by argument and scenario, not by taxonomy alone

- [ ] **Step 5: Commit the Part I rewrite**

```bash
git add docs/book/part-i/index.md docs/book/part-i/chapter-1.md docs/book/part-i/chapter-2.md
git commit -m "docs: strengthen opening act of the book"
```

### Task 4: Compress Part V and Part VIII Framing and Remove Self-Referential Prose

**Files:**
- Modify: `docs/book/part-v/index.md`
- Modify: `docs/book/part-v/evidence-spine.md`
- Modify: `docs/book/part-viii/index.md`
- Modify: `docs/book/part-v/chapter-13.md`
- Modify: `docs/book/part-viii/chapter-20.md`
- Modify: `docs/book/part-viii/chapter-21.md`
- Modify: `docs/book/part-viii/chapter-22.md`
- Modify: `docs/book/part-viii/chapter-27.md`

- [ ] **Step 1: Remove “planned page” language from pages that already exist**

Mandatory fixes:
- `docs/book/part-v/index.md`
- `docs/book/part-v/evidence-spine.md`

Delete or rewrite lines that imply Evidence Spine is still missing or still needs to be added.

- [ ] **Step 2: Shorten every Part V and Part VIII intro by cutting internal metadiscourse**

For `docs/book/part-v/index.md` and `docs/book/part-viii/index.md`:
- keep the reader outcome
- keep the dominant question of the part
- cut repeated role grammar after the first useful mention
- cut phrases that explain the manuscript’s geometry more than the system itself

- [ ] **Step 3: Enforce one-sentence job definitions in the late-book chapter intros**

For chapters 13, 20, 21, 22, and 27, rewrite the first 2-4 paragraphs so each chapter answers exactly one job:
- Chapter 13 = judgment
- Chapter 20 = release judgment
- Chapter 21 = assurance response
- Chapter 22 = lineage / evidence backbone
- Chapter 27 = estate accountability

Anything that belongs to a neighbor gets cut or moved.

- [ ] **Step 4: Reduce stock phrasing and repeated transitions**

Run:

```bash
rg -n "Именно поэтому|Полезно|Это важный|Если тебе нужна связующая страница" docs/book
```

Expected:
- counts drop materially
- repeated chapter rhythms become less obvious

- [ ] **Step 5: Verify the late-book files still preserve the intended editorial geometry**

Manual check:
- Part V still reads as capture -> health -> judgment
- Part VIII still reads as lifecycle frame -> release judgment -> response -> evidence backbone -> closure -> adversarial pressure -> judgment -> evidence substrate -> accountability

- [ ] **Step 6: Commit the late-book compression pass**

```bash
git add docs/book/part-v/index.md docs/book/part-v/evidence-spine.md docs/book/part-viii/index.md docs/book/part-v/chapter-13.md docs/book/part-viii/chapter-20.md docs/book/part-viii/chapter-21.md docs/book/part-viii/chapter-22.md docs/book/part-viii/chapter-27.md
git commit -m "docs: compress late-book framing and remove metadiscourse"
```

### Task 5: Upgrade the Evidence Base Where the Book Makes Its Biggest Claims

**Files:**
- Modify: `docs/appendix/sources.md`
- Modify: `docs/book/part-v/chapter-13.md`
- Modify: `docs/book/part-vii/chapter-18.md`
- Modify: `docs/book/part-viii/chapter-20.md`
- Modify: `docs/book/part-viii/chapter-27.md`

- [ ] **Step 1: Add source classes the manuscript still lacks**

Add at least one concrete source in each class:
- postmortem or incident writeup
- independent governance or assurance source
- HCI/HITL or oversight research
- enterprise inventory / lifecycle governance source that is not just product marketing

- [ ] **Step 2: Mark the source list by type, not just by topic**

In `docs/appendix/sources.md`, group or annotate sources as:
- standards / regulatory
- vendor platform docs
- research
- incident / case studies
- tooling docs

This makes authority differences visible.

- [ ] **Step 3: Use stronger evidence exactly where the claims are strongest**

Priority insertion points:
- `docs/book/part-v/chapter-13.md` for verifier / evaluation claims
- `docs/book/part-vii/chapter-18.md` for rollout readiness and failed-run drills
- `docs/book/part-viii/chapter-20.md` for release-bearing change discipline
- `docs/book/part-viii/chapter-27.md` for inventory / registry / sprawl claims

- [ ] **Step 4: Remove weak or sloppy citations**

Mandatory check:
- replace any link that points only to a generic domain homepage
- fix mixed-language citation titles
- prefer a direct article or paper URL over a top-level vendor blog landing page

- [ ] **Step 5: Commit the evidence upgrade**

```bash
git add docs/appendix/sources.md docs/book/part-v/chapter-13.md docs/book/part-vii/chapter-18.md docs/book/part-viii/chapter-20.md docs/book/part-viii/chapter-27.md
git commit -m "docs: strengthen evidence base for core claims"
```

### Task 6: Run a Dedicated Editorial Polish Pass on Russian Source Pages

**Files:**
- Modify: `docs/start-here.md`
- Modify: `docs/book/**/*.md`
- Modify: `docs/appendix/**/*.md`

- [ ] **Step 1: Fix visible manuscript-quality defects**

Run:

```bash
rg -n "zoo rarely starts|Cloudflare, \\[Reference architecture|## [0-9]+\\.|### [0-9]+\\.[0-9]+\\." docs
```

Expected:
- catches mixed-language slips, bad link text, and heading-number anomalies

- [ ] **Step 2: Normalize the Russian editorial style**

Pass goals:
- remove obvious calques where Russian can be cleaner
- reduce overloaded Anglo-Russian hybrids when a Russian phrase is enough
- keep technical English terms only where they are standard and useful
- shorten paragraphs that merely restate the previous one

- [ ] **Step 3: Keep appendix/reference boundaries clean during polish**

When a chapter drifts into schema inventory:
- cut the inventory from the chapter
- point to the appendix page instead

When an appendix page starts re-arguing the chapter:
- cut the rhetoric
- keep the artifact, schema, checklist, or contract

- [ ] **Step 4: Build the site again after the polish pass**

Run:

```bash
mkdocs build -q
```

Expected:
- exit code `0`

- [ ] **Step 5: Commit the editorial polish**

```bash
git add docs/start-here.md docs/book docs/appendix
git commit -m "docs: run editorial polish pass on source manuscript"
```

### Task 7: Only After Russian Stabilizes, Sync English and Chinese Pages

**Files:**
- Modify later: `docs/**/*.en.md`
- Modify later: `docs/**/*.zh.md`

- [ ] **Step 1: Freeze Russian source pages first**

Do not start translation sync until Tasks 2-6 are merged and reviewed.

- [ ] **Step 2: Translate only stabilized pages**

Priority order:
- entry surfaces
- Part I
- Part V / Evidence Spine
- Part VIII intros
- appendix source pages that changed materially

- [ ] **Step 3: Verify structure parity before publishing**

Run:

```bash
rg --files docs | rg "(.en|.zh)?\\.md$"
```

Expected:
- all rewritten source pages have corresponding translated siblings queued or updated

- [ ] **Step 4: Commit translation sync separately**

```bash
git add docs
git commit -m "docs: sync translated book surfaces after source rewrite"
```

## Self-Review

- Spec coverage: this plan covers the biggest current gaps identified in the manuscript review: entry-surface strength, Part I pull, late-book overreach, evidence weakness, editorial polish, and translation sequencing.
- Placeholder scan: no `TODO`, `TBD`, or “handle appropriately” placeholders remain; every task names exact files and verification commands.
- Type consistency: chapter-role names and editorial geometry are consistent with the current manuscript constraints.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-22-book-revision-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
