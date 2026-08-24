# Source map русской издательской рукописи

Status: карта источников обновлена 2026-08-24. Показатели и производные ниже
относятся к указанным для них контрольным точкам. Репозиторий остается
источником правды, Google Doc является издательским представлением рукописи.

Канонический Markdown:

- редактируемый снимок рукописи:
  `docs/publisher/ru-manuscript-google-doc-final-2026-07-11.md`;
- детерминированная редакционная сборка:
  `docs/publisher/ru-manuscript-editorial-2026-07-13.md`;
- сборщик и манифест схем:
  `docs/publisher/tools/revise_ru_manuscript.py` и
  `docs/publisher/ru-inline-diagrams-2026-07-13.json`;
- манифест двух дополнительных редакционных схем:
  `docs/publisher/ru-editorial-diagrams-2026-07-16.json`.

Текущее покрытие рукописи:

- 8 частей и 28 глав;
- 25 пронумерованных рисунков, 29 встроенных схем, 2 дополнительные
  редакционные схемы и QR-код, всего 57 изображений;
- 8 лабораторных работ и итоговый проект;
- 12 таблиц в канонической и локальных издательских производных;
- около 95 790 слов по метрике издательской сборки;
- 539 страниц в Google-ориентированной производной и 380 страниц в
  производной `Template2000n`; разница вызвана типографикой и плотностью
  стилей, а не сокращением содержания; пустых технических страниц нет.

Google Doc:

- `Архитектура безопасных ИИ-агентов`
- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>
- финальная проверенная ревизия:
  `AIroW376Mm-00rajnQTmtP30M3vDHmLKcS_ervRFIl6HzuaLjNH2UGFCUaBnBf7lwwg4R87M76B0D28Dvib0sCwAHao64RbBYsnf3_rPcb4`;
- точка отката перед синхронизацией 2026-08-24:
  `AIroW36GxTgBw_-2lk3M1lIHnOC-PMQE8n39bTG3myEzMMoUOddC3k9CtHntZD4t3e9FhxMbqmx6PaxnnSHpOskKnJf_nyQ__LdGkxvsjoA`.

Контрольная точка книжных стандартов и политики траекторий:

- текст существующего Google Doc синхронизирован с производной
  `agent-arch-ru-google-doc-book-standards-2026-08-23.docx`;
- после удаления двух обнаруженных при чтении дубликатов последовательность
  всех 8771 непустых абзацев совпадает с DOCX, а тексты всех 12 таблиц
  совпадают ячейка к ячейке;
- в документе сохранены 57 встроенных изображений; у каждого есть название,
  альтернативное описание и URI источника;
- отдельная резервная копия не создавалась: защитный контур коннектора отклонил
  дополнительное копирование частной рукописи, поэтому точкой отката служит
  указанная выше ревизия и встроенная история версий Google Docs;
- итоговый отчёт:
  `docs/publisher/ru-book-standards-and-trajectory-policy-pass-2026-08-24.md`.

Контрольная точка Mermaid-синхронизации:

- 56 схем и рисунков пересозданы в существующем Google Doc без изменения
  порядка и текстовых индексов; вместе с QR-кодом документ содержит 57
  изображений;
- размеры изображений перенесены из проверенной Google-ориентированной
  DOCX-производной без принудительной обрезки;
- неизменяемый источник изображений: коммит
  `8d2d014e0174297b56195182b14451545902f430`;
- резервная копия перед синхронизацией:
  <https://docs.google.com/document/d/1mBlWXweSzfQ8BhVgOSddPckFpL7M1q-gsLmROuMj8xA>;
- отчёт: `docs/publisher/ru-google-doc-mermaid-sync-2026-08-02.md`.

Контрольная точка повторной редакционной полировки:

- `docs/publisher/ru-technical-book-polish-pass-2026-08-02.md`;
- `docs/publisher/ru-technical-book-polish-pass-2026-08-02.manifest.json`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-technical-book-polish-2026-08-02.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-technical-book-polish-2026-08-02.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-technical-book-polish-2026-08-02.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-technical-book-polish-2026-08-02.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-technical-book-polish-2026-08-02.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-technical-book-polish-2026-08-02.pdf`.

Контрольная точка читательского прохода:

- `docs/publisher/ru-reader-experience-pass-2026-08-01.md`;
- `docs/publisher/ru-reader-experience-pass-2026-08-01.manifest.json`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-reader-experience-2026-08-01.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-reader-experience-2026-08-01.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-reader-experience-2026-08-01.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-reader-experience-2026-08-01.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-reader-experience-2026-08-01.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-reader-experience-2026-08-01.pdf`.

