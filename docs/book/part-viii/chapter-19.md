# Глава 19. От SDLC к ADLC

## 1. Почему здесь вообще нужно вспоминать классический SDLC

Когда команды начинают строить агентные системы, у них часто возникает соблазн объявить, что “старые процессы больше не работают” и теперь нужен какой-то совершенно новый жизненный цикл.

Это плохая отправная точка.

Классический software development lifecycle по-прежнему нужен, потому что именно он задает базовую инженерную дисциплину:

- постановку требований;
- дизайн;
- реализацию;
- тестирование;
- выпуск;
- эксплуатацию;
- вывод из эксплуатации.

NIST в своем AI-профиле к SSDF прямо исходит из той же идеи: secure development practices для generative AI нужно не изобретать с нуля, а расширять поверх существующей secure software discipline.[^nist-ssdfa]

То есть агентная система не отменяет SDLC. Она делает его недостаточным в исходном виде.

В этом и состоит главная задача этой главы. Она нужна не для того, чтобы просто переименовать жизненный цикл новыми буквами. Она должна показать, почему системе, собранной в части VII, теперь нужна такая рамка жизненного цикла, которая удержит во времени поведение модели, движение политик, drift в retrieval, побочные эффекты инструментов, evidence и решения о выводе из эксплуатации.

## 2. Что в SDLC остается тем же

Если убрать хайп, в агентной системе остается много очень знакомого:

- требования все так же нужно формулировать заранее;
- архитектурные решения все так же нужно ревьюить;
- у интеграций все так же должны быть owner и contracts;
- рискованные изменения все так же должны проходить через controlled release;
- инциденты все так же требуют postmortem и corrective actions.

Это важный психологический момент для команды: ADLC не должен выглядеть как “магия поверх инженерии”. Он должен выглядеть как взрослая надстройка над уже знакомым SDLC.

## 3. Что в агентных системах ломает классический процесс

Вот здесь и начинается реальная разница.

У обычной системы многое определяется кодом и сравнительно детерминированным поведением. У агентной системы появляется дополнительный слой изменчивости:

- поведение модели вероятностно;
- prompt и routines влияют на результат не хуже кода;
- retrieval и memory меняют вход в систему без изменения business logic;
- tools создают реальные побочные эффекты;
- изменения policy могут менять поведение целого класса задач;
- online drift может появиться даже без “поломки” релиза.

Именно поэтому NIST AI RMF GenAI Profile подчеркивает, что trustworthiness considerations должны жить не только в момент релиза, а на всем жизненном цикле: design, development, use и evaluation.[^nist-genai]

## 4. ADLC полезно мыслить как SDLC плюс новые поверхности изменений

Самая рабочая инженерная рамка здесь простая:

`ADLC = SDLC + model behavior + prompts/routines + policies + retrieval/memory + tools + evals + governed autonomy`

То есть новый жизненный цикл появляется не потому, что “агенты особенные”, а потому, что у них больше подвижных поверхностей, за которыми нужно отдельно следить при выпуске и эксплуатации. Главный артефакт этой главы — ADLC state model: карта состояний и переходов, а не еще один общий governance checklist.

<div class="diagram-card">
<p>Полезно думать об ADLC как о расширении классического SDLC, а не как о его замене</p>

``` mermaid
flowchart LR
    A["Классический SDLC"] --> B["Требования"]
    A --> C["Дизайн"]
    A --> D["Реализация"]
    A --> E["Тестирование"]
    A --> F["Выпуск"]
    A --> G["Эксплуатация"]
    A --> H["Вывод из эксплуатации"]

    H --> I["ADLC добавляет"]
    I --> J["Поведение модели"]
    I --> K["Промпты и routines"]
    I --> L["Политики и approvals"]
    I --> M["Retrieval и память"]
    I --> N["Побочные эффекты инструментов"]
    I --> O["Evals и управляемая автономия"]
```

</div>

## 5. Какие артефакты теперь становятся release-bearing

В обычном SDLC команда чаще всего спорит вокруг кода, инфраструктуры и схем данных. В ADLC список артефактов, несущих релизный риск, шире:

- model selection и routing;
- system instructions и routines;
- policy configs;
- capability contracts;
- retrieval corpus;
- memory write rules;
- eval datasets;
- approval policies;
- rollout gates.

!!! example "Сквозной кейс: дубли как ADLC-change"
    В support-triage системе исправление инцидента с дублем тикета не заканчивается патчем retry-кода. Артефактами, несущими релизный риск, становятся новый eval dataset, policy bundle для `side_effect_unknown`, capability contract для `create_support_ticket`, rollout gate для canary и trace schema, по которой потом можно расследовать outcome. В ADLC все эти изменения должны идти как один проверяемый change set, иначе команда выпустит код, но оставит жизненный цикл сломанным.

Это один из самых важных операционных сдвигов. Если команда считает релизом только изменение кода, она почти наверняка пропустит рискованные agent changes.

## 6. Почему в ADLC одних tests уже недостаточно

Тесты остаются важными, но их уже мало.

В агентных системах нужен более широкий контур assurance:

- deterministic tests для кода и контрактов;
- offline evals для known scenarios;
- simulators или scenario-based checks для многоходового поведения;
- online monitoring для drift и emergent failures;
- policy checks для risky paths;
- approval and rollout gates для ограничения радиуса воздействия.

