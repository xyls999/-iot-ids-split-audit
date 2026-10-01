# OpenWrt 发布溯源适用性：扩展近邻文献审计（进行中）

**目的：**在继续 OpenWrt v2 前，检验“patch/release evidence 用于 CVE 适用性”是否已被更广泛的软件工程工作直接完成。本文不会以仅摘要命中的论文支撑“创新”结论。

## 当前结论：不能宣称“首个 patch-based affected-version 方法”

2022 年的 *Precise (Un)Affected Version Analysis for Web Vulnerabilities* 已明确提出从漏洞修复 patch 抽取漏洞逻辑，并在多个软件版本中判断 affected/unaffected。即使其对象是 Web 应用而非发行版 package，它已经否定了任何泛化的“以 patch 判断版本适用性是新颖的”表述。

因此，如果 OpenWrt 方向继续，唯一可检验的差异应限于：

```text
签名/冻结的发行 release-target package inventory
+ distribution recipe、feed commit 和 tag-contained patch evidence
+ 发行 package-CVE 的可审计 evidence/VEX-style verdict（含 insufficient_evidence）
+ 与名称/版本映射相同候选集的受控比较
```

这仍然只是候选差异，不是新颖性结论。

## 已全文核验

### Decan et al., “Back to the Past – Analysing Backporting Practices in Package Dependency Networks” (IEEE TSE, 2021)

- DOI: `10.1109/TSE.2021.3112204`
- 官方开放 PDF: https://orbi.umons.ac.be/bitstream/20.500.12907/25365/1/TSE-2021.pdf
- 本地只读抽取：`research-os/.cache/literature/back-to-the-past.pdf`（不入库的缓存）

**实际任务。** 论文研究 Cargo、npm、Packagist、RubyGems 四个 package distribution 中低 major train 的 backport 实践（第 1 页摘要、研究问题 RQ1–RQ6）。作者把“在较低 major train 发生的新 release”作为 backport 代理，而不是在发行 package source 中验证 patch 是否保留。

**漏洞部分。** RQ6 使用 Snyk 在 2020-04-12 提供的漏洞报告；因该数据不包含 Cargo/Packagist 的漏洞报告，RQ6 仅分析 npm 和 RubyGems（第 9 页）。它使用报告的 affected/fixed releases 研究不同 major train 是否受益，而非人工 adjudicate 固定 release-target package 是否确实受某 CVE 影响。

**与本研究的边界。** 该文已经覆盖“package ecosystems 的 backport 实践、低版本 train 和漏洞修复”这一大背景。因此不能把这些概念本身当贡献。全文没有报告 OpenWrt、target manifest、distribution recipe/feed、tag-contained patch retention、release-target-CVE 三元证据链或 `insufficient_evidence` 标注。

## 高风险近邻：已确认摘要，全文仍需核验

下列论文会影响新颖性；在取得全文前不得做“未覆盖”断言。

| 工作 | 已确认的摘要级事实 | 对 OpenWrt 方案的风险 | 当前处理 |
|---|---|---|---|
| *Precise (Un)Affected Version Analysis for Web Vulnerabilities* (ISSTA 2022), DOI `10.1145/3551349.3556933` | 从 patch 提取漏洞逻辑，在版本间精确判断 affected/unaffected；报告 34 CVE、299 versions。 | **高**：直接相邻于 patch-based version applicability。 | ACM PDF 的自动请求被 Cloudflare 拒绝；必须取得全文后再界定其是否处理 distribution backports。 |
| *Locating the Security Patches for Disclosed OSS Vulnerabilities with Vulnerability-Commit Correlation Ranking* (ESEC/FSE 2021), DOI `10.1145/3460120.3484593` | PatchScout 对 CVE–commit 相关性排序，并报告跨 branch 的 patch deployment study。 | **中高**：可能覆盖 CVE patch association 与分支部署，但摘要未显示 release package adjudication。 | 全文待核验。 |
| *Automated patch backporting in Linux* (ESEC/FSE 2021), DOI `10.1145/3460319.3464821` | FixMorph 自动把 mainline patch 迁移到旧 stable Linux；350 patches。 | **中**：覆盖 patch 生成，不是发布物适用性。 | 不可包装为“自动回补”创新。 |
| *Enhancing OSS Patch Backporting with Semantics* (FSE 2023), DOI `10.1145/3576915.3623188` | TSBPORT 用语义/PDG 迁移 Linux security patches，1,815 对 patch。 | **中**：同样覆盖 patch migration，不是 release verdict。 | 不可包装为“自动回补”创新。 |
| *PatchScope: LLM-Enhanced Fine-Grained Stable Patch Classification for Linux Kernel* (2025), DOI `10.1145/3728944` | 对 stable patch 的具体 LTS merge status 预测。 | **中高**：接近 branch-local eligibility，但任务是预测应合入哪个 LTS，而非审计已发布 package 的 CVE 状态。 | 需全文核验数据与评价差异。 |

### 访问限制记录

2026-10-01 对 ACM/机构 PDF 的非交互式请求返回 Cloudflare `403`；这不是“论文不存在”或“未覆盖”的证据。没有绕过访问控制，也不会用搜索摘要替代全文结论。

## 由当前证据产生的研究要求

如果 v2 的标注和后续独立数据能够继续，论文必须明确把主张收窄为以下可否证伪问题：

> 对已经发布的 OpenWrt release-target package，能否用可审计 recipe/commit/tag-patch 证据输出受限的 applicability verdict，并量化相对于名称/版本匹配的错误候选减少，同时完整报告无法判定的案例？

不可声称：

- 自动生成或迁移 security backport；
- 首个 patch-based affected-version 分析；
- 自动定位 CVE 修复 patch；
- 真实设备的可利用性、暴露面或攻击成功率。

## 下一步

1. 取得高风险近邻的全文后，按任务、数据、标签、证据来源、baseline、评价逐项复核；
2. 完成 OpenWrt v2 第二轮盲审与分歧 adjudication；
3. 仅当 Gate B、近邻差异和独立验证同时成立时，才讨论方法和投稿。否则将其作为可行性/数据质量负结果保留，并另起独立预注册，而不是在 v2 内按结果扩样。
