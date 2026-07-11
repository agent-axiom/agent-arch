# RU Google Doc visual appendix and terminology pass - 2026-07-11

Target Google Doc: https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4/edit

Final checked Google Doc revision:
`ALtnJHzIhy-HXnhdlLen5wAh-PoTs24myIhmoQzMCrh2Vd5Ou_llCit4F4bHETIWKGRouEpUwQRpyJTJlnIinrILK34WGwNuCfdR7IDMY3o`

Final exported PDF for QA:
`/tmp/agent-arch-google-doc-visual-app-pass-final-2026-07-11.pdf`

## Implemented in the Google Doc

- Tightened the front matter:
  - clarified the editorial status line;
  - expanded the author placeholder with the exact fields the author still needs to fill;
  - changed the manuscript description from eight parts to seven parts plus appendices.
- Fixed the visible part-count inconsistency in the introduction:
  - `Части VI-VIII` -> `Части VI-VII`.
- Removed MkDocs residue from the opening route line and repaired two heading/body joins in the reader path.
- Replaced high-visibility unnecessary English terms in the introductory architecture frame, including `prompt tricks`, `production architecture`, `offline evals`, `simulation`, `gate`, `payload`, `trace events`, `approval record`, `workflow`, `reference package`, `config surface`, and `handoff`, while preserving code identifiers and canonical API names.
- Added a new visual appendix with five localized figures inserted directly into the existing Google Doc:
  - `Рисунок В.1. Фреймворк / испытательный контур / среда выполнения.`
  - `Рисунок В.2. Локальный интерфейс не является границей доверия.`
  - `Рисунок В.3. Симуляция развертывания и целостность оценки.`
  - `Рисунок В.4. MCP-шлюз и постепенное раскрытие.`
  - `Рисунок В.5. Агентная оболочка и долговечный стержень процесса.`
- Added page breaks before the visual appendix figures so captions and images do not split across pages.

## QA evidence

- Google Docs export produced a 467-page PDF.
- Text extraction found seven practical exercises, parts I-VII only.
- Text extraction found the visual appendix heading and all five figure captions.
- Text extraction found no `[[FIG_RU_*]]` markers.
- Text extraction found no raw `github.com/agent-axiom/agent-arch` URLs.
- Text extraction found no old `Части VI-VIII` / `восьми частях` wording.
- Targeted grep found no remaining high-visibility terms from the replacement list: `prompt tricks`, `production architecture`, `offline evals`, `tool-heavy`, `stop conditions`, `handoff package`, `reference package`, `config surface`.
- Final pages 461-467 were rasterized from the exported PDF and visually inspected. The five new figures render and are no longer separated from their captions.

## Remaining author/editor tasks

- Fill the `Об авторе` placeholders with final author identity, role, public links, publisher contact, and short cover/card biography.
- Decide whether the visual appendix should stay as an appendix or whether the five localized figures should replace earlier in-flow figure objects during the final DOCX/layout pass.
- Apply the official publisher template and rerun a full DOCX/PDF layout pass.
- Run a final human copy edit for rhythm, repeated examples, glossary consistency, and code/list formatting in the reference-package appendix.
