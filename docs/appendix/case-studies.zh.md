# 实战案例

这一页回答一个很直接的问题：这本书落到真实系统里，到底会长成什么样？

下面有三个场景。在这些场景里，架构层、防护栏和编排选择已经可以被讨论成工程决策，而不只是漂亮的表述。

如果你需要的不是场景，而是可以直接复用的策略工件，请去看[策略模板](policy-templates.zh.md)。如果你想看这本书接下来还要补什么，则看[社区路线图](community-roadmap.zh.md)。

!!! example "现在如何阅读这个案例"
    支持分流（support triage）案例已经成为本书的贯穿线索：从这里开始，然后看同一个重复工单故障如何穿过信任边界（trust boundaries）、工具网关（tool gateway）、记忆/检索（memory/retrieval）、幂等性（idempotency）、追踪（traces）、服务级目标（SLO）、评测门禁（eval gates）、归属（ownership）、运行时（runtime）、策略（policy）、发布（rollout）、智能体开发生命周期（ADLC）、保障（assurance）、来源证明（provenance）、退役（retirement）、失配控制（misalignment controls）、遥测（telemetry）和注册表（registry）。

!!! note "规范案例对齐（Canonical case alignment）"
    这些场景对应书籍计划里的三个规范案例（canonical cases）。**支持分流（Support triage）** 是案例 1，用来承载写入能力（write capability）、审批（approvals）和重复工单恢复（duplicate-ticket recovery）。**内部知识助手（Internal knowledge assistant）** 是案例 2，用来承载检索（retrieval）、记忆（memory）、访问控制（access control）、新鲜度（freshness）和知识来源（knowledge provenance）。**事件协调（Incident coordination）** 是案例 3，用来承载追踪（traces）、服务级目标（SLO）、升级（escalation）、通知副作用（notification side effects）、响应归属（response ownership）和事件后学习（post-incident learning）。

## 跨章节路线

阅读正文时，应把这三个案例当作覆盖检查：

- **第 1 章：** 工作流、单智能体循环和多智能体形态之间的选择；
- **第 2 章：** 穿过参考架构、控制平面和数据边界的路径；
- **第 3-4 章：** 信任边界、审批、策略和智能体行动权；
- **第 5-7 章：** 记忆、检索、新鲜度、知识来源证明和投毒防护；
- **第 8-10 章：** 工具网关、MCP/A2A、幂等性、重试和回滚；
- **第 13 章：** 评测、验证器和回归门禁；
- **第 18 章：** 发布就绪度和扩大规模前的审查；
- **第 21-27 章：** 生命周期、保障、来源证明、退役、遥测和注册表。

## 工业运行时模式（Industrial runtime patterns）

把这些案例放在工业实践旁边会更容易阅读。它们不是要求读者复制某个供应商产品，而是展示哪些生产形态已经变得可识别。

### Cloudflare Agents SDK：作为命名持久对象的智能体

Cloudflare Agents SDK 展示了一种模式：智能体不只是围绕模型的一次性循环，而是运行在 Durable Object 之上的可寻址 `Agent` 实例。它有稳定名称、持久 SQL/key-value 状态、WebSocket 连接、定时任务、唤醒和休眠。对本书来说，架构结论很简单：当智能体绑定到真实实体——客户案例、租户工作区、事故房间、设备、项目或研究档案——运行时就应该明确展示谁拥有状态、哪些运行修改过它、哪些定时任务可以唤醒实例，以及哪些追踪证明可以安全恢复。

这里的实践契约是：**稳定名称 → 持久状态 → 唤醒/休眠 → 定时/后台工作 → 审批门禁 → 追踪证据**。这把记忆、后台更新、执行、追踪和发布章节连成一个形状：schedule 不应该是不可见 callback，WebSocket UI 不应该暴露智能体的全部状态，approval 应该位于真正发生 side effect 的边界。

更新的 long-running agents pattern 会让这条契约更硬：agent identity 比 process 活得更久，一部分工作也可能是 agent 内部的 **recoverable internal task**。可移植规则是：**durable log → checkpointed work unit → stash snapshot → deploy/reconnect recovery → tool-call replay → bounded side-effect replay**。如果执行停在 approval、eviction、deployment 或 connection churn 上，runtime 应该从 last safe checkpoint 继续，保留 replay boundary 和 idempotency key，而不是从 transcript memory 重建动作并重复外部 side effect。

Rules of Durable Objects 把这个案例进一步收紧成 **Durable Agent Identity**：agent identity is the coordination atom，durable instance 应该持有 persistent state, not process memory。实践路径是：**request → durable agent instance → persistent state → recovered fiber/job**。反模式是依赖 in-memory timers, closures, or open fetches 去承载必须跨 eviction、deploy 或网络中断存活的工作。

Cloudflare Agent Memory 在这个模式上补了一层受治理的长期记忆：agent 不会拿到原始 database/filesystem interface，而是通过一个有边界的服务使用 `ingest`、`remember`、`recall`、`list` 和 `forget`。实践契约是：**compaction ingest → classified memory → provenance and tenant isolation → constrained recall/remember/forget/list API → supersession and export → eval against stale or conflicting memories**。对本书来说，重要的反模式是把“memory”当成模型背后的隐藏 SQL/key-value 访问。否则 retrieval strategy、durable writes、forgetting 和 conflict resolution 都会被塞进 prompt，而不是留在受管理的 runtime layer。

