# OpenWrt 发布溯源候选：三个关键近邻的全文三角审计

**目的：**判断 OpenWrt 的 pre-fix/post-fix release package-CVE 方向是否有除“已有方法换生态”之外的可辩护贡献。只使用已取得全文的结论；未读论文不得被写成不重叠。

## 全文来源

| 工作 | 一手全文 | 核验状态 |
|---|---|---|
| Shi et al., *Precise (Un)Affected Version Analysis for Web Vulnerabilities* (ASE 2022), DOI `10.1145/3551349.3556933` | ACM HTML：https://dl.acm.org/doi/fullHtml/10.1145/3551349.3556933 | 全文已读 |
| Tan et al., *Locating the Security Patches for Disclosed OSS Vulnerabilities with Vulnerability-Commit Correlation Ranking* (CCS 2021, PatchScout), DOI `10.1145/3460120.3484593` | ACM PDF：https://dl.acm.org/doi/pdf/10.1145/3460120.3484593?download=true | 全文已读 |
| David & Gervais, *Patch2Vuln* (arXiv:2605.06601, 2026) | https://arxiv.org/pdf/2605.06601 | 全文已读 |
| Ghebremichael et al., *VERIPORT: Automated and Verified Patch Backporting at Scale* (arXiv:2606.22704, 2026) | https://arxiv.org/pdf/2606.22704 | 全文已读 |

本地抽取均位于 `research-os/.cache/literature/`，只作可重现阅读缓存，不提交仓库。

## 逐项事实

### 1. AFV：版本适用性与 backport 收集已经被直接研究

AFV 的任务是从 PHP Web 漏洞 patch 提取“vulnerability fingerprint”，在其它源码版本判断 `affected`、`unaffected` 或 `unknown`（第 2–3 节）。它：

- 对 patch commit 收集 explicit cherry-pick、相同 code diff、相同 commit title/message 的其它分支 patch（§3.2）；
- 若版本已被 patch commit 覆盖、没有危险函数，则判为 unaffected；完全相同指纹则判 affected，其余为 unknown（§3.4）；
- 构建 34 CVE、299 个版本、5,002 CVE-version pair 的人工真值；affected 由 PoC 验证，unaffected 由人工确认危险函数缺失、已修复或不可触发（§4.1）；
- 以 V-SZZ、ReDebug、V0Finder 为 baseline，报告 98.15% precision、85.01% recall（§4.2–4.3）。

**后果：**不得声称“首个 patch/backport-aware affected-version analysis”“三值版本适用性”或“从 patch history 降低 CVE false positive”。这些高层主张已被 AFV 覆盖。

**边界差异：**AFV 是 PHP Web 应用的源码/危险函数静态分析，真值依赖 Docker、PoC 和运行调试；它不处理 signed release manifest、发行 package recipe/feed、target-specific inventory 或已构建 release package 的 patch retention。

### 2. PatchScout：稳定分支 patch deployment 与三类状态已经被直接研究

PatchScout 首先对 CVE 排序候选 commit，测试集为 685 CVE；之后对 5 个 OSS 项目、225 CVE、83 个 stable/release branch 构成 3,735 个 CVE-branch pair 的 deployment study（§6–7）。

对于没有直接找到 patch 的 branch pair，作者人工区分：

```text
not affected
out of maintenance before disclosure
affected + maintained but not patched
patched but PatchScout did not locate patch
```

（§7.1）。最终收集 2,195 个 CVE-branch patch 对，发现 150 个 maintained-but-not-patched pair，且报告 CVE/NVD 漏记 affected version 的情况（§7.1–7.2）。

**后果：**不得将“CVE × stable/release branch 的 patch deployment、backport status 或 patched/unpatched/not-affected 标签”包装成新颖性；PatchScout 已经完成该层研究。

**边界差异：**PatchScout 的分析对象是 OSS source branch，不是正式发行物。它不验证某 tag 发布物的 manifest package 实例、recipe/feed 解析、patch 是否被 release package source 保留，也没有 package-name/version baseline 或 target-specific release verdict。

### 3. Patch2Vuln：Linux distribution old/new package pair 与人工真值已经存在

Patch2Vuln 以 Ubuntu `.deb` old/new package pair 为单位，用本地 ELF/Ghidra/Ghidriff 证据重建安全更新的 root-cause 类别；分析阶段明确禁止读取 CVE、advisory、source patch、changelog 和 Web（第 1、4 页）。它评估 20 个安全 pair 与 5 个负对照，使用私有 source-patch/binary-function truth 做人工裁决（第 1、6–8 页）。

**后果：**不得将“Linux distribution package pair”“离线 old/new package 比较”或“人工 release update ground truth”称为首创。

