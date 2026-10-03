# 第二数据集审计复核：IoT-23 官方逐场景文件

复核发现：IoT-23 owner 页面链接的官方目录提供 `IndividualScenarios/<scenario>/bro/conn.log.labeled`，因此可以做小规模、可下载、可复现的 scenario-held-out 实验。

但该证据仍不改变原判定：scenario 是 capture-group identity，不是跨场景可比的 row-level device identity。恶意场景说明是在 Raspberry Pi 上运行 malware，良性场景是 Philips Hue、Amazon Echo、Somfy doorlock；这不能构成每个 row 的统一设备标签，也没有足够的 device×label common support。

因此：

- IoT-23 可作为 scenario/capture robustness 数据集；
- 不升级为第二个 device-held-out 数据集；
- 不把场景身份重命名为设备身份；
- 不把 IoT-23 结果与 N-BaIoT device LODO 指标合并。

本次使用的官方文件及 SHA-256 见：`research-os/data/iot23-small-manifest.json`。
