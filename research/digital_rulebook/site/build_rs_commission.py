"""Rules vs standards in obligations on companies, by the Commission that proposed the law (Rules vs Standards page, intro).
Small 100% columns per Commission term: rules, standards (standards, mixed and specified-later provisions) and duties left to
member states. Main acts only; implementing and delegated acts are shown elsewhere on the page.
Reads data/rules_standards/by_commission.json (scripts/rs_by_commission.py) and data/rules_standards/grid/summary.json
(scripts/grid_aggregate.py); records the intro figures through site/counts.py. Writes site/rs_commission.svg.
Run from research/digital_rulebook."""
import json, os, subprocess, sys
sys.path.insert(0, "site"); from counts import record

subprocess.run([sys.executable, "scripts/rs_by_commission.py"], check=True, capture_output=True)   # keep the input current
rows = [r for r in json.load(open("data/rules_standards/by_commission.json")) if r["layer"] == "main" and r["companies"]["n"]]
rows = rows[[r["commission"] for r in rows].index("Prodi"):]   # from Prodi on: the Delors and Santer laws carry too few company obligations
INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
RULE, STD, MS = "#8F6708", "#7FA3CC", "#D4D2CE"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="middle", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                     + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
SMALL = 100          # terms with fewer company obligations than this are drawn faded (too few to read a share from)
# line of the standards share only, on a zoomed axis, so the change between Commissions is visible
W, L, R, TOP, H = 720, 48, 700, 30, 190
n = len(rows); X = lambda i: L + 20 + i * (R - L - 40) / (n - 1)
vals = [r["companies"]["standards"] for r in rows]
big = [i for i, r in enumerate(rows) if r["companies"]["n"] >= SMALL]
lo = max(0.0, (min(vals[i] for i in big) // 0.05) * 0.05 - 0.05); hi = (max(vals) // 0.05) * 0.05 + 0.05
Y = lambda v: TOP + H * (hi - min(max(v, lo), hi)) / (hi - lo)
GOLD, GOLD_D = "#B8860B", "#8F6708"
g = []
v = lo
while v <= hi + 1e-9:
    g.append(f'<line x1="{L}" x2="{R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"></line>' + t(L - 8, Y(v) + 4, f"{v:.0%}", 11.5, MUTED, "end")); v += 0.05
g.append(t(L - 8, TOP - 14, "Share of standards", 12, MUTED, "start"))
pts = [(X(i), Y(vals[i])) for i in big]
g.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{GOLD}" stroke-width="2.5" stroke-linejoin="round"></polyline>')
first, last = big[0], big[-1]
for i, r in enumerate(rows):
    c = r["companies"]; x, y = X(i), Y(vals[i]); faded = c["n"] < SMALL; key = i in (first, last)
    tip = f'<title>{r["commission"]}: {c["n"]:,} obligations on companies in {r["acts"]} laws; standards {vals[i]:.0%}, rules {c["rules"]:.0%}</title>'
    if faded:
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#FFFFFF" stroke="{BASE}" stroke-width="1.5">{tip}</circle>' + t(x, y - 10, f"{vals[i]:.0%}", 11.5, BASE))
    else:
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{7 if key else 5}" fill="{GOLD_D if key else GOLD}" stroke="{BG}" stroke-width="2">{tip}</circle>')
        g.append(t(x, y - 13, f"{vals[i]:.0%}", 16 if key else 12.5, INK if key else INK2, weight=700 if key else 500))
    g.append(t(x, TOP + H + 20, r["commission"].replace("von der Leyen", "vdL"), 12.5, MUTED if faded else INK2))
    g.append(t(x, TOP + H + 36, f'{c["n"]:,} obl.', 11, BASE if faded else MUTED))
svg = (f'<svg viewBox="0 0 {W} {TOP + H + 46}" width="100%" role="img" aria-label="Share of standards in obligations on companies in EU digital laws, by the Commission that proposed the law: '
       + "; ".join(f'{r["commission"]} {r["companies"]["standards"]:.0%}' for r in rows) + '">' + "".join(g) + "</svg>")
open("site/rs_commission.svg", "w").write(svg)

# figures quoted in the intro
by = {r["commission"]: r for r in rows}
record("rs_co_prodi", round(100 * by["Prodi"]["companies"]["standards"]), f'{by["Prodi"]["companies"]["standards"]:.0%}')
last = rows[-1]
record("rs_co_latest", round(100 * last["companies"]["standards"]), f'{last["companies"]["standards"]:.0%}')
record("rs_co_latest_term", last["commission"], {"von der Leyen I": "first term", "von der Leyen II": "second term"}.get(last["commission"], last["commission"]))
G = json.load(open("data/rules_standards/grid/summary.json"))["groups"]
record("grid_xm_co_pre2010", round(100 * G["companies_period|before 2010"]["XM"]), f'{G["companies_period|before 2010"]["XM"]:.0%}')
record("grid_xm_co_2018", round(100 * G["companies_period|2018 or later"]["XM"]), f'{G["companies_period|2018 or later"]["XM"]:.0%}')
print("rs by commission (companies, standards):", {r["commission"]: (r["companies"]["n"], r["companies"]["standards"]) for r in rows})
