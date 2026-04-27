# Google 内容整合路线图

这页单独固定一份计划，说明最近的 Google Cloud 材料里哪些内容值得吸收进这本书。目标不是重复已有章节，而是在 Google 特别强的地方补强全书：平台视角、运行时隔离、身份边界与治理。

## 为什么值得单独做一份路线图

Google 最近真正有价值的内容，不是泛泛而谈“AI 智能体”，而是四条很实用的 production-grade 线索：

- 面向平台的 agent system 视角；
- 把 sandboxed execution 当作基础设施层；
- agent identity、registry 与 governance；
- 明确区分 `MCP` 和 `A2A`。

这些内容和书里已经使用的 OpenAI、Anthropic、LangGraph 材料正好互补。

## 分步计划

### 步骤 1：平台五大支柱与 context layers

放到哪里：

- [第 2 章：安全智能体的参考架构](../book/part-i/chapter-2.zh.md)

要补充什么：

- `framework -> model -> tools -> runtime -> trust` 这条主线；
- context layers：static、session、turn、cached context；
- 关于 prompt budget 和 context discipline 的实战段落。

### 步骤 2：Agent identity 与 access boundaries

放到哪里：

- [第 3 章：安全边界与信任边界](../book/part-ii/chapter-3.zh.md)
- [第 4 章：工具网关、审批与审计轨迹](../book/part-ii/chapter-4.zh.md)

要补充什么：

- machine identity 和 agent identity 作为单独层；
- 面向 tools、memory 和 external systems 的 least privilege；
- identity 与 auditability 的关系。

### 步骤 3：Memory governance 与 memory revisions

放到哪里：

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](../book/part-iii/chapter-5.zh.md)
- [第 6 章：short-term、long-term 与 profile memory](../book/part-iii/chapter-6.zh.md)

要补充什么：

- memory read policy 与 memory write policy 的清晰拆分；
- memory update 的 revisions 与 provenance；
- memory store 本身也是需要治理的 subsystem。

### 步骤 4：把 sandbox execution 写成基础设施层

放到哪里：

- [第 9 章：沙箱执行与 MCP 作为集成契约](../book/part-iv/chapter-9.zh.md)

要补充什么：

- logical isolation、process isolation、runtime isolation 的区别；
- ephemeral sandboxes；
- network egress controls 与 artifact discipline；
- 面向 high-risk tools 的实战 checklist。

### 步骤 5：MCP 用于 tools，A2A 用于 agents

放到哪里：

- [第 9 章：沙箱执行与 MCP 作为集成契约](../book/part-iv/chapter-9.zh.md)
- Part IV 中新增一个实践块

要补充什么：

- 明确区分 `MCP` 与 `A2A`；
- 什么场景需要 capability contract，什么场景才真的需要 agent-to-agent collaboration；
- 什么时候不该过早进入 multi-agent coordination。

### 步骤 6：User simulator 与 continuous eval loop

放到哪里：

- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)

要补充什么：

- user simulator 作为单独的 eval 模式；
- 基于 traces 的 continuous grading；
- eval loop 与 rollout gates 的更强连接。

### 步骤 7：Registry、approved inventory 与 organizational controls

放到哪里：

- [第 14 章：平台团队与产品团队](../book/part-vi/chapter-14.zh.md)
- [第 15 章：黄金路径、共享网关与反动物园模式](../book/part-vi/chapter-15.zh.md)

要补充什么：

- agents、tools、connectors 的 approved registry；
- platform inventory 作为 governance 的一部分；
- 用 continuous controls 代替一次性的人工审批。

### 步骤 8：增强 reference implementation

放到哪里：

- [第 16 章：基础运行时蓝图](../book/part-vii/chapter-16.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
- `agent_runtime_ref`

要补充什么：

- runtime 里的 context layers；
- agent identity；
- memory provenance；
- sandbox profile；
- 类似 registry 的 capability inventory。

## 优先级

如果按读者的直接收益排序，我会这样排：

1. context layers；
2. identity；
3. sandbox infrastructure；
4. MCP vs A2A；
5. memory governance；
6. user simulator；
7. registry 与 continuous controls；
8. runtime uplift。

## 来源

- Google Cloud, [Achieve agentic productivity with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder)
- Google Cloud, [More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
- Google Cloud, [Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
- Google Cloud Architecture Center, [Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
- Google Cloud, [How Google secures AI Agents](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents)
- Google Cloud, [Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)
- Google Cloud, [Building Connected Agents with MCP and A2A](https://cloud.google.com/blog/topics/developers-practitioners/building-connected-agents-with-mcp-and-a2a)
- Google Cloud, [Recommended AI Controls framework](https://cloud.google.com/blog/products/identity-security/audit-smarter-introducing-our-recommended-ai-controls-framework)
