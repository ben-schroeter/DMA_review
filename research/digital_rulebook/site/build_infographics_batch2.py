"""Eight more square infographics (1200x1200) in the same frame as build_infographics_more.py, redrawn from the page charts:
ict_use (Why page, Gordon & Sayed), compliance_2023 and compliance_trend (Why page, OECD), firm_surveys (Why page),
design_grid (Rules vs Standards page), company_types (By type of company), firm_size (By type of company),
reporting_growth (In Numbers). Data come from the same code and files as the page charts, so the figures match.
Writes site/infographics/<name>.svg. Run from research/digital_rulebook."""
import contextlib, io, json, math, os

INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
GOLD, GOLD_D, GOLD2, STONE, SLATE, BG = "#B8860B", "#8F6708", "#E3CF9C", "#C4C1BE", "#5C5858", "#FAF9F5"
SANS = 'font-family="DM Sans, sans-serif"'
SERIF = "font-family=\"'Source Serif 4', Georgia, serif\""
W = H = 1200
esc = lambda s: str(s).replace("&", "&amp;")


def t(x, y, txt, size, fill=INK2, anchor="start", weight=400, font=SANS, halo=False):
    h = f' stroke="{BG}" stroke-width="6" paint-order="stroke"' if halo else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {font} font-size="{size}" font-weight="{weight}" fill="{fill}"{h}>{txt}</text>'


def frame(name, head, sub, notes, body, aria, source):
    g = [f'<rect width="{W}" height="{H}" fill="{BG}"></rect>', f'<rect width="{W}" height="10" fill="{GOLD}"></rect>']
    for i, line in enumerate(head):
        g.append(t(56, 112 + 60 * i, line, 50, INK, weight=700))
    y = 112 + 60 * (len(head) - 1) + 56
    for i, line in enumerate(sub):
        g.append(t(56, y + 32 * i, line, 24, MUTED))
    g += body
    g.append(f'<line x1="56" x2="{W - 56}" y1="1066" y2="1066" stroke="{LINE}"></line>')
    for i, line in enumerate(notes):
        g.append(t(56, 1100 + 24 * i, line, 16, MUTED))
    g.append(f'<g transform="translate({W - 330},1160)"><rect x="0" y="0" width="22" height="22" rx="3" fill="none" stroke="{INK}" stroke-width="1.6"></rect>'
             f'<path d="M5 15h12M5 11h12M5 7h7" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"></path></g>')
    g.append(t(W - 298, 1178, "The EU Digital Rulebook", 22, INK, font=SERIF))
    g.append(t(56, 1180, f'Source: {source} · <tspan fill="{GOLD}" font-weight="700" font-size="18">eutechlaws.org</tspan>', 16, INK2, weight=500))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(aria)}">' + "".join(g) + "</svg>"
    open(f"site/infographics/{name}.svg", "w").write(svg)
    print("wrote", name)


def callout(x, y, w, big, lines, h=120, size=58):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="{LINE}"></rect>',
           t(x + 24, y + h / 2 + size * 0.36, big, size, GOLD, weight=700, font=SERIF)]
    tx = x + 24 + size * 0.55 * len(big.replace(" ", "")) + 26
    off = (h - 26 * len(lines)) / 2 + 20
    for i, line in enumerate(lines):
        out.append(t(tx, y + off + 26 * i, line, 20, INK2))
    return out


def run(path):
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(open(path).read(), path, "exec"), ns)
    return ns


os.makedirs("site/infographics", exist_ok=True)

# 1. Gordon & Sayed: ICT use, US vs EU-10
why = run("site/build_why_charts.py")
data = why["data"]                       # (sector, EU-10, US), percentage points
L, R, Z, TOP = 360, 1144, 0, 360
S = (R - L) / 1.05
X = lambda v: L + (v + 0.4) * S
rh = 104
b = [f'<rect x="56" y="300" width="20" height="20" rx="3" fill="{GOLD}"></rect>' + t(86, 317, "EU-10", 21),
     f'<rect x="176" y="300" width="20" height="20" rx="3" fill="{SLATE}"></rect>' + t(206, 317, "United States", 21)]
