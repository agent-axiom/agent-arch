# RU Publisher Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the first Russian publisher-readiness slice: terminology policy, manuscript assembly map, submission checklist, and targeted packet/surface cleanup.

**Architecture:** Keep the current MkDocs site as the broad public edition and add a separate `docs/publisher/` editorial layer for publisher-facing decisions. Touch existing public manuscript files only where the changes are low-risk and improve visible Russian editorial quality. Preserve unrelated uncommitted work by staging/committing only the files named in each task.

**Tech Stack:** Markdown, MkDocs Material with static i18n, Python/pytest docs surface tests, git.

---

## File structure

- Create `docs/publisher/ru-terminology.md`: canonical Russian editorial term policy and exceptions.
- Create `docs/publisher/ru-manuscript-map.md`: print/publisher assembly map from web chapters to compact manuscript chapters.
- Create `docs/publisher/ru-submission-checklist.md`: readiness gates for RU publisher submission.
- Modify `docs/publisher-ready-toc.md`: add a short RU submission addendum so the existing EN-oriented packet does not imply the same sample/export route for RU.
- Modify selected visible RU files only if the edit is mechanical and safe:
  - `docs/book/index.md`
  - `docs/book/part-iv/practical-mcp-a2a.md`
  - `docs/book/part-v/evidence-spine.md`
- Modify `tests/test_docs_surface.py` only if existing surface tests require old English-heavy Russian markers.

---

### Task 1: Create publisher editorial directory and terminology policy

**Files:**
- Create: `docs/publisher/ru-terminology.md`

- [ ] **Step 1: Create the terminology policy**

Write `docs/publisher/ru-terminology.md` with this content:

