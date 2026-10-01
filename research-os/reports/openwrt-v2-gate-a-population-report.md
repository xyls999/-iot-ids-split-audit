# OpenWrt v2 抽样框：Gate A 总体完整性报告

**日期：**2026-10-01  
**Gate A 结论：通过。**

## 固定总体

按照 `plans/openwrt-broader-sampling-frame-v2-zh.md`，从 OpenWrt 官方发布目录枚举了：

```text
22.03.0–22.03.7   （8 个）
23.05.0–23.05.6   （7 个）
24.10.0–24.10.8   （9 个）
总计：24 个 final numeric release
```

每个 release 固定两个 target：

```text
x86/64
ath79/generic
```

因此预期 release-target 单元为 `24 × 2 = 48`。每个 tag 的 peeled source commit 与 commit 时间记录在：

```text
data/openwrt-v2-release-population.yaml
```

所有 24 个 tag 的 peeled commit 时间均不晚于 `2026-10-01T00:00:00Z`。此时间是可复现的保守 inclusion proxy，不声称它等于所有官方发布公告的精确时间。

## 已冻结的官方小型元数据

对 48 个 release-target 单元，已下载并保留：

```text
manifest
config.buildinfo
feeds.buildinfo
version.buildinfo
sha256sums
CycloneDX BOM（仅官方目录存在时）
```

结果：

| 项目 | 数量 |
|---|---:|
| 固定 release-target 单元 | 48 |
| 已验证 metadata 文件（不含 sha256sums 本身） | 222 |
| 官方未提供 BOM 的单元 | 18 |
| checksum 不匹配文件 | 0 |
| 快照总大小 | 11,925,709 bytes |

校验机器结果：

```text
research-os/artifacts/openwrt-v2-metadata-verification.json
metadata_files_checked: 222
all_match: true
```

完整下载索引：

```text
data/openwrt-v2-snapshots/collection-index.tsv
```

## 解释边界

- “manifest 中有包”支持该官方 target 构建清单包含此 package；不支持任意真实设备已部署或正在运行该包。
- 18 个早期/对应 target 未发布 BOM 的记录保留为 `not_published`，没有用其他 target 替代。
- 此 Gate A 只证明总体与输入冻结完整；不产生 CVE 候选、人工标签、方法比较或效果结论。

## Gate A 决策

```text
总体枚举：通过
固定 target 文件收集：通过
发布 sha256sums 校验：通过
进入下一阶段：允许建立 CVE 候选登记册
仍然禁止：评分代码、性能指标、投稿结论
```
