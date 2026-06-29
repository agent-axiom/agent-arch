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

## Revision trail

- Before content update:
  `ALtnJHxghK0ux39XZSQMkGfFh_TqFc9QasJFxuerN_vYLBxxWKS036rEaQmQRW9mCVrBIR2uNFtXgg1EbDTdIopzLmiVbROaOd-e0Vj1GTQ`
- After content update:
  `ALtnJHw1R83ocN6O1XetQWLZLs2XYdZGe5JLOqDmqHksMFynpYErcDBApwmVkBcchI-afBauu8G3COOifcu-3Z7gN7tZf-RrbY4MVrou4x4`
- After style repair:
  `ALtnJHzjZfOgynVeNrNt6B2heNKnW4Yz5SEWr6GPlCnh2_fq4CMIfLhsDkttY65ciuOYxLTzJic6xE7lqNB426yaiADPWqz2FZoqPcZW1eU`

## Connector verification

Readback confirmed that both inserted text blocks are present in the target
document. The companion paragraph style was repaired back to body text, and the
`Как пользоваться источниками` heading was restored to heading style after the
initial replace operation.

## Remaining limits

- This pass did not export a new DOCX proof.
- This pass did not change author-owned front-matter placeholders.
- This pass did not claim a full source-catalog verification; it only synced
  the manuscript warning and companion routes.

