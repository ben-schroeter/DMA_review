"""Three more Statista-style square infographics (1200x1200), same frame as build_infographic.py:
negotiation (proposal vs adopted, 45-degree scatter), acts by policy area, EU acts vs Sarbanes-Oxley.
Writes site/infographics/{negotiation,policy_areas,sox}.svg. Run from research/ceps_metrics."""
import collections, json, os, statistics
import openpyxl

INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
GOLD, GOLD2, STONE, SLATE, BG = "#B8860B", "#E3CF9C", "#C4C1BE", "#5C5858", "#FAF9F5"
SANS = 'font-family="DM Sans, sans-serif"'
SERIF = "font-family=\"'Source Serif 4', Georgia, serif\""
W = H = 1200

wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values); hdr = rows[0]
inst = [r for r in (dict(zip(hdr, x)) for x in rows[1:] if x[0] is not None)
        if r["adoption_date"] and r["restrictions_total"] is not None and r["status_oct2026"] == "adopted"]
yr = lambda r: int(str(r["adoption_date"])[:4])
SHORT = {"Artificial Intelligence Act": "AI Act", "Markets in Crypto-Assets (MiCA)": "MiCA", "General Data Protection Regulation": "GDPR",
         "Digital Services Act": "DSA", "Digital Markets Act": "DMA", "European Health Data Space": "European Health Data Space",
         "Anti-Money Laundering Regulation": "AML Regulation", "Horizon Europe": "Horizon Europe", "Data Act": "Data Act"}


def esc(s):
    return s.replace("&", "&amp;")


def t(x, y, txt, size, fill=INK2, anchor="start", weight=400, font=SANS):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {font} font-size="{size}" font-weight="{weight}" fill="{fill}">{txt}</text>'


def frame(head, sub, notes, body, aria, name):
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
    g.append(t(56, 1180, f'Source: The EU Digital Rulebook (2026) · <tspan fill="{GOLD}" font-weight="700" font-size="18">eutechlaws.org</tspan>', 16, INK2, weight=500))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(aria)}">' + "".join(g) + "</svg>"
    open(f"site/infographics/{name}.svg", "w").write(svg)


def callout(x, y, w, big, lines, h=132):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="{LINE}"></rect>',
           t(x + 24, y + h / 2 + 22, big, 64, GOLD, weight=700, font=SERIF)]
    off = (h - 26 * len(lines)) / 2 + 20
    for i, line in enumerate(lines):
        out.append(t(x + 24 + 34 * len(big) + 22, y + off + 26 * i, line, 20, INK2))
    return out


os.makedirs("site/infographics", exist_ok=True)

# 1. negotiation: proposal (x) vs adopted (y), 45-degree line
cmp_ = [r for r in inst if isinstance(r.get("proposal_restrictions_total"), (int, float))]
up = sum(r["restrictions_total"] > r["proposal_restrictions_total"] for r in cmp_)
p_tot, a_tot = sum(r["proposal_restrictions_total"] for r in cmp_), sum(r["restrictions_total"] for r in cmp_)
L, R, TOP, BOT, mx = 130, 80, 300, 970, 1200
X = lambda v: L + v / mx * (W - L - R)
Y = lambda v: BOT - v / mx * (BOT - TOP)
b = [f'<path d="M{X(0):.1f},{Y(0):.1f} L{X(0):.1f},{Y(mx):.1f} L{X(mx):.1f},{Y(mx):.1f} Z" fill="{GOLD2}" fill-opacity="0.22"></path>']
for v in range(0, mx + 1, 200):
    b.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>')
    b.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{TOP}" y2="{BOT}" stroke="{BASE if v == 0 else LINE}"></line>')
    b.append(t(L - 12, Y(v) + 6, f"{v:,}", 18, MUTED, "end"))
    b.append(t(X(v), BOT + 28, f"{v:,}", 18, MUTED, "middle"))
