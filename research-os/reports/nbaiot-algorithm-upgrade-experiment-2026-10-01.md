# N-BaIoT 算法升级实验（2026-10-01）

## 结论

在冻结的 common-support、device-held-out 协议下，当前最有效的升级不是 TTA 或 DANN，而是树模型和异构树集成：

```text
5 seeds × 9 held-out devices

MLP：                 mean Macro-F1 = 0.6465
DANN-style MLP：      mean Macro-F1 = 0.6518
ExtraTrees + HGB：    mean Macro-F1 = 0.8107
```

树集成相对 MLP 的绝对提升约为 **0.1642 Macro-F1**。这说明树模型是当前有效工程升级候选，但“树模型集成”本身不能直接作为新算法创新。

## 协议

- 数据：本地 N-BaIoT Kaggle-layout mirror；
- 每设备×类别取 600 行 common-support 样本；
- 9 个设备逐一 device-held-out；
- held-out device 不参与训练；
- 5 个随机种子：20260930–20260934；
- 指标：Macro-F1、Macro-FPR、每类 F1；
- 约束：离线、防御性，不运行固件、PoC 或设备。

## 方法比较

### Test-time adaptation 预研

在目标设备前 K 个无标签 batch 上进行适应：

- BN statistics adaptation；
- Tent；
- entropy-gated Tent；
- target z-score / robust normalization；
- BN statistics blending。

结果：当前协议下均未超过 source-only MLP。典型结果（8 epochs）：

```text
K=5 source-only：0.6507
K=5 BN adaptation：0.6054
K=5 Tent：0.6055
K=5 BN blend：0.6400
K=5 target z-score：0.5541
K=5 target robust：0.2323
```

因此目前不能把 TTA 称为有效升级；它在部分设备上发生明显退化。

### 训练时域泛化候选

在一次 8 epoch 预研中：

```text
MLP：       0.6685
CORAL：     0.6656
GroupDRO：  0.6438
Mixup：     0.6672
```

在 20 epoch 预研中：

```text
MLP：       0.6500
CORAL：     0.6506
GroupDRO：  0.6465
Mixup：     0.6523
```

没有稳定优于 MLP 的证据。

### 异构树集成

最终候选使用：

```text
ExtraTreesClassifier
+
HistGradientBoostingClassifier

预测时平均两者 class probabilities
```

5 seeds × 9 folds 的结果：

- mean LODO Macro-F1：**0.81068**；
- std：0.10592；
- mean LODO Macro-FPR：**0.03032**；
- 最低 fold Macro-F1：0.61269；
- 最高 fold Macro-F1：0.99750。

按 held-out device 的平均 Macro-F1：

```text
device 1: 0.765
device 2: 0.763
device 3: 0.780
device 4: 0.780
device 5: 0.759
device 6: 0.997
device 7: 0.811
device 8: 0.987
device 9: 0.653
```

因此提升并非所有设备均匀发生，device 9 仍是困难设备，不能只报告总体均值。

## 资源记录

树集成脚本同时记录：

- 每 fold 训练时间；
- 集成推理时间；
- ExtraTrees 总节点数；
- HGB 迭代次数。

脚本：`research-os/tools/run_nbaiot_tree_ensemble.py`

结果：`research-os/artifacts/nbaiot-tree-ensemble-results.json`

TTA 脚本：`research-os/tools/run_nbaiot_tta_preflight.py`

TTA 结果：`research-os/artifacts/nbaiot-tta-preflight-8ep-v3.json`

## 解释边界

当前结果支持：

- 异构树集成在这个冻结 LODO 协议下明显优于当前 MLP/DANN baseline；
- TTA、CORAL、GroupDRO、Mixup 在当前预研配置下没有稳定优势；
- 设备间性能差异很大，device-held-out 仍然必要。

当前结果不支持：

- 树集成具有算法学术创新；
- 跨数据集泛化；
- 因果解释；
- 真实在线设备部署性能；
- 改善来自某个特定模块而不是模型族差异。

## 下一步

1. 对树集成与 MLP 运行统一的 per-class F1、FPR 和延迟审计；
2. 在第二个有可核验 group identity 的 IoT 数据集复现；
3. 对树集成进行固定验证集上的超参数选择，避免用 held-out device 调参；
4. 只有在树集成仍存在稳定 failure interval 后，才设计 IoT-specific 新算法；
5. 暂不把 TTA、DANN、CORAL、GroupDRO 或 Mixup 命名为新方法。
