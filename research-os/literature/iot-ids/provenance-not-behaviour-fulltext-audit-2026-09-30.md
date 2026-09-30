# Full-text audit: *Provenance, Not Behaviour* (arXiv:2608.15761)

**Audit date:** 2026-09-30  
**Overall overlap:** direct at the general methodological level; N-BaIoT-specific overlap remains unverified.

## Primary source

- Mostafa M. Galal, *Provenance, Not Behaviour: A Serialisation Artifact in Edge-IIoTset and a Leakage-Free Benchmark for Precision-Agriculture Intrusion Detection*, arXiv:2608.15761v1, 2026-08-16.
- Official abstract: https://arxiv.org/abs/2608.15761
- Official HTML full text: https://arxiv.org/html/2608.15761v1

## Verified primary-source evidence

| Item | Finding | Official source |
|---|---|---|
| Dataset | Uses Edge-IIoTset ML/DNN subsets and reconstructs AgriEdge with 1,276,122 rows and five devices. | [Abstract](https://arxiv.org/abs/2608.15761) |
| Provenance mechanism | Missing-field spellings `0` versus `0.0` encode parsing provenance; four columns recover labels perfectly. | [Abstract](https://arxiv.org/abs/2608.15761), [§4.3/§5.1](https://arxiv.org/html/2608.15761v1#S5.SS1) |
| Variables | Discusses `dns.qry.name.len`, `mqtt.conack.flags`, `mqtt.protoname`, and `mqtt.topic`; AgriEdge retains device/capture attribution. | [§4.3/§5.1, Tables 1–3](https://arxiv.org/html/2608.15761v1#S5.SS1) |
| Splits | Compares random-stratified 80/20 with LODO; the LODO protocol holds out one device’s normal traffic together with 20% of attacks. | [§4.4](https://arxiv.org/html/2608.15761v1#S4.SS4) |
| Models | Includes decision tree, random forest, histogram boosting, logistic regression, Gaussian NB and MLP, with additional deep MLP/CNN experiments. | [§4.5](https://arxiv.org/html/2608.15761v1#S4.SS5) |
| Outcomes | The abstract reports corrected best Macro-F1 `0.9503±0.0011` and RF random-to-Modbus balanced accuracy `0.9988→0.5083`. | [Abstract](https://arxiv.org/abs/2608.15761) |
| Interpretation | The paper distinguishes split optimism from label leakage and limits its architecture interpretation to one actuator; it also identifies LODO as single-run. | [§5.5 and §7](https://arxiv.org/html/2608.15761v1#S7) |

The paper explicitly states in §4.4: “We evaluate under two splitting regimes.”

## Consequences for the current project

### Directly covered

The general methodological act of comparing random-row evaluation and device-held-out/LODO evaluation for IoT IDS is **already published**. The current project must not claim that this comparison is new, first, or absent from prior IoT IDS work.

The paper also shows why a split-dependent performance drop must not automatically be called leakage: it identifies a concrete serialization artifact, then separates it from ordinary split optimism. This reinforces the project rule that device identity or split sensitivity alone is not leakage proof.

### Not established by this audit

This paper uses Edge-IIoTset/AgriEdge, not the current N-BaIoT mirror. It does not by itself establish whether a coverage-balanced N-BaIoT mirror analysis is numerically duplicated, whether its six-class common-support control has been used before, or whether its ordered-row-window sensitivity result is reproduced elsewhere.

Different data alone is not a novelty claim. Those N-BaIoT-specific differences can support only a clearly labelled technical replication/case study unless stronger evidence is found.

## Required claim changes

Remove or avoid any statement that:

- random-row versus device-held-out evaluation is itself a novel IoT IDS contribution;
- no prior IoT IDS work investigates provenance-related benchmark shortcuts;
- no prior work uses held-out-device evaluation;
- a split-dependent performance difference proves serialization leakage.

Allowed bounded statement:

> This repository reports a coverage-balanced N-BaIoT mirror case study of split and ordered-row-window sensitivity, with explicit negative evidence against a simple device-probe explanation.

## Audit boundary

The original external audit executor could retrieve the official arXiv materials but was policy-blocked from reading local reports. This persisted note combines only its quoted full-text findings with the parent’s direct inspection of local material. It is not an absence-of-prior-art proof.