b.append(t((L + W - R) / 2, BOT + 60, "Obligations in the Commission’s proposal", 20, INK2, "middle", 500))
b.append(f'<text transform="translate({L - 82},{(TOP + BOT) / 2}) rotate(-90)" text-anchor="middle" {SANS} font-size="20" font-weight="500" fill="{INK2}">Obligations in the adopted law</text>')
b.append(f'<line x1="{X(0):.1f}" y1="{Y(0):.1f}" x2="{X(mx):.1f}" y2="{Y(mx):.1f}" stroke="{INK2}" stroke-width="1.5" stroke-dasharray="7 6"></line>')
b.append(t(X(1075), Y(985), "no change", 17, MUTED, "middle"))
b.append(t(X(40), Y(1150), "Above the line: more obligations", 18, INK2, weight=500))
b.append(t(X(40), Y(1150) + 24, "after negotiation", 18, INK2, weight=500))
for r in sorted(cmp_, key=lambda r: r["restrictions_total"] > r["proposal_restrictions_total"]):
    c = GOLD if r["restrictions_total"] > r["proposal_restrictions_total"] else SLATE
    b.append(f'<circle cx="{X(r["proposal_restrictions_total"]):.1f}" cy="{Y(r["restrictions_total"]):.1f}" r="7" fill="{c}" fill-opacity="0.85" stroke="{BG}" stroke-width="1.2"></circle>')
top6 = sorted(cmp_, key=lambda r: -(r["restrictions_total"] - r["proposal_restrictions_total"]))[:6]
OFF = {"AI Act": (-14, 0, "end"), "MiCA": (-14, 6, "end"), "European Health Data Space": (-14, -4, "end"),
       "AML Regulation": (-14, 16, "end"), "DSA": (-14, -12, "end"), "Horizon Europe": (-14, 0, "end")}
for r in top6:
    nm = SHORT.get(r["name"], r["name"].split(" (")[0])
    dx, dy, an = OFF.get(nm, (12, 5, "start"))
    b.append(t(X(r["proposal_restrictions_total"]) + dx, Y(r["restrictions_total"]) + dy + 6, f'{esc(nm)} <tspan fill="{MUTED}" font-weight="400">{r["proposal_restrictions_total"]:,} → {r["restrictions_total"]:,}</tspan>', 16, INK, an, 600))
b += callout(X(560), Y(560) + 150, 470, f"{up}/{len(cmp_)}", ["acts gained obligations; together", f"{p_tot:,} → {a_tot:,} (+{100 * (a_tot / p_tot - 1):.0f}%)"], h=110)
frame(["EU digital laws come out of negotiation", "with more rules than went in"],
      [f"Obligations in the Commission’s proposal and in the adopted law, {len(cmp_)} EU digital acts"],
      ["Each dot is one act; gold: more obligations in the adopted law than in the proposal. Legal text only (articles and annexes), counted",
       "the same way in both. Three adopted acts could not be compared because their proposals are not usable in EUR-Lex."],
      b, f"EU digital laws come out of negotiation with more rules than went in: {up} of {len(cmp_)} acts gained obligations, "
         f"together from {p_tot:,} to {a_tot:,}. Largest: " + "; ".join(f'{SHORT.get(r["name"], r["name"])} {r["proposal_restrictions_total"]} to {r["restrictions_total"]}' for r in top6),
      "negotiation")

# 2. acts by policy area, before 2020 and since
pa = collections.defaultdict(lambda: [0, 0])
for r in inst:
    pa[r["policy_area_ceps"]][yr(r) >= 2020] += 1
pa_rows = sorted(pa.items(), key=lambda kv: (-sum(kv[1]), kv[0]))
n_new = sum(v[1] for _, v in pa_rows)
ind = pa["Industrial Policy"]
L, TOP, BOT = 390, 392, 1036
rh = (BOT - TOP) / len(pa_rows)
pmax = max(sum(v) for _, v in pa_rows)
PX = lambda v: v / pmax * (W - L - 110)
b = [f'<rect x="56" y="274" width="20" height="20" rx="3" fill="{GOLD}"></rect>' + t(86, 291, "Since 2020", 21, INK2),
     f'<rect x="236" y="274" width="20" height="20" rx="3" fill="{GOLD2}"></rect>' + t(266, 291, "Before 2020", 21, INK2)]
for i, (a, (old, new)) in enumerate(pa_rows):
    y = TOP + i * rh
    hb = rh - 16
    b.append(t(L - 16, y + rh / 2 + 7, esc(a), 21, INK2, "end"))
    if new:
        b.append(f'<rect x="{L}" y="{y + 8:.1f}" width="{PX(new):.1f}" height="{hb:.1f}" fill="{GOLD}"></rect>')
        if PX(new) > 34:
            b.append(t(L + PX(new) / 2, y + rh / 2 + 7, str(new), 18, "#FFFFFF", "middle", 700))
    if old:
        b.append(f'<rect x="{L + PX(new):.1f}" y="{y + 8:.1f}" width="{PX(old):.1f}" height="{hb:.1f}" fill="{GOLD2}"></rect>')
        if PX(old) > 34:
            b.append(t(L + PX(new) + PX(old) / 2, y + rh / 2 + 7, str(old), 18, INK2, "middle", 600))
    b.append(t(L + PX(old + new) + 12, y + rh / 2 + 8, str(old + new), 22, INK, weight=700))
