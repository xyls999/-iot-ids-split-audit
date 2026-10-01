# IoT/network-security pivot options: publication-feasibility screen

**Date:** 2026-10-01  
**Goal:** select a new IoT/network-security direction with relatively stronger legitimate journal feasibility than the rejected N-BaIoT IDS novelty route.  
**Important:** this is a comparative feasibility screen, not an acceptance-probability estimate or a novelty conclusion.

## Decision rules

A candidate ranks higher only when it has:

1. owner/official, legal and small enough public inputs;
2. a precise falsifiable claim rather than a generic system proposal;
3. an offline defensive protocol;
4. an evaluation ground-truth path that can be independently adjudicated;
5. a narrower overlap risk than generic IDS classification, generic SBOM-to-CVE triage, or generic MUD enforcement.

## Ranked candidates

| Rank | Candidate | Relative feasibility | Why it is promising | Major risk |
|---:|---|---|---|---|
| 1 | **Release-provenance-assisted OpenWrt vulnerability applicability** | Highest of the screened options, conditional on a full-text nearest-work audit and manual labels | Official releases expose small manifests, CycloneDX BOMs, release source, recipes and patch history; official CVE/KEV records support a reproducible offline comparison against name/version matching. | Generic firmware/SBOM/CVE triage is already crowded; manual adjudication may reveal no measurable improvement. |
| 2 | **MUD DNS-binding availability–permission–maintenance trade-off** | Medium; more novel-looking but data feasibility uncertain | RFC 8520 distinguishes MUD policy refresh from DNS binding refresh; a bounded retention/TTL experiment has a concrete measurable trade-off. | RFC 9726 and recent MUD work cover DNS-aware enforcement; public traffic may not retain DNS answers, TTLs, event order or service-success ground truth. |
| 3 | **Vendor-advisory to CVE JSON revision/region constraint preservation audit** | Medium for a short data-quality report; lower for a full journal paper | Very low-cost official HTML/JSON data; a pre-registered, manually auditable cohort can give a clean discrepancy measurement. | Single vendor and 30-record cohort may be too narrow; generic CPE/version-matching work already overlaps. |

## Recommended route: OpenWrt release-provenance-assisted applicability

### Narrow research question

> Across selected official OpenWrt releases, does adding package recipes, feed commits and documented backports reduce false “affected” classifications by at least 20% compared with name/version matching, while reducing recall by no more than five percentage points?

The thresholds are preregistration targets, not observed results. If either condition fails, reject the claim.

### Why this is stronger than the previous route

- It studies **software provenance and release-specific applicability**, not another IoT traffic classifier.
- It uses structured, inspectable official artifacts rather than an unverified Kaggle mirror.
- The baseline is clear: name/version vulnerability matching.
- The output can include an adjudication table showing exactly why a match is affected, not affected, unresolved or backport-corrected.
- It is purely offline and defensive: no firmware execution, scanning, exploitation or target interaction.

### Verified public inputs

