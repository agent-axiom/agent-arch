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
