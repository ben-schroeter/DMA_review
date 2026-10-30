"""Statista-style square infographic (1200x1200), same frame as the others: euro-area GDP-per-head gap to the US,
split into output per hour and hours worked, 1980-2024. Data: Long-Term Productivity Database v2.7
(data/bcl_ltp_v27_selected.json). Writes site/infographics/gap_split.svg. Run from research/ceps_metrics."""
import json, math, os

INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
GOLD, GOLD_D, STONE, BG = "#B8860B", "#8F6708", "#A6A3A0", "#FAF9F5"
SANS = 'font-family="DM Sans, sans-serif"'
SERIF = "font-family=\"'Source Serif 4', Georgia, serif\""
W = H = 1200


def t(x, y, txt, size, fill=INK2, anchor="start", weight=400, font=SANS, halo=False):
    h = f' stroke="{BG}" stroke-width="6" paint-order="stroke"' if halo else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {font} font-size="{size}" font-weight="{weight}" fill="{fill}"{h}>{txt}</text>'


S = json.load(open("data/bcl_ltp_v27_selected.json"))["series"]
ser = lambda c, n: {int(y): v for y, v in S[c][n].items()}
Y0, Y1 = 1980, 2024
rel = {n: {y: ser("ZE", n)[y] / ser("USA", n)[y] for y in range(Y0, Y1 + 1)} for n in ("gdp_pc", "lp", "hours_pc")}
dec = {y: (100 * math.log(rel["lp"][y]), 100 * math.log(rel["hours_pc"][y])) for y in rel["lp"]}
share24 = dec[Y1][0] / sum(dec[Y1])

g = [f'<rect width="{W}" height="{H}" fill="{BG}"></rect>', f'<rect width="{W}" height="10" fill="{GOLD}"></rect>']
for i, line in enumerate(("Europe used to be poorer because it", "worked less. Now it is poorer because", "each hour produces less")):
    g.append(t(56, 112 + 60 * i, line, 50, INK, weight=700))
g.append(t(56, 288, "Euro area GDP per head relative to the US, and how much of the gap comes", 24, MUTED))
g.append(t(56, 320, "from output per hour and from hours worked, 1980–2024", 24, MUTED))
# legend
g.append(f'<rect x="56" y="362" width="20" height="20" rx="3" fill="{GOLD}"></rect>' + t(86, 379, "Output per hour", 21, INK2))
g.append(f'<rect x="276" y="362" width="20" height="20" rx="3" fill="{STONE}"></rect>' + t(306, 379, "Hours worked per head", 21, INK2))
g.append(f'<line x1="560" x2="600" y1="372" y2="372" stroke="{INK}" stroke-width="3.5"></line>' + t(612, 379, "Total gap in GDP per head", 21, INK2))
# chart
L, R, TOP, BOT = 104, 56, 430, 990
vmin, vmax = -30, 10
Yv = lambda v: TOP + (vmax - v) / (vmax - vmin) * (BOT - TOP)
n = Y1 - Y0 + 1
slot = (W - L - R) / n; bw = slot * 0.74
xc = lambda y: L + (y - Y0) * slot + slot / 2
for v in range(vmin, vmax + 1, 10):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Yv(v):.1f}" y2="{Yv(v):.1f}" stroke="{BASE if v == 0 else LINE}" stroke-width="{1.6 if v == 0 else 1}"></line>')
    g.append(t(L - 14, Yv(v) + 7, (f"{v:+d}%".replace("-", "−") if v else "US"), 19, MUTED, "end", 600 if v == 0 else 400))
for y in range(Y0, Y1 + 1):
    x = xc(y) - bw / 2
    p, h = dec[y]
    neg = pos = 0
    for v, c in ((h, STONE), (p, GOLD)):
        if v < 0:
            g.append(f'<rect x="{x:.1f}" y="{Yv(neg):.1f}" width="{bw:.1f}" height="{Yv(neg + v) - Yv(neg):.1f}" fill="{c}"></rect>'); neg += v
        else:
            g.append(f'<rect x="{x:.1f}" y="{Yv(pos + v):.1f}" width="{bw:.1f}" height="{Yv(pos) - Yv(pos + v):.1f}" fill="{c}"></rect>'); pos += v
    if y % 5 == 0 or y == Y1:
        g.append(t(xc(y), BOT + 32, y, 18, INK2, "middle", 500 if y == Y1 else 400))
pts = " ".join(f"{xc(y):.1f},{Yv(sum(dec[y])):.1f}" for y in range(Y0, Y1 + 1))
g.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"></polyline>')
g.append(f'<circle cx="{xc(Y1):.1f}" cy="{Yv(sum(dec[Y1])):.1f}" r="6" fill="{INK}"></circle>')
# annotations
g.append(t(xc(1995), Yv(dec[1995][0]) - 16, "1995: the gap is all hours", 20, INK, "middle", 700, halo=True))
g.append(f'<rect x="{L + 20}" y="{Yv(-17) + 6:.1f}" width="430" height="118" rx="12" fill="#FFFFFF" stroke="{LINE}"></rect>')
g.append(t(L + 44, Yv(-17) + 92, f"{share24 * 100:.0f}%", 64, GOLD, weight=700, font=SERIF))
g.append(t(L + 196, Yv(-17) + 46, "of the gap in 2024 comes", 20, INK2))
g.append(t(L + 196, Yv(-17) + 72, "from lower output per hour;", 20, INK2))
g.append(t(L + 196, Yv(-17) + 98, f"GDP per head is {rel['gdp_pc'][Y1] * 100:.0f}% of the US", 20, INK2))
# footer
g.append(f'<line x1="56" x2="{W - 56}" y1="1066" y2="1066" stroke="{LINE}"></line>')
for i, line in enumerate(("Data: Bergeaud, Cette &amp; Lecat; euro area aggregate vs United States at 2020 PPP; own calculation. GDP per head = output",
                          "per hour × hours worked per head, so the gap splits exactly into the two parts; gaps in log points. For the EU-27, the",
                          "Draghi report (AMECO data) puts the productivity share of the 2023 gap at about 72%; in these euro-area data it is 81%.")):
    g.append(t(56, 1100 + 24 * i, line, 16, MUTED))
g.append(f'<g transform="translate({W - 330},1160)"><rect x="0" y="0" width="22" height="22" rx="3" fill="none" stroke="{INK}" stroke-width="1.6"></rect>'
         f'<path d="M5 15h12M5 11h12M5 7h7" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"></path></g>')
g.append(t(W - 298, 1178, "The EU Digital Rulebook", 22, INK, font=SERIF))
g.append(t(56, 1180, f'Source: Long-Term Productivity Database v2.7 · <tspan fill="{GOLD}" font-weight="700" font-size="18">eutechlaws.org</tspan>', 16, INK2, weight=500))

aria = (f"Europe used to be poorer because it worked less. Now it is poorer because each hour produces less. In 1995 the euro area's gap in GDP per head "
        f"to the US came entirely from fewer hours worked; in 2024, {share24 * 100:.0f}% of the gap came from lower output per hour, and GDP per head was "
        f"{rel['gdp_pc'][Y1] * 100:.0f}% of the US level.")
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"
os.makedirs("site/infographics", exist_ok=True)
open("site/infographics/gap_split.svg", "w").write(svg)
print(round(share24 * 100), round(rel["gdp_pc"][Y1] * 100, 1))
