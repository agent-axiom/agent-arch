# 第 13 章：离线评测、在线评测与回归门禁

!!! info "时效说明"
    最近一次编辑审查：**2026 年 5 月 17 日**。上一次审查：**2026 年 5 月 14 日**。下一次计划审查：**2026 年 6 月 17 日**。

    自上次审查以来的变化：MCP/A2A 安全面、验证器契约、治理感知遥测以及印刷准备问题，现在都有具体契约覆盖和文档表面检查。

    变化最快的部分：

    - 托管式评测产品、模型裁判方法，以及平台化评分流程；
    - 面向记忆、多轮一致性和行为评测的新测试集；
    - 各家平台提供的在线评测与发布门禁工具。

    变化相对较慢的部分：

    - 必须把离线评测、在线评测和回归门禁视为同一个闭环；
    - 评测需要与追踪、SLO 和 rollout 决策绑定；
    - 关键场景必须在发布前被验证，而不是等到事故后才补救。

!!! info "如何阅读本章"
    **章节导向：**请把发布决策放在中心，而不只是看测试集或分数表。本章说明评测数据集、验证器契约、回归门禁和发布门禁如何形成一份可审查的团队契约。这份契约应该能放在一页里，并且在不依赖网站实时导航时仍然清楚。

## 1. 从一个问题开始：怎样避免同一个故障再次被发出去

继续沿用同一个支持场景。

团队已经经历过一次不愉快的事故：

- 智能体创建了重复工单；
- 追踪帮助团队还原了这次运行路径；
- 根因是糟糕的重试路径和薄弱的幂等约束；
- 这个 bug 已经修掉了。

但修完之后，真正的工程问题才出现：

> 怎样保证两周之后，另一次提示、策略或工具适配器改动，不会把类似的退化再次带回发布流量？

这就是评测闭环开始的地方。

而在本章里，评测回路应该被理解成判断层，而不是响应层。它的任务是在 rollout 扩大或变更获得信任之前，产出关于质量与回归风险的可审查决策。

追踪帮你理解发生了什么。
SLO 帮你定义什么叫系统健康。

但最重要的问题还在：怎样系统性地提升质量，并把回退挡在发布之前？

在本书里，评测回路的角色是很具体的：它负责产出关于质量、行为与回归风险的可审查判断。后面的章节会分别说明保证如何响应发现，可观测性如何保存证据，以及注册表/治理如何分配问责。这里的重点只放在团队如何判断到底测试了什么、发生了什么变化，以及这个变更是否值得被信任。

如果你想看一页专门把评测判断再连接回请求、策略、审批、追踪、事故和 rollout 的桥接层，可以直接使用单独的 [Evidence Spine](evidence-spine.zh.md) 页面。

**Eval case-spine note：**评测集应该在三个 canonical cases 之间保持平衡。Support triage 要测试 duplicate tickets、approval gates、retries 和 side effects。Internal knowledge assistant 要测试 retrieval freshness、source attribution、memory provenance 和 access-control failures。Incident coordination 要测试 escalation timing、handoff quality、response ownership，以及 post-incident changes 是否会在下一次 rollout 前变成 regression cases。

!!! info "需要配套的模式和工程工件？"
    如果你需要的不只是原理说明，可以直接打开 [追踪模式与事件目录](../../appendix/trace-schema.zh.md) 和 [评测数据集模式与打分契约](../../appendix/eval-schema.zh.md)。

## 2. 离线评测的作用，是在发布之前改变系统

离线评测回答的是一个非常实际的问题：

> 如果我们修改提示、策略、检索、模型路由或工具行为，系统在已知关键场景上会变好还是变坏？

对于这个支持智能体，一个好的离线评测集不应该只有舒服的顺畅路径场景，还应该包含那些已经真正伤过系统的场景：

- 重复工单场景；
- 已经产生副作用后才超时；
- 含糊的用户请求；
- 需要审批的流程；
- 过期的记忆读取；
- 跨租户的隐私敏感场景。

这也正是失败运行演练进入评测层，而不只是停留在运维演练里的地方。如果团队希望 rollout 审查能信任超时处理、验证失败处理，或者上游依赖故障时的行为，这些降级路径就应该作为带有可追踪失败结果的显式场景进入离线集合。

这里还需要对可追踪保持严格定义。一个降级运行不能因为某处记录了超时就被视为 reviewable。评测回路应验证，这条失败路径仍然保留了足够清晰的发布身份、追踪链接与会话级证据，包括像 `failure_reason` 这样的明确字段，能够支撑后续的 rollout 审查、保证和来源分析。

离线评测的价值就在于：它们让你可以在生产流量到来之前比较系统版本。

最近验证器设计的一个有用补充是，离线评测不该只依赖二元成功标签。对于长周期智能体，往往需要更丰富的评分信号：

- `process quality`；
- `outcome quality`；
- 针对 `controllable` 与 `uncontrollable` causes 的失败归因。

否则，团队就分不清一次运行是“行为正确但被环境阻断”，还是“通过薄弱或不安全路径达成了名义结果”。

因此，实践中的 `verifier contract` 应该被明确写出来，而不是藏在 judge prompt 里。最小契约应该包括：

