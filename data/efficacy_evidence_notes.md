# Efficacy evidence — extraction notes

Companion to `data/efficacy_evidence.csv`. Built in response to Reviewer 2's Major
Comment that the manuscript "frequently conflates the publication volume of specific AI
techniques with proof of their practical effectiveness", and that efficacy claims must be
"supported with comparative data extracted from the primary studies".

**Extraction date:** 2026-09-02. **Retrieval tools:** web search and web fetch only.

## Retrieval limitation affecting this pass — read before using the table

The fetch tool exhausted its per-session quota partway through this pass (hard stop, quota
resets 17:40 UTC). In addition, several publisher hosts were unreachable by policy rather
than by paywall:

* **ScienceDirect (Elsevier)** — `robots.txt` disallowed. This blocks the abstract pages of
  ten target studies (IJDRR, ESWA, Socio-Economic Planning Sciences, IJPE, EAAI, CIE,
  Atmospheric Environment, Journal of Hydrology).
* **PubMed Central** — served a reCAPTCHA challenge instead of article text.
* **ouci.dntb.gov.ua, ADS (Harvard)** — `robots.txt` disallowed.
* **OpenAlex / Semantic Scholar** — `abstract_inverted_index` and `abstract` are `null` for
  most Elsevier and Springer records, because those publishers do not deposit abstracts to
  Crossref. Useful only for IEEE and MDPI records.

Consequently **12 of 25 studies are graded `C-title-only`** — their titles, venues and DOIs
are confirmed, but nothing about their models, datasets or metrics was observed. Every such
cell reads `Not retrievable in this pass`. **No number in this table was inferred,
reconstructed from memory, or estimated.** A second pass after the quota reset — or a pass
with institutional full-text access to ScienceDirect — should be able to convert most of
the C rows to A or B.

Two studies (`Jiang2019EmergencyEarthquakes`, `Wu2022Dynamic-LSTMChina`) could not be
located at all from the citekey and description given; the bibliographic records themselves
need checking against the source `.bib` before either is retained.

---

## Per-study notes

### 1. `Kirbas2020ComparativeApproaches` — grade C-title-only
Title confirmed: "Comparative analysis and forecasting of COVID-19 cases in various European
countries with ARIMA, NARNN and LSTM approaches" (PMID 32565625). Three models are named in
the title, so a comparison is safe at title level; **no error metric, no numeric result and
no statement of which model won was observed.** PMC returned a reCAPTCHA page; ScienceDirect
is robots-disallowed; OpenAlex holds a null abstract.
Source: https://pubmed.ncbi.nlm.nih.gov/32565625/

### 2. `Vollmer2021ADepartments` — grade A-fulltext ✅ real numbers
Full text read. Nine methods on a common dataset: ARIMA, ETS, STLM, StructTS (time series);
glmnet, ranger, gbm, k-NN (machine learning); plus a stacked-regression ensemble. Data are
daily attendances at St Mary's and Charing Cross hospitals, Imperial College Healthcare NHS
Trust, 2011–2018, roughly 75/25 train–test.

Observed values — St Mary's: time-series methods MAE 14.46–17, MAPE 6.9–8.3%; machine
learning (batch) MAE 14.3–15.2, MAPE 6.8–7.4%; best online method glmnet with daily
retraining, MAPE 6.8%; stacked regression MAE 14.51. Charing Cross: MAPE 8.5–12%, best online
MAPE 8.6% (gbm, glmnet and a linear model), stacked regression MAE 10.60.

Supporting sentence, verbatim: "Simple linear methods like generalized linear models are
often better or at least as good as ensemble learning methods like the gradient boosting or
random forest algorithm."

**This is the single most useful citation for Reviewer 2's point**: a well-powered
comparison in which machine learning did *not* beat a penalised linear model. Note that the
MAE range quoted for Charing Cross carried a stray percent sign in the retrieved text; the
MAPE figures and the quoted sentence are the safe ones to cite.
Source: https://link.springer.com/article/10.1186/s12873-020-00395-y

