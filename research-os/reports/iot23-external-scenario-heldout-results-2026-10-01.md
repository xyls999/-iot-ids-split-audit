
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

相关脚本和结果：

- `research-os/tools/run_iot23_moment_tta.py`
- `research-os/tools/run_iot23_prefix_tta.py`
- `research-os/artifacts/iot23-moment-tta-results.json`
- `research-os/artifacts/iot23-prefix-tta-results.json`
