#!/usr/bin/env python3
"""
llm_compare.py -- R2, Reviewer 3 comment 4.

Scores the pre-specified LLM comparison (Supplementary S4) against the
protocol-driven review. Deterministic given the saved raw model outputs.

Inputs
  data/master_extraction.csv                       human reference standard
  references.bib                                   titles/DOIs of the corpus
  data/llm_comparison/armA_run{1,2,3}.json         Arm A raw outputs
  data/llm_comparison/armA_existence.csv           existence check of every
                                                   listed study (optional)
  data/llm_comparison/armC_run{1,2,3}.json         Arm C raw outputs (optional)
Outputs
  data/llm_comparison/armA_matches.csv
  data/llm_comparison/results.json
  data/llm_comparison/llm_macros.tex               macros quoted in the paper

Usage: python3 code/llm_compare.py [--selftest]
"""
import csv, json, os, re, sys, itertools, random
from difflib import SequenceMatcher

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LD = os.path.join(ROOT, 'data', 'llm_comparison')


def norm(s):
    s = re.sub(r'\\[a-zA-Z]+\{?|[{}]', '', s or '')
    s = s.lower()
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return ' '.join(s.split())


def tokset_sim(a, b):
    ta, tb = set(norm(a).split()), set(norm(b).split())
    if not ta or not tb:
        return 0.0
    inter = ' '.join(sorted(ta & tb))
    sa = ' '.join(sorted(ta - tb))
    sb = ' '.join(sorted(tb - ta))
    c1 = (inter + ' ' + sa).strip()
    c2 = (inter + ' ' + sb).strip()
    return max(SequenceMatcher(None, inter, c1).ratio(),
               SequenceMatcher(None, inter, c2).ratio(),
               SequenceMatcher(None, c1, c2).ratio())


def corpus():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'data',
                                                 'master_extraction.csv'))))
    bib = open(os.path.join(ROOT, 'references.bib'), encoding='utf-8').read()
    out = []
    for r in rows:
        m = re.search(r'@\w+\{' + re.escape(r['citekey']) + r',(.*?)\n\}', bib,
                      re.S)
        e = m.group(1) if m else ''
        t = re.search(r'\n\s*title\s*=\s*\{(.*)\},?\s*\n', e)
        d = re.search(r'\n\s*doi\s*=\s*\{(.*)\},?\s*\n', e)
        out.append(dict(r, title=t.group(1) if t else '',
                        doi=(d.group(1).lower().strip() if d else '')))
    return out


def kappa(a, b):
    labs = sorted(set(a) | set(b))
    n = len(a)
    if n == 0:
        return float('nan')
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labs)
    return float('nan') if pe == 1 else (po - pe) / (1 - pe)


def fleiss(table):
    """table: list of per-item lists of labels from m raters"""
    if not table:
        return float('nan')
    m = len(table[0])
    labs = sorted({l for row in table for l in row})
    N = len(table)
    P = []
    pj = {l: 0 for l in labs}
    for row in table:
        c = {l: row.count(l) for l in labs}
        for l in labs:
            pj[l] += c[l]
        P.append((sum(v * v for v in c.values()) - m) / (m * (m - 1)))
    Pbar = sum(P) / N
    pe = sum((v / (N * m)) ** 2 for v in pj.values())
    return float('nan') if pe == 1 else (Pbar - pe) / (1 - pe)