### 3. `Biswas2024AnTurkiye` — grade C-title-only
Title confirmed: "An AI-based framework for earthquake relief demand forecasting: A case
study in Türkiye", IJDRR 102 (2024), doi 10.1016/j.ijdrr.2024.104287. Abstract not obtained:
ScienceDirect robots-disallowed; Semantic Scholar abstract null; the Tecnológico de
Monterrey repository record carries metadata but no abstract. **No models, metrics or
numbers observed.**
Source: https://www.sciencedirect.com/science/article/abs/pii/S2212420924000499

### 4. `Zheng2022Co-EvolutionaryForecasting` — grade B-abstract
Abstract obtained via OpenAlex (IEEE deposits abstracts). Title: "Co-Evolutionary Fuzzy Deep
Transfer Learning for Disaster Relief Demand Forecasting". **Bibliographic note:** the record
is IEEE *Transactions on Emerging Topics in Computing*, publication year 2021, vol. 10(3),
pp. 1361–1373, doi 10.1109/TETC.2021.3085337 — the citekey says 2022 (issue year); the venue
in the target list ("co-evolutionary fuzzy deep transfer learning") is correct but the year
and journal should be checked in the `.bib`.

Content: CoFDTL treats earthquakes, typhoons and floods as distinct transfer-learning tasks;
applied to two real-world Chinese disasters from 2018. Comparison is asserted against
"selected fuzzy learning and deep learning models", but **those comparators are not named and
no error metric or numeric value appears in the abstract** — the claim of "substantial
performance gains" is an author claim only at this grade. The retrieved abstract text was
returned in paraphrased form by the fetch tool, so nothing from it is quoted here as verbatim.
Source: https://api.openalex.org/works/doi:10.1109%2FTETC.2021.3085337

### 5. `Lin2020ADisaster` — grade C-title-only
Title confirmed: "A big data-driven dynamic estimation model of relief supplies demand in
urban flood disaster", IJDRR (PII S2212420919315997). ScienceDirect robots-disallowed;
OpenAlex lookup by title hit a rate limit before the quota expired. **No abstract, no
numbers observed.** The description in the target list (MLP neural network plus Baidu
population big data) is *not* confirmed by anything retrieved in this pass.
Source: https://www.sciencedirect.com/science/article/abs/pii/S2212420919315997

### 6. `Diaz-Robles2008AChile` — grade C-title-only
Title confirmed: "A hybrid ARIMA and artificial neural networks model to forecast particulate
matter in urban areas: The case of Temuco, Chile", Atmospheric Environment (PII
S1352231008006523). A full-text PDF exists at `acs.engr.utk.edu/publications/2008_DIAZ_4_AE.pdf`
but the host returns an HTTPS→HTTP redirect loop that the fetch tool will not follow, so the
PDF was never read. The title establishes a hybrid model; it does **not** establish that
standalone ARIMA and standalone ANN were benchmarked against it, so `comparative` is left
Unknown rather than Yes. **This paper is very likely to yield real numbers on a retry** —
the PDF is openly posted, it just needs a fetch that tolerates the redirect.
Source: https://www.sciencedirect.com/science/article/abs/pii/S1352231008006523

### 7. `Huang2020MedicalMethod` — grade A-fulltext ✅ real numbers
Full text read from the German National Library mirror of the open-access article. Models:
ARIMA alone, self-adaptive filtering alone, the proposed hybrid, and — on a secondary
benchmark series taken from the literature — ANN, EEMD-ANN and DWT-ANN. Data: Ningbo Yinzhou
District Maternal and Child Health Care Hospital, China, 1 January 2017 to 30 March 2018;
two series (prenatal examination visits, B-ultrasound examination visits), 283 training and
22 test observations each.

Observed values — prenatal visits: ARIMA MAPE 18.53%, hybrid MAPE 2.79%. B-ultrasound
visits: ARIMA MAPE 27.69%, hybrid MAPE 1.25%. Secondary emergency-department series: ARIMA
RMSE 201.73, MAE 160.70, R 0.62; hybrid RMSE 49.48, MAE 45, R 0.98549.

Verbatim from the abstract: "to further enlarge the prediction horizon and improve the
prediction accuracy, a hybrid prediction model integrating ARIMA and self-adaptive filtering
method is proposed."

Caveat worth recording in the manuscript: the improvement here is very large (18.53% → 2.79%
MAPE) and is a within-paper comparison against the authors' own baseline on 22 test points.
Source: https://d-nb.info/1221036556/34

