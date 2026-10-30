"""Statista-style square infographic (1200x1200), same frame as the others: obligations on companies by CEPS policy area,
start of 2018 vs October 2026, in adopted acts plus their implementing and delegated acts (dumbbell chart).
Writes site/infographics/areas_growth.svg. Run from research/ceps_metrics."""
import collections, os
import openpyxl

INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
GOLD, GOLD_D, STONE, SLATE, BG = "#B8860B", "#8F6708", "#A6A3A0", "#5C5858", "#FAF9F5"
SANS = 'font-family="DM Sans, sans-serif"'
SERIF = "font-family=\"'Source Serif 4', Georgia, serif\""
W = H = 1200


def t(x, y, txt, size, fill=INK2, anchor="start", weight=400, font=SANS):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {font} font-size="{size}" font-weight="{weight}" fill="{fill}">{txt}</text>'


wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)


def sheet(n):
    rows = list(wb[n].values); h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r[0] is not None]


instruments = sheet("instruments")
area_of = {r["row_id"]: r["policy_area_ceps"] for r in instruments}
inst = [r for r in instruments if r["adoption_date"] and r["restrictions_total"] is not None and r["status_oct2026"] == "adopted"]
sec = [r for r in sheet("secondary_acts") if r["kind"] in ("implementing", "delegated") and r["date"] and r["restrictions_total"] is not None]
yr = lambda d: int(str(d)[:4])
then, now, now_laws = collections.Counter(), collections.Counter(), collections.Counter()
for r in inst:
    now_laws[r["policy_area_ceps"]] += r["addr_private_parties"] or 0
for a, d, v in ([(r["policy_area_ceps"], r["adoption_date"], r["addr_private_parties"] or 0) for r in inst] +
                [(area_of.get(r["parent_row_id"]), r["date"], r["addr_private_parties"] or 0) for r in sec]):
    now[a] += v
    if yr(d) <= 2017:
        then[a] += v
areas = sorted(now, key=lambda a: -now[a])
factor = sum(now.values()) / sum(then.values())

g = [f'<rect width="{W}" height="{H}" fill="{BG}"></rect>', f'<rect width="{W}" height="10" fill="{GOLD}"></rect>']
for i, line in enumerate(("EU rules for tech companies have", "grown in every policy area.")):
    g.append(t(56, 112 + 60 * i, line, 50, INK, weight=700))
g.append(t(56, 228, "Obligations on companies in EU digital laws and their implementing and", 24, MUTED))
g.append(t(56, 260, "delegated acts, by policy area: start of 2018 and October 2026", 24, MUTED))
g.append(f'<circle cx="66" cy="310" r="9" fill="{BG}" stroke="{STONE}" stroke-width="3"></circle>' + t(86, 317, "Start of 2018", 21, INK2))
g.append(f'<circle cx="252" cy="310" r="7" fill="{SLATE}" stroke="{BG}" stroke-width="2"></circle>' + t(268, 317, "2026: laws only", 21, INK2))
g.append(f'<circle cx="452" cy="310" r="10" fill="{GOLD}"></circle>' + t(472, 317, "2026: plus implementing and delegated acts", 21, INK2))
# chart
L, R, TOP, ROW = 400, 990, 370, 52
VMAX = 3600
X = lambda v: L + v / VMAX * (R - L)
BOT = TOP + ROW * len(areas)
g.append(t(W - 56, TOP - 14, "Growth", 18, MUTED, "end"))
for v in range(0, VMAX + 1, 1000):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{TOP - 6}" y2="{BOT}" stroke="{BASE if v == 0 else LINE}"></line>')
    g.append(t(X(v), BOT + 28, f"{v:,}", 18, MUTED, "middle"))
