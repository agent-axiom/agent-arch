# Редакционная дорожная карта русской рукописи

Status: execution roadmap after full source-to-print manuscript import.

Google Doc targets:

- Full manuscript: `Архитектура безопасных ИИ-агентов — полная рукопись`
- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Compressed/staging snapshot: `Архитектура безопасных ИИ-агентов`
- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

## Current verdict

На 2026-06-15 полный source-to-print manuscript собран из Markdown-источников:
введение, 7 частей, 23 главы и приложения. Локальный Markdown содержит около
109k слов после структурной чистки, DOCX render smoke QA дал 437 страниц,
native Google Doc import прошел и контрольные readback-точки подтверждены.

Текущий приоритет - не набор объема, а финальная редакционная доводка:
author-owned факты, внешняя редактура/вычитка, companion metadata, повторный
export QA после авторских полей и чистый publisher submission packet.

На 2026-06-28 current editorial-ready proof собран: raw Google Docs export
рендерится в 499 страниц, Template2000n derivative - в 315 страниц, пустых
страниц не обнаружено, H2/H3 body-style debt закрыт.

На 2026-06-29 Google Doc обновлен companion/source-status wording через
connector batchUpdate; later 2026-07-01 pre-author gate sync moved the current
revision to
`ALtnJHwQSbMVcXf5UUw3QyuuxPZVGdtR-7yOKUdJM8DtE76ktgR6WhHDA0zngCtIQFMNxPaYHMglaPHowPxYQS8TpcL8wryth-RYjYpT_iQ`.
Представительный P0 live-pass по первичным platform/security/protocol
источникам выполнен. Дополнительно полный live URL availability pass по source
catalog выполнен 2026-06-29: 106 URL проверены, 102 вернули HTTP 200, 4 требуют
ручной или браузерной проверки; смысловая сверка быстро меняющихся claims
остается отдельным финальным проходом.

На 2026-06-29 author-intake layer готов: поля автора отделены и готовы к
заполнению, но биография, byline, публичные ссылки, disclaimer и metadata
остаются author-owned и не заполнены Codex.

На 2026-06-30 выполнен targeted source follow-up: Anthropic Claude Code
Security переведен на canonical URL, MLCommons и Microsoft Research
подтверждены через title/body read, Air Canada case переведен на официальный
CRT primary source. OpenReview демотирован из primary evidence в непервичные
research leads для финального редакторского пакета.

На 2026-07-01 выполнена pre-author finalization iteration: Google Doc status
обновлен через connector batchUpdate до revision
`ALtnJHwQSbMVcXf5UUw3QyuuxPZVGdtR-7yOKUdJM8DtE76ktgR6WhHDA0zngCtIQFMNxPaYHMglaPHowPxYQS8TpcL8wryth-RYjYpT_iQ`,
placeholder/source readiness pass записан, а final DOCX export/Template2000n
final derivative/render QA намеренно отложены до заполнения author-owned
полей.

На 2026-07-02 выполнен practice-polish proof pass: поздние практикумы в Google
Doc вычитаны на уровне печатной формулировки, fresh raw Google Docs DOCX proof
сохранен как
`docs/publisher/artifacts/agent-arch-ru-practice-polished-working-proof-2026-07-02.docx`,
render QA подтвердил 513 страниц и 0 blank-like pages. Это актуальный working
proof для редакционного чтения, но не final publisher-ready submission.

Активный аудит:

- `docs/publisher/ru-book-readiness-audit.md`

## Workstream 1. Разделить рукопись и рабочие материалы

Задача: сделать очевидным, что служебные блоки в начале Google Doc не являются
текстом книги.

Что сделать:

- явно пометить служебные блоки как `не включать в финальную сдачу`;
- добавить заметный раздел `Начало основного текста книги` перед введением;
- решить, нужен ли отдельный Google Doc для publisher packet, cover note and
  editorial roadmap.

Definition of done:

- редактор видит, где начинается книга;
- служебные блоки не могут случайно попасть в финальный DOCX;
- repository -> Google Doc sync rule остается явным.

