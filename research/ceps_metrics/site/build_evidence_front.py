"""Front-page evidence chart in two parts on one colour logic (white = nothing found):
  top    what happened to the 440 objectives, indicators and forecasts in the Commission's proposals
  bottom for each kind of effect, the 105 laws in force by the strongest evidence found after adoption (evidence map)
Objective counts are the published figures (data/objectives); law counts come from data/evidence_map/cells.json.
Writes site/evidence_front.svg. Run from research/ceps_metrics."""
import json

d = json.load(open("data/evidence_map/cells.json")); V = list(d["instruments"].values())
INK, INK2, MUTED, LINE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#F5F5F0"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
DEFS = ('<defs><pattern id="hf" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#FFFFFF"></rect>'
        '<line x1="0" y1="0" x2="0" y2="6" stroke="#A6A3A0" stroke-width="2"></line></pattern></defs>')
OBJ = [("Measured", 64, "#8F6708", "#FFFFFF"), ("Partly measured", 64, "#B8860B", "#FFFFFF"), ("Mixed evidence", 27, "#E3CF9C", INK),
       ("Activity only", 67, "url(#hf)", INK), ("Never measured", 218, "#FFFFFF", INK)]
GR = [("causal", "Causal study", "#8F6708", "#FFFFFF"), ("measured", "Other evaluation or study", "#E3CF9C", INK),
      ("forecast", "Forecast only", "url(#hf)", INK), ("none", "Nothing found", "#FFFFFF", INK)]
NAMES = {"costs": "Compliance costs", "consumers": "Prices and consumers", "competition": "Competition", "innovation": "Innovation and investment",
         "growth": "Growth and jobs", "market": "Single market, trade, FDI", "rights": "Rights, safety, security", "implementation": "Implementation"}
W, L, R = 1000, 196, 930
g = [DEFS]
outline = lambda f: LINE if f in ("#FFFFFF", "url(#hf)") else BG


def legend(items, y):
    x = L
    for lab, f in items:
        g.append(f'<rect x="{x}" y="{y - 11}" width="13" height="13" rx="2" fill="{f}" stroke="{outline(f)}"></rect>' + t(x + 19, y, lab, 12.5))
        x += 36 + len(lab) * 6.7


# top: objectives
tot = sum(n for _, n, _, _ in OBJ)
g.append(t(0, 16, "What happened to the 440 objectives in the Commission's proposals", 15, INK, "start", 600))
y0, BH = 34, 34
g.append(t(L - 12, y0 + 22, "440 objectives", 14, INK, "end"))
x = L
for lab, n, f, tc in OBJ:
    w = n / tot * (R - L)
    g.append(f'<rect x="{x:.1f}" y="{y0}" width="{w:.1f}" height="{BH}" fill="{f}" stroke="{outline(f)}"><title>{lab}: {n}</title></rect>')
    if w > 34:
        g.append(t(x + w / 2, y0 + 22, n, 13, tc, "middle", 700))
    x += w
g.append(t(R, y0 - 8, f"{218 / tot:.0%} never measured", 13, INK, "end", 600))
legend([(lab, f) for lab, _, f, _ in OBJ], y0 + BH + 20)

# bottom: effect by effect
y1 = y0 + BH + 74
g.append(t(0, y1, "What has been studied since adoption, by kind of effect: 105 laws in force", 15, INK, "start", 600))
legend([(lab, f) for _, lab, f, _ in GR], y1 + 26)
rows = sorted(NAMES, key=lambda k: sum(1 for v in V if not v["cells"][k]["best"]))
RH, RG, top = 26, 10, y1 + 46
g.append(t(R + 8, top - 6, "none", 11.5, MUTED))
for i, k in enumerate(rows):
    y = top + i * (RH + RG)
    cnt = {gr: sum(1 for v in V if (v["cells"][k]["best"] or "none") == gr) for gr, *_ in GR}
    g.append(t(L - 12, y + 18, NAMES[k], 14, INK, "end"))
    x = L
    for gr, lab, f, tc in GR:
        w = cnt[gr] / len(V) * (R - L)
        g.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{RH}" fill="{f}" stroke="{outline(f)}"><title>{NAMES[k]}: {lab}, {cnt[gr]} laws</title></rect>')
        if gr == "causal" and w > 14:
            g.append(t(x + w / 2, y + 18, cnt[gr], 12, tc, "middle", 700))
        x += w
    g.append(t(R + 8, y + 18, cnt["none"], 14, INK, "start", 600))
H = top + len(rows) * (RH + RG) + 4
aria = ("Top: of 440 objectives in the Commission's proposals, 64 measured, 64 partly measured, 27 mixed evidence, 67 activity only, 218 never measured. "
        "Bottom: for each kind of effect, how many of 105 laws have a causal study, other evidence, a forecast only or nothing: "
        + "; ".join(f'{NAMES[k]} {sum(1 for v in V if not v["cells"][k]["best"])} with nothing' for k in rows))
open("site/evidence_front.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
print(H)
