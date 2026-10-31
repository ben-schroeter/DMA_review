"""Chart: obligations a firm faces at each size, by type of company (company-specific rules plus the baseline that
applies to every company). Online platforms continue into the designated band as gatekeepers and very large platforms.
Reads data/firm_size/summary.json (scripts/firm_size.py). Writes site/firm_size.svg. Run from research/ceps_metrics."""
import json

d = json.load(open("data/firm_size/summary.json"))
INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
COL = {"FI": "#8F6708", "PR": "#B8860B", "CL": "#004494", "TC": "#5C5858", "PL": "#7FA3CC", "B": "#A6A3A0"}
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
base = d["baseline"]
SHORT = {"FI": "Finance, payments and crypto", "PR": "Makers of connected products", "CL": "Cloud, data and AI", "TC": "Telecoms",
         "PL": "Online platforms", "B": "Any other company"}
series = {}
for k in ("FI", "PR", "CL", "TC"):
    series[k] = [a + b for a, b in zip(d["types"][k]["specific"], base)][:5]
pl = [a + b for a, b in zip(d["types"]["PL"]["specific"], base)][:5]
series["PL"] = pl + [d["types"]["GK"]["specific"][5] + base[5]]       # platforms become gatekeepers / very large platforms
series["B"] = base[:5]
COLS = ["Micro", "Small", "Medium", "Small mid-cap", "Large", "Designated"]
SUB = ["under 10 staff", "10–49", "50–249", "250–749", "750+", "gatekeepers, VLOPs"]
W, H, L, R, T, Bm = 1000, 470, 64, 760, 40, 64
YM = 6000
X = lambda i: L + 20 + i * (R - L - 40) / 5
Y = lambda v: H - Bm - v / YM * (H - Bm - T)
g = []
for v in range(0, YM + 1, 1000):
    g.append(f'<line x1="{L}" x2="{R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>' + t(L - 10, Y(v) + 4.5, f"{v:,}", 13, MUTED, "end"))
for i, (c, s) in enumerate(zip(COLS, SUB)):
    g.append(t(X(i), H - Bm + 22, c, 13.5, INK, "middle", 600) + t(X(i), H - Bm + 39, s, 12, MUTED, "middle"))
g.append(t(L, T - 18, "Obligations a firm faces: rules for its type plus those for every company", 13, MUTED))
ends = []
for k, ys in series.items():
    pts = [(X(i), Y(v)) for i, v in enumerate(ys)]
    d_ = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    sw = 2.6 if k != "B" else 2
    dash = ' stroke-dasharray="5 4"' if k == "B" else ""
    g.append(f'<path d="{d_}" fill="none" stroke="{COL[k]}" stroke-width="{sw}"{dash}></path>')
    for i, (x, y) in enumerate(pts):
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{COL[k]}" stroke="{BG}" stroke-width="1.5"><title>{SHORT[k]}, {COLS[i].lower()}: {ys[i]:,} obligations</title></circle>')
    ends.append([pts[-1][1], k, ys])
ends.sort()
for i in range(1, len(ends)):                     # keep end labels apart
    if ends[i][0] - ends[i - 1][0] < 34:
        ends[i][0] = ends[i - 1][0] + 34
for y, k, ys in ends:
    x = X(len(ys) - 1) + 14
    rel = (ys[-1] if k != "PL" else ys[4]) - ys[0]
    note = f"{ys[0]:,} → {ys[-1]:,}" if ys[-1] != ys[0] else f"{ys[0]:,} at every size"
    g.append(t(x, y + 1, SHORT[k], 13.5, COL[k] if k not in ("B", "TC") else INK, "start", 600) + t(x, y + 17, note, 12.5, MUTED))
aria = "Obligations a firm faces at each size, by type of company: " + "; ".join(f"{SHORT[k]} from {ys[0]:,} (micro) to {ys[-1]:,}" for k, ys in series.items())
open("site/firm_size.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
for k, ys in series.items():
    print(k, ys, f"micro faces {ys[0] / ys[4]:.0%} of large")
a = d["all_company_obligations"]
print("all company obligations", a, f"micro {a[0] / a[4]:.1%} of large")
