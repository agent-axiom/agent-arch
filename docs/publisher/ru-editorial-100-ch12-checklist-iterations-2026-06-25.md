# Editorial iteration plan 701-800

Дата: 2026-06-25

Основание: после прохода по главе 12 рукопись имеет рабочий production checklist, нормализованную терминологию `retryable_failure` / `side_effect_unknown` / `rollback boundary` / `reconciliation`, явный выход к observability и свежие DOCX proof-артефакты.

Текущий volume snapshot:

- raw Google Docs export: 633 страницы;
- Template2000n proof: 378 страниц;
- targeted render QA по главе 12: passed;
- blank-like pages: 0.

| Iteration | Goal | Done when | Verification |
| ---: | --- | --- | --- |
| 701 | Проверить opening главы 13 после нового выхода главы 12 | Глава 13 начинает расследование как продолжение `side_effect_unknown`, а не новый независимый блок | Readback + marker pages |
| 702 | Сжать technical preface главы 13 | В главе 13 нет повторного объяснения, уже закрытого в главе 12 | Diff review |
| 703 | Уточнить роль trace vs logs | Читатель видит, почему trace - цепочка доказательств, а logs - только сырой материал | Chapter 13 readthrough |
| 704 | Привязать trace fields к write intent | `intent_id`, `trace_id`, `idempotency_key`, policy decision и approval связаны в одной схеме | Term grep |
| 705 | Проверить examples главы 13 на duplicate-ticket continuity | Кейс поддержки не теряет связь с главой 12 | Scenario continuity pass |
| 706 | Сократить длинные event catalog фрагменты главы 13 | В печати остаются только поля, нужные для аргумента | DOCX render QA |
| 707 | Зафиксировать companion route для trace payloads | Полные event schemas вынесены в companion | Companion route grep |
| 708 | Нормализовать `span`, `event`, `trace`, `session` | Термины не используются взаимозаменяемо | Term audit |
| 709 | Добавить мини-checklist trace readiness | В конце главы 13 есть короткий operational checklist | Google Doc readback |
| 710 | Проверить переход главы 13 -> глава 14 | Observability логично ведет к metrics/SLO, а не повторяет trace | Bridge review |
| 711 | Инвентаризировать главу 14 на повторы SLO/metric | Повторные определения сокращены | Chapter map |
| 712 | Уточнить разницу между product metric и safety metric | Читатель видит, что safety metric не равна успешности ответа | Editorial readthrough |
| 713 | Привязать SLO к agent runtime failure modes | SLO описывает конкретные failure modes из предыдущих глав | Term grep |
| 714 | Сжать metrics examples главы 14 | Таблицы и списки не превращаются в каталог | Render spot check |
| 715 | Добавить route для dashboards companion | Полные dashboard examples вынесены из печати | Companion route |
| 716 | Проверить alert fatigue language | Нет советов, ведущих к шумным алертам без владельца | Content review |
| 717 | Связать metrics с incident response | Метрики ведут к расследованию и containment, а не только к графикам | Chapter bridge |
| 718 | Нормализовать `SLO`, `SLI`, `error budget` | Термины используются последовательно | Term audit |
| 719 | Проверить главу 14 на vendor-neutral wording | Нет привязки к одному observability stack | Source review |
| 720 | Добавить короткий вывод главы 14 | Вывод ведет к eval gates и regression testing | Readback |
| 721 | Инвентаризировать главу 15 eval structure | Eval разделы идут от сценариев к gate decision | Chapter outline |
| 722 | Уточнить связь eval с incident learnings | Инциденты возвращаются в eval-наборы | Cross-reference check |
| 723 | Сжать длинные eval YAML blocks | Печать показывает intention and grading logic, companion хранит full dataset | Render QA |
| 724 | Нормализовать `eval`, `test`, `red team`, `review` | Термины не смешиваются | Term audit |
| 725 | Усилить примеры regression gate | Gate показывает stop/allow decision, а не общий совет тестировать | Scenario review |
| 726 | Добавить checklist для eval readiness | Команда видит минимальные поля и владельца | Google Doc readback |
| 727 | Проверить eval examples на leakage of implementation details | Из печати убраны поля, полезные только CLI | Companion route grep |
| 728 | Связать eval gate с rollout decision | Eval становится входом в rollout, а не отдельным отчетом | Chapter bridge |
| 729 | Проверить chapter 15 visual density | Длинные страницы не перегружены YAML/таблицами | DOCX render spot |
| 730 | Подготовить chapter 15 exit | Выход ведет к rollout/change management | Readthrough |
| 731 | Инвентаризировать rollout chapters | Rollout идет от feature flag к governance evidence | Chapter map |
| 732 | Уточнить `rollout wave` and `kill switch` | Термины используются как operational controls | Term grep |
| 733 | Сократить rollout checklist | Checklist остается decision-oriented | Content diff |
| 734 | Привязать rollout к owner map | Каждая risky capability имеет владельца решения | Cross-reference |
| 735 | Проверить rollback vs retirement language | Rollback не подменяет вывод из эксплуатации | Term audit |
| 736 | Добавить route для rollout configs | Полные config examples вынесены в companion | Companion route |
| 737 | Усилить canary criteria | Canary имеет measurable stop conditions | Scenario review |
| 738 | Проверить incident examples after rollout | Инциденты связаны с change_id и rollout wave | Grep |
| 739 | Сократить repeated governance paragraphs | Управленческие повторения сведены к bridge paragraphs | Readthrough |
| 740 | Подготовить rollout chapter exit | Выход ведет к registry/lifecycle | Chapter bridge |
| 741 | Проверить agent registry chapters | Registry описан как operational inventory, не spreadsheet theater | Editorial review |
| 742 | Нормализовать owner fields | Owner, steward, reviewer, approver не смешаны | Term audit |
| 743 | Связать registry с incident response | По incident можно восстановить agent, owner, policy bundle | Cross-reference |
| 744 | Сжать registry schema listings | В печати остаются только identity/risk/evidence fields | Render QA |
| 745 | Добавить companion route для registry templates | Полные шаблоны вынесены | Companion route |
| 746 | Проверить privacy/security language registry | Нет рекомендаций хранить лишние sensitive fields | Security readthrough |
| 747 | Уточнить lifecycle states | Draft, review, active, limited, retired описаны стабильно | Term grep |
| 748 | Проверить registry chapter exit | Выход ведет к retirement/decommissioning | Bridge review |
| 749 | Инвентаризировать retirement chapter | Retirement не выглядит как appendix afterthought | Chapter map |
| 750 | Уточнить retirement evidence | Вывод из эксплуатации оставляет доказательства отключения | Readback |
| 751 | Сжать decommissioning checklist | Checklist показывает stop criteria и owner action | Content diff |
| 752 | Связать retirement с companion versioning | Companion показывает deprecated/removed examples | Cross-reference |
| 753 | Проверить hidden dependency language | Глава объясняет, как искать зависимые процессы | Editorial review |
| 754 | Нормализовать `deprecation`, `retirement`, `disable` | Термины не заменяют друг друга | Term audit |
| 755 | Добавить case closure paragraph | Читатель видит конец lifecycle loop | Readthrough |
| 756 | Проверить appendix source routes | Источники разделены на primary, practice, learning, author companion | Source audit |
| 757 | Проверить source freshness labels | Нестабильные платформенные факты требуют актуальной проверки | Source note pass |
| 758 | Сократить длинные URL in body | Длинные ссылки остаются в notes/companion | Link audit |
| 759 | Добавить source route per major part | У каждой части есть путь к источникам | Companion map |
| 760 | Проверить claims without source | Сильные утверждения имеют источник или помечены как авторская рекомендация | Source audit |
| 761 | Инвентаризировать glossary | Glossary покрывает recurring terms без лишней энциклопедии | Term list |
| 762 | Нормализовать Russian/English term policy | Английские имена используются как contract names | Style pass |
| 763 | Проверить casing ключевых терминов | `trace_id`, `policy gateway`, `ADLC` выглядят стабильно | Grep |
| 764 | Сократить повторные определения | Повторные определения заменены cross-reference | Diff review |
| 765 | Добавить missing glossary entries | Добавлены только реально recurring terms | Glossary review |
| 766 | Проверить front matter | Аннотация, keywords и reading guide соответствуют текущей книге | Front matter pass |
| 767 | Заполнить author placeholder checklist | Все author-owned placeholders перечислены для автора | Placeholder grep |
| 768 | Проверить TOC consistency | Заголовки не конфликтуют с оглавлением Google Doc/DOCX | Export check |
| 769 | Проверить chapter numbering consistency | Номера глав и приложений не повторяются | Heading grep |
| 770 | Проверить listing numbering consistency | Листинги идут без пропусков и ложных совпадений `12.1`/`12.10` | Listing audit |
| 771 | Проверить tables/captions | Таблицы имеют смысловую подпись или route to companion | Render spot |
| 772 | Проверить figure placeholders | Нет случайных пустых placeholders в печатном потоке | Visual QA |
| 773 | Проверить Markdown artifacts | Нет raw fences, stray bullets, broken code markers | Grep |
| 774 | Проверить quote formatting | User/system examples оформлены единообразно | Style pass |
| 775 | Проверить list density | Списки не заменяют объяснение там, где нужна аргументация | Editorial review |
| 776 | Проверить chapter openings | Каждая глава начинается с проблемы, а не с определения | Readthrough |
| 777 | Проверить chapter exits | Каждая глава ведет к следующему инженерному решению | Bridge audit |
| 778 | Проверить applied cases continuity | Кейс поддержки/тикета проходит через trace/eval/incident | Scenario map |
| 779 | Проверить reference runtime references | Runtime представлен как иллюстрация, не как обязательный фреймворк | Text grep |
| 780 | Проверить companion scope | Companion не заменяет книгу и не перегружает печать | Companion audit |
| 781 | Проверить style for IT book best practices | Текст объясняет tradeoffs, failure modes, ownership, evidence | Editorial pass |
| 782 | Проверить avoidance of hype | Нет маркетинговых обещаний автономности без контроля | Tone pass |
| 783 | Проверить actionability | В каждой крупной части есть usable checklist or decision artifact | Chapter audit |
| 784 | Проверить safety disclaimers | Legal/compliance/security limits сказаны без ухода от инженерной ответственности | Review |
| 785 | Проверить terminology in chapter 12 after export | Новая терминология не потерялась в DOCX proof | PDF marker check |
| 786 | Проверить chapter 13 after Template2000n | Нет растяжки, clipping, orphan heading around chapter start | Visual QA |
| 787 | Проверить all high-density pages in Template2000n | Dense pages readable after style mapping | Render sample |
| 788 | Проверить blank-like pages after next export | Blank-like pages stay 0 | PNG scan |
| 789 | Проверить final page | Последняя страница не пустая и не обрезана | Visual QA |
| 790 | Подготовить editorial packet index | Есть список всех артефактов для редакции | Packet report |
| 791 | Подготовить author-fill packet | Отдельно перечислено, что автор должен заполнить вручную | Placeholder report |
| 792 | Проверить repo artifacts list | В репозитории лежат только нужные DOCX/JSON/MD files | Git status |
| 793 | Проверить mkdocs/doc build | Docs site собирается строго | `mkdocs build --strict` |
| 794 | Прогнать test suite | Runtime/reference package не сломан редакционными артефактами | `pytest` |
| 795 | Сделать fresh Google Doc export | Экспорт соответствует финальной ревизии после очередного pass | DOCX export |
| 796 | Сделать fresh Template2000n derivative | Publisher proof соответствует свежему export | DOCX render |
| 797 | Сравнить page counts | Page count changes объяснены и зафиксированы | QA JSON |
| 798 | Подготовить human proofread brief | Редактор получает фокус: смысл, логика, стилистика, placeholders | Handoff note |
| 799 | Зафиксировать commit and push | Все новые артефакты закоммичены и отправлены | Git log + push |
| 800 | Итоговый readiness report | Пользователь получает краткий итог и список author-owned полей | Final report |
