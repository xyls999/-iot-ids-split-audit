# Evidence Sensitivity Stress Test：pilot 结果

**状态：**探索性机械 pilot；不是 v3、不是 CVE 标签、不是方法效果评估。

## 预先固定的机械规则

输入为既有 62-pair expanded scout 的全部记录。为避免后验挑样，pilot 子集按固定 identity key 的 SHA-256 排序，每条稳定线取前 2 条，得到 12 条；选择规则不读取 closure outcome。完整 62 条仍用于描述性 tier transition。

证据阶梯：

```text
T0  name/version record
T1  package/target presence（侦察规则的入选条件）
T2  post ancestor + pre exclusion
T3  any changed-path exact blob retained
T4  all changed-path exact blobs retained
```

这些是 source-evidence signals，不是 `affected`/`not_affected` 标签；T4 也不等价于语义修复证明。

机器可读输出：`research-os/artifacts/openwrt-evidence-sensitivity-pilot.json`。
生成工具：`research-os/tools/run_evidence_sensitivity_probe.py`。

## OpenWrt 结果

| evidence tier | 支持 signal 的 pair |
|---|---:|
| T0 name/version | 62/62 |
| T1 package/target presence | 62/62 |
| T2 ancestry + pre exclusion | 62/62 |
| T3 any changed-path blob | 54/62 |
| T4 strict all changed-path blobs | 50/62 |

状态转移：

```text
T2 → T3 降级：8/62
T3 → T4 进一步降级：4/62
T2 → T4 总降级：12/62
```

这证明了一个**可操作的证据敏感性现象**：把 ancestry-only signal 换成更强的 artifact-retention signal，会使 12/62 个单位失去 strict support。它不证明 remediation 缺失；已知 lineage spot check 显示 recipe/version update、patch folding 和后续维护提交都可能造成 exact-blob 不同。

## 与 N-BaIoT 的协议连接

已有 `reports/nbaiot-common-support-audit-report.md` 报告了另一种 evidence-boundary stress test：

- Random Forest random-row 与 leave-one-device-out Macro-F1 在两个 ordered windows、五个 seeds 上相差 **5.0–9.6 percentage points**；
- 报告明确禁止将该差异称为新模型、泄漏证明或跨数据集泛化；
- 它表示当 device identity / grouped split 证据被加强时，原有“泛化”叙述发生敏感性变化。

两个案例尚不能合并成一个数值指标。当前能共享的只是 protocol shape：

```text
claim packet
→ predeclared evidence tier
→ evidence ablation/downgrade
→ claim-state or outcome transition
→ independent review / stop rule
```

## Pilot 可行性判断

### 已验证

1. OpenWrt 的 evidence tiers 能从已有官方-source-derived records 机械计算；
2. 不依赖 CVE 标签，不改变 v2 冻结样本；
3. 固定 hash 规则可以产生 outcome-blind 12-pair pilot subset；
4. T2→T4 存在非平凡 transition，而不是 62/62 全部一致；
5. N-BaIoT 已有独立的 split/evidence sensitivity signal，可作为第二案例协议输入。

### 尚未验证

1. 两名独立审查者是否会对 claim-state transition 达成稳定一致；
2. 两案例是否共享超出“都需要 provenance”的 failure taxonomy；
3. 该 protocol 是否比已有 assurance-case、dataset audit、artifact evaluation 和 provenance framework 提供额外解释力；
4. strict exact-blob 之外的 semantic lineage review 是否能形成可重复规则。

## 当前结论

```text
机械 feasibility：PASS
新颖性：未证明
可投稿性：未证明
下一关：盲化 packet review + semantic lineage adjudication
```

若人工 pilot 只能重复“证据越多越好”，或审查一致性低，则停止该方向。若能稳定识别不同领域的最小必要证据 cut set，并且现有框架不能直接表达这种 transition，才允许独立预注册。
