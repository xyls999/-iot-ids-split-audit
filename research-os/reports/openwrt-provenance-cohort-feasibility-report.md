# OpenWrt 发布溯源漏洞适用性：案例集可行性报告

**日期：**2026-10-01  
**结论：**当前冻结的 `23.05.5 / 24.10.0 / 24.10.4 × x86/64 / ath79/generic` 范围，**不能进入“方法 B 减少 false-affected”实验**。

## 预注册的前置条件

计划要求的核心案例必须同时具备：

```text
目标镜像确实包含该 package
+ 官方 CVE 仍覆盖该 package 声明的上游版本
+ OpenWrt 明确将 CVE 关联到补丁/回补
+ 补丁存在于固定 release tag
```

只有这种“版本号仍看似受影响、但 release 已回补”的案例，才能衡量 package recipe/feed/patch 证据相对于名称/版本匹配带来的增益。普通版本升级前后的 CVE 不满足该要求，因为基础方法也可从版本范围得出同样结论。

最低门槛是约 100 个候选和至少 30 个可二元人工判定案例；这不是可通过放宽标签、重复同一 CVE 或把未知项改为负例来规避的门槛。

## 已确认、部分与否决的结果

| 状态 | 案例 | 证据结论 | 是否可作为最终实验标签 |
|---|---|---|---|
| 确认的正对照证据链 | `23.05.5 / x86/64 / Dropbear 2022.82-6 / CVE-2023-48795` | 本地冻结 manifest 列出 `dropbear - 2022.82-6`；CVE Program 描述覆盖 Dropbear through 2022.83；OpenWrt 明确 CVE 关联的 strict-KEX 修复存在于 v23.05.5 patch。 | 否。它是一个待独立人工判定的正对照种子，不是最终标签。 |
| 部分 | `23.05.5 / x86/64 / Dropbear bundled libtommath / CVE-2023-36328` | default package、bundled libtom 选项、CVE-linked OpenWrt 修复与 v23.05.5 patch 均有证据；但 bundled libtommath 的精确上游 revision 与 CVE affected commit 的映射尚未证明。 | 否。保持 `PARTIAL`。 |
| 否决 | OpenSSL 第一轮种子 | 当前六个固定 target BOM 没有 OpenSSL 组件。 | 否。 |
| 否决 | Mbed TLS / BusyBox 第一轮种子 | 当前只证明版本范围或普通升级边界，没有同版本明确回补证据。 | 否。 |
| 否决 | 24.10.4 OpenSSL、Mbed TLS、ubus 线索 | 官方 changelog 显示为常规版本升级，非保留受影响版本的回补；另一个 advisory 只作用于 lantiq。 | 否。 |

## 本轮紧凑检索

| 任务 | 结果 | 解释 |
|---|---|---|
| CVE-2023-36328 严格复核 | `PARTIAL` | 缺少 bundled component 精确 revision → CVE commit 映射，不能升级。 |
| 23.05.5 紧凑官方检索 | 无新增确认案例 | 这不是穷尽性“没有案例”结论，只是本轮无合格案例。 |
| 24.10.0 / 24.10.4 紧凑官方检索 | 无确认案例 | 主要线索是版本升级，或不适用于已选 target。 |

相应的一手依据与固定文件位于：

```text
data/openwrt-provenance-backport-seeds.yaml
literature/iot-security/openwrt-cve-seed-screen-2026-10-01.md
data/openwrt-provenance-snapshots/
```

## 停止规则结果

```text
合格正对照证据链：1
部分证据：1
最小二元人工案例门槛：30
最小候选门槛：约 100
```

因此：

```text
当前案例集可行性：失败
当前 false-affected 改进实验：阻断
当前离线评分代码：不应实现
当前投稿级方法结论：不成立
```

## 不允许的“补救”

- 不能把 24.10 的正常版本升级算作“溯源方法修复的误报”；
- 不能把 CVE JSON、NVD、OSV 或 KEV 缺失当作 `not_affected`；
- 不能为凑样本重复同一 CVE/包/补丁组合；
- 不能把一个 Dropbear 案例扩写成可量化性能提升；
- 不能在案例集不成立时编写或运行评价代码。

## 后续决策

若仍保留 OpenWrt 方向，必须重新设计并预注册一个**更宽的、独立合理的 release/target 抽样框**，然后从零重新冻结数据、审计重叠和标注协议；不能在现有三 release、两个 target 的失败范围上临时加样本。

在未批准新范围前，本项目应把当前路线保存为透明的可行性负结果，而非期刊实验。
