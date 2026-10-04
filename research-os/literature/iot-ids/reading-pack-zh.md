# IoT IDS 论文阅读包（中文导读）

本阅读包面向当前研究：**device-held-out IoT IDS、域泛化和 source-free tabular TTA**。

## 先读顺序

如果每天只能读 1 篇，按此顺序：

1. N-BaIoT 原始论文；
2. DANN；
3. CORAL；
4. GroupDRO；
5. Tent；
6. EATA；
7. AdapTable；
8. PFT3A；
9. CoTTA。

不要一开始阅读大量普通 CNN-LSTM IoT IDS 论文。它们多数只做随机行切分，和当前的设备留出问题不直接对应。

## A. 数据集与问题基线

### 1. N-BaIoT：Network-based Detection of IoT Botnet Attacks Using Deep Autoencoders

- 原文 PDF：<https://arxiv.org/pdf/1805.03409>
- 本地 PDF：`research-os/.cache/literature/reading-pack/nbaiot-1805.03409.pdf`
- 本地原文文本：`research-os/.cache/literature/reading-pack/nbaiot-1805.03409.txt`

核心内容：

- 9 个真实 IoT 设备；
- Mirai 和 BASHLITE 流量；
- 以网络行为 snapshot 建立设备正常行为模型；
- 每个设备训练深度自编码器；
- 重构误差用于异常检测。

必须注意：原论文的“每设备一个模型”不等于当前的 supervised multi-class device-LODO 协议。阅读时重点看：

1. 设备如何采集；
2. 训练/测试是否跨设备；
3. 标签是攻击/正常还是攻击类别；
4. snapshot 如何构造；
5. 结果是否依赖设备专属模型。

### 2. IoT-23 官方数据说明

- owner page：<https://www.stratosphereips.org/datasets-iot23>
- 官方场景目录：<https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/>

IoT-23 的官方身份是 scenario/capture，而不是统一 row-level device ID。当前项目只能把它用于 scenario-held-out 外部验证，不能写成第二个 device-held-out 数据集。

## B. 域泛化训练方法

### 3. DANN：Domain-Adversarial Training of Neural Networks

- 原文 PDF：<https://jmlr.org/papers/volume17/15-239/15-239.pdf>
- 本地 PDF：`research-os/.cache/literature/reading-pack/dann-jmlr.pdf`

核心内容：

- 特征编码器和任务分类器；
- 域分类器通过 gradient reversal 迫使特征域不可区分；
- 使用 source label 和 domain label；
- 主要是 training-time domain adaptation。

你需要理解：

```text
DANN ≠ test-time adaptation
DANN 需要训练阶段的域信息
域不可区分 ≠ 分类性能一定提高
```

当前 N-BaIoT 实验中 DANN 没有稳定超过普通 MLP，因此不能改名为新方法。

### 4. Deep CORAL

- 原文 PDF：<https://arxiv.org/pdf/1607.01719>
- 本地 PDF：`research-os/.cache/literature/reading-pack/coral-1607.01719.pdf`

核心内容：

- 对齐 source 和 target 的二阶统计量；
- 通过协方差差异构造 CORAL loss；
- 不需要目标标签。

你需要理解：

- 对齐统计量不保证类别边界保持；
- 对齐过强可能损失判别特征；
- 当前项目的 CORAL 结果没有稳定优于 MLP。

### 5. GroupDRO

- 原文 PDF：<https://arxiv.org/pdf/1911.08731>
- 本地 PDF：`research-os/.cache/literature/reading-pack/groupdro-1911.08731.pdf`

核心内容：

- 把数据划分为预先定义的 groups；
- 优化最差 group 的训练损失；
- 目标是避免模型只在平均数据上好，而在少数 group 上失败；
- 需要训练阶段的 group identity。

当前项目可以把 device 作为 group，但 GroupDRO 首轮没有稳定改善。重点阅读它对正则化、早停和 worst-group generalization 的讨论。

## C. Test-Time Adaptation

### 6. Tent

- 原文 PDF：<https://arxiv.org/pdf/2006.10726>
- 本地 PDF：`research-os/.cache/literature/reading-pack/tent-2006.10726.pdf`

核心内容：

- 只使用无标签测试 batch；
- 最小化预测熵；
- 更新 normalization statistics 和 affine 参数；
- 不访问 source data。

