# 轨迹策略场景

状态：可执行的配套示例，契约范围经过有意限制。

源文件：

- `agent_runtime_ref/trajectory.py`
- `tests/test_trajectory_policy.py`
- `docs/companion/examples/run_trajectory_policy_scenarios.py`

## 运行

在所选工作树的根目录执行：

```bash
/path/to/agent-arch/.venv/bin/python \
  docs/companion/examples/run_trajectory_policy_scenarios.py
```

这里的 `/path/to/agent-arch` 表示包含 `.venv` 的主克隆目录；运行器从当前工作树导入代码。输出是键已排序、场景顺序固定的 JSON。

## 预期决策

| 场景 | 决策 | 规则 | 原因 |
| --- | --- | --- | --- |
| `destination_fingerprint_mismatch` | `deny` | `destination-binding` | `value_binding_mismatch` |
| `cumulative_limit_exceeded` | `deny` | `daily-amount-limit` | `cumulative_limit_exceeded` |
| `required_predecessor_missing` | `deny` | `destination-confirmed-first` | `required_predecessor_missing` |
| `required_approval_missing` | `approval_required` | `transfer-approval` | `required_approval_missing` |
| `trusted_trajectory_allowed` | `allow` | `trajectory.all_rules` | `all_rules_satisfied` |

在第二个场景中，当前值 `40` 本身低于限制 `100`，但可信快照中已经累计了 `70`，因此总和以关闭方式拒绝。第一个场景只比较规范化指纹，不处理原始账户信息。加法使用局部精确 Decimal 契约：小数位最多 6 位、最大值 `999999999999.999999`、精度 32，并对舍入和算术异常启用陷阱；它不依赖可变的全局 Decimal 上下文。

运行器不接收调用方提供的请求指纹。它根据动作、租户和主体、预期历史引用与版本、序列号、窗口、策略标识与版本、排序后的重要指纹以及计数器增量计算指纹。正向场景把 `ApprovalRecord` 绑定到该值；任何绑定字段发生变化，都不能复用之前的审批。

每个场景都会调用 `TelemetryEmitter.emit` 并发送 `trajectory_policy_decision` 事件。`event.payload` 中的所有值都是字符串。事件只包含指纹和计数器状态，不包含原始目标、账户信息、工具参数或秘密。

标识符和引用必须通过有长度限制的小写 ASCII 白名单，完整载荷在发送前还会再次校验。这是一项结构性保护，并不是语义秘密扫描器：快照提供方仍负责确保形式上合法的标识符、引用和哈希输入中不含秘密。

为防止形式上合法的请求破坏强制审计事件，契约将每个请求和快照限制为最多 16 个指纹和 32 个计数器。对象创建时会执行这些限制，允许的最大集合仍能放入遥测字符串字段。

## 实现边界

`evaluate_trajectory_policy` 是纯确定性函数。它显式接收当前 `TrajectoryRequest`、冻结的 `TrajectorySnapshot` 和 `TrajectoryPolicy`；模型上下文和压缩摘要从不作为历史来源。`integrity=verified` 只是可信快照提供方给出的断言，教学评估器本身不验证该断言的签名或来源。历史为 `None` 时以 `history_missing` 拒绝；类型错误的映射或对象以 `history_malformed` 拒绝，并且不会把原始对象写入决策或遥测。

此示例**不提供**分布式事务一致性、锁、历史版本的比较并交换、动作与计数器的原子更新、策略检查与外部副作用之间的竞态保护、持久追加日志或崩溃恢复。它也没有连接到 `AgentRuntime`。在生产环境中，外部组件必须从可信日志取得完整快照，实施版本同步以及锁或事务，原子记录决策和动作结果，并在故障后执行恢复或核对。
