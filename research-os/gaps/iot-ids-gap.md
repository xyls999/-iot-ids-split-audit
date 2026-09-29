# IoT IDS Research Gap Draft

**Status:** candidate gap, not yet validated as novel.

## Evidence already collected

- P01 N-BaIoT: device-specific deep autoencoders establish normal-behaviour detection.
- P02 IoT-KEEPER: online traffic analysis at the edge establishes an edge/resource-aware framing.
- P05 Edge-IIoTset: broad IoT/IIoT benchmark and centralized/federated context.
- P06 CICIoT2023: modern large-scale attack benchmark.
- P09 cross-domain validation: emulated-to-real domain shift is explicitly studied.
- P10 label harmonization: cross-dataset comparison requires explicit attack-label mapping.
- Open papers 2604.11324 (BRIDGE/TCH-Net): heterogeneous multi-dataset benchmark and leave-one-dataset-out evaluation.
- Open paper 2608.15761: Edge-IIoTset preprocessing can leak labels through serialization/provenance artifacts; device holdout can collapse performance.
- Open paper 2605.02987 (LiteShield): hybrid feature selection + lightweight classifiers + resource analysis is already a direct precedent.
- Open paper 2403.15509: self-distillation for compact IoT attack detection is already a precedent.

## Saturated or unsafe claims to avoid

- “First lightweight IoT IDS.”
- “First feature-selection IoT IDS.”
- “First cross-dataset IoT generalization study.”
- “Detects zero-day attacks” without an open-set protocol.
- “Edge deployment” without target-device measurements.
- Accuracy claims from random row splits that mix the same capture/device/time window.

## Candidate gap

A modest, testable gap remains around a **device-independent, leakage-audited, resource-aware protocol**: train a small model on source devices, use a strictly limited benign-only calibration set from a held-out device to choose a threshold or recalibration rule, and measure the accuracy–false-positive–resource trade-off under leave-one-device-out evaluation.

This is a hypothesis. It must be checked against P09, P10, BRIDGE/TCH-Net and the latest publisher literature before being called novel.
