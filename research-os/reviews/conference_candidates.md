# Source review: Hohai C/B conference candidates for quadruped sim-to-real / vision paper

Reviewed against the local Hohai extracted catalog (`research-os/literature/hhue-catalog-extracted.txt`) and primary venue/publisher pages. Avoided venues that look pay-to-publish or guaranteed-acceptance. Status reflects pages available in this source pass; most 2026 main-paper deadlines are already closed, so next-cycle dates require re-checking official CFPs.

## Shortlist

| Venue | Hohai level | Legitimacy/proceedings | Review/process | Fees / low-cost notes | Fit | Deadline uncertainty |
|---|---:|---|---|---|---|---|
| IEEE ICRA | B | Official 2026 CFP; IEEE Xplore proceedings/history page lists recurring ICRA proceedings. | Double-anonymous via PaperPlaza; regular review; no deadline extension planned. | Student rates exist; full/non-student registration can cover more uploads; remote only as video for non-attending authors, not a cheap publication route. | **Best if high novelty robotics + hardware/sim-to-real evidence.** | 2026 paper deadline was 15 Sep 2025; 2027/current cycle must be rechecked. |
| IEEE/RSJ IROS | C | Official 2026 CFP states accepted archival papers hosted on IEEE Xplore; IEEE Xplore lists recurring IROS proceedings. | Double-anonymous; Conference Paper Review Board; accepted papers presented in person. | Student rates, day rates, workshops separate; no remote presentation route found. | **Best C-level target for quadruped sim-to-real/control/perception.** | 2026 paper deadline was 2 Mar 2026; next cycle not verified. |
| ECCV | B | Official ECVA page; proceedings published by Springer/ECVA; Springer conference page lists ECCV 2026. | OpenReview; double-blind; strict anonymity/dual submission; in-person presentation expected. | Student and virtual registration categories exist, but accepted papers require full registration (not student/virtual). | Strong for vision-heavy paper with methodological novelty; hard bar. | 2026 deadline was Mar 2026; next ECCV is biennial (2028), so high uncertainty for near-term. |
| 3DV | C | Official 2026 site; technically co-sponsored by IEEE Computer Society; proceedings publisher/indexing should be reconfirmed before submission. | OpenReview; double-blind; no rebuttal; code/reproducibility encouraged. | Student registration exists, but single-student author covering a paper must register regular; no remote option found. | Very good for quadruped 3D perception, depth/SLAM/reconstruction, embodied vision. | 2026 deadlines were Aug 2025; 2027/2028 schedule to recheck. |
| BMVC | C | Official BMVA site; proceedings published and DOI-indexed by BMVA. | OpenReview; double-blind; at least three reviewers + AC meta-review; no rebuttal in 2025. | Relatively low full registration (£500 early / £550 late in 2025); no student-rate evidence on source page. | Good lower-cost vision venue for applied CV/perception paper. | 2025 deadline passed; 2026 CFP not checked/posted in this pass. |
| ICPR | C | Official 2026 site; accepted papers in Springer LNCS; Springer conference page lists ICPR 2026. | Single-blind; CMT; reviewer instructions and formatting/desk-reject rules published. | Student and reduced 60+ categories exist, but accepted main papers require full registration. | Good broad pattern-recognition/CV venue; acceptable for vision components of robot paper. | 2026 paper deadline was 10 Jan 2026; next cycle likely biennial and unverified. |
| IEEE ICIP | C | Official 2026 site; accepted regular/special papers published in IEEE Xplore; IEEE Xplore proceedings history page available. | IEEE submission/author kit; no-show policy; all accepted papers/abstracts must be registered/presented. | Student rates and one-day/workshop rates exist; accepted papers require author full registration; in-person required. | Good for image/video processing method; weaker for full robotics system unless contribution is image-processing. | 2026 paper deadline was 4 Feb 2026; 2027 current cycle needs recheck. |
| ACM WSDM | B | Official 2026 CFP; accepted papers published in ACM Digital Library. | ≥3 PC reviews + senior PC; mixed double-/single-blind; originality/COI/ethics policies published. | Student registration/travel awards; **in-person, no remote presentations**. ACM OA APC may apply in 2026 if institution not in ACM Open, with waivers/subsidy noted. | Low fit unless contribution is web/search/data mining; not recommended for quadruped system paper. | 2026 full paper deadlines Aug 2025; next cycle not verified. |
| ECML PKDD | B | Official 2026 research track; proceedings in Springer LNCS; Springer page lists ECML PKDD volumes. | Double-blind; three reviewers; CMT; ethics/reproducibility policies. | Student discount requires proof; accepted papers must be presented in person; registration cap noted. | Moderate fit for ML/data-mining method with strong experiments; less fit for robot hardware/system. | 2026 research-track deadline passed; next cycle not verified. |

## Recommendation order for a small quadruped sim-to-real / vision paper

1. **IROS (C)** — best balance of relevance and legitimacy for quadruped sim-to-real, robot learning/control, and embodied perception.
2. **ICRA (B)** — best if the paper has a strong robotics contribution and enough real-robot evidence; more competitive.
3. **3DV (C)** — strong if the contribution is 3D perception, depth, mapping, pose, reconstruction, or embodied vision; re-check proceedings indexing before committing.
4. **BMVC / ICPR / ICIP (C)** — good if reframed as computer vision/image processing with solid benchmarks; BMVC may be lower-cost, ICPR broad, ICIP more signal/image-processing.
5. **ECCV (B)** — only if the paper is primarily a high-novelty CV method, not mainly a robot application.
6. **ECML PKDD / WSDM (B)** — only if the core is ML/data mining/search; otherwise poor fit for quadruped sim-to-real.

## Key sources

- Hohai extracted catalog: `research-os/literature/hhue-catalog-extracted.txt` lines around 3223-3280, 3278-3281, 3420-3680.
- ICRA official 2026 CFP/registration/final-author pages; IEEE Xplore ICRA proceedings table.
- IROS official 2026 CFP/home/registration pages; IEEE Xplore IROS proceedings table.
- ECCV official ECVA 2026 Dates/CFP/Submission/Registration pages; Springer ECCV conference page.
- 3DV official 2026 Dates/CFP/Author/Registration pages.
- BMVC 2025 official CFP/author/review/registration/proceedings pages.
- ICPR 2026 official dates/authors/review/registration/proceedings pages; Springer ICPR conference page.
- ICIP 2026 official CFP/submission/registration pages; IEEE Xplore ICIP proceedings/history page.
- WSDM 2026 official full/short CFP, registration, camera-ready pages.
- ECML PKDD 2026 official research-track, registration, proceedings pages; Springer ECML conference page.
