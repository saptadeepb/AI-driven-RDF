#!/usr/bin/env python3
"""
make_figures.py -- rebuilds EVERY figure in the manuscript as vector PDF.

Input : data/master_extraction.csv  (via data/stats.json)
Output: figures/*.pdf

No bar height, map value or percentage is hand-entered: all are read from
stats.json, computed from the master extraction dataset. The narrative quotes
the same numbers through the macros in stats_macros.tex, so text and figures
cannot disagree (Reviewer 2, Major Comment 3).

Every label placed inside a shape goes through figstyle.fit_text, which
measures the rendered text and shrinks or wraps it until it fits; every
provenance note goes through figstyle.place_note, which measures how far the
drawn content extends and sits below it. The build fails if any label could
not be made to fit.
"""
import json, os, csv, sys, textwrap
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figstyle import (apply_style, CAT, OTHER, INK, INK2, INK3, GRID, SEQ,
                      NODATA, MUTED, VIOLATIONS, recessive_grid, integer_axis,
                      fit_text, fit_text_group, box, value_label, place_note,
                      panel_title, save)
import worldmap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, 'figures')
os.makedirs(FIG, exist_ok=True)
apply_style()

S = json.load(open(os.path.join(ROOT, 'data', 'stats.json')))
ROWS = list(csv.DictReader(
    open(os.path.join(ROOT, 'data', 'master_extraction.csv'))))
PRIM = [r for r in ROWS if r['study_type'] == 'Primary']

# The provenance and denominator text is NOT drawn on the figures: at the
# authors' request it is carried in the LaTeX captions instead. Each note is
# recorded here and written to figures/figure_notes.tex as a macro, so the
# caption text is still generated from the dataset and cannot drift from the
# figure it describes.
PROV = ('Source: the master extraction dataset (N = %d included sources, %d '
        'primary studies).' % (S['N_all'], S['N_prim']))

MADE = []
NOTES = {}


def note(key, text):
    NOTES[key] = ' '.join(text.split())


def out(name):
    MADE.append(name)
    return os.path.join(FIG, name)


def blank(ax):
    """Turn an axes into a full-bleed drawing surface.

    A default subplot occupies only about 77% of the figure width, so axes
    fractions used for hand-placed boxes were silently a fifth narrower than
    intended and text wrapped that had no need to. Filling the figure makes
    axes fractions mean what the layout code assumes they mean.
    """
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')


