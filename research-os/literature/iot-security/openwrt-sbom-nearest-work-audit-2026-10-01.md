# OpenWrt 发布溯源漏洞适用性研究：近邻文献全文审计

**日期：**2026-10-01  
**目的：**判断“利用 OpenWrt 发布版本的 package recipe、feed commit 与补丁/回补证据，改善 package-release-CVE 漏洞适用性判断”的方案，是否已经被近邻工作直接完成。  
**审计标准：**只有论文全文明确报告的内容才算已覆盖；摘要、标题或推断不算证据。

## 待检验的问题

> 对同一批 OpenWrt `(release, target, package, CVE)` 候选，方法 B 在名称/版本匹配（方法 A）之外加入官方 recipe、feed commit、补丁及回补证据，能否减少错误的 `affected` 判定，同时不明显降低召回？

这不是通用 SBOM 生成、固件提取、CVE 排序、风险评分或二进制相似度检索问题。

## 全文审计结果

| 文献 | 精确任务 | OpenWrt 作用 | 发布 recipe/feed/backport 证据 | 真值/评估 | 与本研究的关系 |
|---|---|---|---|---|---|
| *Impacts of Software Bill of Materials (SBOM) Generation on Vulnerability Detection*（2024） | 比较 Syft/Trivy 生成的 SBOM 与多个扫描器得到的漏洞计数。 | 无。实验对象为 Docker 镜像。 | 未报告。 | 扫描器计数，不是人工核验的漏洞适用性真值。 | **部分重叠**：说明 SBOM/扫描器差异重要；未做发布溯源适用性基准。 |
| *Cybersecurity Vulnerability Prioritisation via Risk Assessment*（2025） | 对 OpenWrt 网关的 SBOM/CVE 进行模拟部署后果与风险排序。 | 以 OpenWrt 住宅网关作为案例。 | `opkg` 名称/版本映射到 SPDX/NVD；未报告 release recipe、feed commit、补丁链或回补判定流程。 | 例子与模拟风险结果；没有独立适用性标注、precision/recall 或对照实验。 | **部分重叠**：OpenWrt 与 SBOM 背景相近；未比较 provenance/backport 与名称/版本匹配。 |
| *Automated SBOM-Driven Vulnerability Triage for IoT Firmware*（2026） | 离线提取 Linux 固件、生成 SBOM、映射 CVE 并排序。 | 计划使用 ARM/MIPS 厂商固件；没有 OpenWrt 发布证据基准。 | 承认 backport 歧义，但未导入官方 OpenWrt recipe、feed commit 或发布补丁链。 | arXiv v1 明示为 **Planned evaluation**；未报告已完成的准确率或人工真值评估。 | **部分重叠**：固件/SBOM/CVE 分诊；没有本研究的发布级对照与召回约束。 |
| *Automating Firmware Vulnerability Triage via High-Level Representations and Similarity Digests*（BAR 2026 workshop） | 用高层中间表示和 TLSH 相似度检索已知脆弱函数，筛选潜在固件。 | 98 个 OpenWrt 镜像、18.06.0–24.10.4、8 个 CVE。 | 提交历史、changelog、补丁元数据被用于构造/验证脆弱与修复函数签名；未报告 package-release-CVE 的 recipe/feed/backport 决策规则。 | Top-K / Recall@K、函数级 vulnerable/fixed/unrelated 标签。 | **部分重叠且最接近**：已有 OpenWrt 补丁相关验证，但任务是二进制函数相似度检索，不是名称/版本基线的包级适用性判定。 |

## 逐篇可核验依据

### 1. SBOM generation（2024）

