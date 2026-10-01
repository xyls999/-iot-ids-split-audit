#!/usr/bin/env python3
"""Build outcome-blind review packets from the frozen closure probe.

The packet includes auditable source observations but omits aggregate tier
outcomes and pilot labels. It is intended for independent review only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def key(row):
    return "|".join(str(row.get(k, "")) for k in (
        "stable_family", "pre_release", "post_release", "target", "package", "cve_id", "commit_sha"
    ))


def main():
    source = json.loads(Path("research-os/artifacts/openwrt-paired-cohort-closure-probe.json").read_text())
    pilot = json.loads(Path("research-os/artifacts/openwrt-evidence-sensitivity-pilot.json").read_text())
    selected = set(pilot["pilot_selected_keys"])
    rows = {key(r): r for r in source["pairs"]}
    packets = []
    for identity in pilot["pilot_selected_keys"]:
        row = rows[identity]
        packet_id = "packet-" + hashlib.sha256(identity.encode()).hexdigest()[:12]
        observations = []
        for state in row["path_states"]:
            observations.append({
                "changed_path": state["path"],
                "pre_path_exists": state["pre_exists"],
                "post_path_exists": state["post_exists"],
                "post_blob_matches_remediation_commit": state["post_blob_equals_commit"],
            })
        packets.append({
            "packet_id": packet_id,
            "identity": {
                "stable_family": row["stable_family"],
                "pre_release": row["pre_release"],
                "post_release": row["post_release"],
                "target": row["target"],
                "package": row["package"],
                "cve_id": row["cve_id"],
                "remediation_commit": row["commit_sha"],
                "commit_subject": row["commit_subject"],
            },
            "claim_boundary": "source-evidence binding only; do not infer affected/not_affected, exploitability, or device exposure",
            "source_observations": {
                "post_release_contains_remediation_commit": row["post_commit_is_ancestor"],
                "pre_release_contains_remediation_commit": row["pre_commit_is_ancestor"],
                "changed_path_observations": observations,
            },
            "review_prompt": {
                "states": ["identified", "conditional", "not_identifiable"],
                "task": "At each tier, rate only the specified claim support. Give one sentence and cite the observation used.",
                "tier_claims": {
                    "T0": "Can name/version alone identify release-level remediation lineage?",
                    "T1": "Can package/target identity alone identify release-level remediation lineage?",
                    "T2": "Does post ancestry plus pre exclusion identify remediation lineage in the post release?",
                    "T3": "Does at least one changed-path blob retained at post release identify artifact-level retention?",
                    "T4": "Does every changed-path blob retained at post release identify strict source retention?",
                },
            },
            "selection_provenance": "two lowest SHA-256 identity-key ranks per stable family; no closure outcome used",
        })
    assert len(packets) == 12 and all(key(rows[k]) in selected for k in selected)
    out = {
        "status": "blinded_openwrt_review_packets_no_aggregate_outcomes",
        "packet_count": len(packets),
        "selection_rule": "two lowest SHA-256 identity-key ranks per stable family",
        "review_states": ["identified", "conditional", "not_identifiable"],
        "packets": packets,
    }
    Path("research-os/artifacts/openwrt-blinded-review-packets.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"packet_count": len(packets), "families": sorted({p['identity']['stable_family'] for p in packets})}))


if __name__ == "__main__":
    main()
