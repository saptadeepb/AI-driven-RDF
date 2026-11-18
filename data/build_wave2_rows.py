#!/usr/bin/env python3
"""Build wave2_rows.csv for the scoping-review revision (wave 2 coding)."""
import csv, unicodedata

COLS = ("study_id citekey first_author year wave study_type author_country focus_country "
        "publisher journal objective disaster_type mf_statistical mf_ml mf_dl mf_knowledge "
        "mf_optsim mf_genai learning_paradigm horizon linearity sustainability stochastic "
        "performance_evidence metric_reported deployment_status data_source coding_note").split()

R = []


def row(**kw):
    missing = [c for c in COLS if c not in kw]
    if missing:
        raise SystemExit("missing fields %s for %s" % (missing, kw.get("citekey")))
    extra = [k for k in kw if k not in COLS]
    if extra:
        raise SystemExit("unknown fields %s" % extra)
    R.append([str(kw[c]) for c in COLS])


NR = "Not reported"
PRED = "Predictive modelling and forecasting"
PREP = "Disaster preparedness and relief planning"
HEALTH = "Healthcare and medical service demand"
HUMLOG = "Humanitarian logistics and supply chain management"
COMM = "Community engagement and social impact"
REVIEW = "Methodological or technology review"

# =====================================================================
# Domain A - all 26 entries (all meet the inclusion criterion)
# =====================================================================

row(study_id="S072", citekey="Zhang2025RAGEarthquakeMaterial", first_author="Zhang, S.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="IEEE", journal="IEEE Access", objective=PRED, disaster_type="Earthquake",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=1,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only; RAG + reasoning LLM stated in title so mf_genai=1. "
                "No dataset, event or metric documented in the note; open-access full text should be "
                "checked before quoting performance.")

row(study_id="S073", citekey="Yang2025CasualtyEmergencyMaterial", first_author="Yang, J.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="MDPI", journal="Systems", objective=PRED, disaster_type="Earthquake",
    mf_statistical=1, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm="Supervised", horizon="Short-term", linearity=NR, sustainability=0,
    stochastic=0, performance_evidence="Qualitative/none", metric_reported=NR,
    deployment_status="Real-data case study", data_source="Historical records",
    coding_note="Abstract read. Regression analysis plus unspecified intelligent analysis; only the "
                "regression component is codable so mf_statistical=1 and paradigm inferred as supervised. "
                "Casualty-then-material two-step estimation; validated on five earthquake-affected villages "
                "(country not stated). Abstract reports no error metric.")

row(study_id="S074", citekey="Kundu2026ReliefFloodPrediction", first_author="Kundu, S.",
    year=2026, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Taylor & Francis", journal="Journal of the Operational Research Society",
    objective=PRED, disaster_type="Flood",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only; method family not determinable - no model class named in title or "
                "note (the note's remark about the second author's prior ML work concerns other papers and "
                "was not used). Objective coded as prediction over planning as prediction is named first.")

row(study_id="S075", citekey="Cai2026SpatialFloodSupplyDemand", first_author="Cai, X.",
    year=2026, wave=2, study_type="Primary", author_country=NR, focus_country="China",
    publisher="Elsevier", journal="Urban Climate", objective=PRED, disaster_type="Flood",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status="Real-data case study",
    data_source=NR,
    coding_note="Title-verified only; method family not determinable - the title names the task (spatial "
                "prediction of emergency supply demand) but no model class. Focus country from the named "
                "case, the July 2023 Beijing rainstorm.")

row(study_id="S076", citekey="Kong2026GreyEmergencyMaterial", first_author="Kong, D.",
    year=2026, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Emerald", journal="Grey Systems: Theory and Application", objective=PRED,
    disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=1, mf_optsim=1, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=1,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. Fractional-order grey model -> mf_knowledge (grey systems) and "
                "stochastic=1 per codebook; Simpson quantum-behaved PSO -> mf_optsim (metaheuristic). "
                "Hazard type not specified in title or note.")

row(study_id="S077", citekey="Wang2026EmergencySuppliesScheduling", first_author="Wang, Y.",
    year=2026, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="Reliability Engineering & System Safety", objective=HUMLOG,
    disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=1, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. Dominant-category decision: scheduling/dispatch is the paper's "
                "contribution, so coded logistics rather than forecasting although a demand forecasting "
                "model is embedded. mf_optsim from alternative-subgraph scheduling formulation; the class "
                "of the embedded forecasting model is not stated.")