Контрольная точка редакционного прохода:

- `docs/publisher/ru-editorial-pass-2026-08-01.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-pass-2026-08-01.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-pass-2026-08-01.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-pass-2026-08-01.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-pass-2026-08-01.pdf`;
- `docs/publisher/ru-google-doc-editorial-pass-2026-08-01.render-qa.json`;
- `docs/publisher/ru-template2000n-editorial-pass-2026-08-01.render-qa.json`;
- `docs/publisher/ru-template2000n-editorial-pass-2026-08-01.visual-audit.json`;
- `docs/publisher/ru-template2000n-editorial-pass-2026-08-01.font-audit.json`.

Контрольная точка синхронизации с актуальной онлайн-книгой:

- `docs/publisher/ru-online-manuscript-sync-2026-07-29.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-online-sync-2026-07-29.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-online-sync-2026-07-29.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-online-sync-2026-07-29.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-online-sync-2026-07-29.pdf`;
- `docs/publisher/ru-google-doc-online-sync-2026-07-29.render-qa.json`;
- `docs/publisher/ru-template2000n-online-sync-2026-07-29.render-qa.json`;
- `docs/publisher/ru-template2000n-online-sync-2026-07-29.visual-audit.json`;
- `docs/publisher/ru-template2000n-online-sync-2026-07-29.font-audit.json`.

Контрольная точка редакционной полировки технической книги:

- `docs/publisher/ru-technical-book-polish-2026-07-27.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-technical-book-polish-2026-07-27.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-technical-book-polish-2026-07-27.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-technical-book-polish-2026-07-27.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-technical-book-polish-2026-07-27.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-technical-book-polish-2026-07-27.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-technical-book-polish-2026-07-27.pdf`;
- `docs/publisher/ru-index-terms-2026-07-27.md`;
- `docs/publisher/ru-learning-outcome-map-2026-07-27.md`;
- `docs/publisher/ru-human-review-packet-2026-07-27.md`.

Контрольная точка финальной читательской редактуры:

- `docs/publisher/ru-final-reader-copyedit-2026-07-23.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-final-reader-copyedit-2026-07-23.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-final-reader-copyedit-2026-07-23.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-final-reader-copyedit-2026-07-23.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-final-reader-copyedit-2026-07-23.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-final-reader-copyedit-2026-07-23.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-final-reader-copyedit-2026-07-23.pdf`;
- `docs/publisher/ru-google-doc-live-final-reader-copyedit-2026-07-23.render.json`;
- `docs/publisher/ru-google-doc-final-reader-copyedit-2026-07-23.render.json`;
- `docs/publisher/ru-template2000n-final-reader-copyedit-2026-07-23.render.json`.

Контрольная точка синхронизации управляемого поиска возможностей и общего
шлюза ИИ:

- `docs/publisher/ru-gateway-discovery-sync-pass-2026-07-22.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-online-sync-2026-07-22.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-online-sync-2026-07-22.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-online-sync-2026-07-22.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-online-sync-2026-07-22.pdf`;
- `docs/publisher/ru-google-doc-online-sync-visual-audit-2026-07-22.json`;
- `docs/publisher/ru-template2000n-online-sync-visual-audit-2026-07-22.json`.

Контрольная точка готовности к издательской передаче:

- `docs/publisher/ru-submission-readiness-pass-2026-07-22.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-submission-readiness-2026-07-22.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-live-submission-readiness-2026-07-22.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-submission-readiness-2026-07-22.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-submission-readiness-2026-07-22.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-submission-readiness-2026-07-22.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-submission-readiness-2026-07-22.pdf`;
- `docs/publisher/ru-google-doc-live-submission-readiness-visual-audit-2026-07-22.json`.

Контрольная точка развивающей редактуры:

