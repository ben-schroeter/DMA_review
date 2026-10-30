"""Chart for the company-types page: obligations by kind of rule for each type of company (equal-length bars, shares),
same colours as the 'By kind of rule' donut on the Rules page. Writes site/company_types_kinds.svg."""
import collections
exec(open("scripts/company_types.py").read().split('out = {"names"')[0])   # rows, M, TYPES, NAMES, applies()

INK, INK2, MUTED, BG = "#282424", "#3F3B3B", "#666666", "#FAF9F5"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
KINDS = [("obligation", "Positive obligations", "#B8860B"), ("prohibition", "Prohibitions", "#5C5858"), ("duty_of_result", "Duties of result", "#E3CF9C"),
         ("restricted_permission", "Restricted permissions", "#A6A3A0"), ("explicit_requirement", "Explicit requirements", "#282424")]
sel = {k: [r for r in rows if k in M.get(r["row_id"], {}) and applies(M[r["row_id"]][k], r, k)] for k in TYPES}
sel["B"] = [r for r in rows if M.get(r["row_id"], {}).get("B") == "F"]
order = sorted(TYPES, key=lambda k: -len(sel[k])) + ["B"]
W, L, R, BH, GAP, TOP = 1000, 300, 840, 30, 22, 40
g, lx = [], 0
for k, lab, c in KINDS:
    g.append(f'<rect x="{lx}" y="4" width="12" height="12" rx="2" fill="{c}"></rect>' + t(lx + 18, 15, lab, 12.5)); lx += 30 + len(lab) * 7
g.append(t(R + 34, TOP - 10, "Prohibitions", 13, MUTED))
for i, k in enumerate(order):
    xs = sel[k]; n = len(xs); c = collections.Counter(r["category"] for r in xs)
    y = TOP + i * (BH + GAP) + (14 if k == "B" else 0)
    name = NAMES[k].replace("Baseline: all companies", "Baseline: every company")
    if k == "B":
        g.append(f'<line x1="0" x2="{W}" y1="{y - 18}" y2="{y - 18}" stroke="#E8E6E3"></line>')
    g.append(t(L - 14, y + 13, name, 14.5, INK if k != "B" else INK2, "end", 600 if k != "B" else 500))
    g.append(t(L - 14, y + 29, f"{n:,} obligations", 12, MUTED, "end"))
    x = L
    for kk, lab, col in KINDS:
        w = c[kk] / n * (R - L)
        g.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{BH}" fill="{col}" stroke="{BG}" stroke-width="1"><title>{name}, {lab}: {c[kk]:,} ({c[kk] / n * 100:.1f}%)</title></rect>')
        if kk == "obligation":
            g.append(t(x + 12, y + 20, f"{c[kk] / n * 100:.0f}% positive obligations", 13, "#FFFFFF", "start", 700))
        x += w
    g.append(t(R + 34, y + 21, f"{c['prohibition'] / n * 100:.1f}%", 18, INK if k != "B" else INK2, "start", 700))
H = TOP + len(order) * (BH + GAP) + 14 + 6
aria = "Obligations by kind of rule for each type of company: " + "; ".join(
    f"{NAMES[k]}: {sum(1 for r in sel[k] if r['category'] == 'prohibition') / len(sel[k]) * 100:.1f}% prohibitions" for k in order)
open("site/company_types_kinds.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
