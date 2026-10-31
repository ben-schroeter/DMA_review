"""Rules vs standards (Kaplow 1992): roll the second-reader codes (data/rules_standards/batches/bNN_coded.json) up to obligations,
instruments, policy areas, periods and addressees; check them against the hand-coded validation sample.
Writes data/rules_standards/summary.json and data/rules_standards/per_instrument.csv. Run from research/ceps_metrics."""
import json, glob, collections, csv, statistics, sys, openpyxl
sys.path.insert(0, "data/rules_standards")
codes = {}
for f in sorted(glob.glob("data/rules_standards/batches/b??_coded.json")):
    for o in json.load(open(f)):
        codes[o["k"]] = o["c"]
inst = [json.loads(l) for l in open("data/rules_standards/instances.jsonl")]
wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values); h = rows[0]
I = {str(r[h.index("celex_measured")]): dict(zip(h, r)) for r in rows[1:] if r[0] and r[h.index("status_oct2026")] == "adopted"
     and r[h.index("restrictions_total")] is not None}
parent = {s["celex"]: s["parent"] for s in json.load(open("data/secondary_acts.json"))}
addr_m = [json.loads(l)["formal"] for l in open("data/addressee/v2_final_main.jsonl")]
addr_s = [json.loads(l)["formal"] for l in open("data/addressee/v2_secondary.jsonl")]
COD = ["R", "S", "M", "L", "D"]
std = lambda c: collections.Counter(c)


def shares(cs):
    n = sum(cs[k] for k in COD)
    return {"n": n, **{k: round(cs[k] / n, 3) if n else None for k in COD},
            "standard_like": round((cs["S"] + cs["M"] + cs["L"]) / n, 3) if n else None}


main = collections.defaultdict(collections.Counter); sec = collections.defaultdict(collections.Counter)
area = collections.defaultdict(collections.Counter); per = collections.defaultdict(collections.Counter)
adr = collections.defaultdict(collections.Counter); tot = {"main": collections.Counter(), "secondary": collections.Counter()}
missing = 0
for x in inst:
    c = codes.get(x["key"])
    if c is None:
        missing += 1; continue
    tot[x["src"]][c] += 1
    if c == "N":
        continue
    if x["src"] == "main":
        r = I[x["doc"]]; main[x["doc"]][c] += 1
        area[r["policy_area_ceps"]][c] += 1
        per["2020 or later" if r["adoption_date"].year >= 2020 else "before 2020"][c] += 1
        adr[addr_m[x["rid"]]][c] += 1
    else:
        p = parent.get(x["doc"])
        if p in I:
            sec[p][c] += 1
LAB = lambda s: "rule-based" if s["R"] >= 0.65 else ("standards-based" if s["standard_like"] >= 0.5 else "mixed")
out = []
for d, r in I.items():
    if not main[d]:
        continue
    sm = shares(main[d]); ss = shares(sec[d]) if sec[d] else None
    out.append({"row_id": r["row_id"], "name": r["name"], "area": r["policy_area_ceps"], "year": r["adoption_date"].year,
                "main": sm, "label": LAB(sm), "secondary": ss})
out.sort(key=lambda o: -(o["main"]["standard_like"] or 0))
summary = {"total_by_code": {k: dict(v) for k, v in tot.items()}, "missing": missing,
           "main_all": shares(sum(main.values(), collections.Counter())), "secondary_all": shares(sum(sec.values(), collections.Counter())),
           "by_area": {a: shares(c) for a, c in area.items()}, "by_period": {a: shares(c) for a, c in per.items()},
           "by_addressee": {a: shares(c) for a, c in adr.items()},
           "labels": dict(collections.Counter(o["label"] for o in out)), "instruments": out}
# validation against the hand codes (fresh sample) and the pilot
from validation_codes import CODES as VC
V = json.load(open("data/rules_standards/validation_sample.json"))
coll = lambda c: {"M": "S", "L": "S"}.get(c, c)
pairs = [(VC[v["n"]], codes.get(v["k"])) for v in V if codes.get(v["k"])]
keep = [(a, b) for a, b in pairs if a != "N" and b != "N"]
summary["validation"] = {"n_coded": len(pairs), "n_compared": len(keep), "exact": round(sum(a == b for a, b in keep) / max(1, len(keep)), 3),
                         "rule_vs_standard_like": round(sum(coll(a) == coll(b) for a, b in keep) / max(1, len(keep)), 3),
                         "confusion": {f"{a}->{b}": n for (a, b), n in collections.Counter(pairs).items()}}
json.dump(summary, open("data/rules_standards/summary.json", "w"), indent=1, default=str)
with open("data/rules_standards/per_instrument.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["row_id", "name", "area", "year", "n_main", "rule", "standard", "mixed", "specified_later", "member_states",
                                   "standard_like", "label", "n_secondary", "secondary_rule", "secondary_standard_like"])
    for o in out:
        m, s = o["main"], o["secondary"] or {}
        w.writerow([o["row_id"], o["name"], o["area"], o["year"], m["n"], m["R"], m["S"], m["M"], m["L"], m["D"], m["standard_like"], o["label"],
                    s.get("n", 0), s.get("R"), s.get("standard_like")])
print(json.dumps({k: v for k, v in summary.items() if k != "instruments"}, indent=1, default=str)[:3500])
