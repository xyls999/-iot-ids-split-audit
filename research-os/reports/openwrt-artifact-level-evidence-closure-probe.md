# OpenWrt artifact-level evidence closure：机械探针（非漏洞标签）

**状态：**探索性方法学探针；不产生 CVE `affected`/`not_affected` 标签，不替换任何冻结样本，不计算方法效果。

## 问题

PatchScout 等工作可从 source branch 判断 patch deployment；AFV 可在源码版本收集 backport patch。对于已发布的 OpenWrt release package，另一个更窄的问题是：

> remediation commit 是 release tag 的祖先，是否已经足以作为“该 release package source 保留 remediation”的可复核证据？

本探针不试图证明漏洞状态，只检查 Git ancestry 与 release tag tree 的**精确 blob 证据**是否一致。

## 输入

- 扩展 paired-cohort 侦察：62 个 non-kernel pre/post target pair、32 个 `(commit,CVE)` cluster；
- 官方 OpenWrt tag source 与官方 checksum-verified release manifest；
- pair 的定义已经在 `reports/openwrt-expanded-paired-cohort-scout-report.md` 说明；
- 机器可读输出：`artifacts/openwrt-paired-cohort-closure-probe.json`。

## 机械检查

对每个 pair 的 remediation commit 列出其相对父提交的所有变更路径，并对每条路径比较：

```text
commit tree blob
vs.
post-release tag tree blob
vs.
pre-release tag tree blob
```

定义的 **strict exact-blob retention** 仅表示 remediation commit 的每个变更路径在 post tag 具有相同 blob。它是一种低成本、可审计的直接证据便利信号，**不是** patch 是否语义保留、CVE 是否修复、或漏洞是否可利用的结论。后续版本升级、patch 折叠、目录调整都可能使正确修复不满足该严格条件。

## 结果

| 检查 | target pair（n=62） | 独立 `(commit,CVE)` cluster（n=32） |
|---|---:|---:|
| post tag 包含 remediation commit | 62 | 32 |
| pre tag 不包含 remediation commit | 62 | 32 |
| strict exact-blob retention | 50 | 26 |
| 至少一个变更路径 blob 精确保留 | 54 | 28 |
| 没有任何变更路径 blob 精确保留 | 8 | 4 |

严格 check 无法闭合的 6 个 cluster 出现在：

- 18.06.2 Dropbear 的两组 CVE-linked backport commit；
- 23.05.3 dnsmasq `version 2.90` commit 所关联的 CVE-2023-50387 与 CVE-2023-50868。

这四个“没有任何精确 blob 保留”的 cluster 不是 `affected`、不是 `not_affected`，也不是对维护者行为的否定。它们只是证明：从 `commit ∈ tag ancestry` 到“release tag 中有一个可直接复核的相同 remediation artifact”存在不可自动跳过的证据间隙。

## strict-fail lineage spot check（仍非自动标签）

对全部 6 个 strict-fail cluster 的 post-tag package lineage 进行只读追溯后，严格 blob 不一致并不等于 remediation 缺失：

- **18.06.2 Dropbear。** `8bb9d053…` 将 `020-Wait-to-fail-invalid-usernames.patch` 加入 package tree；该 patch 的 blob `593dca…` 在 `v18.06.2` 中仍完全相同。随后 `97fddb2f…` 是同一 CVE-2018-15599 backport 的维护线提交，但只修改 Makefile；再后的 `61323d22…` startup 修复使 Makefile blob 改变。因此该例需要跨 commit lineage，而不是“每个 remediating commit 的全部 blob 都相同”。同一提交文本提及 CVE-2018-15473，但固定 CVE 记录的产品是 OpenSSH；这正是 package identity 审查必须独立于 commit-message CVE 抽取的例子。
- **23.05.3 dnsmasq。** `875822f283…` 明确把 package 升至 upstream 2.90 以取得 CVE-2023-50387/CVE-2023-50868 修复。post tag 的 recipe 仍为 `PKG_UPSTREAM_VERSION:=2.90`；其后 `03a3a729…` 仅回补两个 2.90 后 DNSSEC 修复，`853b638f…` 重置 `PKG_RELEASE`。这些后续 commit 改变了 recipe/patch blob，所以 strict exact check 失败，但 release-source lineage 仍可被人工闭合。

因此，strict exact-blob retention 更适合作为 **needs-lineage-review** 触发器，而不是二元 verdict 或效果指标。该检查的价值必须以后续独立审查的可复核性/弃权率来证明，不能从本次六例外推出算法性能。

## 含义

该结果支持继续检验、但尚未证明下列假设：

```text
release applicability audit 应区分：
  Git ancestry evidence
  与
  tag package-source / patch-retention evidence。

当两者未严格闭合时，正确输出可以是
  insufficient_evidence / needs_manual_lineage,
而不是把 ancestor 当成确定修复证据。
```

这与 AFV、PatchScout、Patch2Vuln 的已覆盖任务不同的可能性，在于它关注已发布 distribution artifact 的**证据可复核性与弃权边界**，而非漏洞逻辑分析、patch 排名、分支 deployment 或二进制 root-cause reconstruction。

但它仍不是创新证明。若后续人工追溯发现所有 strict-fail case 都能用简单版本升级立即闭合，或独立审查不产生稳定差异，则该假设不应继续发展成论文方法。

## 下一步（仍不写评分代码）

1. 对 6 个 strict-fail cluster 预先固定 tag recipe、package source 与后续 commit lineage，判断它们是版本升级、patch 折叠、revert，还是无法闭合；
2. 将 source evidence 的层级与最终人工作为分离记录，避免用同一 feature 自动生成标签；
3. 只在高风险近邻继续审计后，决定该“closure”是否有足够独立价值建立新的预注册 cohort。
