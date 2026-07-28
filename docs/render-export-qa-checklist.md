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
- Chapter 1, Chapter 2, and the Reference page keep their main decision/list/layer-map blocks readable after plain text extraction;
- Mermaid blocks have nearby text fallback or summary;
- YAML blocks remain readable in plain text and print;
- print CSS keeps tables, Mermaid wrappers, YAML/code blocks, and diagram cards from splitting awkwardly when possible;
- mobile viewport does not hide or overlap key headings, admonitions, diagrams, or code blocks;
- search index contains the main terms from each priority page;
- PDF and print outputs preserve page order, headings, captions, links, and code wrapping.

Recorded result:

- status: refreshed for Chapter 1 decision-frame prose, Chapter 2 layer-map fallback prose, Reference final rule prose, print CSS guardrails, and fallback static QA; live browser/PDF proof remains required
- owner: editorial QA
- last run: 2026-06-13
- artifacts: not produced in this sandbox; in-app browser webview attach timed out and the local serve port was not reachable from a separate smoke-check process
- scope: local tests, strict MkDocs build, static redirect artifact checks, targeted plain-text checks, and print-CSS guardrails for priority pages after the June surface pass
- blockers: live browser/PDF visual proof, independent human copy-edit, and final print proof remain required before external submission
