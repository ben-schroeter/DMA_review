"""Front-page chart: euro-area output per hour relative to the US, 1995 = 100, 1900-2024 (same design as the earlier EU4 version).
Data: Long-Term Productivity Database v2.7 (data/bcl_ltp_v27_selected.json, euro area aggregate 'ZE' and 'USA').
Writes site/front_productivity.svg. Run from research/ceps_metrics."""
import json

S = json.load(open("data/bcl_ltp_v27_selected.json"))["series"]
ze, us = ({int(y): v for y, v in S[c]["lp"].items()} for c in ("ZE", "USA"))
Y0, Y1 = 1900, 2024
idx = {y: ze[y] / us[y] / (ze[1995] / us[1995]) * 100 for y in range(Y0, Y1 + 1)}

F = 'font-family="DM Sans, sans-serif"'
L, R, TOP, BOT = 16, 524, 72.3, 394
X = lambda y: L + (y - Y0) / (Y1 - Y0) * (R - L)
Y = lambda v: BOT - v / 100 * (BOT - TOP)
pts = lambda a, b: " ".join(f"{X(y):.1f},{Y(idx[y]):.1f}" for y in range(a, b + 1))
low_y = min(range(1945, 1951), key=lambda y: idx[y])
drop = round(idx[Y1] - 100)

g = [f'<rect x="{X(1945):.1f}" y="24" width="{X(1995) - X(1945):.1f}" height="370" fill="#004494" fill-opacity="0.06"></rect>',
     f'<rect x="{X(1995):.1f}" y="24" width="{X(Y1) - X(1995):.1f}" height="370" fill="#B8860B" fill-opacity="0.08"></rect>']
for v in (20, 40, 60, 80):
    g.append(f'<line x1="{L}" x2="{R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#E8E6E3"></line>'
             f'<text x="532" y="{Y(v) + 5:.1f}" {F} font-size="13" fill="#666666">{v}</text>')
g.append(f'<line x1="{L}" x2="{R}" y1="{TOP}" y2="{TOP}" stroke="#282424" stroke-width="1.2"></line>'
         f'<text x="20" y="64.3" {F} font-size="14" fill="#282424" font-weight="600">1995 level = 100</text>')
for y in (1900, 1920, 1945, 1970, 1995, Y1):
    g.append(f'<text x="{X(y):.1f}" y="416" text-anchor="middle" {F} font-size="13" fill="#666666">{y}</text>')
g.append(f'<line x1="{L}" x2="{R}" y1="{BOT}" y2="{BOT}" stroke="#C9C6C3"></line>')
g.append(f'<polygon points="{pts(1995, Y1)} {X(Y1):.1f},{TOP} {X(1995):.1f},{TOP}" fill="#B8860B" fill-opacity="0.22"></polygon>')
for a, b, c in ((Y0, 1945, "#9A9696"), (1945, 1995, "#004494"), (1995, Y1, "#B8860B")):
    g.append(f'<polyline points="{pts(a, b)}" fill="none" stroke="{c}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"></polyline>')
g.append(f'<circle cx="{X(1995):.1f}" cy="{TOP}" r="5.5" fill="#004494" stroke="#FAF9F5" stroke-width="2"></circle>'
         f'<circle cx="{X(Y1):.1f}" cy="{Y(idx[Y1]):.1f}" r="5.5" fill="#B8860B" stroke="#FAF9F5" stroke-width="2"></circle>')
g.append(f'<text x="{X(2010):.1f}" y="98.5" text-anchor="middle" {F} font-size="22" fill="#8F6708" font-weight="600">{drop:+d}%</text>'.replace("+-", "-"))
g.append(f'<text x="{X(low_y) + 10:.1f}" y="{Y(idx[low_y]) + 18:.1f}" {F} font-size="14" fill="#777373" font-weight="600">{idx[low_y]:.0f}</text>')
g.append(f'<text x="{X(1903):.1f}" y="{Y(idx[1945]) + 30:.1f}" {F} font-size="14" fill="#777373">1914–45: two world wars</text>')
g.append(f'<text x="{X(1958):.1f}" y="326.1" {F} font-size="14" fill="#004494" font-weight="600">1945–95:</text>'
         f'<text x="{X(1958):.1f}" y="345.1" {F} font-size="14" fill="#004494" font-weight="600">Europe catches up</text>')
for k, line in enumerate(("Since 1995:", "Europe misses", "the ICT revolution", "and falls behind")):
    g.append(f'<text x="{X(1996):.1f}" y="{198 + 19 * k:.1f}" {F} font-size="14" fill="#8F6708" font-weight="600">{line}</text>')

aria = (f"Output per hour in the euro area relative to the US, 1995 = 100: from {idx[low_y]:.0f} after the war to 100 in 1995, "
        f"then down to {idx[Y1]:.0f} in {Y1}")
svg = f'<svg viewBox="0 0 560 430" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"
open("site/front_productivity.svg", "w").write(svg)
print(low_y, round(idx[low_y], 1), round(idx[Y1], 1), drop)
