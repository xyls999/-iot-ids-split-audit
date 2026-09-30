# Frozen-embedding conditional device-probe feasibility result

**Date:** 2026-09-30  
**Status:** negative feasibility result; rejects the current CDP→DHG paper hypothesis on this one-mirror pilot.

## Question

Does conditional device recoverability from a frozen lightweight IDS representation positively predict the random-row minus leave-one-device-out Macro-F1 gap (DHG)?

## Protocol

- Same N-BaIoT original-layout Kaggle mirror and the six attack labels common to all nine device-number groups as `nbaiot-common-support-audit-report.md`.
- 600 rows per device × label cell, row offset 0; no timestamp claim.
- A 32-unit ReLU `sklearn` MLP attack classifier. It trains on 75% of source-device cells; early stopping is enabled.
- For each held device, the remaining 25% of source-device rows are passed through the frozen MLP. A Random Forest predicts source device number separately within every true attack-label stratum. Mean per-class device-probe Macro-F1 is the pilot CDP statistic.
- The held device is never used for MLP training or for the device-probe data.
- Three seeds (`20260930`, `7`, `23`), nine held-device folds each. The MLP emitted no fit warnings.
- Artifacts: `artifacts/nbaiot-original-preflight/embedding-probe*.json`; executable: `tools/run_nbaiot_embedding_probe.py`.

## Results

| Seed | Random-row MLP Macro-F1 | Mean LODO Macro-F1 | Mean DHG | Mean conditional source-embedding device-probe Macro-F1 | Spearman CDP–DHG across 9 folds |
|---:|---:|---:|---:|---:|---:|
| 20260930 | 0.7642 | 0.6807 | 0.0835 | 0.4633 | -0.600 (p=0.088) |
| 7 | 0.7675 | 0.6849 | 0.0826 | 0.4646 | -0.400 (p=0.286) |
| 23 | 0.7645 | 0.6293 | 0.1352 | 0.4628 | 0.000 (p=1.000) |

The representation retains class-conditional source-device information. For example, on the first seed and held-device-1 model, device-probe Macro-F1 ranges from 0.765 for benign traffic to 0.031 for `gafgyt.udp`.

However, the proposed positive CDP→DHG relationship is not supported: the correlation sign is negative for two seeds and zero for the third, with no significant result. The nine folds are not independent datasets, so the p-values are descriptive only; they are included to prevent an informal correlation story.

## Decision

**Reject the statement “higher conditional device-probe score predicts a larger held-device gap” as the primary paper hypothesis.** The predeclared direction was positive; this pilot produces no stable positive association.

The result does not prove the converse and does not say that representation probes are useless. It shows that this particular probe, model, mirror and support-constrained protocol cannot justify the intended causal/diagnostic claim.

## What remains defensible

The empirical core shifts to a narrower evaluation finding:

> Random-row versus device-held-out performance gaps exist in this coverage-balanced mirror, are window-sensitive and class-specific, but are not explained by a simple conditional device-recoverability score.

This is a negative/benchmark observation. It is not a new IDS model, a leakage claim, or sufficient evidence for submission.

## Next decision gate

Do not invest in CDIAR or in a CDP-based audit method. Either obtain a second officially auditable dataset for a strictly scoped split-sensitivity replication, or pivot away from an IoT IDS paper rather than treating an unsupported probe as a contribution.
