#!/usr/bin/env python3
"""
xref_response.py -- rewrites the cross-references in response/response.tex so
that every pointer to the REVISED manuscript expands from a macro in
response/xref.tex (generated from main.aux), while every reference to the
ORIGINAL submission is left as the reviewer wrote it.

Protected (never rewritten):
  * anything between \begin{reviewer} and \end{reviewer} -- the reviewers'
    own words, quoted verbatim;
  * \comment{...} heading lines, which name the original figure/section the
    reviewer complained about;
  * sentences explicitly discussing "the original ...".
"""
import re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'response', 'response.tex')

# ordered: longest / most specific first
RULES = [
    (r'Section\s+3\.2\s+\(eligibility\)\s+and\s+3\.3\s+\(sources and strategy\)',
     r'Section~\\SecEligibility{} (eligibility) and \\SecSearch{} (sources and strategy)'),
    (r'Section\s+3\.2\s+\(Eligibility criteria\)',
     r'Section~\\SecEligibility{} (Eligibility criteria)'),
    (r'Section\s+3\.3\s+\(Information sources and search strategy\)',
     r'Section~\\SecSearch{} (Information sources and search strategy)'),
    (r'Sections\s+3\.2,\s+3\.3\s+and\s+3\.5',
     r'Sections~\\SecEligibility{}, \\SecSearch{} and \\SecSelection{}'),
    (r'Sections\s+3\.1--3\.5',
     r'Sections~\\SecProtocol{}--\\SecSelection{}'),
    (r'Sections\s+3\.7\s+and\s+10\s+\(L1\);\s+Section\s+9\.1',
     r'Sections~\\SecAppraisal{} and \\SecLimitations{} (L1); Section~\\SecFutureDir{}'),
    (r'Sections\s+3\.6,\s+3\.6\.1\s+and\s+3\.8',
     r'Sections~\\SecCharting{}, \\SecDenominators{} and \\SecRepro{}'),
    (r'Sections\s+3\.5\s+and\s+3\.6;\s+Figure\s+3',
     r'Sections~\\SecSelection{} and \\SecCharting{}; Figure~\\FigWorkflow{}'),
    (r'Section\s+3\.5\s+and\s+Figure\s+3',
     r'Sections~\\SecSelection{} and \\SecCharting{}; Figure~\\FigWorkflow{}'),
    (r'Section\s+3\.5\s+and\s+Figure\s+2',
     r'Section~\\SecSelection{} and Figure~\\FigPrisma{}'),
    (r'Sections\s+9\.1\s+and\s+9\.2',
     r'Sections~\\SecFutureDir{} and \\SecEmerging{}'),
    (r'Section\s+9\.1\s+\(Future research directions\)',
     r'Section~\\SecFutureDir{} (Future research directions)'),
    (r'Section\s+9\.2\s+\(Technological innovations and emerging trends\)',
     r'Section~\\SecEmerging{} (Technological innovations and emerging trends)'),
    (r'Section\s+9\.1\s+\(D2\)', r'Section~\\SecFutureDir{} (D2)'),
    (r'Sections\s+7\s+and\s+8',
     r'Sections~\\SecEfficacy{} and \\SecBottlenecks{}'),
    (r'Sections\s+7\.1--7\.4',
     r'Sections~\\SecHowmuch{}--\\SecClaims{}'),
    (r'Section\s+5\.7\s+and\s+Table\s+4',
     r'Section~\\SecCrosstab{} and Table~\\TabMethodHazard{}'),
    (r'Section\s+5\.8\s+and\s+Figure\s+12',
     r'Section~\\SecTurnover{} and Figure~\\FigOvertime{}'),
    (r'Section\s+5\.2\s+\(knowledge-based methods\)',
     r'Section~\\SecFamKb{} (knowledge-based methods)'),
    (r'Figures\s+11\s+and\s+12',
     r'Figures~\\FigHeatmap{} and \\FigOvertime{}'),
    (r'Figures\s+5\s+and\s+9',
     r'Figures~\\FigAuthorgeo{} and \\FigFocusgeo{}'),
    (r'Figure\s+11\s+and\s+Table\s+4',
     r'Figure~\\FigHeatmap{} and Table~\\TabMethodHazard{}'),
    (r'Section\s+3\.7\s+\(Critical appraisal\)',
     r'Section~\\SecAppraisal{} (Critical appraisal)'),
    (r'Section\s+10\s+\(L1\)', r'Section~\\SecLimitations{} (L1)'),
    (r'Section\s+10\s+\(L2\)', r'Section~\\SecLimitations{} (L2)'),
    (r'Section\s+10\s+\(L3\)', r'Section~\\SecLimitations{} (L3)'),
    (r'Section\s+10\s+states six limitations',
     r'Section~\\SecLimitations{} states six limitations'),
    (r'Section\s+8;\s+Sections\s+11\s+and\s+9\.1\.',
     r'Section~\\SecBottlenecks{}; Sections~\\SecManagerial{} and '
     r'\\SecFutureDir{}.'),
    (r'Section\s+11\s+and\s+Section\s+12',
     r'Section~\\SecManagerial{} and Section~\\SecConclusion{}'),
    (r'Section\s+3\.6\.1', r'Section~\\SecDenominators{}'),
    (r'Section\s+4\.2\.3', r'Section~\\SecCommercial{}'),
    (r'Section\s+3\.7', r'Section~\\SecAppraisal{}'),
    (r'Section\s+3\.1', r'Section~\\SecProtocol{}'),
    (r'Section\s+3\.3', r'Section~\\SecSearch{}'),
    (r'Section\s+3\.5\}', r'Section~\\SecSelection{}}'),
    (r'Section\s+3\.6\}', r'Section~\\SecCharting{}}'),
    (r'Section\s+5\.8', r'Section~\\SecTurnover{}'),
    (r'Section\s+6\.6', r'Section~\\SecParadigm{}'),
    (r'Section\s+7\.1', r'Section~\\SecHowmuch{}'),
    (r'Section\s+7\.2', r'Section~\\SecWhatreport{}'),
    (r'Section\s+7\.3', r'Section~\\SecDegradation{}'),
    (r'Section\s+7\.4', r'Section~\\SecClaims{}'),
    (r'Section\s+9\.1', r'Section~\\SecFutureDir{}'),
    (r'Section\s+9\.2', r'Section~\\SecEmerging{}'),
    (r'Section~7\b', r'Section~\\SecEfficacy{}'),
    (r'Section\s+8\b', r'Section~\\SecBottlenecks{}'),
    (r'Figure\s+15', r'Figure~\\FigEvidence{}'),
    (r'Figure\s+12', r'Figure~\\FigOvertime{}'),
    (r'Table\s+7', r'Table~\\TabIncluded{}'),
    (r'Table\s+6', r'Table~\\TabEfficacy{}'),
    (r'Table\s+5', r'Table~\\TabCoding{}'),
    (r'Table\s+4', r'Table~\\TabMethodHazard{}'),
    (r'Table\s+3', r'Table~\\TabMapping{}'),
    (r'Table\s+1', r'Table~\\TabSearch{}'),
]

