# Nearest-Paper Verification — IoT IDS Candidate

**Date:** 2026-09-29  
**Question:** Does benign-only target-device threshold calibration under leave-one-device-out already appear as the same contribution?

## P09: Cross-domain validation

- Title: *From Emulated IoT Device to Real-IoT Device Traffic: A Dataset-Centered Cross-Domain Validation Framework for Anomaly-Based Intrusion Detection in Internet of Things*
- DOI: `10.1109/ACCESS.2026.3675745`
- Source checked: Crossref metadata, Semantic Scholar record and abstract; IEEE full-text page was blocked by an anti-bot response during this session.
- Open-access evidence: Semantic Scholar/Unpaywall report publisher open access, CC BY; the PDF URL was not retrievable in this environment.
- Abstract-level finding: the paper proposes a dataset-centered cross-domain validation framework using deep transfer learning, four deep-learning models and EmuIoT-VT, evaluated on a held-out test set with accuracy, precision, recall, F1, error rate and confusion matrices.
- Relevance: **very close on cross-domain/held-out validation**, but the checked abstract does not mention benign-only target-device calibration, threshold recalibration, or resource Pareto analysis.
- Status: exact overlap **not established**; full-text verification remains required before a novelty claim.

## P10: Label harmonization

- Title: *A Rule-Based Label Harmonization Framework for Cross-Dataset IoT Intrusion Detection*
- DOI: `10.1016/j.iot.2026.102030`
- Source checked: Crossref metadata, Semantic Scholar record and Unpaywall; Crossref supplied no abstract and ScienceDirect PDF was blocked by a 403/Cloudflare response.
- Open-access evidence: Unpaywall/Semantic Scholar report CC BY/hybrid open access, but the publisher PDF was not retrievable here.
- Relevance: directly covers cross-dataset label comparability, not target-device threshold calibration.
- Status: adjacent, not an exact duplicate; full-text verification remains required.

## Additional adjacent records

- `10.3390/app16052284`: *Operationally Constrained Zero-Day Intrusion Detection with Target-FPR Calibration and Similarity Graph Construction* (2026). Crossref metadata confirms the target-FPR-calibration theme, but detailed method overlap with IoT/device calibration was not verified here.
- `10.1109/access.2026.3732976`: *DA-DCC-IDS: Trustworthy Open-Set IoT Intrusion Detection under Temporal and Device Uncertainty* (2026). Crossref metadata confirms temporal/device uncertainty is already a named IoT IDS problem; detailed method overlap was not verified here.
- `10.1109/icce67443.2026.11449678`: *Lightweight Feature Bridging for On-Device Cross-Domain Intrusion Detection in IoT Environments* (2026). Crossref metadata confirms lightweight cross-domain bridging is already adjacent; detailed method overlap was not verified here.

## Peer-review conclusion

The candidate survives only as a **conditional incremental calibration study**. It is not safe to claim “first” or “novel method.” The defensible contribution, if any, must be an experimentally demonstrated effect under a strict protocol:

- fixed benign calibration budget;
- no attack labels in calibration;
- chronological and device-isolated split;
- contamination-negative control;
- FPR reduction without unacceptable recall loss;
- resource measurements;
- independent replication on a second dataset.

If the effect is only ordinary threshold tuning or disappears under leakage-controlled splits, reject the candidate.
