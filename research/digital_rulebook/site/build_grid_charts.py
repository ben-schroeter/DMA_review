"""Rules vs Standards page, section on the regulatory design grid (Coglianese): the four cells for obligations on companies in
the main laws (site/grid_quadrant.svg) and the share of obligations that leave the means to the firm, by type of company
(site/grid_company_types.svg). Data: data/rules_standards/grid/summary.json (scripts/grid_aggregate.py).
Run from research/digital_rulebook."""
import json, html
S = json.load(open("data/rules_standards/grid/summary.json"))
esc = html.escape
FONT = "DM Sans, sans-serif"; SERIF = "Source Serif 4, Georgia, serif"
COL = {"MM": "#8F6708", "ME": "#D9B86A", "XM": "#4F7FB3", "XE": "#9DBBDB"}
INK = {"MM": "#FFFFFF", "ME": "#282424", "XM": "#FFFFFF", "XE": "#282424"}
pct = lambda v: f"{100 * v:.0f}%"


def text(x, y, s, size=13, fill="#3F3B3B", anchor="start", weight=None, family=FONT, italic=False):
    w = f' font-weight="{weight}"' if weight else ""
    it = ' font-style="italic"' if italic else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{family}" font-size="{size}" fill="{fill}"{w}{it}>{esc(s)}</text>'


def wrap(s, n):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > n and line:
            out.append(line); line = w
        else:
            line = (line + " " + w).strip()
    return out + [line]


# ---- chart A: the grid, obligations on companies in the main laws
g = S["groups"]["companies_main|all"]
CELLS = {
    "MM": ("Prescriptive rule", "The law says what to do", "“Roaming providers shall charge … on a per-kilobyte basis”", "Roaming Regulation"),
    "ME": ("Performance rule", "A specific result; the firm chooses how", "“ensure that the payee receives the full amount of the payment transaction”", "PSD2"),
    "XM": ("Management-based duty", "Set up and run a system the firm designs", "“a sound, comprehensive and well-documented ICT risk management framework”", "DORA"),
    "XE": ("General duty", "An open-ended result, judged afterwards", "“appropriate and proportionate measures to ensure a high level of privacy, safety, and security of minors”", "Digital Services Act"),
}
W, H, X0, Y0, CW, CH, GAP = 1000, 546, 150, 56, 418, 236, 14
p = [text(X0 + CW / 2, 30, "Means: what to do", 14, "#282424", "middle", 600), text(X0 + CW + GAP + CW / 2, 30, "Ends: what to achieve", 14, "#282424", "middle", 600),
     text(0, Y0 + CH / 2 - 4, "Micro:", 14, "#282424", weight=600), text(0, Y0 + CH / 2 + 14, "specific", 13),
     text(0, Y0 + CH + GAP + CH / 2 - 4, "Macro:", 14, "#282424", weight=600), text(0, Y0 + CH + GAP + CH / 2 + 14, "general", 13)]
for code, (cx, cy) in {"MM": (0, 0), "ME": (1, 0), "XM": (0, 1), "XE": (1, 1)}.items():
    x, y = X0 + cx * (CW + GAP), Y0 + cy * (CH + GAP); name, sub, quote, src = CELLS[code]; ink = INK[code]
    soft = "#F3EBD6" if ink == "#FFFFFF" else "#3F3B3B"
    p.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="10" fill="{COL[code]}"><title>{esc(name)}: {pct(g[code])} of obligations on companies in the main laws</title></rect>')
    p.append(text(x + 22, y + 58, pct(g[code]), 44, ink, family=SERIF))
    p.append(text(x + 22, y + 90, name, 17, ink, weight=600))
    p.append(text(x + 22, y + 112, sub, 13.5, soft))
    for i, ln in enumerate(wrap(quote, 54)[:3]):
        p.append(text(x + 22, y + 146 + i * 19, ln, 13, soft, italic=True))
    p.append(text(x + 22, y + CH - 18, src, 12, soft))
# the n and the 'means left to the firm' total are given in the page text
aria = "Regulatory design grid, obligations on companies in the main laws: " + "; ".join(f"{CELLS[c][0]} {pct(g[c])}" for c in ("MM", "ME", "XM", "XE"))
open("site/grid_quadrant.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(aria)}">' + "".join(p) + "</svg>")

# ---- chart B: means left to the firm, by type of company (main laws and implementing/delegated acts together)
NAMES = {"B": "Baseline: all companies", "GK": "Gatekeepers and very large platforms", "PL": "Online platforms and digital services",
         "FI": "Finance, payments and crypto", "CL": "Cloud, data and AI", "TC": "Telecoms", "PR": "Makers of connected products"}
CT = S["company_types"]
rows = sorted(CT, key=lambda t: CT[t]["all"]["means_left_open"])
LX, BX, BW, RH, TOP = 300, 310, 380, 46, 54
scale = lambda v: BW * v / 0.5   # axis 0-50%
p = []
lx = BX
for code, lab in (("ME", "Performance rule"), ("XM", "Management-based duty"), ("XE", "General duty")):
    p.append(f'<rect x="{lx}" y="2" width="13" height="13" rx="2" fill="{COL[code]}"></rect>' + text(lx + 19, 13, lab, 13)); lx += 34 + len(lab) * 7.2
for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5):
    x = BX + scale(v)
    p.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{TOP - 8}" y2="{TOP + RH * len(rows)}" stroke="#E8E6E3"></line>' + text(x, TOP - 14, pct(v), 12, "#666666", "middle"))
for i, t in enumerate(rows):
    a = CT[t]["all"]; y = TOP + i * RH
    p.append(text(LX, y + 22, NAMES[t], 13.5, "#282424", "end"))
    x = BX
    for code in ("ME", "XM", "XE"):
        w = scale(a[code])
        p.append(f'<rect x="{x:.1f}" y="{y + 6}" width="{w:.1f}" height="24" fill="{COL[code]}" stroke="#FAF9F5"><title>{esc(NAMES[t])}: {esc(code)} {pct(a[code])}</title></rect>'); x += w
    p.append(text(x + 8, y + 23, pct(a["means_left_open"]), 13.5, "#282424", weight=600))
    m, s = CT[t]["main"].get("means_left_open"), CT[t]["secondary"].get("means_left_open")
    if m is not None and s is not None:
        p.append(text(BX + BW + 60, y + 23, f"main laws {pct(m)} · secondary acts {pct(s)}", 12, "#666666"))
Hb = TOP + RH * len(rows) + 10
aria = "Share of obligations on companies that leave the means to the firm, by type of company: " + "; ".join(f"{NAMES[t]} {pct(CT[t]['all']['means_left_open'])}" for t in rows)
open("site/grid_company_types.svg", "w").write(f'<svg viewBox="0 0 1000 {Hb}" width="100%" role="img" aria-label="{esc(aria)}">' + "".join(p) + "</svg>")
print("grid charts:", pct(g["means_left_open"]), {t: pct(CT[t]["all"]["means_left_open"]) for t in rows})
