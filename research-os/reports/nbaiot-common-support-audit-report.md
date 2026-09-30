# N-BaIoT common-support device-split audit

**Date:** 2026-09-30  
**Status:** reproducible one-dataset feasibility result; not a paper-ready cross-dataset claim.  
**Scope:** offline defensive analysis of the locally verified original-layout Kaggle mirror. This is not an official-UCI final result.

## Question

When every evaluated device has the same attack-label support, how much does a conventional random-row split overstate multiclass attack-classification performance relative to holding out a device group?

This experiment does **not** claim that a high device probe proves data leakage or that it causes the performance gap.

## Protocol

- Archive: `data/raw/n-baiot-original-kaggle.zip`; archive-integrity test passed. SHA-256 and mirror limitations are documented in `reports/nbaiot-original-preflight-report.md`.
- Nine mirror device-number groups; 115 numeric features.
- To remove a known coverage confound, the analysis used only the six labels present for **all nine** groups: `benign`, `gafgyt.combo`, `gafgyt.junk`, `gafgyt.scan`, `gafgyt.tcp`, and `gafgyt.udp`.
- Exactly 600 earliest rows per device × label cell: 32,400 rows total, balanced across all 54 cells.
- **Random-row baseline:** 25% test set stratified by device × class cell.
- **Leave-one-device-out (LODO):** train on eight groups and test on the ninth; identical common-support rows.
- Baselines: Logistic Regression and Random Forest. Random Forest uses 100 trees, maximum depth 18. Results are in `artifacts/nbaiot-original-preflight/common-support-audit*.json` and the executable protocol is `tools/run_nbaiot_common_support_audit.py`.
- Five seeds: `20260930`, `7`, `23`, `47`, `101`. The seed changes random splits and Random Forest fitting, but not the first-row sampling rule.

## Results

### Stable random-versus-device-held-out gap

| Model | Random-row Macro-F1 range across 5 seeds | Mean LODO Macro-F1 range across 5 seeds | Random − mean LODO Macro-F1 gap | Interpretation |
|---|---:|---:|---:|---|
| Random Forest | 0.8834–0.8878 | 0.7893–0.8020 | **0.0832–0.0958** (mean 0.0879) | A stable 8.3–9.6 percentage-point aggregate gap in this mirror/protocol. |
| Logistic Regression | 0.6883–0.6957 | 0.6367 (fixed because source-only fit does not use split seed) | 0.0517–0.0590 (mean 0.0559) | Exploratory only: several fits emitted an `lbfgs` convergence warning at `max_iter=350`. |

The Random Forest result is the most reliable current evidence because it had no convergence warning. It is still only a one-mirror result.

### Row-window sensitivity

The same five seeds were repeated after moving every device × class sampling window forward by 2,000 rows. This is an ordering sensitivity check, **not** a temporal evaluation: the mirror has no verified timestamps.

| Random Forest window | Random − mean LODO Macro-F1 gap across 5 seeds |
|---|---:|
| rows 0–599 | 0.0832–0.0958 (mean 0.0879) |
| rows 2,000–2,599 | **0.0500–0.0535** (mean 0.0513) |

The gap persists in the later window but is smaller. Therefore the defensible phenomenon is not a fixed “8.8 point” effect. It is a **window-sensitive 5.0–9.6 point random-versus-device-held-out discrepancy** in this mirror and protocol. This strengthens the need to report sampling/capture-window sensitivity rather than choosing a favourable slice.

### Gap is class-specific

For seed `20260930`, Random Forest random-row versus mean LODO class F1 was:

| Class | Random-row F1 | Mean LODO F1 | Gap |
|---|---:|---:|---:|
| benign | 0.999 | 0.939 | 0.060 |
| gafgyt.combo | 0.999 | 0.826 | 0.173 |
| gafgyt.junk | 0.999 | 0.827 | 0.172 |
| gafgyt.scan | 1.000 | 0.995 | 0.005 |
| gafgyt.tcp | 0.542 | 0.409 | 0.134 |
| gafgyt.udp | 0.761 | 0.785 | -0.024 |

Thus the aggregate gap is not a uniform degradation. A report that gives only one aggregate accuracy/F1 would hide both large class-specific drops and one class where held-device performance was slightly higher.

### Conditional raw-feature device probes

A Random Forest device classifier was evaluated within each **true** class on balanced data. These are input-feature probes—not frozen IDS representation probes.

| Fixed true class | Device-probe Macro-F1 |
|---|---:|
| benign | 0.979 |
| gafgyt.combo | 0.589 |
| gafgyt.junk | 0.344 |
| gafgyt.scan | 0.320 |
| gafgyt.tcp | 0.084 |
| gafgyt.udp | 0.022 |

This directly falsifies a simplistic story that “device identity is always equally recoverable.” Device recoverability depends strongly on the attack condition. It also does **not** establish a monotonic CDP→DHG relationship: the probe operates on raw features, while DHG is model- and held-device-specific.

## What has been earned

The project now has a defensible **empirical core for a technical report or paper skeleton**:

> On a coverage-balanced N-BaIoT mirror, random-row evaluation exceeds leave-one-device-out Random Forest multiclass Macro-F1 by 5.0–9.6 points across two ordered sampling windows and five seeds; the discrepancy and device signal are attack-class dependent.

The supported contribution at this point is an **evaluation finding**, not a new detection method and not evidence of leakage.

## What is still missing before a manuscript claim

1. A second dataset with official row-to-device and capture/time/provenance evidence; the current search gate remains blocked (`literature/iot-ids/second-dataset-auditability-scout-2026-09-30.md`).
2. Additional row-offset/capture-block sampling. The 2,000-row offset already shows magnitude sensitivity, and the current mirror lacks explicit timestamps, so neither window supports a chronological claim.
3. A converged linear baseline and at least one neural representation if the project retains a frozen-representation CDP claim.
4. Confidence intervals, duplicate/provenance checks and a preregistered association test before claiming that a conditional device probe predicts any generalization gap.

## Decision

- Keep the **coverage-aware random-versus-LODO audit** as the strongest current paper seed.
- Do not claim that device fingerprints are leakage, or that the raw-feature probe is the proposed conditional representation audit.
- The evidence is sufficient to start a **methods/results outline**, but insufficient to submit or to call the full two-dataset Shortcut Audit Card validated.