# Context-sensitive: these bare numbers appear in both senses, so they are
# rewritten only inside the exact sentence in which they mean the revised
# manuscript.
EXACT = [
    ('Section 5 rewritten as a comparative synthesis',
     'Section~\\SecSynthesis{} rewritten as a comparative synthesis'),
    ('Figure 2 redrawn as a standard PRISMA-ScR diagram',
     'Figure~\\FigPrisma{} redrawn as a standard PRISMA-ScR diagram'),
    ('New Section~\\SecEfficacy{}, new Figure~\\FigEvidence{}',
     'New Section~\\SecEfficacy{}, new Figure~\\FigEvidence{}'),
    ('and Section 5 has been rewritten from scratch',
     'and Section~\\SecSynthesis{} has been rewritten from scratch'),
    ('\\where Section 5 in its entirety',
     '\\where Section~\\SecSynthesis{} in its entirety'),
    ('PRISMA-ScR flow diagram (now \\textbf{Figure 2})',
     'PRISMA-ScR flow diagram (now \\textbf{Figure~\\FigPrisma{}})'),
    ('\\where Figure 2.', '\\where Figure~\\FigPrisma{}.'),
    ('in the revised figure (now \\textbf{Figure 4})',
     'in the revised figure (now \\textbf{Figure~\\FigYear{}})'),
    ('\\where Figure 4; \\texttt{code/make\\_figures.py}.',
     '\\where Figure~\\FigYear{}; \\texttt{code/make\\_figures.py}.'),
    ('Both maps (now \\textbf{Figures 5 and 9})',
     'Both maps (now \\textbf{Figures~\\FigAuthorgeo{} and \\FigFocusgeo{}})'),
    ('itemised on Figure 2 and in Section 3.5 as',
     'itemised on Figure~\\FigPrisma{} and in Section~\\SecSelection{} as'),
    ('Figure 2 is a standard PRISMA-ScR flow diagram',
     'Figure~\\FigPrisma{} is a standard PRISMA-ScR flow diagram'),
    ('Figure 2; PRISMA-ScR checklist',
     'Figure~\\FigPrisma{}; PRISMA-ScR checklist'),
    ('in Table 1 and on\nFigure 2.', 'in Table~\\TabSearch{} and on\nFigure~\\FigPrisma{}.'),
    ('\\textbf{Figure 3} sets the workflow out',
     '\\textbf{Figure~\\FigWorkflow{}} sets the workflow out'),
    ('multi-label note (Figure 6)',
     'multi-label note (Figure~\\FigMethods{})'),
    ('Section 5 narrative did not appear',
     'Section~\\SecSynthesis{} narrative did not appear'),
]