for v in (-0.4, -0.2, 0, 0.2, 0.4, 0.6):
    b.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{TOP - 6}" y2="{TOP + rh * len(data)}" stroke="{BASE if v == 0 else LINE}" stroke-width="{1.8 if v == 0 else 1}"></line>')
    b.append(t(X(v), TOP + rh * len(data) + 28, f"{v:+.1f}".replace("+0.0", "0").replace("-", "−"), 18, MUTED, "middle"))
HL = {"ICT-using services", "ICT-producing goods"}
for i, (lab, e, u) in enumerate(data):
    y = TOP + i * rh
    hl = lab in HL
    if hl:
        b.append(f'<rect x="48" y="{y + 2}" width="{W - 96}" height="{rh - 8}" rx="8" fill="#FFFFFF"></rect>')
    b.append(t(L - 18, y + rh / 2 + 4, lab, 22, INK if hl else MUTED, "end", 600 if hl else 400))
    for j, (v, c) in enumerate(((e, GOLD), (u, SLATE))):
        yy = y + 18 + j * 34
        x0, w = (X(v), X(0) - X(v)) if v < 0 else (X(0), X(v) - X(0))
        b.append(f'<rect x="{x0:.1f}" y="{yy}" width="{max(w, 2):.1f}" height="28" rx="3" fill="{c}" fill-opacity="{1 if hl else 0.4}"></rect>')
        lab_x, anc = (x0 - 8, "end") if v < 0 else (x0 + w + 8, "start")
        b.append(t(lab_x, yy + 21, f"{v:+.2f}".replace("-", "−"), 19, INK if hl else MUTED, anc, 700 if hl else 400))
us_use = next(u for l, e, u in data if l == "ICT-using services"); eu_use = next(e for l, e, u in data if l == "ICT-using services")
b += callout(640, 236, 504, f"+{us_use:.2f}", ["points of extra growth from", "ICT-using services in the US"], h=104, size=50)
frame("ict_use", ["The US gained from using digital", "technology, not just from making it"],
      ["Contribution to the change in productivity growth after 1995, by sector,", "ten EU countries and the US, percentage points"],
      ["ICT-using services are retail, wholesale and finance, among others. EU-10: ten EU countries. Redrawn from R. Gordon and H. Sayed,",
       "“Transatlantic technologies: the role of ICT in the evolution of US and European productivity growth”, NBER w27425 (2020)."],
      b, f"The US gained from using digital technology, not just from making it. Contribution to the change in productivity growth after 1995: "
         + "; ".join(f"{l}: EU-10 {e:+.2f}, US {u:+.2f}" for l, e, u in data), "Gordon &amp; Sayed (2020)")

# 2 and 3. OECD: share of employment spent on regulatory tasks
O = json.load(open("data/external/oecd_regulation_index.json"))
A, P, PU, B = O["panel_A_2023"], O["panel_A_eu_points_2023"]["values"], O["panel_A_us_points_2023"]["values"], O["panel_B_eu"]
eu_m, us_m = A["EU countries"]["median"], A["US states and territories"]["median"]
TOP, BOT, lo, hi = 350, 980, 2.5, 6.0
Y = lambda v: BOT - (v - lo) / (hi - lo) * (BOT - TOP)
b = []
for v in (2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0):
    b.append(f'<line x1="140" x2="1144" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"></line>' + t(124, Y(v) + 7, f"{v:.1f}%", 19, MUTED, "end"))
