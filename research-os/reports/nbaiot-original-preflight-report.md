# N-BaIoT Original-Layout Leave-One-Device-Out Preflight

**Date:** 2026-09-30  
**Status:** preliminary, not a publication result.

## Data and provenance

- Archive: public Kaggle mirror `sonalimishra3/n-baiot-original-dataset`.
- Local archive: `data/raw/n-baiot-original-kaggle.zip`.
- Bytes: 1,883,140,515.
- SHA-256: `077db76493e7a2f7a592bff9b16a95b9c4f1507750c5f071e3f09212412e4c64`.
- ZIP integrity: `testzip()` returned no error.
- Contents: 92 CSV files, nine device-number groups (`1`–`9`), 115 numeric features, benign file plus attack-category files.
- This is an original-layout mirror, not the directly downloaded UCI archive. The archive has no explicit timestamp column; CSV row order is used only as a capture-order proxy.

## Protocol

For each held-out device:

- Source devices: first 5,000 benign rows per source device plus first 500 rows from each attack-category file.
- Target device: first 5,000 benign rows are a warm-up exclusion; next 2,000 benign rows are calibration; next 3,000 benign rows plus first 500 rows from each attack-category file are test data.
- No attack labels are used for threshold calibration.
- Models: balanced Logistic Regression and balanced Random Forest (100 trees, max depth 18).
- Comparisons: fixed probability threshold 0.5; target-benign 95th-percentile threshold; source-recall-constrained threshold.
- Features are imputed for missing/infinite values inside the model pipeline.

## Results summary

### Logistic Regression

Across nine held-out devices:

- Fixed threshold FPR: `0.000–0.017`.
- Fixed attack recall: `0.940–0.999`.
- Benign-only calibration FPR: `0.015–0.081`.
- Benign-only calibration attack recall: `0.996–1.000`.

Calibration generally **increased** FPR instead of reducing it.

### Random Forest

Across nine held-out devices:

- Fixed threshold FPR: `0.000–0.001`.
- Fixed attack recall: `0.991–1.000`.
- Benign-only calibration FPR: `0.036–1.000`.
- Benign-only calibration attack recall: `1.000`.

The calibration threshold was zero or near zero for several devices, causing almost all test rows to be flagged as attacks. For example, held-out devices 3, 7, 8 and 9 had calibrated FPR `1.000` for Random Forest.

Machine-readable output:

```text
artifacts/nbaiot-original-preflight/results.json
```

## Device-identity diagnostic

A Random Forest trained only on benign rows to predict the nine device numbers achieved:

- 45,000 rows;
- 115 features;
- random within-device diagnostic split;
- accuracy `0.9908`;
- macro-F1 `0.9908`.

This is not a final evaluation because the split is random, but it shows that device-specific signatures are extremely strong in this archive. They must be treated as a domain-shift factor, not ignored.

Output:

```text
artifacts/nbaiot-original-preflight/device-identity-audit.json
```

## Device-feature removal probe

Removing the top 10, 20 or 40 features ranked by the benign device-identity classifier did not produce a meaningful improvement in this preflight. Mean results remained approximately FPR `0.000`, attack recall `1.000`, macro-F1 `1.000`. This probe is exploratory and does not establish a new method.

Output:

```text
artifacts/nbaiot-original-preflight/device-invariant-probe.json
```

## Review conclusion

The candidate idea “benign-only target-device threshold calibration” does not pass this second preflight as a primary innovation:

1. On the earlier nine-group mirror, calibration often lowered FPR but collapsed recall.
2. On the original-layout nine-device mirror, fixed thresholds were already near-perfect while calibration often increased FPR to 1.0.
3. A device-identity diagnostic shows strong device fingerprints.
4. No timestamps are available, so true temporal robustness remains untested.

The candidate is therefore **rejected as a standalone method**. It may remain as a negative/diagnostic experiment inside a broader dataset-audit paper, but no manuscript should claim that calibration solves cross-device generalization.
