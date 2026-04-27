# 智能体系统的 Memory Eval Patterns

智能体系统里的 memory 问题，往往和普通 retrieval 不一样。很多错误不会在单次请求里暴露，而是在一串 runs、profile updates 与 background writes 之后才出现。

因此，memory layer 最好被单独评估，而不是指望它被一般性的 eval dataset 顺带覆盖。

## 1. 为什么 memory evals 应该单独存在

即使 overall task success 看起来不错，memory design 也可能悄悄退化：

- profile 被写入了不必要或有风险的事实；
- stale preference 持续影响后续回答；
- system 记住了错误的东西；
- 长会话里没能取回关键事实；
- background compaction 扭曲了记录的原始含义。

这就是为什么 memory layer 需要独立的 evaluation logic。

## 2. 哪些错误类型应该被覆盖

一个最小可用的 memory eval set 通常至少应覆盖：

- incorrect write；
- missing write；
- unsafe write；
- stale retrieval；
- false retrieval；
- profile contradiction；
- over-retention；
- deletion failure。

即使没有大型 benchmark，这个集合也已经很有价值。

## 3. 短期记忆应该评估什么

Short-term memory 通常应检查：

- 是否保留了对话中的关键上下文；
- 是否避免了不必要的跨轮带入；
- 对 noisy user turns 是否足够稳健；
- 在含糊情境下是否会正确澄清。

这里的问题常常不在 storage 本身，而在 runtime 如何判断什么值得继续携带。

## 4. 画像记忆和长期记忆应该评估什么

Profile memory 与 long-term memory 需要更严格的检查：

- 这个事实是否值得被写入；
- 是否被写进了正确的 memory class；
- provenance 能否说清；
- 该记录能否安全地删除或修订；
- stale record 是否仍然影响当前 answer path。

这里尤其要重视 contradiction 与 retention hygiene 的评测。

## 5. Long-horizon memory 必须跨 runs 检查

一个很常见的错误是：只用单个 isolated prompt 检查 memory quality。

但真实问题往往出现在多步序列里：

- 在 run 1 写入偏好；
- 在 run 4 错误取回；
- 在 run 6 被冲突事实覆盖；
- 到了 run 9，stale profile 仍在起作用。

因此，memory evals 更适合设计成 multi-run scenarios，而不是 single-turn checks。

## 6. 一个 memory eval case 里适合记录哪些字段

一个最小可用的 eval record 往往包括：

- `memory_class`
- `write_expected`
- `retrieval_expected`
- `allowed_to_persist`
- `expected_provenance`
- `revision_behavior`
- `deletion_behavior`

这样更容易区分“回答不好”与“memory semantics 被破坏”。

## 7. 为什么这也关系到 safety

Memory evals 不只是为了 personalization，它们也与 safety 密切相关：

- system 会不会在没有权限时写入 sensitive data；
- risky state 会不会被保留过久；
- 会不会混淆 user-specific data；
- harmful memory path 能否被快速停止；
- persistent records 的 provenance 能否被证明。

如果没有这一层，很多 memory incidents 会被误看成“模型行为古怪”，而忽略真正的问题在于 record lifecycle。

## 8. 它和一般 eval loop 的关系

Memory evals 不会替代 [主 eval 章节](../book/part-v/chapter-13.zh.md)，而是增加一个额外维度：

- 普通 offline evals 检查 task success；
- memory evals 检查跨 runs 的 state quality；
- online signals 帮助发现 drift；
- incidents 与 postmortems 负责更新 memory-specific cases。

换句话说，memory layer 应该像 tools 和 policy 一样，明确进入 regression discipline。

## 9. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 是否有单独的 write / no-write cases？
- retrieval 是否跨长序列 runs 被检查？
- 是否包含 stale profile 和 contradiction cases？
- persistent records 的 provenance 是否被评估？
- deletion 与 revision cases 是否被覆盖？
- memory incidents 会回流到 eval dataset 吗？

## 下一步做什么

- [Eval Dataset Schema 与 Grading Contract](eval-schema.zh.md)
- [Memory Record 与 Retrieval Contract Schema](memory-retrieval-schema.zh.md)
- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](../book/part-iii/chapter-5.zh.md)
- [第 7 章：检索、压缩与后台更新](../book/part-iii/chapter-7.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
