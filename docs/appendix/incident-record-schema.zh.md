# Incident Record 与 Postmortem Linkage Schema

这页描述了智能体系统中 incident review 的最小契约层：incident record 应该包含哪些字段，它如何与 traces、approvals、rollout 和 lifecycle artifacts 相连，以及哪些数据必须在 containment phase 之后仍然保留下来。

它也直接连接到书里的 [Evidence Spine：从请求到 rollout judgment](../book/part-v/evidence-spine.zh.md)，因为 incident review 正是这条受治理链路必须保持完整的关键场景之一。

如果 [智能体系统事故响应手册](incident-response-playbook.zh.md) 回答的是“前几分钟和后续复盘该怎么做”，那么这页回答的是“这些内容应该以什么形式被固定下来”。

## 1. 为什么需要单独的 incident record

如果没有专门的 incident artifact，复盘通常会裂成几块彼此脱节的材料：

- traces 在 observability system 里；
- approval history 在 audit trail 里；
- rollback decision 在聊天记录里；
- postmortem 在文档里；
- change linkage 只能靠记忆回溯。

这种方式偶尔可以工作，但对 repeated incidents、audit、regression updates 和 lifecycle corrections 都很脆弱。

## 2. 核心实体

这套最小 schema 通常围绕两个实体展开：

- `incident_record`
- `incident_postmortem_link`

这已经足够把 operational response 与 lifecycle correction 连接起来。

## 3. Incident record

`incident_record` 用来记录发生了什么、blast radius 有多大，以及事件发生时哪些 artifacts 正在生效。

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

- `category`，它把 incident 与 triage taxonomy、eval updates 连接起来；
- `bundle_id`、`change_id` 与 `rollout_wave`，它们把 incident 与 release discipline 连接起来；
- `tool_principal` 与 `approval_id`，它们能更快定位真实的 side effect；
- `affected_surfaces`，它提醒团队不要把问题缩减成单纯的 model output。

## 4. Incident postmortem link

`incident_postmortem_link` 把某个具体 incident 与 corrective actions、lifecycle artifacts 连接起来。

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

这一层的价值在于：它迫使 incident review 以具体的 lifecycle updates 结束，而不只是停留在文字总结里。

## 5. 它与 trace schema 的关系

Incident record 几乎总是依赖 [Trace Schema 与 Event Catalog](trace-schema.zh.md)：

- `trace_id` 与 `session_id` 把 incident 连到 run history；
- policy events 说明什么被允许了；
- approval events 说明是否存在 human gate；
- tool events 说明真实的 side effect；
- session summaries 帮助判断这是一次性 run 还是更大的模式，也能看出像 `failure_reason` 这样的 failed-run 导出证据是否仍然完整。

## 6. 它与 approvals 和 policy bundle 的关系

当团队需要快速恢复这些信息时，incident record 尤其重要：

- 当时激活的是哪条 approval path；
- 做出的 decision 是什么；
- 哪个 policy bundle 正在生效；
- 到底是哪一个 principal 执行了动作。

因此 incident schema 应该紧挨着：

- [Policy Bundle Schema 与 Approval Contract](policy-bundle-schema.zh.md)
- [Approval Request 与 Decision Schema](approval-schema.zh.md)

## 7. 它与 change management 和 rollout 的关系

Incident review 很少止步于 containment。

团队通常还要判断：

- 哪个 `change_id` 引入了 risky path；
- 哪个 `rollout_gate_record` 放行了它；
- 哪些 checks 没有拦住它；
- 是否需要 rollback、restricted mode 或 retirement。

这就是为什么 incident record 应该和 [Change Review 与 Rollout Gate Schema](change-rollout-schema.zh.md) 以及 [Lifecycle Artifact Schema](lifecycle-artifact-schema.zh.md) 相连。

## 8. 与参考运行时包的关系

[agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) 已经具备几类能让这套模型落地的 primitives：

- traces 与 session summaries；
- approval queue；
- lifecycle artifacts；
- rollout checks；
- policy 与 controls linkage。

即使 package 目前还没有存储完整的 `incident_record`，书里也已经可以明确这种 record 至少应包含哪些字段。

## 9. 最小不变量

成熟的 incident layer 通常有这些不变量：

- 每个 incident 都有稳定的 `incident_id`；
- `trace_id` 与 `session_id` 会立刻被保留下来；
- `bundle_id`、`change_id` 与 `rollout_wave` 可以在不靠猜测的情况下恢复；
- containment actions 会被明确记录；
- incident 会连接到 corrective actions；
- postmortem 会推动 lifecycle artifacts、evals 或 policy bundles 的更新。

## 10. 最常见的失败模式

常见问题通常包括：

- incident ticket 根本不知道 trace 和 session；
- side effect 看得见，但 principal 不清楚；
- change linkage 只能靠回忆拼出来；
- postmortem 没有对应的 corrective artifact；
- incidents 从不进入 eval datasets 或 rollout criteria；
- supposedly closed 的 incident 之后，retired path 仍然活着。

## 11. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- incident 有稳定的 `incident_id` 吗？
- 团队能否快速恢复 `trace_id`、`session_id`、`bundle_id` 和 `change_id`？
- 能看出是哪一个 principal 和 approval path 参与了事件吗？
- containment actions 是否被记录？
- 是否存在清晰的 incident -> postmortem -> corrective action 链路？
- incidents 会回流到 evals、rollout gates 与 lifecycle updates 吗？

## 下一步做什么

- [智能体系统事故响应手册](incident-response-playbook.zh.md)
- [Trace Schema 与 Event Catalog](trace-schema.zh.md)
- [Approval Request 与 Decision Schema](approval-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](change-rollout-schema.zh.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.zh.md)
- [智能体 registry 与 inventory 运维手册](registry-operations-handbook.zh.md)
- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](../book/part-viii/chapter-21.zh.md)
- [第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry](../book/part-viii/chapter-26.zh.md)
