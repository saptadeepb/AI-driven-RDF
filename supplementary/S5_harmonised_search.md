# Supplementary Material S5: Harmonized search strategy

*Artificial Intelligence for Relief Demand Forecasting: A PRISMA-ScR Scoping Review of Research Attention and Efficacy Evidence*

## 1. Concept blocks (identical in every database)

**A. Relief-demand object:** "relief demand" OR "humanitarian demand" OR "humanitarian need\*" OR "relief suppl\*" OR "emergency suppl\*" OR "emergency material\*" OR "emergency resource\*" OR "emergency supply chain\*" OR "disaster relief" OR "humanitarian logistic\*"

**B. Forecasting operation:** forecast\* OR predict\* OR estimat\*

**C. Computational method:** "artificial intelligence" OR "machine learning" OR "deep learning" OR "neural network\*" OR "data-driven" OR "time series" OR "large language model\*" OR "generative AI" OR fuzzy OR "case-based reasoning" OR "grey model\*" OR "rough set\*"

Blocks are joined by AND. In PubMed, block A is additionally OR-ed with "Disasters"\[Mesh\], "Relief Work"\[Mesh\], "Emergency Medical Services"\[Mesh\].

## 2. Query in each database's syntax

### Scopus

Field tag: TITLE-ABS-KEY

> TITLE-ABS-KEY ( "relief demand" OR "humanitarian demand" OR "humanitarian need\*" OR "relief suppl\*" OR "emergency suppl\*" OR "emergency material\*" OR "emergency resource\*" OR "emergency supply chain\*" OR "disaster relief" OR "humanitarian logistic\*" ) AND TITLE-ABS-KEY ( forecast\* OR predict\* OR estimat\* ) AND TITLE-ABS-KEY ( "artificial intelligence" OR "machine learning" OR "deep learning" OR "neural network\*" OR "data-driven" OR "time series" OR "large language model\*" OR "generative AI" OR fuzzy OR "case-based reasoning" OR "grey model\*" OR "rough set\*" )

### Web of Science Core Collection

Field tag: TS= (title, abstract, author keywords, Keywords Plus)

> TS=( "relief demand" OR "humanitarian demand" OR "humanitarian need\*" OR "relief suppl\*" OR "emergency suppl\*" OR "emergency material\*" OR "emergency resource\*" OR "emergency supply chain\*" OR "disaster relief" OR "humanitarian logistic\*" ) AND TS=( forecast\* OR predict\* OR estimat\* ) AND TS=( "artificial intelligence" OR "machine learning" OR "deep learning" OR "neural network\*" OR "data-driven" OR "time series" OR "large language model\*" OR "generative AI" OR fuzzy OR "case-based reasoning" OR "grey model\*" OR "rough set\*" )

### ScienceDirect

Field tag: Title, abstract or author-specified keywords

> Same three blocks, split into sub-queries to respect the limit on Boolean connectors per field; the union of the sub-query results is exported (see the note below).

### SpringerLink

Field tag: Title and abstract where the interface allows; otherwise all fields, restricted to articles and chapters

> Same three blocks ( "relief demand" OR "humanitarian demand" OR "humanitarian need\*" OR "relief suppl\*" OR "emergency suppl\*" OR "emergency material\*" OR "emergency resource\*" OR "emergency supply chain\*" OR "disaster relief" OR "humanitarian logistic\*" ) AND ( forecast\* OR predict\* OR estimat\* ) AND ( "artificial intelligence" OR "machine learning" OR "deep learning" OR "neural network\*" OR "data-driven" OR "time series" OR "large language model\*" OR "generative AI" OR fuzzy OR "case-based reasoning" OR "grey model\*" OR "rough set\*" )

### IEEE Xplore

Field tag: All Metadata

> ("All Metadata":( "relief demand" OR "humanitarian demand" OR "humanitarian need\*" OR "relief suppl\*" OR "emergency suppl\*" OR "emergency material\*" OR "emergency resource\*" OR "emergency supply chain\*" OR "disaster relief" OR "humanitarian logistic\*" )) AND ("All Metadata":( forecast\* OR predict\* OR estimat\* )) AND ("All Metadata":( "artificial intelligence" OR "machine learning" OR "deep learning" OR "neural network\*" OR "data-driven" OR "time series" OR "large language model\*" OR "generative AI" OR fuzzy OR "case-based reasoning" OR "grey model\*" OR "rough set\*" ))

### PubMed

Field tag: Title/Abstract [tiab] and MeSH

> ( "Disasters"\[Mesh\] OR "Relief Work"\[Mesh\] OR "Emergency Medical Services"\[Mesh\] OR "relief demand"\[tiab\] OR "humanitarian demand"\[tiab\] OR "humanitarian need\*"\[tiab\] OR "relief suppl\*"\[tiab\] OR "emergency suppl\*"\[tiab\] OR "emergency material\*"\[tiab\] OR "emergency resource\*"\[tiab\] OR "emergency supply chain\*"\[tiab\] OR "disaster relief"\[tiab\] OR "humanitarian logistic\*"\[tiab\] ) AND ( forecast\*\[tiab\] OR predict\*\[tiab\] OR estimat\*\[tiab\] ) AND ( "artificial intelligence"\[tiab\] OR "machine learning"\[tiab\] OR "deep learning"\[tiab\] OR "neural network\*"\[tiab\] OR "data-driven"\[tiab\] OR "time series"\[tiab\] OR "large language model\*"\[tiab\] OR "generative AI"\[tiab\] OR fuzzy\[tiab\] OR "case-based reasoning"\[tiab\] OR "grey model\*"\[tiab\] OR "rough set\*"\[tiab\] )

