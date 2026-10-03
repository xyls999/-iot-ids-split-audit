
## 嵌套设备留出调参

为避免使用目标设备调参，新增嵌套协议：每个外层 held-out device 内，在其余 8 个设备上进行内层设备验证，从以下候选选择配置，再用全部外层训练设备重训：

- ExtraTrees（sqrt / half / leaf=2）；
- HistGradientBoosting（31 / 63 leaves）；
- ExtraTrees + HGB 概率集成（权重 0.5 / 0.7）。

单个固定 seed 的外层结果：

```text
nested outer mean Macro-F1 = 0.81719
std = 0.10613
```

固定集成的五种子结果为 0.81068，因此嵌套选择没有依赖目标设备标签，并且在该 seed 上略有改善。选择结果：

```text
device 1: HGB31       0.8499
device 2: ET sqrt      0.6605
device 3: blend 0.5    0.7807
device 4: ET leaf2     0.7503
device 5: blend 0.5    0.7597
device 6: HGB63       0.9969
device 7: blend 0.7    0.8131
device 8: blend 0.7    0.9908
device 9: blend 0.7    0.7527
```

注意：nested tuning 的 0.81719 目前只有一个 outer seed，不能替代五种子稳定性结论；固定集成的 0.81068 仍是更保守的主要结果。

新增脚本：`research-os/tools/run_nbaiot_nested_tree_tuning.py`
新增证据：`research-os/artifacts/nbaiot-nested-tree-tuning.json`

## 无标签 moment alignment 的反例

将 IoT-23 上的无标签 target moment alignment 直接迁移到 N-BaIoT 后，结果明显恶化：

```text
ExtraTrees source-only：       0.8131
ExtraTrees moment alignment：  0.4862
HGB source-only：              0.8076
HGB moment alignment：         0.1709
```

因此均值/方差对齐不是通用升级算法；它可能破坏 N-BaIoT 中有判别力的绝对流量尺度。该失败结果保留，不能只报告 IoT-23 的正向窗口。
