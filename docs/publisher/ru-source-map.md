# Source map русской издательской рукописи

Status: рабочая карта сборки. Репозиторий остается источником правды, Google Doc
является издательским представлением рукописи.

Google Doc:

- `Архитектура безопасных ИИ-агентов`
- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

## Правило чтения карты

- `Печатная глава` соответствует договорному плану-проспекту от 15 мая 2026 года.
- `Основные источники` указывают Markdown-файлы, из которых собирается глава.
- `Companion boundary` фиксирует материал, который не должен утяжелять печатную
  рукопись и остается в online companion.
- В Google Doc переносится редакционная версия главы, а не весь web-текст один к
  одному.

## Введение

Печатный блок: **Введение**.

Основные источники:

- `docs/index.md`
- `docs/start-here.md`
- `docs/book/index.md`
- `docs/book/plan.md`
- `docs/appendix/why-this-book.md`

Редакторская задача:

- объяснить, для кого книга;
- зафиксировать тезис "agent is not a prompt trick, but a production system";
- кратко объяснить маршрут чтения;
- отделить книгу от framework tutorial и vendor manual.

Companion boundary:

- длинную навигацию сайта оставить online;
- подробные статусы локализаций оставить в web-версии.

## Часть I. От demo-агента к платформе

### Глава 1. Почему агенту нужна платформа, а не магия

Основной источник:

- `docs/book/part-i/chapter-1.md`

Роль:

- первый редакционный sample;
- тезис всей книги;
- вход через failure story и правило выбора формы исполнения.
- статус: первая русская издательская line edit применена в source и
  синхронизирована в Google Doc 2026-06-13.

Companion boundary:

- Mermaid-блок заменить печатным текстовым дублем или редакторской схемой;
- внутренние web-admonitions превратить в обычные врезки или prose.

### Глава 2. Когда нужен агент: workflow, single-agent, multi-agent

Основные источники:

- часть `docs/book/part-i/chapter-1.md`
- `docs/book/part-i/practical-routines.md`
- `docs/book/part-i/practical-manager-handoffs.md`

Роль:

- собрать правило выбора между рабочим процессом, одиночным агентным циклом и
  многоагентной схемой;
- объяснить инструкции, сценарии, шаблоны запросов, координатора и передачу
  управления как инженерные решения, а не как taxonomy.

Companion boundary:

- длинные decision tables и дополнительные routings оставить online.

### Глава 3. Референсная архитектура безопасной агентной системы

Основные источники:

- `docs/book/part-i/chapter-2.md`
- `docs/book/part-ii/chapter-3.md`

Роль:

- показать базовую архитектуру через identity, policy, memory, tool gateway,
  telemetry и ownership;
- связать архитектурные слои с провалами из первой главы.

Companion boundary:

- полные схемы контрактов и runtime walk-through оставить в приложениях и
  companion.

## Часть II. Безопасность и контур управления

### Глава 4. Контур безопасности и границы доверия

Основные источники:

- `docs/book/part-ii/chapter-3.md`

Роль:

- провести границы между пользовательскими данными, trusted instructions,
  retrieved context, tool inputs и write path.

Companion boundary:

- подробные threat worksheets оставить в companion.

### Глава 5. Identity, session, policy layer и capability model

Основные источники:

- часть `docs/book/part-ii/chapter-3.md`
- `docs/book/part-vii/chapter-17.md`
- `docs/appendix/policy-bundle-schema.md`
- `docs/appendix/lifecycle-artifact-schema.md`

Роль:

- объяснить, кто действует, в какой сессии, с какими правами и через какой
  capability contract.

Companion boundary:

- полные YAML/JSON-схемы оставить online;
- в печати оставить минимальный пример и объяснение решений.

### Глава 6. Инструментальный шлюз, подтверждения и журнал аудита

Основные источники:

- `docs/book/part-ii/chapter-4.md`
- часть `docs/book/part-iv/chapter-8.md`
- `docs/appendix/approval-schema.md`

Роль:

- показать tool gateway, approval gates, audit trail и idempotency evidence как
  контур управления побочными эффектами.

Companion boundary:

- полные approval schema и policy bundle оставить online.

## Часть III. Память, знания и контекст

### Глава 7. Зачем агенту память и почему она опасна

Основные источники:

- `docs/book/part-iii/chapter-5.md`

Роль:

- объяснить, почему память является управляемым состоянием и поверхностью риска.

Companion boundary:

- дополнительные сценарии poisoning и review fields оставить online.

### Глава 8. Краткосрочная, долгосрочная и профильная память

Основные источники:

- `docs/book/part-iii/chapter-6.md`
- `docs/appendix/memory-retrieval-schema.md`

Роль:

- разделить виды памяти, provenance, правила записи и очистки.

Companion boundary:

- полный schema contract оставить online.

### Глава 9. Извлечение контекста, уплотнение и фоновые обновления

Основные источники:

- `docs/book/part-iii/chapter-7.md`

Роль:

- показать retrieval, compaction, freshness и background updates как
  контролируемый слой качества.

Companion boundary:

- длинные retrieval policy templates оставить online.

## Часть IV. Инструменты, выполнение и интеграция

### Глава 10. Модель выполнения и каталог инструментов

Основные источники:

- `docs/book/part-iv/chapter-8.md`

Роль:

- объяснить execution loop, tool catalog, tool contracts и разделение read/decide/act.

Companion boundary:

- полный каталог инструментов и runtime output оставить online.

### Глава 11. Песочница выполнения и MCP как интеграционный контракт

Основные источники:

- `docs/book/part-iv/chapter-9.md`
- `docs/book/part-iv/practical-mcp-a2a.md`

Роль:

