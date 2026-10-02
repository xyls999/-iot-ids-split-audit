# N-BaIoT 算法路线预研结果

## 目的

为了判断是否能转成《物联网学报》更常见的算法论文，先比较：

1. 标准监督 MLP；
2. 带设备对抗头的 MLP（DANN-style baseline）。

这不是创新算法声明。设备对抗训练、域适配和域泛化已有大量近邻，当前实验只检验是否值得继续。

## 固定协议

- 数据：本地 Kaggle-layout N-BaIoT mirror；
- 9 个镜像设备组；
- 6 个共同支持类别；
- 每设备×类别 600 行；
- 115 个输入特征；
- Random Forest 既有结果作为背景，不与 MLP 混合；
- random-row 与 leave-one-device-out（LODO）；
- 20 个训练 epoch；
- 单一主 seed `20260930`；
- CPU-only PyTorch；
- 不做设备、固件或漏洞执行。

算法原型：

```text
MLP:
  115 → 64 → 32 → attack classifier

DANN-style:
  115 → 64 → 32 → attack classifier
                 ↘ gradient-reversal device classifier
```

## 结果

### 标准 MLP

```text
random-row Macro-F1：0.6994
mean LODO Macro-F1：0.6551
gap：0.0443
```

### DANN-style，gradient reversal λ=0.01

```text
random-row Macro-F1：0.6985
mean LODO Macro-F1：0.6467
gap：0.0519
```

### DANN-style，λ=0.05

```text
random-row Macro-F1：0.7000
mean LODO Macro-F1：0.6483
gap：0.0517
```

### DANN-style，λ=0.10

```text
random-row Macro-F1：0.6996
mean LODO Macro-F1：0.6497
gap：0.0499
```

### DANN-style，λ=0.20

```text
random-row Macro-F1：0.6997
mean LODO Macro-F1：0.6554
gap：0.0443
```

机器可读结果：

- `artifacts/nbaiot-device-robust-baselines.json`
- `artifacts/nbaiot-device-robust-baselines-grl-0.01.json`
- `artifacts/nbaiot-device-robust-baselines-grl-0.05.json`
- `artifacts/nbaiot-device-robust-baselines-grl-0.2.json`

脚本：`tools/run_nbaiot_device_robust_baselines.py`。

## 当前判断

当前 DANN-style 原型没有显示稳定优势：

- λ=0.01、0.05、0.10 时 LODO 低于标准 MLP；
- λ=0.20 时基本与标准 MLP 持平；
- 不能把“设备对抗训练”直接写成新算法；
- 不能把一次 MLP 结果写成最终性能结论。

这轮实验的价值是提前否决一个过于简单的算法路线，避免把已有 DANN/域适配重新命名成创新。

## 下一步算法实验

按以下顺序继续：

1. 复现现有方法作为 baseline：CORAL、GroupDRO、Mixup 或已有 MMD-style alignment；
2. 保持同一 common-support、LODO、两个 ordered windows 和资源指标；
3. 若现有方法不能稳定改善 LODO，停止“提出新模型”主张；
4. 若存在稳定缺口，再研究一个**受资源约束且 device-held-out 明确的组合方法**；
5. 新方法必须在至少第二个具有可核验 group identity 的数据集上验证，否则只能作为单镜像算法预研。

## 结论

```text
算法论文方向：仍可研究
当前算法原型：未显示优势
创新性：未确认
下一关：现有域泛化 baseline 对照
```
