# IoT IDS paper-readiness review

**Date:** 2026-09-30  
**Decision authority:** this review records evidence and a conservative project decision; it does not establish publication acceptance or absence of prior art.

## Decision matrix

| Decision | Verdict | Evidence |
|---|---|---|
| Start a bounded technical report / manuscript skeleton | **YES** | `reports/nbaiot-common-support-audit-report.md` provides a reproducible common-support protocol and a Random Forest random-row minus LODO Macro-F1 discrepancy of 0.0500–0.0958 across two ordered row windows and five seeds. |
| Start a submission-oriented manuscript | **NO** | `state/blockers.yaml` lists the high-severity second-auditable-IoT-dataset blocker. Both dataset hunts reject the checked candidates for strict device-held-out replication: `literature/iot-ids/second-dataset-auditability-scout-2026-09-30.md` and `second-dataset-owner-schema-hunt-2026-09-30.md`. |
| Claim a new method, novelty, chronology, leakage, or CDP→DHG mechanism | **NO** | The frozen-embedding pilot rejects the predicted positive CDP→DHG relation (`reports/nbaiot-embedding-probe-feasibility-report.md`). The novelty record forbids “first”/“novel” language (`literature/iot-ids/conditional-shortcut-audit-novelty-check-2026-09-30.md`); older novelty audit also rejects a new-method claim (`reviews/iot-ids-novelty-audit.md`). The protocol boundary prohibits upgrading mirror rows to official device or time facts (`literature/iot-ids/n-baiot-primary-protocol-boundary-2026-09-30.md`). |

## What may be drafted now

A narrowly framed technical report, or a manuscript skeleton clearly marked as non-submission-ready:

> **A reproducible, coverage-balanced split-sensitivity case study on a locally verified N-BaIoT Kaggle mirror:** random-row evaluation exceeded leave-one-device-out Random Forest Macro-F1 by 5.0–9.6 points, with class- and row-window-dependent magnitude.

Required language:

- call the data a **Kaggle mirror**, not official-UCI final data;
- call row windows **ordered row windows**, not time windows;
- describe device numbers as **mirror groups**, not owner-verified row identities;
- present device probes as descriptive diagnostics, not leakage or causal tests;
- include the negative MLP CDP→DHG result rather than omitting it.

## Top blockers to a credible submission

1. **No second auditable dataset:** no owner-verified row/device mapping plus independent time/capture/provenance block is available for replication.
2. **Primary mechanism rejected:** three MLP seeds produced CDP–DHG Spearman values `-0.600`, `-0.400`, and `0.000`; the proposed positive explanatory claim is unsupported.
3. **Sole empirical source is an unverified mirror:** no official layout manifest maps current mirror directories/row order to Table-3 device IDs or chronological partitions.

Additional limitations: the Logistic Regression baseline emitted convergence warnings; duplicate/provenance checks and confidence intervals remain incomplete; several nearest-work checks are abstract/metadata-only rather than full-text.

## Review process

A fresh-context read-only reviewer independently reached the same decisions: begin a bounded technical report, block submission claims, and do not make novelty/method/temporal/leakage claims. Its assessment is corroborative only; the cited project artifacts above remain the evidence base.

## Project decision

**Begin drafting only a bounded technical-report skeleton if useful. Do not begin a submission draft, select a target venue, or present a contribution claim until the three blockers are resolved.**
