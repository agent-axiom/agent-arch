# Google Doc chapter 22 policy/catalog pass - 2026-06-28

Цель прохода: переписать главу 22 как полноценную книжную главу про policy/catalog layer, убрать справочную перегрузку в companion route, раскрыть policy decision object и capability catalog как operational contract, затем подготовить свежие DOCX/proof-артефакты.

## Google Doc

- Документ: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI
- Tab: `t.0`
- Начальная revisionId перед заменой: `ALtnJHwk5Xsz1wvzI5wRTcO_Wdz50tLo1tyFX55wR1ZXoDzGPRwM31UrJVOjyp_bhInPIl5lhIFcfg37wyBD-xq4GrDEd7jwhouspBP67CQ`
- RevisionId после замены и style pass: `ALtnJHxbhew6DMK3zFfl00XJ9BS5DT3lLV5F5bWb4L1M2vzdlc5A2FRTxY50xKXVuI2TQvs4KkT4T4a-ziBhAby7dlKH7Mp-7dI9NzD8Qg4`

## Диапазон правки

- Старый диапазон главы 22 заменен в Google Doc: `606950..644178`.
- Новый старт главы 22: `606950..606995`.
- Новый следующий структурный блок после главы 22: `648821..648893`, `Практикум: пройти цепочку trace -> eval gate -> rollout wave -> containment`.
- Новый текст главы 22: около 41,9 тыс. знаков, 272 строки в рабочем черновике.

## Реализованные 9 пунктов

1. Найден точный диапазон главы 22 и проверена граница со следующим структурным блоком.
2. Справочная перегрузка главы снята: YAML, validation-message catalogs and full schemas вынесены в companion route.
3. Opening переписан как прямое продолжение главы 21: runtime уже есть, но без policy/catalog не отвечает на вопрос полномочий.
4. Раскрыт `policy decision object`: `allowed`, `denied`, `approval_required`, `reason_code`, `constraints`, `policy_bundle_version`, `evidence`.
5. `Capability catalog` раскрыт как operational contract: owner, risk tier, data scope, tool binding, approval, verifier, telemetry and lifecycle.
6. Добавлены walkthrough для read capability, write capability and approval-required capability.
7. Добавлен readiness checklist для policy/catalog layer.
8. Google Doc обновлен, raw DOCX and Template2000n DOCX экспортированы, render QA выполнен.
9. Подготовлены локальный отчет, render QA JSON and 100 следующих редакционных целей.

## Содержательные изменения главы 22

Новая глава теперь:

- объясняет, почему policy/catalog следует после runtime, а не до него;
- отделяет tool от capability и показывает capability как действие с владельцем, риском и жизненным циклом;
- описывает policy decision как исполняемый объект, а не как текстовую рекомендацию;
- показывает разные последствия `allowed`, `denied` and `approval_required`;
- объясняет, почему approval должен быть связан с конкретным payload and expiration;
- связывает verifier requirements с catalog, а не с произвольным решением модели;
- добавляет runtime integration points: data access, capability selection, normalized action, post-approval check, post-tool constraints and memory persistence;
- добавляет testing model для policy/catalog: contract, decision, integration, trace, adversarial and operational drills;
- добавляет owner dashboard angle для эксплуатации capabilities;
- готовит переход к практикуму trace -> eval gate -> rollout wave -> containment.

## DOCX artifacts

- Raw Google Doc export: `docs/publisher/artifacts/agent-arch-ru-ch22-policy-catalog-pass-2026-06-28.docx`
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch22-policy-catalog-pass-2026-06-28.docx`
- Render QA metrics: `docs/publisher/ru-google-doc-ch22-policy-catalog-pass-2026-06-28.render-qa.json`
- Next 100 editorial goals: `docs/publisher/ru-editorial-100-ch22-policy-catalog-iterations-2026-06-28.md`

## Template2000n style metrics

- Paragraphs mapped with text: 5989.
- Heading1: 88.
- Heading3: 141.
- BodyText: 5760.
- Removed body/list `numPr`: 2148.
- Source style DOCX: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch21-runtime-pass-2026-06-28.docx`.
- Mapping rule: main body to `BodyText`; real top-level sections to `Heading1`; chapter 19-22/practical structural subheads to `Heading3`; body/list numbering removed to avoid oversized list markers.

## Render QA

Raw DOCX render:

- PDF pages: 579.
- PNG pages: 579.
- Blank-like pages: 0.
- Body marker pages:
  - `Глава 22. Слой политик и каталог возможностей`: pages 29 and 484.
  - `Policy decision как объект исполнения`: page 485.
  - `Walkthrough: read capability`: page 491.
  - `Readiness checklist для policy/catalog layer`: page 493.
  - `Практикум: пройти цепочку trace`: page 499.

Template2000n render:

- PDF pages: 311.
- PNG pages: 311.
- Blank-like pages: 0.
- Body marker pages:
  - `Глава 22. Слой политик и каталог возможностей`: pages 19 and 254.
  - `Policy decision как объект исполнения`: page 255.
  - `Walkthrough: read capability`: page 259.
  - `Readiness checklist для policy/catalog layer`: page 262.
  - `Практикум: пройти цепочку trace`: page 266.

Visual spot-check:

- Raw pages 484-499 checked: chapter start, decision object, catalog contract, walkthroughs, checklist, testing, dashboard, final summary and practical transition are readable; no blank transition page.
- Template2000n pages 254-266 checked: chapter start, H3 sections, walkthroughs and checklist are readable; practical transition is preserved; no oversized bullets in checked range.

## Что автору нужно заполнить самостоятельно

- Блок `Об авторе`: имя, роль, публичное позиционирование, ключевой опыт, публичные проекты и ссылки.
- Авторская формулировка для издательства.
- Публичный адрес companion and final companion structure, especially chapter 22 policy/catalog route.
- Реальные практические кейсы автора, если нужно усилить главу личным опытом.
- Финальные юридические, отраслевые или compliance-disclaimers, если издательство их потребует.
- Решение о названии следующего структурного блока: сейчас в Google Doc он начинается как `Практикум: пройти цепочку trace -> eval gate -> rollout wave -> containment`, а не как явная `Глава 23`.

## Ограничения прохода

- Финальные издательские форматы не экспортировались.
- Template2000n `.dot` напрямую не применялся; использован проверенный derivative-путь через предыдущий Template2000n DOCX.
- Visual QA выполнен по DOCX/PDF render and contact sheets, а не через ручную проверку в Microsoft Word.