OpenAI и Anthropic с разных сторон приходят к той же практической мысли: сначала нужен baseline behavior, потом controlled iteration, а не “сразу автономия и посмотрим, что выйдет”.[^openai-guide][^anthropic-agents]

## 7. Отдельный жизненный цикл нужен и для security assurance

Для обычного сервиса security review часто сосредоточен вокруг кода, зависимостей, инфраструктуры и доступа. Для агентной системы этого мало.

Google Research хорошо показывает, что security assurance здесь лучше собирать как постоянный контур, а не разовый security review: red teaming, vulnerability management, detection and response, threat intelligence и remediation должны жить рядом с выпуском системы, а не после него.[^google-assurance]

Это важная мысль для книги: agent security нельзя сводить к prompt injection checklist. Это полноценная эксплуатационная функция.

## 8. Supply chain агента шире, чем просто пакетные зависимости

Еще одна полезная поправка из Google: AI software supply chain включает не только библиотеки и контейнеры, но и provenance для моделей, данных, конфигов, пайплайнов и артефактов обучения или оценки.[^google-supply-chain]

Для агентной системы это особенно важно, потому что иначе ты не сможешь ответить на вопросы:

- откуда взялась эта модель;
- каким dataset'ом проверяли этот релиз;
- какой policy bundle был в проде;
- какой retrieval corpus использовался;
- какой prompt/routine изменился между двумя волнами rollout.

То есть provenance в ADLC нужен не “для красоты”, а для нормального change management и incident investigation, включая восстановление экспортированных свидетельств failed run, например `failure_reason`, когда release path уходит в degraded state.

## 9. Хороший ADLC начинается не с релиза, а с intake и design review

Если агентная инициатива попадает в инженерную систему только в момент, когда “вот уже что-то собрали”, ты почти гарантированно поздно увидишь архитектурные и governance-проблемы.

Полезно иметь ранние вопросы по стадиям жизненного цикла:

- здесь правда нужен агент, а не обычный workflow;
- какой у системы autonomy budget;
- какие side effects вообще допустимы;
- где будут trust boundaries;
- какие capabilities будут high-risk;
- нужен ли memory layer;
- какие evals должны существовать до пилота.

Вот это уже и есть первые шаги ADLC.

## 10. Предлагаемая рамка ADLC

Для production-grade агентной системы я бы рекомендовал минимум такие стадии:

1. Прием инициативы и проверка уместности агента
2. Архитектурное и safety design review
3. Сборка и интеграция
4. Базовая линия evals
5. Поэтапный rollout
6. Устойчивая эксплуатация
7. Incident response и corrective actions
8. Вывод из эксплуатации или замена

<div class="diagram-card">
<p>ADLC полезно мыслить как непрерывный контур, а не как путь до первой выкладки</p>

``` mermaid
flowchart LR
    A["Прием инициативы"] --> B["Design review"]
    B --> C["Сборка и интеграция"]
    C --> D["Базовая линия eval"]
    D --> E["Поэтапный rollout"]
    E --> F["Эксплуатация"]
    F --> G["Инциденты и corrective actions"]
    G --> H["Вывод из эксплуатации или замена"]
    H --> A
```

</div>

## 11. Чем ADLC полезен команде на практике

Если назвать все это просто “лучшими практиками”, команда обычно воспринимает их как необязательные советы.

Если назвать это моделью жизненного цикла, появляются более зрелые вопросы:

- на какой стадии мы сейчас;
- чего нам не хватает, чтобы перейти дальше;
- какой artifact должен быть готов на этой стадии;
- кто owner у следующего gate;
- какой риск мы берем, если перескакиваем этап.

Именно это и делает ADLC полезным: он превращает разговор про агентов из hype discussion в управляемую инженерную программу.

## 12. Чего не стоит делать

Есть несколько очень частых ошибок:

- объявить, что для агентов “обычная инженерия больше не работает”;
- считать ADLC просто новым названием для prompt iteration;
- думать, что rollout checklist автоматически покрывает весь жизненный цикл;
- не считать prompt, policy и retrieval release-bearing changes;
- не связывать evals с change management;
- не планировать retirement discipline заранее.

Если так делать, ADLC превращается в красивое слово без операционной пользы.

## 13. Практический чеклист

Если хочешь быстро понять, нужен ли тебе уже полноценный ADLC, пройди по вопросам:

- У вас есть не только кодовые, но и prompt/policy/model changes?
- У системы есть risky side effects?
- Есть ли retrieval, memory или mutable knowledge surfaces?
- Требуются ли evals для принятия release decisions?
- Есть ли staged rollout, approval gates и incident review?
- Нужно ли объяснять, какой exact artifact был в проде в момент инцидента?

Если на несколько вопросов подряд ответ “да”, вы уже живете не просто в SDLC, а в ADLC, даже если пока его так не называете.

## 14. Что читать дальше

Эту главу удобно читать вместе с более ранними разделами про оценки, выкладку и организационную модель:

- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../part-v/chapter-13.md)
- [Глава 18. Чеклист промышленного запуска](../part-vii/chapter-18.md)
- [Часть VI. Организационная модель](../part-vi/index.md)
- [Источники](../../appendix/sources.md)

[^nist-ssdfa]: [NIST SP 800-218A: Secure Software Development Practices for Generative AI and Dual-Use Foundation Models](https://csrc.nist.gov/pubs/sp/800/218/a/final)
[^nist-genai]: [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
[^openai-guide]: [OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^anthropic-agents]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