Progress:

- 2026-06-15: Google Doc contains `Начало основного текста книги`; working
  blocks are treated as service/front-matter material and excluded from final
  delivery unless explicitly promoted.

## Workstream 1a. Manuscript volume expansion

Задача: заменить compressed chapter assembly полноценными главами, собранными
из Markdown-источников по `docs/publisher/ru-source-map.md`.

Definition of done:

- каждая из 23 глав имеет развернутый текст, а не только chapter brief;
- суммарный объем Google Doc сопоставим с исходным русским corpus, а не с
  17k-word assembly;
- source-to-print mapping сохранен для каждой главы;
- после разворота повторяются terminology, cross-reference, companion-boundary
  and proofread passes.

Progress:

- 2026-06-15: gap identified by page count and word count: Google Doc has the
  structure, but not the full publisher manuscript volume.
- 2026-06-15: full source-to-print manuscript built as
  `docs/publisher/ru-manuscript-full.md`, rendered from DOCX to 437 pages in
  smoke QA and imported as the native Google Doc full manuscript.

## Workstream 2. Structural editorial pass

Задача: проверить книгу как цельную аргументационную дугу, а не набор
синхронизированных глав.

Что проверить:

- каждая часть отвечает на отдельный крупный вопрос;
- переходы между частями объясняют, почему следующий слой нужен именно сейчас;
- сквозной кейс поддержки не исчезает и не становится декоративным;
- повторяющиеся объяснения runtime, policy, memory, tools, evals and rollout
  не перегружают читателя;
- финальная часть действительно приводит к launch decision, а не обрывается на
  reference implementation.

Definition of done:

- у каждой части есть сильный вводный тезис и понятный выход;
- главы читаются последовательно, но сохраняют практическую автономность;
- нет крупных провалов между архитектурой, эксплуатацией и организационной
  моделью.

Progress:

- 2026-06-14: Introduction and Part I completed as the first structural batch.
- 2026-06-14: Parts II-III completed as the second structural batch.
- 2026-06-14: Parts IV-V completed as the third structural batch.
- 2026-06-14: Parts VI-VII and appendices completed; first full structural
  pass across the manuscript is complete.

## Workstream 3. Terminology pass

Задача: закрепить единый русский словарь для повторяющихся технических
понятий.

Ключевые группы:

- agent, tool, capability, gateway;
- runtime, run, trace, span, event;
- policy, approval, principal, tenant;
- rollout, gate, registry, inventory;
- assurance, incident, retirement, end-of-life;
- eval, verifier, rubric, evidence chain.

Definition of done:

- glossary matches manuscript vocabulary;
- first occurrence of a key English term has a Russian explanation;
- headings avoid English unless the term is essential for industry lookup;
- terms are consistent across introduction, chapters and appendices.

Progress:

- 2026-06-14: first terminology/glossary anchor batch completed for
  `capability`, `principal`, `tenant`, `lifecycle`, `inventory`,
  `assurance loop`, `runtime`, `registry` and `retirement` in Part VI,
  Part VII and appendices.
- 2026-06-15: second terminology anchor batch completed for reader-facing
  `runtime`, `workflow`, `policy layer`, `tool gateway`, `capability model`,
  `rollout`, `trace` and `evidence chain` anchors in Introduction and
  Parts I-V.
- 2026-06-15: third terminology consistency batch completed for reader-facing
  ADLC, assurance, registry, retirement, reference runtime, launch checklist
  and appendix checklist/postmortem language in Parts VI-VII and appendices.

## Workstream 4. Cross-reference and continuity pass

Задача: проверить внутренние связи после сжатия web-структуры 8/27 в печатную
структуру 7/23.

Что проверить:

- ссылки на предыдущие и будущие главы;
- promises made in introduction;
- references to companion material;
- consistency of chapter numbers and part numbers;
- whether Chapter 13 as follow-up technical sample is still described correctly
  after full manuscript assembly.

Progress:

- 2026-06-15: reader-facing `case-spine note` and `canonical cases` labels were
  checked across the assembled manuscript sources; no stale service labels remain.