# ------------------------------------------------------------------ Arm A
def score_armA(C, runs):
    global ADJ
    ADJ = {}
    ap = os.path.join(LD, 'armA_adjudication.csv')
    if os.path.exists(ap):
        for r in csv.DictReader(open(ap, encoding='utf-8')):
            ADJ[(r['listed_title_normalised'], r['candidate_study_id'])] = \
                r['same_paper']
    res, matches, matched_sets = {}, [], []
    exist = {}
    ep = os.path.join(LD, 'armA_existence.csv')
    if os.path.exists(ep):
        for r in csv.DictReader(open(ep, encoding='utf-8')):
            exist[(r['run'], r['item'])] = r['exists']
    for run, data in runs.items():
        studies = data.get('studies', [])
        hit = set()
        n_exist_known = n_exist_yes = 0
        for i, s in enumerate(studies):
            title = s.get('title', '')
            doi = (s.get('doi') or '').lower().strip()
            best, bsim = None, 0.0
            for c in C:
                if doi and doi != 'unknown' and doi == c['doi']:
                    best, bsim = c, 1.0
                    break
                sim = tokset_sim(title, c['title'])
                if sim > bsim:
                    best, bsim = c, sim
            # Every candidate with similarity >= 0.70 is decided by the manual
            # adjudication log (token-set similarity alone accepted false
            # matches between different papers on similar topics).
            status = 'no_match'
            if bsim >= 0.70:
                dec = ADJ.get((norm(title), best['study_id']))
                if dec is None:
                    raise SystemExit('unadjudicated candidate: %r -> %s'
                                     % (title, best['study_id']))
                status = 'match' if dec == 'yes' else 'rejected_candidate'
            if status == 'match':
                hit.add(best['study_id'])
            ex = exist.get((run, str(i)), '')
            if status == 'match':
                ex = 'yes'
            if ex in ('yes', 'no'):
                n_exist_known += 1
                n_exist_yes += ex == 'yes'
            matches.append(dict(run=run, item=i, listed_title=title,
                                listed_year=s.get('year', ''),
                                best_match=best['study_id'] if best else '',
                                best_title=best['title'] if best else '',
                                similarity='%.3f' % bsim, status=status,
                                exists=ex))
        n = len(studies)
        # recall split by publication year (not by search wave)
        w1 = sum(1 for c in C if int(c['year']) < 2024)
        w2 = sum(1 for c in C if int(c['year']) >= 2024)
        hw1 = sum(1 for c in C if c['study_id'] in hit and int(c['year']) < 2024)
        hw2 = sum(1 for c in C if c['study_id'] in hit and int(c['year']) >= 2024)
        years = [int(c['year']) for c in C if c['study_id'] in hit]
        res[run] = dict(
            listed=n, matched=len(hit),
            precision=len(hit) / n if n else float('nan'),
            recall=len(hit) / len(C),
            recall_wave1=hw1 / w1, recall_wave2=hw2 / w2,
            latest_year_recovered=max(years) if years else None,
            existence_checked=n_exist_known,
            existence_rate=(n_exist_yes / n_exist_known
                            if n_exist_known else None),
            rejected_candidates=sum(
                1 for m in matches
                if m['run'] == run and m['status'] == 'rejected_candidate'))
        matched_sets.append(hit)
        yes = lambda k: sum(1 for s in studies
                            if str(s.get(k, '')).strip().lower() == 'yes')
        fams = lambda f: sum(1 for s in studies
                             if f in [x.lower() for x in
                                      (s.get('method_families') or [])])
        res[run].update(
            share_comparative_yes=yes('comparative_benchmark') / n if n else None,
            share_operational_yes=yes('operational_deployment') / n if n else None,
            share_knowledge_based=fams('knowledge_based') / n if n else None,
            share_generative_ai=fams('generative_ai') / n if n else None)
    sp = os.path.join(LD, 'armA_existence_sample_result.csv')
    if os.path.exists(sp):
        S = list(csv.DictReader(open(sp, encoding='utf-8')))
        res['existence_sample'] = dict(
            n=len(S), yes=sum(r['exists'] == 'yes' for r in S),
            partial=sum(r['exists'] == 'partial' for r in S),
            no=sum(r['exists'] == 'no' for r in S),
            unmatched_total=sum(1 for m in matches if m['status'] != 'match'))
    jac = [len(a & b) / len(a | b) if (a | b) else float('nan')
           for a, b in itertools.combinations(matched_sets, 2)]
    res['run_to_run_jaccard_mean'] = sum(jac) / len(jac) if jac else None
    with open(os.path.join(LD, 'armA_matches.csv'), 'w', newline='',
              encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(matches[0].keys()) if matches
                           else ['run'])
        w.writeheader()
        for m in matches:
            w.writerow(m)
    return res


