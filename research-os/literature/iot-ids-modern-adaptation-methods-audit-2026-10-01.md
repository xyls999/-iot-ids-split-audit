# IoT IDS 现代算法方向审查：设备 shift 与 test-time adaptation

## 结论先行

当前最值得做的算法方向不是再堆一个 CNN/Transformer，而是：

> **在未见设备的无标签数据流上做资源受限的 test-time adaptation（TTA），并用严格 LODO 评估。**

但这个方向已经有明显近邻，不能直接称为新颖：PFT3A、AdapTable、TabLog、FTAT、Tent/EATA、持续 TTA 和 IoT domain adaptation 都已覆盖大量组件。

## 1. 为什么这个环境区间有价值

N-BaIoT 提供了一个可离线重放的受限环境：

```text
source：8 个设备组的有标签流量
adaptation：第 9 个未见设备的无标签前 K 个 batch
evaluation：同一未见设备的后续有标签 batch
```

这个区间比普通随机切分更接近实际部署：模型先在已有设备上训练，接入新设备后只能看到无标签网络流量，不能立即取得人工标签。

可研究的具体变量：

- adaptation batch 数量 K：0、1、5、10；
- 设备 shift 强度：按 device-held-out fold；
- label prior shift：不同攻击类别比例；
- feature shift：不同设备的 115 维流量统计变化；
- 资源预算：每 batch 更新参数数量、CPU 时间、内存；
- 安全风险：entropy collapse、class collapse、灾难性遗忘。

## 2. 已有现代方法

### 2.1 PFT3A（ICLR 2026）

全文：本地缓存 `pft3a-tabular-tta.pdf`；官方实现：<https://github.com/rundohe/PFT3A>

PFT3A 针对 prior-free tabular TTA，包含：

- Class Prior Estimating；
- Robust Feature Learning；
- Representative Subspace Exploration。

它明确指出视觉 TTA 直接用于表格数据表现较差，并在五个 tabular datasets 上比较 Tent、EATA、CoTTA、FTAT 等方法。论文报告其平均 Acc、BAcc 和 F1 的改善。

**重叠风险：高。**

当前项目不能把“tabular TTA + class prior + feature alignment”直接作为创新。

### 2.2 AdapTable（2024）

PFT3A 参考文献将其描述为 shift-aware uncertainty calibrator 和 label-distribution handler。它处理 tabular test-time adaptation 和 label shift。

**重叠风险：高。**

### 2.3 TabLog（ICML 2024）

使用逻辑规则进行 tabular test-time adaptation，重点是从表格数据中识别可迁移规则。

**重叠风险：中—高。**

### 2.4 FTAT / ODS

PFT3A 将 FTAT 描述为 source-free 的 tabular TTA 方法，将标签分布优化、低置信样本过滤和 online ensemble 结合；ODS 处理 open-world data shift。

**重叠风险：高。**

### 2.5 Tent、EATA、CoTTA、SAR 类方法

这些是通用 TTA/continual TTA 基线，已经成为现代 adaptation 实验的常见比较对象。不能只与普通 MLP 和 DANN 比较。

### 2.6 IoT domain adaptation

已有 IoT 文献包括：

- MMD-style IoT attack transfer；
- geometric graph alignment；
- adversarial domain adaptation；
- heterogeneous domain adaptation；
- GroupDRO、ANDMASK、Mixup 的 IoT domain-generalization benchmark；
- TriHID（ESWA 2025）等可验证 domain-adaptation IoT IDS。

**结论：** “设备域适配”本身不是空白。

### 2.7 资源受限 TTA

EmbodiTTA / on-demand TTA 等近期工作将关注点放在：

- 持续适配的 memory/energy 负担；
- 何时触发 adaptation；
- 边缘设备的资源限制。

这给 IoT 方向提供了一个更实际的切入点：不要只报告 F1，要报告 adaptation cost 和是否发生错误更新。

## 3. 最值得验证的窄方向

当前推荐的研究假设不是“提出全新的 TTA”，而是先验证：

> 在 N-BaIoT 的未见设备流量中，**uncertainty-gated、class-safe、resource-aware TTA** 是否能在特定 shift 区间改善 LODO Macro-F1，同时减少 entropy collapse 和误报恶化？

可能的候选流程：

```text
source-trained lightweight MLP
→ detect distribution shift
→ only update normalization / adapter parameters
→ use uncertainty gate
→ constrain class-prior drift
→ stop adaptation when confidence collapses
```

这只是算法假设，不是已确认创新。

## 4. 必须先做的基线

至少包括：

1. no adaptation；
2. BN/statistics adaptation；
3. Tent；
4. EATA 或 SAR；
5. CoTTA/continual TTA；
6. FTAT；
7. PFT3A；
8. DANN/CORAL/GroupDRO 作为训练时 adaptation 对照。

指标：

- LODO Macro-F1；
- per-class F1；
- FPR；
- adaptation gain；
- first-batch / later-batch curve；
- update count；
- CPU time；
- parameter count；
- catastrophic forgetting；
- class-collapse rate。

## 5. 何时才允许命名新算法

只有当一个候选方法同时满足：

1. 在至少 5 个 seeds、两个 ordered windows 上改善 LODO；
2. 在多个 held-out devices 上改善，而不是只改善一台；
3. 优于 PFT3A、FTAT、Tent/EATA 等现代基线；
4. 资源成本不超过可接受预算；
5. 不依赖目标标签；
6. 不依赖未经验证的时间戳；
7. 第二个具有 group identity 的数据集上至少保持方向一致；
8. 消融能说明每个模块的作用；

才可以把它写成算法论文贡献。

## 6. 当前判断

```text
现代方向：source-free tabular TTA under unseen-device shift
研究价值：高于普通 MLP/DANN 堆叠
现有近邻：很多
当前创新：未确认
下一步：先完整跑现代 TTA baseline，不先命名算法
```
