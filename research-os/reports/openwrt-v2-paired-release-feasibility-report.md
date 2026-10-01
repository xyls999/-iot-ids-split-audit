# OpenWrt：pre-fix/post-fix 配对发布物的探索性可行性检查

**状态：**探索性；不改变 v2 冻结样本，不能用于 v2 的 Gate B 或任何效果指标。

## 动机

v2 的固定样本条件是“明确 CVE commit 已被 release tag 包含”。已裁决的 34 个案例全部为 `not_affected`，使原研究问题中的 recall 不可估计。一个后继研究若要保留 release-level applicability 目标，必须在标签前同时构造修复前与修复后的发行物。

## 机械配对规则

在已冻结的 24 个 release、两 target、已有 CVE JSON 和原始 candidate registry 内，按每个 `(commit, CVE, package, target, stable family)`：

```text
post = 同一稳定线中最早的、package/target manifest 存在且包含该 explicit-CVE commit 的正式 release tag
pre  = post 之前最近的、同 package/target manifest 存在且不包含该 commit 的正式 release tag
```

候选 commit 与 CVE 的关联仍只来自原登记册中的显式 CVE commit message；不从标签、版本匹配预测或后续人工审查结果选择 pair。

完整可复算记录在：`artifacts/openwrt-v2-paired-release-feasibility.json`。

## 结果

| 指标 | 数值 |
|---|---:|
| 可构造 pre/post target pair | 29 |
| 唯一 `(commit,CVE)` cluster | 15 |
| 稳定线覆盖 | 22.03、23.05、24.10 |
| package 覆盖 | BusyBox、e2fsprogs、dnsmasq、Dropbear、Lua |

按稳定线的 pair 数为：22.03=11，23.05=8，24.10=10。典型 pair 包括：

- `22.03.2 → 22.03.3`：BusyBox/CVE-2022-30065、e2fsprogs/CVE-2022-1304、dnsmasq/CVE-2022-0934；
- `22.03.6 → 22.03.7`：Dropbear/CVE-2023-36328、CVE-2023-48795；
- `23.05.2 → 23.05.3`：Dropbear 两个 CVE、dnsmasq/CVE-2023-50387、CVE-2023-50868；
- `24.10.4 → 24.10.5`：Dropbear/CVE-2019-6111、CVE-2025-14282。

## 解释与限制

29 个 pair 可以提供 58 个 release-target package-CVE 审查单位（每 pair 的 pre 与 post 都要独立审查），但这不是“58 个独立安全事件”；依赖统计只能按 15 个 cluster。当前 population 仍较小，不能不经新预注册就被当作 v2 扩样，也不足以把论文可行性当作已证实。

大量原始 registry group 无法配对主要因为它们在既定 24 release 内不存在更早、target package 仍存在且不含该 commit 的 release。这是完整 Git 历史与短稳定线窗口的自然结果，不是可通过挑选标签修复的问题。

## 继续研究的判据

该配对设计是一个**候选后继协议**，不是创新点。要成为独立研究，仍须：

1. 扩展前先固定新的 release population，而不是针对 29 个 pair 挑案例；
2. 在冻结前决定是否跨更多历史稳定线、更多 target 或更多 package evidence source；
3. 全对标注 `affected` / `not_affected` / `insufficient_evidence`，并保留 pair 两侧；
4. 先全文审计 *Precise (Un)Affected Version Analysis*、PatchScout、PatchScope 等高风险近邻；
5. 在有两类真值和独立 cluster 后，才讨论版本法与 provenance 法的比较。
