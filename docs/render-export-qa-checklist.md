# Render / Export QA Checklist

Purpose: record checks required before calling the manuscript externally sendable.
This is not a public book page and stays outside the published navigation.

Modes:

- HTML browser
- plain text extraction
- PDF export
- print export
- mobile viewport
- search index extraction

Priority pages:

- Chapter 1 decision frame: `docs/book/part-i/chapter-1.md`
- Chapter 2 layer map: `docs/book/part-i/chapter-2.md`
- Chapter 9 Mermaid / YAML / MCP sections: `docs/book/part-iv/chapter-9.md`
- Chapter 13 eval loop Mermaid: `docs/book/part-v/chapter-13.md`
- Reference final rule: `docs/reference.md`
- Reference Package CLI / YAML blocks: `docs/appendix/reference-package.md`
- Chapter 26 telemetry lists: `docs/book/part-viii/chapter-26.md`
- Chapter 27 registry records: `docs/book/part-viii/chapter-27.md`

Pass criteria:

- no key decision frame depends on a markdown table to remain understandable;
- Mermaid blocks have nearby text fallback or summary;
- YAML blocks remain readable in plain text and print;
- mobile viewport does not hide or overlap key headings, admonitions, diagrams, or code blocks;
- search index contains the main terms from each priority page;
- PDF and print outputs preserve page order, headings, captions, links, and code wrapping.

Recorded result:

- status: passed local MkDocs/search/test QA and automated browser/PDF/mobile smoke QA
- owner: editorial QA
- last run: 2026-05-29
- artifacts: `/private/tmp/agent-arch-render-qa-2026-05-29`
- scope: desktop and mobile screenshots, plain text checks, print media emulation, and PDF export for all priority pages after the Chapter 1 decision-frame polish
- blockers: independent human copy-edit and final print proof remain required before external submission
