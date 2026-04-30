# Глава 17. Слой политик и каталог возможностей

!!! info "Как читать эту главу"
    Полезно держать в голове не абстрактную тему “слой политик”, а очень практичную задачу:

    - кто решает, можно ли тому же support-агенту вообще запустить этот run;
    - кто определяет, можно ли читать контекст, открывать тикет или писать в память;
    - где эти решения должны жить, чтобы они не расползлись по коду оркестрации.

    Если ответы на эти вопросы спрятаны в случайных ветках кода, рантайм уже собран, но договорное ядро системы все еще отсутствует.

## 1. Почему без слоя политик справочный рантайм остается слишком наивным

Даже если у тебя уже есть аккуратный цикл рантайма, этого все равно недостаточно. Без явного слоя политик система остается слишком доверчивой:

Именно в этом состоит главная задача этой главы. Она должна показать читателю, где на самом деле находится договорное ядро рантайма и почему система остается незрелой, пока решения о допустимости, риске и управлении возможностями прячутся в коде оркестрации.

В нашем сквозном support-кейсе это проявляется сразу после главы 16. Рантайм уже умеет принять запрос, собрать контекст, вызвать модель и дойти до gateway. Но в момент, когда агент собирается открыть срочный тикет, записать сводку в память или запросить еще один внешний шаг, системе нужен не просто цикл, а явное решение о допустимости и риске.

- нельзя надежно отличить допустимый run от недопустимого;
- вызовы инструментов трудно контролировать одинаково;
- записи в память живут на отдельных договоренностях;
- продуктовые ограничения быстро просачиваются в код оркестрации.

Поэтому следующий обязательный слой справочной реализации - слой политик.

Его задача не в том, чтобы “тормозить систему”. Его задача в том, чтобы решения про доступ, риск и допустимость не были размазаны по случайным `if` в коде.

Поэтому эту главу полезно читать не только как главу про policy pages, но и как главу про управляемые решения. Вопрос не в том, записала ли команда какие-то правила. Вопрос в том, появился ли у рантайма проверяемый договорный центр, который может объяснить, почему run был разрешен, поставлен на паузу, отклонен, ограничен или передан на escalation.

Если тебе нужно увидеть, как это управляемое policy decision дальше связывается с traces, approvals, eval judgments, incidents и rollout, открой отдельную страницу [Сквозная цепочка доказательств](../part-v/evidence-spine.md).

!!! info "Нужен контрактный слой?"
    Для более прикладной формы открой [схему policy bundle и approval contract](../../appendix/policy-bundle-schema.md), [схему запроса на approval и записи о решении](../../appendix/approval-schema.md) и [справочный пакет](../../appendix/reference-package.md).

## 2. Слой политик должен отвечать на маленькие и понятные вопросы

Слабый слой политик пытается быть “умным мозгом системы”. Сильный слой политик делает наоборот: он решает ограниченный набор ясных вопросов.

Например:

- можно ли запускать этот run вообще;
- можно ли читать этот контекст;
- можно ли вызывать эту возможность;
- нужен ли approval;
- можно ли записывать это в память;
- можно ли вернуть этот результат наружу;
- каким verifier contracts вообще можно доверять, если high-risk rollout или assurance зависят от graded evidence.

Когда эти вопросы оформлены явно, рантайм становится объяснимее, а изменения в ограничителях перестают быть хаотичными.

## 3. Каталог возможностей нужен не как реестр имен, а как контрактный слой

Очень легко скатиться к каталогу, который просто хранит список доступных инструментов. Но хороший каталог делает больше:

- описывает контракт возможности;
- хранит профиль риска;
- указывает transport и режим исполнения;
- задает ожидания по идемпотентности;
- фиксирует ownership и lifecycle.

То есть каталог возможностей это не “инвентарь для удобства”, а центральная точка управления способностями платформы.

<div class="diagram-card">
<p>Слой политик и каталог возможностей вместе образуют договорное ядро эталонной реализации</p>

``` mermaid
flowchart LR
    A["Run request"] --> B["Runtime orchestrator"]
    B --> C["Policy layer"]
    B --> D["Capability catalog"]
    C --> E["Allow / deny / approve"]
    D --> F["Capability contract"]
    E --> G["Execution layer"]
    F --> G
```

</div>

## 4. Поверхность инструментов это не то же самое, что управляемая поверхность возможностей

Свежие материалы OpenAI по tooling полезны тем, что проводят различие, которое на практике размывают многие команды: модель может видеть tools, MCP servers, hosted capabilities или local functions, но рантайм все равно должен решать, к какой поверхности управления все это относится.[^openai-tools]

Это различие важно.

Слабая реализация говорит так:

- вот список tools, которые модель может вызывать.

