# Google Doc practice polish proof pass

Date: 2026-07-02.

Status: working proof pass after late-practice wording polish. This is suitable
for continued editor review, but it is not the final publisher-ready DOCX.

## Scope

This pass followed the 2026-07-01 latest-practices sync and focused on the
practice blocks that were inserted into the full Google Doc manuscript. The
goal was to make the new blocks read like a print manuscript, not like raw
source appendices or temporary synchronization notes.

Google Doc:

- `Архитектура безопасных ИИ-агентов — полная рукопись`;
- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>.

## Google Doc edits

Guarded connector `batchUpdate` changed seven practice-polish replacements in
the full Google Doc:

1. `Практикум: назначить владельцев для trace, SLO, eval и rollout`;
2. `Практикум: минимальный золотой путь для пишущего агента`;
3. `Практикум: пройти цепочку trace, eval gate, rollout wave и containment`;
4. clarified the trace/SLO/eval/rollout ownership sentence;
5. clarified `golden path` as `золотой путь (golden path)`;
6. clarified the write-agent path result around `documented exception`;
7. clarified the rollout/containment practice result around a single decision
   record.

Revision evidence:

- before polish:
  `ALtnJHw6WxhO001-I6mNISWhNzNDr7n5YMGTbGYCJgQC70hOmSth96E7ZqoA-Nu2VFfUElLa8JnWk-QcpYhyoU-Zzgu3EUIDi3iKWys1_D4`;
- after polish:
  `ALtnJHzfp6dC10EFS5o6ohijtZNURxfuA7ekf6CeXSwFg1YCzXmjCNOpESmN9VBBEEvbYrZJzansw1fJ8_TU-zsqxWG4y3Q97gUQtQz-Duk`.

Readback checks:

- old arrow/generic headings no longer appear in the Google Doc text export;
- the three polished practice headings appear exactly once each;
- `Хороший золотой путь (golden path) быстрее локального обхода` appears once;
- `reviewer может по одному decision record ответить` appears once.

## Local vs Google Doc state

The local full manuscript remains the complete source assembly:

- `docs/publisher/ru-manuscript-full.md`;
- approximate word count: 123,082.

The Google Doc remains the current working editorial manuscript:

- fresh text readback approximate word count: 101,715;
- it intentionally keeps the late practice blocks in a more print-oriented
  shape than the full source assembly;
- long YAML, raw payloads and operational details remain companion candidates
  rather than print-body expansion.

This means the Google Doc is no longer a compressed 72-page assembly. It is a
full working manuscript proof, but still has deliberate book/companion
compression compared with the complete local source assembly.

## DOCX proof and render QA

Fresh raw Google Docs DOCX proof:

- `docs/publisher/artifacts/agent-arch-ru-practice-polished-working-proof-2026-07-02.docx`;
- size: 689,339 bytes;
- SHA-256:
  `cdc599126b29928d0e5beaffeee609af090066eb6130f1a2745ca6828621e1b2`.

Render QA:

- report:
  `docs/publisher/ru-google-doc-practice-polish-proof-pass-2026-07-02.render-qa.json`;
- rendered pages: 513;
- blank-like pages: 0;
- representative visual pages checked: 1, 337, 338, 423 and 513.

Observed layout issue:

- page 338 has an orphan one-line checklist carryover with a large blank area;
- this is a publisher-style/layout issue for the next pass, not a text-loss
  issue;
- the proof should be treated as a working editor-review artifact, not final
  printer-facing layout.

## Author-owned fields

Author-owned fields remain intentionally unresolved. They are tracked in:

- `docs/publisher/ru-author-fields-after-practice-polish-2026-07-02.md`;
- `docs/publisher/ru-author-input-closure-packet-2026-06-30.md`.

Codex must not invent:

- public byline;
- author bio;
- role and public positioning;
- verified experience claims;
- public project links;
- companion URL/version;
- acknowledgements;
- legal/compliance disclaimer;
- AI-use disclosure, if the publisher requires one.

## Decision

This pass closes the immediate post-practice-sync proof step:

- the new practice blocks are clearer in the Google Doc;
- a fresh DOCX proof exists;
- render QA gives a concrete 513-page working proof with 0 blank-like pages;
- current package state is recorded for editor review.

Open before final publisher-ready submission:

1. author-owned fields;
2. external proofread;
3. publisher style application;
4. page-level layout cleanup, including the page 338 orphan;
5. final raw/Template2000n DOCX export and render QA after author and style
   closure.
