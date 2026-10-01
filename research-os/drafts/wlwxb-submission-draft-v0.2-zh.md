# 物联网安全结论证据敏感性评估

> **稿件状态：** 《物联网学报》投稿格式 v0.2；不是新漏洞检测器，不输出 CVE 真值，不宣称同行评审录用。所有结果均为探索性 pilot，除非明确标注为固定规则下的描述性结果。

## 投稿元数据占位

- 作者：`[待填写]`
- 单位、城市、邮编：`[待填写]`
- 中图分类号：`TP393.08`（需由作者/编辑最终核定）
- 文献标识码：`A`（需按期刊要求核定）
- DOI：`[由编辑部生成]`
- 基金项目：`[如有则填写；无则删除]`

## English title

**Evidence Sensitivity Assessment for IoT Security Claims**

## English abstract

Public security records often combine package identity, commits, releases, device groups, and evaluation splits without establishing that these evidence types support the same claim strength. This report presents a bounded Evidence Sensitivity Stress Test (ESST). For a fixed claim, evidence is disclosed or degraded according to a predeclared, auditable tier order, and the claim state is classified as identified, conditional, or not identifiable. The protocol does not assign vulnerability labels, infer exploitability, or verify artifact safety. In an exploratory OpenWrt cohort, commit ancestry supported 62/62 pairs, any changed-path exact-blob retention supported 54/62, and strict all-path retention supported 50/62. Two independent reviewers agreed on 60/60 cells in the first blinded cohort and 50/50 cells in a second non-overlapping cohort. In an N-BaIoT mirror case, random-row and leave-one-device-out Random Forest Macro-F1 differed by 5.0–9.6 percentage points across two ordered row windows and five seeds. An initial packet schema achieved 16/20 agreement; after explicit tier-scoped evidence fields were frozen, an order-reversed replay achieved 16/16 agreement. These results establish protocol feasibility and bounded repeatability, not a new intrusion detector, vulnerability truth, or acceptance guarantee.

**Keywords:** Internet of Things; security claim; evidence sensitivity; reproducibility; device-held-out evaluation; OpenWrt


## 摘要

公开安全资料经常把名称、版本、提交、发布标签、软件包、设备组或数据切分放在同一条叙述中，但这些证据并不一定支持同样强度的安全结论。本文提出一个有界的 **Evidence Sensitivity Stress Test (ESST)**：对一个预先固定的安全结论，按公开、可审计的证据层级逐级降低或替换证据，记录结论支持状态何时从 `identified` 转为 `conditional` 或 `not_identifiable`。ESST 不判断漏洞是否存在，不把证据缺失转换为 `affected`/`not_affected`，也不构建 provenance assurance engine。

我们在两个不合并真值的案例上做探索性 pilot。OpenWrt 的 62 个 package release pair 中，commit ancestry 与 pre-release exclusion 支持信号为 62/62；任一 changed-path exact blob 保留为 54/62；全部 changed-path exact blob 保留为 50/62，因此 ancestry-only 到 strict source-retention signal 有 12/62 的降级。按固定哈希规则抽取 12 个 packet 后，两名独立审查者在 60/60 个 tier 判断上一致。N-BaIoT 镜像案例中，随机行与留一设备组 Macro-F1 差异在两个有序行窗口、五个种子下为 5.0–9.6 个百分点；初始 packet 设计在 16/20 个判断上一致，暴露 tier 语义歧义。冻结 claim 和 state rule 后，第二轮达到 16/16 一致。

这些结果只确认了 ESST 的机械可行性和有限的审查可重复性，不确认高水平创新、跨数据集真值或投稿录用。Prospector/SCA、Macaron/provenance assurance、Linux package patch-sharing 和普通 dataset split audit 是直接近邻；本文将其作为边界和威胁，而不是声称已超越它们。

**关键词：** security claim identifiability；evidence ablation；release evidence；device-held-out evaluation；reproducibility；OpenWrt；N-BaIoT

---

# 1. 引言

## 1.1 动机

