"""Charts and figures for In Numbers > What companies say (site/mockup/CompanyResponses.dc.html).

Reads the frequency study in data/company_responses/ (frequency_all_*.csv, trend_controls.csv,
trend_by_type.csv, law_patterns_all.json, universe/universe.json) and the database (digital_rulebook.xlsx).
Writes site/cr_trend.svg, cr_types.svg, cr_laws.svg, cr_size.svg, cr_timing.svg and
site/company_responses_facts.json (read by site/facts.py). Run from research/digital_rulebook.
"""
import collections, csv, json, math, statistics as st
import openpyxl

D = "data/company_responses/"
INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD, GOLD_D, STONE, LIGHT, BAND = "#B8860B", "#8F6708", "#A6A3A0", "#E3CF9C", "#F1E6C8"
F = 'font-family="DM Sans, sans-serif"'


def t(x, y, s, size=13, fill=INK2, anchor="start", weight=None):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
            + (f' font-weight="{weight}"' if weight else "") + f">{s}</text>")


def svg(path, w, h, aria, g):
    open(f"site/{path}", "w").write(f'<svg viewBox="0 0 {w} {h:.0f}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")


# ---------- data ----------
laws = {l["id"]: l for l in json.load(open(D + "law_patterns_all.json"))["laws"] if l["scope"] == "eu"}
rep = [r for r in csv.DictReader(open(D + "frequency_all_reports.csv", encoding="utf-8")) if r["words"]]
men = [m for m in csv.DictReader(open(D + "frequency_all_mentions.csv", encoding="utf-8"))
       if int(m["year"]) >= laws[m["law"]].get("min_year", 0)]
trend = collections.defaultdict(dict)
for x in csv.DictReader(open(D + "trend_controls.csv", encoding="utf-8")):
    trend[x["method"]][int(x["year"])] = x
bytype = collections.defaultdict(dict)
for x in csv.DictReader(open(D + "trend_by_type.csv", encoding="utf-8")):
    bytype[(x["type"], x["method"])][int(x["year"])] = x
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True)
rows = list(wb["instruments"].iter_rows(values_only=True)); ix = {k: i for i, k in enumerate(rows[0])}
db = {r[ix["row_id"]]: r for r in rows[1:]}
yr = lambda v: int(str(v)[:4]) if v and str(v)[:4].isdigit() else None
short = {"GDPR": "GDPR", "DMA": "Digital Markets Act", "AI_ACT": "AI Act", "R60": "Digital Services Act", "R57": "DORA", "R56": "MiCA",
         "R61": "NIS2", "R23": "PSD2", "R83": "Cyber Resilience Act", "R76": "Data Act", "R141": "Anti-Money Laundering Dir.",
         "R9": "ePrivacy Directive", "R139": "RoHS", "R19": "Tax reporting (DAC)", "R128": "Consumer Credit Directive",
         "R32": "Electronic Comms Code", "R63": "Roaming Regulation", "R8": "E-commerce Directive", "R11": "EU Merger Regulation",
         "R140": "WEEE Directive", "R136": "Vehicle General Safety Reg.", "R33": "Copyright (DSM) Directive"}
nm = lambda lid: short.get(lid, laws[lid]["name"])
YEARS = list(range(2010, 2026))
facts = {}

# ---------- 1. trend: raw and fixed effects, two panels ----------
raw, fe_l, fe_r = trend["raw"], trend["fe: laws"], trend["fe: log_rate"]
W, LM, PW, GX, PH, TOP = 1000, 44, 430, 70, 250, 64
g = [f'<line x1="{LM}" x2="{LM + 26}" y1="12" y2="12" stroke="{STONE}" stroke-width="2" stroke-dasharray="5 4"></line>' + t(LM + 32, 16, "All reports in the sample each year (raw)", 13),
     f'<rect x="{LM + 330}" y="5" width="26" height="14" fill="{BAND}"></rect><line x1="{LM + 330}" x2="{LM + 356}" y1="12" y2="12" stroke="{GOLD}" stroke-width="2"></line>'
     + t(LM + 362, 16, "Same companies and sources (fixed effects, 95% band)", 13)]
