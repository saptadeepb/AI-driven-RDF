#!/usr/bin/env python3
"""
merge_master.py
---------------
Merges wave-1 and wave-2 extraction rows into the single master dataset, then
overlays the verified performance/deployment evidence gathered at full-text or
abstract level (data/efficacy_evidence.csv).

Output: data/master_extraction.csv  -- the ONE file every number in the
manuscript is computed from.
"""
import csv, os, unicodedata, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, 'data', *p)

HEADER = ['study_id', 'citekey', 'first_author', 'year', 'wave', 'study_type',
          'author_country', 'focus_country', 'publisher', 'journal',
          'objective', 'disaster_type',
          'mf_statistical', 'mf_ml', 'mf_dl', 'mf_knowledge', 'mf_optsim',
          'mf_genai', 'learning_paradigm', 'horizon', 'linearity',
          'sustainability', 'stochastic', 'performance_evidence',
          'metric_reported', 'deployment_status', 'data_source', 'coding_note']


def fold(s):
    s = str(s)
    s = s.replace('ı', 'i').replace('İ', 'I')
    s = s.replace('æ', 'ae').replace('Æ', 'AE')
    s = s.replace('ø', 'o').replace('Ø', 'O')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.encode('ascii', 'ignore').decode('ascii')


# ---- country-label harmonisation (documented in data/CODEBOOK.md) -------
COUNTRY_FIX = {
    'UK': 'United Kingdom',
    'England': 'United Kingdom',
    'Great Britain': 'United Kingdom',
    'United States': 'USA',
    'US': 'USA',
    'Arabia': 'Saudi Arabia',
    'Turkiye': 'Turkey',
    'Korea': 'South Korea',
    'Republic of Korea': 'South Korea',
    '--': 'Not reported',
    '': 'Not reported',
    'Various': 'Global',
    'Focus on Recovery': 'Global',
    'European Countries': 'Europe (multi-country)',
    'Burkina Faso; Mali; Niger; South Sudan': 'Sahel (multi-country)',
}


def harmonise(rows):
    for r in rows:
        for i in (6, 7):                      # author_country, focus_country
            r[i] = COUNTRY_FIX.get(r[i].strip(), r[i].strip())
    return rows


# ---- journal-name harmonisation ----------------------------------------
# The extraction tables of the original submission recorded outlets by
# abbreviation, while the sources added by the 2026 updated search carry the
# full title, so the same journal appeared twice in the outlet distribution
# (e.g. "IJDRR" and "International Journal of Disaster Risk Reduction").
# Every expansion below is taken from the journal URL that the original
# submission itself printed beside the abbreviation, so the mapping is
# verifiable against that table rather than inferred.
JOURNAL_FIX = {
    'IJDRR': 'International Journal of Disaster Risk Reduction',
    'ESWA': 'Expert Systems with Applications',
    'SEPS': 'Socio-Economic Planning Sciences',
    'TRE': 'Transportation Research Part E: Logistics and Transportation Review',
    'Transportation Research Part E':
        'Transportation Research Part E: Logistics and Transportation Review',
    'EAAI': 'Engineering Applications of Artificial Intelligence',
    'IJPE': 'International Journal of Production Economics',
    'Ann Oper Res': 'Annals of Operations Research',
    'APM': 'Applied Mathematical Modelling',
    'EJOR': 'European Journal of Operational Research',
    'NH': 'Natural Hazards',
    '(ASCE)NH': 'Natural Hazards Review',
    'Natural Hazards Review (ASCE)': 'Natural Hazards Review',
    'IJSS': 'International Journal of Systems Science',
    'IJHPM': 'International Journal of Health Planning and Management',
    'IJIM': 'International Journal of Information Management',
    'IJIMDI': 'International Journal of Information Management Data Insights',
    'JEMA': 'Journal of Environmental Management',
    'JIAS': 'Journal of the International AIDS Society',
    'JOOM': 'Journal of Operations Management',
    'JORS': 'Journal of the Operational Research Society',
    'IJERPH': 'International Journal of Environmental Research and Public Health',
    'ijerph': 'International Journal of Environmental Research and Public Health',
    'atmosenv': 'Atmospheric Environment',
    'BMC Emerg Med': 'BMC Emergency Medicine',
    'BMC Med Inform Decis Mak': 'BMC Medical Informatics and Decision Making',
    'Complex Intell. Syst.': 'Complex and Intelligent Systems',
    'Energ Sustain Soc': 'Energy, Sustainability and Society',
    'Int J Data Sci Anal':
        'International Journal of Data Science and Analytics',
    'Computers and Electrical Engineering':
        'Computers and Electrical Engineering',
    'Computers & Electrical Engineering':
        'Computers and Electrical Engineering',
    'Computers & Industrial Engineering':
        'Computers and Industrial Engineering',
    'Chaos, Solitons & Fractals': 'Chaos, Solitons and Fractals',
    'Information Processing & Management':
        'Information Processing and Management',
    'Reliability Engineering & System Safety':
        'Reliability Engineering and System Safety',
    'Data & Policy': 'Data and Policy',
    'Big Data & Society': 'Big Data and Society',
    'Grey Systems: Theory and Application': 'Grey Systems',
    'Earthquake risk zoning study': 'Not reported',
    'Transportation Research Procedia': 'Transportation Research Procedia',
}


