"""Rules page, 'By kind of rule': donut of obligations in the adopted laws by kind of rule, the kinds table, and bars by
adoption period. Writes site/rules_kinds_donut.svg, site/rules_kinds_table.html, site/rules_kinds_period.svg.
Run from research/digital_rulebook."""
import math, openpyxl
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
r = list(wb["instruments"].iter_rows(values_only=True)); h = r[0]
A = [dict(zip(h, x)) for x in r[1:] if x[0] and x[h.index("status")] == "adopted"]
K = [("r_obligation", "Positive obligations", "Positive obligations: &quot;shall&quot;, &quot;must&quot;", "#B8860B"),
     ("r_prohibition", "Prohibitions", "Prohibitions: &quot;shall not&quot;, &quot;no … shall&quot;", "#5C5858"),
     ("r_duty_of_result", "Duties of result", "Duties of result: &quot;shall ensure&quot;", "#E3CF9C"),
     ("r_restricted_permission", "Restricted permissions", "Restricted permissions: &quot;may only&quot;", "#A6A3A0"),
     ("r_explicit_requirement", "Explicit requirements", "Explicit requirements", "#282424")]
tot = {k: sum(x[k] or 0 for x in A) for k, *_ in K}; N = sum(tot.values())
pt = lambda rad, a: (160 + rad * math.sin(a), 160 - rad * math.cos(a))
paths, a0 = [], 0
for k, short, lab, col in K:
    v = tot[k]; a1 = a0 + v / N * 2 * math.pi; lg = 1 if a1 - a0 > math.pi else 0
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pt(150, a0), pt(150, a1), pt(92, a1), pt(92, a0)
    paths.append(f'<path d="M{x0:.2f},{y0:.2f} A150,150 0 {lg} 1 {x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f} A92,92 0 {lg} 0 {x3:.2f},{y3:.2f} Z" fill="{col}" stroke="#FAF9F5" stroke-width="2"><title>{lab}: {v:,} ({v / N:.1%})</title></path>')
    a0 = a1
aria = "Obligations by kind of rule: " + "; ".join(f"{short} {tot[k]:,} ({tot[k] / N:.0%})" for k, short, _, _ in K)
open("site/rules_kinds_donut.svg", "w").write(
    f'<svg viewBox="0 0 320 320" width="100%" role="img" aria-label="{aria}" style="max-width: 300px">' + "".join(paths)
    + f'<text x="160" y="152" text-anchor="middle" font-family="Source Serif 4, Georgia, serif" font-size="34" fill="#282424">{N:,}</text>'
    + '<text x="160" y="178" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="14" fill="#666666">obligations</text>'
    + f'<text x="160" y="287" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="18" font-weight="700" fill="#FFFFFF">{tot["r_obligation"] / N:.0%}</text></svg>')
rows = "".join(f'<div style="display: flex; align-items: center; gap: 12px; padding-block: 14px; border-top: 1px solid #E8E6E3;"><span aria-hidden="true" style="width: 12px; height: 12px; border-radius: 3px; background: {col}; flex: none"></span>'
               f'<span style="flex: 1 1 auto">{lab.replace("&quot;", chr(34))}</span><span style="font-weight: 600">{tot[k]:,}</span><span class="cap" style="width: 44px; text-align: right">{tot[k] / N:.0%}</span></div>'
               for k, short, lab, col in K)
open("site/rules_kinds_table.html", "w").write(rows)
# by adoption period
yr = lambda x: int(str(x["adoption_date"])[:4])
P = [("Before 2010", lambda y: y < 2010), ("2010–2017", lambda y: 2010 <= y < 2018), ("2018 onwards", lambda y: y >= 2018)]
g = ['<text x="848" y="16" font-family="DM Sans, sans-serif" font-size="13" fill="#666666">Prohibitions</text>']
L, W, MINW = 170, 650, 6.3
desc = []
for i, (lab, f) in enumerate(P):
    xs = [x for x in A if f(yr(x))]; t = {k: sum(x[k] or 0 for x in xs) for k, *_ in K}; n = sum(t.values())
    y = 34 + i * 62
    g.append(f'<text x="154" y="{y + 16}" text-anchor="end" font-family="DM Sans, sans-serif" font-size="15" font-weight="600" fill="#282424">{lab}</text>'
             f'<text x="154" y="{y + 33}" text-anchor="end" font-family="DM Sans, sans-serif" font-size="12.5" fill="#666666">{n:,} obligations</text>')
    ws = [max(MINW, t[k] / n * W) if t[k] else 0 for k, *_ in K]
    ws[0] = W - sum(ws[1:])
    x = L
    for (k, short, lab2, col), w in zip(K, ws):
        g.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="34" fill="{col}" stroke="#FAF9F5" stroke-width="1"><title>{lab}, {short}: {t[k]:,} ({t[k] / n:.1%})</title></rect>')
        if k == "r_obligation":
            g.append(f'<text x="182" y="{y + 22}" font-family="DM Sans, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">{t[k] / n:.0%} positive obligations</text>')
        x += w
    pr = t["r_prohibition"] / n
    g.append(f'<text x="848" y="{y + 24}" font-family="DM Sans, sans-serif" font-size="20" font-weight="700" fill="{"#282424" if i == 2 else "#5C5858"}">{pr:.1%}</text>')
    desc.append(f"{lab}: prohibitions {pr:.1%} of {n:,} obligations")
open("site/rules_kinds_period.svg", "w").write(f'<svg viewBox="0 0 1000 220" width="100%" role="img" aria-label="Mix of kinds of rule in adopted EU digital laws by adoption period: {"; ".join(desc)}">' + "".join(g) + "</svg>")
print(N, desc)
