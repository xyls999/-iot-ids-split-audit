# Label-support and harmonization audit for IoT IDS

**Audit performed:** 2026-10-01 (filename retained for project chronology)  
**Question:** has IoT IDS literature already formalized restricting evaluation to labels shared across designated groups/domains before interpreting held-group performance?  
**Conclusion:** shared-category restriction has explicit precedent; the exact all-held-group intersection plus N-BaIoT six-label protocol was not verified. This is not novelty evidence.

## Terms used in this audit

The following notation is the project’s audit vocabulary, not an equation attributed to a cited paper.

- **Class harmonization:** map a group/domain label set through \(h_g:Y_g\rightarrow C\), aligning meanings.
- **Groupwise common-support restriction:** compute \(C_* = \bigcap_{g\in G}\operatorname{support}(h_g(Y_g))\), then retain records whose mapped label belongs to \(C_*\). This aligns observed class availability.
- **Held-domain evaluation:** a domain is absent from model fitting. This differs from domain adaptation, in which target observations participate in training with labels, pseudo-labels or unsupervised objectives.

A common label vocabulary, feature intersection or equal classifier output dimension does not itself prove an all-group observed-support intersection.

## Designated lead: unverified

User-supplied lead: *A rule-based label harmonization framework for cross-dataset IoT intrusion detection*, DOI `10.1016/j.iot.2026.102030`.

| Resource | Observed result |
|---|---|
| DOI resolver | Inaccessible in audit environment |
| Publisher article `S2542660526001605` | HTTP 403 |
| Candidate GitHub repository discovered during lookup | HTTP 404; not treated as evidence |

Exact task, mapping rules, intersection procedure, datasets and splits are therefore **unverified**. The title does not establish that label harmonization includes common-support filtering.

## Verified primary-source precedents

### Joint Semantic Transfer Network for IoT Intrusion Detection

- Primary source: [author arXiv full text, 2210.15911](https://arxiv.org/pdf/2210.15911).
- Task: multi-source heterogeneous domain adaptation with a sparsely labelled IoT target.
- Section V-A (“Shared Intrusion”) explicitly selects five shared categories: benign, DoS, DDoS, reconnaissance and password attacks.
- Datasets: CICIDS2017, NSL-KDD, UNSW-NB15, UNSW-BoT-IoT and UNSW-ToN-IoT.
- The target participates in adaptation; it is not a completely untouched held-device/domain test.

**Overlap:** direct precedent for selecting shared categories before cross-domain evaluation; partial overlap with groupwise common support because the paper does not provide a complete raw-label map or an explicit all-group intersection algorithm. It does not evaluate the N-BaIoT six-label restriction.

### Heterogeneous Domain Adaptation for IoT Intrusion Detection: A Geometric Graph Alignment Approach

- Primary source: [author arXiv v1, 2301.09801](https://arxiv.org/pdf/2301.09801v1).
- Section III-B assumes both domains share \(K\) categories; Section V-B describes up to eight shared categories, including DoS, password and backdoor attacks.
- Datasets: NSL-KDD, UNSW-NB15, CICIDS2017, UNSW-BoT-IoT and UNSW-ToN-IoT.
- Target observations participate in semi-supervised adaptation.

**Overlap:** explicit shared-label assumption/selection; partial overlap with common-support restriction; not an untouched held-device protocol and not an N-BaIoT six-label experiment.

### Original N-BaIoT study

- Primary source: [Meidan et al., arXiv:1805.03409](https://arxiv.org/pdf/1805.03409).
- Nine IoT devices are evaluated with device-specific benign-trained autoencoders.
- Table 3 records BASHLITE infections across all nine devices but lacks Mirai infection for Ennio Doorbell and Samsung SNH 1011 N Webcam; the attack list contains five BASHLITE and five Mirai behaviors.
- Each device’s benign observations are partitioned chronologically for device-specific training, optimization and test use.

**Overlap:** it documents support differences that make a benign-plus-BASHLITE six-label intersection plausible. It does not specify a supervised, groupwise label-intersection protocol or leave-device-out evaluation. The link between the current mirror’s exact six file labels and these Table-3 facts is an audit inference, not an owner-verified mapping.

## Overlap table

| Source | All-group common-label intersection | Held-device/domain evaluation | Current N-BaIoT six-label restriction |
|---|---|---|---|
| DOI `10.1016/j.iot.2026.102030` | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| JSTN | Partial: explicit shared-category selection; exact intersection unestablished | Adaptation target, not untouched holdout | Not evaluated |
| GGA | Partial: shared categories; exact intersection unestablished | Adaptation target, not untouched holdout | Not evaluated |
| Original N-BaIoT | Support differences documented; intersection protocol absent | Device-specific train/test | Conditional rationale only |

## Consequence for the current project

The local N-BaIoT mirror protocol may report its exact common-support filtering as a reproducibility detail. It must not call shared-category control a novel method, because explicit shared-category selection already appears in IoT domain-adaptation literature.

The absence of a verified exact match for the complete protocol is an access- and scope-limited result, **not** evidence that the protocol is publishably new. Combined with the full-text audits of arXiv:2608.15761 and arXiv:2604.11324, this supports retaining the repository as a transparent technical replication record only.

## Audit boundary

The external audit executor could inspect official arXiv materials but was policy-blocked from local file inspection. No local mapping code, group membership or split manifest was independently checked by it. No datasets were downloaded or experiments reproduced.
