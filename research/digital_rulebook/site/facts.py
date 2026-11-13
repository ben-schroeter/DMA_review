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
_a20 = [x for x in A if yr(x) >= 2020]
put("laws_since_2020", len(_a20))
_o20 = sum(x["restrictions_total"] or 0 for x in _a20) / main; put("obligations_since_2020_pct", round(100 * _o20), f"{100 * _o20:.0f}%")
both = [x for x in A if x["proposal_restrictions_total"] and x["restrictions_total"] is not None]
put("compared_with_proposal", len(both)); put("grew_in_negotiation", sum(x["restrictions_total"] > x["proposal_restrictions_total"] for x in both))
# evidence
L = json.load(open("site/studies_data.json"))["L"]
tags = collections.Counter(t for x in L for t in str(x[-1]).split())
put("studies_evidence", tags["ev"]); put("studies_causal", tags["causal"]); put("studies_review", tags["review"])
put("sources_total", tags["ev"])   # ex-post assessments only (impact assessments are counted on the law pages, not here)
_IA = json.load(open("data/ia/summary.json"))
put("ia_full", _IA["status"].get("full", 0)); put("ia_pre", _IA["status"].get("pre", 0)); put("ia_codification", _IA["status"].get("codification", 0))
put("ia_without", _IA["status"].get("none", 0) + _IA["status"].get("swd", 0)); put("ia_unknown", _IA["status"].get("unknown", 0))
for _k, _lab in (("0314", "2003–2014"), ("1519", "2015–2019"), ("20", "2020 onwards")):
    _n, _f = _IA[_lab]; put(f"ia_without_{_k}", _n - _f); put(f"ia_laws_{_k}", _n)
put("rsb_known", _IA["board_known"]); put("rsb_neg_first", _IA["board_neg_first"]); put("rsb_neg_twice", _IA["board_neg_twice"])
put("studies_econ", tags["econ"]); put("library_total", tags["ev"] + tags["econ"])
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
P_ALL = json.load(open("site/forthcoming_list.json"))
P = [x for x in P_ALL if x["stage"] != "withdrawn"]
put("forthcoming_withdrawn", sum(x["stage"] == "withdrawn" for x in P_ALL))
_ia = collections.Counter(x.get("impact_assessment") for x in P if x.get("impact_assessment"))
put("fc_ia_total", sum(_ia.values())); put("fc_ia_full", _ia["full"]); put("fc_ia_without", _ia["analysis"] + _ia["swd"])
c = collections.Counter(x["stage"] for x in P)
put("forthcoming_total", len(P)); put("forthcoming_agreed", c["agreed"]); put("forthcoming_negotiation", c["proposed"]); put("forthcoming_announced", c["announced"])
# evidence map: laws with after-the-fact evidence / with a causal study, per kind of effect (Evidence page table)
_V = list(json.load(open("data/evidence_map/cells.json"))["instruments"].values())
for _k in ["costs", "consumers", "competition", "innovation", "growth", "market", "rights", "implementation"]:
    put(f"ev_{_k}_n", sum(1 for v in _V if v["cells"][_k]["causal"] + v["cells"][_k]["measured"] > 0)); put(f"ev_{_k}_causal", sum(1 for v in _V if v["cells"][_k]["causal"] > 0))
# database sizes (Data page)
put("db_instruments", len(I)); put("db_secondary_all", len(SEC))
_k = collections.Counter(x["kind"] for x in SEC); put("db_secondary_guidance", _k["guidance"]); put("db_secondary_other", _k["other Commission/Council act"])
put("db_amendments", sum(x["kind"] == "amendment" for x in AM)); put("db_corrigenda", sum(x["kind"] == "corrigendum" for x in AM))
put("db_us_mapped", len(sheet("us_counterparts"))); put("db_us_pairs", sum(1 for x in sheet("us_comparison") if x["row_id"]))
put("db_us_mapped_pending", sum(1 for x in sheet("us_counterparts") if x["row_id"] not in Aid))
put("db_agency_guidance", len(sheet("guidance_agencies")))

