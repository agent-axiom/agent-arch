# Google Doc stabilization pass: 2026-06-21

Status: completed stabilization pass for the full Russian Google Doc manuscript.

Working Google Doc:

- `Архитектура безопасных ИИ-агентов — полная рукопись`
- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Repository branch used for this pass:

- `codex/ru-reference-package-inspect-terms-20260608`

## 1. What this pass was for

The manuscript had already reached book-scale volume. The next practical risk was
not page count, but structural drift:

- the live Google Doc is an editorial print assembly, not a one-to-one export of
  `docs/book/**`;
- the public source corpus still has 8 parts and 27 local chapters;
- the print assembly follows the publisher-facing structure of 7 parts, 23
  chapters, front matter and appendices;
- Google Docs text insertion can accidentally inherit list state and turn prose
  or YAML blocks into huge bullet lists.

This pass therefore focused on stabilization, not new volume:

1. build a current page/chapter map from the exported Google Doc PDF;
2. make the structure explicit enough for the next editing pass;
3. remove accidental bullets from the late manuscript section;
4. connect the current Google Doc workflow with the Word template bridge;
5. record verification evidence.

## 2. Current exported PDF map

Latest checked PDF export after this pass:

- pages: 705;
- exporter: Google Docs PDF renderer;
- checked with bundled `pdfinfo`, `pdftoppm` and `pypdf`;
- visual spot check rendered pages 596 and 600 after bullet cleanup.

### Front matter

| Block | Exported page |
| --- | ---: |
| Аннотация | 2 |
| Что получит читатель | 3 |
| Ключевые слова | 4 |
| Об авторе | 5 |
| Предисловие к русской версии | 8 |
| Как читать эту книгу | 20 |

Pages 35-45 contain a compressed navigation/overview block where part and chapter
labels are repeated before the main body starts. This should be reviewed during
the next front-matter cleanup pass.

### Main body

| Print block | Exported page range | Notes |
| --- | ---: | --- |
| Часть I. От demo-агента к платформе | 48-134 | Actual body start is page 48; earlier labels are navigation/overview. |
| Глава 1. Почему агенту нужна платформа, а не магия | 48-76 | Source role: opening thesis/sample chapter. |
| Глава 2. Когда нужен агент: рабочий процесс, одиночный агент, многоагентная схема | 77-103 | Print chapter assembled from local Part I material. |
| Глава 3. Референсная архитектура безопасной агентной системы | 104-134 | Print chapter assembled from local architecture/security sources. |
| Часть II. Безопасность и контур управления | 135-196 | Security/control arc. |
| Глава 4. Контур безопасности и границы доверия | 135-153 | Trust boundary chapter. |
| Глава 5. Идентичность, сессия, слой политик и модель возможностей | 154-184 | Identity/session/policy/capability bridge. |
| Глава 6. Инструментальный шлюз, подтверждения и журнал аудита | 185-196 | Tool gateway and approval path. |
| Часть III. Память, знания и контекст | 197-247 | Memory/retrieval/context arc. |
| Глава 7. Зачем агенту память и почему она опасна | 197-217 | Memory risk framing. |
| Глава 8. Краткосрочная, долгосрочная и профильная память | 218-230 | Memory taxonomy and governance. |
| Глава 9. Извлечение контекста, уплотнение и фоновые обновления | 231-247 | Retrieval/context practice block already present. |
| Часть IV. Инструменты, выполнение и интеграция | 248-339 | Execution/tooling/integration arc. |
| Глава 10. Модель выполнения и каталог инструментов | 248-257 | Needs future style cleanup for contracts/lists. |
| Глава 11. Песочница выполнения и MCP как интеграционный контракт | 258-308 | Long technical chapter; candidate for companion-boundary review. |
| Глава 12. Идемпотентность, повторы, лимиты и границы отката | 309-339 | Side-effect safety and rollback boundary. |
| Часть V. Надежность, наблюдаемость и оценки | 340-433 | Evidence/observability/eval arc. |
| Глава 13. Трассы, спаны и структурированные события | 340-375 | Trace model. |
| Глава 14. SLO для агентных систем | 376-389 | Service-level objectives. |
| Глава 15. Офлайн- и онлайн-оценки и регрессионные шлюзы | 390-419 | Eval gate model. |
| Глава 16. Сквозная цепочка доказательств: от запроса к rollout | 420-433 | Evidence spine. |
| Часть VI. Организационная модель и жизненный цикл | 434-534 | Platform/lifecycle arc. |
| Глава 17. Платформенная команда и продуктовые команды | 434-451 | Team topology and ownership. |
| Глава 18. Поддерживаемые стандартные пути, общие шлюзы и антизоопарк-подход | 452-468 | Golden paths and shared gates. |
| Глава 19. От SDLC к ADLC: жизненный цикл агентной системы | 469-489 | Lifecycle model. |
| Глава 20. Контур заверения, реагирование на инциденты, реестр и вывод из эксплуатации | 490-534 | Compressed lifecycle closure. |
| Часть VII. Эталонная реализация и промышленный запуск | 535-641 | Late manuscript structure stabilized in this pass. |
| Глава 21. Базовая схема среды исполнения | 535-558 | Runtime skeleton marker found on page 549. |
| Глава 22. Слой политик и каталог возможностей | 559-580 | Capability release contract marker found on page 573. |
| Глава 23. Чеклист промышленного запуска | 581-641 | Rollout decision record marker found on pages 598 and 610. |

