# 第 19 章：从 SDLC 到 ADLC

## 1. 为什么这里要先回到经典 SDLC

当团队开始构建智能体系统时，常常会很快得出一个结论：“旧流程已经不适用了，我们需要一个全新的生命周期。”

这不是一个好的起点。

经典的软件开发生命周期依然重要，因为它提供了最基础的工程纪律：

- 需求；
- 设计；
- 实现；
- 测试；
- 发布；
- 运维；
- 退役。

NIST 在面向生成式 AI 的 SSDF 配置文件里采取的也是同样的思路：不是从零发明一套安全开发实践，而是在已有的软件安全纪律之上做扩展。[^nist-ssdfa]

也就是说，智能体系统并没有取代 SDLC。它只是让默认形态的 SDLC 变得不够用。

这正是本章真正的承诺。它不是为了把软件生命周期换一个新缩写，而是为了说明：在 Part VII 已经搭好的那套受治理系统之上，现在需要一个足够宽的生命周期框架，去容纳模型行为、policy 变化、retrieval drift、tool side effects、evidence，以及随时间推进的 retirement decisions。

## 2. 哪些东西并没有变

如果把 hype 拿掉，很多基础工作依然完全熟悉：

- 需求仍然要写清楚；
- 架构仍然需要设计评审；
- 集成仍然需要负责人和契约；
- 高风险变更仍然需要受控发布；
- 事故仍然需要复盘和纠正行动。

这点对团队的心理预期很重要。ADLC 不应该被理解成“超越工程的魔法”，而应该被理解成经典工程纪律的成熟扩展。

## 3. 智能体系统到底改变了什么

真正的差异从这里开始。

在普通系统里，行为主要由代码和相对确定性的逻辑决定。到了智能体系统，额外的可变表面出现了：

- 模型行为具有概率性；
- 提示和例程对结果的影响并不亚于代码；
- 检索和记忆会在不改业务逻辑的情况下改变输入；
- 工具会产生真实的副作用；
- 策略变更会重塑整类任务的行为；
- 即使“发布没坏”，在线漂移也可能慢慢出现。

这也是为什么 NIST 的 GenAI Profile 特别强调：可信性考量不能只在发布时出现，而要贯穿设计、开发、使用和评估的全生命周期。[^nist-genai]

## 4. 最好把 ADLC 理解成 SDLC 加上新的变更表面

最实用的工程表达其实很简单：

`ADLC = SDLC + model behavior + prompts/routines + policies + retrieval/memory + tools + evals + governed autonomy`

也就是说，新的生命周期不是因为“智能体很神秘”，而是因为现在有更多可变部件需要被发布、评估和治理。

<div class="diagram-card">
<p>最稳妥的理解方式，是把 ADLC 看成 SDLC 的扩展，而不是替代品</p>

``` mermaid
flowchart LR
    A["Classical SDLC"] --> B["Requirements"]
    A --> C["Design"]
    A --> D["Implementation"]
    A --> E["Testing"]
    A --> F["Release"]
    A --> G["Operations"]
    A --> H["Retirement"]

    H --> I["ADLC adds"]
    I --> J["Model behavior"]
    I --> K["Prompts and routines"]
    I --> L["Policies and approvals"]
    I --> M["Retrieval and memory"]
    I --> N["Tool side effects"]
    I --> O["Evals and controlled autonomy"]
```

</div>

## 5. 哪些东西现在也成了发布承载工件

在传统 SDLC 里，团队最常围绕代码、基础设施和数据模式讨论发布。但在 ADLC 里，发布承载工件更宽：

- 模型选择与路由；
- 系统指令与例程；
- 策略配置；
- 能力契约；
- 检索语料；
- 记忆写入规则；
- 评测数据集；
- 审批策略；
- 发布门禁。

这是最关键的运行转变之一。如果团队只把代码改动当成发布，它几乎一定会漏掉真正高风险的智能体变更。

## 6. 为什么 tests 已经不够了

测试依然重要，但已经不够。

智能体系统需要更宽的 assurance contour：

- 针对代码和契约的确定性测试；
- 面向已知场景的离线评测；
- 面向多步行为的模拟器或场景化检查；
- 面向漂移和涌现失败的在线监控；
- 针对高风险路径的策略检查；
- 用来控制影响半径的审批与发布门禁。

OpenAI 和 Anthropic 从不同角度都落到了相似的实践结论：先建立基线行为，再在受控条件下迭代，而不是一开始就追求自主性。[^openai-guide][^anthropic-agents]

## 7. 安全保障也需要自己的生命周期

在普通服务里，安全审查常常聚焦于代码、依赖、基础设施和访问控制。但对智能体系统来说，这还不够。

