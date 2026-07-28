# RU Case And Thesis Editorial Design

Date: 2026-07-05.

## Goal

Make the Russian manuscript more memorable and recommendable by giving readers
a recurring production case and concise, quotable chapter theses.

## Design

The pass adds two layers without restructuring the book:

1. A named through-case in the introduction. The case is the support agent
   already used across the manuscript, but it becomes explicit: the reader
   follows the same system as it moves from demo to controlled launch.
2. Seven part-level case episodes. Each episode shows what changed in the
   support-agent system after that part: decision boundary, trust boundary,
   memory, tool execution, evidence, ownership, and launch gate.
3. Twenty-three chapter-level `Фраза для пересказа` lines. These are short,
   sharp formulations that a reader can quote or send to a colleague.

## Editorial Rules

- Do not add a second fictional storyline.
- Do not duplicate the existing production scenes, chapter takeaways, forwarding
  hooks or team workshop blocks.
- Keep each case episode compact enough to read as a bridge, not as a new
  chapter section.
- Keep each quotable thesis technically defensible and aligned with the chapter
  content.
- Preserve the existing Google Doc as the live manuscript and keep the raw DOCX,
  Template2000n derivative, Markdown source and reports in sync.

## Acceptance Criteria

- Markdown, raw DOCX and Template2000n DOCX contain exactly:
  - 1 `Сквозной производственный кейс`;
  - 7 `Эпизод сквозного кейса`;
  - 23 `Фраза для пересказа`.
- Google Doc readback finds all three labels.
- Raw and Template2000n paragraph text equality is preserved.
- Render QA finds 0 blank-like pages in both proof files.
- Exact duplicate paragraph groups with 35+ words remain 0.
- Paragraphs with 250+ words remain 0.
- `git diff --check` and `uv run --group docs mkdocs build --strict` pass.
