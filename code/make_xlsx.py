#!/usr/bin/env python3
"""
make_xlsx.py -- exports the master extraction dataset as a formatted Excel
workbook for reviewers and co-authors who prefer a spreadsheet to the CSV.

Sheets:
  Master extraction   -- one row per included source, all 28 charted variables
  Codebook            -- variable definitions and allowed values
  Coding rules        -- the derived-variable rules R1-R6
  Summary statistics  -- the distributions reported in the manuscript, computed
                         by live formulas over the Master extraction sheet so
                         that the workbook recalculates if a row is edited
  Efficacy evidence   -- the extracted comparative performance results

The CSV remains the canonical file; this workbook is a convenience view.
"""
import csv, json, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, 'data', *p)

HDR_FILL = PatternFill('solid', fgColor='1F5C99')
HDR_FONT = Font(name='Arial', size=10, bold=True, color='FFFFFF')
BODY = Font(name='Arial', size=10)
BOLD = Font(name='Arial', size=10, bold=True)
TITLE = Font(name='Arial', size=12, bold=True, color='1F5C99')
NOTE = Font(name='Arial', size=9, italic=True, color='5A5F66')
THIN = Side(style='thin', color='D9D9D9')
BOX = Border(bottom=THIN)


def style_header(ws, row=1, ncols=None):
    ncols = ncols or ws.max_column
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HDR_FILL
        cell.font = HDR_FONT
        cell.alignment = Alignment(vertical='center', wrap_text=True)
    ws.row_dimensions[row].height = 34
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def widths(ws, spec):
    for i, w in enumerate(spec, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def main():
    rows = list(csv.reader(open(D('master_extraction.csv'),
                                encoding='ascii')))
    header, body = rows[0], rows[1:]
    S = json.load(open(D('stats.json')))

    wb = Workbook()

    # ---------------------------------------------------- master extraction
    ws = wb.active
    ws.title = 'Master extraction'
    ws.append(header)
    # Columns that must be written as NUMBERS, not text: csv.reader yields
    # strings for everything, and a COUNTIF/SUMIFS over text silently returns
    # zero while still recalculating without error.
    NUMCOLS = {3, 4} | set(range(12, 18)) | {21, 22}      # 0-indexed
    for r in body:
        ws.append([int(v) if i in NUMCOLS and v.lstrip('-').isdigit() else v
                   for i, v in enumerate(r)])
    style_header(ws)
    widths(ws, [8, 30, 16, 7, 6, 10, 15, 16, 14, 30, 26, 18,
                8, 6, 6, 9, 9, 8, 14, 13, 11, 9, 9, 20, 20, 18, 16, 60])
    for r in range(2, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            ws.cell(row=r, column=c).font = BODY
            ws.cell(row=r, column=c).alignment = Alignment(vertical='top')
        ws.cell(row=r, column=28).alignment = Alignment(vertical='top',
                                                        wrap_text=True)
    ws.auto_filter.ref = 'A1:%s%d' % (get_column_letter(ws.max_column),
                                      ws.max_row)
    last = ws.max_row

    # ---------------------------------------------------------- codebook
    cb = wb.create_sheet('Codebook')
    cb.append(['Variable', 'Type', 'Allowed values / definition'])
    DEF = [
        ('study_id', 'ID', 'S001 ... , assigned in chronological order'),
        ('citekey', 'text', 'BibTeX key in references.bib'),
        ('first_author', 'text', 'surname of the first author'),
        ('year', 'integer', '2007-2026'),
        ('wave', 'integer',
         '1 = original search (to January 2024); 2 = updated search '
         '(January 2024 - August 2026)'),
        ('study_type', 'category', 'Primary; Review'),
        ('author_country', 'text',
         'country of the first author\'s affiliation; "Not reported" where it '
         'could not be extracted'),
        ('focus_country', 'text',
         'case-study setting; "Global" where not country-specific'),
        ('publisher', 'category',
         'Elsevier; Springer; IEEE; Wiley; Taylor & Francis; MDPI; Emerald; '
         'Other'),
        ('journal', 'text', 'publication outlet'),
        ('objective', 'category',
         'Predictive modelling and forecasting; Disaster preparedness and '
         'relief planning; Healthcare and medical service demand; '
         'Humanitarian logistics and supply chain management; Dynamic and '
         'adaptive demand estimation; Methodological or technology review'),
        ('disaster_type', 'category',
         'Multi-hazard/General; Earthquake; Flood; Hurricane/Cyclone; '
         'Biological/Epidemic; Wildfire; Drought/Food insecurity; '
         'Conflict/Displacement; Technological/Other; Not reported'),
        ('mf_statistical', '0/1',
         'MULTI-LABEL. ARIMA, exponential smoothing, regression, Bayesian, '
         'time series, econometric'),
        ('mf_ml', '0/1',
         'MULTI-LABEL. Trees, random forest, SVM, k-NN, boosting, ensembles'),
        ('mf_dl', '0/1',
         'MULTI-LABEL. ANN, MLP, CNN, RNN, LSTM, transformer, GNN, deep RL'),
        ('mf_knowledge', '0/1',
         'MULTI-LABEL. Case-based and rule-based reasoning, fuzzy, rough and '
         'grey systems'),
        ('mf_optsim', '0/1',
         'MULTI-LABEL. Mathematical programming, metaheuristics, simulation, '
         'agent-based models'),
        ('mf_genai', '0/1',
         'MULTI-LABEL. Large language models, retrieval-augmented generation, '
         'generative models'),
        ('learning_paradigm', 'category',
         'Supervised; Unsupervised; Both; Reinforcement; Not applicable; '
         'Not reported'),
        ('horizon', 'category',
         'Short-term; Long-term; Short-to-long; Dynamic/real-time; '
         'Not reported'),
        ('linearity', 'category', 'Linear; Non-linear; Combined; Not reported'),
        ('sustainability', '0/1',
         'rule R4: an environmental, equity or resilience objective is '
         'explicitly stated'),
        ('stochastic', '0/1',
         'rule R3: the reported method explicitly represents uncertainty'),
        ('performance_evidence', 'category',
         'rule R5: Comparative benchmark; Single-model metric; '
         'Qualitative/none; Not reported; Not applicable (review)'),
        ('metric_reported', 'text',
         'verbatim metric name(s) where known'),
        ('deployment_status', 'category',
         'rule R6: Operational deployment; Real-data case study; '
         'Synthetic/illustrative; Not reported'),
        ('data_source', 'category',
         'Historical records; Social media; Satellite/GIS; Survey/interview; '
         'Simulation; Mixed; Not reported'),
        ('coding_note', 'text',
         'free text: dominant-category decisions, provenance, evidence grade'),
    ]
    for d in DEF:
        cb.append(list(d))
    style_header(cb)
    widths(cb, [24, 12, 110])
    for r in range(2, cb.max_row + 1):
        for c in range(1, 4):
            cb.cell(row=r, column=c).font = BODY
            cb.cell(row=r, column=c).alignment = Alignment(vertical='top',
                                                           wrap_text=True)
    cb.append([])
    cb.append(['DENOMINATOR RULE', '',
               'N_all = all included sources, used for bibliographic '
               'variables. N_prim = primary studies only, used for every '
               'variable describing a method or its evidence. A source that '
               'does not report a variable is EXCLUDED from that variable\'s '
               'denominator rather than counted in a residual category.'])
    cb.cell(row=cb.max_row, column=1).font = BOLD
    cb.cell(row=cb.max_row, column=3).font = BODY
    cb.cell(row=cb.max_row, column=3).alignment = Alignment(vertical='top',
                                                            wrap_text=True)
    cb.append(['MULTI-LABEL RULE', '',
               'The six mf_* flags are multi-label: a hybrid study scores on '
               'every family it employs, so their percentages sum to more '
               'than 100% and are never a partition. All other variables are '
               'mutually exclusive.'])
    cb.cell(row=cb.max_row, column=1).font = BOLD
    cb.cell(row=cb.max_row, column=3).font = BODY
    cb.cell(row=cb.max_row, column=3).alignment = Alignment(vertical='top',
                                                            wrap_text=True)

    # ------------------------------------------------- summary statistics
    st = wb.create_sheet('Summary statistics')
    st['A1'] = 'Summary statistics'
    st['A1'].font = TITLE
    st['A2'] = ('Every value below is computed by a live formula over the '
                '"Master extraction" sheet. Editing a row there updates these '
                'figures, so the workbook stays self-consistent.')
    st['A2'].font = NOTE
    st.merge_cells('A2:F2')

    MX = "'Master extraction'"
    r = 4
    st.cell(row=r, column=1, value='Corpus').font = BOLD
    r += 1
    st.append([])
    hdr_row = r
    for i, h in enumerate(['Quantity', 'Count', 'Denominator', 'Per cent'], 1):
        st.cell(row=hdr_row, column=i, value=h)
    style_header(st, row=hdr_row, ncols=4)
    st.freeze_panes = None
    r = hdr_row + 1

    def line(label, formula_n, denom_formula=None):
        nonlocal r
        st.cell(row=r, column=1, value=label).font = BODY
        st.cell(row=r, column=2, value=formula_n).font = BODY
        if denom_formula:
            st.cell(row=r, column=3, value=denom_formula).font = BODY
            st.cell(row=r, column=4,
                    value='=IF(C%d=0,"",B%d/C%d)' % (r, r, r)).font = BODY
            st.cell(row=r, column=4).number_format = '0.0%'
        r += 1

    N_ALL = '=COUNTA(%s!A2:A%d)' % (MX, last)
    N_PRIM = '=COUNTIF(%s!F2:F%d,"Primary")' % (MX, last)
    line('All included sources (N_all)', N_ALL)
    line('Primary studies (N_prim)', N_PRIM)
    line('Review articles', '=COUNTIF(%s!F2:F%d,"Review")' % (MX, last))
    line('Wave 1 (original search)', '=COUNTIF(%s!E2:E%d,1)' % (MX, last))
    line('Wave 2 (updated search)', '=COUNTIF(%s!E2:E%d,2)' % (MX, last))
    line('Published 2023 or later',
         '=COUNTIF(%s!D2:D%d,">=2023")' % (MX, last), N_ALL)

    r += 1
    st.cell(row=r, column=1,
            value='Method families (MULTI-LABEL; denominator N_prim; '
                  'percentages sum to more than 100%)').font = BOLD
    r += 1
    FAM = [('Statistical / time series', 'M'), ('Classical machine learning', 'N'),
           ('Deep learning / neural', 'O'),
           ('Knowledge-based (CBR, RBR, fuzzy, grey)', 'P'),
           ('Optimisation / simulation', 'Q'), ('Generative AI / LLM', 'R')]
    for label, col in FAM:
        line(label,
             '=SUMIFS(%s!%s2:%s%d,%s!F2:F%d,"Primary")'
             % (MX, col, col, last, MX, last), N_PRIM)

    r += 1
    st.cell(row=r, column=1,
            value='Evidence of efficacy (denominator N_prim)').font = BOLD
    r += 1
    for label, val in [('Comparative benchmark', 'Comparative benchmark'),
                       ('Single-model metric', 'Single-model metric'),
                       ('Qualitative / none', 'Qualitative/none'),
                       ('Not reported', 'Not reported')]:
        line(label,
             '=COUNTIFS(%s!F2:F%d,"Primary",%s!X2:X%d,"%s")'
             % (MX, last, MX, last, val), N_PRIM)

    r += 1
    st.cell(row=r, column=1,
            value='Deployment status (denominator N_prim)').font = BOLD
    r += 1
    for label in ['Operational deployment', 'Real-data case study',
                  'Synthetic/illustrative', 'Not reported']:
        line(label,
             '=COUNTIFS(%s!F2:F%d,"Primary",%s!Z2:Z%d,"%s")'
             % (MX, last, MX, last, label), N_PRIM)

    r += 1
    st.cell(row=r, column=1,
            value='Uncertainty and sustainability (denominator N_prim)'
            ).font = BOLD
    r += 1
    line('Uncertainty explicitly represented (rule R3)',
         '=SUMIFS(%s!W2:W%d,%s!F2:F%d,"Primary")' % (MX, last, MX, last),
         N_PRIM)
    line('Sustainability or equity objective (rule R4)',
         '=SUMIFS(%s!V2:V%d,%s!F2:F%d,"Primary")' % (MX, last, MX, last),
         N_PRIM)

    widths(st, [46, 12, 14, 12])

    r += 2
    st.cell(row=r, column=1,
            value='Values published in the manuscript, for comparison '
                  '(computed by code/compute_stats.py):').font = BOLD
    r += 1
    for label, v in [('N_all', S['N_all']), ('N_prim', S['N_prim']),
                     ('studies combining two or more families',
                      '%d (%.1f%%)' % (S['n_hybrid'], S['pct_hybrid'])),
                     ('comparative benchmark',
                      '%d (%.1f%%)' % (S['n_comparative'],
                                       S['pct_comparative'])),
                     ('operational deployment',
                      '%d (%.1f%%)' % (S['n_operational'],
                                       S['pct_operational']))]:
        st.cell(row=r, column=1, value=label).font = NOTE
        st.cell(row=r, column=2, value=str(v)).font = NOTE
        r += 1

    # ------------------------------------------------- efficacy evidence
    ef = wb.create_sheet('Efficacy evidence')
    with open(D('efficacy_evidence.csv'), encoding='utf-8') as fh:
        for i, row in enumerate(csv.reader(fh)):
            ef.append(row)
    style_header(ef)
    widths(ef, [30, 16, 7, 26, 12, 12, 34, 34, 20, 60, 24, 22, 14, 40])
    for rr in range(2, ef.max_row + 1):
        for c in range(1, ef.max_column + 1):
            ef.cell(row=rr, column=c).font = BODY
            ef.cell(row=rr, column=c).alignment = Alignment(vertical='top',
                                                            wrap_text=True)

    out = D('master_extraction.xlsx')
    wb.save(out)
    print('wrote %s' % os.path.relpath(out, ROOT))
    print('  Master extraction : %d data rows x %d variables'
          % (last - 1, len(header)))
    print('  Codebook          : %d variable definitions' % len(DEF))
    print('  Summary statistics: live formulas over the master sheet')
    print('  Efficacy evidence : %d rows' % (ef.max_row - 1))


if __name__ == '__main__':
    main()