row(study_id="S078", citekey="Zhou2023AgentEmergencyMedical", first_author="Zhou, X.",
    year=2023, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="Chaos, Solitons & Fractals", objective=HEALTH,
    disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=1, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source="Simulation",
    coding_note="Title-verified only. Agent-based model -> mf_optsim and data_source=Simulation. "
                "Deployment left Not reported: no real event or region is named, though a purely "
                "simulated study would arguably be Synthetic/illustrative - flag for full-text check.")

row(study_id="S079", citekey="Nair2023ExplainableHumanitarianNeeds", first_author="Nair, R.",
    year=2023, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Wiley", journal="AI Magazine", objective=PRED,
    disaster_type="Conflict/Displacement",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status="Operational deployment",
    data_source=NR,
    coding_note="Title-verified only; method family not determinable - the note records an explainable "
                "deployed forecasting system but names no model class. Operational deployment coded "
                "because the note names the Danish Refugee Council as the operating agency and the work "
                "also appeared in the AAAI deployed-application (IAAI) track. Author country left Not "
                "reported: the first author's affiliation is not stated in the note.")

row(study_id="S080", citekey="Kjaerum2025DisplacementAnticipatory", first_author="Kjaerum, A.",
    year=2025, wave=2, study_type="Primary", author_country="Denmark",
    focus_country="Burkina Faso; Mali; Niger; South Sudan",
    publisher="Other", journal="Data & Policy", objective=PRED,
    disaster_type="Conflict/Displacement",
    mf_statistical=0, mf_ml=1, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm="Supervised", horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status="Operational deployment",
    data_source="Mixed",
    coding_note="Abstract read. Danish Refugee Council forced-displacement models for Liptako-Gourma "
                "with operational applications in South Sudan and Burkina Faso -> Operational deployment, "
                "author country Denmark. Predictors span armed conflict, food insecurity, vegetation "
                "health and malnutrition -> Mixed. Paradigm inferred supervised from forecasting from "
                "labelled predictors. Accuracy is said to be assessed but no metric is named, so "
                "performance_evidence left Not reported rather than Single-model metric.")

row(study_id="S081", citekey="Sedhain2025ImpactBasedCycloneForecasting", first_author="Sedhain, S.",
    year=2025, wave=2, study_type="Primary", author_country="Netherlands", focus_country=NR,
    publisher="Elsevier", journal="International Journal of Disaster Risk Reduction",
    objective=PRED, disaster_type="Hurricane/Cyclone",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status="Operational deployment",
    data_source=NR,
    coding_note="Title-verified only; method family not determinable - an evaluation of impact-based "
                "forecasting models whose model classes are not named. Judgement call: Operational "
                "deployment coded because the note states the authors are the 510 initiative of the "
                "Netherlands Red Cross, 'the group that actually operates these models'; downgrade to "
                "Real-data case study if the full text shows the evaluated models are not fielded. "
                "Comparative design is noted but no metric is documented, so performance_evidence is "
                "Not reported rather than Comparative benchmark.")

row(study_id="S082", citekey="Quiliche2023ColdWaveRiskML", first_author="Quiliche, R.",
    year=2023, wave=2, study_type="Primary", author_country="Brazil", focus_country=NR,
    publisher="Elsevier", journal="International Journal of Disaster Risk Reduction",
    objective=PRED, disaster_type="Technological/Other",
    mf_statistical=0, mf_ml=1, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. mf_ml=1 from 'using machine learning' in the title; no specific "
                "learner named. Disaster type: cold wave has no matching category, coded "
                "Technological/Other as the residual. Author country from the note's statement that the "
                "team is Leiras's humanitarian-logistics group at PUC-Rio.")

row(study_id="S083", citekey="Shahidian2025EMSDemandMachineLearning", first_author="Shahidian, N.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="Computers & Industrial Engineering", objective=HEALTH,
    disaster_type=NR,
    mf_statistical=0, mf_ml=1, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon="Short-term", linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR,
    data_source="Historical records",
    coding_note="Title-verified only. Horizon from 'short-term' in the title. Disaster type Not reported: "
                "EMS demand is not tied to a hazard - included as an adjacent-literature demand-"
                "forecasting analogue. data_source from the note's statement that EMS supplies dense "
                "historical call series. The note calls it a comparative study but documents no metric, "
                "so performance_evidence stays Not reported.")