安全研究通常把一个结论写成简短句子，例如“某 release 已包含修复”或“模型可以泛化到新设备”。N-BaIoT 原始研究提供了物联网僵尸网络检测的基础数据和模型背景[1]。但支撑这类句子的材料可能只包括软件名称与版本、一个 Git commit 的祖先关系、一个包构建记录、若干 CSV 行，或一次随机切分的分数。证据越多并不自动意味着结论越强；关键问题是：**删除或降级哪一类证据后，原结论仍然可被识别？**

已有工具和研究分别处理若干邻近问题：漏洞 advisory 到 fix commit 的检索与排序[2-3]、SCA 对 artifact 代码的安全判断、供应链 provenance/assurance[4]、Linux distribution package patch sharing[5]，以及 IoT IDS 的 grouped split 与数据集审计。这些工作并不自动提供一个跨任务的、预先声明的“证据降级—结论状态转移”测量协议。另一方面，本文不能据此宣称该协议已经新颖；它必须通过严格近邻审查和可证伪 pilot 才能继续。

## 1.2 研究目标

本文研究的不是“如何发现漏洞”或“如何提高 IDS 分数”，而是一个测量问题：

> 对同一条、边界明确的安全结论，能否用预先声明的证据阶梯测量其支持状态对证据降级的敏感性，并在独立审查者之间得到可重复裁决？

本文将 `identified` 理解为“指定的 source-evidence claim 在当前范围内可由给定证据支持”，不理解为漏洞状态已被识别。

## 1.3 研究问题

- **RQ1（可执行性）：** 能否为不同安全任务声明可审计的 evidence tiers、ablation order 和状态规则？
- **RQ2（转移）：** 在 OpenWrt release evidence 和 N-BaIoT device-split evidence 中，是否观察到非平凡的 claim-support transition？
- **RQ3（可重复性）：** 两名独立审查者是否能在不读取预计算 aggregate outcome 的情况下稳定应用状态规则？
- **RQ4（边界）：** 共同的 failure taxonomy 是否超出泛化的“provenance 不足”或普通 split audit？若不能，何时应停止该方向？

## 1.4 贡献边界

本文只允许以下贡献表述：

1. 一个 claim-specific、预声明、可审计的 evidence-ablation protocol；
2. 两个不合并数值真值的案例 pilot；
3. 对状态规则歧义、审查一致性和停止条件的显式报告；
4. 一个不把证据缺失转换为漏洞状态的安全报告模板。

本文不声称：

- 新的 CVE applicability 算法；
- artifact safety、remediation truth 或 exploitability verifier；
- 新的 IDS 检测模型；
- 设备可预测性等于泄漏；
- 跨生态质量排名或跨案例准确率；
- 已证明重大创新或已获得录用。

---

# 2. 形式化协议

## 2.1 Claim packet

每个案例先建立一个 claim packet：

```text
claim_id
claim wording and scope
non-claims
population/sample boundary
evidence tiers E0...Ek
ablation order
state rule
review instructions
stop conditions
```

claim wording 必须固定。若 tier 改变了 claim 本身，而不是只改变证据，实验无效。

## 2.2 Evidence tier

对 claim `C`，令 `E_i` 表示可使用的证据集合。tier 是一个**预先声明的证据披露顺序**，不是自动保证单调增强的质量排序。对每个 `E_i`，审查者给出：

```text
identified       指定 claim 在当前范围内可由 E_i 支持
conditional      只有部分、间接或范围受限的支持
not_identifiable E_i 不足以识别指定 claim
```

严格禁止以下转换：

```text
not_identifiable → affected
conditional      → not_affected
missing evidence → exploitability
```

## 2.3 状态转移与 cut set

定义：

```text
S(C, E_i) ∈ {identified, conditional, not_identifiable}
Δ_i = S(C, E_i) → S(C, E_{i+1})
```

若移除某一证据组件后状态首次不再是 `identified`，该组件被记录为当前 claim 的 **minimal support cut candidate**。它不是因果证明，只是协议范围内的最小支持候选。

## 2.4 审查协议

审查者只看到 packet 中的 source observations 和 state rule，不看到预先计算的 aggregate tier outcomes。每一格必须引用一条 observation。分歧不被平均隐藏，而是记录为：