def protected_spans(text):
    spans = []
    for m in re.finditer(r'\\begin\{reviewer\}.*?\\end\{reviewer\}',
                         text, re.S):
        spans.append(m.span())
    for m in re.finditer(r'\\comment\{[^}]*\}', text):
        spans.append(m.span())
    # sentences about the ORIGINAL submission
    for pat in [r'The original Figure 2 plotted[^.]*\.',
                r'the original Section 3\.2 was three sentences long',
                r'R1\.3 & Section 5 reads[^&]*&',
                r'R1\.6 & Figure 5 axis labels reversed &',
                r'R1\.8 & Section 7 subheadings not numbered &']:
        for m in re.finditer(pat, text, re.S):
            spans.append(m.span())
    return sorted(spans)


def apply_outside(text, fn):
    spans = protected_spans(text)
    out, pos = [], 0
    for a, b in spans:
        if a < pos:
            continue
        out.append(fn(text[pos:a]))
        out.append(text[a:b])
        pos = b
    out.append(fn(text[pos:]))
    return ''.join(out)


def main():
    text = open(SRC, encoding='utf-8').read()

    def rewrite(chunk):
        for old, new in EXACT:
            chunk = chunk.replace(old, new)
        for pat, rep in RULES:
            chunk = re.sub(pat, rep, chunk)
        return chunk

    new = apply_outside(text, rewrite)
    if '\\input{xref}' not in new:
        new = new.replace('\\begin{document}', '\\input{xref}\n\n\\begin{document}')
    open(SRC, 'w', encoding='utf-8').write(new)

    # report anything left un-macroed outside protected regions
    leftovers = []

    def scan(chunk):
        for m in re.finditer(
                r'(?<!\\)\b(Sections?|Figures?|Tables?)\s+\d+(\.\d+)*', chunk):
            leftovers.append(m.group(0))
        return chunk

    apply_outside(new, scan)
    print('cross-references rewritten in response/response.tex')
    if leftovers:
        print('REMAINING hard-coded references outside protected regions:')
        for l in sorted(set(leftovers)):
            print('   %s' % l)
    else:
        print('no hard-coded references remain outside quoted reviewer text')


if __name__ == '__main__':
    main()