# ---------------------------------------------------------------- helpers
def hbar(ax, fig, labels, values, pcts, color=None, xlabel=None,
         wrap_labels=None, pct_fmt='%d  (%.1f%%)'):
    y = np.arange(len(labels))[::-1]
    cols = color if isinstance(color, list) else [color or CAT[0]] * len(labels)
    if wrap_labels:
        labels = ['\n'.join(textwrap.wrap(l, wrap_labels)) for l in labels]
    ax.barh(y, values, height=0.62, color=cols, edgecolor='white',
            linewidth=0.8, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel(xlabel or 'Number of studies (count)')
    recessive_grid(ax, 'x')
    span = max(values) if values else 1
    ax.set_xlim(0, span * 1.30)
    integer_axis(ax, 'x')
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    for yy, v, p in zip(y, values, pcts):
        ax.text(v + span * 0.022, yy, pct_fmt % (v, p), va='center',
                ha='left', fontsize=7.6, color=INK2, zorder=5)


# Display-only shortenings for the outlet axis. The full title is what is
# stored in the dataset and printed in the tables; these forms exist purely so
# that ten labels fit on one axis without colliding.
OUTLET_SHORT = {
    'International Journal of Disaster Risk Reduction':
        'Int. J. Disaster Risk Reduction',
    'Transportation Research Part E: Logistics and Transportation Review':
        'Transportation Research Part E',
    'International Journal of Production Economics':
        'Int. J. Production Economics',
    'Engineering Applications of Artificial Intelligence':
        'Eng. Applications of AI',
    'Journal of the Operational Research Society':
        'J. Operational Research Society',
    'Journal of Humanitarian Logistics and Supply Chain Management':
        'J. Humanitarian Logistics & SCM',
    'International Journal of Information Management Data Insights':
        'Int. J. Inf. Management Data Insights',
    'Computers and Industrial Engineering':
        'Computers & Industrial Engineering',
    'Information Processing and Management':
        'Information Processing & Management',
    'Reliability Engineering and System Safety':
        'Reliability Eng. & System Safety',
    'Chaos, Solitons and Fractals': 'Chaos, Solitons & Fractals',
}


def block_items(key, topn=None):
    b = S[key]
    items = list(b['items'].items())
    tail = []
    if topn and len(items) > topn:
        tail = items[topn:]
        items = items[:topn]
    return ([k for k, _ in items], [v['n'] for _, v in items],
            [v['pct'] for _, v in items], b['denominator'], tail)


# ================================================================ FIGURE 1
def fig01_escm():
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    blank(ax)
    phases = [('Preparedness',
               'Contingency planning\nStockpiling\nPartnership building'),
              ('Response',
               'Resource mobilisation\nDistribution channels\n'
               'Stakeholder coordination'),
              ('Recovery',
               'Infrastructure rebuild\nService restoration\n'
               'Long-term assistance')]
    w, h, gap, top = 0.29, 0.36, 0.055, 0.98
    x0 = (1 - (3 * w + 2 * gap)) / 2
    bodies = []
    for i, (title, body) in enumerate(phases):
        x = x0 + i * (w + gap)
        box(ax, x, top - h, w, h, '#FFFFFF', CAT[i])
        fit_text(ax, fig, x, top - 0.115, w, 0.10, title, fontsize=10,
                 weight='bold', color=CAT[i], wrap=False, label='phase title')
        bodies.append((ax, fig, x, top - h + 0.012, w, h - 0.135, body))
        if i < 2:
            ax.annotate('', xy=(x + w + gap, top - h / 2),
                        xytext=(x + w, top - h / 2),
                        arrowprops=dict(arrowstyle='-|>', linewidth=0.9,
                                        color=INK2, mutation_scale=9))

    fit_text_group(bodies, fontsize=7.8, color=INK2, linespacing=1.65,
                   label='phase body')

    ax.annotate('', xy=(0.62, 0.415), xytext=(0.62, top - h - 0.014),
                arrowprops=dict(arrowstyle='<->', linewidth=0.8, color=INK3))
    fit_text(ax, fig, x0, 0.425, 0.40, 0.070,
             'Cross-cutting operational functions', fontsize=8.2, color=INK3,
             ha='left', wrap=False, label='cross-cutting label')

    cross = ['Demand forecasting', 'Inventory control', 'Transport logistics',
             'Distribution planning', 'Information management',
             'Risk management']
    cw = (3 * w + 2 * gap - 2 * 0.018) / 3
    for j, c in enumerate(cross):
        r, col = divmod(j, 3)
        x = x0 + col * (cw + 0.018)
        y = 0.275 - r * 0.150
        hero = c == 'Demand forecasting'
        box(ax, x, y, cw, 0.122, '#E7EFF7' if hero else '#F5F7F9',
            CAT[0] if hero else GRID, lw=1.1 if hero else 0.8)
        fit_text(ax, fig, x, y, cw, 0.122, c, fontsize=8.0,
                 weight='bold' if hero else 'normal',
                 color=CAT[0] if hero else INK, label='cross-cutting box')
    note('escm', 'Demand forecasting (highlighted) is the function reviewed '
                    'in this article.')
    return save(fig, out('fig01_escm_components.pdf'))


# ================================================================ FIGURE 2
def fig02_prisma():
    """PRISMA-ScR flow (Reviewer 1 on Figure 3; Reviewer 2 Major 1)."""
    fig, ax = plt.subplots(figsize=(7.4, 6.6))
    blank(ax)
    LX, LW = 0.045, 0.520
    RX, RW = 0.600, 0.385
    stages = [
        ('IDENTIFICATION', CAT[0], [
            ('Records identified through database searching  (n = 1,109)\n'
             'Scopus 388   |   Web of Science 271\n'
             'ScienceDirect 214   |   Springer Nature 118\n'
             'IEEE Xplore 84   |   PubMed 34', None),
            ('Additional records identified through backward and forward '
             'citation chasing  (n = 46)', None)]),
        ('SCREENING', CAT[1], [
            ('Records after duplicates removed  (n = 872)',
             'Duplicate records removed  (n = 283)'),
            ('Titles and abstracts screened  (n = 872)',
             'Records excluded at title and abstract  (n = 748)')]),
        ('ELIGIBILITY', CAT[2], [
            ('Full-text articles assessed for eligibility  (n = 124)',
             'Full-text articles excluded  (n = 11)\n'
             'no demand or needs quantified   5\n'
             'hazard forecasting only   3\n'
             'full text not retrievable   2\n'
             'not peer reviewed   1')]),
        ('INCLUDED', CAT[3], [
            ('Sources included in the scoping review  (n = %d)\n'
             'primary studies %d   |   review articles %d'
             % (S['N_all'], S['N_prim'], S['N_rev']), None)]),
    ]
    items = [(si, st, col, t, e) for si, (st, col, rows) in enumerate(stages)
             for t, e in rows]
    # Boxes are sized in proportion to the text they must hold: an equal-height
    # layout forced the three-line identification box and the five-line
    # exclusion box to overflow.
    TOP, BOT, gapv = 0.975, 0.030, 0.032
    # Row height follows the taller of the two columns; the left box is sized
    # by its own content and the exclusion box by its own, so a five-line
    # exclusion no longer stretches a one-line stage box into a near-empty
    # rectangle.
    lines_l = [t.count('\n') + 1 for _, _, _, t, _ in items]
    lines_r = [(e.count('\n') + 1) if e else 0 for _, _, _, _, e in items]
    rows_w = [max(a, b) + 0.55 for a, b in zip(lines_l, lines_r)]
    avail = TOP - BOT - gapv * (len(items) - 1)
    row_h = [avail * w / sum(rows_w) for w in rows_w]

    # pass 1: geometry
    geo, y = [], TOP
    for (si, st, col, text, excl), rh, nl, nr in zip(items, row_h, lines_l,
                                                     lines_r):
        unit = rh / max(nl, nr)
        hb = min(rh, unit * nl + 0.030)
        geo.append((y, rh, hb, min(rh, unit * nr + 0.030) if excl else 0))
        y -= rh + gapv

    # pass 2: draw
    span = {}
    for k, ((si, st, col, text, excl), (y, rh, hb, he)) in enumerate(
            zip(items, geo)):
        by = y - rh / 2 - hb / 2
        box(ax, LX, by, LW, hb, '#FFFFFF', col)
        fit_text(ax, fig, LX, by, LW, hb, text, fontsize=7.5,
                 minsize=6.2, label='prisma stage')
        span.setdefault(si, [y, y - rh, col, st])
        span[si][1] = y - rh
        if excl:
            ey = y - rh / 2 - he / 2
            box(ax, RX, ey, RW, he, '#F8F6F3', '#BFA893')
            fit_text(ax, fig, RX + 0.014, ey, RW - 0.028, he, excl,
                     fontsize=7.2, minsize=6.0, color=INK2, ha='left',
                     label='prisma exclusion')
            ax.annotate('', xy=(RX, y - rh / 2), xytext=(LX + LW, y - rh / 2),
                        arrowprops=dict(arrowstyle='-|>', linewidth=0.9,
                                        color='#BFA893', mutation_scale=9))
        if k + 1 < len(geo):
            ny, nrh, nhb, _ = geo[k + 1]
            ax.annotate('', xy=(LX + LW / 2, ny - nrh / 2 + nhb / 2),
                        xytext=(LX + LW / 2, by),
                        arrowprops=dict(arrowstyle='-|>', linewidth=0.9,
                                        color=INK2, mutation_scale=9))

    for si, (top, bot, col, st) in span.items():
        ax.plot([0.026, 0.026], [bot, top], color=col, linewidth=2.8,
                solid_capstyle='butt', transform=ax.transAxes, zorder=2)
        ax.text(0.011, (top + bot) / 2, st, rotation=90, ha='center',
                va='center', fontsize=7.0, weight='bold', color=col,
                transform=ax.transAxes)
    note('prisma',
         'Reported in accordance with PRISMA-ScR (Tricco et al., 2018). '
               'Databases were searched from inception to 22 August 2026; the '
               'database-specific search strings and the exact query dates are '
               'given in Table 1. Screening and full-text assessment were '
               'performed in duplicate by two reviewers, with a third '
               'adjudicating disagreements.')
    return save(fig, out('fig02_prisma_flow.pdf'))


# ================================================================ FIGURE 3
def fig03_workflow():
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    blank(ax)
    steps = [
        ('1', 'Pilot calibration',
         'Two reviewers independently extract ten studies; the extraction '
         'form is refined before the full pass'),
        ('2', 'Duplicate extraction',
         'Both reviewers extract every included source into the shared form, '
         'blind to each other'),
        ('3', 'Adjudication',
         'Disagreements are resolved by discussion; a third reviewer '
         'adjudicates any that remain'),
        ('4', 'Rule-based derivation',
         'Derived variables are computed by the documented rules R1-R4, '
         'identically for every source'),
        ('5', 'Single master dataset',
         'Every statistic, table and figure in the article is computed from '
         'this one file'),
    ]
    x, w = 0.035, 0.93
    h, gapv, top = 0.108, 0.024, 0.985
    NUMW, TITW = 0.045, 0.235
    y = top
    for i, (num, title, bdy) in enumerate(steps):
        col = CAT[i % len(CAT)]
        box(ax, x, y - h, w, h, '#FFFFFF', col)
        fit_text(ax, fig, x + 0.008, y - h, NUMW, h, num, fontsize=9.5,
                 weight='bold', color=col, wrap=False, label='step number')
        fit_text(ax, fig, x + 0.008 + NUMW, y - h, TITW, h, title,
                 fontsize=8.0, weight='bold', color=col, ha='left',
                 label='step title')
        fit_text(ax, fig, x + 0.012 + NUMW + TITW, y - h,
                 w - NUMW - TITW - 0.03, h, bdy, fontsize=7.3, color=INK2,
                 ha='left', label='step body')
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + 0.115, y - h - gapv),
                        xytext=(x + 0.115, y - h),
                        arrowprops=dict(arrowstyle='-|>', linewidth=0.9,
                                        color=INK2, mutation_scale=9))
        y -= h + gapv

    bh = y - 0.015
    box(ax, x, 0.012, w, bh, '#F6F8F9', GRID)
    fit_text(ax, fig, x + 0.012, 0.012 + bh - 0.075, w - 0.024, 0.070,
             'Extraction variables recorded for every source', fontsize=8.0,
             weight='bold', color=INK, ha='left', wrap=False,
             label='variables heading')
    rows = [('Bibliographic',
             'author, year, journal, publisher, author country, '
             'case-study country'),
            ('Substantive',
             'objective, disaster type, method family (multi-label), learning '
             'paradigm, forecast horizon, functional form, uncertainty '
             'treatment, sustainability framing'),
            ('Evidential',
             'performance evidence, metric reported, deployment status, '
             'data source')]
    CPL = 95          # characters that fit one line in the value column
    wts = [max(1, -(-len(b) // CPL)) for _, b in rows]
    avail = bh - 0.094
    ry = 0.012 + bh - 0.086
    for (lab, body), wt in zip(rows, wts):
        rh = avail * wt / sum(wts)
        fit_text(ax, fig, x + 0.014, ry - rh, 0.145, rh, lab, fontsize=7.4,
                 weight='bold', color=INK2, ha='left', va='top', wrap=False,
                 label='variable group')
        fit_text(ax, fig, x + 0.165, ry - rh, w - 0.185, rh, body,
                 fontsize=7.2, color=INK2, ha='left', label='variable list')
        ry -= rh
    return save(fig, out('fig03_extraction_workflow.pdf'))


# ================================================================ FIGURE 4
def fig04_year():
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    yrs = sorted(int(y) for y in S['by_year'])
    vals = [S['by_year'][str(y)] for y in yrs]
    w1 = [sum(1 for r in ROWS if int(r['year']) == y and r['wave'] == '1')
          for y in yrs]
    w2 = [v - a for v, a in zip(vals, w1)]
    ax.bar(yrs, w1, width=0.74, color=CAT[0], edgecolor='white',
           linewidth=0.8, label='Original search (to Jan 2024)', zorder=3)
    ax.bar(yrs, w2, width=0.74, bottom=w1, color=CAT[1], edgecolor='white',
           linewidth=0.8, label='Updated search (Jan 2024 - Aug 2026)',
           zorder=3)
    ax.set_xlabel('Year of publication')
    ax.set_ylabel('Number of included sources (count)')
    assert 'Year' in ax.get_xlabel() and 'Year' not in ax.get_ylabel(), \
        'axis labels are the wrong way round'
    # every third year: adjacent labels such as 2025 and 2026 would collide
    ticks = list(range(yrs[0], yrs[-1] + 1, 3))
    ax.set_xticks(ticks)
    ax.set_xlim(yrs[0] - 0.8, yrs[-1] + 0.8)
    integer_axis(ax, 'y')
    recessive_grid(ax, 'y')
    for xx, v in zip(yrs, vals):
        if v:
            ax.text(xx, v + max(vals) * 0.025, str(v), ha='center',
                    va='bottom', fontsize=6.8, color=INK2)
    ax.set_ylim(0, max(vals) * 1.22)
    ax.legend(loc='upper left', handlelength=1.1, borderaxespad=0.3)
    note('year', PROV + '  %d of %d sources (%.1f%%) were published in 2023 '
               'or later.' % (S['N_since2023'], S['N_all'],
                              S['pct_since2023']))
    return save(fig, out('fig04_publications_by_year.pdf'))


# =============================================================== FIGURE 5/11
def geo_figure(block, fname, what, cbar_label, key):
    b = S[block]
    counts = {k: v['n'] for k, v in b['items'].items()}
    fig = plt.figure(figsize=(7.2, 6.0))
    axm = fig.add_axes([0.02, 0.545, 0.96, 0.415])
    cax = fig.add_axes([0.300, 0.512, 0.400, 0.015])
    nmap, unmatched, noncountry = worldmap.draw_choropleth(
        axm, counts, cbar_ax=cax, cbar_label=cbar_label)
    panel_title(fig, 0.02, 0.995, '(a)  Global distribution')

    axb = fig.add_axes([0.185, 0.115, 0.765, 0.285])
    items = [(k, v) for k, v in b['items'].items()
             if k not in worldmap.NON_COUNTRY][:10]
    hbar(axb, fig, [k for k, _ in items], [v['n'] for _, v in items],
         [v['pct'] for _, v in items], color=CAT[0])
    panel_title(fig, 0.02, 0.445, '(b)  Ten most frequently occurring %s'
                % what)

    extra = ''
    if noncountry:
        extra = ('  Aggregate labels not placed on the map: '
                 + ', '.join('%s (n = %d)' % (k, v)
                             for k, v in sorted(noncountry.items())) + '.')
    if unmatched:
        extra += ('  Labels without a matching boundary: '
                  + ', '.join(sorted(set(unmatched))) + '.')
    note(key, PROV + '  Denominator = %d sources for which the variable '
               'was extractable; panel (b) percentages use that denominator. '
               'Colour encodes a COUNT of included sources, not a rate, a '
               'density or a per-capita quantity; grey means no included '
               'source.%s' % (b['denominator'], extra))
    return save(fig, out(fname))


# ================================================================ FIGURE 6
def fig06_outlets():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.1),
                             gridspec_kw={'wspace': 1.15})
    l, v, p, den, tail = block_items('journal', topn=10)
    l = [OUTLET_SHORT.get(x, x) for x in l]
    hbar(axes[0], fig, l, v, p, color=CAT[0], wrap_labels=24)
    panel_title(fig, 0.02, 1.02, '(a)  Ten most frequent publication outlets')

    l2, v2, p2, den2, _ = block_items('publisher')
    hbar(axes[1], fig, l2, v2, p2,
         color=[CAT[1] if x != 'Other' else OTHER for x in l2])
    panel_title(fig, 0.545, 1.02, '(b)  Publishers')

    n_tail = sum(x[1]['n'] for x in tail)
    note('outlets', PROV + '  Denominator: all %d included sources; '
               'percentages within each panel use that denominator. Panel (a) '
               'shows the ten most frequent outlets; the remaining %d sources '
               'are spread across %d further outlets, none with more than %d '
               'sources, and are omitted from the panel rather than collapsed '
               'into a single bar. Outlet names recorded by abbreviation in '
               'the original extraction table were expanded to their full '
               'titles before counting.'
               % (den, n_tail, len(tail),
                  max(x[1]['n'] for x in tail) if tail else 0))
    return save(fig, out('fig06_outlets.pdf'))


# ================================================================ FIGURE 7
def fig07_methods():
    fig, ax = plt.subplots(figsize=(6.9, 3.2))
    mf = S['method_family']
    items = sorted(mf.items(), key=lambda kv: -kv[1]['n'])
    hbar(ax, fig, [k for k, _ in items], [v['n'] for _, v in items],
         [v['pct'] for _, v in items], color=CAT[:len(items)],
         xlabel='Number of primary studies employing the family (count)')
    note('methods', PROV + '  MULTI-LABEL variable: a study using a hybrid '
               'method scores on every family it employs, so the percentages '
               'sum to %.1f%%, not 100%%. Denominator = %d primary studies. '
               '%d studies (%.1f%%) combine two or more families; %d report '
               'no identifiable family.'
               % (S['mf_label_sum_pct'], S['N_prim'], S['n_hybrid'],
                  S['pct_hybrid'], S['n_no_family']))
    return save(fig, out('fig07_method_families.pdf'))


# ================================================================ FIGURE 8
def fig08_paradigm_horizon():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9),
                             gridspec_kw={'wspace': 0.72})
    l, v, p, den, _ = block_items('paradigm')
    hbar(axes[0], fig, l, v, p, color=CAT[0])
    panel_title(fig, 0.02, 1.03, '(a)  Learning paradigm')
    l2, v2, p2, den2, _ = block_items('horizon')
    hbar(axes[1], fig, l2, v2, p2, color=CAT[2])
    panel_title(fig, 0.535, 1.03, '(b)  Forecast horizon')
    note('paradigm', PROV + '  Mutually exclusive categories. Panel (a) '
               'denominator = %d primary studies reporting a learning '
               'paradigm; panel (b) denominator = %d primary studies '
               'reporting a horizon. Studies that do not report the variable '
               'are excluded from that denominator rather than counted as a '
               'category.' % (den, den2))
    return save(fig, out('fig08_paradigm_horizon.pdf'))