- 2026-06-15: stale web-structure references were checked across assembled
  manuscript sources; no reader-facing references to Part VIII or chapters
  24-27 remain, and the 7/23 structure is stable.

Definition of done:

- no stale web-structure references remain in reader-facing prose;
- companion references are deliberate and useful;
- chapter and part numbering are stable.

## Workstream 5. Book/companion boundary pass

Задача: убедиться, что печатная книга не превращается в справочник API, но и не
теряет практическую глубину.

Что проверить:

- long schemas, YAML, CLI walkthroughs and registry operations stay in companion;
- print manuscript keeps enough examples to be operationally useful;
- appendices are short working aids, not a duplicate online reference package;
- source catalog is curated for book use rather than web completeness.

Definition of done:

- each heavy technical artifact has an explicit home: book summary or companion;
- reader can understand the design without opening companion immediately;
- companion remains useful as executable/reference layer.

Progress:

- 2026-06-15: companion boundary checked across assembled manuscript sources;
  YAML, CLI walkthroughs, reference outputs, registry operations and long
  schemas are consistently assigned to the online companion.
- 2026-06-15: current manuscript-source print-readability scan found no
  Mermaid blocks, Markdown tables or fenced code blocks in the assembled
  publisher manuscript sources.

## Workstream 6. Publisher front matter and final delivery prep

Задача: подготовить рукопись к внешнему редакторскому циклу.

Что сделать:

- fill author bio and credential framing fields;
- update cover note only after manuscript-only structure is stable;
- apply БХВ styles when received;
- run DOCX/export QA after style application;
- only then prepare external package.

Definition of done:

- author placeholders are gone;
- Google Doc or exported DOCX has publisher-ready structure;
- final checks include proofread, cross-reference review, glossary match,
  `git diff --check`, `uv run pytest`, and `uv run mkdocs build --strict`.

Progress:

- 2026-06-15: author fields remain intentionally open for the author; БХВ style
  files are explicitly deferred until received.
- 2026-06-15: current-source proofread, cross-reference, glossary, source
  catalog, figure/code and print-readability gates are complete for the
  assembled manuscript. DOCX/export QA remains blocked until styles are applied.
- 2026-06-28: author/front-matter fields are isolated in the Google Doc and
  local author-open-fields report.
- 2026-06-28: current raw editorial-ready proof renders to 499 pages with 0
  blank-like pages.
- 2026-06-28: current Template2000n editorial-ready proof renders to 315 pages
  with 0 blank-like pages and preserves raw proof paragraph text sequence.
- 2026-06-28: clean editor handoff packet is ready for external editorial
  review, but final submission is still blocked by author-owned facts and
  external proofread.
- 2026-06-28: author query packet, editor-facing brief, companion readiness
  pass, final fact-check backlog and post-author export workflow are prepared.
  Final export remains blocked until the author supplies factual metadata.
- 2026-06-28: companion templates/checklist promoted to release-candidate
  headers; executable trace/session/eval companion artifacts generated; source
  verification packet prepared for the final live fact-check pass.
- 2026-06-28: filled companion examples, runtime-reference artifact links,
  source verification records, editor comment intake workflow and final
  placeholder/link scan workflow are prepared.

## Workstream 7. Book-readiness second pass

Задача: превратить полную source-to-print assembly в рукопись, которая читается
как книга, а не как крупная синхронизированная документационная подборка.

Что проверить:

- введение быстро формулирует обещание книги и маршрут читателя;
- каждая глава отвечает на один центральный вопрос;
- повторяющиеся концовки глав компактны и не выглядят механически;
- перегруженные главы 5, 20, 21 and 22 разведены по ролям;
- глава 20 больше не несет сразу весь assurance/registry/incident/retirement
  reference layer;
- глава 21 объясняет эталонную реализацию как narrative reference
  implementation, а не как CLI manual;
- приложения не дублируют поздние главы и online companion.

Definition of done:

- book-readiness audit закрыт по batch 1-6;
- introduction and Part I read as a strong sample opening;
- chapters 5, 20, 21 and 22 no longer contain unresolved large-scale
  duplication;
