# 变更评审与发布门禁 Schema

这一页把智能体系统里的变更评审和发布门禁所需的最小契约层放在一起。它适合用在这样一个阶段：团队已经知道策略、提示、模型路由、检索和工具暴露这些变化不能“凭感觉发布”，但还没有把这些检查沉淀成明确工件。

如果 [生命周期工件 Schema](lifecycle-artifact-schema.zh.md) 回答的是“生命周期里应该有哪些实体”，那么变更与发布门禁 Schema 回答的就是“真正做发布决策时，到底需要哪些字段”。

## 1. 为什么需要单独的 Schema 层

在很多智能体系统里，变更评审会裂成几个互不相连的片段：

- 拉取请求里的工程评审；
- 单独文档里的安全评审；
- CI 里的评测结果；
- 聊天里或会议里口头做出的发布决定。

系统规模还小时，这看起来还能勉强运转。但一旦开始有多个负责人、高风险动作和分阶段发布，这套方式就会失去可控性。

一个机器可读的 Schema 层之所以有价值，是因为它能：

- 把变更记录和评测要求绑在一起；
- 把发布门禁变成显式工件，而不是团队记忆；
- 固定发布策略和影响半径；
- 缩短事故复盘与回滚的路径。

## 2. 核心实体

一个最小可用的 Schema 层，通常围绕两个实体就够了：

- `change_review_record`
- `rollout_gate_record`

这已经足够把第五部分、第七部分和第八部分串成一条完整的运行纪律。

## 3. 变更评审记录

`change_review_record` 用来描述：改了什么、谁审过、上线前必须满足哪些条件。

```yaml
kind: change_review_record
review_id: cr-2026-04-07-001
change_id: chg-2026-04-07-001
owner: platform-runtime
change_type: policy_update
risk_level: high
affected_surfaces:
  - policy_bundle
  - approval_contract
  - delegated_authorization_contract
  - failed_run_handling
  - rollout_rules
required_reviews:
  - engineering
  - safety
  - runtime_owner
required_evals:
  - offline_regression
  - targeted_safety_eval
  - trace_regression_check
  - failed_run_drill
  - verifier_quality_check
status: approved
```

这里最关键的字段是：

- `affected_surfaces` 防止高风险变化伪装成“小调整”；
- `required_reviews` 让负责人显式化；
- `required_evals` 避免每次都重新争论到底该跑什么；
- `status` 是运行事实，而不是漂亮的说明文字。

## 4. 发布门禁记录

`rollout_gate_record` 关注的不是变化本身“好不好”，而是系统是否准备好把它投放到某一波发布中。

```yaml
kind: rollout_gate_record
gate_id: gate-2026-04-07-001
change_id: chg-2026-04-07-001
bundle_id: bundle-2026-04-07-a
rollout_wave: canary
traffic_scope: 5_percent
required_checks:
  - telemetry_ready
  - oncall_ready
  - rollback_plan_ready
  - approval_path_verified
  - high_risk_flow_checked
  - failed_run_traceability_verified
blocking_findings: []
decision: go
# failed_run_traceability_verified 意味着已经检查退化路径、
# 追踪、发布身份，以及像 failure_reason 这样的导出字段。
decided_by:
  - runtime_owner
  - safety_owner
```

这一层重要的原因在于：一个好的变更评审，并不自动等于“现在就可以发布”。

当发布依赖更丰富的验证器输出，而不是只看二元通过 / 失败状态时，这一点会更重要。此时门禁记录应该显式写出：受影响的高风险路径是否已经审过验证器质量与证据链接。

一旦运行时里已经有审批和有状态能力会话，门禁还应该明确说明：中断行为是否被单独审过，而不是默认“应该没问题”。

## 5. 变更评审和发布门禁的区别

这两层经常被混在一起，但它们其实回答的是不同问题：

- `change_review_record` 回答：“这个变化原则上能不能发布？”
- `rollout_gate_record` 回答：“这个变化现在能不能发、以及该以多大范围发？”

所以字段也应该不同：

- 评审更关注变更类型、风险和必需评测；
- 发布门禁更关注遥测、值班、回滚、流量范围、上线准备度，以及审批绑定或有状态能力路径的中断处理。

在实践里，这通常还意味着门禁需要显式说明：

- 发布前是否验证过能力会话过期行为；
- 对受影响路径而言，重新初始化是拒绝、允许还是需要审批绑定；
- 运行追踪、审批记录与会话导出之间的委派授权连续性是否已验证；
- 编排模式变更是否在发布前被当成运行时控制变更单独评审；
- 如果中断语义在发布后开始漂移，紧急冻结由谁负责。

