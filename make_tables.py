#!/usr/bin/env python3
"""
make_tables.py -- generates every data table in the manuscript directly from
the master extraction dataset, so that no table can drift from the figures or
from the narrative.

Writes tables/tab_included_studies.tex   (Reviewer 2, Minor 2)
       tables/tab_efficacy.tex           (Reviewer 2, Major 4)
       tables/tab_search_strategy.tex    (Reviewer 2, Major 1)
       tables/tab_method_by_disaster.tex (Reviewer 1, Section 5 comment)
       tables/tab_coding_rules.tex       (Reviewer 2, Major 3)
"""
import csv, json, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB = os.path.join(ROOT, 'tables')
os.makedirs(TAB, exist_ok=True)
S = json.load(open(os.path.join(ROOT, 'data', 'stats.json')))
ROWS = list(csv.DictReader(
    open(os.path.join(ROOT, 'data', 'master_extraction.csv'))))
PRIM = [r for r in ROWS if r['study_type'] == 'Primary']


def esc(s):
    for a, b in (('&', r'\&'), ('%', r'\%'), ('_', r'\_'), ('#', r'\#'),
                 ('$', r'\$')):
        s = s.replace(a, b)
    return s


def fam(r):
    m = []
    for k, lab in (('mf_statistical', 'ST'), ('mf_ml', 'ML'),
                   ('mf_dl', 'DL'), ('mf_knowledge', 'KB'),
                   ('mf_optsim', 'OS'), ('mf_genai', 'GA')):
        if r[k] == '1':
            m.append(lab)
    return ', '.join(m) if m else '--'


SHORT = {
    'Predictive modelling and forecasting': 'Predictive modelling',
    'Disaster preparedness and relief planning': 'Preparedness',
    'Humanitarian logistics and supply chain management': 'Human. SCM',
    'Healthcare and medical service demand': 'Health service demand',
    'Community engagement and social impact': 'Community/social',
    'Methodological or technology review': 'Review',
    'Dynamic and adaptive demand estimation': 'Dynamic estimation',
    'Multi-hazard/General': 'Multi-hazard',
    'Hurricane/Cyclone': 'Hurricane',
    'Biological/Epidemic': 'Biological',
    'Technological/Other': 'Other',
    'Drought/Food insecurity': 'Drought/food',
    'Conflict/Displacement': 'Conflict',
    'Comparative benchmark': 'Comparative',
    'Single-model metric': 'Single-model',
    'Qualitative/none': 'None',
    'Not reported': '--',
    'Not applicable (review)': 'n/a',
    'Operational deployment': 'Operational',
    'Real-data case study': 'Real-data case',
    'Synthetic/illustrative': 'Synthetic',
    'Short-to-long': 'Short--long',
    'Dynamic/real-time': 'Dynamic',
}
sh = lambda v: SHORT.get(v, v)


ABBR = [('International Journal of', 'Int. J.'),
        ('Transportation Research', 'Transp. Res.'),
        ('IEEE Transactions on', 'IEEE Trans.'),
        ('Computers and Electrical Engineering', 'Comput. Electr. Eng.'),
        ('Computers & Industrial Engineering', 'Comput. Ind. Eng.'),
        ('Annals of Operations Research', 'Ann. Oper. Res.'),
        ('Engineering Applications of Artificial Intelligence', 'EAAI'),
        ('Journal of Humanitarian Logistics and Supply Chain Management',
         'JHLSCM'),
        ('Expert Systems with Applications', 'ESWA'),
        ('Socio-Economic Planning Sciences', 'SEPS'),
        ('Reliability Engineering', 'Reliab. Eng.'),
        ('Progress in Disaster Science', 'Prog. Disaster Sci.'),
        ('Information Processing', 'Inf. Process.'),
        ('Online Social Networks and Media', 'OSNEM'),
        ('Journal of the Operational Research Society', 'JORS')]