# ------------------------------------------------------------------ Arm C
HMAP = {'multi-hazard/general': 'Multi-hazard/General',
        'earthquake': 'Earthquake', 'flood': 'Flood',
        'hurricane/cyclone': 'Hurricane/Cyclone',
        'biological/epidemic': 'Biological/Epidemic', 'wildfire': 'Wildfire',
        'drought/food insecurity': 'Drought/Food insecurity',
        'conflict/displacement': 'Conflict/Displacement',
        'technological/other': 'Technological/Other',
        'not reported': 'Not reported'}
PMAP = {'comparative benchmark': 'Comparative benchmark',
        'single-model metric': 'Single-model metric',
        'qualitative/none': 'Qualitative/none', 'not reported': 'Not reported'}
DMAP = {'operational deployment': 'Operational deployment',
        'real-data case study': 'Real-data case study',
        'synthetic/illustrative': 'Synthetic/illustrative',
        'not reported': 'Not reported'}
FAM = [('statistical', 'mf_statistical'), ('classical_ml', 'mf_ml'),
       ('deep_learning', 'mf_dl'), ('knowledge_based', 'mf_knowledge'),
       ('optimisation_simulation', 'mf_optsim'),
       ('generative_ai', 'mf_genai')]


def armC_vars(rec):
    v = {k2: str(rec.get(k1, '')) for k1, k2 in FAM}
    v['disaster_type'] = HMAP.get(str(rec.get('hazard', '')).lower(),
                                  'Not reported')
    st = str(rec.get('stochastic', '')).lower()
    v['stochastic'] = st if st in ('0', '1') else 'not reported'
    v['performance_evidence'] = PMAP.get(
        str(rec.get('performance_evidence', '')).lower(), 'Not reported')
    v['deployment_status'] = DMAP.get(
        str(rec.get('deployment_status', '')).lower(), 'Not reported')
    return v


def score_armC(C, runs):
    H = {c['study_id']: c for c in C}
    VARS = [k for _, k in FAM] + ['disaster_type', 'stochastic',
                                  'performance_evidence', 'deployment_status']
    res = {}
    per_run = {}
    for run, data in runs.items():
        recs = {r['record_id']: armC_vars(r) for r in data}
        per_run[run] = recs
        rr = {}
        for v in VARS:
            ids = [i for i in recs if i in H]
            a = [recs[i][v] for i in ids]
            b = [H[i][v] for i in ids]
            nr = sum(1 for x in a if x.lower() == 'not reported')
            definite = [(x, y) for x, y in zip(a, b)
                        if x.lower() != 'not reported']
            rr[v] = dict(n=len(ids),
                         agreement=sum(x == y for x, y in zip(a, b)) / len(ids)
                         if ids else float('nan'),
                         kappa=kappa(a, b),
                         share_not_reported=nr / len(ids) if ids else 0,
                         definite_disagree=sum(1 for x, y in definite if x != y)
                         / len(ids) if ids else 0)
        res[run] = rr
    if len(per_run) >= 2:
        common = set.intersection(*[set(r) for r in per_run.values()])
        res['run_to_run_fleiss'] = {
            v: fleiss([[per_run[r][i][v] for r in per_run] for i in sorted(common)])
            for v in VARS}
    return res


def load_runs(prefix):
    runs = {}
    for k in (1, 2, 3):
        p = os.path.join(LD, '%s_run%d.json' % (prefix, k))
        if os.path.exists(p):
            runs['run%d' % k] = json.load(open(p, encoding='utf-8'))
    return runs


