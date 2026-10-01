# Evidence Sensitivity Stress Test：跨案例可检验研究候选

**状态：**当前最强候选；仍需 pilot 与近邻排除，不能称已证明创新。

## 关键突破点

之前的“evidence graph / claim closure”过于静态，也容易只是重命名 provenance 或 assurance case。这里改成一个可证伪的操作：

> 对同一个安全结论，逐级移除或降级其证据，测量结论状态、可识别性或结果指标何时发生变化。

这不是提出 VEX/SLSA/GSN，也不是把字段重新放进 graph；它测量的是**结论对证据粒度的敏感性**。

## 统一实验对象

每个案例预先声明：

```text
claim C
required evidence tiers E1...Ek
admissible evidence levels
ablation order
claim-state transition rule
```

证据等级示例：

```text
T0  name/version 或 row index only
T1  object identity / package presence
T2  independent split or source/remediation link
T3  artifact/release binding
T4  signed/hash-anchored or independently adjudicated evidence
```

输出不是漏洞真值，而是：

```text
identified → conditional → not_identifiable
```

并记录最小失效证据集（minimal cut set）：删除哪一条证据后，原结论不能再被支持。

## 两个已有案例的直接可检验信号

### Case A：N-BaIoT

已有 common-support audit 报告中的直接结果：

- Random Forest 在两个 ordered sampling windows、五个 seeds 上，random-row 与 leave-one-device-out Macro-F1 差距为 **5.0–9.6 percentage points**；
- 报告明确禁止把该结果称为新检测方法、泄漏证明或跨数据集泛化结论；
- 当 device/time provenance 和 grouped split 证据不足时，能支持的结论应从“cross-device generalization”降为“mirror/protocol-specific result”。

该案例的 evidence ablation 是：

```text
row-level random split
→ ordered window disclosure
→ device-group identity
→ leave-one-device-out protocol
```

观察量是 metric/claim state 的变化，而不是重新训练一种模型。

### Case B：OpenWrt exploratory pair cohort

已有 62-pair closure probe 的直接结果：

- 62/62 post tags 包含 remediation commit，62/62 pre tags 不包含；
- 仅使用 ancestry 时，所有 pair 都可被错误地视为“证据闭合”；
- 加入 remediation commit 所有 changed paths 的 exact-blob retention 后，只有 **50/62** pair strict closed，**12/62** 发生降级；
- 在 32 clusters 中，26 strict closed，6 需要 lineage review，其中 4 clusters 没有任何 changed-path blob exact retention；
- 人工 spot check 证明 strict mismatch 不是修复失败证明，而是触发 lineage review 的必要信号。

该案例的 evidence ablation 是：

```text
commit is tag ancestor
→ package/target presence
→ tag recipe/source evidence
→ changed-path/blob retention
→ independent lineage review
```

观察量是 release-claim closure state 的变化，而不是 affected/not_affected。

## 为什么这比原候选更强

| 原候选 | 问题 | Stress Test 修正 |
|---|---|---|
| Evidence graph | 可能只是 GUAC/SLSA/Macaron/assurance case 重命名 | 不提出图；比较证据等级造成的可观测状态转移 |
| Closure rate | 缺少独立 truth，容易变成字段计数 | 使用预注册的证据降级路径与盲审状态转移 |
| OpenWrt applicability | 被 AFV/PatchScout/VERIPORT 覆盖 | 不判断漏洞适用性，只测 ancestry 与 artifact evidence 的分离 |
| IDS split audit | 普通 leakage/split sensitivity 已有近邻 | 将其作为跨案例的一个 evidence-ablation instance，不声称新 IDS 结果 |

## 可证伪 RQ

1. 不同安全任务是否存在可重复的 evidence-sensitivity transition？
2. 哪类证据是结论的最小必要 cut set：对象身份、独立性、标签支持，还是 artifact binding？
3. 两个案例是否共享 `identity / independence / binding` 三类 failure，而不是仅共享“缺 provenance”这个空泛结论？
4. 两名盲审者能否稳定识别状态转移？

## 严格 pilot

### N-BaIoT

不重新挑数据，不改变既有镜像边界。按预注册顺序重放：

1. row-only claim packet；
2. common-support packet；
3. ordered-window packet；
4. device-held-out packet；
5. provenance-limited packet。

审查者只判断 claim 是否 `identified/conditional/not_identifiable`，不读取既有结论列。

### OpenWrt

从已冻结 release population 按 hash 规则抽取新的 non-kernel units；不得从 6 个 strict-fail clusters 反选。每个 packet 按 ancestry、recipe/source、manifest、artifact lineage 顺序开放给审查者。

### 停止条件

- 状态转移只由审查者偏好决定；
- 两案例的 failure taxonomy 不能稳定对齐；
- 结果只是既有 split sensitivity 和 provenance completeness 的换名；
- 任何结论依赖 v2 的 `not_affected` 标签；
- 需要执行固件、PoC、漏洞或设备测试。

## 潜在论文命题

只有 pilot 成功后，才能提出：

> Security conclusions are not equally robust to provenance degradation. A preregistered evidence-sensitivity protocol can identify the minimum evidence required for a claim without converting evidence gaps into vulnerability labels.

这会是一篇**measurement / methodology validation**论文，而非新检测算法论文。

## 当前 verdict

```text
作为已证明重大突破：NO
作为最强、最具体、可快速证伪的候选：YES
作为立即投稿或冻结 v3 的依据：NO
```