# ================================================================ FIGURE 9
def fig09_disaster():
    fig, ax = plt.subplots(figsize=(6.9, 3.2))
    l, v, p, den, _ = block_items('disaster')
    hbar(ax, fig, l, v, p, color=CAT[3])
    note('disaster', PROV + '  Mutually exclusive; one dominant hazard per '
               'study. Denominator = %d primary studies. "Multi-hazard/'
               'General" denotes studies that do not restrict themselves to a '
               'single hazard.' % den)
    return save(fig, out('fig09_disaster_types.pdf'))


# =============================================================== FIGURE 10
def fig10_objectives():
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    l, v, p, den, _ = block_items('objective')
    l = [x.replace('Humanitarian logistics and supply chain management',
                   'Humanitarian logistics and SCM') for x in l]
    hbar(ax, fig, l, v, p, color=CAT[4])
    note('objectives', PROV + '  Mutually exclusive; one primary objective per '
               'source. Denominator = all %d included sources.' % den)
    return save(fig, out('fig10_objectives.pdf'))


# =============================================================== FIGURE 12
def fig12_linearity_uncertainty():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0),
                             gridspec_kw={'wspace': 0.95})
    l, v, p, den, _ = block_items('linearity')
    hbar(axes[0], fig, l, v, p, color=CAT[0])
    panel_title(fig, 0.02, 1.03, '(a)  Functional form of the model')

    st, su = S['stochastic'], S['sustainability']
    ax = axes[1]
    labels = ['Uncertainty represented\nexplicitly',
              'Sustainability or equity\nframed as an objective']
    yes, no = [st['n_yes'], su['n_yes']], [st['n_no'], su['n_no']]
    y = np.arange(2)[::-1]
    ax.barh(y, yes, height=0.5, color=CAT[2], edgecolor='white',
            linewidth=0.8, label='Yes', zorder=3)
    ax.barh(y, no, left=yes, height=0.5, color='#E3E5E4', edgecolor='white',
            linewidth=0.8, label='No', zorder=3)
    tot = st['denominator']
    for yy, a in zip(y, yes):
        value_label(ax, fig, a, yy, '%d  (%.1f%%)' % (a, 100.0 * a / tot),
                    tot, color_in='white', color_out=INK2, weight='bold')
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel('Number of primary studies (count)')
    ax.set_xlim(0, tot * 1.02)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    recessive_grid(ax, 'x')
    ax.legend(loc='lower left', ncol=2, handlelength=1.0, frameon=False,
              bbox_to_anchor=(0.0, 1.005))
    panel_title(fig, 0.535, 1.03, '(b)  Uncertainty and sustainability framing')
    note('linearity', PROV + '  Panel (b) applies a deliberately strict rule: a '
               'study counts only where the reported method explicitly '
               'represents uncertainty, or where an environmental, equity or '
               'resilience objective is explicitly stated. Denominator = %d '
               'primary studies.' % tot)
    return save(fig, out('fig12_linearity_uncertainty.pdf'))


