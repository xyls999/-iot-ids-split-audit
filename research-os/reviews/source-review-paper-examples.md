# Source review: representative paper examples for candidate directions

Date: 2026-09-28
Task label: `paper_examples`

Scope: recent representative papers, primarily 2022-2026. Titles/DOIs below were checked against Crossref DOI records unless explicitly marked as an official non-DOI page. This is a directional source review, not a complete systematic literature review.

Integrity notes:
- I did not invent DOI/title pairs. Rows marked `Crossref DOI verified` came from DOI/Crossref records.
- `Walk These Ways` was verified from its official PMLR page; no DOI was found in this pass, so it is marked `official page verified / DOI not found`.
- Dataset/baseline/metric summaries are recurring patterns from the reviewed cluster. Items labelled `not paper-specific verified in this pass` should be rechecked in full PDFs before manuscript citation.
- Some 2026 records are online-first/forthcoming records in Crossref; re-check final bibliographic metadata before formal citation.

## 1) Quadruped sim-to-real/control

### Verified representative papers

| Year | Venue | Title | DOI / source | Status |
|---:|---|---|---|---|
| 2022 | Science Robotics | Learning robust perceptive locomotion for quadrupedal robots in the wild | https://doi.org/10.1126/scirobotics.abk2822 | Crossref DOI verified |
| 2022 | Robotics: Science and Systems XVIII | Rapid Locomotion via Reinforcement Learning | https://doi.org/10.15607/rss.2022.xviii.022 | Crossref DOI verified |
| 2023 | ICRA | DreamWaQ: Learning Robust Quadrupedal Locomotion With Implicit Terrain Imagination via Deep Reinforcement Learning | https://doi.org/10.1109/icra48891.2023.10161144 | Crossref DOI verified |
| 2023 publication / CoRL proceedings | Conference on Robot Learning / PMLR | Walk These Ways: Tuning Robot Control for Generalization with Multiplicity of Behavior | https://proceedings.mlr.press/v205/margolis23a.html | Official page verified; DOI not found in this pass |
| 2024 | ICRA | Extreme Parkour with Legged Robots | https://doi.org/10.1109/icra57147.2024.10610200 | Crossref DOI verified |
| 2024 | IJRR | Rapid locomotion via reinforcement learning | https://doi.org/10.1177/02783649231224053 | Crossref DOI verified |
| 2026 | IEEE Transactions on Robotics | DreamWaQ++: Obstacle-Aware Quadrupedal Locomotion With Resilient Multimodal Reinforcement Learning | https://doi.org/10.1109/tro.2026.3653774 | Crossref DOI verified |
| 2026 | Science Robotics | Agile perceptive multiskill locomotion for quadrupedal robots in the wild | https://doi.org/10.1126/scirobotics.adz7397 | Crossref DOI verified |

### Recurring datasets / environments

- No single static benchmark dominates. Papers usually train in physics simulation and evaluate on real robots.
- Recurring platforms/environments: ANYmal-class systems, MIT Mini Cheetah, Unitree A1/Go1-class quadrupeds; grass, gravel, ice, stairs, curbs, platforms, parkour obstacles, slopes, outdoor rough terrain.
- Public reproducibility pattern: project videos/code are common; raw real-robot datasets are less standardized than in vision or hydrology.

### Recurring baselines

- Model-based locomotion: MPC/WBC/impulse-control style controllers.
- Learned-control ablations: domain-randomization-only, no curriculum, fixed/box curriculum vs adaptive/grid curriculum, privileged teacher vs student, no-terrain/perception ablations, gait-free baseline.
- Prior sim-to-real methods: RMA-style online system identification, teacher-student RL, terrain-curriculum RL.

### Recurring evaluation metrics

- Velocity tracking error and feasible command area.
- Maximum speed, yaw rate, Froude number, 10 m dash time, obstacle/stair/parkour success.
- Survival time, fall/collision rate, recovery from disturbance, sim-to-real gap.
- Energy/torque/power and gait smoothness in some controller papers.

### Novelty patterns

- Better sim-to-real transfer via privileged learning, online/implicit system identification, domain randomization, actuator/latency modeling.
- Curriculum design for difficult command spaces and agile maneuvers.
- Perceptive or implicit terrain reasoning: height maps, vision/depth, latent terrain imagination.
- Broader skill coverage: multiskill locomotion, parkour, tunable gait families, obstacle-aware multimodal policies.

## 2) Robot-dog / legged-robot visual navigation

### Verified representative papers

