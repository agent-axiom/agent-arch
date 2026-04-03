# 第 15 章：Golden Paths、Shared Gateways 与 Anti-Zoo Patterns

## 1. 为什么即使有不错的组织模型，没有工程模板也会很快散掉

当你已经决定了谁拥有平台、谁拥有产品之后，下一个问题马上就会出现：团队在实践里到底应该复用什么？

如果这个问题没有答案，就会出现熟悉的场景：

- 每个团队都写自己的 runtime wrapper；
- policy hooks 在各处长得都不一样；
- tool adapters 在 contracts 上逐渐分叉；
- rollout practices 散落在各自的 wiki 里；
- observability wiring 靠手工复制，慢慢漂移。

也就是说，形式上你有 operating model，但实际上还是有很多本地系统，它们看起来相似，却互不兼容。

## 2. Golden path 不是“best practice 文档”，而是默认可工作的路径

很重要的一点是，不要把 golden path 和一组建议混为一谈。

建议会被选择性阅读。
而一个好的 platform product 里的 golden path，应该是团队真心觉得“直接用它比绕过去更省事”。

它通常包含：

- starter runtime template；
- 预先接好的 tracing 和 eval hooks；
- 默认接入的 policy integration；
- approved tool gateway；
- deployment 和 rollout defaults；
- 典型 product workflows 的示例。

只有当团队待在这条路径上更划算时，golden path 才是真的有效。

## 3. Shared gateways 的意义，是避免把关键错误复制到整个组织

有几层能力特别不适合留给各团队自由发挥：

- 访问外部 capabilities；
- policy enforcement；
- secret handling；
- audit trail；
- approval workflows；
- telemetry emission。

如果每个团队都自己实现一遍，组织几乎一定会把同样的错误复制出五个版本。

所以 shared gateway 不是官僚主义。它是把最贵、最敏感的问题集中起来，一次性认真解决的方式。

<div class="diagram-card">
<p>Golden path 应该减少关键层的本地实现数量</p>

``` mermaid
flowchart LR
    A["Product team A"] --> D["Shared gateway and platform primitives"]
    B["Product team B"] --> D
    C["Product team C"] --> D
    D --> E["Policy, tracing, approvals, capability access"]
```

</div>

## 4. Reusable template 应该是 opinionated 的，而不是抽象到失去价值

Platform teams 很常见的一个错误，是把 template 做得尽可能中性，好像这样就能“适配所有人”。

现实里这通常帮不到任何人。它太泛化了，需要大量手工拼装，所以团队最后还是会走向自定义实现。

一个好的 template 往往是 opinionated 的：

- 它定义了基础 run 结构；
- 它已经包含 policy hooks；
- 它已经接好 tracing；
- 它有 approved deployment path；
- 它带有可运行示例；
- 它只暴露有限的 extension points。

是的，这样会少一点“通用性”。但它对真实组织更有用。

## 5. 你不需要为所有类型的 agent 准备一条唯一的 golden path

这里也要有成熟度。单一路径很少能同时适合：

- Q&A agents；
- workflow agents；
- approval-heavy agents；
- high-risk action agents；
- internal copilots。

所以更实际的做法通常是：

- 一个基础 platform core；
- 2 到 4 条标准 golden paths；
- shared gateway 和 observability substrate；
- 为 special cases 提供可控的 deviations。

这比“一个统治世界的 giant template”或者“完全混乱”都更靠谱。

## 6. Anti-zoo pattern 的起点，是在正确的地方限制自由

“platform zoo” 这个词通常指的都是类似的问题：

- runtime 太多；
- 连接 tools 的方式太多；
- 本地 policy engine 太多；
- telemetry schema 太多；
- 几乎一样的 wrapper layers 太多。

减少这个动物园，不应该靠一刀切禁止一切，而是要在关键位置加上清晰的限制：

- 一个统一的 contract layer；
- 一个 shared gateway；
- 有限数量的 supported runtime patterns；
- risky deviations 需要 platform review；
- 对旧绕路方案有 deprecation policy。

