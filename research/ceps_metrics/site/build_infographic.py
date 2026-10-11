"""Statista-style square infographic: obligations binding private parties, cumulative, 2010-2026.
Writes site/infographics/private_parties.svg (1200x1200). Run from research/ceps_metrics."""
import collections, os
import openpyxl

INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
GOLD, GOLD2, BG = "#B8860B", "#E3CF9C", "#FAF9F5"
SANS = 'font-family="DM Sans, sans-serif"'
SERIF = "font-family=\"'Source Serif 4', Georgia, serif\""

wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)


def sheet(n):
    rows = list(wb[n].values); h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r[0] is not None]


inst = [r for r in sheet("instruments") if r["adoption_date"] and r["restrictions_total"] is not None and r["status_oct2026"] == "adopted"]
sec = [r for r in sheet("secondary_acts") if r["kind"] in ("implementing", "delegated") and r["date"] and r["restrictions_total"] is not None]
yr = lambda d: int(str(d)[:4])
m, s = collections.Counter(), collections.Counter()
for r in inst:
    m[yr(r["adoption_date"])] += r["addr_private_parties"] or 0
for r in sec:
    s[yr(r["date"])] += r["addr_private_parties"] or 0
cum, cm, cs = {}, 0, 0
for y in range(1950, 2027):
    cm += m[y]; cs += s[y]; cum[y] = (cm, cs)
Y0, Y1 = 2010, 2026
base, now = cum[2017][0], cum[Y1][0]
factor = now / base


def t(x, y, txt, size, fill=INK2, anchor="start", weight=400, font=SANS):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {font} font-size="{size}" font-weight="{weight}" fill="{fill}">{txt}</text>'


W = H = 1200
L, R, TOP, BOT = 104, 56, 400, 1000
ymax = 14000
n = Y1 - Y0 + 1
slot = (W - L - R) / n
bw = slot * 0.72
Yc = lambda v: BOT - v / ymax * (BOT - TOP)
g = [f'<rect width="{W}" height="{H}" fill="{BG}"></rect>', f'<rect width="{W}" height="10" fill="{GOLD}"></rect>']
# headline, subtitle, legend
g.append(t(56, 112, "EU tech rules aimed directly at companies", 50, INK, weight=700))
g.append(t(56, 172, "have quadrupled since 2018", 50, INK, weight=700))
g.append(t(56, 228, "Obligations in EU digital laws that name a company as the one who must act,", 24, MUTED))
g.append(t(56, 260, "cumulative at year end", 24, MUTED))
g.append(f'<rect x="56" y="300" width="20" height="20" rx="3" fill="{GOLD}"></rect>' + t(86, 317, "In the laws themselves", 21, INK2))
g.append(f'<rect x="346" y="300" width="20" height="20" rx="3" fill="{GOLD2}"></rect>' + t(376, 317, "In their implementing and delegated acts", 21, INK2))
# grid
for v in range(0, ymax + 1, 2000):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Yc(v):.1f}" y2="{Yc(v):.1f}" stroke="{BASE if v == 0 else LINE}" stroke-width="{1.5 if v == 0 else 1}"></line>')
    g.append(t(L - 14, Yc(v) + 7, f"{v:,}", 19, MUTED, "end"))
# columns
for i, y in enumerate(range(Y0, Y1 + 1)):
    a, b = cum[y]
    x = L + i * slot + (slot - bw) / 2
    g.append(f'<rect x="{x:.1f}" y="{Yc(a):.1f}" width="{bw:.1f}" height="{BOT - Yc(a):.1f}" fill="{GOLD}"></rect>')
    g.append(f'<rect x="{x:.1f}" y="{Yc(a + b):.1f}" width="{bw:.1f}" height="{Yc(a) - Yc(a + b):.1f}" fill="{GOLD2}"></rect>')
    last = y == Y1
    g.append(t(x + bw / 2, Yc(a + b) - 10, f"{(a + b) / 1000:.1f}k", 17 if not last else 20, INK if last else MUTED, "middle", 700 if last else 500))
    g.append(t(x + bw / 2, BOT + 30, f"{y}*" if last else (f"’{y % 100:02d}" if i % 2 else str(y)), 18, INK2, "middle", 500 if last else 400))
    if y in (2017, Y1):
        g.append(t(x + bw / 2, BOT - 12, f"{a:,}", 14.5, "#FFFFFF", "middle", 700))
# x4 callout: from the 2017 gold bar to the 2026 gold bar
cx, cy = L + 40, TOP + 40
g.append(f'<rect x="{cx}" y="{cy}" width="420" height="132" rx="12" fill="#FFFFFF" stroke="{LINE}"></rect>')
g.append(t(cx + 24, cy + 76, f"×{factor:.1f}", 64, GOLD, weight=700, font=SERIF))
g.append(t(cx + 168, cy + 50, f"{base:,} at the start", 20, INK2))
g.append(t(cx + 168, cy + 76, f"of 2018, {now:,} now,", 20, INK2))
g.append(t(cx + 168, cy + 102, "in the laws themselves", 20, INK2))
# footer
g.append(f'<line x1="56" x2="{W - 56}" y1="1066" y2="1066" stroke="{LINE}"></line>')
g.append(t(56, 1100, "* As of October 2026. Automated count of the 105 adopted EU digital acts in the CEPS inventory and their 690 implementing", 16, MUTED))
g.append(t(56, 1124, "and delegated acts, original texts from EUR-Lex; each obligation coded by who must act. Including the implementing and delegated", 16, MUTED))
g.append(t(56, 1148, f"acts, obligations on companies rose ×{(cum[Y1][0] + cum[Y1][1]) / (cum[2017][0] + cum[2017][1]):.1f} over the same period.", 16, MUTED))
g.append(f'<g transform="translate({W - 330},1160)"><rect x="0" y="0" width="22" height="22" rx="3" fill="none" stroke="{INK}" stroke-width="1.6"></rect>'
         f'<path d="M5 15h12M5 11h12M5 7h7" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"></path></g>')
g.append(t(W - 298, 1178, "The EU Digital Rulebook", 22, INK, weight=400, font=SERIF))
g.append(t(56, 1180, "Source: The EU Digital Rulebook (2026)", 16, INK2, weight=500))

aria = (f"EU tech rules aimed directly at companies have quadrupled since 2018. Obligations naming a company in the laws themselves rose from "
        f"{base:,} at the start of 2018 to {now:,} in 2026 (x{factor:.1f}); with implementing and delegated acts, from "
        f"{sum(cum[2017]):,} to {sum(cum[Y1]):,}.")
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"
os.makedirs("site/infographics", exist_ok=True)
open("site/infographics/private_parties.svg", "w").write(svg)
print(base, now, round(factor, 2), cum[Y1])
