# Evidence Sensitivity Stress Test：近邻全文/一手资料审计补充

## 目标

判断候选是否超出“把已有 vulnerability-to-commit、artifact safety、package patch comparison、provenance assurance 重新命名”的范围。

## 1. Prospector / Finding Fixes of Open-Source Vulnerabilities

一手全文：<https://publicatio.bibl.u-szeged.hu/29926/3/34499877_megjeelnt.pdf>

关键原文事实：

- Prospector 的输入是 advisory、repository URL、可选 version interval；它检索并排序 commits；
- 其目标是帮助专家把 vulnerability advisory 映射到 source-code fix commit；
- 文章讨论：如果知道 fix code changes，SCA 可判断 artifact 是否包含该 code，以及是 fix 前还是 fix 后；
- 其评估使用已知 fixing commits，按 top-10、confidence 等分类。

### 与当前候选的关系

这是**实质性近邻**，不能简单写作“不重叠”：

- 共同点：漏洞 advisory、commit、artifact/code retention 都在论域内；
- 区别：Prospector 解决的是 `advisory → candidate/fix commit` 的检索/排序；当前候选在 commit 已给定后，测量逐级证据降级导致的 claim-state transition；
- 风险：当前 OpenWrt T2–T4 若被写成“判断 artifact 是否安全/是否修复”，会直接落入 Prospector/SCA 语义，必须禁止。

**结论：** 仅保留“证据敏感性测量”，不能保留“安全 artifact 判定”作为贡献。

## 2. Macaron

当前可取得的一手资料：

- ACM DOI/摘要：<https://dl.acm.org/doi/10.1145/3605770.3625213>
- 官方文档：<https://oracle.github.io/macaron/>
- provenance tutorial：<https://oracle.github.io/macaron/pages/tutorials/provenance.html>

公开资料明确 Macaron：

- 分析 source、artifact、dependencies 与 build pipeline；
- 获取、验证 provenance；
- 检查 artifact 是否按可信方式构建、是否满足 policy/conformance；
- 关注 source repository 与 deployed artifact 不一致的 supply-chain 风险。

全文 PDF 当前仍被 ACM 403 阻断，因此不能宣称完成全文排除。

**结论：** Macaron 是 artifact/provenance assurance 的直接语义近邻。当前候选只有在明确“不构建 assurance engine、不验证供应链 policy、不输出 artifact trust verdict”，并只研究**证据降级下的可识别性变化**时才可能保持区分。

## 3. CVECenter

作者公开页面：<https://csu-wingmate.github.io/publication/fse24cvecenter>

公开说明其处理：heterogeneous vulnerability records、retrieval、assessment、auto-fixing、continuous vulnerability management，并在多个 Linux distribution 版本上实践。

**结论：** 它是系统/工作流近邻，不是已证明的 evidence-ablation protocol 近邻；但全文未取得，不能完成排除。

## 4. Toward Efficient Package Maintenance

全文 PDF：<https://zhangyw.work/file/papers/Peng2026ICSE.pdf>

该文在四个 Linux distributions 上比较 homologous packages、patch sets、patch introduction delay，并做 patch recommendation。它明确区分 source package 与 binary package，并把 package patch retention 当作研究对象。

**结论：** 它是 OpenWrt artifact-retention 数据分析的强近邻。当前候选若主张“首次度量跨 distribution package patch retention”，应判定失败；只能主张“在已有 package/source observations 上，预声明证据层级会使安全 claim support 状态发生变化”。

## 5. 近邻反证后的可保留命题

唯一仍可防守的命题是：

> 在不把证据缺失转换为漏洞真值的前提下，预声明的 evidence-ablation protocol 能测量同一安全结论从 identifiable 到 conditional/not-identifiable 的转移，并暴露 ancestry、artifact binding、device independence 等证据边界。

该命题目前有 pilot 可行性证据，但没有完成 novelty proof。尤其需要证明：

1. 状态转移不是由普通 provenance completeness 计数直接得到；
2. OpenWrt 和 N-BaIoT 的共同 taxonomy 不只是 `provenance missing` 的改名；
3. 该 protocol 能产生已有 SCA/package-sharing 工作没有报告的可重复研究对象：**claim-state transition / minimal evidence cut set**。

## Verdict

```text
近邻风险：仍高
候选研究性：可检验
高水平投稿性：未确认
安全 artifact 判定版本：应停止
证据敏感性测量版本：可继续 pilot
```
