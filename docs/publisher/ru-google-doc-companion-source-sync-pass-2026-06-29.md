# Google Doc companion/source-status sync pass

Date: 2026-06-29.

Target document:

- Google Doc: <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Title: `Архитектура безопасных ИИ-агентов - полная рукопись`
- Tab: `t.0`

## What changed

This pass synchronized the current companion/source-status wording into the
full Google Doc manuscript. The update was made through the Google Docs
connector with `batchUpdate`, not by manual browser editing.

Inserted into the reference route section:

- companion examples for the support-ticket running case;
- capability contract, release decision record, incident record and production
  readiness review route;
- trace/session/eval artifact route for the timeout-failure case.

Inserted into the source section:

- a warning that fast-moving platform/API/security sources must be checked live
  before final delivery;
- a rule that the check date must be recorded in the source catalog.

Updated after the full URL availability pass:

- the source-status warning now records the 2026-06-29 full live URL
  availability pass: 102 of 106 source URLs returned HTTP 200, and 4 sources
  require manual or browser/API follow-up;
- the warning still keeps semantic verification of fast-moving platform claims
  as a final pre-submission step;
- the source appendix wording was updated in repository source-of-truth
  Markdown. A direct whole-line Google Docs replace for the appendix paragraph
  matched 0 occurrences because the imported Google Doc paragraph does not keep
  the Markdown line as one exact raw-text span.

## Revision trail

- Before content update:
  `ALtnJHxghK0ux39XZSQMkGfFh_TqFc9QasJFxuerN_vYLBxxWKS036rEaQmQRW9mCVrBIR2uNFtXgg1EbDTdIopzLmiVbROaOd-e0Vj1GTQ`
- After content update:
  `ALtnJHw1R83ocN6O1XetQWLZLs2XYdZGe5JLOqDmqHksMFynpYErcDBApwmVkBcchI-afBauu8G3COOifcu-3Z7gN7tZf-RrbY4MVrou4x4`
- After style repair:
  `ALtnJHzjZfOgynVeNrNt6B2heNKnW4Yz5SEWr6GPlCnh2_fq4CMIfLhsDkttY65ciuOYxLTzJic6xE7lqNB426yaiADPWqz2FZoqPcZW1eU`
- After full URL availability status update:
  `ALtnJHzPEb_vH_SBUgdtT-z3Ff5FOeVdsravgXzeHJI3aKiVqaQBPEqciARhW3cZed5m8mRBNHLvL5Ls1Z0Fgd5chvymjuUIaniWP_fIyos`
- After targeted source follow-up status update:
  `ALtnJHzrSoSQuiJCnRBZeYOE9smBowRGwNdNy2LlzC4ufXG_96_REjYpK5gO864gFg2heFYpfXd956sFwovgi6RFlJyaHt3KOleN5nuTmSQ`

## Connector verification

Readback confirmed that both inserted text blocks are present in the target
document. The companion paragraph style was repaired back to body text, and the
`Как пользоваться источниками` heading was restored to heading style after the
initial replace operation. The later full URL availability status update
reported one changed Google Docs occurrence for the source-status warning.
The 2026-06-30 targeted source follow-up update also reported one changed
Google Docs occurrence for the source-status warning. A second attempted
top-note replacement matched 0 occurrences because the imported paragraph is
not exposed as the exact raw-text span used by repository Markdown.

## Remaining limits

- This pass did not export a new DOCX proof.
- This pass did not change author-owned front-matter placeholders.
- This pass did not claim a full semantic source-catalog verification; it synced
  the manuscript warning, companion routes, URL availability status and the
  later targeted source follow-up status.