- final launch chapter remains the synthesis point of the book;
- Google Doc and Markdown source are synchronized after each batch.

Progress:

- 2026-06-17: created active book-readiness audit in
  `docs/publisher/ru-book-readiness-audit.md`; current verdict changed from
  "almost ready except final dependencies" to "full volume assembled, second
  editorial pass required before publisher-ready claim".
- 2026-06-17: Introduction reader-contract rewrite synced to the full Google
  Doc manuscript from `docs/publisher/ru-book-ready-introduction.md`.
- 2026-06-18: Chapter 1 sample-chapter line edit synced to the full Google Doc
  manuscript from `docs/publisher/ru-book-ready-chapter-1.md`.
- 2026-06-18: Chapter 2 decision-ladder rebuild synced to the full Google Doc
  manuscript from `docs/publisher/ru-book-ready-chapter-2.md`.
- 2026-06-18: Chapter 3 compact bridge into Part II synced to the full Google
  Doc manuscript from `docs/publisher/ru-book-ready-chapter-3-bridge.md`;
  book-readiness batch 1 is complete.
- 2026-06-18: Chapter 5 conceptual identity/session/policy/capability rewrite
  synced to the full Google Doc manuscript from
  `docs/publisher/ru-book-ready-chapter-5.md`; batch 2 is now in progress.
- 2026-06-18: Chapter 22 implementation-focused rewrite synced to the full
  Google Doc manuscript from `docs/publisher/ru-book-ready-chapter-22.md`;
  chapter 5/22 overlap is resolved.
- 2026-06-28: editor handoff readiness pass completed in the full Google Doc:
  two H1-polluted body ranges were normalized, fresh raw DOCX proof was
  exported as
  `docs/publisher/artifacts/agent-arch-ru-editor-handoff-pass-2026-06-28.docx`,
  rendered to 552 pages with 0 blank-like pages, and remaining H2 style debt
  was registered as the next publisher-formatting risk.
- 2026-06-28: global heading normalization completed in the full Google Doc:
  629 long body-like `Heading 2` paragraphs were demoted with style-only
  guarded batch updates, final raw DOCX proof rendered to 504 pages with 0
  blank-like pages, and Template2000n derivative rendered to 315 pages with 0
  blank-like pages. Remaining formatting risk moved to long `Heading 3`
  review.
- 2026-06-28: H3/body-style normalization completed in the full Google Doc:
  65 long body-like `Heading 3` paragraphs were demoted with style-only guarded
  batch updates, final raw DOCX proof rendered to 499 pages with 0 blank-like
  pages, and Template2000n derivative rendered to 315 pages with 0 blank-like
  pages. Long H2/H3 body-style debt is now closed for the current proof.
- 2026-06-29: final QA packet hardening pass added a mechanical
  placeholder/link scan report, print-to-companion links for the support-ticket
  trace/eval/examples, a live source verification action packet, a final
  external packet outline and the next 100 external-packet readiness goals
  (`2501-2600`).
- 2026-07-01: latest-practices sync pass aligned the publisher manuscript with
  the new practical sections in `docs/book/**`: 13 practice headings are now
  present exactly once in `docs/publisher/ru-manuscript-full.md`, eight missing
  print-oriented practice blocks were added to the full Google Doc, and the
  fresh Google Doc readback reports 101,584 approximate words. The pass is
  recorded in
  `docs/publisher/ru-latest-practices-sync-pass-2026-07-01.md`; next goals are
  `2701-2800`.
- 2026-07-02: practice-polish proof pass updated the late practice wording in
  the full Google Doc, exported
  `docs/publisher/artifacts/agent-arch-ru-practice-polished-working-proof-2026-07-02.docx`,
  rendered it to 513 pages with 0 blank-like pages, and recorded next goals
  `3101-3200` in
  `docs/publisher/ru-editorial-100-practice-polish-proof-iterations-2026-07-02.md`.
