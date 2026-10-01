# OpenWrt 漏洞适用性人工标注规范（v1）

## 标注单位

一条案例是固定四元组：`(release, target, package, CVE)`。

## 标签

| 标签 | 允许条件 | 禁止依据 |
|---|---|---|
| `affected` | 官方 CVE/advisory、固定 release 的包/补丁证据共同支持未修复的受影响范围。 | 仅凭包名相似、NVD/OSV/KEV 的单一匹配、或“镜像里有这个包”。 |
| `not_affected` | 官方 release/patch/backport/advisory 明确支持固定版本已修复、已回补或不在受影响范围。 | 没有 CVE、没有 KEV、没有 NVD/OSV 记录。 |
| `insufficient_evidence` | 官方材料不足以支持任一二元结论。 | 为了凑样本而猜测。 |

## 必填证据

每一条标注必须至少填写：

```text
case_id
release / target / package / cve_id
human_label
evidence_url_or_path
evidence_commit_or_sha256
evidence_quote
reviewer_id
reviewed_at_utc
```

证据可以是冻结的 manifest/BOM、指定 OpenWrt tag 的 package recipe、feed commit、提交/补丁文件、官方 CVE JSON 或厂商/上游官方 advisory。不得用聚合数据库的缺失项构成否定证据。

## 独立性

- 第一轮标注前不显示 `baseline_prediction` 或 `provenance_prediction`。
- 至少一名第二审核人复核分层子集，且应包含所有回补、版本范围不明和方法分歧案例。
- 发生分歧时新增一行 `annotation_round=adjudication`，不得修改或删除原始首轮记录。

## 研究边界

适用性结论只表示“这个固定 OpenWrt 发布物的这个包是否有证据受该 CVE 影响”。它不表示漏洞可利用、网络可达、设备实际部署、攻击成功或风险优先级。