```markdown
# Русская терминологическая политика для издательской версии

Status: editorial working document for the Russian publisher manuscript. This file is not part of the public navigation.

## Цель

Русская версия должна читаться как книга, а не как внутренняя англо-русская документация. Английские термины допустимы, когда они являются стандартом отрасли, названием протокола, командой, форматом данных или частью кода. Во всех остальных случаях основной текст должен использовать устойчивую русскую форму.

## Основное правило

1. При первом появлении сложного термина можно дать английский вариант в скобках, если это помогает читателю сопоставить книгу с внешними источниками.
2. После первого появления использовать русскую форму.
3. В коде, CLI, YAML/JSON, именах полей и ссылках сохранять оригинальные английские имена.
4. Не смешивать несколько русских вариантов в одной главе без причины.

## Канонические варианты

| English term | Русская форма | Правило |
| --- | --- | --- |
| agent | агент | Не писать `agent`, кроме кода, названий протоколов и цитат. |
| agents | агенты | Не писать `agents` в заголовках русской книги. |
| tool | инструмент | `tool` допустим только в коде, CLI и именах полей. |
| tools | инструменты | В заголовках и обычном тексте — `инструменты`. |
| runtime | среда исполнения | `рантайм` допустим в главе про реализацию, но только как вторичный термин. |
| reference runtime | эталонная среда исполнения | Не писать `reference runtime` в русском потоке, кроме ссылок на пакет. |
| rollout | поэтапный выпуск | `раскатка` допустима во внутренних заметках, но в книге предпочтителен `поэтапный выпуск`. |
| deploy/deployment | развертывание | `деплой` не использовать в издательском тексте. |
| eval/evals | оценка/оценки | При первом появлении можно: `оценки (evals)`. Далее — `оценки`. |
| trace | трасса | Для сущности telemetry trace использовать `трасса`; не смешивать со `следом аудита`. |
| span | спан | Допустимый технический термин; при первом появлении объяснить как шаг внутри трассы. |
| policy | политика | `policy layer` -> `слой политик`. |
| approval | подтверждение | `approval record` -> `запись подтверждения`. |
| review | проверка | `ревью` использовать только для human/code-review контекста, если это действительно процесс ревью. |
| registry | реестр | Не писать `registry`, кроме имен полей и названий артефактов. |
| inventory | инвентаризация | Для состояния парка агентов: `инвентаризация`; для списка: `инвентарь` только если смысл именно список. |
| workflow | рабочий процесс | `workflow` допустим при первом сравнении с агентом, дальше `рабочий процесс`. |
| framework | фреймворк | Устоявшийся термин; не переводить как `рамка`, если речь о программном framework. |
| prompt | промпт | Допустимо как устоявшийся термин; `подсказка` использовать, когда речь о собранном сообщении модели. |
| prompt template | шаблон запроса | Не писать `prompt template` в русском заголовке. |
| manager pattern | паттерн координатора | При первом появлении можно дать английский вариант. |
| handoff | передача управления | Не писать `handoff` в русском потоке без необходимости. |
| multi-agent | многоагентный | `multi-agent` допустим при первом появлении и в источниках. |
| single-agent | одноагентный | `single-agent` допустим только при сравнении терминов. |
| happy path | успешный путь | Не использовать как регулярную английскую вставку. |
| case study | практический пример | `кейс` допустим разговорно, но в издательской версии лучше `пример` или `сценарий`. |
| canonical cases | канонические сценарии | Не писать `canonical cases` в русской версии. |
| case-spine note | сквозной сценарий | Служебную метку заменить на читательскую врезку или обычный абзац. |
| evidence spine | цепочка доказательств | Не оставлять `evidence spine` в русском заголовке без необходимости. |
| governance | управление | В сложных случаях: `операционное управление` или `управление жизненным циклом`. |
| assurance loop | контур уверенности | При первом появлении можно дать английский термин в скобках. |
| red teaming | red teaming | Оставить английский как стандарт практики; рядом дать объяснение. |
| detection | обнаружение | Не писать `detection` в русских заголовках. |
| response | реагирование | Не писать `response` в русских заголовках. |
| retirement | вывод из эксплуатации | Не писать `retirement` в русских заголовках. |
| replacement | замена | Не писать `replacement` в русских заголовках. |
| end-of-life | конец жизненного цикла | Не писать `end-of-life discipline` в русских заголовках. |
| agentic misalignment | рассогласование поведения агента | Можно дать английский термин при первом появлении. |
| insider risk | внутренний риск | Не писать `insider-risk` в русских заголовках. |
| behavioral evals | поведенческие оценки | При первом появлении можно дать английский термин. |
| control evals | контрольные оценки | При первом появлении можно дать английский термин. |
| automated red teaming | автоматизированный red teaming | Оставить `red teaming`, перевести остальное. |

## Протоколы и форматы, которые не переводим

- MCP
- A2A
- SLO
- CLI
- YAML
- JSON
- GitHub Pages
- MkDocs
- Material for MkDocs
- Mermaid
- Observable Plot
- Python
- TypeScript
- Rust
- uv
- ruff
- pytest

## Издательское правило для приложений

В печатной рукописи не должно быть длинных списков CLI-полей, validation errors, JSON payloads и полного runtime output. Такая информация остается в online companion. В книге оставлять только:

- зачем контракт нужен;
- какие решения он заставляет принять;
- минимальный пример;
- ссылку на полный companion artifact.

## Правило для обращений к читателю

Авторский стиль может обращаться к читателю напрямую, но не должен превращаться в разговорный туториал. Если предложение звучит слишком лично, заменить:

- `у тебя` -> `в системе` или `у команды`;
- `ты должен` -> `команда должна` или `архитектура должна`;
- `если ты строишь` -> `если команда строит`.

Прямое `ты` оставить там, где оно усиливает авторский голос в начале главы или в практическом чеклисте.
```

- [ ] **Step 2: Verify Markdown was created**

Run:

```bash
test -f docs/publisher/ru-terminology.md && grep -n "runtime" docs/publisher/ru-terminology.md
```

Expected: output includes the canonical `runtime` row.

- [ ] **Step 3: Commit Task 1**

Run:

```bash
git add docs/publisher/ru-terminology.md
git commit -m "Add Russian publisher terminology policy" -- docs/publisher/ru-terminology.md
```

Expected: commit succeeds and only `docs/publisher/ru-terminology.md` is committed.

---

### Task 2: Create Russian publisher manuscript map

**Files:**
- Create: `docs/publisher/ru-manuscript-map.md`

- [ ] **Step 1: Create the manuscript map**

Write `docs/publisher/ru-manuscript-map.md` with this content:

