# Supplementary Material S3: Benchmark task card for relief demand forecasting

*Artificial Intelligence for Relief Demand Forecasting: A PRISMA-ScR Scoping Review of Research Attention and Efficacy Evidence*

The machine-readable schema accompanies this document as a JSON Schema (draft 2020-12) file.

**Why a specification and not a baseline model.** The master extraction dataset charts
studies, not demand observations. The primary studies forecast different targets (relief
commodities, casualties, displaced persons, hospital attendances, damaged houses) in different
units, at resolutions from facility to nation and horizons from hours to years, and most do not
release their data. No common task therefore exists on which a reference baseline could be
fitted. The task card fixes what a future task must declare before a baseline is meaningful.

**What the card requires.**

| Field | Purpose |
|---|---|
| `target` | quantity, operational definition, ground-truth source and its latency |
| `unit`, `spatial_resolution`, `temporal_resolution` | make tasks comparable |
| `horizon` | lead times and the decision each forecast serves |
| `issue_time_rule` | information admissible at issue time, preventing look-ahead leakage |
| `hazard_scope` | uses the review's hazard categories, linking tasks to the dataset |
| `severity_strata` | at least two strata, so surge-event error is reported, not averaged away |
| `data_sources` | custodian, access, license, and a mandatory check of the terms of use |
| `split_rule` | event-wise or rolling-origin splits, never random rows |
| `baselines` | at least three rungs of persistence, seasonal or analog, linear or ARIMA-family, gradient boosting |
| `metrics` | scale-free point metrics, probabilistic metrics, and reporting by stratum |
| `uncertainty` | whether predictive intervals are mandatory, and at which levels |
| `reporting` | TRIPOD+AI and a model card |
| `custodian` | who maintains and versions the task |

No benchmark result is implied by this file.