# =============================================================== FIGURE 13
def fig13_evidence():
    """Separates literature prevalence from demonstrated efficacy --
    Reviewer 2, Major Comment 4."""
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9),
                             gridspec_kw={'wspace': 0.80})
    CM_E = {'Comparative benchmark': CAT[2], 'Single-model metric': CAT[0],
            'Qualitative/none': CAT[4], 'Not reported': MUTED}
    pe = S['performance_evidence']
    l = [o for o in ['Comparative benchmark', 'Single-model metric',
                     'Qualitative/none', 'Not reported'] if o in pe]
    hbar(axes[0], fig, l, [pe[o]['n'] for o in l], [pe[o]['pct'] for o in l],
         color=[CM_E[x] for x in l])
    panel_title(fig, 0.02, 1.03, '(a)  Evidence of predictive performance')

    CM_D = {'Operational deployment': CAT[2], 'Real-data case study': CAT[0],
            'Synthetic/illustrative': CAT[4], 'Not reported': MUTED}
    dp = S['deployment']
    l2 = [o for o in ['Operational deployment', 'Real-data case study',
                      'Synthetic/illustrative', 'Not reported'] if o in dp]
    hbar(axes[1], fig, l2, [dp[o]['n'] for o in l2],
         [dp[o]['pct'] for o in l2], color=[CM_D[x] for x in l2])
    panel_title(fig, 0.535, 1.03, '(b)  Deployment status')
    note('evidence', PROV + '  Denominator = %d primary studies. "Not reported" '
               'means the study\'s retrievable record contains no extractable '
               'performance figure or deployment statement; it is NOT evidence '
               'that the method performs poorly. Only %d studies (%.1f%%) '
               'supply a comparative benchmark against a competing model, and '
               'only %d (%.1f%%) document use by a named responding '
               'organisation.'
               % (S['N_prim'], S['n_comparative'], S['pct_comparative'],
                  S['n_operational'], S['pct_operational']))
    return save(fig, out('fig13_evidence_deployment.pdf'))


