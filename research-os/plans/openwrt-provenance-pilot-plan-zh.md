# OpenWrt 发布溯源漏洞适用性：中文研究与实验计划

## 一句话目标

验证 OpenWrt 的**发布级溯源证据**（package recipe、feed commit、补丁与回补记录）是否能比“软件包名 + 版本号”匹配，更准确地判断某个 OpenWrt 发布版本是否真正受某个 CVE 影响。

## 不做什么

- 不做新的 IDS 分类器；
- 不扫描、访问、运行、模拟或攻击任何真实设备；
- 不下载或执行固件镜像；
- 不把“包存在”说成漏洞可利用；
- 不将 NVD、OSV 或 KEV 中没有记录当作“不受影响”。

## 研究对象

每一条样本是：

```text
(OpenWrt release, target profile, package, CVE)
```

例如：某个固定 release 和 target 的 `openssl` 包，对某个固定 CVE 是否受影响。

## 两种待比较方法

| 方法 | 允许使用的证据 | 输出 |
|---|---|---|
| A：基础匹配 | package 名称、版本号、官方 CVE affected 范围 | `affected` / `not_affected` / `unresolved` |
| B：发布溯源匹配 | 方法 A 的全部证据，再加 recipe、feed commit、官方 patch、回补记录 | `affected` / `not_affected` / `unresolved` |

方法 B 只有在存在可引用的发布证据时才能推翻 A；证据不完整时必须输出 `unresolved`，不能伪造“不受影响”。

## 标注真值

人工标注仅有三类：

```text
affected                官方证据支持该 release 的该包仍含漏洞或处于未修复范围
not_affected            官方证据支持该 release 已修复、已回补或不在受影响范围
insufficient_evidence   官方证据不足，不能做二元判断
```

第一轮标注不能看到方法 A/B 的结果。第二人复核分层抽样案例，最后以保留原始记录的方式处理分歧。

## 实验阶段

### 阶段 0：近邻文献闸门（已完成，暂时通过）

全文审计在：

```text
research-os/literature/iot-security/openwrt-sbom-nearest-work-audit-2026-10-01.md
```

结果：四篇最近近邻均为部分重叠；没有发现同一“发布溯源 vs 名称/版本 + 独立适用性标签”的直接对照。该结论不是新颖性保证。

### 阶段 1：冻结可复现实验输入

初步范围：3 个 OpenWrt release、2 个 target profile。

保存的仅是小型官方材料：

```text
manifest / package list
CycloneDX BOM
release tag 与 commit
相关 package recipe 与 feed 信息
选定 CVE JSON
必要的 patch/backport 文本或元数据
URL、获取时间与 SHA-256
```

总源材料不超过 50 MB。若 target 缺少可对应的清单或 source history，则不纳入。

### 阶段 2：预注册候选集与标注协议

- 在知道方法结果前固定候选集合；
- 目标约 100 个 `(release, target, package, CVE)` 候选；
- 少于 30 个可二元判定案例时，报告数据不足并停止；
- 标注表必须保存证据 URL/path、commit/hash、引文和审核人。

### 阶段 3：离线审计工具

工具只读取已冻结的本地 YAML、CSV、JSON、manifest 和 patch 证据；不发网络请求。

功能：

```text
输入验证
候选生成
名称/版本基础匹配
溯源/回补规则应用
未知证据处理
与人工标签对比
JSON 结果生成
重复运行一致性检查
```

所有规则先写单元测试，再实现。尤其测试：

```text
有明确 backport 证据时可从 affected 改为 not_affected
证据未知时必须保持 unresolved
同一输入无论顺序如何都生成相同 case_id
```

### 阶段 4：评估

主要报告：

```text
false-affected 数量和比例
precision
recall（只在人工二元标签子集内）
unresolved / insufficient_evidence 比例
方法分歧案例
人工审核证据量作为成本代理
```

预先拒绝条件：

```text
方法 B 相对 A 的 false-affected 降低 < 20%
或
方法 B 的 recall 比 A 低超过 5 个百分点
```

任一条件失败，就拒绝核心假设；不把负结果包装成改进。

### 阶段 5：论文决策

只有同时满足以下条件才开始投稿稿：

```text
近邻全文审计未发现直接覆盖
+ 官方输入可冻结并由哈希复现
+ 约 100 个候选和至少 30 个二元人工案例
+ 双轮/双人标注可复核
+ 预注册的效果与 recall 条件同时通过
+ 离线脚本重复运行结果一致
```

否则只产出透明技术报告或停止该方向。

## 现阶段立即行动

1. 从 OpenWrt 官方目录检验候选 release/target 是否真的提供 manifest、BOM 与可关联源代码；
2. 固定可复现的 3 release × 2 target 小样本；
3. 建立空白标注表和字段规范；
4. 再以测试先行方式实现离线审计脚手架。