- `rubric_version`，让团队知道 verdict 是按哪一版评分规则产生的；
- `process_score`，用于评价执行路径，而不只是最终结果；
- `outcome_score`，用于评价真实的用户或业务结果；
- `failure_attribution`，包括 `controllable` / `uncontrollable` 以及具体失败层；
- `judge_human_agreement`，让 automated judge 持续相对于 human review 校准；
- `false_positive_budget` 和 `false_negative_budget`，因为不同 rollout gates 的错误成本不同；
- `calibration_dataset_id`，让 judge、prompt 或 rubric 的变化可以在稳定样本集上重放；
- `replay_protocol`，说明如何恢复有争议 verdict 对应的 traces、inputs、policy bundle 和 artifact version。

这样的契约会把 verifier 从自由文本评论变成 release-bearing artifact：它可以被版本化、跨发布比较，并作为阻止 rollout 的依据。

实践中，最好不要只保存 verdict 文本，还要保存一个小的 [验证器裁决记录（verifier verdict record）](../../appendix/eval-schema.zh.md)，并且也可以映射进 [追踪模式（trace schema）](../../appendix/trace-schema.zh.md)：

- `verdict_id`：评审结果的稳定标识符；
- `verifier_id`：是哪一个 verifier 或 judge 生成了结果；
- `verifier_contract_version`：生成 verdict 时使用的 contract version；
- `input_refs`：指向 scenario、trace、prompt/model version 和 policy bundle 的链接；
- `evidence_refs`：verdict 所依据的证据；
- `blocking_decision`：verdict 是阻止 rollout、仅发出 warning，还是要求 human review；
- `comparison_baseline`：结果是和哪个 previous release/eval baseline 比较的；
- `reviewer_override`：automated verdict 是否被 human 覆盖，以及原因。

如果没有这条记录，verifier contract 很容易只是 prose 里的好想法，而不是强 operational control。有了它，eval verdict 才能被比较、被质疑，并真正用于 release governance。

## 3. 在线评测之所以必要，是因为真实世界永远比测试集更大

即使很好的离线评测，也无法覆盖生产环境中真正发生的一切：

- 用户会提出新的任务类型；
- 输入分布会漂移；
- 外部系统会退化；
- 检索基础会不断变大；
- 策略规则在新数据上会表现不同。

所以在线评测不是离线评测的替代，而是第二条闭环：

- 评估真实流量上的行为；
- 捕捉漂移；
- 发现悄无声息的回退；
- 观察系统在真实运行条件下的表现。

对于这个支持智能体，这意味着一件很简单的事：即使关键测试集是干净的，团队仍然要看见智能体是否开始：

- 更频繁地创建不必要的工单；
- 更早地进入升级；
- 更差地处理不完整状态；
- 用更高的成本完成同类运行。

## 4. 最好的形态不是“离线或在线”，而是两条闭环同时存在

一种非常实用的模型是：

- 离线评测在发布前阻挡明显回退；
- 在线评测在发布后发现新问题；
- 追踪提供分析原料；
- SLO 提供运行边界；
- 回归门禁阻止质量悄悄下滑。

<div class="diagram-card">
<p>最好把评测闭环理解成持续循环，而不是一次性检查</p>
<p><strong>文本 fallback：</strong>code、prompt 或 policy 的变更会经过离线评测、回归门禁、生产 rollout、在线评测与追踪、失败分析，然后把经验反馈到下一轮变更。</p>

``` mermaid
flowchart LR
    A["Code / prompt / policy change"] --> B["离线评测"]
    B --> C["回归门禁"]
    C --> D["生产 rollout"]
    D --> E["在线评测 + 追踪"]
    E --> F["失败分析与评分"]
    F --> A
```

</div>

对于这个支持场景，这条闭环意味着一件很重要的事：事故不能只留在复盘里。它必须变成评测案例，也必须变成发布规则。

!!! example "贯穿案例：把重复工单变成回归门"
    在重复工单事故之后，评测案例不应该只检查最终答复文本。它应该让系统走过“副作用之后超时”的场景，保留 `trace_id` 和 `idempotency_key`，避免创建第二张工单，并输出可供发布门检查的结果。如果新的提示或适配器又把系统带回盲目重试，发布就应该在进入生产前停止。

    完整链条应该是这样：trace 显示 `side_effect_unknown`；verifier 把 failure attribution 归到 retry/reconciliation path；regression gate 把这次发布标记为 blocked；rollout owner 要么修复 adapter，要么让 canary 停在当前比例。这样 eval decision 就不再是抽象分数，而是具体的 release judgment。

### 4.1. 当静态案例不够时，user simulator 很有价值

Google 最近的材料还强调了一个很实用的层次：评测闭环最好不要只靠固定测试集，还可以补上一层用户模拟器。[^google-govern]

这在下面这些问题上特别有帮助：

- 智能体在长对话里会怎么表现；
- 回答不完美之后行为会不会跑偏；
- 系统会不会正确发起澄清；
- 多轮场景里策略路径会不会断掉；
- 用户说法更有变化时编排会不会退化。

对这个支持智能体来说，用户模拟器特别适合这类场景：

- 用户先让你查状态，随后突然改变优先级；
- 智能体只拿到不完整的 `request_id`；
- 工具调用失败后，用户又补充了一条新信息；
- 系统必须在升级、追问和安全停止之间做选择。