for i, (key, lab, c, pts) in enumerate((("EU countries", "EU countries", GOLD, P), ("US states and territories", "US states", SLATE, PU))):
    a = A[key]; cx = 380 + i * 420; bw = 150
    b.append(f'<line x1="{cx}" x2="{cx}" y1="{Y(a["max"]):.1f}" y2="{Y(a["min"]):.1f}" stroke="{INK2}" stroke-width="2.5"></line>')
    for v in (a["min"], a["max"]):
        b.append(f'<line x1="{cx - 24}" x2="{cx + 24}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{INK2}" stroke-width="2.5"></line>')
    b.append(f'<rect x="{cx - bw / 2}" y="{Y(a["q3"]):.1f}" width="{bw}" height="{Y(a["q1"]) - Y(a["q3"]):.1f}" fill="#FFFFFF" fill-opacity="0.7" stroke="{c}" stroke-width="2.5"></rect>')
    b.append(f'<line x1="{cx - bw / 2}" x2="{cx + bw / 2}" y1="{Y(a["median"]):.1f}" y2="{Y(a["median"]):.1f}" stroke="{INK}" stroke-width="5"></line>')
    for k, v in enumerate(pts):
        dx = ((k * 37) % 11 - 5) * 9
        b.append(f'<circle cx="{cx + dx:.1f}" cy="{Y(v):.1f}" r="{10 if i == 0 else 8}" fill="{c}" fill-opacity="0.75" stroke="#FFFFFF" stroke-width="1.5"></circle>')
    b.append(t(cx + bw / 2 + 18, Y(a["median"]) + 10, f'{a["median"]:.1f}%', 30, INK, weight=700, halo=True))
    b.append(t(cx, BOT + 44, lab, 26, INK, "middle", 700))
b += callout(700, 300, 444, f"{eu_m:.1f}% v {us_m:.1f}%", ["median EU country", "vs median US state"], h=100, size=40)
frame("compliance_2023", ["Europe spends more of its workforce", "on compliance than the US"],
      ["Share of employment spent on regulatory tasks, 2023:", "each dot is one EU country or US state"],
      ["Box: middle half of countries or states; line: median; whiskers: range. EU countries: the EU except Bulgaria, Malta and Slovenia, plus",
       "Iceland, Norway and Switzerland. Dots read off the published chart; quartiles, median and range from the OECD data. Andrews, Turban",
       "and Tyros, OECD Economics Department Working Paper No. 1856 (2026), Figure 4; OECD Economic Outlook 2025/2, Figure 2.4."],
      b, f"Europe spends more of its workforce on compliance than the US: median share of employment on regulatory tasks {eu_m:.1f}% across {len(P)} EU countries and {us_m:.1f}% across {len(PU)} US states, 2023.",
      "OECD (2025, 2026)")

TOP, BOT, lo, hi = 380, 960, 3.4, 4.2
y0, y1 = B[0]["year"], B[-1]["year"]
X = lambda yr: 150 + (yr - y0) / (y1 - y0) * (1110 - 150)
Y = lambda v: BOT - (v - lo) / (hi - lo) * (BOT - TOP)
b = [f'<line x1="56" x2="96" y1="312" y2="312" stroke="{GOLD}" stroke-width="5"></line>' + t(106, 319, "Mean", 21),
     f'<line x1="190" x2="230" y1="312" y2="312" stroke="{INK2}" stroke-width="3" stroke-dasharray="5 6"></line>' + t(240, 319, "Median", 21),
     f'<rect x="346" y="302" width="26" height="20" fill="{GOLD}" fill-opacity="0.18"></rect>' + t(382, 319, "Middle half of countries", 21)]
for v in (3.4, 3.6, 3.8, 4.0, 4.2):
    b.append(f'<line x1="150" x2="1110" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"></line>' + t(132, Y(v) + 7, f"{v:.1f}%", 19, MUTED, "end"))
for yr in range(y0, y1 + 1, 2):
    b.append(t(X(yr), BOT + 34, str(yr), 19, MUTED, "middle"))
