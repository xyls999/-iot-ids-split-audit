# Evidence Sensitivity Stress Test：可投稿性与研究性确认

**审查状态：** `PILOT-SUPPORTED / PUBLICATION-UNCONFIRMED`

本文件不把候选升为 GO，也不产生漏洞真值。它记录一次独立盲审和近邻反证结果。

## 1. 研究性验证：盲化 packet review

### 设计

从固定 hash 规则得到的 12 个 OpenWrt packet 中，分别交给两个独立、只读审查者。审查者只读取：

`research-os/artifacts/openwrt-blinded-review-packets.json`

packet 提供 source observations，但隐藏预计算的 aggregate tier outcomes。每个 packet 在 T0–T4 逐层判断：`identified`、`conditional` 或 `not_identifiable`。

### 结果

机器可读裁决：`research-os/artifacts/openwrt-blinded-review-adjudication.json`。

| tier | identified | conditional | not_identifiable |
|---|---:|---:|---:|
| T0 | 0 | 0 | 12 |
| T1 | 0 | 0 | 12 |
| T2 | 12 | 0 | 0 |
| T3 | 10 | 0 | 2 |
| T4 | 9 | 1 | 2 |

两个审查者在 **60/60 cells** 完全一致，agreement = **1.00**。这只能证明该 12-packet pilot 的规则可重复，不能报告为总体 inter-rater reliability，也不能替代独立真值。

### 研究性含义

该结果满足“可检验研究问题”的最低条件：

1. evidence tier 可机械重放；
2. 审查者不需要 CVE affected/not_affected 标签；
3. T2→T3→T4 存在非平凡状态变化；
4. partial retention 被稳定判断为 `conditional`，而非被错误转为正面结论；
5. 失败可解释为 identity / artifact binding 的证据边界，而不是任意模型偏好。

但仍有三个测量定义问题必须在预注册前修正：

- T2 的 `contains` 必须明确等价于 Git commit reachability/ancestry；
- T3/T4 必须固定 changed-path 的量词、重命名处理和 blob 比较规则；
- `identified` 必须定义为“识别指定 source-evidence claim”，不能被读作“漏洞状态已识别”。

## 2. 近邻反证

### A. Automated Mapping of Vulnerability Advisories onto their Fix Commits

来源：arXiv preprint `2103.13375`；已取得并离线提取全文：
<https://arxiv.org/pdf/2103.13375>

全文明确的对象是：从 advisory 提取 vulnerability information，过滤候选 commit，并用 NLP/ML 排序 fix commits；数据集包含 2,391 个 known fix commits 和 1,248 个 advisories，报告 top-10 recall 与 ranking precision。

**重叠：** 都使用 advisory/CVE 到 commit 的连接。

**不重叠：** 该工作优化的是“找到哪个 commit 是 fix commit”；本候选不提出 fix-commit finder，也不测 ranking。候选测量的是：在 commit 已给定后，逐级降低 release/source evidence 时，某个安全结论何时不再 identifiable。

**判断：** 不是直接否决，但必须在论文中把“fix commit identification”与“evidence sufficiency after commit identification”明确分开。

### B. Known Vulnerabilities of Open Source Projects: Where Are the Fixes?

官方来源页：
<https://www.eurecom.fr/en/publication/7561>

官方摘要将工作描述为 Prospector 的工业经验，用于帮助开发者在 commits 中追踪 vulnerability。当前环境无法取得出版社/ResearchGate 全文，因此不能声称已完成全文排除。

**判断：** 高风险近邻仍开放。摘要层面显示其核心是 vulnerability-to-commit tracing，和 A 同类；尚未发现其摘要直接主张 evidence-tier degradation protocol，但不能据此宣称无重叠。

### C. CVECenter

作者官方页面：
<https://csu-wingmate.github.io/publication/fse24cvecenter>

页面说明 CVECenter 在 3 个 Linux distribution 版本上处理 heterogeneous vulnerability records、retrieval、assessment、auto-fixing 和持续漏洞管理，并报告管理超过 8,000 CVEs、发布 1,157 advisories。

**重叠：** 都关注 Linux distribution 的安全证据/流程。

**不重叠（基于作者公开页面，不是全文排除）：** CVECenter 是自动化 vulnerability-management system/industry practice；本候选是不改变漏洞检测器的 evidence-sensitivity measurement protocol。

**判断：** 不是已排除的直接近邻；需要全文审计后才能降低风险。

### D. Toward Efficient Package Maintenance: An Empirical Study of Patch Sharing across Four Linux Distributions

已取得作者公开 PDF 并离线提取全文：
<https://zhangyw.work/file/papers/Peng2026ICSE.pdf>

该 ICSE 2026 工作研究 Debian、Ubuntu、Fedora、openEuler 的 homologous packages、patch overlap、patch introduction delay 和 cross-distro patch recommendation。全文明确区分 source packages 与 binary packages，并分析 patch sets。

**重叠：** 都把 distribution package source/patch retention 当作可审计对象；这是目前最强的近邻风险。

**不重叠：** 该工作研究 patch sharing、维护效率与推荐；本候选研究同一安全结论在 evidence ablation 下的 state transition，不做跨 distro patch recommendation，也不把 patch overlap 当安全状态。

**判断：** 可以支持“研究问题仍有不同”的初步判断，但不能支持“独立性已确认”。论文必须把 patch-sharing literature 作为直接 baseline，并展示 stress-test 的 state-transition 结果不能由 patch-overlap 分析直接得到。

### E. Macaron / assurance-case / provenance graph 方向

Macaron 全文尚未取得；SLSA、OpenVEX、OSV、GUAC 和一般 provenance/assurance graph 已完成此前审计。它们覆盖 provenance、status、graph 或 assurance representation，但当前没有因此证明本候选新颖。

**判断：** Macaron 和任何“evidence assurance / claim graph with confidence”近邻仍是 publication blocker，除非全文审计确认其没有相同的 claim-state degradation / minimum-evidence measurement。

## 3. 可投稿性判断

### 已确认

- 有一个可复现的操作对象，而不是概念图：预声明 tier、ablation order、state rule；
- 12-packet blind review 达到 60/60 一致；
- OpenWrt 全体 62 pair 的 T2→T4 降级为 12/62；
- N-BaIoT 提供独立的 split/provenance sensitivity 案例；
- 不依赖固件执行、PoC、设备连接或漏洞利用。

### 尚未确认

- 没有独立真值，因此不能计算 correctness、recall、precision；
- 盲审只有 12 个 OpenWrt packets，不能支撑总体 reliability；
- 跨案例共同 taxonomy 还没有完成第二位案例的独立 packet adjudication；
- Macaron、Prospector/known-fixes、CVECenter 全文排除不完整；
- 不能排除该协议最终只是“provenance completeness + dataset split audit”的统一命名。

## 最终 verdict

```text
研究性：初步确认（可证伪、可重复、已有非平凡 transition）
技术报告价值：确认
可投稿性：未确认
高水平新颖性：未确认
当前项目状态：PILOT-SUPPORTED / PUBLICATION-UNCONFIRMED
```

在完成 Macaron/Prospector 全文近邻审计、N-BaIoT 独立 blind packet review、预注册定义修订前，不得写 `publishable`、`novel`、`validated` 或冻结 v3。