```markdown
# Карта русской издательской рукописи

Status: editorial assembly map. The public website remains broader than this print manuscript.

## Назначение

Публичная версия книги остается полной web-версией: 8 частей, 27 глав, практические страницы, схемы, справочные приложения и эталонная среда исполнения. Для издательства нужна более компактная рукопись: меньше справочного шума, яснее маршрут чтения, меньше повторов и тяжелых runtime-деталей.

## Целевой формат

- 6 частей;
- около 20 глав;
- 2 sample chapters для первого контакта с редактором;
- online companion для схем, CLI, runtime output, validation errors, длинных чеклистов и источников.

## Предлагаемая структура

### Часть I. Зачем агентам нужна платформа

**Печатная глава 1. Почему агенту нужна платформа, а не магия**

Источник:

- `docs/book/part-i/chapter-1.md`

Роль:

- главный sample chapter;
- вводит тезис книги;
- показывает отличие книги от prompt-hype и framework manual.

Редакторская задача:

- сохранить сильный авторский голос;
- убрать служебные англоязычные метки;
- сделать финал главы пригодным для печати без ссылок на структуру сайта.

**Печатная глава 2. Анатомия производственной агентной системы**

Источники:

- `docs/book/part-i/chapter-2.md`
- `docs/book/part-i/practical-routines.md`
- `docs/book/part-i/practical-manager-handoffs.md`

Роль:

- объяснить базовую архитектуру, инструкции, сценарии, шаблоны запросов, координатора и передачу управления.

Что вынести в companion:

- длинные code sketches;
- дополнительные decision tables.

**Печатная глава 3. Границы доверия, идентичность и право действовать**

Источники:

- `docs/book/part-ii/chapter-3.md`
- часть материала из `docs/book/part-ii/chapter-4.md`

Роль:

- задать security perimeter как основу всей книги.

### Часть II. Контекст, память и извлечение

**Печатная глава 4. Контекст как контракт среды исполнения**

Источники:

- `docs/book/part-iii/chapter-5.md`
- начало `docs/book/part-iii/chapter-7.md`

Роль:

- объяснить, почему память и контекст являются управляемым состоянием, а не удобной функцией.

**Печатная глава 5. Память, происхождение знаний и устойчивость**

Источники:

- `docs/book/part-iii/chapter-6.md`
- `docs/appendix/memory-retrieval-schema.md` как companion reference

Роль:

- разделить краткосрочную, долговременную и профильную память;
- ввести provenance и правила записи.

**Печатная глава 6. Извлечение, уплотнение и фоновые обновления**

Источник:

- `docs/book/part-iii/chapter-7.md`

Роль:

- показать retrieval/compaction как управляемый слой качества и безопасности.

### Часть III. Инструменты, побочные эффекты и выполнение

**Печатная глава 7. Модель выполнения и каталог инструментов**

Источник:

- `docs/book/part-iv/chapter-8.md`

Роль:

- показать, почему агент не должен обращаться к инструментам напрямую.

**Печатная глава 8. Песочницы, MCP и интеграционные границы**

Источники:

- `docs/book/part-iv/chapter-9.md`
- `docs/book/part-iv/practical-mcp-a2a.md`

Роль:

- объяснить MCP как контрактную границу, а A2A как отдельную модель доверия.

**Печатная глава 9. Повторы, идемпотентность, лимиты и восстановление после сбоев**

Источники:

- `docs/book/part-iv/chapter-10.md`
- `docs/appendix/tool-failure-recovery.md` as companion reference

Роль:

- связать failure recovery с безопасным выполнением инструментов.

### Часть IV. Надежность, наблюдаемость и оценки

**Печатная глава 10. Трассы и наблюдаемость запусков агента**

Источник:

- `docs/book/part-v/chapter-11.md`

Роль:

- объяснить trace/span/event как доказательную модель, а не только логи.

**Печатная глава 11. SLO и деградированные пути**

Источник:

- `docs/book/part-v/chapter-12.md`

Роль:

- показать, как измерять здоровье агентной системы.

**Печатная глава 12. Оценки, регрессионные шлюзы и решение о выпуске**

Источник:

- `docs/book/part-v/chapter-13.md`

Роль:

- technical credibility sample;
- связать оценки, verifier outputs и release judgment.

**Печатная глава 13. Цепочка доказательств от запроса к решению**

Источник:

- `docs/book/part-v/evidence-spine.md`

Роль:

- короткая синтезирующая глава, не справочник;
- показать общий entity map и end-to-end run.

### Часть V. Выпуск и эксплуатация агентов

**Печатная глава 14. Платформенная команда и продуктовые команды**

Источник:

- `docs/book/part-vi/chapter-14.md`

Роль:

- объяснить ownership model.

**Печатная глава 15. Золотые пути, общие шлюзы и антизоопарк-подходы**

Источник:

- `docs/book/part-vi/chapter-15.md`

Роль:

- показать, как организация избегает хаоса множества агентных реализаций.

**Печатная глава 16. Эталонная среда исполнения и производственный запуск**

Источники:

- `docs/book/part-vii/chapter-16.md`
- `docs/book/part-vii/chapter-17.md`
- `docs/book/part-vii/chapter-18.md`

Роль:

- дать минимальный runtime blueprint без превращения главы в CLI manual.

Что вынести в companion:

- full reference package walkthrough;
- команды CLI;
- config contracts;
- runtime internals.

### Часть VI. Жизненный цикл, управление и вывод из эксплуатации

**Печатная глава 17. От SDLC к ADLC: жизненный цикл агентной системы**

Источники:

- `docs/book/part-viii/chapter-19.md`
- часть `docs/book/part-viii/chapter-20.md`

Роль:

- задать lifecycle frame и change-bearing system model.

**Печатная глава 18. Assurance, реагирование и доверенные артефакты**

Источники:

- `docs/book/part-viii/chapter-21.md`
- `docs/book/part-viii/chapter-22.md`

Роль:

- объединить assurance loop, incident response, provenance и artifact lineage.

**Печатная глава 19. Рассогласование поведения, внутренний риск и контрольные оценки**

Источники:

- `docs/book/part-viii/chapter-24.md`
- `docs/book/part-viii/chapter-25.md`

Роль:

- показать adversarial pressure и reviewable judgment.

**Печатная глава 20. Реестр, инвентаризация и конец жизненного цикла**

Источники:

- `docs/book/part-viii/chapter-23.md`
- `docs/book/part-viii/chapter-26.md`
- `docs/book/part-viii/chapter-27.md`

Роль:

- закрыть книгу ответственностью за estate, retirement и long-term accountability.

## Online companion boundary

Оставить преимущественно online:

- `docs/appendix/reference-package.md`;
- schema appendices for trace/eval/approval/policy/memory/lifecycle/change/incident;
- long CLI outputs;
- validation error catalogs;
- full YAML/JSON examples;
- source catalog;
- community roadmap;
- detailed policy templates and worksheets.

## Sample chapters for Russian publishers

Primary sample:

- role: opening editorial sample;
- source path: `docs/book/part-i/chapter-1.md`;
- reason: strongest thesis chapter.

Secondary sample:

- role: technical credibility sample;
- source path: `docs/book/part-v/chapter-13.md`;
- reason: shows evals, traces, verifier outputs, regression gates and release judgment.

Optional differentiator sample:

- role: lifecycle/governance uniqueness sample;
- source path: merged print chapter from `docs/book/part-viii/chapter-23.md`, `docs/book/part-viii/chapter-26.md`, and `docs/book/part-viii/chapter-27.md`;
- reason: fewer competing books cover registry, retirement and estate accountability.

## First editorial pass order

1. Chapter 1.
2. Chapter 13.
3. Part VIII compression chapters.
4. Reference/runtime chapter compression.
5. Appendix-to-companion pass.
6. Full terminology pass.
7. Print/PDF export pass.
```