# company types and firm size
CT = json.load(open("data/company_types/summary.json"))
for k in ("PR", "FI", "GK", "CL", "TC", "PL"):
    put(f"ct_{k}", CT["types"][k]["obligations"]); put(f"ct_{k}_2018", CT["types"][k]["start_2018"])
put("ct_baseline", CT["baseline"]["obligations"])
PIE = json.load(open("data/company_types/pie.json"))
put("ct_reporting_share", round(100 * PIE["counts"]["reporting"] / PIE["total"]), f"{100 * PIE['counts']['reporting'] / PIE['total']:.0f}%")
REL = json.load(open("data/firm_size/relief.json")); FS = json.load(open("data/firm_size/summary.json"))
put("firm_company_obligations", REL["total"]); put("firm_relief_removed", REL["removed"] + REL["threshold"])
aco = FS["all_company_obligations"]; put("firm_micro_pct", round(100 * aco[0] / aco[4]), f"{100 * aco[0] / aco[4]:.0f}%")
# kinds of rule over time and growth in negotiation
pro = lambda xs: sum(x["r_prohibition"] or 0 for x in xs) / max(1, sum(x["restrictions_total"] or 0 for x in xs))
put("prohib_since_2018", round(100 * pro([x for x in A if yr(x) >= 2018]), 1), f"{100 * pro([x for x in A if yr(x) >= 2018]):.1f}%")
put("prohib_before_2018", round(100 * pro([x for x in A if yr(x) < 2018]), 1), f"{100 * pro([x for x in A if yr(x) < 2018]):.1f}%")
gw = [(x["words_legal_text"] - x["proposal_words_legal_text"]) / x["proposal_words_legal_text"] for x in both if x["proposal_words_legal_text"]]
go = [(x["restrictions_total"] - x["proposal_restrictions_total"]) / x["proposal_restrictions_total"] for x in both]
put("growth_words_median", round(100 * statistics.median(gw)), f"{100 * statistics.median(gw):.0f}%"); put("growth_obligations_median", round(100 * statistics.median(go)), f"{100 * statistics.median(go):.0f}%")
# validation of the classifiers
V = json.load(open("data/validation_results.json"))["addressee_v2_fresh_200"]
put("precision", round(100 * V["precision"]), f"{100 * V['precision']:.0f}%"); put("addressee_accuracy", round(100 * V["addressee_accuracy_v2_rules_plus_model"]), f"{100 * V['addressee_accuracy_v2_rules_plus_model']:.0f}%")

# reporting obligations and other validation figures
REP = json.load(open("data/reporting/summary.json")); RV = REP["validation"] if isinstance(REP["validation"], dict) else json.load(open("data/reporting/validation_results.json"))
put("rep_total", REP["reporting_obligations"]); put("rep_private", REP["by_addressee"]["private_parties"]); put("rep_states", REP["by_addressee"]["member_states"]); put("rep_eu", REP["by_addressee"]["eu_institutions"])
put("rep_precision", round(100 * RV["precision"]), f"{100 * RV['precision']:.0f}%"); put("rep_recall", round(100 * RV["estimated_recall"]), f"{100 * RV['estimated_recall']:.0f}%")
put("rep_estimate_k", RV["estimated_true_total"], k100(RV["estimated_true_total"]))
EM = json.load(open("data/evidence_map/validation.json")); a_, b_ = map(int, EM["combined_before_fixes"].split(" ")[0].split("/"))
put("evmap_check", round(100 * a_ / b_), f"{100 * a_ / b_:.0f}%")
put("us_precision", round(100 * json.load(open("data/us_map/validation_us.json"))["precision"]), f"{100 * json.load(open('data/us_map/validation_us.json'))['precision']:.0f}%")
put("sox_precision", round(100 * json.load(open("data/benchmark_sox.json"))["validation"]["precision"]), f"{100 * json.load(open('data/benchmark_sox.json'))['validation']['precision']:.0f}%")
put("model_clauses_k", sum(1 for _ in open("data/addressee/model_decisions.jsonl")), f"{(sum(1 for _ in open('data/addressee/model_decisions.jsonl')) // 100) * 100:,}")
AR = json.load(open("data/company_types/areas_now.json"))
put("area_finance_k", AR["Finance"], k100(AR["Finance"])); put("area_trust_k", AR["Trust & Safety"], k100(AR["Trust & Safety"]))
byname = {x["name"]: x for x in A}
for key, nm in (("ai", "Artificial Intelligence Act"), ("mica", "Markets in Crypto-Assets (MiCA)"), ("ehds", "European Health Data Space")):
    put(f"ex_{key}_proposal", byname[nm]["proposal_restrictions_total"]); put(f"ex_{key}_adopted", byname[nm]["restrictions_total"])

