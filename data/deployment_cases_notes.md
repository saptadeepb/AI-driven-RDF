# Deployment cases audit: sources read, access limits, deployment judgements

Companion to `deployment_cases.json`. Every field there is a `{value, location, quote}` object. Quotes are 15 words or fewer. "not reported" means the full text was read and the item is absent. "not verified" means the full text could not be read.

## Method and caveats that apply to all three

- The shell has no internet, so I used WebSearch and WebFetch. WebFetch passes each page through a summarising model. I ran three targeted passes per paper and asked for verbatim fragments with page and section. The quotes are the fragments it returned. **Spot-check them against the PDFs before they go into the manuscript.**
- The search budget ran out during the work, so some alternative routes could not be tried (Wiley full text by another URL, ResearchGate, Semantic Scholar, IBM Research).

## 1. Nair, Madsen and Kjaerum (2023), AI Magazine 44:354-362

- **What I read:** the ABSTRACT ONLY, and not the AI Magazine abstract. It is the abstract of the closely related AAAI-23 paper, read via mlanthology.org and papers.cool. That paper is an IAAI deployed-application paper with the same title and authors: Proc. AAAI 37(13), pp. 15569-15575, DOI 10.1609/aaai.v37i13.26846.
- **What failed:**
  - Wiley (doi 10.1002/aaai.12133): the fetch failed (client error).
  - doi.org redirect: not allowed.
  - ojs.aaai.org article page and PDF: blocked by bot protection (Anubis) or not on the allowlist.
- **Not used as evidence:**
  - liner.com: an AI-generated review. It mentions gradient-boosted trees, quantile regression and year-3 MAPE of Myanmar 20.0% and Afghanistan 7.6%, and says the model beat HRPs in 9 of 13 countries. These are unverified secondary claims and must not be charted.
  - HDX Centre model-review page: a separate source. It says DRC built Foresight with technical partner IBM, gives a 1-3 year horizon, and notes that sudden-onset displacement is not captured.
- **Charted content:** only what the abstract states. Foresight is deployed at DRC since early 2020. It produces long-term forced-displacement forecasts for response planning. It is explainable and supports scenarios. It powers several downstream DRC functions and is central to the annual Global Displacement Report. All barrier categories are "not verified".
- **Deployment judgement: MEETS** operational deployment. Evidence: "in deployment since early 2020 and powers several downstream business functions within DRC". The use is for planning and reporting, not trigger-based action. This judgement rests on the abstract alone.
- **Action needed:** someone with library access should pull the AI Magazine PDF to fill the barrier fields. The abstract says the paper discusses "lessons learnt, along with technical limitations and challenges".

## 2. Kjaerum and Madsen (2025), Data & Policy 7, e8

- **What I read:** the FULL TEXT, from the open-access PDF on Cambridge Core (S2632324924000889a.pdf), in three passes. The Cambridge HTML landing page was not allowed. Page numbers (e8-x) were inferred from the running footers.
- **Content:** the paper covers two DRC systems.
  - Foresight: national, 1-3 years ahead; an ensemble of gradient-boosted trees and linear models; 19% mean absolute error, against 23% for humanitarian response plans.
  - AHEAD: Admin 1/2, 3-4 months ahead; a Bayesian state-space model; 15% MAPE, against 21% for two naive baselines.
  - It also covers a trigger design for Akobo, South Sudan: a forecast increase of 1,000 combined with community indicators.
- **Gaps:**
  - The paper does NOT state that the Akobo trigger was reached, that actions were delivered, or that any funding was released.
  - Burkina Faso anticipatory-action use appears only in the abstract; no case is described.
  - Foresight's planning use is phrased as an aim ("The aim of the Foresight is to be used for yearly, strategic planning purposes").
  - Data update cadence is not reported. The source of the displacement data is described only as "official figures".
- **Deployment judgement: PARTIALLY MEETS.** A named organisation (DRC) built the models and uses them in anticipatory-action design: "the DRC set up community action plans to act ahead of displacement". Activation and outcomes are undocumented. The paper itself asks for "Further evidence ... on the different outcomes and impact".

## 3. Sedhain et al. (2025), IJDRR 129, 105782

- **What I read:** the FULL TEXT, from the PDF hosted by Anticipation Hub (Documents/Academic_Papers/Sedhain_etal_2025.pdf), in three passes. Page numbers are the printed journal footers. ScienceDirect was not accessed.
- **Content:**
  - Typhoon Kammuri (2019) in the Philippines is the case study.
  - Statistical-IBF model: XGBoost; target is the fraction of houses completely damaged per municipality; trigger is >10% in more than 3 municipalities at 72 h.
  - It is the operational trigger of the Philippine Red Cross T-EAP, approved in 2019. It triggered at 81 h, with POD 0.03 and FAR 0.75 (Table 4).
  - The BDRCS elementary damage-curve model was adapted post hoc. It "would have triggered" at 72 h, with POD 0.17 and FAR 0.40.
- **Internal inconsistencies to watch** (as reported by the fetch passes):
  - The trigger time is 72 h in the methods but 81 h in the results.
  - The model is trained on 37 storms but tested on 39.
  - The elementary threshold is 10% in Table 4 but 25% in Section 4.3.
  - The C-EAP is dated 2018 in the text but 2021 in the reference.
- **Deployment judgement: MEETS, for the statistical model only, with caveats.**
  - Evidence: "the statistical model was operationally deployed to trigger AA" (Section 1, p. 3) and "which was operational during the event, triggered early action 81 h before landfall" (Section 3.2, pp. 11-12).
  - The study itself is a retrospective single-event evaluation.
  - The elementary model's Philippine use is hypothetical.
  - The R Shiny portal is a "research prototype".
  - Delivery of early actions, people reached and DREF release are not reported.
  - The review's operational coding is therefore supported by the text, not just the title, but it should be worded as "evaluation of an operationally deployed trigger model (PRC T-EAP)".

## Cross-cutting observation

None of the three reports measured outcomes of deployment: no people reached, no avoided losses, no counterfactual. Neither of the two full texts read reports computing or connectivity barriers for the forecasting system (Nair et al. could not be checked). Sedhain notes limited technical capacity in some regions. Kjaerum and Madsen note the need for "systems and tools" to integrate data.
