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
W, H, L, R, T, B = 1000, 360, 64, 128, 20, 36
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
# F. restrictions binding private parties: main acts + implementing/delegated acts
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
charts["private"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Cumulative restrictions binding private parties: {m2:,} in the main '
                     f'acts and {s2:,} in implementing and delegated acts">' + "".join(g + bands + lab) + "</svg>")
meta.update({"private_main": m2, "private_secondary": s2})

# G. combined: cumulative acts by legal type (top) + new acts per year by policy group (bottom), shared x axis
GROUPS = [("Data, privacy & cybersecurity", ["Data & Privacy", "Cybersecurity"], "#D97757"),
          ("Platforms, content & media", ["Trust & Safety", "Media"], "#5E7FA8"),
          ("Markets, consumers & IP", ["Competition & Single Market", "E-commerce & Consumer Protection", "IPR"], "#D4A85A"),
          ("Finance", ["Finance"], "#5E5D59"),
          ("Industry, research & connectivity", ["Industrial Policy", "Research & Innovation", "Connectivity"], "#7D9B76"),
          ("Law enforcement", ["Law Enforcement"], "#BDBAAE")]
gof = {a: gi for gi, (_, areas, _) in enumerate(GROUPS) for a in areas}
TOPH = H
BOT0, BOTH = TOPH + 40, 200            # bottom panel origin and height
HH = BOT0 + BOTH + 40 + 70             # + axis + legend
Yf, g = axes(120, [0, 20, 40, 60, 80, 100, 120])
g = [x for x in g if 'y="' + str(H - 10) + '"' not in x]          # drop top x labels (shared axis below)
top = stack_paths([(t, cols[t], pts[t]) for t in order], Yf)
labt = []
run = 0
for t in order:
    mid = run + cum[t] / 2; run += cum[t]
    labt.append(f'<text x="{W - R + 10}" y="{Yf(mid) + 5:.1f}" {F} font-size="14" fill="{INK2}">{t}s {cum[t]}</text>')
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
        b.append(f'<rect x="{x0:.1f}" y="{y_top:.1f}" width="{bw:.1f}" height="{max(hgt - 1, 1):.1f}" fill="{GROUPS[gi][2]}"></rect>')
        acc += n
b.append(f'<line x1="{L}" x2="{W - R}" y1="{BOT0 + BOTH}" y2="{BOT0 + BOTH}" stroke="{BASE}"></line>')
b += [f'<text x="{X(y):.1f}" y="{BOT0 + BOTH + 24}" text-anchor="middle" {F} font-size="14" fill="{MUTED}">{y}</text>' for y in (1990, 2000, 2010, 2020)]
b.append(f'<text x="{L}" y="{BOT0 - 14}" {F} font-size="14" fill="{INK2}" font-weight="600">New acts adopted each year, by policy area</text>')
b.append(f'<text x="{L}" y="{T - 2 + 10}" {F} font-size="14" fill="{INK2}" font-weight="600">Adopted acts in force, cumulative, by type</text>')
lx, ly = L, BOT0 + BOTH + 52
for name, _, col in GROUPS:
    wtxt = 7.6 * len(name) + 34
    if lx + wtxt > W - 10:
        lx, ly = L, ly + 24
    b.append(f'<rect x="{lx}" y="{ly - 10}" width="12" height="12" rx="2" fill="{col}"></rect><text x="{lx + 18}" y="{ly}" {F} font-size="13.5" fill="{INK2}">{name}</text>')
    lx += wtxt
since = [sum(v) for yr, v in peryear.items() if yr >= 2020]
charts["acts_combined"] = (f'<svg viewBox="0 0 {W} {ly + 16}" width="100%" role="img" aria-label="Top: cumulative adopted acts by legal type '
                           f'({cum["Regulation"]} regulations, {cum["Directive"]} directives, {cum["Decision"]} decisions). Bottom: new acts each year by policy area; '
                           f'{sum(since)} adopted since 2020">' + "".join(g + top + labt + b) + "</svg>")
meta["groups_since_2020"] = {name: sum(v[gi] for yr, v in peryear.items() if yr >= 2020) for gi, (name, _, _) in enumerate(GROUPS)}

# H. small multiples: cumulative restrictions by CEPS policy area (private parties vs others)
areas = sorted({r["policy_area_ceps"] for r in inst}, key=lambda a: -sum(r["restrictions_total"] for r in inst if r["policy_area_ceps"] == a))
SW, NC, PW_, PH_, GX, GY, TOP0 = 1000, 4, 222, 150, 30, 62, 36
SH = TOP0 + 3 * (PH_ + GY) + 10
YM = 4500
g = [f'<rect x="28" y="4" width="12" height="12" rx="2" fill="{CLAY}"></rect><text x="46" y="15" {F} font-size="13.5" fill="{INK2}">Binding private parties</text>',
     f'<rect x="228" y="4" width="12" height="12" rx="2" fill="{STONE}"></rect><text x="246" y="15" {F} font-size="13.5" fill="{INK2}">Other addressees</text>']
