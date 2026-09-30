# Session Handoff

## Last completed

- Source-backed B/C journal candidate review completed and saved at `artifacts/journal-candidates-source-review.md`.
- Official evidence saved under `evidence/journal-candidates/`.
- Manifest updated with venue shortlist artifact.

## Scope override

Quadruped robotics, robot dogs, legged sim-to-real and robot-dog navigation are explicitly excluded. Previous robotics artifacts are historical only.

The screenshot was successfully read and transcribed to `literature/screenshot-venue-transcription.md`.

## Current blockers

1. Requested screenshot missing.
2. Research profile and constraints missing: author skills, available robot/data, deadline, APC budget, language preference.
3. Final venue choice cannot be made without topic/data/budget constraints.
4. Current CFP deadlines, fees and indexing must be rechecked immediately before submission.

## Latest research checkpoint

`literature/venue-direction-brief.md` and `literature_matrix/venue-shortlist.csv` rank RGB-D quadruped visual/task navigation as the conditional lowest-risk legitimate route if the robot, D435/Jetson, ROS/ROS2 control, logs and safe test area exist. Sim-to-real adaptation has higher upside but higher novelty and experimental risk. No acceptance promise is made.

## IoT IDS literature checkpoint

Ten DOI-verified papers and local reading notes are at `literature/iot-ids/`. Start with P01/P02/P03/P05/P06, then read P09/P10 for cross-domain and label-harmonization risks. The collection is defensive/offline only.

## Device-fingerprint innovation spike

`reports/nbaiot-common-support-audit-report.md` is the split-sensitivity empirical core: five seeds and two row windows show Random Forest random-row minus mean LODO Macro-F1 of 0.0500–0.0958, with class-dependent raw device probes. `reports/nbaiot-embedding-probe-feasibility-report.md` rejects the CDP→DHG explanatory hypothesis: frozen-MLP probe versus DHG Spearman is -0.600, -0.400, 0.000 over three seeds. Do not implement CDIAR or claim shortcut causality. `literature/iot-ids/second-dataset-auditability-scout-2026-09-30.md` still rejects all checked families as a second strict device-held-out dataset. Only an official second row-to-device/time source can revive a narrow split-sensitivity replication; otherwise pivot.

## Domain-generalization literature checkpoint

`literature/iot-ids/domain-generalization-review.md` records real adjacent work: MMD-AE DTL (2020), GGA/ABRSI heterogeneous adaptation (2023), attention-sharing adaptation (2024), domain generalization (2025), leakage study (2024), and cross-domain validation (2026). New candidates are in `ideas/iot-ids-next-candidates.yaml`; no novelty claim is approved.

## Original-layout preflight checkpoint

`reports/nbaiot-original-preflight-report.md` records a nine-device, 115-feature original-layout mirror test. Benign-only calibration increased false positives and sometimes flagged every benign target row. Device identity was predictable at 99.08% in a diagnostic split. Reject H-IOT-IDS-01 as the primary method.

## Preflight experiment checkpoint

`reports/nbaiot-preflight-report.md` records a leave-one-group-out smoke test on a public Kaggle-derived mirror. Calibration reduced FPR in many groups but sometimes collapsed recall; no validation claim is allowed because device/time metadata are missing. Official UCI download was interrupted at ~1.3 GB.

## Novelty-audit checkpoint

The proposed point is not proven novel. `reviews/iot-ids-novelty-audit.md` records strong overlap with 2026 adjacent work. Treat it as an auditable incremental study, not a new IDS architecture.

## Innovation checkpoint

Candidate ideas: `ideas/iot-ids-candidates.yaml`; independent critique: `ideas/iot-ids-critic.md`; surviving hypothesis: `hypotheses/iot-ids-active.yaml`. Only modified IOT-IDS-01 survived: benign-only target-device threshold calibration under leakage-controlled leave-one-device-out evaluation. Novelty is not yet established.

## Next action

Complete nearest-paper verification for P09/P10, then decide whether modified H-IOT-IDS-01 passes a bounded N-BaIoT feasibility gate.
