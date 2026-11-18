# Wave-2 coding notes

Companion to `data/wave2_rows.csv` (headerless; column order as specified in
`CODEBOOK.md`, variables 1–28). All rows carry `wave = 2`.

**Studies coded: 37** — `S072`–`S108`.

* `S072`–`S097` = all 26 entries of `newrefs_A.bib` (all meet the inclusion criterion).
* `S098`–`S108` = the 11 entries of `newrefs_B.bib` that survived criterion screening
  (11 of 30 screened; 19 excluded, one of those as a duplicate of an A entry).

Study IDs were assigned sequentially in file order (A first, then B), continuing from
wave 1, which occupies `S001`–`S071`.

---

## 1. Inclusion criterion applied

> Studies whose contribution is the forecasting, prediction or quantitative estimation of
> relief demand, humanitarian needs, affected populations, casualties, impacts or
> emergency resource requirements in disaster/emergency contexts, **or** reviews of AI
> methods for that purpose.

For Domain B this was operationalised as: **include** if the paper predicts or estimates
needs, demand, casualties, affected populations, losses, impact, inundation,
mobility/displacement or risk levels; **exclude** if the contribution is purely
text/image classification, damage segmentation of imagery, social-media event detection,
monitoring-report generation, or a method survey not concerning demand/needs/impact
estimation.

## 2. Domain B screening record — all 30 entries

### 2.1 Included (11)

| study_id | citekey | Estimated quantity — why it qualifies |
|---|---|---|
| S098 | `Xu2025LargeLanguageAgentHousehold` | Household hurricane **food-shortage need** (commodity demand) via LLM agent simulation. |
| S099 | `Han2024EnhancedEarthquakeImpact` | Earthquake **impact** inferred from social-media text (text-to-impact, not classification alone). |
| S100 | `Wang2024NearRealTimeFatalityEstimation` | Near-real-time earthquake **fatality (casualty)** estimation. |
| S101 | `Zhang2025TornadoGraphNeuralNetworks` | Tornado-induced building **damage/loss prediction** from attributes (not imagery segmentation). |
| S102 | `Situ2025AttentionFloodDamageRisk` | Joint **flood prediction + damage and risk assessment**. |
| S103 | `Liu2024FloodDamageCastNowcasting` | Building flood **damage nowcasting** (short-horizon impact prediction). |
| S104 | `Zhou2025ClassificationSeverityDisasterLosses` | **Severity assessment of disaster losses** (see judgement call J3). |
| S105 | `ALBarqawi2026FloodInundationDeepLearning` | Building-level **flood inundation depth** prediction. |
| S106 | `Gunkel2025MachineLearningHumanMobility` | **Review** of ML for disaster-time human **mobility/displacement** — qualifies under the review clause. |
| S107 | `Alshayeb2024ExplainableStormSurgeSusceptibility` | Storm-surge **susceptibility (risk level)** modelling. |
| S108 | `Yang2025KnowledgeGraphGraphNeuralFloodRisk` | Flood disaster **risk-level** prediction. |

### 2.2 Excluded (19) — documented exclusion record

| citekey | Reason for exclusion |
|---|---|
| `Xu2025LargeLanguageDisasterReview` | **Duplicate** of `Xu2025LLMDisasterManagement` in `newrefs_A.bib` (identical DOI 10.1016/j.ijdrr.2025.105642); coded once as S090. Independently confirmed by `newrefs_dedup.json`, which lists 29 B keys and had already dropped this one. |
| `Hao2025LargeLanguageKnowledgeGraph` | LLM-assisted knowledge-graph **construction/representation** of compound crises; no quantity is predicted or estimated. |
| `Chen2024KnowledgeGraphEmergencyDecision` | Decision-support architecture (KG + LLM); no demand, needs or impact estimation. |
| `Chen2026LargeLanguagePublicOpinion` | Social-media **public-opinion analysis** of an incident; text analytics, not estimation. |
| `Zhang2026MultiAgentResilienceGame` | Multi-agent LLM **scenario/serious-game generation**; no predicted quantity. |
| `Xiao2025DamageCATTransformerFramework` | **Damage categorisation of post-disaster imagery** — explicitly out of scope. |
| `Yu2025BenchmarkingAttentionSemiSupervised` | Benchmark of attention/semi-supervised methods for **imagery-based damage assessment** — out of scope. |
| `Lagap2025ExplainableDamageAssessment` | **XAI evaluation of imagery damage-assessment models**; contribution is model evaluation, not impact estimation. |
| `Dinh2025LinguisticPatternsCrisisZones` | Descriptive **linguistic comparison** of crisis vs non-crisis posts; nothing is estimated. |
| `Wahid2025AIDrivenSocialMediaTextCrisis` | **Method survey of crisis text analysis**; does not concern demand/needs/impact estimation. |
| `Upadhyay2024SatCoBiLSTMCrisisEventDetection` | **Social-media crisis event detection** — explicitly out of scope. |
| `Cantini2025PromptBasedLargeLanguageDisasterMonitoring` | **Monitoring-report generation** from social media — explicitly out of scope. |
| `Garg2026DisT5TextToTextTransformer` | Domain-adapted **text-to-text transformer** for disaster NLP tasks; text modelling only. |
| `Adesokan2025DisTGranDGranularEventClassification` | **Event/sub-event text classification**; finer labels, still classification. |
| `Xu2025ArtificialIntelligenceDisasterManagement` | **Bibliometric survey** of AI across disaster management generally; not a review of AI methods for demand/needs/impact estimation. |
| `Hanny2026MultimodalGeospatialFoundationModel` | Foundation-model **disaster detection** framed as binary classification on an H3 grid; detection, not estimation. |
| `Ma2024GenerativeDeepLearningNaturalHazard` | Review of generative DL for **data generation/augmentation**; a data remedy, not needs or impact estimation. |
| `Nascimento2025GraphNeuralFewShotDisasterPosts` | **Multimodal classification of social-media posts**; classification only. |
| `Zarski2024MultiStepFeatureFusionDamage` | **Damage assessment (segmentation) of satellite imagery** — explicitly out of scope. |