row(study_id="S084", citekey="Nikseresht2025BloodDemandEnsemble", first_author="Nikseresht, A.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Springer", journal="Annals of Operations Research", objective=HEALTH,
    disaster_type=NR,
    mf_statistical=0, mf_ml=1, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. Hybrid ensemble learning -> mf_ml. Disaster type Not reported: "
                "blood demand is not hazard-specific; included as a methodological analogue for "
                "non-stationary life-critical demand. stochastic=0 although the title mentions uncertain "
                "conditions, because no uncertainty representation mechanism is documented.")

row(study_id="S085", citekey="Zhang2023IntermittentTransformer", first_author="Zhang, G. P.",
    year=2023, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Springer", journal="Annals of Operations Research", objective=PRED,
    disaster_type=NR,
    mf_statistical=0, mf_ml=0, mf_dl=1, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. Transformer neural networks -> mf_dl. Disaster type Not reported: "
                "a general intermittent-demand methodology paper included because relief demand occupies "
                "the intermittent regime.")

row(study_id="S086", citekey="Svetunkov2023IntermittentStateSpace", first_author="Svetunkov, I.",
    year=2023, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="International Journal of Production Economics", objective=PRED,
    disaster_type=NR,
    mf_statistical=1, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. iETS state-space exponential smoothing -> mf_statistical. Disaster "
                "type Not reported: general intermittent-demand methodology, included as the statistical "
                "baseline class. stochastic left 0: state-space models are distributional but the note "
                "documents no explicit uncertainty treatment.")

row(study_id="S087", citekey="Hasan2024SporadicKNNForecasting", first_author="Hasan, N.",
    year=2024, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="Engineering Applications of Artificial Intelligence",
    objective=PRED, disaster_type=NR,
    mf_statistical=0, mf_ml=1, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. Modified k-nearest-neighbour framework -> mf_ml. Disaster type Not "
                "reported: general sporadic-demand methodology included as a low-data analogue.")

row(study_id="S088", citekey="Abdulrashid2026AIDecisionSupport", first_author="Abdulrashid, I.",
    year=2026, wave=2, study_type="Review", author_country=NR, focus_country="Global",
    publisher="Elsevier",
    journal="Transportation Research Part E: Logistics and Transportation Review",
    objective=REVIEW, disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm="Not applicable", horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence="Not applicable (review)", metric_reported=NR, deployment_status=NR,
    data_source=NR,
    coding_note="Review article: mf_* flags left 0 because review articles do not themselves apply a "
                "method and method-family percentages use the N_prim denominator.")

row(study_id="S089", citekey="Nguyen2026MachineLearningHumanitarian", first_author="Nguyen, S.",
    year=2026, wave=2, study_type="Review", author_country=NR, focus_country="Global",
    publisher="Emerald",
    journal="Journal of Humanitarian Logistics and Supply Chain Management", objective=REVIEW,
    disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm="Not applicable", horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence="Not applicable (review)", metric_reported=NR, deployment_status=NR,
    data_source=NR,
    coding_note="Review of ML application domains and quality assurance in humanitarian logistics; "
                "mf_* left 0 per the review rule.")

row(study_id="S090", citekey="Xu2025LLMDisasterManagement", first_author="Xu, F.",
    year=2025, wave=2, study_type="Review", author_country=NR, focus_country="Global",
    publisher="Elsevier", journal="International Journal of Disaster Risk Reduction",
    objective=REVIEW, disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm="Not applicable", horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence="Not applicable (review)", metric_reported=NR, deployment_status=NR,
    data_source=NR,
    coding_note="Review of LLM applications across disaster management; mf_* left 0 per the review rule "
                "even though the reviewed methods are generative. DUPLICATE: the same article appears in "
                "newrefs_B.bib as Xu2025LargeLanguageDisasterReview (identical DOI "
                "10.1016/j.ijdrr.2025.105642); coded once here, and the B key must be dropped from "
                "references.bib.")

row(study_id="S091", citekey="Sadeghi2026MLStochasticRouting", first_author="Sadeghi, A.",
    year=2026, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier",
    journal="Transportation Research Part E: Logistics and Transportation Review",
    objective=HUMLOG, disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=1, mf_dl=0, mf_knowledge=0, mf_optsim=1, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=1,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. Machine learning embedded in a two-stage stochastic vehicle "
                "routing model -> mf_ml + mf_optsim, stochastic=1 (two-stage stochastic programming is "
                "named in the title).")

