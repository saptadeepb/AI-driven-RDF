#!/usr/bin/env python3
"""
search_harmonisation.py -- R2, Reviewer 3 comment 1.

Audits the six database strings of the R1 search (code/make_tables.py, SEARCH)
concept by concept, writes the term-by-database coverage matrix
data/search_harmonisation_R2.csv, and writes the harmonised R2 strings
(identical concept blocks in every database) to
data/search_strings_R2.json, which make_tables.py prints in the search table.
"""
import csv, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'code'))
src = open(os.path.join(ROOT, 'code', 'make_tables.py'), encoding='utf-8').read()
ns = {}
exec(src[src.index('SEARCH_R1 = ['):src.index('# end SEARCH_R1')], ns)
R1 = ns['SEARCH_R1']

# ---- the three concept blocks of the R2 harmonised strategy -------------
# Block A = union of every relief-demand term used in any R1 string.
# Block B = union of every forecasting term used in any R1 string.
# Block C = union of every method term used in any R1 string, plus the method
#           families named in the eligibility Concept (Section 3.2) that no R1
#           string covered (knowledge-based reasoning, generative AI).
A = ['relief demand', 'humanitarian demand', 'humanitarian need*',
     'relief suppl*', 'emergency suppl*', 'emergency material*',
     'emergency resource*', 'emergency supply chain*', 'disaster relief',
     'humanitarian logistic*']
B = ['forecast*', 'predict*', 'estimat*']
C = ['artificial intelligence', 'machine learning', 'deep learning',
     'neural network*', 'data-driven', 'time series',
     'large language model*', 'generative AI', 'fuzzy', 'case-based reasoning',
     'grey model*', 'rough set*']
MESH = ['"Disasters"[Mesh]', '"Relief Work"[Mesh]',
        '"Emergency Medical Services"[Mesh]']


def present(term, q):
    t = term.lower().replace('*', '')
    ql = q.lower().replace('*', '').replace('"', '')
    ql = re.sub(r'\[[a-z ]+\]', '', ql)
    if t.endswith(' '):
        t = t.strip()
    # treat singular/plural/truncated stems as the same concept term
    stem = t.rstrip('s')
    return int(stem in ql)


def matrix():
    rows = []
    for block, terms in (('A relief-demand object', A),
                         ('B forecasting operation', B),
                         ('C computational method', C)):
        for term in terms:
            rows.append([block, term] + [present(term, ' '.join(q.split()))
                                         for _, _, q, _, _ in R1])
    with open(os.path.join(ROOT, 'data', 'search_harmonisation_R2.csv'), 'w',
              newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['concept_block', 'term'] + [db for db, *_ in R1]
                   + ['in_R2_harmonised_string'])
        for r in rows:
            w.writerow(r + [1])
    return rows


def q(terms, quote=True):
    out = []
    for t in terms:
        if ' ' in t or '-' in t:
            out.append('"%s"' % t)
        else:
            out.append(t)
    return '( ' + ' OR '.join(out) + ' )'


def strings():
    a, b, c = q(A), q(B), q(C)
    pa = ' OR '.join('"%s"[tiab]' % t if (' ' in t or '-' in t) else '%s[tiab]' % t
                     for t in A)
    pb = ' OR '.join('%s[tiab]' % t for t in B)
    pc = ' OR '.join('"%s"[tiab]' % t if (' ' in t or '-' in t) else '%s[tiab]' % t
                     for t in C)
    S = [
        ('Scopus', 'TITLE-ABS-KEY',
         'TITLE-ABS-KEY %s AND TITLE-ABS-KEY %s AND TITLE-ABS-KEY %s' % (a, b, c)),
        ('Web of Science Core Collection', 'TS= (title, abstract, author keywords, Keywords Plus)',
         'TS=%s AND TS=%s AND TS=%s' % (a, b, c)),
        ('ScienceDirect', 'Title, abstract or author-specified keywords',
         'Same three blocks, split into sub-queries to respect the limit on '
         'Boolean connectors per field; the union of the sub-query results is '
         'exported (see Supplementary S5).'),
        ('SpringerLink', 'Title and abstract where the interface allows; otherwise all fields, '
         'restricted to articles and chapters',
         'Same three blocks %s AND %s AND %s' % (a, b, c)),
        ('IEEE Xplore', 'All Metadata',
         '("All Metadata":%s) AND ("All Metadata":%s) AND ("All Metadata":%s)' % (a, b, c)),
        ('PubMed', 'Title/Abstract [tiab] and MeSH',
         '( %s OR %s ) AND ( %s ) AND ( %s )' % (' OR '.join(MESH), pa, pb, pc)),
    ]
    json.dump({'blocks': {'A': A, 'B': B, 'C': C, 'PubMed_MeSH': MESH},
               'strings': [{'database': d, 'fields': f, 'string': s}
                           for d, f, s in S]},
              open(os.path.join(ROOT, 'data', 'search_strings_R2.json'), 'w'),
              indent=1)
    return S


if __name__ == '__main__':
    rows = matrix()
    S = strings()
    dbs = [db for db, *_ in R1]
    print('term coverage in the R1 strings (1 = present):')
    print('%-28s' % 'term' + ' '.join('%5s' % d[:5] for d in dbs))
    for r in rows:
        print('%-28s' % r[1] + ' '.join('%5d' % v for v in r[2:]))
    for d in dbs:
        i = dbs.index(d)
        n = sum(r[2 + i] for r in rows)
        print('%-16s covers %2d of %d harmonised terms' % (d, n, len(rows)))