panels = [("EU laws named per report", 4, [1, 2, 3, 4],
           lambda y: float(raw[y]["laws"]),
           lambda y, k=0: float(raw[2010]["laws"]) + float(fe_l[y]["coef"]) + k * 1.96 * float(fe_l[y]["se"]), "{:.1f}"),
          ("Mentions of EU laws per 100,000 words", 6, [2, 4, 6],
           lambda y: math.exp(float(raw[y]["log_rate"])) - 1,
           lambda y, k=0: math.exp(float(raw[2010]["log_rate"]) + float(fe_r[y]["coef"]) + k * 1.96 * float(fe_r[y]["se"])) - 1, "{:.1f}")]
for i, (title, ym, ticks, fr, ff, fmt) in enumerate(panels):
    x0, y0 = LM + i * (PW + GX), TOP
    X = lambda y, x0=x0: x0 + (y - YEARS[0]) / (YEARS[-1] - YEARS[0]) * PW
    Y = lambda v, y0=y0, ym=ym: y0 + PH - max(0, min(v, ym)) / ym * PH
    g.append(t(x0, y0 - 18, title, 14, INK, weight=600))
    for v in ticks:
        g.append(f'<line x1="{x0}" x2="{x0 + PW}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"></line>' + t(x0 - 6, Y(v) + 4, v, 11.5, MUTED, "end"))
    g.append(f'<line x1="{x0}" x2="{x0 + PW}" y1="{Y(0):.1f}" y2="{Y(0):.1f}" stroke="{BASE}"></line>' + t(x0 - 6, Y(0) + 4, 0, 11.5, MUTED, "end"))
    for y in (2010, 2016, 2018, 2020, 2025):
        g.append(t(X(y), y0 + PH + 16, y, 11.5, MUTED, "middle"))
    for y, lab in ((2016, "GDPR adopted"), (2020, "second wave proposed")):
        g.append(f'<line x1="{X(y):.1f}" x2="{X(y):.1f}" y1="{y0}" y2="{y0 + PH}" stroke="{STONE}" stroke-dasharray="2 3"></line>' + t(X(y) + 4, y0 + 10, lab, 11, MUTED))
    band = " ".join(f"{X(y):.1f},{Y(ff(y, 1)):.1f}" for y in YEARS) + " " + " ".join(f"{X(y):.1f},{Y(ff(y, -1)):.1f}" for y in reversed(YEARS))
    g.append(f'<polygon points="{band}" fill="{BAND}"></polygon>')
    g.append(f'<polyline points="{" ".join(f"{X(y):.1f},{Y(fr(y)):.1f}" for y in YEARS)}" fill="none" stroke="{STONE}" stroke-width="2" stroke-dasharray="5 4"></polyline>')
    g.append(f'<polyline points="{" ".join(f"{X(y):.1f},{Y(ff(y)):.1f}" for y in YEARS)}" fill="none" stroke="{GOLD}" stroke-width="2"></polyline>')
    g.append(f'<circle cx="{X(2025):.1f}" cy="{Y(ff(2025)):.1f}" r="4" fill="{GOLD}" stroke="{BG}" stroke-width="2"></circle>')
    g.append(t(X(2025) + 8, Y(ff(2025)) + 4, fmt.format(ff(2025)), 12.5, INK, weight=600))
    g.append(t(X(2025) + 8, Y(fr(2025)) + (16 if fr(2025) < ff(2025) else -6), fmt.format(fr(2025)), 12, MUTED))
    for y in YEARS:   # hover
        g.append(f'<rect x="{X(y) - PW / 30:.1f}" y="{y0}" width="{PW / 15:.1f}" height="{PH}" fill="transparent"><title>{y}: raw {fmt.format(fr(y))}; same companies and sources {fmt.format(ff(y))} ({fmt.format(ff(y, -1))} to {fmt.format(ff(y, 1))})</title></rect>')
H = TOP + PH + 30
svg("cr_trend.svg", W, H, "Attention to EU laws in annual reports, 2010 to 2025. EU laws named per report: "
    + f"{float(raw[2010]['laws']):.1f} in 2010, {float(raw[2025]['laws']):.1f} in 2025 (raw); {panels[0][4](2025):.1f} for the same companies and sources. "
    + f"Mentions per 100,000 words in a typical report: {panels[1][3](2010):.1f} in 2010, {panels[1][3](2025):.1f} in 2025 (raw); {panels[1][4](2025):.1f} for the same companies and sources.", g)