- 2026-07-03: layout/style proof pass fixed the known page-338 carryover,
  checked late-practice page breaks, cleaned practice heading/body styles,
  exported
  `docs/publisher/artifacts/agent-arch-ru-layout-style-pass-2026-07-02.docx`,
  rebuilt
  `docs/publisher/artifacts/agent-arch-ru-template2000n-layout-style-pass-2026-07-02.docx`,
  rendered raw to 507 pages and Template2000n to 371 pages with 0 blank-like
  pages, and recorded next goals `3201-3300` in
  `docs/publisher/ru-editorial-100-layout-style-proof-iterations-2026-07-03.md`.

## Workstream 8. Editor handoff readiness

Задача: подготовить рукопись к осмысленной передаче редактору без ложного
заявления, что финальный publisher-ready DOCX уже закрыт.

Что уже сделано:

- Google Doc остается основной рабочей рукописью;
- H1 outline очищен от очевидного body-as-heading загрязнения;
- свежий raw DOCX proof получен из текущего Google Doc;
- render QA подтвердил 552 страницы и 0 blank-like pages;
- подготовлен editor handoff packet;
- подготовлен список author-owned полей;
- подготовлен companion skeleton для материалов, которые не должны раздувать
  печатную книгу.
- подготовлен mechanical scan report для placeholder/link/TODO проверки;
- подготовлен live source verification action packet;
- подготовлен final external packet outline;
- добавлен новый блок 100 целей для author/source/export/editor-packet
  readiness.
- добавлен latest-practices sync report и новый блок 100 целей для
  practice-sync/editorial-readiness follow-up.

Закрыто в следующем pass:

- H2 style debt: 629 длинных body-like `Heading 2` абзацев демотированы до
  normal text в Google Doc.
- Fresh raw proof после normalization: 504 pages, 0 blank-like pages.
- Fresh Template2000n proof после normalization: 315 pages, 0 blank-like pages.
- H3 style debt: 65 длинных body-like `Heading 3` абзацев демотированы до
  normal text в Google Doc.
- Fresh raw proof после H3 cleanup: 499 pages, 0 blank-like pages.
- Fresh Template2000n proof после H3 cleanup: 315 pages, 0 blank-like pages.
- Latest-practices content sync: 13 source practice sections added to
  `ru-manuscript-full.md`; eight late Google Doc practice blocks added and
  verified by text readback.
- Practice-polish proof pass: late practice headings and result wording
  polished in the full Google Doc; fresh raw DOCX working proof rendered to
  513 pages with 0 blank-like pages; page 338 orphan/layout issue recorded for
  the next publisher-style pass.
- Layout/style proof pass: page-338 orphan fixed, SLO practice orphan risk
  removed, all 14 practice headings are navigable, raw proof rendered to 507
  pages with 0 blank-like pages, and Template2000n derivative rendered to 371
  pages with 0 blank-like pages.

Открытый риск:

- Late-practice layout/style debt is closed for the current proof. A separate
  older-outline audit still remains for legacy long H2/H3 body-like paragraphs.
  Открыты авторские поля, финальная вычитка, publisher-approved style
  application and final raw/Template2000n DOCX/export QA after author/style
  closure.

Definition of done:

- editor can review the manuscript by link and see the current proof status;
- author-owned gaps are explicit;
- companion routes exist for templates, checklists, changelog and errata;
- next 100 editorial goals are recorded;
- repository has the current DOCX proof, QA metadata and handoff notes.

## Recommended execution order

1. Keep the full Google Doc as the canonical working manuscript.
2. Run book-readiness batch 1: introduction and Part I.
3. Run book-readiness batch 2: safety/control and chapter 5/22 overlap.
4. Run book-readiness batch 3: memory, execution, sandbox and MCP.
5. Run book-readiness batch 4: traces, SLO, evals and rollout evidence chain.
6. Run book-readiness batch 5: organization, ADLC, assurance and chapter 20.
7. Run book-readiness batch 6: runtime, launch checklist and appendices.
8. Fill author/front matter dependencies.
9. Apply publisher styles and perform DOCX/export QA.
10. Run final external proofread and package the publisher handoff artifacts.