def outlet(j):
    for a, b in ABBR:
        j = j.replace(a, b)
    if len(j) > 30:
        cut = j[:30].rsplit(' ', 1)[0]
        j = cut + '.' if cut else j[:30]
    return j


# =================================================== 1. all included studies
def t_included():
    L = [r'\begin{landscape}',
         r'\footnotesize',
         r'\begin{longtable}{@{}p{1.0cm}p{3.3cm}p{0.8cm}p{2.3cm}p{3.1cm}'
         r'p{2.6cm}p{2.2cm}p{1.9cm}p{2.3cm}p{2.2cm}@{}}',
         r'\caption{Characteristics of all %d sources included in the review, '
         r'as extracted into the master dataset. Method families are '
         r'multi-label and abbreviated ST (statistical/time series), ML '
         r'(classical machine learning), DL (deep learning/neural), KB '
         r'(knowledge-based: case-based and rule-based reasoning, fuzzy, '
         r'rough and grey systems), OS (optimisation/simulation) and GA '
         r"(generative AI/large language models). ``--'' denotes a variable "
         r'the source does not report. The complete machine-readable file, '
         r'including the coding notes for every row, is '
         r'\texttt{data/master\_extraction.csv}.}'
         % S['N_all'],
         r'\label{tab:included_studies}\\',
         r'\toprule',
         r'\textbf{ID} & \textbf{Source} & \textbf{Year} & '
         r'\textbf{Case-study focus} & \textbf{Outlet} & '
         r'\textbf{Objective} & \textbf{Hazard} & \textbf{Method '
         r'families} & \textbf{Performance evidence} & '
         r'\textbf{Deployment} \\',
         r'\midrule', r'\endfirsthead',
         r'\multicolumn{10}{@{}l}{\footnotesize\itshape '
         r'Table \ref{tab:included_studies} continued from previous page}\\',
         r'\toprule',
         r'\textbf{ID} & \textbf{Source} & \textbf{Year} & '
         r'\textbf{Case-study focus} & \textbf{Outlet} & '
         r'\textbf{Objective} & \textbf{Hazard} & \textbf{Method '
         r'families} & \textbf{Performance evidence} & '
         r'\textbf{Deployment} \\',
         r'\midrule', r'\endhead',
         r'\midrule\multicolumn{10}{r@{}}{\footnotesize\itshape '
         r'continued on next page}\\', r'\endfoot',
         r'\bottomrule', r'\endlastfoot']
    for r in ROWS:
        src = '%s \\cite{%s}' % (esc(r['first_author']), r['citekey'])
        if r['study_type'] == 'Review':
            src += r'$^{\dagger}$'
        L.append(' & '.join([
            r['study_id'], src, r['year'],
            esc(sh(r['focus_country'])), esc(outlet(r['journal'])),
            esc(sh(r['objective'])), esc(sh(r['disaster_type'])),
            fam(r), esc(sh(r['performance_evidence'])),
            esc(sh(r['deployment_status']))]) + r' \\')
    L += [r'\end{longtable}',
          r'\footnotesize $^{\dagger}$ review or synthesis article; excluded '
          r'from the denominator $N_{\mathrm{prim}}$ used for method, hazard, '
          r'horizon and performance variables.',
          r'\normalsize', r'\end{landscape}']
    open(os.path.join(TAB, 'tab_included_studies.tex'), 'w').write(
        '\n'.join(L) + '\n')
    return len(ROWS)


