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
import csv, json, os, re, collections

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


# R2 (Reviewer 2, comment 2): outlet titles are printed in full and allowed to
# wrap inside the column. The R1 rule abbreviated a few words and then cut the
# string at 30 characters, which produced fragments such as "Transp. Res. Part
# E:." and "Journal of the Interna...". Full titles are taken from
# data/outlet_titles.csv, a reviewed mapping from the outlet string in the
# master dataset to the outlet's full published title.
OUTLETS = {r['journal_in_dataset']: r['full_title'] for r in csv.DictReader(
    open(os.path.join(ROOT, 'data', 'outlet_titles.csv'), encoding='utf-8'))}


def outlet(j):
    full = OUTLETS.get(j, j).strip()
    return full.rstrip(' .:;,')


# =================================================== 1. all included studies
def t_included():
    L = [r'\begin{landscape}',
         r'\footnotesize',
         r'\begin{longtable}{@{}L{0.9cm}L{2.9cm}L{0.8cm}L{2.1cm}L{3.1cm}'
         r'L{2.4cm}L{2.0cm}L{1.8cm}L{2.1cm}L{2.0cm}@{}}',
         r'\caption{Included sources}',
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
          r'\normalsize', r'\end{landscape}']
    open(os.path.join(TAB, 'tab_included_studies.tex'), 'w').write(
        '\n'.join(L) + '\n')
    return len(ROWS)


# ================================================= 2. efficacy evidence table
def t_efficacy():
    ev = list(csv.DictReader(
        open(os.path.join(ROOT, 'data', 'efficacy_evidence.csv'),
             encoding='utf-8')))
    # R2: only studies whose comparative or single-model result could be
    # verified (studies reporting no quantitative metric are not listed)
    keep = [e for e in ev
            if e['evidence_grade'] in ('A-fulltext', 'B-abstract')
            and e['reports_metric'] == 'Yes'
            and 'Not retrievable' not in e['reported_result']
            and e['reported_result'] not in ('', 'None reported')]
    # R2: a longtable so the table can break across pages and never runs
    # into the page foot
    hdr = (r'\textbf{Study} & \textbf{Models compared} & '
           r'\textbf{Case and metric} & \textbf{Reported result} \\')
    L = [r'\begingroup\scriptsize',
         r'\begin{longtable}{@{}L{2.0cm}L{3.6cm}L{3.6cm}L{5.4cm}@{}}',
         r'\caption{Extracted performance evidence}\label{tab:efficacy} \\',
         r'\toprule', hdr, r'\midrule', r'\endfirsthead',
         r'\toprule', hdr, r'\midrule', r'\endhead',
         r'\bottomrule', r'\endlastfoot']
    for e in keep:
        res = e['reported_result'].replace(' \u2014 ', '; ')
        # R2: no character-count truncation (Reviewer 2's point applies to
        # every generated table); '~' means 'approximately' in the source
        def tl(s):
            s = esc(s.replace('~', 'approx. '))
            s = re.sub(r'"([^"]*)"', r"``\1''", s)
            s = re.sub(r'\bR2\b', r'$R^2$', s)
            return s.replace('(Appendix B)', "(source's Appendix B)")
        L.append(' & '.join([
            '%s \\cite{%s}' % (esc(e['first_author']), e['citekey']),
            tl(e['models_compared']),
            tl(e['dataset_case'].rstrip('. ') + '. ' + e['metric']),
            tl(res)]) + r' \\[2pt]')
    L += [r'\end{longtable}', r'\endgroup']
    open(os.path.join(TAB, 'tab_efficacy.tex'), 'w').write('\n'.join(L) + '\n')
    # counts quoted in Section 7 (generated, so text and table cannot diverge)
    W = 'zero one two three four five six seven eight nine ten eleven twelve'.split()
    wd = lambda n: W[n] if n < len(W) else str(n)
    pe = {r['citekey']: r['performance_evidence'] for r in ROWS}
    kk = {e['citekey'] for e in keep}
    comp = [k for k, v in pe.items() if v == 'Comparative benchmark']
    sing = [k for k, v in pe.items() if v == 'Single-model metric']
    mac = {'nTabComp': sum(1 for k in comp if k in kk),
           'nTabSingle': sum(1 for k in sing if k in kk)}
    mac['nCompNoFig'] = len(comp) - mac['nTabComp']
    mac['nSingleNoFig'] = len(sing) - mac['nTabSingle']
    mac['nsingleWord'] = len(sing)
    mac['noperationalWord'] = sum(1 for r in ROWS if r['study_type'] == 'Primary' and r['deployment_status'] == 'Operational deployment')
    with open(os.path.join(TAB, 'efficacy_macros.tex'), 'w') as fh:
        fh.write('% generated by code/make_tables.py\n')
        for k, v in mac.items():
            fh.write('\\newcommand{\\%s}{%s}\n' % (k, wd(v)))
    return len(keep)


