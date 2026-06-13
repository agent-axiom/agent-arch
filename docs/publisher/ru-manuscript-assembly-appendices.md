# Сборка рукописи: Приложения

Status: rough print-manuscript assembly for Google Doc sync.

Google Doc target:

- `Архитектура безопасных ИИ-агентов`
- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

Source map:

- `docs/publisher/ru-source-map.md`

## Assembly note

Эта сборка закрывает следующий практический batch: приложения печатной
рукописи. Текст намеренно не переносит все web-приложения один к одному.
Полные схемы трасс, оценок, памяти, подтверждений, lifecycle artifacts,
change/rollout gates, incident records, registry operations, reference package
CLI walkthrough и длинный список источников остаются в online companion.

В печатную рукопись входят четыре коротких приложения:

1. сжатый глоссарий;
2. проверочные списки для архитектурного и launch-review;
3. форма incident/postmortem;
4. curated source list и карта online companion.

Задача batch - дать читателю рабочие опоры после прочтения книги, но не
перегружать финал справочными схемами.

## Body for Google Doc

### Приложения

Приложения в этой книге выполняют другую задачу, чем главы. Главы объясняют
причины, компромиссы и архитектурную последовательность. Приложения дают
короткие рабочие опоры: как быстро вспомнить термин, чем проверить дизайн,
как оформить разбор инцидента и где искать полный справочный материал.

Полные схемы, длинные YAML-примеры, CLI-выводы, каталоги событий и расширенные
шаблоны намеренно остаются в online companion. В печати важно сохранить не
все возможные поля, а те вопросы и формы, которые помогают команде не потерять
управляемость агентной системы.

### Приложение 1. Глоссарий

**Исполняющая среда агента** - слой, где живут запуск, состояние, сбор
контекста, вызовы модели, вызовы возможностей, подтверждения, память и
телеметрия. Это не просто функция рядом с моделью, а управляемый runtime.

**Управляющий слой** - политики, каталог возможностей, подтверждения, шлюзы
поэтапного выпуска, аудит и действия сдерживания. Он отвечает за право видеть,
решать и действовать.

**Граница доверия** - место, где меняется уровень контроля: пользовательский
ввод, найденный документ, память, инструмент, внешняя система, подтверждающий
человек или фоновая задача. Границы доверия нужно явно маркировать в архитектуре.

**Шлюз политик** - точка, где система принимает структурированное решение:
разрешить, запретить, потребовать подтверждение, очистить вход или эскалировать.
Решение политики должно попадать в трассу.

**Каталог возможностей** - управляемый список capabilities: владелец, риск,
transport, read/write mode, principal, idempotency, approval, timeout, retry,
statefulness и lifecycle status.

**Шлюз инструментов** - контрольная точка между reasoning layer и внешним миром.
Он проверяет capability contract, политику, аргументы, principal, tenant boundary,
лимиты и требования подтверждения до выполнения.

**Исполнение в песочнице** - ограниченная среда для адаптеров и инструментов:
сеть, файловая система, секреты, ресурсы, время жизни и профиль исходящих
соединений должны быть явными.

**Краткосрочная память** - состояние текущей сессии или запуска. Она помогает
удерживать контекст, но обычно не должна жить дольше рабочего сценария без
явного решения.

**Долгосрочная память** - сохраняемые сведения, которые переживают одну сессию.
Она требует правил записи, происхождения, пересмотра, удаления и защиты от
загрязнения.

**Профильная память** - проверенные устойчивые факты о пользователе, команде
или рабочем контексте. Это не архив всех сообщений, а ограниченный слой
полезных и разрешенных сведений.

**Извлечение контекста** - выбор релевантных данных из памяти или базы знаний
под конкретный запуск. Хорошее извлечение ограничивает объем, проверяет
источник и не превращает найденный текст в инструкции.

**Происхождение данных** - ответ на вопросы: откуда запись взялась, кто ее
разрешил, какой версии она принадлежит, можно ли ей доверять и можно ли ее
использовать в этом tenant/context.

**Шлюз подтверждения** - interruptible runtime path, где система останавливает
рискованное действие, показывает контекст и побочный эффект, получает решение
и только после этого продолжает или отменяет запуск.

**Трасса** - связанная история одного запуска: запрос, контекст, решения
политик, извлечение, модельные шаги, вызовы инструментов, подтверждения,
ошибки, оценка и финальный результат.

**Спан** - отдельный участок трассы: retrieval, model step, tool call,
approval pause, memory write, verifier step или rollout decision.

**Шлюз поэтапного выпуска** - gate, который решает, можно ли расширять rollout.
Он должен опираться на безопасность, evals, SLO, наблюдаемость, владельцев,
rollback/containment и доказательства из трасс.