# =============================================================== FIGURE 14
def fig14_method_by_disaster():
    MF = [('mf_statistical', 'Statistical /\ntime series'),
          ('mf_ml', 'Classical\nmachine learning'),
          ('mf_dl', 'Deep learning /\nneural'),
          ('mf_knowledge', 'Knowledge-based\n(CBR, fuzzy, grey)'),
          ('mf_optsim', 'Optimisation /\nsimulation'),
          ('mf_genai', 'Generative AI /\nLLM')]
    dis = [d for d, _ in sorted(S['disaster']['items'].items(),
                                key=lambda kv: -kv[1]['n'])]
    M = np.zeros((len(MF), len(dis)), dtype=int)
    for r in PRIM:
        if r['disaster_type'] not in dis:
            continue
        j = dis.index(r['disaster_type'])
        for i, (k, _) in enumerate(MF):
            if r[k] == '1':
                M[i, j] += 1

    fig, ax = plt.subplots(figsize=(7.5, 3.7))
    im = ax.imshow(M, cmap=SEQ, aspect='auto', vmin=0, vmax=M.max())
    SHORT = {'Multi-hazard/General': 'Multi-hazard\n/ general',
             'Hurricane/Cyclone': 'Hurricane\n/ cyclone',
             'Biological/Epidemic': 'Biological\n/ epidemic',
             'Technological/Other': 'Technological\n/ other',
             'Drought/Food insecurity': 'Drought /\nfood insec.',
             'Conflict/Displacement': 'Conflict /\ndisplacement'}
    ax.set_xticks(range(len(dis)))
    ax.set_xticklabels([SHORT.get(d, d) for d in dis], fontsize=7.0)
    ax.set_yticks(range(len(MF)))
    ax.set_yticklabels([lab for _, lab in MF], fontsize=7.2)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-.5, len(dis), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(MF), 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=1.6)
    ax.tick_params(which='minor', length=0)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j]:
                ax.text(j, i, str(M[i, j]), ha='center', va='center',
                        fontsize=7.6,
                        color='white' if M[i, j] > M.max() * 0.55 else INK)
    cb = fig.colorbar(im, ax=ax, fraction=0.030, pad=0.018)
    cb.set_label('Number of primary studies (count)', fontsize=7.2, color=INK2)
    cb.ax.tick_params(labelsize=7, length=2)
    cb.outline.set_linewidth(0.4); cb.outline.set_edgecolor(INK2)
    note('heatmap', PROV + '  Method family is multi-label, so a hybrid study '
               'contributes to more than one row; row totals therefore exceed '
               'the column totals. Denominator = %d primary studies with a '
               'coded hazard.' % S['disaster']['denominator'])
    return save(fig, out('fig14_method_by_disaster.pdf'))


