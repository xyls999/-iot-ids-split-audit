# OpenWrt v2：回补语言人工审查集预检

**日期：**2026-10-01  
**状态：**已固定待审查单位；没有人工标签、方法输出或效果结果。

## 为什么不是从全部历史 CVE commit 随机抽样

全部 Git 历史登记中含有大量正常版本升级、后来被替换的历史 patch 以及与最终 tag 当前版本无关的旧 commit。随机抽样会让绝大部分样本根本不具备“发布溯源能改变版本匹配判断”的可能性。

因此本审查集的来源条件在看任何标签前固定为：

```text
固定 release tag 可达的 commit message 显式包含规范 CVE ID
+ 同一 commit message 含 backport / cherry-pick / cherry pick
+ subject package hint 与同 release、同 target 的 manifest package 精确匹配
+ CVE JSON 已固定到 cvelist commit 5657707bc397bc80237e9aea2d7e01994208f1b2
```

这只是“维护者用了回补语言”的待审查总体；它不等于 CVE 仍受影响，也不等于 patch 在最终 release 中有效。

## 固定审查集

| 项目 | 数量 |
|---|---:|
| 含回补语言的 target-present 原始行 | 1,420 |
| 唯一 `(commit, CVE)` cluster | 41 |
| 因 CVE JSON 未能固定而排除的 cluster | 3 |
| 最终人工审查单位 | 76 |
| 最终唯一 cluster | 38 |
| x86/64 单位 | 38 |
| ath79/generic 单位 | 38 |

审查集文件：

```text
data/openwrt-v2-label-sample.csv
```

原始回补语言候选（含尚未固定 JSON 的记录）保留在：

```text
data/openwrt-v2-explicit-backport-candidates.csv
```

## 审查顺序和规则

每个审查单位需要依次验证：

1. frozen manifest 的 package/version；
2. fixed CVE JSON 的组件与 affected range/描述；
3. fixed release tag 中该 package Makefile、patch 或 commit 的实际内容；
4. commit/patch 是否真的提供与该 CVE 有关的 release-specific 修复；
5. 缺任何一环时标 `insufficient_evidence`，而非猜测。

人工标签只能是：

```text
affected
not_affected
insufficient_evidence
```

同一 `(commit, CVE)` 在两个 target 的标签保留为两个 target 单位，但统计上必须按 cluster 关联。

## Gate B 仍未通过

Gate B 的 `>= 30` 二元标签与 `>= 10` 二元 cluster 目前都是 **0**，因为审查尚未开始。若这 76 个预先固定单位无法达到门槛，v2 终止；不得根据审查结果重选更多“更容易”的案例。
