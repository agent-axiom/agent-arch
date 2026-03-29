# 第 14 章：Platform Team vs Product Teams

## 1. 为什么 agent platform 往往不是坏在代码上，而是坏在 ownership model 上

一开始一切看起来都很简单：几个热心的人，一两个 agent，几条集成，快速实验。这很正常。

问题通常出现在后面：

- 产品团队开始各自做本地 agent runtime；
- 每个团队都用自己的方式写 policy checks；
- observability 被拆成三种互不兼容的格式；
- tool adapters 重复建设；
- 没人确定 platform-grade incident 到底该谁来修。

所以系统在技术上也许还能跑，但在组织层面已经开始散开了。

## 2. Platform team 不应该把所有决定都从产品团队手里收走

有一种很糟糕的极端：platform team 试图成为所有 agent decision 的唯一审批点。

然后就会发生这些事：

- 平台变成 bottleneck；
- 产品团队失去速度；
- 所有改动都排进同一条队列；
- platform layer 膨胀成一个很重的系统。

这个模型是行不通的。Platform team 的职责不是自己把所有 agent feature 都做完，而是提供稳定的共享层和默认安全路径。

## 3. 反过来的极端也不好：完全联邦化

有些公司会走向另一边：“每个团队自己决定怎么做 agent。”

这很快就会带来：

- 不兼容的 contracts；
- 不同的 security posture；
- 参差不齐的 eval 质量；
- 参差不齐的 observability；
- 每个团队内部又长出自己的小平台。

短期看像自由，长期看几乎总会变成动物园。

## 4. 成熟的模型通常是 platform + product split

一个好的 operating model，责任大致会这样拆：

`platform team` 负责：

- orchestration primitives；
- policy framework；
- tool 和 capability contracts；
- observability 与 eval substrate；
- shared gateways；
- baseline security model。

`product teams` 负责：

- user workflows；
- product-specific prompts 和 policies；
- domain logic；
- task success 的 acceptance criteria；
- 把平台 primitives 集成进具体产品。

<div class="diagram-card">
<p>平台和产品不应该互相复制，因为它们负责的是不同层</p>

``` mermaid
flowchart LR
    A["Platform team"] --> B["Runtime, policy, observability, gateways"]
    C["Product teams"] --> D["User workflows, domain logic, UX outcomes"]
    B --> E["Golden paths and shared primitives"]
    D --> E
```

</div>

## 5. 平台应该提供 golden paths，而不是只给一堆底层零件

如果 platform team 只交付一个“零件箱”，产品团队最后还是会各自拼出不同的系统。

一个 golden path 通常包含：

- baseline runtime template；
- 现成的 policy hooks；
- 标准 tracing 和 eval wiring；
- approved tool gateway pattern；
- 关于 memory usage 的建议；
- rollout 和 regression defaults。

也就是说，一个好的 platform product 不只是让团队“能做”，而是让团队“默认就做得对”。

## 6. 每一层的 ownership 都应该是显式的

最好尽早把这些事情说清楚：

- 谁可以修改 platform contracts；
- 谁批准新的 write capabilities；
- 谁拥有 policy schemas；
- 谁拥有 telemetry schema；
- 谁负责 platform incidents 的 on-call；
- 谁决定什么时候某个产品可以偏离 golden path。

如果 ownership 很模糊，几乎任何 incident 最后都会变成一场很长的组织性乒乓球。

## 7. 不是所有 deviation 都要禁止，但它们必须是有意识的

有时候产品团队确实需要一个 special case：

- 非标准 workflow；
- 单独的 capability；
- 不同的 latency/cost trade-off；
- 实验性的 rollout。

这没有问题。成熟平台和混乱之间的区别在于，deviation 必须：

- 可见；
- 被讨论过；
- blast radius 受限；
- 有明确 owner；
- 不会悄悄变成新的默认标准。

## 8. 一个 agent platform 的 governance policy 示例

下面是一个很实用的模板：

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

这段 YAML 不能解决所有组织问题，但它很擅长解决一个永恒的问题：“这件事到底该谁拍板？”

## 9. 平台的衡量标准不该是功能数量，而是它减少了多少混乱

很重要的一点是，不要掉进 vanity metrics 的陷阱，比如：

- 增加了多少 tools；
- 启动了多少 MCP servers；
- 有多少产品团队“接入了平台”。

强平台应该减少的是：

- 重复建设；
- 自定义绕过路径；
- 增加新 workflow 的成本；
- incident 调查时间；
- unsafe deviations 的数量。

不然你可能建设了很多东西，但系统并没有变得更好。

## 10. Operating model 最常坏在哪里

常见问题基本都很像：

- 平台成了所有决策的 bottleneck；
- 产品完全绕开平台；
- ownership 不清晰；
- reusable primitives 太底层；
- 没有 deviations 流程；
- platform roadmap 和产品团队真实痛点脱节。

这会把组织带向经典岔路：不是平台帮不到人，就是产品团队觉得平台本身就是阻碍。

## 11. Practical Checklist

如果你想快速检查 operating model，可以问自己：

- 哪些东西归 platform team，是否清楚？
- 哪些东西留给 product teams，是否清楚？
- 你有 golden path 吗，还是只有“一组能力”？
- 谁批准新的 risky capabilities，这件事清楚吗？
- 有没有偏离标准路径的流程？
- 平台是否真的减少了本地 runtime implementation 的数量？

如果连续好几个问题答案都是 “no”，那你大概率遇到的已经不是技术问题，而是组织设计问题。

## 12. 接下来读什么

这一部分接下来的自然步骤，就是继续看 shared gateways、reusable templates 和 anti-zoo patterns，避免 operating model 只停留在口头上。

- [第 13 章：Offline Evals、Online Evals 与 Regression Gates](../part-v/chapter-13.zh.md)
- [第 15 章：Golden Paths、Shared Gateways 与 Anti-Zoo Patterns](chapter-15.zh.md)
- [第六部分：组织模型](index.zh.md)
- [参考资料](../../appendix/sources.zh.md)