facts.update(cr_laws_2010=(float(raw[2010]["laws"]), f'{float(raw[2010]["laws"]):.1f}'),
             cr_laws_2025=(float(raw[2025]["laws"]), f'{float(raw[2025]["laws"]):.1f}'),
             cr_fe_laws_2025=(float(fe_l[2025]["coef"]), f'{float(fe_l[2025]["coef"]):.1f}'),
             cr_nongdpr_2010=(float(raw[2010]["non_gdpr"]), f'{float(raw[2010]["non_gdpr"]) * 100:.0f}%'),
             cr_nongdpr_2025=(float(raw[2025]["non_gdpr"]), f'{float(raw[2025]["non_gdpr"]) * 100:.0f}%'),
             cr_fe_nongdpr_2025=(float(trend["fe: non_gdpr"][2025]["coef"]), f'{float(trend["fe: non_gdpr"][2025]["coef"]) * 100:.0f}'),
             cr_rate_2010=(panels[1][3](2010), f"{panels[1][3](2010):.1f}"), cr_rate_2025=(panels[1][3](2025), f"{panels[1][3](2025):.1f}"),
             cr_rate_fe_2025=(panels[1][4](2025), f"{panels[1][4](2025):.1f}"),
             cr_rate_2018=(panels[1][3](2018), f"{panels[1][3](2018):.1f}"), cr_rate_2023=(panels[1][3](2023), f"{panels[1][3](2023):.1f}"),
             cr_reports_fe=(int(fe_l[2025]["n_reports"]), f'{int(fe_l[2025]["n_reports"]):,}'))

# ---------- 2. by company type: small multiples of the fixed-effects change ----------
TN = {"GK": "Gatekeepers and very large platforms", "TC": "Telecoms", "FI": "Finance, payments and crypto",
      "CL": "Cloud, data and AI", "PL": "Online platforms and digital services", "PR": "Makers of connected products"}