pts = [(X(r["year"]), Y(r["q3"])) for r in B] + [(X(r["year"]), Y(r["q1"])) for r in reversed(B)]
b.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{GOLD}" fill-opacity="0.18"></polygon>')
b.append('<polyline points="' + " ".join(f'{X(r["year"]):.1f},{Y(r["median"]):.1f}' for r in B) + f'" fill="none" stroke="{INK2}" stroke-width="3" stroke-dasharray="5 6"></polyline>')
b.append('<polyline points="' + " ".join(f'{X(r["year"]):.1f},{Y(r["mean"]):.1f}' for r in B) + f'" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linejoin="round"></polyline>')
for r in (B[0], B[-1]):
    b.append(f'<circle cx="{X(r["year"]):.1f}" cy="{Y(r["mean"]):.1f}" r="9" fill="{GOLD}"></circle>')
b.append(t(X(B[0]["year"]) + 6, Y(B[0]["mean"]) - 20, f'{B[0]["mean"]:.1f}%', 30, INK, weight=700, halo=True))
b.append(t(X(B[-1]["year"]) - 6, Y(B[-1]["mean"]) - 22, f'{B[-1]["mean"]:.1f}%', 30, INK, "end", 700, halo=True))
frame("compliance_trend", ["The share of Europe's workforce spent", "on compliance keeps rising"],
      ["Share of employment spent on regulatory tasks in EU countries,", f"{y0}–{y1}"],
      ["Each occupation’s share of regulatory tasks, weighted by its employment. EU countries: the EU except Bulgaria, Malta and Slovenia, plus Iceland,",
       "Norway and Switzerland (the UK until 2019). Andrews, Turban and Tyros, OECD Economics Department Working Paper No. 1856 (2026);",
       "OECD Economic Outlook 2025/2, Figure 2.4."],
      b, f"The share of Europe's workforce spent on compliance keeps rising: EU mean from {B[0]['mean']:.1f}% in {y0} to {B[-1]['mean']:.1f}% in {y1}.",
      "OECD (2025, 2026)")

# 4. what firms say: seven surveys
rows = why["SURVEYS"]                       # (label, value, source, url) from the firm_barriers chart
TOP, rh, BW = 330, 100, 700
b = []
for i, (lab, v, src, url) in enumerate(rows):
    y = TOP + i * rh
    b.append(t(56, y + 26, esc(lab).replace("&amp;amp;", "&amp;"), 23, INK, weight=500))
    b.append(f'<rect x="56" y="{y + 40}" width="{BW * v / 100:.1f}" height="30" rx="4" fill="{GOLD}"></rect>')
    vl = "~70%" if v == 69.5 else f"{v:.0f}%"
    b.append(t(56 + BW * v / 100 + 14, y + 65, vl, 30, INK, weight=700))
    b.append(t(56 + BW * v / 100 + 14 + 19 * len(vl) + 14, y + 64, src.replace("&amp;", "&amp;"), 18, MUTED))
frame("firm_surveys", ["Firms see regulation as a brake", "on business and on AI"],
      ["Findings from seven surveys of companies"],
      ["Each survey asks a different question of a different group, so the shares show a common pattern, not a ranking.",
       "Eurostat: EU firms with 10+ employees that considered using AI but did not; several answers possible. IAPP: nearly 7 in 10 businesses."],
      b, "Firms see regulation as a brake on business and on AI: " + "; ".join(f"{l} {v:.0f}% ({s})" for l, v, s, u in rows),
      "Bitkom, IAPP, EIB, Eurobarometer, Eurostat, European Commission")

# 5. regulatory design grid
G = json.load(open("data/rules_standards/grid/summary.json"))["groups"]["companies_main|all"]
CEL = {"MM": ("Prescriptive rule", "The law says what to do", "#8F6708", "#FFFFFF"), "ME": ("Performance rule", "A specific result; the firm chooses how", "#D9B86A", INK),
       "XM": ("Management-based duty", "Set up and run a system the firm designs", "#4F7FB3", "#FFFFFF"), "XE": ("General duty", "An open-ended result, judged afterwards", "#9DBBDB", INK)}
