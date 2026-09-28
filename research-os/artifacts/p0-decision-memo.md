# P0 Read-only Decision Memo

来源：初始只读 discovery workflow，详见 workflow run artifact；本文件只记录可复核结论。

## Verified

- Pi、Git、Python、Node、PDF/DOCX 文本工具已存在。
- Superpowers、Pi subagents、MCP adapter 已存在。
- 当前目录初始为空且无 MCP 配置。
- Zotero MCP 适合只读文献访问，但需工具白名单。
- PaperQA2 适合作为检索/证据辅助，不是事实源。
- 两套 academic-research-skills 都带有自身流程/状态概念，不能无脑覆盖。

## Not verified

- ECC。
- 浏览器/CDP、Brave API。
- OCR/PDF rendering。
- Zotero 本地库和 PaperQA2 模型/凭据。
- 国内数据库（CNKI/Wanfang/VIP）的自动化可用性。

## Decision

Phase 1 采用本地 manifest + artifact DAG + Git；外部工具均为受控子组件。任何外部工具不得覆盖 `research-os/state/manifest.yaml`。
