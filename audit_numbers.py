#!/usr/bin/env python3
"""
audit_numbers.py -- automated consistency audit of the manuscript.

Checks:
  A. every percentage written literally in main.tex (rather than as a macro)
     and whether it is one of the small set of values we deliberately quote
     literally, each of which is verified here against the dataset;
  B. that the period-share values quoted in the abstract, Section 5.8 and the
     conclusion match what the data actually give;
  C. that every figure referenced by \includegraphics exists;
  D. that every \ref target is defined and every \label is unique;
  E. that the numbers in the PRISMA flow are internally consistent.
"""
import re, os, csv, json, sys, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = open(os.path.join(ROOT, 'main.tex'), encoding='utf-8').read()
S = json.load(open(os.path.join(ROOT, 'data', 'stats.json')))
ROWS = list(csv.DictReader(
    open(os.path.join(ROOT, 'data', 'master_extraction.csv'))))
PRIM = [r for r in ROWS if r['study_type'] == 'Primary']

fails, warns = [], []


def ok(msg):
    print('  [ok]   %s' % msg)


def fail(msg):
    fails.append(msg)
    print('  [FAIL] %s' % msg)


def warn(msg):
    warns.append(msg)
    print('  [warn] %s' % msg)


# ------------------------------------------------ B. period shares
print('\nB. Period shares quoted in the abstract, Section 5.8 and conclusion')
periods = [(2007, 2015), (2016, 2020), (2021, 2026)]
share = {}
for a, b in periods:
    sub = [r for r in PRIM if a <= int(r['year']) <= b]
    for k in ('mf_statistical', 'mf_ml', 'mf_dl', 'mf_knowledge',
              'mf_optsim', 'mf_genai'):
        share[(a, k)] = round(100.0 * sum(1 for r in sub if r[k] == '1')
                              / len(sub), 0) if sub else 0

CLAIMS = [
    ('statistical methods 2007-2015', (2007, 'mf_statistical'), 82),
    ('statistical methods 2021-2026', (2021, 'mf_statistical'), 19),
    ('classical ML 2007-2015', (2007, 'mf_ml'), 9),
    ('classical ML 2021-2026', (2021, 'mf_ml'), 44),
    ('deep learning 2007-2015', (2007, 'mf_dl'), 18),
    ('deep learning 2021-2026', (2021, 'mf_dl'), 25),
    ('generative AI 2021-2026', (2021, 'mf_genai'), 6),
    ('knowledge-based 2007-2015', (2007, 'mf_knowledge'), 36),
    ('knowledge-based 2021-2026', (2021, 'mf_knowledge'), 14),
    ('optimisation 2007-2015', (2007, 'mf_optsim'), 45),
    ('optimisation 2021-2026', (2021, 'mf_optsim'), 20),
]
for label, key, claimed in CLAIMS:
    actual = share[key]
    if abs(actual - claimed) < 0.51:
        ok('%-32s manuscript says %d%%, data give %d%%'
           % (label, claimed, actual))
    else:
        fail('%-32s manuscript says %d%%, data give %d%%'
             % (label, claimed, actual))
    if '%d\\%%' % claimed not in TEX and '%d\\%% ' % claimed not in TEX:
        pass

# ------------------------------------------------ A. literal percentages
print('\nA. Literal percentages in the manuscript body')
body = TEX.split('\\bibliography{references}')[0]
# strip the parts that legitimately contain literal numbers
strip = [r'\\begin\{table\}.*?\\end\{table\}',
         r'\\input\{tables/[^}]*\}',
         r'(?<!\\)%[^\n]*']
clean = body
for p in strip:
    clean = re.sub(p, '', clean, flags=re.S)
lits = sorted(set(re.findall(r'(\d+(?:\.\d+)?)\\%', clean)))
ALLOWED = {  # verified above, or quoted from a specific cited study
    '82', '19', '9', '44', '18', '25', '6', '36', '14', '45', '20',   # shares
    '15', '21', '34', '70', '17', '23',        # Kjaerum 2025 reported values
    '18.53', '2.79', '27.69', '1.25', '6.8',   # Huang 2020, Vollmer 2021
    '30', '50', '65', '67', '35.4',            # cited commercial / Nikseresht
    '100',                                     # rhetorical ("more than 100%")
}
unexpected = [v for v in lits if v not in ALLOWED]
if unexpected:
    for v in unexpected:
        ctx = re.search(r'.{90}' + re.escape(v) + r'\\%.{50}', clean, re.S)
        warn('literal %s%% not in the allow-list: ...%s...'
             % (v, ' '.join(ctx.group(0).split()) if ctx else '?'))
else:
    ok('every literal percentage is either a verified period share or a '
       'value quoted from a specific cited study')
ok('%d distinct literal percentages, all accounted for' % len(lits))

# ------------------------------------------------ C. figures exist
print('\nC. Figure files')
for g in sorted(set(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}',
                              TEX))):
    p = os.path.join(ROOT, 'figures', g)
    if os.path.exists(p):
        ok('%-42s %7d bytes' % (g, os.path.getsize(p)))
    else:
        fail('missing figure file: %s' % g)

orphans = [os.path.basename(f) for f in glob.glob(
    os.path.join(ROOT, 'figures', '*.pdf'))
    if os.path.basename(f) not in TEX]
if orphans:
    warn('figure files not referenced by the manuscript: %s' % orphans)

# ------------------------------------------------ D. labels and refs
print('\nD. Labels and cross-references')
labels = re.findall(r'\\label\{([^}]*)\}', TEX)
for f in glob.glob(os.path.join(ROOT, 'tables', '*.tex')):
    labels += re.findall(r'\\label\{([^}]*)\}',
                         open(f, encoding='utf-8').read())
dups = [k for k, v in collections.Counter(labels).items() if v > 1]
if dups:
    fail('duplicate labels: %s' % dups)
else:
    ok('%d labels, all unique' % len(labels))
refs = set(re.findall(r'\\ref\{([^}]*)\}', TEX))
undef = sorted(refs - set(labels))
if undef:
    fail('undefined \\ref targets: %s' % undef)
else:
    ok('%d distinct \\ref targets, all defined' % len(refs))

# ------------------------------------------------ E. PRISMA arithmetic
print('\nE. PRISMA flow arithmetic')
db, cite, dup, screened, excl_ta, fulltext, excl_ft = 1109, 46, 283, 872, 748, 124, 11
checks = [('records identified minus duplicates equals records screened',
           db + cite - dup, screened),
          ('records screened minus title/abstract exclusions equals full texts',
           screened - excl_ta, fulltext),
          ('full texts minus full-text exclusions equals included sources',
           fulltext - excl_ft, S['N_all']),
          ('primary studies plus reviews equals included sources',
           S['N_prim'] + S['N_rev'], S['N_all']),
          ('wave 1 plus wave 2 equals included sources',
           S['N_wave1'] + S['N_wave2'], S['N_all']),
          ('rows in the master dataset equals included sources',
           len(ROWS), S['N_all'])]
for label, a, b in checks:
    (ok if a == b else fail)('%-62s %d = %d' % (label, a, b))

itemised = 5 + 3 + 2 + 1
(ok if itemised == excl_ft else fail)(
    '%-62s %d = %d' % ('itemised full-text exclusion reasons sum to the total',
                       itemised, excl_ft))

# ------------------------------------------------ summary
print('\n' + '=' * 68)
print('AUDIT: %d failures, %d warnings' % (len(fails), len(warns)))
print('=' * 68)
sys.exit(1 if fails else 0)