- объяснить sandbox, MCP boundary и A2A trust contract.

Companion boundary:

- protocol-level examples и длинные integration notes оставить online.

### Глава 12. Идемпотентность, повторы, лимиты и границы отката

Основные источники:

- `docs/book/part-iv/chapter-10.md`
- `docs/appendix/tool-failure-recovery.md`

Роль:

- связать retries, rate limits, rollback boundaries и failure recovery с
  безопасным выполнением инструментов.

Companion boundary:

- recovery pattern catalog оставить online.

## Часть V. Надежность, наблюдаемость и оценки

### Глава 13. Трассы, спаны и структурированные события

Основные источники:

- `docs/book/part-v/chapter-11.md`
- `docs/appendix/trace-schema.md`

Роль:

- объяснить trace/span/event как доказательную модель запуска агента.

Companion boundary:

- полный trace schema и event catalog оставить online.

### Глава 14. SLO для агентных систем

Основные источники:

- `docs/book/part-v/chapter-12.md`

Роль:

- показать health budgets, degraded paths и operational SLO для агентных систем.

Companion boundary:

- расширенные метрики и таблицы оставить online, если они мешают печатному ритму.

### Глава 15. Офлайн- и онлайн-оценки и регрессионные шлюзы

Основные источники:

- `docs/book/part-v/chapter-13.md`
- `docs/appendix/eval-schema.md`

Роль:

- второй технический sample;
- связать наборы оценок, выводы проверяющего, регрессионные шлюзы и релизное
  суждение;
- статус: первая русская издательская line edit применена в source 2026-06-13.

Companion boundary:

- полную схему оценок, наборы данных и validation errors оставить online.

### Глава 16. Сквозная цепочка доказательств: от запроса к rollout

Основные источники:

- `docs/book/part-v/evidence-spine.md`
- часть `docs/appendix/change-rollout-schema.md`

Роль:

- собрать end-to-end evidence chain от запроса к решению о выпуске.

Companion boundary:

- подробные rollout gate schemas оставить online.

## Часть VI. Организационная модель и жизненный цикл

### Глава 17. Платформенная команда и продуктовые команды

Основные источники:

- `docs/book/part-vi/chapter-14.md`

Роль:

- объяснить ownership model между platform team и product teams.

Companion boundary:

- организационные worksheets оставить online.

### Глава 18. Golden paths, общие шлюзы и борьба с агентным зоопарком

Основные источники:

- `docs/book/part-vi/chapter-15.md`

Роль:

- показать, как организация избегает множества несовместимых агентных стеков.

Companion boundary:

- длинные governance checklists оставить online.

### Глава 19. От SDLC к ADLC: жизненный цикл агентной системы

Основные источники:

- `docs/book/part-viii/chapter-19.md`
- `docs/book/part-viii/chapter-20.md`
- `docs/appendix/change-rollout-schema.md`

Роль:

- объяснить ADLC, change-bearing systems и release review для агентных систем.

Companion boundary:

- полные change-review forms оставить online.

### Глава 20. Assurance loop, incident response, registry и retirement

Основные источники:

- `docs/book/part-viii/chapter-21.md`
- `docs/book/part-viii/chapter-22.md`
- `docs/book/part-viii/chapter-23.md`
- `docs/book/part-viii/chapter-26.md`
- `docs/book/part-viii/chapter-27.md`
- `docs/appendix/incident-response-playbook.md`
- `docs/appendix/registry-operations-handbook.md`
- `docs/appendix/incident-record-schema.md`

Роль:

- сжать поздний lifecycle material в одну печатную главу про assurance,
  response, registry, inventory и retirement.

Companion boundary:

- полные playbooks, schemas, registry handbooks и operational templates оставить online.

## Часть VII. Эталонная реализация и промышленный запуск

### Глава 21. Базовая схема runtime

Основные источники:

- `docs/book/part-vii/chapter-16.md`
- `agent_runtime_ref/README.md`

Роль:

- дать minimal runtime blueprint без превращения главы в CLI manual.

Companion boundary:

- runnable package walkthrough, команды и полный output оставить online.

### Глава 22. Слой политик и каталог возможностей

Основные источники:

- `docs/book/part-vii/chapter-17.md`
- `agent_runtime_ref/configs/policy.yaml`
- `agent_runtime_ref/configs/capabilities.yaml`

Роль:

- показать policy layer и capability catalog как исполнимый контрольный слой.

Companion boundary:

- полные config contracts оставить online.

### Глава 23. Чеклист промышленного запуска

Основные источники:

- `docs/book/part-vii/chapter-18.md`
- `docs/appendix/policy-templates.md`
- `docs/appendix/cheat-sheets.md`

Роль:

- дать production launch checklist как финальную практическую рамку.

Companion boundary:

- длинные чеклисты и шаблоны оставить online; в печати оставить критерии решения.

## Приложения

### Приложение 1. Глоссарий

Основной источник:

- `docs/appendix/glossary.md`

Companion boundary:

- web-only glossary expansions можно оставить online.

### Приложение 2. Чеклисты

Основные источники:

- `docs/appendix/cheat-sheets.md`
- `docs/appendix/policy-templates.md`

Companion boundary:

- длинные worksheets оставить online.

### Приложение 3. Шаблон incident/postmortem

Основные источники:

- `docs/appendix/postmortem-template.md`
- `docs/appendix/incident-record-schema.md`

Companion boundary:

- schema fields оставить online; в печати дать форму и объяснение.

### Приложение 4. Источники и online companion

Основные источники:

- `docs/appendix/sources.md`
- `docs/appendix/reference-package.md`
- `docs/reference.md`

Companion boundary:

- полный source catalog может остаться online; в печати нужен curated source list.