### 8. `Jiang2019EmergencyEarthquakes` — grade D-unretrievable
No record matching "adaptive evolutionary support vector regression, blood demand after
earthquakes" in IFAC-PapersOnLine 2019 was located by any search formulation tried. The
bibliographic record should be verified against the source `.bib` — it may be miscited.
**Nothing observed.**

### 9. `Fuqua2022CommodityPlanning` — grade C-title-only
Title confirmed: "Commodity demand forecasting using modulated rank reduction for humanitarian
logistics planning", Expert Systems with Applications (PII S0957417422010314). The method in
the title is a matrix-factorisation technique, not a learner comparison, but whether
comparators were benchmarked is unconfirmed. **No abstract, no numbers observed.**
Source: https://www.sciencedirect.com/science/article/abs/pii/S0957417422010314

### 10. `Paul2022AnBehavior` — grade C-title-only
Identified as: "An ensemble forecasting model for predicting contribution of food donors
based on supply behavior", *Annals of Operations Research* 319(1), doi
10.1007/s10479-021-04146-5. The Springer page and the RePEc mirror were both queued when the
fetch quota expired, so **the abstract was not read**. Both are open and should yield at
least a B grade on retry. The target list's attribution ("Paul & Wang(?)") should be
resolved from the DOI.
Source: https://link.springer.com/article/10.1007/s10479-021-04146-5

### 11. `Nguyen2022ForecastingNetwork` — grade A-fulltext ✅ real numbers
Full text read via the ar5iv rendering of arXiv:1811.04577, the preprint of the IEEE
Transactions on Big Data article. Proposed model: sequence-to-sequence LSTM (encoder–decoder
with attention). Baselines: an LSTM generative model, an n-gram statistical language model,
and a CNN-based model. Data: Twitter plus weather data for Hurricane Harvey (~140,000
tweets, 23 Aug–2 Sep 2017), Irma (~60,000, 4–13 Sep 2017) and Sandy (~150,000, 24 Oct–2 Nov
2012); 80/20 train–test split. Metric: Simple Matching Coefficient.

Observed values — Harvey: seq2seq 0.875, LSTM 0.839, n-gram 0.806, CNN 0.690. Irma: 0.882,
0.858, 0.792, 0.682. Sandy: 0.878, 0.845, 0.805, 0.678. Seq2seq wins on all three events.

**Caveat:** these numbers come from the arXiv preprint, not the published IEEE version; if
they are cited in the manuscript the published version should be checked, since the target
list attributes the work to IEEE Trans. Big Data 2022.
Source: https://ar5iv.labs.arxiv.org/html/1811.04577

### 12. `Shahidian2025EMSDemandMachineLearning` — grade C-title-only
**Flagged in the task brief as open access with real numbers to extract — but not retrieved
in this pass.** Title and authorship confirmed via Semantic Scholar (Shahidian, Abreu,
Santos, Barbosa-Póvoa; *Computers & Industrial Engineering*, 2025; doi
10.1016/j.cie.2024.110765). ScienceDirect is robots-disallowed; the Semantic Scholar record
has `"abstract": null` and an empty `openAccessPdf.url`; `colab.ws` required a permission
approval that did not arrive; `ouci` is robots-disallowed. **No models, metric or numbers
observed.** This is the highest-priority target for a second pass.
Source: https://www.sciencedirect.com/science/article/pii/S0360835224008878

### 13. `Zhang2025RAGEarthquakeMaterial` — grade B-abstract
**Also flagged as open access; only partially retrieved.** Semantic Scholar returned enough
of the record to confirm the method and the case, but IEEE Xplore itself returned empty
content and the CC-BY PDF was not reached before the quota expired.

Observed: the framework "utilizes Chain-of-Thought generation to produce differentiated
prediction schemes"; the methodology was applied during the 7 January 2025 Dingri M6.8
earthquake. **No accuracy, MAPE or error value was observed, and no baseline comparison was
confirmed** — so the "AI-driven prediction" claim currently rests on a demonstration, not on
a measured benchmark, at this evidence grade. The Dingri application makes this the strongest
*deployment*-side citation in the LLM group, but deployment by a named responding
organisation is not established.
Source: https://ieeexplore.ieee.org/document/11029010/