- wording defect；
- observation missing；
- state rule conflict；或
- genuine adjudication disagreement。

若必须在观察结果之后修改 state rule，则修改后的轮次只能称为 protocol refinement，不得与初始轮次合并成一个未经说明的 reliability 数字。

---

# 3. 案例 A：OpenWrt source/release evidence

## 3.1 范围与输入

输入为冻结的 62 个 non-kernel OpenWrt pre/post package release pair，归属于 32 个 `(commit, CVE)` cluster；release 标签来自 OpenWrt 官方 release 目录[6]。该数据仅用于 source-evidence binding pilot；不重新定义 v2 标签，也不输出 `affected`/`not_affected`。

每个 pair 的证据阶梯为：

```text
T0  name/version record
T1  package/target presence
T2  post commit ancestry + pre-release exclusion
T3  at least one changed-path exact blob retained at post release
T4  all changed-path exact blobs retained at post release
```

T4 是低成本、可审计的 source-retention convenience signal，不是语义修复证明，也不是 artifact safety verdict。

## 3.2 机械结果

| tier | 支持 signal 的 pair |
|---|---:|
| T0 | 62/62 |
| T1 | 62/62 |
| T2 | 62/62 |
| T3 | 54/62 |
| T4 | 50/62 |

状态变化：

```text
T2 → T3：8/62 降级
T3 → T4：4/62 进一步降级
T2 → T4：12/62 总降级
```

在 32 个 cluster 中，26 个 strict closed，6 个需要 lineage review；其中 4 个 cluster 没有任何 exact changed-path blob。strict mismatch 不解释为修复失败；它只触发 recipe/version update、patch folding、后续维护提交等 lineage review。

## 3.3 盲化 packet review

按 identity key 的 SHA-256 排序，每条 stable family 取前两条，得到 12 个 packet。两名审查者只读 source observations，不读 aggregate tier output。

结果：

```text
60/60 tier cells exact agreement
agreement = 1.00（仅为 12-packet exploratory agreement）
```

聚合状态：

| tier | identified | conditional | not_identifiable |
|---|---:|---:|---:|
| T0 | 0 | 0 | 12 |
| T1 | 0 | 0 | 12 |
| T2 | 12 | 0 | 0 |
| T3 | 10 | 0 | 2 |
| T4 | 9 | 1 | 2 |

该结果支持协议在小样本 packet 上可重复，但不能报告总体 inter-rater reliability，也不能解释为 CVE 真值正确率。

---

# 4. 案例 B：N-BaIoT device-split evidence

## 4.1 数据和 claim boundary

该案例使用本地验证的 Kaggle 原始布局镜像，不称为官方 UCI 最终归档。主实验只保留九个镜像设备组共同拥有的六类，并在每个设备×类别单元使用 600 行。随机行与 LODO Random Forest Macro-F1 的差异在两个有序行窗口和五个种子上为 **5.0–9.6 个百分点**。

固定 claim（修订后的 v2 packet）：

> 对九组、六类别的 N-BaIoT 镜像，当前证据是否识别出一个不依赖设备组间行共享的模型评估？

该 claim 不包含跨数据集泛化、数据泄漏、因果性或漏洞安全性。

## 4.2 tier

```text
T0  random-row result only
T1  common-support sampling + random-row result
T2  second ordered sampling window + comparison context
T3  explicit leave-one-device-out result on common-support rows
```

状态规则：

- `identified`：该 tier 自身包含明确的 device-held-out evaluation result；
- `conditional`：只有范围受限或协议上下文支持；
- `not_identifiable`：没有 device-group held-out evidence。

## 4.3 盲审结果和协议修订

初始 packet schema 把 random-row、ordered-window、LODO 和 independent dataset 混在一个 claim 中，两个审查者仅达到 16/20 一致。该失败结果被保留，原因是 tier 语义没有固定：

- LODO gap 是否算 standalone result；
- protocol 但没有 model metric 是否足够；
- 单镜像内结论应是 identified 还是 conditional；
- 缺少第二数据集应如何处理。