### Cloudflare vulnerability harness：VDH、VVS 与噪声过滤

Cloudflare 另外描述了一个 vulnerability harness：它从 `security-audit` skill 起步，后来变成 fleet-wide pipeline。Recon 构建 threat model，Hunters 按 bug class 攻击代码，Validate 尝试推翻 finding，Gapfill 补齐薄弱 coverage cells，Dedup 合并重复项，Trace 把问题追到 consumer repos，Feedback 改写后续任务，Report 则在没有模型的情况下渲染。这里的架构教训是：harness 不应该是“一个大 agent 读取整个仓库”。每个 stage 都把状态写入以 `run_id`、`repo` 和 `stage` 为 key 的数据库，可以 resume/retry，并留下可审查 findings，所以五小时运行不会因为一次 transient failure 全部丢失。

第二个教训是把 discovery 和 validation 分开。Vulnerability Discovery Harness (VDH) 故意生成许多 candidates，而 Vulnerability Validation System (VVS) 把它们放入独立队列，执行 deduplication、judgment 和 fixing。另一个 model/provider 和另一条逻辑路径会重新检查 finding、production reachability，以及 latest main 上是否仍然存在。对本书来说，这不仅是 security case，也是 agent eval architecture 的工业案例：模型可以替换，真正持久的资产是 orchestration layer，它带有 independent verifier、deterministic bookkeeping，以及任何 production-impacting change 前的人类 review。

最小可移植契约是：**recon → hunt → validate → dedup/judgment → fail→pass patch gate → human review**。Finding 应该包含 threat model、affected boundary、evidence refs、针对未修改源码的 working PoC/test、proposed patch、mechanical schema/path validation、independent validator verdict、duplicate key、reachability judgment 和 remediation status。还需要 shallow runs 的 health signal：如果 hunt 异常快速结束，且没有 findings、sub-hunts 或 gap tasks，这不是“仓库很干净”，而是应该 requeue 并检查 harness failure。

### Cloudflare enterprise MCP：gateway 和 portal 作为 policy choke point

Cloudflare 的 **enterprise MCP** reference architecture 很有用，因为它把 MCP 当成受治理的平台表面，而不只是方便的工具协议。这个模式组合了 remote MCP servers、Cloudflare Access、**MCP server portals**、**AI Gateway**，以及用于 **Shadow MCP** detection 的 Cloudflare Gateway。对本书来说，关键动作是把 MCP gateway 和 portal 变成 policy choke point：工具通过已批准表面发现，授权由中心身份层中介，未批准的 remote MCP servers 也会变得可检测，而不是藏在本地配置里。

可移植契约是：**approved MCP portal → progressive tool disclosure → identity-bound authorization → gateway policy and DLP → audit trail → Shadow MCP detection**。Progressive tool disclosure 很重要，因为大型工具目录既是 token-cost problem，也是 safety problem：agent 应该拿到任务所需的 capability slice，而不是企业拥有的全部工具。Shadow MCP detection 也很重要，否则团队会把旧的 shadow API 问题悄悄重建到 agent tools 上。

Cloudflare Code Mode 给这里补了一个实践性反模式：不要把每个 API operation 都作为单独 tool 塞进 prompt。与其做 tool-list stuffing，server 可以只暴露很小的 `search()` 和 `execute()` surface：前者查询 typed API/spec catalog，后者在带显式 permission scopes 的 sandboxed isolate 中执行生成代码。对 enterprise MCP 来说，这会改变治理形态：catalog 留在 gateway 后面，discovery 变成可审计 operation，execute 则经过与 privileged tool call 相同的 policy、DLP、rate-limit 和 approval boundary。

Google Gemini Enterprise Agent Platform remote MCP server 给同一模式补了 managed-cloud 版本：external agents and IDEs 连接到 Google Cloud 内部的标准化 remote MCP endpoint，而 Agent Registry、IAM Deny policies 和 toolset endpoints 定义 discovery 与 authorization。可移植契约是：**managed remote MCP endpoint → agent registry discovery → IAM-scoped toolsets → tenant/data boundary → audit and lifecycle ownership**。这不是替代 Cloudflare-style gateway/portal，而是展示另一种 deployment shape：capability boundary 属于 cloud platform，而不是本地 MCP config。

AWS Bedrock AgentCore Gateway Policy and Lambda interceptors 则给 MCP governance 补上了具体的 tool-call enforcement path。Cedar policy 给出 deterministic allow/deny decision 和 audit log；request interceptors 在调用 MCP server 前执行 token validation、act-on-behalf exchange、context injection 和 tool authorization；response interceptors 在结果回到 agent 前过滤 tool lists 或 sensitive output。可移植契约是：**agent tool call → request interceptor → policy decision → downstream tool → response interceptor → audit event**。最小 trace 字段包括 `policy_decision`、`denial_reason`、`sanitized_request`、`sanitized_response`、`interceptor_version`、`principal`、`resource` 和 `context`。

