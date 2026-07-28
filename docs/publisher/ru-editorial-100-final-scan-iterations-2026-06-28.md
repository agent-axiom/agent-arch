# 100 editorial goals for final scan and editor intake

Date: 2026-06-28

Context:

- Filled companion examples exist.
- Runtime-reference pages link to generated artifacts.
- Source verification records exist but are not live-verified.
- Editor comment intake workflow exists.
- Final placeholder/link scan workflow exists.
- Author-owned metadata is still pending.

| # | Goal | Done when |
| --- | --- | --- |
| 2401 | Validate capability contract example. | Example maps to template fields and has no accidental real data. |
| 2402 | Validate release decision example. | Example contains decision, evidence, constraints and rationale. |
| 2403 | Validate incident record example. | Example contains identity, evidence, impact, timeline and actions. |
| 2404 | Validate readiness example. | Example checklist has a clear hold/approve decision. |
| 2405 | Link examples from companion index. | All examples are discoverable from companion routes. |
| 2406 | Link artifacts from CLI page. | CLI page shows commands for generated artifacts. |
| 2407 | Link artifacts from trace page. | Trace page points to happy-path and failed traces. |
| 2408 | Link artifacts from eval page. | Eval page points to session/eval JSON examples. |
| 2409 | Verify artifact regeneration commands. | Manifest commands regenerate current files. |
| 2410 | Verify artifact validation commands. | Validation commands pass on current artifacts. |
| 2411 | Add source verification dates. | Each source batch has a checked date after live review. |
| 2412 | Add source verification results. | Each source batch has unchanged/updated/removed/generalized result. |
| 2413 | Update OpenAI claims. | OpenAI-related manuscript claims match current official docs. |
| 2414 | Update Anthropic claims. | Anthropic-related manuscript claims match current official docs. |
| 2415 | Update LangGraph claims. | LangGraph-related manuscript claims match current official docs. |
| 2416 | Update Google Cloud claims. | Google-related manuscript claims match current official docs. |
| 2417 | Update Microsoft claims. | Microsoft-related manuscript claims match current official docs. |
| 2418 | Update Cloudflare/AWS claims. | Cloudflare/AWS-related claims match current official docs. |
| 2419 | Update OWASP claims. | OWASP references and names are current. |
| 2420 | Update NIST/CISA claims. | Governance source references are current. |
| 2421 | Update MCP/A2A claims. | Protocol status and terminology are accurate. |
| 2422 | Update research claims. | Research references are framed with proper confidence. |
| 2423 | Remove stale review notes. | Final print flow has no expired internal review metadata. |
| 2424 | Scan author placeholders. | Author-owned placeholders are isolated to author packets/front matter. |
| 2425 | Scan manuscript placeholders. | Reader-facing manuscript has no unintended placeholders. |
| 2426 | Scan companion placeholders. | Release routes do not contain accidental placeholders. |
| 2427 | Scan publisher placeholders. | External packet has only intentional author-owned gaps. |
| 2428 | Scan TODO/FIXME. | No TODO/FIXME remains in final-facing content. |
| 2429 | Scan old compressed doc links. | Old 71-72 page Google Doc is never presented as main manuscript. |
| 2430 | Scan stale skeleton labels. | `skeleton` appears only in historical reports or intentional backlog. |
| 2431 | Run strict docs build. | `mkdocs build --strict` passes. |
| 2432 | Run repository tests. | `uv run --group dev pytest` passes. |
| 2433 | Run whitespace check. | `git diff --check` passes. |
| 2434 | Review generated site changes. | Site output is not committed accidentally. |
| 2435 | Review untracked scratch files. | Scratch exports stay uncommitted unless needed. |
| 2436 | Export editor comments. | Google Doc comment list is captured or summarized. |
| 2437 | Categorize editor comments. | Every comment has category and owner. |
| 2438 | Decide structure comments. | Structural comments are accepted, rejected or deferred. |
| 2439 | Decide line-edit comments. | Line edits are accepted, rejected or deferred. |
| 2440 | Decide terminology comments. | Terminology comments update glossary or are deferred. |
| 2441 | Decide source comments. | Source comments get verification records. |
| 2442 | Decide companion-boundary comments. | Print/companion split is updated where needed. |
| 2443 | Decide author-owned comments. | Author questions are moved to author query packet. |
| 2444 | Decide layout/export comments. | Layout issues are handled after final author fields. |
| 2445 | Backport accepted semantic edits. | Markdown source includes accepted meaning changes. |
| 2446 | Sync accepted edits to Google Doc. | Google Doc reflects accepted Markdown changes. |
| 2447 | Re-export after editor batch. | Raw proof reflects accepted comment batch. |
| 2448 | Rebuild Template2000n after editor batch. | Styled proof reflects accepted comment batch. |
| 2449 | Render raw proof after editor batch. | Page count and blank-like pages are recorded. |
| 2450 | Render Template2000n after editor batch. | Page count and blank-like pages are recorded. |
| 2451 | Fill author short bio. | Front matter has final short author bio. |
| 2452 | Fill author long bio. | Front matter has final long author bio. |
| 2453 | Fill author links. | Public links are stable and approved. |
| 2454 | Fill title/subtitle. | Title/subtitle are final across packet. |
| 2455 | Fill cover copy. | Cover copy is publisher-ready. |
| 2456 | Fill companion URL. | Public route is final. |
| 2457 | Fill companion version. | Book companion release version is final. |
| 2458 | Fill errata/changelog route. | Reader update routes are final. |
| 2459 | Fill AI disclosure. | AI tooling disclosure is approved. |
| 2460 | Fill legal disclaimer. | Legal/compliance disclaimer is approved. |
| 2461 | Fill case policy. | Real/anonymized/composite case policy is approved. |
| 2462 | Fill acknowledgements. | Acknowledgements are final or removed. |
| 2463 | Fill publisher metadata. | Publisher metadata is final or intentionally blank. |
| 2464 | Export final raw DOCX. | Raw proof includes final author fields. |
| 2465 | Build final Template2000n DOCX. | Template proof includes final author fields. |
| 2466 | Render final raw proof. | Final raw pages and blank-like count are recorded. |
| 2467 | Render final Template2000n proof. | Final styled pages and blank-like count are recorded. |
| 2468 | Inspect first page. | First page is readable and correct. |
| 2469 | Inspect minimum-density page. | Low-density page is intentional content. |
| 2470 | Inspect final page. | Final page is not blank or clipped. |
| 2471 | Validate final DOCX archives. | `unzip -t` passes for raw and styled DOCX. |
| 2472 | Validate final render JSON. | JSON report parses and matches counts. |
| 2473 | Update final handoff packet. | External packet points to final artifacts. |
| 2474 | Update roadmap. | Roadmap reflects current final blockers only. |
| 2475 | Update workflow. | Google Doc revision and proof artifacts are recorded. |
| 2476 | Update manuscript map. | Current proof status is final. |
| 2477 | Update evolution ledger. | Final export stage is recorded. |
| 2478 | Update submission checklist. | Checklist distinguishes final done/pending gates. |
| 2479 | Prepare publisher email/cover note. | Cover note has no placeholders. |
| 2480 | Prepare editor report. | Editor report is concise and external-facing. |
| 2481 | Prepare author report. | Author report lists final own decisions. |
| 2482 | Prepare proofreader report. | Proofreader gets correct artifact and questions. |
| 2483 | Prepare companion release notes. | Companion notes include version, URL and examples. |
| 2484 | Prepare source verification report. | Source check evidence is dated. |
| 2485 | Decide PR/merge path. | Integration route is explicit. |
| 2486 | Decide release/tag path. | Release tag route is explicit. |
| 2487 | Decide archive policy. | Superseded artifacts are kept or removed intentionally. |
| 2488 | Decide Google Doc freeze. | Final editing freeze point is recorded. |
| 2489 | Decide post-publication errata workflow. | Errata owner and process are final. |
| 2490 | Decide companion maintenance owner. | Companion owner after publication is final. |
| 2491 | Check final package scope. | Internal logs are excluded from external packet. |
| 2492 | Check final Google Doc access. | Editor/publisher access is correct. |
| 2493 | Check final DOCX access. | Publisher can open final DOCX. |
| 2494 | Check final companion access. | Public companion route is reachable. |
| 2495 | Check final source paths. | Repo source paths in packet are stable. |
| 2496 | Check final branch state. | Branch contains intended commits only. |
| 2497 | Commit final scan package. | Commit includes intended final scan files. |
| 2498 | Push final scan package. | Remote branch contains latest package. |
| 2499 | Prepare final status summary. | User sees completed work and remaining author tasks. |
| 2500 | Mark ready for publisher decision. | Only explicit publisher/author decisions remain. |