随后在第二轮前冻结 claim 和 state rule。v2 packet 的两个审查者达到：

```text
16/16 exact agreement
agreement = 1.00（修订协议上的探索性结果）
```

v2 的状态模式为：

| packet | T0 | T1 | T2 | T3 |
|---|---|---|---|---|
| RF window 0 | not_identifiable | conditional | conditional | identified |
| RF window 2000 | not_identifiable | conditional | conditional | identified |
| LR window 0 | not_identifiable | conditional | conditional | identified |
| device-provenance-only | not_identifiable | conditional | conditional | conditional |

这验证了一个重要限制：协议的可重复性依赖于 claim wording、tier quantifier 和“result vs protocol”定义。它不是可以事后自由命名的通用评分表。

随后进行 order-invariance replay：保持 claim、数据和状态规则不变，仅反转 packet/tier 顺序。v3 的 flat-observation schema 只达到 17/20 一致，暴露 gap-only result 与 tier-scoped evidence 未被显式编码的问题。将每个 packet 改为显式 `tier_evidence` 字段并冻结相同语义后，v4 达到 16/16 一致。本文保留 v3 失败，不只报告 v4 成功；v4 仍只是四个 packet 的协议复现，不是总体可靠性估计。

---

# 5. 结果综合

## 5.1 可以支持的跨案例命题

两个案例不合并 Macro-F1、closure rate 或真值。它们只共享以下方法结构：

```text
fixed claim
→ fixed evidence tier
→ evidence ablation or strengthening
→ claim-state transition
→ independent adjudication
→ explicit stop rule
```

OpenWrt 的转移发生在 ancestry/source-retention binding；N-BaIoT 的转移发生在 row-sharing/device-held-out independence。它们是不同 domain 的实例，不是同一个现象的联合估计。

## 5.2 不能支持的命题

当前证据不能支持：

- 一个跨案例的 universal taxonomy；
- 一个“最小必要证据”总体比例；
- `identified` 的正确率或 recall；
- 证据降级引起漏洞状态变化；
- 设备信息引起性能差距的因果解释；
- 新方法优于 Prospector、Macaron、GUAC、VEX/SBOM 或 dataset audit；
- 任何 peer-review acceptance probability。

## 5.3 直接近邻边界

### Prospector / advisory-to-fix mapping

Prospector 的全文明确研究 advisory 到 fix commit 的检索、排序，并讨论已知 fix code 如何帮助判断 artifact 是否包含修复代码。本文不检索 fix commit，不判断 artifact 安全，不输出 affectedness；若出现这些表述，即构成越界。

### Macaron / provenance assurance

Macaron 公开资料覆盖 source、artifact、dependency、build provenance 的获取、验证和 policy/conformance。本文不构建 assurance engine，不验证供应链 policy，只测量在已给 source observations 下 claim support 如何降级。Macaron 论文全文仍需取得，因此不能宣称完全排除。

### Linux package patch-sharing

ICSE 2026 的 patch-sharing 工作研究 homologous package、patch overlap、introduction delay 和 recommendation。本文不做 patch recommendation 或 cross-distro overlap ranking；但 OpenWrt 的 changed-path retention 数据与其有明显邻近性，必须作为直接 baseline。

### IoT split audit

N-BaIoT 的 random-row/LODO 差异不是新 IDS 算法，也不是首次 split audit。它只作为第二个 claim-specific evidence-boundary instance。若跨案例 taxonomy 不能超出普通 grouped split audit，应停止跨案例主张。

---

# 6. 威胁、限制与停止条件

## 6.1 数据和真值

没有独立的 CVE applicability truth、artifact semantic truth 或跨数据集 N-BaIoT truth。因此本文报告 evidence support state，不报告 vulnerability classification accuracy。

## 6.2 选择和后验风险

OpenWrt 12-packet pilot 使用固定 hash rule，但完整 62-pair closure output 已存在。后续研究必须从新的 hash-selected population 抽样，并由 reviewer 只看 packet，不看 closure outcome。N-BaIoT 初始 16/20 分歧说明即使不看 outcome，claim wording 也会制造后验自由度。

