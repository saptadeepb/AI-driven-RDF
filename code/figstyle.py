"""
figstyle.py -- shared figure styling and layout primitives.

Design decisions taken in response to the reviewers:

* Reviewer 1 (Figure 4): "The colour scheme is too bright and jarring."
  -> One muted categorical palette across all figures, validated for
     colour-vision deficiency (see supplementary/palette_validation.txt).

* Reviewer 1 (Figures 6 and 11): "the gradient bar ... lacks clear units."
  -> Choropleths use a single-hue sequential ramp with an explicitly titled,
     integer-ticked colour bar and a labelled "no data" swatch.

* Reviewer 1 (Figure 5): axis labels were reversed.
  -> Axis labelling is asserted in code.

LAYOUT GUARANTEES
-----------------
Hand-placed text in a diagram is the usual source of overflow and collision.
Rather than tuning coordinates by eye, this module measures what it draws:

  fit_text()    wraps and shrinks a label until its RENDERED extent fits
                inside the box it belongs to, and records a violation if it
                cannot -- so an overflowing label fails the build instead of
                reaching the page.
  place_note()  measures how far down the drawn content actually extends and
                puts the provenance note below it, so a note can never sit on
                top of an axis label.
  value_label() measures a bar's value label and places it inside the bar only
                when it demonstrably fits, otherwise outside.

`VIOLATIONS` collects anything that could not be satisfied; make_figures.py
fails the build if it is non-empty.
"""
import os
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import MaxNLocator

# ------------------------------------------------------------------ palette
# Validated (all six checks PASS on a light surface): lightness band, chroma
# floor, CVD separation, normal-vision floor, contrast against the surface.
CAT = ['#1F5C99',   # blue
       '#C4622D',   # burnt orange
       '#2E8B6B',   # green
       '#8E4F8C',   # plum
       '#A17F1E',   # ochre
       '#B23A6E']   # rose
OTHER = '#8A8F98'          # reserved for the folded "Other" slot only

INK = '#1A1A1A'
INK2 = '#5A5F66'
INK3 = '#8A8F98'
GRID = '#DEDEDA'
SURFACE = '#FFFFFF'
MUTED = '#C9CBC9'

SEQ = LinearSegmentedColormap.from_list(
    'seq_blue', ['#F2F6FA', '#CBDCEB', '#93B8D6', '#5590BE', '#2A6BA0',
                 '#12456E'])
NODATA = '#EFEFEC'

VIOLATIONS = []


def apply_style():
    plt.rcParams.update({
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
        'svg.fonttype': 'none',
        'font.family': 'DejaVu Sans',
        'font.size': 8.5,
        'axes.titlesize': 9.5,
        'axes.titleweight': 'bold',
        'axes.labelsize': 8.5,
        'axes.edgecolor': INK2,
        'axes.linewidth': 0.6,
        'axes.labelcolor': INK,
        'axes.facecolor': SURFACE,
        'axes.grid': False,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'xtick.color': INK2,
        'ytick.color': INK2,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'xtick.major.width': 0.6,
        'ytick.major.width': 0.6,
        'xtick.major.size': 3,
        'ytick.major.size': 3,
        'legend.frameon': False,
        'legend.fontsize': 8,
        'figure.facecolor': SURFACE,
        'figure.dpi': 300,
        'savefig.dpi': 300,
    })


# ------------------------------------------------------- measurement helpers
def renderer(fig):
    fig.canvas.draw()
    return fig.canvas.get_renderer()


def extent_in(artist, target, fig):
    """Rendered extent of `artist` expressed in `target` coordinates."""
    bb = artist.get_window_extent(renderer(fig))
    return bb.transformed(target.inverted())


def recessive_grid(ax, axis='x'):
    ax.set_axisbelow(True)
    ax.grid(True, axis=axis, color=GRID, linewidth=0.5, zorder=0)


def integer_axis(ax, which='y'):
    """Counts are integers; never label an axis 2.5 studies."""
    loc = MaxNLocator(integer=True, nbins='auto')
    (ax.yaxis if which == 'y' else ax.xaxis).set_major_locator(loc)