- `docs/publisher/ru-developmental-editing-pass-2026-07-20.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-developmental-edit-2026-07-20.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-developmental-edit-2026-07-20.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-developmental-edit-2026-07-20.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-developmental-edit-2026-07-20.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-synced-developmental-edit-2026-07-20.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-synced-developmental-edit-2026-07-20.pdf`.

Контрольная точка редакторской переработки:

- `docs/publisher/ru-technical-book-best-practices-pass-2026-07-17.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-2026-07-17.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-2026-07-17.pdf`.

Контрольная точка проходки по читательскому маршруту:

- `docs/publisher/ru-technical-book-best-practices-audit-2026-07-17.md`;
- `docs/publisher/ru-reader-journey-best-practices-pass-2026-07-17.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-reader-journey-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-reader-journey-2026-07-17.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-reader-journey-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-reader-journey-2026-07-17.pdf`.

Контрольная точка проходки по стандартам технической литературы:

- `docs/publisher/ru-technical-book-standards-pass-2026-07-17.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-technical-standards-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-technical-standards-2026-07-17.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-technical-standards-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-technical-standards-2026-07-17.pdf`.

Контрольная точка проходки по читательскому качеству технической книги:

- `docs/publisher/ru-bookcraft-readability-pass-2026-07-17.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-bookcraft-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-bookcraft-2026-07-17.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-bookcraft-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-bookcraft-2026-07-17.pdf`.

Контрольная точка финальной проходки по читательской архитектуре:

- `docs/publisher/ru-advanced-bookcraft-final-polish-2026-07-17.md`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-final-polish-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-google-doc-editorial-final-polish-2026-07-17.pdf`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-final-polish-2026-07-17.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-final-polish-2026-07-17.pdf`.

## Правило чтения карты

- `Печатная глава` соответствует договорному плану-проспекту от 15 мая 2026 года.
- `Основные источники` указывают Markdown-файлы, из которых собирается глава.
- `Граница онлайн-приложения` фиксирует материал, который не должен утяжелять
  печатную рукопись и остается в онлайн-приложении.
- В Google Doc переносится редакционная версия главы, а не весь веб-текст один к
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
- зафиксировать тезис "агент - это не трюк с запросом, а промышленная система";
- кратко объяснить маршрут чтения;
- отделить книгу от учебника по программному каркасу и руководства поставщика.

Граница онлайн-приложения:

- длинную навигацию сайта оставить в онлайн-приложении;
- подробные статусы локализаций оставить в веб-версии.

## Часть I. От демо-агента к платформе

### Глава 1. Почему агенту нужна платформа, а не магия

Основной источник:

- `docs/book/part-i/chapter-1.md`

Роль:

- первый редакционный образец;
- тезис всей книги;
- вход через историю отказа и правило выбора формы исполнения.
- статус: первая русская издательская построчная правка применена в источнике и
  синхронизирована в Google Doc 2026-06-13.

Граница онлайн-приложения:

- Mermaid-блок заменить печатным текстовым дублем или редакторской схемой;
- внутренние веб-врезки превратить в обычные врезки или прозу.

### Глава 2. Когда нужен агент: рабочий процесс, одиночный агентный цикл, многоагентная схема

Основные источники:

- часть `docs/book/part-i/chapter-1.md`
- `docs/book/part-i/practical-routines.md`
- `docs/book/part-i/practical-manager-handoffs.md`

Роль:

- собрать правило выбора между рабочим процессом, одиночным агентным циклом и
  многоагентной схемой;
- объяснить инструкции, сценарии, шаблоны запросов, координатора и передачу
  управления как инженерные решения, а не как таксономию.

Граница онлайн-приложения:

- длинные таблицы решений и дополнительные схемы маршрутизации оставить в
  онлайн-приложении.

### Глава 3. Референсная архитектура безопасной агентной системы

Основные источники:

- `docs/book/part-i/chapter-2.md`
- `docs/book/part-ii/chapter-3.md`

Роль:

- показать базовую архитектуру через идентичность, политики, память,
  инструментальный шлюз, телеметрию и владение;
- связать архитектурные слои с провалами из первой главы.

Граница онлайн-приложения:

- полные схемы контрактов и пошаговый разбор среды исполнения оставить в
  приложениях и онлайн-приложении.

## Часть II. Безопасность и контур управления

### Глава 4. Контур безопасности и границы доверия

Основные источники:

- `docs/book/part-ii/chapter-3.md`

