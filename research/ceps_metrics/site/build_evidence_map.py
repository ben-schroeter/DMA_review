"""Evidence map charts from data/evidence_map/cells.json (scripts/evidence_map.py).
  site/evidence_map_compact.svg  policy area x kind of effect, for the Evidence page
  site/evidence_map_full.svg     every adopted law x kind of effect, for the Studies page
Cell colour = strongest evidence found (causal study, other after-the-fact evidence, forecast only, nothing).
Run from research/ceps_metrics."""
import collections, csv, html, json

INK, INK2, MUTED, LINE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#FAF9F5"
GOLD_D, GOLD_L, STONE = "#8F6708", "#E3CF9C", "#A6A3A0"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
esc = lambda s: html.escape(str(s), quote=False)
HEAD = {"costs": ("Compliance", "costs"), "consumers": ("Prices and", "consumers"), "competition": ("Competition", ""),
        "innovation": ("Innovation and", "investment"), "growth": ("Growth", "and jobs"), "market": ("Single market,", "trade and FDI"),
        "rights": ("Rights, safety", "and security"), "implementation": ("Implemen-", "tation")}
SHORT = {"E-commerce & Consumer Protection": "E-commerce & consumer", "Competition & Single Market": "Competition & single market",
         "Data & Privacy": "Data & privacy", "Trust & Safety": "Trust & safety", "Industrial Policy": "Industrial policy",
         "Law Enforcement": "Law enforcement", "Research & Innovation": "Research & innovation", "IPR": "Intellectual property"}
HEAD_FULL = {"costs": ("Compliance", "costs"), "consumers": ("Prices,", "consumers"), "competition": ("Compe-", "tition"),
             "innovation": ("Innovation,", "investment"), "growth": ("Growth,", "jobs"), "market": ("Single mkt,", "trade, FDI"),
             "rights": ("Rights,", "safety"), "implementation": ("Implemen-", "tation")}
FILL = {"causal": (GOLD_D, "#FFFFFF"), "measured": (GOLD_L, INK), "forecast": ("url(#hatch)", INK2), None: ("#FFFFFF", STONE)}
DEFS = (f'<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="6" height="6" fill="#FFFFFF"></rect><line x1="0" y1="0" x2="0" y2="6" stroke="{STONE}" stroke-width="2"></line></pattern></defs>')

d = json.load(open("data/evidence_map/cells.json"))
K = [k for k, _ in d["categories"]]
NAME = dict(d["categories"])
INST = d["instruments"]
titles, grades = {}, {}
for r in csv.DictReader(open("data/evidence_map/sources_tagged.csv")):
    titles[r["id"]] = (r["title"] or "").strip()
    grades[r["id"]] = r["grade"]


def legend(g, y, W):
    x = 0
    for gr, lab in [("causal", "Causal study"), ("measured", "Other evaluation or study"), ("forecast", "Forecast only"), (None, "Nothing found")]:
        f, _ = FILL[gr]
        g.append(f'<rect x="{x}" y="{y}" width="14" height="14" rx="2" fill="{f}" stroke="{LINE if gr is None or gr == "forecast" else f}"></rect>' + t(x + 20, y + 12, lab, 13))
        x += 34 + len(lab) * 7.2


def headers(g, L, CW, y, H=HEAD):
    for j, k in enumerate(K):
        a, b = H[k]
        cx = L + j * CW + CW / 2
        g.append(t(cx, y, a, 13, INK, "middle", 600) + (t(cx, y + 16, b, 13, INK, "middle", 600) if b else ""))


def cell(g, x, y, w, h, best, label, title, size=13):
    f, tc = FILL[best]
    stroke = LINE if best in (None, "forecast") else BG
    g.append(f'<rect x="{x + 1.5:.1f}" y="{y + 1.5:.1f}" width="{w - 3:.1f}" height="{h - 3:.1f}" rx="3" fill="{f}" stroke="{stroke}"><title>{esc(title)}</title></rect>')
    if label:
        g.append(t(x + w / 2, y + h / 2 + size * 0.36, label, size, tc, "middle", 600 if best in ("causal", "measured") else None).replace("<text", '<text pointer-events="none"'))


# ---------- compact: policy area x effect ----------
areas = collections.defaultdict(list)
for n, v in INST.items():
    areas[v["policy_area"]].append((n, v))
