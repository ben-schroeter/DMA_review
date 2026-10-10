"""Generate inline-SVG charts for the website mockup's front page (palette and fonts match the mockup).
Writes site/mock_charts.json: {name: svg string}. Run from research/ceps_metrics."""
import datetime as dt, json, statistics
import openpyxl

INK, INK2, MUTED, LINE, BASE = "#141413", "#3D3D3A", "#6B6A64", "#E6E3D9", "#C9C6BA"
CLAY, CLAY2, SLATE, STONE = "#D97757", "#EDB9A3", "#5E5D59", "#BDBAAE"
F = "font-family=\"DM Sans, sans-serif\""
wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)


def sheet(n):
    rows = list(wb[n].values); h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r[0] is not None]


inst = [r for r in sheet("instruments") if r["adoption_date"] and r["restrictions_total"] is not None and r["status_oct2026"] == "adopted"]
for r in inst:
    r["d"] = dt.date.fromisoformat(str(r["adoption_date"])[:10])
    r["type"] = {"R": "Regulation", "L": "Directive", "D": "Decision"}[r["celex_measured"].split(";")[0][5]]
sec = [r for r in sheet("secondary_acts") if r["kind"] in ("implementing", "delegated") and r["date"] and r["restrictions_total"] is not None]
for r in sec:
    r["d"] = dt.date.fromisoformat(str(r["date"])[:10])
Y0, Y1 = 1986.0, 2027.0
fy = lambda d: d.year + (d.timetuple().tm_yday - 1) / 365.25
W, H, L, R, T, B = 1000, 360, 64, 110, 20, 36
X = lambda y: L + (y - Y0) / (Y1 - Y0) * (W - L - R)


def axes(ymax, ticks, fmt=lambda v: f"{v:,.0f}"):
    Yf = lambda v: H - B - v / ymax * (H - B - T)
    g = [f'<line x1="{L}" x2="{W - R}" y1="{Yf(t):.1f}" y2="{Yf(t):.1f}" stroke="{LINE}"></line>' for t in ticks]
    g += [f'<text x="{L - 10}" y="{Yf(t) + 5:.1f}" text-anchor="end" {F} font-size="14" fill="{MUTED}">{fmt(t)}</text>' for t in ticks if t]
    g += [f'<text x="{X(y):.1f}" y="{H - 10}" text-anchor="middle" {F} font-size="14" fill="{MUTED}">{y}</text>' for y in (1990, 2000, 2010, 2020)]
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{H - B}" y2="{H - B}" stroke="{BASE}"></line>')
    return Yf, g


def step(points, Yf, base=None):
    """points: [(year_float, value)] sorted; returns path for step-after line and, with base, the area down to base series."""
    d = f"M{L},{Yf(points[0][1]):.1f}"
    for y, v in points:
        d += f"H{X(y):.1f}V{Yf(v):.1f}"
    d += f"H{X(Y1 - 0.3):.1f}"
    return d


def stack_paths(series, Yf):
    """series: list of (label, color, [(year, cumvalue_total_of_this_and_below)]) bottom to top -> filled bands."""
    out, prev = [], None
    for lab, col, pts in series:
        top = [f"M{L},{Yf(0):.1f}"] if False else []
        up = step(pts, Yf)
        if prev is None:
            area = up + f"V{Yf(0):.1f}H{L}Z"
        else:
            # walk back along previous top
            back = ""
            for y, v in reversed(prev):
                back += f"V{Yf(v):.1f}H{X(y):.1f}"
            area = up + f"V{Yf(prev[-1][1]):.1f}" + back[back.find('H'):] if back else up
            area = up + "".join([f"V{Yf(prev[-1][1]):.1f}"]) + rev_path(prev, Yf) + "Z"
        out.append(f'<path d="{area}" fill="{col}" stroke="#FAF9F5" stroke-width="1"></path>')
        prev = pts
    return out


