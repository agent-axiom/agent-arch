# 在线配套资料

在线配套资料保存那些需要独立于纸质书稿进行版本管理、验证和更新的内容。

书中保留论证、决策标准和最小契约形式；这里保留完整的命令行演练、运行时配置、追踪与事件目录、评估数据集、资料来源和参考演练。

## 主要入口

- [运行时配置与 MCP 边界](runtime-reference/configs.md)
- [运行时命令行](runtime-reference/cli.md)
- [评估数据集](runtime-reference/eval-datasets.md)
- [追踪与事件](runtime-reference/traces-and-events.md)
- [模板](templates/index.md)
- [检查清单](checklists/index.md)
- [变更日志](changelog.md)
- [勘误](errata.md)
- 示例工件：
  `artifacts/trace-demo.jsonl`、
  `artifacts/trace-failed-tool-timeout.jsonl`、
  `artifacts/trace-post-dispatch-timeout.jsonl`、
  `artifacts/session-failed-tool-timeout.json`、
  `artifacts/eval-failed-run-timeout.json`、
  `artifacts/eval-unknown-effect-reconciliation.json`
- 已填写示例：
  `examples/capability-contract-support-ticket.md`、
  `examples/release-decision-record-support-ticket.md`、
  `examples/incident-record-support-ticket-timeout.md`、
  `examples/production-readiness-support-ticket.md`、
  `examples/context-manifest-support-ticket.yaml`、
  `examples/threat-map-negative-tests.yaml`、
  `examples/slo-card-support-ticket.yaml`、
  `examples/adlc-transition-support-ticket.yaml`、
  `examples/readiness-rubric-support-ticket.yaml`
- [完整参考包演练](../appendix/reference-package.zh.md)
- [完整资料来源列表](../appendix/sources.zh.md)

## 安全智能体实践路径

希望亲手复现材料的读者应从[完整参考包演练](../appendix/reference-package.zh.md)开始。它把各章与 `agent_runtime_ref` 文件、命令行命令、配套工件和测试连接起来。最短实践路径是：用 `inspect-agent` 检查清单，用 `simulate-run` 执行受控运行，用 `dump-events` 和 `inspect-trace` 获取证据，用 `inspect-approvals` 检查人工闸门，用 `export-eval-dataset` 导出评估数据，再用 `check-rollout` 和 `check-controls` 做发布决策。

## 哪些内容应放在这里

- 完整的 YAML 配置和评审表单。
- 命令行命令及预期 JSON 接口。
- 追踪、事件及验证消息目录。
- 评估数据集、验证器契约和发布判断示例。
- 较长的资料目录、变更日志、勘误和更新规则。

## 哪些内容应留在书中

- 为什么需要某个架构决策。
- 它控制什么风险。
- 谁对动作及其证据负责。
- 团队如何判断运行时、策略、追踪、评估闸门和发布已经就绪。

## 章节地图 {#chapter-map}

这张地图把每一章纸质书稿与在线书中的对应主题，以及最接近的可执行或参考工件连接起来。链接名称比网站内部编号更重要：即使在线结构调整，读者仍可按主题和可验证工件查找，而不必猜测哪一章编号相同。