order = sorted(areas, key=lambda a: (-len(areas[a]), a))
W, L, CW, RH = 1000, 214, 98, 44
g = [DEFS]
legend(g, 0, W)
TOP = 70
headers(g, L, CW, TOP - 14)
for i, a in enumerate(order):
    y = TOP + 12 + i * RH
    vs = areas[a]
    g.append(t(L - 14, y + 31, esc(SHORT.get(a, a)), 14.5, INK, "end", 500))
    for j, k in enumerate(K):
        cs = [v["cells"][k] for _, v in vs]
        ca = sum(c["causal"] > 0 for c in cs)
        ev = sum(c["causal"] + c["measured"] > 0 for c in cs)
        fo = sum(c["n"] > 0 and c["causal"] + c["measured"] == 0 for c in cs)
        title = (f"{a} · {NAME[k]}: {ev} of {len(vs)} laws have after-the-fact evidence"
                 + (f", {ca} with a causal study" if ca else "") + (f"; {fo} forecast only" if fo else "") + ".")
        laws = [n for n, v in vs if v["cells"][k]["causal"] + v["cells"][k]["measured"]]
        if laws:
            title += " " + "; ".join(laws[:8]) + (f" and {len(laws) - 8} more" if len(laws) > 8 else "")
        x0, bw, by = L + j * CW + 6, CW - 12, y + 21
        g.append(f'<g><title>{esc(title)}</title><rect x="{x0}" y="{by}" width="{bw}" height="13" rx="2" fill="#FFFFFF" stroke="{LINE}"></rect>')
        x = x0
        for cnt, gr in [(ca, "causal"), (ev - ca, "measured"), (fo, "forecast")]:
            if cnt:
                w = bw * cnt / len(vs)
                g.append(f'<rect x="{x:.1f}" y="{by}" width="{w:.1f}" height="13" fill="{FILL[gr][0]}" stroke="{BG if gr != 'forecast' else LINE}" stroke-width="0.75"></rect>')
                x += w
        g.append(t(x0, y + 14, f"{ev} of {len(vs)}", 12.5, INK if ev else MUTED, "start", 600 if ev else None) + "</g>")
H = TOP + 12 + len(order) * RH + 10
tot = sum(len(v) for v in areas.values())
aria = (f"Evidence map: for {tot} adopted laws in {len(order)} policy areas and eight kinds of effect, the strongest evidence found. "
        f"Each cell gives the number of laws in the area with after-the-fact evidence on that effect.")
svg = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"
open("site/evidence_map_compact.svg", "w").write(svg)

# ---------- full: law x effect ----------
W, L, CW, RH, AH = 1000, 344, 82, 24, 34
g = [DEFS]
legend(g, 0, W)
TOP = 70
headers(g, L, CW, TOP - 14, HEAD_FULL)
y = TOP + 6
for a in order:
    g.append(f'<line x1="0" x2="{L + len(K) * CW}" y1="{y + AH - 6}" y2="{y + AH - 6}" stroke="{LINE}"></line>' + t(0, y + AH - 13, esc(SHORT.get(a, a)).upper(), 11.5, MUTED, "start", 600).replace("<text", '<text letter-spacing="1"'))
    y += AH
    for n, v in sorted(areas[a], key=lambda x: -(x[1]["obligations"] or 0)):
        lab = n if len(n) <= 44 else n[:42].rstrip() + "…"
        g.append(t(L - 12, y + RH / 2 + 4.5, esc(lab) + (f"<title>{esc(n)}</title>" if lab != n else ""), 13, INK, "end"))
        for j, k in enumerate(K):
            c = v["cells"][k]
            title = f"{n} · {NAME[k]}: "
            if c["n"]:
                parts = [f"{c[gr]} {lab2}" for gr, lab2 in [("causal", "causal"), ("measured", "other after-the-fact"), ("forecast", "forecast")] if c[gr]]
                title += ", ".join(parts) + ". " + " | ".join(("Causal: " if grades.get(i) == "causal" else "") + titles.get(i, "")[:90]
                                                     for i in sorted(c["ids"], key=lambda i: ["causal", "measured", "forecast"].index(grades.get(i, "forecast")))[:6]) + (f" | and {len(c['ids']) - 6} more" if len(c["ids"]) > 6 else "")
            else:
                title += "nothing found."
            cell(g, L + j * CW, y, CW, RH, c["best"], str(c[c["best"]]) if c["best"] else "", title, 12)
        y += RH
H = y + 8
aria = f"Evidence map for {tot} adopted laws and eight kinds of effect: strongest evidence found and number of sources in each cell."
svg = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>"
open("site/evidence_map_full.svg", "w").write(svg)
print("compact", len(order), "areas; full height", H)
