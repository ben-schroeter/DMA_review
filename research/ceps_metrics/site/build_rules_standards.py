"""Rules vs standards (Kaplow 1992) chart for the Quantification page.
Top: 100% bars by kind of obligation, for all obligations and for obligations on companies, in the 105 main acts and in their
implementing and delegated acts. Bottom: for each act with at least 60 obligations in its implementing and delegated acts and at
least 50 in the main act, the share of rules in the main act (gold) and in its secondary acts (blue); all obligations.
Reads data/rules_standards (codes, instances, summary). Writes site/rules_standards.svg. Run from research/ceps_metrics."""
import json, glob, collections, openpyxl
C = {}
for f in glob.glob("data/rules_standards/batches/b??_coded.json"):
    for o in json.load(open(f)):
        C[o["k"]] = o["c"]
inst = [json.loads(l) for l in open("data/rules_standards/instances.jsonl")]
am = [json.loads(l)["formal"] for l in open("data/addressee/v2_final_main.jsonl")]
asec = [json.loads(l)["formal"] for l in open("data/addressee/v2_secondary.jsonl")]
parent = {s["celex"]: s["parent"] for s in json.load(open("data/secondary_acts.json"))}
wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True); r = list(wb["instruments"].values); h = r[0]
name2cel = {x[h.index("name")]: str(x[h.index("celex_measured")]) for x in r[1:] if x[0]}
s = json.load(open("data/rules_standards/summary.json"))
I = {name2cel[o["name"]] for o in s["instruments"]}
tot = collections.defaultdict(collections.Counter); per = collections.defaultdict(collections.Counter)
for x in inst:
    c = C[x["key"]]
    if c == "N":
        continue
    d = x["doc"] if x["src"] == "main" else parent.get(x["doc"])
    if d not in I:
        continue
    a = (am if x["src"] == "main" else asec)[x["rid"]]
    for grp in ("all", "companies") if a == "private_parties" else ("all",):
        tot[(grp, x["src"])][c] += 1; per[(d, x["src"], grp)][c] += 1
K = "RSMLD"
share = lambda c: (lambda n: ({k: c[k] / n for k in K} | {"n": n}) if n else {"n": 0})(sum(c[k] for k in K))

INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD, GOLD_D, GOLD_L, BLUE, BLUE_L, STONE = "#B8860B", "#8F6708", "#E3CF9C", "#004494", "#9DB4D3", "#D4D2CE"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s_, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                       + (f' font-weight="{weight}"' if weight else "") + f'>{s_}</text>')
SHORT = {"Markets in Crypto-Assets (MiCA)": "MiCA", "Digital Operational Resilience Act (DORA)": "DORA", "General Data Protection Regulation": "GDPR",
         "Payment Services Directive 2 (PSD2)": "PSD2", "Common VAT system Directive": "VAT Directive", "Digitalisation of judicial cooperation Regulation": "Judicial digitalisation",
         "Ecodesign for Sustainable Products Regulation": "Ecodesign Regulation", "European Electronic Communications Code": "Electronic Communications Code",
         "Artificial Intelligence Act": "AI Act", "NIS 2 Directive": "NIS2", "European Health Data Space": "Health Data Space",
         "Administrative cooperation in taxation (DAC)": "Tax cooperation (DAC)"}
nm = lambda n: "EU information systems" if n.startswith("Interoperability of EU") else SHORT.get(n, n.split(" (")[0])
W, L, R = 1000, 270, 930
g = []
# top: 100% bars, all and companies
SEG = [("R", "Rule", GOLD_D), ("S", "Standard", "#7FA3CC"), ("M", "Mixed", "#B9CCE2"), ("L", "Specified later", "#DCE6F1"), ("D", "Left to member states", STONE)]
lx = L
for k, lab, col in SEG:
    g.append(f'<rect x="{lx}" y="2" width="13" height="13" rx="2" fill="{col}"></rect>' + t(lx + 19, 13, lab, 13)); lx += 40 + len(lab) * 7
y = 34
for grp, glab in (("all", "All obligations"), ("companies", "Obligations on companies")):
    g.append(t(0, y + 14, glab, 13.5, INK, "start", 600)); y += 22
    for src, lab in (("main", "Main acts"), ("secondary", "Implementing and delegated acts")):
        d = share(tot[(grp, src)]); x = L
        g.append(t(L - 14, y + 15, lab, 14, INK2, "end"))
        g.append(t(L - 14, y + 30, f'{d["n"]:,} obligations', 11.5, MUTED, "end"))
        for k, _, col in SEG:
            w = d[k] * (R - L)
            g.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="28" fill="{col}" stroke="{BG}"><title>{glab}, {lab}: {d[k]:.0%}</title></rect>')
            if w > 40:
                g.append(t(x + w / 2, y + 19, f"{d[k]:.0%}", 13, "#FFFFFF" if k == "R" else INK, "middle", 600))
            x += w
        y += 38
    y += 8
# bottom: per act, share of rules, all (light) and companies (bold)
y0 = y + 26
g.append(t(0, y0, "Share of obligations that are rules, in the main act and in its implementing and delegated acts", 14, INK, "start", 600))
X = lambda v: L + (v - 0.4) / 0.6 * (R - L)
acts = [o for o in s["instruments"] if (o["secondary"] or {}).get("n", 0) >= 60 and o["main"]["n"] >= 50]
acts.sort(key=lambda o: o["main"]["R"])
top = y0 + 46; RH = 27
for v in (.4, .5, .6, .7, .8, .9, 1.0):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{top - 12}" y2="{top + len(acts) * RH}" stroke="{LINE}"></line>')
    g.append(t(X(v), top - 18, f"{v:.0%}", 12, MUTED, "middle"))
g.append(f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"></path></marker></defs>')
ncomp = 0
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
open("site/rules_standards.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Rules and standards in EU digital law, all obligations and obligations on companies">' + "".join(g) + "</svg>")
up = sum(o["secondary"]["R"] > o["main"]["R"] for o in acts)
print(len(acts), "acts;", up, "more rule-based in the second layer;", ncomp, "with a company line")
for k in tot: print(k, {kk: round(v, 3) if kk != "n" else v for kk, v in share(tot[k]).items()})
