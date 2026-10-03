
## 无标签 moment-alignment TTA

进一步测试了只使用目标场景无标签特征统计的 moment alignment：

```text
全目标场景统计：
ExtraTrees： 0.5986 → 0.6369
HGB：        0.5335 → 0.6529
```

然后改为只使用目标场景前缀，并在其余行评估：

```text
适应前缀比例       Macro-F1       Macro-FPR
0%                 0.5335         0.0820
5%                 0.6118         0.0697
10%                0.6354         0.0598
25%                0.5654         0.0532
```

10% 前缀是当前最有希望的窗口，但改善不稳定：malware8、malware34 仍然失败，malware42 仅小幅改善；25% 出现退化。因此不能将 moment alignment 写成已经验证的通用算法。

在 N-BaIoT 上用同一无标签 moment alignment 反而严重退化：

```text
ExtraTrees：0.8131 → 0.4862
HGB：       0.8076 → 0.1709
```

这说明简单的无标签均值/方差对齐高度依赖数据集和特征语义，不能直接跨生态复用。

## Quantile TTA：当前最强外部候选

将每个 source/target 场景的数值特征分别映射到 empirical quantile-normal space 后，结果进一步改善：

```text
单 seed、全目标统计：
ExtraTrees：0.5986 → 0.6782
HGB：       0.5335 → 0.6643
```

更严格的前缀适应实验（5 seeds × 6 scenario folds）：

```text
HGB source-only：       mean Macro-F1 = 0.5288，mean FPR = 0.0816
HGB + 10% quantile：    mean Macro-F1 = 0.7297，mean FPR = 0.0444
```

每个 seed 的 HGB Macro-F1（source → 10% quantile）：

```text
0.5335 → 0.7433
0.5698 → 0.7036
0.5392 → 0.8040
0.4615 → 0.7487
0.5396 → 0.6491
```

这是当前 IoT-23 上最有希望的无标签适应候选，但仍不能宣称通用新算法。相同 quantile TTA 在 N-BaIoT 五种子上反而退化：

```text
ExtraTrees：0.8117 → 0.7891
HGB：       0.8066 → 0.7619
```

因此它表现为明显的数据集条件性：对 IoT-23 场景 shift 有效，对 N-BaIoT device shift 不应启用。

相关脚本和结果：

- `research-os/tools/run_iot23_moment_tta.py`
- `research-os/tools/run_iot23_prefix_tta.py`
- `research-os/tools/run_iot23_quantile_tta.py`
- `research-os/tools/run_iot23_prefix_quantile_tta.py`
- `research-os/tools/run_nbaiot_quantile_tta_tree.py`
- `research-os/artifacts/iot23-moment-tta-results.json`
- `research-os/artifacts/iot23-prefix-tta-results.json`
- `research-os/artifacts/iot23-quantile-tta-results.json`
- `research-os/artifacts/iot23-prefix-quantile-tta-results.json`