静态评测集很适合比较已知案例。用户模拟器更适合检查行为动态，而不只是看一个预设样例上的分数。

### 4.1.1. Deployment simulation 增加了发布前真实分布回放

OpenAI 描述了一个位于静态评测集和线上 rollout 之间的有用层级：deployment simulation。[^openai-deployment-simulation] 它不是只检查人工编写或 adversarial prompts，而是取真实历史上下文，做隐私过滤，移除旧模型的 assistant completion，再用候选模型在发布前重放同一段前缀。对 agentic settings 来说，这不只是 transcript replay；它还需要可信的 tool environment simulation，因为一次智能体轨迹可能依赖数百次工具调用、仓库状态、网络响应和临时故障。

本书里的架构结论很直接：发布前门禁不应该只会回放 curated incidents，也应该能回放真实任务分布的一小段。最小 replay contract 包括：

- `source_window` 和 privacy-filtering 规则；
- `candidate_model` 或新的 policy/runtime 版本；
- 不含旧 assistant completion 的 `conversation_prefix`；
- simulated 或 read-only 的 `tool_environment_ref`；
- 针对新 failure modes、behavior delta 和 tool-use regression 的 verdict；
- post-release validation hook，用来把预测和真实 rollout traffic 对比。

Deployment simulation 不能替代 red team 和 targeted tail-risk evals。它填补的是另一个缺口：在新 model、runtime 或 policy 进入大范围用户流量之前，先在 deployment-like contexts 中发现常见或新出现的失败模式。

### 4.1.2. ToolSimulator 展示了独立的工具模拟契约

AWS ToolSimulator 适合作为 deployment simulation 旁边更窄但很重要的一层：它是面向依赖外部工具的智能体的 LLM-powered tool simulation。[^aws-toolsimulator] 它避免直接使用可能泄露 PII、触发真实副作用或遇到 rate limits 的 live API calls，也避免只靠很难支撑 multi-turn workflows 的 static mocks；模拟器会基于注册的 schema 生成工具响应，并支持 stateful tool simulations。

对本书来说，重点不是“必须使用 Strands Evals”。重点是任何 agent-eval 平台都需要一个明确的 tool simulator contract：

- 哪些工具可以被模拟，哪些工具必须保持 read-only 或直接禁止；
- `simulated_tool_state`、初始状态，以及每个 case run 之间的 reset 规则；
- 对 tool responses 和错误的 schema enforcement；
- 覆盖 recovery path 的 fault、latency 和 empty-result cases，而不只是 happy path；
- fidelity boundaries：模拟器能模仿什么，哪里必须使用真实 sandbox 或 canary；
- tool simulator fidelity 指标，避免团队把看似合理的 mock 当成 production evidence。

实践结论很简单：tool-heavy evals 必须单独审查工具模拟器质量。如果智能体通过测试只是因为 simulator 总是返回方便的答案，即使最终文本看起来正确，rollout gate 也应该把这个信号视为弱证据。

### 4.1.3. Analytics-agent evals 应该检查 query path，而不只是答案

GitHub 的 Qubot 案例展示了 internal analytics agent 的一个好用生产模式：context layer 和 agent configuration 的变更通过 pull request 进入，再用 known prompts、ground-truth SQL、metadata、multiple trials，以及 completion、accuracy、duration 报告进行 offline evals。[^github-qubot]

对本书来说，重点不是 SQL agent 本身，而是 eval contract 的形状。internal knowledge/data agent 不应该只按最终答案文本来评测，还应该检查生成答案的路径：

- 加载了哪个 context layer；
- 应用了哪些 mandatory filters 和 ownership rules；
- 选择了哪个 query engine，为什么；
- source attribution 是否指向 dataset 或 metric definition；
- 权限不足或 grain/filter 有歧义时发生了什么；
- 哪条 trace 证明 query review 和 access boundary 没有被绕过。

这种 eval 更能捕捉真实 production regressions：agent 可能生成看似合理的答案，却选错 grain、跳过 mandatory filter、引用过期 metric definition，或者在本该拒绝时执行 query。

### 4.2. 持续评测闭环应该反过来影响发布决策

当你已经有了在线评测、追踪分级和模拟对话，下一步就很关键：这些结果不能只是被记录下来，它们应该真正影响发布流程。

一个健康的运行模型通常是：

- 离线评测在发布前拦住明显回退；
- 用户模拟器帮你测试那些难以固化进静态数据集的场景；
- 在线评测和追踪分级捕捉漂移与新的失效模式；
- 发布门禁决定是否继续扩大暴露范围。

也就是说，评测闭环最好不要被看成“独立的分析活动”，而应该被视为变更管理的一部分。

这个边界很重要，因为评测不应该被塞进生命周期里的所有职责。它们的任务是产出 rollout 可以消费的判断，而不是替代事故响应、遥测设计或全域负责人归属。

这也意味着评测不拥有遏制。它们不会冻结路由、禁用能力，也不会分配紧急响应。它们告诉团队，这个变更是否值得被信任、regression risk 在哪里，以及 rollout 是否应该继续。

