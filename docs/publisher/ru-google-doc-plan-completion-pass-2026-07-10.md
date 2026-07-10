# Russian Google Doc plan completion pass - 2026-07-10

Target manuscript: https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4/edit?tab=t.0

Final checked Google Docs revision:
`ALtnJHyzuTBl25nnpAKuB-tw0EpgFufcHnUpinKtaGmga9m8V33IP30Xmn4ei8kYEhkZE_dEt7hECyKSwBwWjDCRPxk89urjN0fHamVaf7o`

## Scope

This pass implements the follow-up plan from the previous frontier enrichment report:

1. Run a terminology pass over the newly added 2026 blocks.
2. Normalize new figure captions and numbering where the publisher-style pass exposed drift.
3. Add practical "what to try in the repository" callouts.
4. Clean the most important source/package reference issue found during the pass.
5. Expand the author-owned front-matter placeholders without inventing author facts.

## Google Doc changes

Terminology and caption updates:

- `Safe Agent Architecture Brief` -> `бриф безопасной архитектуры агента`
- `hands` in the policy heading -> `исполнительный контур`
- `tool descriptions, prompt-to-tool-to-execution` -> `описания инструментов, путь от промпта к инструменту`
- `MCP gateway, private reachability` -> `MCP-шлюз, приватная достижимость`
- `reasoning privacy и searchable spans` -> `приватность рассуждений и поисковые фрагменты трассы`
- `deployment simulation` in headings/captions -> `симуляция развертывания`
- `framework, harness и runtime` -> `фреймворк, испытательный контур и среда выполнения`
- `launch gate` / `happy path` -> `выпускной шлюз` / `успешный путь`

Figure caption normalization:

- `Рисунок 3.2. Локальный интерфейс и плоскость управления как поверхность атаки`
- `Рисунок 9.2. MCP-шлюз и постепенное раскрытие`
- `Рисунок 13.2. Симуляция развертывания и аудит целостности оценки`
- `Рисунок 13.3. Поток записи оценки и аудита (eval_audit_record)`
- `Рисунок 16.2. Фреймворк / испытательный контур / среда выполнения как три разных слоя`
- `Рисунок 16.3. Долговечный стержень процесса и восстанавливаемая внутренняя нить`

Practical callouts added near the relevant discussion:

- reference package / companion entry point for the architecture brief
- MCP capability and policy configuration review
- failed-run eval dataset drill
- runtime trace walkthrough with `simulate-run`, `dump-events`, `export-events`, and `inspect-trace`

Source-reference cleanup:

- Replaced 165 literal `agentruntimeref` occurrences with the actual package name `agent_runtime_ref`.

Author-owned front matter:

- Replaced the short author placeholder with a fill checklist: public name, role/positioning, experience line, public links, and publisher contact fields.
- Left factual author content as placeholders because those facts must be supplied by the author.

## Verification

Connector readback:

- New localized headings found in the target document.
- New practical command/path callouts found in the target document.
- `agentruntimeref` no longer found by connector exact-text search.

PDF export QA:

- Exported final Google Doc to PDF.
- PDF page count: 458 pages.
- Rasterized all 458 pages at low resolution.
- Built a full-document contact sheet for coarse visual review.
- Rendered and inspected detail pages for front matter, changed practical callouts, and all color figure pages.
- Color/figure pages after this pass: 24, 55, 66, 148, 209, 231, 347, 349, 350, and 397.
- No clipped figures, missing pages, or obvious broken page render found in the inspected export.

Text extraction checks from the final PDF:

- `Практическое дополнение 2026`: 10 occurrences.
- `Практика в репозитории`: 4 occurrences.
- No `[[RU_FIGURE_*]]` markers.
- No `agentruntimeref` occurrences.
- New figure numbers present: 3.2, 9.2, 13.2, 13.3, 16.2, 16.3.

## Remaining author tasks

- Fill the `Об авторе` block with factual public information.
- Decide whether publisher-facing terminology should keep selected English terms of art in figure images, especially `Framework / Harness / Runtime`, `Deployment simulation`, and `MCP gateway`.
- Approve or revise the new practical callouts before final editorial freeze.

## Recommended next improvement plan

1. Do a focused chapter-16 terminology pass so the text, captions, and figure internals use the same Russian/English policy.
2. Add one compact "reader exercise" box at the end of each major part, not just near the new frontier updates.
3. Normalize all raw GitHub config links into readable labels during the final link pass.
4. Run a full duplicate-practice scan: keep chapter-level exercises, move long command matrices to companion materials.
5. After publisher styles are applied, repeat PDF QA and check orphaned captions/headings page by page.