# ============================ charting basis of sources charted after R1
def charting_basis():
    """Records, for every source whose coding note says it was charted from
    its title, the text actually read: full text, abstract or title and
    bibliographic record. Writes data/charting_basis_R2.csv and macros."""
    ft = {r['citekey'] for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'fulltext_verification_R2.csv')))}
    ev = {r['citekey']: r['evidence_grade'] for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'efficacy_evidence.csv')))}
    dc = {r['citekey']: r['evidence_read'] for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'deployment_cases.csv')))}
    out, n = [], collections.Counter()
    for r in ROWS:
        if not (r['coding_note'].startswith('Title-verified only') or r['coding_note'].startswith('First charted from the title')):
            continue
        k = r['citekey']
        if k in ft or ev.get(k) == 'A-fulltext' or dc.get(k) == 'Full text':
            b = 'Full text'
        elif ev.get(k) == 'B-abstract' or dc.get(k) == 'Abstract':
            b = 'Abstract'
        else:
            b = 'Title and bibliographic record'
        n[b] += 1
        out.append((r['study_id'], k, b))
    # record the basis in the released dataset's coding note as well
    mp = os.path.join(ROOT, 'data', 'master_extraction.csv')
    rows = list(csv.reader(open(mp, encoding='utf-8')))
    hdr = rows[0]; ci, ki = hdr.index('coding_note'), hdr.index('citekey')
    bk = {k: b for _, k, b in out}
    for r in rows[1:]:
        if r[ki] in bk and r[ci].startswith('Title-verified only'):
            r[ci] = 'First charted from the title; now charted from: %s' % bk[r[ki]].lower() + r[ci][len('Title-verified only'):]
    with open(mp, 'w', newline='', encoding='utf-8') as fh:
        csv.writer(fh).writerows(rows)
    with open(os.path.join(ROOT, 'data', 'charting_basis_R2.csv'), 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['study_id', 'citekey', 'text_charted']); w.writerows(out)
    W = 'zero one two three four five six seven eight nine'.split()
    wd = lambda v: W[v] if v < 10 else str(v)
    with open(os.path.join(TAB, 'charting_macros.tex'), 'w') as fh:
        fh.write('% generated by code/make_tables.py\n')
        fh.write('\\newcommand{\\nChartLate}{%s}\n' % wd(len(out)))
        fh.write('\\newcommand{\\nChartFull}{%s}\n' % wd(n['Full text']))
        fh.write('\\newcommand{\\nChartAbstract}{%s}\n' % wd(n['Abstract']))
        fh.write('\\newcommand{\\nChartTitle}{%s}\n' % wd(n['Title and bibliographic record']))