### Appendices

| Appendix | Exported page range | Notes |
| --- | ---: | --- |
| Приложение 1. Шаблон capability contract | 642-651 | Template appendix. |
| Приложение 2. Шаблон production readiness и rollout | 652-662 | Readiness appendix. |
| Приложение 3. Шаблон incident/postmortem | 663-672 | Incident appendix. |
| Приложение 4. Источники и online companion | 673-705 | Sources and companion boundary. |

## 3. Source relationship

The live Google Doc should be treated as a print assembly layer.

Primary current assembly artifact:

- `docs/publisher/ru-manuscript-full.md`

Source-to-print map:

- `docs/publisher/ru-source-map.md`

Publisher-facing map:

- `docs/publisher/ru-manuscript-map.md`

Important rule for future edits:

- use `docs/book/**` and `docs/appendix/**` as source material;
- use `docs/publisher/ru-source-map.md` to understand print chapter assembly;
- keep print-specific stabilization notes in `docs/publisher/**`;
- do not assume local chapter number equals print chapter number.

## 4. Google Doc changes made in this pass

The following direct Google Docs edits were applied:

1. Re-applied heading styles to late-manuscript structural anchors:
   - `Часть VII. Эталонная реализация и промышленный запуск`;
   - `Глава 21. Базовая схема среды исполнения`;
   - `Глава 22. Слой политик и каталог возможностей`;
   - `Глава 23. Чеклист промышленного запуска`;
   - `Глоссарий`;
   - `Приложение 1. Шаблон capability contract`;
   - `Приложение 4. Источники и online companion`.
2. Removed accidental paragraph bullets from the late inserted practical blocks
   and the visible Chapter 23 range.
3. Re-exported PDF and visually spot-checked pages 596 and 600 after cleanup.

The bullet cleanup changed the exported page count from 706 to 705 because
Google Docs no longer renders the affected prose/code pages as large bullet
lists with extra vertical spacing.

## 5. Editorial cleanup gate

The next editing passes should not add more bulk before these structural issues
are handled:

1. Front matter has merged heading/body transitions in exported text, for
   example `Что получит читатель1.` and similar adjacency. This is probably a
   paragraph-break/style issue in the Google Doc export.
2. Pages 35-45 contain a navigation/overview cluster before the actual main body
   starts on page 48. Decide whether this is a real table of contents, a reading
   guide, or leftover assembly scaffolding.
3. YAML/Python blocks are structurally present but not yet styled as final code
   blocks. This belongs to the DOCX/style pass, not to content expansion.
4. Chapter 11 and the late reference-package material are long enough to require
   companion-boundary review before publisher submission.
5. Appendices should be reviewed for print/online split: the printed manuscript
   should keep the explanation and minimal templates; long schema/manual detail
   should stay in the online companion.

## 6. Template2000n.dot handling

The attached publisher template file was inspected as:

- old binary Microsoft Word template (`Composite Document File V2`);
- Word 9.0 / Word 2000 era;
- code page 1251;
- contains VBA/macros.

Operational decision:

- do not apply or run this `.dot` template directly against the live Google Doc;
- use it as a style bridge for the future DOCX/export pass;
- preserve logical structure in Google Doc now: real headings, lists, code blocks,
  tables, appendix headings and source blocks.

Existing style bridge:

- `docs/publisher/ru-template2000n-style-bridge.md`

## 7. Verification evidence

Fresh checks from this pass:

- Google Doc connector identity:
  - document id: `1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
  - title: `Архитектура безопасных ИИ-агентов — полная рукопись`;
  - tab: `t.0`.
- Latest exported PDF:
  - `/private/tmp/agent_arch_manuscript_stabilized_nobullets_20260621.pdf`;
  - `pdfinfo` page count: 705.
- Marker checks:
  - `runtime_skeleton_contract`: page 549;
  - `capability_release_contract`: page 573;
  - `rollout_decision_record`: pages 598 and 610.
- Visual spot checks:
  - page 596: prose no longer renders as a bullet list;
  - page 600: YAML/list-like content no longer has Google Docs bullet markers.

Limitations:

- full rendered visual QA of every page was not performed;
- only targeted pages around the detected structural defect were rasterized and
  inspected;
- final DOCX/template application remains a separate publisher-production step.

## 8. Recommended next pass

Next pass should be a front-matter and navigation cleanup pass:

1. Fix merged heading/body transitions in front matter.
2. Decide whether pages 35-45 are a real TOC/reading guide or leftover assembly
   scaffolding.
3. Ensure chapter headings are visible in the generated TOC/export.
4. Normalize code/YAML blocks for the future `VBACodeText` / `VBACodeHead` style
   mapping.
5. Re-export PDF and inspect front matter plus the chapter 21-23 boundary again.
