"""Rules vs standards (Kaplow 1992) chart, draft for review.
Top: obligations in the 105 main acts and in their implementing/delegated acts, split by kind (100% bars).
Bottom: for each act with at least 60 obligations (and a main act with at least 50) in its implementing/delegated acts, the standard-like share
(standard + mixed + specified later) in the main act (gold) and in its secondary acts (blue), with an arrow.
Reads data/rules_standards/summary.json. Writes site/rules_standards.svg. Run from research/ceps_metrics."""
import json
s = json.load(open("data/rules_standards/summary.json"))
INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD, GOLD_D, GOLD_L, BLUE, STONE = "#B8860B", "#8F6708", "#E3CF9C", "#004494", "#D4D2CE"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s_, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                       + (f' font-weight="{weight}"' if weight else "") + f'>{s_}</text>')
SHORT = {"Markets in Crypto-Assets (MiCA)": "MiCA", "Digital Operational Resilience Act (DORA)": "DORA", "General Data Protection Regulation": "GDPR",
         "Payment Services Directive 2 (PSD2)": "PSD2", "Common VAT system Directive": "VAT Directive", "Digitalisation of judicial cooperation Regulation": "Judicial digitalisation",
         "Interoperability of EU information systems (borders and visa)": "EU information systems", "Ecodesign for Sustainable Products Regulation": "Ecodesign Regulation",
         "European Electronic Communications Code": "Electronic Communications Code", ".eu Top-Level Domain Regulation": ".eu domain", "Artificial Intelligence Act": "AI Act",
         "Digital Services Act": "Digital Services Act", "NIS 2 Directive": "NIS2", "European Health Data Space": "Health Data Space", "Administrative cooperation in taxation (DAC)": "Tax cooperation (DAC)", "Recovery and Resilience Facility": "Recovery and Resilience Facility", "Digital Markets Act": "Digital Markets Act"}
nm = lambda n: SHORT.get(n, n.split(" (")[0]) if not n.startswith("Interoperability of EU") else "EU information systems"
W, L, R = 1000, 260, 930
X = lambda v: L + (v - 0.4) / 0.6 * (R - L)
g = []
# top: 100% bars
SEG = [("R", "Rule", GOLD_D), ("S", "Standard", "#7FA3CC"), ("M", "Mixed", "#B9CCE2"), ("L", "Specified later", "#DCE6F1"), ("D", "Left to member states", STONE)]
lx = L
for k, lab, col in SEG:
    g.append(f'<rect x="{lx}" y="2" width="13" height="13" rx="2" fill="{col}"></rect>' + t(lx + 19, 13, lab, 13)); lx += 40 + len(lab) * 7
for i, (key, lab) in enumerate((("main_all", "105 main acts"), ("secondary_all", "Implementing and delegated acts"))):
    d = s[key]; y = 34 + i * 46; x = L
    g.append(t(L - 14, y + 22, lab, 14.5, INK, "end"))
    g.append(t(L - 14, y + 38, f'{d["n"]:,} obligations', 12, MUTED, "end"))
    for k, _, col in SEG:
        w = d[k] * (R - L)  # 100% bar
        g.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="32" fill="{col}" stroke="{BG}"><title>{d[k]:.0%}</title></rect>')
        if w > 40:
            g.append(t(x + w / 2, y + 21, f"{d[k]:.0%}", 13, "#FFFFFF" if k in "R" else INK, "middle", 600))
        x += w
# bottom: arrows per act
y0 = 160
g.append(t(0, y0, "Share of obligations that are rules, in the main act and in its implementing and delegated acts", 14, INK, "start", 600))
acts = sorted([o for o in s["instruments"] if (o["secondary"] or {}).get("n", 0) >= 60 and o["main"]["n"] >= 50], key=lambda o: o["main"]["R"])
top = y0 + 46; RH = 27
for v in (.4, .5, .6, .7, .8, .9, 1.0):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{top - 12}" y2="{top + len(acts) * RH}" stroke="{LINE}"></line>')
    g.append(t(X(v), top - 18, f"{v:.0%}", 12, MUTED, "middle"))
g.append(f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"></path></marker></defs>')
for i, o in enumerate(acts):
    y = top + i * RH + 10
    a, b = o["main"]["R"], o["secondary"]["R"]
    g.append(t(L - 14, y + 5, nm(o["name"]), 13.5, INK, "end"))
    if abs(b - a) > 0.012:
        g.append(f'<line x1="{X(a):.1f}" x2="{X(b) + (-7 if b > a else 7):.1f}" y1="{y}" y2="{y}" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#ah)" opacity="0.8"></line>')
    g.append(f'<circle cx="{X(a):.1f}" cy="{y}" r="6" fill="{GOLD}"><title>{o["name"]}: main act {a:.0%} ({o["main"]["n"]} obligations)</title></circle>')
    g.append(f'<circle cx="{X(b):.1f}" cy="{y}" r="5" fill="{BLUE}"><title>{o["name"]}: implementing and delegated acts {b:.0%} ({o["secondary"]["n"]} obligations)</title></circle>')
ly = top + len(acts) * RH + 22
g.append(f'<circle cx="{L + 6}" cy="{ly - 4}" r="6" fill="{GOLD}"></circle>' + t(L + 18, ly, "Main act", 13))
g.append(f'<circle cx="{L + 106}" cy="{ly - 4}" r="5" fill="{BLUE}"></circle>' + t(L + 118, ly, "Its implementing and delegated acts", 13))
H = ly + 10
open("site/rules_standards.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Rules and standards in EU digital law">' + "".join(g) + "</svg>")
down = sum(o["secondary"]["R"] > o["main"]["R"] for o in acts)
print(len(acts), "acts;", down, "with a more rule-like secondary layer")
