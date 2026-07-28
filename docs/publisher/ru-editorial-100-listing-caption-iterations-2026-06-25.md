# 100 listing-compression iterations for редакционная подготовка

Дата прохода: 2026-06-25.

Назначение: продолжить backlog 401-500 после listing-caption pass. Эти итерации 501-600 фокусируются на фактическом сокращении dense listing layer: в печатной книге должны остаться только representative excerpts, а полные YAML, code, CLI, trace catalogs, validation-message catalogs и runtime walkthrough должны быть вынесены в companion routes.

Исходная точка:

- Google Doc source: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
- fresh Google Docs export after listing-caption pass: 655 страниц, blank-like pages: 0;
- Template2000n listing-caption derivative: 345 страниц, blank-like pages: 0;
- generic listing labels removed: `Листинг (YAML):` = 0, `Листинг (Python):` = 0;
- semantic listing captions: 28;
- remaining debt: dense field-name prose, full config/code/reference material, companion route mapping, author-owned fields;
- предыдущий backlog: `docs/publisher/ru-editorial-100-codeblock-iterations-2026-06-24.md`;
- этот backlog: дополнительные итерации 501-600.

## Итерации 501-600

| # | Цель итерации | Критерий готовности | Следующий action |
| ---: | --- | --- | --- |
| 501 | Caption-to-block inventory | Для всех 28 captions найден ближайший listing block | Создать compression ledger |
| 502 | Listing block boundaries | У каждого listing есть start/end в Google Doc | Разделить на print/companion |
| 503 | Companion route ledger | Для каждого полного артефакта назначен route | Обновить manifest |
| 504 | Print excerpt budget | Для каждого listing задан лимит строк/абзацев | Сжать oversized blocks |
| 505 | Field-name sequence audit | Найдены страницы с длинными цепочками полей | Сократить до examples |
| 506 | Chapter 12 excerpt compression | Write/retry/rollback YAML оставлен как representative excerpts | Full YAML to companion |
| 507 | Chapter 12 outcome matrix compression | Outcome matrix показывает только decision branches | Full matrix to companion |
| 508 | Chapter 12 trace event compression | Trace events показывают evidence shape | Full event catalog to companion |
| 509 | Chapter 12 eval scenario compression | Eval scenario остается коротким release-gate example | Full eval dataset to companion |
| 510 | Chapter 12 post-pass render | Chapter 12 pages have no dense dump pages | Template spot-check |
| 511 | Chapter 15 trace review compression | Trace review оставляет only investigation fields | Full trace record to companion |
| 512 | Chapter 15 timeline compression | Timeline показывает order, not full event catalog | Full timeline catalog to companion |
| 513 | Chapter 15 identity invariant compression | Identity invariant list remains reader-friendly | Full checks to companion |
| 514 | Chapter 15 approval review compression | Approval review keeps linking fields only | Full approval schema to companion |
| 515 | Chapter 15 span usage compression | Span/event explanation replaces long payload | Full telemetry examples to companion |
| 516 | Chapter 15 verification compression | Verification result is one compact evidence example | Full verification logs to companion |
| 517 | Chapter 15 regression compression | Regression candidate remains a short bridge to eval | Full dataset to companion |
| 518 | Chapter 15 post-pass render | Trace practicum pages read as investigation guide | Template spot-check |
| 519 | Chapter 14 SLO excerpt compression | User story and SLO map remain compact | Full SLO examples to companion |
| 520 | Chapter 14 SLO realism check | SLO text avoids impossible reliability promises | Add caveat if needed |
| 521 | Ownership map compression | Ownership map shows roles and decisions only | Full owner matrix to companion |
| 522 | Golden path compression | Golden path lists controls without becoming catalog dump | Full checklist to companion |
| 523 | Runtime skeleton contract compression | Runtime skeleton shows lifecycle nodes only | Full contract to companion |
| 524 | Python skeleton compression | Python listing shows minimal path only | Full code to companion |
| 525 | Release contract compression | Release contract keeps launch gates only | Full release YAML to companion |
| 526 | Rollout record compression | Rollout decision record remains one-page artifact | Full examples to companion |
| 527 | Caption style audit | All captions use `Style20` in Template derivative | Re-render proof |
| 528 | Code style audit | Code-like lines stay in `Style16`, not headings | Re-render proof |
| 529 | Heading guard audit | No code line promoted to Heading1/2/3 | PDF text + visual spot |
| 530 | List style audit | Lists remain true Word lists, not fake hyphens where avoidable | OOXML check |
| 531 | Page 286 regression | Python block stays code style after rerender | Visual check |
| 532 | Page 87 compression target | Dense field-name prose on page 87 is reduced | Re-render page |
| 533 | High-ink page audit | Top 12 high-ink Template pages classified | Compression queue |
| 534 | Low-ink page audit | Low-ink pages are meaningful tails | Page notes |
| 535 | Final page audit | Final page contains content, no blank tail | Render check |
| 536 | Raw export regression | Raw export stays at 0 blank-like pages | Render metrics |
| 537 | Template export regression | Template proof stays at 0 blank-like pages | Render metrics |
| 538 | Caption numbering audit | Listing numbers are unique and chapter-aligned | Search pass |
| 539 | Caption wording audit | Captions explain purpose, not file format | Style pass |
| 540 | Caption punctuation audit | Captions use consistent dash/punctuation | Typography pass |
| 541 | Companion manifest chapter 12 | Chapter 12 artifacts listed with route names | Update manifest |
| 542 | Companion manifest chapter 15 | Chapter 15 artifacts listed with route names | Update manifest |
| 543 | Companion manifest chapter 14 | SLO artifacts listed with route names | Update manifest |
| 544 | Companion manifest org/golden path | Ownership/golden path artifacts listed | Update manifest |
| 545 | Companion manifest runtime | Runtime/Python/release artifacts listed | Update manifest |
| 546 | Companion route link policy | Printed links use stable labels, not raw URLs | Link pass |
| 547 | Companion version tag | Route list has version tag placeholder | Author decision |
| 548 | Companion readiness flags | Each artifact has status: example/draft/recommended | Update manifest |
| 549 | Source freshness note | Fast-moving implementation examples flagged | Source note |
| 550 | Reproducibility boundary | Book does not promise runnable code in print | Add note |
| 551 | Chapter 12 narrative bridge | After compression, prose still explains why each excerpt exists | Add bridge |
| 552 | Chapter 15 narrative bridge | Trace practicum remains coherent after payload removal | Add bridge |
| 553 | Chapter 14 narrative bridge | SLO section keeps story-to-metric logic | Add bridge |
| 554 | Part VII narrative bridge | Runtime proof reads as architecture, not code dump | Add bridge |
| 555 | Cross-reference update | References from prose to listings remain valid | Search pass |
| 556 | TOC side-effect check | Caption style does not pollute TOC | Export check |
| 557 | PDF text extraction check | Captions survive PDF extraction | Marker pass |
| 558 | DOCX extraction check | Captions survive DOCX extraction | Parser pass |
| 559 | HTML export check | Captions survive HTML export if needed | Export check |
| 560 | Accessibility captions | Listing captions are meaningful without surrounding paragraph | A11y pass |
| 561 | Glossary alignment | side_effect_unknown, idempotency, trace terms align with glossary policy | Terminology pass |
| 562 | Russian-English balance | Captions avoid unnecessary English unless term is contract name | Style pass |
| 563 | Inline code typography | Inline identifiers in prose are readable in Template proof | Typography pass |
| 564 | Long identifier wrapping | Long identifiers do not create over-wide lines | Render check |
| 565 | Code indentation audit | Code snippets preserve readable indentation | Visual check |
| 566 | YAML indentation audit | YAML excerpts preserve readable indentation | Visual check |
| 567 | Dense prose alternative | Replace field sequences with short tables where better | Form-factor pass |
| 568 | Table introduction decision | Decide if any listing should become a table | Editor note |
| 569 | Figure alternative decision | Decide if any listing should become a diagram | Diagram backlog |
| 570 | Workshop usability check | Compressed listings still support team review | Add prompts |
| 571 | Security usability check | Security reader sees controls and evidence | Add notes |
| 572 | Platform usability check | Platform reader sees reusable runtime boundaries | Add notes |
| 573 | Product usability check | Product reader sees rollout and owner tradeoffs | Add notes |
| 574 | Incident usability check | Incident reader sees trace/evidence workflow | Add notes |
| 575 | Executive readability check | Dense technical payload does not block decision narrative | Add summaries |
| 576 | Author bio short | Short bio remains placeholder until author fills it | Author task |
| 577 | Author bio extended | Extended bio remains placeholder until author fills it | Author task |
| 578 | Author role and facts | Role, experience, projects, links remain explicit must-fill fields | Author task |
| 579 | Acknowledgments decision | Section added or explicitly omitted | Author task |
| 580 | Dedication decision | Section added or explicitly omitted | Author task |
| 581 | Errata channel decision | Public errata channel is chosen | Author task |
| 582 | Companion canonical URL | Canonical URL and version tag chosen | Author task |
| 583 | Publisher title style decision | Boxed title treatment accepted or changed | Publisher task |
| 584 | Publisher code style decision | `Style16` code appearance accepted | Publisher task |
| 585 | Publisher caption style decision | `Style20` listing caption appearance accepted | Publisher task |
| 586 | Publisher page budget check | 345-page Template proof acceptable for review stage | Publisher task |
| 587 | Full proof read round 1 | Human proofread on compressed proof completed | Editorial task |
| 588 | Full proof read round 2 | Corrections integrated and rerendered | Editorial task |
| 589 | Source legal caveat | Compliance/legal caveat reviewed | Editorial task |
| 590 | Trademark/product names | Product names reviewed for publisher policy | Editorial task |
| 591 | Sensitive data scan | No secrets/customer data/internal endpoints in examples | Verification |
| 592 | Metadata scrub | DOCX metadata has no unwanted private fields | Verification |
| 593 | JSON QA gate | Render QA JSON validates | Verification |
| 594 | DOCX zip gate | Raw and Template DOCX pass zip integrity | Verification |
| 595 | Diff whitespace gate | New reports pass `git diff --check` | Verification |
| 596 | Test suite gate | `uv run --group dev pytest` passes | Verification |
| 597 | Docs build gate | `uv run --group docs mkdocs build --strict` passes | Verification |
| 598 | Commit gate | Commit contains only intended pass files | Git check |
| 599 | Push gate | Remote branch includes commit | Git push |
| 600 | Final author report | Author receives pages, risks, must-fill list and next action | Handoff |

## Итог по итерациям 501-600

Главная цель следующего блока - не добавлять больше объёма, а сделать существующий объём редакционно пригодным. После listing-caption pass книга уже не содержит generic `Листинг (YAML):` labels, но многие фрагменты всё ещё слишком похожи на reference dump. Итерации 501-600 превращают эти фрагменты в короткие печатные excerpts и связывают полные версии с companion, чтобы редактор видел книгу, а не распечатанный справочник runtime-пакета.
