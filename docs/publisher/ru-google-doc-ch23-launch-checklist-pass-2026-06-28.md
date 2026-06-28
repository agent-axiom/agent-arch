# Google Doc chapter 23 launch checklist pass

Date: 2026-06-28

Google Doc: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI

Goal: replace the compressed post-chapter-22 editorial assembly with a full book chapter/practicum about industrial launch readiness, then export and verify the manuscript proof.

## Result

The Google Doc now contains an explicit new chapter:

`Глава 23. Чеклист промышленного запуска`

The chapter turns the previous short practical block into a complete publishing-ready chapter that connects trace, eval gate, rollout wave and containment into one launch decision workflow.

The pass also fixed an inherited Google Docs list-format artifact at the beginning of the glossary. The final manuscript proof no longer shows oversized bullets in the chapter 23 -> glossary transition.

## Implemented plan

1. Tools and access stabilized: Google Docs/Drive connector, DOCX export, Template2000n derivative workflow and render QA path were used.
2. Target range located: old post-chapter-22 practicum started at `648821`; the next boundary was `Глоссарий` at `655941` before insertion.
3. Full chapter drafted and inserted: the new text is about 27k characters and includes narrative, walkthrough, release decision record, readiness checklist, failure modes and companion routing.
4. Google Doc verified by readback: the new chapter starts at `648821`, and the glossary boundary moved to `675966`.
5. Formatting stabilized: chapter 23 paragraph bullets were removed; glossary bullets were also removed in the exact range `675966-692117`.
6. DOCX artifacts prepared: raw Google Docs export and Template2000n derivative were created.
7. Render QA completed: raw and Template2000n DOCX were rendered to PDF/PNG and visually inspected.
8. Next 100 editorial goals prepared: see `docs/publisher/ru-editorial-100-ch23-launch-checklist-iterations-2026-06-28.md`.
9. Repository handoff prepared: this report, render metrics and DOCX artifacts are ready for commit/push after test verification.

## Chapter structure

- Зачем запуску нужен отдельный чеклист
- Связь с предыдущими главами
- Trace как первое доказательство
- Eval gate как условие перехода
- Rollout wave как управляемое изменение
- Containment как часть готовности
- Практический walkthrough: агент поддержки
- Release decision record как объект
- Readiness checklist для промышленного запуска
- Expand, hold, freeze and rollback
- Типовые ошибки launch checklist
- Companion route для этой главы
- Переход к глоссарию и приложениям
- Короткий вывод

## Render QA

Raw Google Doc export:

- DOCX: `docs/publisher/artifacts/agent-arch-ru-ch23-launch-checklist-pass-2026-06-28.docx`
- PDF render: `/private/tmp/agent_arch_ch23_launch_checklist_pass_2026_06_28_render_final3/agent-arch-ru-ch23-launch-checklist-pass-2026-06-28.pdf`
- Pages: 579
- Blank-like pages: 0
- Chapter 23 starts on page 499.
- Glossary transition starts on pages 512-513 and continues without oversized bullets.

Template2000n derivative:

- DOCX: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch23-launch-checklist-pass-2026-06-28.docx`
- Source style DOCX: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch22-policy-catalog-pass-2026-06-28.docx`
- PDF render: `/private/tmp/agent_arch_template2000n_ch23_launch_checklist_pass_2026_06_28_render_final3/agent-arch-ru-template2000n-ch23-launch-checklist-pass-2026-06-28.pdf`
- Pages: 315
- Blank-like pages: 0
- Chapter 23 starts on page 265.
- Glossary starts on page 274.

Template2000n style metrics:

- Body Text: 5787
- Heading 1: 117
- Heading 2: 994
- Heading 3: 280
- Removed body/list `numPr`: 2010

Visual spot checks:

- Raw pages 499-513: chapter start, trace/eval sections, walkthrough, checklist and glossary transition are readable.
- Template2000n pages 265-274: chapter start, H3 sections, walkthrough, release decision record, checklist and glossary transition are readable.
- Template2000n page 280: transition from glossary to practical cases is readable.

## Verification

- `python3 -m json.tool docs/publisher/ru-google-doc-ch23-launch-checklist-pass-2026-06-28.render-qa.json` passed.
- `uv run --group dev pytest` passed: 948 tests.
- `uv run --group docs mkdocs build --strict` passed. MkDocs still reports the existing publisher working files as pages outside `nav`; this is the established repository pattern for publisher-pass reports.

## Author-owned fields still open

The manuscript still needs author-owned factual input before publisher handoff:

- `Об авторе`: name/public name, role, verified experience, public projects, links and publisher wording.
- Public companion URL and version policy for the book release.
- Real author cases or anonymized implementation stories, if any should be added.
- Legal/compliance wording: especially AI tooling disclosure, limitations of templates and jurisdiction-specific disclaimers.
- Final publisher metadata: title wording, subtitle, cover copy, acknowledgements and any required imprint fields.

## Notes

- The Google Doc remains the source of truth for the manuscript.
- Template2000n is applied only as a derived DOCX proof.
- Existing unrelated local changes in publisher docs were left untouched.
