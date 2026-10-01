# Evidence Sensitivity Stress Test：实验方向计划

**目标：** 将当前 pilot 转换为一份边界严格、可复现、可停止的 methods/report，而不是继续扩张为漏洞检测或 provenance 产品。

**当前状态：** `submission_ready_bounded_report_high_level_novelty_unconfirmed`。

## A. 总体原则

1. 每个案例单独定义 claim；不合并真值、指标或 closure rate。
2. tier 是 claim-specific 的 evidence disclosure order，不假设所有 tier 天然单调。
3. 所有 `conditional` / `not_identifiable` 必须保持弃权，不转成漏洞状态。
4. 先冻结 packet、state rule、ablation order，再审查；规则修改必须作为独立 protocol-refinement 轮次。
5. 任何近邻或实验结果证明该方向只是已有工作重命名时，停止高层 novelty 叙事。

## B. 阶段 0：预注册冻结

### B1. OpenWrt

固定：

- population：新的 non-kernel package release pair population；
- selection：identity-key SHA-256，不读取 closure outcome；
- claim：指定为 source-evidence binding claim，不写 artifact safety、affectedness 或 remediation truth；
- tier：T0 name/version、T1 package/target、T2 ancestry/pre-exclusion、T3 any-path blob、T4 all-path blob；
- changed-path、rename、delete、Makefile、patch folding 的处理规则；
- state rule：identified / conditional / not_identifiable；
- lineage review 的 admissible evidence；
- reviewer 盲化范围和停止条件。

### B2. N-BaIoT

固定：

- claim：九组六类别镜像中的 device-independent evaluation；
- population：已归档的 common-support rows，不重新挑选窗口；
- tier：random-row、common-support、ordered-window、explicit LODO result；
- row offset 只能称 ordered window，不称 timestamp；
- device number 只能称 mirror group，不称 owner-verified identity；
- model、seed、metric、warning handling；
- 不加入 cross-dataset 或 leakage claim。

### B3. 公共停止条件

- 若 state rule 不能由两名 reviewer 独立应用，先停止并修订定义；
- 若只有“证据越多越好”而没有可解释 transition，停止；
- 若必须调用 CVE truth 或 artifact semantic truth 才能完成，停止；
- 若近邻全文显示同一 protocol 已被直接提出，停止 novelty claim。

## C. 阶段 1：新 OpenWrt outcome-blind cohort

### C1. 抽样

1. 从冻结 release population 建立新的 eligibility manifest；
2. 对 identity key 做 SHA-256 排序；
3. 按 stable family 固定抽取，不按已知 strict-fail 或 strict-pass 反选；
4. 生成 packet，不生成 aggregate state；
5. 保存输入 manifest、selection hash 和 source URLs/commit IDs。

### C2. 证据 packet

每个 packet 至少包含：

- package、target、pre/post release、remediation commit；
- source observation 原文；
- changed paths；
- pre/post ancestry observation；
- exact blob comparison observation；
- claim boundary 和 non-claims。

packet 不包含：

- `affected` / `not_affected`；
- precomputed strict/any aggregate label；
- reviewer gold answer；
- 依赖后验标签的 sample name。

### C3. 双审与 lineage adjudication

- Reviewer A、B 独立填写 T0–T4 state 和一条证据理由；
- 第三步只处理 disagreement，不重写原始评分；
- strict mismatch 只能触发 lineage review；
- lineage review 记录 recipe update、patch folding、rename、follow-up maintenance 等具体原因；
- 不允许把“找不到 exact blob”写成“漏洞未修复”。

### C4. 输出

- packet-level states；
- tier transition matrix；
- agreement 与 disagreement 类型；
- minimal support cut candidates；
- unresolved semantic cases；
- 不计算 CVE classification performance。

## D. 阶段 2：N-BaIoT protocol replication

### D1. 只重放既有镜像

- 不增加新镜像；
- 不声明官方 UCI final data；
- 不执行设备、固件或网络实验；
- 保持 common-support six labels；
- 保持两个 ordered windows 和五个 seeds；
- 保存每个 device fold 的 Macro-F1、每类 F1、warning 和失败状态。

### D2. Claim packet review

使用 v2 schema：

- T0/T1/T2：只能支持 conditional 或 not_identifiable；
- T3：必须有 packet 自身的显式 LODO result；仅有 protocol 描述时为 conditional；
- 不把第二数据集缺失写成“模型失败”；只写 external evidence unavailable。

### D3. 负结果和审查分歧

