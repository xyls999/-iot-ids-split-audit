# IoT IDS Ten-Paper Synthesis

## Collection result

Ten DOI-verified papers are stored locally under `research-os/literature/iot-ids/`. The local collection is metadata + abstracts when Crossref supplied them + reading checklists. Full text must be read from the DOI/publisher link before quoting detailed experimental results.

## What the papers establish

1. **N-BaIoT (P01)** establishes a foundational deep-autoencoder approach for network-based IoT botnet detection and is the easiest starting baseline.
2. **IoT-KEEPER (P02)** moves detection toward online traffic analysis at the edge, making resource and latency constraints central.
3. **TON_IoT (P03)** provides heterogeneous IoT/IIoT telemetry and network data; useful but more complex than N-BaIoT.
4. **CorrAUC (P04)** illustrates feature-correlation and classical ML treatment of malicious Bot-IoT traffic.
5. **Edge-IIoTset (P05)** provides a broader realistic IoT/IIoT cybersecurity benchmark and discusses centralized/federated learning.
6. **CICIoT2023 (P06)** provides a modern large-scale dataset: 33 attack types across seven categories and 105 IoT devices. It is stronger for publication validation but not the easiest first dataset.
7. **IoT-23 ML study (P07)** shows dataset-specific malicious-traffic classification; it is useful as a baseline reference but does not by itself solve cross-device generalization.
8. **ToN-IoT applied IDS study (P08)** is a recent application reference for industrial IoT detection and a warning that “new IDS + one dataset” is a crowded claim.
9. **Cross-domain validation (P09)** directly supports the concern that emulated-device performance may not transfer to real-device traffic.
10. **Label harmonization (P10)** shows that cross-dataset comparison requires explicit mapping of attack labels; otherwise “generalization” results are not comparable.

## Research implication

The strongest defensible contribution is not another deep classifier. A narrower contribution is:

> A lightweight, leakage-controlled IoT traffic detector evaluated under device/time holdout and cross-dataset label harmonization, with accuracy–resource trade-offs reported.

## Recommended staged plan

### Stage 1 — feasibility

- Dataset: N-BaIoT.
- Task: normal vs anomaly binary classification.
- Models: Logistic Regression, Random Forest, LightGBM/XGBoost, small MLP.
- Split: hold out complete devices or time blocks; never randomly split duplicated flow windows without checking capture identity.
- Metrics: Macro-F1, recall, FPR, AUROC, inference time, model size.

### Stage 2 — publication-strength validation

- Add Edge-IIoTset or CICIoT2023.
- Define an explicit common label mapping; do not compare incompatible attack taxonomies.
- Evaluate cross-device and cross-dataset degradation.
- Add feature-count and model-size ablations.

### Stage 3 — optional edge claim

Only claim “resource-constrained/edge-ready” after measuring a real target or a clearly documented hardware proxy. A laptop runtime alone is not an edge deployment result.

## Difficulty assessment

- First prototype: medium, approximately 5/10.
- Defensible paper: medium-high, approximately 6–7/10.
- Main risk: weak novelty and invalid random splits, not model coding.
- Safer than live penetration testing because the work can remain entirely offline and defensive.

## Safety boundary

Use public offline datasets only. Do not scan, exploit, probe or generate traffic against third-party systems. Do not present synthetic attack generation as real-world validation. Do not claim a model detects zero-day attacks unless an appropriate open-set protocol is actually tested.
