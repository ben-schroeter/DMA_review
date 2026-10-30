"""Evidence map: for each adopted instrument and each of eight kinds of effect, the strongest evidence found and how many sources.

Sources are the literature records in data/impact/*.json (the same records behind the Studies and Evidence pages).
  grade     causal   = an evidence source with a causal design (same test as build_studies_data.py / build_workbook.py)
            measured = any other evidence source (evaluations, audits, statistics, descriptive and survey studies)
            forecast = an ex-ante assessment (impact assessment, proposal estimates)
  outcomes  the free-text 'outcomes' field (plus the headline when it is empty), mapped to eight categories by keywords;
            one source can count for several categories.
Enforcement decisions and case law are not evidence and are left out, as on the Evidence page.
Writes data/evidence_map/cells.json, sources_tagged.csv and summary.json. Run from research/ceps_metrics."""
import collections, csv, json, os, re
import openpyxl

CATS = [
    ("costs", "Compliance costs and burden", r"compliance cost|cost of compliance|compliance burden|administrative (cost|burden)|business cost|\bcosts?\b|burden|red tape|overhead"),
    ("consumers", "Prices and consumers", r"\bprices?\b|pricing|consumer|tariff|retail|roaming charge|\bbills?\b|customer savings|welfare|financial exclusion|surplus|detriment|\bchoice|quality of service|user experience|traffic|visits?\b|visitors|clicks|bookings?|news consumption"),
    ("competition", "Competition and market structure", r"competition|competitive|market concentration|concentration on|level playing field|market share|\bentry|entrant|switching|contestab|self-preferenc|merger|market structure|dominan|gatekeeper|interoperab|lock-in|market power|\brivals?\b"),
    ("innovation", "Innovation and investment", r"innovat|investment|\binvest\b|r&d|\bresearch|patent|venture|start-?up|funding|\bcapital\b|technolog|deployment|adoption|ai uptake|connectivity|coverage|digitali[sz]|digital maturity|skills|datasets?|database"),
    ("growth", "Growth and jobs", r"\bgdp\b|growth|employment|\bjobs?\b|productivity|\boutput\b(?! indicator)|\bsales\b|(?<!tax )(?<!vat )revenue|turnover|exports?|value added|economic (impact|value)|competitiveness|profit|firm performance|conversion|survival|monetiz|\breturns\b(?! behav)|volatility|trading volume|bond spreads"),
    ("market", "Single market, trade and FDI", r"single market|cross-border|internal market|\btrade\b|fragmentation|harmoni[sz]|geo-?block|market integration|barrier|\bfdi\b|foreign (direct )?invest|acquisitions?|\bm&a\b"),
    ("rights", "Rights, safety and security", r"privacy|data protection|fundamental right|safety|cyber|security\b|fraud|incident|\bharms?\b|harmful|illegal content|disinformation|\bchild|terror|crime|\btrust\b|accessib|freedom|pluralism|moderat(ion|or)|minors|threat|takedown|propaganda|political ad|violence|csam|tracking|consent"),
    ("implementation", "Implementation and enforcement", r"enforce|complian(ce|t)\b(?! (cost|burden))|transpos|implement|uptake|awareness|take-up|governance|supervis|sanction|\bfines?\b|legal certainty|effectiveness|efficiency|coherence|relevance|monitoring|cooperation|litigation|transparen|absorption|disburs|budget|delays|milestone|notif|designat|registr|readiness|data quality|preparation|perception|threshold|(?<!web )(?<!and )referrals?\b(?! (web|traffic))|collected|participation|beneficiar|services delivered|alerts|access requests|screening"),
]
CAUSAL_SRC = open("scripts/build_workbook.py").read()
CAUSAL = eval(re.search(r"^CAUSAL = (\(.*?\)|\[.*?\])$", CAUSAL_SRC, re.M | re.S).group(1))


