"""Front-page options aggregating the evidence map (data/evidence_map/cells.json). Writes site/evidence_front_options.json
({A, B, C, D: svg}). A: per kind of effect, laws by strongest evidence (100% bars). B: waffle of all law-effect pairs.
C: funnel of laws. D: obligations by whether their law has a causal study of its economic effects. Run from research/ceps_metrics."""
import json

d = json.load(open("data/evidence_map/cells.json")); V = list(d["instruments"].values())
INK, INK2, MUTED, LINE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#FAF9F5"
COL = {"causal": "#8F6708", "measured": "#E3CF9C", "forecast": "url(#h)", "none": "#FFFFFF"}
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
DEFS = ('<defs><pattern id="h" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#FFFFFF"></rect>'
        '<line x1="0" y1="0" x2="0" y2="6" stroke="#A6A3A0" stroke-width="2"></line></pattern></defs>')
LAB = {"causal": "Causal study", "measured": "Other evaluation or study", "forecast": "Forecast only", "none": "Nothing found"}
core = ["costs", "consumers", "competition", "innovation", "growth"]
ev = lambda c: c["causal"] + c["measured"] > 0
NAMES = {"costs": "Compliance costs", "consumers": "Prices and consumers", "competition": "Competition", "innovation": "Innovation and investment",
         "growth": "Growth and jobs", "market": "Single market, trade and FDI", "rights": "Rights, safety and security", "implementation": "Implementation"}


def legend(x, y, keys=("causal", "measured", "forecast", "none")):
    g = []
    for k in keys:
        g.append(f'<rect x="{x}" y="{y - 11}" width="13" height="13" rx="2" fill="{COL[k]}" stroke="{LINE if k in ("none", "forecast") else COL[k]}"></rect>' + t(x + 19, y, LAB[k], 13))
        x += 40 + len(LAB[k]) * 7
    return g


out = {}
# A: per effect, 100% bars of 105 laws, sorted by share with any after-the-fact evidence
W, L, R, BH, GP, TOP = 1000, 210, 900, 26, 12, 46
g = [DEFS] + legend(0, 14)
rows = sorted(NAMES, key=lambda k: sum(1 for v in V if not v["cells"][k]["best"]))
for i, k in enumerate(rows):
    y = TOP + i * (BH + GP)
    cnt = {gr: sum(1 for v in V if (v["cells"][k]["best"] or "none") == gr) for gr in COL}
    g.append(t(L - 12, y + 18, NAMES[k], 14, INK, "end", 600 if k in core else None))
    x = L
    for gr in ("causal", "measured", "forecast", "none"):
        w = cnt[gr] / len(V) * (R - L)
        g.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{BH}" fill="{COL[gr]}" stroke="{LINE if gr in ("none", "forecast") else BG}"><title>{NAMES[k]}: {LAB[gr]} {cnt[gr]} laws</title></rect>')
        if gr == "causal" and cnt[gr]:
            g.append(t(x + w / 2, y + 18, cnt[gr], 12, "#FFFFFF", "middle", 700))
        x += w
    g.append(t(R + 12, y + 18, f'{cnt["none"]}', 14, INK, "start", 600))
g.append(t(R + 12, TOP - 10, "nothing", 12, MUTED))
H = TOP + len(rows) * (BH + GP) + 10
out["A"] = f'<svg viewBox="0 0 {W} {H}" width="100%">' + "".join(g) + "</svg>"

# B: waffle of 840 pairs, grouped by grade
pairs = sorted([(v["cells"][k]["best"] or "none") for v in V for k in NAMES], key=["causal", "measured", "forecast", "none"].index)
NC, S, GAP = 42, 18, 3
g = [DEFS] + legend(0, 14)
for i, gr in enumerate(pairs):
    x, y = (i % NC) * (S + GAP), 34 + (i // NC) * (S + GAP)
    g.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" rx="2" fill="{COL[gr]}" stroke="{LINE if gr in ("none", "forecast") else COL[gr]}"></rect>')
cnt = {gr: pairs.count(gr) for gr in COL}
H = 34 + (len(pairs) // NC + 1) * (S + GAP) + 30
g.append(t(0, H - 6, f'{len(pairs)} pairs of law and effect (105 laws × 8 kinds of effect): {cnt["causal"]} causal study · {cnt["measured"]} other evidence · {cnt["forecast"]} forecast only · {cnt["none"]} nothing found', 13, MUTED))
out["B"] = f'<svg viewBox="0 0 {NC * (S + GAP)} {H}" width="100%">' + "".join(g) + "</svg>"

# C: funnel of laws
steps = [("Laws in force", len(V)),
         ("with any evidence on an economic effect", sum(1 for v in V if any(ev(v["cells"][k]) for k in core))),
         ("with a causal study of an economic effect", sum(1 for v in V if any(v["cells"][k]["causal"] for k in core))),
         ("with evidence on all five economic effects", sum(1 for v in V if all(ev(v["cells"][k]) for k in core))),
         ("with a causal study of their compliance costs", sum(1 for v in V if v["cells"]["costs"]["causal"]))]
W, L, R, BH, GP = 1000, 0, 640, 40, 14
g = []
for i, (lab, n) in enumerate(steps):
    y = i * (BH + GP)
    w = n / len(V) * (R - L)
    col = ["#C9C6C3", "#E3CF9C", "#B8860B", "#8F6708", "#8F6708"][i]
    g.append(f'<rect x="{L}" y="{y}" width="{max(w, 3):.1f}" height="{BH}" fill="{col}"></rect>')
    g.append(t(L + max(w, 3) + 12, y + 27, f'<tspan font-weight="700" font-size="22" fill="{INK}">{n}</tspan>  {lab}', 15, INK2))
H = len(steps) * (BH + GP)
out["C"] = f'<svg viewBox="0 0 {W} {H}" width="100%">' + "".join(g) + "</svg>"

# D: obligations by whether their law has a causal study of its economic effects
tot = sum(v["obligations"] or 0 for v in V)
groups = [("causal", "Law has a causal study|of an economic effect", sum(v["obligations"] or 0 for v in V if any(v["cells"][k]["causal"] for k in core))),
          ("measured", "Only other evidence|on economic effects", sum(v["obligations"] or 0 for v in V if any(ev(v["cells"][k]) for k in core) and not any(v["cells"][k]["causal"] for k in core))),
          ("none", "No evidence on|any economic effect", sum(v["obligations"] or 0 for v in V if not any(ev(v["cells"][k]) for k in core)))]
W, BH = 1000, 64
g = [DEFS]
x = 0
for k, lab, n in groups:
    w = n / tot * W
    g.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="{BH}" fill="{COL[k]}" stroke="{LINE if k == "none" else BG}" stroke-width="1.5"></rect>')
    g.append(t(x + 12, 40, f"{n / tot:.0%}", 26, "#FFFFFF" if k == "causal" else INK, "start", 700))
    a, b = lab.split("|")
    g.append(t(x, BH + 24, a, 13.5, INK, "start", 600) + t(x, BH + 41, b, 13.5, INK, "start", 600) + t(x, BH + 59, f"{n:,} obligations", 12.5, MUTED))
    x += w
out["D"] = f'<svg viewBox="0 0 {W} {BH + 68}" width="100%">' + "".join(g) + "</svg>"
json.dump(out, open("site/evidence_front_options.json", "w"))
print({k: n for k, _, n in groups}, tot, steps)
