# Research-OS 当前完整总结

**更新时间：** 2026-10-01  
**目标期刊假设：** 截图中的《物联网学报》；如果目标不是该刊，需要重新核验。  
**当前状态：** `algorithm_route_preflight_no_method_claim_yet`

---

# 0. 一句话说明

现在真正保留的研究只有一条主线：

> **研究公开安全结论对证据强弱变化是否敏感，并用预先固定的证据阶梯测量结论何时从“可识别”变成“有条件”或“不可识别”。**

英文暂名：**Evidence Sensitivity Stress Test（ESST）**。

它不是：

- 新的入侵检测算法；
- CVE 漏洞判定器；
- artifact 安全验证器；
- provenance 图系统；
- 设备泄漏检测器；
- 固件、设备或 PoC 实验。

---

# 1. 最终论文想回答什么

安全论文常常写出这样的结论：

```text
某个 OpenWrt release 已包含修复
某个 IDS 可以泛化到新设备
某个 package 与某个 CVE 有关
```

但这些结论所使用的证据可能只有：

```text
名称/版本
Git commit
release tag ancestry
package/target
changed-path blob
随机行切分
设备留出切分
```

这些证据强度不同，不能自动支持同样强的结论。

ESST 的基本流程是：

```text
固定一个 claim
→ 规定证据阶梯
→ 逐级删除或降级证据
→ 判断 claim 状态
→ 记录状态转移和审查分歧
```

状态只有三种：

```text
identified          当前证据能支持指定 claim
conditional         只能部分或范围受限地支持
not_identifiable    当前证据不足以识别该 claim
```

明确禁止：

```text
证据不足 → affected
证据不足 → not_affected
设备可预测 → leakage
exact blob mismatch → 修复失败
```

---

# 2. 当前论文使用两个案例

两个案例不合并真值，不合并 F1，不计算一个所谓“跨案例平均分”。它们只用来检验同一种方法结构是否可执行。

## 案例 A：OpenWrt release/source evidence

### 数据

- 62 个 non-kernel OpenWrt pre/post package release pair；
- 32 个 `(commit, CVE)` cluster；
- 来自官方 release/tag/source 记录；
- 当前只做 source-evidence binding；
- 不重新修改 v2 标签；
- 不输出 `affected`/`not_affected`。

### 证据阶梯

```text
T0  name/version record
T1  package/target presence
T2  post commit ancestry + pre-release exclusion
T3  至少一个 changed-path exact blob 被 post release 保留
T4  所有 changed-path exact blob 被 post release 保留
```

### 机械结果

| 证据层 | 支持数量 |
|---|---:|
| T0 | 62/62 |
| T1 | 62/62 |
| T2 | 62/62 |
| T3 | 54/62 |
| T4 | 50/62 |

最重要的结果：

```text
仅看 ancestry：62/62
要求 strict source retention：50/62
总共 12/62 发生 evidence-support downgrade
```

这不证明漏洞修复失败，只说明：

```text
commit 在 release ancestry 中
≠ changed source blob 在 release 中逐字保留
```

### 审查结果

第一轮：

```text
12 个 hash-selected packet
60/60 判断一致
```

第二轮：

```text
10 个不与第一轮重叠的 packet
50/50 判断一致
```

第二轮只有 10 个，是因为某个 stable family 没有足够的后续 rank，避免人为补样和重复抽样。

---

## 案例 B：N-BaIoT device-split evidence

### 数据边界

- 使用本地验证的 Kaggle 原始布局镜像；
- 不是官方 UCI final-data 结果；
- 9 个镜像设备组；
- 115 个数值特征；
- 只保留 6 个所有设备组共同拥有的攻击类别；
- 每个设备×类别取 600 行；
- 总计 32,400 行；
- 镜像没有已核验的时间戳。

### 实验比较

```text
random-row split
vs.
leave-one-device-out（LODO）
```

### 结果

Random Forest 在两个有序行窗口、五个种子下：

```text
random-row Macro-F1 - mean LODO Macro-F1
= 5.0–9.6 percentage points
```

