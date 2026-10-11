"""Generate inline-SVG charts for the website mockup's front page (palette and fonts match the mockup).
Writes site/mock_charts.json: {name: svg string}. Run from research/ceps_metrics."""
import collections, datetime as dt, json, statistics
import openpyxl

INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
CLAY, CLAY2, SLATE, STONE = "#B8860B", "#E3CF9C", "#5C5858", "#C4C1BE"
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
W, H, L, R, T, B = 1000, 360, 64, 128, 20, 36
X = lambda y: L + (y - Y0) / (Y1 - Y0) * (W - L - R)


def axes(ymax, ticks, fmt=lambda v: f"{v:,.0f}"):
    Yf = lambda v: H - B - v / ymax * (H - B - T)
    g = [f'<line x1="{L}" x2="{W - R}" y1="{Yf(t):.1f}" y2="{Yf(t):.1f}" stroke="{LINE}"></line>' for t in ticks]
    g += [f'<text x="{L - 10}" y="{Yf(t) + 5:.1f}" text-anchor="end" {F} font-size="14" fill="{MUTED}">{fmt(t)}</text>' for t in ticks if t]
    g += [f'<text x="{X(y):.1f}" y="{H - 10}" text-anchor="middle" {F} font-size="14" fill="{MUTED}">{y}</text>' for y in (1990, 2000, 2010, 2020)]
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{H - B}" y2="{H - B}" stroke="{BASE}"></line>')
    return Yf, g


def resample(points, x0=None, x1=None, stepy=1.0):
    """Cumulative step series [(year, value)] -> values on a regular grid (yearly by default) (value reached by each grid date)."""
    x0 = Y0 if x0 is None else x0; x1 = Y1 - 0.3 if x1 is None else x1
    out, j, v, x = [], 0, 0, x0
    while x < x1 + 1e-9:
        while j < len(points) and points[j][0] <= x:
            v = points[j][1]; j += 1
        out.append((x, v)); x += stepy
    if out[-1][0] < x1:
        out.append((x1, points[-1][1]))
    return out


def smooth_d(pts, start="M"):
    """Monotone cubic (Fritsch-Carlson) through screen points: smooth, no overshoot, never dips."""
    n = len(pts)
    if n < 2:
        return f"{start}{pts[0][0]:.1f},{pts[0][1]:.1f}"
    dx = [pts[i + 1][0] - pts[i][0] for i in range(n - 1)]
    sl = [(pts[i + 1][1] - pts[i][1]) / dx[i] if dx[i] else 0 for i in range(n - 1)]
    m = [sl[0]] + [0 if sl[i - 1] * sl[i] <= 0 else (sl[i - 1] + sl[i]) / 2 for i in range(1, n - 1)] + [sl[-1]]
    for i in range(n - 1):
        if sl[i] == 0:
            m[i] = m[i + 1] = 0
        else:
            a_, b_ = m[i] / sl[i], m[i + 1] / sl[i]
            h = a_ * a_ + b_ * b_
            if h > 9:
                t = 3 / h ** 0.5; m[i] = t * a_ * sl[i]; m[i + 1] = t * b_ * sl[i]
    d = f"{start}{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(n - 1):
        (xa, ya), (xb, yb), h3 = pts[i], pts[i + 1], dx[i] / 3
        d += f"C{xa + h3:.1f},{ya + m[i] * h3:.1f} {xb - h3:.1f},{yb - m[i + 1] * h3:.1f} {xb:.1f},{yb:.1f}"
    return d


def band_d(top, bot, Xf, Yf):
    """Smooth filled band between two resampled series (bot None = down to zero)."""
    T = [(Xf(x), Yf(v)) for x, v in top]
    d = smooth_d(T)
    if bot is None:
        return d + f"L{T[-1][0]:.1f},{Yf(0):.1f}L{T[0][0]:.1f},{Yf(0):.1f}Z"
    B = [(Xf(x), Yf(v)) for x, v in reversed(bot)]
    return d + smooth_d(B, start="L") + "Z"


def stack_paths(series, Yf):
    """series: list of (label, color, [(year, cumvalue_total_of_this_and_below)]) bottom to top -> smooth filled bands."""
    out, prev = [], None
    for lab, col, pts in series:
        cur = resample(pts)
        out.append(f'<path d="{band_d(cur, prev, X, Yf)}" fill="{col}" stroke="#FAF9F5" stroke-width="1"></path>')
        prev = cur
    return out


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

