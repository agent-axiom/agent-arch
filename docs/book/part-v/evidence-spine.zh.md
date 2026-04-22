# Evidence Spine：从请求到 rollout judgment

这页把一个结构性判断明确写出来：在 production agent system 里，不能把 tracing、policy、approvals、evals、incident review 和 rollout judgment 看成只是彼此相邻的话题。

它们其实是一条统一的运行记录。

如果你没法沿着这些层一路追踪同一个 run，那你还没有 evidence spine，你只有彼此断开的 controls。

## 读完这页后，你应该能够

- 解释为什么追踪、policy、approvals、evals、incidents 与 rollout judgment 属于同一条受治理记录；
- 说清楚让一次可疑 run 保持可审查所需的最小标识符集合；
- 展示 runtime behavior、人工决策、lifecycle artifacts 与 release judgment 如何在不靠猜测的情况下连起来。

## 为什么需要这页

书里已经有几章分别讲了这条链上的不同部分：

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)
- [第 17 章：策略层与能力目录](../part-vii/chapter-17.zh.md)
- [第 20 章：智能体系统的 Change Management](../part-viii/chapter-20.zh.md)
- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](../part-viii/chapter-21.zh.md)
- [第 22 章：Supply Chain、Provenance 与 Approved Artifacts](../part-viii/chapter-22.zh.md)

但这些章节之间还缺一页明确的桥接页，用一次清楚的 walkthrough 展示：同一个受治理的 run，怎样从 user request 一直保持可追溯，一直到 rollout judgment。

这就是这页的任务。

## 核心判断

Evidence spine 是一种最小但受治理的连续性，它能让操作人员在不靠猜测的情况下回答这些问题：

- 是哪个 request 启动了这个 run；
- 当时激活的是哪个 policy bundle 和哪一个 release identity；
- 调用了哪些 tools；
- approval 是必需的、被 granted、被 denied，还是已经 expired；
- 产生了哪些 trace events 和 structured signals；
- 这个 run 之后是怎样被 graded 或 evaluated 的；
- 它有没有触发 incident review；
- 这些 evidence 最终是否改变了 rollout judgment。

这一点对 degraded paths 也必须成立。只有当同一条链仍然能解释是哪一个 release identity 在治理这次失败、是哪条 trace 把它保留下来、哪一个具体失败原因，例如 `failure_reason` 字段，仍然可见、它是怎样被 graded 的，以及它是否改变了 rollout judgment，failed-run drill 才真正有意义。

如果缺少这种连续性，团队也许仍然拥有 traces、approval logs 和 eval reports，但依然没有一条可复核的统一运行记录。

## 最小共享实体图

强健的 evidence spine 并不要求一个巨大的统一 schema，但它要求各层之间有一组稳定的标识符和链接。

至少，一个受治理的 run 应该能通过这些实体保持可读：

- `run_id`，运行时的执行身份；
- `trace_id`，这个 run 的 trace 或 event lineage；
- `approval_id`，在需要审批时的人类门禁记录；
- `policy_bundle_version`，该 run 所处的受治理策略表面；
- `artifact_id`，与 release surface 相关联的 approved artifact 或 artifact bundle；
- `evaluation_result_id`，后续附加的 grading 或 judgment 记录。

在更成熟的系统里，这条链通常还会包括：

- `release_identity`；
- `change_id`；
- `session_id`；
- `incident_id`；
- `verifier_contract_id` 或 verifier bundle 的 lineage。

这里重点不是命名是否完美，而是链接是否可复核。

<div class="diagram-card">
<p>把 evidence spine 看成一串相互链接的记录，会比把它看成一堆分散工件更有用</p>

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
    I --> J["rollout judgment"]
