"""Inline-SVG redraws of three external charts for the 'Why it matters' page (Draghi, Gordon & Sayed, McKinsey).
Writes site/why_charts.json. Values are as published; McKinsey points are read off the published chart. Run from research/digital_rulebook."""
import json, math

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
     ]
HL = {"ICT-using services", "ICT-producing goods"}   # highlighted rows; the rest are drawn pale
for i, (lab, e, u) in enumerate(data):
    y = 34 + i * rh
    hl = lab in HL
    if hl:
        g.append(f'<rect x="4" y="{y - 2}" width="{W - 8}" height="{rh - 8}" rx="6" fill="#F5F5F0"></rect>')
    g.append(t(L - 12, y + 25, lab, 13.5, INK if hl else MUTED, "end", 600 if hl else None))
    op = 1 if hl else 0.32
    for j, (v, c) in enumerate(((e, EU), (u, US))):
        yy = y + 6 + j * 20
        x0, w = (X(v), Z - X(v)) if v < 0 else (Z, X(v) - Z)
        g.append(f'<rect x="{x0:.1f}" y="{yy}" width="{max(w, 1.5):.1f}" height="16" fill="{c}" fill-opacity="{op}"></rect>')
        lx, an = (x0 - 6, "end") if v < 0 else (x0 + max(w, 1.5) + 6, "start")
        g.append(t(lx, yy + 12.5, f"{v:+.2f}".replace("+0", "+0").replace("-", "−"), 12.5, INK if hl else MUTED, an, 600 if hl else 400))
g.append(f'<line x1="{Z}" x2="{Z}" y1="30" y2="{H - 4}" stroke="{INK2}"></line>')
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

# 4. What firms say: regulation as a brake on business and on AI, six surveys, one compact chart (0-100%)
rows = [("German firms: data-protection rules are the biggest brake on digitalisation", 77, None, "Bitkom"),
        ("EU firms: regulation limits their investment", 69, None, "EIB Investment Survey 2025"),
        ("EU SMEs: administrative burden is a persistent challenge", 64, None, "Flash Eurobarometer, July 2025"),
        ("EU firms weighing AI: unclear legal consequences held them back", 53.61, 52.52, "Eurostat 2025"),
        ("EU firms weighing AI: data-protection concerns held them back", 52.72, None, "Eurostat 2025"),
        ("Spanish companies: compliance is the main obstacle to innovation", 46, None, "Deloitte, Spain"),
        ("EU SMEs: more than 10% of staff work on compliance", 28, None, "Single Market &amp; Competitiveness Report")]
W, BW, rh = 560, 300, 40
X = lambda v: v / 100 * BW
g = []
y = 4
for lab, v, prev, src in rows:
    g.append(t(0, y + 11, lab, 12.5, INK2))
    g.append(f'<rect x="0" y="{y + 17}" width="{BW}" height="12" fill="{LINE}" fill-opacity="0.6"></rect>')
    g.append(f'<rect x="0" y="{y + 17}" width="{X(v):.1f}" height="12" fill="{EU}"><title>{lab}: {v:.0f}%</title></rect>')
    g.append(t(X(v) + 7, y + 28, f"{v:.0f}%", 12.5, INK, weight=600))
    if prev:
        g.append(f'<line x1="{X(prev):.1f}" x2="{X(prev):.1f}" y1="{y + 14}" y2="{y + 32}" stroke="{INK}" stroke-width="2"></line>')
        src = f"{src} · line: 2024 ({prev:.0f}%)"
    g.append(t(X(v) + 42, y + 28, src, 11, MUTED))
    y += rh
H = y + 4
charts["firm_barriers"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Regulation as a brake on business and on AI, seven surveys: '
                           + "; ".join(f"{lab} {v:.0f}% ({src})" for lab, v, p_, src in rows).replace("&amp;", "and") + '">' + "".join(g) + "</svg>")

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
W, H = 1200, 830
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
        g.append(t(cx, cy + 6, nm.replace(" (Google)", ""), 17, INK, "middle", 600))
    elif r >= 24:
        g.append(t(cx, cy + 4, nm.replace(" Holdings", "").replace(" Sciences", ""), 11.5 if len(nm) < 11 else 9.5, INK, "middle", 500))