这说明当前镜像中，随机行评估与设备留出评估不同。

但不能写成：

- 已证明数据泄漏；
- 已证明设备指纹导致性能虚高；
- 已证明因果机制；
- 已证明跨数据集泛化失败。

### 审查重放

第一版 packet schema：

```text
16/20 一致
```

暴露问题：

- LODO gap 是否算 explicit result；
- 只有 held-out protocol 是否够强；
- flat observations 没有明确绑定到具体 tier。

第二版冻结 claim 和规则后：

```text
16/16 一致
```

第三轮把 packet/tier 顺序反转：

```text
17/20 一致
```

这再次暴露 flat schema 问题。

第四轮加入显式 `tier_evidence` 字段后：

```text
16/16 一致
```

因此论文必须诚实写出：

```text
规则最初不充分
→ 顺序重放发现 schema 缺陷
→ 显式 tier schema 后重复性改善
```

不能只写最后一个 16/16。

---

# 3. 当前真正的研究贡献是什么

现在可以防守的贡献只有三点：

## 贡献 1：claim-specific evidence protocol

不是简单列 provenance 字段，而是先固定 claim，再固定证据降级顺序和状态规则。

## 贡献 2：把“证据不足”变成显式弃权状态

不把缺证据强行转成漏洞标签、设备暴露或攻击结论。

## 贡献 3：把规则失败也作为结果

N-BaIoT 的 16/20 和 17/20 不是被删掉的失败，而是说明 evidence schema 必须显式化。

---

# 4. 已经停止的方向

以下方向已经停止，不再作为投稿主张：

## 4.1 OpenWrt CVE applicability algorithm

被 AFV、PatchScout、Patch2Vuln、VERIPORT 等近邻阻断。

## 4.2 普通 provenance/evidence graph

SLSA、OpenVEX、OSV、GUAC、Macaron 等已覆盖很多高层组件。

## 4.3 Security Update Evidence-Join

容易被认为是 provenance、traceability、scanner 或 lifecycle research 的重新命名，已降为 `NO-GO/pilot-only`。

## 4.4 新 IDS 模型

当前没有提出新模型，不做 accuracy 竞争，也不做设备运行、固件运行或漏洞利用。

---

# 5. 近邻研究边界

## Prospector / advisory-to-fix mapping

已有工作研究：

```text
advisory → candidate/fix commit
```

并讨论通过 fix code 判断 artifact 是否包含修复代码。

因此本文不能说：

```text
我们判断 artifact 是否安全
我们判断 CVE 是否已修复
```

本文只能说：

```text
在 commit 已给定的前提下，观察不同 source evidence tier 对 claim support 的影响
```

## Macaron

Macaron 关注：

- source/artifact/dependency；
- build provenance；
- policy/conformance；
- supply-chain assurance。

本文不构建 assurance engine，不验证 SLSA policy，也不输出 artifact trust verdict。Macaron 全文仍未完全取得，因此不能声称已彻底排除重叠。

## Linux package patch-sharing

已有 ICSE 2026 工作研究：

- homologous packages；
- patch overlap；
- patch introduction delay；
- patch recommendation。

本文不做 patch recommendation，也不做跨发行版 patch ranking，但 OpenWrt 的 source retention 与其有邻近性，必须在论文中承认。

## IoT split audit

N-BaIoT 的 random-row/LODO 比较不是新 IDS 方法，也不是首次发现 split sensitivity。它只作为第二个 claim-specific evidence-boundary case。

---

# 6. 《物联网学报》匹配情况

已核验官方页面：

- 期刊介绍：<https://www.wlwxb.com.cn/zh/info/15336/>
- 投稿须知：<https://www.wlwxb.com.cn/zh/info/15343/>
- 稿件格式：<https://www.wlwxb.com.cn/zh/info/15345/>
- 稿件流程：<https://www.wlwxb.com.cn/zh/info/15344/>

官方范围包含：

```text
物联网基础理论
关键技术
数据融合处理
安全管控
```

近年官方文章包括：

