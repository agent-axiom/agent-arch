# 100 editorial goals for companion and source verification

Date: 2026-06-28

Context:

- Companion templates/checklist have release-candidate headers.
- Trace/session/eval companion artifacts exist.
- Source verification packet exists.
- Final live fact-check is still pending.
- Author-owned metadata is still pending.

| # | Goal | Done when |
| --- | --- | --- |
| 2301 | Verify companion artifact manifest. | Manifest lists every generated artifact and source command. |
| 2302 | Validate trace demo JSONL. | `inspect-trace` reads the happy-path trace. |
| 2303 | Validate failed trace JSONL. | `inspect-trace` reads the failed timeout trace. |
| 2304 | Validate session JSON. | `python3 -m json.tool` parses session export. |
| 2305 | Validate eval dataset JSON. | `python3 -m json.tool` parses eval dataset. |
| 2306 | Add release decision example. | Companion has a filled release decision record example. |
| 2307 | Add incident record example. | Companion has a filled incident record example. |
| 2308 | Add capability contract example. | Companion has a filled capability contract example. |
| 2309 | Add production readiness example. | Companion has a filled checklist example. |
| 2310 | Add redacted trace example. | Companion demonstrates field redaction. |
| 2311 | Add approval resolution example. | Companion shows approval closure evidence. |
| 2312 | Add rollout gate example. | Companion shows rollout decision evidence. |
| 2313 | Link artifacts from runtime CLI page. | CLI companion page points to example artifacts. |
| 2314 | Link artifacts from trace/event page. | Trace companion page points to example JSONL. |
| 2315 | Link artifacts from eval page. | Eval companion page points to dataset example. |
| 2316 | Add artifact regeneration script or recipe. | Maintainer can regenerate all artifacts consistently. |
| 2317 | Add artifact freshness note. | Companion states artifacts match current runtime contracts. |
| 2318 | Check artifact file sizes. | Artifacts are small enough for repo and reader use. |
| 2319 | Check artifact privacy. | Example artifacts contain no real secrets or personal data. |
| 2320 | Check artifact naming. | Names are stable, descriptive and versionable. |
| 2321 | Verify OpenAI source URLs. | Official source records are current. |
| 2322 | Verify Anthropic source URLs. | Official source records are current. |
| 2323 | Verify LangGraph source URLs. | Official source records are current. |
| 2324 | Verify Google Cloud source URLs. | Official source records are current. |
| 2325 | Verify Microsoft source URLs. | Official source records are current. |
| 2326 | Verify Cloudflare source URLs. | Official source records are current. |
| 2327 | Verify AWS source URLs. | Official source records are current. |
| 2328 | Verify GitHub Copilot source URLs. | Official source records are current. |
| 2329 | Verify OWASP source URLs. | Official source records are current. |
| 2330 | Verify NIST/CISA source URLs. | Official source records are current. |
| 2331 | Verify MCP spec status. | Draft/final status is accurately represented. |
| 2332 | Verify A2A spec status. | Draft/final status is accurately represented. |
| 2333 | Verify agent registry terminology. | Microsoft/Google terminology is current. |
| 2334 | Verify sandbox terminology. | OpenAI/Google sandbox terms are current. |
| 2335 | Verify eval terminology. | Evals, trace grading and verifier terms are current. |
| 2336 | Verify memory terminology. | Memory/retrieval claims match current sources. |
| 2337 | Verify HITL terminology. | Human-in-the-loop claims match current sources. |
| 2338 | Verify legal case reference. | Case name, jurisdiction and date are correct. |
| 2339 | Verify research references. | Research claims are not overstated. |
| 2340 | Update source last-checked date. | `docs/appendix/sources.md` reflects real verification date. |
| 2341 | Remove stale chapter review notes. | Print flow contains no expired internal review notes. |
| 2342 | Generalize volatile API claims. | Fast-changing product details are not over-specific. |
| 2343 | Update source footnote titles. | Footnotes match current source titles. |
| 2344 | Update source verification packet. | Packet records completed source checks. |
| 2345 | Update fact-check backlog. | Completed checks are marked with evidence. |
| 2346 | Update companion readiness pass. | Release blockers reflect current companion state. |
| 2347 | Update clean handoff packet. | Handoff packet points to current source status. |
| 2348 | Update submission checklist. | Checklist distinguishes verified and pending facts. |
| 2349 | Update editor-facing brief. | Editor sees current fact-check status. |
| 2350 | Update author query packet. | Author-only facts remain separate from source checks. |
| 2351 | Collect author answers. | Author query packet is filled or explicitly deferred. |
| 2352 | Insert author answers into Google Doc. | Front matter no longer has author placeholders. |
| 2353 | Backport author answers. | Repository files match Google Doc author fields. |
| 2354 | Re-export raw DOCX. | Final author fields are in raw proof. |
| 2355 | Rebuild Template2000n proof. | Styled proof matches raw text. |
| 2356 | Render raw proof. | Page count and blank-like count are recorded. |
| 2357 | Render Template2000n proof. | Page count and blank-like count are recorded. |
| 2358 | Inspect first page. | Title/front matter are readable. |
| 2359 | Inspect minimum-density page. | Low-density page is intentional. |
| 2360 | Inspect final page. | Final page is not broken or blank. |
| 2361 | Validate raw DOCX archive. | `unzip -t` passes. |
| 2362 | Validate Template2000n archive. | `unzip -t` passes. |
| 2363 | Validate final render JSON. | JSON report parses. |
| 2364 | Run repository tests. | `uv run --group dev pytest` passes. |
| 2365 | Run strict docs build. | `uv run --group docs mkdocs build --strict` passes. |
| 2366 | Run whitespace check. | `git diff --check` is clean. |
| 2367 | Review untracked files. | Scratch artifacts stay out of commit. |
| 2368 | Review generated site changes. | Site output is not committed accidentally. |
| 2369 | Prepare final editor packet. | Packet contains only external-facing docs. |
| 2370 | Prepare final publisher packet. | Packet is ready for publisher workflow. |
| 2371 | Prepare proofreader packet. | Proofreader receives correct DOCX/PDF and questions. |
| 2372 | Prepare copyedit query list. | Copyeditor questions are grouped and actionable. |
| 2373 | Prepare author final report. | Author sees all remaining inputs and decisions. |
| 2374 | Prepare editor final report. | Editor sees review priorities and artifact status. |
| 2375 | Prepare source verification report. | Source checks have dated evidence. |
| 2376 | Prepare companion release report. | Companion blockers and routes are clear. |
| 2377 | Decide companion URL. | Public route is final. |
| 2378 | Decide companion version. | First book version is final. |
| 2379 | Decide companion license. | Template usage terms are final. |
| 2380 | Decide errata route. | Correction route is final. |
| 2381 | Decide changelog route. | Update route is final. |
| 2382 | Decide issue/discussion policy. | Reader contribution channel is final. |
| 2383 | Decide release branch. | Repo release path is explicit. |
| 2384 | Decide tag naming. | Tag name matches book/companion version. |
| 2385 | Decide PR path. | Integration path is explicit. |
| 2386 | Decide archived proof policy. | Superseded DOCX/PDF artifacts are handled intentionally. |
| 2387 | Decide Google Doc freeze point. | Editing freeze is recorded before copyedit. |
| 2388 | Decide semantic backport policy. | Google Doc comments become Markdown changes where needed. |
| 2389 | Resolve editor comments. | Structural comments are accepted, rejected or deferred. |
| 2390 | Resolve author comments. | Author factual comments are reflected in front matter. |
| 2391 | Resolve proofreader comments. | Proof comments are applied or tracked. |
| 2392 | Resolve publisher comments. | Publisher-specific formatting/metadata issues are closed. |
| 2393 | Check final placeholder scan. | No unintended placeholders remain. |
| 2394 | Check final link scan. | External and internal links are valid or intentionally deferred. |
| 2395 | Check final terminology scan. | Glossary and manuscript terms match. |
| 2396 | Check final book/companion boundary. | Print and companion responsibilities are clear. |
| 2397 | Check final page-count report. | Raw and styled proof page counts are recorded. |
| 2398 | Commit final readiness package. | Commit contains intended final files only. |
| 2399 | Push final readiness branch. | Remote branch contains latest package. |
| 2400 | Mark editorial readiness. | Remaining blockers are only explicit publisher or author decisions. |