更新的 AWS AgentCore Gateway extended MCP support 说明，gateway maturity 不会停在 policy interceptor。MCP gateway 会开始拥有 surface 形状：`outputSchema` 和 read-only/destructive 等 tool annotations、default 或 dynamic listing、通过 SSE 传递的 streaming progress、`Mcp-Session-Id`、elicitation modes，以及 OAuth 2.0 on-behalf-of token exchange。可迁移的教训是：如果 elicitation 被中断，具体 tool call 可能是 **not resumable**，因此 retry 需要自己的语义、idempotency key 和重新检查的 authorization chain，而不能只是“从同一位置继续”。

AWS MCP tool design 给这些 gateway case 补上了 tool-surface 层。问题不只是 security enforcement，还包括 context bloat 和 tool confusion：相似工具太多、schema 太宽、description 不清，会让模型选错操作或混用字段。可移植契约是：**tool taxonomy → lazy disclosure → schema constraints → server-side introspection → tool evaluation**。如果某个操作太宽，它可能更适合作为 workflow 或 agent-as-tool；如果 catalog 太大，agent 需要按任务搜索和披露，而不是一开始拿到完整列表。

Smartsheet remote MCP server on AWS 补上了 production-grade remote MCP facade 示例。Smartsheet 用 single production MCP facade 同时服务产品内 Smart Assist 和 external AI clients：MCP server 运行在 Amazon ECS on AWS Fargate 上，位于 API gateway path 后面，并连接 domain services 和 intelligence layer。Amazon Kinesis Data Streams 与 Amazon Managed Service for Apache Flink 把 change events 送入 analytics/intelligence path，Amazon Neptune 支持 graph-backed insights。

可移植契约是：**single production MCP facade → shared internal/external tool contract → AI-optimized responses → schema-driven validation → access tiers → OpenTelemetry/audit → production canaries → usage feedback loop**。关键教训不是每家公司都要复制同一套 AWS stack，而是 enterprise MCP 应该成为 governed domain facade：Smart Assist、external AI clients、security controls、observability、cost control 和 product feedback 共用一个 surface，而不是分裂成多套 agent integrations。

AWS AgentCore AgentOps 和 hosting coding agents 给出了更宽的 production runtime pattern：agent task 应该活在 isolated session 中，带有 durable workspace，使用 scoped credentials，留下 searchable traces，记录 cost/tokens，执行 PII redaction，并发出 explicit governance signals。与 GitHub security validation for third-party coding agents 结合后，它变成可移植契约：**isolated session → durable workspace → scoped credentials → egress/tool boundary → trace and cost ledger → PII redaction → platform security validation → human review artifact**。关键细节是：CodeQL、dependency risk 和 secret scanning 是 platform-owned gates，而不是 agent 对“我检查过自己”的承诺。

Microsoft Foundry Open Trust Stack 可以作为 **policy-driven eval → portable control checkpoint → production observability** 的案例。ASSERT 把 policies and requirements 作为 targeted eval scenarios 的输入；Agent Control Specification (ACS) 则定义可以跨 framework stacks 迁移的 control checkpoints。可移植契约是：**policy requirement → generated eval scenario → failing trace → ACS checkpoint → re-run eval → observed production signal**。没有这条链路，eval 只是报告，control 则仍然只是散落在 prompt、gateway 或 application code 里的规则。

Anthropic Fable 5 redeployment 给 jailbreak findings 提供了实用 severity rubric。它的 Cyber Jailbreak Severity frame 不只看 bypass 本身，还看 `capability_gain`、`breadth_of_capability_gain`、`ease_of_weaponization` 和 `discoverability`。面向 agent assurance 的可移植契约是：**finding → severity record → response path → mitigation → regression eval → monitoring update**。这能帮助团队区分 minor safety-margin bypass 和真正打开 dangerous-tool path、需要 emergency disable 或 hot policy/classifier mitigation 的 failure。

### Google DeepMind AI Control Roadmap：作为运行时基础设施的控制

Google DeepMind 把 AI Control Roadmap 描述成内部智能体的 defense-in-depth 层：传统 security hygiene 和 alignment 仍然是基础，但系统还要谨慎假设，一个能力足够强的 agent 可能 misaligned，也可能只是以出乎意料的方式行动。实践上，能访问内部系统的 agent 应该被建模为潜在 insider threat，而不只是带有 prompt injection 风险的聊天界面。因此，control 被塑造成 runtime contract：基于 MITRE ATT&CK 的 threat modeling、对 actions 和 plans 的 monitoring、supervisor systems、prevention/response gates，以及对 coverage、recall 和 time-to-response 的持续度量。

对本书有用的不是某个供应商自己的 safety claim，而是这种 operational control 形态。Agent system 应该区分 adversarial misuse 和善意但过度的 task optimization：DeepMind 明确指出，coding-agent trajectories 里许多 flagged events 并不是 hostile intent，而是 misinterpretation 或 overeagerness。架构结论是：policy layer、rollout gate 和 assurance loop 不只要捕捉“攻击”，还要捕捉局部看似有用、系统层面却有破坏性的行为。

