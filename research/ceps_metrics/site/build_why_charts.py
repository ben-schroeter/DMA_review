"""Inline-SVG redraws of three external charts for the 'Why it matters' page (Draghi, Gordon & Sayed, McKinsey).
Writes site/why_charts.json. Values are as published; McKinsey points are read off the published chart. Run from research/ceps_metrics."""
import json

INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
EU, US = "#B8860B", "#5C5858"
F = 'font-family="DM Sans, sans-serif"'
charts = {}


def t(x, y, s, size=13, fill=INK2, anchor="start", weight=None, italic=False):
    w = f' font-weight="{weight}"' if weight else ""
    it = ' font-style="italic"' if italic else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"{w}{it}>{s}</text>'


# 1. Draghi report: GDP per capita gap, EU-27 vs US, 2023, split into productivity and labour contributions
W, H, L = 560, 330, 130
eu_len, us_len = 270, 400          # schematic: only the 72/28 split of the gap is to scale
gap = us_len - eu_len
p_len = 0.72 * gap
rows = [("EU-27", L, eu_len, EU, None), ("Productivity|GDP per hour", L + eu_len, p_len, "#D9BE7A", "~72%"),
        ("Labour|hours per head", L + eu_len + p_len, gap - p_len, "#E3CF9C", "~28%"), ("US", L, us_len, US, None)]
g = [f'<line x1="{L}" x2="{L}" y1="10" y2="{H - 20}" stroke="{BASE}"></line>']
for i, (lab, x0, w, c, pct) in enumerate(rows):
    y = 18 + i * 76
    if "|" in lab:
        a, b = lab.split("|"); g.append(t(L - 12, y + 18, a, 13.5, INK2, "end")); g.append(t(L - 12, y + 35, b, 12, MUTED, "end"))
    else:
        g.append(t(L - 12, y + 27, lab, 13.5, INK, "end", 600))
    g.append(f'<rect x="{x0:.1f}" y="{y}" width="{w:.1f}" height="40" fill="{c}"></rect>')
    if pct:
        g.append(t(x0 + w / 2, y + 26, pct, 14, INK, "middle", 600) if w > 50 else t(x0 + w + 8, y + 26, pct, 14, INK, "start", 600))
        g.append(f'<line x1="{x0:.1f}" x2="{x0:.1f}" y1="{y - 36}" y2="{y}" stroke="{BASE}" stroke-dasharray="2 3"></line>')
g.append(f'<line x1="{L + us_len:.1f}" x2="{L + us_len:.1f}" y1="{18 + 2 * 76 + 40}" y2="{18 + 3 * 76}" stroke="{BASE}" stroke-dasharray="2 3"></line>')
charts["draghi_gap"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="GDP per capita gap between the EU-27 and the US in 2023: '
                        f'about 72% of the gap is due to lower productivity per hour and about 28% to fewer hours worked per head">' + "".join(g) + "</svg>")

# 2. Gordon & Sayed (2020): contribution to post-1995 change in productivity growth, US vs EU-10 (percentage points)
data = [("ICT-using services", -0.28, 0.63), ("ICT-producing goods", -0.02, 0.26), ("Non-ICT goods", -0.32, 0.21),
        ("ICT-producing services", 0.11, 0.15), ("ICT-using goods", -0.11, 0.05), ("Non-ICT services", -0.10, 0.01)]
W, L, Z, S = 560, 168, 318, 300      # label column, zero line x, px per point
rh = 58
H = 40 + len(data) * rh
X = lambda v: Z + v * S
g = [f'<rect x="{L}" y="6" width="12" height="12" rx="2" fill="{EU}"></rect>' + t(L + 18, 16.5, "EU-10", 12.5),
     f'<rect x="{L + 80}" y="6" width="12" height="12" rx="2" fill="{US}"></rect>' + t(L + 98, 16.5, "US", 12.5),
     f'<line x1="{Z}" x2="{Z}" y1="30" y2="{H - 4}" stroke="{INK2}"></line>']
