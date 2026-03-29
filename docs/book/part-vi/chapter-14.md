# Глава 14. Platform team vs product teams

## 1. Почему агентная платформа почти всегда ломается не на коде, а на модели владения

На раннем этапе все обычно выглядит просто: есть несколько энтузиастов, один-два агента, пара интеграций, быстрые эксперименты. Это нормально.

Проблемы начинаются позже:

- продуктовые команды делают свои локальные agent runtimes;
- каждая команда по-своему пишет policy checks;
- observability собирается в трех несовместимых форматах;
- tool adapters дублируются;
- никто не уверен, кто должен чинить platform-grade инциденты.

То есть технически система может даже работать, но организационно она уже начинает расползаться.

## 2. Платформенная команда не должна забирать у продуктов все решения

Есть плохая крайность: platform team пытается стать единственной точкой принятия любых agent decisions.

Тогда получается:

- платформа становится bottleneck;
- продуктовые команды теряют скорость;
- все изменения упираются в одну очередь;
- platform layer разрастается до неповоротливого комбайна.

Это нерабочая модель. Платформенная команда нужна не для того, чтобы писать все агентские фичи самой, а для того, чтобы давать устойчивые общие слои и безопасные пути по умолчанию.

## 3. И обратная крайность тоже плохая: полный федерализм

Иногда компании идут в другую сторону: “пусть каждая команда сама решает, как ей строить агентов”.

Это быстро дает:

- несовместимые contracts;
- разный security posture;
- разное качество evals;
- разную observability;
- локальные платформы внутри каждой команды.

На короткой дистанции это выглядит как свобода. На длинной это почти всегда зоопарк.

## 4. Зрелая модель обычно выглядит как platform + product split

Хороший operating model обычно делит ответственность примерно так:

`platform team` отвечает за:

- orchestration primitives;
- policy framework;
- tool and capability contracts;
- observability and eval substrate;
- shared gateways;
- baseline security model.

`product teams` отвечают за:

- user workflows;
- product-specific prompts and policies;
- domain logic;
- acceptance criteria for task success;
- интеграцию платформенных примитивов в конкретный продукт.

<div class="diagram-card">
<p>Платформа и продукт не должны дублировать друг друга, у них разный слой ответственности</p>

``` mermaid
flowchart LR
    A["Platform team"] --> B["Runtime, policy, observability, gateways"]
    C["Product teams"] --> D["User workflows, domain logic, UX outcomes"]
    B --> E["Golden paths and shared primitives"]
    D --> E
```

</div>

## 5. Платформа должна давать golden paths, а не просто набор low-level деталей

Если platform team поставляет только “конструктор из запчастей”, продуктовые команды все равно начнут собирать системы по-разному.

Golden path обычно включает:

- базовый runtime template;
- готовые policy hooks;
- стандартный tracing/eval wiring;
- approved tool gateway pattern;
- рекомендации по memory usage;
- rollout and regression defaults.

То есть хороший platform product помогает не только “мочь”, но и “делать правильно по умолчанию”.

## 6. Ownership должен быть явным на каждом слое

Очень полезно заранее разложить, кто владеет чем:

- кто меняет platform contracts;
- кто утверждает новые write-capabilities;
- кто владеет policy schemas;
- кто отвечает за telemetry schema;
- кто on-call за platform incidents;
- кто решает, когда продукту можно отойти от golden path.

Если ownership размыт, почти любой инцидент превращается в длинный организационный пинг-понг.

## 7. Не все отклонения от платформы нужно запрещать, но их нужно делать осознанными

Иногда продуктовой команде правда нужен special case:

- нестандартный workflow;
- отдельная capability;
- другой latency/cost trade-off;
- экспериментальный rollout.

Это нормально. Но разница между зрелой платформой и хаосом в том, что deviation:

- виден;
- обсужден;
- ограничен по blast radius;
- имеет owner;
- не становится тихим новым стандартом.

## 8. Пример governance policy для agent platform

Ниже очень практичный шаблон:

```yaml
governance:
  platform_owned:
    - runtime_contracts
    - policy_framework
    - telemetry_schema
    - shared_tool_gateway
  product_owned:
    - workflow_logic
    - domain_prompts
    - task_success_criteria
  requires_platform_review:
    - new_write_capability
    - custom_policy_engine
    - telemetry_schema_change
    - direct_external_tool_access
```

Такой YAML не решает все организационные проблемы, но он очень хорошо снимает вечный вопрос “а кто вообще это должен решать?”.

## 9. Платформа должна измеряться не числом фич, а снижением хаоса

Очень важно не попадать в ловушку vanity metrics вроде:

- сколько tools добавили;
- сколько MCP servers подняли;
- сколько продуктовых команд “подключились”.

Сильная платформа должна уменьшать:

- дублирование;
- число кастомных обходов;
- стоимость добавления нового workflow;
- время расследования инцидентов;
- число unsafe deviations.

Иначе ты можешь много строить, но не становиться системно лучше.

## 10. Что чаще всего ломается в operating model

Обычно проблемы повторяются:

- платформа становится bottleneck для всех решений;
- продукты полностью обходят платформу;
- ownership неясен;
- reusable primitives слишком низкоуровневые;
- нет процесса для deviations;
- platform roadmap не связан с pain points продуктовых команд.

Это приводит к классической развилке: либо платформа никому не помогает, либо продукты считают ее препятствием.

## 11. Practical checklist

Если хочешь быстро проверить operating model, пройди по вопросам:

- Ясно ли, что именно owned by platform team?
- Ясно ли, что остается за product teams?
- Есть ли golden path, а не только “набор возможностей”?
- Понятно ли, кто approve'ит новые risky capabilities?
- Есть ли процесс для отклонений от стандартного пути?
- Уменьшает ли платформа реально число локальных runtime-реализаций?

Если на несколько вопросов подряд ответ “нет”, у тебя, скорее всего, уже не техническая проблема, а проблема организационного дизайна.

## 12. Что читать дальше

Следующий естественный шаг в этой части: разобрать, как именно строить shared gateways, reusable templates и anti-zoo patterns, чтобы орг-модель не оставалась только на словах.

- [Глава 13. Offline evals, online evals и regression gates](../part-v/chapter-13.md)
- [Глава 15. Golden paths, shared gateways и anti-zoo patterns](chapter-15.md)
- [Часть VI. Организационная модель](index.md)
- [Источники](../../appendix/sources.md)