| 纸质书章号 | 在线主题 | 实践与参考 |
| ---: | --- | --- |
| 1 | [为什么智能体需要平台](../book/part-i/chapter-1.zh.md) | [参考包](../appendix/reference-package.zh.md) |
| 2 | [执行形式](../book/part-i/chapter-2.zh.md)、[管理者与交接](../book/part-i/practical-manager-handoffs.zh.md) | [实用请求模式](../book/part-i/practical-routines.zh.md) |
| 3 | [安全智能体架构](../book/part-i/chapter-2.zh.md) | [技术栈地图](../appendix/stack.zh.md) |
| 4 | [信任边界](../book/part-ii/chapter-3.zh.md) | [策略模板](../appendix/policy-templates.zh.md) |
| 5 | [策略层与能力目录](../book/part-vii/chapter-17.zh.md) | [策略包模式](../appendix/policy-bundle-schema.zh.md) |
| 6 | [工具网关与审批](../book/part-ii/chapter-4.zh.md) | [审批模式](../appendix/approval-schema.zh.md) |
| 7 | [记忆风险](../book/part-iii/chapter-5.zh.md) | [记忆评估模式](../appendix/memory-eval-patterns.zh.md) |
| 8 | [记忆类型与生命周期](../book/part-iii/chapter-6.zh.md) | [记忆检索模式](../appendix/memory-retrieval-schema.zh.md) |
| 9 | [上下文检索与压缩](../book/part-iii/chapter-7.zh.md) | [连续性信封](../appendix/continuity-envelope-schema.zh.md) |
| 10 | [执行模型与工具](../book/part-iv/chapter-8.zh.md) | [配置参考](runtime-reference/configs.md) |
| 11 | [沙箱与 MCP](../book/part-iv/chapter-9.zh.md)、[MCP 与 A2A 边界](../book/part-iv/practical-mcp-a2a.zh.md) | [工具故障恢复](../appendix/tool-failure-recovery.zh.md) |
| 12 | [重试、限制与回滚](../book/part-iv/chapter-10.zh.md) | [工具故障恢复](../appendix/tool-failure-recovery.zh.md) |
| 13 | [追踪与事件](../book/part-v/chapter-11.zh.md) | [追踪与事件目录](runtime-reference/traces-and-events.md) |
| 14 | [智能体系统 SLO](../book/part-v/chapter-12.zh.md) | [已填写的 SLO 卡片](examples/slo-card-support-ticket.yaml) |
| 15 | [评估与回归闸门](../book/part-v/chapter-13.zh.md) | [评估数据集](runtime-reference/eval-datasets.md) |
| 16 | [端到端证据链](../book/part-v/evidence-spine.zh.md) | [变更评审与发布模式](../appendix/change-rollout-schema.zh.md) |
| 17 | [平台团队与产品团队](../book/part-vi/chapter-14.zh.md) | [能力契约模板](templates/capability-contract.md) |
| 18 | [受支持的黄金路径](../book/part-vi/chapter-15.zh.md) | [已填写的黄金路径契约](examples/capability-contract-support-ticket.md) |
| 19 | [智能体清单与注册表](../book/part-viii/chapter-27.zh.md) | [注册表运维手册](../appendix/registry-operations-handbook.zh.md) |
| 20 | [从 SDLC 到 ADLC](../book/part-viii/chapter-19.zh.md)、[变更管理](../book/part-viii/chapter-20.zh.md) | [ADLC 转换示例](examples/adlc-transition-support-ticket.yaml) |
| 21 | [来源与可信工件](../book/part-viii/chapter-22.zh.md) | [生命周期工件模式](../appendix/lifecycle-artifact-schema.zh.md) |
| 22 | [可观测性与检测遥测](../book/part-viii/chapter-26.zh.md) | [追踪模式](../appendix/trace-schema.zh.md) |
| 23 | [目标错位与内部风险](../book/part-viii/chapter-24.zh.md)、[行为评估](../book/part-viii/chapter-25.zh.md) | [威胁模型负面场景](examples/threat-map-negative-tests.yaml) |
| 24 | [保障与响应](../book/part-viii/chapter-21.zh.md) | [事件响应手册](../appendix/incident-response-playbook.zh.md) |
| 25 | [退役与替换](../book/part-viii/chapter-23.zh.md) | [生命周期工件模式](../appendix/lifecycle-artifact-schema.zh.md) |
| 26 | [基础运行时](../book/part-vii/chapter-16.zh.md) | [命令行参考](runtime-reference/cli.md) |
| 27 | [策略与能力目录](../book/part-vii/chapter-17.zh.md) | [可执行轨迹策略场景](examples/trajectory-policy-scenarios.zh.md) |
| 28 | [生产发布检查清单](../book/part-vii/chapter-18.zh.md) | [生产就绪检查清单](checklists/production-readiness.md) |
