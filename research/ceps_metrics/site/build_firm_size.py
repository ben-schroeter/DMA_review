"""Chart: obligations a firm faces at each size, by type of company (company-specific rules plus the general rules that
apply to any company in the digital economy). Online platforms continue into the designated band as gatekeepers and
very large platforms; cloud, data and AI as providers of general-purpose AI models with systemic risk.
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
         "PL": "Online platforms", "B": "Any other company in the digital economy"}
tot = lambda k: [a + b for a, b in zip(d["types"][k]["specific"], base)]
series = {"PR": tot("PR")[:5], "FI": tot("FI")[:5], "CL": tot("CL"), "TC": tot("TC")[:5],
          "PL": tot("PL")[:5] + [d["types"]["GK"]["specific"][5] + base[5]],      # platforms become gatekeepers / very large platforms
          "B": base[:5]}
COLS = ["Micro", "Small", "Medium", "Small mid-cap", "Large", "Designated"]
SUB = ["under 10 staff", "10–49", "50–249", "250–749", "750+", "gatekeepers, VLOPs, GPAI"]
W, H, L, R, T, Bm = 1000, 470, 64, 990, 110, 56
YM = 6000
X = lambda i: L + 50 + i * (R - L - 110) / 5
Y = lambda v: H - Bm - v / YM * (H - Bm - T)
g = []
for v in range(0, YM + 1, 1000):
    g.append(f'<line x1="{L}" x2="{R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>' + t(L - 10, Y(v) + 4.5, f"{v:,}", 13, MUTED, "end"))
for i, (c, s) in enumerate(zip(COLS, SUB)):
    g.append(t(X(i), H - Bm + 22, c, 13.5, INK, "middle", 600) + t(X(i), H - Bm + 39, s, 12, MUTED, "middle"))
ORDER = ["PR", "FI", "CL", "TC", "PL", "B"]
for k in ORDER:
    ys = series[k]
    pts = [(X(i), Y(v)) for i, v in enumerate(ys)]
    dash = ' stroke-dasharray="5 4"' if k == "B" else ""
    g.append(f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{COL[k]}" stroke-width="{2 if k == "B" else 2.6}"{dash}></path>')
    for i, (x, y) in enumerate(pts):
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{COL[k]}" stroke="{BG}" stroke-width="1.5"><title>{SHORT[k]}, {COLS[i].lower()}: {ys[i]:,} obligations</title></circle>')
for n, k in enumerate(ORDER):                    # legend above the plot: three columns, two rows
    ys = series[k]
    lx, ly = [0, 340, 680][n % 3], 16 + (n // 3) * 44
    dash = ' stroke-dasharray="5 4"' if k == "B" else ""
    g.append(f'<line x1="{lx}" x2="{lx + 22}" y1="{ly - 4}" y2="{ly - 4}" stroke="{COL[k]}" stroke-width="3"{dash}></line>')
    g.append(t(lx + 30, ly, SHORT[k], 13.5, INK, "start", 600))
    g.append(t(lx + 30, ly + 17, f"{ys[0]:,} at micro → {ys[-1]:,} {'designated' if len(ys) == 6 else 'at large'}", 12.5, MUTED))
aria = "Obligations a firm faces at each size, by type of company: " + "; ".join(f"{SHORT[k]} from {series[k][0]:,} (micro) to {series[k][-1]:,}" for k in ORDER)
open("site/firm_size.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
for k in ORDER:
    print(k, series[k], f"micro faces {series[k][0] / series[k][4]:.0%} of large")
a = d["all_company_obligations"]
print("all company obligations", a, f"micro {a[0] / a[4]:.1%} of large")
