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

# 6. Andrew McAfee (MIT): public from-scratch companies under 50 years old with $10bn+ market cap, US vs EU (26 Nov 2024).
# Totals only, as printed on his chart; circle AREA proportional to total market cap.
import math
us_n, us_v, eu_n, eu_v = 241, 29.57, 14, 0.43
W, H = 600, 420
R = 168
rad = lambda v: R * math.sqrt(v / us_v)
cx_us, cy = 178, 200
g = [f'<circle cx="{cx_us}" cy="{cy}" r="{R}" fill="{US}"></circle>',
     t(cx_us, cy - 16, "US", 30, "#FAF9F5", "middle", 600),
     t(cx_us, cy + 18, f"{us_n} companies", 18, "#FAF9F5", "middle"),
     t(cx_us, cy + 44, f"${us_v:.2f} trillion", 18, "#FAF9F5", "middle", 600)]
cx_eu = 400; r_eu = rad(eu_v)
g += [f'<circle cx="{cx_eu}" cy="{cy - 30}" r="{r_eu:.1f}" fill="{EU}"></circle>',
      t(cx_eu + r_eu + 12, cy - 40, "EU", 26, INK, "start", 600),
      t(cx_eu + r_eu + 12, cy - 16, f"{eu_n} companies", 16, INK2),
      t(cx_eu + r_eu + 12, cy + 6, f"${eu_v:.2f} trillion", 16, INK2, "start", 600)]
g.append(t(cx_eu - r_eu, cy + 52, f"US total about {us_v / eu_v:.0f}× the EU’s", 16, INK, "start", 600))
kx, kb = 545, 398   # scale key, circles sit on a common baseline
for v in (1, 0.1):
    r = rad(v)
    g.append(f'<circle cx="{kx}" cy="{kb - r:.1f}" r="{r:.1f}" fill="none" stroke="{BASE}" stroke-width="1.2"></circle>')
g.append(t(kx, kb - 2 * rad(1) - 6, "$1trn", 13, MUTED, "middle"))
g.append(t(kx, kb - 2 * rad(0.1) - 4, "$100bn", 11, MUTED, "middle"))
g.append(t(kx - rad(1) - 10, kb - 22, "Circle area =", 13, MUTED, "end"))
g.append(t(kx - rad(1) - 10, kb - 5, "market value", 13, MUTED, "end"))
charts["mcafee_bubbles"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Public companies founded from scratch in the last 50 years and worth '
                            f'over $10 billion: {us_n} in the US with a combined ${us_v} trillion, {eu_n} in the EU with ${eu_v} trillion. Circle areas are proportional to total market value.">'
                            + "".join(g) + "</svg>")

# 7. McAfee's EU detail: the 14 companies. Positions and radii measured from his published chart
# (data/mcafee_eu_bubbles_measured.json); values = bubble areas scaled to his stated EU total of $0.43trn.
m = json.load(open("data/mcafee_eu_bubbles_measured.json"))
tot_a = sum(v[3] ** 2 for v in m.values())
val = {n: 430 * v[3] ** 2 / tot_a for n, v in m.items()}
TECH, OTHER = EU, "#A6A3A0"
W, H, s_ = 600, 440, 1.2
x0 = min(v[0] - v[3] for v in m.values()); y0 = min(v[1] - v[3] for v in m.values())
ox, oy = 14, 34
g = [f'<rect x="{ox}" y="6" width="12" height="12" rx="2" fill="{TECH}"></rect>' + t(ox + 18, 16.5, "Tech", 13),
     f'<rect x="{ox + 70}" y="6" width="12" height="12" rx="2" fill="{OTHER}"></rect>' + t(ox + 88, 16.5, "Other industries", 13)]