def rev_path(pts, Yf):
    s = ""
    for i in range(len(pts) - 1, -1, -1):
        y, v = pts[i]
        s += f"H{X(y):.1f}V{Yf(pts[i - 1][1] if i else 0):.1f}"
    return s + f"H{L}"


charts = {}

# A. cumulative number of adopted acts by legal type (stacked)
order = ["Regulation", "Directive", "Decision"]
cols = {"Regulation": CLAY, "Directive": SLATE, "Decision": STONE}
ev = sorted(inst, key=lambda r: r["d"])
cum = {t: 0 for t in order}; pts = {t: [(Y0, 0)] for t in order}
for r in ev:
    cum[r["type"]] += 1
    y = fy(r["d"]); run = 0
    for t in order:
        run += cum[t]; pts[t].append((y, run))
tot = sum(cum.values())
Yf, g = axes(120, [0, 20, 40, 60, 80, 100, 120])
bands = stack_paths([(t, cols[t], pts[t]) for t in order], Yf)
lab = []
run = 0
for t in order:
    mid = run + cum[t] / 2; run += cum[t]
    lab.append(f'<text x="{W - R + 10}" y="{Yf(mid) + 5:.1f}" {F} font-size="14" fill="{INK2}">{t}s {cum[t]}</text>')
charts["acts_by_type"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Cumulative number of adopted EU digital acts by legal type: '
                          f'{cum["Regulation"]} regulations, {cum["Directive"]} directives, {cum["Decision"]} decisions">' + "".join(g + bands + lab) + "</svg>")

# B. cumulative restrictions: main acts vs implementing and delegated acts
evs = sorted([(fy(r["d"]), r["restrictions_total"], 0) for r in inst] + [(fy(r["d"]), 0, r["restrictions_total"]) for r in sec])
m = s = 0; pm = [(Y0, 0)]; ps = [(Y0, 0)]
for y, a, b in evs:
    m += a; s += b; pm.append((y, m)); ps.append((y, m + s))
Yf, g = axes(35000, [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000])
bands = stack_paths([("main", CLAY, pm), ("sec", CLAY2, ps)], Yf)
lab = [f'<text x="{W - R + 10}" y="{Yf(m / 2) + 5:.1f}" {F} font-size="14" fill="{INK2}">Main acts</text>',
       f'<text x="{W - R + 10}" y="{Yf(m / 2) + 23:.1f}" {F} font-size="14" fill="{INK}" font-weight="600">{m:,}</text>',
       f'<text x="{W - R + 10}" y="{Yf(m + s / 2) - 4:.1f}" {F} font-size="14" fill="{INK2}">Implementing</text>',
       f'<text x="{W - R + 10}" y="{Yf(m + s / 2) + 13:.1f}" {F} font-size="14" fill="{INK2}">&amp; delegated</text>',
       f'<text x="{W - R + 10}" y="{Yf(m + s / 2) + 31:.1f}" {F} font-size="14" fill="{INK}" font-weight="600">{s:,}</text>']
charts["main_vs_secondary"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Cumulative restrictions: {m:,} in the main acts and {s:,} in '
                               f'implementing and delegated acts">' + "".join(g + bands + lab) + "</svg>")
meta = {"acts_by_type": cum, "main": m, "secondary": s}

# C. proposal vs adopted (45-degree line)
cmp = [r for r in inst if isinstance(r.get("proposal_restrictions_total"), (int, float))]
mx = 1200
S, P = 560, 56
sx = lambda v: P + v / mx * (S - P - 16)
sy = lambda v: S - P - v / mx * (S - P - 16)
g = []
for t in (0, 300, 600, 900, 1200):
    g.append(f'<line x1="{P}" x2="{S - 16}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" stroke="{LINE}"></line>')
    g.append(f'<text x="{P - 8}" y="{sy(t) + 5:.1f}" text-anchor="end" {F} font-size="13" fill="{MUTED}">{t}</text>')
    g.append(f'<text x="{sx(t):.1f}" y="{S - P + 22}" text-anchor="middle" {F} font-size="13" fill="{MUTED}">{t}</text>')
