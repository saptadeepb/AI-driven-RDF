# AI-driven-RDF

Data and code for the scoping review **"Artificial Intelligence for Relief Demand Forecasting: A PRISMA-ScR Scoping Review of Research Attention and Efficacy Evidence"** (Biswas, Kumar, Hajiaghaei-Keshteli, Simic, Pamucar and Bera; *Systems and Soft Computing*, under review).

Every statistic, figure and table that describes the corpus of 110 included sources is computed by the code here from one master extraction dataset.

## Contents

| Path | What it holds |
|---|---|
| `data/master_extraction.csv` (`.xlsx`) | One row per included source (110 rows: 96 primary studies, 14 reviews), 28 variables. Defined in `data/CODEBOOK.md`. |
| `data/wave1_rows.csv`, `data/wave2_rows.csv` | Charted rows from which the master dataset is assembled |
| `data/recoding_R2.csv`, `data/outlet_corrections_R2.csv` | Every correction applied after the first charting, with its evidence |
| `data/excluded_after_verification_R2.csv` | Sources excluded at full-text re-assessment |
| `data/charting_basis_R2.csv` | The text (full text, abstract, or title and record) from which late-charted sources are coded |
| `data/efficacy_evidence.csv` | Extracted performance results (Table 5 of the article) |
| `data/deployment_cases.csv` | Charting of the field-validated studies (Tables 6 and 7) |
| `data/search_*`, `data/screening_log_R2.csv` | Search-string coverage audit and the harmonized search strategy, with blank logs for a future update |
| `data/reference_audit_R2.csv`, `data/reference_corrections_R2.csv` | Audit of every cited reference and the corrections made |
| `data/llm_comparison/` | Raw outputs, adjudication and scoring of the pre-specified LLM comparison (Supplementary S4) |
| `code/` | The pipeline (see below) |
| `figures/`, `tables/`, `stats_macros.tex`, `period_macros.tex` | Generated outputs, as used in the article |
| `supplementary/` | S1 PRISMA-ScR checklist, S2 practitioner guide, S3 benchmark task card (JSON Schema), S4 LLM comparison (protocol, prompts and results), S5 harmonized search strategy |

## Reproducing the results

```
pip install pandas numpy matplotlib openpyxl
bash reproduce.sh
```

`reproduce.sh` rebuilds the master dataset from the charted rows and the logged corrections, then every statistic (`stats_macros.tex`), the search audit, the worked examples of the practitioner guide, the LLM-comparison scoring, every figure and every table. Run on this repository it reproduces the committed outputs exactly.

The coding rules R1 to R6 (Table 2 of the article) are applied in code, so derived variables such as functional form are reproducible from the method-family flags.

## Citation

Please cite the article and this repository (`CITATION.cff`).

## Licence

MIT (see `LICENSE`).