- [ ] **Step 2: Verify key source paths exist**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    'docs/book/part-i/chapter-1.md',
    'docs/book/part-v/chapter-13.md',
    'docs/book/part-viii/chapter-23.md',
    'docs/book/part-viii/chapter-26.md',
    'docs/book/part-viii/chapter-27.md',
]
for path in paths:
    print(path, Path(path).exists())
PY
```

Expected: every line ends with `True`.

- [ ] **Step 3: Commit Task 2**

Run:

```bash
git add docs/publisher/ru-manuscript-map.md
git commit -m "Add Russian publisher manuscript map" -- docs/publisher/ru-manuscript-map.md
```

Expected: commit succeeds and only `docs/publisher/ru-manuscript-map.md` is committed.

---

### Task 3: Create Russian submission checklist

**Files:**
- Create: `docs/publisher/ru-submission-checklist.md`

- [ ] **Step 1: Create the checklist**

Write `docs/publisher/ru-submission-checklist.md` with this content:

```markdown
# Чеклист готовности русской версии к издательству

Status: working gate for Russian publisher submission.

## Verdict scale

- **Ready:** можно отправлять редактору как издательский пакет.
- **Almost ready:** можно показывать доверенному редактору/агенту как предварительный пакет.
- **Not ready:** не отправлять как готовую рукопись; сначала закрыть блокеры.

Current status: **Not ready as a final publisher submission; strong enough for internal editorial packaging.**

## P0 gates before external submission

