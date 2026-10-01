# OpenWrt v2：冻结审查集的时间资格诊断（非标签结果）

**日期：**2026-10-01  
**阶段：**Gate A 后、Gate B 前  
**状态：**探索性诊断；不修改已冻结的 76 个审查单位，不产生人工标签、方法输出或效果指标。

## 目的

v2 的候选登记规则要求 CVE 明示提交可由固定 release tag 到达。该规则保证提交在 Git 历史中可达，但不保证提交是在该稳定发布线的维护窗口中引入，也不保证其变更仍能直接映射到 tag 中的 package source。

本诊断只回答两个机械问题：

1. 冻结集中的 commit 与对应 release tag 相差多久？
2. Git 可达性之外，commit 所修改的路径在 tag tree 中是否仍具有可直接比较的 blob 状态？

它**不**回答 CVE 是否适用、修复是否有效、目标是否暴露，也不把路径/版本缺失解释为 `not_affected`。

## 输入与可复现来源

- 冻结审查集：`data/openwrt-v2-label-sample.csv`（76 release-target 单位，38 个 `(commit_sha, cve_id)` cluster）。
- 官方只读 Git 缓存：`https://github.com/openwrt/openwrt.git`；本地 bare cache 使用 `--filter=blob:none`，并获取官方 tag 与 `openwrt-22.03`、`openwrt-23.05`、`openwrt-24.10` 分支。
- 机械输出：
  - `artifacts/openwrt-v2-frozen-sample-temporal-diagnostic.json`
  - `artifacts/openwrt-v2-review-tag-path-preflight.json`

对带签名的 annotated release tag，时间读取显式解引用为 `v<release>^{}` 所指 commit 的 committer timestamp；不会把 tag message 或签名文本当作时间。

## 发现 1：Git 可达性把大量历史提交带入了冻结集

为避免将相同 cluster 的两个 target 重复计入，时间统计按 `(commit, CVE, release)` 折叠为 38 个单位：

| commit 到 tag 的时间间隔 | cluster-release 数 | 比例 |
|---|---:|---:|
| <= 180 天 | 9 | 23.7% |
| 181–365 天 | 3 | 7.9% |
| 1–3 年 | 3 | 7.9% |
| > 3 年 | 23 | 60.5% |

时间间隔中位数为 **1,483 天**；最小值为 1 天，最大值为 2,212 天。

这解释了为何冻结集包含例如较早 Linux kernel、dnsmasq、BusyBox 和 Dropbear 维护历史：稳定 release tag 包含完整祖先历史，所以“commit 可达”不是“该 release 的维护期修复”的同义词。

该统计是**候选生成规则的结构性限制**，不是任一 CVE 的标签或补丁保留结论。

## 发现 2：祖先关系不足以提供 release-source 证据

对 38 个 cluster-release 单位，所有 38 个 commit 都是相应 tag 的祖先，符合原登记规则。随后机械列出每个 commit 的变更路径，并比较 commit tree 与 tag tree：

| 机械状态 | 结果 |
|---|---:|
| commit 是 release tag 祖先 | 38 / 38 |
| commit 全部变更路径仍存在于 tag tree | 9 / 38 |
| commit 全部变更路径的 tag blob 与 commit blob 完全相同 | 9 / 38 |
| 所有变更路径总数 | 710 |
| 路径仍存在于 tag tree | 72 |
| tag blob 与 commit blob 相同 | 43 |

这些数值**不能**被解释为 patch 被删除或 CVE 已修复/未修复：路径可因 package 升级、目录重排、补丁折叠或后续重构而变化。它们只说明祖先关系不能替代 release-tag package source、recipe、patch series 和 CVE 描述之间的逐项证据链。

## 探索性后继设计检查（不替换 v2）

为判断将来独立预注册的样本框是否可能更有证据密度，额外检查了全部 9,537 条 target-presence 原始候选中“commit 时间不早于该稳定线 `.0` tag”的机械子集：

| 子集 | 原始 release-target 行 | `(commit,CVE)` cluster | 首次 target 单位 | 唯一 CVE |
|---|---:|---:|---:|---:|
| 所有显式 CVE、维护窗口后 | 105 | 19 | 37 | 16 |
| 上述且本地已有 CVE JSON | 87 | 15 | 29 | 12 |
| 仅含 `backport/cherry-pick` 语言、维护窗口后 | 56 | 12 | 24 | — |

这只是对未来可行性的探索，不能事后替换 v2 的 76 单位。它表明在当前 24 release、两 target、显式 CVE commit 的边界内，即使不用回补语言限定，维护窗口后的固定 JSON 目标单位也只有 29，仍低于 v2 Gate B 的 30 个二元标签门槛。因此，若 v2 最终未通过 Gate B，合理下一步不是挑选“更容易”的条目，而是另立、独立预注册的样本总体与外部验证策略。

## 可继续检验、但尚非创新主张的研究线索

一个可能的研究问题是：

> 对 patch-carrying distribution 的 release-level CVE 审计，**branch-local temporal eligibility** 与 tag package-source evidence 是否应作为版本匹配之前的必要前提，从而减少无法判定的人工审查负担？

它不能被称为创新，除非后续证明：

1. 与已有版本适用性分析、patch 定位、自动 backport 和 stable-patch 分类工作存在明确任务差异；
2. 在独立、预注册且足够大的 release population 上，能得到独立人工证据标签；
3. 时间资格规则不会仅因事后剔除困难样本而改善结果；
4. 结果报告所有 `insufficient_evidence`，并以 cluster 而非重复 target 单位计推断。

## 当前决定

- v2 冻结样本保持不变；不根据上述诊断替换、删除或重抽样。
- Gate B 仍未通过；禁止评分代码、效果指标和投稿结论。
- 接下来继续补全冻结样本的本地、官方 source evidence 审查，同时并行完成上述线索的近邻文献审计；若 v2 失败，再决定是否建立独立 v3，而不是事后扩张 v2。
