# Google Doc chapter 21 runtime pass - 2026-06-28

Цель прохода: переписать главу 21 как полноценную книжную главу про reference runtime, связать ее с организационным слоем глав 17-20, убрать справочный CLI/YAML перегруз в companion route и подготовить свежие DOCX/proof-артефакты.

## Google Doc

- Документ: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI
- Tab: `t.0`
- Начальная revisionId перед заменой: `ALtnJHzSEd0xNyRpBp8L6ZT0oqMUaP8sDukuWX_hwHyMoVET-3_jIQjSJUOjn5-fttDTOxLoPmF6UUx0gVyZOLCPEAzXQ3yYlO55G7bEa58`
- RevisionId после текстовой замены: `ALtnJHz7srEe3YlMZvRlsbNoMlek3k9Bk03cfCxT52fnE5g4hT088hkDiDgVMOsvfldvPIKDzgNOdV20nCvWigmXacFVDt2iZjyFkmzeSf8`
- RevisionId после style pass: `ALtnJHzQZsQgasNUFUBPNGce4a6ydH3FZF1f85zbjr1q0qvJaoy1SKgBUW54o4w5iQFw7jhsucE-cc1OW3mc_2hhzeAvWTgCkfH6wMhtsB8`
- RevisionId после финального anti-blank-page блока: `ALtnJHwk5Xsz1wvzI5wRTcO_Wdz50tLo1tyFX55wR1ZXoDzGPRwM31UrJVOjyp_bhInPIl5lhIFcfg37wyBD-xq4GrDEd7jwhouspBP67CQ`

## Диапазон правки

- Старый диапазон главы 21 заменен в Google Doc: `576810..595281`.
- Новый старт главы 21: `576810..576850`.
- Новый старт главы 22 после финального блока: `606950..606995`.
- Глава 22 сохранена как отдельный соседний блок: `Глава 22. Слой политик и каталог возможностей`.

## Реализованные пункты

1. Разобрана текущая глава 21 и найдена справочная перегрузка: CLI/YAML/skeleton details смешивали книжную аргументацию с companion material.
2. Opening переписан как переход от organizational layer к reference runtime.
3. Runtime описан как минимальный набор границ и контрактов, а не production framework.
4. Раскрыты runtime components: run identity, principal, policy gateway, capability catalog, tool gateway, memory, approval queue, trace, eval export and rollout controls.
5. Добавлен walkthrough одного запуска: request intake -> context -> model step -> policy/capability -> approval -> tool execution -> verification/evidence -> user/operator response.
6. CLI, YAML, event catalogs, payload and detailed schemas вынесены в companion route.
7. Добавлен readiness checklist для reference runtime.
8. Google Doc обновлен, raw DOCX and Template2000n DOCX экспортированы, render QA выполнен.
9. Подготовлены локальный отчет, QA JSON and 100 следующих редакционных итераций.

## Содержательные изменения главы 21

Новая глава 21 теперь выполняет роль входа в часть VII:

- связывает главы 17-20 с исполнимой средой, а не начинает part VII как отдельный справочник;
- объясняет reference runtime как проверяемую форму системы;
- показывает границы между model intent, policy decision, capability, tool gateway, memory, approval, trace, evidence and rollout;
- показывает, как один запрос поддержки проходит через runtime;
- оставляет в печатной книге архитектурные решения, а механические команды и payload относит к companion;
- добавляет практический review angle, чтобы команды могли использовать главу как checklist для одного golden path.

## DOCX artifacts

- Raw Google Doc export: `docs/publisher/artifacts/agent-arch-ru-ch21-runtime-pass-2026-06-28.docx`
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch21-runtime-pass-2026-06-28.docx`
- Render QA metrics: `docs/publisher/ru-google-doc-ch21-runtime-pass-2026-06-28.render-qa.json`
- Next 100 editorial iterations: `docs/publisher/ru-editorial-100-ch21-runtime-iterations-2026-06-28.md`

## Template2000n style metrics

- Paragraphs: 6130.
- Heading1: 82.
- Heading3: 58.
- BodyText: 5990.
- Removed body/list `numPr`: 2150.
- H3 для глав 19-21 сохранены; body/list numbering снят, чтобы Template2000n не создавал oversized list markers.

## Render QA

Raw DOCX render:

- PDF pages: 601.
- PNG pages: 601.
- Blank-like pages: 0.
- Body marker pages:
  - `Глава 21. Базовая схема среды исполнения`: pages 29 and 470.
  - `Зачем нужна эталонная среда исполнения`: page 471.
  - `Walkthrough одного запуска`: page 479.
  - `Readiness checklist для reference runtime`: page 481.
  - `Глава 22. Слой политик и каталог возможностей`: pages 29 and 485.

Template2000n render:

- PDF pages: 277.
- PNG pages: 277.
- Blank-like pages: 0.
- Body marker pages:
  - `Глава 21. Базовая схема среды исполнения`: pages 18 and 218.
  - `Зачем нужна эталонная среда исполнения`: page 218.
  - `Walkthrough одного запуска`: page 224.
  - `Readiness checklist для reference runtime`: page 225.
  - `Глава 22. Слой политик и каталог возможностей`: pages 18 and 227.

Visual spot-check:

- Raw pages 470-485 checked: chapter 21 start, dense component sections, walkthrough, checklist, final review block and chapter 22 transition are readable; first-pass blank page was removed.
- Template2000n pages 218-227 checked: chapter start, H3 sections, checklist and chapter 22 transition are readable; no oversized bullets observed in the checked range.

## Что автору нужно заполнить самостоятельно

- Блок `Об авторе`: имя, роль, публичное позиционирование, ключевой опыт, публичные проекты и ссылки.
- Авторская формулировка для издательства.
- Публичный адрес companion и финальная структура материалов, особенно runtime companion route.
- Реальные практические примеры или кейсы автора, если нужно усилить главу личным опытом.
- Дисклеймеры по юридическим, отраслевым или compliance-ограничениям, если издательство их потребует.

## Ограничения прохода

- Финальные издательские форматы не экспортировались.
- Template2000n `.dot` напрямую не применялся; использован проверенный derivative-путь через предыдущий Template2000n DOCX.
- Visual QA выполнен по DOCX/PDF render and spot-check pages, а не через live browser view.
