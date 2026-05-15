# Evidence Spine：从请求到发布判断

在生产智能体系统里，追踪、策略、审批、评测、事故评审和发布判断不应该被看成只是彼此相邻的话题。对于操作员来说，它们是一条统一的运行记录。

如果你无法沿着这些层一路追踪同一个可疑运行，那你还没有 Evidence Spine，只有彼此断开的控制。

## 读完这页后，你应该能够

- 解释为什么追踪、策略、审批、评测、事故与发布判断属于同一条受治理记录；
- 说清楚让一次可疑运行保持可审查所需的最小标识符集合；
- 展示运行时行为、人工决策、生命周期工件与发布判断如何在不靠猜测的情况下连起来。

## 为什么需要这页

书里已经有几章分别讲了这条链上的不同部分：

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)
- [第 17 章：策略层与能力目录](../part-vii/chapter-17.zh.md)
- [第 20 章：智能体系统的变更管理](../part-viii/chapter-20.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](../part-viii/chapter-21.zh.md)
- [第 22 章：供应链、来源追踪与已批准工件](../part-viii/chapter-22.zh.md)

这页把它们收拢成一条端到端串讲，用来展示同一个受治理运行如何从用户请求一直保持可追溯，直到发布判断。

## 核心判断

Evidence Spine 是一种最小但受治理的连续性，它能让操作员不靠猜测地回答下面这些问题：

- 是哪个请求启动了这个运行；
- 当时激活的是哪个策略包和哪一个发布身份；
- 调用了哪些工具；
- 审批是必需的、已批准、已拒绝，还是已经过期；
- 产生了哪些追踪事件和结构化信号；
- 这个运行之后是怎样被评分或评测的；
- 它有没有触发事故评审；
- 这些证据最终是否改变了发布判断。

这一点对退化路径也必须成立。只有当同一条链仍然能解释是哪一个发布身份在治理这次失败、是哪条追踪把它保留下来、哪一个具体失败原因（例如 `failure_reason`）仍然可见、它是怎样被评分的，以及它是否改变了发布判断，失败运行演练才真正有意义。

如果缺少这种连续性，团队也许仍然拥有追踪、审批日志和评测报告，但依然没有一条可复核的统一运行记录。

**Case-spine routing note：**同一条 evidence spine 应该在本书三个 canonical cases 中都保持可见。Support triage 重点考验 approvals 和 side effects；Internal knowledge assistant 重点考验 retrieval provenance、freshness 和 access control；Incident coordination 重点考验 escalation、response ownership 和 post-incident rollout judgment。如果某个 control 只适用于一个 case，它只是 local feature，而不是 evidence spine。

## 最小共享实体图

强健的 Evidence Spine 不需要一个巨大的统一 schema 文件，但它要求各层之间有一组稳定的标识符和链接。

至少，一个受治理运行应该能通过这些实体保持可读：

- `run_id`，运行时的执行身份；
- `trace_id`，这个运行的追踪或事件谱系；
- `approval_id`，在需要审批时的人类门禁记录；
- `policy_bundle_version`，该运行所处的受治理策略表面；
- `artifact_id`，与发布表面相关联的已批准工件或工件包；
- `evaluation_result_id`，后续附加的评分或判断记录。

在更成熟的系统里，这条链通常还会包括：

- `release_identity`；
- `change_id`；
- `session_id`；
- `incident_id`；
- `verifier_contract_id` 或验证器契约包的谱系；
- `handoff_artifact_id`，当长时间运行的工作跨越上下文重置或角色交接边界时尤其如此。[^anthropic-harness]

重点不在术语是否完美，而在这些链接是否可复核。

<div class="diagram-card">
<p>把 Evidence Spine 看成一串相互链接的记录，会比把它看成一堆分散工件更有用</p>

``` mermaid
flowchart LR
    A["run_id"] --> B["trace_id"]
    A --> C["policy_bundle_version"]
    A --> D["approval_id"]
    A --> E["evaluation_result_id"]
    C --> F["release_identity"]
    C --> G["artifact_id"]
    E --> H["verifier_contract_id"]
    E --> I["incident_id"]
    I --> J["发布判断"]
```

</div>

## 一个端到端运行串讲

设想一次 Support triage run，它可以分类用户请求、检索内部知识，并且只在高风险情况下经过审批后创建工单。

### 第一步：用户请求进入系统

用户发送一条消息，请求为某个生产客户问题创建工单。

此时系统至少应该创建：

- 这次执行的 `run_id`；
- 对应事件链的 `trace_id`；
- 指向当前 `policy_bundle_version` 和 `release_identity` 的链接。

如果团队之后无法证明到底是哪一个受治理的发布表面处理了这次请求，那么在第一次工具调用之前，这条链就已经是脆弱的了。

### 第二步：策略评估决定接下来允许发生什么

策略层会决定：

- 这个能力是否对当前租户和行动者可用；
- 是否允许检索内部知识；
- 创建工单是否需要审批；
- 是否允许委派授权；
- 高风险处理是否要求验证器契约。