row(study_id="S092", citekey="Yilmaz2025ResilientHumanitarianML", first_author="Yilmaz, O. F.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier",
    journal="Transportation Research Part E: Logistics and Transportation Review",
    objective=HUMLOG, disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=1, mf_dl=0, mf_knowledge=0, mf_optsim=1, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=1, stochastic=1,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. ML-embedded supply chain design -> mf_ml + mf_optsim. "
                "sustainability=1 because resilience and viability are explicit design objectives, which "
                "the codebook includes under this flag. stochastic=1 from 'under uncertainty' in a "
                "design-optimisation title; confirm the mechanism at full text.")

row(study_id="S093", citekey="Hu2024MachineLearningSupplierRelief", first_author="Hu, S.",
    year=2024, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier",
    journal="Transportation Research Part E: Logistics and Transportation Review",
    objective=HUMLOG, disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=1, mf_dl=0, mf_knowledge=0, mf_optsim=1, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=1,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. ML-based sample average approximation for supplier selection -> "
                "mf_ml + mf_optsim; SAA is scenario-based stochastic optimisation -> stochastic=1. Role "
                "of prediction here is learned scenario generation rather than point demand forecasting.")

row(study_id="S094", citekey="Ahmad2025DeepRLReliefDistribution", first_author="Ahmad, M.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="Engineering Applications of Artificial Intelligence",
    objective=HUMLOG, disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=1, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm="Reinforcement", horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. Deep reinforcement learning is stated in the title -> mf_dl and "
                "learning_paradigm=Reinforcement (the one paradigm the title does assert). "
                "sustainability=0: the paper's equity objective is a fairness rather than an "
                "environmental/resilience objective - borderline, flag for adjudication.")

row(study_id="S095", citekey="Chen2026FloodHumanitarianDataDriven", first_author="Chen, R.",
    year=2026, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="Computers & Industrial Engineering", objective=HUMLOG,
    disaster_type="Flood",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=1, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=1,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only. Data-driven stochastic planning framework -> mf_optsim, "
                "stochastic=1. Horizon left Not reported although the framing is forward-looking "
                "('future flood risks'), because no horizon is stated.")

row(study_id="S096", citekey="Geng2024ResourceManagementReview", first_author="Geng, S.",
    year=2024, wave=2, study_type="Review", author_country=NR, focus_country="Global",
    publisher="Springer", journal="Annals of Operations Research", objective=REVIEW,
    disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm="Not applicable", horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence="Not applicable (review)", metric_reported=NR, deployment_status=NR,
    data_source=NR,
    coding_note="Bibliometric and content-analysis review of disaster-relief resource management; mf_* "
                "left 0 per the review rule.")

row(study_id="S097", citekey="Zhang2025PredictiveAnalyticsHumanitarian", first_author="Zhang, Y.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Emerald",
    journal="Journal of Humanitarian Logistics and Supply Chain Management", objective=HUMLOG,
    disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="Title-verified only; method family not determinable. This is an empirical "
                "organisational-capability study of big data and predictive analytics in humanitarian "
                "supply chains, not a study that applies a forecasting method, so no mf_* flag is set; "
                "its analysis technique (likely survey-based modelling) is not documented. Consider "
                "excluding from N_prim method denominators at analysis time.")

# =====================================================================
# Domain B - the 11 entries that meet the demand/needs/impact criterion
# =====================================================================

row(study_id="S098", citekey="Xu2025LargeLanguageAgentHousehold", first_author="Xu, J.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="International Journal of Disaster Risk Reduction",
    objective=PRED, disaster_type="Hurricane/Cyclone",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=1, mf_genai=1,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source="Simulation",
    coding_note="INCLUDED from Domain B: estimates a household commodity need (hurricane food "
                "shortages). Title-verified only. LLM agent simulation -> mf_genai + mf_optsim "
                "(agent-based simulation). Objective coded as prediction rather than community "
                "engagement because the target is a quantified need gap.")