Borderline exclusions worth re-checking at full text if the review's scope is widened:
`Xu2025ArtificialIntelligenceDisasterManagement` (a general AI-in-disaster-management
review, comparable in kind to the A-domain reviews that *were* included because their
scope is demand/needs/impact), `Ma2024GenerativeDeepLearningNaturalHazard` (relevant to
the data-scarcity argument even though it estimates nothing), and
`Hanny2026MultimodalGeospatialFoundationModel` (detection, but the only abstract-verified
foundation-model exemplar in the set).

## 3. Coding rules applied

1. **Evidence grade.** For entries marked **[T] / [TITLE-VERIFIED]** in the notes files,
   `learning_paradigm`, `horizon` and `linearity` were coded `Not reported` unless the
   title or note asserts the value (e.g. "short-term" in `S083`, "nowcasting" in `S103`,
   "near-real-time" in `S100`, "deep reinforcement learning" in `S094`), and
   `performance_evidence` was coded `Not reported` unless the note documents an actual
   metric. Only one entry, `S107`, has abstract-verified metrics; it is the single
   `Comparative benchmark` in wave 2.
2. **Method families from the method string.** `mf_*` flags were set only from method
   terms that actually appear in the title or note (e.g. transformer → `mf_dl`; grey
   model → `mf_knowledge`; PSO → `mf_optsim`; RAG/LLM → `mf_genai`). Where no model class
   is named the study carries all six flags at 0 with the phrase
   `method family not determinable` in `coding_note`: `S074`, `S075`, `S079`, `S081`,
   `S097`, `S104` (6 primaries). These should be excluded from, or reported as unknown
   in, any method-family denominator.
3. **Reviews.** The five review articles (`S088`, `S089`, `S090`, `S096`, `S106`) carry
   all `mf_*` = 0, `learning_paradigm = Not applicable` and
   `performance_evidence = Not applicable (review)`, per the codebook's N_prim rule that
   review articles do not themselves apply a method.
4. **`deployment_status`.** `Operational deployment` only where a real responding
   organisation is named as using the system: `S079` and `S080` (Danish Refugee Council)
   and `S081` (see J1 below). `Real-data case study` where a named real event or region
   is analysed: `S073` (five earthquake-affected villages), `S075` (Beijing "23·7"
   rainstorm), `S107` (Sagar Island, Indian Sundarbans). All other 31 rows are
   `Not reported`.
5. **`data_source`** was coded only where the title or note names the data (social media,
   crowdsourced content, agent-based simulation, EMS call series, DRC predictor set);
   otherwise `Not reported`. It is `Not reported` for 29 of 37 rows (Social media 3,
   Historical records 2, Simulation 2, Mixed 1).
6. **`author_country` / `focus_country`** were coded only from statements in the notes.
   Author country is known for three studies only (`S080` Denmark, `S081` Netherlands,
   `S082` Brazil); focus country for `S075` (China), `S080` (Burkina Faso; Mali; Niger;
   South Sudan) and `S107` (India), with `Global` used for the five reviews. Everything
   else is `Not reported` rather than guessed from author names or venue.
7. **Non-ASCII.** Author names were transliterated for the CSV: Kjærum → Kjaerum,
   Yılmaz → Yilmaz. (Baião, Żarski, Mühlhäuser and Díaz do not appear in a
   `first_author` cell.) The build script fails hard on any non-ASCII byte.

## 4. Judgement calls

* **J1 — `S081` `Sedhain2025ImpactBasedCycloneForecasting` coded
  `Operational deployment`.** The note states the authors are the 510 initiative of the
  Netherlands Red Cross, "the group that actually operates these models". That is a named
  responding organisation using the models in practice, so the rule is satisfied — but the
  paper itself is an *evaluation*, so if the full text shows the evaluated models are not
  fielded this should be downgraded to `Real-data case study`. Flagged in `coding_note`.