- [ ] Целевая подача выбрана: Russian publisher package, English publisher package, or dual-track package.
- [ ] Для Russian package sample manifest указывает RU source paths, not `.en.md` paths.
- [ ] Есть отдельная assembly map for print manuscript.
- [ ] Терминологическая политика применена к sample chapters.
- [ ] Chapter 1 passed Russian line edit.
- [ ] Chapter 13 passed Russian line edit.
- [ ] Part VIII compression plan is applied or explicitly deferred with a waiver.
- [ ] Book/reference split is explicit: runtime/schema details moved or marked as companion-only.
- [ ] Author bio / credential framing is provided by the author.
- [ ] Target editor/imprint formatting requirements are known or explicitly waived.

## P1 gates before serious editor review

- [ ] `case-spine note` and `canonical cases` are removed from Russian reader-facing prose or turned into Russian reader-facing labels.
- [ ] Russian headings avoid unnecessary English terms.
- [ ] `tools`, `agents`, `rollout`, `runtime`, `review`, `registry`, `inventory`, `assurance`, `retirement`, and `end-of-life` follow the terminology policy.
- [ ] Repeated maturity-check endings are intentionally templated rather than accidentally repetitive.
- [ ] Dense CLI/runtime details are moved to online companion or summarized.
- [ ] All Mermaid diagrams have print-safe fallback prose or captions.
- [ ] Long tables and code blocks are reviewed for PDF/print readability.
- [ ] Public companion links are stable.

## P2 gates before final manuscript delivery

- [ ] Full Russian proofread completed.
- [ ] Cross-references checked after print assembly.
- [ ] Glossary matches the terminology policy.
- [ ] Bibliography/source catalog is curated for book use rather than web completeness.
- [ ] Figure captions are complete.
- [ ] Code examples have consistent formatting and line length.
- [ ] Final `mkdocs build --strict` passes.
- [ ] Final docs surface tests pass.
- [ ] `git diff --check` is clean.

## Recommended first external packet

Include:

1. One-page Russian positioning memo.
2. Proposed print table of contents.
3. Chapter 1 sample.
4. Chapter 13 sample if the editor asks for technical depth.
5. Companion-site description.
6. Author bio and platform note.
7. Status note: public web manuscript exists; publisher manuscript is being assembled from it.

Do not include:

- full schema appendices;
- full CLI reference;
- generated site files;
- internal editorial backlog;
- raw source catalog unless requested.
```

- [ ] **Step 2: Verify checklist status line**

Run:

```bash
grep -n "Current status" docs/publisher/ru-submission-checklist.md
```

Expected: output says the final publisher submission is not ready yet.

- [ ] **Step 3: Commit Task 3**

Run:

```bash
git add docs/publisher/ru-submission-checklist.md
git commit -m "Add Russian publisher submission checklist" -- docs/publisher/ru-submission-checklist.md
```

Expected: commit succeeds and only `docs/publisher/ru-submission-checklist.md` is committed.

---

### Task 4: Add RU submission addendum to existing publisher packet

**Files:**
- Modify: `docs/publisher-ready-toc.md`

- [ ] **Step 1: Add a short Russian-track addendum after the Manuscript status section**

Find the `**Manuscript status:**` bullet block near the top of `docs/publisher-ready-toc.md`. After that block, insert:

```markdown
## Russian Submission Track Addendum

The packet above is still useful for positioning, but Russian publisher submission should not reuse the English sample manifest unchanged.

For a Russian publisher-facing packet:

- use `docs/book/part-i/chapter-1.md` as the primary sample source;
- use `docs/book/part-v/chapter-13.md` as the technical credibility sample source;
- use [Russian publisher manuscript map](publisher/ru-manuscript-map.md) as the assembly guide;
- use [Russian terminology policy](publisher/ru-terminology.md) before line-editing samples;
- use [Russian submission checklist](publisher/ru-submission-checklist.md) as the pre-send gate.

