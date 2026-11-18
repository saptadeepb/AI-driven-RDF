#!/usr/bin/env python3
"""
practitioner_examples.py -- R2, Reviewer 1 comment 1.

Runs the four worked use-cases of the practitioner guide (Supplementary S2)
against data/master_extraction.csv and writes
  supplementary/S2_examples_output.txt  (the printed results)
  supplementary/S2_macros.tex           (counts quoted in the guide)
so that every count in the guide is produced by the code the guide shows.
Requires only pandas.
"""
import os, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(ROOT, 'data', 'master_extraction.csv'), dtype=str)
out, mac = [], {}

def show(title, frame, cols):
    out.append('=' * 72); out.append(title); out.append('-' * 72)
    out.append(frame[cols].to_string(index=False) if len(frame) else '(none)')
    out.append('rows: %d' % len(frame)); out.append('')

# --- Use-case A: candidate methods for a hazard and a data type ------------
prim = df[df.study_type == 'Primary']
a = prim[(prim.disaster_type == 'Flood')]
fam = ['mf_statistical', 'mf_ml', 'mf_dl', 'mf_knowledge', 'mf_optsim', 'mf_genai']
counts = a[fam].astype(int).sum()
out.append('Use-case A: flood studies, method families employed (multi-label)')
out.append(counts.to_string()); out.append('')
show('Use-case A: flood studies', a,
     ['study_id', 'first_author', 'year', 'data_source', 'performance_evidence',
      'deployment_status'])
mac['ucAflood'] = len(a)
mac['ucAfloodDL'] = int(counts['mf_dl'])
a2 = prim[prim.data_source == 'Social media']
show('Use-case A (variant): studies using social-media inputs', a2,
     ['study_id', 'first_author', 'year', 'disaster_type', 'performance_evidence'])
mac['ucAsocial'] = len(a2)

# --- Use-case B: studies that benchmark against a competing model ---------
b = prim[prim.performance_evidence == 'Comparative benchmark']
show('Use-case B: comparative benchmarks', b,
     ['study_id', 'first_author', 'year', 'disaster_type', 'metric_reported'])
mac['ucBcomparative'] = len(b)

# --- Use-case C: explicit uncertainty representation (rule R3) ------------
c = prim[prim.stochastic == '1']
show('Use-case C: explicit uncertainty representation', c,
     ['study_id', 'first_author', 'year', 'disaster_type'])
mac['ucCstochastic'] = len(c)

# --- Use-case D: field-validated (operationally deployed) studies ---------
d = prim[prim.deployment_status == 'Operational deployment']
show('Use-case D: operational deployment', d,
     ['study_id', 'first_author', 'year', 'journal', 'disaster_type'])
mac['ucDoperational'] = len(d)

open(os.path.join(ROOT, 'supplementary', 'S2_examples_output.txt'), 'w').write(
    '\n'.join(out) + '\n')
with open(os.path.join(ROOT, 'supplementary', 'S2_macros.tex'), 'w') as fh:
    for k, v in mac.items():
        fh.write('\\newcommand{\\%s}{%d}\n' % (k, v))
print(mac)