* **J2 — `S077` `Wang2026EmergencySuppliesScheduling` objective coded
  `Humanitarian logistics and supply chain management`.** A demand forecasting model is
  embedded, but the paper's contribution is the scheduling formulation. Dominant-category
  rule applied and recorded in `coding_note`.
* **J3 — `S104` `Zhou2025ClassificationSeverityDisasterLosses` included.** Its
  classification half would have been excluded; the *severity assessment of disaster
  losses* half is loss-magnitude estimation and carries the inclusion. Borderline —
  recommend R3 adjudication.
* **J4 — `S108` `Yang2025KnowledgeGraphGraphNeuralFloodRisk` scored `mf_knowledge = 1`.**
  The codebook's knowledge-based family lists CBR, rule-based reasoning, fuzzy, rough and
  grey systems, and does not name knowledge graphs. A knowledge graph is a symbolic
  knowledge representation, so the flag was set, but the codebook may need an explicit
  ruling on knowledge graphs (it also affects `Hao2025` and `Chen2024`, both excluded).
* **J5 — disaster types with no matching category.** Cold wave (`S082`) and tornado
  (`S101`) were coded `Technological/Other` as the residual category; neither is
  technological. If the codebook gains a "Meteorological/Other natural" value these two
  should move. `S107` (storm surge) was coded `Hurricane/Cyclone` because cyclone track is
  a predictor; `Flood` is a defensible alternative.
* **J6 — `disaster_type = Not reported` for five non-hazard-specific studies**
  (`S083` EMS demand, `S084` blood demand, `S085`, `S086`, `S087` intermittent/sporadic
  demand methodology). These are adjacent-literature methodological analogues included
  because relief demand occupies the intermittent regime; coding them
  `Multi-hazard/General` would have overstated hazard coverage.
* **J7 — `S097` `Zhang2025PredictiveAnalyticsHumanitarian` is `Primary` but applies no
  forecasting method.** It is an empirical organisational-capability study. It has no
  `mf_*` flag and is marked `method family not determinable`; consider excluding it from
  method and performance denominators at analysis time.
* **J8 — `sustainability = 1` for `S092` only.** The codebook includes resilience under
  this flag and `S092` makes resilience/viability an explicit design objective. `S094`'s
  equity objective was **not** counted (fairness, not environmental/social
  sustainability) — flagged for adjudication.
* **J9 — `stochastic`.** Set to 1 only where an uncertainty mechanism is named: grey
  model (`S076`), two-stage stochastic programming (`S091`), design under uncertainty
  (`S092`), sample average approximation (`S093`), data-driven stochastic framework
  (`S095`). Deliberately left 0 for `S084` ("uncertain conditions" claimed but no
  mechanism), `S086` (state-space model, distributional but not documented as such) and
  `S105` ("probability gating" is a gating mechanism, not documented uncertainty
  quantification).
* **J10 — `S078` `Zhou2023AgentEmergencyMedical` deployment left `Not reported`.** A
  purely agent-based study would arguably be `Synthetic/illustrative`, but no real event
  is named and the note does not confirm the study is simulation-only, so the
  conservative rule was applied.

## 5. Discrepancies found in the source notes

* `newrefs_A_notes.md` states its year coverage as "2023 × 5, 2024 × 3, 2025 × 9,
  2026 × 9". Counted from `newrefs_A.bib` the split is **2023 × 5, 2024 × 3, 2025 × 10,
  2026 × 8** (2025: S072, S073, S080, S081, S083, S084, S090, S092, S094, S097; 2026:
  S074, S075, S076, S077, S088, S089, S091, S095). The CSV follows the `.bib` years.
* `newrefs_B_notes.md` counts 30 entries; one (`Xu2025LargeLanguageDisasterReview`) is a
  duplicate of an A entry, so Domain B contributes at most 29 unique candidates.

## 6. Wave-2 tallies (from the CSV)

* Rows: **37** (Primary 32, Review 5).
* Years: 2023 × 5, 2024 × 7, 2025 × 16, 2026 × 9.
* Method families (counts of primary studies; multi-label, so they sum to > 32):
  statistical 2, ML 11, DL 7, knowledge-based 2, optimisation/simulation 8,
  generative AI 4. Studies with more than one family (`n_hybrid`): **8**.
  Primaries with no determinable family: 6.
* Objective: predictive modelling and forecasting 22, humanitarian logistics and SCM 7,
  methodological/technology review 5, healthcare and medical service demand 3.
* Performance evidence: `Comparative benchmark` 1 (`S107`), `Qualitative/none` 1
  (`S073`), `Not applicable (review)` 5, `Not reported` 30 — a direct consequence of the
  title-only evidence grade of most source notes, and consistent with the review's
  finding that comparative efficacy evidence is available for only a minority of the
  corpus.
* Deployment: `Operational deployment` 3, `Real-data case study` 3, `Not reported` 31.

## 7. Reproduction

`wave2_rows.csv` was generated by a build script that asserts: sequential IDs from S072,
unique citekeys, 28 fields per row, ASCII-only content, and that every primary study
either carries an `mf_*` flag or the phrase `method family not determinable` in its
`coding_note`.
