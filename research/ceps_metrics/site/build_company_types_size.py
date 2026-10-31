"""Chart for the company-types page: obligations specific to each type of company against the size of the sectors behind it.
Size from Eurostat (fetched live): persons employed and number of enterprises from structural business statistics
(sbs_ovw_act), total EU employment from national accounts (nama_10_a64_e).
Sectors per type (chosen not to overlap):
  TC telecoms                         J61
  FI finance, payments and crypto     K64-K66
  PL online platforms and services    J63.12 web portals + G47.91 retail via internet
  CL cloud, data and AI               J62 programming and consultancy + J63.11 data processing and hosting
  PR makers of connected products     C26-C29 electronics, electrical equipment, machinery, vehicles
Gatekeepers and very large platforms are a few dozen named companies, not a sector, so they are not plotted.
Writes data/company_types/eurostat_size.json, site/company_types_size.svg (against employment) and
site/company_types_firmsize.svg (against average firm size). Run from research/ceps_metrics."""
import itertools, json, urllib.request

B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"


def get(ds, **kw):
    q = "&".join(f"{k}={v}" for k, vs in kw.items() for v in (vs if isinstance(vs, list) else [vs]))
    d = json.load(urllib.request.urlopen(B + ds + "?" + q, timeout=60))
    cats = [sorted(d["dimension"][i]["category"]["index"].items(), key=lambda x: x[1]) for i in d["id"]]
    return {tuple(c[0] for c in combo): d["value"][str(i)] for i, combo in enumerate(itertools.product(*cats)) if str(i) in d["value"]}


SECT = {"TC": ["J61"], "FI": ["K64-K66"], "PL": ["J6312", "G4791"], "CL": ["J62", "J6311"], "PR": ["C26", "C27", "C28", "C29"]}
codes = sorted({c for v in SECT.values() for c in v}) + ["B-S_X_O_S94"]
size = {}
for yr in ("2023", "2022"):          # latest year first; fill gaps from the year before
    o = get("sbs_ovw_act", geo="EU27_2020", time=yr, nace_r2=codes, indic_sbs=["ENT_NR", "EMP_NR"])
    for (_, n, ind, _, _), v in o.items():
        size.setdefault(n, {}).setdefault(ind, (v, int(yr)))
o = get("nama_10_a64_e", geo="EU27_2020", unit="THS_PER", na_item="EMP_DC", time="2023", nace_r2=["TOTAL"])
for k, v in o.items():
    size.setdefault(k[2], {})["EMP_NR"] = (v * 1000, 2023)
tot = size.pop("TOTAL")["EMP_NR"][0]
ct = json.load(open("data/company_types/summary.json"))
out = {"total_employment_eu27_2023": tot, "nace": size, "types": {}}
for k, cs in SECT.items():
    emp = sum(size[c]["EMP_NR"][0] for c in cs)
    ent = sum(size[c]["ENT_NR"][0] for c in cs)
    out["types"][k] = {"name": ct["names"][k], "nace": cs, "employment": emp, "enterprises": ent,
                       "share_of_eu_jobs": emp / tot, "avg_firm_size": emp / ent, "obligations": ct["types"][k]["obligations"]}
out["baseline_obligations"] = ct["baseline"]["obligations"]
json.dump(out, open("data/company_types/eurostat_size.json", "w"), indent=1)

INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD, GOLD_D = "#B8860B", "#8F6708"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=13, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                      + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
W, H, L, R, T, Bm = 1000, 470, 70, 960, 30, 60
XM, YM = 9, 4000
X = lambda v: L + v / XM * (R - L)
Y = lambda v: H - Bm - v / YM * (H - Bm - T)
g = []
for v in range(0, YM + 1, 1000):
    g.append(f'<line x1="{L}" x2="{R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>' + t(L - 10, Y(v) + 4.5, f"{v:,}", 13, MUTED, "end"))
for v in range(0, XM + 1):
    g.append(t(X(v), H - Bm + 22, f"{v}m" if v else "0", 13, MUTED, "middle"))
g.append(t(L, T - 12, "Obligations aimed at this type of company", 13, MUTED))
g.append(t(R, H - 12, "People employed in the EU in the sectors behind it", 13, MUTED, "end"))
SHORT = {"TC": "Telecoms", "FI": "Finance, payments and crypto", "PL": "Online platforms and digital services", "CL": "Cloud, data and AI",
         "PR": "Makers of connected products"}