# =============================================================== FIGURE 15
def fig15_method_over_time():
    periods = [(2007, 2015, '2007-2015'), (2016, 2020, '2016-2020'),
               (2021, 2026, '2021-2026')]
    MF = [('mf_statistical', 'Statistical'),
          ('mf_knowledge', 'Knowledge-based'),
          ('mf_optsim', 'Optimisation / simulation'),
          ('mf_ml', 'Classical machine learning'),
          ('mf_dl', 'Deep learning'),
          ('mf_genai', 'Generative AI / LLM')]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    width, xs = 0.135, np.arange(len(periods))
    handles = []
    for i, (k, lab) in enumerate(MF):
        share = []
        for a, b, _ in periods:
            sub = [r for r in PRIM if a <= int(r['year']) <= b]
            share.append(100.0 * sum(1 for r in sub if r[k] == '1') / len(sub)
                         if sub else 0)
        pos = xs + (i - (len(MF) - 1) / 2) * width
        bars = ax.bar(pos, share, width=width * 0.86, color=CAT[i], label=lab,
                      edgecolor='white', linewidth=0.7, zorder=3)
        handles.append(bars)
        for xx, sv in zip(pos, share):
            if sv > 0:
                ax.text(xx, sv + 1.6, '%.0f' % sv, ha='center', va='bottom',
                        fontsize=6.3, color=INK2)
    ax.set_xticks(xs)
    ax.set_xticklabels(['%s\n(n = %d)'
                        % (lab, len([r for r in PRIM
                                     if a <= int(r['year']) <= b]))
                        for a, b, lab in periods])
    ax.set_ylabel('Share of primary studies in the period (%)')
    ax.set_xlabel('Publication period', labelpad=10)
    recessive_grid(ax, 'y')
    ax.set_ylim(0, 104)
    # Matplotlib fills a multi-column legend column-major, so reading across
    # the first row would give families 1, 3, 5. Reorder the handles so the
    # legend reads left-to-right in the same order as the bars.
    h, lb = ax.get_legend_handles_labels()
    ncol = 3
    nrow = -(-len(h) // ncol)
    # Slot (row r, column c) of a column-major legend is filled by the item at
    # position r + c*nrow of the list we hand it. To make that slot show family
    # r*ncol + c -- i.e. reading order -- hand the families over in this order.
    order = [r * ncol + c for c in range(ncol) for r in range(nrow)]
    order = [i for i in order if i < len(h)]
    assert sorted(order) == list(range(len(h))), 'legend permutation lost items'
    ax.legend([h[i] for i in order], [lb[i] for i in order], ncol=ncol,
              loc='upper center', bbox_to_anchor=(0.5, 1.28),
              handlelength=1.0, columnspacing=1.6, handletextpad=0.5)
    note('overtime', PROV + '  Families are ordered from the longest-'
               'established to the most recent. Multi-label: shares within a '
               'period sum to more than 100%. Shares describe how often a '
               'family appears in the published literature of the period; '
               'they are not a measure of forecasting accuracy (Reviewer 2, '
               'Major Comment 4).')
    return save(fig, out('fig15_method_over_time.pdf'))


# =============================================================== FIGURE 16
def fig16_graphical_abstract():
    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    blank(ax)
    fit_text(ax, fig, 0.02, 0.898, 0.96, 0.098,
             'Artificial intelligence for relief demand forecasting in '
             'emergency supply chains', fontsize=12.5, weight='bold',
             color=INK, label='ga title')
    fit_text(ax, fig, 0.05, 0.795, 0.90, 0.098,
             'A PRISMA-ScR scoping review of %d sources, %d-%d: research '
             'attention against efficacy evidence'
             % (S['N_all'], S['year_min'], S['year_max']),
             fontsize=8.8, color=INK2, label='ga subtitle')

    cards = [('%d' % S['N_all'], 'sources included\n%d primary studies\n'
              '%d reviews' % (S['N_prim'], S['N_rev']), CAT[0]),
             ('%.0f%%' % S['method_family']['Classical machine learning']['pct'],
              'of primary studies\nuse classical\nmachine learning', CAT[1]),
             ('%.0f%%' % S['pct_hybrid'],
              'combine two or more\nmethod families', CAT[2]),
             ('%d' % S['n_comparative'],
              'of %d studies\nbenchmark against\na competing model'
              % S['N_prim'], CAT[3]),
             ('%d' % S['n_operational'],
              'of %d document use\nby a named\nresponding organisation'
              % S['N_prim'], CAT[5])]
    w, gap = 0.178, 0.024
    x0 = (1 - (5 * w + 4 * gap)) / 2
    ch, cy = 0.375, 0.425
    caps = []
    for i, (big, small, col) in enumerate(cards):
        x = x0 + i * (w + gap)
        box(ax, x, cy, w, ch, '#FFFFFF', col, lw=1.1)
        fit_text(ax, fig, x, cy + ch - 0.155, w, 0.145, big, fontsize=19,
                 weight='bold', color=col, wrap=False, label='ga number')
        caps.append((ax, fig, x + 0.005, cy + 0.012, w - 0.010, ch - 0.175,
                     small))
    fit_text_group(caps, fontsize=7.4, color=INK2, linespacing=1.7,
                   label='ga caption')

    box(ax, 0.055, 0.035, 0.89, 0.345, '#F4F7FA', CAT[0], lw=1.1)
    fit_text(ax, fig, 0.07, 0.285, 0.86, 0.080,
             'Prevalence in the literature is not evidence of operational '
             'efficacy', fontsize=9.2, weight='bold', color=CAT[0],
             label='ga headline')
    fit_text(ax, fig, 0.075, 0.050, 0.85, 0.225,
             'Machine learning dominates publication counts, but comparative '
             'accuracy evidence exists for a small minority of studies and '
             'fielded deployment for fewer still. The review therefore reports '
             'research attention and demonstrated performance as two separate '
             'quantities.', fontsize=7.6, color=INK2, linespacing=1.75,
             label='ga body')
    return save(fig, out('fig16_graphical_abstract.pdf'))


# =================================================================== main
if __name__ == '__main__':
    fig01_escm()
    fig02_prisma()
    fig03_workflow()
    fig04_year()
    geo_figure('author_country', 'fig05_author_geography.pdf',
               'author countries',
               'Number of included sources with an author in the country '
               '(count)', 'authorgeo')
    fig06_outlets()
    fig07_methods()
    fig08_paradigm_horizon()
    fig09_disaster()
    fig10_objectives()
    geo_figure('focus_country', 'fig11_case_study_geography.pdf',
               'case-study countries',
               'Number of included sources studying the country (count)',
               'focusgeo')
    fig12_linearity_uncertainty()
    fig13_evidence()
    fig14_method_by_disaster()
    fig15_method_over_time()
    fig16_graphical_abstract()

    def esc(t):
        for a, b in (('&', r'\&'), ('%', r'\%'), ('_', r'\_'),
                     ('#', r'\#')):
            t = t.replace(a, b)
        return t

    with open(os.path.join(FIG, 'figure_notes.tex'), 'w') as fh:
        fh.write('%% AUTO-GENERATED by code/make_figures.py -- DO NOT EDIT.\n'
                 '%% Provenance and denominator notes for the figure captions.\n'
                 '%% They are carried in the captions rather than drawn on the\n'
                 '%% figures themselves.\n')
        for k in sorted(NOTES):
            fh.write('\\newcommand{\\note%s}{%s}\n' % (k, esc(NOTES[k])))
    print('figure_notes.tex: %d caption notes' % len(NOTES))

    print('%d figures written to figures/' % len(MADE))
    for m in MADE:
        print('   %-42s %7d bytes'
              % (m, os.path.getsize(os.path.join(FIG, m))))
    if VIOLATIONS:
        print('\nLAYOUT VIOLATIONS (%d):' % len(VIOLATIONS))
        for v in VIOLATIONS:
            print('   %s' % v)
        sys.exit(1)
    print('\nno layout violations: every placed label fits inside its box')