**边界差异：**Patch2Vuln 故意做 binary-only root-cause reconstruction，不输出公开 source-provenance-supported package-release-CVE status，也不检验 recipe/tag patch 对 verdict 的证据闭合。

### 4. VERIPORT：verified backport、evidence chain 与版本范围纠错也已被覆盖

VERIPORT 对 npm/PyPI dependency package 的 advisory affected range 生成并验证每个版本的 backport；它为 package、vulnerability、upstream fix 和 backport 生成 evidence chain，并以 exploit oracle 验证 backport 阻断漏洞、以 functionality oracle 验证不破坏行为（摘要、§1、§4）。其 BackportBench 实验处理 128 个任务，另引入 393 npm task 的 CVEPatchBench；论文也通过执行 exploit 找到被 advisory 错误列为 affected 或漏列的版本（摘要、§5）。

**后果：**不得把“evidence chain”“backport verification”“纠正 affected version range”或“在 package release 之间构造验证链”作为新颖性。VERIPORT 的公开结论远强于纯 Git-history heuristic。

**边界差异：**VERIPORT 为尚未发布的 npm/PyPI 旧版本**生成并运行验证** backport；本研究边界禁止执行代码/PoC/漏洞利用，也不生成 patch。若 OpenWrt 候选继续，它只能审计已发布、target-specific distribution artifact 的公开 source evidence 是否闭合，且其输出必须允许 `insufficient_evidence`，不能假装达到 VERIPORT 的 exploit-verified 含义。

## 覆盖矩阵

| 维度 | AFV | PatchScout | Patch2Vuln | OpenWrt 候选可保留部分（尚未证明创新） |
|---|---|---|---|---|
| CVE 到 patch 关联 | 收集多分支 patch | 核心任务 | 隐藏 source patch，仅作 oracle | 只能使用公开、固定 OpenWrt commit/patch |
| backport / stable branch | 明确收集 cherry-pick/diff/message | 直接测 deployment/backport | Ubuntu update pair 可能含回补 | 不能把该概念当贡献 |
| affected/unaffected/unknown | 直接输出 | 人工状态分层 | 安全/负对照与 unknown | 不能把三值本身当贡献 |
| old/new package pair | 无 | 无 | 直接使用 | 不能把 pair 本身当贡献 |
| 发布 manifest/recipe/target | 无 | 无 | binary package，非 recipe target | 可能的差异点 |
| artifact-level patch retention | 无 | source branch patch deployment | binary diff，而非 source evidence closure | 可能的差异点 |
| evidence chain / verified backport | 不以此为任务 | 不以此为任务 | 不以此为任务 | VERIPORT 已覆盖 npm/PyPI 的生成式、运行验证 evidence chain；OpenWrt 只能讨论已发布 artifact 的非执行证据闭合 |
| name/version-only baseline | 非该 baseline | 非该 baseline | 非该 baseline | 可能的 evaluation seam |

## 严格收缩后的唯一候选问题

剩余可研究的问题不是“如何判断漏洞版本”，而是：

> 对一个固定、已发布的 OpenWrt `(release, target, package, CVE)`，Git commit ancestry 能否充分支持 package-level remediation status？若不能，怎样以 `manifest → recipe/feed → CVE-linked commit → tag-contained patch/source` 的**证据闭合**生成可复核、可弃权的 verdict，并量化仅名称/版本或仅 ancestry 会产生多少无证据结论？

该问题还不是创新主张。它只有在以下条件同时满足时才可能成立：

1. 结论是 **已发布 artifact 的非执行 evidence closure / audit reproducibility**，而不是 patch-based vulnerability analysis、verified backport 或 evidence-chain generation；
2. pair cohort、kernel 边界、target stratification 和 CVE source 在标签前独立预注册；
3. 标签不由同一 closure rule 自动推导，避免 label-feature 循环；
4. 结果完整保留 `insufficient_evidence`，且不宣称生成正式标准 VEX；
5. 进一步排除专门处理已发布发行 package source/manifest patch-retention 的近邻工作。

## 当前判断

```text
原始“provenance 提升 CVE 适用性”算法主张：STOP
配对 release package benchmark 主张：STOP（Patch2Vuln 已覆盖高层构造）
artifact-level evidence-closure corpus / audit-reproducibility 假说：CONDITIONAL，仅可继续检验
```

下一项最有信息量的实验不是训练模型，而是在冻结的 non-kernel pre/post pair 上独立测量三种证据是否分离：

```text
1. commit 是 tag ancestor
2. tag package recipe/source 实际保留 remediation 的可验证证据
3. release-target manifest 确认 package instance
```

若三者几乎总是一致，evidence-closure 也没有足够贡献，应停止该方向；若存在可审计、非平凡的不一致，并能由独立审查稳定裁决，才有可能形成一个严格收缩的数据/实证论文题目。