Google Research 很清楚地指出，安全保障更应该作为持续循环存在，而不是一次性安全审查：红队测试、漏洞管理、检测与响应、威胁情报和修复必须紧贴发布流程，而不是等问题发生后再补。[^google-assurance]

这对本书很重要：智能体安全不能被简化成提示注入检查清单，它本质上是一个持续运行的能力。

## 8. 智能体的供应链不只是包依赖

Google 还有一个很有价值的修正：AI 软件供应链不只包含库和容器，还包括模型、数据、配置、流水线以及评测工件的来源证明。[^google-supply-chain]

对智能体系统来说，这很关键，因为否则你就回答不了这些问题：

- 这个模型从哪里来；
- 这个发布是用什么数据集验证的；
- 生产环境里到底是哪一个策略包；
- 当时用的是哪一版检索语料；
- 两次发布波次之间到底变了哪个提示或例程。

换句话说，ADLC 里的来源证明不是“锦上添花”，而是变更管理和事故调查的基础设施。

## 9. 好的 ADLC 应该从 intake 和 design review 开始

如果一个智能体项目只有在“已经做出点东西”之后才进入工程流程，那么 architecture 和 governance 问题往往会暴露得太晚。

有价值的早期问题包括：

- 这里真的需要智能体，还是工作流就够了；
- 自主性预算是多少；
- 哪些副作用是允许的；
- 信任边界在哪里；
- 哪些能力属于高风险；
- 是否真的需要记忆层；
- 在试点前必须具备哪些评测。

这些其实已经是 ADLC 的第一阶段了。

## 10. 一个实用的 ADLC 框架

对于 production-grade 智能体系统，我建议至少有这些阶段：

1. Intake and suitability review
2. Architecture and safety design review
3. Build and integration
4. Eval baseline
5. Staged rollout
6. Steady-state operations
7. Incident response and corrective action
8. Retirement or replacement

<div class="diagram-card">
<p>把 ADLC 看成持续循环，而不是“第一次上线之前的流程”，会更接近真实世界</p>

``` mermaid
flowchart LR
    A["Intake"] --> B["Design review"]
    B --> C["Build and integration"]
    C --> D["Eval baseline"]
    D --> E["Staged rollout"]
    E --> F["Operations"]
    F --> G["Incidents and corrective actions"]
    G --> H["Retirement or replacement"]
    H --> A
```

</div>

## 11. 为什么这会对团队产生真正帮助

如果这些内容只被叫做“最佳实践”，团队往往会把它当成可选建议。

但一旦它被组织成 lifecycle model，问题就会变得更成熟：

- 我们现在在哪个阶段；
- 下一阶段还缺什么；
- 过下一道 gate 前必须产出什么 artifact；
- 下一步由谁负责；
- 如果跳过某个阶段，我们究竟在承担什么风险。

这正是 ADLC 的实际价值所在：它把关于智能体的讨论，从 hype discussion 变成可管理的工程计划。

## 12. 不该怎么做

这里有几种非常常见的错误：

- 直接宣布“普通工程方法对智能体无效”；
- 把 ADLC 误解成 prompt iteration 的新名字；
- 以为 rollout checklist 就等于整个 lifecycle；
- 不把 prompt、policy 和 retrieval 视为 release-bearing changes；
- 不把 evals 和 change management 连起来；
- 在最后时刻才想起 retirement discipline。

如果这样做，ADLC 最终就只会变成一个好听但没 operational 价值的词。

## 13. 实用检查清单

如果你想快速判断自己是否已经需要完整的 ADLC，可以问：

- 你们除了代码，还会持续发布 prompt、policy 或 model changes 吗？
- 系统会产生高风险 side effects 吗？
- 系统使用 retrieval、memory 或其他 mutable knowledge surfaces 吗？
- release decisions 是否依赖 evals？
- 是否已经需要 staged rollout、approval gates 和 incident review？
- 在发生事故时，你们是否需要解释“当时生产环境里到底是哪一个 exact artifact”？

如果连续几个问题的答案都是“是”，那你们其实已经活在 ADLC 里了，只是还没有把它明确说出来。

## 14. 接下来读什么

这章之后最自然的延伸，是 change management、assurance loop 和 supply chain discipline。但它现在已经可以和书里已有的内容连起来：

- [第 13 章：离线评测、在线评测与回归门禁](../part-v/chapter-13.zh.md)
- [第 18 章：生产上线检查清单](../part-vii/chapter-18.zh.md)
- [第六部分：组织模型](../part-vi/index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^nist-ssdfa]: [NIST SP 800-218A: Secure Software Development Practices for Generative AI and Dual-Use Foundation Models](https://csrc.nist.gov/pubs/sp/800/218/a/final)
[^nist-genai]: [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
[^openai-guide]: [OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^anthropic-agents]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