Роль:

- провести границы между пользовательскими данными, доверенными инструкциями,
  извлеченным контекстом, входами инструментов и путем записи.

Граница онлайн-приложения:

- подробные рабочие листы модели угроз оставить в онлайн-приложении.

### Глава 5. Идентичность, сессия, слой политик и модель возможностей

Основные источники:

- часть `docs/book/part-ii/chapter-3.md`
- `docs/book/part-vii/chapter-17.md`
- `docs/appendix/policy-bundle-schema.md`
- `docs/appendix/lifecycle-artifact-schema.md`

Роль:

- объяснить, кто действует, в какой сессии, с какими правами и через какой
  контракт возможностей.

Граница онлайн-приложения:

- полные YAML/JSON-схемы оставить в онлайн-приложении;
- в печати оставить минимальный пример и объяснение решений.

### Глава 6. Инструментальный шлюз, подтверждения и журнал аудита

Основные источники:

- `docs/book/part-ii/chapter-4.md`
- часть `docs/book/part-iv/chapter-8.md`
- `docs/appendix/approval-schema.md`

Роль:

- показать инструментальный шлюз, шлюзы подтверждения, журнал аудита и
  доказательства идемпотентности как контур управления побочными эффектами.

Граница онлайн-приложения:

- полные схемы подтверждений и набор политик оставить в онлайн-приложении.

## Часть III. Память, знания и контекст

### Глава 7. Зачем агенту память и почему она опасна

Основные источники:

- `docs/book/part-iii/chapter-5.md`

Роль:

- объяснить, почему память является управляемым состоянием и поверхностью риска.

Граница онлайн-приложения:

- дополнительные сценарии отравления и поля проверки оставить в
  онлайн-приложении.

### Глава 8. Краткосрочная, долгосрочная и профильная память

Основные источники:

- `docs/book/part-iii/chapter-6.md`
- `docs/appendix/memory-retrieval-schema.md`

Роль:

- разделить виды памяти, происхождение, правила записи и очистки.

Граница онлайн-приложения:

- полный контракт схемы оставить в онлайн-приложении.

### Глава 9. Извлечение контекста, уплотнение и фоновые обновления

Основные источники:

- `docs/book/part-iii/chapter-7.md`

Роль:

- показать извлечение, уплотнение, свежесть и фоновые обновления как
  контролируемый слой качества.

Граница онлайн-приложения:

- длинные шаблоны политик извлечения оставить в онлайн-приложении.

## Часть IV. Инструменты, выполнение и интеграция

### Глава 10. Модель выполнения и каталог инструментов

Основные источники:

- `docs/book/part-iv/chapter-8.md`

Роль:

- объяснить цикл выполнения, каталог инструментов, контракты инструментов и
  разделение "прочитать / решить / действовать".

Граница онлайн-приложения:

- полный каталог инструментов и вывод среды исполнения оставить в
  онлайн-приложении.

### Глава 11. Песочница выполнения и MCP как интеграционный контракт

Основные источники:

- `docs/book/part-iv/chapter-9.md`
- `docs/book/part-iv/practical-mcp-a2a.md`

Роль:

- объяснить песочницу, границу MCP и контракт доверия A2A.

Граница онлайн-приложения:

- примеры уровня протокола и длинные интеграционные заметки оставить в
  онлайн-приложении.

### Глава 12. Идемпотентность, повторы, лимиты и границы отката

Основные источники:

- `docs/book/part-iv/chapter-10.md`
- `docs/appendix/tool-failure-recovery.md`

Роль:

- связать повторы, лимиты запросов, границы отката и восстановление после
  отказов с безопасным выполнением инструментов.

Граница онлайн-приложения:

- каталог паттернов восстановления оставить в онлайн-приложении.

## Часть V. Надежность, наблюдаемость и оценки

### Глава 13. Трассы, спаны и структурированные события

Основные источники:

- `docs/book/part-v/chapter-11.md`
- `docs/appendix/trace-schema.md`

Роль:

- объяснить trace/span/event как доказательную модель запуска агента.

Граница онлайн-приложения:

- полную схему трассировки и каталог событий оставить в онлайн-приложении.

### Глава 14. SLO для агентных систем

Основные источники:

- `docs/book/part-v/chapter-12.md`