| Year | Venue | Title | DOI | Status |
|---:|---|---|---|---|
| 2023 | Field Robotics | ArtPlanner: Robust Legged Robot Navigation in the Field | https://doi.org/10.55417/fr.2023013 | Crossref DOI verified |
| 2023 | ICRA | Visual Language Maps for Robot Navigation | https://doi.org/10.1109/icra48891.2023.10160969 | Crossref DOI verified |
| 2024 | ICRA | ViPlanner: Visual Semantic Imperative Learning for Local Navigation | https://doi.org/10.1109/icra57147.2024.10610025 | Crossref DOI verified |
| 2024 | IROS | AMCO: Adaptive Multimodal Coupling of Vision and Proprioception for Quadruped Robot Navigation in Outdoor Environments | https://doi.org/10.1109/iros58592.2024.10801962 | Crossref DOI verified |
| 2024 | IEEE RA-L | ProNav: Proprioceptive Traversability Estimation for Legged Robot Navigation in Outdoor Environments | https://doi.org/10.1109/lra.2024.3418270 | Crossref DOI verified |
| 2024 | IEEE CASE | Autonomous Visual Navigation for Quadruped Robot in Farm Operation | https://doi.org/10.1109/case59546.2024.10711780 | Crossref DOI verified |
| 2025 | PLOS ONE | Application of 3D point cloud and visual-inertial data fusion in Robot dog autonomous navigation | https://doi.org/10.1371/journal.pone.0317371 | Crossref DOI verified |
| 2025 | Robotics: Science and Systems XXI | NaVILA: Legged Robot Vision-Language-Action Model for Navigation | https://doi.org/10.15607/rss.2025.xxi.018 | Crossref DOI verified |
| 2026 | ISARC / IAARC proceedings | Vision-Language Navigation for Indoor Construction Site Inspection using Quadruped Robots | https://doi.org/10.22260/isarc2026/0084 | Crossref DOI verified |

### Recurring datasets / environments

- Field/robot trials matter more than fixed datasets: subterranean/factory/farm/construction/outdoor trails, dense vegetation, stairs, negative obstacles, unstructured terrain.
- Sensor stacks recur: RGB/RGB-D, semantic segmentation, LiDAR, visual-inertial odometry, proprioceptive signals, topological/semantic maps.
- Verified dataset mentions in accessible abstracts/pages: PLOS ONE 2025 reports urban navigation and multi-modal multi-scene ground-robot datasets; Springer/IEEE rows need full-PDF checks for exact dataset names.
- Commonly seen but not paper-specific verified in this pass: RELLIS-3D, RUGD, SemanticKITTI, Matterport/Habitat/Gibson-style indoor navigation datasets.

### Recurring baselines

- Classical navigation: A*/D*/RRT-style global planning, local costmap planners, geometric traversability planners.
- SLAM/localization baselines: ORB-SLAM, VIO, LiDAR-inertial odometry / LIO-SAM-style methods.
- Learning baselines: exteroceptive-only traversability, proprioception-only ablations, semantic-costmap ablations, visual navigation foundation models such as GNM/ViNT/NoMaD (`not paper-specific verified in this pass`).

### Recurring evaluation metrics

- Navigation success rate, collision/failure rate, planning failure count, traversal time/path length.
- Localization and mapping: ATE, RMSE, MAE, drift, map quality.
- Traversability: terrain classification/traversability prediction accuracy, energy consumption, crash prediction.
- Language/VLM navigation: goal-reaching accuracy, instruction completion, SPL/path-efficiency (`verify exact metric per paper`).

### Novelty patterns

- Moving from geometry-only to semantic/affordance-aware local planning.
- Adaptive fusion of vision, LiDAR, VIO, and proprioception to handle bad lighting, blur, vegetation, deformable terrain, and negative obstacles.
- Vision-language-action/topological-map methods for open-vocabulary goals and inspection tasks.
- Application papers increasingly emphasize deployability on commercial quadrupeds/robot dogs, not only simulator navigation scores.

## 3) Wavelet/GNN hydrology and water/ocean forecasting

### Verified representative papers