这也是为什么[第 17 章](../part-vii/chapter-17.zh.md)属于这条链的一部分。策略不只是静态配置层，它还是解释这次运行为什么被允许或禁止继续的重要证据。

### 第三步：工具调用与运行时事件形成原始历史

运行时会检索上下文，也许会先分类问题，并准备一个拟议中的工单载荷。

这时，[第 11 章](chapter-11.zh.md)就体现为原始证据层。运行应该发出结构化事件，让操作员事后能看清：

- 哪些输入被接受或拒绝；
- 哪些工具调用被执行了；
- 是否发生了重试；
- 会话是否暂停过；
- 输出是否被脱敏；
- 退化路径的具体失败原因（例如 `failure_reason`）是否被保留下来，它在评审时是否仍出现在像 `latest_failure_reason` 这样的操作员可见摘要里，以及这次运行在会话评审中是否仍然计入 `traceable_failed_runs`；
- 系统究竟停在副作用之前的哪个位置。

没有这一层，后面的判断就会变成讲故事，而不是做重建。

### 第四步：审批生成人的决策记录

策略层要求在创建工单之前先完成审批。

此时应该创建或绑定一个 `approval_id`，并把它链接回：

- `run_id`；
- `trace_id`；
- `policy_bundle_version`；
- `release_identity`；
- 被请求的能力与风险等级。

如果审批被拒绝，这不只是一次交互结果，而是受治理运行历史的一部分。

如果审批已过期，这同样是证据，不应该消失在界面状态里。

### 第五步：评测与评分把历史变成判断

之后，这个运行可能进入离线评审、在线评分或回归对比。

这时，[第 13 章](chapter-13.zh.md)进入这条链。评测层不应该像一张独立的评分表那样漂浮在外，它应该把判断绑定回产生该行为的具体运行、追踪和受治理发布表面。

这样团队才能区分：

- 一次性故障；
- 策略回归；
- 只属于某个发布的退化；
- 验证器信任问题；
- 审批路径故障。

### 第六步：事故评审把证据变成运营响应

如果这个运行暴露了严重问题，[第 21 章](../part-viii/chapter-21.zh.md)就会开始发挥作用。

此时团队需要一条连贯记录，能显示：

- 到底发生了什么；
- 哪些控制起作用了；
- 哪些控制缺失了；
- 审批的介入是否正确；
- 问题究竟属于运行时、策略包、发布工件、验证器契约，还是操作员工作流。

如果这些链接不存在，事故评审就会变成跨系统考古。

### 第七步：发布判断依赖同一条链

最后，[第 20 章](../part-viii/chapter-20.zh.md)会利用这条证据链来回答发布问题：

- rollout 能不能继续；
- 是否需要暂停 rollout；
- 是否需要回滚；
- 策略包是否需要修订；
- 工件集是否需要替换；
- 审批契约是否需要收紧。

这也是 Evidence Spine 如此重要的最后一个原因。发布判断不应只依赖直觉或仪表盘，而应依赖一条已经把运行时行为、控制、审批、证据与发布身份串起来的链。

## 一个工件层级的例子

同一条受治理的记录可以压缩成这样：

```yaml
run_id: run-support-042
trace_id: trace-support-042
session_id: session-support-007
policy_bundle_version: 2026.04.19
release_identity: release-support-triage-2026-04-19-canary
approval_id: approval-118
artifact_id: artifact-bundle-2026-04-19-a
change_id: change-2026-04-19-17
verifier_contract_id: verifier-contract-v3
evaluation_result_id: eval-result-042
incident_id: incident-2026-04-19-3
latest_rollout_decision: pause-canary
```

这个例子的重点不在于字段是否完全一致，而在于一次可疑运行应该留下足够多的链接，让团队能从运行时行为走到审批记录、评测判断、事故评审和发布动作，而不必手工重建整条链。

## 操作员应该能重建什么

面对一次可疑运行，操作员应该能很快回答下面这些问题：

- 是哪个请求触发了它；
- 是哪个发布身份处理了它；
- 是哪个版本的策略包在治理它；
- 审批是否被请求，以及结果是什么；
- 哪些追踪事件描述了这条路径；
- 是哪条评测或评分记录给出了判断；
- 这次运行是否影响了事故或 rollout 决策。

如果其中任何一个答案都需要靠猜测，那 Evidence Spine 就还不完整。

## 这页不替代什么

这页不会替代周围章节：

- 第 11 章仍然负责原始证据捕获；
- 第 13 章仍然负责可评审判断；
- 第 17 章仍然负责受治理运行时里的策略；
- 第 20 章仍然负责发布判断；
- 第 21 章仍然负责保障响应；
- 第 22 章仍然负责来源证明、工件谱系与证据骨架。

这页只是把它们之间的连接组织显式写出来。

## 接下来读什么

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)
- [第 17 章：策略层与能力目录](../part-vii/chapter-17.zh.md)
- [第 20 章：智能体系统的变更管理](../part-viii/chapter-20.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](../part-viii/chapter-21.zh.md)
- [第 22 章：供应链、来源追踪与已批准工件](../part-viii/chapter-22.zh.md)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
