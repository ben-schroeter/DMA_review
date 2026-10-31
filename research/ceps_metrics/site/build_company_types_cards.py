"""Small charts for the 'Six types of company' cards: obligations a company of each type faces over time, cumulative
2000-2026 by year of adoption, stacked: the general rules every company follows (baseline), then the type's own rules in
the laws and in implementing and delegated acts. Shared axes across cards. Uses the matrix in scripts/company_types.py.
Writes site/company_types_cards.json ({type: svg}) and site/company_types_cards_legend.html. Run from research/ceps_metrics."""
import collections, json

exec(open("scripts/company_types.py").read().split('out = {"names"')[0])   # rows, M, TYPES, NAMES, applies()

INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD, GOLD_D, LIGHT, GREY = "#B8860B", "#8F6708", "#E3CF9C", "#D4D2CE"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=12, fill=MUTED, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                       + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
sel = {k: [r for r in rows if k in M.get(r["row_id"], {}) and applies(M[r["row_id"]][k], r, k)] for k in TYPES}
base = [r for r in rows if M.get(r["row_id"], {}).get("B") == "F"]
Y0, Y1, YM = 2000, 2026, 6000
W, H, L, R, T, B = 300, 132, 30, 252, 10, 20


def cum(xs, kind=None):
    c = collections.Counter(r["year"] for r in xs if kind is None or r["kind"] == kind)
    run, out = sum(v for y, v in c.items() if y < Y0), {}
    for y in range(Y0, Y1 + 1):
        run += c[y]; out[y] = run
    return out


X = lambda y: L + (y - Y0) / (Y1 - Y0) * (R - L)
Y = lambda v: H - B - v / YM * (H - B - T)


def steps(vals):
    out, prev = [], None
    for y in range(Y0, Y1 + 1):
        if prev is not None:
            out.append(f"{X(y):.1f},{prev:.1f}")
        out.append(f"{X(y):.1f},{Y(vals[y]):.1f}"); prev = Y(vals[y])
    return out


def band(top, bot):
    up = steps(top)
    down = list(reversed(steps(bot))) if bot else [f"{X(Y1):.1f},{Y(0):.1f}", f"{X(Y0):.1f},{Y(0):.1f}"]
    return " ".join(up + down)


b = cum(base)
out = {}
for k in TYPES:
    law, sec_ = cum(sel[k], "main"), cum(sel[k], "secondary")
    l1 = {y: b[y] + law[y] for y in b}
    l2 = {y: l1[y] + sec_[y] for y in b}
    g = []
    for v in (2000, 4000, 6000):
        g.append(f'<line x1="{L}" x2="{R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"></line>' + t(L - 5, Y(v) + 4, f"{v // 1000}k", 11, MUTED, "end"))
    g.append(f'<polygon points="{band(b, None)}" fill="{GREY}"></polygon>')
    g.append(f'<polygon points="{band(l1, b)}" fill="{GOLD}"></polygon>')
    g.append(f'<polygon points="{band(l2, l1)}" fill="{LIGHT}"></polygon>')
    g.append(f'<line x1="{X(2018):.1f}" x2="{X(2018):.1f}" y1="{T - 4}" y2="{H - B}" stroke="#A6A3A0" stroke-dasharray="3 3"></line>')
    g.append(f'<line x1="{L}" x2="{R}" y1="{H - B}" y2="{H - B}" stroke="{BASE}"></line>')
    for y in (2000, 2018, 2026):
        g.append(t(X(y), H - 5, y, 11, MUTED, "middle"))
    g.append(t(R + 6, Y(l2[Y1]) + 4, f"{l2[Y1]:,}", 13, INK, "start", 600))
    g.append(t(R + 6, Y(l2[Y1]) + 18, "in total", 11, MUTED))
    then = l2[2017]
    g.append(t(X(2018) - 4, Y(then) - 6, f"{then:,}", 11, MUTED, "end"))
    aria = (f"{NAMES[k]}: obligations over time including the general rules for every company. {then:,} at the start of 2018, "
            f"{l2[Y1]:,} in 2026: {b[Y1]:,} general, {law[Y1]:,} in the type's laws, {sec_[Y1]:,} in their implementing and delegated acts")
    out[k] = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"
    print(k, then, l2[Y1], b[Y1], law[Y1], sec_[Y1])
json.dump(out, open("site/company_types_cards.json", "w"), ensure_ascii=False)
sw = lambda c, lab: (f'<span style="display: inline-flex; align-items: center; gap: 6px"><span style="width: 12px; height: 12px; border-radius: 2px; background: {c}"></span>{lab}</span>')
legend = ('<p class="cap" style="margin: 0; display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: center">Charts: obligations a company of this type faces, cumulative by year of adoption · '
          + sw(GREY, "General rules for every company") + sw(GOLD, "Rules for this type, in the laws") + sw(LIGHT, "in implementing and delegated acts")
          + '<span style="display: inline-flex; align-items: center; gap: 6px"><span style="width: 0; height: 12px; border-left: 1.5px dashed #A6A3A0"></span>start of 2018</span></p>')
open("site/company_types_cards_legend.html", "w").write(legend)
