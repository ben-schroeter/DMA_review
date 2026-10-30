"""Statista-style square infographic (1200x1200), same frame as the others: HQ migration between Europe and the US by funding raised.
Data: Reichardt & Reis (2026), Figure 1, values measured from the published chart (as in build_why_charts.py, chart 9).
Writes site/infographics/hq_migration.svg. Run from research/ceps_metrics."""
import os

INK, INK2, MUTED, LINE, BASE = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3"
GOLD, GOLD_D, SLATE, BG = "#B8860B", "#8F6708", "#5C5858", "#FAF9F5"
SANS = 'font-family="DM Sans, sans-serif"'
SERIF = "font-family=\"'Source Serif 4', Georgia, serif\""
W = H = 1200


def t(x, y, txt, size, fill=INK2, anchor="start", weight=400, font=SANS, halo=False):
    h = f' stroke="{BG}" stroke-width="6" paint-order="stroke"' if halo else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {font} font-size="{size}" font-weight="{weight}" fill="{fill}"{h}>{txt}</text>'


hq = [("No funding", 1.9, 0.7), ("Under $1m", 2.9, 1.0), ("$1–10m", 6.5, 0.8), ("$10–100m", 9.9, 0.8), ("Over $100m", 10.7, 0.8)]
avg_eu, avg_us = 3.3, 0.8

g = [f'<rect width="{W}" height="{H}" fill="{BG}"></rect>', f'<rect width="{W}" height="10" fill="{GOLD}"></rect>']
for i, line in enumerate(("The more a European start-up raises,", "the more likely it is to leave.")):
    g.append(t(56, 112 + 60 * i, line, 50, INK, weight=700))
g.append(t(56, 228, "Share of firms under ten years old that moved their headquarters between", 24, MUTED))
g.append(t(56, 260, "Europe and the US, 2014–2024, by total funding raised", 24, MUTED))
g.append(f'<rect x="56" y="300" width="20" height="20" rx="3" fill="{GOLD}"></rect>' + t(86, 317, "Europe to US", 21, INK2))
g.append(f'<rect x="246" y="300" width="20" height="20" rx="3" fill="{SLATE}"></rect>' + t(276, 317, "US to Europe", 21, INK2))
g.append(f'<line x1="436" x2="476" y1="310" y2="310" stroke="{MUTED}" stroke-width="2" stroke-dasharray="7 6"></line>' + t(488, 317, "average across all firms", 21, MUTED))
# chart
L, R, TOP, BOT = 104, 56, 380, 960
ymax = 12
Yh = lambda v: BOT - v / ymax * (BOT - TOP)
slot = (W - L - R) / len(hq); bw = 82
for v in range(0, ymax + 1, 2):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Yh(v):.1f}" y2="{Yh(v):.1f}" stroke="{BASE if v == 0 else LINE}" stroke-width="{1.6 if v == 0 else 1}"></line>')
    g.append(t(L - 14, Yh(v) + 7, f"{v}%", 19, MUTED, "end"))
for val, c in ((avg_eu, GOLD), (avg_us, SLATE)):
    g.append(f'<line x1="{L}" x2="{W - R}" y1="{Yh(val):.1f}" y2="{Yh(val):.1f}" stroke="{c}" stroke-width="2" stroke-dasharray="7 6"></line>')
for i, (lab, e, u) in enumerate(hq):
    x = L + i * slot + slot / 2
    for val, c, dx in ((e, GOLD, -bw - 4), (u, SLATE, 4)):
        g.append(f'<rect x="{x + dx:.1f}" y="{Yh(val):.1f}" width="{bw}" height="{BOT - Yh(val):.1f}" fill="{c}"></rect>')
        g.append(t(x + dx + bw / 2, Yh(val) - 12, f"{val:.1f}%", 22 if c == GOLD else 18, INK if c == GOLD else INK2, "middle", 700 if c == GOLD else 500, halo=True))
    g.append(t(x, BOT + 34, lab, 20, INK2, "middle", 500))
g.append(t(L + (W - L - R) / 2, BOT + 66, "Total external funding raised by 2024", 18, MUTED, "middle"))
# callout
cx, cy, cw, ch = L + 24, TOP + 20, 500, 140
g.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="#FFFFFF" stroke="{LINE}"></rect>')
g.append(t(cx + 24, cy + 92, "1 in 10", 58, GOLD, weight=700, font=SERIF))
g.append(t(cx + 224, cy + 44, "European start-ups that", 20, INK2))
g.append(t(cx + 224, cy + 72, "raised over $100m moved", 20, INK2))
g.append(t(cx + 224, cy + 100, "to the US; under 1% of US", 20, INK2))
g.append(t(cx + 224, cy + 128, "firms moved to Europe", 20, INK2))
# footer
g.append(f'<line x1="56" x2="{W - 56}" y1="1066" y2="1066" stroke="{LINE}"></line>')
for i, line in enumerate(("Europe = the 27 EU countries and the UK. Based on 173,712 firms in matched Crunchbase snapshots of 2014 and 2024; tech",
                          "start-ups are over-represented, so rates are likely higher than for firms in general. Values measured from the published",
                          "chart (H. Reichardt and R. Reis, “Why Do Firms Prefer the US over the EU?”, June 2026, Figure 1).")):
    g.append(t(56, 1100 + 24 * i, line, 16, MUTED))
g.append(f'<g transform="translate({W - 330},1160)"><rect x="0" y="0" width="22" height="22" rx="3" fill="none" stroke="{INK}" stroke-width="1.6"></rect>'
         f'<path d="M5 15h12M5 11h12M5 7h7" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"></path></g>')
g.append(t(W - 298, 1178, "The EU Digital Rulebook", 22, INK, font=SERIF))
g.append(t(56, 1180, f'Source: Reichardt &amp; Reis (2026) · <tspan fill="{GOLD}" font-weight="700" font-size="18">eutechlaws.org</tspan>', 16, INK2, weight=500))

aria = ("The more a European start-up raises, the more likely it is to leave. Share of firms under ten years old that moved their headquarters, 2014-2024: "
        "Europe to US 1.9% with no funding, 2.9% under $1m, 6.5% at $1-10m, 9.9% at $10-100m, 10.7% over $100m (average 3.3%); "
        "US to Europe 0.7% to 1.0% at every funding level (average 0.8%).")
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"
os.makedirs("site/infographics", exist_ok=True)
open("site/infographics/hq_migration.svg", "w").write(svg)