xpx = lambda x0, y: x0 + (y - Y0) / (Y1 - Y0) * PW_
pa_tot = {}
for i, a in enumerate(areas):
    x0 = 28 + (i % NC) * (PW_ + GX); y0 = TOP0 + 28 + (i // NC) * (PH_ + GY)
    yv = lambda v: y0 + PH_ - v / YM * PH_
    rs = sorted([r for r in inst if r["policy_area_ceps"] == a], key=lambda r: r["d"])
    p = o = 0; pp, po = [(Y0, 0)], [(Y0, 0)]
    for r in rs:
        pv = r["addr_private_parties"] or 0
        p += pv; o += r["restrictions_total"] - pv
        pp.append((fy(r["d"]), p)); po.append((fy(r["d"]), p + o))
    pa_tot[a] = p + o
    def band(top, bot):
        d = f"M{x0},{yv(top[0][1]):.1f}"
        for y, v in top: d += f"H{xpx(x0, y):.1f}V{yv(v):.1f}"
        d += f"H{x0 + PW_}"
        if bot is None: return d + f"V{yv(0):.1f}H{x0}Z"
        d += f"V{yv(bot[-1][1]):.1f}"
        for j in range(len(bot) - 1, -1, -1):
            d += f"H{xpx(x0, bot[j][0]):.1f}V{yv(bot[j - 1][1] if j else 0):.1f}"
        return d + f"H{x0}Z"
    for t in (2000, 4000):
        g.append(f'<line x1="{x0}" x2="{x0 + PW_}" y1="{yv(t):.1f}" y2="{yv(t):.1f}" stroke="{LINE}"></line>')
        if i % NC == 0:
            g.append(f'<text x="{x0 - 6}" y="{yv(t) + 4:.1f}" text-anchor="end" {F} font-size="12" fill="{MUTED}">{t // 1000}k</text>')
    g.append(f'<path d="{band(po, pp)}" fill="{STONE}"></path><path d="{band(pp, None)}" fill="{CLAY}"></path>')
    g.append(f'<line x1="{x0}" x2="{x0 + PW_}" y1="{y0 + PH_}" y2="{y0 + PH_}" stroke="{BASE}"></line>')
    for y in (1990, 2010):
        g.append(f'<text x="{xpx(x0, y):.1f}" y="{y0 + PH_ + 16}" text-anchor="middle" {F} font-size="12" fill="{MUTED}">{y}</text>')
    g.append(f'<text x="{x0}" y="{y0 - 10}" {F} font-size="14" fill="{INK}" font-weight="600">{a.replace(" Protection", "").replace("&", "&amp;")} <tspan font-weight="400" fill="{MUTED}">{p + o:,}</tspan></text>')
charts["policy_areas"] = (f'<svg viewBox="0 0 {SW} {SH}" width="100%" role="img" aria-label="Cumulative restrictions by CEPS policy area, twelve panels on shared axes, '
                          f'split into restrictions binding private parties and other addressees">' + "".join(g) + "</svg>")
meta["policy_area_totals"] = pa_tot

# I. restrictions per act and per 1,000 words over time, with 5-year averages and the Sarbanes-Oxley line
TC = {"Regulation": CLAY, "Directive": SLATE, "Decision": STONE}
VW, VH, PL, PR_, PT, PB, PGAP = 1000, 400, 52, 16, 40, 36, 60
pw = (VW - 2 * PL - PR_ - PGAP) / 2
dens = lambda r: 1000 * r["restrictions_total"] / max(1, (r["words_articles"] or 0) + (r["words_annexes"] or 0))
g = []
for k, (title, f, ym, ticks, sv) in enumerate((("Restrictions per act", lambda r: r["restrictions_total"], 1200, (400, 800, 1200), sox["restrictions_total"]),
                                               ("Restrictions per 1,000 words", dens, 40, (10, 20, 30, 40), sox["per_1000_words"]))):
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
charts["per_act_density"] = (f'<svg viewBox="0 0 {VW} {VH + 30}" width="100%" role="img" aria-label="Left: restrictions per act over time, rising. Right: restrictions per 1,000 words, roughly flat. '
                             f'Dots are acts; lines are 5-year averages; dashed line is the Sarbanes-Oxley Act">' + "".join(g) + "</svg>")

json.dump({"charts": charts, "meta": meta}, open("site/mock_charts.json", "w"), ensure_ascii=False)
print(json.dumps(meta))