Роль:

- показать health budgets, degraded paths и operational SLO для агентных систем.

Граница онлайн-приложения:

- расширенные метрики и таблицы оставить в онлайн-приложении, если они мешают
  печатному ритму.

### Глава 15. Офлайн- и онлайн-оценки и регрессионные шлюзы

Основные источники:

- `docs/book/part-v/chapter-13.md`
- часть `docs/book/part-viii/chapter-25.md`
- `docs/appendix/eval-schema.md`

Роль:

- второй технический образец;
- связать наборы оценок, выводы проверяющего, регрессионные шлюзы и релизное
  суждение;
- добавить контрольные оценки и автоматизированное соревновательное
  тестирование как проверку контура управления, а не только итогового ответа;
- статус: первая русская издательская построчная правка применена в источнике
  2026-06-13.

Граница онлайн-приложения:

- полную схему оценок, наборы данных и ошибки валидации оставить в
  онлайн-приложении.

### Глава 16. Сквозная цепочка доказательств: от запроса к поэтапному выпуску

Основные источники:

- `docs/book/part-v/evidence-spine.md`
- часть `docs/appendix/change-rollout-schema.md`

Роль:

- собрать сквозную доказательную цепочку от запроса к решению о выпуске.

Граница онлайн-приложения:

- подробные схемы шлюзов поэтапного выпуска оставить в онлайн-приложении.

## Часть VI. Организационная модель и жизненный цикл

### Глава 17. Платформенная команда и продуктовые команды

Основные источники:

- `docs/book/part-vi/chapter-14.md`

Роль:

- объяснить модель владения между платформенной командой и продуктовыми
  командами.

Граница онлайн-приложения:

- организационные рабочие листы оставить в онлайн-приложении.

### Глава 18. Поддерживаемые стандартные пути, общие шлюзы и борьба с агентным зоопарком

Основные источники:

- `docs/book/part-vi/chapter-15.md`

Роль:

- показать, как организация избегает множества несовместимых агентных стеков.

Граница онлайн-приложения:

- длинные управленческие проверочные списки оставить в онлайн-приложении.

### Глава 19. От SDLC к ADLC: жизненный цикл агентной системы

Основные источники:

- `docs/book/part-viii/chapter-19.md`
- `docs/book/part-viii/chapter-20.md`
- `docs/appendix/change-rollout-schema.md`

Роль:

- объяснить ADLC, системы, несущие изменения, и проверку выпуска для агентных
  систем.

Граница онлайн-приложения:

- полные формы проверки изменений оставить в онлайн-приложении.

### Глава 20. Агентное несоответствие целей и внутренний риск

Основные источники:

- `docs/book/part-viii/chapter-24.md`
- `docs/book/part-viii/chapter-25.md`

Роль:

- показать, как полезная цель может превратиться в обход контроля при уже
  выданных полномочиях;
- связать модель внутреннего риска с подтверждениями, переходными состояниями,
  обнаружением, сдерживанием и регрессионными оценками.

### Глава 21. Контур заверения: соревновательное тестирование, обнаружение и реагирование

Основные источники:

- `docs/book/part-viii/chapter-21.md`
- `docs/appendix/incident-response-playbook.md`
- `docs/appendix/incident-record-schema.md`

Роль:

- превратить находки, жалобы и отклонения поведения в сдерживание, исправление
  и обновление оценок;
- показать путь первых минут инцидента без смешивания его с реестром и выводом
  из эксплуатации.

### Глава 22. Цепочка поставки, происхождение и доверенные артефакты

Основной источник:

- `docs/book/part-viii/chapter-22.md`

Роль:

- связать версии модели, инструкций, корпуса, политик, возможностей и оценок с
  конкретным запуском и решением о выпуске.

### Глава 23. Вывод из эксплуатации, замена и дисциплина завершения жизненного цикла

Основной источник:

- `docs/book/part-viii/chapter-23.md`

Роль:

- закрыть право старой системы действовать, отозвать полномочия и доказать
  завершение замены.

### Глава 24. Наблюдаемость для ИИ-систем и телеметрия обнаружения

Основной источник:

- `docs/book/part-viii/chapter-26.md`

Роль:

- превратить телеметрию из средства отладки в доказательную основу управления,
  обнаружения и выпуска.

