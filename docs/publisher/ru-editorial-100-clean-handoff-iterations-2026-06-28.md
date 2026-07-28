# 100 editorial goals after clean editor handoff

Date: 2026-06-28

Context:

- Current Google Doc is the full manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Raw editorial-ready proof: 499 pages, blank-like pages: 0.
- Template2000n editorial-ready proof: 315 pages, blank-like pages: 0.
- H2/H3 body-style debt: closed for the current proof.
- Author-owned fields are isolated but not filled.

| # | Goal | Done when |
| --- | --- | --- |
| 2101 | Confirm clean packet scope. | External packet excludes internal iteration logs unless requested. |
| 2102 | Confirm Google Doc is the review source. | Editor link points to the full manuscript, not the compressed snapshot. |
| 2103 | Confirm raw proof artifact. | Raw DOCX path and 499-page QA result are recorded. |
| 2104 | Confirm Template2000n proof artifact. | Template DOCX path and 315-page QA result are recorded. |
| 2105 | Confirm render QA JSON. | JSON parses and matches current page counts. |
| 2106 | Confirm author field list. | Every author-owned field appears in one consolidated checklist. |
| 2107 | Fill short author bio. | Front matter has a verified short bio. |
| 2108 | Fill long author bio. | Extended bio is factual, concise and publisher-ready. |
| 2109 | Fill role and title. | Author role is specific and not inflated. |
| 2110 | Fill public links. | GitHub, site, blog or profile URLs are stable. |
| 2111 | Fill public project facts. | Projects are real, checkable and safe to publish. |
| 2112 | Confirm final book title. | Google Doc, DOCX, cover note and metadata match. |
| 2113 | Confirm subtitle. | Subtitle states the offer without overpromising. |
| 2114 | Confirm cover copy. | Back-cover copy matches the manuscript promise. |
| 2115 | Confirm companion URL. | Public route is live or explicitly scheduled. |
| 2116 | Confirm companion version. | `v1.0-book` or equivalent release label is chosen. |
| 2117 | Confirm errata route. | Readers know where corrections will live. |
| 2118 | Confirm changelog policy. | Companion updates can be tracked after publication. |
| 2119 | Confirm AI tooling disclosure. | Disclosure is factual and acceptable to the publisher. |
| 2120 | Confirm legal disclaimer. | Disclaimer is scoped to architecture guidance. |
| 2121 | Confirm case-study policy. | Real, anonymized and composite cases are clearly distinguished. |
| 2122 | Confirm acknowledgements. | Names are approved or the block is removed. |
| 2123 | Confirm publisher metadata. | Imprint, ISBN and editorial fields are filled or intentionally blank. |
| 2124 | Review annotation after author fields. | First-page positioning still matches the book. |
| 2125 | Review keywords after title lock. | Metadata terms are useful and not duplicated noise. |
| 2126 | Review preface after author fields. | Preface has the correct author voice. |
| 2127 | Review reading guide. | It explains how to use print and companion together. |
| 2128 | Review Chapter 1 opening. | Opening failure story leads naturally to platform responsibility. |
| 2129 | Review Chapter 2 decision model. | Workflow, agent and multi-agent choices are easy to compare. |
| 2130 | Review Chapter 3 architecture map. | The system map is clear before security chapters begin. |
| 2131 | Review Chapter 4 trust boundaries. | Threats are connected to control points. |
| 2132 | Review Chapter 5 policy concepts. | Conceptual policy model does not duplicate Chapter 22. |
| 2133 | Review Chapter 6 side effects. | Tool gateway and approvals read as one mechanism. |
| 2134 | Review Chapter 7 memory risk. | Memory is treated as durable state with owners. |
| 2135 | Review Chapter 8 memory taxonomy. | Memory types lead to design decisions, not labels only. |
| 2136 | Review Chapter 9 retrieval. | Context, provenance and freshness are balanced. |
| 2137 | Review Chapter 10 execution model. | Runtime explanation stays architectural. |
| 2138 | Review Chapter 11 sandbox and MCP. | MCP references are stable and not vendor hype. |
| 2139 | Review Chapter 12 retries and rollback. | Limits and idempotency are clear for product teams. |
| 2140 | Review Chapter 13 trace vocabulary. | Trace, span and event terms match glossary. |
| 2141 | Review Chapter 14 SLO model. | SLOs connect technical signals to owner decisions. |
| 2142 | Review Chapter 15 eval gates. | Offline and online checks support release judgment. |
| 2143 | Review Chapter 16 evidence chain. | Evidence reads as one operational chain. |
| 2144 | Review Chapter 17 operating model. | Platform and product team responsibilities are distinct. |
| 2145 | Review Chapter 18 golden paths. | Shared gateways reduce sprawl without blocking teams. |
| 2146 | Review Chapter 19 ADLC. | Agent lifecycle differs concretely from SDLC. |
| 2147 | Review Chapter 20 assurance. | Assurance, incidents, registry and retirement are balanced. |
| 2148 | Review Chapter 21 reference runtime. | Runtime chapter is narrative, not a CLI manual. |
| 2149 | Review Chapter 22 policy/catalog runtime. | It complements earlier policy chapters. |
| 2150 | Review Chapter 23 launch checklist. | It synthesizes the book without adding large new theory. |
| 2151 | Review glossary. | High-frequency terms have one stable meaning. |
| 2152 | Review practical cases. | Cases are reusable in workshops and review meetings. |
| 2153 | Review appendices. | Appendices are aids, not hidden chapters. |
| 2154 | Review companion boundary. | Long executable material has a stable online home. |
| 2155 | Review cross-references. | Chapter and part references match the 7/23 structure. |
| 2156 | Review figure and table references. | Every reference has a visible artifact or prose fallback. |
| 2157 | Review code-like blocks. | Print keeps only examples that aid understanding. |
| 2158 | Review list density. | Dense lists are either useful checklists or converted to prose. |
| 2159 | Review repeated endings. | Repetition is intentional and compact. |
| 2160 | Review running case. | The support-agent case carries the reader through the book. |
| 2161 | Review Russian/English balance. | English terms remain where they are necessary lookup names. |
| 2162 | Review current provider facts. | Fast-changing API/provider/model statements are rechecked. |
| 2163 | Review OpenAI-specific statements. | Current facts are verified against official sources before publication. |
| 2164 | Review security claims. | Claims are framed as architecture guidance, not guarantees. |
| 2165 | Review legal/compliance language. | Risk language is precise and not alarmist. |
| 2166 | Review privacy language. | Tenant, identity and data-boundary explanations are consistent. |
| 2167 | Review operational ownership. | Every durable artifact has a named owner type. |
| 2168 | Review incident language. | Incident response is actionable but not overly process-heavy. |
| 2169 | Review retirement language. | End-of-life guidance is connected to inventory and evidence. |
| 2170 | Review bibliography/source catalog. | Sources are curated for the print book. |
| 2171 | Prepare editor query list. | Open questions are grouped by structure, terminology and facts. |
| 2172 | Prepare author query list. | Only factual author-owned gaps are assigned to the author. |
| 2173 | Prepare copyedit query list. | Style decisions are phrased for copyeditor resolution. |
| 2174 | Prepare companion readiness query list. | Missing online artifacts have owners and dates. |
| 2175 | Re-export raw DOCX after author fields. | Proof reflects final front matter. |
| 2176 | Rebuild Template2000n after author fields. | Template proof text equals raw export text. |
| 2177 | Render raw proof after author fields. | Page count and blank-like pages are recorded. |
| 2178 | Render Template2000n after author fields. | Page count and blank-like pages are recorded. |
| 2179 | Inspect first page. | Title/front matter are readable and not clipped. |
| 2180 | Inspect minimum-density page. | Low-density page is intentional content, not blank output. |
| 2181 | Inspect final page. | No trailing blank or clipped ending remains. |
| 2182 | Validate raw DOCX archive. | `unzip -t` passes. |
| 2183 | Validate Template2000n DOCX archive. | `unzip -t` passes. |
| 2184 | Validate render QA JSON. | `python -m json.tool` passes. |
| 2185 | Run whitespace check. | `git diff --check` is clean. |
| 2186 | Run repository tests. | `uv run --group dev pytest` passes or failures are explained. |
| 2187 | Run strict docs build. | `uv run --group docs mkdocs build --strict` passes. |
| 2188 | Review generated artifacts. | Build outputs are not committed accidentally. |
| 2189 | Review untracked files. | Old scratch exports stay out of the commit. |
| 2190 | Stage current handoff files. | Staged set contains only intended artifacts. |
| 2191 | Commit current handoff files. | Commit message reflects manuscript editor handoff. |
| 2192 | Push branch. | Remote branch contains current proof artifacts and reports. |
| 2193 | Prepare author-facing report. | Report lists what changed and what author must fill. |
| 2194 | Prepare editor-facing report. | Report lists proof artifacts and review priorities. |
| 2195 | Prepare publisher-facing report. | Report omits internal iteration history and focuses on readiness. |
| 2196 | Decide PR route. | Integration path is explicit after push. |
| 2197 | Decide final tag route. | Release/tag is deferred until author fields and proofread close. |
| 2198 | Decide companion release route. | Companion launch aligns with manuscript review timeline. |
| 2199 | Decide external proofreader handoff. | Proofreader receives the correct DOCX/PDF and query list. |
| 2200 | Produce final readiness decision. | Remaining blockers are only author fields, external proofread and final publisher acceptance. |
