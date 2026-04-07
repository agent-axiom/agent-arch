# Policy Bundle Schema 与 Approval Contract

这一页把书里已经写过的几个主题连起来：

- [第 4 章：工具网关、审批与审计链路](../book/part-ii/chapter-4.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
- [第 20 章：智能体系统的 Change Management](../book/part-viii/chapter-20.zh.md)

同时它也依赖可运行的 package：

- [参考包](reference-package.zh.md)

如果 trace schema 和 eval schema 那两页回答的是：

- 如何描述实际行为；
- 如何描述期望行为；

那么这一页回答的就是第三个问题：

- 如何描述位于 reasoning 和 side effects 之间的治理规则。

## 为什么要把 policy bundle 当成 artifact

在 agent systems 里，一个很常见的问题是：

- policy rules 一部分藏在 prompt 里；
- 一部分在 gateway code 里；
- 一部分在 approval UI 里；
- 一部分只存在于团队脑子里。

系统还小时也许能勉强运转，但一旦进入 change management、audit 和 staged rollout，这种 policy layer 就会变得太模糊。

所以最好把 `policy bundle` 视作一个一等 artifact。

## 什么是 policy bundle

这里可以把 `policy bundle` 理解为一组作为整体发布的相关规则：

- runtime policy；
- tool policy；
- approval policy；
- memory write rules；
- escalation rules；
- egress rules。

重点不在于所有内容必须塞进一个 YAML 文件，而在于这个 bundle 应该是：

- versioned；
- reviewable；
- traceable；
- releasable。

## 最小 policy bundle 结构

一个最小可用的 bundle 可以长这样：

```yaml
bundle:
  bundle_id: policy-support-triage-2026-04-07
  version: 2026.04.07
  owner_team: platform-safety
  applies_to:
    agent_ids: ["support-triage-ref"]
  artifacts:
    - policy.yaml
    - approvals.yaml
    - controls.yaml
```

这里还不是具体规则本身，而是一个 envelope，用来回答：

“对于这套 agent system，我们到底把哪些东西视为当前的 policy artifact？”

## 为什么 approval contract 不能只写在 prose 里

Approval logic 经常只是这样被描述：

- “高风险动作需要确认”；
- “manager 负责批准建 ticket”；
- “危险动作需要 security sign-off”。

这远远不够。

更好的做法是把 approval contract 写清楚：

- 谁可以 approve；
- 哪类 action 需要 approval；
- approval request 必须带哪些字段；
- 允许哪些决策；
- reject 之后会发生什么；
- audit trail 里必须留下什么。

## approval contract 示例

下面是一个可工作的 skeleton：

```yaml
approval_contract:
  capability: create_ticket
  risk_tier: high
  required_reviewers:
    - manager
  request_fields:
    - trace_id
    - session_id
    - requested_by
    - reason
    - tool_arguments_redacted
  allowed_decisions:
    - approved
    - rejected
  on_reject: stop_run
```

重点很简单：approval 应该是 machine-readable operational contract，而不只是 UI 上的一颗按钮。

## policy bundle 和 lifecycle 的关系

从 Part VIII 里，这里最重要的是两点：

- policy changes 属于 release-bearing changes；
- policy bundle 应该作为完整 artifact 进入 change management。

也就是说，团队不应该只回答：

“我们原则上有什么 policy？”

还应该回答：

“这个 rollout 或 incident 发生时，到底是哪一个 policy bundle version 在生效？”

## policy bundle 和 traces 的关系

它们之间的关系非常直接：

- trace 告诉你，哪一个 policy decision 真正触发了；
- policy bundle 告诉你，这个 decision 来自哪里；
- approval contract 告诉你，human gate 本来应该长什么样。

少了这三者的联动，调查很快就会变成猜测。

## reference runtime 现在已经支持什么

在 `agent_runtime_ref` 里，现在已经有：

- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [approvals.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/approvals.yaml)
- [controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/controls.yaml)
- [change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)

也就是说，这个 package 已经活在一种模型里：policy 和 approvals 不再只是“附带设置”，而是 governed artifacts。

## production schema 还应该补什么

一旦系统变得更成熟，policy bundle 很快就应该继续补充：

- `bundle_version`
- `artifact_lineage`
- `change_id`
- `approval_contracts`
- `deprecated_rules`
- `redaction_policy`

这会把 policy layer 从“一堆配置文件”提升成真正的 release surface。

## 为什么 policy bundle 和 capability catalog 不能彼此漂移

有一种很糟糕的状态是：policy bundle、capability catalog 和 approval rules 各自分开存在，而且它们之间的链接很弱。

然后很快就会出现问题：

- catalog 里有 capability，但没有对应的 approval contract；
- policy 还在引用已经不存在的 capability name；
- audit 看到了 decision，却没法把它和具体 bundle version 关联起来。

所以 practical rule 很简单：

- capability catalog 描述系统能做什么；
- policy bundle 描述这些能力在什么条件下可以被调用；
- approval contract 描述 reasoning 应该在何处停下并把控制权交给人。

## 实用检查清单

如果你想快速判断自己的 policy artifact layer 是否已经足够成熟，可以问自己：

- 是否有 versioned policy bundle？
- 能不能把 bundle 和 rollout、incident review 关联起来？
- Approval contract 是 machine-readable 还是只写在 prose 里？
- Approval request 必须带哪些字段，是否清楚？
- Policy bundle 和 capability catalog 之间是否有稳定关联？
- 能不能知道某条 trace 对应的是哪个 policy version？

如果连续几个答案都是“不能”，那说明你的 policy layer 虽然存在，但还没有被塑造成完整的 operational artifact。

## 延伸阅读

- [Trace Schema 与 Event Catalog](trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](eval-schema.zh.md)
- [参考包](reference-package.zh.md)
- [按场景组织的 Policy Templates 与 Checklists](policy-templates.zh.md)
