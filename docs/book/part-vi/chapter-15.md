# Глава 15. Golden paths, shared gateways и anti-zoo patterns

## 1. Почему даже хорошая орг-модель без инженерных шаблонов быстро расползается

После того как ты определил, кто владеет платформой, а кто продуктом, появляется следующий вопрос: а что именно команды должны переиспользовать на практике?

Если ответа нет, происходит знакомый сценарий:

- каждая команда пишет свой runtime wrapper;
- policy hooks выглядят по-разному;
- tool adapters расходятся по контрактам;
- rollout практики живут в локальных wiki;
- observability wiring копируется вручную и медленно расходится.

То есть формально operating model есть, а по факту у тебя все равно много локальных систем с похожими, но несовместимыми реализациями.

## 2. Golden path это не “best practice документ”, а рабочий путь по умолчанию

Очень важно не путать golden path с набором рекомендаций.

Рекомендации читают выборочно.
Golden path в хорошем platform product выглядит как то, что реально проще взять, чем обойти.

Обычно он включает:

- стартовый runtime template;
- pre-wired tracing и eval hooks;
- policy integration по умолчанию;
- approved tool gateway;
- deployment и rollout defaults;
- примеры типовых product workflows.

То есть золотой путь хорош тогда, когда команде выгодно оставаться на нем.

## 3. Shared gateways нужны, чтобы не размножать критичные ошибки по всей организации

Есть несколько слоев, которые особенно опасно оставлять на локальную импровизацию:

- доступ к внешним capabilities;
- policy enforcement;
- secret handling;
- audit trail;
- approval workflows;
- telemetry emission.

Если каждая команда реализует их сама, организация почти гарантированно размножит одни и те же ошибки в пяти версиях.

Поэтому shared gateway это не бюрократия. Это способ централизованно решить самые дорогие и чувствительные задачи один раз и хорошо.

<div class="diagram-card">
<p>Golden path должен снижать число локальных реализаций критичных слоев</p>

``` mermaid
flowchart LR
    A["Product team A"] --> D["Shared gateway and platform primitives"]
    B["Product team B"] --> D
    C["Product team C"] --> D
    D --> E["Policy, tracing, approvals, capability access"]
```

</div>

## 4. Reusable template должен быть opinionated, а не абстрактным

Очень частая ошибка platform teams: делать template максимально нейтральным, чтобы “подошло всем”.

На практике такой template почти никому не помогает. Он слишком общий и требует столько ручной сборки, что команды все равно уходят в кастомную реализацию.

Хороший template обычно opinionated:

- задает базовую структуру run;
- уже включает policy hooks;
- already wired to tracing;
- имеет approved deployment path;
- содержит working examples;
- поддерживает ограниченное число extension points.

Да, это менее “универсально”. Но это гораздо полезнее для реальной организации.

## 5. Не нужно пытаться сделать один golden path для всех типов агентов

Здесь тоже важна зрелость. Один путь редко одинаково хорош для:

- Q&A agents;
- workflow agents;
- approval-heavy agents;
- high-risk action agents;
- internal copilots.

Поэтому practical подход обычно такой:

- один базовый platform core;
- 2-4 типовых golden paths;
- shared gateway и observability substrate;
- controlled deviations для special cases.

Это лучше, чем либо один giant template для всего мира, либо полный хаос.

## 6. Anti-zoo pattern начинается с ограничения свободы в правильных местах

Термин “platform zoo” обычно означает одно и то же:

- слишком много runtimes;
- слишком много способов подключать tools;
- слишком много локальных policy engines;
- слишком много разных telemetry schemas;
- слишком много почти одинаковых wrapper-слоев.

Уменьшать этот зоопарк полезно не через запреты на все подряд, а через ясные ограничения:

- единый contract layer;
- единый shared gateway;
- ограниченный набор supported runtime patterns;
- platform review для risky deviations;
- deprecation policy для старых обходных путей.

## 7. Пример platform defaults policy

Ниже очень практичный шаблон, который показывает, как оформить golden path и deviations явно:

```yaml
platform_defaults:
  required:
    - shared_tool_gateway
    - standard_trace_schema
    - policy_hooks
    - eval_gate_in_ci
  supported_templates:
    - qa_agent
    - workflow_agent
    - approval_agent
  deviations_require_review:
    - custom_runtime
    - direct_tool_access
    - custom_telemetry_schema
    - bypass_of_policy_layer
```

Такая политика не убивает скорость. Она убирает неявность.

## 8. Shared gateways хороши не только для безопасности, но и для скорости эволюции

Когда critical path централизован, platform team может:

- обновлять contracts в одном месте;
- улучшать audit trail один раз на всех;
- менять rollout guardrails без переписывания десятка продуктов;
- быстрее внедрять новые policy capabilities;
- быстрее чинить массовые operational issues.

То есть shared gateway это не только контроль. Это еще и масштабируемость инженерных улучшений.

## 9. Что чаще всего ломается в anti-zoo efforts

Здесь тоже много типовых ошибок:

- golden path слишком тяжелый, и его обходят;
- shared gateway слишком медленный или неудобный;
- exceptions становятся обычной практикой;
- templates быстро устаревают;
- platform team не отслеживает, где команды реально сходят с пути;
- deprecation обещана, но never enforced.

Тогда организация формально говорит о стандартизации, а фактически просто производит новые варианты старого хаоса.

## 10. Что стоит измерять, если ты правда борешься с зоопарком

Полезные operational метрики здесь такие:

- число локальных runtime forks;
- число direct tool access paths мимо gateway;
- доля агентов на supported templates;
- median time to launch a new workflow on golden path;
- число active deviations без owner;
- time to deprecate unsafe patterns.

Это намного полезнее, чем просто считать “сколько команд используют платформу”.

## 11. Practical checklist

Если хочешь быстро проверить anti-zoo strategy, пройди по вопросам:

- Есть ли у тебя реальный golden path, который проще использовать, чем обходить?
- Есть ли shared gateway для чувствительных capability?
- Ограничен ли набор поддерживаемых runtime patterns?
- Видны ли deviations и есть ли у них owner?
- Умеет ли платформа deprecate unsafe local patterns?
- Снижает ли новый platform layer реально число копипасты и локальных форков?

Если на несколько вопросов подряд ответ “нет”, значит ты пока строишь не platform product, а просто библиотеку с благими намерениями.

## 12. Что читать дальше

Следующий логичный шаг в Part VI: добить тему организационной модели через паттерны platform roadmap, adoption и lifecycle management. А дальше уже переходить к reference implementation.

- [Глава 14. Platform team vs product teams](chapter-14.md)
- [Глава 16. Базовый runtime blueprint](../part-vii/chapter-16.md)
- [Часть VI. Организационная модель](index.md)
- [Источники](../../appendix/sources.md)
