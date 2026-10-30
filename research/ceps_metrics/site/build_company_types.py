"""Chart for the 'By type of company' page: company-specific obligations per type, in force at the start of 2018 vs added since,
plus the baseline that applies to all companies. Reads data/company_types/summary.json; writes site/company_types_chart.svg."""
import json

INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD, GOLD_D, STONE = "#B8860B", "#8F6708", "#A6A3A0"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
d = json.load(open("data/company_types/summary.json"))
rows = sorted(((k, d["names"][k], v["obligations"], v["start_2018"]) for k, v in d["types"].items()), key=lambda r: -r[2])
rows.append(("B", "Baseline: all companies", d["baseline"]["obligations"], d["baseline"]["start_2018"]))
W, L, R, TOP, BH, GAP = 1000, 300, 860, 44, 30, 16
XM = 4000
X = lambda v: L + v / XM * (R - L)
g = [f'<rect x="{L}" y="4" width="12" height="12" rx="2" fill="{STONE}"></rect>' + t(L + 18, 15, "In force at the start of 2018", 13),
     f'<rect x="{L + 220}" y="4" width="12" height="12" rx="2" fill="{GOLD}"></rect>' + t(L + 238, 15, "Added since", 13),
     t(W - 4, TOP - 12, "Growth", 13, MUTED, "end")]
bot = TOP + len(rows) * (BH + GAP) - GAP + 14
for v in range(0, XM + 1, 1000):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{TOP - 4}" y2="{bot + 4}" stroke="{BASE if v == 0 else LINE}"></line>' + t(X(v), bot + 22, f"{v:,}", 12, MUTED, "middle"))
for i, (k, name, tot, s18) in enumerate(rows):
    y = TOP + i * (BH + GAP) + (14 if k == "B" else 0)
    if k == "B":
        g.append(f'<line x1="0" x2="{W}" y1="{y - 15}" y2="{y - 15}" stroke="{LINE}"></line>')
    g.append(t(L - 14, y + BH / 2 + 5, name, 14.5, INK if k != "B" else INK2, "end", 600 if k != "B" else 500))
    g.append(f'<rect x="{X(0):.1f}" y="{y}" width="{X(s18) - X(0):.1f}" height="{BH}" fill="{STONE}"><title>{name}: {s18:,} at the start of 2018</title></rect>')
    g.append(f'<rect x="{X(s18):.1f}" y="{y}" width="{X(tot) - X(s18):.1f}" height="{BH}" fill="{GOLD}"><title>{name}: {tot - s18:,} added since 2018</title></rect>')
    g.append(t(X(tot) + 10, y + BH / 2 + 5, f"{tot:,}", 14, INK, "start", 600))
    g.append(t(W - 4, y + BH / 2 + 5, "new" if s18 == 0 else f"×{tot / s18:.0f}" if tot / s18 >= 10 else f"×{tot / s18:.1f}", 15, GOLD_D, "end", 700))
H = bot + 32
aria = "Obligations specific to each type of company, at the start of 2018 and in October 2026: " + "; ".join(f"{n} {s:,} to {tt:,}" for k, n, tt, s in rows)
svg = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"
open("site/company_types_chart.svg", "w").write(svg)
print(rows)
