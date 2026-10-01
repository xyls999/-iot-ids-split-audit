# OpenWrt 发布溯源漏洞适用性：扩大抽样框 v2

**状态：**已批准的重新立项协议；尚未开始数据收集、人工标注或评分代码。  
**替代对象：**仅替代旧的 `23.05.5 / 24.10.0 / 24.10.4 × x86/64 / ath79/generic` 固定范围。旧范围的负可行性结论继续有效，不能被改写。

## 研究问题

> 在预先固定的多个 OpenWrt 稳定分支及其正式点发布版中，使用 release tag、包 recipe、feed/commit 和回补 patch 证据，是否能比名称/版本匹配减少错误的 package-release-CVE `affected` 判断，且不造成不可接受的漏判？

研究对象仍然只是**发布级软件包漏洞适用性**，不是漏洞可利用性、攻击成功率、实际设备暴露或风险优先级。

## 新总体：先枚举、后筛选

### 时间和版本总体

冻结日期为：

```text
2026-10-01T00:00:00Z
```

纳入 OpenWrt 官方发布目录中、在冻结日期前公开的以下稳定分支的**全部最终数字点发布版**：

```text
22.03.x
23.05.x
24.10.x
```

- 仅收录正式 release tag 与官方 release 目录；不收录 RC、snapshot、nightly 或第三方镜像。
- 实际 release 清单必须由官方目录枚举后写入 manifest；不能预先挑对结果有利的 patch 版本。
- 每个 release 固定检查 `x86/64` 和 `ath79/generic` 两个官方 target；若任一 target 不存在，记录缺失而不是换成任意方便的 target。

### CVE 总体

候选 CVE 只能来自以下两类一手证据的并集：

1. 上述稳定分支官方 changelog 或官方 OpenWrt advisory 中**明确写出 CVE 编号**的修复；
2. 固定 release tag 中能由提交信息或补丁正文明确关联到 CVE 的 package patch。

每条 CVE 必须固定到 CVE Program `cvelistV5` 的具体 commit 和本地 SHA-256。NVD、OSV、KEV 可作补充元数据，不能用于把缺失记录转换为 `not_affected`。

### 分析单位与去重

原始记录单位：

```text
(release, target, package, CVE, OpenWrt_fix_commit_or_patch)
```

但同一个 `package × CVE × fix commit` 在多个 release 出现时，不被当成独立的安全事件。结果表必须同时报告：

```text
原始记录数
唯一 package-CVE-fix cluster 数
每个 cluster 覆盖的 release/target 数
```

统计推断若进行，必须按 cluster 处理；不得把同一 patch 复制到多个 release 后当成大量独立样本。

## 数据与冻结规则

每个 release × target 仅保存：

```text
manifest
CycloneDX BOM（若官方提供）
config.buildinfo
feeds.buildinfo
version.buildinfo
sha256sums
```

每条候选额外保存：

```text
固定 CVE JSON
对应 OpenWrt tag 的 package Makefile
明确关联 CVE 的 commit patch 或 tagged package patch
必要的 target/default-package 定义文件
```

- 不下载固件镜像、不运行固件、不扫描、不连接设备。
- 总快照预算为 50 MB；达到预算前先保存候选清单和哈希，不自动删减“难例”。
- 若官方目录/sha256sums 不足以验证一个文件，则该 release/target 记录标为不合格，不悄悄保留。

## 方法和标签

### 方法 A：名称/版本匹配

只使用 package 标识、声明版本和官方 CVE 描述/结构化 affected 范围。输出：

```text
affected / not_affected / unresolved
```

若 CVE 范围不明确，输出 `unresolved`，而不是猜测 `affected`。

### 方法 B：发布溯源匹配

在方法 A 之外，可使用固定的 recipe、release tag、feed/commit 与 patch/backport 证据。只有当证据明确、可定位、位于该 release tag 内时，才允许改变方法 A 的判断。

### 人工参考标签

```text
affected
not_affected
insufficient_evidence
```

第一轮人工标注不能看到方法 A/B 结果。至少第二位审核人复核所有方法分歧案例与分层样本；保留原始行和裁决行。

## 三个实施闸门

### 闸门 A：总体枚举完整性

通过条件：

```text
官方目录已列出所有纳入的 release tag
+ 每个 release × target 的文件与 SHA-256 可追溯
+ 无按 CVE 结果挑选 release 的行为
```

失败：停止，不进入候选抽取。

### 闸门 B：回补候选可行性

通过条件：

```text
至少 100 个原始 package-release-CVE 候选
+ 至少 30 个可由独立证据做二元人工标注的案例
+ 至少 10 个唯一 package-CVE-fix cluster
+ 不少于 2 个稳定分支
```

这些是最低可行性条件，不是预期结果。若失败，写负可行性报告，不写评分代码。

### 闸门 C：比较效果

只有闸门 B 通过才计算：

```text
false-affected reduction = (false_affected_A - false_affected_B) / false_affected_A
```

继续成文的最低条件：

```text
false-affected reduction >= 20%
且
recall_B - recall_A >= -5 个百分点
```

任一条件失败，拒绝“方法 B 改进”的核心假设，完整报告负结果。

## 旧范围与 v2 的关系

旧范围的唯一确认正对照 `Dropbear / CVE-2023-48795 / 23.05.5 x86/64` 可以在 v2 重新枚举到时作为候选，但不能带入旧标签或以它证明 v2 有效。`CVE-2023-36328` 保持部分证据，除非 v2 中补齐 bundled libtommath revision 到 CVE affected commit 的一手映射。

## 立即执行顺序

1. 从 OpenWrt 官方目录枚举 22.03.x、23.05.x、24.10.x 的所有最终数字 release；
2. 对每一个 release × 两个 target 下载并核验小型 metadata；
3. 从官方 changelog/advisory/显式 CVE patch 建立候选登记册；
4. 统计候选数和唯一 cluster 数，先执行闸门 B；
5. 仅在闸门 B 通过后，再以测试先行方式开发离线审计脚本。
