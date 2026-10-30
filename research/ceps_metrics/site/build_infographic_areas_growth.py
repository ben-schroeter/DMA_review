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
