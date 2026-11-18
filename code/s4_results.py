#!/usr/bin/env python3
"""s4_results.py -- writes the results section of Supplementary S4 (the LLM
comparison) from the scored outputs, so the supplement and the data agree.
Replaces everything from the heading '## 6. Results' to the end of the file."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def macros(path):
    return dict(re.findall(r'\\newcommand\{\\(\w+)\}\{([^}]*)\}', open(path, encoding='utf-8').read()))
M = macros(os.path.join(ROOT, 'data', 'llm_comparison', 'llm_macros.tex'))
M.update(macros(os.path.join(ROOT, 'stats_macros.tex')))
tab = open(os.path.join(ROOT, 'tables', 'tab_llm_armA.tex'), encoding='utf-8').read()
rows = []
for line in tab.split('\n'):
    if '&' in line and '\\\\' in line:
        cells = [c.strip() for c in line.replace('\\\\', '').split('&')]
        cells = [re.sub(r'\\multicolumn\{\d\}\{\w\}\{([^}]*)\}', r'\1', c) for c in cells]
        cells = [re.sub(r'\\textbf\{([^}]*)\}', r'\1', c).replace('\\%', '%') for c in cells]
        rows.append(cells + [''] * (5 - len(cells)))
md = ['| ' + ' | '.join(rows[0]) + ' |', '|:' + '-' * 60 + '|' + '-' * 12 + ':|' + '-' * 12 + ':|' + '-' * 12 + ':|' + '-' * 14 + ':|']
md += ['| ' + ' | '.join(r[:5]) + ' |' for r in rows[1:]]
txt = """## 6. Results

The model was Claude Opus 5.5 (Anthropic), accessed on 17 November 2026 through an agent session whose sampling temperature is not user-controllable. Each run used a fresh session that received only the prompt and had no access to the released dataset, the manuscript or any search or file tool. Arm A was run three times; Arms B and C were not run, because they require the complete record export and the abstracts as inputs. Arm A is scored against the {Nall} sources included in the review.

**Arm A.** Across three runs the model listed between {llmListedMin} and {llmListedMax} studies, of which {llmMatchedMin} to {llmMatchedMax} were among the included sources, a recall of {llmRecallMin} to {llmRecallMax}%. No run recovered any of the {llmNrecent} included sources published from 2024 onwards ({llmRecentPct}% of the corpus), and the most recent included source recovered dates from {llmLatestYear}. The matched sources overlapped only partly between runs (mean Jaccard index {llmJaccard}). The model described a quarter or more of its listed studies as benchmarking against a competing model, and about one in six as operationally deployed, against {pctcomparative}% and {pctoperational}% of the primary studies charted in the review. A random sample of {llmExistN} of the {llmUnmatched} listed studies that are not in the corpus (seed 20261117) was checked against bibliographic records, and all {llmExistYes} exist; they are released as candidate records for any future update of the review.

""".format(**M) + '\n'.join(md) + """

**Interpretation.** A model asked to stand in for the search returns a list that is not reproducible between runs, misses most of the literature and all of its most recent part, and describes its listed studies as more often benchmarked and deployed than the charted corpus. Fabricated references did not occur in the sample checked. None of these weaknesses is visible in the model's output itself; each was revealed only by comparison with the protocol-driven review, which is the sense in which PRISMA-ScR and LLM assistance are complements.
"""
p = os.path.join(ROOT, 'supplementary', 'S4_llm_prompts.md')
s = open(p, encoding='utf-8').read()
s = s.split('\n## 6. Results')[0].rstrip() + '\n\n' + txt
open(p, 'w', encoding='utf-8').write(s)
print('S4 results section written')
