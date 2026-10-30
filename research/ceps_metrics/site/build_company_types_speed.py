"""Chart for the company-types page: reporting obligations by type of company, by when they are due.
Writes site/company_types_speed.svg and prints the counts. Run from research/ceps_metrics."""
import collections
exec(open("scripts/company_types.py").read().split('out = {"names"')[0])   # rows, M, TYPES, NAMES, applies()

INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
CATS = [("fast", "When something happens: without undue delay or within 72 hours", "#8F6708", "#FFFFFF"),
        ("event", "When something happens: later or no deadline", "#B8860B", "#FFFFFF"),
        ("periodic", "Periodic", "#5C5858", "#FFFFFF"), ("on_request", "On request", "#004494", "#FFFFFF"),
        ("ongoing", "Ongoing (records, keeping up to date)", "#A6A3A0", INK), ("one_off", "Once", "#282424", "#FFFFFF"),
        ("unspecified", "Timing not stated in the provision", "#E3E1DD", INK)]


def cat(r):
    if r["cadence"] == "event":
        return "fast" if r["period"] == "without delay" or (r["deadline_hours"] and r["deadline_hours"] <= 72) else "event"
    return r["cadence"]


sel = {k: [r for r in rows if r["reporting"] and k in M.get(r["row_id"], {}) and applies(M[r["row_id"]][k], r, k)] for k in TYPES}
sel["B"] = [r for r in rows if r["reporting"] and M.get(r["row_id"], {}).get("B") == "F"]
order = sorted(TYPES, key=lambda k: -len(sel[k])) + ["B"]
cnt = {k: collections.Counter(cat(r) for r in sel[k]) for k in order}
W, L, R, BH, GAP = 1000, 300, 880, 30, 16
lx, ly, g = 0, 4, []
for k, lab, c, _ in CATS:   # legend
    w = 30 + len(lab) * 6.9
    if lx + w > W:
        lx, ly = 0, ly + 22
    g.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" rx="2" fill="{c}"' + (' stroke="#C9C6C3"' if k == "unspecified" else "") + '></rect>' + t(lx + 18, ly + 11, lab, 12.5))
    lx += w + 14
TOP = ly + 40
XM = 650
X = lambda v: L + v / XM * (R - L)
bot = TOP + len(order) * (BH + GAP) - GAP + 14
for v in range(0, XM + 1, 100):
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{TOP - 4}" y2="{bot + 4}" stroke="{BASE if v == 0 else LINE}"></line>' + t(X(v), bot + 22, v, 12, MUTED, "middle"))
for i, k in enumerate(order):
    y = TOP + i * (BH + GAP) + (14 if k == "B" else 0)
    name = NAMES[k].replace("Baseline: all companies", "Baseline: every company")
    if k == "B":
        g.append(f'<line x1="0" x2="{W}" y1="{y - 15}" y2="{y - 15}" stroke="{LINE}"></line>')
    g.append(t(L - 14, y + BH / 2 + 5, name, 14.5, INK if k != "B" else INK2, "end", 600 if k != "B" else 500))
    x = 0
    for c, lab, col, tc in CATS:
        v = cnt[k][c]
        if not v:
            continue
        g.append(f'<rect x="{X(x):.1f}" y="{y}" width="{X(x + v) - X(x):.1f}" height="{BH}" fill="{col}" stroke="{BG}" stroke-width="1"><title>{name}, {lab}: {v}</title></rect>')
        if c == "fast" and X(x + v) - X(x) > 12:
            g.append(t((X(x) + X(x + v)) / 2, y + BH / 2 + 5, v, 12.5 if X(x + v) - X(x) > 22 else 10.5, tc, "middle", 700))
        x += v
    g.append(t(X(x) + 10, y + BH / 2 + 5, f"{x:,}", 14, INK, "start", 600))
H = bot + 32
aria = "Reporting obligations by type of company and timing: " + "; ".join(f"{NAMES[k]} {sum(cnt[k].values())} in total, {cnt[k]['fast']} due without undue delay or within 72 hours" for k in order)
open("site/company_types_speed.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
for k in order:
    print(k, sum(cnt[k].values()), dict(cnt[k]))
