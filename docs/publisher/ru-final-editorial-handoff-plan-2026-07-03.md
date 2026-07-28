# Final editorial handoff plan

Date: 2026-07-03.

Status: current handoff plan after Template2000n pre-author proof.

## Purpose

This file describes what can be sent to a trusted editor now, what remains
blocked for final publisher submission and how the next export should be run
after author-owned fields are filled.

## Current sendable working packet

Use this packet for structural/substantive editorial review:

- Google Doc manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Raw DOCX proof:
  `docs/publisher/artifacts/agent-arch-ru-final-preauthor-raw-2026-07-03.docx`
- Template2000n pre-author proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-final-preauthor-2026-07-03.docx`
- Pre-author publisher packet:
  `docs/publisher/ru-preauthor-publisher-submission-packet-2026-07-03.md`
- Style acceptance gate:
  `docs/publisher/ru-template2000n-acceptance-gate-2026-07-03.md`
- Author fill packet:
  `docs/publisher/ru-author-editorial-fill-packet-2026-07-03.md`
- Manuscript map:
  `docs/publisher/ru-manuscript-map.md`
- Submission checklist:
  `docs/publisher/ru-submission-checklist.md`

## What to ask the editor to review now

Priority order:

1. Does the book argument hold across all seven parts?
2. Are the 23 chapters balanced enough for copyediting?
3. Are technical examples at the right print depth, with companion material
   moved out when needed?
4. Are headings and section rhythm suitable for a technical book?
5. Are source/status notes and AI/policy claims clear enough for fact-checking?
6. Is the Template2000n styled proof acceptable as the next DOCX shape?

## Do not call final until these are closed

- author bio/byline/credentials and public links;
- companion URL/version/changelog/errata route;
- final title/subtitle/cover-copy/imprint metadata;
- AI-use disclosure if required by publisher;
- legal/compliance disclaimer;
- acknowledgements and permissions;
- real/composite/anonymized case policy;
- publisher/editor acceptance of the Template2000n style route;
- independent proofread after the export shape is stable;
- fresh raw export, fresh Template2000n rebuild and render QA after author
  fields are inserted.

## Handoff wording

Use this status line in messages to editors:

```text
Это полнообъемная рабочая рукопись для структурной и содержательной редакторской
оценки. Google Doc является рабочей рукописью, DOCX с Template2000n является
издательским proof candidate. Финальная сдача будет подготовлена после закрытия
авторских полей, принятия style route и повторного export/render QA.
```

## Completion rule

The final publisher submission packet is created only after the post-author
workflow runs against the latest Google Doc state and produces a new dated raw
DOCX, a new dated Template2000n derivative, a new render QA report and a clean
repository verification pass.
