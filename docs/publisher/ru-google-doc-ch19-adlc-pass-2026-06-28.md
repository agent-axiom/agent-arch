# Google Doc chapter 19 ADLC pass - 2026-06-28

Цель прохода: реализовать полноценную книжную версию главы 19 в рабочем Google Doc, связать ее с главами 17-18 и подготовить свежие DOCX/proof-артефакты для издательского цикла.

## Google Doc

- Документ: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI
- Tab: `t.0`
- Начальная revisionId перед заменой: `ALtnJHyFmRqkbvGG-qsEouswRq4sFXlDcXCEKbMzYNA430Zubk5zUDtm_oAhni8bYiifRnpdcq4Gm3u2Nl_lxPaDpXqJ_OAAOaoMRCTRl-4`
- RevisionId после текстовой замены: `ALtnJHy8T0NBGhTFNhT1mi25CSZBQZ86hjwMmcrIPOPRmaZ4ODNsyYBBywIGUx0r0raLagzes0RFU2IpaQxM2iEPjNNPsfsdM-MKXjcBDOA`
- RevisionId после style pass: `ALtnJHymhwTY8Cilz8eKPw9g_XGrS9bg4rhvUWH3_8VP9qyGzVCmV4pEF4CiNCGnFPE7QPFvGyz9lEXIp6iNw3SSWTmsTB91QHxq8cBWV9o`

## Диапазон правки

- Старый диапазон главы 19 заменен в Google Doc: `518741..539016`.
- Новый старт заголовка главы 19: `519195..519252`.
- Новый старт главы 20: `553113..553198`.
- Соседняя глава 20 сохранена и начинается отдельным заголовком.

## Реализованные пункты

1. Переписан вход главы 19 как прямой переход от глав 17-18: ownership, standard paths and shared gateways превращаются в основу ADLC.
2. SDLC и ADLC разведены как базовый инженерный цикл и агентное расширение, а не как конкурирующие методологии.
3. Добавлены behavior-changing surfaces: prompts, model route, tools/capabilities, retrieval, memory, policy/verifier, approvals, evals, rollout/runtime controls, registry/ownership.
4. Добавлена классификация изменений: low, medium, high risk.
5. Для типов изменений добавлены owner, evidence and rollback routes.
6. Добавлен lifecycle gate: design -> build -> eval -> rollout -> observe -> incident -> retirement.
7. Длинные схемы, шаблоны и datasets вынесены в companion route.
8. Добавлен readiness checklist для ADLC.
9. Подготовлены fresh raw DOCX и Template2000n DOCX.
10. Выполнены render QA, локальный отчет, 100 следующих редакционных итераций.

## Содержательные изменения главы 19

Новая глава 19 стала самостоятельной книжной главой, а не compressed editorial assembly. В нее добавлены:

- объяснение, почему обычный SDLC не видит все агентные поверхности поведения;
- практическая модель ADLC как расширения SDLC;
- change record как единица управления жизненным циклом;
- риск-классификация и правила эскалации;
- связка owner/evidence/rollback для prompt, model route, tool, retrieval, memory, policy, approval, eval, rollout and registry changes;
- два практических сценария: support ticket agent и prompt/model/retrieval update;
- антибюрократический слой: tiered process, reusable evidence, standard paths;
- companion route для полных шаблонов;
- readiness checklist из 15 пунктов;
- переход к главе 20 про assurance loop, incident response, registry and retirement.

## DOCX artifacts

- Raw Google Doc export: `docs/publisher/artifacts/agent-arch-ru-ch19-adlc-pass-2026-06-28.docx`
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch19-adlc-pass-2026-06-28.docx`
- Render QA metrics: `docs/publisher/ru-google-doc-ch19-adlc-pass-2026-06-28.render-qa.json`
- Next 100 editorial iterations: `docs/publisher/ru-editorial-100-ch19-adlc-iterations-2026-06-28.md`

## Template2000n style metrics

- Paragraphs: 8258.
- Heading1: 55.
- Heading3: 14.
- BodyText: 6140.
- Removed body/list `numPr`: 2150.
- All 14 new chapter 19 subheads were found and mapped to `Heading3`.

## Render QA

Raw DOCX render:

- PDF pages: 623.
- PNG pages: 623.
- Blank-like pages: 0.
- Body marker pages:
  - `Глава 19. От SDLC к ADLC`: page 423.
  - `Readiness checklist для ADLC`: page 443.
  - `Глава 20. Контур заверения`: page 445.

Template2000n render:

- PDF pages: 322.
- PNG pages: 322.
- Blank-like pages: 0.
- Body marker pages:
  - `Глава 19. От SDLC к ADLC`: page 230.
  - `Readiness checklist для ADLC`: page 237.
  - `Глава 20. Контур заверения`: page 238.

Visual spot-check:

- Raw pages 423-426 and 442-445 checked: chapter start, readiness checklist and transition to chapter 20 are readable.
- Template2000n pages 230-233 and 236-239 checked: heading hierarchy and transition to chapter 20 are readable.

## Что автору нужно заполнить самостоятельно

- Блок `Об авторе`: имя, роль, публичное позиционирование, ключевой опыт, проекты, ссылки, формулировка для издательства.
- Финальное название/подзаголовок книги, если издательство попросит маркетинговую адаптацию.
- Предисловие: при желании добавить личный мотив и контекст автора.
- Степень раскрытия реального опыта: заменить общие placeholders на проверяемые авторские факты.
- Публичные ссылки: GitHub, сайт, блог, профиль, companion URL.
- Юридические и compliance-дисклеймеры: согласовать с издательством, если они нужны в конкретной серии.

## Ограничения прохода

- Экспорт в финальные издательские форматы пока не выполнялся.
- Template2000n `.dot` напрямую не применялся; использован проверенный derivative-путь через предыдущий Template2000n DOCX.
- Визуальная проверка была точечной по измененному диапазону и автоматической по blank-like pages.