row(study_id="S099", citekey="Han2024EnhancedEarthquakeImpact", first_author="Han, J.",
    year=2024, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="International Journal of Disaster Risk Reduction",
    objective=PRED, disaster_type="Earthquake",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=1,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source="Social media",
    coding_note="INCLUDED from Domain B: text-to-impact inference, i.e. earthquake impact estimation, "
                "not text classification alone. Title-verified only; LLM stated in title -> mf_genai; "
                "social media texts stated -> data_source.")

row(study_id="S100", citekey="Wang2024NearRealTimeFatalityEstimation", first_author="Wang, C.",
    year=2024, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="International Journal of Disaster Risk Reduction",
    objective=PRED, disaster_type="Earthquake",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=1,
    learning_paradigm=NR, horizon="Dynamic/real-time", linearity=NR, sustainability=0,
    stochastic=0, performance_evidence=NR, metric_reported=NR, deployment_status=NR,
    data_source="Social media",
    coding_note="INCLUDED from Domain B: near-real-time earthquake fatality (casualty) estimation. "
                "Title-verified only; LLMs -> mf_genai; 'near-real-time' -> horizon. data_source coded "
                "Social media for the stated crowdsourced user-generated data. Deployment left Not "
                "reported: USGS PAGER personnel are co-authors but the note does not state the system is "
                "in operational use.")

row(study_id="S101", citekey="Zhang2025TornadoGraphNeuralNetworks", first_author="Zhang, D.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="International Journal of Disaster Risk Reduction",
    objective=PRED, disaster_type="Technological/Other",
    mf_statistical=0, mf_ml=1, mf_dl=1, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="INCLUDED from Domain B: predicts tornado-induced building damage (physical impact "
                "prediction from attributes, not imagery segmentation). Title-verified only; tree-based "
                "models -> mf_ml, graph neural networks -> mf_dl. Disaster type: tornado has no matching "
                "category, coded Technological/Other as the residual. The note explicitly warns the "
                "direction of the comparison was not observed and no metric is documented, so "
                "performance_evidence stays Not reported despite the comparative design.")

row(study_id="S102", citekey="Situ2025AttentionFloodDamageRisk", first_author="Situ, Z.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="International Journal of Disaster Risk Reduction",
    objective=PRED, disaster_type="Flood",
    mf_statistical=0, mf_ml=0, mf_dl=1, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="INCLUDED from Domain B: joint flood prediction and damage/risk assessment, i.e. impact "
                "estimation rather than damage segmentation alone. Title-verified only; attention-based "
                "deep learning -> mf_dl. data_source left Not reported: the land-use segmentation task "
                "implies imagery but no data source is named. Crossref records volume 116 (2025) under a "
                "2024-prefixed DOI; year coded 2025 as published.")

row(study_id="S103", citekey="Liu2024FloodDamageCastNowcasting", first_author="Liu, C.-F.",
    year=2024, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="International Journal of Disaster Risk Reduction",
    objective=PRED, disaster_type="Flood",
    mf_statistical=0, mf_ml=1, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon="Dynamic/real-time", linearity=NR, sustainability=0,
    stochastic=0, performance_evidence=NR, metric_reported=NR, deployment_status=NR,
    data_source=NR,
    coding_note="INCLUDED from Domain B: building flood damage nowcasting is short-horizon impact "
                "prediction. Title-verified only; machine learning with data augmentation -> mf_ml; "
                "'nowcasting' -> horizon Dynamic/real-time.")

row(study_id="S104", citekey="Zhou2025ClassificationSeverityDisasterLosses", first_author="Zhou, W.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="Information Processing & Management", objective=PRED,
    disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source="Social media",
    coding_note="INCLUDED from Domain B on the strength of the severity-assessment component (loss "
                "magnitude estimation); the classification half alone would have been excluded - "
                "borderline, flag for adjudication. Title-verified only; method family not determinable "
                "- multi-modal text-plus-image analysis is described but no architecture is named.")

row(study_id="S105", citekey="ALBarqawi2026FloodInundationDeepLearning", first_author="ALBarqawi, A.",
    year=2026, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="Elsevier", journal="Progress in Disaster Science", objective=PRED,
    disaster_type="Flood",
    mf_statistical=0, mf_ml=0, mf_dl=1, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="INCLUDED from Domain B: building-level flood inundation depth prediction. "
                "Title-verified only; building-focused deep learning -> mf_dl. stochastic=0: "
                "'probability gating' is named but is not documented as an uncertainty representation.")