### 14. `Kjaerum2025DisplacementAnticipatory` — grade A-fulltext ✅ real numbers, best entry in the table
Full text read on Cambridge Core. Two Danish Refugee Council models are reported and both are
benchmarked.

*AHEAD* (sub-national, 3–4 month horizon, Liptako-Gourma): "mean absolute percentage error is
15%" over 315 historical forecasts in Burkina Faso, against two simple baseline approaches
that both showed a "mean average percentage error of 21%". As a classifier it can "correctly
classify future displacement in ~70% of the time"; at a 1,200-person threshold it gets the
action/inaction decision right "69% of the time", with "17% false negatives and 14% false
positives".

*Foresight* (national, 1–3 year horizon): "mean absolute margin of error of 19% and a median
absolute margin of error of 11%" across 214 historical forecasts in 26 countries. Against the
human comparator, humanitarian plans have an "average margin of error is 23%" versus "19% for
this subset of the Foresight predictions".

**Degradation under surge — exactly what Reviewer 2 asked to see distinguished:** the
"correlation between the relative, absolute increase in displacement and the absolute margin
of error is 0.74"; where displacement increased by more than 4,759 people in three months the
"absolute average margin of error increases to 21%"; where the relative increase exceeded
35.4% the "average absolute margin of error on the forecasts is 34%". The authors state that
"predicting the onset or unprecedented escalation in displacement due to conflict is
difficult for the model".

Deployment: operational — the forecasts drive anticipatory action programming in South Sudan
and Burkina Faso. This is the only study in the 25 with confirmed operational use by a named
responding organisation, *and* it is the one that documents its own accuracy collapsing
precisely in the surge conditions that relief demand forecasting exists to serve. It should
carry the manuscript's central caveat.
Source: https://www.cambridge.org/core/journals/data-and-policy/article/pushing-the-boundaries-of-anticipatory-action-using-machine-learning/5CA9D6358F29AE35C886B92492CFFF65

### 15. `Nikseresht2025BloodDemandEnsemble` — grade B-abstract ✅ one real number
Springer abstract read. Proposed framework has three phases: signal decomposition via fuzzy
cognitive mapping, trend modelling, and ensemble correction via gradient boosting. It is
compared against "sixteen state-of-the-art algorithms" across three blood demand cases and
eight real-life datasets; **the sixteen comparators are not individually named in the
abstract.**

Observed value, verbatim: "The framework achieves an average RMSE improvement of
approximately 67% across all evaluated cases." This is a relative improvement figure only —
no absolute RMSE for any model was observed, and the baseline against which 67% is measured
is not identified in the abstract. Cite it as a claimed relative improvement, not as a
measured error level.
Source: https://link.springer.com/article/10.1007/s10479-025-06784-5

### 16. `Zhang2023IntermittentTransformer` — grade B-abstract
Springer abstract read. Transformer benchmarked against Croston's method, the
Syntetos–Boylan approximation, feedforward neural networks, recurrent neural networks and
LSTM, on 925 intermittent demand items from an airline spare parts provider, using "six
different forecasting performance measures". **No numeric result appears in the abstract.**

The reported qualitative finding is directly relevant to the review's argument: "the
advantage of Transformer over other models increases with sparsity", while models perform
comparably when sparsity is low. That is a conditional claim of superiority, not a general
one — useful for reframing assertions about deep learning's benefit in the low-data relief
regime.
Source: https://link.springer.com/article/10.1007/s10479-023-05447-7

### 17. `Svetunkov2023IntermittentStateSpace` — grade C-title-only
Title, venue and DOI confirmed from prior indexer-verified metadata: "iETS: State space model
for intermittent demand forecasting", IJPE 265:109013, doi 10.1016/j.ijpe.2023.109013.
ScienceDirect robots-disallowed and the fetch quota expired before a RePEc mirror
(`eee/proeco`) could be tried. **Nothing beyond metadata observed.** RePEc should carry this
abstract on a retry.
Source: https://doi.org/10.1016/j.ijpe.2023.109013

### 18. `Hasan2024SporadicKNNForecasting` — grade C-title-only
Title, venue and DOI confirmed from prior metadata: "Improving sporadic demand forecasting
using a modified k-nearest neighbor framework", Engineering Applications of Artificial
Intelligence 129:107633. ScienceDirect robots-disallowed; EAAI is not indexed in RePEc.
**Nothing beyond metadata observed.**
Source: https://doi.org/10.1016/j.engappai.2023.107633

