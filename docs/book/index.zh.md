# 书籍（book）

这是整本书的主入口页（main entry page）。如果你想用最短路径（shortest path）进入正文（main text），请从[第一部分：基础](part-i/index.zh.md)开始。如果你想先看结构与发布状态（structure and publication status），请打开[全书计划（Book Plan）](plan.zh.md)。

## 这本书的承诺（book promise）

这本书有一个核心判断（main thesis）：智能体需要平台（platform），而不是魔法。

构建智能体很枯燥，但结果令人震撼：你得到的不是一次性炫技（one-off trick），而是一个可以约束（constrain）、观察（observe）、发布（ship）并无需猜测地持续改进（improve without guessing）的系统。

读完后，你应该能够做到（learning outcomes）：

- 判断什么时候真的需要智能体，什么时候普通工作流（workflow）就够了；
- 看清在允许高风险动作（risky actions）之前，系统需要的最小平台层集合（minimum platform layers）；
- 追踪一次受治理的运行（run）如何穿过策略（policy）、执行（execution）、证据（evidence）、审批（approval）、发布（rollout）与生命周期控制（lifecycle control）；
- 把记忆（memory）、评测（evals）、来源谱系（provenance）、退役（retirement）与操作员问责（operator accountability）看成同一个运行模型的一部分。

!!! example "贯穿的支持案例（support case throughline）"
    读这本书的一种方式，是一路跟随支持分诊（support-triage）案例：从检索（retrieval）与工具执行（tool execution），到重复工单恢复（duplicate-ticket recovery）、追踪（traces）、SLO、评测门（eval gates）、归属（ownership）、参考运行时（reference runtime）、策略（policy）、发布（rollout）、ADLC、保障（assurance）、来源谱系（provenance）、退役（retirement）、失配控制（misalignment controls）、遥测（telemetry）和注册表（registry）。这样，各章就不再只是主题集合，而是一条可审阅的故事线：一个事故如何变成平台契约。

!!! note "规范案例地图（Canonical case map）"
    **支持分诊（Support triage）**仍然是写入能力（write capabilities）、审批（approvals）和重复工单恢复（duplicate-ticket recovery）的主线。**内部知识助手（Internal knowledge assistant）**用来检查检索（retrieval）、记忆（memory）、租户边界（tenant boundaries）、新鲜度（freshness）和来源锚定（source grounding）没有在架构里消失。**事件协调（Incident coordination）**用来检查追踪（traces）、SLO、升级（escalation）、通知副作用（notification side effects）、响应归属（response ownership）和事后学习（post-incident learning）。三个规范案例（canonical cases）合在一起，让本书不只是一条支持案例故事，而是一张不同控制表面（control surfaces）的地图。

## 推荐阅读路径（recommended reading path）

如果你想走最短有效路径（shortest useful path），可以按这个顺序读：

1. [第一部分：基础](part-i/index.zh.md)
2. [第二部分：安全边界](part-ii/index.zh.md)
3. [第三部分：记忆与知识](part-iii/index.zh.md)
4. [第四部分：工具与执行](part-iv/index.zh.md)
5. [第五部分：可靠性与可观测性](part-v/index.zh.md)
6. [第六部分：组织模型](part-vi/index.zh.md)
7. [第七部分：参考实现](part-vii/index.zh.md)
8. [第八部分：智能体系统生命周期](part-viii/index.zh.md)

## 稳定性指南（stability guide）

这本书可以粗分为两个实践层（practical layers）：

- `稳定核心`（stable core）：第一到第七部分，尤其是第 1 到 12 章以及第 18 章；
- `快速变化层`（fast-moving layer）：第 13 章、第八部分，以及研究型附录页面（research appendix pages）。

如果你是第一次阅读，建议先读稳定核心（stable core），再回来看变化更快的层（fast-moving layer）。

## 直接入口（direct entry points）

- [从第一部分开始](part-i/index.zh.md)
- [打开全书计划](plan.zh.md)
- [跳到证据主线（Evidence Spine）](part-v/evidence-spine.zh.md)
- [跳到智能体系统生命周期](part-viii/index.zh.md)

[开始读书](part-i/index.zh.md){ .md-button .md-button--primary }
[查看计划](plan.zh.md){ .md-button }
