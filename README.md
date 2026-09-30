# IoT IDS Split Audit

> **Research status: technical-report case study; not submission-ready.**

中文研究仓库：审计 IoT 入侵检测（IDS）中“随机行切分”和“留一设备组切分”如何改变模型评估结果。

## Current finding

On a locally verified **Kaggle mirror** laid out like N-BaIoT, a coverage-balanced Random Forest experiment found that random-row Macro-F1 exceeded mean leave-one-device-out Macro-F1 by **0.0500–0.0958** across two ordered-row windows and five seeds.

arXiv:2608.15761 already studies random versus device-held-out evaluation and provenance artifacts in IoT IDS. This repository is therefore a restricted, mirror-level replication/case-study record, not a novel split-audit method. It is **not** evidence of:

- official UCI N-BaIoT final-data results;
- real chronological generalization;
- data leakage;
- a new IDS method;
- a causal device-fingerprint mechanism; or
- publication readiness.

The attempted conditional device-probe explanation was tested with a lightweight frozen MLP and rejected as a primary claim: its CDP–DHG correlations were `-0.600`, `-0.400`, and `0.000` across three seeds.

## Read first

| Document | Purpose |
|---|---|
| [`research-os/README-FOR-BEGINNERS-zh.md`](research-os/README-FOR-BEGINNERS-zh.md) | Full beginner-friendly Chinese explanation of the project, experiments, limitations, and next steps. |
| [`research-os/reviews/iot-ids-paper-readiness-review-2026-09-30.md`](research-os/reviews/iot-ids-paper-readiness-review-2026-09-30.md) | Whether drafting or submission is currently justified. |
| [`research-os/drafts/iot-ids-split-sensitivity-introduction-and-methods.md`](research-os/drafts/iot-ids-split-sensitivity-introduction-and-methods.md) | Bounded Chinese technical-report draft. |
| [`research-os/state/manifest.yaml`](research-os/state/manifest.yaml) | Authoritative project state. |

## Reproducible artifacts

- Main split-sensitivity report: [`research-os/reports/nbaiot-common-support-audit-report.md`](research-os/reports/nbaiot-common-support-audit-report.md)
- Frozen-embedding negative result: [`research-os/reports/nbaiot-embedding-probe-feasibility-report.md`](research-os/reports/nbaiot-embedding-probe-feasibility-report.md)
- N-BaIoT original-versus-mirror boundary: [`research-os/literature/iot-ids/n-baiot-primary-protocol-boundary-2026-09-30.md`](research-os/literature/iot-ids/n-baiot-primary-protocol-boundary-2026-09-30.md)
- Dataset schema hunts: [`research-os/literature/iot-ids/`](research-os/literature/iot-ids/)

## Run the current experiments

The raw archive is intentionally ignored by Git. Obtain it only through a documented, authorized route and place it at:

```text
research-os/data/raw/n-baiot-original-kaggle.zip
```

Then run:

```bash
python research-os/tools/test_run_nbaiot_common_support_audit.py
python research-os/tools/run_nbaiot_common_support_audit.py

python research-os/tools/test_run_nbaiot_embedding_probe.py
python research-os/tools/run_nbaiot_embedding_probe.py
```

Validate Research-OS structure:

```bash
python research-os/tools/validate_setup.py
```

## Data and ethics boundary

- Public, offline, defensive research only.
- No network scanning, exploitation, attack execution, credentials, or operational target data.
- The repository excludes raw data archives and generated processed data.
- Do not infer device IDs, timestamps, or collection blocks from filenames, IP addresses, directories, or scenario labels without owner documentation.

## What is required before submission-oriented writing

1. A second public dataset with owner-verified row/file-to-device identity and independent time, capture, or provenance blocks.
2. Official N-BaIoT archive/layout evidence if official-device or temporal wording is desired.
3. Completed duplicate/provenance controls, confidence intervals, converged baselines, and full-text nearest-work checks.

Until then, this repository supports a transparent technical report and reproducibility record—not a novelty or publication claim.