for n, (x, y, c, r) in m.items():
    cx, cy, rr = ox + (x - x0) * s_, oy + (y - y0) * s_, r * s_
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr - 0.8:.1f}" fill="{TECH if c == "g" else OTHER}" stroke="#FAF9F5" stroke-width="1.6"></circle>')
    words = n.split(" ") if (len(n) > 8 and " " in n) else [n]
    fs = 13 if rr > 34 else 11 if rr > 26 else 9.5
    for k, w_ in enumerate(words):
        g.append(t(cx, cy + 4 + (k - (len(words) - 1) / 2) * (fs + 1), w_, fs, INK if c == "g" else INK, "middle", 600 if rr > 34 else 500))
# ranked list
lx = 370; ly = 46
g.append(t(lx, ly - 18, "Approx. market value, $bn", 12.5, MUTED))
for k, (n, v) in enumerate(sorted(val.items(), key=lambda kv: -kv[1])):
    yy = ly + k * 26
    c = m[n][2]
    g.append(f'<rect x="{lx}" y="{yy - 10}" width="10" height="10" rx="2" fill="{TECH if c == "g" else OTHER}"></rect>')
    g.append(t(lx + 18, yy, n, 14, INK2))
    g.append(t(lx + 210, yy, f"{v:.0f}", 14, INK, "end", 600))
tech_v = sum(v for n, v in val.items() if m[n][2] == "g")
g.append(t(lx, ly + 14 * 26 + 6, f"Tech firms: about ${tech_v:.0f}bn", 13, INK, "start", 600))
g.append(t(lx, ly + 14 * 26 + 24, "of the $430bn total", 13, MUTED))
charts["mcafee_eu14"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="The 14 EU companies founded from scratch in the last 50 years and worth over $10 billion, '
                         f'with approximate market values: ' + "; ".join(f"{n} about ${v:.0f}bn" for n, v in sorted(val.items(), key=lambda kv: -kv[1])) + '">' + "".join(g) + "</svg>")

# 8. Full recreation: US and EU at the same scale (positions/radii measured from McAfee's chart), plus an enlarged EU inset.
usb = json.load(open("data/mcafee_us_bubbles_measured.json"))["us"]
eus = json.load(open("data/mcafee_eu_small_measured.json"))["eu_small"]
eub = json.load(open("data/mcafee_eu_bubbles_measured.json"))
TECH, OTHER = EU, "#A6A3A0"
W, H = 1200, 760
ux0 = min(o["x"] - o["r"] for o in usb); uy0 = min(o["y"] - o["r"] for o in usb)
OX, OY = 20, 34
P = lambda x, y: (OX + (x - ux0), OY + (y - uy0))
g = [f'<rect x="{OX}" y="4" width="13" height="13" rx="2" fill="{TECH}"></rect>' + t(OX + 20, 15.5, "Tech", 14),
     f'<rect x="{OX + 74}" y="4" width="13" height="13" rx="2" fill="{OTHER}"></rect>' + t(OX + 94, 15.5, "Other industries", 14)]
def bub(cx, cy, r, c, title):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{max(r - 0.6, 0.8):.1f}" fill="{TECH if c == "g" else OTHER}" stroke="#FAF9F5" stroke-width="1.1"><title>{title}</title></circle>'
for o in sorted(usb, key=lambda o: o["r"]):
    cx, cy = P(o["x"], o["y"])
    nm = o.get("name")
    g.append(bub(cx, cy, o["r"], o["c"], (nm + ": " if nm else "") + f"about ${o['v']:,.0f}bn"))
for o in usb:
    nm = o.get("name")
    if not nm: continue
    cx, cy = P(o["x"], o["y"]); r = o["r"]
    if r >= 50:
        g.append(t(cx, cy - 2, nm.replace(" (Google)", ""), 17, INK, "middle", 600))
        g.append(t(cx, cy + 18, f"${o['v'] / 1000:.1f}trn", 14, INK2, "middle"))
    elif r >= 24:
        g.append(t(cx, cy + 4, nm.replace(" Holdings", "").replace(" Sciences", ""), 11.5 if len(nm) < 11 else 9.5, INK, "middle", 500))
