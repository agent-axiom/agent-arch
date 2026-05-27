# Review Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the remaining review-driven gaps that separate the current open manuscript from an externally reviewable publisher packet.

**Architecture:** Treat the May review as a regression and readiness backlog, not as a request to add more book volume. Preserve the work already landed on `docs-prod`: EN/ZH Cyrillic cleanup, RU/EN status sync, ZH draft-localization disclosure, freshness metadata, OWASP agent-specific sources, MCP/A2A contracts, verifier contract, governance telemetry, Part VIII role map, and publisher packet scaffolding.

**Tech Stack:** Markdown, MkDocs Material, `mkdocs-static-i18n`, JavaScript redirect shim, pytest documentation-surface tests, `uv run mkdocs build --strict`

---

## Current State From Local Audit

Already covered in the current tree:

- `docs/book/plan.en.md` uses the synced status model for RU core, EN draft cleanup, ZH draft localization preview, reference layer, runtime package, and publisher package.
- `rg -n "[А-Яа-яЁё]" docs -g "*.en.md" -g "*.zh.md"` returns no EN/ZH markdown Cyrillic leaks.
- `docs/index.zh.md`, `docs/start-here.zh.md`, and `docs/book/plan.zh.md` disclose ZH as a localization preview rather than a finished Chinese edition.
- `docs/appendix/sources*.md` already include OWASP AI Agent Security, OWASP MCP Security, OWASP LLM Prompt Injection Prevention, and OWASP RAG Security.
- `docs/book/part-iv/chapter-9*.md`, `docs/book/part-iv/practical-mcp-a2a*.md`, `docs/book/part-v/chapter-13*.md`, `docs/book/part-viii/chapter-26*.md`, and schema pages already cover the requested P1 security-contract material.
- `tests/test_docs_surface.py` contains regression tests for translated Cyrillic residue, Chapter 1/2 print-friendly frames, fast-moving freshness metadata, MCP/A2A, verifier contract, governance telemetry, and publisher packet structure.

Still open or worth tightening:

- `/book/part-iv/chapter-9` was explicitly named in the review, but the extensionless fallback pages and canonical redirect tests currently cover Chapter 1 and Chapter 13, not Chapter 9.
- `docs/whats-new*.md` now says the publisher-facing pass is in progress, but the earlier "publisher-readiness QA package is now closed" sentence can still be read too broadly.
- Rendering/export readiness is mostly guarded by markdown-surface tests, not by a recorded QA matrix for browser, plain text, PDF, print, mobile, and search extraction.
- External submission remains blocked by human/editorial inputs: author-bio framing, independent sample copy-edit, sample scope decision, and target editor/imprint formatting.

### Task 1: Close Chapter 9 Extensionless Routing

**Files:**
- Modify: `tests/test_docs_surface.py`
- Modify: `docs/javascripts/canonical-redirects.js`
- Create: `docs/book/part-iv/chapter-9.html`

- [ ] **Step 1: Add failing redirect coverage for Chapter 9**

In `test_public_book_canonical_redirects_are_configured`, add:

```python
'"/book/part-iv/chapter-9"',
```

In `test_public_book_canonical_redirects_add_trailing_slash_to_entrypoints`, add:

```python
    assert _canonical_redirects_for("/agent-arch/book/part-iv/chapter-9") == [
        "https://agent-axiom.github.io/agent-arch/book/part-iv/chapter-9/"
    ]
```

In `test_public_book_extensionless_fallback_redirect_pages_exist`, add:

```python
        "docs/book/part-iv/chapter-9.html": ("ru", "chapter-9/"),
```

- [ ] **Step 2: Run the targeted test and confirm it fails**

Run:

```bash
uv run pytest tests/test_docs_surface.py::test_public_book_canonical_redirects_are_configured tests/test_docs_surface.py::test_public_book_canonical_redirects_add_trailing_slash_to_entrypoints tests/test_docs_surface.py::test_public_book_extensionless_fallback_redirect_pages_exist -q
```

Expected: fail because Chapter 9 is not in `canonical-redirects.js` and `docs/book/part-iv/chapter-9.html` does not exist.

- [ ] **Step 3: Add Chapter 9 to the redirect shim**

Add this item to `canonicalDirectories` in `docs/javascripts/canonical-redirects.js`:

```javascript
    "/book/part-iv/chapter-9",
```

- [ ] **Step 4: Add the Chapter 9 extensionless fallback page**

Create `docs/book/part-iv/chapter-9.html` with:

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=chapter-9/">
  <link rel="canonical" href="chapter-9/">
  <script>
    window.location.replace("chapter-9/" + window.location.search + window.location.hash);
  </script>
</head>
<body>
  <a href="chapter-9/">Перейти к главе 9</a>
