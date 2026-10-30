"""Four candidate charts combining the GDP-per-head split and the productivity trend, euro area vs US.
Data: Long-Term Productivity Database v2.7 (data/bcl_ltp_v27_selected.json). GDP per head = output per hour x hours per head,
so in logs the income gap is exactly the productivity gap plus the hours gap. Writes site/gap_options.json. Run from research/ceps_metrics."""
import json, math

INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
GOLD, GOLD_D, US_C, STONE, PANEL = "#B8860B", "#8F6708", "#5C5858", "#A6A3A0", "#F5F5F0"
F = 'font-family="DM Sans, sans-serif"'


def t(x, y, s, size=13, fill=INK2, anchor="start", weight=None, halo=False):
    w = f' font-weight="{weight}"' if weight else ""
    h = ' stroke="#FAF9F5" stroke-width="5" paint-order="stroke"' if halo else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"{w}{h}>{s}</text>'


S = json.load(open("data/bcl_ltp_v27_selected.json"))["series"]
ser = lambda c, n: {int(y): v for y, v in S[c][n].items()}
ZE, US = {n: ser("ZE", n) for n in ("gdp_pc", "lp", "hours_pc")}, {n: ser("USA", n) for n in ("gdp_pc", "lp", "hours_pc")}
YRS = list(range(1950, 2025))
rel = {n: {y: ZE[n][y] / US[n][y] * 100 for y in YRS} for n in ZE}
# log decomposition of the GDP-per-head gap, in percent (100 x ln)
dec = {y: (100 * math.log(rel["lp"][y] / 100), 100 * math.log(rel["hours_pc"][y] / 100)) for y in YRS}
share = lambda y: dec[y][0] / (dec[y][0] + dec[y][1])
out = {}

# A. Three lines relative to the US (US = 100), 1950-2024
W, H, L, R, TOP, BOT = 1000, 470, 52, 150, 40, 420
X = lambda y: L + (y - 1950) / (2024 - 1950) * (W - L - R)
Y = lambda v: BOT - (v - 30) / (150 - 30) * (BOT - TOP)
g = [f'<rect x="{X(1995):.1f}" y="{TOP}" width="{X(2024) - X(1995):.1f}" height="{BOT - TOP}" fill="{PANEL}"></rect>',
     t(X(1995) + 10, TOP + 18, "Since 1995: the digital revolution", 13, MUTED, weight=600)]
for v in range(40, 151, 20):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"></line>' + t(L - 8, Y(v) + 4.5, v, 12, MUTED, "end"))
g.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(100):.1f}" y2="{Y(100):.1f}" stroke="{US_C}" stroke-width="1.6"></line>')
g.append(t(X(1951), Y(100) - 8, "US = 100", 13, US_C, weight=600))
for y in range(1950, 2021, 10):
    g.append(t(X(y), BOT + 22, y, 12.5, MUTED, "middle"))
for n, c, wdt, lab in (("hours_pc", STONE, 2.2, "Hours worked per head"), ("lp", GOLD, 3, "Output per hour"), ("gdp_pc", INK, 3, "GDP per head")):
    pts = " ".join(f"{X(y):.1f},{Y(rel[n][y]):.1f}" for y in YRS)
    g.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{wdt}" stroke-linejoin="round"></polyline>')
ends = {"gdp_pc": ("GDP per head", INK, 0), "lp": ("Output per hour", GOLD_D, 0), "hours_pc": ("Hours per head", US_C, 0)}
ly = {"gdp_pc": Y(rel["gdp_pc"][2024]) + 16, "lp": Y(rel["lp"][2024]) - 4, "hours_pc": Y(rel["hours_pc"][2024]) + 2}
for n, (lab, c, _) in ends.items():
    g.append(f'<circle cx="{X(2024):.1f}" cy="{Y(rel[n][2024]):.1f}" r="3.5" fill="{c}"></circle>')
    g.append(t(X(2024) + 10, ly[n], f"{lab} {rel[n][2024]:.0f}", 13, c, weight=600))