| Input | Role | Primary source |
|---|---|---|
| OpenWrt 24.10.0 release artifacts | Small manifest, CycloneDX BOM, checksums and release metadata; no firmware image download is required for the pilot. | [Official release directory](https://downloads.openwrt.org/releases/24.10.0/targets/x86/64/) |
| OpenWrt source history | Release-specific recipes, feeds and patches used to assess provenance/backports. | [Official release source, v24.10.0](https://github.com/openwrt/openwrt/tree/v24.10.0) |
| CVE Program records | Vulnerability assertions, affected fields and record revision history. | [Official CVE List v5](https://github.com/CVEProject/cvelistV5) |
| CISA KEV | Exploitation-priority annotation only, not a negative label or applicability ground truth. | [Official KEV data](https://github.com/cisagov/kev-data) |
| SPDX/CycloneDX | Validate the format of collected SBOMs; schema validity does not prove inventory completeness. | [SPDX](https://spdx.github.io/spdx-spec/v2.3/), [CycloneDX](https://github.com/CycloneDX/specification) |

### Minimum pilot protocol

1. Select three official OpenWrt releases and two target profiles only after verifying that each has a manifest/BOM and associated source history.
2. Freeze URL, retrieval time, SHA-256, source commit, schema version and CVE snapshot before analysis.
3. Construct the same candidate package–release–CVE set for two methods:
   - **A:** package name/version matching;
   - **B:** A plus release recipe, feed commit and documented backport evidence.
4. Independently adjudicate roughly 100 package–release–CVE triples from official advisories and patch history; label exact affected, false affected, unresolved or insufficient evidence. Include candidates missed by either method.
5. Measure precision, recall within the adjudicated cohort, unresolved fraction, method agreement and manual review effort. Use package/CVE-clustered uncertainty rather than treating repeated releases as independent.
6. Reject a paper claim if the preregistered improvement or recall constraint fails.

### Literature/overlap gate before implementation

The following adjacent work is already known and must receive full-text method/protocol review before any experiment:

- [*Impacts of SBOM Generation on Vulnerability Detection* (2024)](https://www.cs.montana.edu/izurieta/pubs/SCORED2024.pdf): SBOM generation/formats and vulnerability detection.
- [*Cybersecurity Vulnerability Prioritisation via Risk Assessment* (2025)](https://jaatun.no/papers/2025/CVE_pri_ARES_WS.pdf): SBOM-derived CVEs and contextual risk for an OpenWrt gateway.
- [*Automated SBOM-Driven Vulnerability Triage for IoT Firmware* (2026)](https://arxiv.org/abs/2601.01308): direct firmware/SBOM/triage overlap; audit notes it reports planned evaluation.
- [*Automating Firmware Vulnerability Triage via High-Level Representations and Similarity Digests* (2026)](https://www.ndss-symposium.org/ndss-paper/auto-draft-655/): OpenWrt-based triage using binary/function similarity.

The prospective distinction is **not** generic SBOM generation, CVE ranking, KEV prioritization or firmware triage. It is the measured value and review cost of release-specific provenance/backport evidence for applicability decisions. This distinction is **unverified** until full texts are audited.

## Alternative 2: MUD DNS-binding trade-off

### Narrow question

> On chronologically held-out IoT traffic, can device-observed TTL-aware DNS bindings with bounded retention reduce blocked legitimate flows by at least 25% against periodic controller-side resolution, without increasing stale endpoint permission-hours or rule changes per device-day?

Relevant standards and sources:

- [RFC 8520 §3.5](https://www.rfc-editor.org/rfc/rfc8520.html#section-3.5): MUD-file refresh timing.
- [RFC 9726](https://www.rfc-editor.org/rfc/rfc9726.html): resolver disagreement, DNS/CDN complications and enforcement strategies.
- [UNSW-IoTraffic](https://datadryad.org/dataset/doi:10.5061/dryad.w0vt4b94b): 27 devices and about 203 days; traffic/protocol data but no interaction/event ground truth.
- [UNSW MUDactivity](https://iotanalytics.unsw.edu.au/mudactivity.html): ten MUD profiles, behavior grammars and fixtures.

Do not start this route until a small metadata inspection confirms preservation of DNS answers, TTLs and event order. Without them, packet-accurate DNS-binding evaluation is not defensible.

## Alternative 3: vendor advisory constraint-preservation audit

A bounded audit could ask whether hardware revisions, regions and inclusive version bounds in official router advisories survive into CVE JSON affected fields. A candidate protocol samples a preregistered cohort of 30 eligible TP-Link CVEs from official advisory pages and CVE Program JSON.

Verified agreement example: [TP-Link CVE-2025-6151 advisory](https://www.tp-link.com/us/support/faq/4536/) and its [CVE Program JSON](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2025/6xxx/CVE-2025-6151.json) preserve stated revisions/bounds. This is a control, not evidence that errors are common.

The route is cheap and auditable but likely better as a small dataset-quality study than as the first-choice journal project.

## Recommendation and stop rules

**Recommendation:** carry only the OpenWrt provenance pilot into full-text nearest-work auditing. Keep MUD as a contingency only if its trace data preserve required DNS semantics. Do not start the TP-Link audit unless the user prefers a small, fast data-quality report over a stronger journal attempt.

Stop/pivot the OpenWrt route if:

- official release artifacts cannot be connected to target-specific package inventories;
- a 100-triple independent adjudication set cannot be constructed from official evidence;
- nearest work already measures the same release-provenance/backport comparison;
- the preregistered precision improvement and recall guardrail fail.