row(study_id="S106", citekey="Gunkel2025MachineLearningHumanMobility", first_author="Gunkel, J.",
    year=2025, wave=2, study_type="Review", author_country=NR, focus_country="Global",
    publisher="Elsevier", journal="Progress in Disaster Science", objective=REVIEW,
    disaster_type="Multi-hazard/General",
    mf_statistical=0, mf_ml=0, mf_dl=0, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm="Not applicable", horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence="Not applicable (review)", metric_reported=NR, deployment_status=NR,
    data_source=NR,
    coding_note="INCLUDED from Domain B under the 'reviews of AI methods for that purpose' clause: a "
                "systematic review of ML for disaster-time human mobility, i.e. displacement, which "
                "determines where relief demand materialises. mf_* left 0 per the review rule.")

row(study_id="S107", citekey="Alshayeb2024ExplainableStormSurgeSusceptibility",
    first_author="Alshayeb, M. J.", year=2024, wave=2, study_type="Primary", author_country=NR,
    focus_country="India", publisher="Springer", journal="Natural Hazards", objective=PRED,
    disaster_type="Hurricane/Cyclone",
    mf_statistical=0, mf_ml=1, mf_dl=1, mf_knowledge=0, mf_optsim=0, mf_genai=0,
    learning_paradigm="Supervised", horizon=NR, linearity="Non-linear", sustainability=0,
    stochastic=0, performance_evidence="Comparative benchmark",
    metric_reported="Accuracy; F1-score", deployment_status="Real-data case study",
    data_source=NR,
    coding_note="INCLUDED from Domain B: storm surge susceptibility, i.e. hazard risk-level estimation. "
                "Abstract verified: DNN and 1D-CNN -> mf_dl, LightGBM -> mf_ml; three models compared on "
                "one dataset with accuracy and F1 (DNN 97.75 percent accuracy, 97.85 percent F1; CNN and "
                "LightGBM 97.5 percent accuracy) -> Comparative benchmark. Case is Sagar Island, Indian "
                "Sundarbans -> focus country India. Disaster type coded Hurricane/Cyclone as storm surge "
                "with cyclone track as a predictor; Flood is a defensible alternative. Bayesian "
                "hyperparameter optimisation and SHAP were not counted as method families. data_source "
                "Not reported: predictor layers are named but the source is not.")

row(study_id="S108", citekey="Yang2025KnowledgeGraphGraphNeuralFloodRisk", first_author="Yang, P.",
    year=2025, wave=2, study_type="Primary", author_country=NR, focus_country=NR,
    publisher="IEEE", journal="IEEE Access", objective=PRED, disaster_type="Flood",
    mf_statistical=0, mf_ml=0, mf_dl=1, mf_knowledge=1, mf_optsim=0, mf_genai=0,
    learning_paradigm=NR, horizon=NR, linearity=NR, sustainability=0, stochastic=0,
    performance_evidence=NR, metric_reported=NR, deployment_status=NR, data_source=NR,
    coding_note="INCLUDED from Domain B: predicts flood disaster risk levels. Title-verified only; "
                "graph neural networks -> mf_dl. mf_knowledge=1 is a judgement call: the codebook's "
                "knowledge-based family lists CBR, rules, fuzzy, rough and grey but not knowledge "
                "graphs, and a knowledge graph is a symbolic knowledge representation - flag for "
                "adjudication.")

# ---------------------------------------------------------------------
out = "/home/claude/rev/data/wave2_rows.csv"
for r in R:
    for i, v in enumerate(r):
        v2 = unicodedata.normalize("NFKD", v)
        if any(ord(c) > 127 for c in v2):
            raise SystemExit("non-ASCII in %s field %s: %r" % (r[0], COLS[i], v))
        r[i] = v2
ids = [r[0] for r in R]
assert ids == ["S%03d" % n for n in range(72, 72 + len(R))], ids
assert len(set(r[1] for r in R)) == len(R)
for r in R:
    if r[COLS.index("study_type")] == "Primary":
        flags = [int(r[COLS.index(c)]) for c in
                 ("mf_statistical", "mf_ml", "mf_dl", "mf_knowledge", "mf_optsim", "mf_genai")]
        if sum(flags) == 0 and "method family not determinable" not in r[COLS.index("coding_note")]:
            raise SystemExit("primary %s has no mf flag and no note" % r[0])
with open(out, "w", newline="") as f:
    csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n").writerows(R)
print("wrote", len(R), "rows to", out)