**Набор оценочных данных** - версия сценариев, запусков и expected outcomes,
которые проверяют систему перед изменением или после инцидента.

**Проверяющий** - человек, модель или гибридный контракт, который оценивает
процесс, исход, доказательства и attribution failure. Проверяющий должен быть
калиброван и версионирован, если от него зависит выпуск.

**Утвержденный реестр** - управляемый список агентов, runtime templates,
capabilities, gateways, owners, lifecycle states и deprecated paths. Реестр
делает парк агентов подотчетным.

**Вывод из эксплуатации** - закрытие права действовать. Старый агент, capability,
principal, connector, approval path, memory write path or background route
должен потерять возможность влиять на внешний мир.

### Приложение 2. Чеклисты

Эти чеклисты не заменяют архитектурное ревью. Их задача - быстро показать,
где у системы уже есть управляемый контур, а где пока есть только намерение.

**Проверка безопасности**

- Разделены ли пользовательские данные, trusted instructions, retrieved context,
  память, инструменты и внешние системы?
- Есть ли явный субъект действия: user principal, runtime principal,
  tool principal, tenant and approval actor?
- Проходит ли каждый чувствительный шаг через policy decision, а не только
  через prompt?
- Есть ли отдельная граница для write actions and irreversible side effects?
- Можно ли быстро объяснить, почему действие было разрешено, запрещено или
  отправлено на подтверждение?
- Есть ли аудиторский след для policy, approval, tool execution and memory write?

**Проверка памяти и контекста**

- Разделены ли краткосрочная, долгосрочная и профильная память?
- Есть ли правила записи в память, пересмотра и удаления?
- Сохраняется ли provenance у постоянных записей?
- Ограничено ли извлечение по tenant, роли, свежести, объему и доверенности?
- Не может ли найденный документ переписать инструкции агента?
- Есть ли способ обнаружить memory poisoning or stale knowledge?

**Проверка tool gateway**

- У каждой capability есть владелец, риск, read/write mode and lifecycle status?
- Ясно ли, какие tools видит модель, а какие capabilities разрешены runtime?
- Требуют ли write capabilities idempotency key and normalized outcome?
- Различает ли система `success`, `retryable_failure`, `validation_failure`,
  `permission_denied`, `side_effect_unknown` and `partial_side_effect`?
- Есть ли sandbox profile, allowed egress and secret boundary?
- Можно ли отключить одну high-risk capability без полной остановки агента?

**Проверка наблюдаемости и оценок**

- Есть ли `trace_id` у каждого запуска?
- Видны ли spans для retrieval, model step, tool call, approval and memory write?
- Сохраняются ли policy decisions, approval decisions, tool principals and
  outcome classes?
- Есть ли offline eval baseline до rollout?
- Есть ли online signals для drift, escalation rate, approval backlog,
  stuck runs, session expiry and verifier drift?
- Попадают ли инциденты обратно в eval dataset and rollout gates?

**Проверка промышленного запуска**

- Есть ли владелец агента, on-call owner and approval queue owner?
- Проверены ли happy path, bad input, empty retrieval, model failure, policy
  denial, tool timeout, cancel, background route and approval pause?
- Определены ли SLO and failure budgets именно для агентной системы, а не только
  для модели?
- Есть ли rollback or containment action для каждого high-risk path?
- Ограничен ли blast radius через shadow, canary, tenant subset or read-only mode?
- Есть ли registry record and retirement trigger до запуска?

**Проверка жизненного цикла**

- Считаются ли prompt, policy, retrieval, memory, capability, verifier and
  rollout changes release-risk changes?
- Есть ли change packet: что меняется, почему, риск, eval coverage, rollback?
- Можно ли восстановить active artifact bundle for a failed run?
- Есть ли assurance loop после выпуска: detection, response, remediation,
  lifecycle update?
- Можно ли вывести агента или capability из эксплуатации так, чтобы они потеряли
  право действовать?

### Приложение 3. Шаблон incident/postmortem

Используй этот шаблон после этапа сдерживания, когда первые доказательства уже
сохранены. Цель postmortem - не красивый документ, а корректирующие действия:
обновить политики, оценки, rollout gates, registry, lifecycle artifacts or
retirement plan.

**Первые 15 минут**

1. Остановить или сузить рискованную цепочку.
2. Сохранить `trace_id`, `session_id`, `agent_id`, `bundle_id`, `change_id`
   and `rollout_wave`.
3. Проверить, было ли внешнее побочное действие.
4. Зафиксировать `tool_principal`, `approval_id`, `idempotency_key` and active
   policy bundle.
