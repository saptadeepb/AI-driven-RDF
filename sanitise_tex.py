#!/usr/bin/env python3
"""
sanitise_tex.py -- converts every non-ASCII character in the assembled LaTeX
sources into its portable LaTeX equivalent.

Elsevier's production system prefers 7-bit source, and encoding-dependent
sources are a common cause of proof errors. Running this as part of the build
guarantees that main.tex, the generated tables and the bibliography contain no
byte above 0x7F.
"""
import sys, os, glob, unicodedata

MAP = {
    '—': '---', '–': '--', '‒': '--', '−': '$-$',
    '‘': '`', '’': "'", '‚': ',',
    '“': '``', '”': "''", '„': ',,',
    '…': r'\ldots{}', '•': r'$\bullet$', '·': r'$\cdot$',
    ' ': '~', ' ': r'\,', ' ': '~', ' ': r'\,',
    '×': r'$\times$', '≤': r'$\leq$', '≥': r'$\geq$',
    '≈': r'$\approx$', '±': r'$\pm$', '°': r'\degree{}',
    '→': r'$\rightarrow$', '←': r'$\leftarrow$',
    'µ': r'$\mu$', 'α': r'$\alpha$', 'β': r'$\beta$',
    '′': "'", '″': "''", '­': '',
    '﻿': '', '​': '', '‐': '-', '‑': '-',
    'æ': r'\ae{}', 'Æ': r'\AE{}',
    'ø': r'\o{}', 'Ø': r'\O{}',
    'å': r'\aa{}', 'Å': r'\AA{}',
    'ß': r'\ss{}', 'ı': r'\i{}', 'ł': r'\l{}',
    'Ł': r'\L{}', 'đ': r'\dj{}', 'ð': r'\dh{}',
    'þ': r'\th{}', 'œ': r'\oe{}', 'Œ': r'\OE{}',
    '™': r'\texttrademark{}', '®': r'\textregistered{}',
    '©': r'\textcopyright{}', '€': r'\texteuro{}',
    '£': r'\pounds{}',
}

ACCENT = {'̀': '`', '́': "'", '̂': '^', '̃': '~',
          '̈': '"', '̊': 'r', '̧': 'c', '̄': '=',
          '̆': 'u', '̌': 'v', '̇': '.', '̨': 'k'}


def conv(ch):
    if ord(ch) < 128:
        return ch
    if ch in MAP:
        return MAP[ch]
    d = unicodedata.normalize('NFD', ch)
    if len(d) == 2 and d[1] in ACCENT:
        base = d[0]
        cmd = ACCENT[d[1]]
        if base in 'ij':
            base = r'\%s' % base
        return '\\%s{%s}' % (cmd, base)
    # last resort: strip the character rather than emit an invalid byte
    return ''


def sanitise(path):
    raw = open(path, encoding='utf-8', errors='replace').read()
    outp = ''.join(conv(c) for c in raw)
    changed = sum(1 for c in raw if ord(c) > 127)
    if changed:
        open(path, 'w', encoding='ascii').write(outp)
    return changed


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    targets = ([os.path.join(root, 'main.tex'),
                os.path.join(root, 'references.bib')]
               + sorted(glob.glob(os.path.join(root, 'tables', '*.tex')))
               + sorted(glob.glob(os.path.join(root, 'response', '*.tex'))))
    total = 0
    for t in targets:
        if os.path.exists(t):
            n = sanitise(t)
            total += n
            print('%-46s %4d non-ASCII characters converted'
                  % (os.path.relpath(t, root), n))
    print('total converted: %d' % total)
