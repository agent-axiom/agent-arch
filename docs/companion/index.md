# Online companion

Online companion хранит материалы, которые должны быть версионируемыми, проверяемыми и обновляемыми отдельно от печатной рукописи.

В книге остаются аргумент, критерии решений и минимальные формы контрактов. Здесь остаются полные CLI-проходы, runtime configs, trace/event catalogs, eval datasets, источники и справочные walkthrough.

## Основные маршруты

- [Runtime configs and MCP boundary](runtime-reference/configs.md)
- [Runtime CLI](runtime-reference/cli.md)
- [Eval datasets](runtime-reference/eval-datasets.md)
- [Traces and events](runtime-reference/traces-and-events.md)
- [Templates](templates/index.md)
- [Checklists](checklists/index.md)
- [Changelog](changelog.md)
- [Errata](errata.md)
- Example artifacts:
  `artifacts/trace-demo.jsonl`,
  `artifacts/trace-failed-tool-timeout.jsonl`,
  `artifacts/trace-post-dispatch-timeout.jsonl`,
  `artifacts/session-failed-tool-timeout.json`,
  `artifacts/eval-failed-run-timeout.json`,
  `artifacts/eval-unknown-effect-reconciliation.json`
- Filled examples:
  `examples/capability-contract-support-ticket.md`,
  `examples/release-decision-record-support-ticket.md`,
  `examples/incident-record-support-ticket-timeout.md`,
  `examples/production-readiness-support-ticket.md`,
  `examples/context-manifest-support-ticket.yaml`,
  `examples/threat-map-negative-tests.yaml`,
  `examples/slo-card-support-ticket.yaml`,
  `examples/adlc-transition-support-ticket.yaml`,
  `examples/readiness-rubric-support-ticket.yaml`
- [Полный reference package walkthrough](../appendix/reference-package.md)
- [Полный список источников](../appendix/sources.md)

## Практика по безопасному агенту

Если читатель хочет не только читать, но и повторять материал руками, основной вход — [полный reference package walkthrough](../appendix/reference-package.md). Там главы связаны с файлами `agent_runtime_ref`, командами CLI, companion artifacts и тестами. Минимальная линия практики: `inspect-agent` для инвентаря, `simulate-run` для управляемого запуска, `dump-events`/`inspect-trace` для доказательств, `inspect-approvals` для человеческого шлюза, `export-eval-dataset` для оценок и `check-rollout`/`check-controls` для решения о выпуске.

## Что должно жить здесь

- Полные YAML-конфиги и review forms.
- CLI-команды и ожидаемые JSON-поверхности.
- Trace/event catalogs и validation-message catalogs.
- Eval datasets, verifier contracts и rollout judgment examples.
- Длинные source catalogs, changelog, errata и правила обновления.

## Что должно оставаться в книге

- Почему архитектурное решение нужно.
- Какой риск оно закрывает.
- Кто владеет действием и доказательствами.
- Как команда понимает, что runtime, policy, trace, eval gate и rollout готовы.

## Chapter map {#chapter-map}

Карта связывает номер печатной главы с тематическим разделом электронной книги
и ближайшим исполняемым или справочным материалом. Названия ссылок важнее
внутренней нумерации сайта: при перестройке онлайн-книги читатель по-прежнему
ищет тему и проверяемый артефакт, а не «главу с тем же номером».