g.append(f'<line x1="{sx(0):.1f}" y1="{sy(0):.1f}" x2="{sx(mx):.1f}" y2="{sy(mx):.1f}" stroke="{SLATE}" stroke-width="1.2" stroke-dasharray="5 4"></line>')
g.append(f'<text x="{sx(1050):.1f}" y="{sy(1080):.1f}" {F} font-size="13" fill="{SLATE}" text-anchor="end" transform="rotate(-45 {sx(1050):.1f} {sy(1080):.1f})">no change</text>')
above = sum(r["restrictions_total"] > r["proposal_restrictions_total"] for r in cmp)
for r in cmp:
    c = CLAY if r["restrictions_total"] > r["proposal_restrictions_total"] else SLATE
    g.append(f'<circle cx="{sx(min(r["proposal_restrictions_total"], mx)):.1f}" cy="{sy(min(r["restrictions_total"], mx)):.1f}" r="5" fill="{c}" fill-opacity="0.75" stroke="#FAF9F5" stroke-width="1.2"></circle>')
big = sorted(cmp, key=lambda r: -(r["restrictions_total"] - r["proposal_restrictions_total"]))[:4]
for r in big:
    nm = r["name"].replace("Artificial Intelligence Act", "AI Act").replace("General Data Protection Regulation", "GDPR").replace("Markets in Crypto-Assets (MiCA)", "MiCA").split(" (")[0]
    g.append(f'<text x="{sx(r["proposal_restrictions_total"]) + 9:.1f}" y="{sy(r["restrictions_total"]) + 4:.1f}" {F} font-size="13" fill="{INK2}">{nm}</text>')
g.append(f'<text x="{(P + S) / 2:.0f}" y="{S - 8}" text-anchor="middle" {F} font-size="13" fill="{MUTED}">Restrictions in the Commission proposal</text>')
g.append(f'<text x="14" y="{(S - P) / 2:.0f}" text-anchor="middle" {F} font-size="13" fill="{MUTED}" transform="rotate(-90 14 {(S - P) / 2:.0f})">Restrictions in the adopted act</text>')
charts["proposal_vs_adopted"] = (f'<svg viewBox="0 0 {S} {S}" width="100%" style="max-width: 560px" role="img" aria-label="{above} of {len(cmp)} acts have more '
                                 f'restrictions after adoption than in the proposal">' + "".join(g) + "</svg>")
meta.update({"cmp_n": len(cmp), "cmp_above": above})

# D. EU acts vs Sarbanes-Oxley: per act (bars) and density (strip)
sox = json.load(open("data/benchmark_sox.json"))["all_text"]
recent = [r for r in inst if r["d"].year >= 2020]
pick = ["Artificial Intelligence Act", "Digital Services Act", "General Data Protection Regulation", "Digital Markets Act", "Data Act"]
bars = [(n.replace("General Data Protection Regulation", "GDPR").replace("Artificial Intelligence Act", "AI Act"),
         next(r["restrictions_total"] for r in inst if r["name"] == n), CLAY) for n in pick]
bars += [("EU average since 2020", round(statistics.mean(r["restrictions_total"] for r in recent)), STONE),
         ("EU average, all 105", round(statistics.mean(r["restrictions_total"] for r in inst)), STONE),
         ("Sarbanes-Oxley Act (US)", sox["restrictions_total"], INK)]
bars.sort(key=lambda b: -b[1])
BW, rowh, LB = 1000, 40, 230
mxb = 800
g = []
for i, (n, v, c) in enumerate(bars):
    y = 10 + i * rowh
    w = v / mxb * (BW - LB - 70)
    g.append(f'<text x="{LB - 14}" y="{y + 20}" text-anchor="end" {F} font-size="15" fill="{INK if c == INK else INK2}" {"font-weight=\"600\"" if c == INK else ""}>{n}</text>')
    g.append(f'<rect x="{LB}" y="{y + 6}" width="{w:.1f}" height="20" rx="4" fill="{c}"></rect>')
    g.append(f'<text x="{LB + w + 10:.1f}" y="{y + 21}" {F} font-size="15" fill="{INK}" font-weight="600">{v:,}</text>')