# B. cumulative obligations: main acts vs implementing and delegated acts
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
charts["main_vs_secondary"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Cumulative obligations: {m:,} in the main acts and {s:,} in '
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
g.append(f'<text x="{(P + S) / 2:.0f}" y="{S - 8}" text-anchor="middle" {F} font-size="13" fill="{MUTED}">Obligations in the Commission proposal</text>')
g.append(f'<text x="14" y="{(S - P) / 2:.0f}" text-anchor="middle" {F} font-size="13" fill="{MUTED}" transform="rotate(-90 14 {(S - P) / 2:.0f})">Obligations in the adopted act</text>')
charts["proposal_vs_adopted"] = (f'<svg viewBox="0 0 {S} {S}" width="100%" style="max-width: 560px" role="img" aria-label="{above} of {len(cmp)} acts have more '
                                 f'obligations after adoption than in the proposal">' + "".join(g) + "</svg>")
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
charts["sox_per_act"] = (f'<svg viewBox="0 0 {BW} {10 + len(bars) * rowh + 6}" width="100%" role="img" aria-label="Obligations per act: recent EU acts '
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
charts["sox_density"] = (f'<svg viewBox="0 0 {DW} {DH}" width="100%" role="img" aria-label="Obligations per 1,000 words: median EU act {med:.1f}, '
                         f'Sarbanes-Oxley {sox["per_1000_words"]:g}">' + "".join(g) + "</svg>")
meta.update({"eu_median_density": round(med, 1), "sox": sox["restrictions_total"], "sox_density": sox["per_1000_words"]})

# E. productivity, EA-4 relative to US (1995 = 100)
pdat = json.load(open("data/external/ea4_us_productivity.json"))
def prod_svg(PW, PH, PL=50, PR=50, PT=30, PB=40):
    """Productivity chart at a given viewBox size (fonts stay in viewBox units)."""
    px = lambda y: PL + (y - 1900) / (2022 - 1900) * (PW - PL - PR)
    py = lambda v: PH - PB - v / 115 * (PH - PB - PT)
    g = [f'<rect x="{px(1945):.1f}" y="{PT}" width="{px(1995) - px(1945):.1f}" height="{PH - PB - PT}" fill="#004494" fill-opacity="0.06"></rect>',
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
    for (a, b), c in (((1900, 1945), "#9A9696"), ((1945, 1995), "#004494"), ((1995, 2022), CLAY)):
        g.append(f'<polyline points="{seg(a, b)}" fill="none" stroke="{c}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"></polyline>')
    v22 = [o for o in pdat if o["year"] == 2022][0]["ratio_1995_100"]
    tr = min((o for o in pdat if 1940 <= o["year"] <= 1950), key=lambda o: o["ratio_1995_100"])
    g.append(f'<circle cx="{px(1995):.1f}" cy="{py(100):.1f}" r="5.5" fill="#004494" stroke="#FAF9F5" stroke-width="2"></circle>')
    g.append(f'<circle cx="{px(2022):.1f}" cy="{py(v22):.1f}" r="5.5" fill="{CLAY}" stroke="#FAF9F5" stroke-width="2"></circle>')
    g.append(f'<text x="{px(2010):.1f}" y="{py((v22 + 100) / 2 + 2):.1f}" text-anchor="middle" {F} font-size="22" fill="#8F6708" font-weight="600">{v22 - 100:+.0f}%</text>')
    g.append(f'<text x="{px(tr["year"]) + 10:.1f}" y="{py(tr["ratio_1995_100"]) + 6:.1f}" {F} font-size="14" fill="#777373" font-weight="600">{tr["ratio_1995_100"]:.0f}</text>')
    g.append(f'<text x="{px(1903):.1f}" y="{py(30):.1f}" {F} font-size="14" fill="#777373">1914–45: two world wars</text>')
    g.append(f'<text x="{px(1958):.1f}" y="{py(18):.1f}" {F} font-size="14" fill="#004494" font-weight="600">1945–95: Europe catches up</text>')
    g.append(f'<text x="{px(1997):.1f}" y="{py(55):.1f}" {F} font-size="14" fill="#8F6708" font-weight="600">Since 1995:</text>')
    g.append(f'<text x="{px(1997):.1f}" y="{py(55) + 19:.1f}" {F} font-size="14" fill="#8F6708" font-weight="600">falling behind</text>')
    return (f'<svg viewBox="0 0 {PW} {PH}" width="100%" role="img" aria-label="Productivity per hour in Germany, France, Italy and Spain relative '
                              f'to the US, 1995 = 100: from {tr["ratio_1995_100"]:.0f} after the war to 100 in 1995, then down to {v22:.0f} in 2022">' + "".join(g) + "</svg>")


charts["productivity"] = prod_svg(1000, 420)
charts["productivity_tall"] = prod_svg(560, 430, PL=16, PR=36, PT=24, PB=36)
v22 = [o for o in pdat if o["year"] == 2022][0]["ratio_1995_100"]
meta["productivity_2022"] = v22
# F. obligations binding private parties: main acts + implementing/delegated acts
evp = sorted([(fy(r["d"]), r["addr_private_parties"] or 0, 0) for r in inst] + [(fy(r["d"]), 0, r["addr_private_parties"] or 0) for r in sec])
m2 = s2 = 0; qm = [(Y0, 0)]; qs = [(Y0, 0)]
for y, a, b in evp:
    m2 += a; s2 += b; qm.append((y, m2)); qs.append((y, m2 + s2))
Yf, g = axes(9000, [0, 2000, 4000, 6000, 8000])
bands = stack_paths([("main", CLAY, qm), ("sec", CLAY2, qs)], Yf)
lab = [f'<text x="{W - R + 10}" y="{Yf(m2 / 2) + 5:.1f}" {F} font-size="14" fill="{INK2}">Main acts</text>',
       f'<text x="{W - R + 10}" y="{Yf(m2 / 2) + 23:.1f}" {F} font-size="14" fill="{INK}" font-weight="600">{m2:,}</text>',
       f'<text x="{W - R + 10}" y="{Yf(m2 + s2 / 2) - 4:.1f}" {F} font-size="14" fill="{INK2}">Implementing</text>',
       f'<text x="{W - R + 10}" y="{Yf(m2 + s2 / 2) + 13:.1f}" {F} font-size="14" fill="{INK2}">&amp; delegated</text>',
       f'<text x="{W - R + 10}" y="{Yf(m2 + s2 / 2) + 31:.1f}" {F} font-size="14" fill="{INK}" font-weight="600">{s2:,}</text>']
charts["private"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Cumulative obligations binding private parties: {m2:,} in the main '
                     f'acts and {s2:,} in implementing and delegated acts">' + "".join(g + bands + lab) + "</svg>")
meta.update({"private_main": m2, "private_secondary": s2})

# G. combined: cumulative acts by legal type (top) + new acts per year by policy group (bottom), shared x axis
GROUPS = [("Data, privacy & cybersecurity", ["Data & Privacy", "Cybersecurity"], "#B8860B"),
          ("Platforms, content & media", ["Trust & Safety", "Media"], "#004494"),
          ("Markets, consumers & IP", ["Competition & Single Market", "E-commerce & Consumer Protection", "IPR"], "#D9BE7A"),
          ("Finance", ["Finance"], "#5C5858"),
          ("Industry, research & connectivity", ["Industrial Policy", "Research & Innovation", "Connectivity"], "#7FA3CC"),
          ("Law enforcement", ["Law Enforcement"], "#C4C1BE")]
gof = {a: gi for gi, (_, areas, _) in enumerate(GROUPS) for a in areas}
TOPH = H
BOT0, BOTH = TOPH + 64, 200            # bottom panel origin and height
Yf, g = axes(120, [0, 20, 40, 60, 80, 100, 120])
g = [x for x in g if 'y="' + str(H - 10) + '"' not in x]          # drop top x labels (shared axis below)
# Commission terms: dashed rules with names in two staggered rows
TERMS = [("Santer", dt.date(1995, 1, 23)), ("Prodi", dt.date(1999, 9, 16)), ("Barroso", dt.date(2004, 11, 22)), ("Barroso II", dt.date(2010, 2, 10)),
         ("Juncker", dt.date(2014, 11, 1)), ("von der Leyen I", dt.date(2019, 12, 1)), ("von der Leyen II", dt.date(2024, 12, 1))]
for i, (nm, d) in enumerate(TERMS):
    x = X(fy(d)); ly_ = T + 14 + (i % 2) * 16
    g.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{ly_ + 4}" y2="{BOT0 + BOTH}" stroke="#B5B1AC" stroke-dasharray="2 4"></line>')
    g.append(f'<text x="{x + 4:.1f}" y="{ly_:.1f}" {F} font-size="11.5" letter-spacing="0.02em" fill="{MUTED}">{nm}</text>')
# light stacked fills, solid outlines on the regulation boundary and the total
rs = [resample(pts[t]) for t in order]
FILL = {"Regulation": (CLAY, 0.30), "Directive": (SLATE, 0.16), "Decision": (SLATE, 0.08)}
prev = None
top = []
for t, cur in zip(order, rs):
    c, o = FILL[t]
    top.append(f'<path d="{band_d(cur, prev, X, Yf)}" fill="{c}" fill-opacity="{o}"></path>')
    prev = cur
top.append(f'<path d="{smooth_d([(X(x), Yf(v)) for x, v in rs[0]])}" fill="none" stroke="{CLAY}" stroke-width="2"></path>')
top.append(f'<path d="{smooth_d([(X(x), Yf(v)) for x, v in rs[-1]])}" fill="none" stroke="{INK}" stroke-width="2.2"></path>')
ex, ey = X(rs[-1][-1][0]), Yf(rs[-1][-1][1])
top.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="5" fill="{INK}" stroke="#FAF9F5" stroke-width="2"></circle>')
labt = [f'<text x="{W - R + 12}" y="{ey + 6:.1f}" {F} font-size="20" fill="{INK}" font-weight="600">{tot}</text>',
        f'<text x="{W - R + 12}" y="{ey + 24:.1f}" {F} font-size="13" fill="{MUTED}">adopted acts</text>',
        f'<text x="{W - R + 12}" y="{Yf(cum["Regulation"] / 2) + 5:.1f}" {F} font-size="14" fill="{CLAY}" font-weight="600">Regulations {cum["Regulation"]}</text>',
        f'<text x="{W - R + 12}" y="{Yf(cum["Regulation"] + cum["Directive"] / 2) - 2:.1f}" {F} font-size="14" fill="{INK2}">Directives {cum["Directive"]}</text>',
        f'<text x="{W - R + 12}" y="{Yf(cum["Regulation"] + cum["Directive"] / 2) + 15:.1f}" {F} font-size="12.5" fill="{MUTED}">+ {cum["Decision"]} decisions</text>']
peryear = {}
for r in inst:
    peryear.setdefault(r["d"].year, [0] * len(GROUPS))[gof[r["policy_area_ceps"]]] += 1
ymax = max(sum(v) for v in peryear.values())
ymaxr = 20 if ymax <= 20 else 25
by = lambda v: BOT0 + BOTH - v / ymaxr * BOTH
b = []
for t in (5, 10, 15, 20) if ymaxr == 20 else (5, 10, 15, 20, 25):
    b.append(f'<line x1="{L}" x2="{W - R}" y1="{by(t):.1f}" y2="{by(t):.1f}" stroke="{LINE}"></line>')
    b.append(f'<text x="{L - 10}" y="{by(t) + 5:.1f}" text-anchor="end" {F} font-size="14" fill="{MUTED}">{t}</text>')
bw = (W - L - R) / (Y1 - Y0) * 0.72
for yr, v in sorted(peryear.items()):
    x0 = X(yr + 0.5) - bw / 2; acc = 0
    for gi, n in enumerate(v):
        if not n:
            continue
        y_top = by(acc + n); hgt = by(acc) - by(acc + n)
        b.append(f'<rect x="{x0:.1f}" y="{y_top:.1f}" width="{bw:.1f}" height="{max(hgt - 1, 1):.1f}" fill="{GROUPS[gi][2]}" fill-opacity="0.85"></rect>')
        acc += n
b.append(f'<line x1="{L}" x2="{W - R}" y1="{BOT0 + BOTH}" y2="{BOT0 + BOTH}" stroke="{BASE}"></line>')
b += [f'<text x="{X(y):.1f}" y="{BOT0 + BOTH + 24}" text-anchor="middle" {F} font-size="13.5" fill="{MUTED}">{y}</text>' for y in range(1990, 2026, 5)]
b.append(f'<text x="{L}" y="{BOT0 - 24}" {F} font-size="15" fill="{INK}"><tspan font-weight="600">New acts adopted each year, by policy area.</tspan>'
         f'<tspan fill="{INK2}"> Adoptions bunch before each European election; none on the list was adopted in 2020.</tspan></text>')

ly = BOT0 + BOTH + 52
COLW = [0, 260, 500, 730]            # legend columns: row 2 sits under row 1
for i, (name, _, col) in enumerate(GROUPS):
    lx, yy = L + COLW[i % 4], ly + (i // 4) * 24
    b.append(f'<rect x="{lx}" y="{yy - 10}" width="12" height="12" rx="2" fill="{col}"></rect><text x="{lx + 18}" y="{yy}" {F} font-size="13.5" fill="{INK2}">{name}</text>')
ly += 24 * ((len(GROUPS) - 1) // 4)
since = [sum(v) for yr, v in peryear.items() if yr >= 2020]
charts["acts_combined"] = (f'<svg viewBox="0 0 {W} {ly + 16}" width="100%" role="img" aria-label="Top: cumulative adopted acts by legal type '
                           f'({cum["Regulation"]} regulations, {cum["Directive"]} directives, {cum["Decision"]} decisions). Bottom: new acts each year by policy area; '
                           f'{sum(since)} adopted since 2020">' + "".join(g + top + labt + b) + "</svg>")
meta["groups_since_2020"] = {name: sum(v[gi] for yr, v in peryear.items() if yr >= 2020) for gi, (name, _, _) in enumerate(GROUPS)}

# H. small multiples: cumulative obligations by CEPS policy area, main acts vs their implementing and delegated acts
area_of = {r["row_id"]: r["policy_area_ceps"] for r in sheet("instruments")}
secs_by_area = collections.defaultdict(list)
for r in sec:
    secs_by_area[area_of.get(r["parent_row_id"])].append(r)
tot_area = lambda a: sum(r["restrictions_total"] for r in inst if r["policy_area_ceps"] == a) + sum(r["restrictions_total"] for r in secs_by_area[a])
areas = sorted({r["policy_area_ceps"] for r in inst}, key=lambda a: -tot_area(a))
SW, NC, PW_, PH_, GX, GY, TOP0 = 1000, 4, 222, 150, 30, 62, 36
SH = TOP0 + 3 * (PH_ + GY) + 10
YM = 1000 * (max(tot_area(a) for a in areas) // 1000 + 1)
g = [f'<rect x="28" y="4" width="12" height="12" rx="2" fill="{CLAY}"></rect><text x="46" y="15" {F} font-size="13.5" fill="{INK2}">Main acts</text>',
     f'<rect x="148" y="4" width="12" height="12" rx="2" fill="{CLAY2}"></rect><text x="166" y="15" {F} font-size="13.5" fill="{INK2}">Implementing and delegated acts</text>']
xpx = lambda x0, y: x0 + (y - Y0) / (Y1 - Y0) * PW_
pa_tot = {}
for i, a in enumerate(areas):
    x0 = 28 + (i % NC) * (PW_ + GX); y0 = TOP0 + 28 + (i // NC) * (PH_ + GY)
    yv = lambda v: y0 + PH_ - v / YM * PH_
    ev_a = sorted([(fy(r["d"]), r["restrictions_total"], 0) for r in inst if r["policy_area_ceps"] == a] +
                  [(fy(r["d"]), 0, r["restrictions_total"]) for r in secs_by_area[a]])
    p = o = 0; pp, po = [(Y0, 0)], [(Y0, 0)]
    for y_, mv, sv in ev_a:
        p += mv; o += sv
        pp.append((y_, p)); po.append((y_, p + o))
    pa_tot[a] = p + o
    rp, ro = resample(pp, stepy=2.0), resample(po, stepy=2.0)
    xf = lambda y, x0=x0: xpx(x0, y)
    for t in [k * (2000 if YM > 6000 else 1000) for k in range(1, 10) if k * (2000 if YM > 6000 else 1000) < YM]:
        g.append(f'<line x1="{x0}" x2="{x0 + PW_}" y1="{yv(t):.1f}" y2="{yv(t):.1f}" stroke="{LINE}"></line>')
        if i % NC == 0:
            g.append(f'<text x="{x0 - 6}" y="{yv(t) + 4:.1f}" text-anchor="end" {F} font-size="12" fill="{MUTED}">{t // 1000}k</text>')
    g.append(f'<path d="{band_d(ro, rp, xf, yv)}" fill="{CLAY2}"></path><path d="{band_d(rp, None, xf, yv)}" fill="{CLAY}"></path>')
    g.append(f'<line x1="{x0}" x2="{x0 + PW_}" y1="{y0 + PH_}" y2="{y0 + PH_}" stroke="{BASE}"></line>')
    for y in (1990, 2010):
        g.append(f'<text x="{xpx(x0, y):.1f}" y="{y0 + PH_ + 16}" text-anchor="middle" {F} font-size="12" fill="{MUTED}">{y}</text>')
    g.append(f'<text x="{x0}" y="{y0 - 10}" {F} font-size="14" fill="{INK}" font-weight="600">{a.replace(" Protection", "").replace("&", "&amp;")} <tspan font-weight="400" fill="{MUTED}">{p + o:,}</tspan></text>')
charts["policy_areas"] = (f'<svg viewBox="0 0 {SW} {SH}" width="100%" role="img" aria-label="Cumulative obligations by CEPS policy area, twelve panels on shared axes, '
                          f'split into obligations in the main acts and in their implementing and delegated acts">' + "".join(g) + "</svg>")
meta["policy_area_totals"] = pa_tot

# I. obligations per act and per 1,000 words over time, with 5-year averages and the Sarbanes-Oxley line
TC = {"Regulation": CLAY, "Directive": SLATE, "Decision": STONE}
VW, VH, PL, PR_, PT, PB, PGAP = 1000, 400, 52, 16, 40, 36, 60
pw = (VW - 2 * PL - PR_ - PGAP) / 2
dens = lambda r: 1000 * r["restrictions_total"] / max(1, (r["words_articles"] or 0) + (r["words_annexes"] or 0))
g = []
for k, (title, f, ym, ticks, sv) in enumerate((("Obligations per act", lambda r: r["restrictions_total"], 1200, (400, 800, 1200), sox["restrictions_total"]),
                                               ("Obligations per 1,000 words", dens, 40, (10, 20, 30, 40), sox["per_1000_words"]))):
    x0 = PL + k * (pw + PL + PGAP)
    xx = lambda y: x0 + (y - Y0) / (Y1 - Y0) * pw
    yy = lambda v: PT + (VH - PT - PB) * (1 - min(v, ym) / ym)
    g.append(f'<text x="{x0}" y="18" {F} font-size="15" fill="{INK}" font-weight="600">{title}</text>')
    for t in ticks:
        g.append(f'<line x1="{x0}" x2="{x0 + pw:.1f}" y1="{yy(t):.1f}" y2="{yy(t):.1f}" stroke="{LINE}"></line>'
                 f'<text x="{x0 - 8}" y="{yy(t) + 5:.1f}" text-anchor="end" {F} font-size="13" fill="{MUTED}">{t:,}</text>')
    g.append(f'<line x1="{x0}" x2="{x0 + pw:.1f}" y1="{VH - PB}" y2="{VH - PB}" stroke="{BASE}"></line>')
    g += [f'<text x="{xx(y):.1f}" y="{VH - 12}" text-anchor="middle" {F} font-size="13" fill="{MUTED}">{y}</text>' for y in (1990, 2000, 2010, 2020)]
    g.append(f'<line x1="{x0}" x2="{x0 + pw:.1f}" y1="{yy(sv):.1f}" y2="{yy(sv):.1f}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="5 4"></line>'
             f'<text x="{x0 + 4}" y="{yy(sv) - 6:.1f}" {F} font-size="12.5" fill="{INK}">Sarbanes-Oxley Act {sv:g}</text>')
    for r in sorted(inst, key=lambda r: r["type"] != "Regulation"):
        g.append(f'<circle cx="{xx(fy(r["d"])):.1f}" cy="{yy(f(r)):.1f}" r="4.5" fill="{TC[r["type"]]}" fill-opacity="0.85" stroke="#FAF9F5" stroke-width="1"></circle>')
    bins = {}
    for r in inst: bins.setdefault(r["d"].year // 5 * 5, []).append(r)
    line = [(statistics.median(fy(r["d"]) for r in bins[b]), statistics.mean(f(r) for r in bins[b])) for b in sorted(bins) if len(bins[b]) >= 3]
    g.append(f'<polyline points="{" ".join(f"{xx(a):.1f},{yy(v):.1f}" for a, v in line)}" fill="none" stroke="{INK}" stroke-width="2.5"></polyline>')
    meta[f"avg5_{k}"] = [(round(a, 1), round(v, 1)) for a, v in line]
lx = PL
for t in ("Regulation", "Directive", "Decision"):
    g.append(f'<circle cx="{lx + 6}" cy="{VH + 14}" r="5" fill="{TC[t]}"></circle><text x="{lx + 16}" y="{VH + 19}" {F} font-size="13.5" fill="{INK2}">{t}s</text>'); lx += 120
g.append(f'<line x1="{lx}" x2="{lx + 22}" y1="{VH + 14}" y2="{VH + 14}" stroke="{INK}" stroke-width="2.5"></line><text x="{lx + 30}" y="{VH + 19}" {F} font-size="13.5" fill="{INK2}">5-year average</text>')
charts["per_act_density"] = (f'<svg viewBox="0 0 {VW} {VH + 30}" width="100%" role="img" aria-label="Left: obligations per act over time, rising. Right: obligations per 1,000 words, roughly flat. '
                             f'Dots are acts; lines are 5-year averages; dashed line is the Sarbanes-Oxley Act">' + "".join(g) + "</svg>")

# J. compact cumulative charts (half page width, or tall for a side column): same style as the restyled rulebook chart
TERMS_SHORT = [("Santer", dt.date(1995, 1, 23)), ("Prodi", dt.date(1999, 9, 16)), ("Barroso", dt.date(2004, 11, 22)),
               ("Barroso II", dt.date(2010, 2, 10)), ("Juncker", dt.date(2014, 11, 1)), ("vdL I", dt.date(2019, 12, 1)), ("vdL II", dt.date(2024, 12, 1))]


def compact(layers, ymax, ticks, labels, aria, W_=560, H_=420, L_=48, R_=150, T_=44, B_=34, fmt=lambda v: f"{v:,.0f}", terms=True, years=(1990, 2000, 2010, 2020)):
    """layers: [(color, opacity, cumulative points stacked bottom->top, outline color or None)]; labels: [(text, value_y, color, weight, size)]."""
    Xc = lambda y: L_ + (y - Y0) / (Y1 - Y0) * (W_ - L_ - R_)
    Yc = lambda v: H_ - B_ - v / ymax * (H_ - B_ - T_)
    g = []
    for t in ticks:
        g.append(f'<line x1="{L_}" x2="{W_ - R_}" y1="{Yc(t):.1f}" y2="{Yc(t):.1f}" stroke="{LINE}"></line>')
        if t:
            g.append(f'<text x="{L_ - 8}" y="{Yc(t) + 5:.1f}" text-anchor="end" {F} font-size="14" fill="{MUTED}">{fmt(t)}</text>')
    g += [f'<text x="{Xc(y):.1f}" y="{H_ - 10}" text-anchor="middle" {F} font-size="14" fill="{MUTED}">{y}</text>' for y in years]
    g.append(f'<line x1="{L_}" x2="{W_ - R_}" y1="{H_ - B_}" y2="{H_ - B_}" stroke="{BASE}"></line>')
    if terms:
        for i, (nm, d) in enumerate(TERMS_SHORT):
            x = Xc(fy(d)); ly_ = 14 + (i % 2) * 15
            g.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{ly_ + 4}" y2="{H_ - B_}" stroke="#B5B1AC" stroke-dasharray="2 4"></line>')
            g.append(f'<text x="{x + 3:.1f}" y="{ly_}" {F} font-size="11.5" fill="{MUTED}">{nm}</text>')
    prev = None
    for col, op, pts_, line in layers:
        cur = resample(pts_)
        g.append(f'<path d="{band_d(cur, prev, Xc, Yc)}" fill="{col}" fill-opacity="{op}"></path>')
        if line:
            g.append(f'<path d="{smooth_d([(Xc(x), Yc(v)) for x, v in cur])}" fill="none" stroke="{line}" stroke-width="2"></path>')
        prev = cur
    ex, ey = Xc(prev[-1][0]), Yc(prev[-1][1])
    g.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" fill="{INK}" stroke="#FAF9F5" stroke-width="2"></circle>')
    for text, vy, col, wt, sz in labels:
        g.append(f'<text x="{W_ - R_ + 10}" y="{Yc(vy) + 5:.1f}" {F} font-size="{sz}" fill="{col}" font-weight="{wt}">{text}</text>')
    return f'<svg viewBox="0 0 {W_} {H_}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"


def by_type(weight):
    c = {t: 0 for t in order}; pts_ = {t: [(Y0, 0)] for t in order}
    for r in sorted(inst, key=lambda r: r["d"]):
        c[r["type"]] += weight(r); run = 0
        for t in order:
            run += c[t]; pts_[t].append((fy(r["d"]), run))
    return c, pts_


FILLS = {"Regulation": (CLAY, 0.30, CLAY), "Directive": (SLATE, 0.16, None), "Decision": (SLATE, 0.08, INK)}
for key, wfun, ymax, ticks, unit in (("acts_by_type_half", lambda r: 1, 120, [0, 20, 40, 60, 80, 100, 120], "adopted acts"),
                                     ("restr_by_type_half", lambda r: r["restrictions_total"], 24000, [0, 4000, 8000, 12000, 16000, 20000, 24000], "obligations")):
    cc, pp_ = by_type(wfun)
    tot_ = sum(cc.values())
    layers = [(FILLS[t][0], FILLS[t][1], pp_[t], FILLS[t][2]) for t in order]
    reg, dirc = cc["Regulation"], cc["Directive"]
    dy = min(reg + dirc / 2, tot_ - ymax * 0.17)
    labs = [(f"{tot_:,}", tot_ + ymax * 0.02, INK, 600, 19), (unit, tot_ - ymax * 0.055, MUTED, 400, 12.5),
            ("Regulations", reg / 2 + ymax * 0.03, CLAY, 600, 13.5), (f"{reg:,}", reg / 2 - ymax * 0.03, CLAY, 600, 13.5),
            (f"Directives {dirc:,}", dy, INK2, 400, 13.5), (f"+ {cc['Decision']:,} in decisions", dy - ymax * 0.055, MUTED, 400, 12)]
    fmt = (lambda v: f"{v / 1000:.0f}k") if ymax > 1000 else (lambda v: f"{v:,.0f}")
    charts[key] = compact(layers, ymax, ticks, labs, f"Cumulative {unit} in adopted EU digital acts by legal type: {reg:,} in regulations, {dirc:,} in directives, "
                          f"{cc['Decision']:,} in decisions; dashed lines mark new Commissions", fmt=fmt)
    meta[key] = cc

# private parties, tall version for the side column of the rulebook page
labs = [(f"{m2 + s2:,}", m2 + s2 + 300, INK, 600, 19), ("in total", m2 + s2 - 500, MUTED, 400, 12.5),
        ("Main acts", m2 / 2 + 250, CLAY, 600, 13.5), (f"{m2:,}", m2 / 2 - 450, INK, 600, 13.5),
        ("Implementing", m2 + s2 / 2 + 300, INK2, 400, 13.5), ("& delegated", m2 + s2 / 2 - 250, INK2, 400, 13.5), (f"{s2:,}", m2 + s2 / 2 - 900, INK, 600, 13.5)]
charts["private_tall"] = compact([(CLAY, 0.85, qm, None), (CLAY2, 0.9, qs, INK)], 14000, [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000], labs,
                                 f"Cumulative obligations binding private parties: {m2:,} in the main acts and {s2:,} in implementing and delegated acts",
                                 W_=560, H_=600, fmt=lambda v: f"{v / 1000:.0f}k")

# private parties, half-width version for the front page (same size as acts_by_type_half)
ym = 14000
labs = [(f"{m2 + s2:,}", m2 + s2 + ym * 0.02, INK, 600, 19), ("obligations", m2 + s2 - ym * 0.055, MUTED, 400, 12.5),
        ("Main acts", m2 / 2 + ym * 0.03, CLAY, 600, 13.5), (f"{m2:,}", m2 / 2 - ym * 0.03, CLAY, 600, 13.5),
        ("Implementing", m2 + s2 / 2 + ym * 0.06, INK2, 400, 13.5), ("&amp; delegated", m2 + s2 / 2 + ym * 0.005, INK2, 400, 13.5),
        (f"{s2:,}", m2 + s2 / 2 - ym * 0.05, INK, 600, 13.5)]
charts["private_half"] = compact([(CLAY, 0.30, qm, CLAY), (SLATE, 0.16, qs, None)], ym, [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000], labs,
                                 f"Cumulative obligations binding private parties: {m2:,} in the main acts and {s2:,} in implementing and delegated acts; dashed lines mark new Commissions",
                                 fmt=lambda v: f"{v / 1000:.0f}k")

# acts per CEPS policy area, half-width bar chart for the front page: adopted acts, split before / since 2020
pa = collections.defaultdict(lambda: [0, 0])
for r in inst:
    pa[r["policy_area_ceps"]][r["d"].year >= 2020] += 1
pa_rows = sorted(pa.items(), key=lambda kv: (-sum(kv[1]), kv[0]))
PW, PH, PL, PT = 560, 420, 238, 40
prow = (PH - PT - 8) / len(pa_rows)
pmax = max(sum(v) for _, v in pa_rows)
px = lambda v: v / pmax * (PW - PL - 44)
g = [f'<rect x="{PL}" y="8" width="12" height="12" rx="2" fill="{CLAY}"></rect><text x="{PL + 18}" y="18.5" {F} font-size="12.5" fill="{INK2}">2020 or later</text>',
     f'<rect x="{PL + 118}" y="8" width="12" height="12" rx="2" fill="{CLAY2}"></rect><text x="{PL + 136}" y="18.5" {F} font-size="12.5" fill="{INK2}">Before 2020</text>']
for i, (a, (old, new)) in enumerate(pa_rows):
    y = PT + i * prow
    g.append(f'<text x="{PL - 12}" y="{y + prow / 2 + 4.5:.1f}" text-anchor="end" {F} font-size="13" fill="{INK2}">{a.replace("&", "&amp;")}</text>')
    if new:
        g.append(f'<rect x="{PL}" y="{y + 5:.1f}" width="{px(new):.1f}" height="{prow - 10:.1f}" fill="{CLAY}"></rect>')
    if old:
        g.append(f'<rect x="{PL + px(new):.1f}" y="{y + 5:.1f}" width="{px(old):.1f}" height="{prow - 10:.1f}" fill="{CLAY2}"></rect>')
    g.append(f'<text x="{PL + px(old + new) + 8:.1f}" y="{y + prow / 2 + 4.5:.1f}" {F} font-size="13.5" fill="{INK}" font-weight="600">{old + new}</text>')
charts["acts_by_area_half"] = (f'<svg viewBox="0 0 {PW} {PH}" width="100%" role="img" aria-label="Adopted EU digital acts by CEPS policy area, split into acts adopted before 2020 and from 2020: '
                               + "; ".join(f"{a} {o + n} ({n} since 2020)" for a, (o, n) in pa_rows).replace("&", "&amp;") + '">' + "".join(g) + "</svg>")
meta["acts_by_area"] = {a: v for a, v in pa_rows}

# instrument page: where one act sits among all adopted acts by number of obligations (dot strip, beeswarm)
def rank_strip(celex, refs=("General Data Protection Regulation", "Artificial Intelligence Act", "Markets in Crypto-Assets Regulation")):
    vals = sorted(((r["restrictions_total"], r) for r in inst), key=lambda t: t[0])
    me = next(r for v, r in vals if r["celex_measured"] == celex)
    W_, L_, R_, rad = 1000, 24, 24, 5.5
    vmax = 1200
    X = lambda v: L_ + v / vmax * (W_ - L_ - R_)
    placed = []  # (x, dy)
    for v, r in vals:
        x = X(v); dy = 0; k = 0
        while any(abs(x - px_) < 2 * rad + 1 and abs(dy - pdy) < 2 * rad + 1 for px_, pdy in placed):
            k += 1; dy = (k + 1) // 2 * (2 * rad + 1) * (1 if k % 2 else -1)
        placed.append((x, dy)); r["_dy"] = dy
    span = max(abs(d) for _, d in placed)
    BASE_ = 70 + span
    H_ = BASE_ + span + 64
    med = statistics.median(v for v, _ in vals)
    below = sum(v < me["restrictions_total"] for v, _ in vals)
    g = [f'<line x1="{L_}" x2="{W_ - R_}" y1="{BASE_}" y2="{BASE_}" stroke="{BASE}" stroke-width="1"></line>']
    for t in range(0, vmax + 1, 200):
        g.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{BASE_ + span + 14}" y2="{BASE_ + span + 20}" stroke="{BASE}"></line>')
        g.append(f'<text x="{X(t):.1f}" y="{BASE_ + span + 38}" text-anchor="middle" {F} font-size="13" fill="{MUTED}">{t:,}</text>')
    g.append(f'<line x1="{X(med):.1f}" x2="{X(med):.1f}" y1="{BASE_ - span - 16}" y2="{BASE_ + span + 10}" stroke="{INK2}" stroke-dasharray="3 3"></line>')
    g.append(f'<text x="{X(med) + 6:.1f}" y="{BASE_ - span - 6}" {F} font-size="12.5" fill="{INK2}">median {med:,.0f}</text>')
    for v, r in vals:
        if r is me: continue
        g.append(f'<circle cx="{X(v):.1f}" cy="{BASE_ + r["_dy"]:.1f}" r="{rad}" fill="{STONE}" fill-opacity="0.85"><title>{r["name"].replace("&", "&amp;")}: {v:,}</title></circle>')
    for n in refs:
        r = next((r for r in inst if r["name"] == n), None)
        if r is None or r is me: continue
        lbl = n.replace("General Data Protection Regulation", "GDPR").replace("Artificial Intelligence Act", "AI Act").replace("Markets in Crypto-Assets Regulation", "MiCA")
        g.append(f'<text x="{X(r["restrictions_total"]):.1f}" y="{BASE_ + r["_dy"] - 12:.1f}" text-anchor="middle" {F} font-size="12.5" fill="{MUTED}">{lbl}</text>')
    mx_, my_ = X(me["restrictions_total"]), BASE_ + me["_dy"]
    g.append(f'<circle cx="{mx_:.1f}" cy="{my_:.1f}" r="{rad + 2.5}" fill="{CLAY}" stroke="#FAF9F5" stroke-width="2"></circle>')
    g.append(f'<line x1="{mx_:.1f}" x2="{mx_:.1f}" y1="{my_ - rad - 4:.1f}" y2="26" stroke="{CLAY}"></line>')
    g.append(f'<text x="{mx_:.1f}" y="18" text-anchor="middle" {F} font-size="14" fill="{INK}" font-weight="600">{me["name"].split(" (")[0]}: {me["restrictions_total"]:,}</text>')
    aria = (f'{me["name"]} has {me["restrictions_total"]:,} obligations, more than {below} of the {len(vals)} adopted EU digital acts; median {med:,.0f}. '
            f'Each dot is one act on a scale from 0 to {vmax:,} obligations')
    return f'<svg viewBox="0 0 {W_} {H_:.0f}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>", below, len(vals), med


charts["rank_dma"], b_, n_, m_ = rank_strip("32022R1925")
meta["rank_dma"] = {"below": b_, "n": n_, "median": m_}

json.dump({"charts": charts, "meta": meta}, open("site/mock_charts.json", "w"), ensure_ascii=False)
print(json.dumps(meta))
