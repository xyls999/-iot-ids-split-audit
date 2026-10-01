# OpenWrt v2：CVE 候选登记册预检报告

**日期：**2026-10-01  
**阶段：**Gate A 已通过后的候选登记；尚未开始人工标签、方法 A/B 或效果计算。

## 为什么改用 Git 历史

OpenWrt Wiki 的 changelog/release-note 页面受机器人验证限制，直接读取无法证明页面覆盖完整。为避免把搜索索引片段当成穷尽性资料，本登记册改以 OpenWrt 官方 Git 稳定维护分支的 blob-less commit history 为来源：

```text
origin/openwrt-22.03: 4e1d1b7df0ce6fa96d7462dc883917682f428046
origin/openwrt-23.05: 33063b4ccf00d39393796499b23df55187b192dc
origin/openwrt-24.10: 97f7026b3dc97aff135da1ef3575c44cddcf8fb5
```

对 v2 总体中每一个固定 release tag 的可达历史，检索 commit message（subject 和 body）中的规范 `CVE-YYYY-NNNN...` 标识。每条记录都包含其所属 release tag、完整 commit SHA、commit subject、CVE ID 与 subject 的 package hint。

## 生成的登记册

| 文件 | 含义 |
|---|---|
| `data/openwrt-v2-cve-commit-registry.csv` | 所有由固定 release tag 可达、且 commit message 显式提及规范 CVE ID 的原始记录。 |
| `data/openwrt-v2-target-package-inventory.csv` | 从 48 个冻结 target manifest 解析出的 package/version 清单。 |
| `data/openwrt-v2-candidate-target-presence.csv` | 将 commit subject package hint 与同一 release 的 manifest package 做**精确字符串匹配**后的候选行；只表示 target package presence，绝不表示 CVE 适用性。 |
| `data/openwrt-v2-snapshots/cvelistV5/` | 固定到 CVE Program commit `5657707bc397bc80237e9aea2d7e01994208f1b2` 的单独 CVE JSON。 |

## 当前计数

```text
commit-message 原始记录：19,229
唯一明确 CVE commit：442
唯一 CVE：809
精确 package-hint × target manifest 命中行：9,537
命中行中的唯一 CVE：133
唯一 (commit, CVE) cluster：231
已固定 CVE JSON：129
未能从固定 cvelist commit 获取的 CVE JSON：4
```

四个无法获取 JSON 的记录为：

```text
CVE-2025-32108
CVE-2026-55612
CVE-2026-55613
CVE-2026-55614
```

它们保留在下载索引中为 `missing_or_fetch_failed`，不允许在后续被默认解释为不存在、未受影响或已修复。

## 这证明什么，尚未证明什么

当前登记册说明：在预先冻结的 release/target 总体中，至少存在足以继续做**人工证据可行性检查**的候选规模；它没有证明任何 CVE 对某个 release 真正适用，也没有证明回补。

特别地：

- 一个 commit 在 release tag 的历史中出现，不等于其 patch 一定仍保留在该 tag 的 package tree；
- commit subject 的 package hint 与 manifest 的精确名称匹配可能遗漏别名、子包、bundle 或 feed package，也可能不能证明代码路径被启用；
- 同一 commit 在多个 release tag 可达会产生多条原始记录，不能被当成独立观察；后续必须按 `(commit, CVE)` cluster 处理；
- 本登记册只覆盖 commit message 明示 CVE 的修复；不覆盖只在 patch 文本、advisory 或外部 feed 中关联 CVE 的修复；
- CVE Program JSON 的存在只提供漏洞记录，不等于 fixed release 的适用性标签。

## Gate B 的当前状态

Gate B 有三部分门槛：

```text
至少 100 原始 package-release-CVE 候选：候选量已满足
至少 10 个唯一 package-CVE-fix cluster：候选量已满足
至少 30 个独立证据支持的二元人工标签：尚未开始，未满足
```

因此，下一步是从 231 个 cluster 中按预先确定规则抽取一批待人工证据审查的 cluster，并固定需要的 tag Makefile、patch/commit 与 CVE JSON。此时仍禁止写评分代码、计算 false-affected reduction 或宣称方法有效。