### 19. `Yang2025CasualtyEmergencyMaterial` — grade A-fulltext (negative finding)
Full open-access text read on MDPI. This is a **negative case for the efficacy table and an
important one for Reviewer 2.** The paper proposes a single hybrid pipeline — regression
analysis plus intelligent analysis of pre- and post-disaster satellite imagery (Python,
OpenCV) — that estimates casualties from building collapse rates and population data and
then derives material demand indirectly. It is validated on five real earthquake-affected
villages (n1–n5) in YX Township, producing classified demand for food, water, medicine and
tents.

Verbatim from the abstract: "The findings demonstrate that the proposed approach effectively
addresses the 'black box' condition by utilizing correction factors for population density,
disaster preparedness, and emergency response capacity, providing a structured framework for
rapid and accurate demand forecasting in disaster scenarios."

**No competing model is benchmarked and no error metric is reported anywhere.** The only
validation shown is a qualitative juxtaposition of predicted against "empirically observed
statistical data" (Figure 6 caption). The word "accurate" in the abstract is therefore
unsupported by any quantitative measure — precisely the conflation Reviewer 2 objects to.
Source: https://www.mdpi.com/2079-8954/13/6/478

### 20. `Sedhain2025ImpactBasedCycloneForecasting` — grade C-title-only
Title confirmed: "Evaluating Impact-based Forecasting Models for Tropical Cyclone Anticipatory
Action", IJDRR (PII S2212420925006065). Since this is framed as an evaluation study a
comparative design is likely, but **the models, metrics and results were not observed**, so
`comparative` remains Unknown. ScienceDirect robots-disallowed; a ResearchGate PDF listing
exists and may be fetchable on retry.
Source: https://www.sciencedirect.com/science/article/abs/pii/S2212420925006065

### 21. `Fei2022DemandTheory` — grade B-abstract (negative finding)
Full abstract read verbatim via RePEc. Title: "Demand prediction of emergency materials using
case-based reasoning extended by the Dempster-Shafer theory", Fei, Liguo and Wang, Yanqing,
Socio-Economic Planning Sciences 84 (2022).

The abstract describes three contributions — a Dempster–Shafer case-retrieval strategy, a
scenario-matching method for natural hazards, and a dynamic demand prediction model — and
closes: "typhoon and earthquake disasters are used as case studies to demonstrate the
application of the proposed materials demand prediction model, and the effectiveness of the
method is demonstrated through empirical analysis."

**No competing method is named and no error metric or numeric result appears anywhere in the
abstract.** The target list records this study as "claims better accuracy than other
methods"; that claim is not visible in the abstract, and at this evidence grade the study
supplies no comparative data at all. Any manuscript sentence asserting superior accuracy for
CBR on the strength of this citation must be reframed.
Source: https://ideas.repec.org/a/eee/soceps/v84y2022ics0038012122001811.html

### 22. `Shao2021ReliefReasoning` — grade C-title-only
Identified as: Shao, J., Liang, C., Liu, Y., Xu, J. and Zhao, S., "Relief Demand Forecasting
Based on Intuitionistic Fuzzy Case-Based Reasoning", *Socio-Economic Planning Sciences* 74,
article 100932 (PII S0038012119302472). **Bibliographic note:** secondary sources date this
2020 (online) / 2021 (issue) — the citekey year should be checked. The RePEc mirror
(`eee/soceps/v74y2021ics0038012119302472.html`) is fetchable and was queued when the quota
expired; it should give a B grade on retry. **No abstract, no numbers observed.**
Source: https://www.sciencedirect.com/science/article/abs/pii/S0038012119302472

### 23. `Wu2022Dynamic-LSTMChina` — grade D-unretrievable
No Journal of Hydrology 2022 article using the term "Dynamic-LSTM" was located under any
search formulation tried. The record needs verification against the source `.bib` — the
method name may be a paraphrase rather than the paper's own term. **Nothing observed.**

