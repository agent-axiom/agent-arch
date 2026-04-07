# 第八部分：智能体系统生命周期

到这里为止，这本书已经解释了如何搭建架构、加固安全、建立可观测性以及安全地上线。但生产级纪律并不会在上线检查清单结束。

只要系统活得比一场 demo 更久，你很快就会遇到另一类问题：

- 智能体项目如何正式进入交付流程；
- design review 应该如何进行；
- 哪些变更应该被视为高风险变更；
- model、prompt、policy 和 tool changes 应该如何发布；
- 事故发生后如何调查，以及系统何时应该退役。

这正是经典工程纪律与智能体特性相遇的地方。所以这一部分最好的开场，不是“发明一个全新流程”，而是先说明如何从经典 SDLC 过渡到 ADLC。

如果把这一部分当成一个完整模块来读，它的顺序很清晰：

- 先通过从 SDLC 到 ADLC 的过渡建立共同框架；
- 再定义哪些智能体系统变更真正属于 release-bearing changes；
- 接着围绕 red teaming、detection 和 response 建立 assurance loop；
- 然后把工件纪律与来源追踪固定下来；
- 最后用替换与退役把整个生命周期收束起来。

## 本部分内容

- [第 19 章：从 SDLC 到 ADLC](chapter-19.zh.md)
- [第 20 章：智能体系统的 Change Management](chapter-20.zh.md)
- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](chapter-21.zh.md)
- [第 22 章：Supply Chain、Provenance 与 Approved Artifacts](chapter-22.zh.md)
- [第 23 章：Retirement、Replacement 与 End-of-Life Discipline](chapter-23.zh.md)

## 读完这一部分后，你应该得到什么

- 一套面向生产级 agent systems 的完整生命周期框架；
- 一种更成熟的变更评审与发布门禁视角；
- 对 evals、incidents、provenance 与 ownership 之间关系的清晰理解；
- 一套可以真正讨论 replacement、retirement 与 end-of-life discipline 的实践语言。
