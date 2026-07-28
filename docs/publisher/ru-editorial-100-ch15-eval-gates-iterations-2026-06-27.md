# Следующие 100 редакционных итераций

Дата: 2026-06-27

Контекст: после прохода 901-910 глава 15 стала release-decision главой про offline/online evals, regression gates, false pass/false block, override and evidence bundle. Следующий блок должен довести главы 16-23, companion, proof и издательский пакет до редакционной готовности.

## Итерации 1001-1100

| Итерация | Цель | Проверка готовности |
| --- | --- | --- |
| 1001 | Переписать opening главы 16 как продолжение eval gate. | Глава начинается с вопроса о сквозной цепочке доказательств после release verdict. |
| 1002 | Нормализовать evidence chain: request, trace, policy decision, approval, eval verdict, SLO snapshot, rollout gate, incident evidence. | Все сущности названы одним словарем. |
| 1003 | Убрать устаревшие ссылки на неверные номера глав внутри главы 16. | Cross-chapter references соответствуют текущей нумерации. |
| 1004 | Исправить list-style артефакты главы 16 в Template2000n proof. | Переходная страница после главы 15 читается без oversized list markers. |
| 1005 | Добавить minimal identifier set для подозрительного запуска. | Один запуск можно восстановить без произвольного чтения логов. |
| 1006 | Связать evidence chain с override record из главы 15. | Override не теряется после release decision. |
| 1007 | Добавить diagram-free textual chain для печатной версии. | Читатель понимает цепочку без companion. |
| 1008 | Вынести полные schema examples главы 16 в companion. | Печатная глава не превращается в reference dump. |
| 1009 | Добавить readiness checklist главы 16. | Команда может проверить evidence chain перед rollout. |
| 1010 | Экспортировать главу 16 и провести render QA. | Маркеры главы 16/17 найдены, пустых страниц нет. |
| 1011 | Переписать главу 17 вокруг разделения platform/product ownership. | Глава продолжает evidence chain через ответственность команд. |
| 1012 | Развести platform-owned и product-owned artifacts. | Нет смешения ответственности за политику, сценарий и эксплуатацию. |
| 1013 | Добавить owner map для capability lifecycle. | У каждого решения есть владелец и escalation path. |
| 1014 | Связать product metrics с safety gates. | Product не может обойти safety decision. |
| 1015 | Добавить anti-pattern: platform as bottleneck. | Глава объясняет риск чрезмерной централизации. |
| 1016 | Добавить anti-pattern: local agent zoo. | Глава готовит переход к стандартным путям главы 18. |
| 1017 | Вынести RACI-like matrices в companion. | В книге остается принцип и минимальный пример. |
| 1018 | Проверить терминологию owner_role, expected_action, registry owner. | Термины не расходятся с главами 14-16. |
| 1019 | Добавить checklist передачи ownership. | Смена владельца становится проверяемой процедурой. |
| 1020 | Экспортировать главу 17 и провести render QA. | Переход к главе 18 стабилен. |
| 1021 | Переписать главу 18 вокруг supported paths как инструмента управления, а не бюрократии. | Читатель понимает, почему хороший путь должен быть проще обхода. |
| 1022 | Нормализовать понятие common gateway. | Gateway описан как операционный контракт. |
| 1023 | Добавить критерии supported path adoption. | Можно измерить, пользуются ли команды стандартным путем. |
| 1024 | Связать supported paths с eval gates. | Новые пути не обходят главу 15. |
| 1025 | Связать supported paths с registry. | Путь имеет владельца и lifecycle state. |
| 1026 | Убрать повторяющиеся аргументы о зоопарке агентов. | Глава не повторяет platform/product ownership. |
| 1027 | Добавить migration pattern с локальных ботов на платформенный путь. | Есть практический путь улучшения. |
| 1028 | Вынести full gateway configs в companion. | В книге остаются только decision excerpts. |
| 1029 | Добавить checklist стандартного пути. | Читатель может применить главу на ревью. |
| 1030 | Экспортировать главу 18 и провести render QA. | Переход к ADLC не ломается. |
| 1031 | Переписать главу 19 вокруг ADLC как расширения SDLC для агентных изменений. | Глава не звучит как переименование процессов. |
| 1032 | Развести SDLC, MLOps, LLMOps and ADLC. | Читатель видит, что нового добавляет агентный жизненный цикл. |
| 1033 | Добавить change taxonomy: prompt, policy, tool, memory, retrieval, model, workflow. | Изменения классифицируются до gate. |
| 1034 | Связать ADLC с eval gates главы 15. | Каждая категория изменения имеет проверку. |
| 1035 | Связать ADLC с evidence chain главы 16. | Изменение оставляет проверяемый след. |
| 1036 | Добавить emergency change path. | Срочные исправления не обходят audit trail. |
| 1037 | Добавить rollback and retirement hooks. | ADLC включает завершение, а не только выпуск. |
| 1038 | Вынести подробные change templates в companion. | Печатный текст остается читаемым. |
| 1039 | Добавить ADLC readiness checklist. | Готовность процесса можно проверить. |
| 1040 | Экспортировать главу 19 и провести render QA. | ADLC-глава визуально стабильна. |
| 1041 | Переписать главу 20 как assurance loop: incident, registry, retirement. | Глава связывает эксплуатацию и управление жизненным циклом. |
| 1042 | Развести assurance, incident response and audit. | Термины не смешиваются. |
| 1043 | Добавить incident-to-eval feedback loop. | Инцидент возвращается в regression suite. |
| 1044 | Добавить registry-to-runtime enforcement. | Registry не является пассивным каталогом. |
| 1045 | Добавить retirement evidence. | Вывод из эксплуатации проверяем. |
| 1046 | Проверить privacy boundary incident evidence. | Evidence не раскрывает лишние данные. |
| 1047 | Вынести full incident forms в companion. | В книге остается методология. |
| 1048 | Добавить assurance checklist. | Читатель может применить главу к своей системе. |
| 1049 | Сверить главу 20 с appendices. | Приложения не дублируют главу. |
| 1050 | Экспортировать главу 20 и провести render QA. | Маркеры и переходы найдены. |
| 1051 | Проверить главы 21-23 как runtime/reference continuation. | Поздние главы не повторяют основную часть. |
| 1052 | Сжать длинные runtime configs в companion route. | Печатный текст не становится справочником полей. |
| 1053 | Проверить chapter 21 execution environment на связь с evidence chain. | Runtime объясняется через эксплуатационные доказательства. |
| 1054 | Проверить chapter 22 policy/catalog на связь с chapters 14-15. | Policy changes проходят eval and rollout gates. |
| 1055 | Проверить chapter 23 production launch checklist. | Checklist не повторяет главы, а собирает их в launch review. |
| 1056 | Убрать устаревшие chapter references в главах 21-23. | Нумерация совпадает с текущей рукописью. |
| 1057 | Проверить приложения на повторение full payloads. | Длинные payloads вынесены в companion. |
| 1058 | Сформировать appendices gap list. | Видно, что еще нужно дозаполнить. |
| 1059 | Экспортировать поздние главы и приложения. | DOCX открывается. |
| 1060 | Провести render QA поздних глав. | Нет пустых страниц и грубых style regressions. |
| 1061 | Провести cross-manuscript terminology audit. | Capability, policy, gate, trace, SLO, eval, registry используются стабильно. |
| 1062 | Нормализовать русско-английские пары терминов. | Английские термины оставлены только там, где они контрактны. |
| 1063 | Проверить `eval`, `judge`, `verdict`, `threshold`, `gate`. | Словарь главы 15 закреплен дальше по рукописи. |
| 1064 | Проверить `evidence`, `bundle`, `trace`, `event`. | Глава 16 не конфликтует с главой 13. |
| 1065 | Проверить `owner`, `owner_role`, `expected_action`. | Alerting и ownership согласованы. |
| 1066 | Проверить `rollout`, `limited mode`, `rollback`. | Release terms используются одинаково. |
| 1067 | Проверить `incident`, `postmortem`, `review`. | Incident terms не смешиваются с defects. |
| 1068 | Проверить `retirement`, `decommission`, `disable`. | Lifecycle terms стабильны. |
| 1069 | Составить glossary delta для редактора. | Редактор видит намеренные англоязычные термины. |
| 1070 | Экспортировать terminology QA report. | Есть проверяемый список правок. |
| 1071 | Провести companion manifest audit. | Все companion routes из глав существуют в manifest. |
| 1072 | Нормализовать route names. | Имена короткие, стабильные и chapter-scoped. |
| 1073 | Разделить printable excerpt и companion-only payload. | Нет ложного обещания печатного справочника. |
| 1074 | Проверить companion privacy boundary. | Нет PII, secrets, internal endpoints. |
| 1075 | Добавить companion version policy. | Версия companion связана с редакцией книги. |
| 1076 | Сформировать route owner map. | У каждого companion material есть владелец. |
| 1077 | Проверить errata workflow. | Читатель знает, куда сообщать ошибки. |
| 1078 | Проверить source citation policy. | Источники не перегружают основной текст. |
| 1079 | Сформировать publisher note о companion. | Издатель понимает структуру online materials. |
| 1080 | Экспортировать companion packet. | Manifest и notes готовы к ревью. |
| 1081 | Провести полный raw DOCX export. | Raw DOCX проходит zip integrity. |
| 1082 | Провести полный Template2000n derivative. | Производный DOCX проходит zip integrity. |
| 1083 | Выполнить raw render QA. | Page count, marker pages and blankish pages зафиксированы. |
| 1084 | Выполнить Template2000n render QA. | Page count and visual spot checks зафиксированы. |
| 1085 | Проверить первые страницы всех глав. | Заголовки и openings не ломают верстку. |
| 1086 | Проверить последние страницы всех глав. | Companion routes and next-read sections читаемы. |
| 1087 | Проверить checklist/list rendering. | Numbered details не становятся ложными heading blocks. |
| 1088 | Проверить dense technical paragraphs. | Нет stretched justification вокруг `snake_case`. |
| 1089 | Проверить TOC marker noise. | Отчет различает TOC hits и body hits. |
| 1090 | Подготовить proof QA summary. | Издатель получает краткие page counts and caveats. |
| 1091 | Сформировать final editorial packet. | Пакет содержит Google Doc link, DOCX exports, QA reports and companion notes. |
| 1092 | Составить author-owned fields checklist. | Авторские поля явно перечислены. |
| 1093 | Проверить block about author. | Биография остается заполняемой, без выдуманных фактов. |
| 1094 | Проверить front matter. | Введение, аннотация и навигация соответствуют рукописи. |
| 1095 | Запустить `uv run --group dev pytest`. | Все тесты проходят. |
| 1096 | Запустить `uv run --group docs mkdocs build --strict`. | Сборка проходит, предупреждения известны. |
| 1097 | Проверить git status and staged files. | В коммит попадают только файлы текущего прохода. |
| 1098 | Создать финальный commit. | Commit message описывает редакционный проход. |
| 1099 | Push в рабочую ветку. | Ветка обновлена на origin. |
| 1100 | Подготовить итоговый отчет для автора. | Отчет содержит страницы, проверки, commit, push and author-owned fields. |

## Author-owned поля

- Имя автора и публичная подпись.
- Текущая роль, компания или независимый статус.
- Краткая биография для издательства.
- Ключевой опыт и публичные проекты.
- Ссылки на сайт, GitHub, профиль или другие публичные ресурсы.
- Посвящение и благодарности.
- Контакт для errata.
- Публичный адрес companion-материалов.
- Финальная версия companion-пакета, соответствующая печатной рукописи.
