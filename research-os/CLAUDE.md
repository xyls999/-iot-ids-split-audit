# Research-OS Claude Compatibility Rules

This file is subordinate to the user instruction and `AGENTS.md`.

## Non-negotiable state policy

`research-os/state/manifest.yaml` is authoritative. Claude/ECC memory, chat context, hooks, and session summaries are supplemental only. Never infer project progress from conversation history when disk state is available.

## Required startup

Execute the Resume Protocol in `AGENTS.md` before research, writing, tool configuration, or delegation.

## Required completion

Execute the Checkpoint Protocol in `AGENTS.md` after every substantive task.

## ECC policy

ECC/Everything Claude Code is not enabled in Phase 1. Its generic memory, hooks, context-management, and verification rules must not overwrite Research-OS rules. Any future ECC integration requires a recorded decision and conflict review.

## External services

No network model, Zotero write operation, or corpus upload is allowed unless the manifest records the approval, purpose, data class, and verification result.