Более сильная реализация говорит так:

- вот управляемая поверхность возможностей;
- вот какая ее часть вообще видна модели;
- вот через какой transport идет исполнение;
- вот какие возможности можно звать напрямую, какие идут через gateway, а какие вообще не экспонируются.

Именно поэтому каталог возможностей должен стоять выше сырых определений инструментов. Он не дает рантайму перепутать:

- что модель может упомянуть;
- что runtime может маршрутизировать;
- что платформа вообще готова исполнять.

## 5. Что полезно хранить в каталоге возможностей

Как только платформа начинает работать с stateful MCP-подобными возможностями, каталог уже должен описывать не только transport и risk, но и то, является ли возможность sessionless, session-bound, interruptible или resumable через несколько turns.

Из-за этого mature catalog часто полезно дополнить такими полями:

- capability session mode: `stateless / stateful`;
- допускается ли elicitation;
- испускаются ли progress events;
- как ведет себя session expiry;
- требует ли resume нового approval или может продолжаться под уже выданным решением;
- можно ли capability автоматически reinitialize remote session.

Без этих полей policy layer может формально разрешить возможность, но не суметь нормально управлять тем, как ее живая runtime session ведет себя на практике.

Таксономия workflow-паттернов у Anthropic добавляет сюда еще одно недостающее измерение governance.[^anthropic] Policy layer должен решать не только то, разрешена ли возможность сама по себе. Он еще должен решать, в каких orchestration patterns ее вообще допустимо вызывать.

Их более поздняя работа про harness design добавляет сюда тесно связанный урок: как только система начинает работать через роли planner, generator и evaluator на длинном горизонте, policy должен управлять уже не только вызовом инструмента, но и **ролевым контрактом** вокруг этого вызова.[^anthropic-harness] Если generator предлагает sprint, evaluator оценивает результат, а planner перестраивает scope, платформе нужны явные правила о том, кто имеет право определять done-ness, кто оценивает качество, кто вправе инициировать reset и какой handoff artifact считается авторитетным после context reset.

Например, policy contract может требовать явного ответа на то, что возможность:

- безопасна внутри `prompt chaining`, но не внутри unconstrained loop;
- допустима в `routing` только для некоторых классов запросов;
- может использоваться в `parallelization` только если ветки read-only;
- доступна delegated workers в `orchestrator-workers` или остается только у parent runtime.

Так управление возможностью остается привязанным к форме runtime, а не делает вид, будто один и тот же контракт инструмента одинаково безопасен в любом execution pattern.

Практически полезный набор полей обычно такой:

- имя возможности;
- owner;
- mode: read / write / high_risk;
- transport: mcp / gateway / sandboxed_exec;
- exposure: direct / brokered / restricted;
- входная схема;
- формат выхода;
- требования к approval;
- требования к идемпотентности;
- значения timeout и retry по умолчанию.

С таким контрактом runtime уже может вести себя предсказуемо, а не подстраиваться под каждую возможность на ходу.

## 6. Approval должен выглядеть как прерываемый путь выполнения в рантайме, а не как разговор в стороне

Policy layer становится намного реальнее, когда approval моделируется как часть управляющего потока рантайма, а не как ручной процесс вне системы. Модель interrupts в LangGraph полезна именно этим: pause, review и resume становятся явными примитивами рантайма, а не ad hoc человеческими обходами.[^langgraph-interrupts]

Именно такая форма нужна и системам агентов с сильным policy-слоем.

Когда high-risk возможность доходит до approval boundary, runtime должен уметь:

- поставить run на паузу;
- показать ожидающее действие и его контекст;
- дождаться внешнего решения;
- продолжить выполнение со структурированным результатом.

Это намного сильнее, чем просто отправить сообщение оператору и надеяться, что окружающий код все еще помнит, на чем остановился.

Полезно сразу различать два approval-паттерна:

- прямой human approval для редких или действительно high-risk actions;
- classifier-mediated approval paths для повторяющихся low-context решений, где ручной review создает усталость от подтверждений.

Второй путь не надо воспринимать как “approval убрали”. Его лучше мыслить как delegated control с более жесткими требованиями к evidence:

- какой classifier или gate принял решение;
- какой evidence был ему виден;
- когда он обязан escalate к человеку;
- как subagent или follow-on actions наследуют такое delegated approval или теряют его;
- каким verifier contracts можно доверять для grading тех же high-risk paths, если rollout или assurance зависят от verifier output.

## 7. Policy decision должен быть объектом, а не просто bool

Очень полезная инженерная привычка: policy decision не должен сводиться к `True/False`.

Чаще полезнее возвращать что-то вроде:

- `allow`
- `deny`
- `approval_required`
- `sanitize_and_continue`
- `escalate`

И дополнительно:

