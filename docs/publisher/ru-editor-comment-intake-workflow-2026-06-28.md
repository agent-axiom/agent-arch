# Editor comment intake workflow

Date: 2026-06-28.

Status: ready for editor-review cycle.

## Purpose

Google Doc is the editor-facing manuscript, but the repository remains the
source of truth for semantic content. This workflow prevents editorial comments
from becoming untracked Google Doc-only changes.

## Inputs

- Google Doc manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Clean handoff packet:
  `docs/publisher/ru-clean-editor-handoff-packet-2026-06-28.md`
- Editor-facing brief:
  `docs/publisher/ru-editor-facing-brief-2026-06-28.md`

## Comment categories

Classify every editor comment as one of:

1. `structure`: chapter order, missing bridge, weak opening or weak payoff.
2. `line edit`: sentence-level clarity, voice, repetition, rhythm.
3. `terminology`: Russian/English term choice, glossary mismatch.
4. `fact/source`: claim needs source check or update.
5. `book/companion boundary`: material should move to or from companion.
6. `author-owned`: bio, credentials, acknowledgements, case permissions.
7. `layout/export`: page break, heading style, table/code readability.
8. `publisher metadata`: title, subtitle, imprint, ISBN, cover copy.

## Intake table

Track each comment with:

```text
Comment ID:
Google Doc location:
Category:
Editor request:
Decision: accept / reject / defer / needs author / needs source check
Repository source path:
Google Doc action:
Markdown action:
Owner:
Status:
Notes:
```

## Decision rules

- Semantic content changes must be applied to Markdown first or backported to
  Markdown immediately after Google Doc editing.
- Pure layout/export changes may remain in Google Doc or DOCX if they do not
  change meaning.
- Author-owned questions go to `docs/publisher/ru-author-query-packet-2026-06-28.md`.
- Fact/source questions go to `docs/publisher/ru-source-verification-records-2026-06-28.md`.
- Companion-boundary questions update both the print manuscript and companion
  route.

## Implementation order

1. Export or list current open Google Doc comments.
2. Assign categories and owners.
3. Resolve `author-owned` and `fact/source` blockers before final copyedit.
4. Apply accepted semantic edits to Markdown.
5. Sync edited sections back to Google Doc.
6. Re-export raw DOCX after each large batch.
7. Rebuild Template2000n proof if structure/front matter changes.
8. Run render QA after structural or style-impacting edits.

## Completion criteria

Editor comment intake is complete when:

- every editor comment has a decision;
- accepted semantic changes exist in Markdown and Google Doc;
- rejected/deferred comments have a reason;
- author-owned comments are listed for the author;
- source-check comments have verification records;
- export QA has been rerun after the final accepted batch.