# Not yet public (dashed): sized at the midpoint of reported valuation ranges, same scale; not in the US count or total
kk = 29570 / sum(o["r"] ** 2 for o in usb)
for nm, v, cx, cy in (("Anthropic", 1750, 738, 128), ("OpenAI", 1325, 882, 150)):
    r = math.sqrt(v / kk)
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{TECH}" fill-opacity="0.10" stroke="{TECH}" stroke-width="2" stroke-dasharray="6 5">'
             f'<title>{nm}: private company, not yet listed</title></circle>')
    g.append(t(cx, cy + 2, nm, 15, INK, "middle", 600))
    g.append(t(cx, cy + 20, "not yet public", 11.5, MUTED, "middle"))
g.append(t(668, 40, "Not yet public, at private valuations", 13, MUTED, "start", 600))
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
IX, IY, s_ = 880, 272, 1.0
ix0 = min(v[0] - v[3] for v in eub.values()); iy0 = min(v[1] - v[3] for v in eub.values())
iw = max(v[0] + v[3] for v in eub.values()) - ix0; ih = max(v[1] + v[3] for v in eub.values()) - iy0
g.append(f'<rect x="{IX - 18}" y="{IY - 40}" width="{iw + 36}" height="{ih + 140}" rx="10" fill="#FFFFFF" stroke="{LINE}"></rect>')
g.append(t(IX - 4, IY - 18, "The EU's 14, enlarged ×3.8", 13, MUTED, "start", 600))
g.append(f'<line x1="{EX + 66}" y1="{EY + 26}" x2="{IX - 18}" y2="{IY + ih / 2}" stroke="{BASE}" stroke-dasharray="3 4"></line>')
m_tot = sum(v[3] ** 2 for v in eub.values())
for n, (x, y, c, r) in eub.items():
    cx, cy = IX + (x - ix0), IY + (y - iy0)
    g.append(bub(cx, cy, r, c, f"{n}: about ${430 * r * r / m_tot:,.0f}bn"))
    words = n.split(" ") if (len(n) > 8 and " " in n) else [n]
    fs = 11.5 if r > 34 else 10 if r > 26 else 8.5
    for k, w_ in enumerate(words):
        g.append(t(cx, cy + 4 + (k - (len(words) - 1) / 2) * (fs + 1), w_, fs, INK, "middle", 600 if r > 34 else 500))
# EU companies not yet public (dashed), inset scale; valuations from latest funding rounds (Mistral EUR 21bn ~ $24bn)
eu_priv = (("Mistral AI", 24), ("Helsing", 18), ("Trade Republic", 14))
py_ = IY + ih + 62
g.append(f'<line x1="{IX - 4}" x2="{IX + iw + 4}" y1="{IY + ih + 10}" y2="{IY + ih + 10}" stroke="{LINE}"></line>')
g.append(t(IX - 4, IY + ih + 28, "Not yet public, at private valuations", 11.5, MUTED, "start", 600))
for (n, v), cx in zip(eu_priv, (IX + 40, IX + 128, IX + 214)):
    r = math.sqrt(v * m_tot / 430)
    g.append(f'<circle cx="{cx}" cy="{py_}" r="{r:.1f}" fill="{TECH}" fill-opacity="0.10" stroke="{TECH}" stroke-width="1.6" stroke-dasharray="5 4">'
             f'<title>{n}: private company, not yet listed</title></circle>')
    words = n.split(" ")
    for k, w_ in enumerate(words):
        g.append(t(cx, py_ + 4 + (k - (len(words) - 1) / 2) * 11, w_, 10, INK, "middle", 500))
# same companies at the main scale, beside the EU cluster
for (n, v), dx in zip(eu_priv, (0, 19, 36)):
    r = math.sqrt(v / kk)
    g.append(f'<circle cx="{EX + 88 + dx}" cy="{EY + 68}" r="{r:.1f}" fill="{TECH}" fill-opacity="0.10" stroke="{TECH}" stroke-width="1.1" stroke-dasharray="2.5 2"><title>{n}: private company, not yet listed</title></circle>')
