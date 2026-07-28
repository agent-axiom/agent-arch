# 100 editorial goals after H3/body-style normalization

Date: 2026-06-28

Context:

- Google Doc source was normalized with style-only H3/body-style updates.
- Raw proof: 499 pages, blank-like pages: 0.
- Template2000n proof: 315 pages, blank-like pages: 0.
- Long non-empty `Heading 2` debt: 0.
- Long non-empty `Heading 3` debt: 0.
- Text equality was preserved across the style-only pass.

| # | Goal | Done when |
| --- | --- | --- |
| 2001 | Reconfirm manuscript outline after H2/H3 cleanup. | TOC-level H1/H2/H3 headings reflect real structure, not body paragraphs. |
| 2002 | Check front matter after style cleanup. | Annotation, keywords, author block, preface and reading guide are in the intended order. |
| 2003 | Fill author short bio. | `[Имя автора]`, role and public positioning are replaced with final author text. |
| 2004 | Fill author extended bio. | Verified experience, projects and links are included without inflated claims. |
| 2005 | Fill author publisher wording. | The author block has a concise version acceptable for the publisher packet. |
| 2006 | Confirm title and subtitle. | Cover, metadata, Google Doc title and front matter use the same wording. |
| 2007 | Confirm companion public URL. | Companion route is stable, public and versioned for the book edition. |
| 2008 | Confirm companion version policy. | `v1.0-book`, errata and changelog rules are stated. |
| 2009 | Confirm AI tooling disclosure. | Disclosure is factual, short and editor-ready. |
| 2010 | Confirm legal/compliance disclaimer. | Disclaimer is appropriate for an IT architecture book and not overbroad. |
| 2011 | Proofread annotation. | The first-page promise matches the full manuscript, not the old compressed version. |
| 2012 | Proofread keywords. | Terms are useful for metadata and not a raw keyword dump. |
| 2013 | Proofread preface. | It explains why the Russian edition exists and does not repeat the introduction. |
| 2014 | Proofread reading guide. | It tells readers how to use chapters, templates and companion routes. |
| 2015 | Review book/companion boundary statement. | Print and companion responsibilities are clear before chapter 1. |
| 2016 | Review Chapter 1 as sample opening. | Chapter 1 is strong enough to be sent as the primary sample. |
| 2017 | Review Chapter 2 decision ladder. | Workflow, single-agent, multi-agent and handoff distinctions are crisp. |
| 2018 | Review Chapter 3 architecture bridge. | Chapter 3 exits cleanly into security and control. |
| 2019 | Review Chapter 4 trust-boundary argument. | Security is framed as action/control architecture, not generic risk prose. |
| 2020 | Review Chapter 5 identity/session/policy terminology. | The chapter is conceptual and not duplicated by Chapter 22. |
| 2021 | Review Chapter 6 tool gateway narrative. | Tool calls, approvals and audit log are connected as one side-effect boundary. |
| 2022 | Review Chapter 7 memory risk framing. | Memory is treated as durable state with ownership and rollback. |
| 2023 | Review Chapter 8 memory types. | Short-term, long-term and profile memory are not just labels. |
| 2024 | Review Chapter 9 context and retrieval. | Provenance, freshness and tenant boundary remain visible. |
| 2025 | Review Chapter 10 execution model. | Runtime decisions are explained without becoming API reference. |
| 2026 | Review Chapter 11 sandbox and MCP. | MCP is treated as an integration contract, not vendor-specific hype. |
| 2027 | Review Chapter 12 idempotency and rollback. | Retry, limits and rollback are understandable to product and engineering readers. |
| 2028 | Review Chapter 13 trace model. | Trace, span and event vocabulary is consistent with glossary. |
| 2029 | Review Chapter 14 SLO model. | Metrics are connected to owner decisions and not only observability tooling. |
| 2030 | Review Chapter 15 eval gates. | Offline/online evals are positioned as release gates, not a test catalog. |
| 2031 | Review Chapter 16 evidence chain. | Request, trace, eval, approval and rollout evidence form one chain. |
| 2032 | Review Chapter 17 operating model. | Platform team and product teams have clear ownership boundaries. |
| 2033 | Review Chapter 18 golden paths. | Common gateways reduce sprawl without over-centralizing product work. |
| 2034 | Review Chapter 19 ADLC lifecycle. | ADLC differs from SDLC in concrete artifacts and gates. |
| 2035 | Review Chapter 20 assurance and incidents. | Assurance, incident response, registry and retirement are balanced. |
| 2036 | Review Chapter 21 reference runtime. | It reads as narrative reference implementation, not CLI manual. |
| 2037 | Review Chapter 22 policy/catalog implementation. | It complements Chapter 5 and avoids conceptual repetition. |
| 2038 | Review Chapter 23 launch checklist. | The checklist synthesizes the book and does not introduce large new theory. |
| 2039 | Review glossary coverage. | Every high-frequency English term has a consistent explanation. |
| 2040 | Review practical cases. | Cases are useful for workshops and tied to the chapters. |
| 2041 | Review appendices. | Appendices are short working aids, not hidden extra chapters. |
| 2042 | Normalize chapter endings. | Repeated ending templates feel intentional and compact. |
| 2043 | Strengthen running support-agent case. | The recurring case appears across parts without forced repetition. |
| 2044 | Check Russian/English term balance. | English remains only for stable engineering artifacts or lookup terms. |
| 2045 | Check figure references. | Every figure reference has a figure, caption or prose fallback. |
| 2046 | Check table readability. | Tables fit the print flow and do not require horizontal scrolling assumptions. |
| 2047 | Check code-like snippets. | Long YAML/CLI/payload material is routed to companion. |
| 2048 | Check list density. | Dense lists are not masquerading as prose or headings. |
| 2049 | Check quote punctuation. | Russian quotes and English terms are typographically consistent. |
| 2050 | Check dash and hyphen policy. | Dashes, minus signs and compound terms are consistent enough for copyedit. |
| 2051 | Check cross-references to chapters. | Chapter numbers and names match the current 7/23 structure. |
| 2052 | Check references to parts. | No old 8-part web structure remains in reader-facing prose. |
| 2053 | Check companion references. | Each companion route points to a stable intended home. |
| 2054 | Check source references. | Bibliography and source catalog are curated for book use. |
| 2055 | Check author placeholders. | No `[заполнить]` remains except explicitly author-owned fields. |
| 2056 | Check publisher placeholders. | ISBN, imprint and editor-specific fields are either filled or absent. |
| 2057 | Check acknowledgements decision. | Acknowledgements are filled or intentionally removed. |
| 2058 | Check cover-note alignment. | Cover note reflects current 499/315 proof state and open fields. |
| 2059 | Check submission checklist status. | Checklist distinguishes editor-review readiness from final submission readiness. |
| 2060 | Check roadmap status. | Roadmap does not present old H2/H3 debt as current risk. |
| 2061 | Check manuscript map status. | Current proof points to H3-normalized raw and Template2000n artifacts. |
| 2062 | Check Google Doc workflow status. | Workflow records the latest Google Doc revision and proof artifacts. |
| 2063 | Check evolution ledger status. | Ledger includes H3 cleanup as a completed checkpoint. |
| 2064 | Prepare editor note for style-only passes. | Editor can see what changed and that text was preserved. |
| 2065 | Prepare publisher artifact inventory. | Raw DOCX, Template2000n DOCX, QA JSON and reports are listed. |
| 2066 | Prepare final proofing route. | The next proofread order is front matter, chapters, appendices, then artifacts. |
| 2067 | Prepare copyedit query list. | Open terminology or style decisions are phrased as editor questions. |
| 2068 | Prepare author query list. | Only author-owned factual gaps are assigned to the author. |
| 2069 | Prepare companion readiness checklist. | README, errata, changelog, templates and examples have owners. |
| 2070 | Prepare external packet scope. | Internal iteration reports are excluded unless requested. |
| 2071 | Re-export raw DOCX after author fields. | Author-owned front matter is reflected in the proof. |
| 2072 | Rebuild Template2000n after author fields. | Template proof text matches final raw export. |
| 2073 | Render raw proof after author fields. | Page count and blank-like pages are recorded. |
| 2074 | Render Template2000n after author fields. | Page count and blank-like pages are recorded. |
| 2075 | Apply publisher styles when final style package is confirmed. | Style application is tracked separately from text edits. |
| 2076 | Render publisher-styled proof. | Styled DOCX has no blank-like pages or clipped headings. |
| 2077 | Check title page in styled proof. | Title and subtitle match publisher expectations. |
| 2078 | Check first 20 pages in styled proof. | Front matter and introduction do not have layout regressions. |
| 2079 | Check all chapter starts in styled proof. | No chapter opens with broken spacing or orphaned heading. |
| 2080 | Check final appendix pages in styled proof. | No trailing blank or clipped companion route remains. |
| 2081 | Validate QA JSON after final proof. | JSON parses and matches actual render counts. |
| 2082 | Validate raw DOCX archive. | `unzip -t` passes. |
| 2083 | Validate Template2000n DOCX archive. | `unzip -t` passes. |
| 2084 | Validate publisher-styled DOCX archive. | `unzip -t` passes. |
| 2085 | Run `git diff --check`. | Whitespace and Markdown formatting are clean. |
| 2086 | Run repository tests. | `uv run --group dev pytest` passes or failures are documented. |
| 2087 | Run docs build. | `uv run --group docs mkdocs build --strict` passes. |
| 2088 | Review generated site diff. | Generated `site/` changes are not committed unless intended. |
| 2089 | Review untracked artifacts. | Old scratch exports stay uncommitted unless explicitly needed. |
| 2090 | Commit proof artifacts. | Commit includes only current reports, DOCX artifacts and relevant docs. |
| 2091 | Push branch. | Remote branch contains the latest H3 cleanup pass. |
| 2092 | Prepare final author report. | The report lists completed work, proof pages and open author fields. |
| 2093 | Prepare final editor report. | The report is shorter and omits internal workflow noise. |
| 2094 | Prepare final publisher packet. | Packet includes manuscript link, proof artifacts and author metadata. |
| 2095 | Decide PR/tag/release route. | Branch integration path is explicit after review. |
| 2096 | Decide whether to keep raw Google Docs styles. | Final workflow states whether Google Doc or DOCX is the style source. |
| 2097 | Decide whether to regenerate Markdown source. | Any semantic Google Doc changes are backported to Markdown. |
| 2098 | Decide companion release date. | Companion launch is aligned with publisher review timeline. |
| 2099 | Decide final external proofreader handoff. | Proofreader gets the right DOCX/PDF and open questions. |
| 2100 | Produce final publisher-ready decision. | Remaining blockers are author fields, publisher style application or external proofread only. |
