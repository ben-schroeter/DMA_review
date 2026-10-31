"""Chart for the company page: what size-based relief does to the obligations on companies, each obligation counted once,
in priority order: removed for small firms by an SME exemption, removed by a turnover threshold (rules that only reach large
firms), lightened (still applies in simpler or less frequent form), lower fines only, unchanged. Obligations that apply only
to designated firms are left out (they are counted in the firm-size chart). Uses the coding in scripts/firm_size.py.
Writes site/firm_relief.svg and data/firm_size/relief.json. Run from research/ceps_metrics."""
import json, re

exec(open("scripts/firm_size.py").read().split("def staircase")[0])     # rows, M, min_band, RULES, bands, art(), text()
rid = lambda s: next(k for k, v in by_id.items() if v["name"] and s in v["name"])
THRESH = {rid("EC Merger Regulation"), rid("Foreign Subsidies Regulation"), rid("Critical Raw Materials")}
LIGHT = [(rid("General Data Protection"), lambda r: r["kind"] == "main" and art(r) == 30),
         (rid("Artificial Intelligence"), lambda r: r["kind"] == "main" and art(r) == 17),
         (rid("Cyber Resilience"), lambda r: r["kind"] == "main" and (art(r) == 31 or (r.get("article") or "").lower().startswith("annex vii"))),
         (rid("Copyright in the Digital"), lambda r: r["kind"] == "main" and art(r) == 17),
         (rid("Platform Work"), lambda r: r["kind"] == "main" and art(r) == 17),
         (rid("Short-Term Rental"), lambda r: r["kind"] == "main" and art(r) == 9),
         (rid("Operational Resilience"), lambda r: "microenterprise" in text(r) and "other than microenterprise" not in text(r))]
FINES = {rid(s) for s in ("Artificial Intelligence", "Cyber Resilience", "European Chips", "Single Market Emergency", "Compulsory licensing")}

cnt = {"removed": 0, "threshold": 0, "lightened": 0, "fines": 0, "unchanged": 0}
for r in rows:
    if r["row_id"] not in M:
        continue
    b, _ = min_band(r)
    if b == DESIG:
        continue
    if r["row_id"] in THRESH and b > MICRO:
        cnt["threshold"] += 1
    elif b > MICRO:
        cnt["removed"] += 1
    elif any(r["row_id"] == k and f(r) for k, f in LIGHT):
        cnt["lightened"] += 1
    elif r["row_id"] in FINES:
        cnt["fines"] += 1
    else:
        cnt["unchanged"] += 1
tot = sum(cnt.values())
json.dump({"total": tot, **cnt}, open("data/firm_size/relief.json", "w"), indent=1)

INK, INK2, MUTED, LINE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#FAF9F5"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
DEFS = ('<defs><pattern id="hr" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#FFFFFF"></rect>'
        '<line x1="0" y1="0" x2="0" y2="6" stroke="#B8860B" stroke-width="2"></line></pattern></defs>')
SEG = [("removed", "Removed by an SME exemption", "#8F6708", "#FFFFFF"),
       ("threshold", "Removed by a turnover threshold", "#B8860B", "#FFFFFF"),
       ("lightened", "Lightened", "#E3CF9C", INK),
       ("fines", "Lower fines only", "url(#hr)", INK),
       ("unchanged", "Unchanged", "#D4D2CE", INK)]
W, BH, Y0 = 1000, 46, 30
g = [DEFS, t(0, 16, f"What size-based relief does to the {tot:,} obligations a large company faces, for a firm with fewer than 10 staff", 14, INK, "start", 600)]
x = 0
for k, lab, col, tc in SEG:
    w = cnt[k] / tot * W
    g.append(f'<rect x="{x:.1f}" y="{Y0}" width="{w:.1f}" height="{BH}" fill="{col}" stroke="{BG}" stroke-width="1.5"><title>{lab}: {cnt[k]:,} ({cnt[k] / tot:.1%})</title></rect>')
    if k == "unchanged":
        g.append(t(x + w - 14, Y0 + 29, f"{cnt[k] / tot:.0%} unchanged", 16, INK, "end", 700))
    x += w
# legend with shares below the bar
lx, ly = 0, Y0 + BH + 28
for k, lab, col, tc in SEG:
    item = f"{lab} {cnt[k] / tot:.1%}"
    g.append(f'<rect x="{lx}" y="{ly - 11}" width="13" height="13" rx="2" fill="{col}" stroke="{LINE if col.startswith("url") else col}"></rect>' + t(lx + 19, ly, item, 13))
    lx += 38 + len(item) * 6.9
H = ly + 12
aria = "Obligations on companies for a firm with fewer than 10 staff: " + "; ".join(f"{lab} {cnt[k]:,} ({cnt[k] / tot:.1%})" for k, lab, *_ in SEG)
open("site/firm_relief.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
print(tot, cnt, {k: round(v / tot * 100, 1) for k, v in cnt.items()})