## 6. 它和评测 Schema 的关系

变更评审与发布门禁和 [评测 Schema](eval-schema.zh.md) 是紧密耦合的：

- 评审会声明哪些评测是必须的；
- 门禁会判断这些结果是否足够支撑当前发布波次；
- 事故与发现结果后续还会回流进必需检查；
- 验证器回归与证据链接失败也会成为和发布相关的发现结果。

也就是说，评测层不是独立存在的，而是门禁的一根支柱。

## 7. 它和追踪 Schema 的关系

一旦追踪 Schema 完整，发布门禁就会强很多：

- 追踪能看出高风险路径是否真的被覆盖；
- 会话摘要能看出是否已经出现回归；
- 结构化事件能说明上线前到底检查了什么；
- 中断与过期信号能看出审批绑定运行是否在操作员注意到之前就已经开始退化；
- 验证器证据能说明发布评审所依赖的过程 / 结果判断是否真的可追溯。

这也是为什么成熟团队里，追踪与发布门禁往往是并排建设的。

失败运行证据也应该一路进入发布判断。如果超时密集的工具路径、校验失败或上游依赖故障只被看成普通的失败演示运行，发布门禁就无法区分产品风险和运行时退化。成熟的门禁应该能看见这些失败运行是否被专门演练过、它们的追踪与具体失败原因，例如 `failure_reason`，是否仍然可供评审，以及顺利路径和退化路径是否都受同一个发布身份治理。

## 8. 它和参考包的关系

[agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) 已经包含了这套模型的一部分：

- [rollout.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/rollout.py)
- [lifecycle.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/lifecycle.py)
- [configs/rollout.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/rollout.yaml)
- [configs/change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
- [configs/runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)
- CLI：
  - `check-rollout`
  - `check-change`

这让书里不只是能解释门禁的概念，还能直接给出一个可运行的骨架。

## 9. 最小不变量

一个健康的变更发布层，至少应该保证：

- 高风险变更没有评审记录就不能进入发布；
- 发布门禁必须指向明确的 `bundle_id` 和 `rollout_wave`；
- 必需检查和阻断性发现结果必须显式可见；
- 每个决定都有负责人；
- 事故追踪可以还原出评审和门禁；
- 审批绑定或有状态能力会话的中断行为会在发布前被检查；
- 能力会话的过期与重新初始化行为会在发布前被检查；
- 运行追踪、审批记录与会话导出之间的委派授权连续性会在发布前被检查；
- 如果发布控制依赖打分结果，验证器质量与证据链接也会在发布前被检查；
- 编排模式变更会在发布前被检查，尤其是它们引入路由、并行化或委派工作器表面时；
- 回滚计划不能只存在于人的脑子里。

## 10. 最常见的断裂点

常见问题通常长这样：

- 评审和发布决定分散在不同地方，彼此不相连；
- 门禁标准没有版本；
- 遥测准备度靠肉眼判断；
- 安全发现结果没有被当作阻断项；
- 验证器质量或证据链接被默认假定，而不是被检查；
- 能力会话过期或重新初始化行为没有被建模；
- 编排模式变更被当成“实现细节”溜过去，没有显式评审；
- 发布波次的定义太模糊；
- 没人能解释为什么这个变更居然能进金丝雀发布。

## 11. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 高风险变更是否有明确的评审记录？
- 是否真的有独立的发布门禁，而不是只有一句“评审已批准”？
- 是否能清楚看到发布前必须通过哪些检查？
- 是否能看到 `change_id -> bundle_id -> rollout_wave` 这条链？
- 当打分结果会影响发布时，验证器质量与证据链接检查是否可见？
- 阻断性发现结果和决策负责人是否被保留？
- 事故复盘时能不能还原出到底是哪个门禁放行了这个变化？

如果连续几个答案都是“否”，那说明你可能已经有了变更流程，但还没有真正完整的发布门禁层。

## 下一步做什么

- [评测数据集 Schema 与打分契约](eval-schema.zh.md)
- [生命周期工件 Schema](lifecycle-artifact-schema.zh.md)
- [策略包 Schema 与审批契约](policy-bundle-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 18 章：生产上线检查清单](../book/part-vii/chapter-18.zh.md)
- [第 20 章：智能体系统的变更管理](../book/part-viii/chapter-20.zh.md)