# --------------------------------------------------------------- fit_text
def _wrap_to_width(ax, fig, s, size, width, weight, linespacing):
    """Wrap s so that no line exceeds `width` (axes fraction) at `size`.

    The characters-per-line estimate is taken by measuring THIS string, not a
    reference glyph: measuring a row of capital M grossly overestimates the
    average advance width of real prose and forces needless extra lines.
    """
    out = []
    for p in s.split('\n'):
        if not p:
            out.append('')
            continue
        probe = ax.text(0, 0, p, fontsize=size, weight=weight,
                        transform=ax.transAxes, alpha=0)
        w = extent_in(probe, ax.transAxes, fig).width
        probe.remove()
        if w <= width or w <= 0:
            out.append(p)
            continue
        chars = max(6, int(len(p) * width / w))
        wrapped = textwrap.wrap(p, chars) or ['']
        # verify and tighten: the estimate is linear, real text is not
        for _ in range(6):
            probe = ax.text(0, 0, max(wrapped, key=len), fontsize=size,
                            weight=weight, transform=ax.transAxes, alpha=0)
            wl = extent_in(probe, ax.transAxes, fig).width
            probe.remove()
            if wl <= width:
                break
            chars = max(6, chars - max(1, int(chars * 0.06)))
            wrapped = textwrap.wrap(p, chars) or ['']
        out.extend(wrapped)
    return '\n'.join(out)


def fit_text(ax, fig, x, y, w, h, s, fontsize=7.4, minsize=5.0, pad=0.012,
             weight='normal', color=None, ha='center', va='center',
             linespacing=1.45, wrap=True, label='', zorder=5):
    """Draw `s` inside the axes-fraction box (x, y, w, h).

    The text is wrapped to the box width and then shrunk until its rendered
    extent fits inside the box with `pad` clearance on every side. If it still
    does not fit at `minsize`, a violation is recorded so the build fails
    rather than silently shipping an overflowing label.
    """
    wav, hav = w - 2 * pad, h - 2 * pad
    cx = x + w / 2 if ha == 'center' else (x + pad if ha == 'left'
                                           else x + w - pad)
    cy = y + h / 2 if va == 'center' else (y + h - pad if va == 'top'
                                           else y + pad)
    size = fontsize
    art = None
    while size >= minsize - 1e-9:
        body = _wrap_to_width(ax, fig, s, size, wav, weight,
                              linespacing) if wrap else s
        if art is not None:
            art.remove()
        art = ax.text(cx, cy, body, transform=ax.transAxes, fontsize=size,
                      weight=weight, color=color or INK, ha=ha, va=va,
                      linespacing=linespacing, zorder=zorder)
        bb = extent_in(art, ax.transAxes, fig)
        if bb.width <= wav + 1e-9 and bb.height <= hav + 1e-9:
            art._fit_size = size
            return art
        size -= 0.2
    VIOLATIONS.append(
        'text does not fit its box even at %.1fpt: %r%s'
        % (minsize, s[:60], (' [%s]' % label) if label else ''))
    return art


def fit_text_group(specs, **shared):
    """Fit a set of labels that belong together at a SINGLE type size.

    Each label is fitted independently first; the smallest size any of them
    needed is then applied to all. A row of summary cards therefore reads as
    one typographic system instead of five different sizes.

    `specs` is a list of (ax, fig, x, y, w, h, text) tuples.
    """
    arts, sizes = [], []
    for ax, fig, x, y, w, h, txt in specs:
        a = fit_text(ax, fig, x, y, w, h, txt, **shared)
        arts.append((ax, fig, x, y, w, h, txt, a))
        sizes.append(getattr(a, '_fit_size', shared.get('fontsize', 7.4)))
    common = min(sizes)
    out = []
    for ax, fig, x, y, w, h, txt, a in arts:
        if getattr(a, '_fit_size', None) == common:
            out.append(a)
            continue
        a.remove()
        kw = dict(shared)
        kw['fontsize'] = common
        kw['minsize'] = min(common, kw.get('minsize', 5.0))
        out.append(fit_text(ax, fig, x, y, w, h, txt, **kw))
    return out


def box(ax, x, y, w, h, fc, ec, lw=0.9, radius=0.014, zorder=3):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0,rounding_size=%f' % radius,
        transform=ax.transAxes, facecolor=fc, edgecolor=ec, linewidth=lw,
        zorder=zorder, mutation_aspect=1))


