"""Reproduce the four figures in the research brief from the tables in results/.

Run from the repository root:  python scripts/make_brief_figures.py
Municipal boundaries (geoBoundaries gbOpen, PHL ADM3/ADM0) are downloaded on first run.
"""
import numpy as np, pandas as pd, geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

import os, urllib.request
RES = "results/"
OUT = "figures/"
CACHE = "data/"
os.makedirs(OUT, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
GB = "https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/main/releaseData/gbOpen/PHL/{lvl}/geoBoundaries-PHL-{lvl}_simplified.geojson"
for lvl in ("ADM3", "ADM0"):
    path = f"{CACHE}PHL_{lvl}.geojson"
    if not os.path.exists(path):
        urllib.request.urlretrieve(GB.format(lvl=lvl), path)

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
BLUE, ORANGE = "#2a78d6", "#eb6834"
RAMP = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]      # ordinal, validated on white
LAND, NOMEAS = "#f0efec", "#d9d8d1"
plt.rcParams.update({"font.family": ["Liberation Sans", "Arial", "DejaVu Sans"], "font.size": 9, "axes.edgecolor": AXIS,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": INK2,
                     "text.color": INK, "axes.titlecolor": INK, "figure.facecolor": "white",
                     "axes.facecolor": "white", "savefig.facecolor": "white", "hatch.color": "#b3b2aa",
                     "hatch.linewidth": 0.5})

def tidy(ax, grid_axis="x"):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)

EVENTS = [("mangkhut_2018", "Mangkhut (Ompong), Sep 2018"), ("kammuri_2019", "Kammuri (Tisoy), Dec 2019"),
          ("phanfone_2019", "Phanfone (Ursula), Dec 2019"), ("rai_2021", "Rai (Odette), Dec 2021")]

# ---------------------------------------------------------------- Figure 1: map
adm3 = gpd.read_file(CACHE + "PHL_ADM3.geojson")
adm0 = gpd.read_file(CACHE + "PHL_ADM0.geojson")
L = pd.read_csv(RES + "labels_step2b.csv")
bins = [-np.inf, 20, 50, 80, np.inf]
labels_cls = ["Below 20%", "20–49%", "50–79%", "80% or more"]
colors_cls = RAMP[::-1]                 # darkest = least light
fig, axes = plt.subplots(2, 2, figsize=(7.2, 8.6))
xmin, xmax, ymin, ymax = 116.9, 126.9, 7.7, 19.9
for ax, (key, title) in zip(axes.flat, EVENTS):
    e = L[L.event == key]
    g = adm3.merge(e[["shapeID", "duration_source", "min_pct_w0_3"]], on="shapeID", how="inner")
    adm0.plot(ax=ax, color=LAND, edgecolor="none")
    meas = g[g.duration_source != "none"].copy()
    meas["cls"] = pd.cut(meas.min_pct_w0_3, bins, labels=range(4), right=False).astype(int)   # [20, 50) etc.
    nomeas = g[g.duration_source == "none"]
    nomeas.plot(ax=ax, facecolor=NOMEAS, edgecolor="white", lw=0.15, hatch="//////")
    for c in range(4):
        sub = meas[meas.cls == c]
        if len(sub):
            sub.plot(ax=ax, color=colors_cls[c], edgecolor="white", lw=0.15)
    adm0.boundary.plot(ax=ax, color=AXIS, lw=0.3)
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal"); ax.set_axis_off()
    ax.set_title(title, loc="left", fontsize=9.5, pad=3)
    ax.text(0.99, 0.985, f"{len(meas)} of {len(g)}\nmunicipalities\nmeasurable", ha="right", va="top",
            transform=ax.transAxes, fontsize=8, color=INK2, linespacing=1.15)
handles = [Patch(facecolor=colors_cls[i], edgecolor="none", label=labels_cls[i]) for i in range(4)][::-1]
handles.append(Patch(facecolor=NOMEAS, edgecolor="#b3b2aa", hatch="//////", lw=0.3, label="Not measurable (too few lit pixels)"))
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=8,
           title="Lowest nighttime light in the 4 weeks after landfall (% of pre-storm level)",
           title_fontsize=8.5, bbox_to_anchor=(0.5, 0.0), handlelength=1.6, columnspacing=1.4)
fig.subplots_adjust(left=0.01, right=0.99, top=0.97, bottom=0.075, wspace=0.03, hspace=0.07)
fig.savefig(OUT + "fig1_map.png", dpi=220)
plt.close(fig)

# ---------------------------------------------------------------- Figure 2: label validation
C = pd.read_csv(RES + "step4_calibration.csv")
chosen = {"mangkhut_2018": 70, "kammuri_2019": 50, "phanfone_2019": 60, "rai_2021": 50}
fig, ax = plt.subplots(figsize=(7.2, 3.0))
series = [("real > 7 d (≤30 km)", -0.22, dict(color=BLUE)), ("real > 7 d (>100 km)", 0.0, dict(color=ORANGE)),
          ("placebo > 7 d", 0.22, dict(facecolor="white", edgecolor=INK2, lw=1.2))]