def macros(resA):
    L = []
    runs = [k for k in resA if re.fullmatch(r'run[0-9]', k)]
    if not runs:
        return
    f = lambda key: [resA[r][key] for r in runs]
    pct = lambda x: '%.0f' % (100 * x)
    L.append('\\newcommand{\\llmRuns}{%d}' % len(runs))
    L.append('\\newcommand{\\llmListedMin}{%d}' % min(f('listed')))
    L.append('\\newcommand{\\llmListedMax}{%d}' % max(f('listed')))
    L.append('\\newcommand{\\llmMatchedMin}{%d}' % min(f('matched')))
    L.append('\\newcommand{\\llmMatchedMax}{%d}' % max(f('matched')))
    L.append('\\newcommand{\\llmRecallMin}{%s}' % pct(min(f('recall'))))
    L.append('\\newcommand{\\llmRecallMax}{%s}' % pct(max(f('recall'))))
    L.append('\\newcommand{\\llmPrecMin}{%s}' % pct(min(f('precision'))))
    L.append('\\newcommand{\\llmPrecMax}{%s}' % pct(max(f('precision'))))
    L.append('\\newcommand{\\llmRecallWaveTwoMax}{%s}'
             % pct(max(f('recall_wave2'))))
    L.append('\\newcommand{\\llmRecallWaveOneMax}{%s}'
             % pct(max(f('recall_wave1'))))
    ly = [y for y in f('latest_year_recovered') if y]
    L.append('\\newcommand{\\llmLatestYear}{%s}' % (max(ly) if ly else '--'))
    j = resA.get('run_to_run_jaccard_mean')
    L.append('\\newcommand{\\llmJaccard}{%s}' % ('%.2f' % j if j is not None
                                                 else '--'))
    es = resA.get('existence_sample')
    if es:
        L.append('\\newcommand{\\llmExistN}{%d}' % es['n'])
        L.append('\\newcommand{\\llmExistYes}{%d}' % es['yes'])
        L.append('\\newcommand{\\llmExistNo}{%d}' % (es['no'] + es['partial']))
        L.append('\\newcommand{\\llmUnmatched}{%d}' % es['unmatched_total'])
    n_all = len(corpus())
    n24 = sum(1 for c in corpus() if int(c['year']) >= 2024)
    L.append('\\newcommand{\\llmNrecent}{%d}' % n24)
    L.append('\\newcommand{\\llmRecentPct}{%.0f}' % (100.0 * n24 / n_all))
    open(os.path.join(LD, 'llm_macros.tex'), 'w').write('\n'.join(L) + '\n')


def selftest():
    """Arm C scoring on dummy data: perfect copy -> kappa 1; random -> ~0."""
    C = corpus()
    sample = [c for c in C if c['study_type'] == 'Primary'][:30]
    inv = {v: k for k, v in HMAP.items()}
    pinv = {v: k for k, v in PMAP.items()}
    dinv = {v: k for k, v in DMAP.items()}
    perfect = [dict(record_id=c['study_id'],
                    **{k1: int(c[k2]) for k1, k2 in FAM},
                    hazard=inv.get(c['disaster_type'], 'not reported'),
                    stochastic=int(c['stochastic']),
                    performance_evidence=pinv.get(c['performance_evidence'],
                                                  'not reported'),
                    deployment_status=dinv.get(c['deployment_status'],
                                               'not reported'))
               for c in sample]
    r = score_armC(C, {'run1': perfect, 'run2': perfect})
    assert abs(r['run1']['disaster_type']['agreement'] - 1) < 1e-9
    rng = random.Random(1)
    noisy = [dict(p, hazard=rng.choice(list(HMAP))) for p in perfect]
    r2 = score_armC(C, {'run1': noisy})
    print('selftest perfect agreement (hazard): %.2f; random agreement: %.2f'
          % (r['run1']['disaster_type']['agreement'],
             r2['run1']['disaster_type']['agreement']))
    print('selftest OK')


