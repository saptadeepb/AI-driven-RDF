"""
worldmap.py -- minimal, dependency-light TopoJSON -> polygon reader and
choropleth renderer for the manuscript's two geographic figures.

Geometry: Natural Earth 1:110m country boundaries, as distributed in the
`world-atlas` package (public domain). The file is bundled in
data/world-110m.json so the figures rebuild offline and reproducibly.

The renderer exists so that the colour bar can be given an explicit title,
explicit integer ticks and an explicit "no data" swatch -- the three things
Reviewer 1 identified as missing from Figures 6 and 11 of the original
submission.
"""
import json, os
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import numpy as np

from figstyle import SEQ, NODATA, INK2, INK3

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPO = os.path.join(HERE, 'data', 'world-110m.json')


# ------------------------------------------------------------- topojson
def _decode_arcs(topo):
    sc = topo['transform']['scale']
    tr = topo['transform']['translate']
    arcs = []
    for arc in topo['arcs']:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
        arcs.append(pts)
    return arcs


def _ring(arcs, idxs):
    pts = []
    for i in idxs:
        if i < 0:
            seg = arcs[~i][::-1]
        else:
            seg = arcs[i]
        pts.extend(seg if not pts else seg[1:])
    return pts


def load_countries():
    """-> {country_name: [ring, ring, ...]} in lon/lat degrees."""
    topo = json.load(open(TOPO))
    arcs = _decode_arcs(topo)
    out = {}
    for g in topo['objects']['countries']['geometries']:
        name = g['properties'].get('name')
        if not name:
            continue
        rings = []
        if g['type'] == 'Polygon':
            for r in g['arcs']:
                rings.append(_ring(arcs, r))
        elif g['type'] == 'MultiPolygon':
            for poly in g['arcs']:
                for r in poly:
                    rings.append(_ring(arcs, r))
        out[name] = rings
    return out


# ------------------------------------------- name harmonisation (documented)
# Left: the label used in the extraction dataset. Right: the Natural Earth
# name. Every substitution is listed so the mapping is auditable.
ALIAS = {
    'USA': 'United States of America',
    'United States': 'United States of America',
    'UK': 'United Kingdom',
    'United Kingdom': 'United Kingdom',
    'Turkey': 'Turkey',
    'Turkiye': 'Turkey',
    'Arabia': 'Saudi Arabia',
    'Korea': 'South Korea',
    'Republic of Korea': 'South Korea',
    'Netherlands': 'Netherlands',
    'Czech Republic': 'Czechia',
    'Bosnia': 'Bosnia and Herz.',
    'Dominican Republic': 'Dominican Rep.',
    'Ivory Coast': "Côte d'Ivoire",
    'Burkina Faso': 'Burkina Faso',
    'Congo': 'Dem. Rep. Congo',
    'DRC': 'Dem. Rep. Congo',
    'Serbia': 'Serbia',
    'Taiwan': 'Taiwan',
    'Hong Kong': 'China',
}

# Values that are not countries and are therefore excluded from the map but
# reported in the figure note.
NON_COUNTRY = {'Global', 'Not reported', ''}

# Multi-country labels are expanded to their constituent states for mapping
# only; the tabulated distribution keeps the aggregate label.
MULTI = {
    'Sahel (multi-country)': ['Burkina Faso', 'Mali', 'Niger', 'South Sudan'],
    'Europe (multi-country)': ['France', 'Germany', 'Italy', 'Spain',
                               'United Kingdom', 'Turkey'],
}


def draw_choropleth(ax, counts, cbar_ax=None, cbar_label=None,
                    unmapped_note=True):
    """counts: {label: int}. Returns (n_mapped, unmatched list)."""
    geo = load_countries()
    vals, unmatched, non_country = {}, [], {}
    for label, n in counts.items():
        if label in NON_COUNTRY:
            non_country[label] = n
            continue
        for part in MULTI.get(label, [label]):
            nm = ALIAS.get(part, part)
            if nm in geo:
                vals[nm] = vals.get(nm, 0) + n
            else:
                unmatched.append(part)

    vmax = max(vals.values()) if vals else 1
    norm = Normalize(vmin=0, vmax=vmax)

    patches, colors = [], []
    for name, rings in geo.items():
        v = vals.get(name)
        c = SEQ(norm(v)) if v else NODATA
        for r in rings:
            if len(r) < 4:
                continue
            a = np.asarray(r, dtype=float)
            # Drop degenerate rings: a zero-area or hairline-thin ring renders
            # as a stray line across the plate carree canvas.
            area = 0.5 * abs(np.dot(a[:, 0], np.roll(a[:, 1], 1))
                             - np.dot(a[:, 1], np.roll(a[:, 0], 1)))
            if area < 1e-3 or (a[:, 1].max() - a[:, 1].min()) < 0.05:
                continue
            # A ring that spans more than half the globe in longitude has been
            # stitched across the antimeridian: drawn as-is it smears the
            # country right across the map (this is what put a full-width
            # sliver through Russia, Fiji and Antarctica). Unwrap it into a
            # contiguous 0-360 range and draw both the eastern and the western
            # copy, letting the axis limits clip whichever falls outside.
            if a[:, 0].max() - a[:, 0].min() > 180.0:
                b = a.copy()
                b[b[:, 0] < 0, 0] += 360.0
                for shift in (0.0, -360.0):
                    q = b.copy()
                    q[:, 0] += shift
                    if q[:, 0].max() < -180 or q[:, 0].min() > 180:
                        continue
                    patches.append(Polygon(q, closed=True))
                    colors.append(c)
                continue
            patches.append(Polygon(a, closed=True))
            colors.append(c)
    pc = PatchCollection(patches, facecolor=colors, edgecolor='#FFFFFF',
                         linewidths=0.25, zorder=2)
    ax.add_collection(pc)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-58, 84)
    ax.set_aspect(1.0)
    ax.axis('off')

    if cbar_ax is not None:
        sm = cm.ScalarMappable(norm=norm, cmap=SEQ)
        sm.set_array([])
        cb = ax.figure.colorbar(sm, cax=cbar_ax, orientation='horizontal')
        # integer ticks only -- the quantity is a count of studies
        step = max(1, int(np.ceil(vmax / 5)))
        ticks = list(range(0, vmax + 1, step))
        # add the maximum only if it will not sit on top of the previous tick
        if ticks[-1] != vmax:
            if vmax - ticks[-1] >= step * 0.55:
                ticks.append(vmax)
            else:
                ticks[-1] = vmax
        cb.set_ticks(ticks)
        cb.set_ticklabels([str(t) for t in ticks])
        cb.outline.set_linewidth(0.4)
        cb.outline.set_edgecolor(INK2)
        cb.ax.tick_params(labelsize=7, width=0.5, length=2.5)
        cb.set_label(cbar_label or 'Number of included studies (count)',
                     fontsize=7.5, color=INK2, labelpad=4)
        # explicit no-data swatch, immediately left of the bar
        cb.ax.add_patch(
            __import__('matplotlib').patches.Rectangle(
                (-0.115, 0), 0.075, 1, transform=cb.ax.transAxes,
                facecolor=NODATA, edgecolor=INK2, linewidth=0.4,
                clip_on=False))
        cb.ax.text(-0.125, 0.5, 'no studies', transform=cb.ax.transAxes,
                   ha='right', va='center', fontsize=7, color=INK3)

    return sum(vals.values()), unmatched, non_country
