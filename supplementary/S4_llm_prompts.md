# Supplementary Material S4: LLM comparison (protocol, prompts and results)

*Artificial Intelligence for Relief Demand Forecasting: A PRISMA-ScR Scoping Review of Research Attention and Efficacy Evidence*

Version 1.0, fixed on 17 November 2026 before any model output was generated.

## 1. Design

Three arms were pre-specified. Each tests one way an LLM could replace or assist a step of the protocol-driven review.

| Arm | Question | Input given to the model | Reference standard | Status |
|---|---|---|---|---|
| A. Unconstrained generation | Can an LLM, from its training data alone, enumerate and characterize the literature? | Prompt A only (no retrieval, no files, no web) | The included sources of the review (110 after full-text re-assessment) | Executed, three runs |
| B. Title and abstract screening | Can an LLM apply the eligibility criteria to retrieved records? | Prompt B plus the deduplicated database export | The human screening decisions | Specified, not run: requires the complete deduplicated record export, including excluded records |
| C. Data charting | Can an LLM chart included studies under the codebook? | Prompt C plus the retrieved title and abstract of each study | The human coding in the released dataset | Specified, not run: requires the retrieved abstract of each sampled study; planned sample of 30 primary studies (seed 20261117) |

Isolation. Every LLM run was executed in a fresh model session that received only the prompt (and, for Arms B and C, would receive the record texts). No run had access to the released dataset, the manuscript, the codebook file beyond the rules embedded verbatim in the prompt, or any web or file tools.

Model. Claude Opus 5.5 (Anthropic; model identifier `claude-opus-5-5`), accessed 17 November 2026 through an agent session. Sampling temperature is not user-controllable in that interface and is reported as "default". Arm A was run three times in independent sessions to measure run-to-run stability; Arms B and C are specified for three runs each.

Scoring is fully deterministic given the saved raw outputs, which are released with the dataset together with the scoring code.

## 2. Prompt A (unconstrained generation)

```
You are assisting with a scoping review. Answer from your own knowledge only.
Do not use any tools, web search, files or retrieval.

Task: list the peer-reviewed studies and review articles published from 2007 to
2026 that develop, apply or review artificial-intelligence, machine-learning,
statistical, knowledge-based (case-based reasoning, fuzzy, rough or grey
systems), optimisation/simulation or generative-AI methods for the forecasting,
prediction or quantitative estimation of relief demand, humanitarian needs,
affected or displaced populations, casualties, impacts or emergency resource
requirements in emergency, disaster and humanitarian relief operations
(including the health services mobilized within them). List as many as you can, up to 120.

For each study give: authors, year, title, venue, DOI (or "unknown"),
method_families (subset of: statistical, classical_ml, deep_learning,
knowledge_based, optimisation_simulation, generative_ai), hazard (one of:
multi-hazard/general, earthquake, flood, hurricane/cyclone, biological/epidemic,
wildfire, drought/food insecurity, conflict/displacement, technological/other,
not reported), comparative_benchmark (yes/no/unknown: at least two competing
models compared on a common dataset with an error metric), operational_deployment
(yes/no/unknown: used in practice by a named responding organisation).

Then give a summary: the share of studies in each method family, the most
studied hazards, how many studies benchmark against a competing model, and how
many report operational deployment.

Return a single JSON object:
{"studies":[{...}], "summary":{...}}
If you are not confident a study exists, do not list it.
```

## 3. Prompt B (title and abstract screening)

The eligibility criteria are embedded verbatim from Section 3.2 of the manuscript.

```
You are screening records for a scoping review. Apply these eligibility
criteria exactly as written, using only the title and abstract given.

Population: Emergency, disaster and humanitarian relief operations, including
the health services mobilized within them.
Concept: The forecasting, prediction or quantitative estimation of relief
demand, humanitarian needs, affected or displaced populations, casualties,
impacts or emergency resource requirements, using artificial intelligence,
machine learning, deep learning, knowledge-based reasoning, statistical or
hybrid computational methods.
Context: Any geography; any hazard type; any organisational setting.

Inclusion criteria:
1. Peer-reviewed journal articles, peer-reviewed conference papers, and book
   chapters.
2. Published from database inception to August 2026.
3. Written in English.
4. Reporting either a primary application of a forecasting or estimation method
   to relief demand, needs, impacts or emergency resources, or a review or
   synthesis of such methods.
Exclusion criteria:
1. Studies addressing other aspects of emergency management (routing, facility
   location, evacuation, procurement) in which demand is an exogenous input
   rather than an object of estimation.
2. Studies forecasting the hazard alone (rainfall, ground motion, storm track)
   with no link to relief requirements or impacts.
3. Editorials, commentaries, abstracts without full text, theses, preprints and
   non-peer-reviewed grey literature.

For each record return {"record_id":..., "decision":"include"|"exclude",
"criterion": the first failing criterion or "all met", "confidence": 0-1}.
Return a JSON list only.
```

## 4. Prompt C (data charting)