- 保留初始 16/20 ambiguity 作为 protocol refinement evidence；
- 保留第三轮 order replay 的 17/20 schema failure；
- 不能只报告修订后的 16/16；
- 主文同时报告“初始规则不充分”“顺序重放暴露 flat schema 缺陷”和“显式 tier schema 下重复性改善”；
- 不把任一 16/16 当总体 inter-rater reliability。

### D4. Tier schema robustness

- packet 必须包含显式 `tier_evidence`，不允许 reviewer 从 flat observations 反推 tier 内容；
- order-invariance replay 应在不改变 claim、数据和 state rule 的情况下反转 packet/tier 顺序；
- 若 v3 类似的 flat-schema disagreement 再出现，暂停扩样，先修订 schema；
- 将 schema failure 作为结果报告，不作为异常删除。

## E. 阶段 3：跨案例 synthesis

### E1. 允许的共同结构

只比较：

```text
claim wording
→ evidence tier
→ state rule
→ transition
→ reviewer agreement
→ stop condition
```

### E2. 禁止的合并

- 不合并 OpenWrt pair counts 与 N-BaIoT F1；
- 不计算一个跨案例“平均敏感性”；
- 不声称共同 ground truth；
- 不把 source retention 和 device generalization 写成同一安全属性。

### E3. taxonomy test

候选 taxonomy：

1. identity：对象/设备/包是否被正确界定；
2. independence：训练—测试或 source—release 是否有独立性证据；
3. binding：commit/row identity 是否绑定到 release/held-out group；
4. externality：是否有独立来源或第二数据集支持。

若评审者认为这些只是 generic provenance completeness，必须将跨案例 taxonomy 降级为解释框架，不作为创新贡献。

## F. 阶段 4：近邻和稿件质量门

### F1. 必须完成

- Prospector / Finding Fixes 全文边界已记录；
- package patch-sharing 全文边界已记录；
- Macaron 至少取得公开摘要、官方文档和 provenance tutorial；若无法取得全文，稿件必须明确“不完全排除”；
- CVECenter 至少取得作者公开描述；全文缺失必须显式列为 limitation；
- 最近两年 IoT split audit 与 Linux vulnerability-management 论文逐条写出 overlap matrix。

### F2. 投稿前 reviewer checklist

审稿人应能回答“是”：

- claim 是否固定？
- tier 是否可由外部读者重算？
- state 是否不是 CVE label？
- negative / disagreement 是否保留？
- 每个数字是否有 artifact 和生成脚本？
- 是否没有把 exact blob 当作语义修复证明？
- 是否明确 Prospector/Macaron/package-sharing 的边界？
- 是否有停止条件？

## G. 阶段 5：论文版本和发布门

### G1. Draft v0.1

包含：

- abstract；
- formal protocol；
- two case packets；
- results tables；
- disagreement/refinement subsection；
- nearest-work boundary；
- threats and stop conditions；
- reproducibility index。

当前初稿：

`research-os/drafts/evidence-sensitivity-stress-test-methods-report-draft-zh.md`

### G2. Draft v0.2 触发条件

只有以下条件同时满足才写 v0.2：

1. 新 OpenWrt cohort 至少完成一次 outcome-blind dual review；
2. N-BaIoT v2 packet schema 在第三次独立重放中没有新增语义分歧；
3. lineage review 的 failure categories 可以由两名 reviewer 独立复现；
4. 文献 audit 没有发现同一 protocol 的直接先例；
5. 所有主张仍能在不使用漏洞真值的情况下成立。

### G3. 停止/降级门

若任一条件发生：

- 新 cohort agreement 明显下降且无法通过预先规则解释；
- strict retention 的主要变化来自 source history artifact，而非 claim evidence；
- taxonomy 只剩 generic provenance/split audit；
- Macaron 或其他近邻明确已经测量同一 state transition；
- 需要新增 vulnerability labels 或执行设备/固件；

则将稿件降级为：

```text
reproducible technical report / negative replication note
```

不再使用“novel methodology”标题。

## H. 交付顺序

1. 完成并审校当前 methods/report draft；
2. 生成新的 OpenWrt outcome-blind cohort；
3. 做 dual review 与 lineage adjudication；
4. 重放 N-BaIoT v2 packet schema；
5. 更新 overlap matrix；
6. 运行 manuscript claim lint；
7. 由外部读者式 reviewer 做一次只读 adversarial review；
8. 只有通过所有门，才选择合法、低负担、范围匹配的 venue。