</body>
</html>
```

- [ ] **Step 5: Re-run the targeted redirect tests**

Run:

```bash
uv run pytest tests/test_docs_surface.py::test_public_book_canonical_redirects_are_configured tests/test_docs_surface.py::test_public_book_canonical_redirects_add_trailing_slash_to_entrypoints tests/test_docs_surface.py::test_public_book_extensionless_fallback_redirect_pages_exist -q
```

Expected: pass.

- [ ] **Step 6: Commit**

```bash
git add tests/test_docs_surface.py docs/javascripts/canonical-redirects.js docs/book/part-iv/chapter-9.html
git commit -m "docs: add chapter 9 canonical fallback"
```

### Task 2: Tighten Publish-Readiness Language In What's New

**Files:**
- Modify: `tests/test_docs_surface.py`
- Modify: `docs/whats-new.md`
- Modify: `docs/whats-new.en.md`
- Modify: `docs/whats-new.zh.md`

- [ ] **Step 1: Add a regression test for cautious publisher-readiness wording**

Add a test near the existing What's New surface tests:

```python
def test_whats_new_does_not_overstate_publisher_readiness() -> None:
    forbidden_markers = (
        "publisher-readiness QA package is now closed",
        "publisher-facing quality pass is closed",
        "закрыт publisher-facing слой качества",
        "издательский слой качества закрыт",
        "出版质量层已经关闭",
    )
    checked_files = (
        "docs/whats-new.md",
        "docs/whats-new.en.md",
        "docs/whats-new.zh.md",
    )

    for path in checked_files:
        text = _read(path)
        for marker in forbidden_markers:
            assert marker not in text, (path, marker)

    expected_by_file = {
        "docs/whats-new.md": (
            "Издательский проход качества идет, но еще не закрыт полностью.",
            "До статуса готовности к публикации еще остаются",
        ),
        "docs/whats-new.en.md": (
            "The publisher-facing quality pass is in progress, not fully closed.",
            "Remaining before this can be called publisher-ready",
        ),
        "docs/whats-new.zh.md": (
            "面向出版的质量检查正在进行中，但还没有完全关闭。",
            "在称为出版就绪之前，仍然需要完成",
        ),
    }

    for path, markers in expected_by_file.items():
        _assert_files_contain_all((path,), markers)
```

- [ ] **Step 2: Replace the broad closed-claim in English**

In `docs/whats-new.en.md`, replace:

```markdown
The first publisher-readiness QA package is now closed: the Chapter 1 decision frame was moved from a table into extraction-safe prose for HTML/PDF/plain-text surfaces, and fast-moving chapters, Sources, and What’s New now carry a fresh editorial review date.
```

with:

```markdown
The first review-remediation QA slice is closed: the Chapter 1 decision frame was moved from a table into extraction-safe prose for HTML/PDF/plain-text surfaces, and fast-moving chapters, Sources, and What’s New now carry a fresh editorial review date. The broader publisher-facing quality pass remains in progress.
```

- [ ] **Step 3: Mirror the same caution in Russian and Chinese**

Use equivalent wording in:

- `docs/whats-new.md`: "первый QA-срез по замечаниям ревью закрыт", with "более широкий publisher-facing quality pass остается в работе".
- `docs/whats-new.zh.md`: "第一轮评审修复 QA 切片已经关闭", with "更大的 publisher-facing quality pass 仍在进行中".

- [ ] **Step 4: Run targeted tests**

Run:

```bash
uv run pytest tests/test_docs_surface.py::test_whats_new_does_not_overstate_publisher_readiness -q
```

Expected: pass.

- [ ] **Step 5: Commit**

```bash
git add tests/test_docs_surface.py docs/whats-new.md docs/whats-new.en.md docs/whats-new.zh.md
git commit -m "docs: soften publisher readiness status"
```

### Task 3: Add A Render/Export QA Matrix Artifact

**Files:**
- Modify: `mkdocs.yml`
- Create: `docs/render-export-qa-checklist.md`
- Modify: `tests/test_docs_surface.py`

- [ ] **Step 1: Keep the QA artifact out of public navigation**

Add this line to `exclude_docs` in `mkdocs.yml`:

```yaml
  render-export-qa-checklist.md
```

- [ ] **Step 2: Add the checklist artifact**

Create `docs/render-export-qa-checklist.md`:

```markdown
# Render / Export QA Checklist

Purpose: record the checks required before calling the manuscript externally sendable.

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

