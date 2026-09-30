# Second public IoT IDS dataset: auditability scout

**Checked:** 2026-09-30. **Scope:** a second dataset for the Conditional Shortcut Audit Card, not a novelty claim. This report uses only owner/first-party dataset pages and their stated distributions; it does not download any dataset.

## Decision rule

A candidate is acceptable only if owner evidence confirms (1) a device identity field, or an explicitly documented device/group proxy that can be carried into each row, and (2) a timestamp or a capture/provenance block. A strict protocol must hold out an identity while preserving attack-label common support and independently block time/capture inside the appropriate fold. A filename inferred after download, an IP address without an owner-provided identity mapping, or an attack directory is **not** treated as a device ID.

## Evidence table

| Family | Official source and access | Confirmed identity/group | Confirmed time/capture/provenance | Confirmed labels | Access / licence | Strict device-held-out + time/capture-block without invented IDs | Result |
|---|---|---|---|---|---|---|---|
| **ToN_IoT (UNSW)** | [UNSW ToN_IoT dataset page](https://research.unsw.edu.au/projects/toniot-datasets) (accessed 2026-09-30) | The page confirms **more than 10 IoT/IIoT sensors**, including weather and Modbus sensors, but does **not** document a row-level sensor/device-ID column, nor a manifest mapping files/rows to particular sensors. Thus identity field: **unknown**; sensor identity proxy: **not confirmed**. | Raw IoT/IIoT telemetry is logged in log/CSV; network data are PCAP, log and Zeek CSV. The ground-truth folder contains security-event timestamp `ts`, and labelling uses attack IP addresses and timestamps ([UNSW](https://research.unsw.edu.au/projects/toniot-datasets)). That is confirmed temporal/provenance evidence, but alignment to every proposed row modality remains **unknown**. | The processed data have a label; the description statistics report normal and attack types; ground truth identifies hacking events ([UNSW](https://research.unsw.edu.au/projects/toniot-datasets)). Exact label vocabulary/columns: **unknown**. | The page links a download and grants free academic use in perpetuity; commercial use requires asking the author ([UNSW](https://research.unsw.edu.au/projects/toniot-datasets)). No standard licence identifier is stated there. | **No, on available official evidence.** Time/event provenance is adequate in principle, but a strict device holdout would require a documented per-row sensor/device mapping that was not confirmed. | **Reject for now: insufficient confirmed device identity.** Reconsider only after the owner supplies a manifest/schema proving per-row identity and timestamp alignment. |
| **Bot-IoT (UNSW)** | [UNSW Bot-IoT dataset page](https://research.unsw.edu.au/projects/bot-iot-dataset) (accessed 2026-09-30) | The owner page describes a Cyber Range network environment but does **not** identify a row-level device field or publish a device-to-address mapping on that page. Device identity and defensible proxy: **unknown**. | The owner confirms original PCAP, generated Argus and CSV files; files are separated by attack category/subcategory ([UNSW](https://research.unsw.edu.au/projects/bot-iot-dataset)). PCAP is confirmed as original-capture provenance; a documented exported timestamp field is **unknown**. Attack-category files are not device/capture blocks. | The page states normal and botnet traffic and names DDoS, DoS, OS/service scan, keylogging and data exfiltration, with DDoS/DoS organised by protocol ([UNSW](https://research.unsw.edu.au/projects/bot-iot-dataset)). Exact CSV label field/vocabulary: **unknown**. | Owner download is a UNSW-linked SharePoint folder. Free academic research use is granted in perpetuity; commercial use requires agreement with authors ([UNSW](https://research.unsw.edu.au/projects/bot-iot-dataset)). | **No.** Device identity is unconfirmed, and attack-category separation cannot be promoted to a device or independent capture block. | **Reject: insufficient device identity and block provenance for the required protocol.** |
| **IoT-23 (Stratosphere Laboratory / CTU)** | [IoT-23 owner page](https://www.stratosphereips.org/datasets-iot23) (accessed 2026-09-30) | Each of 23 captures is a documented **scenario**: 20 malware captures and 3 benign-device captures. The three benign device identities are Philips Hue smart LED lamp, Amazon Echo and Somfy smart door lock; malicious scenarios execute malware on a Raspberry Pi ([owner page](https://www.stratosphereips.org/datasets-iot23)). `scenario` is a defensible capture-group proxy, but it is not a distinct-device ID across the malware scenarios. | Owner page documents per-scenario PCAP and `conn.log.labeled`, README capture duration, 2018--2019 temporal coverage, and says captures may be rotated every 24 hours ([owner page](https://www.stratosphereips.org/datasets-iot23)). Thus scenario/capture provenance is confirmed. A specific row timestamp column is **not verified here**. | Owner says `conn.log.labeled` adds two network-behaviour label columns; labels were analyst-generated using the published rules/Flaber process ([owner page](https://www.stratosphereips.org/datasets-iot23)). Exact two-column names and full vocabulary: **unknown**. | The owner page exposes full and small download distributions and declares [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) in its dataset metadata ([owner page](https://www.stratosphereips.org/datasets-iot23)). | **No for the Audit Card's device protocol.** Scenario-held-out/capture-blocked evaluation is possible without invented IDs, but device-held-out attack evaluation has no confirmed common device×attack support: benign traffic comes from three named devices while malware runs on Raspberry Pi. | **Reject as the second device audit dataset; retain only as a capture/scenario-group robustness dataset.** |
| **CICIoT2023 (UNB/CIC)** | [UNB CIC IoT Dataset 2023 page](https://www.unb.ca/cic/datasets/iotdataset-2023.html) (accessed 2026-09-30) | UNB states its topology has 105 devices and attacks are by malicious IoT devices against other IoT devices. It does **not** document a row-level device-ID field or address-to-device mapping on the page. Identity/proxy: **unknown**. | The page confirms PCAP originals and derived ML CSV features, plus collection/wrangling tools ([UNB](https://www.unb.ca/cic/datasets/iotdataset-2023.html)). A documented CSV timestamp field or capture-block manifest is **unknown**. | UNB confirms 33 attacks in seven categories (DDoS, DoS, Recon, Web-based, Brute Force, Spoofing, Mirai) and malicious/benign classification use ([UNB](https://www.unb.ca/cic/datasets/iotdataset-2023.html)). Exact exported label field: **unknown**. | Download is linked by UNB ([UNB](https://www.unb.ca/cic/datasets/iotdataset-2023.html)); licence/access terms were **not found on the retrieved owner page**. | **No on current evidence.** The topology count is not a usable per-row holdout ID, and no qualifying block mapping is documented. | **Reject for now: insufficient confirmed identity and block provenance.** |
| **Edge-IIoTset** | No owner-hosted dataset page/repository or owner-hosted paper with auditable schema was successfully retrieved under the constrained check. | **Unknown.** | **Unknown.** | **Unknown.** | **Unknown.** | **Not assessable; therefore no.** | **Reject: official-source evidence unavailable.** |

## Ranking and recommendation

1. **No candidate currently qualifies as the required second device-held-out dataset.** This is the recommended outcome rather than weakening the identity rule.
2. **IoT-23** is the strongest *partial* alternative because its owner explicitly supplies scenario/capture provenance, labels, named benign devices, distributions and CC BY 2.0 terms ([owner page](https://www.stratosphereips.org/datasets-iot23)). It may support a clearly labelled **scenario-held-out + capture-block** sensitivity analysis, not CDP/DHG device-held-out inference.
3. **ToN_IoT** is the first re-check target if a first-party file manifest/schema becomes available: owner evidence already establishes multiple sensors and timestamped security events ([UNSW](https://research.unsw.edu.au/projects/toniot-datasets)), but not the necessary row-to-device mapping.

**Stop condition:** do not implement or claim cross-dataset replication of the Conditional Shortcut Audit Card until an official source verifies per-row device/group identity, time/capture-block provenance, and coverage sufficient for held identities to contain the evaluated labels. If no such evidence is obtained for ToN_IoT, stop this candidate family search and record the minimum empirical standard as unmet rather than substituting IPs, filenames, attack folders, or scenarios as device IDs.

## Source-access limitations

Only small HTML/API metadata requests were made; no archive, PCAP, CSV, mirror, Kaggle asset, or dataset contents were downloaded. Owner pages often describe collection and directories but not row schemas; every such absence above is marked **unknown**, not negative evidence about an archive. Edge-IIoTset is explicitly unassessed because an official source was not retrieved. These limitations are why no candidate is promoted on inference.

## Commands and sources used

Commands were small `bash`-hosted Python `urllib.request` GETs with exception handling (no browser/search/fetch tool):

```bash
python - <<'PY'
import urllib.request, re
for u in [
 'https://research.unsw.edu.au/projects/toniot-datasets',
 'https://research.unsw.edu.au/projects/bot-iot-dataset',
 'https://www.stratosphereips.org/datasets-iot23',
 'https://www.unb.ca/cic/datasets/iotdataset-2023.html']:
 try:
  html=urllib.request.urlopen(u, timeout=20).read().decode('utf-8','replace')
  print(u, re.sub(r'\\s+', ' ', re.sub(r'<[^>]+>', ' ', html))[:18000])
 except Exception as exc:
  print(u, 'INACCESSIBLE', repr(exc))
PY
```

The source URLs are the four owner pages linked in the table. An attempted GitHub API repository-name lookup for Edge-IIoTset did not establish an owner repository and is not used as evidence.