### 24. `Indra2023AnCGDNN` — grade C-title-only
Title confirmed: "An improved flood forecasting system with cluster based visualization and
analyzing using GK-ANFIS and CGDNN", Expert Systems with Applications (PII S0957417422017651).
Two methods are named in the title (GK-ANFIS and CGDNN) but they appear to be pipeline
components rather than competitors, so `comparative` is Unknown. **No abstract, no numbers
observed.**
Source: https://www.sciencedirect.com/science/article/pii/S0957417422017651

### 25. `Abreu2023Data-drivenServices` — grade B-abstract
Abstract read via RePEc. Title: "Data-driven forecasting for operational planning of emergency
medical services", Abreu, Paulo; Santos, Daniel; Barbosa-Povoa, Ana; Socio-Economic Planning
Sciences 86 (2023). The paper proposes "a generic data-driven forecasting method", evaluates
the relevance of contextual data, and discusses the computational complexity of modern
techniques including neural networks; it finds that different priority calls and vehicle types
show distinct demand patterns, and that "the operational impact of the demand shared by
neighboring zones proved to be significant at bases near the border."

**No specific competing models are named, no error metric appears, and no numeric result was
observed in the abstract**, so despite the paper evidently evaluating several techniques the
comparative status is left Unknown. Note this is the same research group as
`Shahidian2025EMSDemandMachineLearning` (Abreu, Santos, Barbosa-Póvoa), so the two should be
treated as related rather than independent evidence.
Source: https://ideas.repec.org/a/eee/soceps/v86y2023ics0038012122002993.html

---

## Summary counts

| Evidence grade | n | Studies |
|---|---|---|
| **A-fulltext** | 5 | Vollmer2021, Huang2020, Nguyen2022, Kjaerum2025, Yang2025 |
| **B-abstract** | 6 | Zheng2022, Zhang2025RAG, Nikseresht2025, Zhang2023, Fei2022, Abreu2023 |
| **C-title-only** | 12 | Kirbas2020, Biswas2024, Lin2020, Diaz-Robles2008, Fuqua2022, Paul2022, Shahidian2025, Svetunkov2023, Hasan2024, Sedhain2025, Shao2021, Indra2023 |
| **D-unretrievable** | 2 | Jiang2019, Wu2022 |

* **Grade A or B: 11 of 25 (44%).** Grade C or D: 14 of 25 (56%).
* **Comparative benchmark confirmed (≥2 models on a common dataset): 8 of 25 (32%)** —
  Vollmer2021, Huang2020, Nguyen2022, Kjaerum2025, Nikseresht2025, Zhang2023, Zheng2022, and
  Kirbas2020 (title-level inference only). For the remaining 17 the comparative status is
  Unknown (16) or confirmed absent (1: Yang2025).
* **A quantitative predictive-performance metric was actually observed for 5 of 25 (20%)** —
  Vollmer2021, Huang2020, Nguyen2022, Kjaerum2025, Nikseresht2025. Confirmed absent for 2
  (Yang2025, Fei2022). Unknown for the remaining 18.
* **Operational deployment by a named responding organisation: 1 of 25** — Kjaerum2025
  (Danish Refugee Council). One further study was applied to a real event without a named
  responding organisation (Zhang2025RAG, Dingri earthquake). Nine are real-data case studies
  or unconfirmed.

### How these counts should be read in the manuscript

The 20% figure is a floor, not an estimate of the literature: it is depressed by the
retrieval failures documented at the top of this file, not only by the papers' own reporting.
The defensible claims from this pass are:

1. Where comparative benchmarks *were* recovered, they do not uniformly favour the more
   complex model. Vollmer2021 is an explicit counter-example (penalised linear regression
   matched or beat gradient boosting and random forests on two hospitals' ED demand), and
   Zhang2023 makes its transformer claim conditional on sparsity rather than general.
2. Two studies that the manuscript may currently cite as efficacy evidence report no
   quantitative metric at all (Yang2025, Fei2022) while using the language of accuracy and
   effectiveness. These are the clearest instances of the conflation Reviewer 2 identifies.
3. The one operationally deployed system in the set (Kjaerum2025) is also the one that
   quantifies its own failure mode: error roughly doubles, from 15% to 34% MAPE, in exactly
   the rapid-escalation conditions that anticipatory action targets. Any claim of operational
   benefit should be stated together with this degradation.
