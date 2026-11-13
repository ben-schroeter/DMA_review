"""Studies page: cumulative number of sources in the studies library (ex-post assessments and economics of regulation) by type of study,
stacked area by publication year. Types follow the Studies page collections and do not overlap: causal studies, official reviews,
other evidence since adoption (the rest of "All evidence"), economics of regulation.
Reads site/studies_data.json (built by site/build_studies_data.py); writes site/studies_area.svg. Run from research/digital_rulebook."""
import collections, json

L = json.load(open("site/studies_data.json"))["L"]
INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
# bottom to top
SERIES = [("ev causal", "Causal studies", "#8F6708", "#FFFFFF"), ("ev review", "Official reviews", "#B8860B", "#FFFFFF"),
          ("ev", "Other evidence", "#E3CF9C", INK), ("econ", "Economics of regulation", "#5C5858", "#FFFFFF")]
assert {x[10] for x in L} <= {s[0] for s in SERIES}, {x[10] for x in L}
Y0, Y1 = 2000, max(x[2] for x in L if x[2] and x[10] in {s[0] for s in SERIES})
cnt = {k: collections.Counter(x[2] for x in L if x[10] == k and x[2]) for k, *_ in SERIES}
cum = {}
for k, *_ in SERIES:
    c = sum(v for y, v in cnt[k].items() if y < Y0); cum[k] = {}
    for y in range(Y0, Y1 + 1):
        c += cnt[k][y]; cum[k][y] = c
total = {y: sum(cum[k][y] for k, *_ in SERIES) for y in range(Y0, Y1 + 1)}

W, LM, RM, TOP, PH = 580, 40, 196, 30, 260   # compact: sits beside the intro text
PW = W - LM - RM
step = 100
YM = -(-total[Y1] // step) * step
X = lambda y: LM + (y - Y0) / (Y1 - Y0) * PW
Y = lambda v: TOP + PH - v / YM * PH
g = []
for v in range(0, YM + 1, step):
    g.append(f'<line x1="{LM}" x2="{LM + PW}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>')
    g.append(t(LM - 8, Y(v) + 4, f"{v:,}", 12, MUTED, "end"))
for y in [y for y in range(Y0, Y1 + 1, 10) if Y1 - y >= 4] + [Y1]:   # last year (to date) always labelled, no crowding
    g.append(t(X(y), TOP + PH + 18, y, 12, MUTED, "middle"))
below = {y: 0 for y in range(Y0, Y1 + 1)}
ends = []
for k, lab, col, txt in SERIES:
    top = {y: below[y] + cum[k][y] for y in below}
    pts = " ".join(f"{X(y):.1f},{Y(top[y]):.1f}" for y in range(Y0, Y1 + 1)) + " " + " ".join(f"{X(y):.1f},{Y(below[y]):.1f}" for y in range(Y1, Y0 - 1, -1))
    g.append(f'<polygon points="{pts}" fill="{col}" stroke="#FAF9F5" stroke-width="1"><title>{lab}: {cum[k][Y1]:,} by {Y1}</title></polygon>')
    ends.append((lab, col, cum[k][Y1], (Y(top[Y1]) + Y(below[Y1])) / 2))
    below = top
# end labels on the right, nudged apart
ys = [e[3] for e in ends]
for i in range(1, len(ys)):
    ys[i] = min(ys[i], ys[i - 1] - 34)
lx = LM + PW + 14
for (lab, col, n, y0), y in zip(ends, ys):
    g.append(f'<line x1="{LM + PW + 2}" x2="{lx - 2}" y1="{y0:.1f}" y2="{y:.1f}" stroke="{BASE}"></line>')
    g.append(f'<rect x="{lx}" y="{y - 13:.1f}" width="10" height="10" rx="2" fill="{col}"></rect>')
    g.append(t(lx + 16, y - 4, lab, 13.5, INK2))
    g.append(t(lx + 16, y + 12, f"{n:,}", 13, INK, weight="600"))
g.append(t(LM, TOP - 12, f"Total: {total[Y1]:,} sources", 13, INK, weight="600"))
H = TOP + PH + 28
aria = "Cumulative number of sources in the evidence library by type of study, " + f"{Y0} to {Y1}: " + "; ".join(f"{lab} {n:,}" for lab, _, n, _ in ends)
svg = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"
open("site/studies_area.svg", "w").write(svg)
print("studies area:", {lab: n for lab, _, n, _ in ends}, "total", total[Y1], "before", Y0, sum(sum(v for y, v in cnt[k].items() if y < Y0) for k in cnt))