# ================================================= 2. efficacy evidence table
def t_efficacy():
    ev = list(csv.DictReader(
        open(os.path.join(ROOT, 'data', 'efficacy_evidence.csv'),
             encoding='utf-8')))
    keep = [e for e in ev
            if e['evidence_grade'] in ('A-fulltext', 'B-abstract')
            and 'Not retrievable' not in e['reported_result']
            and e['reported_result'] not in ('', 'None reported')]
    L = [r'\begin{table}[htbp!]', r'\centering', r'\scriptsize',
         r'\caption{Comparative performance evidence that could be extracted '
         r'from the included primary studies. Only the studies listed here '
         r'report a quantitative predictive-performance result that we were '
         r'able to verify against the published record; for the remaining '
         r'primary studies no extractable figure was found. The table is '
         r'therefore evidence of how thin the comparative-efficacy base '
         r'currently is, and is the basis for the distinction the review '
         r'draws between publication prevalence and demonstrated efficacy.}',
         r'\label{tab:efficacy}',
         r'\begin{tabular}{@{}p{2.3cm}p{3.5cm}p{2.7cm}p{5.4cm}@{}}',
         r'\toprule',
         r'\textbf{Study} & \textbf{Models compared} & '
         r'\textbf{Case and metric} & \textbf{Reported result} \\',
         r'\midrule']
    for e in keep:
        res = e['reported_result']
        res = res[:330] + ('\\ldots' if len(res) > 330 else '')
        L.append(' & '.join([
            '%s \\cite{%s}' % (esc(e['first_author']), e['citekey']),
            esc(e['models_compared'][:150]),
            esc((e['dataset_case'][:90] + '. ' + e['metric'])[:130]),
            esc(res)]) + r' \\[2pt]')
    L += [r'\bottomrule', r'\end{tabular}', r'\normalsize', r'\end{table}']
    open(os.path.join(TAB, 'tab_efficacy.tex'), 'w').write('\n'.join(L) + '\n')
    return len(keep)


# ================================================== 3. search strategy table
SEARCH = [
    ('Scopus', 'TITLE-ABS-KEY', r'''( "relief demand" OR "humanitarian
 demand" OR "emergency material*" OR "relief suppl*" OR "emergency suppl*" OR
 "humanitarian need*" ) AND ( forecast* OR predict* OR estimat* ) AND (
 "artificial intelligence" OR "machine learning" OR "deep learning" OR "neural
 network*" OR "large language model*" OR "data-driven" OR "time series" )''',
     '1 Jan 1990 -- 22 Aug 2026', '388'),
    ('Web of Science', 'TS=', r'''( "relief demand" OR "humanitarian logistic*"
 OR "emergency supply chain" OR "disaster relief" ) AND ( forecast* OR
 predict* ) AND ( "artificial intelligence" OR "machine learning" OR "deep
 learning" OR "neural network*" )''', '1 Jan 1990 -- 22 Aug 2026', '271'),
    ('ScienceDirect', 'Title, abstract, keywords',
     r'''("relief demand" OR "emergency supplies") AND (forecasting OR
 prediction) AND ("machine learning" OR "artificial intelligence")''',
     '1 Jan 1990 -- 22 Aug 2026', '214'),
    ('Springer Nature', 'Title/abstract',
     r'''("relief demand" OR "humanitarian logistics") AND (forecasting OR
 prediction) AND ("machine learning" OR "artificial intelligence")''',
     '1 Jan 1990 -- 22 Aug 2026', '118'),
    ('IEEE Xplore', 'All metadata',
     r'''("relief demand" OR "emergency resource*" OR "disaster relief") AND
 (forecast* OR predict*) AND ("machine learning" OR "deep learning" OR
 "artificial intelligence")''', '1 Jan 1990 -- 22 Aug 2026', '84'),
    ('PubMed', 'Title/Abstract + MeSH',
     r'''("Disasters"[Mesh] OR "Relief Work"[Mesh] OR "Emergency Medical
 Services"[Mesh]) AND (forecast*[tiab] OR predict*[tiab]) AND ("machine
 learning"[tiab] OR "artificial intelligence"[tiab])''',
     '1 Jan 1990 -- 22 Aug 2026', '34'),
]


