# Conditional Shortcut Audit Card: novelty and feasibility check

**Date:** 2026-09-30  
**Scope:** defensive, offline IoT IDS research using public datasets only.  
**Status:** bounded feasibility study may proceed; this is **not** a novelty claim or a method proposal.

## Question

Can a reproducible audit suite test whether device-identifying information retained by a frozen IDS representation—*conditional on the true attack label*—is associated with loss on a held-out device?

The candidate suite is:

- **CDP (Conditional Device Probe):** balanced device prediction from frozen representation within true attack-label strata;
- **DHG (Device-Holdout Generalization Gap):** random-row metric minus leave-one-device-out metric, with all preprocessing contained in each training fold;
- **coverage matrix:** observed device × attack combinations before interpreting CDP or DHG;
- **CFR (Conditional Feature Reliance):** a sensitivity analysis, not a causal test, using conditionally constrained permutation.

## Source policy

A claim below is limited to what its linked primary paper/full text or official DOI metadata establishes. Publisher full text unavailable to this environment is labelled **unverified**; its abstract must not be expanded into an implementation-level claim.

| Work / source | What the source establishes | Relation to candidate | Confidence |
|---|---|---|---|
| Vu et al., *Deep Transfer Learning for IoT Attack Detection* (2020), DOI [`10.1109/ACCESS.2020.3000476`](https://doi.org/10.1109/ACCESS.2020.3000476); locally saved full text: `sources/related/2020-deep-transfer-learning-iot.txt` | Uses two autoencoders with MMD alignment and unlabeled target-device data. Its described N-BaIoT protocol uses internal per-device/attack-type transfer, not the candidate class-conditional device probe plus leave-one-device-out audit. | Adjacent domain adaptation; no direct audit-suite match confirmed. | High |
| Zhang et al., *3D-IDS: Doubly Disentangled Dynamic Intrusion Detection* (2023), DOI [`10.1145/3580305.3599238`](https://doi.org/10.1145/3580305.3599238); locally saved full text: `sources/related/2023-3d-ids.txt` | Learns disentangled attack-related representation in a dynamic graph IDS that uses device identities as graph information. | Adjacent representation disentanglement; no conditional device-recoverability probe or held-device audit confirmed. | High |
| *Cross-Domain Cybersecurity Threat Detection via Self-Supervised Feature Disentanglement* (2025), DOI [`10.1109/CISAT66811.2025.11181896`](https://doi.org/10.1109/CISAT66811.2025.11181896) | The accessible abstract says it disentangles domain-specific and threat-specific features for unseen-domain detection. Full text was not obtained. | Close conceptual overlap with any broad “device/domain versus attack disentanglement” algorithm. It does **not** confirm or refute the exact CDP+DHG audit suite. | Medium, abstract only |
| *Disentangled Dynamic Intrusion Detection* (2025), DOI [`10.1109/TPAMI.2025.3595671`](https://doi.org/10.1109/TPAMI.2025.3595671) | Accessible metadata/abstract describes dynamic and few-shot attack-feature disentanglement. Full text not obtained. | Adjacent; conditional device nuisance suppression and device-held-out protocol unverified. | Low–medium |
| *Enhancing IoT Attack Classification through Domain Generalization* (2025), DOI [`10.1109/ICSC65596.2025.11140153`](https://doi.org/10.1109/ICSC65596.2025.11140153) | Accessible abstract reports comparison of GroupDRO, ANDMASK and Mixup on multiple IoT datasets. Full text not obtained. | Establishes that IoT domain-generalization benchmarking is active; exact split/audit overlap unverified. | Low–medium |
| OpenAlex Works API, [`https://api.openalex.org/works`](https://api.openalex.org/works) | Searches for the exact concepts “conditional device predictability”, “shortcut-learning audit”, “representation probing”, “device-held-out NIDS evaluation”, and “IoT-NIDS dataset auditing” did not return a direct exact audit-suite match in this bounded metadata search. | Absence from metadata search is not evidence of novelty. | Medium |

## What local evidence does and does not show

1. The original-layout N-BaIoT mirror has very strong benign-traffic device fingerprinting: a random within-device diagnostic achieved macro-F1 `0.9908`. **Source:** `research-os/reports/nbaiot-original-preflight-report.md`, “Device-identity diagnostic”, with underlying JSON at `artifacts/nbaiot-original-preflight/device-identity-audit.json`.
2. That result **does not prove data leakage, invalid detection, or cross-device failure**. The same report found near-perfect fixed-threshold leave-one-device-out preflight metrics and no meaningful improvement after removing the top 10/20/40 device-predictive features. **Source:** the same report, “Results summary” and “Device-feature removal probe”.
3. Therefore the only scientifically testable claim is associative and falsifiable:

> Across coverage-supported held-device folds and independent datasets, does source-only CDP predict DHG after accounting for attack prevalence, device imbalance, and the device × attack coverage matrix?

If this association fails under preregistered, fold-contained evaluation, the substantive audit claim must be rejected.

## Required controls before any paper-level conclusion

- Use true labels, not model predictions, for conditioning the CDP.
- Analyze only common-support device × attack strata; report missing/sparse cells rather than impute them.
- Use balanced per-class probes and per-device confidence intervals.
- Keep scaling, feature selection, deduplication, thresholding, and model selection inside each train fold.
- Add capture/time/provenance blocks where the dataset exposes them; the current N-BaIoT mirror lacks explicit timestamps and cannot independently test temporal shortcut risk.
- Treat CFR as sensitivity analysis until a conditional resampling/matching design and permutation sanity checks show it does not merely destroy legitimate feature correlation.

## Decision

- **Reject as an algorithm claim:** a broad attack/device disentanglement method is too close to established and 2025 adjacent work.
- **Keep only as audit feasibility:** no direct match for the full CDP + DHG + coverage suite was confirmed in the bounded evidence search, but no “first” or “novel” claim is justified.
- **Stop condition:** abandon the audit direction if (a) the CDP–DHG association does not replicate on two auditable datasets, (b) coverage support is too sparse, or (c) gaps disappear under duplicate/provenance/time controls.

## Next evidence gate

Before implementation, identify a second public dataset whose official documentation exposes defensible device/group identity **and** capture/time or provenance blocks. Then preregister the CDP–DHG association test and baseline protocol.
