# N-BaIoT primary protocol: device and chronology boundary

**Date:** 2026-09-30  
**Purpose:** distinguish what the original N-BaIoT collection paper establishes from what the locally used Kaggle mirror establishes.

## Primary-source evidence

The original N-BaIoT paper is Meidan et al., *N-BaIoT—Network-Based Detection of IoT Botnet Attacks Using Deep Autoencoders*, arXiv [`1805.03409`](https://arxiv.org/abs/1805.03409). Its full text is locally preserved at `literature/iot-ids/sources/arxiv/1805.03409.txt`.

The paper states that the authors collected traffic from IoT devices in an isolated lab, infected **nine commercial IoT devices**, and lists device IDs, make/model and device type in Table 3. It also states:

> “Each of the nine sets of benign data we collected in our lab, corresponding to the nine IoT devices, was divided chronologically into three equidimensional sets: (1) DStrn … (2) DSopt … and (3) the benign part of DStst …”

**Source:** [`1805.03409`, empirical-evaluation/Table-3 discussion](https://arxiv.org/html/1805.03409), locally at `sources/arxiv/1805.03409.txt` lines 322–326.

The UCI owner record confirms public distribution, sequential multivariate characteristics, 7,062,606 instances, 115 features, benign/malicious labels and ten attacks, under CC BY 4.0.

**Source:** [UCI dataset 442](https://archive.ics.uci.edu/dataset/442/detection+of+iot+botnet+attacks+n+ba+iot); local profile: `data/n-baiot-uci-profile.md`.

## What this supports

For the **official original distribution**, the collection protocol supports these constrained statements:

- device IDs are an author-defined experimental grouping associated with the nine Table-3 devices;
- benign traffic was deliberately partitioned in chronological order into training, optimization and test portions;
- cross-device and within-device chronological questions are scientifically motivated by the original collection design.

## What this does not support

The current experiments use `data/raw/n-baiot-original-kaggle.zip`, an unverified Kaggle mirror. Its numeric directories and row order have not been verified against an official archive manifest or timestamp field.

Therefore no current report may claim:

- that a mirror directory name is an official row-to-device mapping;
- that a mirror row offset is an actual timestamp or an official DStrn/DSopt/DStst boundary;
- that a row-window sensitivity experiment is a chronological generalization experiment;
- that this single mirror supplies the independent second dataset required for a paper-level replication.

## Consequence for the project

The current common-support findings remain valid only as **mirror-based split-sensitivity evidence**. A legitimate temporal/device protocol needs either:

1. the official N-BaIoT archive plus an owner-distributed manifest that connects its file layout to Table-3 device IDs and chronological partitions; or
2. a different public dataset with equivalent owner-documented row/device/block schema.

Until one is obtained, retain the strict boundary rather than upgrading row order into time evidence.