if __name__ == '__main__':
    os.makedirs(LD, exist_ok=True)
    if '--selftest' in sys.argv:
        selftest()
        sys.exit(0)
    C = corpus()
    out = {}
    A = load_runs('armA')
    if A:
        out['armA'] = score_armA(C, A)
        macros(out['armA'])
    Cr = load_runs('armC')
    if Cr:
        out['armC'] = score_armC(C, Cr)
    json.dump(out, open(os.path.join(LD, 'results.json'), 'w'), indent=1,
              default=str)
    print(json.dumps(out, indent=1, default=str)[:3000])


def table_armA(resA):
    """tables/tab_llm_armA.tex -- generated from results.json (Arm A)."""
    runs = [k for k in resA if re.fullmatch(r'run[0-9]', k)]
    pct = lambda x: '--' if x is None else '%.0f\\%%' % (100 * x)
    rows = [('Studies listed', lambda r: str(resA[r]['listed'])),
            ('Matched to an included source', lambda r: str(resA[r]['matched'])),
            ('Precision against the included sources',
             lambda r: pct(resA[r]['precision'])),
            ('Recall of the included sources', lambda r: pct(resA[r]['recall'])),
            ('Recall, sources published before 2024',
             lambda r: pct(resA[r]['recall_wave1'])),
            ('Recall, sources published 2024 to 2026',
             lambda r: pct(resA[r]['recall_wave2'])),
            ('Most recent included source recovered',
             lambda r: str(resA[r]['latest_year_recovered'] or '--')),
            ('Listed studies coded as comparative benchmark',
             lambda r: pct(resA[r]['share_comparative_yes'])),
            ('Listed studies coded as operationally deployed',
             lambda r: pct(resA[r]['share_operational_yes'])),
            ('Listed studies using knowledge-based methods',
             lambda r: pct(resA[r]['share_knowledge_based'])),
            ('Listed studies using generative AI',
             lambda r: pct(resA[r]['share_generative_ai']))]
    S = json.load(open(os.path.join(ROOT, 'data', 'stats.json')))
    P = [c for c in corpus() if c['study_type'] == 'Primary']
    ref = {'Listed studies coded as comparative benchmark':
               pct(sum(c['performance_evidence'] == 'Comparative benchmark'
                       for c in P) / len(P)),
           'Listed studies coded as operationally deployed':
               pct(sum(c['deployment_status'] == 'Operational deployment'
                       for c in P) / len(P)),
           'Listed studies using knowledge-based methods':
               pct(sum(c['mf_knowledge'] == '1' for c in P) / len(P)),
           'Listed studies using generative AI':
               pct(sum(c['mf_genai'] == '1' for c in P) / len(P)),
           'Studies listed': str(len(corpus()))}
    L = [r'\begin{table}[htbp!]', r'\centering', r'\footnotesize',
         r'\caption{LLM versus protocol-driven review}',
         r'\label{tab:llm_armA}',
         r'\begin{tabular}{@{}l' + 'r' * len(runs) + 'r@{}}', r'\toprule',
         'Measure & ' + ' & '.join(r'\textbf{Run %s}' % r[-1] for r in runs)
         + r' & \textbf{This review} \\', r'\midrule']
    for lab, f in rows:
        L.append(lab + ' & ' + ' & '.join(f(r) for r in runs)
                 + ' & ' + ref.get(lab, '') + r' \\')
    L += [r'\midrule', r'Mean pairwise overlap of matched sources (Jaccard) & '
          r'\multicolumn{%d}{r}{%.2f} & \\' % (len(runs),
                                            resA['run_to_run_jaccard_mean']),
          r'Sampled unmatched listed studies that exist & '
          r'\multicolumn{%d}{r}{%d of %d} & \\' % (
              len(runs), resA['existence_sample']['yes'],
              resA['existence_sample']['n']),
          r'\bottomrule', r'\end{tabular}', r'\end{table}']
    open(os.path.join(ROOT, 'tables', 'tab_llm_armA.tex'), 'w').write(
        '\n'.join(L) + '\n')


if __name__ == '__main__' and 'armA' in locals().get('out', {}):
    table_armA(out['armA'])