order = sorted(TN, key=lambda k: -float(bytype[(k, "fe: laws")][2025]["coef"]))
NC, PW2, GX2, PH2, GY2, LM2 = 3, 270, 46, 150, 78, 40
YMIN, YMAX = -1, 7
g = []
for i, k in enumerate(order):
    x0, y0 = LM2 + (i % NC) * (PW2 + GX2), 54 + (i // NC) * (PH2 + GY2)
    X = lambda y, x0=x0: x0 + (y - 2010) / 15 * PW2
    Y = lambda v, y0=y0: y0 + PH2 - (max(YMIN, min(v, YMAX)) - YMIN) / (YMAX - YMIN) * PH2
    fe = bytype[(k, "fe: laws")]; n = fe[2025]["n_companies"]
    for v in (0, 2, 4, 6):
        g.append(f'<line x1="{x0}" x2="{x0 + PW2}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>')
        if i % NC == 0:
            g.append(t(x0 - 6, Y(v) + 4, f"+{v}" if v else "0", 11, MUTED, "end"))
    band = " ".join(f"{X(y):.1f},{Y(float(fe[y]['coef']) + 1.96 * float(fe[y]['se'])):.1f}" for y in YEARS) + " " + \
           " ".join(f"{X(y):.1f},{Y(float(fe[y]['coef']) - 1.96 * float(fe[y]['se'])):.1f}" for y in reversed(YEARS))
    g.append(f'<polygon points="{band}" fill="{BAND}"></polygon>')
    g.append(f'<polyline points="{" ".join(f"{X(y):.1f},{Y(float(fe[y]["coef"])):.1f}" for y in YEARS)}" fill="none" stroke="{GOLD}" stroke-width="2"></polyline>')
    for y in (2010, 2025):
        g.append(t(X(y), y0 + PH2 + 15, y, 11, MUTED, "middle"))
    v25 = float(fe[2025]["coef"])
    g.append(t(x0, y0 - 22, TN[k] if len(TN[k]) < 34 else TN[k].replace(" and digital services", ", digital services"), 13.5, INK, weight=600))
    g.append(t(x0, y0 - 6, f'<tspan fill="{GOLD_D}" font-weight="600">+{v25:.1f}</tspan> laws named by 2025 · {n} companies', 12, MUTED))
    g.append(f'<rect x="{x0}" y="{y0}" width="{PW2}" height="{PH2}" fill="transparent"><title>{TN[k]}: '
             + "; ".join(f"{y} {float(fe[y]['coef']):+.1f}" for y in (2016, 2018, 2020, 2022, 2025)) + "</title></rect>")
    facts[f"cr_type_{k}"] = (v25, f"{v25:.1f}")
H = 54 + 2 * (PH2 + GY2) - GY2 + 24
svg("cr_types.svg", 1000, H, "Change since 2010 in the number of EU laws named per report, within the same companies and sources, by type of company: "
    + "; ".join(f"{TN[k]} +{float(bytype[(k, 'fe: laws')][2025]['coef']):.1f} by 2025" for k in order), g)

ns = [int(bytype[(k, "fe: laws")][2025]["n_companies"]) for k in TN]
facts.update(cr_type_n_min=(min(ns), str(min(ns))), cr_type_n_max=(max(ns), str(max(ns))))

# ---------- 3. which laws: share of companies naming each law since 2020, by region ----------
reg = {r["company"]: r["region"] for r in rep}
ncomp = collections.Counter(reg[c] for c in {r["company"] for r in rep if int(r["year"]) >= 2020})
named = collections.defaultdict(lambda: collections.defaultdict(set))
for m in men:
    if int(m["year"]) >= 2020:
        named[m["law"]][reg[m["company"]]].add(m["company"])
allc = sum(ncomp.values())
top = sorted(named, key=lambda l: -sum(len(v) for v in named[l].values()))[:15]
REGS = [("US", "US companies"), ("EU", "EU companies"), ("UK", "UK companies")]
LBL, PW3, GX3, RH = 200, 230, 30, 26
g = []
for j, (rk, rl) in enumerate(REGS):
    x0 = LBL + j * (PW3 + GX3)
    g.append(t(x0, 18, f"{rl} ({ncomp[rk]})", 13.5, INK, weight=600))
    for v in (0, 50, 100):
        xx = x0 + v / 100 * PW3
        g.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="30" y2="{36 + len(top) * RH}" stroke="{LINE if v else BASE}"></line>' + t(xx, 50 + len(top) * RH, f"{v}%", 11, MUTED, "middle"))
for i, l in enumerate(top):
    y = 36 + i * RH
    g.append(t(LBL - 10, y + 16, nm(l), 13, INK2, "end"))
    for j, (rk, rl) in enumerate(REGS):
        x0 = LBL + j * (PW3 + GX3); s = len(named[l][rk]) / ncomp[rk]
        g.append(f'<rect x="{x0}" y="{y + 5}" width="{max(s * PW3, 1.5):.1f}" height="16" rx="3" fill="{GOLD}"><title>{nm(l)}: {len(named[l][rk])} of {ncomp[rk]} {rl} ({s * 100:.0f}%)</title></rect>')
        g.append(t(x0 + s * PW3 + 5, y + 17, f"{s * 100:.0f}%", 11.5, MUTED))
H = 60 + len(top) * RH
svg("cr_laws.svg", 1000, H, "Share of companies naming each EU law in an annual report since 2020, by region: "
    + "; ".join(f"{nm(l)} US {len(named[l]['US']) / ncomp['US'] * 100:.0f}%, EU {len(named[l]['EU']) / ncomp['EU'] * 100:.0f}%, UK {len(named[l]['UK']) / ncomp['UK'] * 100:.0f}%" for l in top), g)
for l, key in (("AI_ACT", "ai"), ("R57", "dora"), ("R60", "dsa"), ("DMA", "dma"), ("R61", "nis2"), ("GDPR", "gdpr")):
    for rk in ("US", "EU", "UK"):
        s = len(named[l][rk]) / ncomp[rk]
        facts[f"cr_{key}_{rk.lower()}"] = (s, f"{s * 100:.0f}%")
facts["cr_top_n"] = (len(top), str(len(top)))
facts.update(cr_n_us=(ncomp["US"], str(ncomp["US"])), cr_n_eu=(ncomp["EU"], str(ncomp["EU"])), cr_n_uk=(ncomp["UK"], str(ncomp["UK"])))

# ---------- 4. attention vs size of the law ----------
comp = collections.defaultdict(set)
for m in men:
    comp[m["law"]].add(m["company"])
pts = [(db[l["row_id"]][ix["addr_private_parties"]] or 0, len(comp[lid]), lid) for lid, l in laws.items()]
W4, LM4, TM4, PW4, PH4 = 1000, 64, 20, 880, 380
XM, YMX = 3000, 130
X = lambda v: LM4 + math.log10(1 + v) / math.log10(1 + XM) * PW4
Y = lambda v: TM4 + PH4 - math.log10(1 + v) / math.log10(1 + YMX) * PH4
g = []
for v in (0, 10, 100, 1000):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{TM4}" y2="{TM4 + PH4}" stroke="{LINE}"></line>' + t(X(v), TM4 + PH4 + 18, f"{v:,}", 11.5, MUTED, "middle"))
for v in (0, 1, 10, 100):
    g.append(f'<line x1="{LM4}" x2="{LM4 + PW4}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>' + t(LM4 - 8, Y(v) + 4, v, 11.5, MUTED, "end"))
g.append(t(LM4 + PW4, TM4 + PH4 + 38, "Obligations on companies in the law (log scale)", 12.5, MUTED, "end"))
g.append(t(LM4 - 8, TM4 - 6, "Companies naming it", 12.5, MUTED, "start"))
LAB = {"GDPR", "DMA", "AI_ACT", "R57", "R60", "R61", "R65", "R135", "R103", "R110", "R81", "R139"}
for o, c, lid in sorted(pts, key=lambda p: p[2] in LAB):
    hi = lid in LAB
    g.append(f'<circle cx="{X(o):.1f}" cy="{Y(c):.1f}" r="{5 if hi else 4}" fill="{GOLD if hi else STONE}" stroke="{BG}" stroke-width="2" fill-opacity="{1 if hi else 0.8}"><title>{laws[lid]["name"]}: {o:,} obligations on companies; named by {c} companies</title></circle>')
    if hi:
        # label position (dy, anchor) chosen so that labels of neighbouring laws do not overlap
        pos = {"R65": (-10, "start", 6), "R103": (-26, "middle", 0), "R110": (-10, "end", -6), "R81": (-10, "end", -6), "R135": (-10, "start", 6)}
        dy, anc, dx = pos.get(lid, (-10, "middle", 0))
        lab = {"R65": "Machinery Regulation", "R135": "In-vitro diagnostics Reg.", "R103": "Toys Safety Regulation",
               "R110": "Radio Equipment Directive", "R81": "Health Data Space"}.get(lid, nm(lid))
        g.append(t(X(o) + dx, Y(c) + dy, lab, 11.5, INK, anc))
# fitted curves: second-degree polynomial (least squares) of log(1 + companies) on log(1 + obligations), the scales of the chart.
# The legend gives the correlation r (as in the text) and the curve's R².
import numpy as _np
for P, dash, col, lab in ((pts, "6 5", MUTED, "all laws"), ([p for p in pts if p[1] >= 2], "", GOLD_D, "laws named by 2+ companies")):
    xs_ = _np.array([math.log1p(p[0]) for p in P]); ys_ = _np.array([math.log1p(p[1]) for p in P])
    cf = _np.polyfit(xs_, ys_, 2); fit = _np.polyval(cf, xs_)
    r2 = 1 - ((ys_ - fit) ** 2).sum() / ((ys_ - ys_.mean()) ** 2).sum()
    r = float(_np.corrcoef(xs_, ys_)[0, 1])
    us = _np.linspace(xs_.min(), xs_.max(), 60)
    pts_ = " ".join(f"{X(math.expm1(u)):.1f},{Y(max(math.expm1(float(_np.polyval(cf, u))), 0)):.1f}" for u in us)
    g.append(f'<polyline points="{pts_}" fill="none" stroke="{col}" stroke-width="2"' + (f' stroke-dasharray="{dash}"' if dash else "") + "></polyline>")
    ly = TM4 + 14 + (0 if dash else 20)   # legend, top left of the plot (no dots there)
    g.append(f'<line x1="{LM4 + 14}" x2="{LM4 + 44}" y1="{ly - 4}" y2="{ly - 4}" stroke="{col}" stroke-width="2"' + (f' stroke-dasharray="{dash}"' if dash else "") + "></line>")
    g.append(t(LM4 + 52, ly, f"Polynomial fit, {lab}: r = {r:.2f}, R² = {r2:.2f}", 12.5, col, "start", 600))
H = TM4 + PH4 + 44
svg("cr_size.svg", W4, H, "Each EU law by the number of obligations it places on companies and the number of companies naming it in an annual report. "
    "The GDPR, the AI Act, DORA and the platform laws are widely named; large product laws such as the Machinery Regulation, the Toys Safety Regulation and the Radio Equipment Directive are never named.", g)
xs = [math.log1p(p[0]) for p in pts]; ys = [math.log1p(p[1]) for p in pts]
mx, my = st.mean(xs), st.mean(ys)
corr = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / math.sqrt(sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys))
never = [p for p in pts if p[1] == 0]; wide = [p for p in pts if p[1] >= 10]
# the same correlation among laws that at least two companies name (laws nobody names pull the overall figure down)
_p2 = [p for p in pts if p[1] >= 2]
_x2 = [math.log1p(p[0]) for p in _p2]; _y2 = [math.log1p(p[1]) for p in _p2]
_mx2, _my2 = st.mean(_x2), st.mean(_y2)
corr2 = sum((a - _mx2) * (b - _my2) for a, b in zip(_x2, _y2)) / math.sqrt(sum((a - _mx2) ** 2 for a in _x2) * sum((b - _my2) ** 2 for b in _y2))
facts.update(cr_corr_size=(corr, f"{corr:.2f}"), cr_corr_named2=(corr2, f"{corr2:.2f}"), cr_named2_n=(len(_p2), str(len(_p2))), cr_laws_never=(len(never), str(len(never))), cr_laws_named=(len(pts) - len(never), str(len(pts) - len(never))),
             cr_laws_total=(len(pts), str(len(pts))), cr_never_median_oblig=(st.median(p[0] for p in never), f"{st.median(p[0] for p in never):.0f}"),
             cr_wide_n=(len(wide), str(len(wide))), cr_wide_median_oblig=(st.median(p[0] for p in wide), f"{st.median(p[0] for p in wide):.0f}"),
             cr_machinery_oblig=(db[laws["R65"]["row_id"]][ix["addr_private_parties"]], f'{db[laws["R65"]["row_id"]][ix["addr_private_parties"]]:,}'))

