from __future__ import annotations

import json
from pathlib import Path

from run_evidence_sensitivity_probe import main


def test_probe_is_deterministic_and_does_not_create_labels(tmp_path, monkeypatch):
    output = tmp_path / "probe.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_evidence_sensitivity_probe.py",
            "--output",
            str(output),
            "--per-family",
            "2",
        ],
    )
    main()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["status"] == "exploratory_evidence_sensitivity_probe_not_labels"
    assert data["counts"]["pairs"] == 62
    assert data["counts"]["tier2_post_ancestor_pre_exclusion"] == 62
    assert data["counts"]["tier3_any_changed_path_blob_retention"] == 54
    assert data["counts"]["tier4_strict_all_changed_path_blob_retention"] == 50
    assert data["counts"]["pilot_selected"] == 12
    assert data["transitions"]["tier2_to_tier4_downgraded"] == 12
    assert all(row["label_status"] == "not_a_cve_label" for row in data["pairs"])
    assert all("affected" not in row for row in data["pairs"])