def is_causal(m):
    did = bool(re.search(r"\bDiD\b|\bDID\b", m)); m = m.lower()
    return (did or any(k in m for k in CAUSAL)) and "non-causal" not in m and "not causal" not in m


def grade(l):
    if l.get("category") == "ex-ante assessment":
        return "forecast"
    if l.get("category") != "evidence":
        return None
    return "causal" if is_causal(l.get("method") or "") else "measured"


def cats(l):
    text = (l.get("outcomes") or "").lower() or (l.get("headline") or "").lower()
    found = [k for k, _, p in CATS if re.search(p, text)]
    if not found and l.get("outcomes"):
        found = [k for k, _, p in CATS if re.search(p, (l.get("headline") or "").lower())]
    return found


wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values); h = rows[0]
inst = [dict(zip(h, r)) for r in rows[1:] if r[0]]
RANK = {"causal": 3, "measured": 2, "forecast": 1}
cells, tagged, untagged = {}, [], 0
for r in inst:
    if r["status_oct2026"] != "adopted" or not r["celex_measured"]:
        continue
    c = r["celex_measured"].split(";")[0]
    try:
        rec = json.load(open(f"data/impact/{c}.json"))
    except FileNotFoundError:
        continue
    row = {k: {"best": None, "n": 0, "causal": 0, "measured": 0, "forecast": 0, "ids": []} for k, _, _ in CATS}
    for l in rec.get("literature") or []:
        gr = grade(l)
        if not gr:
            continue
        ks = cats(l)
        if not ks:
            untagged += 1
        tagged.append({"instrument": r["name"], "id": l.get("id"), "grade": gr, "categories": ";".join(ks), "outcomes": l.get("outcomes"), "title": l.get("title")})
        for k in ks:
            cell = row[k]
            cell["n"] += 1; cell[gr] += 1; cell["ids"].append(l.get("id"))
            if cell["best"] is None or RANK[gr] > RANK[cell["best"]]:
                cell["best"] = gr
    cells[r["name"]] = {"policy_area": r["policy_area_ceps"], "row_id": r["row_id"], "year": int(str(r["adoption_date"])[:4]) if r["adoption_date"] else None,
                        "obligations": r["restrictions_total"], "cells": row}
os.makedirs("data/evidence_map", exist_ok=True)
json.dump({"categories": [(k, n) for k, n, _ in CATS], "instruments": cells}, open("data/evidence_map/cells.json", "w"), indent=1, ensure_ascii=False)
with open("data/evidence_map/sources_tagged.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(tagged[0].keys())); w.writeheader(); w.writerows(tagged)
# summary: per category, how many instruments have causal / measured / forecast-only / nothing
summ = {}
for k, n, _ in CATS:
    best = collections.Counter(v["cells"][k]["best"] or "none" for v in cells.values())
    summ[k] = {"name": n, **best}
V, core = cells.values(), ["costs", "consumers", "competition", "innovation", "growth"]
ev = lambda c: c["causal"] + c["measured"] > 0
json.dump({"instruments": len(cells), "sources": len(tagged), "sources_without_category": untagged, "by_category": summ,
           "pairs": len(V) * len(CATS), "pairs_evidence": sum(ev(c) for v in V for c in v["cells"].values()),
           "pairs_causal": sum(c["causal"] > 0 for v in V for c in v["cells"].values()), "core_pairs": len(V) * len(core),
           "core_evidence": sum(ev(v["cells"][k]) for v in V for k in core), "core_causal": sum(v["cells"][k]["causal"] > 0 for v in V for k in core)},
          open("data/evidence_map/summary.json", "w"), indent=1)
print("instruments", len(cells), "sources", len(tagged), "untagged", untagged)
for k, v in summ.items():
    print(f"{v['name']:34s} causal {v.get('causal',0):3d} measured {v.get('measured',0):3d} forecast-only {v.get('forecast',0):3d} none {v.get('none',0):3d}")
