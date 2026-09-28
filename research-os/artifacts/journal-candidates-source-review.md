# Journal candidates source review: B/C venues in Hohai catalog

Accessed: 2026-09-28. Sources are official publisher/API/catalog pages fetched by direct HTTP and saved under `evidence/journal-candidates/`. APCs and metrics can change; verify again immediately before submission. No acceptance is implied.

## Shortlist summary

| # | Journal | Hohai catalog evidence | Best-fit use case | OA/APC snapshot | Source/recognition evidence | Fit risk |
|---|---|---|---|---|---|---|
| 1 | **Robotics and Autonomous Systems** | line 1587: `1429 ... 0921-8890 B` | quadruped/autonomous robot control, learning, navigation, sim-to-real with system validation | Elsevier JournalFinder: **Hybrid**, gold OA **USD 3,140**; submission `submit.elsevier.com/ROBOT` | JournalFinder: CiteScore 9.9, JIF 5.2, subject areas AI/control/computational mechanics/CS apps; ScienceDirect RSS examples | Strong robotics fit, but likely needs rigorous autonomous-system contribution and experiments; APC only if choosing OA; Elsevier official indexing list not retrieved |
| 2 | **Autonomous Robots** | line 1870: `1679 ... 0929-5593 C` | autonomous robots with real-robot evidence, multi-robot, HRI, planning/navigation | Springer: **Hybrid**; OA APC **£2,790 / USD 4,190 / €3,190**; subscription route no APC after acceptance | Springer page lists SCOPUS, SCIE, EI Compendex, INSPEC etc.; JIF 6.0 (2025) | Excellent robotics fit, but scope explicitly values performance data on actual robots; high OA APC |
| 3 | **Pattern Recognition Letters** | lines 2763/3942: `... 0167-8655 C` | concise robot perception / computer vision / recognition method paper | Elsevier JournalFinder: **Hybrid**, gold OA **USD 2,380**; submission `submit.elsevier.com/PRLETTERS` | JournalFinder: CiteScore 9.5, JIF 3.3; official IAPR publication per scope | Not a robotics systems venue; paper must be a concise pattern-recognition contribution, not primarily control/sim-to-real |
| 4 | **Neural Computing and Applications** | line 3938: `649 ... 0941-0643 C` | applied neural/ML control, perception, remote sensing detection, intelligent systems | Springer: **Hybrid**; OA APC **£2,290 / USD 3,190 / €2,590**; subscription route no APC after acceptance | Springer lists SCOPUS, EI Compendex, INSPEC etc.; article types include Original Articles/Reviews/Book Reviews/Announcements | Broad AI venue; robotics/water paper needs strong application and validation, otherwise looks generic |
| 5 | **Remote Sensing Applications: Society and Environment** | line 2854: `2557 Remote Sensing Applications-Society and Environment 2352-9385 C` | remote-sensing + water/environment AI, floods/lakes/drought/mangroves, regional study with broader significance | Elsevier JournalFinder: **Hybrid**, gold OA **USD 2,620**; submission `submit.elsevier.com/RSASE` | JournalFinder: CiteScore 7.9, JIF 4.5; ScienceDirect RSS examples | Good for remote sensing/water-AI, weak for quadruped robotics unless remote-sensing/environment problem is central |
| 6 | **Applied Water Science** | line 1848: `1661 ... 2190-5487 C` | water-resource/water-quality/hydrology AI, treatment, planning/management | Springer: **full OA**, APC **£1,890 / USD 2,590 / €2,190** | Springer lists DOAJ, SCOPUS, SCIE, EI Compendex, INSPEC etc.; JIF 5.7 (2025) | Water-only fit; robotics paper would need a water-management/application framing |
| 7 | **Journal of Hydrology X** | line 2468: `2214 ... 2589-9155 C` | hydrology/water sensors/ML/reservoir/water hazards/open-data paper | Elsevier JournalFinder: **full OA**, APC **USD 2,350**; submission `submit.elsevier.com/JOHX` | JournalFinder: CiteScore 6.4, JIF 3.1; ScienceDirect RSS examples on ML water sensors/reservoir releases | Hydrology focus; not suitable for robot control unless hydrologic science contribution dominates |
| 8 | **Water Science and Engineering** | line 1686: `1519 ... 1674-2370 B` | water engineering, water-distribution optimization/surrogate models, aquatic environment/ecology | Elsevier JournalFinder: **subsidised OA**, APC **USD 0**; submission `mc03.manuscriptcentral.com/wse` | Scope says peer review under Hohai University and IAHR collaboration; JournalFinder: CiteScore 7.6, JIF 4.3 | Most affordable; fit is water engineering, not robotics. Because it is Hohai-associated, check departmental conflict/recognition expectations |

## Recent official paper examples

- **Robotics and Autonomous Systems** RSS (`09218890`, lastBuildDate 2026-09-28): “A soft gripper with an adaptive grasp control system...”; “Adaptive pair weighting for robust hand-eye calibration”; “Forced sliding mode synergetic robust control...”
- **Autonomous Robots** Springer latest articles: “Civil: causal and intuitive visual imitation learning” (2026-09-18); “A RGB-D SLAM method based on contact experience in dynamic environment” (2026-09-16); “Implicit semantic control manifolds for learning-enabled multi-UAV coordination” (2026-09-01).
- **Pattern Recognition Letters** RSS: “Transferable adversarial attack via energy-based model”; “GACF: Graph augmentation and co-awareness fusion...”
- **Neural Computing and Applications** Springer latest articles: “CGFM: attention-guided multimodal feature interaction for remote sensing detection” (2026-09-28); “Variational autoencoder in analysis of motion capture data” (2026-09-23).
- **RSASE** RSS: “Widespread decline in water storage of large South American lakes...” and “Effectiveness of machine learning algorithms in mapping mangrove forests...”
- **Applied Water Science** Springer latest: “Integrated groundwater quality assessment using Water Quality Index...” (2026-09-17); Review on electrochemical disinfection (2026-09-11).
- **Journal of Hydrology X** RSS: low-cost water-level sensors with machine learning; piecewise linear regression trees for reservoir release estimation; ML emulation from citizen soil-moisture observations.
- **Water Science and Engineering** RSS: “Accelerating optimal operation of water distribution systems with surrogating models”; “Coupled rigid water column–global gradient formulation...”

## Notes / near-misses

- **Engineering Applications of Artificial Intelligence** is highly relevant to AI/control, but the extracted Hohai catalog contains conflicting entries (`A` at line 282 and `C` at line 3853). Do not rely on the `C` label without administrative confirmation; OA fee from JournalFinder was USD 3,040 if needed later.
- **Journal of Vibration and Control** official SAGE pages were not retrievable from this environment due TLS failures, so it was not shortlisted here despite possible control/vibration relevance.
- **IET Intelligent Transport Systems** official Wiley pages returned anti-bot 403, so it was not shortlisted.

## Evidence files

- Hohai catalog: `literature/hhue-catalog-extracted.txt`
- Elsevier JournalFinder/RSS/serial metadata: `evidence/journal-candidates/*.journalfinder.json`, `*.sciencedirect-rss.xml`, `*.elsevier-serial.json`
- Springer official pages: `evidence/journal-candidates/*.springer-home.html`, `*.springer-publish.html`