for i, (lab, e, u) in enumerate(data):
    y = 34 + i * rh
    g.append(t(L - 12, y + 25, lab, 13.5, INK if i == 0 else INK2, "end", 600 if i == 0 else None))
    for j, (v, c) in enumerate(((e, EU), (u, US))):
        yy = y + 6 + j * 20
        x0, w = (X(v), Z - X(v)) if v < 0 else (Z, X(v) - Z)
        g.append(f'<rect x="{x0:.1f}" y="{yy}" width="{max(w, 1.5):.1f}" height="16" fill="{c}"></rect>')
        lx, an = (x0 - 6, "end") if v < 0 else (x0 + max(w, 1.5) + 6, "start")
        g.append(t(lx, yy + 12.5, f"{v:+.2f}".replace("+0", "+0").replace("-", "−"), 12.5, INK, an, 600))
charts["gordon_ict"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Contribution to post-1995 change in productivity growth, '
                        f'percentage points, EU-10 vs US: ' + "; ".join(f"{a} EU {e:+.2f}, US {u:+.2f}" for a, e, u in data) + '">' + "".join(g) + "</svg>")

# 3. McKinsey Global Institute (2015 digitisation index) vs US labour productivity growth 1989-2019, by sector
pts = [("Information", 6, 5.1, -9, 4.5, "end"), ("Wholesale trade", 4, 3.5, 0, -10, "middle"), ("Retail trade", 3, 2.6, -8, 4, "end"),
       ("Manufacturing", 3, 2.45, 8, 0, "start"), ("", 3, 2.0, 0, 0, "start"), ("", 3, 1.9, 0, 0, "end"),
       ("", 3, 1.7, 0, 0, "start"), ("Other services", 3, 1.0, 8, 0, "start"), ("Accommodation &amp; food", 3, 0.9, 0, 20, "middle"),
       ("Utilities", 4, 2.2, 0, 20, "middle"), ("Finance", 5, 2.2, 0, -10, "middle"), ("Professional services", 5, 1.7, 0, 20, "middle"),
       ("Arts &amp; entertainment", 1, 1.8, 0, -10, "middle"), ("Mining", 2, 1.9, 0, -10, "middle"), ("Transport &amp; storage", 2, 1.0, 0, -10, "middle"),
       ("Construction", 1, -0.2, 0, 18, "middle"), ("Healthcare", 2, 0.0, 0, 18, "middle")]
W, H, L, R, T, B = 560, 440, 48, 24, 16, 52
X = lambda v: L + v / 6.4 * (W - L - R)
Y = lambda v: T + (6 - v) / 7 * (H - T - B)
g = []
for v in range(-1, 7):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE if v else BASE}"></line>')
    g.append(t(L - 8, Y(v) + 4.5, f"{v}%" if v == 6 else str(v), 12.5, MUTED, "end"))
for v in range(0, 7):
    g.append(t(X(v), H - B + 20, str(v), 12.5, MUTED, "middle"))
g.append(t(X(0), H - 8, "← less digitised", 12.5, MUTED))
g.append(t(W - R, H - 8, "more digitised →", 12.5, MUTED, "end"))
g.append(f'<line x1="{X(1):.1f}" y1="{Y(0.25):.1f}" x2="{X(6):.1f}" y2="{Y(3.5):.1f}" stroke="{EU}" stroke-width="1.5" stroke-dasharray="5 4"></line>')
g.append(t(X(4.3), Y(4.6), "~70% correlation", 13, INK, "middle", 600))
for n, x, y, dx, dy, an in pts:
    g.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="5" fill="{US}"></circle>')
    g.append(t(X(x) + dx, Y(y) + dy, n, 11.5, MUTED, an))
charts["mckinsey_digital"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="US sectors: labour productivity growth 1989-2019 against the '
                              f'McKinsey Global Institute digitisation index (2015); more digitised sectors grew faster, correlation about 70%. '
                              f'Information is highest (index 6, 5.1% a year); construction lowest (index 1, -0.2%)">' + "".join(g) + "</svg>")

json.dump(charts, open("site/why_charts.json", "w"), ensure_ascii=False)
print({k: len(v) for k, v in charts.items()})
