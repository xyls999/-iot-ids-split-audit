# IoT-23 外部场景留出实验（2026-10-01）

## 定位

这是第二个公开 IoT 数据集上的外部验证，但必须严格称为 **scenario-held-out**，不是 device-held-out：IoT-23 官方证据确认了每个 capture scenario 的组身份和 benign/malicious 场景信息，但不提供可跨场景共用的 row-level device identity。

官方来源：

- owner page：<https://www.stratosphereips.org/datasets-iot23>
- 官方逐场景目录：<https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/>
- 许可：CC BY 2.0

本次仅下载了 8 个小型官方 `bro/conn.log.labeled` 文件，总大小约 5.9 MB；没有下载 8.7 GB 总包或 PCAP。

## 协议

- 6 个同时包含 benign/malicious 的场景作为外层 scenario folds：8、20、21、34、42、44；
- 4、5 作为额外 benign 训练数据；
- 每个场景每个类别最多取 1000 行；
- held-out 场景不参与训练；
- 排除 `ts`、`uid`、源/目的 IP，避免直接场景或端点 shortcut；
- 数值特征：端口、持续时间、字节、包数、IP 字节数等；
- 类别特征：proto、service、conn_state、history；
- 模型：ExtraTrees、HistGradientBoosting；
- 指标：Macro-F1、FPR。

## 结果

```text
ExtraTrees：              mean Macro-F1 = 0.5986，mean FPR = 0.081
HistGradientBoosting：    mean Macro-F1 = 0.5335，mean FPR = 0.082
```

ExtraTrees 各场景 Macro-F1：

```text
malware8：   0.3333
malware20：  0.9836
malware21：  0.9812
malware34：  0.3225
malware42：  0.3621
malware44：  0.6086
```

## 解释

结果显示，N-BaIoT 上的树集成提升不能直接外推到 IoT-23 场景。不同捕获场景之间存在明显 distribution shift：

- malware20/21 上表现很高；
- malware8/34/42 上明显失败；
- 单一总体均值会掩盖严重的场景 failure interval。

这不是算法“失败无价值”，而是说明当前树集成主要是 **N-BaIoT device-held-out 的有效升级 baseline**，尚不足以支持跨数据集泛化或论文级新算法主张。

## 当前结论

```text
N-BaIoT device-held-out：树集成明显有效
IoT-23 scenario-held-out：树集成不稳定
跨数据集泛化：尚未成立
第二数据集 device-held-out：仍不成立（IoT-23 只能作 scenario proxy）
```

不能把 IoT-23 的 scenario 重新命名为 device，也不能把场景间性能差异写成因果机制。

## 可复现实验

脚本：`research-os/tools/run_iot23_scenario_heldout.py`

数据 manifest（含官方 URL、字节数和 SHA-256）：

`research-os/data/iot23-small-manifest.json`

结果：

`research-os/artifacts/iot23-scenario-heldout-results.json`