# scale key (main scale): area of $1trn and $100bn
import math as _m
k1 = _m.sqrt(1000 / (29570 / sum(o["r"] ** 2 for o in usb)))
kx, kb = 1100, 822
for v_, lab in ((1000, "$1trn"), (100, "$100bn")):
    r = _m.sqrt(v_ / (29570 / sum(o["r"] ** 2 for o in usb)))
    g.append(f'<circle cx="{kx}" cy="{kb - r:.1f}" r="{r:.1f}" fill="none" stroke="{BASE}" stroke-width="1.2"></circle>')
g.append(t(kx, kb - 2 * k1 - 6, "$1trn", 12.5, MUTED, "middle"))
g.append(t(kx, kb - 2 * _m.sqrt(100 / (29570 / sum(o["r"] ** 2 for o in usb))) - 4, "$100bn", 10.5, MUTED, "middle"))
g.append(t(kx - k1 - 10, kb - 20, "Circle area =", 12.5, MUTED, "end"))
g.append(t(kx - k1 - 10, kb - 4, "market value", 12.5, MUTED, "end"))
charts["mcafee_full"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Public companies founded from scratch in the last 50 years and worth over $10 billion, '
                         f'one bubble per company sized by market value: 241 in the US worth $29.6 trillion, led by Apple, Nvidia, Microsoft, Amazon and Alphabet; '
                         f'14 in the EU worth $0.43 trillion, led by Spotify. Dashed: private companies not yet listed (Anthropic, OpenAI; in the EU Mistral AI, Helsing, Trade Republic).">' + "".join(g) + "</svg>")

# 9. Reichardt & Reis (2026), Figure 1: HQ migration rates of firms under ten years old, 2014-2024, by total funding raised.
# Values measured from the published bar chart (vector PDF rendered at 400 dpi); averages are the paper's dashed lines.
hq = [("None", 1.9, 0.7), ("Under $1m", 2.9, 1.0), ("$1–10m", 6.5, 0.8), ("$10–100m", 9.9, 0.8), ("Over $100m", 10.7, 0.8)]
avg_eu, avg_us = 3.3, 0.8
W, H, L, R, TOP, BOT = 560, 400, 44, 6, 74, 340
ymax = 12
Yh = lambda v: BOT - v / ymax * (BOT - TOP)
slot = (W - L - R) / len(hq); bw = 34
g = [f'<rect x="0" y="4" width="12" height="12" rx="2" fill="{EU}"></rect>' + t(18, 14.5, f"Europe to US (average {avg_eu:.1f}%)", 13),
     f'<rect x="0" y="26" width="12" height="12" rx="2" fill="{US}"></rect>' + t(18, 36.5, f"US to Europe (average {avg_us:.1f}%)", 13),
     f'<line x1="250" x2="276" y1="10" y2="10" stroke="{MUTED}" stroke-width="1.3" stroke-dasharray="5 4"></line>' + t(282, 14.5, "average across all firms", 12.5, MUTED)]