另一个 lifecycle risk 是把 eval discipline 和某个 hosted eval product 混为一谈。OpenAI 在 2026 年 6 月宣布 Evals platform 和 Agent Builder deprecation：现有 evals 计划在 2026 年 10 月 31 日变成 read-only，Evals dashboard/API 和 Agent Builder 计划在 2026 年 11 月 30 日关闭。[^openai-deprecations] 对本章的实践结论很简单：hosted dashboard 可以是有用界面，但持久基础应该是 portable datasets、verifier contracts、traces、grading rules、export paths 和 release-gate decisions，这些东西应该能在产品替换或迁移后继续存在。如果 workflow 需要活得比一个 UI 产品更久，迁移目标应该偏向 Agents SDK 或另一个 code-owned runtime，让 eval artifacts 和代码一起版本化。

LangChain 的 State of Agent Engineering 补上了一个有用的 production-readiness baseline。[^langchain-state-agent-engineering] 在它的调查中，57.3% 的受访者已经把 agents 放进 production，但最大的 production barrier 仍然是 quality：32% 把它列为首要 blocker。同时，observability 已经接近基础设施默认项：89% 的组织已经实现某种 observability layer，而 offline evals 只有 52.4%。对本章来说，这个差距很关键：agent maturity 不能只靠 traces 证明。Release gate 应该显式看到 `quality blocker`、`observability baseline` 和 `eval adoption gap`：团队能解释哪些 failures，能在发布前抓住哪些 failures，又有哪些 failures 仍然只能在 exposure 之后发现。

这还意味着，发布纪律必须谨慎决定自己在奖励什么。单一的最终状态分数往往太弱，因为它会掩盖部分成功、被阻断但正确的行为，或者通过糟糕控制路径获得的侥幸成功。成熟的评测回路会使用更丰富的验证器输出，让 rollout 决策反映的不只是最后一个屏幕看起来是否正常，而是系统到底如何行动的。

同样的纪律也应该适用于验证器契约变更。如果评分标准因验证器契约版本变更而改变，eval loop 就应该把它显式暴露为承载发布意义的回归信号，而不是悄悄把新的裁决当作与旧结果可直接比较。

## 5. 追踪分级对智能体系统特别有价值

普通应用往往只要业务 KPI 和错误率就够了。智能体系统不行，因为质量经常藏在一次运行内部，而不只在最终答案上。

追踪分级的价值在于，你可以评估：

- 检索是否合适；
- 工具调用是否必要；
- 提示是否被过度塞满；
- 是否发生了不必要的升级；
- 是否遵守了策略约束；
- 工作流是否高效。

对这个支持智能体来说，这一点尤其重要，因为用户看到的最终答复也许还“能接受”，但 run 内部可能已经开始：

- 过度调用 `create_support_ticket`；
- 产生不必要的工具跳转；
- 太早进入升级；
- 在没有足够 grounding 的情况下返回状态。

### 5.1. 行为评测与控制评测评估的不只是答案

随着智能体系统获得更多自主性，仅仅评估“一次运行有没有完成任务”已经不够了，还需要评估“系统在过程中表现出了什么样的行为”。

也正是在这里，

- 行为评测；
- 控制评测；
- 自动化红队测试；

开始变得重要。

它们特别适合那些普通回归集合过于扁平的场景：

- 智能体试图避开监督；
- 它变得过度积极地保留状态；
- 它试图绕过审批路径；
- 它产生了不必要的工具跳转；
- 多个智能体之间的协作开始退化。

也就是说，评测层不应该只评估最终答案质量，还要评估行为层面的失效模式。

这也是验证器设计为什么重要。如果 grading layer 无法区分过程失败与结果失败，它就无法为训练和发布控制提供足够强的证据。

一个好的评测判断可以说“不要继续扩大 rollout”或者“这个场景已经不再可信”；但对这种判断的运营响应属于后面的层次，尤其是 rollout 控制与保证负责人归属。

### 5.2. 协作失效也应该成为评测设计的一部分

如果系统使用交接、管理者模式，或者多个协作智能体，那么只检查“答案对不对”已经不够。

还需要额外观察：

- 交接过程中是否丢失上下文；
- 是否出现相互冲突的动作；
- 验证纪律是否退化；
- 是否出现更多不必要的委派步骤；
- 协作失效能否从追踪中被定位。

因此，多智能体可靠性研究在这里的价值，不是鼓励默认把运行时做得更复杂，而是在提醒我们：编排越复杂，评测设计就必须越丰富。

Anthropic 对 Research 系统的生产复盘还给这里补了一道经济性评测门：如果 multi-agent path 之所以胜出，是因为消耗了更多 token、tool calls 和并行 context windows，那么 release gate 不只要判断答案质量，还要判断这笔预算是否合理。[^anthropic-multi-agent-research] 对广度优先研究来说，这可能是正确权衡；但对共享状态很强的紧密任务，同样的成本增长应该算作架构回归，即使少数样例的最终答案看起来更好。

这个选择的最小 eval 应该在两类任务上比较 single-agent 与 multi-agent 模式：

- **read-heavy breadth-first：** 多个独立来源、分开的 retrieval branches、最终 synthesis；如果质量提升、`token_budget` 可接受，并且 trace 清晰，multi-agent 可以通过；
- **write-heavy shared-state：** 多个步骤修改同一个对象或同一条 incident record；如果出现冲突动作、上下文丢失、额外 approvals 或较高 `merge_conflict_risk`，multi-agent 应该失败或被拦截。

