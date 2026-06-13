# Russian Publisher Sample Slice Plan

Date: 2026-06-13

Status: completed

## Goal

Prepare the next publisher-ready Russian manuscript slice without pushing remote
changes: Chapter 1 as the primary editorial sample, source Chapter 13 as the
technical credibility sample, and the tracking artifacts that keep Google Docs
aligned with the repository.

## Scope

- Source of truth remains the repository.
- Google Doc remains the publisher-facing working manuscript.
- This slice does not apply final БХВ styles; those are still pending.
- This slice does not assemble the entire book. It creates a verified baseline
  for the two sample chapters and the next repeatable workflow.

## IT Book Editorial Rubric

Use these checks before calling a chapter sample-ready:

1. Reader promise: the opening states what practical decision the reader can make
   after the chapter.
2. Problem-first opening: the chapter starts from an operational failure or
   concrete engineering pressure, not from taxonomy.
3. Decision frame: the chapter gives a compact rule, checklist, or gate that can
   survive print, PDF, and excerpting.
4. Terminology stability: Russian forms follow
   `docs/publisher/ru-terminology.md`; English remains only for code, source
   names, protocol names, and first-use alignment.
5. Companion boundary: schemas, long code/output blocks, source catalogs, and
   web-only navigation stay online unless they are needed for the book argument.
6. Evidence hygiene: claims that depend on vendor practice, research, or
   implementation artifacts are either cited or framed as author synthesis.
7. Print-safe figures: Mermaid and web components have prose fallbacks or
   captions.
8. Chapter ending: the ending leaves memory hooks, common mistakes, and an
   immediate architecture check, not a motivational summary.

## Execution Checklist

- [x] Stabilize Chapter 1 with a first Russian publisher line edit.
- [x] Sync Chapter 1 line-edit deltas into the Google Doc manuscript.
- [x] Update publisher tracking artifacts for Chapter 1.
- [x] Apply the same rubric to source Chapter 13, focusing on terminology,
      direct-address cleanup, rollout/evals/review wording, and print/companion
      boundaries.
- [x] Update the Google Doc manuscript with the completed slice status.
- [x] Run repository verification.
- [x] Commit locally and do not push.

## Chapter 1 Acceptance Criteria

- The chapter keeps the support-triage failure story.
- The reader promise is explicit.
- Direct-address wording is reduced where it reads like a tutorial.
- The workflow / single-agent / multi-agent rule remains compact.
- The Google Doc contains the same line-edit deltas.

## Source Chapter 13 Acceptance Criteria

- The sample frames evaluation as release judgment, not a metrics list.
- `evals`, `rollout`, `review`, `assurance`, `runtime`, `dataset`, `score`,
  and `prompt` follow the Russian terminology policy in prose.
- Direct-address wording is reduced to team/system phrasing.
- Web-only companion references remain available but are no longer required for
  the print argument.
- The ending points to the Russian contract structure, not the old web-only
  part numbering.

## Verification

Run before completion:

- `git diff --check` - passed.
- `uv run pytest` - passed, 948 tests.
- `uv run mkdocs build --strict` - passed; emitted the existing Material for
  MkDocs future-compatibility warning.
- Google Doc read-back for the key updated status phrases - passed.