b += callout(W - 56 - 560, 256, 560, f"{n_new}/{len(inst)}", ["acts adopted since 2020, incl.", f"all {ind[1]} industrial-policy acts"], h=110)
frame(["More than half of EU digital laws", "were adopted since 2020"],
      ["Adopted EU digital acts by policy area, before 2020 and since"],
      ["Policy areas follow CEPS (Zenner &amp; Marcus, 2025). The 105 adopted EU digital acts in the CEPS inventory, by year of adoption;",
       "numbers in the bars: acts since 2020 (gold) and before 2020 (light gold). As of October 2026."],
      b, f"More than half of EU digital laws were adopted since 2020: {n_new} of {len(inst)}. By policy area: "
         + "; ".join(f"{a} {o + n} ({n} since 2020)" for a, (o, n) in pa_rows), "policy_areas")

# 3. EU acts vs Sarbanes-Oxley
sox = json.load(open("data/benchmark_sox.json"))["all_text"]["restrictions_total"]
recent = [r for r in inst if yr(r) >= 2020]
pick = ["Artificial Intelligence Act", "Digital Services Act", "General Data Protection Regulation", "Digital Markets Act", "Data Act"]
bars = [(SHORT[n], next(r["restrictions_total"] for r in inst if r["name"] == n), GOLD) for n in pick]
bars += [("EU average, acts since 2020", round(statistics.mean(r["restrictions_total"] for r in recent)), STONE),
         ("EU average, all 105 acts", round(statistics.mean(r["restrictions_total"] for r in inst)), STONE),
         ("Sarbanes-Oxley Act (US, 2002)", sox, SLATE)]
bars.sort(key=lambda x: -x[1])
ai = bars[0][1]
L, TOP, BOT = 370, 320, 1020
rh = (BOT - TOP) / len(bars)
bmax = 800
BX = lambda v: v / bmax * (W - L - 120)
b = [f'<line x1="{L + BX(sox):.1f}" x2="{L + BX(sox):.1f}" y1="{TOP - 6}" y2="{BOT}" stroke="{SLATE}" stroke-width="1.5" stroke-dasharray="6 5"></line>',
     t(L + BX(sox) + 8, TOP + 4, f"Sarbanes-Oxley: {sox}", 17, SLATE, weight=600)]
for i, (nm, v, c) in enumerate(bars):
    y = TOP + 16 + i * rh
    hb = rh - 24
    bold = c == SLATE or i == 0
    b.append(t(L - 16, y + hb / 2 + 7, esc(nm), 21, INK if bold else INK2, "end", 600 if bold else 400))
    b.append(f'<rect x="{L}" y="{y:.1f}" width="{BX(v):.1f}" height="{hb:.1f}" rx="4" fill="{c}"></rect>')
    b.append(t(L + BX(v) + 12, y + hb / 2 + 8, f"{v:,}", 22, INK, weight=700))
b += callout(W - 56 - 430, TOP + 16 + rh * 3.5, 430, f"×{ai / sox:.1f}", ["obligations in the AI Act", "vs Sarbanes-Oxley"], h=100)
frame(["The AI Act carries three times as many", "obligations as Sarbanes-Oxley"],
      ["Obligations per act: major EU digital laws and EU averages against the US", "Sarbanes-Oxley Act (2002), counted the same way"],
      ["Automated count of obligations in the legal text (articles and annexes; for Sarbanes-Oxley, the enacted text). The counter was",
       "89% precise on EU texts and 68% on Sarbanes-Oxley, so the US figure is likely overstated rather than understated. As of October 2026."],
      b, f"The AI Act carries three times as many obligations as Sarbanes-Oxley: " + "; ".join(f"{n} {v}" for n, v, _ in bars), "sox")
print("negotiation", up, len(cmp_), p_tot, a_tot, "| areas", n_new, len(inst), ind, "| sox", sox, ai, round(ai / sox, 2))