ScienceDirect limits the number of Boolean connectors per field. Run block A in sub-queries of at most eight terms, each combined with the full blocks B and C as far as the limit allows (splitting block C in the same way if necessary), export every sub-query, and take the union before deduplication. Record every sub-query as executed.

Where an interface does not support right-hand truncation, enter the truncated terms as their singular and plural forms.

Verify the exact operator and field syntax in each interface on the day of execution and record any adaptation in the execution log.

## 3. Execution checklist

1. Run each query from inception to the execution date; record the date, the exact query as executed, any filters and the number of records.
2. Export full records (title, abstract, authors, year, venue, DOI) in RIS or CSV.
3. Deduplicate across databases and against all records already screened for the review.
4. Screen titles and abstracts of new records in duplicate under the unchanged eligibility criteria (Section 3.2); log every decision.
5. Assess full texts of potentially eligible records in duplicate, recording the exclusion reason.
6. Chart included studies under the codebook, regenerate the statistics and update the PRISMA flow diagram.

## 4. Coverage audit of the strings with which the corpus was identified

1 = term present in that database's string.

| Concept block | Term | Scopus | Web of Science | ScienceDirect | Springer Nature | IEEE Xplore | PubMed |
|---|---|---|---|---|---|---|---|
| A relief-demand object | relief demand | 1 | 1 | 1 | 1 | 1 | 0 |
| A relief-demand object | humanitarian demand | 1 | 0 | 0 | 0 | 0 | 0 |
| A relief-demand object | humanitarian need* | 1 | 0 | 0 | 0 | 0 | 0 |
| A relief-demand object | relief suppl* | 1 | 0 | 0 | 0 | 0 | 0 |
| A relief-demand object | emergency suppl* | 1 | 1 | 1 | 0 | 0 | 0 |
| A relief-demand object | emergency material* | 1 | 0 | 0 | 0 | 0 | 0 |
| A relief-demand object | emergency resource* | 0 | 0 | 0 | 0 | 1 | 0 |
| A relief-demand object | emergency supply chain* | 0 | 1 | 0 | 0 | 0 | 0 |
| A relief-demand object | disaster relief | 0 | 1 | 0 | 0 | 1 | 0 |
| A relief-demand object | humanitarian logistic* | 0 | 1 | 0 | 1 | 0 | 0 |
| B forecasting operation | forecast* | 1 | 1 | 1 | 1 | 1 | 1 |
| B forecasting operation | predict* | 1 | 1 | 1 | 1 | 1 | 1 |
| B forecasting operation | estimat* | 1 | 0 | 0 | 0 | 0 | 0 |
| C computational method | artificial intelligence | 1 | 1 | 1 | 1 | 1 | 1 |
| C computational method | machine learning | 1 | 1 | 1 | 1 | 1 | 1 |
| C computational method | deep learning | 1 | 1 | 0 | 0 | 1 | 0 |
| C computational method | neural network* | 1 | 1 | 0 | 0 | 0 | 0 |
| C computational method | data-driven | 1 | 0 | 0 | 0 | 0 | 0 |
| C computational method | time series | 1 | 0 | 0 | 0 | 0 | 0 |
| C computational method | large language model* | 1 | 0 | 0 | 0 | 0 | 0 |
| C computational method | generative AI | 0 | 0 | 0 | 0 | 0 | 0 |
| C computational method | fuzzy | 0 | 0 | 0 | 0 | 0 | 0 |
| C computational method | case-based reasoning | 0 | 0 | 0 | 0 | 0 | 0 |
| C computational method | grey model* | 0 | 0 | 0 | 0 | 0 | 0 |
| C computational method | rough set* | 0 | 0 | 0 | 0 | 0 | 0 |

## 5. Strings with which the corpus was identified

**Scopus** (TITLE-ABS-KEY): ( "relief demand" OR "humanitarian demand" OR "emergency material\*" OR "relief suppl\*" OR "emergency suppl\*" OR "humanitarian need\*" ) AND ( forecast\* OR predict\* OR estimat\* ) AND ( "artificial intelligence" OR "machine learning" OR "deep learning" OR "neural network\*" OR "large language model\*" OR "data-driven" OR "time series" )

**Web of Science** (TS=): ( "relief demand" OR "humanitarian logistic\*" OR "emergency supply chain" OR "disaster relief" ) AND ( forecast\* OR predict\* ) AND ( "artificial intelligence" OR "machine learning" OR "deep learning" OR "neural network\*" )

**ScienceDirect** (Title, abstract, keywords): ("relief demand" OR "emergency supplies") AND (forecasting OR prediction) AND ("machine learning" OR "artificial intelligence")

**Springer Nature** (Title/abstract): ("relief demand" OR "humanitarian logistics") AND (forecasting OR prediction) AND ("machine learning" OR "artificial intelligence")

**IEEE Xplore** (All metadata): ("relief demand" OR "emergency resource\*" OR "disaster relief") AND (forecast\* OR predict\*) AND ("machine learning" OR "deep learning" OR "artificial intelligence")

**PubMed** (Title/Abstract + MeSH): ("Disasters"\[Mesh\] OR "Relief Work"\[Mesh\] OR "Emergency Medical Services"\[Mesh\]) AND (forecast\*\[tiab\] OR predict\*\[tiab\]) AND ("machine learning"\[tiab\] OR "artificial intelligence"\[tiab\])