### 6.1. Approved patterns registry 不只帮助控制，也帮助提速

当平台维护一份活的 approved patterns 列表时，产品团队会更快回答两个常见问题：

1. 什么可以直接使用，不需要单独 review？
2. 什么已经算 risky deviation？

一个好的 registry 通常会包含：

- supported runtime templates；
- approved gateways；
- approved capability classes；
- allowed connector patterns；
- deprecated local bypasses。

这不仅对安全团队有帮助，也会提升开发速度，因为团队不需要每次都从零重新判断。

## 7. 一个 platform defaults policy 示例

下面是一个很实用的模板，用来把 golden path 和 deviations 明确写出来：

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

这样的 policy 不会扼杀速度，它只是去掉了模糊地带。

### 7.1. Registry 和 deprecation policy 最好一起存在

一种很弱的模式是：平台有“推荐路径”，但没有正式说明哪些做法已经不该再被接受。

更成熟的组合通常是：

- approved registry；
- visible deviations；
- deprecation windows；
- exceptions 的 review path。

这才不会让 anti-zoo strategy 退化成一句无力的“请大家尽量走标准路径”。

## 8. Shared gateways 不只提升安全，也能提升演进速度

当 critical path 被集中起来以后，platform team 可以：

- 在一个地方更新 contracts；
- 一次性改进 audit trail，所有团队都受益；
- 调整 rollout guardrails，而不用重写十个产品；
- 更快推出新的 policy capabilities；
- 更快修复大面积 operational issues。

所以 shared gateway 不只是控制手段，它也是工程改进可以规模化传播的方式。

## 9. Anti-zoo efforts 最常坏在哪里

这里也有很多重复出现的错误：

- golden path 太重，团队就绕开；
- shared gateway 太慢或太难用；
- exception 逐渐变成常态；
- templates 很快过时；
- platform team 没有追踪团队到底在哪些地方偏离路径；
- 说了要 deprecate，但从来没有真正执行。

于是组织表面上在谈标准化，实际上只是在继续生产旧混乱的新变体。

## 10. 如果你真的想对抗“动物园”，该测什么

这里更有价值的 operational metrics 是：

- 本地 runtime forks 的数量；
- 绕过 gateway 的 direct tool access 路径数量；
- 使用 supported templates 构建的 agents 占比；
- 在 golden path 上启动一个新 workflow 的中位时间；
- 没有 owner 的 active deviations 数量；
- 淘汰 unsafe patterns 所需时间。

这些指标比单纯统计“有多少团队在用平台”更有意义。

### 10.1. Inventory drift 本身也值得被计量

还可以单独跟踪 platform inventory 里的 drift：

- 有多少 runtimes 没被注册；
- 有多少 active agents 运行在 approved templates 之外；
- 有多少 connectors 没有 owner；
- 有多少 deviations 超过了 review window 还在继续。

如果这些数字在上涨，那 anti-zoo strategy 也许形式上还存在，但实际上已经在失守。

## 11. 实用检查清单

如果你想快速检查 anti-zoo strategy，可以问自己：

- 你真的有一条比绕过去更容易用的 golden path 吗？
- 敏感 capability 是否有 shared gateway？
- supported runtime patterns 的集合是否受控？
- deviations 是否可见，而且有 owner？
- 平台能不能淘汰 unsafe local patterns？
- 新的平台层是否真的减少了 copy-paste 和本地 forks？

如果连续好几个问题答案都是 “no”，那你现在做的还不是 platform product，而是一套带着良好愿望的 library。

## 12. 接下来读什么

Part VI 下一步最自然的延伸，是继续补 platform roadmap、adoption 和 lifecycle management 这些组织层模式。再之后，就可以进入 reference implementation。

- [第 14 章：Platform Team vs Product Teams](chapter-14.zh.md)
- [第 16 章：基础 Runtime Blueprint](../part-vii/chapter-16.zh.md)
- [第六部分：组织模型](index.zh.md)
- [参考资料](../../appendix/sources.zh.md)
