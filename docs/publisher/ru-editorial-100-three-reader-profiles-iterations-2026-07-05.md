# RU 100 Three Reader Profiles Editorial Iterations

Date: 2026-07-05.

Purpose: record 100 controlled editorial iterations that make the manuscript more recommendable for three reader profiles: technical lead / architect, engineering manager / CTO, and practicing developer.

| # | Area | Goal | Result | Verification |
| --- | --- | --- | --- | --- |
| 1 | Входная рамка архитектора | Сделать явным, что книга помогает принимать архитектурные решения, а не только понимать агентные термины. | Добавлен маршрут для технического лидера и архитектора. | Найден заголовок "Для технического лидера и архитектора". |
| 2 | Граница доверия | Проверить, что архитектор сразу видит границу доверия как главный объект проектирования. | Во вводном маршруте названа граница доверия. | Фраза о границе доверия присутствует во введении. |
| 3 | Capability как интерфейс | Подсветить capability как предмет ревью, а не как внутреннюю деталь реализации. | В part-level блоках capability связан с правом действия. | Часть II содержит архитектурный исход про контракты. |
| 4 | Трассы как доказательство | Показать, что trace нужен не для логирования, а для доказательства решения. | В архитектурной траектории упомянуты трассы и доказательная цепочка. | Часть V содержит исход про цепочку доказательств. |
| 5 | Оценки и выпуск | Связать evals с решением о выпуске, чтобы архитектор не воспринимал их как отдельный отчет. | В маршруте и Part V названы оценки и шлюзы выпуска. | Chapter forwarding hook для главы 16 найден. |
| 6 | Владение жизненным циклом | Показать, что владение и вывод из эксплуатации являются архитектурными решениями. | В маршруте архитектора назван жизненный цикл. | Часть VI содержит исход про ADLC и контур заверения. |
| 7 | ADR-совместимость | Дать архитектору понятный способ использовать книгу рядом с ADR и threat model. | Вводный маршрут говорит о карте решений рядом с ADR, угрозами и SLO. | Фраза ADR присутствует в Markdown и DOCX. |
| 8 | Переход от демо к платформе | Сделать первый part-level исход решением о форме инициативы. | Часть I говорит о выборе между агентом, workflow и платформенным компонентом. | Part optics count равен 7. |
| 9 | Security review | Сделать безопасность обсуждаемой через архитектурные контракты. | Часть II формулирует контракты границ доверия, политик и журнала. | Part II optics содержит архитекторскую строку. |
| 10 | Memory review | Перевести память из функции продукта в архитектурный слой с правилами. | Часть III описывает разные правила записи, чтения, происхождения и удаления. | Part III optics содержит архитекторскую строку. |
| 11 | Tool review | Показать инструменты как каталог возможностей, а не список функций. | Часть IV описывает каталог возможностей, адаптеры, песочницу и идемпотентность. | Part IV optics содержит архитекторскую строку. |
| 12 | Reliability review | Сделать reliability-слой частью архитектурного решения. | Часть V связывает трассы, SLO, оценки и выпуск. | Part V optics содержит архитекторскую строку. |
| 13 | Operating model review | Сделать организационную модель частью архитектуры. | Часть VI связывает владельцев, золотые пути, ADLC и заверение. | Part VI optics содержит архитекторскую строку. |
| 14 | Runtime review | Показать финальный proof как проверяемую среду исполнения. | Часть VII говорит о runtime, политиках и launch checklist. | Part VII optics содержит архитекторскую строку. |
| 15 | Командное ревью | Добавить повод использовать главы на architecture review. | Добавлены 23 строки "Почему главу стоит переслать". | Markdown and DOCX count = 23. |
| 16 | Глава 1 forwarding | Сделать главу 1 полезной для спора о магии модели. | Добавлен forwarding hook про владельца действия. | Hook главы 1 найден. |
| 17 | Глава 3 forwarding | Сделать референсную архитектуру общей картой для разных ролей. | Hook главы 3 говорит о единой карте для архитектора, разработчика и руководителя. | Hook главы 3 найден. |
| 18 | Глава 4 forwarding | Перевести безопасность в проверяемые границы доверия. | Hook главы 4 говорит о конкретных границах в дизайне и коде. | Hook главы 4 найден. |
| 19 | Глава 10 forwarding | Сделать каталог инструментов темой архитектурного ревью. | Hook главы 10 говорит о ревью и версионировании платформенного интерфейса. | Hook главы 10 найден. |
| 20 | Глава 16 forwarding | Подсветить цепочку доказательств как материал ревью. | Hook главы 16 говорит о proof chain. | Hook главы 16 найден. |
| 21 | Глава 23 forwarding | Превратить финальный чеклист в gate, а не приложение. | Hook главы 23 говорит о практическом gate перед запуском. | Hook главы 23 найден. |
| 22 | Оглавительная структура | Убедиться, что краткая структура не потеряла части после правок. | Восстановлены части IV-VI в книжной структуре. | Short structure parts = 7. |
| 23 | Главные части | Убедиться, что основное тело имеет все семь частей. | Part-level blocks вставлены после main part headings. | Main parts = 7. |
| 24 | Проверка недостающей Part V в DOCX | Закрыть структурную дырку raw DOCX перед Google Doc sync. | В DOCX добавлен Heading 1 для Части V перед главой 13. | DOCX Heading 1 parts = 7. |
| 25 | Согласованность Markdown/DOCX | Сделать одинаковыми контрольные элементы в source и proof. | Одинаковые counts для profile, team, optics и forwarding hooks. | Both surfaces report 1/1/7/23. |
| 26 | Снижение абстрактности | Заменить общую мотивацию на конкретные решения архитектора. | Во введении перечислены boundaries, capabilities, traces, evals, rollout и ownership. | Route text verified. |
| 27 | Рекомендательность | Сделать каждую главу пригодной для пересылки конкретному адресату. | Добавлен короткий reason-to-forward после командного takeaway. | 23 hooks verified. |
| 28 | Проверка тона | Сохранить инженерную прямоту без маркетингового шума. | Новые блоки формулируют решения, риски и артефакты. | No generic praise-only block added. |
| 29 | Проверка плотности | Не превращать pass в длинное повторение. | Part blocks короткие, chapter hooks однофразовые. | No long paragraph gate will be checked in DOCX QA. |
| 30 | Architect handoff | Подготовить итоговый отчет для архитектурного профиля. | Architect outcomes included in pass report plan. | Report file will summarize this group. |
| 31 | Executive route | Сделать отдельный маршрут для руководителя инженерии или CTO. | Добавлен маршрут во введении. | Заголовок маршрута найден. |
| 32 | Risk language | Показать книгу как карту управляемого риска. | Маршрут руководителя говорит о risk acceptance. | Фраза про управляемый риск найдена. |
| 33 | Ownership | Подсветить владельцев как управленческое решение. | Новые блоки говорят о владельце риска, владельцах capability и ownership. | Ownership references verified by text scan. |
| 34 | Stop-the-line | Сделать право остановки выпуска явным вопросом руководителя. | Во введении добавлен вопрос, кто сможет остановить выпуск. | Team handoff block found. |
| 35 | Rollout decision | Связать rollout с управленческим решением, а не только с техникой. | Part V и intro route говорят о продолжении, остановке или откате. | Part V manager line found. |
| 36 | Incident learning | Показать инциденты как источник управления системой. | Part VI и Chapter 20 forwarding hook говорят о заверении и инцидентах. | Chapter 20 hook found. |
| 37 | Platform chaos | Показать платформу как способ снизить хаос. | Маршрут руководителя говорит о снижении хаоса вместо исключений. | Intro route verified. |
| 38 | Demo risk | Сделать риск демо без владельца видимым уже в Part I. | Part I manager line говорит про дорогое демо без владельца риска. | Part I manager line found. |
| 39 | Security conversation | Перевести безопасность из страха в решения о полномочиях. | Part II manager line прямо формулирует эту смену. | Part II manager line found. |
| 40 | Knowledge debt | Показать память как организационный долг. | Part III manager line говорит о свежести, приватности, арендаторах и праве забыть. | Part III manager line found. |
| 41 | Integration risk | Подсветить стоимость побочных эффектов интеграций. | Part IV manager line говорит, что side effect дороже ответа модели. | Part IV manager line found. |
| 42 | Release governance | Дать руководителю язык для решения о выпуске. | Part V manager line говорит о продолжении, остановке и откате. | Part V manager line found. |
| 43 | Operating model | Подсветить модель команд как часть зрелости. | Part VI manager line говорит о командах, бюджете риска и выводе из эксплуатации. | Part VI manager line found. |
| 44 | Readiness criterion | Сделать критерий готовности частью управленческого обсуждения. | Part VII manager line говорит о доказательствах перед волной выпуска. | Part VII manager line found. |
| 45 | Leadership handoff | Добавить отдельный блок про разговор с руководством. | Добавлен "Как сделать книгу полезной для команды". | Block count = 1. |
| 46 | Chapter 17 forwarding | Сделать владение платформой поводом переслать главу. | Hook главы 17 говорит, что ownership важнее framework choice. | Hook главы 17 found. |
| 47 | Chapter 18 forwarding | Показать ценность золотых путей для снижения хаоса. | Hook главы 18 говорит о golden paths и shared gateways. | Hook главы 18 found. |
| 48 | Chapter 19 forwarding | Связать ADLC с процессом разработки. | Hook главы 19 говорит о lifecycle instead of experiment. | Hook главы 19 found. |
| 49 | Chapter 20 forwarding | Сделать заверение, реестр и retirement общим языком руководителя и команды. | Hook главы 20 формулирует этот язык. | Hook главы 20 found. |
| 50 | Management brevity | Сохранить управленческие формулировки короткими. | Manager outcomes добавлены одной строкой на часть. | Part optics remain compact. |
| 51 | Not a business book | Не уводить рукопись в generic management prose. | Все manager lines привязаны к архитектурным рискам и proof obligations. | No standalone generic leadership chapter added. |
| 52 | Decision review | Сделать chapters useful for decision meetings. | Chapter hooks say what chapter helps decide. | 23 forwarding hooks verified. |
| 53 | Risk owner | Сделать владельца риска повторяемым мотивом. | Part I and team block mention owner/stop decision. | Text scan finds owner/risk wording. |
| 54 | Budget of risk | Связать риск с budget and rollout. | Part VI and Part V mention budget/risk/rollout. | Text scan verified. |
| 55 | Incident process | Проверить, что incident conversation remains visible. | Team handoff and Chapter 20 hook keep incidents visible. | Hook verified. |
| 56 | Exec readability | Добавить быстрый executive reading path without bloating chapters. | Executive route is in intro only; part lines summarize outcomes. | No chapter-level manager subsections added. |
| 57 | Recommendation social object | Сделать главу объектом командной пересылки. | Every chapter has "why forward" line. | Count = 23. |
| 58 | Manager handoff report | Подготовить итоговый отчет, где перечислены author-owned blockers. | Report will include author-owned fields. | Report file planned. |
| 59 | Publisher relevance | Показать издателю, что книга адресует не одну роль. | Three-profile pass report will name all profiles. | Report plan includes profiles. |
| 60 | Management QA | Проверить, что управленческие additions appear in Google Doc readback. | Planned readback phrase: "Читай книгу как карту управляемого риска". | Readback gate defined. |
| 61 | Developer route | Сделать отдельный маршрут для практикующего разработчика. | Добавлен route во введении. | Heading found. |
| 62 | PR usefulness | Сформулировать практический критерий: вопрос должен проверяться в pull request. | Developer route includes PR check framing. | Phrase found. |
| 63 | Capability contract | Показать первый concrete artifact for developers. | Developer route names capability contract. | Route text verified. |
| 64 | Policy decision | Добавить policy decision как практический объект. | Developer route names policy decision. | Route text verified. |
| 65 | Trace record | Добавить trace as implementation target. | Developer route names trace record. | Route text verified. |
| 66 | Eval set | Добавить eval as runnable check. | Developer route names eval set. | Route text verified. |
| 67 | Release gate | Добавить release gate as deployable control. | Developer route names release gate. | Route text verified. |
| 68 | Incident card | Добавить incident card as operational artifact. | Developer route names incident card. | Route text verified. |
| 69 | Runtime skeleton | Добавить минимальную среду исполнения as concrete target. | Developer route names runtime. | Route text verified. |
| 70 | Part I developer outcome | Сделать первую часть action-oriented. | Part I developer line asks for component map and allowed actions. | Part I developer line found. |
| 71 | Part II developer outcome | Сделать безопасность проверяемой в code. | Part II developer line asks for tool, confirmation and audit in code. | Part II developer line found. |
| 72 | Part III developer outcome | Сделать memory contract testable. | Part III developer line asks for retrieval contract and memory record. | Part III developer line found. |
| 73 | Part IV developer outcome | Сделать execution layer implementable. | Part IV developer line names tool gateway, retries, limits and rollback. | Part IV developer line found. |
| 74 | Part V developer outcome | Сделать observability/eval layer runnable. | Part V developer line names events, checks and release gate. | Part V developer line found. |
| 75 | Part VI developer outcome | Сделать lifecycle artifacts concrete. | Part VI developer line asks what artifacts should live near code. | Part VI developer line found. |
| 76 | Part VII developer outcome | Сделать final implementation incremental. | Part VII developer line names project skeleton, contracts and gate. | Part VII developer line found. |
| 77 | Chapter 6 developer hook | Make risky tool launch actionable. | Hook asks about confirmation, audit and rollback. | Hook found. |
| 78 | Chapter 9 developer hook | Make context assembly concrete. | Hook connects answer quality to context assembly and provenance. | Hook found. |
| 79 | Chapter 11 developer hook | Make MCP integration safety concrete. | Hook warns about isolation error becoming operational risk. | Hook found. |
| 80 | Chapter 12 developer hook | Make idempotency a team discussion. | Hook asks to agree on retries, limits and rollback. | Hook found. |
| 81 | Chapter 13 developer hook | Make trace format shareable. | Hook says trace avoids guessing through logs. | Hook found. |
| 82 | Chapter 15 developer hook | Make evals production-protective. | Hook says behavior must be checked before/after release. | Hook found. |
| 83 | Chapter 21 developer hook | Make runtime useful immediately. | Hook points to constrained and observable minimal runtime. | Hook found. |
| 84 | Chapter 22 developer hook | Make policies code-adjacent. | Hook says capability catalog lives near code. | Hook found. |
| 85 | Chapter 23 developer hook | Make launch checklist operational. | Hook says final gate makes release decision discussable. | Hook found. |
| 86 | Code-adjacent wording | Keep English technical labels only where useful. | New text uses Russian framing around ADR, SLO, release gate and pull request. | Anglicism scan will be run. |
| 87 | No new code listings | Avoid adding unverified code in this editorial pass. | Only prose and decision hooks were added. | No fenced code added by this pass. |
| 88 | Practical density | Add action without bloating every chapter. | One line per chapter plus one line per part. | Diff size remains bounded. |
| 89 | Developer report | Document developer-facing outcomes in final report. | Report will include implementation counts and verification. | Report plan includes developer profile. |
| 90 | Developer Google readback | Verify developer route reaches Google Doc. | Planned readback phrase: "контракт возможности, решение политики". | Readback gate defined. |
| 91 | Markdown structural count | Verify seven short-structure and seven main parts. | Counts checked after repair. | short=7, main=7. |
| 92 | DOCX structural count | Verify DOCX has seven Heading 1 parts. | Missing Part V heading added before Chapter 13. | Heading1 parts=7. |
| 93 | Control block count | Verify all new control blocks exist on both source surfaces. | Counts checked for profile, team, optics, forwarding hooks. | Markdown and DOCX both report 1/1/7/23. |
| 94 | Template rebuild | Rebuild Template2000n after raw DOCX patch. | Scheduled through existing builder. | Metrics JSON will report text_equality. |
| 95 | Google Doc sync | Replace existing Google Doc content with updated raw DOCX. | Scheduled through Drive connector update. | Readback will verify three profile phrases. |
| 96 | Render QA | Render raw and Template proof files. | Scheduled through render_docx.py and render_qa_metrics.py. | Expected no blank-like pages. |
| 97 | Duplicate audit | Check exact duplicate long paragraphs. | Scheduled in structural QA script. | Expected zero duplicate groups >=35 words. |
| 98 | Long paragraph audit | Check dense paragraph risk in DOCX. | Scheduled in structural QA script. | Expected zero paragraphs >=250 words. |
| 99 | Docs build | Verify repository docs still build. | Scheduled mkdocs strict build. | Expected exit 0 with known nav warnings. |
| 100 | Git handoff | Commit and push only files from this pass. | Scheduled final git status, commit and push. | Old unrelated untracked txt remains untouched. |