- status: not run
- owner: editorial QA
- last run: not run
- blockers: not evaluated yet
```

- [ ] **Step 3: Add a documentation-surface test for the QA matrix**

Add:

```python
def test_render_export_qa_matrix_tracks_review_priority_pages() -> None:
    required_markers = (
        "Render / Export QA Checklist",
        "HTML browser",
        "plain text extraction",
        "PDF export",
        "print export",
        "mobile viewport",
        "search index extraction",
        "Chapter 1 decision frame",
        "Chapter 2 layer map",
        "Chapter 9 Mermaid / YAML / MCP sections",
        "Chapter 13 eval loop Mermaid",
        "Reference final rule",
        "Reference Package CLI / YAML blocks",
        "Chapter 26 telemetry lists",
        "Chapter 27 registry records",
        "status: not run",
    )
    _assert_files_contain_all(("docs/render-export-qa-checklist.md",), required_markers)
    assert "render-export-qa-checklist.md" in _read("mkdocs.yml")
```

- [ ] **Step 4: Run targeted tests**

Run:

```bash
uv run pytest tests/test_docs_surface.py::test_render_export_qa_matrix_tracks_review_priority_pages -q
```

Expected: pass.

- [ ] **Step 5: Commit**

```bash
git add mkdocs.yml docs/render-export-qa-checklist.md tests/test_docs_surface.py
git commit -m "docs: add render export qa matrix"
```

### Task 4: Execute And Record The QA Pass

**Files:**
- Modify: `docs/render-export-qa-checklist.md`

- [ ] **Step 1: Build the site strictly**

Run:

```bash
uv run mkdocs build --strict
```

Expected: exit code `0`.

- [ ] **Step 2: Run the documentation-surface tests**

Run:

```bash
uv run pytest tests/test_docs_surface.py -q
```

Expected: exit code `0`.

- [ ] **Step 3: Run the full test suite**

Run:

```bash
uv run pytest -q
```

Expected: exit code `0`.

- [ ] **Step 4: Check that the review priority pages appear in the search index**

Run:

```bash
rg -n "workflow|single-agent|multi-agent|MCP threat model|mcp_server|verifier_verdict|governance_action|registry record" site/search
```

Expected: all eight terms appear in the built search assets.

- [ ] **Step 5: Record the QA result**

Update the bottom of `docs/render-export-qa-checklist.md`:

```markdown
Recorded result:

- status: passed local MkDocs/search/test QA
- owner: editorial QA
- last run: 2026-05-28
- blockers: browser visual, PDF export, print export, and independent mobile visual QA still require a human/browser pass before external submission
```

- [ ] **Step 6: Commit**

```bash
git add docs/render-export-qa-checklist.md
git commit -m "docs: record local render export qa"
```

### Task 5: Preserve The Publisher Packet Boundary

**Files:**
- Modify: `docs/publisher-ready-toc.md`
- Modify: `tests/test_docs_surface.py`

- [ ] **Step 1: Add a test for the remaining external-submission blockers**

Add:

```python
def test_publisher_packet_keeps_external_submission_blockers_visible() -> None:
    required_markers = (
        "Still blocked before external submission",
        "Author bio and credential framing",
        "Independent sample copy-edit",
        "Sample selection",
        "Target editor / imprint formatting",
        "author explicitly waives",
    )
    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)
```

- [ ] **Step 2: Ensure the blocker register stays explicit**

If any of these lines are missing from `docs/publisher-ready-toc.md`, restore them:

```markdown
- **Author bio and credential framing**
- **Independent sample copy-edit**
- **Sample selection**
- **Target editor / imprint formatting**
```

- [ ] **Step 3: Run targeted tests**

Run:

```bash
uv run pytest tests/test_docs_surface.py::test_publisher_packet_keeps_external_submission_blockers_visible -q
```

Expected: pass.

- [ ] **Step 4: Commit**

```bash
git add docs/publisher-ready-toc.md tests/test_docs_surface.py
git commit -m "docs: keep publisher submission blockers visible"
```

### Task 6: Final Verification

**Files:**
- Verify only

- [ ] **Step 1: Re-run localization leak scans**

Run:

```bash
rg -n "[А-Яа-яЁё]" docs -g "*.en.md" -g "*.zh.md"
```

Expected: no output.

- [ ] **Step 2: Re-run review keyword checks**

Run:

```bash
rg -n "first chapter is published|План интеграции идей Google|Глава 24|Глава 25|Глава 26|Глава 27|publisher-facing quality pass is closed" docs mkdocs.yml
```

Expected: no stale or over-claiming hits in EN/ZH public surfaces.

- [ ] **Step 3: Run complete verification**

Run:

```bash
uv run pytest -q
uv run mkdocs build --strict
```

Expected: both commands exit `0`.

- [ ] **Step 4: Summarize remaining non-code blockers**

Report these as still requiring human/editorial input:

- author bio and credential framing;
- independent sample copy-edit;
- target-specific sample decision;
- target editor/imprint formatting;
- real browser/PDF/print/mobile visual QA if not completed in the current environment.
