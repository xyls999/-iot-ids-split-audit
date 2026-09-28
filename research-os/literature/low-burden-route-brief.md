# Low-Burden Legitimate Publication Route

**Workflow:** `low-burden-venue-research-mulboum8-xugjvr`  
**Scope:** non-water, non-robot-dog, no-special-hardware, public-data research.

## Recommendation

**Topic:** Public-data sensor calibration / measurement correction under temporal drift  
**Primary venue:** **电子测量与仪器学报**  
**Backups:** **Measurement Science and Technology**, **Digital Signal Processing**

This is a comparatively feasible route, not a guaranteed-acceptance route.

## Why this route

- The journal is listed as **C** in the supplied Hohai catalog, ISSN `1000-7105`.
- Its official scope includes electronic measurement, sensors, information processing, calibration, fault diagnosis and AI detection.
- Official submission pages reviewed in the workflow describe double-blind review and a three-review process; no official acceptance rate was found.
- The workflow verified a 2026 fee notice: review fee about RMB 300/article and page fee about RMB 600/page. Recheck before submission.
- The project can use public data and laptop-scale Python experiments; no special hardware is required.

## Proposed research question

Can a lightweight, leakage-free, time-aware calibration protocol reduce the degradation of low-cost air-quality sensor estimates under temporal drift and missing data while keeping model size and inference cost low?

## Dataset

Primary candidate: **UCI Air Quality** dataset, using raw sensor channels and reference pollutant measurements. Possible targets include CO, NOx, NO2 and benzene. Confirm download integrity, missing-value markers and licensing before use.

## Minimum experiment

1. Chronological train/validation/test split; no random leakage across time.
2. Predict reference concentration from raw sensor and environmental channels.
3. Compare static calibration with rolling-window/drift-aware recalibration.
4. Add missing-data and noise robustness tests.
5. Report performance by time window, not only one aggregate score.

## Baselines

- raw/no-calibration baseline
- linear regression
- Ridge/Lasso
- Random Forest
- XGBoost or LightGBM
- SVR or Gaussian Process Regression
- small MLP

## Metrics

MAE, RMSE, R², mean bias, calibration slope/intercept, degradation across time windows, inference time, parameter count/model size.

## Defensible contribution boundary

Do not claim novelty as merely applying XGBoost to UCI Air Quality. A defensible contribution would be a reproducible temporal-drift and missingness protocol, a lightweight calibration comparison, and an accuracy–cost analysis under realistic chronological validation.

## Why other screenshot venues are poorer fits

- 土壤学报: requires a real soil-science contribution.
- 中国电机工程学报: power-engineering domain and higher evidence burden.
- 中国激光: optical/laser system contribution normally requires specialized experiments.
- 中兴通讯技术: better for telecom, edge computing, PON/5G and network operations.
- 微电子学与计算机 / 小型微型计算机系统: scope/details were not reliably verifiable in this run.
- 物联网学报: possible for an IoT architecture/prototype, but less direct than measurement calibration.
- 机器人: outside the active project scope.

## Alternatives if the researcher dislikes air-quality data

1. IoT intrusion/anomaly detection with cross-dataset generalization — defensive security, but more crowded and cyber-specific.
2. Software defect prediction with temporal validation and calibration — no hardware, but high novelty risk and software-engineering venue fit is narrower.
3. Lightweight multivariate time-series forecasting under accuracy–cost constraints — broad but crowded; requires strong leakage control and meaningful cost analysis.

## Evidence provenance

- Hohai catalog: `literature/hhue-catalog-extracted.txt`.
- Screenshot transcription: `literature/screenshot-venue-transcription.md`.
- Full delegated source review: `C:/Users/Administrator/.pi/workflows/projects/water-paper-61b15211d27c/runs/low-burden-venue-research-mulboum8-xugjvr.json`.
- Venue evidence and recent-paper observations were gathered from official journal/editorial pages or DOI/Crossref records where available. Acceptance rates were not verified.