这道 gate 用来防止那个很诱人但错误的结论：“multi-agent 在 research demo 里更好，所以应该到处打开”。

### 5.2.1. Vulnerability harness 是 validation funnel，不是单个 scanner

Cloudflare 描述了同一原则在 security 场景里的一个好版本：vulnerability discovery 只有在 raw findings 经过独立 validation system 后才有用，而不是直接把候选结果当作“bugs”丢给工程团队。[^cloudflare-vulnerability-harness] 它们把 VDH（Vulnerability Discovery Harness）和 VVS（Vulnerability Validation System）分开：VDH 激进地寻找 candidates，VVS 负责 deduplication、judgment 和 fixing。Discovery 可以有噪声、可以受模型波动影响；validation 必须更严格、可复现，并且独立。

对 eval architecture 来说，这个模式几乎可以直接迁移：

- 没有 threat model、affected boundary 和 working PoC/test 的 finding 只能是 candidate，不是 verified issue；
- deterministic checks 应该验证 schema、files、functions、paths、patch/test parseability，并确认原始源码没有被修改来制造 exploit；
- independent validator 不应该有权创建自己的 findings，而应该尝试推翻 hunter；
- triage 应该区分 real-but-latent、wrong-repo、duplicate 和 production-reachable findings；
- fixing gate 应该要求 targeted fail→pass flip，阻止 post-patch failure，并把 branch 留给 human review；
- harness health 应该检测 shallow runs：如果 hunt 异常快速结束，且没有 findings、sibling tasks 或 gapfill work，这更像 tool failure，而不是“没有 bug”的证据。

核心结论是：好的 eval loop 不只是计算 score。它把廉价的模型噪声变成可验证工件，让团队能够 deduplicate、replay、challenge、绑定 owner，并安全地进入 patch review。

### 5.3. 多轮一致性也值得单独检查

最近几个月一个很有价值的信号是：智能体在短场景里看起来可能很合理，但在更长的交互回路中会逐渐滑向自相矛盾。

这在下面这些场景里尤其重要：

- 长对话；
- 依赖累积状态；
- 多次重新评估同一个决定；
- 公开解释自己的理由。

因此最好增加明确的 consistency checks：

- 运行会不会在多个轮次之间自我矛盾；
- 没有新信息时理由会不会自己变化；
- 更长的推敲会不会带来更多而不是更少的矛盾；
- 时间漂移能不能通过追踪被定位出来。

### 5.4. LLM-as-a-judge 只有在完成校准之后才真正有用

随着评测层变得更成熟，几乎总会出现另一个诱惑：引入评判模型，然后默认评分现在就可以几乎自动扩展了。

这确实是有用工具，但前提是不要把它误当成事实本身。

对智能体系统来说，评判器往往有一个很重要的限制：只看最终答案文本通常是不够的。如果评分真正想反映结果，评判器最好还能看到那些真正描述系统行为的东西：

- 追踪片段；
- 工具结果；
- 审批事件；
- 结构化评分字段；
- 在可用时接入外部状态检查。

否则系统很容易因为文本写得漂亮而拿到"高分"，即使事实结果其实很差。

这里还有一个很重要的实用规则：如果评判器与人工的一致性很低，第一步通常不应该是扩大数据集，而应该先分析分歧案例，再修正评分规程或评判提示。

这也符合更广泛的人机交互纪律：当 AI 系统出错时，人需要理解自动化的边界，并且能够纠正行为，而不是盲目接受自动评分。[^amershi][^consensus]

这里一个有用信号是 `Cohen's kappa`，但往往比具体数值更重要的是分歧长什么样：评判器到底是在策略违规、工具误用，还是模糊结果上理解错了。

还有一个很常见的自我欺骗来源：一个在强模型上校准好的评判提示，换到更弱模型后可能迁移得很差。所以评判模型一旦变化，最好重新做校准，而不是假设旧提示还能自动沿用。

最后一个规则非常简单：如果你在评估提示变更，就不要同时改提示和模型。否则后面就无法对"到底是什么改善或恶化了系统"做出诚实的因果判断。

## 6. 评测数据集里应该放什么

一个很常见的错误是：评测数据集主要由舒服的演示场景组成。这种集合几乎帮不上什么忙。

好的数据集通常会包含：

- 顺畅路径任务；
- 含糊的用户请求；
- 提示注入尝试；
- 检索边界案例；
- 缺失数据场景；
- 工具超时和部分失败场景；
- 需要审批的流程；
- 跨租户和隐私敏感场景。

对于这个支持智能体，这意味着数据集里不该只有“检查状态并回复”，还应该有：

- “创建工单，但工具返回模糊结果”；
- “用户发来一句紧急话术，但不能被盲目写成偏好”；
- “检索返回冲突状态”；
- “审批路径必须阻止写动作”。

真正的工程价值，通常正是在这些困难又不舒服的场景里。

还应该加入这样一类案例：行为是正确的，但因为环境侧限制，最终结果仍然不完整。没有这类样本，团队很容易过度优化二元完成，而忽略系统在压力下是否仍然行为正确。

### 6.1. 记忆层也应该显式进入评测数据集