- reason code;
- policy id;
- risk class;
- optional constraints;
- allowed orchestration patterns или явные pattern restrictions;
- trusted verifier contracts или verifier-contract requirements для high-risk paths;
- при необходимости approval или resume requirements.

Это резко повышает explainability и делает telemetry намного полезнее.

## 8. Пример policy contract

Ниже очень простой, но практичный шаблон:

```yaml
policy:
  run_precheck:
    require_tenant: true
    deny_if_principal_missing: true
  capabilities:
    search_docs:
      decision: allow
    create_ticket:
      decision: approval_required
      approver: manager
    run_shell:
      decision: deny
  memory_write:
    allow_kinds:
      - validated_fact
      - session_summary
```

Его сила не в полноте, а в явности. Ты можешь спорить с конкретным правилом и понимать, где оно применяется.

По мере того как verifier-aware governance становится частью production model, такая же явность нужна и для доверия к verifier. High-risk paths не должны зависеть от «любого доступного verifier». Policy layer должен уметь сказать, какие verifier contracts считаются trusted, когда они обязательны и что происходит, если в release path появляется untrusted verifier contract.

## 9. Пример capability catalog contract

Catalog полезно мыслить примерно так:

```yaml
capabilities:
  search_docs:
    owner: knowledge_platform
    mode: read
    transport: mcp
    exposure: direct
    timeout_seconds: 5
    approval: none
  create_ticket:
    owner: support_platform
    mode: write
    transport: gateway
    exposure: brokered
    timeout_seconds: 15
    approval: manager
    idempotency_key_required: true
  run_shell:
    owner: platform_runtime
    mode: high_risk
    transport: sandboxed_exec
    exposure: restricted
    timeout_seconds: 10
    approval: always
```

Такой catalog уже задает operational semantics, а не просто список имен. Он еще и явно показывает, какая capability видна модели, какая идет через runtime-broker, а какая остается только у операторского контура.

## 10. Structured outputs важны потому, что contracts должны переживать встречу с кодом

Stateful capability flows делают это требование еще жестче. Если approval, pause/resume, session expiry и re-init decisions описаны только словами, runtime уже не может безопасно различить, продолжает ли он ту же управляемую session или случайно открывает новую.

Именно поэтому policy artifacts все чаще стоит делать структурно явными по таким полям, как:

- `capability_session_id`;
- `capability_session_mode`;
- `resume_policy`;
- `on_session_expiry`;
- `progress_event_policy`;
- `elicitation_policy`.

Эти поля помогают держать approval control и capability session control в одной модели, а не давать им расползаться в две разные неявные системы.

По мере взросления approval system в контракт почти сразу полезно добавлять и поля для classifier-backed approval control, например:

- `approval_mode`
- `approval_delegate`
- `classifier_verdict`
- `escalate_to_human_if`
- `subagent_handoff_policy`

Такие поля помогают делать delegated approval path явным, а не прятать его в product logic или поведении UI.

Та же дисциплина нужна и для delegated workers. Если runtime поддерживает путь `orchestrator-workers`, policy layer должен уметь явно сказать:

- наследует ли worker родительский approval context;
- истекает ли delegated approval на handoff boundary;
- может ли worker запрашивать дополнительные capabilities или работает только с worker-safe subset;
- должен ли worker output пройти review до того, как будет выполнена любая write-capability.

Тот же уровень дисциплины нужен и на identity boundary. Если capability использует delegated user authorization через MCP или другой brokered transport, policy layer должен уметь явно зафиксировать:

- доступ platform-owned или user-delegated;
- можно ли reuse delegated scopes после paused run;
- ведет ли revoked authorization к cancel, re-approval или re-initialization;
- могут ли subagents наследовать тот же delegated authorization context.

Так delegated approval и delegated authorization остаются внутри одной governed contract model, а не превращаются в два несвязанных исключения.

Справочный runtime теперь несет эти предположения и прямо в execution artifacts: `run_start`, `approval_requested`, `tool_execution`, `run_complete`, approval records и session export могут сохранять один и тот же delegated authorization context. Это важно, потому что rollout и расследование не должны восстанавливать delegated identity по побочным следам.

Свежий материал OpenAI по structured outputs полезен и для policy layer.[^openai-structured]

Контракт наполовину нереален, если runtime все равно вынужден догадываться, вернулись ли policy result, approval request или capability payload в ожидаемой форме.

Поэтому systems с сильным policy-слоем полезно делать структурно явными такие артефакты:

- policy decisions;
- approval requests;
- approval outcomes;
- capability inputs и outputs.

Смысл здесь не в эстетике. Смысл в том, чтобы уменьшить тихий drift между runtime logic, audit records и окружающим control surface.

## 11. Простой кодовый каркас policy decision

