# Rust、Python 与 TypeScript：如何为智能体平台选型

这页不回答“哪门语言总体上更好”，而是回答一个更有用的问题：

**今天在智能体平台的不同层里，哪门语言更适合哪类职责。**

## 简短结论

对大多数团队来说，2026 年更实际的组合通常是：

- 用 **Python** 或 **TypeScript** 做最快的智能体行为迭代；
- 用 **Rust** 做长期运行的平台服务，在严格契约、性能和可靠性最重要的地方发力；
- 混合栈通常比“全站只用一种语言”的意识形态更成熟。

## 决策矩阵

| 维度 | Rust | Python | TypeScript |
| --- | --- | --- | --- |
| 快速应用层迭代 | 较弱 | 很强 | 很强 |
| 厂商 agent SDK 成熟度 | 不均衡 | 强 | 强 |
| 严格契约型服务 | 很强 | 中等 | 中等 |
| gateway/runtime 性能 | 很强 | 较弱 | 中等 |
| 基础设施网络服务 | 很强 | 中等 | 中等 |
| eval 与 experiment loop | 中等 | 很强 | 强 |
| MCP server 与集成层 | 强 | 强 | 强 |
| control plane 与策略执行 | 很强 | 中等 | 中等 |

## 什么时候选 Rust

Rust 特别适合这些服务：

- 共享工具网关；
- 策略引擎；
- 审批服务；
- trace ingestion pipeline；
- 面向审计的 control plane；
- 对可靠性要求较高的 MCP server；
- 负载更重的记忆或索引服务。

这些地方更看重的是系统是否稳定、干净、可预测，而不是语言本身是否“流行”。

## 什么时候选 Python

Python 通常更适合：

- 快速调整智能体行为；
- 迭代 prompt、routines 与 evals；
- 紧贴 data-heavy stack 工作；
- 使用模型厂商最新的示例和特性；
- 做研究型或实验型 workflow。

当真正的瓶颈是团队学习和试错速度，而不是网关性能时，Python 往往更占优。

## 什么时候选 TypeScript

TypeScript 特别实用的情况包括：

- 产品主体已经在 JS/TS 生态里；
- 智能体靠近 web/backend 应用；
- 希望 frontend、backend 和工具契约共享一套类型模型；
- 团队想快速交付 product-facing integration，而不切换技术栈。

对产品侧智能体层来说，TypeScript 常常是最自然的选择。

## 为什么混合栈通常更成熟

对真实团队来说，更健康的结构通常是：

1. 产品行为与实验继续放在 Python 或 TypeScript。
2. 网关、策略、审批、可观测性逐步抽成更严格的服务。
3. 当平台开始变成长期运行的工程系统，而不只是快速试验层时，再引入 Rust。

这通常比在真正的平台约束还没弄清楚之前，就先争论“哪门语言才是正确答案”更稳妥。

## 常见错误

- 为了语言纯度过早选择 Rust；
- 当高吞吐 gateway 已经被基础设施约束卡住时，仍然把它留在 Python；
- 只是因为产品里已经有 TypeScript，就把它硬塞进低层 control plane；
- 在还不知道长期运维负担会落在哪一层之前，就先决定语言。

## 一个实用规则

如果某一层主要负责：

- **behavior iteration** —— 往往更适合 Python/TypeScript；
- **platform control** —— 往往更适合 Rust；
- **product integration** —— 往往更适合 TypeScript；
- **eval 和 experimentation** —— 往往更适合 Python。

## 语言选型前先确定什么

在选语言之前，更重要的是先搞清楚：

- trust boundary 在哪里；
- 哪些服务会长期运行；
- 哪一层最需要 strongest contract layer；
- 真实需要哪些 vendor SDK；
- 哪些地方更在乎交付速度，哪些地方更在乎运行可靠性。

这些问题定下来之后，语言选择会自然得多，也更少意识形态色彩。

## 结论

今天做智能体系统时，很少需要“全部用 Rust”或“全部用 Python”这种答案。

更成熟的答案通常是：

- **Python/TypeScript** 加快智能体行为开发；
- **Rust** 强化围绕这些行为的平台层。

也正因为如此，Rust 在这本书里更适合作为 **agent platform services** 的语言出现，而不是成为“如何构建智能体”的唯一主线。

## 延伸阅读

- [Rust 与智能体平台](rust-agent-platforms.zh.md)
- [第 8 章：执行模型与工具目录](../book/part-iv/chapter-8.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
- [参考运行时包](reference-package.zh.md)
- [参考来源](sources.zh.md)
