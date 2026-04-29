# Google 内容整合路线图

这页单独固定一份计划，说明最近的 Google Cloud 材料里哪些内容值得吸收进这本书。目标不是重复已有章节，而是在 Google 特别强的地方补强全书：平台视角、运行时隔离、身份边界与治理。

## 为什么值得单独做一份路线图

Google 最近真正有价值的内容，不是泛泛而谈“AI 智能体”，而是四条很实用的生产级线索：

- 面向平台的智能体系统视角；
- 把沙箱执行当作基础设施层；
- 智能体身份、注册表与治理；
- 明确区分 `MCP` 和 `A2A`。

这些内容和书里已经使用的 OpenAI、Anthropic、LangGraph 材料正好互补。

## 分步计划

### 步骤 1：平台五大支柱与上下文层

放到哪里：

- [第 2 章：安全智能体的参考架构](../book/part-i/chapter-2.zh.md)

要补充什么：

- `framework→model→tools→runtime→trust` 这条主线；
- 上下文层：静态、会话、轮次、缓存上下文；
- 关于提示预算和上下文纪律的实战段落。

### 步骤 2：智能体身份与访问边界

放到哪里：

- [第 3 章：安全边界与信任边界](../book/part-ii/chapter-3.zh.md)
- [第 4 章：工具网关、审批与审计轨迹](../book/part-ii/chapter-4.zh.md)

要补充什么：

- 机器身份和智能体身份作为单独层；
- 面向工具、记忆和外部系统的最小权限；
- 身份与可审计性的关系。

### 步骤 3：记忆治理与记忆修订

放到哪里：

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](../book/part-iii/chapter-5.zh.md)
- [第 6 章：短期记忆、长期记忆与用户画像记忆](../book/part-iii/chapter-6.zh.md)

要补充什么：

- 记忆读取策略与记忆写入策略的清晰拆分；
- 记忆更新的修订与来源证明；
- 记忆存储本身也是需要治理的子系统。

### 步骤 4：把沙箱执行写成基础设施层

放到哪里：

- [第 9 章：沙箱执行与 MCP 作为集成契约](../book/part-iv/chapter-9.zh.md)

要补充什么：

- 逻辑隔离、进程隔离、运行时隔离的区别；
- 短暂沙箱；
- 网络出口控制与工件纪律；
- 面向高风险工具的实战检查清单。

### 步骤 5：MCP 用于工具，A2A 用于智能体

放到哪里：

- [第 9 章：沙箱执行与 MCP 作为集成契约](../book/part-iv/chapter-9.zh.md)
- Part IV 中新增一个实践块

要补充什么：

- 明确区分 `MCP` 与 `A2A`；
- 什么场景需要能力契约，什么场景才真的需要智能体到智能体协作；
- 什么时候不该过早进入多智能体协调。

### 步骤 6：用户模拟器与连续评测闭环

放到哪里：

- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)

要补充什么：

- 用户模拟器作为单独的评测模式；
- 基于追踪的连续打分；
- 评测闭环与发布门禁的更强连接。

### 步骤 7：注册表、已批准清单与组织控制

放到哪里：

- [第 14 章：平台团队与产品团队](../book/part-vi/chapter-14.zh.md)
- [第 15 章：黄金路径、共享网关与反动物园模式](../book/part-vi/chapter-15.zh.md)

要补充什么：

- 智能体、工具、连接器的已批准注册表；
- 平台清单作为治理的一部分；
- 用连续控制代替一次性的人工审批。

### 步骤 8：增强参考实现

放到哪里：

- [第 16 章：基础运行时蓝图](../book/part-vii/chapter-16.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
- `agent_runtime_ref`

要补充什么：

- 运行时里的上下文层；
- 智能体身份；
- 记忆来源证明；
- 沙箱画像；
- 类似注册表的能力清单。

## 优先级

如果按读者的直接收益排序，我会这样排：

1. 上下文层；
2. 身份；
3. 沙箱基础设施；
4. MCP vs A2A；
5. 记忆治理；
6. 用户模拟器；
7. 注册表与连续控制；
8. 运行时升级。

## 来源

- Google Cloud, [Achieve agentic productivity with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder)
- Google Cloud, [More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
- Google Cloud, [Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
- Google Cloud Architecture Center, [Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
- Google Cloud, [How Google secures AI Agents](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents)
- Google Cloud, [Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)
- Google Cloud, [Building Connected Agents with MCP and A2A](https://cloud.google.com/blog/topics/developers-practitioners/building-connected-agents-with-mcp-and-a2a)
- Google Cloud, [Recommended AI Controls framework](https://cloud.google.com/blog/products/identity-security/audit-smarter-introducing-our-recommended-ai-controls-framework)