### Глава 25. Инвентаризация агентов, реестр и контроль разрастания

Основные источники:

- `docs/book/part-viii/chapter-27.md`
- `docs/appendix/registry-operations-handbook.md`

Роль:

- связать каждый промышленный агент с владельцем, состоянием жизненного цикла,
  покрытием телеметрией и операционным ритмом проверки реестра.

Граница онлайн-приложения:

- полные плейбуки, схемы, руководства по реестру и операционные шаблоны оставить
  в онлайн-приложении.

## Часть VII. Эталонная реализация и промышленный запуск

### Глава 26. Базовая схема среды исполнения

Основные источники:

- `docs/book/part-vii/chapter-16.md`
- `agent_runtime_ref/README.md`

Роль:

- дать минимальную схему среды исполнения без превращения главы в руководство по
  командной строке.

Граница онлайн-приложения:

- пошаговый разбор исполняемого пакета, команды и полный вывод оставить в
  онлайн-приложении.

### Глава 27. Слой политик и каталог возможностей в эталонной реализации

Основные источники:

- `docs/book/part-vii/chapter-17.md`
- `agent_runtime_ref/configs/policy.yaml`
- `agent_runtime_ref/configs/capabilities.yaml`
- `docs/companion/examples/run_trajectory_policy_scenarios.py`
- [AWS, Control agent behaviors and cost beyond a single action: New capabilities in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/control-agent-behaviors-and-cost-beyond-a-single-action-new-capabilities-in-amazon-bedrock-agentcore/)

Роль:

- показать слой политик и каталог возможностей как исполнимый контрольный слой;
- отделить проверку одного вызова от политики всей траектории: связывания
  значений, накопленного бюджета, порядка шагов и подтверждения.

Граница онлайн-приложения:

- полные контракты конфигурации и исполняемые сценарии оставить в
  онлайн-приложении; промышленное распределенное хранилище истории,
  конкурентную фиксацию и восстановление после сбоя не приписывать учебному
  вычислителю решений.

### Глава 28. Проверочный список промышленного запуска

Основные источники:

- `docs/book/part-vii/chapter-18.md`
- `docs/appendix/policy-templates.md`
- `docs/appendix/cheat-sheets.md`

Роль:

- дать проверочный список промышленного запуска как финальную практическую
  рамку.

Граница онлайн-приложения:

- длинные проверочные списки и шаблоны оставить в онлайн-приложении; в печати
  оставить критерии решения.

## Приложения

### Приложение 1. Глоссарий

Основной источник:

- `docs/appendix/glossary.md`

Граница онлайн-приложения:

- расширения глоссария только для сайта можно оставить в онлайн-приложении.

### Приложение 2. Проверочные списки

Основные источники:

- `docs/appendix/cheat-sheets.md`
- `docs/appendix/policy-templates.md`

Граница онлайн-приложения:

- длинные рабочие листы оставить в онлайн-приложении.

### Приложение 3. Шаблон incident/postmortem

Основные источники:

- `docs/appendix/postmortem-template.md`
- `docs/appendix/incident-record-schema.md`

Граница онлайн-приложения:

- поля схем оставить в онлайн-приложении; в печати дать форму и объяснение.

### Приложение 4. Источники и онлайн-приложение

Основные источники:

- `docs/appendix/sources.md`
- `docs/appendix/reference-package.md`
- `docs/reference.md`

Граница онлайн-приложения:

- полный каталог источников может остаться в онлайн-приложении; в печати нужен
  отобранный список источников.

## Визуальная система рукописи

Источники Mermaid:

- `docs/publisher/ru-inline-diagrams-2026-07-13.json`;
- `docs/publisher/ru-numbered-diagrams-2026-07-15.json`;
- `docs/publisher/ru-editorial-diagrams-2026-07-16.json`.

Правила и сборка:

- `docs/publisher/ru-visual-style-guide-2026-08-02.md`;
- `docs/publisher/tools/render_ru_inline_diagrams.mjs`;
- `docs/publisher/tools/revise_ru_manuscript.py`.

Производные SVG и PNG находятся в `docs/publisher/visuals/`. Они не являются
ручными источниками: при изменении смысла сначала исправляется Mermaid, затем
полностью повторяется сборка и контроль размещения в DOCX/PDF.