X0, Y0, CW, CH, GP = 190, 380, 470, 320, 16
b = [t(X0 + CW / 2, Y0 - 18, "Means: what to do", 24, INK, "middle", 700), t(X0 + CW + GP + CW / 2, Y0 - 18, "Ends: what to achieve", 24, INK, "middle", 700),
     t(56, Y0 + CH / 2 - 4, "Specific", 24, INK, weight=700), t(56, Y0 + CH + GP + CH / 2 - 4, "General", 24, INK, weight=700)]
for code, (cx, cy) in {"MM": (0, 0), "ME": (1, 0), "XM": (0, 1), "XE": (1, 1)}.items():
    x, y = X0 + cx * (CW + GP), Y0 + cy * (CH + GP); name, sub, col, ink = CEL[code]
    b.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="14" fill="{col}"></rect>')
    b.append(t(x + 32, y + 136, f"{G[code]:.0%}", 108, ink, weight=700, font=SERIF))
    b.append(t(x + 32, y + 200, name, 31, ink, weight=700))
    b.append(t(x + 32, y + 240, sub, 21, ink))
frame("design_grid", [f"{G['MM']:.0%} of EU obligations on companies", "say exactly what to do"],
      ["Obligations on companies in the main EU digital laws, by regulatory design"],
      [f"{G['n']:,} obligations on companies in the 105 adopted main laws, each coded by what it fixes (the means or the end) and how precisely",
       "(specific or general), following C. Coglianese’s regulatory design framework. Obligations that set no duty, leave matters to member states",
       "or are specified later are not shown. Coding by AI readers, checked against a hand-coded sample (89% agreement)."],
      b, f"{G['MM']:.0%} of EU obligations on companies say exactly what to do: prescriptive rules {G['MM']:.0%}, performance rules {G['ME']:.0%}, "
         f"management-based duties {G['XM']:.0%}, general duties {G['XE']:.0%}.", "The EU Digital Rulebook (2026)")

# 6. company types: specific obligations, 2018 and added since by policy area
c = run("site/build_company_types.py")
order, sel, NAMES, AREAS, area = c["order"], c["sel"], c["NAMES"], c["AREAS"], c["area"]
import collections
L, R, TOP, BH, GAP = 400, 1060, 400, 58, 22
XM = 4000
X = lambda v: L + v / XM * (R - L)
b, lx, ly = [], 56, 300
for k, lab, col, _ in [("_pre", "In force at the start of 2018", BG, None)] + AREAS:
    w = 34 + len(lab.replace("&amp;", "&")) * 10.4
    if lx + w > W - 56:
        lx, ly = 56, ly + 32
    stroke = f' stroke="{STONE}" stroke-width="2"' if k == "_pre" else ""
    b.append(f'<rect x="{lx}" y="{ly}" width="18" height="18" rx="3" fill="{col}"{stroke}></rect>' + t(lx + 26, ly + 15, lab, 18))
    lx += w + 14
