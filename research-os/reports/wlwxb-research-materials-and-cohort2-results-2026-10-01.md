# 《物联网学报》准备资料与 OpenWrt cohort 2 结果

## 1. 期刊资料核验

官方范围、投稿格式、审稿流程和近邻文章记录于：

`research-os/literature/venue-wlwxb-scope-and-nearest-articles-2026-10-01.md`

主要结论：

- 《物联网学报》官方业务范围包含“数据融合处理与安全管控”；
- 近年官方文章确实发表 IoT 入侵检测、边缘学习和安全风险评估；
- 投稿要求中文标题通常少于 15 字、最长不超过 25 字，摘要约 200 字，关键词 3–8 个，Word 字符数（含空格）不超过 20,000；
- 采用双向匿名审稿，官方流程页写明平均约 5 个月；
- 稿件需突出作者创新，且必要时可要求原始数据或源代码；
- 投稿方向匹配，但不能因此推断录用。

## 2. OpenWrt 第二个 outcome-blind cohort

### 抽样规则

从 62-pair frozen scout 的 identity-key SHA-256 排序中，按每条 stable family 的 rank 2–3 抽取，不读取 closure outcome；由于 21.02 family 没有 rank 2 之后的 pair，本轮不做 deterministic fill，得到 10 个不与第一轮 12-packet pilot 重叠的 packet。

机器可读 packet：

`research-os/artifacts/openwrt-blinded-review-packets-cohort2.json`

### 双审结果

两名独立只读审查者各自判断 10 packets × 5 tiers，共 50 cells：

```text
exact agreement: 50/50
agreement: 1.00
```

机器可读裁决：

`research-os/artifacts/openwrt-cohort2-blind-review-adjudication.json`

| tier | identified | conditional | not_identifiable |
|---|---:|---:|---:|
| T0 | 0 | 0 | 10 |
| T1 | 0 | 0 | 10 |
| T2 | 10 | 0 | 0 |
| T3 | 8 | 0 | 2 |
| T4 | 7 | 1 | 2 |

其中一个 packet 在 T4 为 `conditional`，原因是 changed-path 中部分 blob 匹配、部分不匹配；两个 packet 在 T3/T4 均为 `not_identifiable`，因为没有任何 exact changed-path blob。该状态不被写成修复失败。

## 3. 当前意义

这是第二个不重叠 OpenWrt cohort 的规则复现结果，支持：

1. tier 规则不是只在第一轮 12 个 packet 上工作的；
2. partial retention 的 `conditional` 状态可重复识别；
3. metadata-only、ancestry-only 和 artifact-retention 的边界仍可被机械重放。

它仍然不能支持：

- 总体 inter-rater reliability；
- CVE applicability accuracy；
- artifact semantic remediation truth；
- 录用概率或“已证明重大创新”。

## 4. 投稿准备判断

```text
《物联网学报》主题匹配：是
格式可适配：是
第二 cohort 规则复现：通过
当前直接投稿：仍需先完成稿件 claim lint 和外部式盲审
```
