# Editorial iterations 1301-1400 - chapter 19 ADLC pass

Цель набора: зафиксировать следующие 100 редакционных итераций после расширения главы 19, чтобы рукопись двигалась к сильному редакционному варианту без потери логической нити.

Текущий Google Doc: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI

Текущий объем proof после прохода:

- Raw Google Doc DOCX render: 623 страницы, blank-like pages: 0.
- Template2000n proof: 322 страницы, blank-like pages: 0.

| # | Цель итерации | Критерий готовности |
|---:|---|---|
| 1301 | Сверить логический переход глав 17 -> 18 -> 19. | Переход от ownership к standard paths и ADLC читается как один аргумент. |
| 1302 | Проверить, не дублирует ли глава 19 материал главы 20. | Глава 19 отвечает за lifecycle, глава 20 - за assurance and incidents. |
| 1303 | Уточнить формулу "ADLC расширяет SDLC". | В тексте нет противопоставления SDLC и ADLC. |
| 1304 | Проверить все behavior surfaces в главе 19. | Каждая поверхность связана с риском и lifecycle. |
| 1305 | Добавить короткую cross-reference к capability contracts. | Читатель понимает, где capability contract входит в ADLC. |
| 1306 | Проверить связку policy gateway and ADLC. | Policy change трактуется как behavior-changing artifact. |
| 1307 | Проверить связку tool gateway and ADLC. | Tool contract change имеет owner/evidence/rollback. |
| 1308 | Проверить retrieval section на ясность. | Corpus, ranking, access boundary and poisoning раскрыты без перегруза. |
| 1309 | Проверить memory section на практичность. | Memory schema, retention, deletion and poisoning названы явно. |
| 1310 | Сжать слишком длинные предложения в начале главы 19. | Первые две страницы читаются без чрезмерной плотности. |
| 1311 | Проверить risk tier low. | Low risk не выглядит как "без процесса". |
| 1312 | Проверить risk tier medium. | Medium risk имеет clear eval and rollout expectations. |
| 1313 | Проверить risk tier high. | High risk связан с write actions, regulated data and autonomy. |
| 1314 | Добавить пример ambiguous risk escalation. | Неопределенность временно повышает tier. |
| 1315 | Проверить change record example low risk. | Пример короткий и полезный для команды. |
| 1316 | Проверить change record example medium risk. | Пример показывает retrieval/model evidence. |
| 1317 | Проверить change record example high risk. | Пример показывает rollback drill and observation window. |
| 1318 | Уточнить owner roles в разделе 7. | Роли не конфликтуют с главой 17. |
| 1319 | Проверить evidence package vocabulary. | Термины evidence, eval, proof, record используются стабильно. |
| 1320 | Проверить rollback terminology. | Rollback, containment and degraded mode различены. |
| 1321 | Проверить design gate. | Gate задает право системы действовать до build. |
| 1322 | Проверить build gate. | Build gate связан со standard paths и agent zoo prevention. |
| 1323 | Проверить eval gate. | Eval gate покрывает refusal, escalation and unsafe action prevention. |
| 1324 | Проверить rollout gate. | Blast radius, canary, kill switch and observation window названы. |
| 1325 | Проверить observe gate. | Production metrics представлены как lifecycle evidence. |
| 1326 | Проверить incident gate. | Incident возвращает знания в evals/policy/runbooks. |
| 1327 | Проверить retirement gate. | Retirement не сводится к удалению кода. |
| 1328 | Добавить cross-reference к registry. | Registry status связан с active/retiring/retired состояниями. |
| 1329 | Проверить support ticket agent scenario. | Сценарий ясно показывает эволюцию read-only -> action -> background. |
| 1330 | Проверить prompt/model/retrieval scenario. | Сценарий показывает, что не только код меняет поведение. |
| 1331 | Проверить anti-bureaucracy section. | ADLC ускоряет зрелые команды, а не только добавляет формы. |
| 1332 | Проверить reusable evidence. | Повторное использование артефактов объяснено достаточно. |
| 1333 | Проверить standard paths в главе 19. | Они связаны с главой 18, но не повторяют ее дословно. |
| 1334 | Сверить companion route главы 19 с приложением. | Файлы companion не дублируют печатный текст. |
| 1335 | Проверить readiness checklist на полноту. | В чеклисте есть owner, surfaces, risk, evidence, rollout, rollback. |
| 1336 | Проверить readiness checklist на длину. | Чеклист не превращается в тяжелую таблицу в печатном тексте. |
| 1337 | Проверить переход к главе 20. | Последний абзац явно открывает assurance loop. |
| 1338 | Проверить H1/H3 стили главы 19 в Google Doc. | Заголовки видны в структуре документа. |
| 1339 | Проверить H1/H3 стили в Template2000n DOCX. | Chapter heading and section headings рендерятся корректно. |
| 1340 | Проверить raw page 423. | Старт главы 19 не имеет orphan heading. |
| 1341 | Проверить raw pages 424-426. | Первая аргументация главы читается без сломанной верстки. |
| 1342 | Проверить raw pages 442-445. | Companion, checklist, вывод и глава 20 читаются последовательно. |
| 1343 | Проверить Template pages 230-233. | Начало главы 19 читается после стилей шаблона. |
| 1344 | Проверить Template pages 236-239. | Readiness checklist и глава 20 не конфликтуют визуально. |
| 1345 | Сверить page count после следующего pass. | Рост/снижение объема объяснимы. |
| 1346 | Проверить термин ADLC в front matter. | Термин соответствует главе 19. |
| 1347 | Проверить глоссарий на ADLC/lifecycle terms. | Lifecycle terms не расходятся с главой 19. |
| 1348 | Проверить sources/companion references. | Длинные технические шаблоны вынесены наружу. |
| 1349 | Проверить английские terms in Russian prose. | Смешение русского/английского выглядит осознанным. |
| 1350 | Проверить "behavior-changing artifact" как ключевой термин. | Термин объяснен до активного использования. |
| 1351 | Проверить "side effect" usage. | Side effect связан с high risk and rollback. |
| 1352 | Проверить "owner map" usage. | Owner map не выглядит как новая неописанная сущность. |
| 1353 | Проверить "policy bundle" usage. | Policy bundle связан с verifier and rollout. |
| 1354 | Проверить "approval semantics" usage. | Approval semantics раскрывает, что именно подтверждает человек. |
| 1355 | Проверить "eval suite change" как governance artifact. | Изменение evals описано как изменение готовности. |
| 1356 | Проверить "registry update" как обязательный след. | Registry не упоминается только в конце. |
| 1357 | Проверить стиль перечислений. | Длинные списки не перегружают страницу. |
| 1358 | Проверить плотные англоязычные фразы. | Английские связки не ломают русскую читаемость. |
| 1359 | Проверить тире и дефисы в главе 19. | Стиль согласован с остальной рукописью. |
| 1360 | Проверить отсутствие Markdown artifacts. | Нет лишних backticks, fences or raw YAML blocks. |
| 1361 | Проверить all chapter 19 headings in TOC/outline. | В outline нет пунктов чеклиста как heading. |
| 1362 | Проверить, не стал ли checklist numbered heading в Google Doc. | Пункты чеклиста остаются body/list text. |
| 1363 | Проверить chapter 20 start after style pass. | Глава 20 начинается отдельно и не утонула в body. |
| 1364 | Проверить raw DOCX integrity after future edits. | `zipfile -t` проходит. |
| 1365 | Проверить Template DOCX integrity after future edits. | `zipfile -t` проходит. |
| 1366 | Повторить render QA после следующей главы. | Blank-like pages остаются 0. |
| 1367 | Проверить known dirty files перед commit. | В commit попадают только новые pass artifacts. |
| 1368 | Обновить submission checklist после author fill. | Авторские placeholders больше не блокируют сдачу. |
| 1369 | Подготовить human proofread checklist для главы 19. | Человек проверяет плотность, термины and examples. |
| 1370 | Проверить chapter 19 against "best practices for IT books". | В главе есть тезис, объяснение, сценарий, чеклист and takeaway. |
| 1371 | Проверить наличие "why it matters" в каждом крупном блоке. | Разделы не выглядят как справочник. |
| 1372 | Проверить наличие "what breaks without it". | Риски описаны через практические последствия. |
| 1373 | Проверить наличие "how to implement". | Команда видит минимальный внедренческий путь. |
| 1374 | Проверить наличие "how to verify". | Evidence and QA связаны с действиями. |
| 1375 | Проверить наличие "how to rollback". | Rollback не остается декларацией. |
| 1376 | Проверить glossary consistency across chapters 17-20. | Terms owner, evidence, lifecycle, assurance согласованы. |
| 1377 | Проверить examples for confidentiality. | Нет реальных чувствительных данных. |
| 1378 | Проверить examples for vendor neutrality. | Глава не привязана к одному провайдеру. |
| 1379 | Проверить examples for shelf life. | Рекомендации не зависят от текущих API limits. |
| 1380 | Проверить chapter 19 against agent_runtime_ref companion. | Companion route соответствует реальным путям репозитория. |
| 1381 | Проверить, нужен ли ADLC diagram. | Если нужна схема, вынести в companion или отдельный рисунок. |
| 1382 | Проверить, нужна ли таблица risk tier. | Таблицу лучше держать компактной или вынести в companion. |
| 1383 | Проверить, нужен ли один full-page checklist. | Если печатный поток перегружен, перенести expanded checklist наружу. |
| 1384 | Проверить chapter 19 introduction after copyedit. | Первый экран главы должен быстро вводить конфликт. |
| 1385 | Проверить chapter 19 conclusion after copyedit. | Вывод должен подводить к assurance loop. |
| 1386 | Проверить page breaks around chapter 19 in Template proof. | Нет коротких висячих заголовков. |
| 1387 | Проверить page breaks around chapter 20 in Template proof. | Глава 20 стартует на чистой логической границе. |
| 1388 | Проверить author block before publisher handoff. | Все placeholders в "Об авторе" заполнены или помечены. |
| 1389 | Проверить final DOCX filename convention. | Имена артефактов отражают дату и pass. |
| 1390 | Проверить render QA JSON after final pass. | Метрики содержат raw/template page counts and markers. |
| 1391 | Проверить commit scope. | Только ch19 pass reports/artifacts/staged files включены. |
| 1392 | Проверить mkdocs build после новых отчетов. | Документация собирается с известными nav warnings only. |
| 1393 | Проверить pytest после новых файлов. | Тесты проходят без влияния editorial artifacts. |
| 1394 | Проверить push branch status. | Remote branch содержит latest commit. |
| 1395 | Подготовить short editor handoff note. | Редактор видит, что изменилось и где смотреть. |
| 1396 | Подготовить author TODO block. | Авторские поля перечислены отдельно. |
| 1397 | Подготовить final manuscript readiness view. | Главы 17-20 образуют зрелый production lifecycle arc. |
| 1398 | Проверить no accidental TOC/body mismatch. | Body headings and TOC entries согласованы после Google Docs refresh. |
| 1399 | Проверить next highest-risk chapter. | Следующий pass должен идти туда, где больше всего влияет на редакционную готовность. |
| 1400 | Сформировать следующий practical pass. | После главы 19 следующая цель выбрана по impact, not chronology. |

## Следующий recommended practical pass

Следующий содержательный pass лучше направить на главу 20 и связку с главой 19:

- убрать возможное дублирование lifecycle/assurance;
- усилить incident response через trace, rollout gate and registry;
- проверить retirement как завершение ADLC, а не отдельную тему;
- обновить companion routes для incident/postmortem, agent registry and retirement evidence.
