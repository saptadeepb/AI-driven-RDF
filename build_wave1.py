#!/usr/bin/env python3
"""
build_wave1.py
--------------
Parses the extraction tables of the ORIGINAL submission (main_original.tex,
Table 1 = primary studies, Table 2 = recent AI-in-disaster works) and emits the
wave-1 portion of the master extraction dataset.

Every derived variable is produced by an explicit, deterministic rule so that a
reader can reproduce the coding from the reported method string. The rules are
documented in data/CODEBOOK.md and reproduced in the manuscript's Methods.

Usage:  python3 code/build_wave1.py
Output: data/wave1_rows.csv (headerless, 28 fields, ASCII only)
"""
import re, csv, unicodedata, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'main_original.tex')
OUT = os.path.join(ROOT, 'data', 'wave1_rows.csv')

# ---------------------------------------------------------------- utilities

def ascii_fold(s):
    """Transliterate to ASCII: Kirbas, Diaz, Kjaerum, Yilmaz ..."""
    if s is None:
        return ''
    s = s.replace('\u0131', 'i').replace('\u0130', 'I')
    s = s.replace('\u00e6', 'ae').replace('\u00c6', 'AE')
    s = s.replace('\u00f8', 'o').replace('\u00d8', 'O')
    s = s.replace('\u0141', 'L').replace('\u0142', 'l')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.encode('ascii', 'ignore').decode('ascii')


def clean(cell):
    """Strip LaTeX markup from one table cell."""
    c = cell
    c = re.sub(r'\\href\{[^}]*\}\{([^}]*)\}', r'\1', c)
    c = re.sub(r'\\cite\{[^}]*\}', '', c)
    c = re.sub(r'\\text(bf|it)\{([^}]*)\}', r'\2', c)
    c = c.replace('\\&', '&').replace('\\\\', ' ').replace('\\hline', '')
    c = re.sub(r'[{}~]', '', c)
    c = re.sub(r'\s+', ' ', c).strip()
    return ascii_fold(c)


def citekey(cell):
    m = re.search(r'\\cite\{([^}]*)\}', cell)
    return m.group(1).split(',')[0].strip() if m else ''


def split_row(line):
    """Split a LaTeX table row on unescaped ampersands."""
    return re.split(r'(?<!\\)&', line)


# ------------------------------------------------- controlled vocabularies

# --------------------------------------------- method-detail enrichment
# Table 1 of the original submission records the method at a very coarse
# granularity ("Statistical", "ML").  data/method_detail.csv records, for each
# study, the technique actually named in the narrative of the original
# submission, together with the sentence it was taken from.  The method-family
# rules below are applied to that richer string, which is why the revised
# coding is reproducible and auditable.

