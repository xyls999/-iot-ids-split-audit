# N-BaIoT 第三轮重放与稿件 claim lint

## 1. 第三轮 order-invariance replay

### v3 失败结果

将 v2 packet 的顺序和 tier 顺序反转后，两个审查者在 20 个 cells 上达到 **17/20** 一致。分歧集中在：

- gap-only observation 是否算 explicit LODO result；
- random-row observation 在 T0 下是否仍可称 conditional；
- packet 以 flat observations 存储，缺少 tier-scoped evidence。

机器可读记录：

`research-os/artifacts/nbaiot-v3-order-replay-adjudication.json`

该失败被保留，不能被丢弃或与成功轮次平均。

### v4 schema 修复

在不修改 claim、数据、模型或窗口的前提下，将 packet 改为显式 `tier_evidence` 字段，并冻结：

- T0：对 device-independent claim，random-row alone 始终 `not_identifiable`；
- T1：common support + random-row 为 `conditional`；
- T2：ordered-window + comparison context 为 `conditional`；
- T3：显式 LODO metric/bounded gap 为 `identified`，protocol-only 为 `conditional`。

同时保持 packet/tier 顺序反转。两名独立审查者在 16/16 cells 完全一致。

机器可读 packet：

`research-os/artifacts/nbaiot-blinded-review-packets-v4-explicit-tiers.json`

机器可读裁决：

`research-os/artifacts/nbaiot-v4-explicit-tier-adjudication.json`

## 2. Claim lint

新增工具：

`research-os/tools/lint_esst_claims.py`

对 methods/report 初稿扫描 `affected`、`not_affected`、artifact safety、数据泄漏、重大创新、投稿录用等高风险词，并要求其处于明确的否定/边界上下文。

验证结果：

```text
findings: 18
unsafe: 0
exit code: 0
```

该 lint 不是语义证明，只是投稿前的机械越界检查。

## 3. 结论

```text
v3 order replay：暴露 schema defect
v4 explicit-tier replay：16/16 agreement
claim lint：通过
```

因此 protocol 的可重复性得到更强支持，但仍不等价于高水平创新、独立真值或录用保证。