g.append(f'<circle cx="{X(1995):.1f}" cy="{Y(rel["lp"][1995]):.1f}" r="4" fill="{GOLD}"></circle>')
g.append(t(X(1995) - 8, Y(rel["lp"][1995]) - 12, f"1995: {rel['lp'][1995]:.0f}, euro area ahead of the US", 13, GOLD_D, "end", 600, True))
g.append(t(X(1952), Y(rel["hours_pc"][1960]) - 10, "Europeans worked more hours…", 12.5, US_C, "start", None, True))
g.append(t(X(1952), Y(rel["lp"][1952]) + 22, "…but produced far less per hour", 12.5, GOLD_D, "start", None, True))
out["A"] = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Euro area relative to the US, 1950-2024">' + "".join(g) + "</svg>"

# B. Where the gap comes from, every year 1980-2024: diverging bars of the log contributions, GDP-per-head gap as a line
W, H, L, R, TOP, BOT = 1000, 470, 52, 20, 60, 420
Y0, Y1 = 1980, 2024
slot = (W - L - R) / (Y1 - Y0 + 1); bw = slot * 0.74
vmin, vmax = -30, 10
Yv = lambda v: TOP + (vmax - v) / (vmax - vmin) * (BOT - TOP)
g = [f'<rect x="{L}" y="6" width="13" height="13" rx="2" fill="{GOLD}"></rect>' + t(L + 20, 17.5, "Output per hour", 14),
     f'<rect x="{L + 150}" y="6" width="13" height="13" rx="2" fill="{STONE}"></rect>' + t(L + 170, 17.5, "Hours worked per head", 14),
     f'<line x1="{L + 350}" x2="{L + 378}" y1="12.5" y2="12.5" stroke="{INK}" stroke-width="2.6"></line>' + t(L + 386, 17.5, "Total gap in GDP per head", 14),
     t(W - R, 17.5, "Below zero: euro area behind the US", 13, MUTED, "end")]
for v in range(vmin, vmax + 1, 10):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Yv(v):.1f}" y2="{Yv(v):.1f}" stroke="{BASE if v == 0 else LINE}" stroke-width="{1.4 if v == 0 else 1}"></line>')
    g.append(t(L - 8, Yv(v) + 4.5, f"{v:+d}%".replace("-", "−") if v else "0", 12, MUTED, "end"))
for i, y in enumerate(range(Y0, Y1 + 1)):
    x = L + i * slot + (slot - bw) / 2
    p, h = dec[y]
    neg, pos = 0, 0
    for v, c in ((h, STONE), (p, GOLD)):
        if v < 0:
            g.append(f'<rect x="{x:.1f}" y="{Yv(neg):.1f}" width="{bw:.1f}" height="{Yv(neg + v) - Yv(neg):.1f}" fill="{c}"><title>{y}</title></rect>'); neg += v
        else:
            g.append(f'<rect x="{x:.1f}" y="{Yv(pos + v):.1f}" width="{bw:.1f}" height="{Yv(pos) - Yv(pos + v):.1f}" fill="{c}"><title>{y}</title></rect>'); pos += v
    if y % 5 == 0:
        g.append(t(x + bw / 2, BOT + 22, y, 12.5, MUTED, "middle"))
pts = " ".join(f"{L + i * slot + slot / 2:.1f},{Yv(sum(dec[y])):.1f}" for i, y in enumerate(range(Y0, Y1 + 1)))
g.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"></polyline>')
xc = lambda y: L + (y - Y0) * slot + slot / 2
g.append(t(xc(1995), Yv(dec[1995][0]) - 10, "1995: the gap is all hours", 13, INK, "middle", 600, True))
g.append(t(xc(2024) - 4, Yv(sum(dec[2024])) + 40, f"2024: {share(2024) * 100:.0f}% of the gap", 13, INK, "end", 600, True))
g.append(t(xc(2024) - 4, Yv(sum(dec[2024])) + 57, "is lower output per hour", 13, INK, "end", 600, True))
out["B"] = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Euro area GDP per head gap to the US, split into output per hour and hours worked, 1980-2024">' + "".join(g) + "</svg>"

# C. Then and now: the split of the gap in 1995, 2008 and 2024 (diverging horizontal bars)
W, H, L, R = 1000, 330, 110, 40
rows = (1995, 2008, 2024)
vmin, vmax = -30, 10
Xv = lambda v: L + (v - vmin) / (vmax - vmin) * (W - L - R)
g = [f'<rect x="{L}" y="6" width="13" height="13" rx="2" fill="{GOLD}"></rect>' + t(L + 20, 17.5, "Output per hour", 14),
     f'<rect x="{L + 150}" y="6" width="13" height="13" rx="2" fill="{STONE}"></rect>' + t(L + 170, 17.5, "Hours worked per head", 14),
     f'<rect x="{L + 340}" y="4" width="3" height="17" fill="{INK}"></rect>' + t(L + 352, 17.5, "Total gap in GDP per head", 14)]
