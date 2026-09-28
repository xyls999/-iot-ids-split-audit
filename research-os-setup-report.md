# Research-OS Setup Report

**Date:** 2026-09-28  
**Status:** `PARTIALLY_CONFIGURED`

## 1. 当前环境

已实际验证：

- 工作目录：`E:/water paper`，初始为空；现已初始化 Git。
- Pi：`0.85.1`。
- Git：`2.55.0.windows.3`。
- Python：Anaconda `3.13.5`，pip `26.2.1`，conda `26.5.0`。
- Node：`v24.19.0`，npm `11.17.0`，pnpm `11.21.0`。
- PDF 文本：`pdftotext`、`pypdf 6.16.2`。
- DOCX：`python-docx 1.2.0`、`lxml 6.1.3`、`docx2txt`、`antiword`。
- 网络：`curl https://example.com` 可达。
- Pi 子代理、MCP 适配器、Superpowers、动态 workflow 包已存在。

## 2. 可以安装什么

可以在隔离环境中继续配置：

1. Research-OS 本地状态与证据目录（本次已完成）。
2. Zotero MCP 的只读本地 API 接入（需先验证版本、Zotero 7+ 本地 API 和权限）。
3. PaperQA2 的本地/明确授权模型配置（需单独虚拟环境、模型和隐私审批）。
4. PDF 渲染/OCR 工具（扫描版中文 PDF 才需要）。
5. 浏览器/CDP 或 Brave Search（需要浏览器运行或 API key）。

未批准或不建议在 Phase 1 安装：ECC 全套、全局 hooks、n8n、LangGraph、OpenAI Agents SDK、academic-research-skills 自动路由器。

## 3. 已有功能

已建立：

- `research-os/AGENTS.md`、`CLAUDE.md`、`README.md`。
- `state/manifest.yaml` 单一权威状态。
- `state/workflow.yaml`、`next_action.yaml`、`decisions.yaml`、`blockers.yaml`。
- `memory/` 双层语义记忆。
- 文献、Gap、Idea、Hypothesis、Method、Experiment、Evidence、Manuscript、Review、Submission 目录。
- Zotero/PaperQA2 只读/本地配置模板。
- 离线验证脚本：`research-os/tools/validate_setup.py`。
- Hohai 目录 PDF 文本证据：`research-os/literature/hhue-catalog-extracted.txt`。

## 4. 缺失依赖

未验证或缺失：

- 用户指定 JPG 不存在于 `C:/Users/Administrator/Downloads/`，因此无法读取图片中的期刊/会议。
- 浏览器/CDP 未启动。
- `BRAVE_API_KEY` 未设置。
- PDF 渲染/OCR 工具（如 `pdftoppm`、PyMuPDF、Tesseract）未验证。
- LibreOffice、Pandoc 未安装。
- Zotero MCP、PaperQA2 尚未安装。
- Zotero 账户/本地库、模型 API 凭据、作者研究约束尚未提供。

## 5. P0 项目的兼容性

| 项目 | 结论 |
|---|---|
| `Imbad0202/academic-research-skills` | 可参考其研究流程与状态思想，但不能接管 manifest；其路由、hooks、passport/state 需隔离。 |
| `zhangjiazhe/academic-research-skills` | Codex/Claude 取向，需适配后才能用于 Pi；不能直接覆盖本项目规则。 |
| `obra/superpowers` | 已安装；仅用于 brainstorming、计划、编码、测试、调试、验证和代码审查。 |
| `54yyyu/zotero-mcp` | 可作为只读文献访问层；写入工具必须禁用并做工具白名单。 |
| `mmrech/paper-qa2` | 可作为检索/证据辅助层；不作为事实源或状态源。 |

P0 详细审查证据见 `research-os/artifacts/p0-decision-memo.md`。

## 6. Skill 冲突分析

所有外部 skill 服从：用户明确要求 > Research-OS `AGENTS.md`/`CLAUDE.md` > workflow gates > 外部学术 skill > Superpowers > ECC generic rules。

