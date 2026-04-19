# 全书计划

这一版书籍按照工程实践手册来组织，而不是框架综述。每一部分都回答一个实际问题：要让智能体在生产环境中真正可用、安全且可治理，系统中必须具备什么。

这页只负责说明全书结构和当前状态。如果你要按角色选择阅读路线，请看[从这里开始](../start-here.zh.md)。如果你关心发布技术栈的取舍，请看单独的[发布技术栈](../appendix/stack.zh.md)页面。

理解这页最干净的方式是：

- 本书承诺 argument、sequence 与 reader transformation；
- support layers 承诺 schemas、runnable anchors、templates 与 contract pages；
- 这份计划的作用，是展示书本身的形状，而不是用一个 project dashboard 来替代这本书。

!!! info "按稳定性来阅读这本书"
    这本书可以分成两个层次：

    - `稳定内核`：第一到第七部分，尤其是第 1-12 章和第 18 章。它们变化较慢，因为描述的是基础工程纪律。
    - `快速变化层`：第 13 章、第八部分，以及研究色彩更强的 appendix 页面。它们更新更频繁，因为 vendor tooling 和 research 变化更快。

    如果你是第一次读这本书，先走稳定内核。如果你需要最新的 production contour，再进入快速变化层。

## 结构

这本书现在有了更明确的内部几何。它不只是主题的顺序，也是读者需要逐步学会区分的一组角色顺序。

### 第一部分：基础

- 什么是现代智能体，以及它与 workflow 的区别。
- 为什么安全架构的起点是 control plane，而不是“聪明的 prompt”。
- 安全智能体的平台级参考架构。

状态：第一章已发布。

这一部分下一步会继续加强：

- 如何判断这里到底需要 agent，还是普通 workflow 就够了；
- 为什么 `single-agent first` 往往比一开始就做多智能体更健康；
- 如何把 instructions、SOP 和 playbooks 变成 routines，而不是混乱的 prompt 段落。

已经加入的实践层：

- [实践篇：Instructions、Routines 与 Prompt Templates](part-i/practical-routines.md)
- [实践篇：Manager Pattern vs Handoffs](part-i/practical-manager-handoffs.md)

### 第二部分：安全边界

- 智能体身份与 machine IAM。
- 面向模型、记忆和工具的 policy-as-code。
- Prompt injection、数据外流、密钥泄漏、工具滥用。
- 高风险操作的人类审批。

### 第三部分：记忆与知识

- short-term 与 long-term memory。
- Retrieval、压缩、摘要、profile memory。
- 何时把 memory 放在热路径，何时放到后台处理。

### 第四部分：工具与执行

- Tool gateway 与 sandbox execution。
- MCP 与外部系统的契约式集成。
- 幂等性、重试、速率限制、回滚边界。

这一部分下一步会继续加强：

- 工具的实用分类：`data`、`action`、`orchestration`；
- 明确的 run loop 停止条件；
- 什么时候应该把 single-agent loop 演进成 manager pattern 或 handoffs。

### 第五部分：可靠性与可观测性

- 第 11 章：traces、spans 与 structured events，作为 raw evidence capture。
- 第 12 章：智能体系统的 SLO，作为 health 与 risk budgets。
- 第 13 章：offline evals、online evals、trace grading 与回归闸门，作为 judgment discipline。
- 计划中的连接页：Evidence Spine，它会把 request、policy、approval、traces、evals、incidents 与 rollout 串成一条统一的工件路径。

说明：Part V 的核心思想相对稳定，但第 13 章比第 11、12 章变化更快。

编辑形状：Part V 现在作为一个三步块来工作，capture -> health -> judgment。下一步要补强的，就是把这条 evidence spine 明确写出来，而不是让读者自己去拼接。

### 第六部分：组织模型

- 平台团队与产品团队的分工。
- Templates、golden paths、shared gateways。
- 如何避免把智能体平台做成“动物园”。

编辑形状：Part VI 是 ownership bridge，用来决定 Part V 在技术上定义的那些层分别由谁负责，以及 Part VII 将怎样把它们落成可运行结构。

### 第七部分：参考实现

- 基础 runtime。
- 安全策略。
- 工具目录。
- 生产上线清单。

编辑形状：Part VII 是 embodiment bridge，在这里，architecture、policy、ownership 与 rollout 会落成 runnable structure。

### 第八部分：智能体系统生命周期

- 第 19 章：从 SDLC 到 ADLC。
- 第 20 章：智能体系统的 Change Management。
- 第 21 章：Assurance Loop：Red Teaming、Detection 与 Response。
- 第 22 章：Supply Chain、Provenance 与 Approved Artifacts。
- 第 23 章：Retirement、Replacement 与 End-of-Life Discipline。
- 第 24 章：Agentic Misalignment 与 Insider Risk。
- 第 25 章：Behavioral Evals、Control Evals 与 Automated Red Teaming。
- 第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry。
- 第 27 章：Agent Inventory、Registry 与 Sprawl 治理。

状态：Part VIII 现在已经组成一个完整的生命周期模块，并补上了 sabotage-like behavior、control-heavy evals、AI-native observability 与 agent-estate governance 这些更前沿的主题。

说明：这是全书变化最快的部分。原则相对稳定，但 tooling、benchmarks、vendor guidance 和 threat patterns 更新更频繁。

编辑形状：Part VIII 现在作为一个后段生命周期轮廓来工作，lifecycle frame -> release judgment -> response -> evidence backbone -> lifecycle closure -> adversarial pressure -> judgment -> evidence substrate -> accountability。

## 发布路线图

1. 固化架构框架与术语。
2. 将安全扩展为独立层，而不是附属小节。
3. 加入参考图和运维检查清单。
4. 提供实用的 reference implementation。
5. 补充 eval 示例和策略配置。
6. 明确整理出贯穿 runtime、policy、approval、trace、eval、incident 与 rollout 的端到端 evidence spine。
7. 增强这本书的决策框架：什么时候该用 agent，什么时候 workflow 足够，以及什么时候不该过早走向多智能体。
8. 保护 editorial role clarity，避免相邻的 operational chapters 再次塌回重复与 overlap。

## 已完成内容

- GitHub Pages 站点骨架。
- 书籍导航与结构。
- 第一部分参考架构。
- 第一组面向 production-like 场景的实战案例。
- 第一组可复用的按场景组织的 policy templates 与 checklists。
- 新增了一部分 lifecycle discipline 内容，用来连接经典 SDLC 与 ADLC。
- 独立的发布技术栈页面。
- 后续章节可复用的来源基础。

[进入第一部分](part-i/index.md){ .md-button .md-button--primary }
