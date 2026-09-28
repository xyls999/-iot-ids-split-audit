# Research-OS

长期、可恢复、证据可追溯的中文/国内学术研究生产线。

## Current state

Read `state/manifest.yaml` first. The project is currently in `DISCOVERY_READONLY`/initial setup and must not enter manuscript generation until the gates pass.

## Pipeline

选题 → 文献 → Gap → 创新点 → 假设 → 方法 → 实验/数据 → 证据 → 写作 → 多审稿人 → 修改 → 期刊适配 → 投稿

## Source of truth

- Machine state: `state/manifest.yaml`, `state/workflow.yaml`, `state/next_action.yaml`, `state/decisions.yaml`, `state/blockers.yaml`
- Research semantics: `memory/` and registered artifacts
- Chat history is never authoritative.

## Artifact DAG

Every result must declare `inputs`, `processing`, `outputs`, and `supports`. Corrections create a new artifact with `supersedes`; locked artifacts are not edited in place.

## Phase 1 boundaries

The first phase uses local disk state, Git, existing Pi skills/subagents, and manually reviewed source material. No global hooks, ECC, n8n, LangGraph, OpenAI Agents SDK, automatic academic-research-skill routing, or remote corpus upload is enabled.

Zotero MCP and PaperQA2 are represented by reviewed configuration templates only until privacy, credentials, version, and read-only smoke tests pass.

## Gates

A Literature completeness · B Novelty verification · C Method validity · D Experiment completeness · E Claim-evidence · F Citation integrity · G Peer review · H Journal formatting.
