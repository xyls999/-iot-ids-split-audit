# 面向设备留出泛化的 IoT IDS 算法论文计划

## 目标

将当前项目从纯审计 methods/report 转为可验证的算法研究；但只有在方法相对已有域泛化/域适配 baseline 出现稳定、可复现改进时，才保留算法论文路线。

## 固定问题

> 在设备组未出现在训练集的条件下，如何提高轻量级 IoT 入侵检测的跨设备 Macro-F1，同时控制模型参数量、CPU 延迟和误报风险？

这不是“随机切分分数最高”的问题，而是 LODO 下的泛化问题。

## 阶段 1：基线矩阵

必须实现并统一评估：

1. Random Forest；
2. Logistic Regression；
3. 标准 MLP；
4. DANN-style device-adversarial MLP；
5. CORAL 或 MMD-style alignment；
6. GroupDRO；
7. Mixup/feature-noise 作为简单正则化 baseline。

每个方法都使用：

- random-row；
- LODO；
- 两个 ordered row windows；
- 五个种子；
- Macro-F1、per-class F1、FPR、参数量、CPU 推理时间。

## 阶段 2：算法候选筛选

### 候选 A：设备对抗表征

已有方法很多。只有在 class-conditional device adversary 或资源约束版本稳定优于 DANN、CORAL、GroupDRO 时，才继续。

### 候选 B：设备组鲁棒优化

使用 group-wise worst-case/class-balanced objective。GroupDRO 本身不是创新，只能作为 baseline。若需要新方法，必须有新的 IoT-specific constraint，并证明不是简单超参数调整。

### 候选 C：轻量资源约束泛化

同时优化：

```text
LODO Macro-F1
+ FPR
+ parameter count
+ CPU latency
```

不能只追求分数。该方向更符合 IoT 工程论文，但需要明确的资源约束和公平基线。

### 候选 D：证据感知模型选择

ESST 只作为实验协议，不作为模型本身。可以研究在没有独立真值时，如何根据证据层级选择报告方式，但这仍偏方法/评估，不应与算法贡献混写。

## 阶段 3：停止条件

以下任一情况发生就停止新算法主张：

1. DANN、CORAL、GroupDRO 等已有方法已达到同等效果；
2. 改进只出现在一个 seed 或一个 row window；
3. LODO 改善以 random-row 性能显著下降为代价且无资源优势；
4. 需要依赖未经验证的时间戳或设备身份；
5. 不能取得第二个具有明确 group identity 的公开数据集；
6. 算法只是已有 domain-adaptation 模块的重新组合；
7. 只能通过事后选择设备、类别或窗口获得优势。

## 阶段 4：论文结构

若算法候选通过：

1. 问题定义：device-held-out IoT IDS；
2. 方法：算法结构、目标函数、复杂度；
3. 理论/机制：为什么对设备组变化有效；
4. 实验：两个以上数据集、LODO/时间/随机切分；
5. 资源评估：参数量、内存、CPU latency；
6. 消融：去掉每个模块；
7. 失败案例：设备组和攻击类别差异；
8. 安全边界：不把分数差距解释成漏洞或泄漏。

## 当前实验结论

第一轮 MLP/DANN-style 预研没有显示稳定优势。因此现在还不能给算法命名、写“提出了新方法”或冻结算法论文题目。