# --------------------------------------------------------------- value label
def value_label(ax, fig, xval, yval, text, span, color_in='white',
                color_out=None, fontsize=7.6, weight='normal', gap=0.012):
    """Label a horizontal bar. Placed inside the bar only if it measurably
    fits there; otherwise outside, to the right. Never encroaches on the
    axis labels."""
    pad = span * 0.018
    probe = ax.text(0, 0, text, fontsize=fontsize, weight=weight, alpha=0)
    wtxt = extent_in(probe, ax.transData.inverted().inverted(), fig).width
    probe.remove()
    # measure in data units
    p2 = ax.text(0, yval, text, fontsize=fontsize, weight=weight, alpha=0)
    bb = p2.get_window_extent(renderer(fig)).transformed(
        ax.transData.inverted())
    p2.remove()
    need = bb.width
    if xval - 2 * pad >= need:
        return ax.text(xval - pad, yval, text, va='center', ha='right',
                       fontsize=fontsize, weight=weight, color=color_in,
                       zorder=5)
    return ax.text(xval + pad, yval, text, va='center', ha='left',
                   fontsize=fontsize, weight=weight,
                   color=color_out or INK2, zorder=5)


# --------------------------------------------------------------- place_note
def place_note(fig, text, fontsize=6.6, gap=0.022, side_pad=0.012):
    """Put the provenance note below everything already drawn.

    The vertical position is measured from the lowest rendered element in the
    figure, so the note cannot land on top of an axis label or a legend no
    matter how the panels are laid out.
    """
    r = renderer(fig)
    inv = fig.transFigure.inverted()
    low = 1.0
    for ax in fig.axes:
        try:
            bb = ax.get_tightbbox(r).transformed(inv)
        except Exception:
            continue
        low = min(low, bb.y0)
    for t in fig.texts:
        bb = t.get_window_extent(r).transformed(inv)
        low = min(low, bb.y0)

    width = 1.0 - 2 * side_pad
    probe = fig.text(0, 0, 'M' * 60, fontsize=fontsize, alpha=0)
    w60 = probe.get_window_extent(r).transformed(inv).width
    probe.remove()
    chars = max(40, int(60.0 * width / w60)) if w60 > 0 else 110
    body = '\n'.join(textwrap.wrap(' '.join(text.split()), chars))
    return fig.text(side_pad, low - gap, body, ha='left', va='top',
                    fontsize=fontsize, color=INK3, linespacing=1.55)


def panel_title(fig, x, y, s, fontsize=9.2):
    return fig.text(x, y, s, fontsize=fontsize, weight='bold', ha='left',
                    va='top', color=INK)


def _overlap_report(fig, path):
    """Flag any two pieces of text in the same axes that visibly overlap.

    fit_text guarantees a label sits inside its own box; this is the
    independent check that two labels do not sit on top of each other -- the
    failure that produced colliding tick labels and notes running through axis
    titles in the previous revision.
    """
    r = renderer(fig)
    groups = {}
    for ax in fig.axes:
        items = []
        for t in (list(ax.texts) + list(ax.get_xticklabels())
                  + list(ax.get_yticklabels())
                  + ([ax.xaxis.label, ax.yaxis.label, ax.title])):
            if t is None or not t.get_visible() or not t.get_text().strip():
                continue
            if getattr(t, 'get_alpha', lambda: 1)() == 0:
                continue
            try:
                bb = t.get_window_extent(r)
            except Exception:
                continue
            if bb.width <= 0 or bb.height <= 0:
                continue
            items.append((t.get_text()[:32], bb))
        groups[ax] = items
    groups[None] = [(t.get_text()[:32], t.get_window_extent(r))
                    for t in fig.texts
                    if t.get_text().strip() and t.get_visible()]
    bad = []
    for items in groups.values():
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                (s1, b1), (s2, b2) = items[i], items[j]
                ow = min(b1.x1, b2.x1) - max(b1.x0, b2.x0)
                oh = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
                if ow <= 0 or oh <= 0:
                    continue
                small = min(b1.width * b1.height, b2.width * b2.height)
                if small > 0 and (ow * oh) / small > 0.15:
                    bad.append('%s: %r overlaps %r'
                               % (os.path.basename(path), s1, s2))
    for b in bad:
        VIOLATIONS.append(b)


def save(fig, path):
    _overlap_report(fig, path)
    fig.savefig(path, format='pdf', bbox_inches='tight', pad_inches=0.035)
    plt.close(fig)
    return path
