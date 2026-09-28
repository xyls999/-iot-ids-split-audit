"""Offline Research-OS Phase-1 validation; no network and no corpus access."""
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md", "CLAUDE.md", "README.md",
    "state/manifest.yaml", "state/workflow.yaml", "state/next_action.yaml",
    "state/decisions.yaml", "state/blockers.yaml",
    "memory/project_memory.md", "memory/session_handoff.md",
]
missing = [p for p in required if not (ROOT / p).is_file()]
manifest = (ROOT / "state/manifest.yaml").read_text(encoding="utf-8")
checks = {
    "required_files": not missing,
    "manifest_single_source_of_truth": "single source" in (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower() and "source_of_truth: state/manifest.yaml" in (ROOT / "state/workflow.yaml").read_text(encoding="utf-8"),
    "resume_protocol": "Resume Protocol" in (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
    "checkpoint_protocol": "Checkpoint Protocol" in (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
    "manifest_status_present": "status: PARTIALLY_CONFIGURED" in manifest,
    "no_private_runtime_config": not (ROOT / "config" / "zotero-mcp.json").exists() and not (ROOT / "config" / "paperqa2.yaml").exists(),
}
result = {"root": str(ROOT), "missing": missing, "checks": checks, "passed": not missing and all(checks.values())}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if result["passed"] else 1)