5. Решить, нужно ли отключить capability, connector, principal, memory write
   or rollout wave.

**Краткое описание**

- `incident_id`:
- Дата и время:
- Уровень серьезности:
- Статус:
- Владелец:
- Краткое резюме:

**Что произошло**

- Какой агент или workflow участвовал:
- Какой пользовательский ввод, retrieved context or external trigger запустил
  цепочку:
- Какое рискованное действие, отказ или обход произошли:
- Было ли реальное побочное действие:
- Это единичный запуск или повторяющийся паттерн:

**Активные артефакты**

- `trace_id`:
- `session_id`:
- `bundle_id`:
- `change_id`:
- `rollout_wave`:
- `policy_bundle`:
- `approval_mode`:
- `tool_principal`:
- `idempotency_key`:

Если этот блок нельзя заполнить быстро, проблема уже не только в инциденте.
Команде не хватает наблюдаемости, provenance or lifecycle discipline.

**Сдерживание**

- Что было отключено, ограничено или переведено в mandatory approval:
- Нужен ли rollback:
- Были ли отозваны principals, connectors or delegated authorization:
- Остановлены ли memory writes, background routes or paused approvals:
- Кто владелец временного сдерживания:

**Первопричина**

- Непосредственная причина:
- Сопутствующие факторы:
- Какой gate, policy, verifier, approval, memory rule or rollout assumption
  не сработал:
- Почему существующие evals or detection не поймали проблему раньше:

**Корректирующие действия**

Для каждого действия зафиксируй owner, due date and artifact updated.

- Обновить policy bundle:
- Ужесточить approval mode:
- Добавить targeted eval/regression:
- Обновить rollout gate:
- Изменить capability contract or idempotency path:
- Обновить registry record:
- Создать retirement plan:
- Добавить detection rule:

**Закрытие postmortem**

Инцидент считается закрытым только тогда, когда corrective actions связаны с
артефактами жизненного цикла. Если итогом стал только текстовый разбор, система
почти наверняка повторит тот же класс ошибок.

### Приложение 4. Источники и online companion

Печатная версия не должна тащить весь web source catalog. Для книги важнее
дать читателю устойчивую карту: какие источники задают нормативный каркас, какие
показывают практику платформ, какие помогают строить evals/observability и где
лежит полный companion.

**Нормативный каркас и безопасность**

- OWASP AI Agent Security Cheat Sheet.
- OWASP Top 10 for Agentic Applications.
- OWASP MCP Security Cheat Sheet and MCP Tool Poisoning.
- NIST AI RMF 1.0 and Generative AI Profile.
- NIST SP 800-218A for secure development around generative AI.
- CISA Artificial Intelligence resources.

**Архитектура и платформенная практика**

- OpenAI, A practical guide to building agents.
- OpenAI Agents SDK, Agent Builder, Safety in building agents.
- Anthropic, Building Effective AI Agents.
- Anthropic, Harness design for long-running application development.
- Anthropic, Scaling Managed Agents.
- LangGraph durable execution, persistence, memory and interrupts.
- Model Context Protocol security best practices and authorization.
- Agent2Agent Protocol specification.
- Microsoft Azure Architecture Center, AI Agent Orchestration Patterns.
- Google Cloud Agent Builder and multi-agent system architecture.

**Наблюдаемость, оценки и HITL**

- OpenAI Agent evals and trace grading.
- Microsoft observability for generative AI and agentic AI systems.
- Microsoft Research Guidelines for Human-AI Interaction.
- LangGraph and LangChain human-in-the-loop documentation.
- Anthropic, Demystifying evals for AI agents.
- Research on verifier design, trace observability and multi-turn consistency.

**Governance, assurance and lifecycle**

- Google Research, Security Assurance in the Age of Generative AI.
- Google Research, Securing the AI Software Supply Chain.
- Google materials on securing AI agents and recommended AI controls.
- Microsoft guidance on secure autonomous agentic systems and agentic risk.
- Microsoft guidance on production infrastructure inventory and agent registry.
- Research and incident writeups on agentic misalignment, red teaming and
  liability for AI-assisted systems.

**Online companion**

Полный companion живет в репозитории `agent-axiom/agent-arch` и нужен для
того, что в печатной книге занимало бы слишком много места:

- runnable `agent_runtime_ref` package;
- CLI walkthrough and reference outputs;
- trace/eval/approval/policy/memory/lifecycle/change/incident schemas;
- registry operations handbook;
- policy templates and case-specific worksheets;
- extended recovery patterns for tool failures;
- full source catalog;
- community roadmap and publishing stack notes.

Самое простое правило: книгу используй для аргумента и последовательности,
online companion - для контрактов, проверочных форм и исполнимых деталей.
