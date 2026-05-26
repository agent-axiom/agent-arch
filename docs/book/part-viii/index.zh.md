# 第八部分：智能体系统生命周期

到这里为止，这本书已经解释了如何搭建架构、加固安全、建立可观测性以及安全地发布变更。但生产纪律不会在上线时结束。

只要智能体系统活得比一场演示更久，你很快就会遇到另一类问题：

- 哪些变更应该被视为对发布有实质影响；
- 怎样响应漂移与发现项；
- 怎样保留受信任工件的谱系；
- 怎样让系统退出运行；
- 怎样把控制范围扩展到整个智能体群体，而不只是一个智能体。

这一部分回答的正是这些问题。它不再把智能体系统读成一张架构图，而是读成一个受治理的生命周期。

!!! example "这一部分中的贯穿案例"
    支持分诊（support-triage）案例在这里贯穿完整生命周期弧线：重复工单修复会变成 ADLC 变更集、高风险变更包、受管理的保障发现项（finding）、已批准工件包、旧工单写入器的退役控制、失配/控制评测场景、可用于检测的遥测（telemetry），以及带负责人的注册表记录（registry record）。这样读者能看到，一个事故应该改变的不只是代码，还包括证据（evidence）、发布（rollout）、运行（operations）和问责（accountability）。

!!! note "规范生命周期案例（Canonical lifecycle cases）"
    在这一部分，三个规范案例（canonical cases）会拆到不同生命周期问题（lifecycle questions）上。**支持分诊（Support triage）** 检查写能力变更包（write-capability change packets）、审批（approvals）和重复工单恢复证据（duplicate-ticket recovery evidence）。**内部知识助手（Internal knowledge assistant）** 检查语料责任归属（corpus ownership）、新鲜度审查（freshness review）、访问控制（access control）和知识来源证明（knowledge provenance）。**事故协调（Incident coordination）** 检查升级权限（escalation authority）、通知副作用（notification side effects）、响应责任归属（response ownership）和事故后学习（post-incident learning）。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 19 章](chapter-19.zh.md)：先把从 SDLC 到 ADLC 当作工作框架建立起来；
    - [第 20 章](chapter-20.zh.md)：判断哪些变更真正对发布有实质影响；
    - [第 21 章](chapter-21.zh.md)：看清发现项怎样变成响应；
    - [第 22 章](chapter-22.zh.md)：锁定受信任工件的谱系；
    - [第 23 章](chapter-23.zh.md)：通过替换与退役把生命周期闭合起来；
    - [第 24 到 27 章](chapter-24.zh.md)：把同一条轮廓继续扩展到对抗压力、判断、可观测性与整个智能体群体的问责。

## 这一部分解决什么问题

- 它把智能体系统展示成受治理的生命周期，而不是一次性发布；
- 它把发布判断与响应、谱系、闭合和智能体群体问责区分开来；
- 它给出一套可以讨论变更评审、事故、退役和蔓延的语言；
- 它帮助读者把生产智能体系统资产读成一个有负责人机制的系统，而不是一堆控制措施。

## 这一部分的角色地图

用这张地图（map）来避免后半部分读起来像同一个治理（governance）观点被反复换名。便于打印（print-friendly）的版本故意很短：

- **生命周期框架** 管住从设计到退役的状态转换。它的工件（artifact）是 ADLC 状态模型；它不是只给 SDLC 换名字。
- **变更管理** 判断哪些变更需要评审和发布门禁。它的工件（artifact）是 [变更包](../../appendix/change-rollout-schema.zh.md)；它不是普通项目管理。
- **保障闭环** 把发现项（findings）转成遏制（containment）、修复（remediation）和责任归属（ownership）。它的工件（artifact）是 [发现与响应记录（finding and response record）](../../appendix/incident-record-schema.zh.md)；它不是可观测性或评测打分（eval scoring）。
- **来源追踪** 保留受信任工件谱系和发布身份。它的工件（artifact）是 [已批准工件包](../../appendix/lifecycle-artifact-schema.zh.md)；它不是泛泛的证据（evidence）文件夹。
- **退役** 在不丢失问责的情况下关闭或替换系统。它的工件（artifact）是 [退役计划](../../appendix/lifecycle-artifact-schema.zh.md)；它不是删除旧智能体。
- **失配与内部人风险** 命名对抗性或激励驱动的误用路径。它的工件（artifact）是风险场景与控制计划；它不是提示注入（prompt-injection）指南的重复。
- **行为/控制评测** 对行为和控制给出发布判断。它的工件（artifact）是 [评测门禁与验证器契约（eval gate and verifier contract）](../../appendix/eval-schema.zh.md)；它不是事故响应。
- **可观测性** 让证据基底（evidence substrate）可见、可查询。它的工件（artifact）是 [追踪与遥测覆盖记录（trace and telemetry coverage record）](../../appendix/trace-schema.zh.md)；它不是治理决策（governance decision）的负责人。
- **清单与注册表** 通过负责人（owner）和生命周期状态让整个智能体群体（estate）可问责。它的工件（artifact）是 [注册表记录（registry record）](../../appendix/registry-operations-handbook.zh.md)；它不是松散的智能体表格。

把这些章节当作一条链来读：生命周期（lifecycle）定义状态，变更管理（change management）控制移动，评测（evals）判断是否可发布，来源追踪（provenance）记录哪些工件可信，可观测性（observability）保留证据（evidence），保障（assurance）在证据变成风险（risk）时响应，退役（retirement）关闭旧路径，注册表（registry）维持整个智能体群体（estate）的问责（accountability）。如果两章听起来都像“治理（governance）”，就用它们在评审（review）后必须留下的工件来区分。

## 本部分内容

- [第 19 章：从 SDLC 到 ADLC](chapter-19.zh.md)
- [第 20 章：智能体系统的变更管理](chapter-20.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](chapter-21.zh.md)
- [第 22 章：供应链、来源追踪与已批准工件](chapter-22.zh.md)
- [第 23 章：退役、替换与终止使用纪律](chapter-23.zh.md)
- [第 24 章：智能体失配与内部人风险](chapter-24.zh.md)
- [第 25 章：行为评测、控制评测与自动化红队测试](chapter-25.zh.md)
- [第 26 章：AI 原生可观测性、清单覆盖率与可用于检测的遥测](chapter-26.zh.md)
- [第 27 章：智能体清单、注册表与蔓延治理](chapter-27.zh.md)

## 读完这一部分后，你应该得到什么

- 一套更成熟的发布门禁与变更评审框架；
- 更清楚地区分判断、响应、谱系、可观测性与问责；
- 一套关于智能体系统如何在时间中被修改、约束、调查与关闭的实用模型。
