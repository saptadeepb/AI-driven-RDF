#!/usr/bin/env bash
# Rebuilds the dataset, every statistic, figure and table of the review from
# the charted rows. Requires Python 3 with pandas, numpy, matplotlib and openpyxl.
set -e
cd "$(dirname "$0")"
echo "1/5  master extraction dataset";  python3 code/merge_master.py > /dev/null
echo "2/5  statistics";                 python3 code/compute_stats.py > /dev/null; python3 code/period_stats.py > /dev/null
echo "3/5  search audit, worked examples and LLM comparison"
python3 code/search_harmonisation.py > /dev/null
python3 code/americanize.py supplementary/S5_harmonised_search.md > /dev/null
python3 code/practitioner_examples.py > /dev/null
python3 code/llm_compare.py > /dev/null
echo "4/5  figures";                    python3 code/make_figures.py > /dev/null
echo "5/5  tables and Excel export";    python3 code/make_tables.py > /dev/null
python3 code/americanize.py tables/tab_*.tex > /dev/null
python3 code/sanitise_tex.py > /dev/null
python3 code/make_xlsx.py > /dev/null
echo "done: data/master_extraction.csv, stats_macros.tex, figures/, tables/"