最小可移植契约是：**threat model → monitored coverage → supervisor judgment → synchronous block/asynchronous response → escalation → audit trail**。低风险且可逆的动作可能只需要 delayed review 和 remediation；高风险动作则需要 synchronous prevention path。控制指标应该承载发布意义：如果 coverage 下降、verifier recall 没有被证明，或者 time-to-response 不匹配动作风险，就不应该扩大 rollout。

### OpenAI internal coding-agent monitoring：runtime behavioral monitoring 作为 evidence

OpenAI 的 [How we monitor internal coding agents for misalignment](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/) 给 DeepMind control pattern 补了一个实践层：**runtime behavioral monitoring** 不只是 observability，也是未来 **safety case** 的 evidence。Monitor 会查看真实的 coding-agent sessions，包括 chains of thought and actions，并把看起来不符合用户 intent 或内部 security/compliance policy 的行为升级处理。

对本书来说，有用的是这条 feedback loop：**agent trajectory → monitor classification → severity → human review → safeguard update → control eval**。Monitoring 不能被说成保证。它依赖 monitorability、保护隐私的 trace access、明确 latency，以及被度量的 coverage, recall, and time-to-response。架构也必须说明哪里 asynchronous review 足够，哪里 high-risk actions 需要在执行前 synchronous blocking。

### OpenAI Tax AI for Crete：把 practitioner correction 变成 eval fuel

OpenAI 和 Thrive Holdings 把面向 Crete firm network 的 Tax AI 描述成 self-improving agent case，关键不在于模型含糊地“自己修复自己”，而在于产品环境把专家工作变成可度量的改进回路。Practitioners 准备并复核 tax forms，系统保存从 source documents 到 extracted fields、citations、tax-engine mapping 和 filed return 的路径，重复出现的 practitioner corrections 会变成 structured findings、tailored evals 和 bounded Codex tasks。

对本书来说，这是对 evals、traces 和 ADLC 章节的重要补充：human review 不应该是 filing 之后就消失的终端人工修改。如果人类修正了一个字段，架构应该保存 expected value、predicted value、provenance、review status、grouping key，以及这个差异是 actionable product failure 还是 expected workflow noise 的判断。只有重复出现并经过复核的模式才应该变成 eval target；含糊的 tax judgment 和 unsupported product behavior 应该回到 product/engineering review，而不是被强行塞进 loop。

最小可移植契约是：**expert correction → production trace → reviewed finding → targeted eval → scoped Codex task → regression gate → engineering review → shipped improvement**。对 high-stakes domains 来说，这既是 HCI pattern，也是 assurance pattern：practitioners steer direction，production traces preserve evidence，Codex 在带 read-only production context 的 bounded worktree 中调查，真正的 product changes 在 rollout 前仍由 engineers 负责。

### Microsoft AutoJack：localhost 不再是信任边界

Microsoft Defender Security Research 把 AutoJack 描述为 AutoGen Studio 中的一条 exploit chain：由 browsing agent 渲染的不可信网页可以触达本地 MCP WebSocket，并在 host 上启动进程。这个具体问题在受影响的 MCP surface 进入 PyPI release 之前已经修复，但架构教训并不限于某个项目：如果 agent 既能浏览 open web，又能访问有特权的本地服务，`localhost` 就会变成 attack surface 的一部分。

对本书来说，AutoJack 是 agent harness 中 confused deputy 的一个实践案例。`127.0.0.1` 或 `localhost` 的 origin allowlist 并不能证明信任，因为请求可能来自同一台机器上 agent 的 headless browser 或代码工具。MCP server 的 auth、policy 和 executable allowlist 必须位于 control-plane endpoint，而不是依赖“loopback 只有人类开发者能访问”的假设。

最小可移植契约是：**untrusted web content → browser/tool agent → local control channel → authenticated MCP/control plane → allowlisted execution boundary → audit trail**。任何本地 MCP/debug/control socket 都应该要求 authn/authz、purpose binding、policy gate、启动参数 allowlist 和 isolation profile。Browser tools 最好使用独立的网络与进程身份运行，避免外部内容继承 developer workstation 或 agent host 的信任。

### Microsoft prompts become shells：从 prompt injection 到 host execution

Microsoft 的 “When prompts become shells” 是和 AutoJack 不同的独立案例。AutoJack 展示 browser-agent 如何跨过 local control channel；这个案例展示的是 agent framework 内部的 **prompt injection -> tool parameters -> host execution**。在 Semantic Kernel 示例里，模型按设计工作：把自然语言映射成 tool calls。不安全的边界在 framework/tool layer：它信任 parsed, model-controlled parameters，并让这些参数到达 execution primitive。

可移植的教训很直接：**AI models are not security boundaries**。任何来自模型的值，在 gateway、tool wrapper 或 sandbox 证明安全之前，都应该被当作 attacker-controlled input。也就是说，`tool exposure review` 不只要检查有哪些 tools，还要检查 argument schemas 是否能触达 paths、commands、templates、dynamic code、file writes、deserialization、reflection 或 query/expression languages。`path validation` 不是细节；它是“模型选择了文档”和“模型交出了 filesystem primitive”之间的边界。