# ================================================== 3. search strategy table
# R1 strings, kept verbatim so the R2 harmonisation audit can compare them
SEARCH_R1 = [
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
# end SEARCH_R1
SEARCH = SEARCH_R1


def t_search():
    """R2 (Reviewer 3, comment 1): one harmonised strategy. The three concept
    blocks are identical in every database and are printed once; each row
    gives only the database's field tag and its record count from the
    harmonised search (data/search_counts_R2.csv). Counts not yet entered are
    printed as a visible placeholder so the table cannot be mistaken for a
    final one. The R1 strings and the coverage audit are in Supplementary S5."""
    J = json.load(open(os.path.join(ROOT, 'data', 'search_strings_R2.json')))
    cnt = {r['database']: r for r in csv.DictReader(open(os.path.join(
        ROOT, 'data', 'search_counts_R2.csv'), encoding='utf-8'))}
    blk = lambda ts: ' OR '.join(('"%s"' % x) if (' ' in x or '-' in x) else x
                                  for x in ts)
    L = [r'\begin{table}[htbp!]', r'\centering', r'\scriptsize',
         r'\caption{Harmonised search strategy}',
         r'\label{tab:search_strategy}',
         r'\begin{tabular}{@{}L{3.0cm}L{9.2cm}r@{}}', r'\toprule',
         r'\multicolumn{3}{@{}l}{\textbf{Concept blocks (identical in every '
         r'database; blocks joined by AND)}} \\', r'\midrule']
    for k, lab in (('A', 'A. Relief-demand object'),
                   ('B', 'B. Forecasting operation'),
                   ('C', 'C. Computational method')):
        L.append(r'%s & \multicolumn{2}{L{10.8cm}@{}}{\texttt{%s}} \\[2pt]'
                 % (lab, esc(blk(J['blocks'][k]))))
    L.append(r'PubMed only & \multicolumn{2}{L{10.8cm}@{}}{Block A is '
             r'additionally OR-ed with \texttt{%s}} \\[2pt]'
             % esc(' OR '.join(J['blocks']['PubMed_MeSH'])))
    L += [r'\midrule', r'\textbf{Database} & \multicolumn{2}{l@{}}{\textbf{Field '
          r'tag applied to each block}} \\', r'\midrule']
    for s in J['strings']:
        L.append(r'%s & \multicolumn{2}{L{10.8cm}@{}}{%s} \\' % (
            esc(s['database']), esc(s['fields'])))
    L += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
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
         r'\caption{Method family and hazard counts}',
         r'\setlength{\tabcolsep}{3.5pt}',
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
    L = [r'\begin{table}[htbp!]', r'\centering', r'\scriptsize', r'\tiny',
         r'\caption{Coding rules}',
         r'\label{tab:coding_rules}',
         r'\begin{tabular}{@{}p{0.6cm}p{2.6cm}p{7.6cm}p{3.4cm}@{}}',
         r'\toprule',
         r'\textbf{Rule} & \textbf{Variable} & \textbf{Definition as '
         r'implemented} & \textbf{Exclusivity and denominator} \\',
         r'\midrule']
    for rid, var, defn, excl in RULES:
        L.append(' & '.join([rid, var, defn, excl]) + r' \\[3pt]')
    L += [r'\bottomrule', r'\end{tabular}', r'\normalsize', r'\end{table}']
    open(os.path.join(TAB, 'tab_coding_rules.tex'), 'w').write(
        '\n'.join(L) + '\n')


# ================================== 6. field-validated cases (R2, Reviewer 1)
def t_deployment():
    """Two tables generated from data/deployment_cases.csv: the three
    operationally deployed studies, and the barriers each reports."""
    D = list(csv.DictReader(open(os.path.join(ROOT, 'data',
                                              'deployment_cases.csv'),
                                 encoding='utf-8')))
    cell = lambda s: esc(s).replace('[TBC: full text]',
                                    r'\textbf{[TBC: full text]}')
    L = [r'\begin{table}[htbp!]', r'\centering', r'\scriptsize',
         r'\caption{Field-validated studies}',
         r'\label{tab:deployment_cases}',
         r'\begin{tabular}{@{}L{2.1cm}L{2.4cm}L{4.0cm}L{4.0cm}L{1.5cm}@{}}',
         r'\toprule', r'\textbf{Study} & \textbf{Responding organisation} & '
         r'\textbf{Documented use} & \textbf{Forecast target and model} & '
         r'\textbf{Text charted} \\', r'\midrule']
    for d in D:
        L.append(' & '.join([r'%s \cite{%s}' % (cell(d['study']), d['citekey']),
                             cell(d['organisation']), cell(d['use']),
                             cell(d['target_model']), cell(d['evidence_read'])])
                 + r' \\[3pt]')
    L += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
    open(os.path.join(TAB, 'tab_deployment_cases.tex'), 'w').write(
        '\n'.join(L) + '\n')
    rows = [('Data availability and curation', 'data'),
            ('Infrastructure and computing', 'infrastructure'),
            ('Governance, trust and the action link', 'governance'),
            ('Model quality and uncertainty', 'model_quality'),
            ('Organisational capability and ethics', 'organisational'),
            ('Reported outcomes of deployment', 'outcomes')]
    L = [r'\begin{table}[htbp!]', r'\centering', r'\scriptsize',
         r'\caption{Barriers in field-validated studies}',
         r'\label{tab:deployment_barriers}',
         r'\begin{tabular}{@{}L{2.3cm}' + 'L{3.95cm}' * len(D) + '@{}}',
         r'\toprule', r'\textbf{Barrier} & ' + ' & '.join(
             r'\textbf{%s} \cite{%s}' % (cell(d['study']), d['citekey'])
             for d in D) + r' \\', r'\midrule']
    for lab, k in rows:
        L.append(lab + ' & ' + ' & '.join(cell(d[k]) for d in D) + r' \\[3pt]')
    L += [r'\midrule', r'Location in source & ' + ' & '.join(
        cell(d['locations']) for d in D) + r' \\',
          r'\bottomrule', r'\end{tabular}', r'\end{table}']
    open(os.path.join(TAB, 'tab_deployment_barriers.tex'), 'w').write(
        '\n'.join(L) + '\n')


if __name__ == '__main__':
    t_deployment()
    n1 = t_included()
    n2 = t_efficacy()
    charting_basis()
    t_search()
    t_method_by_disaster()
    t_rules()
    print('tab_included_studies.tex   %d rows' % n1)
    print('tab_efficacy.tex           %d studies with extractable results' % n2)
    print('tab_search_strategy.tex    6 databases')
    print('tab_method_by_disaster.tex')
    print('tab_coding_rules.tex       6 rules')