for i, (key, title) in enumerate(EVENTS):
    r = C[(C.event == key) & (C.level == chosen[key])].iloc[0]
    for col, dy, sty in series:
        v = r[col]
        ax.plot([0, v], [i + dy, i + dy], color=GRID, lw=1.4, zorder=1, solid_capstyle="round")
        ax.scatter(v, i + dy, s=40, zorder=3, **({"edgecolor": "white", "lw": 1.0} | sty))
    ax.text(r["real > 7 d (≤30 km)"] + 2, i - 0.22, f"{r['real > 7 d (≤30 km)']:.0f}%", va="center", fontsize=8, color=INK2)
    ax.text(max(r["placebo > 7 d"], 0) + 2, i + 0.22, f"{r['placebo > 7 d']:.1f}%", va="center", fontsize=8, color=INK2)
    ax.text(r["real > 7 d (>100 km)"] + 2, i, f"{r['real > 7 d (>100 km)']:.0f}%", va="center", fontsize=8, color=INK2)
ax.set_yticks(range(4), [f"{t.split(' (')[0]} {t.split()[-1]}\nthreshold {chosen[k]}%" for k, t in EVENTS])
ax.set_ylim(3.5, -0.75)
ax.set_xlim(-1.5, 100)
ax.set_xlabel("Municipalities with an outage longer than 7 days (%)")
tidy(ax)
ax.legend(handles=[Line2D([], [], marker="o", ls="", color=BLUE, ms=6, label="Within 30 km of the track"),
                   Line2D([], [], marker="o", ls="", color=ORANGE, ms=6, label="More than 100 km away"),
                   Line2D([], [], marker="o", ls="", mfc="white", mec=INK2, ms=6, label="Placebo, all distances (no storm)")],
          loc="lower left", bbox_to_anchor=(-0.02, 0.97), ncol=3, frameon=False, fontsize=8, handletextpad=0.3)
fig.subplots_adjust(left=0.17, right=0.98, top=0.9, bottom=0.16)
fig.savefig(OUT + "fig2_labels.png", dpi=220)
plt.close(fig)

# ---------------------------------------------------------------- Figure 3: transfer
B = pd.read_csv(RES + "step4_bootstrap.csv")
b = B[(B.label == "calibrated") & (B.model == "Logistic regression")].set_index("set")
order = [("H", "Hazard only"),
         ("H+Sgeo", "+ neighbouring wind, island size"),
         ("H+S", "+ neighbouring wind, island size, utility"),
         ("H+E", "+ exposure"),
         ("H+E+S", "+ exposure, neighbouring wind, island size, utility"),
         ("H+E+Emb3", "+ exposure, embeddings (3 components)"),
         ("H+E+Emb10", "+ exposure, embeddings (10 components)")]
fig, ax = plt.subplots(figsize=(7.2, 3.3))
for i, (k, name) in enumerate(order):
    r = b.loc[k]
    ax.plot([r["LOTO AUC"], r["random-split AUC"]], [i, i], color="#ecebe6", lw=9, solid_capstyle="butt", zorder=1)
    ax.hlines(i, r["CI low"], r["CI high"], color=BLUE, lw=1.2, zorder=2)
    ax.scatter(r["LOTO AUC"], i, s=48, color=BLUE, zorder=3, edgecolor="white", lw=1.2)
    ax.scatter(r["random-split AUC"], i, s=48, facecolor="white", edgecolor=INK2, lw=1.2, zorder=3)
    ax.text(0.925, i, f"{r['transfer loss']:.2f}", va="center", ha="right", fontsize=8.5, color=INK2)
ax.text(0.925, -0.95, "Gap (shaded)", ha="right", va="center", fontsize=8.5, color=INK2, fontweight="bold")
ax.axvline(b.loc["H", "LOTO AUC"], color=BLUE, lw=0.6, alpha=0.5, zorder=0)
ax.axhline(0.5, color=AXIS, lw=0.6); ax.axhline(2.5, color=AXIS, lw=0.6)
ax.set_yticks(range(len(order)), [n for _, n in order])
ax.set_ylim(len(order) - 0.5, -1.4)
ax.set_xlim(0.6, 0.93)
ax.set_xticks(np.arange(0.6, 0.91, 0.05))
ax.set_xlabel("AUC")
tidy(ax)
fig.legend(handles=[Line2D([], [], marker="o", ls="", color=BLUE, ms=6.5, label="Unseen typhoon: mean of 4 held-out storms, 95% CI"),
                   Line2D([], [], marker="o", ls="", mfc="white", mec=INK2, ms=6.5, label="Random split: mean of 15 folds")],
          loc="upper right", bbox_to_anchor=(0.98, 0.995), ncol=2, frameon=False, fontsize=8, handletextpad=0.3)
fig.subplots_adjust(left=0.43, right=0.98, top=0.9, bottom=0.14)
fig.savefig(OUT + "fig3_transfer.png", dpi=220)
plt.close(fig)

# ---------------------------------------------------------------- Figure 4: equity
V = pd.read_csv(RES + "step4_coverage.csv")
fig, ax = plt.subplots(figsize=(7.2, 1.9))
for i, r in V.iterrows():
    n_meas = round(r["share measurable"] * r["municipalities in swath"])
    ax.barh(i, r["share measurable"] * 100, color=BLUE, height=0.56)
    ax.text(r["share measurable"] * 100 + 1.2, i, f"{r['share measurable']*100:.0f}%  ({n_meas} of {r['municipalities in swath']})",
            va="center", fontsize=8.5, color=INK)
ax.set_yticks(range(len(V)), ["Poorest third", "Middle third", "Richest third"])
ax.invert_yaxis(); ax.set_xlim(0, 100)
ax.set_xlabel("Municipality–storm pairs whose outage could be measured from satellite (%)")
tidy(ax)
fig.subplots_adjust(left=0.17, right=0.98, top=0.95, bottom=0.27)
fig.savefig(OUT + "fig4_equity.png", dpi=220)
plt.close(fig)
print("done")
