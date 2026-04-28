# 事故记录与事后复盘链接 Schema

这页描述了智能体系统中事故评审的最小契约层：事故记录应该包含哪些字段，它如何与追踪、审批、发布和生命周期工件相连，以及哪些数据必须在遏制阶段之后仍然保留下来。

它也直接连接到书里的 [Evidence Spine：从请求到发布判断](../book/part-v/evidence-spine.zh.md)，因为事故评审正是这条受治理链路必须保持完整的关键场景之一。

如果 [智能体系统事故响应手册](incident-response-playbook.zh.md) 回答的是“前几分钟和后续复盘该怎么做”，那么这页回答的是“这些内容应该以什么形式被固定下来”。

## 1. 为什么需要单独的事故记录

如果没有专门的事故工件，复盘通常会裂成几块彼此脱节的材料：

- 追踪在可观测性系统里；
- 审批历史在审计轨迹里；
- 回滚决策在聊天记录里；
- 事后复盘在文档里；
- 变更链接只能靠记忆回溯。

这种方式偶尔可以工作，但对重复事故、审计、回归更新和生命周期修正都很脆弱。

## 2. 核心实体

这套最小 Schema 通常围绕两个实体展开：

- `incident_record`
- `incident_postmortem_link`

这已经足够把运营响应与生命周期修正连接起来。

## 3. 事故记录

`incident_record` 用来记录发生了什么、影响半径有多大，以及事件发生时哪些工件正在生效。

```yaml
kind: incident_record
incident_id: inc-2026-04-09-001
title: "Unauthorized ticket_write path during onboarding run"
severity: sev2
status: contained
category: unauthorized_side_effect
detected_at: 2026-04-09T09:14:00Z
detected_by: automated_detection
agent_id: support-triage-ref
trace_id: trace-2026-04-09-001
session_id: session-2026-04-09-001
bundle_id: bundle-2026-04-07-a
change_id: chg-2026-04-07-001
rollout_wave: canary
tool_principal: svc-ticket-writer
approval_id: apr-2026-04-09-001
affected_surfaces:
  - approval_path
  - tool_gateway
  - rollout_gate
containment_actions:
  - force_mandatory_approval
  - disable_ticket_write_v1
owner: platform-operations
```

这里最关键的字段是：

- `category`，它把事故与分诊分类、评测更新连接起来；
- `bundle_id`、`change_id` 与 `rollout_wave`，它们把事故与发布纪律连接起来；
- `tool_principal` 与 `approval_id`，它们能更快定位真实的副作用；
- `affected_surfaces`，它提醒团队不要把问题缩减成单纯的模型输出。

## 4. 事故事后复盘链接

`incident_postmortem_link` 把某个具体事故与纠正动作、生命周期工件连接起来。

```yaml
kind: incident_postmortem_link
incident_id: inc-2026-04-09-001
postmortem_id: pm-2026-04-09-001
corrective_actions:
  - change_id: chg-2026-04-09-003
  - bundle_id: bundle-2026-04-09-b
  - eval_dataset_update: eval-set-2026-04-09
  - retirement_plan: retire-ticket-write-v1
owners:
  - platform-safety
  - platform-runtime
status: open
```

这一层的价值在于：它迫使事故评审以具体的生命周期更新结束，而不只是停留在文字总结里。

## 5. 它与追踪 Schema 的关系

事故记录几乎总是依赖 [追踪 Schema 与事件目录](trace-schema.zh.md)：

- `trace_id` 与 `session_id` 把事故连到运行历史；
- 策略事件说明什么被允许了；
- 审批事件说明是否存在人工门禁；
- 工具事件说明真实的副作用；
- 会话摘要帮助判断这是一次性运行还是更大的模式，也能看出像 `failure_reason` 这样的失败运行导出证据是否仍然完整。

## 6. 它与审批和策略包的关系

当团队需要快速恢复这些信息时，事故记录尤其重要：

- 当时激活的是哪条审批路径；
- 做出的决策是什么；
- 哪个策略包正在生效；
- 到底是哪一个主体执行了动作。

因此事故 Schema 应该紧挨着：

- [策略包 Schema 与审批契约](policy-bundle-schema.zh.md)
- [审批请求与决策记录 Schema](approval-schema.zh.md)

## 7. 它与变更管理和发布的关系

事故评审很少止步于遏制。

团队通常还要判断：

- 哪个 `change_id` 引入了高风险路径；
- 哪个 `rollout_gate_record` 放行了它；
- 哪些检查没有拦住它；
- 是否需要回滚、受限模式或退役。

这就是为什么事故记录应该和 [变更评审与发布门禁 Schema](change-rollout-schema.zh.md) 以及 [生命周期工件 Schema](lifecycle-artifact-schema.zh.md) 相连。

## 8. 与参考运行时包的关系

[agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) 已经具备几类能让这套模型落地的基础构件：

- 追踪与会话摘要；
- 审批队列；
- 生命周期工件；
- 发布检查；
- 策略与控制链接。

即使包目前还没有存储完整的 `incident_record`，书里也已经可以明确这种记录至少应包含哪些字段。

## 9. 最小不变量

成熟的事故层通常有这些不变量：

- 每个事故都有稳定的 `incident_id`；
- `trace_id` 与 `session_id` 会立刻被保留下来；
- `bundle_id`、`change_id` 与 `rollout_wave` 可以在不靠猜测的情况下恢复；
- 遏制动作会被明确记录；
- 事故会连接到纠正动作；
- 事后复盘会推动生命周期工件、评测或策略包的更新。

## 10. 最常见的失败模式

常见问题通常包括：

- 事故工单根本不知道追踪和会话；
- 副作用看得见，但主体不清楚；
- 变更链接只能靠回忆拼出来；
- 事后复盘没有对应的纠正工件；
- 事故从不进入评测数据集或发布标准；
- 名义上已关闭的事故之后，已退役路径仍然活着。

## 11. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 事故有稳定的 `incident_id` 吗？
- 团队能否快速恢复 `trace_id`、`session_id`、`bundle_id` 和 `change_id`？
- 能看出是哪一个主体和审批路径参与了事件吗？
- 遏制动作是否被记录？
- 是否存在清晰的事故 -> 事后复盘 -> 纠正动作链路？
- 事故会回流到评测、发布门禁与生命周期更新吗？

## 下一步做什么

- [智能体系统事故响应手册](incident-response-playbook.zh.md)
- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [审批请求与决策记录 Schema](approval-schema.zh.md)
- [变更评审与发布门禁 Schema](change-rollout-schema.zh.md)
- [生命周期工件 Schema](lifecycle-artifact-schema.zh.md)
- [智能体注册表与清单运维手册](registry-operations-handbook.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](../book/part-viii/chapter-21.zh.md)
- [第 26 章：AI 原生可观测性、清单覆盖率与可用于检测的遥测](../book/part-viii/chapter-26.zh.md)
