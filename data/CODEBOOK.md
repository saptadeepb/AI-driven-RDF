# Master Extraction Codebook
Scoping Review: AI-Driven Forecasting for Relief Demand in Emergency Supply Chains
Companion to the article in *Systems and Soft Computing*

This codebook defines every variable in `master_extraction.csv`, the SINGLE master
dataset from which every percentage in the abstract, main text, figures and tables is
computed. No number appears in the manuscript that is not computed from this file by
`code/compute_stats.py`.

## Denominator rule

Two denominators are used and are ALWAYS stated explicitly in the text:

* **N_all** = all included sources (primary studies + review/synthesis articles).
* **N_prim** = primary studies only (`study_type == "Primary"`). Method, disaster,
  horizon, linearity, paradigm and performance variables use **N_prim**, because
  review articles do not themselves apply a forecasting method to data.

## Multi-label rule

* `objective`, `disaster_type`, `horizon`, `linearity`, `learning_paradigm`,
  `performance_evidence`, `deployment_status` are **mutually exclusive** (one value per
  study; a dominant-category rule is applied and recorded in `coding_note`).
* The six `mf_*` method-family flags are **multi-label**: a hybrid ARIMA-ANN study scores
  1 on both `mf_statistical` and `mf_dl`. Method-family percentages therefore sum to
  MORE than 100% and are reported as "% of primary studies employing X", never as a
  partition. The number of studies with >1 method family is reported as `n_hybrid`.

## Variables

| # | Variable | Type | Allowed values |
|---|---|---|---|
| 1 | `study_id` | ID | S001 … |
| 2 | `citekey` | text | BibTeX key in `references.bib` |
| 3 | `first_author` | text | |
| 4 | `year` | int | 2007–2026 |
| 5 | `wave` | int | Charting batch (1 or 2), recorded for traceability only. All sources come from the single search to 22 August 2026. |
| 6 | `study_type` | cat | Primary, Review |
| 7 | `author_country` | text | country of the corresponding/first author's affiliation |
| 8 | `focus_country` | text | case-study country; `Global` if not country-specific; `Not reported` |
| 9 | `publisher` | text | Elsevier, Springer, IEEE, Wiley, Taylor & Francis, MDPI, Emerald, INFORMS, Other |
| 10 | `journal` | text | |
| 11 | `objective` | cat | Predictive modeling and forecasting; Disaster preparedness and relief planning; Healthcare and medical service demand; Humanitarian logistics and supply chain management; Community engagement and social impact; Methodological or technology review |
| 12 | `disaster_type` | cat | Multi-hazard/General; Earthquake; Flood; Hurricane/Cyclone; Biological/Epidemic; Wildfire; Drought/Food insecurity; Conflict/Displacement; Technological/Other; Not reported |
| 13 | `mf_statistical` | 0/1 | ARIMA, ETS, regression, Bayesian, time-series, econometric |
| 14 | `mf_ml` | 0/1 | classical machine learning: trees, RF, SVM, k-NN, boosting, ensembles |
| 15 | `mf_dl` | 0/1 | ANN, MLP, CNN, RNN, LSTM, transformer, GNN, deep RL |
| 16 | `mf_knowledge` | 0/1 | case-based reasoning, rule-based reasoning, fuzzy sets, rough sets, grey systems |
| 17 | `mf_optsim` | 0/1 | mathematical programming, metaheuristics, simulation, agent-based models |
| 18 | `mf_genai` | 0/1 | large language models, retrieval-augmented generation, generative models |
| 19 | `learning_paradigm` | cat | Supervised; Unsupervised; Both; Reinforcement; Not applicable; Not reported |
| 20 | `horizon` | cat | Short-term; Long-term; Short-to-long; Dynamic/real-time; Not reported |
| 21 | `linearity` | cat | Linear; Non-linear; Combined; Not reported |
| 22 | `sustainability` | 0/1 | study explicitly treats environmental/social sustainability or resilience as an objective or outcome |
| 23 | `stochastic` | 0/1 | study explicitly represents uncertainty (probabilistic, Bayesian, fuzzy, grey, stochastic programming, scenario-based, interval) |
| 24 | `performance_evidence` | cat | **Comparative benchmark** = ≥2 competing models compared on a common dataset with a reported error/accuracy metric; **Single-model metric** = one model, quantitative metric reported; **Qualitative/none** = no quantitative predictive-performance metric; **Not applicable (review)** |
| 25 | `metric_reported` | text | verbatim metric name(s) if known, else `Not reported` |
| 26 | `deployment_status` | cat | **Operational deployment** = used by a named responding organization in practice; **Real-data case study** = validated on real event data, not fielded; **Synthetic/illustrative** = simulated or numerical example only; **Not reported** |
| 27 | `data_source` | cat | Historical records; Social media; Satellite/GIS; Survey/interview; Simulation; Mixed; Not reported |
| 28 | `coding_note` | text | free text: dominant-category decisions, ambiguities, confidence |

## Provenance of codes

* Variables 2–12, 19, 20 for wave-1 studies are transcribed from the extraction tables of
  the original submission.
* Variables 13–18, 21–23 are derived from the reported method by the deterministic rules
  R1–R4 of the article (Table 2), so they are reproducible from the method string. Functional
  form (`linearity`) is derived from the method-family flags by rule R2 for every primary study.
* `year` is the year of first publication (online first where applicable). The reference
  list cites the version of record, so for a few online-first articles the year printed in
  the reference list is later than `year`.
* Corrections are applied by the build and logged with their evidence:
  `data/outlet_corrections_R2.csv` (outlet and publisher transcription errors) and
  `data/recoding_R2.csv` (recoding from the full text). `data/charting_basis_R2.csv` records,
  for the sources first charted from their titles, the text from which they are now charted.
* Variables 24–26 were coded from the abstract or full text where retrievable. Where a
  study's performance evidence could not be confirmed, it is coded `Qualitative/none`
  only if the abstract makes no performance claim; otherwise `Not reported`. This
  conservative rule is why the review reports that comparative efficacy evidence is
  available for only a minority of the corpus: a finding, not an omission.

## Screening and extraction procedure

Screening and extraction were performed by two reviewers independently with a third adjudicating
(manuscript, Section 3.5).