# ---------- 5. timing: proposal, adoption and first mentions ----------
first = collections.defaultdict(dict)
for m in men:
    c, l, y = m["company"], m["law"], int(m["year"])
    first[l][c] = min(first[l].get(c, 9999), y)
TL = ["GDPR", "R23", "R60", "DMA", "R57", "R61", "AI_ACT", "R76"]
Y0, Y1 = 2012, 2026
LBL5, PW5, RH5, TOP5 = 190, 620, 38, 46
X = lambda y: LBL5 + (y - Y0) / (Y1 - Y0) * PW5
g = [f'<circle cx="{LBL5 + 6}" cy="12" r="5" fill="{BG}" stroke="{INK2}" stroke-width="2"></circle>' + t(LBL5 + 16, 16, "Proposed", 12.5),
     f'<rect x="{LBL5 + 96}" y="7" width="10" height="10" fill="{INK2}"></rect>' + t(LBL5 + 112, 16, "Adopted", 12.5),
     f'<line x1="{LBL5 + 186}" x2="{LBL5 + 216}" y1="12" y2="12" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" stroke-opacity="0.45"></line>'
     + f'<path d="M{LBL5 + 201},6 l6,6 l-6,6 l-6,-6 z" fill="{GOLD}"></path>' + t(LBL5 + 224, 16, "First mention by companies: middle half, and median", 12.5)]
