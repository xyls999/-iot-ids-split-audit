# N-BaIoT blind adjudication and cross-case gate

## Initial packet round

The initial packet schema asked one claim to span random-row, ordered-window, LODO, and independent-dataset evidence. Two independent reviewers agreed on **16/20** cells (0.80). The four disagreements were caused by underspecified semantics:

- whether a within-mirror LODO result is `identified` or only `conditional`;
- whether a LODO gap is an explicit result;
- whether a protocol without a reported model result is sufficient;
- whether the absent independent dataset should be `conditional` or `not_identifiable`.

This round is retained as a negative measurement result. It is not discarded or averaged away.

## Frozen refinement

A revised packet file fixed the claim and state rule before the second review:

`research-os/artifacts/nbaiot-blinded-review-packets-v2.json`

Fixed claim:

> For the nine-group, six-label N-BaIoT mirror, does the evidence identify a model evaluation that is independent of row sharing across device groups?

The revised rule explicitly requires an explicit LODO result for `identified`; a protocol alone is only `conditional`. It excludes cross-dataset and leakage claims.

## Second round

Two independent reviewers agreed on **16/16** packet-tier cells (1.00):

| packet | T0 | T1 | T2 | T3 |
|---|---|---|---|---|
| RF window 0 | not_identifiable | conditional | conditional | identified |
| RF window 2000 | not_identifiable | conditional | conditional | identified |
| LR window 0 | not_identifiable | conditional | conditional | identified |
| device provenance | not_identifiable | conditional | conditional | conditional |

The protocol-only packet remains conditional because it lacks a model-result metric. The RF/LR packets become identified at T3 because each supplies a bounded LODO result or gap tied to common-support rows.

## Cross-case interpretation

The two cases now have a common **measurement discipline**, not a common truth:

```text
fixed claim
→ fixed evidence tier semantics
→ independent state adjudication
→ retain disagreements and schema defects
→ revise rule before repeat adjudication
```

OpenWrt provides a source/artifact-binding transition. N-BaIoT provides a device-independence transition. They must not be pooled into a single accuracy or reliability statistic.

## Gate effect

### Earned

- Evidence-tier wording can be made operational and independently reproducible;
- the initial disagreement exposed a real schema defect rather than being hidden;
- after predeclared refinement, the second round is perfectly reproducible on the supplied packets;
- the protocol supports claim-specific tiers instead of forcing one universal tier vocabulary.

### Not earned

- second-case independent truth;
- population-level reviewer reliability;
- novelty against every assurance/provenance/package-maintenance system;
- acceptance probability or publication success.

**Status:** the protocol is now suitable for a bounded methods/report submission draft, but high-level publication novelty remains unconfirmed.