Ниже каркас, который показывает, что runtime получает не просто разрешение, а структурированное решение.

```python
from dataclasses import dataclass


@dataclass
class PolicyDecision:
    action: str
    reason: str
    policy_id: str
    approval_mode: str = "human"
    escalate_to_human: bool = False
    requires_approval: bool = False


def evaluate_capability(name: str) -> PolicyDecision:
    if name == "search_docs":
        return PolicyDecision(action="allow", reason="low_risk_read", policy_id="cap_001")
    if name == "create_ticket":
        return PolicyDecision(action="approval_required", reason="write_action", policy_id="cap_014", requires_approval=True)
    return PolicyDecision(action="deny", reason="unsupported_capability", policy_id="cap_999")
```

Даже такой простой код уже задает правильную форму для telemetry, UI approval flows и расследований.

## 12. Простой кодовый каркас capability lookup

И еще один практичный кусок: runtime не должен знать capability details напрямую, он должен вытаскивать их из catalog.

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    mode: str
    transport: str
    exposure: str
    timeout_seconds: int


def get_capability(name: str) -> CapabilitySpec | None:
    registry = {
        "search_docs": CapabilitySpec("search_docs", "read", "mcp", "direct", 5),
        "create_ticket": CapabilitySpec("create_ticket", "write", "gateway", "brokered", 15),
    }
    return registry.get(name)
```

Это скучный слой. И это хорошо. Catalog layer как раз и должен быть стабильным и обозримым.

## 13. Частые ошибки

Проблемы здесь очень типовые:

- policy rules размазаны по runtime;
- capability contract неполный;
- tools, видимые модели, воспринимаются так, будто это автоматически разрешенные capabilities;
- ownership capability неясен;
- approval logic вшита прямо в orchestration;
- approval существует как человеческий процесс, но не как явный pause/resume path внутри runtime;
- structured contracts отсутствуют, поэтому policy и approval payloads дрейфуют по форме;
- memory policy и execution policy живут как будто отдельно;
- catalog и real adapters расходятся по поведению.

Когда это происходит, справочная реализация перестает быть опорой и снова превращается в связку договоренностей.

## 14. Быстрый тест зрелости для policy layer и capability catalog

Команде не стоит думать, что она уже собрала contract core своей agent system, только потому, что у нее есть несколько policy checks и список tools.

Более сильная планка такая:

- policy decisions существуют как явные объекты, а не как размазанные booleans;
- capability contracts несут ownership, transport, exposure, risk и approval semantics;
- runtime code зависит от catalog, а не от direct calls и ad hoc exceptions;
- approval моделируется как явный interruptible path, а не как ручной обход вне потока;
- memory policy, execution policy и approval policy принадлежат одному видимому control surface;
- telemetry умеет показать не только что произошло, но и какой policy и capability contract этим управлял.

Если большинство этих условий не выполняется, runtime уже может существовать, но contract core у системы пока не собран.

## 15. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли у тебя отдельный policy layer, а не набор `if` по коду?
- Возвращает ли policy structured decision?
- Есть ли единый capability catalog?
- Есть ли у capabilities owner, transport, exposure и risk semantics?
- Использует ли runtime catalog, а не прямые вызовы?
- Может ли approval явно поставить run на паузу и продолжить его?
- Видны ли policy decisions в telemetry?

Если на несколько вопросов подряд ответ “нет”, skeleton у тебя уже есть, но contract core пока еще не собран.

## 16. Что делать дальше

Сначала сделай policy decisions и capability contracts явными, а потом проверь, готова ли эта же система к первому rollout.

Следующий логичный шаг в опорной реализации - собрать production rollout checklist, чтобы из blueprint и contract core выйти в практический go-live framework.

- [Глава 16. Базовая схема рантайма](chapter-16.md)
- [Глава 18. Чеклист промышленного запуска](chapter-18.md)
- [Часть VII. Эталонная реализация](index.md)
- [Источники](../../appendix/sources.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^openai-tools]: [OpenAI, Using tools](https://developers.openai.com/api/docs/guides/tools)
[^langgraph-interrupts]: [LangGraph, Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
[^openai-structured]: [OpenAI, Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

## 17. Полезные справочные страницы

- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)
- [Справочный пакет](../../appendix/reference-package.md)

Эта глава служит контрактным шарниром для всего runtime-control cluster. Дальше полезнее всего идти в Chapter 18 за rollout gates и в Chapter 21 за assurance response, построенный на тех же approval и policy paths.

- [Глава 16. Базовая схема рантайма](chapter-16.md)
- [Глава 18. Чеклист промышленного запуска](chapter-18.md)
- [Часть VII. Эталонная реализация](index.md)
- [Источники](../../appendix/sources.md)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
