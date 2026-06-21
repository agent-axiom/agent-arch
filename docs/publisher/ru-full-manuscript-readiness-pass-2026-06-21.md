# Full Russian manuscript readiness pass: 2026-06-21

Status: applied a five-point readiness pass to the live Russian Google Doc
manuscript and recorded the editorial outcomes for repository tracking.

Working Google Doc:

- `Архитектура безопасных ИИ-агентов — полная рукопись`
- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- tab: `t.0`

Repository branch:

- `codex/ru-reference-package-inspect-terms-20260608`

## 1. Structural pass

The manuscript was exported as plain text for whole-book analysis. Baseline
export metrics before this pass:

- lines: `8,743`;
- words: `107,453`;
- characters: `845,784`;
- major structure: `7` parts, `23` chapters, appendices and a late reference
  package block.

Main structural finding:

- the manuscript has real book-scale volume, but the editorial risk has shifted
  from missing volume to uneven density;
- early chapters read mostly as a book;
- chapters 11-16 are technically dense and need stronger print/companion
  boundaries;
- chapters 17-20 are comparatively compressed for their organizational role;
- chapter 23 and the late reference-package material are useful, but too close
  to implementation changelog form for a print manuscript.

## 2. Chapter-by-chapter readiness

The live Google Doc now contains a working appendix:

- `Редакционный паспорт готовности рукописи (рабочий раздел, не для печати)`

This block records a chapter-by-chapter readiness model based on five criteria:

1. chapter purpose;
2. reader's entry question;
3. key architectural decision;
4. verifiable artifact;
5. boundary with the online companion.

Chapter groups recorded in the Google Doc:

- chapters 1-3: keep as the foundation and check duplication across the
  introduction, book map and chapter 1;
- chapters 4-6: keep technical density but explain risk and owner before each
  contract;
- chapters 7-9: strengthen the memory/retrieval running example and reduce
  repeated provenance explanations;
- chapters 10-12: separate runtime architecture, sandbox/MCP and reliability;
- chapters 13-16: keep the evidence chain as the central line;
- chapters 17-20: expand the organizational model and lifecycle material;
- chapters 21-23 and appendices: preserve a print walkthrough, but move long
  config dumps, CLI output and validation catalogs to companion.

## 3. Listings, YAML, tables and captions

Technical-density scan by chapter:

| Chapter | Lines | Words | Technical markers | Companion markers | Risk |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | 144 | 3,452 | 0 | 0 | low |
| 2 | 140 | 2,929 | 0 | 0 | low |
| 3 | 316 | 4,461 | 0 | 0 | low |
| 4 | 255 | 4,088 | 0 | 0 | low |
| 5 | 140 | 3,687 | 1 | 1 | low |
| 6 | 319 | 2,789 | 6 | 0 | low |
| 7 | 300 | 3,433 | 0 | 0 | low |
| 8 | 365 | 3,394 | 5 | 0 | medium |
| 9 | 477 | 4,001 | 0 | 0 | medium |
| 10 | 284 | 2,361 | 0 | 0 | low |
| 11 | 1,008 | 9,421 | 33 | 1 | high |
| 12 | 552 | 3,934 | 31 | 0 | high |
| 13 | 683 | 5,862 | 47 | 0 | high |
| 14 | 307 | 2,808 | 6 | 0 | low |
| 15 | 717 | 6,470 | 20 | 2 | high |
| 16 | 334 | 3,499 | 12 | 0 | medium |
| 17 | 83 | 1,940 | 0 | 0 | low |
| 18 | 71 | 2,100 | 0 | 2 | low |
| 19 | 90 | 2,625 | 1 | 3 | low |
| 20 | 102 | 3,954 | 0 | 3 | low |
| 21 | 179 | 2,329 | 6 | 3 | low |
| 22 | 174 | 2,209 | 15 | 2 | medium |
| 23 | 1,315 | 18,854 | 113 | 24 | high |

Print rule recorded in the Google Doc:

- keep only short listings that show the shape of a capability, policy, trace,
  eval gate or lifecycle artifact;
- every technical block needs an introduction explaining why it is there and a
  follow-up explaining what the team should verify;
- long field lists, validation-message catalogs, CLI output and complete YAML
  configs belong in the versioned online companion.

## 4. Terminology pass

The Google Doc now records canonical explanations for the next terminology
normalization pass:

- `agent / агент`;
- `capability / возможность`;
- `tool gateway / инструментальный шлюз`;
- `policy gateway / шлюз политик`;
- `verifier / проверяющий`;
- `trace / трасса`;
- `memory / память`;
- `retrieval / извлечение контекста`;
- `sandbox / песочница`;
- `MCP`;
- `ADLC`;
- `rollout`;
- `retirement`.

Term-frequency scan from the plain-text export:

| Term group | Count |
| --- | ---: |
| agent / агент | 1,217 |
| capability / возможность | 632 |
| tool gateway / инструментальный шлюз | 44 |
| policy gateway / шлюз политик | 23 |
| verifier / проверяющий | 171 |
| trace / трасса | 638 |
| memory / память | 571 |
| retrieval / извлечение контекста | 115 |
| sandbox / песочница | 110 |
| MCP | 159 |
| ADLC | 35 |
| rollout / поэтапный выпуск | 229 |
| retirement / вывод из эксплуатации | 79 |
| review / ревью | 154 |
| companion / online companion | 49 |

## 5. DOCX/template readiness

Applied directly to the Google Doc:

- normalized the front matter body text from inherited heading styling to
  normal text for the confirmed range from `Аннотация` through the early
  team-reading material;
- restored explicit heading levels for confirmed front matter headings;
- added the working editorial-readiness appendix at the end of the document and
  styled its heading hierarchy.

Important DOCX/template gate:

- do not apply `Template2000n.dot` styles until the manuscript text is stable;
- do not run template macros automatically;
- use `docs/publisher/ru-template2000n-style-bridge.md` as the style mapping
  guide after a clean Google Docs export;
- remove or move the working editorial appendix before final publisher-facing
  DOCX unless the editor explicitly wants it in the manuscript file.

## Verification

Completed after final PDF export of the updated Google Doc:

- exported the updated Google Doc to PDF:
  `/private/tmp/agent_arch_full_readiness_20260621.pdf`;
- confirmed PDF metadata with `pdfinfo`:
  - page count: `692`;
  - page size: `612 x 792 pts`;
  - producer: `Skia/PDF m151 Google Docs Renderer`;
- visually inspected rendered spot pages:
  - page `1`: title, annotation and the start of `Что получит читатель`;
  - page `2`: reader outcomes, keywords and `Об авторе`;
  - page `3`: author placeholder and start of the foreword;
  - page `4`: foreword continuation and heading transitions;
  - page `690`: working editorial appendix around the listings/YAML policy;
  - page `692`: final working appendix queue.

Observed result:

- front matter now renders as ordinary manuscript text instead of oversized
  inherited heading text;
- the Google Docs PDF page count changed from the previous `707`-page export to
  `692` pages after front matter style normalization;
- the newly added working appendix is readable in the exported PDF.

Limitations:

- this was targeted PDF spot-check QA, not a full rendered inspection of all
  `692` pages;
- the working editorial appendix is intentionally marked as non-print material
  and must be removed or moved to the publisher packet before final DOCX
  delivery.
