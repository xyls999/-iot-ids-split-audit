# Full-text audit: BRIDGE and TCH-Net (arXiv:2604.11324)

**Audit date:** 2026-09-30  
**Audit scope:** determine whether BRIDGE directly covers the remaining bounded elements of the N-BaIoT mirror case study.  
**Overall result:** partial overlap; no basis for a novelty claim.

## Primary sources

- Ammar Bhilwarawala, Likhamba Rongmei, Harsh Sharma, Arya Jena, Kaushal Singh, Jayashree Piri, Raghunath Dey. *BRIDGE and TCH-Net: Heterogeneous Benchmark and Multi-Branch Baseline for Cross-Domain IoT Botnet Detection*, arXiv:2604.11324v1, 2026-04-13. [Official record](https://arxiv.org/abs/2604.11324), [official full text](https://arxiv.org/html/2604.11324v1).
- Linked author repository and version note: https://github.com/Ammar-ss/TCH-Net#readme

## Verified v1 findings

| Audit dimension | Verified finding | Source |
|---|---|---|
| Datasets | CICIDS-2017, CIC-IoT-2023, Bot-IoT, Edge-IIoTset and N-BaIoT. | [§3.2](https://arxiv.org/html/2604.11324v1) |
| Harmonization | 46 features and binary benign/attack labels. | [§§3.3, 4.1](https://arxiv.org/html/2604.11324v1) |
| Splits | 80:20 stratified random windows, early/late temporal split and held-dataset evaluation. | [§3.4.6, §§5.8–5.9](https://arxiv.org/html/2604.11324v1#S5) |
| Leakage/provenance | Reports training-only scaling and hash checks; overlapping-window independence remains unverified. | [§§3.4, 4.5](https://arxiv.org/html/2604.11324v1) |
| Results | Random F1 0.8296, temporal F1 0.8203 and held-dataset F1 0.5577; N-BaIoT held-dataset F1 0.6021. | [Tables 7, 12–13](https://arxiv.org/html/2604.11324v1#S5) |
| Limits | Notes untrained held-domain embeddings, testbed limits, binary scope and microcontroller constraints. | [§6.6](https://arxiv.org/html/2604.11324v1) |

## Comparison with the local N-BaIoT case-study protocol

| Case-study element | Classification | Basis |
|---|---|---|
| Restricting to labels shared across all held groups | **NONE in BRIDGE v1** | BRIDGE collapses labels to binary benign/attack and does not report a groupwise multiclass label intersection. [§4.1](https://arxiv.org/html/2604.11324v1) |
| Random-row versus held-device evaluation | **PARTIAL** | BRIDGE compares random windows with held datasets, not a device/capture holdout within one dataset. [§5.9](https://arxiv.org/html/2604.11324v1#S5) |
| Multiple ordered sampling-window sensitivity | **PARTIAL** | It includes an early/late temporal split, but uses a fixed window configuration (`W=32`, `S=4`) rather than a sampling-window sweep. [§5.8 and Table 6](https://arxiv.org/html/2604.11324v1#S5) |

The non-overlap in the table is **not** novelty evidence. It only means this one full-text audit did not find direct coverage for those protocol details.

## Version boundary

The linked author repository explicitly says it documents a subsequent manuscript under review and that the arXiv version remains unchanged during review. The repository describes a revised benchmark with CICIDS-2017, BCCC-2024, CICIoMT-2024 and UNSW-NB15; it excludes N-BaIoT-style exports for insufficient feature coverage and removes the contextual branch. Its reported revised metrics and test-time BatchNorm calibration belong to that later evaluation, not arXiv v1.

Do not silently attribute repository-revision datasets, architecture or results to arXiv:2604.11324v1.

## Consequence for this project

BRIDGE reinforces that random, temporal and held-domain comparisons are established. The local N-BaIoT mirror report may still document its exact common-support and ordered-row-window controls as a restricted technical replication detail, but it cannot call those details a novel research contribution without much broader full-text verification and independent data.

No BRIDGE result supplies the missing official row-to-device/time mapping or a second auditable dataset for the local work.

## Audit boundary

The external audit executor was allowed to inspect official arXiv and linked author-repository materials but was blocked from local shell access. This note preserves only its primary-source findings. No datasets were downloaded and no experiments were reproduced.