mult = {}
for i, k in enumerate(order):
    y = TOP + i * (BH + GAP) + (18 if k == "B" else 0)
    name = NAMES[k].replace("Baseline: all companies", "Every company (baseline)")
    if k == "B":
        b.append(f'<line x1="56" x2="{W - 56}" y1="{y - 20}" y2="{y - 20}" stroke="{LINE}"></line>')
    words = name.split(" "); l1, l2 = name, ""
    if len(name) > 26:
        cut = max(i for i in range(len(words)) if len(" ".join(words[:i])) <= 26); l1, l2 = " ".join(words[:cut]), " ".join(words[cut:])
    b.append(t(L - 16, y + BH / 2 + (8 if not l2 else -4), esc(l1), 21, INK, "end", 600 if k != "B" else 500))
    if l2:
        b.append(t(L - 16, y + BH / 2 + 20, esc(l2), 21, INK, "end", 600 if k != "B" else 500))
    pre = sum(1 for r in sel[k] if r["year"] <= 2017)
    add = collections.Counter(area(r) for r in sel[k] if r["year"] >= 2018)
    if pre:
        b.append(f'<rect x="{X(0) + 1:.1f}" y="{y + 1}" width="{max(X(pre) - X(0) - 2, 0.5):.1f}" height="{BH - 2}" fill="{BG}" stroke="{STONE}" stroke-width="2"></rect>')
    x = pre
    for a, lab, col, tc in AREAS:
        v = add[a]
        if v:
            b.append(f'<rect x="{X(x):.1f}" y="{y}" width="{X(x + v) - X(x):.1f}" height="{BH}" fill="{col}" stroke="{BG}" stroke-width="1.5"></rect>')
            x += v
    tot = len(sel[k]); mult[k] = (pre, tot)
    b.append(t(X(tot) + 12, y + BH / 2 + 9, f"{tot:,}", 24, INK, weight=700))
    b.append(t(W - 56, y + BH / 2 + 9, "new" if pre == 0 else f"×{tot / pre:.0f}" if tot / pre >= 10 else f"×{tot / pre:.1f}", 24, GOLD_D, "end", 700))
spec = [k for k in order if k != "B"]
pre_all, tot_all = sum(mult[k][0] for k in spec), sum(mult[k][1] for k in spec)
frame("company_types", ["EU rules aimed at specific types of", "companies have multiplied since 2018"],
      ["Obligations specific to each type of company: in force at the start of 2018", "and added since, by policy area of the law"],
      ["Obligations in the main laws and their implementing and delegated acts that apply only to that type of company; the baseline applies to every",
       "company. Right column: growth since the start of 2018. Types can overlap (a gatekeeper is also an online platform). As of October 2026."],
      b, "EU rules aimed at specific types of companies have multiplied since 2018: " + "; ".join(f"{NAMES[k]} from {mult[k][0]:,} to {mult[k][1]:,}" for k in order),
      "The EU Digital Rulebook (2026)")