| Печатная глава | Онлайн-раздел | Практика и справочник |
| ---: | --- | --- |
| 1 | [Почему агенту нужна платформа](../book/part-i/chapter-1.md) | [Эталонный пакет](../appendix/reference-package.md) |
| 2 | [Формы выполнения](../book/part-i/chapter-2.md), [координатор и передача управления](../book/part-i/practical-manager-handoffs.md) | [Практические схемы запросов](../book/part-i/practical-routines.md) |
| 3 | [Архитектура безопасного агента](../book/part-i/chapter-2.md) | [Карта технологического стека](../appendix/stack.md) |
| 4 | [Границы доверия](../book/part-ii/chapter-3.md) | [Шаблоны политик](../appendix/policy-templates.md) |
| 5 | [Слой политик и каталог возможностей](../book/part-vii/chapter-17.md) | [Схема набора политик](../appendix/policy-bundle-schema.md) |
| 6 | [Шлюз инструментов и подтверждения](../book/part-ii/chapter-4.md) | [Схема подтверждения](../appendix/approval-schema.md) |
| 7 | [Риски памяти](../book/part-iii/chapter-5.md) | [Сценарии оценки памяти](../appendix/memory-eval-patterns.md) |
| 8 | [Виды и жизненный цикл памяти](../book/part-iii/chapter-6.md) | [Схема извлечения памяти](../appendix/memory-retrieval-schema.md) |
| 9 | [Извлечение и уплотнение контекста](../book/part-iii/chapter-7.md) | [Конверт непрерывности](../appendix/continuity-envelope-schema.md) |
| 10 | [Модель выполнения и инструменты](../book/part-iv/chapter-8.md) | [Справочник конфигураций](runtime-reference/configs.md) |
| 11 | [Песочница и MCP](../book/part-iv/chapter-9.md), [граница MCP и A2A](../book/part-iv/practical-mcp-a2a.md) | [Восстановление после отказов инструментов](../appendix/tool-failure-recovery.md) |
| 12 | [Повторы, лимиты и откат](../book/part-iv/chapter-10.md) | [Восстановление после отказов инструментов](../appendix/tool-failure-recovery.md) |
| 13 | [Трассы и события](../book/part-v/chapter-11.md) | [Каталог трасс и событий](runtime-reference/traces-and-events.md) |
| 14 | [SLO агентных систем](../book/part-v/chapter-12.md) | [Заполненная карточка SLO](examples/slo-card-support-ticket.yaml) |
| 15 | [Оценки и регрессионные шлюзы](../book/part-v/chapter-13.md) | [Наборы оценок](runtime-reference/eval-datasets.md) |
| 16 | [Сквозная цепочка доказательств](../book/part-v/evidence-spine.md) | [Схема проверки изменений и выпуска](../appendix/change-rollout-schema.md) |
| 17 | [Платформенная и продуктовые команды](../book/part-vi/chapter-14.md) | [Шаблон контракта возможности](templates/capability-contract.md) |
| 18 | [Поддерживаемые стандартные пути](../book/part-vi/chapter-15.md) | [Заполненный контракт стандартного пути](examples/capability-contract-support-ticket.md) |
| 19 | [Инвентаризация и реестр агентов](../book/part-viii/chapter-27.md) | [Руководство по работе с реестром](../appendix/registry-operations-handbook.md) |
| 20 | [Переход от SDLC к ADLC](../book/part-viii/chapter-19.md), [управление изменениями](../book/part-viii/chapter-20.md) | [Пример перехода ADLC](examples/adlc-transition-support-ticket.yaml) |
| 21 | [Происхождение и доверенные артефакты](../book/part-viii/chapter-22.md) | [Схема артефактов жизненного цикла](../appendix/lifecycle-artifact-schema.md) |
| 22 | [Наблюдаемость и телеметрия обнаружения](../book/part-viii/chapter-26.md) | [Схема трасс](../appendix/trace-schema.md) |
| 23 | [Несоответствие целей и внутренний риск](../book/part-viii/chapter-24.md), [поведенческие оценки](../book/part-viii/chapter-25.md) | [Отрицательные сценарии модели угроз](examples/threat-map-negative-tests.yaml) |
| 24 | [Заверение и реагирование](../book/part-viii/chapter-21.md) | [Плейбук реагирования](../appendix/incident-response-playbook.md) |
| 25 | [Вывод из эксплуатации и замена](../book/part-viii/chapter-23.md) | [Схема артефактов жизненного цикла](../appendix/lifecycle-artifact-schema.md) |
| 26 | [Базовая среда исполнения](../book/part-vii/chapter-16.md) | [Справочник команд](runtime-reference/cli.md) |
| 27 | [Политики и каталог возможностей](../book/part-vii/chapter-17.md) | [Исполняемые сценарии политики траектории](examples/trajectory-policy-scenarios.md) |
| 28 | [Проверочный список промышленного запуска](../book/part-vii/chapter-18.md) | [Проверка готовности к промышленной эксплуатации](checklists/production-readiness.md) |
