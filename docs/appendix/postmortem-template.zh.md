# 智能体系统事后复盘模板

这个模板不是为了生成一份“好看”的文档，而是为了确保事故评审最终会落到具体的纠正动作、生命周期更新与评测纪律变化上。

最好在遏制阶段之后使用它，也就是追踪、审批、发布数据与当前生效的包都已经恢复出来之后。

## 1. 简要摘要

- `incident_id`：
- 日期与时间：
- 严重性：
- 状态：
- 负责人：
- 事故摘要：

## 2. 发生了什么

- 参与的是哪个智能体或工作流：
- 哪个用户输入、检索到的上下文或外部触发启动了这条路径：
- 发生了什么高风险动作或失败：
- 是否产生了真实副作用：

这一节的目的，是简短且不带解释地固定事件链本身。

## 3. 当时哪些工件在生效

- `trace_id`：
- `session_id`：
- `bundle_id`：
- `change_id`：
- `rollout_wave`：
- `policy_bundle`：
- `approval_mode`：
- `tool_principal`：

如果这个部分很难快速补齐，问题就不只是事故本身，也在可观测性或生命周期层。

## 4. 遏制动作

- 最初几分钟采取了哪些动作：
- 哪些能力、路径或模式被禁用、收窄或转入受限模式：
- 是否需要回滚：
- 是否撤销了主体、连接器或能力：

这里最好区分：

- 临时遏制；
- 永久修正。

## 5. 根因

- 事故的直接原因是什么：
- 哪些促成因素放大了问题：
- 哪个门禁、评审或假设失效了：
- 问题主要落在策略、审批、发布、记忆、可观测性还是清单：

这一节应当通向系统性解释，而不是简单写成“模型出错了”。

## 6. 控制层哪些地方失效了

- 哪个策略决策放过了高风险路径：
- 是否存在审批绕过、缺失审批或错误的审批范围：
- 哪些检查或评测没有拦住问题：
- 哪些检测规则没有触发，或者触发得太晚：

这一节不仅要描述错误，还要描述缺失的护栏。

## 7. 影响半径

- 哪些用户、系统或数据受到了影响：
- 是否触达外部系统：
- 是否影响了记忆记录：
- 这是单次运行，还是发布波次/会话族中的更大模式：

## 8. 纠正动作

对每个动作，最好固定：

- 动作本身；
- 负责人；
- 截止时间；
- 会更新哪个工件。

常见纠正动作包括：

- 更新策略包；
- 收紧审批模式；
- 更新评测数据集；
- 增加定向回归测试；
- 更新发布门禁；
- 退役能力或主体；
- 更新注册表记录；
- 增加检测规则。

## 9. 生命周期工件要更新什么

- 如果需要修正发布，新的 `change_id` 是什么：
- 如果发布配置变了，新的 `bundle_id` 是什么：
- 是否需要新的 `retirement_plan`：
- 是否需要更新注册表或清单：
- 是否需要调整事故分类或事后复盘准则：

这一节的价值在于把事后复盘连接到可治理的工件，而不仅仅是任务系统里的待办项。

## 10. 评测与发布要更新什么

- 哪些案例应进入评测数据集：
- 要补哪些行为评测或控制评测：
- 发布门禁标准是否需要调整：
- 金丝雀范围或审批阈值是否需要修改：

如果事故不回流到评测和发布规则，团队往往会重复同一类故障。

!!! example "重复工单线索的事后复盘"
    对于 support-triage 事故，事后复盘需要明确回答：是哪一次 `create_ticket` 调用产生了副作用，是否存在 `idempotency_key`，哪个 `policy_bundle` 和 `rollout_wave` 放行了它，为什么 `side_effect_unknown` 没能阻止重复写入，以及哪些纠正动作会更新评测数据集、发布门禁、审批策略、注册表记录和旧 ticket writer 的退役计划。

!!! note "规范事后复盘案例（Canonical postmortem cases）"
    事后复盘（postmortem）应该把三个规范案例（canonical cases）的不同失败类别（failure classes）回流到控制循环（control loop）。**支持分流（Support triage）** 检查重复工单根因（duplicate-ticket root cause）、审批范围（approval scope）、`idempotency_key`、副作用遏制（side-effect containment）和评测/发布修正（eval/rollout correction）。**内部知识助手（Internal knowledge assistant）** 检查陈旧来源（stale source）、检索新鲜度（retrieval freshness）、记忆来源（memory provenance）、访问控制缺口（access-control gap）和知识库修正（knowledge-base correction）。**事件协调（Incident coordination）** 检查升级延迟（escalation delay）、通知副作用（notification side effects）、响应归属缺口（response ownership gap）、交接崩溃（handoff breakdown）和事件后学习更新（post-incident learning update）。

## 11. YAML 简版模板

```yaml
postmortem:
  incident_id: inc-2026-04-09-001
  severity: sev2
  owner: platform-operations
  active_artifacts:
    trace_id: trace-2026-04-09-001
    session_id: session-2026-04-09-001
    bundle_id: bundle-2026-04-07-a
    change_id: chg-2026-04-07-001
    rollout_wave: canary
  root_cause:
    primary: approval_scope_too_broad
    contributing:
      - missing_targeted_eval
      - stale_rollout_gate
  corrective_actions:
    - owner: platform-safety
      action: tighten_approval_policy
      due: 2026-04-12
    - owner: runtime-team
      action: add_regression_eval
      due: 2026-04-13
  lifecycle_updates:
    change_id: chg-2026-04-09-003
    bundle_id: bundle-2026-04-09-b
```

## 12. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 事后复盘里是否有精确的 `incident_id`？
- 是否恢复了 `trace_id`、`session_id`、`bundle_id` 与 `change_id`？
- 是否写明了促成因素，而不只是根因？
- 是否记录了控制缺口？
- 是否给出了带负责人和截止时间的纠正动作？
- 是否明确了要更新哪些生命周期工件？
- 事故是否回流到了评测与发布标准？

## 下一步做什么

- [智能体系统事故响应手册](incident-response-playbook.zh.md)
- [事故记录与事后复盘链接模式](incident-record-schema.zh.md)
- [变更评审与发布门禁模式](change-rollout-schema.zh.md)
- [生命周期工件模式](lifecycle-artifact-schema.zh.md)
- [智能体注册表与清单运维手册](registry-operations-handbook.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](../book/part-viii/chapter-21.zh.md)
