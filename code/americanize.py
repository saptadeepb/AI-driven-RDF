#!/usr/bin/env python3
"""americanize.py -- converts British to American spelling in prose files.

Usage: americanize.py FILE [FILE ...]   (edits in place; prints counts)

Only whole words from the explicit map below are changed. LaTeX arguments
that are keys or paths (cite, ref, label, input, url, includegraphics,
begin/end) are protected, as are reviewer quotations in the response
letter (reviewer environments), so that quoted text stays verbatim.
"""
import re, sys

STEMS = {
    'harmonis': 'harmoniz', 'organis': 'organiz', 'optimis': 'optimiz',
    'summaris': 'summariz', 'itemis': 'itemiz', 'standardis': 'standardiz',
    'characteris': 'characteriz', 'synthesis': 'synthesiz', 'penalis': 'penaliz',
    'hybridis': 'hybridiz', 'generalis': 'generaliz', 'recognis': 'recogniz',
    'realis': 'realiz', 'mobilis': 'mobiliz', 'materialis': 'materializ',
    'monetis': 'monetiz', 'prioritis': 'prioritiz', 'emphasis': 'emphasiz',
    'operationalis': 'operationaliz', 'utilis': 'utiliz', 'minimis': 'minimiz',
    'maximis': 'maximiz', 'categoris': 'categoriz', 'conceptualis': 'conceptualiz',
    'contextualis': 'contextualiz', 'digitis': 'digitiz', 'formalis': 'formaliz',
    'normalis': 'normaliz', 'parameteris': 'parameteriz', 'visualis': 'visualiz',
    'stabilis': 'stabiliz', 'specialis': 'specializ', 'localis': 'localiz',
    'internalis': 'internaliz', 'institutionalis': 'institutionaliz',
    'centralis': 'centraliz', 'decentralis': 'decentraliz', 'criticis': 'criticiz',
    'scrutinis': 'scrutiniz', 'operationalis': 'operationaliz', 'randomis': 'randomiz',
    'initialis': 'initializ', 'finalis': 'finaliz', 'analys': 'analyz',
}
# endings that may follow a -ise/-yse stem
ENDS = ['e', 'es', 'ed', 'ing', 'ation', 'ations', 'ational', 'ationally', 'er', 'ers']
WORDS = {
    'modelling': 'modeling', 'modelled': 'modeled', 'modeller': 'modeler',
    'labelled': 'labeled', 'labelling': 'labeling', 'travelled': 'traveled',
    'cancelled': 'canceled', 'signalled': 'signaled', 'fuelled': 'fueled',
    'favour': 'favor', 'favours': 'favors', 'favoured': 'favored',
    'favourable': 'favorable', 'favourably': 'favorably', 'unfavourable': 'unfavorable',
    'behaviour': 'behavior', 'behaviours': 'behaviors', 'behavioural': 'behavioral',
    'neighbour': 'neighbor', 'neighbours': 'neighbors', 'neighbouring': 'neighboring',
    'colour': 'color', 'colours': 'colors', 'labour': 'labor', 'honour': 'honor',
    'centre': 'center', 'centres': 'centers', 'metre': 'meter', 'metres': 'meters',
    'programme': 'program', 'programmes': 'programs', 'analogue': 'analog',
    'catalogue': 'catalog', 'catalogues': 'catalogs', 'defence': 'defense',
    'licence': 'license', 'judgement': 'judgment', 'judgements': 'judgments',
    'whilst': 'while', 'amongst': 'among', 'towards': 'toward',
    'acknowledgement': 'acknowledgment', 'enrol': 'enroll', 'fulfil': 'fulfill',
    'ageing': 'aging', 'artefact': 'artifact', 'artefacts': 'artifacts',
    'learnt': 'learned', 'apologise': 'apologize', 'apologised': 'apologized',
    'analogues': 'analogs', 'neighbourhood': 'neighborhood', 'grey': 'gray',
}
# 'grey' is a technical term (grey systems, grey model): keep it.
WORDS.pop('grey')
for s, a in STEMS.items():
    for e in ENDS:
        WORDS[s + e] = a + e
