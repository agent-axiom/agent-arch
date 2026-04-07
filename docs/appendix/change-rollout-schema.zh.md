# Change Review 与 Rollout Gate Schema

这一页把 agent systems 里的 change review 和 rollout gate 所需的最小 contract layer 放在一起。它适合用在这样一个阶段：团队已经知道 policy、prompt、model routing、retrieval 和 tool exposure 这些变化不能“凭感觉发布”，但还没有把这些检查沉淀成明确的 artifacts。

如果 [lifecycle artifact schema](lifecycle-artifact-schema.zh.md) 回答的是“lifecycle 里应该有哪些实体”，那么 change-rollout schema 回答的就是“真正做发布决策时，到底需要哪些字段”。

## 1. 为什么需要单独的 schema layer

在很多 agent system 里，change review 会裂成几个互不相连的片段：

- pull request 里的 engineering review；
- 单独文档里的 safety review；
- CI 里的 eval results；
- 聊天里或会议里口头做出的 rollout decision。

系统小时候，这看起来还能勉强运转。但一旦开始有多个 owners、high-risk actions 和 staged rollout，这套方式就会失去可控性。

一个 machine-readable layer 之所以有价值，是因为它能：

- 把 change record 和 eval requirements 绑在一起；
- 把 release gate 变成显式 artifact，而不是团队记忆；
- 固定 rollout strategy 和 blast radius；
- 缩短 incident review 与 rollback 的路径。

## 2. 核心实体

一个最小可用的层，通常围绕两个实体就够了：

- `change_review_record`
- `rollout_gate_record`

这已经足够把 Part V、Part VII 和 Part VIII 串成一条完整的 operational discipline。

## 3. Change review record

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
  - rollout_rules
required_reviews:
  - engineering
  - safety
  - runtime_owner
required_evals:
  - offline_regression
  - targeted_safety_eval
  - trace_regression_check
status: approved
```

这里最关键的字段是：

- `affected_surfaces` 防止高风险变化伪装成“小调整”；
- `required_reviews` 让 ownership 显式化；
- `required_evals` 避免每次都重新争论到底该跑什么；
- `status` 是 operational fact，而不是漂亮的 prose。

## 4. Rollout gate record

`rollout_gate_record` 关注的不是变化本身“好不好”，而是系统是否准备好把它投放到某一波 rollout。

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
blocking_findings: []
decision: go
decided_by:
  - runtime_owner
  - safety_owner
```

这一层重要的原因在于：一个好的 change review，并不自动等于“现在就可以 rollout”。

## 5. Change review 和 rollout gate 的区别

这两层经常被混在一起，但它们其实回答的是不同问题：

- `change_review_record` 回答：“这个变化原则上能不能发布？”
- `rollout_gate_record` 回答：“这个变化现在能不能发、以及该以多大范围发？”

所以字段也应该不同：

- review 更关注 change type、risk 和 required evals；
- rollout gate 更关注 telemetry、on-call、rollback、traffic scope 和 live readiness。

## 6. 它和 eval schema 的关系

Change review 与 rollout gate 和 [eval schema](eval-schema.zh.md) 是紧密耦合的：

- review 会声明哪些 eval 是必须的；
- gate 会判断这些结果是否足够支撑当前 rollout wave；
- incidents 与 findings 后续还会回流进 required checks。

也就是说，eval layer 不是独立存在的，而是 gate 的一根支柱。

## 7. 它和 trace schema 的关系

一旦 trace schema 完整，rollout gate 就会强很多：

- traces 能看出 high-risk paths 是否真的被覆盖；
- session summaries 能看出是否已经出现 regressions；
- structured events 能说明上线前到底检查了什么。

这也是为什么成熟团队里，trace 和 rollout gate 往往是并排建设的。

## 8. 它和 reference package 的关系

[agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) 已经包含了这套模型的一部分：

- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
- [lifecycle.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/lifecycle.py)
- [configs/rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)
- [configs/change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)
- CLI：
  - `check-rollout`
  - `check-change`

这让书里不只是能解释 gate 的概念，还能直接给出一个 runnable skeleton。

## 9. 最小不变量

一个健康的 change-rollout layer，至少应该保证：

- high-risk change 没有 review record 就不能进入 rollout；
- rollout gate 必须指向明确的 `bundle_id` 和 `rollout_wave`；
- required checks 和 blocking findings 必须显式可见；
- 每个 decision 都有 owner；
- incident trace 可以还原出 review 和 gate；
- rollback plan 不能只存在于人的脑子里。

## 10. 最常见的断裂点

常见问题通常长这样：

- review 和 rollout decision 分散在不同地方，彼此不相连；
- gating criteria 没有版本；
- telemetry readiness 靠肉眼判断；
- safety findings 没有被当作 blocker；
- rollout wave 的定义太模糊；
- 没人能解释为什么这个 change 居然能进 canary。

## 11. 实用检查清单

你可以快速问自己：

- high-risk changes 是否有明确的 review record？
- 是否真的有独立的 rollout gate，而不是只有一句“review approved”？
- 是否能清楚看到 rollout 前必须通过哪些 checks？
- 是否能看到 `change_id -> bundle_id -> rollout_wave` 这条链？
- blocking findings 和 decision owners 是否被保留？
- incident review 时能不能还原出到底是哪个 gate 放行了这个变化？

如果连续几个答案都是“否”，那说明你可能已经有了 change process，但还没有真正完整的 rollout gate layer。

## 延伸阅读

- [Eval Dataset Schema 与 Grading Contract](eval-schema.zh.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](policy-bundle-schema.zh.md)
- [Reference Package](reference-package.zh.md)
- [第 18 章：生产上线检查清单](../book/part-vii/chapter-18.zh.md)
- [第 20 章：智能体系统的 Change Management](../book/part-viii/chapter-20.zh.md)