def t_search():
    L = [r'\begin{table}[htbp!]', r'\centering', r'\scriptsize',
         r'\caption{Database-specific search strategy. All six databases were '
         r'searched from inception to the final query date of 22 August 2026. '
         r'Boolean operators are reproduced exactly as executed; an asterisk '
         r'denotes right-hand truncation. The strategy was additionally '
         r'supplemented by backward and forward citation chasing of every '
         r'included source ($n = 46$ additional records).}',
         r'\label{tab:search_strategy}',
         r'\begin{tabular}{@{}p{2.1cm}p{2.4cm}p{7.4cm}p{2.4cm}r@{}}',
         r'\toprule',
         r'\textbf{Database} & \textbf{Field(s) searched} & '
         r'\textbf{Search string as executed} & \textbf{Search window} & '
         r'\textbf{Records} \\', r'\midrule']
    for db, fld, q, win, n in SEARCH:
        q = ' '.join(q.split())
        L.append(' & '.join([db, fld, r'\texttt{\scriptsize %s}' % esc(q), win, n])
                 + r' \\[3pt]')
    L += [r'\midrule',
          r'\multicolumn{4}{@{}l}{\textbf{Total records identified through '
          r'database searching}} & \textbf{1,109} \\',
          r'\multicolumn{4}{@{}l}{Additional records from citation chasing} '
          r'& 46 \\',
          r'\bottomrule', r'\end{tabular}', r'\normalsize', r'\end{table}']
    open(os.path.join(TAB, 'tab_search_strategy.tex'), 'w').write(
        '\n'.join(L) + '\n')


# ============================================ 4. method x disaster crosstab
def t_method_by_disaster():
    MF = [('mf_statistical', 'Statistical / time series'),
          ('mf_ml', 'Classical machine learning'),
          ('mf_dl', 'Deep learning / neural'),
          ('mf_knowledge', 'Knowledge-based (CBR, RBR, fuzzy, grey)'),
          ('mf_optsim', 'Optimisation / simulation'),
          ('mf_genai', 'Generative AI / LLM')]
    dis = [d for d, _ in sorted(S['disaster']['items'].items(),
                                key=lambda kv: -kv[1]['n'])]
    L = [r'\begin{table}[htbp!]', r'\centering', r'\footnotesize',
         r'\caption{Cross-tabulation of method family against dominant hazard '
         r'for the %d primary studies with a coded hazard. Method family is '
         r'multi-label, so a hybrid study contributes to more than one row '
         r'and the row total exceeds the number of studies; the final row '
         r'gives the number of distinct studies per hazard.}'
         % S['disaster']['denominator'],
         r'\label{tab:method_by_disaster}',
         r'\begin{tabular}{@{}l' + 'r' * len(dis) + r'r@{}}', r'\toprule',
         'Method family & ' + ' & '.join(
             r'\rotatebox{60}{%s}' % esc(sh(d)) for d in dis)
         + r' & \textbf{Total} \\', r'\midrule']
    for k, lab in MF:
        cells = []
        for d in dis:
            n = sum(1 for r in PRIM
                    if r['disaster_type'] == d and r[k] == '1')
            cells.append(str(n) if n else '--')
        tot = sum(1 for r in PRIM if r[k] == '1'
                  and r['disaster_type'] in dis)
        L.append(esc(lab) + ' & ' + ' & '.join(cells)
                 + r' & \textbf{%d} \\' % tot)
    L.append(r'\midrule')
    tots = [sum(1 for r in PRIM if r['disaster_type'] == d) for d in dis]
    L.append(r'\textbf{Distinct studies} & '
             + ' & '.join(r'\textbf{%d}' % t for t in tots)
             + r' & \textbf{%d} \\' % sum(tots))
    L += [r'\bottomrule', r'\end{tabular}', r'\normalsize', r'\end{table}']
    open(os.path.join(TAB, 'tab_method_by_disaster.tex'), 'w').write(
        '\n'.join(L) + '\n')


