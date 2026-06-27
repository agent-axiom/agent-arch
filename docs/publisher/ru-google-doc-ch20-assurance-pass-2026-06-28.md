# Google Doc chapter 20 assurance pass - 2026-06-28

Цель прохода: доработать главу 20 как полноценную книжную главу про production assurance loop, incident response, agent registry and retirement, убрать дублирование с главой 19 и подготовить свежие DOCX/proof-артефакты.

## Google Doc

- Документ: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI
- Tab: `t.0`
- Начальная revisionId перед заменой: `ALtnJHymhwTY8Cilz8eKPw9g_XGrS9bg4rhvUWH3_8VP9qyGzVCmV4pEF4CiNCGnFPE7QPFvGyz9lEXIp6iNw3SSWTmsTB91QHxq8cBWV9o`
- RevisionId после текстовой замены: `ALtnJHwQgDNli79rleRHpOYp_DG6GsZpiGyNg5ZqW0U6he5Aa0lLKx4LEyLt0V2NkXM_eQhTePOcP3qvYysFA1DMal6A2njqZ5_XKGdreYg`
- RevisionId после style pass: `ALtnJHzSEd0xNyRpBp8L6ZT0oqMUaP8sDukuWX_hwHyMoVET-3_jIQjSJUOjn5-fttDTOxLoPmF6UUx0gVyZOLCPEAzXQ3yYlO55G7bEa58`

## Диапазон правки

- Старый диапазон главы 20 заменен в Google Doc: `553113..583530`.
- Новый старт главы 20: `553113..553198`.
- Новый старт части VII: `576756..576809`.
- Новый старт главы 21: `576810..576850`.
- Часть VII и глава 21 сохранены как отдельные соседние блоки.

## Реализованные пункты

1. Разобрана текущая глава 20 и подтверждены точные Google Docs-границы главы 20/части VII/главы 21.
2. Убрано дублирование с главой 19: глава 20 теперь не повторяет ADLC gates, а развивает production assurance.
3. Усилен assurance loop и его отличие от evals and release gates.
4. Incident response связан с trace, change_id, rollout gate and owner map.
5. Agent registry раскрыт как production inventory of authority, а не как таблица описаний.
6. Retirement описан как инженерный процесс с gates: stop-new-work, authority cleanup, memory/data cleanup, migration, decommission evidence.
7. Добавлены readiness checklist, companion route and transition to part VII.
8. Подготовлены fresh raw DOCX, Template2000n DOCX and render QA.
9. Подготовлены локальный отчет и 100 следующих редакционных итераций.

## Содержательные изменения главы 20

Новая глава 20 теперь держит отдельную роль в дуге глав 17-20:

- главы 17-18: ownership and standard paths;
- глава 19: ADLC as lifecycle for behavior-changing changes;
- глава 20: assurance loop as ongoing production control.

В главе добавлены:

- distinction between evaluation, release gate and assurance loop;
- production signals: quality drift, policy/verifier signals, tool/side-effect signals, approval anomalies, memory/retrieval signals, lifecycle/ownership signals, near misses;
- finding record and finding taxonomy;
- incident response flow: evidence freeze, containment, incident timeline, root cause, corrective action package;
- trace/change/rollout/owner linkage invariant;
- production registry fields and enforceable lifecycle states;
- retirement as a practical decommission process;
- assurance cadence by risk tier and lifecycle state;
- readiness checklist for assurance loop;
- companion route for full templates and schemas.

## DOCX artifacts

- Raw Google Doc export: `docs/publisher/artifacts/agent-arch-ru-ch20-assurance-pass-2026-06-28.docx`
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch20-assurance-pass-2026-06-28.docx`
- Render QA metrics: `docs/publisher/ru-google-doc-ch20-assurance-pass-2026-06-28.render-qa.json`
- Next 100 editorial iterations: `docs/publisher/ru-editorial-100-ch20-assurance-iterations-2026-06-28.md`

## Template2000n style metrics

- Paragraphs: 8142.
- Heading1: 55.
- Heading3: 26.
- BodyText: 6112.
- Removed body/list `numPr`: 2150.
- All chapter 19 and chapter 20 subheads were found and mapped inside their chapter ranges only.

## Render QA

Raw DOCX render:

- PDF pages: 608.
- PNG pages: 608.
- Blank-like pages: 0.
- Body marker pages:
  - `Глава 20. Контур заверения`: page 445.
  - `Readiness checklist для assurance loop`: page 465.
  - `Часть VII. Эталонная реализация`: page 470.
  - `Глава 21. Базовая схема среды исполнения`: page 470.

Template2000n render:

- PDF pages: 314.
- PNG pages: 314.
- Blank-like pages: 0.
- Body marker pages:
  - `Глава 20. Контур заверения`: page 238.
  - `Readiness checklist для assurance loop`: page 242.
  - `Часть VII. Эталонная реализация`: page 243.
  - `Глава 21. Базовая схема среды исполнения`: page 243.

Visual spot-check:

- Raw pages 445-448 and 464-470 checked: chapter start, checklist, transition to part VII and chapter 21 are readable.
- Template2000n pages 238-245 checked: chapter start, dense sections, checklist and chapter 21 transition are readable.

## Что автору нужно заполнить самостоятельно

- Блок `Об авторе`: имя, роль, публичное позиционирование, ключевой опыт, публичные проекты и ссылки.
- Авторская формулировка для издательства.
- Публичный адрес companion и финальная структура материалов, если она изменится перед сдачей.
- Реальные практические примеры или кейсы автора, если нужно усилить главу личным опытом.
- Дисклеймеры по юридическим, отраслевым или compliance-ограничениям, если издательство их потребует.

## Ограничения прохода

- Финальные издательские форматы не экспортировались.
- Template2000n `.dot` напрямую не применялся; использован проверенный derivative-путь через предыдущий Template2000n DOCX.
- Visual QA выполнен по DOCX/PDF render and spot-check pages, а не через live browser view.