If the target is an English-language publisher, keep the existing `.en.md` sample manifest and describe the Russian manuscript as the public source/core edition.
```

- [ ] **Step 2: Verify links resolve by running strict build**

Run:

```bash
.venv/bin/mkdocs build --strict
```

Expected: build succeeds. If the build does not include excluded editorial docs, this still verifies no accidental public nav/link break was introduced in included files.

- [ ] **Step 3: Commit Task 4**

Run:

```bash
git add docs/publisher-ready-toc.md
git commit -m "Clarify Russian publisher submission track" -- docs/publisher-ready-toc.md
```

Expected: commit succeeds and only `docs/publisher-ready-toc.md` is committed.

---

### Task 5: Clean visible Russian reader-facing headings and labels

**Files:**
- Modify: `docs/book/index.md`
- Modify: `docs/book/part-iv/practical-mcp-a2a.md`
- Modify: `docs/book/part-v/evidence-spine.md`
- Modify: `tests/test_docs_surface.py` if tests assert old labels

- [ ] **Step 1: Inspect current English-heavy headings**

Run:

```bash
grep -RInE 'book promise|recommended reading path|direct entry points|tools|agents|Decision table|code sketch|walkthrough run|rollout' docs/book/index.md docs/book/part-iv/practical-mcp-a2a.md docs/book/part-v/evidence-spine.md
```

Expected: output shows current labels to clean.

- [ ] **Step 2: Apply mechanical replacements in the three RU files**

Use exact replacements:

- In `docs/book/index.md`:
  - `## Что обещает эта книга (book promise)` -> `## Что обещает эта книга`
  - `## Рекомендуемый маршрут чтения (recommended reading path)` -> `## Рекомендуемый маршрут чтения`
  - `## Быстрый ориентир по стабильности (stability guide)` -> `## Быстрый ориентир по стабильности`
  - `## Прямые точки входа (direct entry points)` -> `## Прямые точки входа`
  - `canonical cases` -> `канонические сценарии`
  - `Support triage` -> `разбор обращений поддержки`
  - `Internal knowledge assistant` -> `внутренний ассистент знаний`
  - `Incident coordination` -> `координация инцидентов`

- In `docs/book/part-iv/practical-mcp-a2a.md`:
  - `# Практика. MCP для tools, A2A для agents` -> `# Практика. MCP для инструментов, A2A для агентов`
  - `## 4. Типовая ошибка: строить multi-agent слишком рано` -> `## 4. Типовая ошибка: строить многоагентную систему слишком рано`
  - `## 5. Decision table` -> `## 5. Таблица решений`
  - `## 8. Минимальный code sketch` -> `## 8. Минимальный кодовый эскиз`

- In `docs/book/part-v/evidence-spine.md`:
  - `# Сквозная цепочка доказательств: от запроса к решению о rollout` -> `# Сквозная цепочка доказательств: от запроса к решению о поэтапном выпуске`
  - `## Один сквозной walkthrough run` -> `## Один сквозной запуск`

- [ ] **Step 3: Run surface tests to reveal any old-marker expectations**

Run:

```bash
.venv/bin/pytest tests/test_docs_surface.py -q
```

Expected: tests either pass or fail only on old English-heavy Russian marker expectations.

- [ ] **Step 4: If tests fail on old Russian labels, update only those assertions**

For each failure in `tests/test_docs_surface.py`, replace the old expected Russian marker with the new Russian marker. Do not change English or Chinese assertions unless the failure specifically requires it.

- [ ] **Step 5: Commit Task 5**

Run:

```bash
git add docs/book/index.md docs/book/part-iv/practical-mcp-a2a.md docs/book/part-v/evidence-spine.md tests/test_docs_surface.py
git commit -m "Clean visible Russian publisher terminology" -- docs/book/index.md docs/book/part-iv/practical-mcp-a2a.md docs/book/part-v/evidence-spine.md tests/test_docs_surface.py
```

Expected: commit succeeds with only touched files staged. If `tests/test_docs_surface.py` did not change, git will ignore it in the pathspec commit.

---

### Task 6: Final verification for the slice

**Files:**
- Verify only; no planned file modifications.

- [ ] **Step 1: Run docs surface tests**

Run:

```bash
.venv/bin/pytest tests/test_docs_surface.py
```

Expected: all tests pass.

- [ ] **Step 2: Run strict docs build**

Run:

```bash
.venv/bin/mkdocs build --strict
```

Expected: build succeeds.

- [ ] **Step 3: Check whitespace in touched files**

Run:

```bash
git diff --check HEAD~5..HEAD
```

Expected: no output.

- [ ] **Step 4: Inspect final status without disturbing unrelated work**

Run:

```bash
git status --short
```

Expected: only pre-existing unrelated files remain modified, or working tree is clean if no unrelated edits exist.

- [ ] **Step 5: Report completion**

Report:

- commits created;
- tests/build results;
- files added/modified;
- remaining publisher-readiness work not covered by this first slice.
```