# 7. firm size
f = run("site/build_firm_size.py")
series, ORDER, SHORT, COL, COLS, SUB = f["series"], f["ORDER"], f["SHORT"], f["COL"], f["COLS"], f["SUB"]
L, R, TOP, BOT, YM = 140, 1110, 470, 960, 6000
X = lambda i: L + 30 + i * (R - L - 60) / 5
Y = lambda v: BOT - v / YM * (BOT - TOP)
b = []
for n, k in enumerate(ORDER):
    lx, ly = 56 + (n % 2) * 560, 300 + (n // 2) * 52
    dash = ' stroke-dasharray="8 6"' if k == "B" else ""
    b.append(f'<line x1="{lx}" x2="{lx + 34}" y1="{ly - 7}" y2="{ly - 7}" stroke="{COL[k]}" stroke-width="5"{dash}></line>')
    b.append(t(lx + 46, ly, SHORT[k], 21, INK, weight=600))
    b.append(t(lx + 46, ly + 22, f"{series[k][0]:,} at micro → {series[k][-1]:,} {'designated' if len(series[k]) == 6 else 'at large'}", 17, MUTED))
for v in range(0, YM + 1, 1000):
    b.append(f'<line x1="{L}" x2="{R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>' + t(L - 14, Y(v) + 7, f"{v:,}", 19, MUTED, "end"))
for i, (cc, s) in enumerate(zip(COLS, SUB)):
    b.append(t(X(i), BOT + 32, cc, 20, INK, "middle", 600) + t(X(i), BOT + 56, s, 16, MUTED, "middle"))
for k in ORDER:
    pts = [(X(i), Y(v)) for i, v in enumerate(series[k])]
    dash = ' stroke-dasharray="8 6"' if k == "B" else ""
    b.append(f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{COL[k]}" stroke-width="{3.5 if k == "B" else 5}"{dash} stroke-linejoin="round"></path>')
    for x, y in pts:
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{COL[k]}" stroke="{BG}" stroke-width="2"></circle>')
fi0 = series["FI"][0]
frame("firm_size", [f"Even a micro firm in finance faces", f"about {round(fi0, -2):,} EU obligations"],
      ["Obligations that apply to a firm of each size, by type of company"],
      ["Obligations for the firm’s type plus those for any company in the digital economy, counting size thresholds and SME relief in the laws.",
       "Online platforms continue as gatekeepers and very large platforms; cloud, data and AI as providers of general-purpose AI models with",
       "systemic risk. Main laws and their implementing and delegated acts, as of October 2026."],
      b, "Obligations that apply to a firm of each size: " + "; ".join(f"{SHORT[k]} from {series[k][0]:,} (micro) to {series[k][-1]:,}" for k in ORDER),
      "The EU Digital Rulebook (2026)")

# 8. companies' reporting duties by policy area
r = run("site/build_reporting_charts.py")
then, now, areas = r["then"], r["now"], r["areas"]
L, R, TOP, VMAX = 380, 1040, 380, 600
PX = lambda v: L + v / VMAX * (R - L)
rh = (1000 - TOP) / len(areas)
b = [f'<circle cx="68" cy="312" r="10" fill="{BG}" stroke="{STONE}" stroke-width="3.5"></circle>' + t(88, 319, "Start of 2018", 21),
     f'<circle cx="270" cy="312" r="11" fill="{GOLD}"></circle>' + t(290, 319, "October 2026", 21)]
for v in range(0, VMAX + 1, 100):
    b.append(f'<line x1="{PX(v):.1f}" x2="{PX(v):.1f}" y1="{TOP - 6}" y2="{TOP + rh * len(areas)}" stroke="{BASE if v == 0 else LINE}"></line>' + t(PX(v), TOP + rh * len(areas) + 28, v, 18, MUTED, "middle"))
for i, a in enumerate(areas):
    y = TOP + rh * i + rh / 2
    b.append(t(L - 18, y + 7, esc(a.replace(" Protection", "")), 21, INK, "end", 500))
    b.append(f'<line x1="{PX(then[a]):.1f}" x2="{PX(now[a]):.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity="0.45" stroke-width="8" stroke-linecap="round"></line>')
    b.append(f'<circle cx="{PX(then[a]):.1f}" cy="{y:.1f}" r="9" fill="{BG}" stroke="{STONE}" stroke-width="3.5"></circle>')
    b.append(f'<circle cx="{PX(now[a]):.1f}" cy="{y:.1f}" r="11" fill="{GOLD}"></circle>')
    b.append(t(PX(now[a]) + 18, y + 7, f"{now[a]:,}", 19, INK2, weight=600))
    b.append(t(W - 56, y + 8, "new" if then[a] == 0 else f"×{now[a] / then[a]:.1f}", 22, GOLD_D, "end", 700))
T0, T1 = sum(then.values()), sum(now.values())
b += callout(640, 262, 504, f"×{T1 / T0:.1f}", [f"{T0:,} reporting duties on companies", f"in 2018, {T1:,} today"], h=96, size=50)
frame("reporting_growth", ["Companies’ reporting duties have", "grown in every policy area"],
      ["Reporting obligations on companies, by policy area, start of 2018 and October 2026"],
      ["Reports, notifications, disclosures, record-keeping, information on request and registration that companies must provide, in the main laws",
       "and their implementing and delegated acts; policy areas adapted from Zenner &amp; Marcus (2025). Right column: growth since the start of 2018."],
      b, f"Companies' reporting duties have grown in every policy area, from {T0:,} at the start of 2018 to {T1:,} in October 2026: "
         + "; ".join(f"{a} {then[a]} to {now[a]}" for a in areas), "The EU Digital Rulebook (2026)")
