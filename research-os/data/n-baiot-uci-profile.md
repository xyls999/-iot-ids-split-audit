# N-BaIoT Official Dataset Profile

**Source:** UCI Machine Learning Repository dataset 442  
**URL:** https://archive.ics.uci.edu/dataset/442/detection+of+iot+botnet+attacks+n+ba+iot  
**DOI:** `10.24432/C5RC8J`  
**License:** CC BY 4.0 (as stated by UCI)  
**Profile checked:** 2026-09-29

## Official metadata observed

- Dataset characteristics: multivariate, sequential.
- Tasks: classification and clustering.
- Feature type: real.
- Instances: 7,062,606.
- Missing values: none.
- Download archive path shown by UCI: `/static/public/442/detection+of+iot+botnet+attacks+n+baiot.zip`.

## Label structure described on the UCI page

The dataset distinguishes benign and malicious traffic. The malicious traffic is divided into 10 attacks carried out by two botnets, Mirai and BASHLITE. The page also describes 115 feature variables and aggregation prefixes such as H and HH for traffic statistics over recent windows.

## Feasibility implications

- The official dataset is large; full download and extraction should be treated as a storage/time decision, not done silently.
- It is sequential and has device/source structure, so random row splitting is not an adequate main evaluation.
- The first experiment should use a documented subset or streaming/chunked preprocessing, while preserving device and time identifiers if available.
- Before training, inspect archive contents, file names, labels, device identifiers and timestamps; record SHA-256 and provenance.
- A benign-only calibration window must be selected chronologically from the held-out device and must not overlap the final test window.
- Do not call this a real embedded deployment: only offline CPU/memory/latency measurements are currently available.

## Current status

Metadata verified; official archive not yet downloaded. The bounded feasibility gate is therefore not started.