| Year | Venue | Title | DOI | Status |
|---:|---|---|---|---|
| 2022 | Journal of Hydrology | Directed graph deep neural network for multi-step daily streamflow forecasting | https://doi.org/10.1016/j.jhydrol.2022.127515 | Crossref DOI verified |
| 2023 | Journal of Hydrology | Graph neural network for groundwater level forecasting | https://doi.org/10.1016/j.jhydrol.2022.128792 | Crossref DOI verified |
| 2023 | Science of The Total Environment | Assessing spatial connectivity effects on daily streamflow forecasting using Bayesian-based graph neural network | https://doi.org/10.1016/j.scitotenv.2022.158968 | Crossref DOI verified |
| 2023 | Digital Signal Processing | ST-GRF: Spatiotemporal graph neural networks for rainfall forecasting | https://doi.org/10.1016/j.dsp.2023.103989 | Crossref DOI verified |
| 2023 | Dynamics of Atmospheres and Oceans | Significant wave height prediction based on dynamic graph neural network with fusion of ocean characteristics | https://doi.org/10.1016/j.dynatmoce.2023.101388 | Crossref DOI verified |
| 2024 | Ocean Engineering | Dynamic adaptive wavelet based fuzzy framework for extended significant wave height forecasting | https://doi.org/10.1016/j.oceaneng.2024.116814 | Crossref DOI verified |
| 2026 | Environmental Modelling & Software | HydroTGNN: Filling missing streamflow data with graph neural network | https://doi.org/10.1016/j.envsoft.2026.106937 | Crossref DOI verified |
| 2026 | Applied Sciences | Explicit Water Balance Constraints for Trustworthy Graph Neural Network Flood Forecasting | https://doi.org/10.3390/app16104963 | Crossref DOI verified |
| 2026 | Water Resources Management | A Novel Spectral Decomposition Framework for TimesNet: Integrating DCT and Wavelet Transforms for Hydrological Forecasting | https://doi.org/10.1007/s11269-026-04529-y | Crossref DOI verified |
| 2026 | Engineering Applications of Artificial Intelligence | A heterogeneous multi-graph spatio-temporal network for runoff forecasting | https://doi.org/10.1016/j.engappai.2026.114967 | Crossref DOI verified |

### Recurring datasets / environments

- River forecasting: streamflow/discharge gauge networks, rainfall-runoff basins, hydrometric stations, catchment graphs.
- Verified examples from accessible abstracts: Applied Sciences 2026 reports LamaH-CE and CAMELS; Water Resources Management 2026 reports Danube River stations Chilia, Sulina, and Sfântu Gheorghe.
- Groundwater: monitoring-well networks and spatial aquifer connectivity.
- Ocean/wave: buoy/reanalysis or station grids for significant wave height (`exact source names not paper-specific verified in this pass`).

### Recurring baselines

- Naive persistence, ARIMA/statistical models, SVR/RF/XGBoost (`not paper-specific verified in this pass`).
- Deep temporal models: ANN/MLP, LSTM/GRU, TCN, CNN-LSTM, TimesNet.
- Hydrology-specific and graph baselines: EA-LSTM, Pure-GNN, STGCN/DCRNN/Graph WaveNet-style models (`exact baseline names vary`).
- Wavelet hybrids: wavelet-ANN/LSTM/fuzzy frameworks, DWT/DCT/FFT decomposition variants.

### Recurring evaluation metrics

- Regression: RMSE, MAE, MSE, MAPE/sMAPE, R²/correlation.
- Hydrological skill: NSE and KGE are common for streamflow/discharge.
- Event forecasting: peak timing/peak error and sometimes POD/FAR/CSI for flood events (`verify per paper`).
- Physical consistency: Applied Sciences 2026 reports Physical Inconsistency Ratio (PIR) alongside NSE/RMSE.

### Novelty patterns

- Graph construction from river topology, spatial proximity, catchment attributes, learned/dynamic adjacency, or heterogeneous multi-graphs.
- Uncertainty-aware graph learning, e.g., Bayesian GNN variants.
- Spectral/multiscale decomposition: DWT/DCT/FFT, wavelet features, graph wavelets, temporal-frequency modules.
- Physics-informed constraints: explicit mass/water-balance loss terms and physically interpretable consistency checks.
- Task expansion from pure forecasting to gap filling/missing-data imputation and extreme-event robustness.

## Direction-level comparison

| Direction | Evidence maturity | Data burden | Hardware burden | Main publication risk | Safer novelty angle |
|---|---|---|---|---|---|
| Quadruped sim-to-real/control | Very active, high bar in RSS/ICRA/T-RO/Science Robotics | Simulation + real robot logs | High | Hard to beat SOTA without robot access and extensive experiments | Narrow, reproducible controller ablation on available robot/sim; transfer/stability analysis |
| Robot-dog visual navigation | Active and application-driven | Moderate to high; real-world navigation logs valuable | Medium-high | Pure VLM demos can look incremental without real deployments | Application-specific semantic/proprioceptive fusion with measurable field trials |
| Wavelet/GNN hydrology forecasting | Active in Journal of Hydrology/WRM/EMS/AI journals | Public datasets more available | Low | Many hybrid deep-learning papers; novelty can be shallow | Physics/topology-constrained GNN + wavelet/spectral decomposition + strong baselines and ablations |