for v in range(0, ymax + 1, 2):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Yh(v):.1f}" y2="{Yh(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>')
    g.append(t(L - 8, Yh(v) + 4.5, f"{v}%", 12, MUTED, "end"))
for val, c in ((avg_eu, EU), (avg_us, US)):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Yh(val):.1f}" y2="{Yh(val):.1f}" stroke="{c}" stroke-width="1.3" stroke-dasharray="5 4"></line>')
for i, (lab, e, u) in enumerate(hq):
    x = L + i * slot + slot / 2
    for val, c, dx in ((e, EU, -bw - 2), (u, US, 2)):
        g.append(f'<rect x="{x + dx:.1f}" y="{Yh(val):.1f}" width="{bw}" height="{BOT - Yh(val):.1f}" fill="{c}"><title>{lab}: {val:.1f}%</title></rect>')
        g.append(t(x + dx + bw / 2, Yh(val) - 7, f"{val:.1f}%", 12.5 if c == EU else 11.5, INK if c == EU else INK2, "middle", 600 if c == EU else None)
                 .replace("<text ", '<text stroke="#F3F1EC" stroke-width="4" paint-order="stroke" ', 1))
    g.append(t(x, BOT + 22, lab, 12.5, INK2, "middle"))
g.append(t(L + (W - L - R) / 2, BOT + 48, "Total external funding raised by 2024", 12.5, MUTED, "middle"))
charts["hq_migration"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Share of firms under ten years old that moved their headquarters between 2014 and 2024, '
                          f'by funding raised. Europe to US: no funding 1.9%, under $1m 2.9%, $1-10m 6.5%, $10-100m 9.9%, over $100m 10.7% (average 3.3%). '
                          f'US to Europe: 0.7%, 1.0%, 0.8%, 0.8%, 0.8% (average 0.8%).">' + "".join(g) + "</svg>")

# 10. GDP-per-head gap, euro area vs US, split into output per hour and hours worked (built in build_gap_options.py, option B)
charts["gap_split"] = json.load(open("site/gap_options.json"))["B"]


# OECD (Andrews, Turban and Tyros 2026, Figure 4 A; Economic Outlook 2025/2, Figure 2.4 B): share of employment devoted to regulatory tasks
_O = json.load(open("data/external/oecd_regulation_index.json"))
_A = _O["panel_A_2023"]; _P = _O["panel_A_eu_points_2023"]["values"]; _PU = _O["panel_A_us_points_2023"]["values"]; _B = _O["panel_B_eu"]
W, H = 1000, 440
g = []
# panel A: EU countries as dots over a box plot; US states as a box plot, 2023
ax0, ax1, top, bot, lo, hi = 70, 400, 56, 380, 2.5, 6.0
Y = lambda v: bot - (v - lo) / (hi - lo) * (bot - top)
g.append(t(0, 18, "A. Share of employment spent on regulatory tasks, 2023", 14, INK, weight=600))
g.append(t(0, 38, "Each dot is one EU country or US state; %", 12.5, MUTED))
for v in (2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0):
    g.append(f'<line x1="{ax0}" x2="{ax1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"></line>' + t(ax0 - 8, Y(v) + 4, f"{v:.1f}", 12, MUTED, "end"))
for i, (key, lab, c) in enumerate((("EU countries", "EU countries", EU), ("US states and territories", "US states", US))):
    a = _A[key]; cx = ax0 + 95 + i * 160; bw = 70
    top_w = a["max"]
    g.append(f'<line x1="{cx}" x2="{cx}" y1="{Y(top_w):.1f}" y2="{Y(a["min"]):.1f}" stroke="{INK2}" stroke-width="1.5"></line>')
    for v in (a["min"], top_w):
        g.append(f'<line x1="{cx - 12}" x2="{cx + 12}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{INK2}" stroke-width="1.5"></line>')
    g.append(f'<rect x="{cx - bw / 2}" y="{Y(a["q3"]):.1f}" width="{bw}" height="{Y(a["q1"]) - Y(a["q3"]):.1f}" fill="#FFFFFF" fill-opacity="0.6" stroke="{c}" stroke-width="1.5"><title>{lab}: middle half {a["q1"]:.1f}–{a["q3"]:.1f}%, median {a["median"]:.1f}%</title></rect>')
    g.append(f'<line x1="{cx - bw / 2}" x2="{cx + bw / 2}" y1="{Y(a["median"]):.1f}" y2="{Y(a["median"]):.1f}" stroke="{INK}" stroke-width="3"></line>')
    g.append(t(cx + bw / 2 + 8, Y(a["median"]) + 4, f'{a["median"]:.1f}%', 13, INK, weight=600))
    who = "One EU country" if i == 0 else "One US state"
    for k, v in enumerate(_P if i == 0 else _PU):   # deterministic jitter, as in the paper
        dx = ((k * 37) % 11 - 5) * 4.2
        g.append(f'<circle cx="{cx + dx:.1f}" cy="{Y(v):.1f}" r="{5 if i == 0 else 4}" fill="{c}" fill-opacity="0.7" stroke="#FFFFFF" stroke-width="0.8"><title>{who}: {v:.1f}%</title></circle>')
    g.append(t(cx, bot + 24, lab, 13.5, INK, "middle", 600))
g.append(t(ax0, bot + 50, "Box: middle half; line: median; whiskers: range", 12, MUTED))
# panel B: EU countries over time, mean, median and middle half
bx0, bx1, lo, hi = 520, 965, 3.4, 4.2
yrs = [r["year"] for r in _B]; y0, y1 = min(yrs), max(yrs)
X = lambda yr: bx0 + (yr - y0) / (y1 - y0) * (bx1 - bx0)
Y = lambda v: bot - (v - lo) / (hi - lo) * (bot - top)
g.append(t(bx0 - 40, 18, f"B. EU countries, {y0}–{y1}", 14, INK, weight=600))
g.append(t(bx0 - 40, 38, "Share of employment spent on regulatory tasks; %", 12.5, MUTED))
for v in (3.4, 3.6, 3.8, 4.0, 4.2):
    g.append(f'<line x1="{bx0}" x2="{bx1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"></line>' + t(bx0 - 8, Y(v) + 4, f"{v:.1f}", 12, MUTED, "end"))
for yr in range(y0, y1 + 1, 2):
    g.append(t(X(yr), bot + 20, str(yr), 12, MUTED, "middle"))
pts = [(X(r["year"]), Y(r["q3"])) for r in _B] + [(X(r["year"]), Y(r["q1"])) for r in reversed(_B)]
g.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{EU}" fill-opacity="0.15"><title>Middle half of EU countries</title></polygon>')
g.append('<polyline points="' + " ".join(f'{X(r["year"]):.1f},{Y(r["median"]):.1f}' for r in _B) + f'" fill="none" stroke="{INK2}" stroke-width="2" stroke-dasharray="3 4"></polyline>')
g.append('<polyline points="' + " ".join(f'{X(r["year"]):.1f},{Y(r["mean"]):.1f}' for r in _B) + f'" fill="none" stroke="{EU}" stroke-width="3"></polyline>')
for r in (_B[0], _B[-1]):
    g.append(f'<circle cx="{X(r["year"]):.1f}" cy="{Y(r["mean"]):.1f}" r="4" fill="{EU}"><title>Mean {r["year"]}: {r["mean"]:.1f}%</title></circle>')
g.append(t(X(_B[0]["year"]) + 4, Y(_B[0]["mean"]) - 12, f'{_B[0]["mean"]:.1f}%', 12.5, INK2))
g.append(t(X(_B[-1]["year"]) - 4, Y(_B[-1]["mean"]) - 14, f'{_B[-1]["mean"]:.1f}%', 13, INK, "end", 600))
ly = bot + 42
g.append(f'<line x1="{bx0}" x2="{bx0 + 22}" y1="{ly}" y2="{ly}" stroke="{EU}" stroke-width="3"></line>' + t(bx0 + 28, ly + 4, "Mean", 12, INK2))
g.append(f'<line x1="{bx0 + 80}" x2="{bx0 + 102}" y1="{ly}" y2="{ly}" stroke="{INK2}" stroke-width="2" stroke-dasharray="3 4"></line>' + t(bx0 + 108, ly + 4, "Median", 12, INK2))
g.append(f'<rect x="{bx0 + 170}" y="{ly - 5}" width="16" height="10" fill="{EU}" fill-opacity="0.15"></rect>' + t(bx0 + 192, ly + 4, "Middle half of countries", 12, INK2))
charts["oecd_regulation"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Share of employment spent on regulatory tasks. 2023: median '
    f'{_A["EU countries"]["median"]:.1f}% across {len(_P)} EU countries, ranging from {min(_P):.1f}% to {max(_P):.1f}%, against {_A["US states and territories"]["median"]:.1f}% across {len(_PU)} US states and territories, ranging from {min(_PU):.1f}% to {max(_PU):.1f}%. '
    f'EU countries, {y0}–{y1}: mean from {_B[0]["mean"]:.1f}% to {_B[-1]["mean"]:.1f}%">' + "".join(g) + "</svg>")


# OECD (Andrews, Turban and Tyros 2026, Figure 7): impulse responses to an average-sized yearly increase in regulatory costs, US states
_R = json.load(open("data/external/oecd_regulation_irf.json"))
W, H = 1000, 425
g = []
top, bot = 60, 330
for pi, (key, head, sub, lo, hi, step, unit) in enumerate((
        ("productivity_pct", "A. Output per worker", "% relative to no increase", -0.5, 0.3, 0.1, "%"),
        ("young_firms_pp", "B. Share of workers in young firms", "Percentage points relative to no increase", -0.35, 0.1, 0.05, ""))):
    x0 = 60 + pi * 510; x1 = x0 + 420
    rows = _R[key]
    X = lambda yr: x0 + yr / 5 * (x1 - x0)
    Y = lambda v: bot - (v - lo) / (hi - lo) * (bot - top)
    g.append(t(x0 - 50, 18, head, 14, INK, weight=600)); g.append(t(x0 - 50, 38, sub, 12.5, MUTED))
    k = 0
    while lo + k * step <= hi + 1e-9:
        v = round(lo + k * step, 2); k += 1
        g.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if abs(v) < 1e-9 else LINE}" stroke-width="{1.5 if abs(v) < 1e-9 else 1}"></line>')
        g.append(t(x0 - 8, Y(v) + 4, (f"{v:.1f}{unit}" if pi == 0 else f"{v:.2f}").replace("-", "−"), 12, MUTED, "end"))
    for lohi, op, lab in (("ci90", 0.16, "90%"), ("ci68", 0.30, "68%")):
        pts = [(X(r["year"]), Y(r[lohi][1])) for r in rows] + [(X(r["year"]), Y(r[lohi][0])) for r in reversed(rows)]
        g.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{EU}" fill-opacity="{op}"><title>{lab} confidence interval</title></polygon>')
    g.append('<polyline points="' + " ".join(f'{X(r["year"]):.1f},{Y(r["est"]):.1f}' for r in rows) + f'" fill="none" stroke="{EU}" stroke-width="3"></polyline>')
    for r in rows:
        g.append(f'<circle cx="{X(r["year"]):.1f}" cy="{Y(r["est"]):.1f}" r="3.5" fill="{EU}"><title>Year {r["year"]}: {r["est"]:.2f}{unit or " points"}</title></circle>')
        g.append(t(X(r["year"]), bot + 20, str(r["year"]), 12, MUTED, "middle"))
    e = rows[-1]["est"]
    g.append(t(X(5) - 6, Y(e) + 20, (f"{e:.2f}{unit}" if pi == 0 else f"{e:.2f} points").replace("-", "−"), 13, INK, "end", 600))
    g.append(t((x0 + x1) / 2, bot + 42, "Years after the increase", 12.5, INK2, "middle"))
ly = H - 14
g.append(f'<line x1="10" x2="32" y1="{ly - 4}" y2="{ly - 4}" stroke="{EU}" stroke-width="3"></line>' + t(38, ly, "Estimate", 12, INK2))
g.append(f'<rect x="110" y="{ly - 10}" width="16" height="11" fill="{EU}" fill-opacity="0.46"></rect>' + t(132, ly, "68% confidence", 12, INK2))
g.append(f'<rect x="240" y="{ly - 10}" width="16" height="11" fill="{EU}" fill-opacity="0.16"></rect>' + t(262, ly, "90% confidence", 12, INK2))
pr, yf = _R["productivity_pct"][-1]["est"], _R["young_firms_pp"][-1]["est"]
charts["oecd_regulation_irf"] = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Effect of an average-sized yearly increase in regulatory compliance costs across US states: '
    f'after five years output per worker is about {abs(pr):.2f}% lower and the share of workers in young firms about {abs(yf):.2f} percentage points lower than without the increase">' + "".join(g) + "</svg>")

json.dump(charts, open("site/why_charts.json", "w"), ensure_ascii=False)
print({k: len(v) for k, v in charts.items()})
