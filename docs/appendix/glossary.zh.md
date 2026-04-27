# 术语表

这页是整本书的快速术语参考。它不替代正文，但可以帮助你快速回忆一个词的含义，并跳到相关章节继续读。

## Agent runtime

代理的执行环境，也就是运行循环、上下文组装、工具调用、策略检查、记忆和遥测所在的地方。

继续阅读：

- [第 2 章：安全智能体的参考架构](../book/part-i/chapter-2.zh.md)
- [第 16 章：基础运行时蓝图](../book/part-vii/chapter-16.zh.md)

## Control plane

平台的治理层。通常包括策略、能力目录、审批、上线检查和审计逻辑。

继续阅读：

- [第 2 章：安全智能体的参考架构](../book/part-i/chapter-2.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)

## Trust boundary

不同信任级别和控制级别之间的边界，例如用户输入、记忆层、工具层和外部系统之间的边界。

继续阅读：

- [第 3 章：安全边界与信任边界](../book/part-ii/chapter-3.zh.md)

## Policy gate

系统做出决策的检查点，用来判断是否允许执行动作、读取数据、写入记忆或调用工具。

继续阅读：

- [第 4 章：工具网关、审批与审计链路](../book/part-ii/chapter-4.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)

## Capability catalog

代理能力的注册表：有哪些工具、谁负责、风险级别是什么、使用什么传输方式，以及适用哪些限制。

继续阅读：

- [第 8 章：执行模型与工具目录](../book/part-iv/chapter-8.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)

## Approved inventory

为某个代理或某类代理明确批准的能力清单。它帮助团队区分“目录里存在”与“允许使用”。

继续阅读：

- [第 14 章：平台团队与产品团队](../book/part-vi/chapter-14.zh.md)
- [第 15 章：黄金路径、共享网关与反动物园模式](../book/part-vi/chapter-15.zh.md)

## Tool gateway

工具调用前的控制点。它会先检查调用者、策略、风险等级、审批要求和外联规则，再决定是否放行。

继续阅读：

- [第 4 章：工具网关、审批与审计链路](../book/part-ii/chapter-4.zh.md)
- [第 8 章：执行模型与工具目录](../book/part-iv/chapter-8.zh.md)

## Sandbox execution

在隔离环境中执行工具，以限制副作用，并减少其对网络、文件系统和其他敏感资源的访问。

继续阅读：

- [第 9 章：沙箱执行与 MCP 作为集成契约](../book/part-iv/chapter-9.zh.md)

## Egress policy

规定代理或工具可以向外访问哪些目标的规则，包括允许访问的域名、服务和网络访问类型。

继续阅读：

- [第 9 章：沙箱执行与 MCP 作为集成契约](../book/part-iv/chapter-9.zh.md)

## Short-term memory

当前会话或当前运行的短期记忆。它帮助系统保留最近的上下文，一般不应该长期保留。

继续阅读：

- [第 6 章：短期记忆、长期记忆与用户画像记忆](../book/part-iii/chapter-6.zh.md)

## Long-term memory

能够跨会话保留的持久记忆。它需要更严格的治理，因为一次错误写入可能长期存在并持续传播。

继续阅读：

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](../book/part-iii/chapter-5.zh.md)
- [第 6 章：短期记忆、长期记忆与用户画像记忆](../book/part-iii/chapter-6.zh.md)

## Profile memory

专门保存用户偏好、稳定属性或工作画像的记忆层。它不是完整互动档案，而是一组经过验证、真正有用的事实。

继续阅读：

- [第 6 章：短期记忆、长期记忆与用户画像记忆](../book/part-iii/chapter-6.zh.md)

## Retrieval

针对某次运行，从记忆层或知识层挑选合适记录的过程。好的 retrieval 不在于多，而在于准。

继续阅读：

- [第 7 章：检索、压缩与后台更新](../book/part-iii/chapter-7.zh.md)

## Compaction

记忆层的后台整理过程，包括合并、压缩、去重和重建记录，避免 memory layer 变成信息垃圾堆。

继续阅读：

- [第 7 章：检索、压缩与后台更新](../book/part-iii/chapter-7.zh.md)

## Provenance

数据来源信息：它从哪里来、通过什么路径进入记忆、由哪条规则放行，以及它值得被信任到什么程度。

继续阅读：

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](../book/part-iii/chapter-5.zh.md)
- [第 6 章：短期记忆、长期记忆与用户画像记忆](../book/part-iii/chapter-6.zh.md)

## Approval gate

系统不会自动执行高风险动作，而是先把它提交给人或其他受信任角色确认的阶段。

继续阅读：

- [第 4 章：工具网关、审批与审计链路](../book/part-ii/chapter-4.zh.md)
- [第 18 章：生产上线检查清单](../book/part-vii/chapter-18.zh.md)

## Trace

单次代理运行的完整关联历史：发生了哪些步骤、做了哪些策略决策、调用了哪些工具，以及最终如何结束。

继续阅读：

- [第 11 章：追踪、跨度与结构化事件](../book/part-v/chapter-11.zh.md)

## Span

Trace 内部的一个片段，例如 retrieval span、tool execution span 或 approval span。

继续阅读：

- [第 11 章：追踪、跨度与结构化事件](../book/part-v/chapter-11.zh.md)

## Rollout gate

在上线或扩大流量前的就绪性检查。它通常会综合考虑安全、评测、可观测性、归属关系和运维控制。

继续阅读：

- [第 12 章：智能体系统的 SLO](../book/part-v/chapter-12.zh.md)
- [第 18 章：生产上线检查清单](../book/part-vii/chapter-18.zh.md)

## Eval dataset

用于回归检查和质量评估的一组样本、运行记录或会话，通常用于上线前或变更后的验证。

继续阅读：

- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
- [参考包](reference-package.zh.md)