for v in range(vmin, vmax + 1, 10):
    g.append(f'<line x1="{Xv(v):.1f}" x2="{Xv(v):.1f}" y1="44" y2="{H - 34}" stroke="{BASE if v == 0 else LINE}" stroke-width="{1.4 if v == 0 else 1}"></line>')
    g.append(t(Xv(v), H - 14, f"{v:+d}%".replace("-", "−") if v else "0 = US level", 12.5, MUTED, "middle"))
for k, y in enumerate(rows):
    yy = 62 + k * 80
    p, h = dec[y]
    g.append(t(L - 16, yy + 25, y, 18, INK, "end", 600))
    neg, pos = 0, 0
    for v, c, lab in ((h, STONE, "hours"), (p, GOLD, "per hour")):
        if v < 0:
            x0, x1 = Xv(neg + v), Xv(neg); neg += v
        else:
            x0, x1 = Xv(pos), Xv(pos + v); pos += v
        g.append(f'<rect x="{x0:.1f}" y="{yy}" width="{x1 - x0:.1f}" height="40" fill="{c}"></rect>')
        if x1 - x0 > 46:
            g.append(t((x0 + x1) / 2, yy + 25, f"{v:+.0f}".replace("-", "−"), 14, INK if c == GOLD else "#FFFFFF" if False else INK, "middle", 600))
    tot = p + h
    g.append(f'<rect x="{Xv(tot) - 1.5:.1f}" y="{yy - 6}" width="3" height="52" fill="{INK}"></rect>')
    g.append(t(Xv(tot) - 8, yy - 10, f"GDP per head {tot:+.0f}%".replace("-", "−"), 12.5, INK, "end", 600))
out["C"] = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Euro area GDP per head gap to the US in 1995, 2008 and 2024, split into output per hour and hours worked">' + "".join(g) + "</svg>"

# D. Growth since 2000 (2000 = 100): euro area vs US, GDP per head and output per hour
W, H, L, R, TOP, BOT = 1000, 440, 52, 230, 30, 400
X = lambda y: L + (y - 2000) / 24 * (W - L - R)
Y = lambda v: BOT - (v - 95) / (150 - 95) * (BOT - TOP)
g = []
for v in range(100, 151, 10):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 100 else LINE}"></line>' + t(L - 8, Y(v) + 4.5, v, 12, MUTED, "end"))
for y in range(2000, 2025, 4):
    g.append(t(X(y), BOT + 22, y, 12.5, MUTED, "middle"))
idx = lambda D, n, y: D[n][y] / D[n][2000] * 100
lines = (("lp", US, US_C, "US, output per hour", "none"), ("gdp_pc", US, US_C, "US, GDP per head", "6 5"),
         ("lp", ZE, GOLD, "Euro area, output per hour", "none"), ("gdp_pc", ZE, GOLD, "Euro area, GDP per head", "6 5"))
lab_y = {}
for n, D, c, lab, dash in lines:
    pts = " ".join(f"{X(y):.1f},{Y(idx(D, n, y)):.1f}" for y in range(2000, 2025))
    g.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2.8" stroke-dasharray="{dash}" stroke-linejoin="round"></polyline>')
    v = idx(D, n, 2024)
    g.append(f'<circle cx="{X(2024):.1f}" cy="{Y(v):.1f}" r="3.5" fill="{c}"></circle>')
    g.append(t(X(2024) + 10, Y(v) + 4.5, f"{lab} +{v - 100:.0f}%", 13, GOLD_D if c == GOLD else US_C, weight=600))
out["D"] = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Growth since 2000, euro area vs US: GDP per head and output per hour">' + "".join(g) + "</svg>"

json.dump(out, open("site/gap_options.json", "w"), ensure_ascii=False)
for y in (1995, 2008, 2023, 2024):
    print(y, {k: round(v[y], 1) for k, v in rel.items()}, [round(x, 1) for x in dec[y]], round(share(y) * 100))
for n in ("gdp_pc", "lp"):
    print(n, "since 2000: ZE +%.0f%%, US +%.0f%%" % (ZE[n][2024] / ZE[n][2000] * 100 - 100, US[n][2024] / US[n][2000] * 100 - 100))