- 联邦强化学习 IoT 入侵检测；
- 海洋气象传感器网络入侵检测；
- 工业控制系统安全风险评估。

因此主题匹配是成立的。

但期刊要求突出创新，且采用双盲审稿。所以：

```text
主题可投：是
格式可适配：是
现在录用：不能确认
```

---

# 7. 当前论文文件

## 当前投稿版

`research-os/drafts/wlwxb-submission-draft-v0.2-zh.md`

状态：投稿格式初稿。

已完成：

- 14 字中文标题；
- 中英文摘要；
- 参考文献；
- 13,541 个 Python 字符；
- claim lint unsafe = 0。

尚未完成：

- 作者信息；
- 单位、城市、邮编；
- 作者照片和简介；
- 基金信息；
- Word 最终排版；
- 图表编号和图形；
- OpenWrt semantic lineage adjudication。

## 完整方法版

`research-os/drafts/evidence-sensitivity-stress-test-methods-report-draft-zh.md`

## 实验计划

`research-os/plans/evidence-sensitivity-stress-test-experiment-plan-zh.md`

---

# 8. 算法路线最新预研

由于《物联网学报》近期文章以明确算法和实验为主，项目已正式转向算法论文预研。第一轮比较了标准 MLP 与 DANN-style 设备对抗 MLP：

| 方法 | random-row Macro-F1 | mean LODO Macro-F1 | gap |
|---|---:|---:|---:|
| MLP | 0.6994 | 0.6551 | 0.0443 |
| DANN λ=0.01 | 0.6985 | 0.6467 | 0.0519 |
| DANN λ=0.05 | 0.7000 | 0.6483 | 0.0517 |
| DANN λ=0.10 | 0.6996 | 0.6497 | 0.0499 |
| DANN λ=0.20 | 0.6997 | 0.6554 | 0.0443 |

结论：当前 DANN-style 原型没有稳定改善，不能称为新算法。现代方向筛选和首轮实验证明，TTA、CORAL、GroupDRO、Mixup 在当前协议下没有稳定优势；异构 ExtraTrees + HistGradientBoosting 集成在 5 seeds × 9 device-held-out folds 上达到 mean Macro-F1=0.8107，而 MLP=0.6465、DANN=0.6518。该结果支持“有效升级 baseline”，但不等于新算法创新。新增嵌套设备留出调参后，单 seed 外层 mean Macro-F1=0.8172；固定树集成的五 seed 保守结果仍为 0.8107。下一步先完成树集成的统一 per-class/FPR/延迟审计和第二数据集复现，再决定是否针对困难设备设计 IoT-specific 方法。

详细结果：`reports/nbaiot-algorithm-preflight-results-2026-10-01.md`。算法计划：`plans/nbaiot-algorithm-paper-research-plan-zh.md`。

# 9. 当前状态和下一步

当前状态不是“已经成功发表”，而是：

```text
实验协议可执行：已确认
小规模规则重复性：已确认
期刊主题匹配：已确认
高水平创新：未确认
独立真值：未获得
同行评审录用：未确认
```

下一步只做三件事：

1. 完成 OpenWrt second cohort 的 semantic lineage adjudication；
2. 把审查结果、负结果和 schema failure 放入投稿稿件；
3. 做一次外部读者式双盲预审，然后再决定是否投稿。

如果 lineage review 不能形成可重复规则，或者审稿式评估认为 ESST 只是 provenance/split audit 的重新命名，稿件将降级为：

```text
reproducible technical report / bounded case study
```

而不是继续声称“新方法”或“重大创新”。

---

# 10. 你现在最应该先看的三个文件

如果不想被大量文件分散，先只看这三个：

1. `research-os/reports/project-current-state-summary-zh.md`（本文件）
2. `research-os/drafts/wlwxb-submission-draft-v0.2-zh.md`
3. `research-os/plans/evidence-sensitivity-stress-test-experiment-plan-zh.md`

这三个文件分别回答：

```text
现在到底在做什么
论文具体怎么写
接下来实验怎么做
```
