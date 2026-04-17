# 第八部分：智能体系统生命周期

到这里为止，这本书已经解释了如何搭建架构、加固安全、建立可观测性以及安全地上线。但生产级纪律并不会在上线检查清单结束。

在贯穿全书的 support 场景里，到这里已经有了可运行的 runtime、policy layer、capability catalog 和一次受控 rollout。现在问题变了：怎样让这套系统稳定运行几个月，怎样在不失控的前提下持续修改它，以及什么时候应该停止、替换或退役。

只要系统活得比一场 demo 更久，你很快就会遇到另一类问题：

- 智能体项目如何正式进入交付流程；
- design review 应该如何进行；
- 哪些变更应该被视为高风险变更；
- model、prompt、policy 和 tool changes 应该如何发布；
- 事故发生后如何调查，以及系统何时应该退役。

这正是经典工程纪律与智能体特性相遇的地方。所以这一部分最好的开场，不是“发明一个全新流程”，而是先说明如何从经典 SDLC 过渡到 ADLC。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 19 章](chapter-19.zh.md)：先用从 SDLC 到 ADLC 的过渡建立共同框架；
    - [第 20 章](chapter-20.zh.md)：再定义哪些 agent changes 真正属于 release-bearing；
    - [第 21 章](chapter-21.zh.md) 和 [第 22 章](chapter-22.zh.md)：补齐 assurance、provenance、artifact discipline、contract/schema governance、delegated authorization lineage 与 verifier-aware evidence discipline；
    - [第 23 章](chapter-23.zh.md)：再用 replacement、retirement、runtime-control shutdown 与 delegated-authorization revocation/archival 把生命周期收束起来；
    - [第 24 到 27 章](chapter-24.zh.md)：沿着同一条线继续扩展到 misalignment、behavioral evals、verifier-aware AI-native observability，以及围绕 interruption、expiry 与 re-init paths 的 agent estate 治理。

## 这一部分解决什么问题

- 把 reference implementation 推进成可管理的 lifecycle；
- 把 change management、assurance、provenance、incidents、retirement、observability、verifier-aware evidence、runtime-control governance、interruption/expiry/re-init discipline、delegated authorization lineage 与 agent-estate governance 接成一个 operational contour；
- 把稳定的工程纪律和快速变化的 vendor / research 细节区分开来。

如果把这一部分当成一个完整模块来读，它的顺序很清晰：

- 先通过从 SDLC 到 ADLC 的过渡建立共同框架；
- 再定义哪些智能体系统变更真正属于 release-bearing changes；
- 接着围绕 red teaming、detection 和 response 建立 assurance loop；
- 然后把工件纪律、来源追踪与 contract/schema governance 固定下来；
- 再用替换、退役与 runtime-control shutdown 把生命周期先收束起来；
- 最后把同一套纪律扩展到 misalignment、behavioral assurance、verifier-aware AI-native observability、整个 agent estate 的治理，以及对 interruption、expiry 与 re-init paths 的显式控制。

## 本部分内容

- [第 19 章：从 SDLC 到 ADLC](chapter-19.zh.md)
- [第 20 章：智能体系统的 Change Management](chapter-20.zh.md)
- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](chapter-21.zh.md)
- [第 22 章：Supply Chain、Provenance 与 Approved Artifacts](chapter-22.zh.md)
- [第 23 章：Retirement、Replacement 与 End-of-Life Discipline](chapter-23.zh.md)
- [第 24 章：Agentic Misalignment 与 Insider Risk](chapter-24.zh.md)
- [第 25 章：Behavioral Evals、Control Evals 与 Automated Red Teaming](chapter-25.zh.md)
- [第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry](chapter-26.zh.md)
- [第 27 章：Agent Inventory、Registry 与 Sprawl 治理](chapter-27.zh.md)

## 读完这一部分后，你应该得到什么

- 一套面向生产级 agent systems 的完整生命周期框架；
- 一种更成熟的变更评审与发布门禁视角；
- 对 evals、incidents、provenance、ownership 与 session-control responsibilities 之间关系的清晰理解；
- 一套可以真正讨论 replacement、retirement、end-of-life discipline、runtime-control shutdown 与 interruption/expiry/re-init governance 的实践语言；
- 一套可以讨论 sabotage-like behavior、control failures、contract drift 与 automated assurance 的更成熟框架；
- 一套把 observability 当作 inventory、detection、runtime-control signals、verifier judgments 与 governance 证据层的实践视角；
- 一套治理整个 agent estate 而不是单个 agent system 的工作框架；
- 更清晰地理解 Part VIII 不是几章松散的安全内容，而是一套连续的 operating model。
