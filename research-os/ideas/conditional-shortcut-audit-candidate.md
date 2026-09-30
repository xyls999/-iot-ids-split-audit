# Candidate: Conditional Shortcut Audit Card for IoT IDS

**Status:** rejected as a primary explanatory claim after one-mirror embedding-probe feasibility testing; not a novelty claim.

## Motivation

An IDS can achieve high attack accuracy while its learned representation still makes device identity easily recoverable. Device fingerprinting is not automatically invalid: device-specific traffic may contain genuine security information. The relevant question is conditional:

> After attack class is fixed, how much device-identifying information remains in the representation, and does that reliance predict a loss under held-out-device evaluation?

## Proposed audit, not new classifier

For each dataset/model/split configuration, report:

1. **Conditional Device Probe (CDP):** train a device classifier on frozen model representations separately within each class, then aggregate performance. High CDP means that device identity remains recoverable after class is controlled.
2. **Device-Holdout Generalization Gap (DHG):** random-row performance minus leave-one-device-out performance under identical preprocessing contained inside each training fold.
3. **Conditional Feature Reliance (CFR):** within-class, within-device permutation of a feature/feature group; measure attack-score loss versus across-device permutation. This distinguishes attack-useful features from device shortcuts more carefully than simple feature importance.
4. **Attack–Device Coverage Matrix:** show which attack types and devices are observed together; flag missing cells that make device and attack inseparable in the dataset.
5. **Resource card:** model bytes, CPU inference latency and peak host memory measured with the same feature pipeline.

## Distinction from nearby work

- Existing leakage work commonly focuses on test information leaking into feature selection, serialization artifacts or duplicate capture provenance.
- Existing domain adaptation/disentanglement trains a better predictor or aligns distributions.
- This candidate audits *whether a trained IDS representation encodes device shortcut information conditional on attack label* and tests whether that signal predicts failure on unseen devices.

This distinction is a hypothesis. A systematic search must verify whether a NIDS/Iot IDS paper has already defined the same metric/probe suite.

## Minimum empirical standard

- At least N-BaIoT and one independent dataset with device/group labels.
- Random-row, leave-one-device-out, and time/capture-block split wherever timestamps/provenance allow.
- At least Logistic Regression, Random Forest, small MLP and one published adaptation baseline.
- Nested preprocessing/selection and fixed seeds.
- Per-device confidence intervals; no aggregate-only accuracy.
- Negative result is valid: CDP may not predict DHG, in which case reject the audit's central claim.

## Possible paper contribution, if verified

A reproducible **IoT IDS split-sensitivity report** may remain an evaluation artifact. The stronger claim that a conditional device probe exposes or predicts device-dependent shortcut reliance is not supported by the current feasibility test.

## Likely reviewer objection

“Device predictability is expected in IoT traffic and not evidence of leakage.”

Required response: never label it leakage by default; call it *shortcut risk* only when high conditional device probe is associated with degraded device-held-out outcomes, while controlling attack/device coverage.