除了回答质量，还应该单独检查状态在多次运行之间的质量。

这意味着要包含这些案例：

- 写入/不写入决策；
- 过期的档案读取；
- 档案记录之间的矛盾；
- 不安全的持久化；
- 删除与修订行为；
- 长时记忆漂移。

否则记忆事故会反复出现在复盘里，却始终回不到回归纪律。

## 7. 回归门禁应该是形式化的，而不是“大家看了一眼”

团队常会说：“我们测过了，感觉没有更差。” 对生产级的智能体系统来说，这远远不够。

回归门禁更有价值的做法，是把它定义为一组明确规则，例如：

- 关键评测集上的成功率不能下降；
- 安全指标不能退化；
- 单任务成本不能超过阈值；
- 升级率不能升高；
- 提示预算或每次运行的工具数量不能超过上限。

对这个支持智能体来说，所谓回归不只是“更不准确了”，还包括：

- 写入工具的重复尝试更多了；
- 不必要的升级更多了；
- 记忆被写入了更多无关内容；
- 解决同类任务的成本变高了。

这样发布决策就不会只依赖改动作者的直觉。

### 7.1. Harness 也应该作为系统的一部分被评测

GitHub Copilot agentic harness 给了一个很有用的生产信号：agent quality 不能被简化成 model quality。[^github-copilot-agentic-harness] Harness 负责 tools、context 和 workflow，因此也应该作为独立层来比较：same model、same benchmark task、归一化的 context window、reasoning effort、tool selection 和 MCP servers，然后再与 model-vendor harness 对照。

对 release gate 来说，这会改变指标集合。除了 task resolution，团队还应该显式观察：

- token efficiency；
- run-to-run variance；
- wall-clock duration；
- tool-call count 和 retry budget；
- 不同任务类别的 cost profile；
- Auto model selection 或其他 model router 的质量；
- memory、context handling 和 skill triggering 的退化。

实际结论是：如果团队改动 harness、context strategy 或 model routing，就需要 harness-level release gate。否则团队很容易误判成“模型变好了”或“模型变差了”，而真正原因其实在 orchestration layer。

### 7.2. 质量回归也可能在产品 harness 里

Anthropic 关于 Claude Code quality reports 的复盘，把同一个问题展示得更直接。[^anthropic-claude-code-quality-reports] 用户感受到 Claude Code、Claude Agent SDK 和 Claude Cowork 的质量下降，但 API 和 inference layer 并不是原因。三个变化都在产品 harness 层：为了 latency 降低 default reasoning effort；stale-session optimization 反复裁掉 older thinking；为了降低 verbosity 加入的 system prompt instruction 又伤害了 coding quality。

对 release gate 来说，这是一个单独的 failure pattern：**model unchanged → harness/config/prompt/context change → quality regression → user reports before eval reproduction**。所以发布检查应该显式版本化 `model_id`、`effort_default`、`context_pruning_policy`、`prompt_bundle_version`、`cache_header_behavior`、`harness_version` 和 `rollout_slice`。否则团队会把问题当成“模型变差”，而真正的回归来自 latency optimization、cache policy 或 prompt hygiene。

这类事故之后的实践契约很具体：prompt changes 要有 per-model eval suite 和 ablation；intelligence/latency tradeoff 要有 soak period 和 gradual rollout；context-pruning changes 要有 stale-session regression cases；dogfooding 要使用 public build，而不只是 internal testing build。User feedback 也应该进入 gate signal，但必须绑定到具体 version slices，否则广泛抱怨会被 normal variance 稀释掉。

## 8. 评测回路的实用规则

如果要把工程规则压缩成一小组，通常这些就够了：

1. 每个重要事故都应该变成一个评测案例和一条 rollout 规则。
2. 离线和在线评测应该一起存在：一个在发布前拦回归，一个在发布后抓漂移。
3. 追踪评分应该优先覆盖关键写路径和策略敏感流程，而不只是顺畅路径。
4. 数据集应该按真实失败刷新，而不只是沿用旧演示案例。
5. 回归门禁应该是机器可读的，并且不仅阻止质量回归，还要阻止安全、成本、升级和验证器契约回归。

## 9. 一个评测门禁策略示例

```yaml
gates:
  offline:
    min_task_success_rate: 0.97
    max_policy_violation_rate: 0.002
    max_avg_cost_delta_pct: 8
  online:
    max_slo_burn_rate: 1.0
    max_manual_intervention_rate: 0.08
    max_unknown_side_effect_rate: 0.0005
  rollout:
    require_offline_pass: true
    require_online_shadow_period: true
```

这些数字不是普适标准。重要的是门禁要可机读，团队对它的争论应发生在标准层，而不是感觉层。

## 10. 一个简单的回归决策示例

下面这个骨架展示的是一个核心思路：发布要绑定在可度量阈值上，而不是绑定在“总体感觉不错”上。

```python
from dataclasses import dataclass


@dataclass
class EvalSummary:
    task_success_rate: float
    policy_violation_rate: float
    avg_cost_delta_pct: float


def passes_regression_gate(summary: EvalSummary) -> bool:
    if summary.task_success_rate < 0.97:
        return False
    if summary.policy_violation_rate > 0.002:
        return False
    if summary.avg_cost_delta_pct > 8:
        return False
    return True
```

