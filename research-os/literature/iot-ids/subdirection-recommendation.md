# Recommended IoT IDS Subdirection

## Recommended title

**面向资源受限物联网的无泄漏轻量流量异常检测与跨设备泛化研究**

English working title: *Leakage-Free Lightweight IoT Traffic Anomaly Detection Under Cross-Device Generalization*

## Why this subdirection

Compared with generic “improved neural-network IDS,” this direction has a concrete evaluation problem:

1. Models trained on one device often fail on another device.
2. Random row splits can mix highly similar flows from the same capture and inflate scores.
3. Some public datasets contain serialization, device-identity or label leakage.
4. Resource-constrained deployment requires a trade-off among F1, false positives, memory, parameters and latency.

The topic remains pure software if all experiments use public offline datasets and measured/proxied resource cost. A real embedded board is optional, not required for the first paper.

## Bounded research question

> Under a fixed leakage-controlled device/time split, how much detection performance is retained when feature count and model complexity are reduced, and does the ranking remain stable across a second IoT dataset?

## Proposed contribution

Not a new large neural architecture. The contribution should be a reproducible protocol combining:

- leakage audit;
- device-level or time-block holdout;
- lightweight feature selection;
- classical/lightweight ML baselines;
- resource-performance Pareto analysis;
- cross-dataset label mapping and validation when feasible.

## Dataset path

### Feasibility dataset

`N-BaIoT`: start with a binary normal/anomaly task and device-level holdout. It is relatively manageable and has a clear foundational paper.

### Publication-strength check

Add one of:

- `Edge-IIoTset`, only after inspecting provenance and possible leakage;
- `CICIoT2023`, if storage and preprocessing are manageable.

Do not start with all datasets at once.

## Minimum models

- Logistic Regression
- Decision Tree
- Random Forest
- LightGBM/XGBoost
- small MLP

Optional later: a compact autoencoder or knowledge-distilled model. No Transformer/GNN is needed for the first experiment.

## Minimum metrics

- Macro-F1
- Recall and FPR
- AUROC/AUPRC for imbalance
- per-device performance
- model size/parameter count
- CPU inference time
- peak memory or a clearly documented proxy

## Minimum baselines and splits

1. Random row split only as a warning baseline, never the main result.
2. Time-block split.
3. Leave-one-device-out split.
4. If adding a second dataset, define a documented common-label map and report unmapped classes.

## Difficulty

- Download/parse first dataset: 3–5/10.
- Baseline ML: 3–4/10.
- Leakage audit and device split: 6/10.
- Cross-dataset alignment: 7/10.
- Defensible paper: 6–7/10.

## Venue fit

Primary domestic candidate: `物联网学报` if the manuscript emphasizes IoT system/edge relevance.  
Alternative: `中兴通讯技术` if the framing is communication-network diagnosis/edge analytics.  
PDF C-level alternatives: `Computer Communications` or `Ad Hoc Networks`, but they are more demanding and not automatically easier.

## Two-week feasibility gate

- Days 1–2: obtain N-BaIoT, record hash/source/license, parse labels and device IDs.
- Days 3–4: run Logistic Regression, Random Forest and LightGBM on a time split.
- Days 5–6: implement leave-one-device-out evaluation.
- Days 7–8: perform feature-count ablation and leakage checks.
- Days 9–10: measure model size, inference time and peak memory.
- Days 11–12: reproduce one published baseline from P01/P02 or the local notes.
- Days 13–14: decide whether the cross-device gap is large and stable enough to justify a paper.

If the device holdout causes performance to collapse or the dataset cannot be audited, do not hide the result; treat it as a direction failure or narrow the research question.
