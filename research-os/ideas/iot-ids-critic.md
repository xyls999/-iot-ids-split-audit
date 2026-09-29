# Independent Research Critic — IoT IDS Ideas

**Critic:** reviewer subagent  
**Evidence boundary:** local ten-paper collection and six open PDFs only; P09/P10 metadata/details remain pending full-text verification.

## Verdicts

- `IOT-IDS-01`: **retain with major modification**. Most promising, but must be framed as benign-only target-device threshold calibration under leave-one-device-out, not fully device-independent detection. Highest risks: leakage, unrealistic benign calibration, and prior overlap.
- `IOT-IDS-02`: **reject as standalone**. LiteShield already covers feature selection + lightweight classifiers + resource analysis; retain only as an ablation inside IOT-IDS-01.
- `IOT-IDS-03`: **reject current version**. IoT-KEEPER and online detection already cover the framing; no reliable natural temporal drift data or contamination-safe update protocol is yet established.
- `IOT-IDS-04`: **reject as standalone**. Existing lightweight/knowledge-distillation work already reports model size, latency and memory; it is a baseline package, not a new paper contribution.
- `IOT-IDS-05`: **defer/high risk**. Open-set/unknown attack detection requires stronger threat model, attack-category holdouts and leakage control; current evidence is insufficient.

## Required changes to IOT-IDS-01

1. Rename contribution to **benign-only target-device threshold calibration** rather than fully device-independent IDS.
2. Fix calibration budget and chronological order before testing.
3. Compare no calibration, fixed source threshold, and benign-only calibration.
4. Add contamination-negative experiment where the calibration window contains attack traffic.
5. Audit label/provenance/device/time leakage before every model-selection step.
6. Use N-BaIoT for a bounded feasibility test, then add one second dataset only if label mapping is defensible.
7. Complete nearest-paper verification for P09/P10 before claiming any novelty.

## Merge verdict

`BLOCK` current candidate set from immediate hypothesis freeze. Only modified `IOT-IDS-01` may proceed to a bounded feasibility experiment; novelty remains `pending_nearest_paper_search`.
