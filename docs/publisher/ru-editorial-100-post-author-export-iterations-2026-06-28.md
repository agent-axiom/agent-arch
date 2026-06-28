# 100 editorial goals for post-author final export

Date: 2026-06-28

Context:

- Clean editor handoff exists.
- Author query packet exists.
- Companion readiness pass exists.
- Final fact-check backlog exists.
- Post-author export workflow exists.
- Final export cannot be executed until author-owned facts are filled.

| # | Goal | Done when |
| --- | --- | --- |
| 2201 | Receive author query answers. | All required author-owned fields have explicit answers or `omit`. |
| 2202 | Validate short bio. | Short bio is factual, 40-70 words and publisher-ready. |
| 2203 | Validate long bio. | Long bio is factual, 120-180 words and free of unverifiable claims. |
| 2204 | Validate author public links. | URLs resolve and are safe to publish. |
| 2205 | Validate author role wording. | Role/title is precise and not inflated. |
| 2206 | Lock title. | Title is identical in Google Doc, DOCX, cover note and metadata. |
| 2207 | Lock subtitle. | Subtitle matches the book promise. |
| 2208 | Lock cover copy. | Cover copy reflects the manuscript without overpromising. |
| 2209 | Lock target reader wording. | Audience description matches the book's actual level. |
| 2210 | Lock keywords. | Keywords are useful for catalog metadata. |
| 2211 | Lock companion URL. | Public route is final or intentionally delayed. |
| 2212 | Lock companion release version. | First book edition version is defined. |
| 2213 | Lock errata route. | Reader correction path is defined. |
| 2214 | Lock changelog route. | Companion update history is defined. |
| 2215 | Lock template license. | Usage terms for templates are publishable. |
| 2216 | Lock AI tooling disclosure. | Disclosure is approved by author/publisher. |
| 2217 | Lock legal disclaimer. | Disclaimer is scoped and approved. |
| 2218 | Lock privacy/security note. | Examples and templates have correct limitations. |
| 2219 | Lock real/composite case policy. | Each case type is real, anonymized, composite or omitted. |
| 2220 | Lock acknowledgements. | Names are approved or section is removed. |
| 2221 | Lock publisher metadata. | ISBN/imprint/editor fields are filled or intentionally blank. |
| 2222 | Update Google Doc author block. | Placeholder block is replaced with final author text. |
| 2223 | Update Google Doc companion metadata. | Public companion/version/errata appear in front matter. |
| 2224 | Update Google Doc disclosure/disclaimer. | Approved wording is present. |
| 2225 | Update repository author fields. | Local author-open-fields file reflects final answers. |
| 2226 | Update cover note. | Cover note no longer contains author placeholders. |
| 2227 | Update clean handoff packet. | Packet reflects final author metadata. |
| 2228 | Update submission checklist. | Author-owned blockers are closed or explicitly deferred. |
| 2229 | Update manuscript map. | Current proof status points to final-author-fields artifacts. |
| 2230 | Update workflow log. | Google Doc revision and final export path are recorded. |
| 2231 | Export raw DOCX. | Dated raw DOCX artifact exists. |
| 2232 | Inspect raw DOCX text metrics. | Paragraphs, words and placeholders are counted. |
| 2233 | Check raw author placeholders. | No unintended `[заполнить]` remains. |
| 2234 | Check raw title page. | Title/front matter are not clipped. |
| 2235 | Render raw PDF. | Raw PDF render completes. |
| 2236 | Count raw pages. | PDF and PNG page counts match. |
| 2237 | Check raw blank-like pages. | Blank-like page count is 0 or explained. |
| 2238 | Inspect raw first page. | First page is readable. |
| 2239 | Inspect raw minimum-density page. | Low-density page is intentional content. |
| 2240 | Inspect raw final page. | Final page has no broken ending. |
| 2241 | Rebuild Template2000n proof. | Template proof reflects final author fields. |
| 2242 | Check Template2000n text equality. | Text sequence equals raw export or delta is documented. |
| 2243 | Check Template2000n paragraph count. | Paragraph count matches raw export or delta is intentional. |
| 2244 | Check Template2000n styles. | H2/H3 body-style debt remains closed. |
| 2245 | Render Template2000n PDF. | Template PDF render completes. |
| 2246 | Count Template2000n pages. | PDF and PNG page counts match. |
| 2247 | Check Template2000n blanks. | Blank-like page count is 0 or explained. |
| 2248 | Inspect Template2000n first page. | First page is readable. |
| 2249 | Inspect Template2000n minimum-density page. | Low-density page is intentional content. |
| 2250 | Inspect Template2000n final page. | Final page has no broken ending. |
| 2251 | Validate raw DOCX archive. | `unzip -t` passes. |
| 2252 | Validate Template2000n archive. | `unzip -t` passes. |
| 2253 | Validate render JSON. | `python -m json.tool` passes. |
| 2254 | Run whitespace check. | `git diff --check` passes. |
| 2255 | Run tests. | `uv run --group dev pytest` passes. |
| 2256 | Run strict docs build. | `uv run --group docs mkdocs build --strict` passes. |
| 2257 | Review generated site output. | Generated site is not committed accidentally. |
| 2258 | Review untracked files. | Scratch artifacts stay uncommitted. |
| 2259 | Verify source catalog date. | Last checked date reflects actual verification. |
| 2260 | Verify OpenAI sources. | Current claims match official sources. |
| 2261 | Verify Anthropic sources. | Current claims match official sources. |
| 2262 | Verify LangGraph sources. | Current claims match official sources. |
| 2263 | Verify Google Cloud sources. | Current claims match official sources. |
| 2264 | Verify Microsoft sources. | Current claims match official sources. |
| 2265 | Verify Cloudflare sources. | Current claims match official sources. |
| 2266 | Verify AWS sources. | Current claims match official sources. |
| 2267 | Verify GitHub Copilot sources. | Current claims match official sources. |
| 2268 | Verify OWASP sources. | Security references are current. |
| 2269 | Verify NIST/CISA sources. | Governance references are current. |
| 2270 | Verify MCP/A2A status. | Draft/final protocol language is accurate. |
| 2271 | Review model-name examples. | Synthetic model names are neutral or intentional. |
| 2272 | Review dated IDs. | Example dates cannot be mistaken for real claims. |
| 2273 | Review legal case references. | Jurisdiction/date framing is accurate. |
| 2274 | Review research claims. | Research is not overclaimed as consensus. |
| 2275 | Update companion template statuses. | Templates are no longer bare skeletons. |
| 2276 | Update companion checklist status. | Production readiness checklist is release-scoped. |
| 2277 | Add companion route headers. | Each route has chapter/user/status metadata. |
| 2278 | Generate trace example artifact. | Companion can show a stable trace sample. |
| 2279 | Generate failed-run artifact. | Companion can show a degraded-path sample. |
| 2280 | Generate session artifact. | Companion can show session-level evidence. |
| 2281 | Generate eval dataset artifact. | Companion can show regression-gate input. |
| 2282 | Generate release decision artifact. | Companion can show launch decision record. |
| 2283 | Generate incident record artifact. | Companion can show incident/postmortem linkage. |
| 2284 | Review companion links in print. | Print routes point to stable companion homes. |
| 2285 | Review glossary after fact-check. | Terms reflect final source vocabulary. |
| 2286 | Review chapter cross-references. | Part/chapter references match final manuscript. |
| 2287 | Review figure/table references. | Every reference has a visible artifact or fallback. |
| 2288 | Review editor comments. | Structural comments are resolved or tracked. |
| 2289 | Review copyedit questions. | Style decisions are closed or assigned. |
| 2290 | Prepare final author report. | Author sees final status and remaining obligations. |
| 2291 | Prepare final editor report. | Editor receives concise proof/readiness notes. |
| 2292 | Prepare final publisher packet. | Packet includes only external-facing files. |
| 2293 | Stage final export files. | Staged set contains intended artifacts only. |
| 2294 | Commit final export. | Commit message names final author-fields export. |
| 2295 | Push final export branch. | Remote branch contains final proof package. |
| 2296 | Decide PR path. | Review/merge route is explicit. |
| 2297 | Decide tag path. | Release/tag waits for publisher acceptance if needed. |
| 2298 | Decide archive policy. | Superseded proofs remain or are pruned intentionally. |
| 2299 | Decide external proofreader handoff. | Proofreader gets correct artifact and query list. |
| 2300 | Mark final readiness. | Remaining blockers are publisher acceptance or explicit author decisions only. |