# ================================================= 5. coding-rules table
RULES = [
    ('R1', 'Method family (multi-label)',
     'Six binary flags set by matching the reported method string against '
     'fixed keyword lists: statistical/time series; classical machine '
     'learning; deep learning/neural; knowledge-based (case- and rule-based '
     'reasoning, fuzzy, rough and grey systems); optimisation/simulation; '
     'generative AI/LLM. A study may score on several flags.',
     'Multi-label. Percentages use $N_{\\mathrm{prim}}$ and sum to more '
     'than 100\\%.'),
    ('R2', 'Functional form',
     '\\emph{Linear} if only statistical families are present; '
     '\\emph{Combined} if a statistical family co-occurs with a machine-'
     'learning, deep-learning or generative family; \\emph{Non-linear} '
     'otherwise.',
     'Mutually exclusive. Studies with no identifiable method are excluded '
     'from the denominator.'),
    ('R3', 'Uncertainty represented',
     'Set to 1 where the reported method explicitly represents uncertainty: '
     'probabilistic or Bayesian formulations, stochastic programming, '
     'fuzzy, rough or grey systems, interval, scenario-based, robust or '
     'Monte-Carlo treatments.',
     'Binary; denominator $N_{\\mathrm{prim}}$.'),
    ('R4', 'Sustainability or equity framing',
     'Set to 1 only where an environmental, social-equity or resilience '
     'objective is explicitly stated in the study\'s objective, method or '
     'outlet scope. A deliberately strict rule.',
     'Binary; denominator $N_{\\mathrm{prim}}$. Deliberately conservative; '
     'see Section~\\ref{sec:limitations}.'),
    ('R5', 'Performance evidence',
     '\\emph{Comparative benchmark} where two or more competing models are '
     'compared on a common dataset with a reported error or accuracy '
     'metric; \\emph{Single-model metric} where one model and a quantitative '
     'metric are reported; \\emph{Qualitative/none} where the source makes '
     'no quantitative performance claim; \\emph{Not reported} where no '
     'figure could be extracted from the retrievable record.',
     "Mutually exclusive. ``Not reported'' is a statement about the "
     'retrievable record, not about the method.'),
    ('R6', 'Deployment status',
     '\\emph{Operational deployment} only where a named responding '
     'organisation is documented as using the system in practice; '
     '\\emph{Real-data case study} where a named real event or region is '
     'analysed; \\emph{Synthetic/illustrative} where only a numerical '
     'example is given.',
     'Mutually exclusive; conservative by construction.'),
]


def t_rules():
    L = [r'\begin{table}[htbp!]', r'\centering', r'\footnotesize',
         r'\caption{Coding rules for the derived extraction variables. Each '
         r'rule is implemented verbatim in \texttt{code/build\_wave1.py} and '
         r'applied identically to every source, so that any reader can '
         r'reproduce the coding from the reported method. The fourth column '
         r'states whether the variable is mutually exclusive or multi-label '
         r'and which denominator it uses.}',
         r'\label{tab:coding_rules}',
         r'\begin{tabular}{@{}p{0.7cm}p{3.0cm}p{8.0cm}p{3.6cm}@{}}',
         r'\toprule',
         r'\textbf{Rule} & \textbf{Variable} & \textbf{Definition as '
         r'implemented} & \textbf{Exclusivity and denominator} \\',
         r'\midrule']
    for rid, var, defn, excl in RULES:
        L.append(' & '.join([rid, var, defn, excl]) + r' \\[3pt]')
    L += [r'\bottomrule', r'\end{tabular}', r'\normalsize', r'\end{table}']
    open(os.path.join(TAB, 'tab_coding_rules.tex'), 'w').write(
        '\n'.join(L) + '\n')


if __name__ == '__main__':
    n1 = t_included()
    n2 = t_efficacy()
    t_search()
    t_method_by_disaster()
    t_rules()
    print('tab_included_studies.tex   %d rows' % n1)
    print('tab_efficacy.tex           %d studies with extractable results' % n2)
    print('tab_search_strategy.tex    6 databases')
    print('tab_method_by_disaster.tex')
    print('tab_coding_rules.tex       6 rules')
