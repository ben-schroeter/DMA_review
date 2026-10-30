"""Charts for the reporting-obligations section of the Rules page (from data/reporting/reporting_instances.jsonl).
  who_type      stacked bars: reporting obligations by who must report, split by type
  areas_growth  dumbbell: companies' reporting obligations by CEPS policy area, start of 2018 vs October 2026
Writes site/reporting_charts.json. Run from research/ceps_metrics."""
import collections, json
import openpyxl

INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD, GOLD_D, STONE, SLATE = "#B8860B", "#8F6708", "#A6A3A0", "#5C5858"
F = 'font-family="DM Sans, sans-serif"'


def t(x, y, s, size=13, fill=INK2, anchor="start", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"{w}>{s}</text>'


wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)


def sheet(n):
    rows = list(wb[n].values); h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r[0] is not None]


I, S = sheet("instruments"), sheet("secondary_acts")
main = {r["celex_measured"]: r for r in I if r["celex_measured"] and r["status_oct2026"] == "adopted" and r["adoption_date"] and r["restrictions_total"] is not None}
sec = {r["celex"]: r for r in S if r["kind"] in ("implementing", "delegated") and r["date"] and r["restrictions_total"] is not None}
by_id = {r["row_id"]: r for r in I}
rep = [r for r in map(json.loads, open("data/reporting/reporting_instances.jsonl"))
       if r["reporting"] and ((r["kind"] == "main" and r["doc"] in main) or (r["kind"] == "secondary" and r["doc"] in sec))]
year = lambda r: int(str(main[r["doc"]]["adoption_date"])[:4]) if r["kind"] == "main" else int(str(sec[r["doc"]]["date"])[:4])
area = lambda r: (main[r["doc"]] if r["kind"] == "main" else by_id[sec[r["doc"]]["parent_row_id"]])["policy_area_ceps"]
charts = {}

# 1. who reports, by type
TYPES = [("report_submission", "Reports and submissions", GOLD, "#FFFFFF"), ("notification", "Notifications", SLATE, "#FFFFFF"),
         ("disclosure", "Disclosure to public or users", "#E3CF9C", INK), ("record_keeping", "Record-keeping", STONE, INK),
         ("on_request", "Information on request", "#004494", "#FFFFFF"), ("registration", "Registration", INK, "#FFFFFF")]
WHO = [("private_parties", "Companies"), ("member_states", "Member states"), ("eu_institutions", "EU institutions")]
cnt = {w: collections.Counter(r["type"] for r in rep if r["addressee"] == w) for w, _ in WHO}
W, L, R, TOP, BH, GAP = 1000, 150, 900, 70, 40, 26
XMAX = 2200
X = lambda v: L + v / XMAX * (R - L)
g, lx, ly = [], 0, 6
for k, lab, c, _ in TYPES:     # legend, wraps to two rows
    w = 26 + len(lab) * 7.2
    if lx + w > W:
        lx, ly = 0, ly + 22
    g.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" rx="2" fill="{c}"></rect>' + t(lx + 18, ly + 11, lab, 13))
    lx += w + 18
for v in range(0, XMAX + 1, 500):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{TOP - 6}" y2="{TOP + 3 * (BH + GAP) - GAP + 6}" stroke="{BASE if v == 0 else LINE}"></line>')
    g.append(t(X(v), TOP + 3 * (BH + GAP) - GAP + 26, f"{v:,}", 12, MUTED, "middle"))
for i, (w, lab) in enumerate(WHO):
    y = TOP + i * (BH + GAP); x = 0
    g.append(t(L - 14, y + BH / 2 + 5, lab, 15, INK, "end", 600))
    for k, tl, c, tc in TYPES:
        v = cnt[w][k]
        if not v:
            continue
        g.append(f'<rect x="{X(x):.1f}" y="{y}" width="{X(x + v) - X(x):.1f}" height="{BH}" fill="{c}" stroke="{BG}" stroke-width="1"><title>{lab}, {tl}: {v:,}</title></rect>')
        if X(x + v) - X(x) > 44:
            g.append(t((X(x) + X(x + v)) / 2, y + BH / 2 + 5, f"{v:,}", 12.5, tc, "middle", 600))
        x += v
    g.append(t(X(x) + 10, y + BH / 2 + 5, f"{x:,}", 15, INK, "start", 600))
H = TOP + 3 * (BH + GAP) - GAP + 36
charts["who_type"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Reporting obligations by who must report and type: '
                      + "; ".join(f"{lab} {sum(cnt[w].values()):,}" for w, lab in WHO) + '">' + "".join(g) + "</svg>")

# 2. companies by policy area, start of 2018 vs now
pp = [r for r in rep if r["addressee"] == "private_parties"]
then, now = collections.Counter(area(r) for r in pp if year(r) <= 2017), collections.Counter(area(r) for r in pp)
areas = sorted(now, key=lambda a: -now[a])
W, PL, PR, PTOP, PROW = 1000, 250, 860, 50, 36
VMAX = 600
PX = lambda v: PL + v / VMAX * (PR - PL)
PBOT = PTOP + PROW * len(areas)
g = [f'<circle cx="10" cy="12" r="6.5" fill="{BG}" stroke="{STONE}" stroke-width="2.5"></circle>' + t(24, 17, "Start of 2018", 14),
     f'<circle cx="140" cy="12" r="7" fill="{GOLD}"></circle>' + t(154, 17, "October 2026", 14), t(W - 4, PTOP - 12, "Growth", 13, MUTED, "end")]
for v in range(0, VMAX + 1, 100):
    g.append(f'<line x1="{PX(v):.1f}" x2="{PX(v):.1f}" y1="{PTOP - 4}" y2="{PBOT}" stroke="{BASE if v == 0 else LINE}"></line>' + t(PX(v), PBOT + 20, v, 13, MUTED, "middle"))
for i, a in enumerate(areas):
    y = PTOP + PROW * i + PROW / 2
    al = a.replace(" Protection", "").replace("&", "&amp;")
    g.append(t(PL - 14, y + 5, al, 14.5, INK, "end", 500))
    g.append(f'<line x1="{PX(then[a]):.1f}" x2="{PX(now[a]):.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity="0.45" stroke-width="4.5" stroke-linecap="round"></line>')
    g.append(f'<circle cx="{PX(then[a]):.1f}" cy="{y:.1f}" r="6" fill="{BG}" stroke="{STONE}" stroke-width="2.5"><title>{al}, start of 2018: {then[a]}</title></circle>')
    g.append(f'<circle cx="{PX(now[a]):.1f}" cy="{y:.1f}" r="7.5" fill="{GOLD}"><title>{al}, October 2026: {now[a]}</title></circle>')
    g.append(t(PX(now[a]) + 13, y + 5, f"{now[a]:,}", 13, INK2))
    g.append(t(W - 4, y + 5, "new" if then[a] == 0 else f"×{now[a] / then[a]:.1f}", 15, GOLD_D, "end", 700))
charts["areas_growth"] = (f'<svg viewBox="0 0 {W} {PBOT + 30}" width="100%" role="img" aria-label="Companies\' reporting obligations by policy area, start of 2018 and October 2026: '
                          + "; ".join(f"{a.replace('&', 'and')} {then[a]} to {now[a]}" for a in areas) + '">' + "".join(g) + "</svg>")
json.dump(charts, open("site/reporting_charts.json", "w"), ensure_ascii=False)
print({w: sum(cnt[w].values()) for w, _ in WHO}, sum(then.values()), len(pp), {a: (then[a], now[a]) for a in areas})