任何带有自动路由、自动 checkpoint、独立 state 或“source of truth”表述的外部套件只能产出子 artifact，不能修改 manifest 状态而不经过 checkpoint。

## 7. Superpowers 冲突分析

Superpowers 对软件工程非常有用，但不能决定：

- Research Gap 是否成立；
- 创新性是否成立；
- 统计设计是否有效；
- Claim 是否有充分证据；
- 是否达到投稿标准。

因此已在 `research-os/AGENTS.md` 和 `CLAUDE.md` 中明确边界。

## 8. ECC 冲突分析

ECC 当前未安装/未验证。其 memory persistence、hooks、continuous learning、context management 可能与 Research-OS 双重记忆和 manifest 规则冲突。Phase 1 暂缓；如启用，必须先审查所有 hooks、commands、MCP、CLAUDE.md 和权限。

## 9. Zotero / PaperQA2 配置方式

配置模板：

- `research-os/config/zotero-mcp.readonly.example.json`
- `research-os/config/paperqa2.local.example.yaml`

Zotero 建议：本地 API、只读工具白名单、禁用写工具、先做 search/get/fulltext smoke test。PaperQA2 建议：独立 `PQA_HOME`、明确 source manifest、本地或已批准模型、所有回答回写 source IDs 和 evidence artifact。

本次没有写入真实凭据，也没有上传私人文献。

## 10. 推荐最终架构

```text
Research-OS manifest/state/gates
        ↓
Academic research skills (subordinate)
        ↓
Literature sources + Zotero read-only
        ↓
PaperQA2 retrieval/evidence helper
        ↓
Independent Gap/Novelty Critic
        ↓
Method/Experiment/Claim-Evidence DAG
        ↓
Writer → seven-role reviewer panel → journal adapter
```

Superpowers 位于工程实现层；ECC 不是 Phase 1 组件；n8n/LangGraph/OpenAI Agents SDK 延后。

## 11. 安装顺序

1. 已完成本地目录、状态、规则、验证脚本和 Git 初始化。
2. 读取缺失 JPG 或更正路径。
3. 完成研究者画像、数据/平台、截止时间、预算、语言和目标认可度 intake。
4. 基于目录与一手来源建立文献/期刊/会议比较矩阵。
5. 单独验证 Zotero MCP 版本与只读调用。
6. 单独创建 PaperQA2 隔离环境并做本地小语料 smoke test。
7. 仅在流程稳定后评估 ECC、定时雷达和外部 orchestrator。

## 12. 风险

- “最好发/最水”无法由可靠证据保证；只能评估范围匹配、成本、实验负担、审稿透明度和认可度。
- 目录等级是学校目录口径，不等于当前所有数据库或目标单位最新认定；投稿前需再次核验。
- 会议等级、是否收录、注册费、截止日期会变化，必须以当届官方 CFP 和出版商页面为准。
- 机器人方向若没有真实实验、仿真对照、基线和统计报告，不能仅靠模型堆叠形成可接受论文。
- 当前缺少用户指定图片，无法完成图片期刊识别。
- 扫描中文 PDF 可能需要 OCR；当前未验证 OCR。

## 13. 配置后测试方案

已执行：

```text
python research-os/tools/validate_setup.py
```

结果：`passed: true`，必需文件、manifest 权威性、Resume/Checkpoint Protocol 和 Phase-1 状态检查均通过。

待执行：

- JPG 重新上传后的图像识别与人工复核。
- Zotero 只读连接 smoke test。
- PaperQA2 本地小语料解析/检索 smoke test。
- 目标期刊/会议官方 scope、费用、审稿与收录核验。
- 研究方向的独立 novelty/feasibility critique。

## 结论

`PARTIALLY_CONFIGURED`：Research-OS 核心状态层已配置并通过离线验证；外部文献工具、浏览器/OCR 和图片输入仍未配置或不可验证，因此不能宣称完整可用，也不应开始论文生成。
