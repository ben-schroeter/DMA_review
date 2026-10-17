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
W, H, L = 560, 430, 130
eu_len, us_len = 250, 370          # schematic: only the 72/28 split of the gap is to scale
gap = us_len - eu_len
p_len = 0.72 * gap
rows = [("EU-27", L, eu_len, EU, None), ("Productivity|GDP per hour", L + eu_len, p_len, "#D9BE7A", "~72%"),
        ("Labour|hours per head", L + eu_len + p_len, gap - p_len, "#E3CF9C", "~28%"), ("US", L, us_len, US, None)]
g = [f'<line x1="{L}" x2="{L}" y1="10" y2="{H - 20}" stroke="{BASE}"></line>']
for i, (lab, x0, w, c, pct) in enumerate(rows):
    y = 22 + i * 100
    if "|" in lab:
        a, b = lab.split("|"); g.append(t(L - 12, y + 24, a, 14, INK2, "end")); g.append(t(L - 12, y + 41, b, 12.5, MUTED, "end"))
    else:
        g.append(t(L - 12, y + 32, lab, 14, INK, "end", 600))
    g.append(f'<rect x="{x0:.1f}" y="{y}" width="{w:.1f}" height="52" fill="{c}"></rect>')
    if pct:
        g.append(t(x0 + w / 2, y + 32, pct, 15, INK, "middle", 600) if w > 50 else t(x0 + w + 8, y + 32, pct, 15, INK, "start", 600))
        g.append(f'<line x1="{x0:.1f}" x2="{x0:.1f}" y1="{y - 48}" y2="{y}" stroke="{BASE}" stroke-dasharray="2 3"></line>')
g.append(f'<line x1="{L + us_len:.1f}" x2="{L + us_len:.1f}" y1="{22 + 2 * 100 + 52}" y2="{22 + 3 * 100}" stroke="{BASE}" stroke-dasharray="2 3"></line>')
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

# 4. Eurostat ICT usage in enterprises survey, 2025: barriers among EU firms (10+ employees) that considered using AI
STONE = "#C4C1BE"
rows = [("Lack of relevant expertise", 70.31, STONE, None), ("Unclear legal consequences", 53.61, EU, 52.52),
        ("Data protection and privacy concerns", 52.72, EU, None)]
W, L, T0, rh = 560, 0, 34, 86
H = T0 + len(rows) * rh + 10
X = lambda v: L + v / 100 * (W - 70)
g = [f'<rect x="0" y="6" width="12" height="12" rx="2" fill="{EU}"></rect>' + t(18, 16.5, "Legal and regulatory", 12.5),
     f'<rect x="170" y="6" width="12" height="12" rx="2" fill="{STONE}"></rect>' + t(188, 16.5, "Other", 12.5)]
for i, (lab, v, c, prev) in enumerate(rows):
    y = T0 + i * rh
    g.append(t(0, y + 16, lab, 14, INK if c == EU else INK2, weight=600 if c == EU else None))
    g.append(f'<rect x="{L}" y="{y + 26}" width="{X(100) - L:.1f}" height="22" fill="{LINE}" fill-opacity="0.6"></rect>')
    g.append(f'<rect x="{L}" y="{y + 26}" width="{X(v) - L:.1f}" height="22" fill="{c}"></rect>')
    g.append(t(X(v) + 8, y + 42, f"{v:.1f}%", 14, INK, weight=600))
    if prev:
        g.append(f'<line x1="{X(prev):.1f}" x2="{X(prev):.1f}" y1="{y + 21}" y2="{y + 53}" stroke="{INK}" stroke-width="2"></line>')
        g.append(t(X(prev) - 6, y + 66, f"2024: {prev:.1f}%", 12, MUTED, "end"))
charts["eurostat_ai_barriers"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Barriers to using AI cited by EU enterprises with 10 or more employees '
                                  f'that had considered it, 2025: lack of relevant expertise 70.3%; unclear legal consequences 53.6% (52.5% in 2024); '
                                  f'data protection and privacy concerns 52.7%">' + "".join(g) + "</svg>")

# 5. What firms say about regulation: seven surveys, different questions (lollipop, 0-100%)
sv = [(77, "German firms: data-protection rules are the", "biggest brake on digitalisation", "Bitkom, Germany"),
      (69, "EU firms: regulation limits", "their investment", "EIB Investment Survey 2025 (France: 58%)"),
      (64, "EU SMEs: administrative burden or regulatory", "obstacles are a persistent challenge", "Flash Eurobarometer, July 2025"),
      (54, "EU firms that considered AI: unclear", "legal consequences hold them back", "Eurostat 2025"),
      (49, "Legal uncertainty is holding back", "AI adoption", "Eurobarometer 578"),
      (46, "Spanish companies: compliance is the main", "obstacle to innovation", "Deloitte, Spain"),
      (28, "EU SMEs: more than 10% of staff work on", "regulatory compliance", "Single Market &amp; Competitiveness Report")]
W, L, rh, T0 = 1000, 420, 64, 30
H = T0 + len(sv) * rh
X = lambda v: L + v / 100 * (W - L - 60)
g = []
for v in range(0, 101, 25):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{T0 - 8}" y2="{H - 6}" stroke="{LINE}"></line>')
    g.append(t(X(v), 16, f"{v}%", 12.5, MUTED, "middle"))
for i, (v, a, b, src) in enumerate(sv):
    y = T0 + i * rh
    g.append(t(0, y + 18, a, 14.5, INK2))
    g.append(t(0, y + 36, b, 14.5, INK2))
    g.append(t(0, y + 53, src, 12, MUTED))
    g.append(f'<line x1="{X(0):.1f}" x2="{X(v):.1f}" y1="{y + 28}" y2="{y + 28}" stroke="{EU}" stroke-width="3"></line>')
    g.append(f'<circle cx="{X(v):.1f}" cy="{y + 28}" r="8" fill="{EU}"></circle>')
    g.append(t(X(v) + 16, y + 33, f"{v}%", 16, INK, weight=600))
charts["firm_surveys"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Regulation as an obstacle in seven business surveys: '
                          + "; ".join(f"{a} {b} {v}% ({src})" for v, a, b, src in sv).replace("&amp;", "and") + '">' + "".join(g) + "</svg>")

json.dump(charts, open("site/why_charts.json", "w"), ensure_ascii=False)
print({k: len(v) for k, v in charts.items()})