for i, a in enumerate(areas):
    y = TOP + ROW * i + ROW / 2
    lab = a.replace(" Protection", "").replace("&", "&amp;")
    g.append(t(L - 20, y + 7, lab, 20, INK, "end", 500))
    g.append(f'<line x1="{X(then[a]):.1f}" x2="{X(now[a]):.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity="0.45" stroke-width="6" stroke-linecap="round"></line>')
    g.append(f'<circle cx="{X(then[a]):.1f}" cy="{y:.1f}" r="8" fill="{BG}" stroke="{STONE}" stroke-width="3"></circle>')
    g.append(f'<circle cx="{X(now[a]):.1f}" cy="{y:.1f}" r="10" fill="{GOLD}"></circle>')
    g.append(f'<circle cx="{X(now_laws[a]):.1f}" cy="{y:.1f}" r="7" fill="{SLATE}" stroke="{BG}" stroke-width="2"></circle>')
    g.append(t(X(now[a]) + 18, y + 6, f"{now[a]:,}", 17, INK2))
    gr = "new" if then[a] == 0 else f"×{now[a] / then[a]:.1f}"
    g.append(t(W - 56, y + 7, gr, 21, GOLD_D, "end", 700))
# callout
cx, cy, cw, ch = 600, BOT - 4 * ROW - 6, 474, 132
g.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="#FFFFFF" stroke="{LINE}"></rect>')
g.append(t(cx + 24, cy + 90, f"×{factor:.1f}", 64, GOLD, weight=700, font=SERIF))
g.append(t(cx + 190, cy + 50, "obligations on companies", 20, INK2))
g.append(t(cx + 190, cy + 76, f"across all areas: {sum(then.values()):,} at the", 20, INK2))
g.append(t(cx + 190, cy + 102, f"start of 2018, {sum(now.values()):,} now", 20, INK2))
# footer
g.append(f'<line x1="56" x2="{W - 56}" y1="1066" y2="1066" stroke="{LINE}"></line>')
for i, line in enumerate(("Policy areas follow CEPS (Zenner &amp; Marcus, 2025). Automated count of obligations naming a company as the one who must act, in the",
                          "105 adopted EU digital acts and their 690 implementing and delegated acts; “new”: no such obligations before 2018. Counts measure",
                          "the number of rules, not their cost. Acts repealed before 2018 are not in the inventory, so earlier totals are a lower bound.")):
    g.append(t(56, 1100 + 24 * i, line, 16, MUTED))
g.append(f'<g transform="translate({W - 330},1160)"><rect x="0" y="0" width="22" height="22" rx="3" fill="none" stroke="{INK}" stroke-width="1.6"></rect>'
         f'<path d="M5 15h12M5 11h12M5 7h7" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"></path></g>')
g.append(t(W - 298, 1178, "The EU Digital Rulebook", 22, INK, font=SERIF))
g.append(t(56, 1180, f'Source: The EU Digital Rulebook (2026) · <tspan fill="{GOLD}" font-weight="700" font-size="18">eutechlaws.org</tspan>', 16, INK2, weight=500))

aria = ("EU rules for tech companies have grown in every policy area. Obligations on companies, start of 2018 to October 2026: "
        + "; ".join(f"{a} {then[a]:,} to {now[a]:,}" for a in areas) + f". Across all areas x{factor:.1f}.")
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria.replace("&", "&amp;")}">' + "".join(g) + "</svg>"
os.makedirs("site/infographics", exist_ok=True)
open("site/infographics/areas_growth.svg", "w").write(svg)
print({a: (then[a], now[a]) for a in areas}, round(factor, 2))

# Page version for the Rules page (1000 wide, no headline or footer), same data and encoding
PW, PL, PR, PTOP, PROW = 1000, 250, 840, 64, 40
PX = lambda v: PL + v / VMAX * (PR - PL)
PBOT = PTOP + PROW * len(areas)
p = [f'<circle cx="10" cy="12" r="6.5" fill="{BG}" stroke="{STONE}" stroke-width="2.5"></circle>' + t(24, 17, "Start of 2018", 14, INK2),
     f'<circle cx="138" cy="12" r="5" fill="{SLATE}" stroke="{BG}" stroke-width="1.5"></circle>' + t(150, 17, "2026: laws only", 14, INK2),
     f'<circle cx="282" cy="12" r="7" fill="{GOLD}"></circle>' + t(296, 17, "2026: plus implementing and delegated acts", 14, INK2),
     t(PW - 4, PTOP - 14, "Growth", 13, MUTED, "end")]