- 使用 Syft 0.102.0、Trivy 0.49.0 生成 CycloneDX/SPDX SBOM，再以 Grype、Trivy、CVE-bin-tool 做数据库匹配（第 3 节，第 2–3 页）。
- 2,313 个 Docker 镜像中，1,303 个能通过所有工具；作者比较工具/格式对漏洞计数的影响（第 3–4 节，第 3–8 页）。
- 作者将 SBOM 真值列为未来工作，未标注具体发布物是否真的受 CVE 影响（第 6–7 节，第 8–9 页）。
- 一手全文：[PDF](https://www.cs.montana.edu/izurieta/pubs/SCORED2024.pdf)。

### 2. OpenWrt 风险排序（2025）

- 该文从固件 inventory 的 OPKG 名称/版本映射到 SPDX，并查询 NVD；目标是将 CVSS 映射到 Spyderisk 属性并对模拟风险排序（第 4.3–4.5 节，第 10–11 页）。
- 文中没有指定可复现的 OpenWrt release、recipe/feed commit、patch lineage 或回补漏洞适用性规则。
- 以 `pppd` / CVE-2020-8597 展示“Very High”模拟风险；这不是对漏洞是否存在的独立适用性真值（第 5 节，第 11–12 页）。
- 一手全文：[PDF](https://jaatun.no/papers/2025/CVE_pri_ARES_WS.pdf)。

### 3. 自动化固件 SBOM 分诊（2026）

- 任务是离线固件文件系统提取、Syft/CycloneDX SBOM、PURL/CPE 对 NVD/GitHub advisory 的映射与风险排序（第 4–11 节，第 3–8 页）。
- 方法提到 `opkg`、版本不确定性与 backport 歧义，但没有官方 OpenWrt 发布 recipe、feed commit、发布补丁人工判定或与名称/版本法的误判对照（第 9.1 节）。
- arXiv 记录和全文写明是 **Planned evaluation**；计划抽查 5%，没有已发布的人工标签、准确率或召回结果（第 12 节）。
- 一手来源：[arXiv record](https://arxiv.org/abs/2601.01308)，[PDF](https://arxiv.org/pdf/2601.01308)。

### 4. 高层表示和相似摘要的固件分诊（BAR 2026）

- 该文在 98 个 OpenWrt 镜像上，以 Binary Ninja HLIL、TLSH 和 APOTHEOSIS 检索潜在脆弱函数；评估为 Top-10、Recall@K 与架构比较（第 III–IV 节）。
- 提交记录、changelog 和 patch metadata 用于查询签名和验证，但论文未提供“包-发布-CVE → 已回补/未回补”的通用判定表，也未以名称/版本匹配为 baseline。
- 数据集包含 8 个 CVE、18.06.0–24.10.4 的 x86/ARM 镜像；MIPS 被排除，函数提升/配置差异和 patch 接近性是局限（第 III–V 节）。
- 复核发现其第 6 页把 `10/48` 写成 `35.71%`；正确值是 `20.83%`。这不改变上述范围判断，但在后续引用时不得复述该错误比例。
- 一手全文：[BAR 2026 PDF](https://www.ndss-symposium.org/wp-content/uploads/bar2026-27.pdf)，[官方项目页](https://www.ndss-symposium.org/ndss-paper/auto-draft-655/)，[官方会议项目](https://www.ndss-symposium.org/ndss-program/bar-2026/)。

## 结论与闸门决定

**结论：暂时通过（GO，带条件）。** 四篇中没有一篇全文明确评估下列完整组合：

```text
冻结的官方 OpenWrt release/target package inventory
+ package recipe、feed commit 与已记录 backport 证据
+ 与名称/版本匹配使用完全相同的候选集
+ 独立人工判定的 package-release-CVE 适用性标签
+ false-affected 降低与 recall 保护线
```

这不是“已证明新颖”，也不是投稿保证。它仅说明当前四篇最近近邻工作**没有直接阻止**一个有严格边界的试点。

进入数据冻结前还必须遵守：

1. 只用官方 OpenWrt 发布元数据、源代码/补丁历史与官方 CVE 记录；
2. 先检查所选 target 的 manifest、BOM、recipe 与补丁记录是否可以对应；
3. 若无法构造至少约 100 个候选和 30 个以上可二元判定案例，停止而非补猜标签；
4. 如果后续检索发现直接的同类 package-release-CVE backport 基准，立即重新判定为 `STOP/PIVOT`。
