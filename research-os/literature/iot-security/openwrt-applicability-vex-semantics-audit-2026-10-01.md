# OpenWrt package-release-CVE 适用性与 OpenVEX 语义边界审计

**目的：**防止把不讨论 exploitability 的 release package-CVE 适用性标签错误称为“VEX-style verdict”或标准 VEX 生成。

## 一手标准来源

- OpenVEX Specification v0.2.0：
  https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md
- 本地只读缓存：`research-os/.cache/literature/openvex-spec.md`

## OpenVEX 已提供什么

OpenVEX statement 表示 `product(s) + vulnerability + status`，有 `affected`、`not_affected`、`fixed`、`under_investigation` 四个状态。产品对象可以有 identifiers、hashes 与 subcomponents；statement 有 timestamp，`status_notes` 可自由描述状态由来。

对于 `not_affected`，OpenVEX 要求 justification 或 impact statement。其固定 justification 语义包括 `component_not_present`、`vulnerable_code_not_present`、`vulnerable_code_not_in_execute_path`、`vulnerable_code_cannot_be_controlled_by_adversary`、`inline_mitigations_already_exist`。这些是漏洞影响/可利用性语义。

## 为什么当前研究输出不能称为 VEX

当前 OpenWrt 研究的标签只讨论固定发布物中的**package-CVE 适用性证据**：

```text
affected
not_affected
insufficient_evidence
```

它明确不讨论设备部署、网络可达性、漏洞可利用性、攻击路径或缓解措施。因此：

1. `not_affected` 不等价于 OpenVEX `not_affected` 的“无需 remediation / 不可利用”含义；
2. `insufficient_evidence` 不等价于 OpenVEX `under_investigation` 的产品影响状态，只表示研究者无法以固定公开证据支持二元 package-release verdict；
3. OpenVEX 的 optional `hashes` 能识别 component，但该规范不要求、也不结构化表达 `manifest → recipe/feed → CVE-linked commit → tag patch/source` 的 provenance closure；
4. 因而不能声称生成了标准 VEX，或以 VEX 合规性作为创新。

## 对剩余候选研究问题的影响

如继续，应把输出命名为 **package-release-CVE applicability evidence record**（描述性工作名，不是新标准），而非 VEX。其研究价值若存在，应来自：

```text
对已发布 distribution artifact 的 source-evidence closure 可复核性
+ 清楚区分 release package applicability 与 VEX exploitability/impact
+ 将证据不足显式保留为弃权，而不生成过度确定的状态声明
```

这仍只是条件假设；必须先证明该 evidence record 在现有 VEX 的自由文本/链接能力之外提供可测量、可复现的审计价值。