# ----------------------------------------------------------- macros (R2)
def write_macros(rows):
    dbs = [db for db, *_ in R1]
    cov = {d: sum(r[2 + i] for r in rows) for i, d in enumerate(dbs)}
    U = json.load(open(os.path.join(ROOT, 'data', 'search_update_R2.json')))
    tbc = r'\textbf{[TBC]}'
    v = lambda k: tbc if U.get(k) in (None, '') else str(U[k])
    L = ['%% generated by code/search_harmonisation.py -- do not edit',
         r'\newcommand{\HarmNTerms}{%d}' % len(rows),
         r'\newcommand{\HarmCovMax}{%d}' % max(cov.values()),
         r'\newcommand{\HarmCovMaxDb}{%s}' % max(cov, key=cov.get),
         r'\newcommand{\HarmCovMin}{%d}' % min(cov.values()),
         r'\newcommand{\HarmCovMinDb}{%s}' % min(cov, key=cov.get),
         r'\newcommand{\HarmCovWoS}{%d}' % cov['Web of Science'],
         r'\newcommand{\HarmLLMOnly}{%d}' % sum(
             1 for r in rows if r[1] == 'large language model*' and sum(r[2:]) == 1),
         r'\newcommand{\HarmSearchDate}{%s}' % v('date_executed'),
         r'\newcommand{\HarmRecords}{%s}' % v('records_identified_total'),
         r'\newcommand{\HarmNewRecords}{%s}' % v('new_records_after_deduplication'),
         r'\newcommand{\HarmNewFullText}{%s}' % v('new_records_full_text_assessed'),
         r'\newcommand{\HarmNewIncluded}{%s}' % v('new_studies_included')]
    open(os.path.join(ROOT, 'search_macros.tex'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    write_macros(matrix())


def write_S5():
    J = json.load(open(os.path.join(ROOT, 'data', 'search_strings_R2.json')))
    rows = list(csv.reader(open(os.path.join(ROOT, 'data',
                                             'search_harmonisation_R2.csv'))))
    def esc(s):
        s = ' '.join(s.split())
        for ch in '\\*_[]#<>`':
            s = s.replace(ch, '\\' + ch)
        return s
    L = ['# Supplementary Material S5: Harmonised search strategy', '',
         '*Artificial Intelligence for Relief Demand Forecasting: A PRISMA-ScR Scoping Review of Research Attention and Efficacy Evidence*', '',
         '## 1. Concept blocks (identical in every database)', '']
    for k, lab in (('A', 'Relief-demand object'), ('B', 'Forecasting operation'),
                   ('C', 'Computational method')):
        L.append('**%s. %s:** %s' % (k, lab, esc(' OR '.join(
            ('"%s"' % x) if (' ' in x or '-' in x) else x for x in J['blocks'][k]))))
        L.append('')
    L += ['Blocks are joined by AND. In PubMed, block A is additionally OR-ed '
          'with %s.' % esc(', '.join(J['blocks']['PubMed_MeSH'])), '',
          '## 2. Query in each database\'s syntax', '']
    for s in J['strings']:
        L += ['### %s' % s['database'], '', 'Field tag: %s' % s['fields'], '',
              '> ' + esc(s['string'].replace('(see Supplementary S5)', '(see the note below)')), '']
    L += ['ScienceDirect limits the number of Boolean connectors per field. Run '
          'block A in sub-queries of at most eight terms, each combined with the '
          'full blocks B and C as far as the limit allows (splitting block C in '
          'the same way if necessary), export every sub-query, and take the '
          'union before deduplication. Record every sub-query as executed.', '',
          'Where an interface does not support right-hand truncation, enter the '
          'truncated terms as their singular and plural forms.', '',
          'Verify the exact operator and field syntax in each interface on the '
          'day of execution and record any adaptation in the execution log.', '',
          '## 3. Execution checklist', '',
          '1. Run each query from inception to the execution date; record the date, the exact query as executed, any filters and the number of records.',
          '2. Export full records (title, abstract, authors, year, venue, DOI) in RIS or CSV.',
          '3. Deduplicate across databases and against all records already screened for the review.',
          '4. Screen titles and abstracts of new records in duplicate under the unchanged eligibility criteria (Section 3.2); log every decision.',
          '5. Assess full texts of potentially eligible records in duplicate, recording the exclusion reason.',
          '6. Chart included studies under the codebook, regenerate the statistics and update the PRISMA flow diagram.', '',
          '## 4. Coverage audit of the strings with which the corpus was identified', '',
          '1 = term present in that database\'s string.', '',
          '| ' + ' | '.join(['Concept block', 'Term'] + rows[0][2:-1]) + ' |',
          '|' + '---|' * (len(rows[0]) - 1)]
    for r in rows[1:]:
        L.append('| ' + ' | '.join(r[:-1]) + ' |')
    L += ['', '## 5. Strings with which the corpus was identified', '']
    for db, fld, q, win, n in R1:
        L += ['**%s** (%s): %s' % (db, fld, esc(q)), '']
    open(os.path.join(ROOT, 'supplementary', 'S5_harmonised_search.md'), 'w').write(
        '\n'.join(L) + '\n')
    with open(os.path.join(ROOT, 'data', 'screening_log_R2.csv'), 'w') as fh:
        fh.write('record_id,database,title,doi,reviewer_1_decision,reviewer_2_decision,'
                 'final_decision,stage,exclusion_reason,notes\n')


if __name__ == '__main__':
    write_S5()