def load_method_detail():
    path = os.path.join(ROOT, 'data', 'method_detail.csv')
    d = {}
    with open(path, newline='', encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            d[row['citekey'].strip()] = ascii_fold(row['method_detail'].strip())
    return d

METHOD_DETAIL = {}


OBJECTIVE_MAP = {
    'Risk Assessment and Optimization':      'Disaster preparedness and relief planning',
    'Dynamic and Adaptive':                  'Dynamic and adaptive demand estimation',
    'Time Series Analysis and Forecasting':  'Predictive modelling and forecasting',
    'Specialized Forecasting Models':        'Predictive modelling and forecasting',
    'Supply Chain Management':               'Humanitarian logistics and supply chain management',
    'Humanitarian Operations':               'Humanitarian logistics and supply chain management',
    'Data-Driven Approach':                  'Predictive modelling and forecasting',
}

DISASTER_MAP = {
    'Natural':        'Multi-hazard/General',
    'Earthquake':     'Earthquake',
    'Flood':          'Flood',
    'Hurricanes':     'Hurricane/Cyclone',
    'Hurricane':      'Hurricane/Cyclone',
    'Typhoon':        'Hurricane/Cyclone',
    'Bio-Hazardous':  'Biological/Epidemic',
    'Air Pollution':  'Technological/Other',
    'Food':           'Drought/Food insecurity',
    'Hospital':       'Biological/Epidemic',
    'Medical':        'Biological/Epidemic',
    '--':             'Not reported',
    '':               'Not reported',
}

HORIZON_MAP = {
    'Short to Long term': 'Short-to-long',
    'Long term':          'Long-term',
    'Short term':         'Short-term',
    'Dynamic':            'Dynamic/real-time',
    '--':                 'Not reported',
    '':                   'Not reported',
}

PARADIGM_MAP = {
    'Supervised':                'Supervised',
    'Unsupervised':              'Unsupervised',
    'Unsupervised & Supervised': 'Both',
    'Supervised & Unsupervised': 'Both',
    '--':                        'Not reported',
    '':                          'Not reported',
}

PUBLISHER_MAP = {
    'Science Direct': 'Elsevier',
    'ScienceDirect':  'Elsevier',
    'Elsevier':       'Elsevier',
    'Springer':       'Springer',
    'IEEE':           'IEEE',
    'Wiley':          'Wiley',
    'Taylor & Francis': 'Taylor & Francis',
    'MDPI':           'MDPI',
    'BMJ Journals':   'Other',
    'PLOS':           'Other',
    'Semnan University': 'Other',
}


# --------------------------------------------- RULE 1: method family flags
# Multi-label. Applied to the concatenation of the "Forecasting Method" and
# "Method Types"/"AI Techniques"/"Model" cells, lower-cased.

def method_flags(text):
    t = text.lower()
    f = dict(mf_statistical=0, mf_ml=0, mf_dl=0,
             mf_knowledge=0, mf_optsim=0, mf_genai=0)
    if re.search(r'statistic|arima|regress|bayes|time series|econometric|'
                 r'smoothing|probabil|zinbm|state space', t):
        f['mf_statistical'] = 1
    if re.search(r'\bml\b|machine learning|random forest|decision tree|svm|'
                 r'support vector|k-nn|knn|boost|ensemble|xgboost|catboost|'
                 r'gradient|lightgbm|extra tree|\bdm\b|data mining', t):
        f['mf_ml'] = 1
    if re.search(r'\bdl\b|deep learning|neural|\bann\b|\bnn\b|cnn|rnn|lstm|'
                 r'mlp|bpnn|transformer|bert|xlnet|segnet|u-net|deeplab|'
                 r'reinforcement|autoencoder|gnn|graph neural', t):
        f['mf_dl'] = 1
    if re.search(r'fuzzy|case-based|case based|\bcbr\b|rule-based|rule based|'
                 r'\brbr\b|rough set|grey|knowledge graph|intuitionistic|'
                 r'\bahp\b|topsis|mcdm|dempster', t):
        f['mf_knowledge'] = 1
    if re.search(r'algorithm|simulation|optimi[sz]|programming|metaheuristic|'
                 r'genetic|particle swarm|\bpso\b|bee colony|agent-based|'
                 r'agent based|routing|scheduling|stochastic program', t):
        f['mf_optsim'] = 1
    if re.search(r'large language|\bllm\b|generative|\brag\b|retrieval-augmented|'
                 r'gpt|foundation model', t):
        f['mf_genai'] = 1
    return f


# -------------------------------------------------- RULE 2: linearity
# Linear    -> only statistical families, and no non-linear learner present
# Non-linear-> any ML / DL / metaheuristic / knowledge-based non-linear method
# Combined  -> statistical AND (ML or DL) present  (explicit hybrids)

def linearity(f, raw):
    nonlin = f['mf_ml'] or f['mf_dl'] or f['mf_genai']
    if f['mf_statistical'] and nonlin:
        return 'Combined'
    if nonlin or f['mf_optsim'] or f['mf_knowledge']:
        return 'Non-linear'
    if f['mf_statistical']:
        return 'Linear'
    return 'Not reported'


# ------------------------------------------- RULE 3: stochastic / uncertainty
# 1 if the method explicitly represents uncertainty.

def stochastic(text):
    t = text.lower()
    return int(bool(re.search(
        r'fuzzy|bayes|stochastic|probabil|rough set|grey|intuitionistic|'
        r'uncertain|scenario|interval|dempster|monte carlo|robust', t)))


# ------------------------------------------- RULE 4: sustainability
# 1 if the study's objective or context explicitly concerns environmental or
# social sustainability, resilience, energy, or equity.

def sustainability(objective, journal, extra=''):
    t = (objective + ' ' + journal + ' ' + extra).lower()
    return int(bool(re.search(
        r'sustainab|resilien|environment|energy|equit|social impact|'
        r'community|ecolog|climate', t)))


# =========================================================== TABLE 1 parse

def parse_table1(tex):
    lines = tex.split('\n')
    start = next(i for i, l in enumerate(lines)
                 if 'tab:forecasting_methods_summary' in l)
    end = next(i for i, l in enumerate(lines[start:], start)
               if 'tab:research_papers_summary' in l)
    rows = []
    for l in lines[start:end]:
        s = l.strip()
        if not s or s.startswith('%') or '\\cite{' not in s:
            continue
        if 'textbf' in s:          # header row
            continue
        cells = split_row(s)
        if len(cells) < 11:
            continue
        rows.append(cells)
    return rows


def code_table1(cells, sid):
    author_cell = cells[0]
    key = citekey(author_cell)
    author = clean(re.sub(r'\\cite\{[^}]*\}', '', author_cell))
    author = re.sub(r'\s*et al\.?\s*$', '', author).strip()
    author = re.sub(r'^[A-Z]\.\s*', '', author)          # drop leading initial
    author_country = clean(cells[1]) or 'Not reported'
    focus = clean(cells[2]) or 'Not reported'
    year = clean(cells[3])
    publisher = PUBLISHER_MAP.get(clean(cells[4]), clean(cells[4]) or 'Other')
    journal = clean(cells[5])
    obj_raw = clean(cells[6])
    dis_raw = clean(cells[7])
    meth_raw = clean(cells[8])
    para_raw = clean(cells[9])
    hor_raw = clean(cells[10])

    objective = OBJECTIVE_MAP.get(obj_raw, 'Predictive modelling and forecasting')
    disaster = DISASTER_MAP.get(dis_raw, 'Multi-hazard/General'
                                if dis_raw not in ('--', '') else 'Not reported')
    detail = METHOD_DETAIL.get(key, '')
    f = method_flags(meth_raw + ' ' + para_raw + ' ' + detail)
    paradigm = PARADIGM_MAP.get(para_raw, 'Not reported')
    horizon = HORIZON_MAP.get(hor_raw, 'Not reported')
    lin = linearity(f, meth_raw)
    sto = stochastic(meth_raw + ' ' + obj_raw + ' ' + detail)
    sus = sustainability(obj_raw, journal, detail)

    note = 'wave-1 primary study; codes transcribed from Table 1 of the ' \
           'original submission; derived variables by rules R1-R4'
    if meth_raw in ('--', '') and not detail:
        note += '; method family not stated in source record'

    return [sid, key, author, year, '1', 'Primary', author_country, focus,
            publisher, journal, objective, disaster,
            f['mf_statistical'], f['mf_ml'], f['mf_dl'],
            f['mf_knowledge'], f['mf_optsim'], f['mf_genai'],
            paradigm, horizon, lin, sus, sto,
            'Not reported', 'Not reported', 'Not reported',
            'Historical records', note]


# =========================================================== TABLE 2 parse

def parse_table2(tex):
    lines = tex.split('\n')
    start = next(i for i, l in enumerate(lines)
                 if 'tab:research_papers_summary' in l)
    end = next(i for i, l in enumerate(lines[start:], start)
               if 'Insights from Literature Analysis' in l)
    rows = []
    for l in lines[start:end]:
        s = l.strip()
        if not s or s.startswith('%') or '\\cite{' not in s:
            continue
        if 'textbf' in s:
            continue
        cells = split_row(s)
        if len(cells) < 10:
            continue
        rows.append(cells)
    return rows


SUBFIELD_OBJ = {
    'Disaster Recovery':        'Disaster preparedness and relief planning',
    'Disaster Management':      'Methodological or technology review',
    'Risk Reduction':           'Methodological or technology review',
    'Agriculture':              'Predictive modelling and forecasting',
    'Supply Chain':             'Humanitarian logistics and supply chain management',
    'Business Continuity':      'Humanitarian logistics and supply chain management',
    'Emergency Management':     'Methodological or technology review',
    'Disaster Preparedness':    'Disaster preparedness and relief planning',
    'Disaster Response, AISDR': 'Methodological or technology review',
    'Hurricane':                'Predictive modelling and forecasting',
    'Earthquakes':              'Predictive modelling and forecasting',
    'Natural Disasters General':'Methodological or technology review',
    'Natural Disasters':        'Methodological or technology review',
}

SUBFIELD_DIS = {
    'Hurricane': 'Hurricane/Cyclone',
    'Earthquakes': 'Earthquake',
    'Agriculture': 'Drought/Food insecurity',
}

DATASOURCE_MAP = {
    'Survey': 'Survey/interview',
    'Various': 'Mixed',
    'Agricultural Data': 'Historical records',
    'Social Media (Twitter)': 'Social media',
    'Survey and TrashNet': 'Mixed',
}

# Studies in Table 2 that apply a method to data (Primary) rather than
# synthesising the literature (Review).
T2_PRIMARY = {
    'Kankanamge2021PublicBrisbane', 'Jamei2022CombinedSelection',
    'Powers2023UsingApproach', 'Pitakaso2024Optimization-drivenManagement',
    'Biswas2024AnTurkiye', 'Ghouri2023AnDevelopment',
}


def code_table2(cells, sid):
    key = citekey(cells[0])
    author = clean(re.sub(r'\\cite\{[^}]*\}', '', cells[0]))
    author = re.sub(r',?\s*\d{4}\s*$', '', author)
    author = re.sub(r'\s*et al\.?\s*$', '', author).strip()
    author_country = clean(cells[1]) or 'Not reported'
    focus = clean(cells[2]) or 'Not reported'
    focus = 'Global' if 'Focus on Recovery' in focus else focus
    year = clean(cells[3])
    subfield = clean(cells[4])
    ai_tech = clean(cells[5])
    model = clean(cells[6])
    datasrc = clean(cells[7])
    journal = clean(cells[8])
    publisher = PUBLISHER_MAP.get(clean(cells[9]), clean(cells[9]) or 'Other')

    stype = 'Primary' if key in T2_PRIMARY else 'Review'
    objective = SUBFIELD_OBJ.get(subfield, 'Methodological or technology review')
    disaster = SUBFIELD_DIS.get(subfield, 'Multi-hazard/General')
    detail = METHOD_DETAIL.get(key, '')
    f = method_flags(ai_tech + ' ' + model + ' ' + detail)
    if stype == 'Review':
        f = dict.fromkeys(f, 0)          # N_prim rule: reviews carry no method flags
    lin = linearity(f, ai_tech) if stype == 'Primary' else 'Not reported'
    sto = stochastic(ai_tech + ' ' + model + ' ' + detail) if stype == 'Primary' else 0
    sus = sustainability(subfield, journal, ai_tech + ' ' + detail)

    note = ('wave-1 %s; codes transcribed from Table 2 of the original '
            'submission' % stype.lower())
    return [sid, key, author, year, '1', stype, author_country, focus,
            publisher, journal, objective, disaster,
            f['mf_statistical'], f['mf_ml'], f['mf_dl'],
            f['mf_knowledge'], f['mf_optsim'], f['mf_genai'],
            'Not reported' if stype == 'Review' else 'Supervised',
            'Not reported', lin, sus, sto,
            'Not applicable (review)' if stype == 'Review' else 'Not reported',
            'Not reported',
            'Not reported' if stype == 'Review' else 'Real-data case study',
            DATASOURCE_MAP.get(datasrc, 'Not reported'), note]


# ================================================================== main

def main():
    global METHOD_DETAIL
    METHOD_DETAIL = load_method_detail()
    tex = open(SRC, encoding='utf-8').read()
    t1 = parse_table1(tex)
    t2 = parse_table2(tex)
    rows = []
    n = 0
    for c in t1:
        n += 1
        rows.append(code_table1(c, 'S%03d' % n))
    for c in t2:
        n += 1
        rows.append(code_table2(c, 'S%03d' % n))

    # integrity checks
    keys = [r[1] for r in rows]
    assert all(keys), 'row with empty citekey'
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, 'duplicate citekeys in wave 1: %s' % dup
    for r in rows:
        assert len(r) == 28, 'bad field count: %s' % r[0]
        for v in r:
            assert all(ord(ch) < 128 for ch in str(v)), 'non-ASCII in %s' % r[0]

    with open(OUT, 'w', newline='', encoding='ascii') as fh:
        csv.writer(fh).writerows(rows)

    print('Table 1 primary studies : %d' % len(t1))
    print('Table 2 sources         : %d' % len(t2))
    print('wave-1 rows written     : %d -> %s' % (len(rows), OUT))


if __name__ == '__main__':
    main()