# EU cluster at the same scale
ex0 = min(o["x"] for o in eus); ey0 = min(o["y"] for o in eus)
EX, EY = 735, 330
for o in sorted(eus, key=lambda o: o["r"]):
    g.append(bub(EX + (o["x"] - ex0), EY + (o["y"] - ey0), o["r"], o["c"], "EU company"))
# totals
g.append(t(560, 690, "US", 26, INK, "start", 600))
g.append(t(560, 714, "241 companies, $29.6 trillion", 16, INK2))
g.append(t(EX - 6, EY + 100, "EU", 24, INK, "start", 600))
g.append(t(EX - 6, EY + 122, "14 companies,", 14, INK2))
g.append(t(EX - 6, EY + 140, "$0.43 trillion", 14, INK2))
# enlarged EU inset (x3.8 relative to the main scale)
IX, IY, s_ = 880, 300, 1.0
ix0 = min(v[0] - v[3] for v in eub.values()); iy0 = min(v[1] - v[3] for v in eub.values())
iw = max(v[0] + v[3] for v in eub.values()) - ix0; ih = max(v[1] + v[3] for v in eub.values()) - iy0
g.append(f'<rect x="{IX - 18}" y="{IY - 40}" width="{iw + 36}" height="{ih + 58}" rx="10" fill="#FFFFFF" stroke="{LINE}"></rect>')
g.append(t(IX - 4, IY - 18, "The EU's 14, enlarged ×3.8", 13, MUTED, "start", 600))
g.append(f'<line x1="{EX + 70}" y1="{EY + 40}" x2="{IX - 18}" y2="{IY + ih / 2}" stroke="{BASE}" stroke-dasharray="3 4"></line>')
m_tot = sum(v[3] ** 2 for v in eub.values())
for n, (x, y, c, r) in eub.items():
    cx, cy = IX + (x - ix0), IY + (y - iy0)
    g.append(bub(cx, cy, r, c, f"{n}: about ${430 * r * r / m_tot:,.0f}bn"))
    words = n.split(" ") if (len(n) > 8 and " " in n) else [n]
    fs = 11.5 if r > 34 else 10 if r > 26 else 8.5
    for k, w_ in enumerate(words):
        g.append(t(cx, cy + 4 + (k - (len(words) - 1) / 2) * (fs + 1), w_, fs, INK, "middle", 600 if r > 34 else 500))
# scale key (main scale): area of $1trn and $100bn
import math as _m
k1 = _m.sqrt(1000 / (29570 / sum(o["r"] ** 2 for o in usb)))
kx, kb = 1135, 735
for v_, lab in ((1000, "$1trn"), (100, "$100bn")):
    r = _m.sqrt(v_ / (29570 / sum(o["r"] ** 2 for o in usb)))
    g.append(f'<circle cx="{kx}" cy="{kb - r:.1f}" r="{r:.1f}" fill="none" stroke="{BASE}" stroke-width="1.2"></circle>')
g.append(t(kx, kb - 2 * k1 - 6, "$1trn", 12.5, MUTED, "middle"))
g.append(t(kx, kb - 2 * _m.sqrt(100 / (29570 / sum(o["r"] ** 2 for o in usb))) - 4, "$100bn", 10.5, MUTED, "middle"))
g.append(t(kx - k1 - 10, kb - 20, "Circle area =", 12.5, MUTED, "end"))
g.append(t(kx - k1 - 10, kb - 4, "market value", 12.5, MUTED, "end"))
charts["mcafee_full"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Public companies founded from scratch in the last 50 years and worth over $10 billion, '
                         f'one bubble per company sized by market value: 241 in the US worth $29.6 trillion, led by Apple, Nvidia, Microsoft, Amazon and Alphabet; '
                         f'14 in the EU worth $0.43 trillion, led by Spotify.">' + "".join(g) + "</svg>")

json.dump(charts, open("site/why_charts.json", "w"), ensure_ascii=False)
print({k: len(v) for k, v in charts.items()})
