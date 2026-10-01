# OpenWrt 扩展 paired-release cohort：官方数据可得性与规模侦察

**状态：**探索性侦察；不是 v2 扩样、不是 v3 预注册、没有新增人工标签、没有方法分数或论文结论。

## 问题

v2 的固定样本只取“已含 remediation commit”的 release，因此已裁决二元标签全为 `not_affected`，不能估计 recall。后继研究只有在标签前配对修复前/后 release，才可能检验 package-release-CVE applicability。

本侦察只问：公开官方 archive 和 Git 历史是否提供足以设计独立 paired cohort 的规模？

## 官方 archive 可得性

对三个额外结束稳定线的所有最终数字 release，下载且以同目录官方 `sha256sums` 验证 target manifest：

| 稳定线 | 最终数字 release | target | 经 checksum 验证 manifest |
|---|---:|---|---:|
| 18.06.x | 10 | x86/64、ar71xx/generic | 20 |
| 19.07.x | 11 | x86/64、ath79/generic | 22 |
| 21.02.x | 8 | x86/64、ath79/generic | 16 |

合计 58 个官方 manifest，全部验证通过。18.06/19.07 的 x86 manifest 命名为 `openwrt-<release>-x86-64-generic.manifest`，而不是新 release 的 `...-x86-64.manifest`；未来的 collection 程序必须显式支持该历史命名差异。

临时、忽略 Git 的证据缓存：`research-os/.cache/openwrt-historical-scout/`。它不构成已冻结数据集。

## paired rule（仅为侦察）

对每个 explicit-CVE commit、package 与 target，在同一稳定线内：

```text
post = package/target 存在且首次包含该 commit 的正式 tag
pre  = post 前 package/target 存在、且不包含该 commit 的最近正式 tag
```

所有基础 commit 均来自 OpenWrt 官方 Git；candidate package 仍是 commit subject prefix 与 target manifest package 的精确匹配。这个规则没有查看人工标签。

## 原始规模与 kernel 结构问题

只看 18.06/19.07/21.02，规则得到：

```text
207 target pair
104 (commit,CVE) cluster
63 CVE
```

但其中 166 pair 是 `kernel`。同一 release 中 x86/64 和 ar71xx/ath79 的 kernel manifest version 不同，且一个“kernel” commit 可能对应多个内核线。若把它们与普通 package 相同处理，会把 target-specific kernel instance 混入 package-level release verdict。

因此，**仅为可行性统计**，扩展 tally 排除了 `kernel`，理由是对象模型不一致，而不是因为标签结果。任何未来协议若保留这个排除，必须在数据冻结前写明，并将 kernel 作为独立研究对象或分层，而不能事后挑掉。

## 可用于独立后继设计的规模信号

在非 kernel pair 中，且只计 CVE JSON 已存在于当前固定 cvelistV5 snapshot 的 CVE：

| 来源 | pair | `(commit,CVE)` cluster |
|---|---:|---:|
| 18.06/19.07/21.02 archive scout | 33 | 17 |
| 已冻结 22.03/23.05/24.10 population 的探索性 pair | 29 | 15 |
| 合并侦察（六条稳定线） | **62** | **32** |

62 个 pair 在两侧都被审查时对应 124 个 release-target package-CVE 单位、24 个 CVE；涉及 BusyBox、dnsmasq、Dropbear、e2fsprogs、Lua、opkg、ppp，覆盖六条稳定线。target 计数为 x86/64=32、ar71xx/generic=6、ath79/generic=24；目标架构差异必须在未来分析中分层，不得当作独立安全事件。

完整机器可读 tally：`artifacts/openwrt-paired-cohort-expanded-scout.json`。

## 对“创新点”的影响

该侦察表明**数据规模不再是立即否决条件**：如果独立预注册，新 cohort 有机会满足 100+ review units 与 30+ cluster 的规模需求。

但它没有证明创新。特别是全文审计的 Patch2Vuln（arXiv:2605.06601）已使用 Ubuntu old/new package pair 与人工真值。它不使用 source provenance、并且任务是 binary root-cause reconstruction，但这意味着“Linux distribution 的 old/new pair”本身不能构成贡献。

要继续，论文主张必须收窄为：

```text
公开 OpenWrt release-tag recipe / explicit-CVE commit / tag-patch 证据
→ 可审计 package-release-CVE applicability verdict（含 insufficient_evidence）
→ 与仅名称/版本映射相同候选总体的受控比较
```

并且需要全文排除 PatchScout、PatchScope、Precise (Un)Affected Version Analysis 等高风险近邻的直接任务重叠。

## 当前决定

- 不把 62 pair 写入 v2，不改变 v2 的 76-unit 冻结样本；
- 不开始 A/B 评分代码；
- 扩展 cohort 是**值得进入独立预注册设计阶段的候选**，不是已发现、已验证或可投稿的创新点；
- 下一轮研究应先完成高风险近邻的全文审计和一个明确的 source-provenance evidence model，再决定是否创建独立 v3 Gate A。
