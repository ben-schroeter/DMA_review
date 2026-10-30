"""Small multiples for the Rules page: obligations on companies by type of company, cumulative 2000-2026, laws vs implementing/delegated
acts, shared axes (same design as the policy-area panels). Uses the law-to-type matrix in scripts/company_types.py.
Writes site/company_types_time.svg. Run from research/ceps_metrics."""
import collections
src = open("scripts/company_types.py").read().split('out = {"names"')[0]
exec(src)   # rows, M, TYPES, NAMES, applies()

INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD, GOLD_D, STONE, LIGHT = "#B8860B", "#8F6708", "#A6A3A0", "#E3CF9C"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
sel = {k: [r for r in rows if k in M.get(r["row_id"], {}) and applies(M[r["row_id"]][k], r, k)] for k in TYPES}
sel["B"] = [r for r in rows if M.get(r["row_id"], {}).get("B") == "F"]
order = sorted(TYPES, key=lambda k: -len(sel[k])) + ["B"]
Y0, Y1 = 2000, 2026
NC, W, LM, PW, GX, PH, GY, TT = 4, 1000, 44, 206, 34, 110, 74, 12
YM = 4000
g = [f'<rect x="{LM}" y="4" width="12" height="12" rx="2" fill="{GOLD}"></rect>' + t(LM + 18, 15, "In the laws", 13),
     f'<rect x="{LM + 120}" y="4" width="12" height="12" rx="2" fill="{LIGHT}"></rect>' + t(LM + 138, 15, "In implementing and delegated acts", 13),
     f'<line x1="{LM + 390}" x2="{LM + 390}" y1="2" y2="18" stroke="{STONE}" stroke-dasharray="3 3"></line>' + t(LM + 398, 15, "start of 2018", 13, MUTED)]
for i, k in enumerate(order):
    x0 = LM + (i % NC) * (PW + GX); y0 = TT + 58 + (i // NC) * (PH + GY)
    X = lambda y, x0=x0: x0 + (y - Y0) / (Y1 - Y0) * PW
    Y = lambda v, y0=y0: y0 + PH - v / YM * PH
    law = collections.Counter(r["year"] for r in sel[k] if r["kind"] == "main")
    sec_ = collections.Counter(r["year"] for r in sel[k] if r["kind"] == "secondary")
    cl, cs = sum(v for y, v in law.items() if y < Y0), sum(v for y, v in sec_.items() if y < Y0)
    sl, st = {}, {}
    for y in range(Y0, Y1 + 1):
        cl += law[y]; cs += sec_[y]; sl[y], st[y] = cl, cl + cs
    for v in (1000, 2000, 3000, 4000):
        g.append(f'<line x1="{x0}" x2="{x0 + PW}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"></line>')
        if i % NC == 0:
            g.append(t(x0 - 6, Y(v) + 4, f"{v // 1000}k", 11.5, MUTED, "end"))
    def steps(vals):
        out, prev = [], None
        for y in range(Y0, Y1 + 1):
            if prev is not None:
                out.append(f"{X(y):.1f},{prev:.1f}")
            out.append(f"{X(y):.1f},{Y(vals[y]):.1f}"); prev = Y(vals[y])
        return " ".join(out)
    top_c, law_c = (STONE, "#D4D2CE") if k == "B" else (LIGHT, GOLD)
    g.append(f'<polygon points="{X(Y0):.1f},{Y(0):.1f} {steps(st)} {X(Y1):.1f},{Y(0):.1f}" fill="{top_c}"></polygon>')
    g.append(f'<polygon points="{X(Y0):.1f},{Y(0):.1f} {steps(sl)} {X(Y1):.1f},{Y(0):.1f}" fill="{law_c if k != "B" else "#8E8B88"}"></polygon>')
    g.append(f'<line x1="{X(2018):.1f}" x2="{X(2018):.1f}" y1="{y0 - 4}" y2="{y0 + PH}" stroke="{STONE}" stroke-dasharray="3 3"></line>')
    g.append(f'<line x1="{x0}" x2="{x0 + PW}" y1="{y0 + PH}" y2="{y0 + PH}" stroke="{BASE}"></line>')
    for y in (2000, 2018, 2026):
        g.append(t(X(y), y0 + PH + 15, y, 11, MUTED, "middle"))
    now, then = st[Y1], st[2017]
    gr = "new since 2018" if then == 0 else (f"×{now / then:.0f} since 2018" if now / then >= 10 else f"×{now / then:.1f} since 2018")
    name = NAMES[k].replace("Baseline: all companies", "Baseline: every company")
    g.append(f'<rect x="{x0}" y="{y0}" width="{PW}" height="{PH}" fill="transparent"><title>{name}: {then:,} at the start of 2018, {now:,} in October 2026 ({sl[Y1]:,} in the laws)</title></rect>')
    g.append(t(x0, y0 - 22, name if len(name) < 30 else name.replace(" and very large platforms", " and very large platforms").replace("Online platforms and digital services", "Online platforms, digital services"), 14 if len(name) < 30 else 12.5, INK, "start", 600))
    g.append(t(x0, y0 - 6, f'{now:,} <tspan fill="{GOLD_D if k != "B" else MUTED}" font-weight="600">{gr}</tspan>', 12.5, MUTED))
H = TT + 58 + 2 * (PH + GY) - GY + 26
aria = "Obligations on companies by type of company, cumulative 2000 to 2026, on shared axes: " + "; ".join(
    f"{NAMES[k]} {sum(1 for r in sel[k] if r['year'] <= 2017):,} at the start of 2018, {len(sel[k]):,} in 2026" for k in order)
open("site/company_types_time.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
print({k: len(sel[k]) for k in order})
