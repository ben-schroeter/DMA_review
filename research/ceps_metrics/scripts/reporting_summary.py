"""Summary of reporting obligations (from scripts/reporting.py) for adopted acts and their implementing and delegated acts.
Writes data/reporting/summary.json. Run from research/ceps_metrics."""
import collections, json
import openpyxl

wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)


def sheet(n):
    rows = list(wb[n].values); h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r[0] is not None]


I, S = sheet("instruments"), sheet("secondary_acts")
main = {r["celex_measured"]: r for r in I if r["celex_measured"] and r["status_oct2026"] == "adopted" and r["adoption_date"] and r["restrictions_total"] is not None}
sec = {r["celex"]: r for r in S if r["kind"] in ("implementing", "delegated") and r["date"] and r["restrictions_total"] is not None}
by_id = {r["row_id"]: r for r in I}
rows = [json.loads(l) for l in open("data/reporting/reporting_instances.jsonl")]
scope = [r for r in rows if (r["kind"] == "main" and r["doc"] in main) or (r["kind"] == "secondary" and r["doc"] in sec)]
rep = [r for r in scope if r["reporting"]]
inst = lambda r: main[r["doc"]] if r["kind"] == "main" else by_id[sec[r["doc"]]["parent_row_id"]]
year = lambda r: int(str(main[r["doc"]]["adoption_date"])[:4]) if r["kind"] == "main" else int(str(sec[r["doc"]]["date"])[:4])
cnt = lambda xs, f: dict(collections.Counter(f(x) for x in xs).most_common())

out = {"obligations_in_scope": len(scope), "reporting_obligations": len(rep),
       "share_of_obligations": round(len(rep) / len(scope), 4),
       "in_laws": sum(r["kind"] == "main" for r in rep), "in_implementing_delegated": sum(r["kind"] == "secondary" for r in rep),
       "by_addressee": cnt(rep, lambda r: r["addressee"]), "review_reports_eu": sum(r["review"] for r in rep), "by_who": {}}
for a in ("private_parties", "member_states", "eu_institutions"):
    xs = [r for r in rep if r["addressee"] == a]
    out["by_who"][a] = {"total": len(xs), "type": cnt(xs, lambda r: r["type"]), "cadence": cnt(xs, lambda r: r["cadence"]),
                        "period": cnt([x for x in xs if x["cadence"] == "periodic"], lambda r: r["period"]),
                        "recipient": cnt(xs, lambda r: r["recipient"]),
                        "deadline_hours": cnt([x for x in xs if x["deadline_hours"]], lambda r: r["deadline_hours"]),
                        "without_delay": sum(1 for x in xs if x["period"] == "without delay"),
                        "start_2018": sum(1 for x in xs if year(x) <= 2017),
                        "by_year": dict(sorted(collections.Counter(year(x) for x in xs).items())),
                        "by_policy_area": cnt(xs, lambda r: inst(r)["policy_area_ceps"]),
                        "top_instruments": dict(collections.Counter(inst(x)["name"] for x in xs).most_common(15))}
out["start_2018_all"] = sum(1 for r in rep if year(r) <= 2017)
out["by_year_all"] = dict(sorted(collections.Counter(year(r) for r in rep).items()))
out["top_instruments_all"] = dict(collections.Counter(inst(r)["name"] for r in rep).most_common(15))
out["validation"] = json.load(open("data/reporting/validation_results.json"))
json.dump(out, open("data/reporting/summary.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in out.items() if k not in ("by_who", "by_year_all")}, indent=1)[:1500])
for a, v in out["by_who"].items():
    print(a, v["total"], v["type"], v["cadence"])