## 6.3 证据代理

exact blob retention 是便利信号；它不能替代 patch semantic lineage、build recipe 展开、二进制包内容或签名 provenance。LODO 是一种 device-independence protocol；它不能替代独立数据集、设备身份验证或真实时间证据。

## 6.4 停止规则

满足任一条件时停止高层 novelty 叙事，保留技术报告：

1. 近邻全文显示已有工作直接测量同一 claim-state transition；
2. 新一轮 packet review 在冻结规则下出现不可解释的大量分歧；
3. taxonomy 只能写成 generic provenance completeness 或 generic split audit；
4. 任一结果需要把 `conditional/not_identifiable` 转换成 CVE truth；
5. 结果依赖后验选择或未记录的 artifact/row mapping；
6. 需要执行固件、PoC、漏洞或设备连接。

---

# 7. 结论（当前版本）

ESST 在两个案例上表现出机械可执行性，并在小规模、明确规则的 blind packet review 中获得重复裁决。OpenWrt 显示 ancestry-only 与 strict source-retention signal 之间存在 12/62 的描述性降级；N-BaIoT 显示 random-row 与 device-held-out evaluation 的数值敏感性，并暴露了证据层级语义需要预先固定。

因此，本文目前可以作为一篇**边界严格的 methods/report 初稿**继续准备。最强、最诚实的结论是：

> 公开安全结论的支持强度可能对证据粒度敏感；一个 claim-specific、预声明的 evidence-ablation protocol 可以测量这种状态转移，但当前 pilot 尚不足以证明高水平新颖性、独立真值或投稿录用。

---

# 参考文献

[1] MEIDAN Y, BOHADANA M, MATHOV Y, et al. N-BaIoT—Network-based detection of IoT botnet attacks using deep autoencoders[J]. IEEE Pervasive Computing, 2018, 17(3): 12-22. DOI:10.1109/MPRV.2018.03367731.

[2] HOMMERSOM D, SABETTA A, COPPOLA B, et al. Automated mapping of vulnerability advisories onto their fix commits in open source repositories[J]. Empirical Software Engineering, 2024, 29: 1-34. DOI:10.1145/3649590.

[3] SABETTA A, PONTA S E, CABRERA LOZOYA R, et al. Known vulnerabilities of open source projects: Where are the fixes?[J]. IEEE Security & Privacy, 2024, 22(2): 49-58. DOI:10.1109/MSEC.2023.3343836.

[4] HASSANSHAHI B, MORSCHER M, MENG W, et al. Macaron: A logic-based framework for software supply chain security assurance[C]//Proceedings of SCORED 2023. New York: ACM, 2023: 29-38. DOI:10.1145/3605770.3625213.

[5] PENG J, ZHU J, ZHANG Y, et al. Toward efficient package maintenance: An empirical study of patch sharing across four Linux distributions[C]//Proceedings of ICSE 2026. New York: ACM, 2026: 1635-1647. DOI:10.1145/3744916.3787836.

[6] OPENWRT PROJECT. OpenWrt releases[EB/OL]. https://downloads.openwrt.org/releases/.



# 作者简介

`[按期刊格式填写全部作者简介及照片]`

# 附录 A：可复现实验索引

- OpenWrt mechanical probe：`tools/run_evidence_sensitivity_probe.py`
- OpenWrt pilot artifact：`artifacts/openwrt-evidence-sensitivity-pilot.json`
- OpenWrt blinded packets：`artifacts/openwrt-blinded-review-packets.json`
- OpenWrt adjudication：`artifacts/openwrt-blinded-review-adjudication.json`
- N-BaIoT common-support audit：`reports/nbaiot-common-support-audit-report.md`
- N-BaIoT blinded packets v2：`artifacts/nbaiot-blinded-review-packets-v2.json`
- N-BaIoT adjudication record：`reviews/nbaiot-blind-adjudication-and-cross-case-gate-2026-10-01.md`
- Nearest-work audit：`literature/iot-security/evidence-sensitivity-nearest-work-fulltext-audit-2026-10-01.md`