charts["sox_per_act"] = (f'<svg viewBox="0 0 {BW} {10 + len(bars) * rowh + 6}" width="100%" role="img" aria-label="Restrictions per act: recent EU acts '
                         f'against the Sarbanes-Oxley Act ({sox["restrictions_total"]})">' + "".join(g) + "</svg>")
dens = sorted(1000 * r["restrictions_total"] / max(1, (r["words_articles"] or 0) + (r["words_annexes"] or 0)) for r in inst)
med = statistics.median(dens)
DW, DH = 1000, 150
dx = lambda v: 30 + v / 40 * (DW - 60)
g = [f'<line x1="30" x2="{DW - 30}" y1="{DH - 40}" y2="{DH - 40}" stroke="{BASE}"></line>']
for t in (0, 10, 20, 30, 40):
    g.append(f'<text x="{dx(t):.1f}" y="{DH - 14}" text-anchor="middle" {F} font-size="13" fill="{MUTED}">{t}</text>')
import random
random.seed(4)
for v in dens:
    g.append(f'<circle cx="{dx(min(v, 40)):.1f}" cy="{DH - 72 + random.uniform(-16, 16):.1f}" r="4.5" fill="{CLAY}" fill-opacity="0.45"></circle>')
g.append(f'<line x1="{dx(med):.1f}" x2="{dx(med):.1f}" y1="{DH - 100}" y2="{DH - 44}" stroke="{CLAY}" stroke-width="2.5"></line>')
g.append(f'<text x="{dx(med):.1f}" y="{DH - 108}" text-anchor="middle" {F} font-size="14" fill="{INK}" font-weight="600">EU median {med:.1f}</text>')
g.append(f'<line x1="{dx(sox["per_1000_words"]):.1f}" x2="{dx(sox["per_1000_words"]):.1f}" y1="{DH - 100}" y2="{DH - 44}" stroke="{INK}" stroke-width="2.5"></line>')
g.append(f'<text x="{dx(sox["per_1000_words"]):.1f}" y="{DH - 108}" text-anchor="end" {F} font-size="14" fill="{INK}" font-weight="600">SOX {sox["per_1000_words"]:g}</text>')
charts["sox_density"] = (f'<svg viewBox="0 0 {DW} {DH}" width="100%" role="img" aria-label="Restrictions per 1,000 words: median EU act {med:.1f}, '
                         f'Sarbanes-Oxley {sox["per_1000_words"]:g}">' + "".join(g) + "</svg>")
meta.update({"eu_median_density": round(med, 1), "sox": sox["restrictions_total"], "sox_density": sox["per_1000_words"]})

# E. productivity, EA-4 relative to US (1995 = 100)
pdat = json.load(open("data/external/ea4_us_productivity.json"))
PW, PH, PL, PR, PT, PB = 1000, 420, 50, 50, 30, 40
px = lambda y: PL + (y - 1900) / (2022 - 1900) * (PW - PL - PR)
py = lambda v: PH - PB - v / 115 * (PH - PB - PT)
g = [f'<rect x="{px(1945):.1f}" y="{PT}" width="{px(1995) - px(1945):.1f}" height="{PH - PB - PT}" fill="#5E7FA8" fill-opacity="0.06"></rect>',
     f'<rect x="{px(1995):.1f}" y="{PT}" width="{px(2022) - px(1995):.1f}" height="{PH - PB - PT}" fill="{CLAY}" fill-opacity="0.08"></rect>']
for t in (20, 40, 60, 80):
    g.append(f'<line x1="{PL}" x2="{PW - PR}" y1="{py(t):.1f}" y2="{py(t):.1f}" stroke="{LINE}"></line>')
    g.append(f'<text x="{PW - PR + 8}" y="{py(t) + 5:.1f}" {F} font-size="13" fill="{MUTED}">{t}</text>')
