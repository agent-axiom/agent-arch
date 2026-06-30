# OpenReview demotion pass

Date: 2026-06-30.

Status: OpenReview records are demoted from primary evidence to non-primary
research leads.

## Reason

The 2026-06-29 URL pass returned HTTP 200 challenge redirects for OpenReview
links. The 2026-06-30 follow-up confirmed that the public page and API access
still require challenge verification instead of returning stable paper
metadata. Because the final publisher packet must not depend on sources that
cannot be verified in the current workflow, OpenReview records are no longer
treated as primary evidence.

## What changed

Updated:

- `docs/appendix/sources.md`
- `docs/book/part-v/chapter-13.md`
- `docs/publisher/ru-manuscript-full.md`

Decision:

- keep OpenReview links only as non-primary research leads;
- remove the OpenReview footnote from Chapter 13's primary HCI/evaluation
  argument;
- keep the stable Microsoft Research HCI source as primary support for the
  relevant claim;
- do not include OpenReview records in the final editor packet unless the
  editor explicitly asks for research leads or the metadata is verified later.

## Final packet impact

This closes the OpenReview primary-evidence blocker by demotion. The remaining
final-submission blockers are author-owned fields, companion public metadata,
fresh final DOCX export, render QA and external proofread/editorial triage.