put("rs_no_duty_main", RS["total_by_code"]["main"]["N"]); put("rs_no_duty_secondary", RS["total_by_code"]["secondary"]["N"])
put("rs_agreement", round(100 * RS["validation"]["rule_vs_standard_like"]), f"{100 * RS['validation']['rule_vs_standard_like']:.0f}%"); put("rs_validation_n", RS["validation"]["n_coded"])
RSF = json.load(open("data/rules_standards/site_figures.json")); pct = lambda v: f"{100 * v:.0f}%"
for k in ("all_main_R", "all_main_standard_like", "comp_main_R", "all_sec_R", "comp_sec_R"):
    put("rs_" + k, round(100 * RSF[k]), pct(RSF[k]))
put("rs_acts_second_layer", RSF["acts_with_second_layer"]); put("rs_acts_more_rules", RSF["acts_more_rules"])
for key, nm in (("ecodesign", "Ecodesign for Sustainable Products Regulation"), ("csa", "Cybersecurity Act"), ("dora", "Digital Operational Resilience Act (DORA)"), ("nis2", "NIS 2 Directive")):
    c = RSF["companies_by_law"][nm]; put(f"rs_{key}_main", round(100 * c["main"]), pct(c["main"])); put(f"rs_{key}_sec", round(100 * c["secondary"]), pct(c["secondary"]))

# regulatory design grid (Coglianese): data/rules_standards/grid/summary.json, written by scripts/grid_aggregate.py
GR = json.load(open("data/rules_standards/grid/summary.json")); _gc = GR["groups"]["companies_main|all"]
for c in ("MM", "ME", "XM", "XE"):
    put("grid_comp_" + c, round(100 * _gc[c]), pct(_gc[c]))
put("grid_comp_open", round(100 * _gc["means_left_open"]), pct(_gc["means_left_open"])); put("grid_comp_n", _gc["n"])
_gs = GR["groups"]["companies_secondary|all"]; put("grid_comp_sec_open", round(100 * _gs["means_left_open"]), pct(_gs["means_left_open"]))
put("grid_no_duty_main", round(100 * GR["not_a_duty"]["main"]), pct(GR["not_a_duty"]["main"]))
put("grid_val_n", GR["validation"]["n"]); put("grid_val_agree", GR["validation"]["agree"]); put("grid_val_kappa", GR["validation"]["kappa"], f'{GR["validation"]["kappa"]:.2f}')
for t, v in GR["company_types"].items():
    put(f"grid_ct_{t}_open", round(100 * v["all"]["means_left_open"]), pct(v["all"]["means_left_open"]))
    put(f"grid_ct_{t}_main_open", round(100 * v["main"]["means_left_open"]), pct(v["main"]["means_left_open"]))
    put(f"grid_ct_{t}_sec_open", round(100 * v["secondary"]["means_left_open"]), pct(v["secondary"]["means_left_open"]))

# external statistics quoted on the site (Why it matters, front page): edited in data/external_figures.json, with page context
for k, v in json.load(open("data/external_figures.json")).items():
    F[k] = {"value": v["text"], "text": v["text"], "external": True}
json.dump(F, open("site/facts.json", "w"), indent=1, ensure_ascii=False)
print(len(F), {k: v["text"] for k, v in F.items()})
