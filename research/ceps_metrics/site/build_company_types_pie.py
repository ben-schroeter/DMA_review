"""Small pie for the reporting section of the company-types page: all obligations on companies in the laws coded for
company types (each obligation once), by kind of rule, with reporting obligations split out and set off.
Same kinds and colours as site/build_company_types_kinds.py. Writes site/company_types_pie.svg. Run from research/ceps_metrics."""
import collections, math

exec(open("scripts/company_types.py").read().split('out = {"names"')[0])   # rows, M

INK, INK2, MUTED, BG = "#282424", "#3F3B3B", "#666666", "#FAF9F5"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
KINDS = [("reporting", "Reporting obligations", "#8F6708"), ("obligation", "Other positive duties", "#B8860B"), ("duty_of_result", "Duties of result", "#E3CF9C"),
         ("prohibition", "Prohibitions", "#5C5858"), ("restricted_permission", "Restricted permissions", "#A6A3A0"), ("explicit_requirement", "Explicit requirements", "#282424")]
xs = [r for r in rows if r["row_id"] in M]
c = collections.Counter("reporting" if r["reporting"] and r["category"] != "prohibition" else r["category"] for r in xs)
n = len(xs)
W, H, CX, CY, RAD, OFF = 390, 196, 88, 98, 80, 11
g, a0 = [], -math.pi / 2
for k, lab, col in KINDS:
    a1 = a0 + c[k] / n * 2 * math.pi
    mid = (a0 + a1) / 2
    dx, dy = (OFF * math.cos(mid), OFF * math.sin(mid)) if k == "reporting" else (0, 0)
    x0, y0 = CX + dx + RAD * math.cos(a0), CY + dy + RAD * math.sin(a0)
    x1, y1 = CX + dx + RAD * math.cos(a1), CY + dy + RAD * math.sin(a1)
    large = 1 if a1 - a0 > math.pi else 0
    g.append(f'<path d="M{CX + dx:.1f},{CY + dy:.1f} L{x0:.1f},{y0:.1f} A{RAD},{RAD} 0 {large} 1 {x1:.1f},{y1:.1f} Z" fill="{col}" stroke="{BG}" stroke-width="1.5">'
             f'<title>{lab}: {c[k]:,} ({c[k] / n:.1%})</title></path>')
    if k == "reporting":
        lx, ly = CX + dx + RAD * 0.62 * math.cos(mid), CY + dy + RAD * 0.62 * math.sin(mid)
        g.append(t(lx, ly + 5, f"{c[k] / n:.0%}", 15, "#FFFFFF", "middle", 700))
    a0 = a1
LX = 192
for i, (k, lab, col) in enumerate(KINDS):
    y = 30 + i * 26
    bold = k == "reporting"
    g.append(f'<rect x="{LX}" y="{y - 11}" width="12" height="12" rx="2" fill="{col}"></rect>'
             + t(LX + 18, y, lab, 12.5, INK if bold else INK2, "start", 600 if bold else None)
             + t(W - 2, y, f"{c[k] / n:.0%}", 12.5, INK if bold else MUTED, "end", 600 if bold else None))
g.append(t(LX, 30 + len(KINDS) * 26 + 4, f"{n:,} obligations on companies", 12, MUTED))
aria = "Obligations on companies by kind of rule: " + "; ".join(f"{lab} {c[k] / n:.0%}" for k, lab, _ in KINDS)
open("site/company_types_pie.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width: {W}px" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
print(n, {k: (c[k], round(c[k] / n * 100, 1)) for k, _, _ in KINDS})
