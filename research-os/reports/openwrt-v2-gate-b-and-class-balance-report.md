# OpenWrt v2：Gate B 数量核验与标签类别平衡审计

**日期：**2026-10-01  
**范围：**固定的 v2 backport-language 审查集；不含方法 A/B 预测、评分、指标或投稿结论。

## 输入与审查记录

| 项目 | 路径/标识 |
|---|---|
| 冻结总体 | `data/openwrt-v2-label-sample.csv`（76 release-target 单位，38 个 `(commit,CVE)` cluster） |
| 第一轮 | `data/openwrt-v2-label-round1.csv` |
| 盲第二轮输入（无标签列） | `data/openwrt-v2-round1-second-review-packet.csv` |
| 盲第二轮 | `data/openwrt-v2-label-round2-blind.csv` |
| 裁决 | `data/openwrt-v2-label-adjudication.csv` |
| 第二轮只读运行 | `97f533dc-ad0e-4f6a-82ab-5d98ee1f87dd` |

第二轮被明确禁止读取第一轮标签文件。它返回 34 个逐案标签，所有固定 CVE JSON 与 manifest 均可读取；34/34 与第一轮一致，因此不存在需要以结果替换样本或重写原始标签的分歧。

## Gate B 的原始数量条件

| 原始条件 | 结果 | 判断 |
|---|---:|---|
| 二元人工标签至少 30 个 | 34 | **满足** |
| 至少 10 个二元 `(commit,CVE)` cluster | 17 | **满足** |
| 二元标签类别 | 34 `not_affected`、0 `affected` | 数量条件未限制类别，但见下节 |
| 盲第二轮复核 | 34/34 一致 | 完成于本批 34 条 |

所以，**Gate B 的两个明示数量门槛机械上已通过**。这不是方法有效性结论。

## 关键有效性问题：类别完全单侧

本批所有已裁决二元案例都是 `not_affected`。它们来自两类直接证据：

1. 固定 CVE JSON 明示 package/product 或受影响版本上界，而相应 OpenWrt release manifest 与 tag recipe 给出范围之外的版本；
2. OpenWrt commit 明示关联 CVE，且该 patch 的相同 blob 可在固定 release tag 的 Dropbear patch series 中验证。

该分布本身是有效的审查结果，不能将其改写为“没有漏洞”。但它不足以评价原研究问题中“降低 false-affected，同时保持 recall”的后半部分：没有裁决为 `affected` 的真值单元时，recall 没有可估计的分母。

## 为什么这是设计问题，而不是应当忽略的负结果

固定样本的资格条件包含“明确 CVE commit 可由 release tag 到达”，而人工审查单位保留该 commit 对每个 target 的最早合格 release。这个条件并不逻辑保证 patch 最终仍在 release package tree 中，但它把样本系统性偏向**修复 commit 已进入历史之后**的 release。

已完成的时间资格诊断也表明，23/38 个 cluster-release 单位的 commit 比相应 tag 早超过三年：`reports/openwrt-v2-temporal-eligibility-diagnostic.md`。所以当前 v2 不是一个合理的 pre-fix/post-fix 对照集，也不能把“34 个负标签”冒充为能测 recall 的 benchmark。

## 决定

```text
Gate B（明示数量）：通过
方法比较 / 效果指标：仍禁止
原因：已裁决样本的 affected 类为零，无法回答原声明的 recall 保护问题。
```

这不是停止研究，而是拒绝在一个不能识别原假设的样本上生成看似漂亮的 precision/recall 数字。

## 持续研究的后继要求

若继续这条线，后继设计必须在独立预注册中机械地构造 paired release units：

```text
对每个已明确 CVE-linked remediation commit：
  post-fix = 首个包含该 commit 且 package/target presence 已证实的正式 tag
  pre-fix  = 同稳定线紧前一个 package/target presence 已证实、且不包含该 commit 的正式 tag
```

并须在标签前冻结：release population、target、CVE JSON、对的生成规则、独立 cluster 统计规则及 `insufficient_evidence` 处理。它不能被追溯写回 v2，也不能以当前 34 个负标签为“成功数据”来宣称方法性能。
