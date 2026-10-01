# OpenWrt v2：人工证据审查抽样协议

## 目的

从 v2 的 source-pinned candidate registry 中机械地选出人工证据审查单位，用来检查 Gate B 是否能获得至少 30 个二元标签；该协议不选择“看起来容易证明”的回补案例。

## 候选资格

一个原始候选单位必须同时满足：

```text
commit message 有规范 CVE ID
+ commit 可由固定 release tag 到达
+ commit subject 的 package hint 与同 release、同 target 的 manifest package 精确匹配
+ 该 CVE 的 JSON 已固定到 cvelist commit 5657707bc397bc80237e9aea2d7e01994208f1b2
```

这只是审查资格，不代表 package identity、patch retention、affected range 或漏洞适用性已成立。

## 分析与抽样单位

- 依赖 cluster：`(commit_sha, cve_id)`；同一 cluster 出现在多个 release 不能当成独立安全事件。
- 人工审查单位：`(commit_sha, cve_id, release, target)`。
- 对每个 cluster 和 target，先保留版本序最早的一个 release；它是该明确 CVE commit 在固定总体内、且 package 已出现在该 target manifest 的最早可审查 release。
- 同一 cluster 可在 x86/64 和 ath79/generic 分别拥有一个审查单位；这两个标签需在报告中按 cluster 关联，不能独立计数为两个安全事件。

## 固定审查集规则

为使方法 B 的证据来源在审查前已确定，审查集不从全部历史 CVE commit 随机抽取，而是使用下列**完整的、规则定义的子总体**：

```text
候选资格
+ commit message（subject 或 body）含 backport、cherry-pick 或 cherry pick
```

这表示提交者明确使用了回补语言；它不是“已经回补成功”、也不是 `not_affected` 标签。

1. 对每个 `(commit_sha, cve_id, target)`，保留版本序最早的合格 release 单位。
2. 不再按结果挑选 36 条：将这个子总体中的**全部单位**写入 `openwrt-v2-label-sample.csv`。
3. 若同一 cluster 在两个 target 均出现，两个 target 单位都保留，但最终统计仍以 `(commit_sha, cve_id)` cluster 为依赖单元。
4. 所有单位都必须保留到报告中，包括之后被判为普通版本升级、证据不足或 package identity 不成立的单位；不得以标签结果删除或替换。

## Gate B 的解释

- Gate B 的 30 个二元标签只计 `affected` 或 `not_affected`；`insufficient_evidence` 保留且不冒充负例。
- 至少 10 个唯一 `(commit, CVE)` cluster 必须在二元标签中出现。
- 若 72 个预先抽取单位仍无法得到 30 个二元标签，v2 失败并停止于可行性阶段；不得基于标签结果挑新的 72 个单位。
- 在 Gate B 通过前，不编写方法 A/B 评分代码，不计算效果指标。
