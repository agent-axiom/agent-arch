# 第八部分：智能体系统生命周期

到这里为止，这本书已经解释了如何搭建架构、加固安全、建立可观测性以及安全地发布变更。但 production discipline 不会在 go-live 结束。

只要 agent system 活得比一场 demo 更久，你很快就会遇到另一类问题：

- 哪些变更应该被视为对发布有实质影响；
- 怎样响应 drift 与 findings；
- 怎样保住受信任工件的 lineage；
- 怎样让系统退出运行；
- 怎样把控制范围扩展到整个 estate，而不只是一个 agent。

这一部分回答的正是这些问题。它不再把 agent system 读成一张架构图，而是读成一个 governed lifecycle。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 19 章](chapter-19.zh.md)：先把从 SDLC 到 ADLC 当作工作框架建立起来；
    - [第 20 章](chapter-20.zh.md)：判断哪些变更真正对发布有实质影响；
    - [第 21 章](chapter-21.zh.md)：看清 findings 怎样变成 response；
    - [第 22 章](chapter-22.zh.md)：固定受信任工件的 lineage；
    - [第 23 章](chapter-23.zh.md)：通过 replacement 与 retirement 把生命周期闭合起来；
    - [第 24 到 27 章](chapter-24.zh.md)：把同一条轮廓继续扩展到 adversarial pressure、judgment、observability 与整个 estate 的 accountability。

## 这一部分解决什么问题

- 它把 agent system 展示成 governed lifecycle，而不是一次性 launch；
- 它把 release judgment 与 response、lineage、closure 和 estate accountability 区分开来；
- 它给出一套可以讨论 change review、incident、retirement 和 sprawl 的语言；
- 它帮助读者把 production agent estate 读成一个有 ownership 的系统，而不是一堆 controls。

## 本部分内容

- [第 19 章：从 SDLC 到 ADLC](chapter-19.zh.md)
- [第 20 章：智能体系统的 Change Management](chapter-20.zh.md)
- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](chapter-21.zh.md)
- [第 22 章：Supply Chain、Provenance 与 Approved Artifacts](chapter-22.zh.md)
- [第 23 章：Retirement、Replacement 与 End-of-Life Discipline](chapter-23.zh.md)
- [第 24 章：Agentic Misalignment 与 Insider Risk](chapter-24.zh.md)
- [第 25 章：Behavioral Evals、Control Evals 与 Automated Red Teaming](chapter-25.zh.md)
- [第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry](chapter-26.zh.md)
- [第 27 章：智能体清单、注册表与蔓延治理](chapter-27.zh.md)

## 读完这一部分后，你应该得到什么

- 一套更成熟的 release gates 与 change review 框架；
- 更清楚地区分 judgment、response、lineage、observability 与 accountability；
- 一套关于 agent system 如何在时间中被修改、约束、调查与关闭的实用模型。
