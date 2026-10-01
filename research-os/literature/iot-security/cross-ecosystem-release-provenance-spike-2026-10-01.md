# 跨发行生态发布安全声明溯源：只读侦察

**状态：**已获准的探索性 spike；不冻结 cohort、不产生漏洞标签、不实现工具或评分代码。

## 问题

已审计的 AFV、PatchScout、Patch2Vuln、VERIPORT 已排除“新 version-applicability algorithm”“patch/backport analysis”“Linux package pair”与“verified evidence chain”。本 spike 改问：跨发行生态中，**已发布安全声明能否被独立重放为 artifact-level claim**，以及这一问题是否仍有足够独立贡献。

这里的 claim audit 不判断真实设备暴露、可利用性或攻击效果；它只检查公开声明是否携带足以将 CVE、发布 artifact、source remediation 和 build/release provenance 连起来的可验证见证（witness）。

## 已直接核验的一手资料

| 层 | 一手来源与事实 | 对候选问题的含义 |
|---|---|---|
| Build provenance | [SLSA Provenance v1.0](https://slsa.dev/spec/v1.0/provenance) 将 provenance 定义为 build platform 通过 `buildDefinition` 产出 artifact 的 attestation；它包含 `resolvedDependencies`，让消费者检查 artifact 是否按预期构建并支持重建。 | 强烈证明“artifact → build/source materials”本身不是新问题；但该规范不定义 CVE status。 |
| Vulnerability version status | [OSV schema](https://ossf.github.io/osv-schema/) 的 `affected` 对象描述“包含漏洞的 package versions”，用显式版本或 range 判断某一版本是否受影响。 | OSV 已标准化 package/version applicability；它不是 release artifact 的 build/release witness。 |
| VEX status | [OpenVEX v0.2.0](https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md) 定义 `affected`、`not_affected`、`fixed`、`under_investigation`；产品可有 hash，`status_notes` 可说明 status 来源。 | VEX 已表示 product-vulnerability status；不能把另一套 status schema 包装成 VEX 创新。其状态语义仍不等于非执行的 release-applicability audit。 |
| Metadata graph | [GUAC 官方 README](https://github.com/guacsec/guac) 将自身定义为聚合安全 metadata、规范化实体 identity 和映射标准关系的高保真 graph；输入已包括 CycloneDX、in-toto、OSV、SLSA、CSAF/CSAF VEX 与 OpenVEX。 | “把 SBOM、VEX、SLSA 放进一个 graph”不是新颖方向。其 README 也明示 identity 标识不足时需 heuristic，提示发行包 identity 仍是实证难点。 |
| Target/configuration-aware CVE filtering | Helmke & vom Dorp, [*Towards Reliable and Scalable Linux Kernel CVE Attribution in Automated Static Firmware Analyses*](https://arxiv.org/pdf/2209.05217), 2022，全读。它用 binary image 的 kernel version、ISA 与 configuration dry-build 过滤 version-centric matches；127 router firmware case study 中报告 68% version matches 被判为 false positives，12% 获额外适用性证据。 | 不得把“architecture/configuration-aware CVE applicability、降低 version matching false positive”作为创新，尤其不能重新包装 kernel 方向。该工作不审计 signed release claim 的 source/build/repository witness 链。 |

本地只读阅读缓存（不提交）位于 `research-os/.cache/literature/`。

## 综合：不是一个缺少 graph 的问题，而是缺少可检验的 claim-closure 问题

现有工件的职责可抽象为：

```text
OSV / VEX / CSAF:       CVE × product/package-version 的 status claim
SLSA / in-toto:         source/materials × builder → artifact 的 provenance claim
signed repository index: artifact 属于某一 release/channel 的 distribution claim
GUAC:                   汇聚上述 metadata 与 identity relationship
```

因此下列主张均为 **STOP**：

- 提出新的 SBOM/VEX/SLSA 聚合 graph；
- 从 graph 自动判断 CVE applicability；
- 用 source patch/backport 或 release pair 证明首创；
- 以 target/architecture/configuration 过滤版本 CVE 匹配；
- 生成或验证 backport。

若存在可研究问题，它必须更窄：给定一个发布方的“package P 在 release R 对 CVE C 的 remediation/status”声明，声明是否有足够的、彼此可验证的证据边来支持该**发布 claim**，而不声称该 CVE 可利用性或真实漏洞状态。

一个最小 closure profile 至少需要以下可定位 witness：

```text
W1  Security statement:        CVE + downstream package/release status
W2  Release subject:           immutable package artifact / repository index identity
W3  Source-remediation:        fixed source revision, patch bundle, or explicit source-version rationale
W4  Build/release binding:     source/materials → built package artifact → published release/channel
W5  Variant scope (if any):    architecture / target / configuration applicability boundary
```

审计输出只能是 **closure completeness**，例如 `closed`、`partially_witnessed`、`unclosed`、`not_evaluable`；不得写成 `affected`/`not_affected`，从而避免与 OpenVEX 影响状态和 AFV/PatchScout 的 version verdict 混淆。

## 目前可想象、但尚不够格的候选贡献

### Release Security Claim Closure Audit（条件候选）

一个跨 OpenWrt、Debian/Ubuntu、Fedora/RHEL 等公开生态的可重复测量研究：

1. 定义上面的 witness/closure profile，并将每一条边绑定到不可变 digest、signed index、可访问 source revision 或明确的缺口；
2. 对预注册、分层抽取的 security release claims 测量 W1–W5 的 closure rate 与不可重放原因；
3. 不把 lack-of-closure 推断成 package 有漏洞，明确保留 `not_evaluable`；
4. 将结果定位为 release-security-claim **auditability/interoperability**，而非 vulnerability detection、VEX replacement 或 exploitability assessment。

其潜在价值是可复现地暴露“status metadata、provenance 和 published artifact 各自存在却不能构成一个可审计 claim”的断链。但目前只是一种研究设计假设，**不是创新结论**。

## 高风险近邻与阻断项

- *Macaron: A Logic-based Framework for Software Supply Chain Security Assurance*（CCS 2023，DOI `10.1145/3605770.3625213`）与 *An Empirically Grounded Reference Architecture for Software Supply Chain Metadata Management*（2024，DOI `10.1145/3661167.3661212`）标题和一手摘要索引显示它们高度接近 metadata graph / assurance 主题。ACM 自动下载与 full HTML 当前均为 403；**访问失败不构成不重叠证据**。在取得全文前，候选不得进入预注册。
- GUAC 已直接阻断通用 graph/aggregation 贡献；若 closure profile 只是 GUAC query 的换名，也应停止。
- Helmke & vom Dorp 已阻断 configuration-aware version filtering；kernel 不能作为“target sensitivity”新颖性来源。
- 任何跨生态比较若只展示公开接口差异，而没有预先定义的 audit outcome、独立复查和实证的 policy/identity consequence，只是工程目录，不是研究贡献。

## 当前 spike verdict

```text
原 OpenWrt applicability algorithm:                       STOP
泛化 SBOM/VEX/SLSA evidence graph:                         STOP
跨生态 release-security-claim closure audit:               CONDITIONAL, 未达“足够创新”
立即冻结新 cohort、写指标/系统、或投稿主张:                 NO-GO
```

## 最有信息量的下一步

先取得并全文审计 **Macaron**，并将其实体/edge model、逻辑推理、输入格式、vulnerability semantics 和 evaluation unit 与 W1–W5 profile 逐项比较。若它已对 release security claims 做同样的 closure/assurance 判定，则停止该候选；若它只验证一般 supply-chain policy、没有 security statement 到 released artifact 的 closure unit，再以一个 Debian/Ubuntu 与一个 Fedora 的官方安全更新做**只读、单例**重放，确认 W1–W5 真能产生可区分的缺口，才考虑设计独立预注册。
