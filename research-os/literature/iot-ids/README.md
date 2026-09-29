# IoT IDS Literature Collection

## Topic

面向资源受限物联网设备的轻量级流量异常检测与跨设备泛化。

## Collection policy

- Ten papers were selected for dataset provenance, edge/resource constraints, lightweight detection, or cross-device/cross-dataset evaluation.
- Metadata was retrieved and verified from Crossref DOI records on 2026-09-28.
- Each paper has a local note under `papers/`; full text must be read from the DOI/publisher link before quoting detailed results.
- This collection is for defensive offline research only. Do not scan, exploit, or test third-party systems.

## Reading order

1. P01 — N-BaIoT foundational dataset/model.
2. P02 — edge-oriented online traffic analysis.
3. P03/P05/P06 — TON-IoT, Edge-IIoTset, CICIoT2023 dataset provenance.
4. P04/P07/P08 — dataset-specific detection studies.
5. P09/P10 — cross-domain and cross-dataset validity, most relevant to the proposed research gap.

## Local files

- `bibliography.csv`: machine-readable bibliography.
- `papers.json`: Crossref metadata and abstracts when supplied.
- `papers/P01.md` ... `papers/P10.md`: individual reading notes/checklists.
- `sources/arxiv/`: six publicly accessible original PDFs and extracted text files.
- `cn-reading-notes.md`: Chinese译读重点。
- `translations/`: three complete, non-official Chinese translations of open-licensed arXiv papers, with generated PDFs.
- `subdirection-recommendation.md`: recommended narrow research direction and feasibility gate.
- `sources/`: optional downloaded publisher/open-access files; do not add private credentials or unverified copies.

## Initial synthesis

The easiest prototype is N-BaIoT + classical/lightweight models. A publishable contribution needs more than a single random split and accuracy table: use device/time holdout, report false-positive rate and resource cost, and preferably validate on a second dataset or explicitly study cross-dataset label harmonization.
