"""EU vs US matched pairs: obligations per act for each pair, all obligations and obligations on companies only.
Reads data/us_map/us_private.json (scripts/us_private.py). Pairs whose both sides mainly bind public bodies are left out.
Writes site/us_pairs.svg and prints the summary figures used in the text. Run from research/ceps_metrics."""
import json, statistics

DROP = {35, 43, 78}       # EU institutions data protection / Privacy Act, Open Data / OPEN Government Data Act, EU institutions cybersecurity / FISMA
SHORT = {13: "Unfair Commercial Practices → FTC Act §5", 17: "Toy Safety → CPSIA", 20: "GDPR → CCPA (California)", 26: "Trade Secrets → Defend Trade Secrets Act",
         42: "E-evidence → CLOUD Act", 67: "Product Safety → CPSA", 74: "Chips Act → CHIPS Act", 64: "AI Act → Colorado AI Act (state)"}
P = [x for x in json.load(open("data/us_map/us_private.json")) if x["row_id"] not in DROP]
for x in P:
    x["ra"] = x["eu_total"] / x["us_total"]; x["rc"] = x["eu_private"] / x["us_private"]
P.sort(key=lambda x: -x["ra"])
INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#F5F5F0"
GOLD, GOLD_L, GREY = "#B8860B", "#E3CF9C", "#A6A3A0"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
W, L, R, RH, TOP, XM = 1000, 330, 830, 58, 58, 800
X = lambda v: L + v / XM * (R - L)
g = []
# legend
lx = 0
for lab, fill, stroke in (("EU act", GOLD, GOLD), ("US counterpart", INK, INK)):
    g.append(f'<circle cx="{lx + 6}" cy="10" r="6" fill="{fill}"></circle>' + t(lx + 18, 15, lab, 13)); lx += 34 + len(lab) * 7
g.append(f'<line x1="{lx}" x2="{lx + 26}" y1="10" y2="10" stroke="{BASE}" stroke-width="2"></line>' + t(lx + 32, 15, "All obligations (light)", 13)); lx += 210
g.append(f'<line x1="{lx}" x2="{lx + 26}" y1="10" y2="10" stroke="{INK2}" stroke-width="2.5"></line>' + t(lx + 32, 15, "Obligations on companies (bold)", 13))
g.append(t(R + 40, TOP - 12, "All", 12, MUTED, "end") + t(W, TOP - 12, "Companies", 12, MUTED, "end"))
for v in range(0, XM + 1, 200):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{TOP - 4}" y2="{TOP + len(P) * RH - 6}" stroke="{LINE if v else BASE}"></line>')
    g.append(t(X(v), TOP + len(P) * RH + 12, v, 12, MUTED, "middle"))
for i, x in enumerate(P):
    y = TOP + i * RH
    g.append(t(L - 16, y + 25, SHORT[x["row_id"]], 14.5, INK, "end"))
    ya, yc = y + 14, y + 34
    # all obligations: light
    a0, a1 = sorted((x["us_total"], x["eu_total"]))
    g.append(f'<line x1="{X(a0):.1f}" x2="{X(a1):.1f}" y1="{ya}" y2="{ya}" stroke="{BASE}" stroke-width="2"></line>')
    g.append(f'<circle cx="{X(x["us_total"]):.1f}" cy="{ya}" r="5" fill="{GREY}"><title>{x["us"]}: {x["us_total"]} obligations</title></circle>')
    g.append(f'<circle cx="{X(x["eu_total"]):.1f}" cy="{ya}" r="5" fill="{GOLD_L}"><title>{x["eu"]}: {x["eu_total"]} obligations</title></circle>')
    # companies: bold
    c0, c1 = sorted((x["us_private"], x["eu_private"]))
    g.append(f'<line x1="{X(c0):.1f}" x2="{X(c1):.1f}" y1="{yc}" y2="{yc}" stroke="{INK2}" stroke-width="2.5"></line>')
    g.append(f'<circle cx="{X(x["us_private"]):.1f}" cy="{yc}" r="6.5" fill="{INK}"><title>{x["us"]}: {x["us_private"]} obligations on companies</title></circle>')
    g.append(f'<circle cx="{X(x["eu_private"]):.1f}" cy="{yc}" r="6.5" fill="{GOLD}"><title>{x["eu"]}: {x["eu_private"]} obligations on companies</title></circle>')
    g.append(t(R + 40, y + 25, f'×{x["ra"]:.1f}', 14, MUTED, "end"))
    g.append(t(W, y + 25, f'×{x["rc"]:.1f}', 15, INK, "end", 700))
    if i < len(P) - 1:
        g.append(f'<line x1="0" x2="{W}" y1="{y + RH - 6}" y2="{y + RH - 6}" stroke="{LINE}"></line>')
H = TOP + len(P) * RH + 22
aria = "Matched EU and US laws, obligations per act, all and on companies only: " + "; ".join(
    f'{SHORT[x["row_id"]]}: all {x["eu_total"]} vs {x["us_total"]}, companies {x["eu_private"]} vs {x["us_private"]}' for x in P)
open("site/us_pairs.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
ra, rc = [x["ra"] for x in P], [x["rc"] for x in P]
print("pairs", len(P), "median all", round(statistics.median(ra), 2), "median companies", round(statistics.median(rc), 2))
print("means all", round(statistics.mean(x["eu_total"] for x in P)), round(statistics.mean(x["us_total"] for x in P)),
      "companies", round(statistics.mean(x["eu_private"] for x in P)), round(statistics.mean(x["us_private"] for x in P)))