def harmonise_journals(rows):
    for r in rows:
        j = r[9].strip()
        r[9] = JOURNAL_FIX.get(j, j)
    return rows


def read_rows(path):
    with open(path, newline='', encoding='utf-8') as fh:
        return [[fold(c) for c in r] for r in csv.reader(fh) if r and any(r)]


def main():
    rows = (read_rows(D('wave1_rows.csv'))
            + read_rows(D('wave1_supplement_rows.csv'))
            + read_rows(D('wave2_rows.csv')))
    rows = harmonise(rows)
    rows = harmonise_journals(rows)

    # ---- renumber sequentially, guaranteeing uniqueness ----
    seen = {}
    dedup = []
    for r in rows:
        key = r[1]
        if key in seen:
            print('  ! duplicate citekey dropped: %s (kept %s)'
                  % (key, seen[key]))
            continue
        seen[key] = r[0]
        dedup.append(r)
    for i, r in enumerate(dedup, 1):
        r[0] = 'S%03d' % i

    # ---- overlay verified efficacy evidence ----
    ev = {}
    with open(D('efficacy_evidence.csv'), newline='', encoding='utf-8') as fh:
        for e in csv.DictReader(fh):
            ev[fold(e['citekey']).strip()] = {k: fold(v).strip()
                                              for k, v in e.items()}
    idx = {r[1]: r for r in dedup}
    n_over = 0
    for key, e in ev.items():
        r = idx.get(key)
        if r is None:
            print('  ! efficacy row has no matching study: %s' % key)
            continue
        grade = e['evidence_grade']
        comparative = e['comparative']
        reports = e['reports_metric']
        result = e['reported_result']
        got_number = (grade in ('A-fulltext', 'B-abstract')
                      and result
                      and 'Not retrievable' in result is False)
        got_number = grade in ('A-fulltext', 'B-abstract') and \
            'Not retrievable' not in result and result not in ('', 'None reported')

        if reports == 'No':
            r[23] = 'Qualitative/none'
        elif got_number and comparative == 'Yes':
            r[23] = 'Comparative benchmark'
        elif got_number:
            r[23] = 'Single-model metric'
        else:
            r[23] = 'Not reported'

        r[24] = (e['metric'] if e['metric'] and
                 'Not retrievable' not in e['metric'] else 'Not reported')
        if e['deployment_status'] and e['deployment_status'] != 'Not reported':
            ds = e['deployment_status']
            if ds.startswith('Operational'):
                r[25] = 'Operational deployment'
            elif ds.startswith('Real-data'):
                r[25] = 'Real-data case study'
            else:
                r[25] = ds
        r[27] = (r[27] + '; performance evidence verified at grade %s' % grade)
        n_over += 1

    # ---- integrity ----
    for r in dedup:
        assert len(r) == 28, 'field count %d in %s' % (len(r), r[0])
        for v in r:
            assert all(ord(c) < 128 for c in str(v)), 'non-ASCII in %s' % r[0]

    with open(D('master_extraction.csv'), 'w', newline='',
              encoding='ascii') as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerows(dedup)

    # near-duplicate check: two labels that normalise to the same string, or
    # one that is a strict prefix of another, indicate an unharmonised pair.
    import re as _re
    norm = lambda x: _re.sub(r'[^a-z0-9]', '', x.lower())
    js = sorted({r[9] for r in dedup if r[9] != 'Not reported'})
    groups = {}
    for j in js:
        groups.setdefault(norm(j), []).append(j)
    dup = [v for v in groups.values() if len(v) > 1]
    # genuinely distinct journals whose names are prefixes of one another
    DISTINCT = {('International Journal of Information Management',
                 'International Journal of Information Management Data Insights'),
                ('Natural Hazards', 'Natural Hazards Review')}
    pre = [(a, b) for a in js for b in js
           if a != b and norm(b).startswith(norm(a)) and len(norm(a)) > 12
           and (a, b) not in DISTINCT]
    if dup or pre:
        print('  ! possible unharmonised journal names:')
        for d in dup:
            print('      same after normalising: %s' % d)
        for a, b in pre:
            print('      prefix pair: %r  /  %r' % (a, b))
    else:
        print('journal names            : %d distinct, no near-duplicates' % len(js))

    print('efficacy overlays applied : %d' % n_over)
    print('MASTER DATASET            : %d studies -> data/master_extraction.csv'
          % len(dedup))


if __name__ == '__main__':
    main()