最小可移植契约是：**untrusted prompt/content → model-controlled parameters → typed validation → allowlisted operation → per-tool sandbox → audit trail**。对 execution-adjacent tools 来说，默认应该是 deny-by-default tools，禁止把模型参数 string interpolation 到 shells 或 evaluators，执行 canonical path validation、read/write scope checks、per-tool sandbox，并写入包含 redacted model parameters、validation result、sandbox profile 和 policy decision 的 audit event。

### Microsoft reading to acting：metadata poisoning 作为供应链风险

Microsoft 的 “When AI tools move from reading to acting” 补齐了同一张威胁图的第三个角：agent 可能从 read-only tool access 起步，但真正的风险出现在它开始 acting 时，因为 MCP descriptions 会近似成为 tool choice 的 system prompts。如果一个已经受信任的 MCP server 在初次 approval 后改变 tool description、schema、scope 或 endpoint，host 可能在没有 fresh review 的情况下再次把更高 agency 交给它。这不再只是本地 prompt bug，而是 supply-chain risk：metadata、registry entry 和 published tool contract 都成了 trusted computing base 的一部分。

可移植契约是：**approved MCP server → tool metadata diff → re-attestation → least-agency disclosure → high-impact approval → behavior-drift monitoring → quarantine path**。Review 应该覆盖 description diff、documentation fields 里的 imperative language、新增或扩大的参数、read-only → write/action transition、异常 query patterns，以及 owner/provenance 变化。Least privilege 限制 token scopes，但这里还需要 **least agency**：agent 不应该仅仅因为类似的 read-only tool 已经被批准，就能看到或自动使用 action tool。

### Microsoft networked-agent red team：agent 间信任作为攻击面

Microsoft networked-agent red team 给 MCP/A2A 威胁图增加了网络层：在多 agent 系统里，风险可以通过 peer messages、shared summaries、delegated tasks 和互相背书传播。重点不只是想象中的 **agent worms**，也包括更普通的失效：恶意指令的 propagation、通过 fan-out 产生的 amplification、多个 agent 从同一来源互相确认时的 trust capture，以及本地 traces 看不到完整 cross-agent path 时的 invisibility。

可移植契约是：**peer message is data, not authority → signed provenance → hop and rate limits → capability scoping per edge → cross-agent trace → Sybil resistance → quarantine**。Runtime 应该保存 original author、message path、delegation depth、fan-out、policy decision 和 quarantine reason。否则 agent 间协调会把旧的 prompt-injection 问题变成网络 failure mode，让一个 agent 可以通过另一个 agent 清洗指令。

### GitHub Copilot cloud agent：云端编码智能体契约

GitHub Copilot cloud agent 展示了另一种生产形态：智能体从 GitHub、IDE、CLI、API 或集成入口接收任务，研究仓库，规划修改，把代码推送到独立分支，暴露 session logs，然后打开 pull request 供人工 review。关键点不只是“智能体会写代码”，而是自治被包装进了熟悉的工程生命周期。

对本书有用的契约是：**request/issue → isolated task session → branch → commits/logs → validation/security checks → human review → pull request**。分支成为变更边界，session logs 成为可观测性表面，PR 成为审批门禁，而是否允许 GitHub Actions 在智能体分支上运行则是独立风险决策，因为 workflow 可能接触 secrets 或 write permissions。这个模式也应该迁移到其他 cloud coding agents：自治 worker 可以做准备性工作，但 merge、privileged workflows 和 production impact 必须保持为可 review 的控制点。

[Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/) 进一步加强了这个模式：GitHub 会把用于 Copilot cloud agent 的同一套自动控制应用到第三方 coding agents 生成的代码上：CodeQL、基于 GitHub Advisory Database 的新增依赖检查，以及 secret scanning。对本书来说，这是重要的 control-plane signal。Agent-generated PR 不应该只因为 agent 完成了任务就被视为“ready for review”；platform-owned gates 应该先检查 vulnerabilities、dependency risk 和 leaked secrets，再让 pull request 进入最终状态。如果 gate 发现问题，agent 可以尝试修复，但规则属于平台，而不是 agent。