POS = {"TC": ("start", 12, -8), "FI": ("start", 12, 5), "PL": ("start", 14, 30), "CL": ("start", 12, 5), "PR": ("end", -12, -14)}
for k, v in out["types"].items():
    x, y = X(v["employment"] / 1e6), Y(v["obligations"])
    g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{GOLD}" stroke="{BG}" stroke-width="2"><title>{SHORT[k]}: {v["obligations"]:,} obligations; '
             f'{v["employment"] / 1e6:.1f} million people employed ({v["share_of_eu_jobs"]:.1%} of EU jobs)</title></circle>')
    a, dx, dy = POS[k]
    g.append(t(x + dx, y + dy, SHORT[k], 14, INK, a, 600))
    g.append(t(x + dx, y + dy + 17, f'{v["obligations"]:,} obligations · {v["share_of_eu_jobs"]:.1%} of EU jobs', 12.5, MUTED, a))
aria = "Obligations aimed at each type of company against people employed in the EU in its sectors: " + "; ".join(
    f'{SHORT[k]} {v["obligations"]:,} obligations, {v["employment"] / 1e6:.1f} million people' for k, v in out["types"].items())
open("site/company_types_size.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
for k, v in out["types"].items():
    print(k, v["nace"], f'{v["employment"]:,.0f}', v["enterprises"], f'{v["share_of_eu_jobs"]:.2%}', v["obligations"], f'{v["obligations"] / (v["employment"] / 1e6):.0f} per m jobs')
print("total jobs", tot, "covered share", sum(v["share_of_eu_jobs"] for v in out["types"].values()))

# second chart: against average firm size (persons employed per enterprise), log scale
import math
biz = size["B-S_X_O_S94"]; avg_all = biz["EMP_NR"][0] / biz["ENT_NR"][0]
out["business_economy_avg_firm_size"] = avg_all
json.dump(out, open("data/company_types/eurostat_size.json", "w"), indent=1)
X0, X1 = 1, 100
XL = lambda v: L + (math.log10(v) - math.log10(X0)) / (math.log10(X1) - math.log10(X0)) * (R - L)
g = []
for v in range(0, YM + 1, 1000):
    g.append(f'<line x1="{L}" x2="{R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{BASE if v == 0 else LINE}"></line>' + t(L - 10, Y(v) + 4.5, f"{v:,}", 13, MUTED, "end"))
for v in (1, 2, 5, 10, 20, 50, 100):
    g.append(t(XL(v), H - Bm + 22, str(v), 13, MUTED, "middle"))
g.append(f'<line x1="{XL(avg_all):.1f}" x2="{XL(avg_all):.1f}" y1="{T}" y2="{H - Bm}" stroke="{MUTED}" stroke-dasharray="3 4"></line>')
g.append(t(XL(avg_all) + 6, T + 12, f"Average EU firm: {avg_all:.1f} people", 12.5, MUTED))
g.append(t(L, T - 12, "Obligations aimed at this type of company", 13, MUTED))
g.append(t(R, H - 12, "Average number of people per firm in the sectors behind it (log scale)", 13, MUTED, "end"))
POS2 = {"TC": ("start", 12, 5), "FI": ("start", 12, 5), "PL": ("start", 12, 26), "CL": ("start", 12, -16), "PR": ("end", -12, -14)}
for k, v in out["types"].items():
    x, y = XL(v["avg_firm_size"]), Y(v["obligations"])
    g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{GOLD}" stroke="{BG}" stroke-width="2"><title>{SHORT[k]}: {v["obligations"]:,} obligations; '
             f'{v["enterprises"]:,.0f} firms, {v["avg_firm_size"]:.1f} people per firm on average</title></circle>')
    a, dx, dy = POS2[k]
    g.append(t(x + dx, y + dy, SHORT[k], 14, INK, a, 600))
    g.append(t(x + dx, y + dy + 17, (f'{v["enterprises"] / 1e6:.2f}m' if v["enterprises"] >= 1e6 else f'{v["enterprises"] / 1000:,.0f}k') + f' firms · {v["avg_firm_size"]:.1f} people per firm', 12.5, MUTED, a))
aria = "Obligations aimed at each type of company against the average number of people per firm in its sectors: " + "; ".join(
    f'{SHORT[k]} {v["obligations"]:,} obligations, {v["avg_firm_size"]:.1f} people per firm' for k, v in out["types"].items())
open("site/company_types_firmsize.svg", "w").write(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">' + "".join(g) + "</svg>")
for k, v in out["types"].items():
    print(k, f'{v["enterprises"]:,.0f} firms', f'{v["avg_firm_size"]:.1f} per firm')
print("business economy", f"{avg_all:.1f}")
