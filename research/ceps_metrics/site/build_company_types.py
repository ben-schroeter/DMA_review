"""Chart for the 'By type of company' page: company-specific obligations per type, in force at the start of 2018 (open bar)
and added since, split by CEPS policy area of the law, plus the baseline that applies to all companies.
Writes site/company_types_chart.svg. Run from research/ceps_metrics."""
import collections
exec(open("scripts/company_types.py").read().split('out = {"names"')[0])   # rows, M, TYPES, NAMES, applies(), by_id

INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD_D, STONE = "#8F6708", "#A6A3A0"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
AREAS = [("Finance", "Finance", "#8F6708", "#FFFFFF"), ("Trust & Safety", "Trust &amp; safety", "#B8860B", "#FFFFFF"),
         ("Cybersecurity", "Cybersecurity", "#004494", "#FFFFFF"), ("E-commerce & Consumer Protection", "E-commerce &amp; consumer", "#E3CF9C", INK),
         ("Data & Privacy", "Data &amp; privacy", "#5C5858", "#FFFFFF"), ("Competition & Single Market", "Competition &amp; single market", "#8FA9C9", INK),
         ("Connectivity", "Connectivity", "#282424", "#FFFFFF"), ("Other", "Other", "#D4D2CE", INK)]
KEYS = {a for a, *_ in AREAS}
sel = {k: [r for r in rows if k in M.get(r["row_id"], {}) and applies(M[r["row_id"]][k], r, k)] for k in TYPES}
sel["B"] = [r for r in rows if M.get(r["row_id"], {}).get("B") == "F"]
order = sorted(TYPES, key=lambda k: -len(sel[k])) + ["B"]
area = lambda r: by_id[r["row_id"]]["policy_area_ceps"] if by_id[r["row_id"]]["policy_area_ceps"] in KEYS else "Other"
W, L, R, BH, GAP = 1000, 300, 860, 30, 16
g, lx, ly = [], 2, 4
legend = [("_pre", "In force at the start of 2018", BG, None)] + AREAS
for k, lab, c, _ in legend:
    w = 30 + len(lab.replace("&amp;", "&")) * 6.9
    if lx + w > W:
        lx, ly = 0, ly + 22
    stroke = f' stroke="{STONE}" stroke-width="1.5"' if k == "_pre" else ""
    g.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" rx="2" fill="{c}"{stroke}></rect>' + t(lx + 18, ly + 11, lab, 12.5))
    lx += w + 12
g.append(t(lx if lx + 120 < W else 0, ly + 11 if lx + 120 < W else ly + 33, "Added since, by policy area of the law", 12.5, MUTED) if False else "")
TOP = ly + 52
XM = 4000
X = lambda v: L + v / XM * (R - L)
bot = TOP + len(order) * (BH + GAP) - GAP + 14
g.append(t(W - 4, TOP - 12, "Growth", 13, MUTED, "end"))
for v in range(0, XM + 1, 1000):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{TOP - 4}" y2="{bot + 4}" stroke="{BASE if v == 0 else LINE}"></line>' + t(X(v), bot + 22, f"{v:,}", 12, MUTED, "middle"))
for i, k in enumerate(order):
    y = TOP + i * (BH + GAP) + (14 if k == "B" else 0)
    name = NAMES[k].replace("Baseline: all companies", "Baseline: every company")
    if k == "B":
        g.append(f'<line x1="0" x2="{W}" y1="{y - 15}" y2="{y - 15}" stroke="{LINE}"></line>')
    g.append(t(L - 14, y + BH / 2 + 5, name, 14.5, INK if k != "B" else INK2, "end", 600 if k != "B" else 500))
    pre = sum(1 for r in sel[k] if r["year"] <= 2017)
    add = collections.Counter(area(r) for r in sel[k] if r["year"] >= 2018)
    if pre:
        g.append(f'<rect x="{X(0) + 0.75:.1f}" y="{y + 0.75}" width="{max(X(pre) - X(0) - 1.5, 0.5):.1f}" height="{BH - 1.5}" fill="{BG}" stroke="{STONE}" stroke-width="1.5"><title>{name}: {pre:,} in force at the start of 2018</title></rect>')
    x = pre
    for a, lab, col, tc in AREAS:
        v = add[a]
        if not v:
            continue
        g.append(f'<rect x="{X(x):.1f}" y="{y}" width="{X(x + v) - X(x):.1f}" height="{BH}" fill="{col}" stroke="{BG}" stroke-width="1"><title>{name}, added since 2018 from {lab.replace("&amp;", "&")}: {v:,}</title></rect>')
        if X(x + v) - X(x) > 30:
            g.append(t((X(x) + X(x + v)) / 2, y + BH / 2 + 4.5, f"{v:,}", 11.5, tc, "middle", 600))
        x += v
    tot = len(sel[k])
    g.append(t(X(tot) + 10, y + BH / 2 + 5, f"{tot:,}", 14, INK, "start", 600))
    g.append(t(W - 4, y + BH / 2 + 5, "new" if pre == 0 else f"×{tot / pre:.0f}" if tot / pre >= 10 else f"×{tot / pre:.1f}", 15, GOLD_D, "end", 700))
H = bot + 32
aria = ("Obligations specific to each type of company, in force at the start of 2018 and added since by policy area: "
        + "; ".join(f"{NAMES[k]} {sum(1 for r in sel[k] if r['year'] <= 2017):,} to {len(sel[k]):,}" for k in order))
open("site/company_types_chart.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria.replace("&", "and")}">' + "".join(g) + "</svg>")