# false friends: words that legitimately end in -is(e) etc.
for k in ('synthesis', 'synthesise', 'emphasis', 'analyse'):
    pass
WORDS.pop('synthesise', None); WORDS['synthesise'] = 'synthesize'
WORDS['synthesised'] = 'synthesized'; WORDS['synthesises'] = 'synthesizes'
WORDS['synthesising'] = 'synthesizing'
for k in ('synthesis', 'synthesiser'):  # noun stays
    WORDS.pop(k, None)
WORDS.pop('emphasis', None)
WORDS['emphasise'] = 'emphasize'; WORDS['emphasised'] = 'emphasized'
WORDS['emphasises'] = 'emphasizes'
for k in list(WORDS):
    if k.startswith('emphasis') and k not in ('emphasise', 'emphasised', 'emphasises'):
        WORDS.pop(k)
    if k.startswith('synthesis') and k not in ('synthesised', 'synthesises', 'synthesising'):
        WORDS.pop(k)
WORDS['analyse'] = 'analyze'; WORDS['analysed'] = 'analyzed'
WORDS['analyses'] = 'analyses'  # noun plural: unchanged
WORDS['analysing'] = 'analyzing'

PROTECT = re.compile(
    r'\\begin\{reviewer\}.*?\\end\{reviewer\}'
    r'|```.*?```|\\begin\{(?:Verbatim|verbatim|lstlisting)\}.*?\\end\{(?:Verbatim|verbatim|lstlisting)\}|'
    r'\\(?:cite[tp]?\*?|citeauthor|citeyear|ref|eqref|label|input|include|url|href|'
    r'includegraphics|begin|end|bibliography(?:style)?|newcommand|renewcommand|'
    r'graphicspath|usepackage|documentclass)(?:\[[^\]]*\])*\{[^}]*\}'
    r'|https?://\S+|`[^`\n]*`|\[[^\]\n]*\]\([^)\n]*\)', re.S)
# proper names (journal titles) keep their published spelling
import csv as _csv, os as _os
_OT = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                    'data', 'outlet_titles.csv')
_NAMES = set()
if _os.path.exists(_OT):
    for _r in _csv.DictReader(open(_OT, encoding='utf-8')):
        for _k in ('journal_in_dataset', 'full_title'):
            _NAMES.add(_r[_k].replace('&', r'\&'))
            _NAMES.add(_r[_k])
_NAMES = sorted((n for n in _NAMES if n), key=len, reverse=True)
if _NAMES:
    PROTECT = re.compile(PROTECT.pattern + '|' + '|'.join(re.escape(n) for n in _NAMES), re.S)
WORD = re.compile(r'(?<![\\A-Za-z0-9_/.])([A-Za-z]+)(?![A-Za-z0-9_])')


def fix_word(m):
    w = m.group(1)
    low = w.lower()
    if low not in WORDS or WORDS[low] == low:
        return w
    a = WORDS[low]
    if w.isupper():
        return a.upper()
    if w[0].isupper():
        return a[0].upper() + a[1:]
    return a


def convert(text):
    out, pos, n = [], 0, 0
    for m in PROTECT.finditer(text):
        seg = text[pos:m.start()]
        new = WORD.sub(fix_word, seg)
        n += sum(1 for a, b in zip(WORD.findall(seg), WORD.findall(new)) if a != b)
        out += [new, m.group(0)]
        pos = m.end()
    seg = text[pos:]
    new = WORD.sub(fix_word, seg)
    n += sum(1 for a, b in zip(WORD.findall(seg), WORD.findall(new)) if a != b)
    out.append(new)
    return ''.join(out), n


if __name__ == '__main__':
    for f in sys.argv[1:]:
        t = open(f, encoding='utf-8').read()
        new, n = convert(t)
        if new != t:
            open(f, 'w', encoding='utf-8').write(new)
        print('%-50s %d words' % (f, n))
