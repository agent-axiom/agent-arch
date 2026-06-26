# Editorial iteration plan 801-900

Дата: 2026-06-26

Основание: после прохода по главе 13 рукопись имеет связанный переход от `write-path` к trace evidence, нормализованные `trace` / `span` / `event` / `session`, минимальный trace field contract, readiness checklist, companion route для полных payloads и свежие DOCX proof-артефакты.

Текущий volume snapshot:

- raw Google Docs export: 616 страниц;
- Template2000n proof: 308 страниц;
- targeted render QA по главе 13: passed;
- blank-like pages: 0.

| Iteration | Goal | Done when | Verification |
| ---: | --- | --- | --- |
| 801 | Проверить chapter 14 opening после нового выхода главы 13 | Глава 14 начинает SLO как ежедневное здоровье системы, а не повтор trace | Readback + marker pages |
| 802 | Сжать повторные объяснения observability в главе 14 | Повтор главы 13 заменен коротким bridge paragraph | Diff review |
| 803 | Нормализовать `SLO`, `SLI`, `error budget` | Термины не используются взаимозаменяемо | Term grep |
| 804 | Привязать SLO к failure modes агентной системы | SLO отражают latency, unsafe action, tool outcome, approval delay, recovery | Chapter readthrough |
| 805 | Развести product metric и safety metric | Успешность ответа не подменяет безопасность действия | Editorial review |
| 806 | Проверить примеры alerting в главе 14 | Alert ведет к владельцу и action, а не к шуму | Scenario review |
| 807 | Вынести dashboard examples в companion | В печати остаются только decision-oriented excerpts | Companion route grep |
| 808 | Добавить short SLO readiness checklist | Команда видит минимальный operational gate | Google Doc readback |
| 809 | Проверить chapter 14 visual density | Нет перегруженных страниц с таблицами и списками | DOCX render spot |
| 810 | Подготовить выход главы 14 к eval gates | SLO логично ведут к regression/eval chapter | Bridge review |
| 811 | Инвентаризировать eval chapter structure | Eval идет от сценариев и рисков к gate decision | Chapter map |
| 812 | Нормализовать `eval`, `test`, `red team`, `review` | Термины имеют разные роли в тексте | Term audit |
| 813 | Связать eval cases с trace evidence | Eval может ссылаться на trace fields and event outcomes | Cross-reference check |
| 814 | Проверить incident learnings в eval-наборах | Инциденты возвращаются в regression suite | Scenario continuity |
| 815 | Сжать длинные eval YAML blocks | Full dataset уходит в companion, печать хранит grading logic | Render QA |
| 816 | Усилить negative examples для unsafe tool use | Пример показывает stop decision, а не общий совет тестировать | Editorial review |
| 817 | Добавить eval readiness checklist | Есть owner, dataset version, pass/fail rule, escalation | Readback |
| 818 | Проверить leakage implementation details | CLI-only поля и полный payload вынесены из печати | Companion route grep |
| 819 | Привязать eval gate к rollout decision | Eval становится входом в release decision | Chapter bridge |
| 820 | Подготовить выход eval chapter к rollout | Следующая глава начинается с controlled release | Readthrough |
| 821 | Инвентаризировать rollout/change chapters | Rollout идет от capability risk к controlled waves | Chapter map |
| 822 | Нормализовать `rollout wave`, `feature flag`, `kill switch` | Термины используются как operational controls | Term grep |
| 823 | Уточнить canary stop criteria | Canary имеет measurable stop conditions | Scenario review |
| 824 | Связать rollout с owner map | Рискованная capability имеет владельца решения | Cross-reference |
| 825 | Проверить rollback vs retirement language | Rollback не подменяет вывод из эксплуатации | Term audit |
| 826 | Сократить rollout checklist | Checklist остается decision-oriented | Content diff |
| 827 | Вынести rollout configs в companion | Full configs живут вне печатного потока | Companion route |
| 828 | Проверить change_id and evidence refs | Release decision восстанавливается после incident | Grep |
| 829 | Убрать повторные governance paragraphs | Управленческие повторы заменены bridge paragraphs | Readthrough |
| 830 | Подготовить выход rollout chapter к registry | Release ведет к operational inventory | Bridge review |
| 831 | Проверить agent registry chapters | Registry описан как operational inventory, не формальная таблица | Editorial review |
| 832 | Нормализовать owner/steward/reviewer/approver | Роли не смешиваются | Term audit |
| 833 | Связать registry с policy bundle | По агенту можно восстановить активные политики | Cross-reference |
| 834 | Связать registry с incident response | По incident можно найти agent, owner, rollout wave | Scenario check |
| 835 | Сжать registry schema listings | В печати остаются identity/risk/evidence fields | Render QA |
| 836 | Вынести registry templates в companion | Full templates доступны отдельным route | Companion route |
| 837 | Проверить privacy/security fields registry | Нет рекомендации хранить лишние sensitive fields | Security readthrough |
| 838 | Уточнить lifecycle states | Draft, review, active, limited, retired стабильны | Term grep |
| 839 | Проверить registry chapter exit | Выход ведет к lifecycle and retirement | Bridge review |
| 840 | Сверить registry with appendix templates | Приложения не противоречат главе | Appendix check |
| 841 | Инвентаризировать incident/assurance chapters | Incident response связан с trace, eval, rollout, registry | Chapter map |
| 842 | Нормализовать incident record fields | `incident_id`, `trace_id`, `change_id`, `policy_bundle_id` стабильны | Term grep |
| 843 | Связать containment with recovery evidence | Containment фиксирует действие и доказательства | Scenario review |
| 844 | Проверить postmortem action loop | Postmortem возвращается в eval, policy, rollout | Cross-reference |
| 845 | Сжать incident templates в печати | Полные шаблоны уходят в companion | Companion route |
| 846 | Проверить assurance loop wording | Assurance не выглядит как одноразовая проверка перед запуском | Editorial review |
| 847 | Развести compliance и engineering assurance | Текст не обещает compliance-гарантию вместо процесса | Risk review |
| 848 | Добавить короткий incident readiness gate | Есть минимальные вопросы перед production | Readback |
| 849 | Проверить incident chapter visual density | Списки и templates не перегружают страницы | Render spot |
| 850 | Подготовить выход к retirement/decommissioning | Инциденты логично ведут к lifecycle corrections | Bridge review |
| 851 | Инвентаризировать retirement/decommission chapter | Retirement не выглядит как appendix afterthought | Chapter map |
| 852 | Нормализовать `disable`, `deprecation`, `retirement` | Термины имеют разные operational meanings | Term audit |
| 853 | Уточнить retirement evidence | Вывод оставляет proof отключения и owner sign-off | Readthrough |
| 854 | Связать retirement with registry states | Registry отражает retired/limited states | Cross-reference |
| 855 | Проверить hidden dependency language | Глава объясняет поиск зависимых процессов | Editorial review |
| 856 | Сжать decommissioning checklist | Checklist показывает stop criteria and owner action | Content diff |
| 857 | Вынести retirement templates в companion | Full checklists and evidence forms routed out | Companion route |
| 858 | Связать companion versioning with retired examples | Deprecated examples отмечены версией | Companion audit |
| 859 | Добавить case closure paragraph | Читатель видит полный lifecycle loop | Readthrough |
| 860 | Проверить chapter exit к appendices | Финал не обрывает практическую логику | Bridge review |
| 861 | Проверить appendix source routes | Источники разделены на primary, practice, learning, author companion | Source audit |
| 862 | Проверить freshness labels | Нестабильные платформенные факты требуют актуальной проверки | Source note pass |
| 863 | Сократить длинные URL in body | Длинные ссылки уходят в notes/companion | Link audit |
| 864 | Добавить source route per major part | У каждой части есть понятный путь к источникам | Companion map |
| 865 | Проверить claims without source | Сильные утверждения имеют источник или помечены как авторская рекомендация | Source audit |
| 866 | Проверить companion README requirements | Companion имеет README, changelog, errata, versioning | Repo checklist |
| 867 | Проверить trace/event catalogs in companion scope | Каталоги не перегружают печатную книгу | Companion audit |
| 868 | Сверить source appendix with manuscript claims | Appendix не обещает того, чего нет в книге | Cross-check |
| 869 | Проверить license and reuse notes | Companion материалы имеют понятный reuse status | Publisher check |
| 870 | Подготовить source handoff brief | Редактор понимает, какие источники должны быть проверены вручную | Handoff note |
| 871 | Инвентаризировать glossary | Glossary покрывает recurring terms без энциклопедии | Term list |
| 872 | Нормализовать Russian/English term policy | Английские имена используются как contract names | Style pass |
| 873 | Проверить casing ключевых терминов | `trace_id`, `policy gateway`, `ADLC`, `SLO` стабильны | Grep |
| 874 | Сократить повторные определения | Повторы заменены cross-reference или bridge | Diff review |
| 875 | Добавить missing glossary entries | Добавлены только реально recurring terms | Glossary review |
| 876 | Проверить front matter against current manuscript | Аннотация, keywords, reading guide соответствуют книге | Front matter pass |
| 877 | Сверить author placeholder list | Все author-owned placeholders перечислены | Placeholder grep |
| 878 | Подготовить author-fill packet | Автор получает отдельный список ручных полей | Report |
| 879 | Проверить dedication/acknowledgements decision | Блоки есть или явно исключены | Author review |
| 880 | Проверить public companion URL placeholder | URL companion отмечен как author-owned | Placeholder report |
| 881 | Проверить TOC consistency after export | Заголовки не конфликтуют с DOCX/Google Doc TOC | Export check |
| 882 | Проверить chapter numbering consistency | Номера глав и приложений не повторяются | Heading grep |
| 883 | Проверить listing numbering consistency | Листинги идут без пропусков и ложных совпадений | Listing audit |
| 884 | Проверить tables/captions | Таблицы имеют смысловую подпись или companion route | Render spot |
| 885 | Проверить figure placeholders | Нет случайных пустых placeholders в печатном потоке | Visual QA |
| 886 | Проверить Markdown artifacts | Нет raw fences, stray bullets, broken code markers | Grep |
| 887 | Проверить quote formatting | User/system examples оформлены единообразно | Style pass |
| 888 | Проверить list density | Списки не заменяют объяснение там, где нужна аргументация | Editorial review |
| 889 | Проверить page count deltas | Изменения объема объяснены и зафиксированы | QA JSON |
| 890 | Сделать fresh raw + Template2000n proof | Proof соответствует последней редакции | Render QA |
| 891 | Проверить chapter openings | Каждая глава начинается с проблемы, а не определения | Readthrough |
| 892 | Проверить chapter exits | Каждая глава ведет к следующему инженерному решению | Bridge audit |
| 893 | Проверить applied cases continuity | Кейс поддержки проходит через trace/eval/incident/lifecycle | Scenario map |
| 894 | Проверить reference runtime references | Runtime представлен как иллюстрация, не обязательный фреймворк | Text grep |
| 895 | Проверить avoidance of hype | Нет обещаний автономности без контроля | Tone pass |
| 896 | Проверить actionability | В каждой крупной части есть usable checklist or decision artifact | Chapter audit |
| 897 | Проверить safety disclaimers | Limits сказаны без ухода от инженерной ответственности | Review |
| 898 | Подготовить final editorial packet index | Есть список всех артефактов для редакции | Packet report |
| 899 | Зафиксировать commit and push | Новые артефакты закоммичены и отправлены | Git log + push |
| 900 | Итоговый readiness report | Пользователь получает итог и список author-owned полей | Final report |