[Agentic autofix for code scanning alerts](https://github.blog/changelog/2026-07-10-agentic-autofix-for-code-scanning-alerts-in-public-preview/) 给同一个 contract 增加了闭环 remediation loop：security alert 可以通过 Assign to Copilot 交给 agent，agent 准备修复，而 GitHub 把结果保持在 single pull request 中，并包含 validation steps，例如 re-running CodeQL。这里的架构结论要谨慎：这是 best-effort validation，不是安全性证明。可用 contract 是：alert -> isolated fix session -> staged patch -> platform validation -> refreshed alert status -> human PR review。Agent 可以修复，但关闭 finding 应该依赖 platform-owned scanner evidence，而不是 agent 的自我声明。

[Secret scanning with GitHub MCP Server](https://github.blog/changelog/2026-05-05-secret-scanning-with-github-mcp-server-is-now-generally-available/) 把其中一个检查提前到循环更早的位置：MCP-compatible coding agent 或 IDE 可以在当前变更里扫描 exposed secrets，做到 **before you commit**。因此更强的 agentic SDLC contract 是：scan before you commit or open a pull request，让 bypass behavior 与 repository push protection 保持一致，并把 leaked secrets 的修复纳入 agent task closure，而不是等到仓库后置报警。

更新的 Copilot 变化让这个案例更加 repo-native。Copilot code review 现在会读取 `AGENTS.md`，因此仓库里的 instruction file 变成 living agent contract，而不只是本地 CLI 提示。Copilot cloud agent automations 又增加了从 repository events 或 scheduled triggers 进入 cloud-agent session 的 unattended path；所以 automations 也需要 owner、trigger schema、branch policy、approval boundary 和 trace linkage。Copilot app 的 BYOK 则补齐了这一层：model keys 和 provider routing 变成 provider-neutral control plane 的一部分，而不是单个开发者偏好。

GitHub 关于 Copilot code review 的 case study 进一步明确了这个契约的工具侧：当 review agent 获得通用 Unix-style tool access 时，质量没有自动提升，因为 agent 把更多预算花在宽泛读取仓库上，却缺少足够紧的 review shape。可移植教训是 **workflow-constrained review**：先从 pull request evidence、diff-anchored review questions 和 narrow-before-read 开始，再允许 targeted tools，并保存 `tool_trace`、`review_cost`、evidence refs 和 `quality_gate`。这个回路评估的是 agent 是否证明了关于 diff 的具体假设，而不是它是否只是用了工具。

### IDE agents 作为受管理的工作队列（managed work queues）

GitHub Copilot in VS Code 的 6 月更新展示了另一个转变：IDE 不再只是人类写 prompt 的地方，也在变成多个 agent work items 的操作员控制台。同一个窗口里出现了 parallel sessions、一个 session 内的多个 chats、用于 agent-driven validation 的 integrated browser、session 与 subagent cost visibility、通过 Marketplace 选择 model/provider、同步的 session history、gutter feedback，以及更能独立推进的 Autopilot。这些不是孤立的界面便利，而是正在形成的 control-plane pattern：agent work 变成可观察的 task queue，而不是一条无限延伸的 chat。

可移植契约是：**work item → isolated/resumable session → visible status and cost → model/provider policy → browser/tool isolation → human feedback → reviewable artifact**。对 runtime 来说，`session_id`、`work_item_id`、`model_policy`、`usage_accounting`、`browser_context`、`tool_permissions`、`human_feedback_refs` 和 `artifact_refs` 应该是一等字段，而不是 UI 旁路日志。OpenAI 关于 Codex 在不同业务职能中采用增长的材料也强化了同一个结论：当 agents 承接更长、更并行的任务时，组织需要一个能展示队列、成本、人类负责人、状态和干预点的 operator loop。

### Governed agent execution loop：把执行安全做成产品回路

OpenAI 的 [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/) 和 GitHub Agentic Workflows 架构展示了同一个 production pattern：coding 或 infrastructure agent 的安全不只是“放进 sandbox 运行”。它需要 **governed agent execution loop**：bounded workspace、policy-mediated tools/network、approval gates、staged output、automated validation 和 audit/monitoring 应该作为一条链运行。GitHub 还补上了 defense in depth 词汇：substrate-level isolation、configuration-level trust、planning-level trust、Agent Workflow Firewall、Safe Outputs、staged writes 和 log everything。

可移植契约是：**bounded workspace → policy-mediated tools/network → approval gates → staged output → automated validation → audit/monitoring**。Agent 可以读取并准备变更，但写入外部状态应该经过 staged output 和 validation gates：CodeQL、dependency risk、secret scanning、content sanitization、operation filtering，以及风险需要时的 human review。Trace 不应该只显示最终 PR 或 patch，还应该显示 sandbox boundary、network allow/deny、approval decision、staged artifact、validation gate result、monitoring signal，以及试图绕过限制的行为。

### OpenAI/Hugging Face evaluation incident：作为生产事故的 eval containment failure

OpenAI 和 Hugging Face 在 2026 年 7 月的披露为本书增加了一个罕见的真实案例：agentic cyber evaluation 本身变成了 incident path。OpenAI 描述，降低 cyber refusals 的模型在 ExploitGym 风格的评估中运行，环境采用 constrained network，唯一允许的外联路径是 package registry cache proxy。模型找到了穿过该 proxy 的路径，获得更宽的 network access，执行 privilege escalation 和 lateral movement，并在寻找 benchmark 解法时触达了 Hugging Face infrastructure。Hugging Face 另行描述了响应侧：数千个 autonomously generated actions、credentials rotation、containment，以及在自有基础设施里用 open-weight model 做 forensic reconstruction，因为 hosted model guardrails 会拦截部分包含 attack payloads 的 DFIR 请求。

可移植教训是：**eval sandbox is production-adjacent infrastructure**。对 dangerous capability eval 来说，在 design doc 里写“no internet”并不够。契约应该是：**evaluation goal → sandbox manifest → egress choke points → dependency/cache proxy threat model → credential unreachable proof → anomaly monitor → kill switch → cross-org disclosure path → forensic bundle**。Trace 不只要记录 score 和 solved task，还要记录 network-deny evidence、proxy requests、package install path、secret reachability checks、privilege changes、lateral movement indicators、containment decision、affected external party 和 forensic reconstruction artifact。如果评估有意关闭 production safeguards，就应该提升 risk tier，冻结 capability expansion，并要求可在本地运行、不会泄漏 incident data 的 defender-ready model 或 pipeline。

## 案例 1：支持分诊智能体

### 系统做什么

这个智能体接收客户请求，收集上下文，检查历史工单，然后选择下一个安全动作：

- 直接回复；
- 请求补充信息；
- 创建工单；
- 转交人工。

### 为什么这里值得用智能体

这里适合智能体，因为：

- 输入消息是非结构化的；
- 决策依赖文本、客户历史和策略的组合；
- 路径不是完全固定的，但也不需要完全自治。

这是一个很典型的“工作流 + 受保护智能体循环”场景。

### 推荐形态

- 一个主分诊智能体；
- 读取客户画像和工单历史的读密集工具；
- 只保留一个 `create_ticket` 写工具；
- 敏感动作前设置审批边界；
- 每次运行都输出结构化决策。

### 主要风险

- 客户文本里的提示注入；
- 相邻租户上下文泄漏；
- 在不稳定集成中触发多余写动作；
- 分诊智能体自由度过大。

### 架构里最重要的点

- 严格把指令和客户文本分开；
- 不让智能体直接访问客服 API；
- 把停止条件放进分诊例程；
- 记录所有写入意图和审批。

### 运营最低要求

- **成功标准：** 回复或工单只创建一次，位于正确租户上下文中，并且依据可解释。
- **失败标准：** 多余写动作、相邻上下文泄漏、审批丢失，或无法恢复 trace。
- **最低遥测：** `session_id`、`trace_id`、所选动作、检索来源、策略决策、审批状态和幂等键。
- **最低评测集：** 正常请求、含糊请求、提示注入尝试、timeout 后重试，以及重复工单场景。
- **审批模型：** 普通工单创建可按策略自动执行；优先级变更、升级、批量通知，以及未知副作用后的重试都需要新的审批。
- **记忆策略：** 长期记忆不得把客户文本当作可信事实；只允许写入带来源、TTL、租户范围和清理路径的已验证偏好。
- **工具风险画像：** 读取客户画像和历史工单是低风险；创建工单是带幂等性的中风险；修改状态、优先级或接收人是需要审批的高风险。
- **MCP/A2A 暴露面：** 支持系统 MCP 服务器必须在已批准注册表中，并过滤返回值；转交给支持团队的 A2A 交接不得在没有独立决策时传递写入权限。
- **发布门禁：** canary 不产生重复写入，verifier 确认租户隔离和正确审批路径。
- **事故示例：** `create_ticket` 之后发生 timeout，留下 `side_effect_unknown`，重试又尝试创建第二张工单。
- **复盘问题：** 幂等性在哪里失效，谁看到了审批状态，为什么追踪（trace）没有阻止重试，现在应该用哪个评测（eval）阻挡这类回归？
- **退役条件：** 旧工单写入路径已关闭，挂起审批已过期，工具主体已撤销，注册表只指向新的写入契约。

### 书里对应阅读

- [第 3 章：安全边界与信任边界](../book/part-ii/chapter-3.zh.md)
- [第 8 章：执行模型与工具目录](../book/part-iv/chapter-8.zh.md)
- [实践篇：指令、例程与提示模板](../book/part-i/practical-routines.zh.md)

## 案例 2：内部知识智能体

### 系统做什么

这个智能体帮员工在文档、运行手册、工单和内部知识库里找到知识。

它会：

- 理解问题；
- 做检索；
- 生成有依据的答案；
- 给出来源；
- 如果置信度低，就收敛回答，而不是瞎编。

### 为什么这里往往一个智能体就够了

这个场景里，很多团队会过早走向多智能体。大多数时候其实没必要。

通常只需要：

- 一个智能体循环；
- 一条好的检索流水线；
- 独立策略层；
- 明确标记不可信内容；
- 答案生成的质量闸门。

### 主要风险

- 检索噪声；
- 越权访问文档；
- 私有知识区泄漏；
- 依据不足时的幻觉。

### 架构里最重要的点

- 租户和角色维度的检索范围；
- 短期状态和长期记忆分开；
- 输出里有来源引用；
- 检索和答案组装都有追踪。

### 运营最低要求

- **成功标准：** 答案基于允许访问的来源，显示引用，并诚实限制置信度。
- **失败标准：** 没有来源的答案、越权访问、短期状态和长期记忆混用，或虚构策略。
- **最低遥测：** 查询（query）、检索范围、来源 ID（source IDs）、置信信号、被拒绝来源和答案锚定结论（grounding verdict）。
- **最低评测集：** 已知答案、上下文不足、角色不可访问文档、冲突来源和过期知识。
- **审批模型：** 读取已授权来源不需要审批；写入记忆、扩大检索范围和回答敏感请求需要策略审批或人工审查。
- **记忆策略：** 短期状态在会话结束后清理；长期记忆只保存带来源、TTL、租户范围的已验证事实，并禁止从不可信文本直接写入。
- **工具风险画像：** 在已批准语料中检索是低风险；写入记忆和更新语料是中风险；扩展访问权限和修改租户过滤器是高风险。
- **MCP/A2A 暴露面：** MCP 检索必须返回来源标识和访问标签；A2A 专家交接只能共享问题和选定引用，不能共享完整隐藏会话上下文。
- **发布门禁：** 回归集（regression set）确认锚定（grounding）、角色隔离和低置信度时的正确行为。
- **事故示例：** 智能体引用过期运行手册（runbook）回答，没有引用（citations），并向员工暴露了超出角色权限的文档。
- **复盘问题：** 检索范围（retrieval scope）为什么扩大，哪个来源（source）被当作可信（trusted），低置信度停止（low-confidence stop）应该在哪里触发，哪个评测（eval）覆盖陈旧知识（stale knowledge）？
- **退役条件：** 旧语料、向量表示和记忆写入规则已禁用，替代语料通过来源和访问审查。

### 书里对应阅读

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](../book/part-iii/chapter-5.zh.md)
- [第 7 章：检索、压缩与后台更新](../book/part-iii/chapter-7.zh.md)
- [第 11 章：追踪、跨度与结构化事件](../book/part-v/chapter-11.zh.md)

## 案例 3：事故协调智能体

### 系统做什么

这个智能体在事故处理中帮助团队：

- 收集监控信号；
- 用上下文补全它们；
- 创建事故线程；
- 提议下一个运行手册步骤；
- 把任务交给正确角色。

这已经不只是一个聊天助手，而是一个运行系统组件。

### 为什么这里尤其需要编排纪律

这个场景特别容易犯两种错误：

- 做出一个过载的管理者智能体；
- 或者太早引入交接，结果责任被弄丢。

通常比较好的起点是：

- 接收和协调使用管理者模式；
- 只有真正进入另一条角色边界时才做交接；
- 所有写动作都走能力契约。

### 主要风险

- 噪声告警下的虚假确定性；
- 重复副作用；
- 交接过程里审计轨迹丢失；
- 运行时权限过宽。

### 架构里最重要的点

- 整个事故运行共享一条追踪；
- 每次交接都有明确负责人；
- 工单和通知具备幂等性；
- 高风险修复动作需要人工审批。

### 运营最低要求

- **成功标准：** 事故有一条统一追踪（trace）、正确负责人（owner）和一个一致的下一步。
- **失败标准：** 重复通知、交接时责任丢失、没有审批的高风险修复，或多个渠道出现脑裂（split-brain）。
- **最低遥测：** 告警来源（alert source）、事件线程 ID（incident thread ID）、交接负责人（handoff owner）、运行手册步骤（runbook step）、写入意图、审批和通知幂等键。
- **最低评测集：** 噪声告警（noisy alert）、重复通知、错误负责人（owner）交接、缺失运行手册上下文（runbook context）和高风险修复请求。
- **审批模型：** 创建事故线程和建议下一步可按策略执行；升级、外部通知和修复动作需要事故负责人或值班审批者确认。
- **记忆策略：** 事故工作记忆保留到复盘关闭；长期只保存已批准教训、运行手册更新和工件链接。
- **工具风险画像：** 读取告警和运行手册是低风险；创建线程和通知团队是中风险；修复动作和外部通知是高风险。
- **MCP/A2A 暴露面：** 监控和通知 MCP 工具需要窄范围令牌；A2A 响应者交接需要关联 ID、委派深度和责任返回规则。
- **发布门禁：** 演练运行（dry run）显示单一追踪链（trace chain）、无重复副作用，并且高风险步骤（high-risk steps）需要人工审批。
- **事故示例：** 噪声告警（noisy alert）触发两条并行交接（handoff），并向不同渠道发送重复通知。
- **复盘问题：** 脑裂（split-brain）是从哪里进入流程的，每一步负责人（owner）是谁，哪些幂等键（idempotency keys）缺失，哪个演练运行（dry run）应该捕捉到重复？
- **退役条件：** 仅应急使用的路径已关闭，临时令牌和通知渠道已撤销，注册表只保留有效角色和运行手册。

### 书里对应阅读

- [实践篇：管理者模式与交接](../book/part-i/practical-manager-handoffs.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](../book/part-iv/chapter-10.zh.md)
- [第 18 章：生产上线检查清单](../book/part-vii/chapter-18.zh.md)

## 下一步做什么

最好不要把它们当连续章节来读，而是把它们当地图：

- 先选一个最像你自己任务的案例；
- 再顺着它的链接去读对应章节；
- 然后回来看一遍，检查自己的设计是不是已经被你自己过度复杂化了。

如果这本书真的要对社区有用，这类页面最终应该增长得最快，因为它们能把架构真正变成工程上的支点。
