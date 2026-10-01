#!/usr/bin/env python3
"""Exploratory evidence-tier ablation probe for the frozen OpenWrt scout output.

This does not assign CVE labels. It compares increasingly strong source-evidence
signals and emits deterministic, outcome-blind pilot selection metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


def stable_key(row: dict) -> str:
    return "|".join(
        str(row.get(k, ""))
        for k in (
            "stable_family",
            "pre_release",
            "post_release",
            "target",
            "package",
            "cve_id",
            "commit_sha",
        )
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="research-os/artifacts/openwrt-paired-cohort-closure-probe.json")
    ap.add_argument("--output", default="research-os/artifacts/openwrt-evidence-sensitivity-pilot.json")
    ap.add_argument("--per-family", type=int, default=2)
    args = ap.parse_args()

    source = json.loads(Path(args.input).read_text(encoding="utf-8"))
    pairs = []
    for row in source["pairs"]:
        digest = hashlib.sha256(stable_key(row).encode("utf-8")).hexdigest()
        strict = bool(row["path_states"]) and all(
            state["post_blob_equals_commit"] for state in row["path_states"]
        )
        any_retained = any(
            state["post_blob_equals_commit"] for state in row["path_states"]
        )
        pairs.append(
            {
                "stable_key": stable_key(row),
                "selection_hash": digest,
                "stable_family": row["stable_family"],
                "pre_release": row["pre_release"],
                "post_release": row["post_release"],
                "target": row["target"],
                "package": row["package"],
                "cve_id": row["cve_id"],
                "commit_sha": row["commit_sha"],
                "evidence_tiers": {
                    "tier0_name_version_record": True,
                    "tier1_package_target_presence": True,
                    "tier2_post_ancestor_pre_exclusion": row["post_commit_is_ancestor"]
                    and not row["pre_commit_is_ancestor"],
                    "tier3_any_changed_path_blob_retention": any_retained,
                    "tier4_strict_all_changed_path_blob_retention": strict,
                },
                "ablation_states": {
                    "ancestry_only_support_signal": row["post_commit_is_ancestor"]
                    and not row["pre_commit_is_ancestor"],
                    "any_blob_support_signal": any_retained,
                    "strict_blob_support_signal": strict,
                },
                "label_status": "not_a_cve_label",
            }
        )

    pairs.sort(key=lambda row: row["selection_hash"])
    by_family: dict[str, list[dict]] = defaultdict(list)
    for row in pairs:
        by_family[row["stable_family"]].append(row)
    selected = []
    for family in sorted(by_family):
        selected.extend(by_family[family][: args.per_family])
    selected_keys = {row["stable_key"] for row in selected}
    for row in pairs:
        row["pilot_selected_by_hash_rule"] = row["stable_key"] in selected_keys

    def count(field: str, rows: list[dict]) -> int:
        return sum(bool(row["evidence_tiers"][field]) for row in rows)

    counts = {
        "pairs": len(pairs),
        "families": len(by_family),
        "clusters": len({(r["commit_sha"], r["cve_id"]) for r in pairs}),
        "tier0_name_version_record": count("tier0_name_version_record", pairs),
        "tier1_package_target_presence": count("tier1_package_target_presence", pairs),
        "tier2_post_ancestor_pre_exclusion": count("tier2_post_ancestor_pre_exclusion", pairs),
        "tier3_any_changed_path_blob_retention": count("tier3_any_changed_path_blob_retention", pairs),
        "tier4_strict_all_changed_path_blob_retention": count("tier4_strict_all_changed_path_blob_retention", pairs),
        "pilot_selected": len(selected),
    }
    transitions = {
        "tier2_to_tier3_downgraded": counts["tier2_post_ancestor_pre_exclusion"]
        - counts["tier3_any_changed_path_blob_retention"],
        "tier3_to_tier4_downgraded": counts["tier3_any_changed_path_blob_retention"]
        - counts["tier4_strict_all_changed_path_blob_retention"],
        "tier2_to_tier4_downgraded": counts["tier2_post_ancestor_pre_exclusion"]
        - counts["tier4_strict_all_changed_path_blob_retention"],
    }
    cluster_states: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in pairs:
        cluster_states[(row["commit_sha"], row["cve_id"])].append(row)
    cluster_summary = []
    for (commit, cve), rows in sorted(cluster_states.items()):
        cluster_summary.append(
            {
                "commit_sha": commit,
                "cve_id": cve,
                "pair_count": len(rows),
                "tier2_all": all(r["ablation_states"]["ancestry_only_support_signal"] for r in rows),
                "tier3_all": all(r["ablation_states"]["any_blob_support_signal"] for r in rows),
                "tier4_all": all(r["ablation_states"]["strict_blob_support_signal"] for r in rows),
            }
        )

    output = {
        "status": "exploratory_evidence_sensitivity_probe_not_labels",
        "selection_rule": "sort all scout pairs by SHA-256 of the fixed identity key; select first two per stable family for a 12-pair pilot; no closure outcome is used",
        "evidence_semantics": "signals only; no signal is a CVE affected/not_affected truth",
        "input": args.input,
        "counts": counts,
        "transitions": transitions,
        "pilot_selected_keys": [row["stable_key"] for row in selected],
        "cluster_summary": cluster_summary,
        "pairs": pairs,
    }
    Path(args.output).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"counts": counts, "transitions": transitions}, sort_keys=True))


if __name__ == "__main__":
    main()