for y in range(Y0, Y1 + 1, 2):
    g.append(f'<line x1="{X(y):.1f}" x2="{X(y):.1f}" y1="{TOP5 - 6}" y2="{TOP5 + len(TL) * RH5}" stroke="{LINE}"></line>' + t(X(y), TOP5 + len(TL) * RH5 + 16, y, 11.5, MUTED, "middle"))
for i, l in enumerate(TL):
    r = db[laws[l]["row_id"]]; p, a = yr(r[ix["proposal_date"]]), yr(r[ix["adoption_date"]])
    fs = sorted(first[l].values()); q1, q2, q3 = fs[len(fs) // 4], st.median(fs), fs[(3 * len(fs)) // 4]
    before = sum(f < a for f in fs) / len(fs)
    y = TOP5 + i * RH5 + RH5 / 2
    g.append(t(LBL5 - 10, y + 4, nm(l), 13, INK2, "end"))
    g.append(f'<line x1="{X(p):.1f}" x2="{X(a):.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{BASE}" stroke-width="2"></line>')
    g.append(f'<line x1="{X(q1):.1f}" x2="{X(q3) + 0.01:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GOLD}" stroke-width="8" stroke-linecap="round" stroke-opacity="0.45"></line>')
    g.append(f'<circle cx="{X(p):.1f}" cy="{y:.1f}" r="5" fill="{BG}" stroke="{INK2}" stroke-width="2"></circle>')
    g.append(f'<rect x="{X(a) - 5:.1f}" y="{y - 5:.1f}" width="10" height="10" fill="{INK2}"></rect>')
    g.append(f'<path d="M{X(q2):.1f},{y - 7:.1f} l7,7 l-7,7 l-7,-7 z" fill="{GOLD}" stroke="{BG}" stroke-width="1.5"></path>')
    g.append(t(LBL5 + PW5 + 14, y + 4, f"{before * 100:.0f}% before adoption", 12, MUTED))
    g.append(f'<rect x="{LBL5}" y="{y - RH5 / 2:.1f}" width="{PW5}" height="{RH5}" fill="transparent"><title>{nm(l)}: proposed {p}, adopted {a}; {len(fs)} companies name it; median first mention {q2:.0f}; {before * 100:.0f}% first named it before adoption</title></rect>')
    facts[f"cr_before_{l.lower()}"] = (before, f"{before * 100:.0f}%")
    facts[f"cr_median_first_{l.lower()}"] = (q2, f"{q2:.0f}")
    facts[f"cr_companies_{l.lower()}"] = (len(fs), str(len(fs)))
H = TOP5 + len(TL) * RH5 + 26
svg("cr_timing.svg", 1000, H, "When companies first name a law, compared with its proposal and adoption: "
    + "; ".join(f"{nm(l)} proposed {yr(db[laws[l]['row_id']][ix['proposal_date']])}, adopted {yr(db[laws[l]['row_id']][ix['adoption_date']])}, median first mention {facts['cr_median_first_' + l.lower()][1]}" for l in TL), g)

# ---------- other figures ----------
have = collections.defaultdict(set)
for r in rep:
    have[r["company"]].add(int(r["year"]))
ment = collections.defaultdict(set)
for m in men:
    ment[(m["company"], m["law"])].add(int(m["year"]))
cont = sum(1 for (c, l), ys in ment.items() for y in ys if y + 1 in have[c] and y + 1 in ys)
tot = sum(1 for (c, l), ys in ment.items() for y in ys if y + 1 in have[c])
u = json.load(open(D + "universe/universe.json"))["companies"]
types_ai = {(c.get("company_types") or "").split(";")[0] for c in u if c["id"] in first["AI_ACT"]}
rate = lambda c, y, l: next((float(m["per_100k"]) for m in men if m["company"] == c and int(m["year"]) == y and m["law"] == l), 0.0)
gdpr_rates = [float(m["per_100k"]) for m in men if m["law"] == "GDPR" and int(m["year"]) == 2024]
facts.update(cr_companies=(len({r["company"] for r in rep}), str(len({r["company"] for r in rep}))),
             cr_reports=(len(rep), f"{len(rep):,}"), cr_year_first=(min(int(r["year"]) for r in rep), str(min(int(r["year"]) for r in rep))),
             cr_persist=(cont / tot, f"{cont / tot * 100:.0f}%"), cr_ai_types=(len(types_ai), {6: "all six", 5: "five"}.get(len(types_ai), str(len(types_ai)))),
             cr_meta_gdpr_2024=(rate("meta-platforms", 2024, "GDPR"), f'{rate("meta-platforms", 2024, "GDPR"):.0f}'),
             cr_gdpr_median_2024=(st.median(gdpr_rates), f"{st.median(gdpr_rates):.0f}"),
             cr_apple_dma_2023=(rate("apple", 2023, "DMA"), f'{rate("apple", 2023, "DMA"):.0f}'), cr_apple_dma_2024=(rate("apple", 2024, "DMA"), f'{rate("apple", 2024, "DMA"):.0f}'),
             cr_meta_dma_2022=(rate("meta-platforms", 2022, "DMA"), f'{rate("meta-platforms", 2022, "DMA"):.0f}'), cr_meta_dma_2024=(rate("meta-platforms", 2024, "DMA"), f'{rate("meta-platforms", 2024, "DMA"):.0f}'),
             cr_booking_dma_2023=(rate("booking-holdings", 2023, "DMA"), f'{rate("booking-holdings", 2023, "DMA"):.0f}'), cr_booking_dma_2024=(rate("booking-holdings", 2024, "DMA"), f'{rate("booking-holdings", 2024, "DMA"):.0f}'))
json.dump({k: {"value": v, "text": s} for k, (v, s) in facts.items()}, open("site/company_responses_facts.json", "w"), indent=1)
print({k: s for k, (v, s) in facts.items()})

# ---------- top five companies per company type (table below the 'by type' chart) ----------
# Measure: distinct EU tech laws named per annual report, averaged over each company's 2024 and 2025 reports; second column:
# mentions per 100,000 words. Each company counts under its main type (the first listed in universe/company_types.json).
import csv as _csv, html as _html
_T = json.load(open("data/company_responses/universe/company_types.json"))["types"]
_reps = [r for r in _csv.DictReader(open("data/company_responses/frequency_all_reports.csv")) if r["report_status"] == "ok"]
_men = list(_csv.DictReader(open("data/company_responses/frequency_all_mentions.csv")))
_name = {r["company"]: r["name"] for r in _reps}; _hq = {r["company"]: r["hq"] for r in _reps}
_laws, _rate = collections.defaultdict(set), collections.defaultdict(float)
for m in _men:
    _laws[(m["company"], int(m["year"]))].add(m["law"]); _rate[(m["company"], int(m["year"]))] += float(m["per_100k"] or 0)
_YRS = (2024, 2025)
_by = collections.defaultdict(list)
for c in {r["company"] for r in _reps}:
    ys = sorted({int(r["year"]) for r in _reps if r["company"] == c and int(r["year"]) in _YRS})
    t = _T.get(_name[c])
    if not ys or not t or t.get("status") not in ("include", "borderline"):
        continue
    _by[t["types"].split(";")[0]].append((st.mean(len(_laws[(c, y)]) for y in ys), st.mean(_rate[(c, y)] for y in ys), _name[c], _hq[c]))
_LAB = [("TC", "Telecoms"), ("GK", "Gatekeepers and very large platforms"), ("FI", "Finance, payments and crypto"),
        ("CL", "Cloud, data and AI"), ("PL", "Online platforms and digital services"), ("PR", "Makers of connected products")]
_cells = []
for k, lab in _LAB:
    L = sorted(_by[k], key=lambda x: (-x[0], -x[1]))
    rows = "".join(f'<tr><td style="padding: 5px 8px 5px 0; border-bottom: 1px solid #EFEDE9">{_html.escape(nm)} <span style="color: {MUTED}; font-size: 12.5px">{h}</span></td>'
                   f'<td style="padding: 5px 8px; border-bottom: 1px solid #EFEDE9; text-align: right; font-weight: 600">{n:.1f}</td>'
                   f'<td style="padding: 5px 0 5px 8px; border-bottom: 1px solid #EFEDE9; text-align: right; color: {MUTED}">{f:.0f}</td></tr>' for n, f, nm, h in L[:5])
    _cells.append(f'<div style="display: flex; flex-direction: column; gap: 6px"><p style="margin: 0; font-weight: 600; font-size: 15px">{lab}</p>'
                  f'<p class="cap" style="margin: 0">{len(L)} companies; median {st.median(x[0] for x in L):.1f} laws per report</p>'
                  f'<table style="border-collapse: collapse; font-size: 14px; width: 100%; font-variant-numeric: tabular-nums"><thead><tr>'
                  f'<th style="text-align: left; font-weight: 500; color: {MUTED}; font-size: 12px; padding: 0 8px 4px 0">Company</th>'
                  f'<th style="text-align: right; font-weight: 500; color: {MUTED}; font-size: 12px; padding: 0 8px 4px">Laws</th>'
                  f'<th style="text-align: right; font-weight: 500; color: {MUTED}; font-size: 12px; padding: 0 0 4px 8px">Per 100k words</th></tr></thead><tbody>{rows}</tbody></table></div>')
open("site/cr_top_by_type.html", "w").write('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 28px 40px">' + "".join(_cells) + "</div>")
print("top by type:", {k: [x[2] for x in sorted(_by[k], key=lambda x: (-x[0], -x[1]))[:5]] for k, _ in _LAB})
