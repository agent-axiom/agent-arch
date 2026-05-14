# 全书计划

这页讲的是全书的结构与当前状态。如果你需要阅读路线，先看[从这里开始](../start-here.zh.md)。如果你需要发布技术栈和站点工具层，请看[单独页面](../appendix/stack.zh.md)。

!!! info "Draft localization preview"
    中文层当前是 draft localization preview，而不是 finished Chinese edition。章节结构和技术内容会跟随主稿更新，但正式出版前还需要单独的中文编辑、术语表锁定、图表/表格导出 QA 和整稿母语审校。

!!! info "按稳定性来阅读本书"
    这本书有两个层次：

    - `稳定内核`：第一到第七部分，尤其是第 1-12 章和第 18 章。这些内容对应基础工程纪律，变化相对更慢。
    - `快速变化层`：第 13 章、第八部分，以及研究色彩更重的附录页面。这些页面更新更频繁，因为厂商工具、评测实践和威胁模式变化更快。

    如果你第一次读这本书，先走稳定内核。如果你需要最新的运营轮廓，再进入更快变化的层。

!!! example "编辑线索：support-triage"
    在当前已发布层里，support-triage 案例承担着贯穿全书的编辑线索。它把检索、工具执行、重复工单恢复、traces、SLO、评测门、ownership、运行时模块、能力策略、rollout gates、ADLC、保障、来源谱系、退役、失配控制、telemetry 和 registry 串在一起。这有助于检查全书结构没有碎成一组互不相干的主题。

!!! summary "Case-spine map"
    本书使用三个 canonical cases，但它们承担不同角色。**Support triage** 是主线案例，用来贯穿 write capabilities、approvals、duplicate-ticket recovery 和 production lifecycle。**Internal knowledge assistant** 是辅助案例，用来承载 retrieval、memory、access control、freshness 和 knowledge provenance。**Incident coordination** 是辅助案例，用来承载 traces、SLO、assurance loop、escalation 和 post-incident learning。

    当某章引入新机制时，检查它强化的是哪条 case：support triage 对应 side effects，internal knowledge 对应 context quality，incident coordination 对应 response and governance。

## 结构

### 第一部分：基础

状态：`Published`

这一部分的问题是：什么时候智能体真的有必要，以及如果不把它做成提示技巧，而是做成系统，一个最小成熟架构应该长什么样。

- 第 1 章：为什么智能体需要的是平台，而不是魔法。
- 第 2 章：安全智能体的参考架构。
- [实践：Instructions、Routines 与 Prompt Templates](part-i/practical-routines.zh.md)
- [实践：Manager Pattern vs Handoffs](part-i/practical-manager-handoffs.zh.md)

### 第二部分：安全边界

状态：`Published`

这一部分的问题是：智能体系统真正的 trust boundaries 在哪里，什么层应该掌控“行动的权利”。

- 第 3 章：安全边界与信任边界。
- 第 4 章：工具网关、审批与审计轨迹。

### 第三部分：记忆与知识

状态：`Published`

这一部分的问题是：怎样让记忆真正有用，同时不把它变成一个不受控的错误与泄漏来源。

- 第 5 章：为什么智能体需要记忆，以及为什么记忆很危险。
- 第 6 章：短期记忆、长期记忆与用户画像记忆。
- 第 7 章：检索、压缩与后台更新。

### 第四部分：工具与执行

状态：`Published`

这一部分的问题是：怎样把工具使用和执行变成受治理契约，而不是一堆混乱的调用。

- 第 8 章：执行模型与工具目录。
- 第 9 章：沙箱执行与 MCP 作为集成契约。
- 第 10 章：幂等性、重试、速率限制与回滚边界。
- [实践：MCP 与 A2A 作为集成层](part-iv/practical-mcp-a2a.zh.md)

### 第五部分：可靠性与可观测性

状态：`Published`

这一部分的问题是：怎样在第一次事故之后不靠猜，而是能够捕获运行历史、定义预算，并产出可评审判断。

- 第 11 章：追踪、跨度与结构化事件。
- 第 12 章：智能体系统的 SLO。
- 第 13 章：离线评测、在线评测与回归门禁。
- [Evidence Spine：从请求到发布判断](part-v/evidence-spine.zh.md)

### 第六部分：组织模型

状态：`Published`

这一部分的问题是：谁拥有智能体平台，谁守住质量门槛，以及如何避免把组织做成智能体动物园。

- 第 14 章：平台团队与产品团队。
- 第 15 章：黄金路径、共享网关与反动物园模式。

### 第七部分：参考实现

状态：`Published`

这一部分的问题是：怎样把架构模型落成可运行结构，让它真的成为可执行系统。

- 第 16 章：基础运行时蓝图。
- 第 17 章：策略层与能力目录。
- 第 18 章：生产上线检查清单。

### 第八部分：智能体系统生命周期

状态：`Published`

这一部分的问题是：怎样与智能体系统共处数月，发布变更、响应故障、关闭旧轮廓，并让整个系统资产保持在控制之下。

- 第 19 章：从 SDLC 到 ADLC。
- 第 20 章：智能体系统的变更管理。
- 第 21 章：保障闭环：红队测试、检测与响应。
- 第 22 章：供应链、来源追踪与已批准工件。
- 第 23 章：退役、替换与终止使用纪律。
- 第 24 章：智能体失配与内部人风险。
- 第 25 章：行为评测、控制评测与自动化红队测试。
- 第 26 章：AI 原生可观测性、清单覆盖率与可用于检测的遥测。
- 第 27 章：智能体清单、注册表与蔓延治理。

## 发布路线图

1. 继续收紧入口页和第一幕。
2. 继续压缩后半本的重叠内容，并保持章节角色分离。
3. 在本书提出强论断的地方继续加强证据基础。
4. 继续清理公开入口页和 sample chapters。
5. 将 `.en` 和 `.zh` 保持为可读的 draft translation layers，并在俄文 core 出现语义修改后同步。

## 已经完成的内容

- 基于 MkDocs 和 Material 的站点骨架。
- 完整的全书结构和已发布的俄文 core。
- 仍在进行 editorial cleanup、但已经可读的 `.en` 与 `.zh` translation layers。
- 可运行的参考运行时 `agent_runtime_ref`。
- 覆盖追踪、评测、记忆、审批和生命周期的参考层。
- 实战案例、策略模板、检查清单与术语表。

[进入第一部分](part-i/index.zh.md){ .md-button .md-button--primary }