当前项目的 Tent 结果说明：视觉领域的 entropy minimization 不能直接假设适用于 IoT 表格流量。

### 7. EATA

- 原文 PDF：<https://arxiv.org/pdf/2204.02610>
- 本地 PDF：`research-os/.cache/literature/reading-pack/eata-2204.02610.pdf`

核心内容：

- 只选择可靠样本；
- 排除高熵样本；
- 避免重复样本造成不稳定更新；
- 减轻 catastrophic forgetting。

这篇对当前研究最重要的部分是：为什么不是所有目标样本都适合用于 adaptation。未来若设计 safe TTA，应先复现其 gating 思路，再考虑 IoT-specific 改动。

### 8. CoTTA

- 原文 PDF：<https://arxiv.org/pdf/2203.13591>
- 本地 PDF：`research-os/.cache/literature/reading-pack/cotta-2203.13591.pdf`

核心内容：

- continual test-time adaptation；
- teacher/student 或 weight-averaged 模型；
- 处理动态变化目标域；
- 重点解决伪标签错误累积和遗忘。

注意：CoTTA 主要是视觉实验。当前工作不能只引用 CoTTA 就声称已经覆盖 IoT 场景。

## D. 表格 TTA 直接近邻

### 9. AdapTable

- 原文 PDF：<https://arxiv.org/pdf/2407.10784>
- 本地 PDF：`research-os/.cache/literature/reading-pack/adaptable-2407.10784.pdf`

核心内容：

- 面向 tabular distribution shift；
- shift-aware uncertainty calibrator；
- label distribution handler；
- source-free tabular TTA。

这是当前研究必须认真对比的直接近邻。不能把“uncertainty gate + label prior”直接重新命名为原创。

### 10. PFT3A：Prior-Free Tabular Test-Time Adaptation

- ICLR 2026 官方 PDF：<https://proceedings.iclr.cc/paper_files/paper/2026/file/718dd6fa696c6303ca13ad81836014ee-Paper-Conference.pdf>
- 本地 PDF：`research-os/.cache/literature/reading-pack/pft3a-iclr2026.pdf`
- 官方代码：<https://github.com/rundohe/PFT3A>

核心内容：

- prior-free tabular TTA；
- Class Prior Estimating；
- Robust Feature Learning；
- Representative Subspace Exploration；
- 同时处理 label shift 和 feature shift；
- 不访问 source data 和 source class prior。

这是当前候选算法最重要的 novelty boundary。任何“表格 TTA + 类别先验 + 特征对齐”的设计都必须和 PFT3A 逐模块比较。

## E. 当前项目结果应该如何对照

| 方法 | 当前结果 | 可写结论 |
|---|---|---|
| MLP | N-BaIoT mean LODO Macro-F1 约 0.6465 | 基线 |
| DANN | 约 0.6518 | 没有稳定优势 |
| CORAL | 无稳定优势 | 不可称新方法 |
| GroupDRO | 无稳定优势 | group robustness 尚未解决问题 |
| Tent/BN TTA | 当前 N-BaIoT 退化 | tabular TTA 需要谨慎 |
| ExtraTrees + HGB | N-BaIoT 约 0.8107 | 有效升级 baseline |
| IoT-23 quantile TTA | 5 seeds HGB 约 0.7297 | scenario shift 下的条件性正结果 |
| N-BaIoT quantile TTA | 退化 | 不能称通用 TTA |

## 每篇论文必须回答的 8 个问题

1. 它的 domain/group 是什么？
2. 目标域标签是否被使用？
3. adaptation 是否看到目标测试样本？
4. 是 offline training-time 还是 online test-time？
5. split 是否按行、时间、设备或场景？
6. 是否报告 Macro-F1、FPR、per-class F1？
7. 是否报告资源开销和失败案例？
8. 它和当前候选方法具体重叠在哪里？

## 当前建议

先读前 8 篇并填写对照表，再决定论文贡献。当前最可能的诚实论文贡献是：

```text
严格设备/场景留出协议
+ 多种 DG/TTA 方法的统一比较
+ 条件性适应收益和 failure interval 分析
```

除非 quantile TTA 或新的 gating 方法能在 N-BaIoT 和第二个合格数据集上稳定有效，否则不要把它写成通用新算法。