```
You are charting studies for a scoping review. For each record below, read only
the title and abstract provided. Code these variables using the rules exactly as
written. If the text does not let you decide, answer "not reported". Do not use
outside knowledge of the paper and do not guess.

method_families (multi-label, 0/1 each):
  statistical: ARIMA, ETS, regression, Bayesian, time-series, econometric
  classical_ml: trees, random forest, SVM, k-NN, boosting, ensembles
  deep_learning: ANN, MLP, CNN, RNN, LSTM, transformer, GNN, deep RL
  knowledge_based: case-based reasoning, rule-based reasoning, fuzzy sets,
                   rough sets, grey systems
  optimisation_simulation: mathematical programming, metaheuristics,
                   simulation, agent-based models
  generative_ai: large language models, retrieval-augmented generation,
                   generative models
hazard (one): multi-hazard/general; earthquake; flood; hurricane/cyclone;
  biological/epidemic; wildfire; drought/food insecurity;
  conflict/displacement; technological/other; not reported
stochastic (0/1): the study explicitly represents uncertainty (probabilistic,
  Bayesian, fuzzy, grey, stochastic programming, scenario-based, interval)
performance_evidence (one):
  comparative benchmark = at least two competing models compared on a common
    dataset with a reported error or accuracy metric
  single-model metric = one model, quantitative metric reported
  qualitative/none = no quantitative predictive-performance metric
  not reported = the text does not allow a decision
deployment_status (one):
  operational deployment = used by a named responding organisation in practice
  real-data case study = validated on real event data, not fielded
  synthetic/illustrative = simulated or numerical example only
  not reported

Return a JSON list: {"record_id":..., "statistical":0|1, "classical_ml":0|1,
"deep_learning":0|1, "knowledge_based":0|1, "optimisation_simulation":0|1,
"generative_ai":0|1, "hazard":..., "stochastic":0|1|"not reported",
"performance_evidence":..., "deployment_status":...}
```

## 5. Pre-specified metrics

Arm A: number of studies listed; citation existence rate (a listed study counts as existing only if a matching record is found by title search in a bibliographic source); precision (listed studies that are among the included sources / listed studies); recall (included sources recovered / number of included sources); recall by publication year (before 2024; 2024 to 2026); the latest publication year correctly recovered; run-to-run overlap (Jaccard index of matched corpus IDs).

Arm C: per-variable percentage agreement and Cohen's kappa against the human coding; for categorical variables, the share of "not reported" answers and of definite answers that disagree with the human code; run-to-run agreement (Fleiss' kappa across the three runs). Abstract-only coding by the model is compared with human coding that may have used the full text; this asymmetry is reported, not corrected.

Matching rule for Arm A: a listed study matches an included source when the normalized titles (lower case, punctuation removed) have a token-set similarity of at least 0.85, or the DOIs are identical. Borderline matches (0.70 to 0.85) are adjudicated manually and logged.

## 6. Results

The model was Claude Opus 5.5 (Anthropic), accessed on 17 November 2026 through an agent session whose sampling temperature is not user-controllable. Each run used a fresh session that received only the prompt and had no access to the released dataset, the manuscript or any search or file tool. Arm A was run three times; Arms B and C were not run, because they require the complete record export and the abstracts as inputs. Arm A is scored against the 110 sources included in the review.

**Arm A.** Across three runs the model listed between 80 and 115 studies, of which 8 to 11 were among the included sources, a recall of 7 to 10%. No run recovered any of the 35 included sources published from 2024 onwards (32% of the corpus), and the most recent included source recovered dates from 2023. The matched sources overlapped only partly between runs (mean Jaccard index 0.54). The model described a quarter or more of its listed studies as benchmarking against a competing model, and about one in six as operationally deployed, against 12.5% and 3.1% of the primary studies charted in the review. A random sample of 45 of the 268 listed studies that are not in the corpus (seed 20261117) was checked against bibliographic records, and all 45 exist; they are released as candidate records for any future update of the review.

| Measure | Run 1 | Run 2 | Run 3 | This review |
|:------------------------------------------------------------|------------:|------------:|------------:|--------------:|
| Studies listed | 115 | 100 | 80 | 110 |
| Matched to an included source | 11 | 8 | 8 |  |
| Precision against the included sources | 10% | 8% | 10% |  |
| Recall of the included sources | 10% | 7% | 7% |  |
| Recall, sources published before 2024 | 15% | 11% | 11% |  |
| Recall, sources published 2024 to 2026 | 0% | 0% | 0% |  |
| Most recent included source recovered | 2022 | 2023 | 2022 |  |
| Listed studies coded as comparative benchmark | 32% | 27% | 26% | 12% |
| Listed studies coded as operationally deployed | 14% | 17% | 16% | 3% |
| Listed studies using knowledge-based methods | 6% | 6% | 9% | 21% |
| Listed studies using generative AI | 0% | 2% | 0% | 4% |
| Mean pairwise overlap of matched sources (Jaccard) | 0.54 |  |  |  |
| Sampled unmatched listed studies that exist | 45 of 45 |  |  |  |

**Interpretation.** A model asked to stand in for the search returns a list that is not reproducible between runs, misses most of the literature and all of its most recent part, and describes its listed studies as more often benchmarked and deployed than the charted corpus. Fabricated references did not occur in the sample checked. None of these weaknesses is visible in the model's output itself; each was revealed only by comparison with the protocol-driven review, which is the sense in which PRISMA-ScR and LLM assistance are complements.