代码刻意很简单。恰恰是这种简单性，让门禁对团队而言可理解、可讨论。

## 11. 在线评测必须和发布策略连起来

一个非常有用的做法是不要把大变更一次性打给所有人，而是使用：

- 影子模式；
- 金丝雀 rollout；
- 有限租户暴露；
- model routing experiments；
- 分阶段策略 rollout。

这样在线评测就不只是“上线后看看会不会出事”，而是发布流程中的受控阶段。

对这个支持智能体来说，这意味着：如果新的适配器或新的提示改变了复杂状态案例上的行为，团队应该在金丝雀或影子阶段就看到，而不是等到大范围发布之后。

### 11.1. 好的模拟器不会替代真实数据，只会补充真实数据

也要注意不要高估用户模拟器。

它不能替代：

- 真实生产追踪；
- 真实投诉模式；
- 真实的成本与延迟分布；
- 真实事故复盘。

但它很适合作为离线数据集和在线 rollout 之间的中间层，因为它能更快帮助你检查：

- 对话稳健性；
- 交接行为；
- 升级纪律；
- 回退质量；
- 策略敏感轮次。

### 11.2. Production evals 应该把闭环带回开发

AWS Agent-EvalKit 展示了同一模式的一个实践版本：agent evaluation 不应该只是上线前的一次性 benchmark。[^aws-agent-evalkit] 完整闭环更像一个 pipeline：根据代码和 risk areas 规划评测，生成或导入测试用例，插入 trace instrumentation，让 agent 跑过这些场景，基于 traces 计算指标，并产出带有具体 code-level recommendations 的报告。

Microsoft Foundry 的 Open Trust Stack 给 policy、evals 和 runtime controls 之间补了一条实用连接。[^microsoft-open-trust-stack] ASSERT 提醒我们，eval cases 应该从组织 policies and requirements 生成，而不只是来自临时 regression prompts。Agent Control Specification (ACS) 则用 portable control checkpoints 补上运行时侧：如果 eval 显示 agent 没有满足 policy requirement，修复不应该只是一段 prompt change，还应该可能落在 tool call 之前、tool result 之后，或 external action 之前的控制点。

Google Cloud Agent Platform 把这个闭环的 production 侧说得更具体：**Online Monitors** 会持续从 Cloud Trace 和 Cloud Logging 中抽样已部署 agent 的 traces，运行配置好的 evaluation metrics，把结果写回 Cloud Logging，并把数字分数导出到 Cloud Monitoring。[^google-evaluate-agents][^google-agent-online-monitors] 可移植契约不是“看 dashboard”，而是 **live trace → sampled eval → score → alert or regression gate → reviewed improvement**。每条被抽样的记录都应该保留 `trace_id`、`agent_version`、`tool_calls`、`expected_outcome`、`grader_version`、`score`、`failure_mode` 和 `review_required`，这样团队才能复现当时的判断，并跨 release 比较。

Google 的 Discovery Bench 还补了第二个提醒：团队也要 **evaluate your evals**。[^google-evaluate-agent-performance] Benchmark 可能隐藏脆弱的 ground truth、不稳定的难度，或看不见 cliff 的 pass/fail threshold：用户请求只要稍微更模糊，agent 就可能突然崩掉。因此成熟的 eval loop 也要校准 evaluator 本身：测量任务难度，检查 disagreement，版本化 rubrics，并把 grader drift 当成 release risk。

这里重要的不是某个具体 toolkit，而是闭环形状。Production traces 不应该只变成 dashboards；它们还应该变成新的 test cases、regression thresholds 和 code-level fixes。如果真实流量显示 agent 在空 tool output 之上仍然给出漂亮答案，这不只是 observability signal。它也是未来针对 faithfulness、tool-use discipline 和 fallback behavior 的 eval case。

在成熟闭环里，每次有意义的变更之后，团队都应该能做到：

- 复用已有 test cases 和 instrumentation；
- 从 production logs 或人工复盘里补充场景；
- 比较不同 agent versions 的报告；
- 把 failed metric 绑定到具体 trace 和 code location；
- 在 sampled production traces 上跑质量检查，而不只依赖合成数据。

这样 eval loop 才会变成 release discipline：它接收来自开发、生产、事故和专家复盘的信号，再返回的不是“分数变差了”，而是下一次变更可以审查、可以执行的工作。

## 12. 评测文化最常见的崩坏点

这些问题很常见：

- 离线评测太像玩具；
- 在线评测和追踪断开；
- 回归门禁只看成功率；
- 安全回退不阻止发布；
- 成本回退不被当成真正的回退；
- 数据集不更新，系统开始优化陈旧场景。

一旦如此，评测闭环就会退化成仪式，而不是改进机制。

## 13. 给评测回路做一次快速成熟度测试

团队不应该只因为会跑基准集合、偶尔看几项在线指标，就觉得自己已经有评估纪律。

更高的标准应该是：

- 事故会被转化成评测案例和 rollout 规则；
- 离线和在线评测作为同一个闭环运行，而不是两个分开的仪式；
- 回归门禁不只拦任务失败，也会拦安全、成本、升级和验证器契约回归；
- 追踪被当成证据来评分，而不是被动堆成遥测；
- 数据集会持续从真实失败中学习。