for v in range(0, VMAX + 1, 1000):
    p.append(f'<line x1="{PX(v):.1f}" x2="{PX(v):.1f}" y1="{PTOP - 4}" y2="{PBOT}" stroke="{BASE if v == 0 else LINE}"></line>')
    p.append(t(PX(v), PBOT + 20, f"{v:,}", 13, MUTED, "middle"))
for i, a in enumerate(areas):
    y = PTOP + PROW * i + PROW / 2
    p.append(t(PL - 14, y + 5, a.replace(" Protection", "").replace("&", "&amp;"), 14.5, INK, "end", 500))
    p.append(f'<line x1="{PX(then[a]):.1f}" x2="{PX(now[a]):.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity="0.45" stroke-width="4.5" stroke-linecap="round"></line>')
    p.append(f'<circle cx="{PX(then[a]):.1f}" cy="{y:.1f}" r="6" fill="{BG}" stroke="{STONE}" stroke-width="2.5"><title>{a.replace("&", "&amp;")}, start of 2018: {then[a]:,}</title></circle>')
    p.append(f'<circle cx="{PX(now[a]):.1f}" cy="{y:.1f}" r="7.5" fill="{GOLD}"><title>{a.replace("&", "&amp;")}, October 2026: {now[a]:,}</title></circle>')
    p.append(f'<circle cx="{PX(now_laws[a]):.1f}" cy="{y:.1f}" r="5" fill="{SLATE}" stroke="{BG}" stroke-width="1.5"><title>{a.replace("&", "&amp;")}, laws only, October 2026: {now_laws[a]:,}</title></circle>')
    p.append(t(PX(now[a]) + 13, y + 5, f"{now[a]:,}", 13, INK2))
    p.append(t(PW - 4, y + 5, "new" if then[a] == 0 else f"×{now[a] / then[a]:.1f}", 15, GOLD_D, "end", 700))
page_svg = (f'<svg viewBox="0 0 {PW} {PBOT + 30}" width="100%" role="img" aria-label="{aria.replace("&", "&amp;")}">' + "".join(p) + "</svg>")
open("site/areas_growth_page.svg", "w").write(page_svg)

# Small multiples over time for the Rules page: cumulative obligations on companies by policy area, laws vs implementing/delegated acts
TY0, TY1 = 2000, 2026
LAWC, SECC = GOLD, "#E3CF9C"
ser_l, ser_s = {}, {}
for a in areas:
    bl = collections.Counter(yr(r["adoption_date"]) for r in inst if r["policy_area_ceps"] == a for _ in range(r["addr_private_parties"] or 0))
    bs = collections.Counter(yr(r["date"]) for r in sec if area_of.get(r["parent_row_id"]) == a for _ in range(r["addr_private_parties"] or 0))
    rl, rs = sum(v for y, v in bl.items() if y < TY0), sum(v for y, v in bs.items() if y < TY0)
    ser_l[a], ser_s[a] = {}, {}
    for y in range(TY0, TY1 + 1):
        rl += bl[y]; rs += bs[y]; ser_l[a][y], ser_s[a][y] = rl, rs
