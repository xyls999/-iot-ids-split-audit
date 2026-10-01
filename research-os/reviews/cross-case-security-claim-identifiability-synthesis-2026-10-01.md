# 跨案例综合：Security Claim Identifiability

**状态：**概念候选；当前 NO-GO，仅允许反证 pilot。

## 核心问题

把 N-BaIoT 与 OpenWrt 生硬合并没有意义：一个是网络流量 IDS，一个是发行包安全适用性。真正可能共享的不是领域，而是**结论支持结构**：

> 一个安全研究结论，是否能由与该结论独立的、可追溯的证据支持？

### 案例一：IDS 泛化结论

```text
claim: model generalizes across devices/time
support requirements:
  dataset identity → capture/device/time provenance
  split manifest → group/time independence
  label schema → semantic support
  test outcome → identifiable denominator
```

既有 N-BaIoT 审计已经发现：官方身份/时间信息不足、镜像行窗口不能升级为真实时间、随机行 split 与 device-held-out 不能互换；因此只能写技术复现/案例报告。

### 案例二：发布安全声明

```text
claim: package-release-CVE applicability/remediation status
support requirements:
  advisory → CVE/package identity
  package → immutable source/binary artifact
  source → remediation revision
  source/materials → published binary
  binary → release/channel/variant
```

OpenWrt/Debian/Fedora 侦察显示：status、source、binary、release metadata 各自存在，不代表它们已经形成可重放的 join。

## 可能的共同输出

不是一个新的检测器，也不是 VEX/SLSA/SBOM 标准，而是一个**Claim Identifiability Audit**：

```text
identified          evidence supports the stated claim under frozen rules
conditional         some support exists but a named denominator/edge is missing
unidentified        the claim would require unsupported inference
not_evaluable       public evidence cannot establish the unit
```

每个案例都报告：

1. claim unit；
2. required evidence edges；
3. evidence level；
4. missing/ambiguous edge taxonomy；
5. whether the requested metric or verdict is mathematically identifiable。

## 与现有工作的差异（尚未证明）

- N-BaIoT 方向的普通 split/leakage audit 不是新方法；
- OpenWrt 的普通 provenance/applicability 也不是新方法；
- 数据集 provenance、artifact evaluation、SBOM/VEX、SLSA、GUAC、Macaron 都已覆盖各自领域的 provenance/assurance 组件；
- 该候选若有价值，只能是把 **claim identifiability** 作为共同测量对象，使用两个性质不同的 security case study 展示哪些结论无法由现有公开证据识别。

但这仍可能只是“可复现性/数据质量审计”的新命名。近期工作已研究 security artifact reproducibility、dataset audit、SBOM/VEX scanner consistency；因此不能把框架名称当创新。

## 诚实的最小反证 pilot

不做新模型，不冻结新漏洞标签，不将已有结果当真值。

### Case A：已有 N-BaIoT audit artifact

盲于既有结果，重新依据预先写好的 checklist 判断：

- capture/device/time identity 是否存在；
- split independence 是否可验证；
- label semantics 是否足以支持 metric denominator；
- claim 是否只能依赖 mirror row order。

已有报告只作待审计来源，不作 oracle。

### Case B：全新、非后验挑选的 OpenWrt/Debian/Fedora records

依据冻结哈希抽样规则记录 E1–E5 edge，不使用已有 strict-fail case 选择样本。

### 停止条件

- 两案例无法共享稳定的 evidence taxonomy；
- 结论只是“需要更多 provenance”；
- 既有 dataset-audit / artifact-evaluation 框架可无损表达全部结果；
- 审查者一致性低；
- 只能依赖已有标签或后验挑样。

## 当前决定

```text
跨案例 Claim Identifiability：NO-GO（概念尚未证明创新）
Security Update Evidence-Join：NO-GO（先前 CONDITIONAL-GO 过于乐观）
唯一允许动作：严格反证 pilot
若失败：停止 OpenWrt provenance 与 N-BaIoT 投稿主线
```

## 不能声称

- 不能声称提出了通用安全研究审计框架；
- 不能声称发现了数据泄漏、漏洞状态错误或发行版质量问题；
- 不能把 N-BaIoT 的技术复现结果与 OpenWrt 的探索性 evidence probe 合成方法效果；
- 不能将两个弱案例相加包装成创新。