g.append(f'<line x1="{PL}" x2="{PW - PR}" y1="{py(100):.1f}" y2="{py(100):.1f}" stroke="{INK}" stroke-width="1.2"></line>')
g.append(f'<text x="{PL + 4}" y="{py(100) - 8:.1f}" {F} font-size="14" fill="{INK}" font-weight="600">1995 level = 100</text>')
for y in (1900, 1920, 1945, 1970, 1995, 2022):
    g.append(f'<text x="{px(y):.1f}" y="{PH - 14}" text-anchor="middle" {F} font-size="13" fill="{MUTED}">{y}</text>')
g.append(f'<line x1="{PL}" x2="{PW - PR}" y1="{PH - PB}" y2="{PH - PB}" stroke="{BASE}"></line>')
seg = lambda a, b: " ".join(f"{px(o['year']):.1f},{py(o['ratio_1995_100']):.1f}" for o in pdat if a <= o["year"] <= b)
fill = seg(1995, 2022) + f" {px(2022):.1f},{py(100):.1f} {px(1995):.1f},{py(100):.1f}"
g.append(f'<polygon points="{fill}" fill="{CLAY}" fill-opacity="0.22"></polygon>')
for (a, b), c in (((1900, 1945), "#9C9A92"), ((1945, 1995), "#5E7FA8"), ((1995, 2022), CLAY)):
    g.append(f'<polyline points="{seg(a, b)}" fill="none" stroke="{c}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"></polyline>')
v22 = [o for o in pdat if o["year"] == 2022][0]["ratio_1995_100"]
tr = min((o for o in pdat if 1940 <= o["year"] <= 1950), key=lambda o: o["ratio_1995_100"])
g.append(f'<circle cx="{px(1995):.1f}" cy="{py(100):.1f}" r="5.5" fill="#5E7FA8" stroke="#FAF9F5" stroke-width="2"></circle>')
g.append(f'<circle cx="{px(2022):.1f}" cy="{py(v22):.1f}" r="5.5" fill="{CLAY}" stroke="#FAF9F5" stroke-width="2"></circle>')
g.append(f'<text x="{px(2010):.1f}" y="{py((v22 + 100) / 2 + 2):.1f}" text-anchor="middle" {F} font-size="22" fill="#B85C3F" font-weight="600">{v22 - 100:+.0f}%</text>')
g.append(f'<text x="{px(tr["year"]) + 10:.1f}" y="{py(tr["ratio_1995_100"]) + 6:.1f}" {F} font-size="14" fill="#7A786F" font-weight="600">{tr["ratio_1995_100"]:.0f}</text>')
g.append(f'<text x="{px(1903):.1f}" y="{py(30):.1f}" {F} font-size="14" fill="#7A786F">1914–45: two world wars</text>')
g.append(f'<text x="{px(1958):.1f}" y="{py(18):.1f}" {F} font-size="14" fill="#5E7FA8" font-weight="600">1945–95: Europe catches up</text>')
g.append(f'<text x="{px(1997):.1f}" y="{py(55):.1f}" {F} font-size="14" fill="#B85C3F" font-weight="600">Since 1995:</text>')
g.append(f'<text x="{px(1997):.1f}" y="{py(55) + 19:.1f}" {F} font-size="14" fill="#B85C3F" font-weight="600">falling behind</text>')
charts["productivity"] = (f'<svg viewBox="0 0 {PW} {PH}" width="100%" role="img" aria-label="Productivity per hour in Germany, France, Italy and Spain relative '
                          f'to the US, 1995 = 100: from {tr["ratio_1995_100"]:.0f} after the war to 100 in 1995, then down to {v22:.0f} in 2022">' + "".join(g) + "</svg>")
meta["productivity_2022"] = v22
json.dump({"charts": charts, "meta": meta}, open("site/mock_charts.json", "w"), ensure_ascii=False)
print(json.dumps(meta))