```

</div>

## 一个端到端 run walkthrough

设想一个 support-triage agent，它可以分类用户请求、检索内部知识，并且只在 high-risk 情况下经过 approval 后创建 ticket。

### 第一步：user request 进入系统

用户发送一条消息，请求为某个生产客户问题创建 ticket。

此时系统至少应该创建：

- 这次执行的 `run_id`；
- 对应事件链的 `trace_id`；
- 指向当前 `policy_bundle_version` 和 `release_identity` 的链接。

如果团队之后无法证明到底是哪一个受治理的 release surface 处理了这次请求，那么在第一次 tool call 之前，这条链就已经是脆弱的了。

### 第二步：policy evaluation 决定接下来允许发生什么

策略层会决定：

- 这个 capability 是否对当前 tenant 和 actor 可用；
- 是否允许检索内部知识；
- 创建 ticket 是否需要 approval；
- 是否允许 delegated authorization；
- high-risk handling 是否要求 verifier contract。

这也是为什么[第 17 章](../part-vii/chapter-17.zh.md)属于 evidence spine 的一部分。Policy 不是静态配置附录，而是解释这次 run 为什么被允许或禁止继续的重要 evidence。

### 第三步：tool calls 与 runtime events 形成原始历史

Runtime 会检索上下文，也许会先分类问题，并准备一个拟议中的 ticket payload。

这时，[第 11 章](chapter-11.zh.md)就体现为原始 evidence 层。Run 应该发出结构化事件，让操作人员事后能看清：

- 哪些输入被接受或拒绝；
- 哪些 tool calls 被尝试了；
- 是否发生了 retries；
- session 是否 pause 过；
- 输出是否被 redacted；
- degraded paths 的具体失败原因，例如 `failure_reason` 字段，是否被保留下来，以及它在 review 当时是否仍出现在像 `latest_failure_reason` 这样的 operator-facing summary 里；
- 系统究竟停在 side effects 之前的哪个位置。

没有这一层，后面的 judgment 就会变成讲故事，而不是做重建。

### 第四步：approval 生成人的决策记录

策略层要求在创建 ticket 之前先完成 approval。

此时应该创建或绑定一个 `approval_id`，并把它链接回：

- `run_id`；
- `trace_id`；
- `policy_bundle_version`；
- `release_identity`；
- 被请求的 capability 与 risk tier。

如果 approval 被 denied，这不只是一次交互结果，而是受治理 run 历史的一部分。

如果 approval expired，这同样是 evidence，不应该消失在 UI 状态里。

### 第五步：eval 与 grading 把历史变成 judgment

之后，这个 run 可能进入 offline review、online grading 或 regression comparison。

这时，[第 13 章](chapter-13.zh.md)进入 evidence spine。Eval 层不应该像一张独立的评分表那样漂浮在外，它应该把 judgment 绑定回产生该行为的具体 run、trace 和受治理 release surface。

这样团队才能区分：

- 一次性故障；
- 策略回归；
- 只属于某个 release 的退化；
- verifier trust 问题；
- approval path 故障。

### 第六步：incident review 把 evidence 变成 operational response

如果这个 run 暴露了严重问题，[第 21 章](../part-viii/chapter-21.zh.md)就会开始发挥作用。

此时团队需要一条连贯记录，能显示：

- 到底发生了什么；
- 哪些 controls 起作用了；
- 哪些 controls 缺失了；
- approval 的介入是否正确；
- 问题究竟属于 runtime、policy bundle、release artifact、verifier contract，还是 operator workflow。

如果这些链接不存在，incident review 就会变成跨系统考古。

### 第七步：rollout judgment 依赖同一条链

最后，[第 20 章](../part-viii/chapter-20.zh.md)会利用这条证据链来回答 release 问题：

- rollout 能不能继续；
- 是否需要暂停；
- 是否需要回滚；
- policy bundle 是否需要修订；
- artifact set 是否需要替换；
- approval contract 是否需要收紧。

这也是 evidence spine 如此重要的最后一个原因。Rollout judgment 不应只依赖直觉或 dashboard，而应依赖一条已经把 runtime behavior、controls、approval、evidence 与 release identity 串起来的链。

## 一个工件层级的例子

同一条受治理运行记录，压缩后可以长这样：

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

这个例子的重点不在于字段必须完全一样，而在于一次可疑 run 应该留下足够多的链接，让团队可以从 runtime behavior 一路走到 approval record、eval judgment、incident review 和 rollout action，而不需要手工重新拼整条链。

## 操作人员应该能重建什么

面对一次可疑 run，操作人员应该能很快回答下面所有问题：

- 是哪个 request 触发了它；
- 是哪个 release identity 处理了它；
- 是哪个版本的 policy bundle 在约束它；
- approval 是否被请求，以及结果是什么；
- 哪些 trace events 描述了它的路径；
- 是哪条 eval 或 grading record 给出了 judgment；
- 这次 run 是否影响了 incident 或 rollout decision。

如果这些问题里有任何一项只能靠猜，那 evidence spine 就还不完整。

## 这页不替代什么

这页不会取代周围那些章节：

- 第 11 章仍然负责 raw evidence capture；
- 第 13 章仍然负责 reviewable judgment；
- 第 17 章仍然负责受治理 runtime policy；
- 第 20 章仍然负责 release judgment；
- 第 21 章仍然负责 assurance response；
- 第 22 章仍然负责 provenance、artifact lineage 与 evidence backbone。

这页只是把它们之间的连接组织明确写出来。

## 接下来读什么

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)
- [第 17 章：策略层与能力目录](../part-vii/chapter-17.zh.md)
- [第 20 章：智能体系统的 Change Management](../part-viii/chapter-20.zh.md)
- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](../part-viii/chapter-21.zh.md)
- [第 22 章：Supply Chain、Provenance 与 Approved Artifacts](../part-viii/chapter-22.zh.md)