NC, TW, LM, PW, GX, PH, GY, TT = 4, 1000, 44, 206, 34, 110, 74, 12
TYM = 4000
q = [f'<rect x="{LM}" y="4" width="12" height="12" rx="2" fill="{LAWC}"></rect>' + t(LM + 18, 15, "In the laws", 13),
     f'<rect x="{LM + 120}" y="4" width="12" height="12" rx="2" fill="{SECC}"></rect>' + t(LM + 138, 15, "In implementing and delegated acts", 13),
     f'<line x1="{LM + 390}" x2="{LM + 390}" y1="2" y2="18" stroke="{STONE}" stroke-dasharray="3 3"></line>' + t(LM + 398, 15, "start of 2018", 13, MUTED)]
for i, a in enumerate(areas):
    x0 = LM + (i % NC) * (PW + GX); y0 = TT + 58 + (i // NC) * (PH + GY)
    SX = lambda y, x0=x0: x0 + (y - TY0) / (TY1 - TY0) * PW
    SY = lambda v, y0=y0: y0 + PH - v / TYM * PH
    for v in (1000, 2000, 3000, 4000):
        q.append(f'<line x1="{x0}" x2="{x0 + PW}" y1="{SY(v):.1f}" y2="{SY(v):.1f}" stroke="{LINE}"></line>')
        if i % NC == 0:
            q.append(t(x0 - 6, SY(v) + 4, f"{v // 1000}k", 11.5, MUTED, "end"))
    def steps(vals):
        out, prev = [], None
        for y in range(TY0, TY1 + 1):
            px, py = SX(y), SY(vals[y])
            if prev is not None:
                out.append(f"{px:.1f},{prev:.1f}")
            out.append(f"{px:.1f},{py:.1f}"); prev = py
        return out
    tot = {y: ser_l[a][y] + ser_s[a][y] for y in ser_l[a]}
    top_pts, law_pts = steps(tot), steps(ser_l[a])
    q.append(f'<polygon points="{SX(TY0):.1f},{SY(0):.1f} {" ".join(top_pts)} {SX(TY1):.1f},{SY(0):.1f}" fill="{SECC}"></polygon>')
    q.append(f'<polygon points="{SX(TY0):.1f},{SY(0):.1f} {" ".join(law_pts)} {SX(TY1):.1f},{SY(0):.1f}" fill="{LAWC}"></polygon>')
    q.append(f'<line x1="{SX(2018):.1f}" x2="{SX(2018):.1f}" y1="{y0 - 4}" y2="{y0 + PH}" stroke="{STONE}" stroke-dasharray="3 3"></line>')
    q.append(f'<line x1="{x0}" x2="{x0 + PW}" y1="{y0 + PH}" y2="{y0 + PH}" stroke="{BASE}"></line>')
    for y in (2000, 2018, 2026):
        q.append(t(SX(y), y0 + PH + 15, y, 11, MUTED, "middle"))
    gr = "new since 2018" if then[a] == 0 else f"×{now[a] / then[a]:.1f} since 2018"
    q.append(f'<rect x="{x0}" y="{y0}" width="{PW}" height="{PH}" fill="transparent"><title>{a.replace("&", "&amp;")}: {then[a]:,} at the start of 2018, {now[a]:,} in October 2026 ({now_laws[a]:,} in the laws)</title></rect>')
    q.append(t(x0, y0 - 22, a.replace(" Protection", "").replace("&", "&amp;"), 14, INK, "start", 600))
    q.append(t(x0, y0 - 6, f'{now[a]:,} <tspan fill="{GOLD_D}" font-weight="600">{gr}</tspan>', 12.5, MUTED))
TH = TT + 58 + 3 * (PH + GY) - GY + 26
time_svg = (f'<svg viewBox="0 0 {TW} {TH}" width="100%" role="img" aria-label="Obligations on companies by policy area, cumulative 2000 to 2026, twelve panels on shared axes, '
            f'split into the laws and their implementing and delegated acts: ' + "; ".join(f"{a.replace('&', 'and')} {then[a]:,} at the start of 2018, {now[a]:,} in 2026" for a in areas) + '">' + "".join(q) + "</svg>")
open("site/areas_growth_time.svg", "w").write(time_svg)
