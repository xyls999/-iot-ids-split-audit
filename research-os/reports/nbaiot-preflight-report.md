# N-BaIoT Preflight Experiment Report

**Date:** 2026-09-29

## Scope

This is a **preflight smoke experiment**, not the final official UCI result. The tested archive is a public Kaggle mirror (`nguynhnhthuy/n-baiot-final`) containing nine CSV files. The files have 15 numeric features and a `Label` column, but no timestamp column and no verified device-name column. We therefore treat file identity as a temporary group proxy only.

## Provenance and download status

- Official UCI archive: 1.7 GB compressed / about 2.2 GB uncompressed according to the UCI page; the direct connection terminated after approximately 1.3 GB during this run.
- Zenodo record `3673877` (N-BaIoT_data.mat): resumable but extremely slow; the run was stopped before completion.
- Kaggle mirror downloaded for a bounded smoke test: `research-os/data/raw/n-baiot-final-kaggle.zip`.
- Kaggle ZIP SHA-256: `b715d2771f197f50956631c12c42837eb6fb93bd53ff129129b17d79a7e783d2`.
- The Kaggle mirror is not treated as official provenance for a final paper.

## Data inspection

| Group file | sampled rows | benign | attack | features |
|---|---:|---:|---:|---:|
| `Final/merge_dataframe_1.csv` | 4000 | 2000 | 2000 | 15 |
| `Final/merge_dataframe_2.csv` | 4000 | 2000 | 2000 | 15 |
| `Final/merge_dataframe_3.csv` | 4000 | 2000 | 2000 | 15 |
| `Final/merge_dataframe_4.csv` | 4000 | 2000 | 2000 | 15 |
| `Final/merge_dataframe_5.csv` | 4000 | 2000 | 2000 | 15 |
| `Final/merge_dataframe_6.csv` | 4000 | 2000 | 2000 | 15 |
| `Final/merge_dataframe_7.csv` | 4000 | 2000 | 2000 | 15 |
| `Final/merge_dataframe_8.csv` | 4000 | 2000 | 2000 | 15 |
| `Final/merge_dataframe_9.csv` | 4000 | 2000 | 2000 | 15 |

The original files contain far more rows; the preflight caps each class at 2,000 rows per group. Labels are mapped as `BENIGN=0`, all other labels=`1`.

## Protocol

1. For each group, read CSV in chunks; replace infinities with missing values and use median imputation inside each model pipeline.
2. Sample at most 2,000 benign and 2,000 attack rows per group.
3. For each of nine held-out groups, train on the other eight groups.
4. Reserve 20% of held-out benign rows for benign-only threshold calibration; evaluate on the remaining benign rows plus all sampled attacks.
5. Compare fixed threshold 0.5 with the 95th percentile of the held-out benign calibration scores.
6. Models: balanced Logistic Regression and balanced Random Forest (80 trees, max depth 16).

## Results

| held-out group | model | fixed FPR | calibrated FPR | fixed attack recall | calibrated attack recall | fixed macro-F1 | calibrated macro-F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| `Final/merge_dataframe_1.csv` | logistic_regression | 0.998 | 0.066 | 1.000 | 0.000 | 0.359 | 0.293 |
| `Final/merge_dataframe_1.csv` | random_forest | 0.599 | 0.598 | 0.999 | 0.996 | 0.689 | 0.688 |
| `Final/merge_dataframe_2.csv` | logistic_regression | 0.477 | 0.052 | 1.000 | 0.000 | 0.763 | 0.296 |
| `Final/merge_dataframe_2.csv` | random_forest | 0.276 | 0.274 | 0.996 | 0.994 | 0.868 | 0.868 |
| `Final/merge_dataframe_3.csv` | logistic_regression | 0.887 | 0.049 | 1.000 | 0.001 | 0.470 | 0.298 |
| `Final/merge_dataframe_3.csv` | random_forest | 0.226 | 0.009 | 0.992 | 0.270 | 0.890 | 0.552 |
| `Final/merge_dataframe_4.csv` | logistic_regression | 0.870 | 0.042 | 1.000 | 0.000 | 0.486 | 0.299 |
| `Final/merge_dataframe_4.csv` | random_forest | 0.029 | 0.039 | 0.999 | 1.000 | 0.986 | 0.982 |
| `Final/merge_dataframe_5.csv` | logistic_regression | 0.703 | 0.068 | 0.999 | 0.001 | 0.619 | 0.294 |
| `Final/merge_dataframe_5.csv` | random_forest | 0.176 | 0.048 | 0.997 | 0.403 | 0.917 | 0.632 |
| `Final/merge_dataframe_6.csv` | logistic_regression | 0.654 | 0.051 | 1.000 | 0.000 | 0.653 | 0.297 |
| `Final/merge_dataframe_6.csv` | random_forest | 0.158 | 0.152 | 0.991 | 0.987 | 0.922 | 0.922 |
| `Final/merge_dataframe_7.csv` | logistic_regression | 0.504 | 0.111 | 0.999 | 0.927 | 0.747 | 0.909 |
| `Final/merge_dataframe_7.csv` | random_forest | 0.115 | 0.113 | 0.995 | 0.989 | 0.944 | 0.943 |
| `Final/merge_dataframe_8.csv` | logistic_regression | 0.912 | 0.124 | 1.000 | 0.874 | 0.447 | 0.873 |
| `Final/merge_dataframe_8.csv` | random_forest | 0.400 | 0.398 | 0.999 | 0.998 | 0.805 | 0.806 |
| `Final/merge_dataframe_9.csv` | logistic_regression | 0.956 | 0.256 | 1.000 | 0.861 | 0.404 | 0.804 |
| `Final/merge_dataframe_9.csv` | random_forest | 0.814 | 0.007 | 0.998 | 0.560 | 0.533 | 0.748 |

Full machine-readable output: `research-os/artifacts/nbaiot-preflight/results-loo.json`.

## Interpretation

1. Benign-only calibration often reduced FPR, but it could also destroy attack recall. For example, the held-out group 3 Random Forest changed from FPR 0.226 / attack recall 0.992 to FPR 0.009 / attack recall 0.270.
2. Logistic Regression was unstable under this cross-group proxy: in several groups calibration drove attack recall close to zero. This is a useful negative result, not evidence of a successful method.
3. Random Forest was more stable on some groups, but the effect was not uniform; group 9 changed from FPR 0.814 / recall 0.998 to FPR 0.007 / recall 0.560.
4. The experiment supports the need for a predeclared FPR–recall trade-off and contamination controls. It does **not** validate the proposed innovation.

## Validity limits

- File groups are not verified device IDs; the Kaggle mirror does not expose timestamps or capture provenance in these CSVs.
- Sampling is not a chronological split.
- The target calibration set is not guaranteed to be a naturally continuous benign window.
- Only binary labels and 15 features are present in this mirror.
- No real embedded hardware was used.
- Results cannot be cited as final N-BaIoT official-dataset results.

## Decision

`H-IOT-IDS-01` remains **conditional and not validated**. Before any paper claim, repeat on the official UCI archive or an auditable mirror with verified device IDs and timestamps. The calibration objective should be constrained, for example: minimize FPR subject to attack recall not falling below a predeclared tolerance.
