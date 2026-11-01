"""Headline figures for the site, computed from the database (digital_rulebook.xlsx) and the derived data files.
Writes site/facts.json: {key: {"value": number, "text": as shown on the site}}. site/assemble.py puts these into every
page wherever a figure is marked with <span data-fact="key">. Run from research/digital_rulebook."""
import json, collections, statistics, openpyxl

wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
def sheet(n):
    r = list(wb[n].iter_rows(values_only=True)); return [dict(zip(r[0], x)) for x in r[1:] if any(v is not None for v in x)]
I = [x for x in sheet("instruments") if x["row_id"]]
A = [x for x in I if x["status"] == "adopted"]; Aid = {x["row_id"] for x in A}
SEC = sheet("secondary_acts"); AM = sheet("amendments"); PI = sheet("proposal_indicators"); LIT = sheet("impact_literature")
s = lambda xs, k: sum(x[k] or 0 for x in xs)
F = {}
def put(k, v, text=None):
    F[k] = {"value": v, "text": text if text is not None else (f"{v:,}" if isinstance(v, int) else str(v))}
k100 = lambda v: f"{round(v, -2):,.0f}"
put("laws_adopted", len(A))
main = s(A, "restrictions_total"); put("obligations_main", main); put("obligations_main_k", main, k100(main))
put("words_m", s(A, "words_legal_text"), f"{s(A, 'words_legal_text') / 1e6:.1f}")
impl = [x for x in SEC if x["parent_row_id"] in Aid and x["kind"] in ("implementing", "delegated")]
put("secondary_acts", len(impl)); put("implementing_acts", sum(x["kind"] == "implementing" for x in impl)); put("delegated_acts", sum(x["kind"] == "delegated" for x in impl))
sec_obl = s(impl, "restrictions_total"); put("obligations_secondary", sec_obl); put("obligations_secondary_k", sec_obl, k100(sec_obl))
put("amending_acts", sum(1 for x in AM if x["parent_row_id"] in Aid and x["kind"] == "amendment"))
put("national_measures", s(A, "national_transposition_measures"))
pm = s(A, "addr_private_parties"); ps = s(impl, "addr_private_parties")
put("private_main", pm); put("private_secondary", ps); put("private_total", pm + ps); put("private_total_k", pm + ps, k100(pm + ps))
yr = lambda x: int(str(x["adoption_date"])[:4])
put("obligations_since_2018", sum(x["restrictions_total"] or 0 for x in A if yr(x) >= 2018))
both = [x for x in A if x["proposal_restrictions_total"] and x["restrictions_total"] is not None]
put("compared_with_proposal", len(both)); put("grew_in_negotiation", sum(x["restrictions_total"] > x["proposal_restrictions_total"] for x in both))
# evidence
L = json.load(open("site/studies_data.json"))["L"]
tags = collections.Counter(t for x in L for t in str(x[-1]).split())
put("studies_evidence", tags["ev"]); put("studies_causal", tags["causal"]); put("impact_assessments", tags["ia"]); put("studies_review", tags["review"])
put("sources_total", tags["ev"] + tags["ia"])
krs = [p for p in PI if p["indicator / promised impact"] and p["parent_row_id"] in Aid]
sg = collections.Counter(p["status_group"] for p in krs)
put("objectives", len(krs))
for k, key in (("measured", "obj_measured"), ("partially measured", "obj_partly"), ("mixed evidence", "obj_mixed"), ("reported as activity", "obj_activity"), ("not measured", "obj_never")):
    put(key, sg[k])
put("obj_never_pct", round(100 * sg["not measured"] / len(krs)), f"{100 * sg['not measured'] / len(krs):.0f}%")
ev = [x for x in LIT if (x["category"] or "evidence") == "evidence" and x["parent_row_id"] in Aid]
sc = collections.Counter(x["source_class"] for x in ev)
for k, key in (("official", "src_official"), ("academic", "src_academic"), ("think tank", "src_thinktank"), ("consultancy or industry", "src_industry"), ("other", "src_other")):
    put(key, sc[k])
lv = collections.Counter(x["impact_evidence_level"] for x in A)
for k, key in (("strong", "lvl_strong"), ("moderate", "lvl_moderate"), ("thin", "lvl_thin"), ("ex-ante only", "lvl_too_early"), ("none", "lvl_none")):
    put(key, lv[k])
# rules and standards base
RS = json.load(open("data/rules_standards/summary.json"))
put("rs_main_n", RS["main_all"]["n"]); put("rs_secondary_n", RS["secondary_all"]["n"])
put("rs_total_k", RS["main_all"]["n"] + RS["secondary_all"]["n"], k100(RS["main_all"]["n"] + RS["secondary_all"]["n"]))
# pending initiatives
P = json.load(open("site/forthcoming_list.json"))
c = collections.Counter(x["stage"] for x in P)
put("forthcoming_total", len(P)); put("forthcoming_agreed", c["agreed"]); put("forthcoming_negotiation", c["proposed"]); put("forthcoming_announced", c["announced"])
json.dump(F, open("site/facts.json", "w"), indent=1, ensure_ascii=False)
print(len(F), {k: v["text"] for k, v in F.items()})
