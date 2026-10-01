# 多篇近邻“拼合”后的创新性反证审查：release security claims

**审查方式：**不把已有论文的技术名词相加就称创新。每一候选必须与近邻在 **研究单位、输出语义、可证伪评价、结论边界** 四项同时不同，且不以数据字段缺失代替漏洞/修复结论。

## 已知近邻施加的边界

| 工作/标准 | 已覆盖的核心 |
|---|---|
| AFV | patch/backport-aware `affected`/`unaffected`/`unknown` version analysis |
| PatchScout | CVE-to-commit 排名与 stable/release branch patch deployment 的人工状态审计 |
| Patch2Vuln | Linux distribution old/new package artifact pair 与人工 oracle |
| VERIPORT | package affected-range 纠错、evidence chain 与 exploit/functionality-verified backport |
| Helmke & vom Dorp | firmware kernel version + ISA + configuration 的 CVE filtering |
| OSV/OpenVEX/CSAF | package/product vulnerability status 与版本范围表达 |
| SLSA/in-toto | artifact build/source materials provenance attestation |
| GUAC | SBOM、VEX、OSV、SLSA、in-toto 等安全 metadata 的 graph aggregation |

因此，不能把这些能力的任意子集重新命名成 algorithm、VEX、evidence graph、backport verifier 或 configuration-aware applicability method。

## 候选组合的反证

| 候选 | 试图组合什么 | 独立研究单位与输出 | 致命风险 | 最小可证伪 pilot | 当前决定 |
|---|---|---|---|---|---|
| A. Release Security Claim Closure | VEX/OSV status + SLSA/in-toto provenance + signed release index + OpenWrt recipe | 单位是 `(issuer,CVE,release/channel,artifact,variant,time)` 的**发布声明**；输出是 W1–W5 witness closure completeness，不是 CVE status | 可能只是 GUAC query 或 Macaron 的 logic assurance 换名；W1–W5 若同时定义标签则 feature–label 循环 | 3 个生态各 10 条预注册 claim，双盲审查固定官方证据能否定位/重放每条边；若 GUAC 可直接无损表达或 failure taxonomy 不稳定即停 | **CONDITIONAL，尚不足以投稿** |
| B. Temporal Security Claim Decay | A + archive/EOL/time dimension | 同一 claim 在明确时间点的 witness survival transition | 现时抓取不能证明历史上曾存在；age、EOL、生态 archive policy 强混杂；易退化为 URL availability survey | 每生态 5 条有官方双时间点 archive 索引的 claim；预定义“decay”为曾可验证的 witness 后来无法定位 | **STOP，除非先有可信历史快照** |
| C. Variant-Scoped Closure | A + architecture/target matrix | `(claim, architecture/target/configuration)` 的 closure matrix | source-level `fixed` 未必需要 per-variant rationale；Helmke 已覆盖 config-aware filtering；non-kernel 可能无分离信号 | Debian amd64/arm64 与 OpenWrt 两 target 各一固定 package，只看 W5 是否真的改变 closure 分类 | **STOP，作为 A 的后续分层而非题目** |

## 唯一可能的论文核

若且仅若 Macaron 不处理同一单位，A 可被收缩为：

> **Security advisory correctness is not claimed.** We measure whether a publisher's already-issued release-security claim is independently replayable through typed, immutable witnesses from status declaration to released artifact, and report closure gaps without inferring vulnerability presence or exploitability.

它的贡献必须是三者的**交集问题**，而不是三者的拼接：

```text
status systems alone       cannot bind a claim to a shipped artifact
provenance systems alone   cannot give a CVE/remediation semantics
metadata graphs alone      may aggregate edges without a reproducible
                           release-security-claim closure predicate
```

可发表性还需要同时证明：

1. W1–W5 不是可由既有 GUAC schema/query 不加语义地表达的同义物；
2. two-reviewer agreement 针对 edge presence/replay 可稳定，而不是由研究者解释性补全；
3. 多生态、预注册样本存在非平凡、可解释的 closure failure classes；
4. 结果能改进某种明确的审计/发布实践（例如发行方最小 witness profile），而不是仅列接口差异；
5. 不读取或不使用同一 witness 集自动派生“ground truth CVE status”。

## 对“创新点拼合”的结论

```text
把 AFV + PatchScout + Patch2Vuln + VERIPORT 拼在一起：不可行，均已覆盖。
把 OSV/VEX + SLSA + GUAC 拼在一起：不可行，通用 graph/metadata integration 已覆盖。
将它们改为 release-security-claim 的可重放性审计：存在一个条件性新研究单位，
但 Macaron 未全文排除、没有双审查 pilot，也没有独立实践效用证据。

目前“可以发论文的创新点”：NONE。
```

最可能改变该结论的工作不是扩样或实现，而是取得并全文审计 *Macaron: A Logic-based Framework for Software Supply Chain Security Assurance*（CCS 2023，DOI `10.1145/3605770.3625213`）。若它覆盖 release-security-claim witness closure，则终止 A；若不覆盖，才做 A 的最小预注册 pilot。
