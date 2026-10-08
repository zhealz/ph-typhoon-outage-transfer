# Result tables

Every number in the project README comes from these files. They are exported by the notebooks to `MyDrive/ph_typhoon_ntl`.

| File | Produced by | Contents |
| --- | --- | --- |
| `labels_step2b.csv` | 02b | One row per municipality and storm within 150 km of the track (five storms, including the Haiyan reference). Weekly and nightly outage measures, the combined outage duration, measurement status and whether the row enters the model |
| `step3_results.csv` | 03 | AUC, average precision and Brier score by validation design, model and feature set (uncalibrated labels) |
| `step3_folds.csv` | 03 | AUC for every fold |
| `step3_morans_i.csv` | 03 | Moran's I of leave-one-typhoon-out residuals |
| `step3_placebo.csv` | 03 | Outage shares, real storm versus placebo, at the original 80% threshold |
| `step4_calibration.csv` | 04 | Real and placebo shares of outages longer than 7 days at thresholds from 80% to 40% |
| `step4_bootstrap.csv` | 04 | Leave-one-typhoon-out AUC with 95% bootstrap intervals, paired difference from the hazard-only model, random-split AUC and transfer loss |
| `step4_folds.csv` | 04 | AUC for every fold, including each held-out typhoon |
| `step4_residual_diagnostics.csv` | 04 | Moran's I and η² (by utility and by province) of leave-one-typhoon-out residuals |
| `step4_coverage.csv` | 04 | Share of affected municipalities with a satellite label, by Relative Wealth Index tercile |
| `step4_recall.csv` | 04 | Share of measured long outages caught when the top 30% of predicted risk in each storm is prioritised, by wealth tercile, with 95% bootstrap intervals |
| `step4_utility_matching.txt` | 04 | Output of the utility-to-municipality matching (match rates and unmatched names) |

Feature-set codes: H = hazard; E = exposure; Sgeo = neighbouring wind and island size; S = Sgeo plus utility features; Emb3 / Emb10 = AlphaEarth embeddings reduced to 3 or 10 principal components.