如果这些条件大多不成立，那团队也许已经有一些评估活动，但还没有真正的学习回路。

## 14. 读完这一章后先做什么

如果你想快速检查评测闭环，可以先过一遍这个短清单：

1. 是否有针对关键场景的精选离线评测集？
2. 是否有和追踪、SLO 相连的在线评测信号？
3. 是否不仅能评估最终答案，也能评估运行过程本身？
4. 发布前是否存在形式化的回归门禁？
5. 是否把安全和成本也放进了门禁，而不只是任务成功率？
6. 评测数据集是否会依据真实事故持续更新？

如果连续几个答案都是否，那说明你可能已经有评测层，但还没有真正强健的判断层。

这时团队也许已经有评分活动，但还没有形成那种足以让后续运营功能稳定依赖的可审查评测纪律。

## 15. 本章的证据模型

本章应该被读成一套 judgment model，而不是 benchmark checklist：

- **稳定主张：** final-answer success 不够；evals 需要覆盖 process quality、outcome quality、failure attribution 和 regression gates。
- **厂商实践：** Google Cloud 的 agent governance guidance 和现代 agent-platform 材料都把 evals 视为 rollout 与 operational control 的一部分，而不只是模型选择。
- **研究与 human-AI practice：** human-centered evaluation 相关工作提醒我们，apparent agreement 或 user satisfaction 可能掩盖薄弱的 judgment signals。
- **运行时实践：** trace-linked eval rows、verifier outputs、rollout gates 和 failed-run reasons 让 eval evidence 可以被 operators 审查。
- **另一种观点：** automated judges 很有吸引力，因为它们可以扩大 review 规模并减少 human bottleneck。本章承认这种价值，但把 judge output 视为需要校准的 evidence，而不是必须服从的 authority；高风险 rollout decisions 仍然需要 disagreement review、明确的 rubric owner 和 trace-backed attribution。
- **作者解释：** 本书把 evals 视为 observability 与 lifecycle governance 之间的 release-judgment layer。
- **快速变化层：** judge models、simulators 与 automated red-team techniques 会快速变化；但 explicit gates 与 attributable failures 的需求不会。

!!! note "适合印刷的章节结尾"
    在一页里，本章应该留下三个决策：哪个评测数据集检查行为；哪份验证器契约把一次运行变成裁决；哪个发布门禁在出现回归时阻止发布。

## 16. 接下来读什么

到这里，第五部分已经形成一个完整的运行闭环：追踪、SLO 和评测回路。下一步就是组织模型，因为这种平台最终既会碰到代码问题，也会碰到团队设计问题。

## 17. 值得配套阅读的参考页

- [追踪模式与事件目录](../../appendix/trace-schema.zh.md)
- [评测数据集模式与打分契约](../../appendix/eval-schema.zh.md)
- [生命周期工件模式](../../appendix/lifecycle-artifact-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第 25 章：行为评测、控制评测与自动化红队测试](../part-viii/chapter-25.zh.md)
- [第 14 章：平台团队与产品团队](../part-vi/chapter-14.zh.md)
- [第五部分：可靠性与可观测性](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
[^amershi]: Microsoft Research, [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
[^consensus]: OpenReview, [The Illusion of Consensus in Human-Centered Interactive AI](https://openreview.net/forum?id=eJtBEBmYGB)

[^anthropic-multi-agent-research]: Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system).
[^openai-deployment-simulation]: OpenAI, [Predicting model behavior before release by simulating deployment](https://openai.com/index/deployment-simulation/).
[^github-qubot]: GitHub Blog, [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/).
[^github-copilot-agentic-harness]: GitHub Blog, [Evaluating performance and efficiency of the GitHub Copilot agentic harness across models and tasks](https://github.blog/ai-and-ml/github-copilot/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/).
[^anthropic-claude-code-quality-reports]: Anthropic, [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem), 23 April 2026.
[^langchain-state-agent-engineering]: LangChain, [State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering).
[^openai-deprecations]: OpenAI, [Deprecations](https://developers.openai.com/api/docs/deprecations).
[^cloudflare-vulnerability-harness]: Cloudflare Blog, [Build your own vulnerability harness](https://blog.cloudflare.com/build-your-own-vulnerability-harness/).
[^aws-agent-evalkit]: AWS, [Evaluate AI agents systematically with Agent-EvalKit](https://aws.amazon.com/blogs/machine-learning/evaluate-ai-agents-systematically-with-agent-evalkit/).
[^microsoft-open-trust-stack]: Microsoft Foundry Blog, [Build agents you can trust across any framework with open evals and a control standard](https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/).
[^google-agent-online-monitors]: Google Cloud, [Continuous evaluation with online monitors](https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/evaluation/evaluate-online).
[^google-evaluate-agents]: Google Cloud, [Evaluate your agents](https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/evaluation/evaluate-agents).
[^google-evaluate-agent-performance]: Google Cloud Blog, [Evaluate agent performance](https://cloud.google.com/blog/products/data-analytics/evaluate-agent-performance).
[^aws-toolsimulator]: AWS, [ToolSimulator: scalable tool testing for AI agents](https://aws.amazon.com/blogs/machine-learning/toolsimulator-scalable-tool-testing-for-ai-agents/).
