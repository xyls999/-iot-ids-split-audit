# 可发表候选：Security Update Evidence-Join Reliability

**状态：**目前第一条达到“值得做最小 pilot”的候选；仍不是已证明可投稿。

## 一句话命题

> 现有 Linux/OpenWrt 生态分别发布 security status、source package/revision、binary package 与 release/channel metadata；但这些记录是否形成一条可由独立审查者重放的 security-update evidence join，缺少跨生态的实证测量。

研究的对象不是“漏洞是否可利用”、不是“设备是否暴露”，也不是自动生成 VEX。对象是**发布记录之间的证据连接质量**。

## 为什么不是把多篇论文简单拼接

| 近邻 | 它研究什么 | 本候选严格不同之处 |
|---|---|---|
| Lin et al., *Vulnerability management in Linux distributions* (ESE 2023) | Debian/Fedora 的 CVE 生命周期、修复耗时、跨发行版 fixing practice | 不只测时间/流程；测每条 `security claim → source → binary → release/variant` edge 是否可定位、可验证、可重放 |
| Nath et al., *Establishing Traceability between Release Notes & Software Artifacts* (arXiv 2511.18187, 2025) | 通用 release note 与 commit/PR/issue 的 traceability 和 LLM recovery | 不做通用 release-note link recovery；研究 security-specific claim、包仓库、source/binary/release 对象，且不把 LLM top-1 当贡献 |
| SVS-TEST (Rosso et al., SAC 2026) | 16 个 SBOM fixture 上比较 7 个 vulnerability scanner 的输入/解析/VEX 行为 | 不测 scanner 输出；测发行方公开记录是否能闭合为一个可审计 update claim |
| Hidden Dependencies and Component Variants (arXiv 2604.21278, 2026) | hidden dependency、component variant、SBOM/VEX scanner inconsistency | 不研究依赖 reachability、clone identity 或 scanner；其结果反而要求本候选不把 VEX/SBOM 语义当作已闭合证据 |
| AFV / PatchScout / Patch2Vuln / VERIPORT | version applicability、branch deployment、package pair、verified backport | 不输出 affected/unaffected，不定位/生成 patch，不构造 pair benchmark |
| SLSA/in-toto/OpenVEX/OSV/GUAC/Macaron | 标准化或验证各类 provenance/status/metadata/policy | 本候选做跨生态实证：哪些公开 edge 实际存在、哪些只可 heuristic join、哪些无法重放；不是提出标准或 graph engine |

## 研究单位与标签

### 原子单位

```text
claim = (issuer, CVE/advisory, downstream package, release/channel,
         artifact identity, architecture/variant, observation time)
```

### 五条预注册 evidence edge

```text
E1  advisory/status  → CVE + downstream package identity
E2  package/release  → immutable source/binary artifact identity
E3  source artifact   → remediation revision / patch / explicit version rationale
E4  source/materials  → published binary package or release artifact
E5  artifact          → release/channel + architecture/target scope
```

### 每条 edge 的四值证据等级

```text
explicit_anchored    官方记录明确给出，且指向 immutable digest/revision/index
explicit_replayable  官方记录明确给出，链接可读但缺少不可变锚点
inferred             需由名称、时间、版本或 ancestry 推断
absent_or_unreplayable
```

最终输出是 edge vector 与 failure taxonomy，不是漏洞标签：

```text
closed               E1–E5 全部 explicit_anchored 或预注册可接受组合
partially_closed     至少一条明确边，但存在可识别缺口
inferred_only        只能靠 heuristic join
not_evaluable        公开证据不足
```

`not_evaluable` 不是 `not_affected`，也不表示修复无效。

## 可证伪 RQ

1. **RQ1：**Debian、Fedora、OpenWrt 的公开 security update records 在 E1–E5 上的 closure/failure profile 是否显著不同？
2. **RQ2：**最常见的断链是 identity、source-remediation、source-to-binary、release/variant 还是 archive accessibility？
3. **RQ3：**只使用 package name/version 或只使用 Git ancestry，分别会把多少 `inferred_only` 记录错误提升为 `closed`？这里“错误”只表示违反预注册 closure predicate，不表示漏洞状态错误。
4. **RQ4：**独立审查者对 edge presence/replay 的一致性是否足以支持一个可复核 audit protocol？

RQ1–RQ3 是描述性/审计性问题；不能事先承诺某生态更差，也不能把 closure failure 解读为安全缺陷。

## 最小 pilot（先于任何 v3）

三生态各抽取 10 条公开 security update claim：

- Debian：Security Tracker + signed `InRelease` + `Sources`/`Packages` + source VCS；
- Fedora：Bodhi update + Koji/RPM build identity + package repository metadata + source package；
- OpenWrt：官方 CVE/commit evidence + release tag recipe/patch + checksum-verified manifest。

抽样规则、时间窗和 inclusion/exclusion 在读取具体证据前冻结；不得只挑容易闭合的案例。每条 claim 由两名审查者独立填写 edge form，只允许引用固定官方 URL、revision 或 digest。第三名裁决者只处理分歧，不补猜证据。

**停止条件：**

- 30 条中大部分都可由现成 GUAC/Macaron/SLSA query 无损表达；
- edge failure taxonomy 无法稳定区分；
- Fedora/OpenWrt 的官方记录无法在合理时间内形成最小闭合/部分闭合样本；
- 审查者 agreement 只靠事后解释而非预注册规则。

**继续条件：**出现非平凡、可重复的跨生态断链类型，且两名审查者能稳定判断 edge presence/replay；这时才写独立预注册 Gate A，不修改既有 OpenWrt v2。

## 可发表性判断

这是一个**经验型软件供应链/安全工程论文**候选，不是新算法论文。可能的贡献组合为：

1. 跨发行生态的 security-update evidence-join 数据集（保留缺口，不伪造完整性）；
2. 预注册、可重放的 edge-level audit protocol；
3. `identity / source / build-binding / release-variant` 断链分类及跨生态比较；
4. 对标准/工具的具体 coverage gap，而不是再造 VEX/SBOM 标准。

它只有在 pilot 后才可能升级为 `GO`。目前结论：

```text
原 OpenWrt applicability：STOP
通用 provenance/VEX graph：STOP
Security Update Evidence-Join Reliability：CONDITIONAL-GO（唯一值得做 pilot 的候选）
```

## 不能声称的内容

- 不能声称发现了 affected/not_affected 真值；
- 不能声称某发行版发布了错误修复；
- 不能声称首个 provenance/VEX/SBOM graph；
- 不能把 closure rate 当漏洞检测 precision/recall；
- 不能把 Debian/Fedora/OpenWrt 的记录差异解释为真实安全质量排名。
