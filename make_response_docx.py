#!/usr/bin/env python3
"""
make_response_docx.py -- produces the Word version of the response letter.

Pandoc does not resolve \input{} files or user-defined macros, so a direct
conversion of response.tex silently drops every cross-reference. This script
therefore flattens the source first: it expands the xref macros to their
printed values, rewrites the custom environments into constructs pandoc
understands, and only then converts.

Output: response/response.docx  (and response/response_flat.tex, the flattened
intermediate, kept so the conversion is inspectable).
"""
import re, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *p: os.path.join(ROOT, 'response', *p)


def load_macros():
    macros = {}
    for line in open(R('xref.tex'), encoding='utf-8'):
        m = re.match(r'\\newcommand\{\\(\w+)\}\{([^}]*)\}', line)
        if m:
            macros[m.group(1)] = m.group(2)
    return macros


def flatten(text, macros):
    # 1. expand cross-reference macros, longest name first so that
    #    \SecFamStat is not clobbered by a shorter prefix
    for name in sorted(macros, key=len, reverse=True):
        text = text.replace('\\%s{}' % name, macros[name])
        text = re.sub(r'\\%s(?![A-Za-z])' % name, macros[name], text)

    # 2. custom environments -> quote blocks pandoc renders
    text = re.sub(r'\\begin\{reviewer\}(.*?)\\end\{reviewer\}',
                  lambda m: '\\begin{quote}\\textbf{Reviewer comment.}'
                            + m.group(1) + '\\end{quote}',
                  text, flags=re.S)
    text = re.sub(r'\\begin\{revised\}(.*?)\\end\{revised\}',
                  lambda m: '\\begin{quote}\\textbf{From the revised '
                            'manuscript:}' + m.group(1) + '\\end{quote}',
                  text, flags=re.S)

    # 3. custom commands -> headings and runs
    text = re.sub(r'\\comment\{([^}]*)\}', r'\\subsection*{\1}', text)
    text = text.replace('\\response ', '\n\n\\textbf{Response.} ')
    text = text.replace('\\where ', '\n\n\\textbf{Where to find it:} ')

    # 4. strip preamble machinery pandoc does not need
    drop = [r'\\usepackage(\[[^\]]*\])?\{(mdframed|titlesec|xcolor|geometry|'
            r'parskip|hyperref|enumitem|amssymb|graphicx|fontenc|longtable|'
            r'booktabs)\}',
            r'\\definecolor\{[^}]*\}\{[^}]*\}\{[^}]*\}',
            r'\\newmdenv\[[^\]]*\]\{\w+\}',
            r'\\newcommand\{\\(comment|response|where)\}(\[\d\])?\{[^}]*\}',
            r'\\titleformat\{[^}]*\}\{[^}]*\}\{[^}]*\}\{[^}]*\}\{[^}]*\}',
            r'\\hypersetup\{[^}]*\}',
            r'\\input\{xref\}']
    for d in drop:
        text = re.sub(d, '', text)
    text = re.sub(r'\\newcommand\{\\where\}\{[^}]*\{[^}]*\}[^}]*\}', '', text)
    text = re.sub(r'\\textcolor\{\w+\}\{([^{}]*)\}', r'\1', text)
    text = text.replace('\\clearpage', '\\newpage')
    text = re.sub(r'\\vspace\{[^}]*\}', '', text)
    text = re.sub(r'\\rule\{[^}]*\}\{[^}]*\}', '', text)
    text = text.replace('\\hrule', '')
    text = re.sub(r'\\begin\{minipage\}\{[^}]*\}\\centering', '', text)
    text = text.replace('\\end{minipage}', '')
    text = re.sub(r'\\begin\{enumerate\}\[[^\]]*\]', r'\\begin{enumerate}',
                  text)
    text = re.sub(r'\\begin\{itemize\}\[[^\]]*\]', r'\\begin{itemize}', text)
    return text


def main():
    src = open(R('response.tex'), encoding='utf-8').read()
    flat = flatten(src, load_macros())
    open(R('response_flat.tex'), 'w', encoding='utf-8').write(flat)

    cmd = ['pandoc', R('response_flat.tex'), '-o', R('response.docx'),
           '--from=latex', '--to=docx', '--toc', '--toc-depth=2',
           '--metadata', 'title=Response to Reviewers -- SASC-D-26-00151']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        print(res.stderr[:2000])
        sys.exit('pandoc failed')

    # sanity check: did the cross-references survive?
    import zipfile
    x = zipfile.ZipFile(R('response.docx')).read(
        'word/document.xml').decode('utf-8')
    body = re.sub(r'<[^>]+>', '', x)
    checks = ['Where to find it', 'Reviewer comment',
              'From the revised manuscript']
    missing = [c for c in checks if c not in body]
    stray = re.findall(r'\\[A-Za-z]{3,}', body)
    print('response.docx written (%d characters of text)' % len(body))
    for c in checks:
        print('   %-32s %s' % (c, 'present' if c in body else 'MISSING'))
    if stray:
        print('   unexpanded commands: %s' % sorted(set(stray))[:10])
    if missing:
        sys.exit(1)


if __name__ == '__main__':
    main()
