# Second public IoT IDS dataset: owner-schema hunt

**Checked:** 2026-09-30  
**Scope:** a second dataset for random-row versus device-held-out split-sensitivity replication, not a novelty claim.  
**Status:** no candidate qualified on the verified owner evidence.

## Decision rule

Acceptance requires all of the following from a dataset owner, official institution, owner repository, source code or schema:

1. explicit row-level device identity or a complete owner-documented file-to-device mapping;
2. timestamps, capture blocks or independently documented collection/provenance blocks; and
3. attack labels and authorized public research access.

Capture-held-out results must never be represented as device-held-out results. An IP address, path, filename, attack directory or scenario label is not accepted as a device ID unless an owner explicitly documents the mapping.

## Evidence table

| Candidate | Device/group identity | Time or provenance | Labels and access | Decision |
|---|---|---|---|---|
| **N-BaIoT** | UCI describes nine devices and displays device-named paths. The inspected listing is partial, and no complete explicit row/file-to-device manifest was verified. Device identity was not inferred from those paths. [UCI](https://archive.ics.uci.edu/dataset/442/detection+of+iot+botnet+attacks+n+ba+iot) | The creators document collection in an isolated laboratory and identify devices in Table III. This establishes experimental provenance; it does not establish collection-block membership for every distributed row. [Creator paper, §IV](https://arxiv.org/html/1805.03409) | UCI documents benign traffic and ten attack classes, provides a public download, and specifies CC BY 4.0. [UCI](https://archive.ics.uci.edu/dataset/442/detection+of+iot+botnet+attacks+n+ba+iot) | **Not qualified:** requirement 1 remains unverified; a usable row-to-block mapping also remains unresolved. |
| **ToN_IoT** | The institutional page identifies telemetry, network and operating-system datasets, but does not provide a complete named-device mapping for network rows. Its attacker-IP labeling description is not a substitute for device identity. [UNSW](https://research.unsw.edu.au/projects/toniot-datasets) | UNSW explicitly documents timestamped security-event ground truth and collection at its Cyber Range and IoT laboratories. **Pass at documentation level.** [UNSW](https://research.unsw.edu.au/projects/toniot-datasets) | Processed CSV labels and normal/attack statistics are documented. Academic research use is expressly permitted, with citation requirements; commercial use requires author permission. [UNSW](https://research.unsw.edu.au/projects/toniot-datasets) | **Not qualified:** requirement 1 unverified. The linked SharePoint material could not be inspected successfully. |
| **IoT-23** | The owner maps labeled logs to capture scenarios. However, malicious scenarios use a Raspberry Pi, while the three benign scenarios use named commercial devices. Scenario identity does not establish distinct physical-device identity across malicious captures. [Owner documentation](https://www.stratosphereips.org/datasets-iot23) | Per-capture folders and README metadata document capture duration and provenance. **Pass for capture blocks.** [Owner documentation](https://www.stratosphereips.org/datasets-iot23) | The owner documents flow labels and publicly distributes labeled logs. The owner-linked Zenodo deposit is marked open; its extracted license field was blank, so a specific reuse license was not verified. [Owner](https://www.stratosphereips.org/datasets-iot23), [deposit](https://zenodo.org/records/4743746) | **Not qualified for device-held-out replication.** Capture grouping is supported, but must not be relabeled device grouping. |
| **CICIoT2023** | The official page provides topology information and a feature table, but neither supplies an explicit device identifier or complete row-to-device manifest. [UNB](https://www.unb.ca/cic/datasets/iotdataset-2023.html) | Collection and PCAP-to-CSV processing are described. The inspected documentation does not establish a complete CSV-row mapping to independent collection blocks. Duration and interarrival statistics do not establish timestamps. [UNB](https://www.unb.ca/cic/datasets/iotdataset-2023.html) | Attack categories and benign/malicious classification are documented. The official download endpoint presents a registration form; explicit reuse terms were not verified. [UNB](https://www.unb.ca/cic/datasets/iotdataset-2023.html), [download endpoint](https://cicresearch.ca/IOTDataset/CIC_IOT_Dataset2023/) | **Not qualified:** requirements 1 and 2 remain unverified, and access terms need confirmation. |
| **IoTID20** | The creators’ project page does not expose a row-level device schema or complete file-to-device manifest. [Project page](https://sites.google.com/view/iot-network-intrusion-dataset/home) | The page identifies derivation from earlier traffic, but does not expose a row-to-time or collection-block mapping. [Project page](https://sites.google.com/view/iot-network-intrusion-dataset/home) | Academic research use is expressly permitted and a download is linked; the inspected page does not enumerate the distributed label schema. [Project page](https://sites.google.com/view/iot-network-intrusion-dataset/home) | **Not qualified:** requirements 1 and 2, and exact label-schema evidence, remain unverified. |

## Conclusion

Do not select a second dataset for device-held-out replication yet. This is an evidence-verification outcome, not proof that suitable metadata cannot exist.

The most useful next evidence is an official N-BaIoT manifest or README explicitly connecting every distributed data file to its named device and collection block. Until that evidence is obtained, no device-held-out experiment should be claimed from this hunt.

## Verification boundary

Only owner documentation and small metadata pages were inspected. No archives, PCAPs, large data files, network scans, security tools or model experiments were used. Secondary search results were not used as evidence. No numerical replication result is claimed.
